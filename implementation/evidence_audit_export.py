"""Deterministic end-to-end evidence audit export.

Joins an inert sealed sampling schedule, receipt audit state, durable archive
membership and HOLD-only replay provenance. No network, credentials, publication,
task acceptance, wallet or settlement action is performed.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from archive_replay import archive_replay_report
from evidence_archive import EvidenceArchive
from sampling_audit import sampling_audit_summary


def _archive_by_bundle(archive: EvidenceArchive) -> dict[str, Any]:
    return {entry.bundle_sha256: entry for entry in archive.entries}


def _replay_by_bundle(replay: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        row["bundle_sha256"]: row
        for row in replay.get("platforms", [])
        if isinstance(row, Mapping) and isinstance(row.get("bundle_sha256"), str)
    }


def _gap_reasons(row: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    state = row["receipt_state"]
    if state == "scheduled_but_uncaptured":
        reasons.append("production_capture_missing")
    elif state == "receipt_invalid":
        reasons.append("valid_capture_receipt_missing")
    elif state == "receipt_valid_non_production":
        reasons.append("production_receipt_missing")

    if state == "receipt_valid_production":
        if not row["archive_member"]:
            reasons.append("production_capture_not_in_durable_archive")
        elif not row["replay_member"]:
            reasons.append("archived_capture_not_latest_production_replay")
        else:
            if row["replay_freshness_state"] != "fresh":
                reasons.append(f"replay_evidence_{row['replay_freshness_state']}")
            if not row["replay_receipt_provenance_verified"]:
                reasons.append("replay_receipt_provenance_missing")
    return reasons


def evidence_audit_export(
    manifest_envelope: Mapping[str, Any],
    receipts: Iterable[Mapping[str, Any]],
    archive: EvidenceArchive,
    *,
    receipt_capture_reports: Iterable[Mapping[str, Any]] = (),
    now: datetime | None = None,
    max_age_hours: float = 24.0,
) -> dict[str, Any]:
    """Join schedule -> receipt -> archive -> replay into one deterministic audit.

    Missing/invalid/non-production evidence remains an explicit unresolved
    production gap. Archive and replay evidence are informational only and can
    never authorize execution.
    """
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    receipt_audit = sampling_audit_summary(manifest_envelope, receipts)
    replay = archive_replay_report(
        archive,
        now=current,
        max_age_hours=max_age_hours,
        receipt_capture_reports=receipt_capture_reports,
    )
    archive_index = _archive_by_bundle(archive)
    replay_index = _replay_by_bundle(replay)

    rows: list[dict[str, Any]] = []
    for item in receipt_audit["items"]:
        bundle_sha = item.get("sanitized_bundle_sha256")
        archive_entry = archive_index.get(bundle_sha) if bundle_sha else None
        replay_row = replay_index.get(bundle_sha) if bundle_sha else None
        row = {
            "item_index": item["item_index"],
            "platform": item["platform"],
            "source_url": item["source_url"],
            "manifest_sha256": item["manifest_sha256"],
            "manifest_item_sha256": item["manifest_item_sha256"],
            "receipt_state": item["state"],
            "receipt_sha256": item.get("receipt_sha256"),
            "captured_environment": item.get("captured_environment"),
            "sanitized_bundle_sha256": bundle_sha,
            "archive_member": archive_entry is not None,
            "archive_sequence": archive_entry.sequence if archive_entry else None,
            "archive_environment": archive_entry.environment if archive_entry else None,
            "replay_member": replay_row is not None,
            "replay_freshness_state": replay_row.get("freshness_state") if replay_row else None,
            "replay_receipt_provenance_verified": (
                bool(replay_row.get("receipt_provenance_verified")) if replay_row else False
            ),
            "demand_state": replay_row.get("demand_state") if replay_row else None,
            "open_item_count": replay_row.get("open_item_count") if replay_row else None,
            "paid_utilization_state": (
                replay_row.get("paid_utilization_state") if replay_row else None
            ),
            "paid_transaction_count": (
                replay_row.get("paid_transaction_count") if replay_row else None
            ),
            "paid_value_usd": replay_row.get("paid_value_usd") if replay_row else None,
        }
        row["unresolved_production_gaps"] = _gap_reasons(row)
        row["production_evidence_complete"] = not row["unresolved_production_gaps"]
        row["action_enabled"] = False
        rows.append(row)

    rows.sort(key=lambda row: (row["platform"] or "", row["source_url"] or "", row["item_index"]))

    source_gaps = [
        {
            "platform": row["platform"],
            "source_url": row["source_url"],
            "item_index": row["item_index"],
            "gaps": list(row["unresolved_production_gaps"]),
        }
        for row in rows
        if row["unresolved_production_gaps"]
    ]

    platform_summary: list[dict[str, Any]] = []
    for platform in sorted({row["platform"] for row in rows if row["platform"]}):
        platform_rows = [row for row in rows if row["platform"] == platform]
        unresolved = sorted(
            {
                gap
                for row in platform_rows
                for gap in row["unresolved_production_gaps"]
            }
        )
        platform_summary.append({
            "platform": platform,
            "scheduled_source_count": len(platform_rows),
            "production_complete_source_count": sum(
                row["production_evidence_complete"] for row in platform_rows
            ),
            "unresolved_source_count": sum(
                not row["production_evidence_complete"] for row in platform_rows
            ),
            "unresolved_gap_types": unresolved,
        })

    return {
        "schema_version": 1,
        "generated_at": current.isoformat(),
        "manifest_sha256": receipt_audit["manifest_sha256"],
        "scheduled_source_count": len(rows),
        "production_complete_source_count": sum(
            row["production_evidence_complete"] for row in rows
        ),
        "unresolved_production_source_count": len(source_gaps),
        "receipt_invalid_source_count": receipt_audit["receipt_invalid_count"],
        "receipt_valid_non_production_source_count": receipt_audit[
            "receipt_valid_non_production_count"
        ],
        "receipt_valid_production_source_count": receipt_audit[
            "receipt_valid_production_count"
        ],
        "archive_membership_count": sum(row["archive_member"] for row in rows),
        "replay_membership_count": sum(row["replay_member"] for row in rows),
        "verified_replay_provenance_count": sum(
            row["replay_receipt_provenance_verified"] for row in rows
        ),
        "platforms": platform_summary,
        "sources": rows,
        "unresolved_production_gaps": source_gaps,
        "missing_capture_is_not_zero_demand": True,
        "non_production_can_close_production_gap": False,
        "archive_or_receipt_can_authorize_action": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }
