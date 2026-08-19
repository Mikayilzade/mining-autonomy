"""Deterministic sanitized evidence archive with explicit environment isolation.

Consumes already-produced read-only capture reports. No network/auth/payment actions.
Only normalized observation metadata is persisted; raw platform payloads and buyer
identities are excluded. Only explicit ``production`` observations may enter the
production scorecard; ``testnet`` and ``unknown`` fail closed from production claims.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib
import json
from typing import Any, Mapping

SCHEMA_VERSION = 1
ENVIRONMENTS = frozenset({"production", "testnet", "unknown"})
DEMAND_STATES = frozenset({"positive_open_demand", "zero_open_observation", "unproven"})
UTILIZATION_STATES = frozenset({"positive_paid_utilization", "unproven"})
_HEX = frozenset("0123456789abcdef")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _require_mapping(value: Any, error: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(error)
    return value


def _require_sha(value: Any, error: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(error)
    lowered = value.lower()
    if any(char not in _HEX for char in lowered):
        raise ValueError(error)
    return lowered


def _require_timestamp(value: Any, error: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None:
        raise ValueError(error)
    return parsed.isoformat()


def _require_environment(value: Any) -> str:
    if value not in ENVIRONMENTS:
        raise ValueError("archive_environment_invalid")
    return str(value)


@dataclass(frozen=True)
class ArchiveEntry:
    sequence: int
    environment: str
    platform: str
    source_url: str
    source_timestamp: str
    captured_at: str
    bundle_sha256: str
    request_snapshot_sha256: str
    demand_state: str
    open_item_count: int
    paid_utilization_state: str
    paid_transaction_count: int | None
    paid_value_usd: float | None
    source_report_sha256: str
    previous_entry_sha256: str | None
    entry_sha256: str


@dataclass(frozen=True)
class EvidenceArchive:
    entries: tuple[ArchiveEntry, ...] = ()


def _entry_core(entry: ArchiveEntry | Mapping[str, Any]) -> dict[str, Any]:
    raw = asdict(entry) if isinstance(entry, ArchiveEntry) else dict(entry)
    raw.pop("entry_sha256", None)
    return raw


def _validated_delta(delta: Any) -> dict[str, Any]:
    value = _require_mapping(delta, "capture_delta_must_be_object")
    platform = value.get("platform")
    if not isinstance(platform, str) or not platform:
        raise ValueError("capture_delta_platform_required")
    source_url = value.get("source_url")
    if not isinstance(source_url, str) or not source_url.startswith("https://"):
        raise ValueError("capture_delta_source_must_use_https")
    demand_state = value.get("demand_state")
    if demand_state not in DEMAND_STATES:
        raise ValueError("capture_delta_demand_state_invalid")
    open_count = value.get("open_item_count")
    if not isinstance(open_count, int) or isinstance(open_count, bool) or open_count < 0:
        raise ValueError("capture_delta_open_item_count_invalid")
    utilization_state = value.get("paid_utilization_state")
    if utilization_state not in UTILIZATION_STATES:
        raise ValueError("capture_delta_paid_utilization_state_invalid")
    tx_count = value.get("paid_transaction_count")
    paid_value = value.get("paid_value_usd")
    if utilization_state == "positive_paid_utilization":
        if not isinstance(tx_count, int) or isinstance(tx_count, bool) or tx_count <= 0:
            raise ValueError("capture_delta_paid_transaction_count_invalid")
        if not isinstance(paid_value, (int, float)) or isinstance(paid_value, bool) or paid_value < 0:
            raise ValueError("capture_delta_paid_value_invalid")
        normalized_paid_value: float | None = float(paid_value)
    else:
        if tx_count is not None or paid_value is not None:
            raise ValueError("capture_delta_unproven_utilization_must_not_have_values")
        normalized_paid_value = None
    return {
        "platform": platform,
        "source_url": source_url,
        "source_timestamp": _require_timestamp(value.get("source_timestamp"), "capture_delta_source_timestamp_invalid"),
        "captured_at": _require_timestamp(value.get("captured_at"), "capture_delta_captured_at_invalid"),
        "bundle_sha256": _require_sha(value.get("bundle_sha256"), "capture_delta_bundle_sha256_invalid"),
        "request_snapshot_sha256": _require_sha(value.get("request_snapshot_sha256"), "capture_delta_request_snapshot_sha256_invalid"),
        "demand_state": demand_state,
        "open_item_count": open_count,
        "paid_utilization_state": utilization_state,
        "paid_transaction_count": tx_count,
        "paid_value_usd": normalized_paid_value,
    }


def validate_capture_report(report: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    value = dict(_require_mapping(report, "capture_report_must_be_object"))
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("capture_report_schema_version_unsupported")
    if value.get("dry_run_only") is not True or value.get("action_enabled") is not False:
        raise ValueError("capture_report_must_be_dry_run_action_disabled")
    deltas = value.get("deltas")
    if not isinstance(deltas, list):
        raise ValueError("capture_report_deltas_must_be_list")
    registry = _require_mapping(value.get("registry"), "capture_report_registry_required")
    if registry.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("capture_report_registry_schema_version_unsupported")
    hashes = registry.get("bundle_hashes")
    if not isinstance(hashes, list):
        raise ValueError("capture_report_registry_hashes_required")
    registry_hashes = {_require_sha(item, "capture_report_registry_hash_invalid") for item in hashes}
    normalized = [_validated_delta(delta) for delta in deltas]
    for delta in normalized:
        if delta["bundle_sha256"] not in registry_hashes:
            raise ValueError("capture_delta_bundle_missing_from_registry")
    return value, normalized


def append_capture_report(archive: EvidenceArchive, report: Any, *, environment_by_bundle_sha256: Mapping[str, str] | None = None, default_environment: str = "unknown") -> EvidenceArchive:
    default_env = _require_environment(default_environment)
    raw_report, deltas = validate_capture_report(report)
    report_sha = _sha256(raw_report)
    mapping = dict(environment_by_bundle_sha256 or {})
    existing_hashes = {entry.bundle_sha256 for entry in archive.entries}
    entries = list(archive.entries)
    previous = entries[-1].entry_sha256 if entries else None
    for delta in deltas:
        bundle_sha = delta["bundle_sha256"]
        if bundle_sha in existing_hashes:
            raise ValueError("archive_duplicate_bundle_hash")
        environment = _require_environment(mapping.get(bundle_sha, default_env))
        core = {
            "sequence": len(entries) + 1,
            "environment": environment,
            **delta,
            "source_report_sha256": report_sha,
            "previous_entry_sha256": previous,
        }
        entry_sha = _sha256(core)
        entry = ArchiveEntry(**core, entry_sha256=entry_sha)
        entries.append(entry)
        existing_hashes.add(bundle_sha)
        previous = entry_sha
    return EvidenceArchive(tuple(entries))


def archive_record(archive: EvidenceArchive) -> dict[str, Any]:
    entries = [asdict(entry) for entry in archive.entries]
    core = {
        "schema_version": SCHEMA_VERSION,
        "entry_count": len(entries),
        "entries": entries,
        "environment_policy": "explicit_only",
        "production_scorecard_filter": "environment_equals_production",
        "append_only": True,
        "raw_payloads_persisted": False,
        "dry_run_only": True,
        "action_enabled": False,
    }
    return {**core, "archive_sha256": _sha256(core)}


def serialize_archive(archive: EvidenceArchive) -> str:
    return _canonical_json(archive_record(archive))


def parse_archive(document: str | Mapping[str, Any]) -> EvidenceArchive:
    if isinstance(document, str):
        try:
            parsed = json.loads(document)
        except json.JSONDecodeError as exc:
            raise ValueError("archive_json_invalid") from exc
    else:
        parsed = dict(_require_mapping(document, "archive_document_must_be_object"))
    value = dict(_require_mapping(parsed, "archive_document_must_be_object"))
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("archive_schema_version_unsupported")
    if value.get("dry_run_only") is not True or value.get("action_enabled") is not False:
        raise ValueError("archive_must_be_dry_run_action_disabled")
    if value.get("environment_policy") != "explicit_only" or value.get("production_scorecard_filter") != "environment_equals_production":
        raise ValueError("archive_environment_policy_invalid")
    if value.get("append_only") is not True or value.get("raw_payloads_persisted") is not False:
        raise ValueError("archive_integrity_policy_invalid")
    supplied_archive_sha = _require_sha(value.pop("archive_sha256", None), "archive_sha256_invalid")
    if _sha256(value) != supplied_archive_sha:
        raise ValueError("archive_sha256_mismatch")
    raw_entries = value.get("entries")
    if not isinstance(raw_entries, list) or value.get("entry_count") != len(raw_entries):
        raise ValueError("archive_entry_count_mismatch")

    entries: list[ArchiveEntry] = []
    prior_hash: str | None = None
    seen: set[str] = set()
    for position, raw in enumerate(raw_entries, start=1):
        item = dict(_require_mapping(raw, "archive_entry_must_be_object"))
        if item.get("sequence") != position:
            raise ValueError("archive_sequence_invalid")
        item["environment"] = _require_environment(item.get("environment"))
        if not isinstance(item.get("platform"), str) or not item["platform"]:
            raise ValueError("archive_platform_required")
        if not isinstance(item.get("source_url"), str) or not item["source_url"].startswith("https://"):
            raise ValueError("archive_source_must_use_https")
        item["source_timestamp"] = _require_timestamp(item.get("source_timestamp"), "archive_source_timestamp_invalid")
        item["captured_at"] = _require_timestamp(item.get("captured_at"), "archive_captured_at_invalid")
        item["bundle_sha256"] = _require_sha(item.get("bundle_sha256"), "archive_bundle_sha256_invalid")
        item["request_snapshot_sha256"] = _require_sha(item.get("request_snapshot_sha256"), "archive_request_snapshot_sha256_invalid")
        item["source_report_sha256"] = _require_sha(item.get("source_report_sha256"), "archive_source_report_sha256_invalid")
        if item["bundle_sha256"] in seen:
            raise ValueError("archive_duplicate_bundle_hash")
        seen.add(item["bundle_sha256"])
        if item.get("demand_state") not in DEMAND_STATES:
            raise ValueError("archive_demand_state_invalid")
        if item.get("paid_utilization_state") not in UTILIZATION_STATES:
            raise ValueError("archive_paid_utilization_state_invalid")
        if item.get("previous_entry_sha256") != prior_hash:
            raise ValueError("archive_hash_chain_broken")
        supplied_entry_sha = _require_sha(item.get("entry_sha256"), "archive_entry_sha256_invalid")
        if _sha256(_entry_core(item)) != supplied_entry_sha:
            raise ValueError("archive_entry_sha256_mismatch")
        entry = ArchiveEntry(**item)
        entries.append(entry)
        prior_hash = entry.entry_sha256
    return EvidenceArchive(tuple(entries))


def require_append_only(base: EvidenceArchive, candidate: EvidenceArchive) -> None:
    if len(candidate.entries) < len(base.entries):
        raise ValueError("archive_append_only_truncation")
    for index, existing in enumerate(base.entries):
        if candidate.entries[index] != existing:
            raise ValueError("archive_append_only_rewrite")


def production_scorecard(archive: EvidenceArchive) -> dict[str, Any]:
    production = [entry for entry in archive.entries if entry.environment == "production"]
    grouped: dict[str, list[ArchiveEntry]] = {}
    for entry in production:
        grouped.setdefault(entry.platform, []).append(entry)
    platforms: list[dict[str, Any]] = []
    for platform in sorted(grouped):
        entries = grouped[platform]
        latest = max(entries, key=lambda item: (item.source_timestamp, item.entry_sha256))
        paid = [item for item in entries if item.paid_utilization_state == "positive_paid_utilization"]
        positive = [item for item in entries if item.demand_state == "positive_open_demand"]
        zero = [item for item in entries if item.demand_state == "zero_open_observation"]
        if paid:
            status = "confirmed_paid_utilization_observed"
        elif latest.demand_state == "positive_open_demand":
            status = "positive_open_demand_observed_latest"
        elif latest.demand_state == "zero_open_observation":
            status = "zero_open_observed_latest"
        elif positive:
            status = "historical_open_demand_only"
        else:
            status = "demand_unproven"
        latest_paid = max(paid, key=lambda item: (item.source_timestamp, item.entry_sha256)) if paid else None
        platforms.append({
            "platform": platform,
            "production_observation_count": len(entries),
            "distinct_request_snapshot_count": len({item.request_snapshot_sha256 for item in entries}),
            "latest_source_timestamp": latest.source_timestamp,
            "latest_demand_state": latest.demand_state,
            "latest_open_item_count": latest.open_item_count,
            "positive_open_observation_count": len(positive),
            "zero_open_observation_count": len(zero),
            "paid_utilization_observation_count": len(paid),
            "evidence_status": status,
            "latest_paid_transaction_count": latest_paid.paid_transaction_count if latest_paid else None,
            "latest_paid_value_usd": latest_paid.paid_value_usd if latest_paid else None,
            "paid_value_aggregation": "none_across_snapshots",
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "environment": "production",
        "platform_count": len(platforms),
        "production_observation_count": len(production),
        "excluded_testnet_observation_count": sum(entry.environment == "testnet" for entry in archive.entries),
        "excluded_unknown_observation_count": sum(entry.environment == "unknown" for entry in archive.entries),
        "platforms": platforms,
        "cross_snapshot_paid_value_sum_usd": None,
        "cross_snapshot_extrapolation": False,
        "dry_run_only": True,
        "action_enabled": False,
    }
