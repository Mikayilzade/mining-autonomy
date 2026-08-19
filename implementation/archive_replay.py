"""Environment-aware replay bridge for sanitized evidence archives.

This module intentionally converts archive evidence into HOLD-only orchestrator items.
Archive metadata can inform prioritization and reporting, but cannot authorize task
execution because raw task payloads, trusted policy evidence, and cost estimates are
not present in the sanitized archive.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from evidence_archive import ArchiveEntry, EvidenceArchive
from orchestrator import ObservationItem, rank_observations
from sampling_audit import receipt_provenance_index


@dataclass(frozen=True)
class EvidenceFreshness:
    source_timestamp: str
    age_hours: float
    state: str


def _aware(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("archive_replay_timestamp_must_be_timezone_aware")
    return parsed.astimezone(timezone.utc)


def evidence_freshness(source_timestamp: str, *, now: datetime | None = None,
                       max_age_hours: float = 24.0,
                       max_future_skew_minutes: float = 5.0) -> EvidenceFreshness:
    if max_age_hours <= 0 or max_future_skew_minutes < 0:
        raise ValueError("archive_replay_freshness_bounds_invalid")
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    source = _aware(source_timestamp)
    age_hours = (current - source).total_seconds() / 3600.0
    if age_hours < -(max_future_skew_minutes / 60.0):
        state = "future_invalid"
    elif age_hours <= max_age_hours:
        state = "fresh"
    else:
        state = "stale"
    return EvidenceFreshness(source.isoformat(), round(age_hours, 6), state)


def _latest_production_entries(archive: EvidenceArchive) -> list[ArchiveEntry]:
    grouped: dict[str, list[ArchiveEntry]] = {}
    for entry in archive.entries:
        if entry.environment == "production":
            grouped.setdefault(entry.platform, []).append(entry)
    return [
        max(grouped[platform], key=lambda item: (item.source_timestamp, item.entry_sha256))
        for platform in sorted(grouped)
    ]


def _evidence_class(entry: ArchiveEntry) -> str:
    if entry.paid_utilization_state == "positive_paid_utilization":
        return "settled_receipt"
    if entry.demand_state == "positive_open_demand":
        return "open_paid_request"
    if entry.demand_state == "zero_open_observation":
        return "exact_zero_open"
    return "unknown"


def _receipt_provenance(reports: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    combined: dict[str, dict[str, Any]] = {}
    for report in reports:
        current = receipt_provenance_index(report)
        for bundle_sha, provenance in current.items():
            existing = combined.get(bundle_sha)
            if existing is not None and existing != provenance:
                raise ValueError("archive_replay_conflicting_receipt_provenance")
            combined[bundle_sha] = provenance
    return combined


def archive_observation_items(archive: EvidenceArchive, *, now: datetime | None = None,
                              max_age_hours: float = 24.0) -> list[ObservationItem]:
    """Replay latest production evidence into the unified queue as non-actionable HOLDs."""
    items: list[ObservationItem] = []
    for entry in _latest_production_entries(archive):
        freshness = evidence_freshness(entry.source_timestamp, now=now, max_age_hours=max_age_hours)
        reasons = ["archive_evidence_only_no_raw_payload"]
        if freshness.state != "fresh":
            reasons.append(f"evidence_{freshness.state}")
        items.append(ObservationItem(
            source_type="archived_evidence", platform=entry.platform, external_id=entry.bundle_sha256,
            state="hold", expected_monthly_value_usd=None, expected_margin_usd=None,
            reasons=tuple(reasons), demand_evidence_class=_evidence_class(entry),
            evidence_strength=4 if entry.paid_utilization_state == "positive_paid_utilization" else (3 if entry.demand_state == "positive_open_demand" else 2),
            paid_utilization_proven=entry.paid_utilization_state == "positive_paid_utilization",
            open_paid_demand_proven=entry.demand_state == "positive_open_demand",
            dry_run_only=True, action_enabled=False,
        ))
    return rank_observations(items)


def archive_replay_report(archive: EvidenceArchive, *, now: datetime | None = None,
                          max_age_hours: float = 24.0,
                          receipt_capture_reports: Iterable[Mapping[str, Any]] = ()) -> dict[str, Any]:
    """Build a HOLD-only replay audit report with optional verified receipt provenance."""
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    latest = _latest_production_entries(archive)
    provenance = _receipt_provenance(receipt_capture_reports)
    rows: list[dict[str, Any]] = []
    for entry in latest:
        fresh = evidence_freshness(entry.source_timestamp, now=current, max_age_hours=max_age_hours)
        receipt_ref = provenance.get(entry.bundle_sha256)
        rows.append({
            "platform": entry.platform, "bundle_sha256": entry.bundle_sha256,
            "source_timestamp": fresh.source_timestamp, "age_hours": fresh.age_hours,
            "freshness_state": fresh.state, "demand_state": entry.demand_state,
            "open_item_count": entry.open_item_count,
            "paid_utilization_state": entry.paid_utilization_state,
            "paid_transaction_count": entry.paid_transaction_count,
            "paid_value_usd": entry.paid_value_usd,
            "source_report_sha256": entry.source_report_sha256,
            "receipt_provenance": receipt_ref,
            "receipt_provenance_verified": receipt_ref is not None,
            "orchestrator_state": "hold", "action_enabled": False,
        })
    return {
        "generated_at": current.isoformat(), "environment": "production",
        "max_age_hours": max_age_hours, "production_platform_count": len(rows),
        "fresh_platform_count": sum(row["freshness_state"] == "fresh" for row in rows),
        "stale_platform_count": sum(row["freshness_state"] == "stale" for row in rows),
        "future_invalid_platform_count": sum(row["freshness_state"] == "future_invalid" for row in rows),
        "receipt_provenance_verified_platform_count": sum(row["receipt_provenance_verified"] for row in rows),
        "receipt_provenance_missing_platform_count": sum(not row["receipt_provenance_verified"] for row in rows),
        "excluded_testnet_observation_count": sum(entry.environment == "testnet" for entry in archive.entries),
        "excluded_unknown_observation_count": sum(entry.environment == "unknown" for entry in archive.entries),
        "platforms": rows, "archive_evidence_can_authorize_action": False,
        "receipt_provenance_can_authorize_action": False,
        "cross_snapshot_paid_value_sum_usd": None, "cross_snapshot_extrapolation": False,
        "dry_run_only": True, "action_enabled": False,
    }
