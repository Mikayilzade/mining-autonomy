"""Deterministic offline registry and scorecard for observation bundles.

The registry is intentionally read-only. It indexes already integrity-checked bundle
records, deduplicates bundle hashes globally, preserves exact per-observation demand
states, and never extrapolates utilization across time windows.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from typing import Any, Iterable, Mapping


_HEX = frozenset("0123456789abcdef")


@dataclass(frozen=True)
class BundleIndexEntry:
    bundle_sha256: str
    platform: str
    request_snapshot_sha256: str
    source_url: str
    source_timestamp: str
    captured_at: str
    request_evidence_class: str
    open_item_count: int
    demand_state: str
    paid_utilization_state: str
    paid_transaction_count: int | None
    paid_value_usd: float | None
    evidence_strength: int


@dataclass(frozen=True)
class BundleRegistry:
    entries: tuple[BundleIndexEntry, ...] = ()


def _require_object(value: Any, error: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(error)
    return value


def _require_sha256(value: Any, error: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(error)
    lowered = value.lower()
    if any(ch not in _HEX for ch in lowered):
        raise ValueError(error)
    return lowered


def _parse_timestamp(value: Any, error: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None:
        raise ValueError(error)
    return parsed.isoformat()


def _bundle_mapping(bundle: Any) -> Mapping[str, Any]:
    if isinstance(bundle, Mapping):
        return bundle
    if hasattr(bundle, "__dataclass_fields__"):
        return asdict(bundle)
    raise ValueError("bundle_registry_input_must_be_bundle_record")


def _classify_request(evidence_class: str, item_count: int) -> tuple[str, int]:
    if evidence_class == "open_paid_request":
        if item_count <= 0:
            raise ValueError("open_paid_request_must_have_items")
        return "positive_open_demand", 3
    if item_count == 0:
        return "zero_open_observation", 2
    if evidence_class in {"listing_only", "marketing_claim", "unknown"}:
        return "unproven", 1 if evidence_class == "listing_only" else 0
    raise ValueError("unsupported_registry_request_evidence_class")


def _classify_utilization(value: Any) -> tuple[str, int | None, float | None, int]:
    if value is None:
        return "unproven", None, None, 0
    util = _require_object(value, "bundle_utilization_must_be_object")
    count = util.get("transaction_count")
    amount = util.get("total_value_usd")
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        raise ValueError("bundle_utilization_transaction_count_invalid")
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
        raise ValueError("bundle_utilization_value_invalid")
    return "positive_paid_utilization", count, float(amount), 4


def index_bundle(bundle: Any) -> BundleIndexEntry:
    """Normalize one already integrity-verified observation bundle for history indexing."""
    record = _bundle_mapping(bundle)
    platform = record.get("platform")
    if not isinstance(platform, str) or not platform:
        raise ValueError("bundle_platform_required")
    manifest = _require_object(record.get("manifest"), "bundle_manifest_required")
    if manifest.get("platform") != platform:
        raise ValueError("bundle_manifest_platform_mismatch")
    if manifest.get("dry_run_only") is not True or manifest.get("action_enabled") is not False:
        raise ValueError("bundle_registry_requires_dry_run_action_disabled")
    bundle_sha = _require_sha256(record.get("manifest_sha256"), "bundle_manifest_sha256_invalid")
    envelope = _require_object(record.get("request_envelope"), "bundle_request_envelope_required")
    evidence_class = envelope.get("demand_evidence_class")
    if not isinstance(evidence_class, str) or not evidence_class:
        raise ValueError("bundle_request_evidence_class_required")
    snapshot = _require_object(envelope.get("snapshot"), "bundle_request_snapshot_required")
    if snapshot.get("platform") != platform:
        raise ValueError("bundle_snapshot_platform_mismatch")
    request_sha = _require_sha256(snapshot.get("payload_sha256"), "bundle_request_snapshot_sha256_invalid")
    payload = _require_object(snapshot.get("payload"), "bundle_request_payload_required")
    items = payload.get(envelope.get("records_key", "items"))
    if not isinstance(items, list):
        raise ValueError("bundle_request_items_must_be_list")
    source_url = snapshot.get("source_url")
    if not isinstance(source_url, str) or not source_url.startswith(("https://", "http://")):
        raise ValueError("bundle_source_url_invalid")
    source_timestamp = _parse_timestamp(snapshot.get("source_timestamp"), "bundle_source_timestamp_invalid")
    captured_at = _parse_timestamp(snapshot.get("captured_at"), "bundle_captured_at_invalid")
    demand_state, request_strength = _classify_request(evidence_class, len(items))
    util_state, tx_count, paid_value, util_strength = _classify_utilization(record.get("utilization"))
    return BundleIndexEntry(
        bundle_sha256=bundle_sha, platform=platform, request_snapshot_sha256=request_sha,
        source_url=source_url, source_timestamp=source_timestamp, captured_at=captured_at,
        request_evidence_class=evidence_class, open_item_count=len(items), demand_state=demand_state,
        paid_utilization_state=util_state, paid_transaction_count=tx_count,
        paid_value_usd=paid_value, evidence_strength=max(request_strength, util_strength),
    )


def add_bundle(registry: BundleRegistry, bundle: Any) -> BundleRegistry:
    entry = index_bundle(bundle)
    if any(existing.bundle_sha256 == entry.bundle_sha256 for existing in registry.entries):
        raise ValueError("duplicate_observation_bundle_hash")
    entries = tuple(sorted((*registry.entries, entry), key=lambda item: (item.source_timestamp, item.platform, item.bundle_sha256)))
    return BundleRegistry(entries)


def build_registry(bundles: Iterable[Any]) -> BundleRegistry:
    registry = BundleRegistry()
    for bundle in bundles:
        registry = add_bundle(registry, bundle)
    return registry


def registry_record(registry: BundleRegistry) -> dict[str, Any]:
    return {"schema_version": 1, "observation_count": len(registry.entries),
            "bundle_hashes": [entry.bundle_sha256 for entry in registry.entries],
            "entries": [asdict(entry) for entry in registry.entries],
            "dry_run_only": True, "action_enabled": False}


def serialize_registry(registry: BundleRegistry) -> str:
    return json.dumps(registry_record(registry), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _platform_score(entries: list[BundleIndexEntry]) -> dict[str, Any]:
    latest = max(entries, key=lambda item: (item.source_timestamp, item.bundle_sha256))
    paid = [entry for entry in entries if entry.paid_utilization_state == "positive_paid_utilization"]
    positive = [entry for entry in entries if entry.demand_state == "positive_open_demand"]
    zero = [entry for entry in entries if entry.demand_state == "zero_open_observation"]
    distinct_request_snapshots = len({entry.request_snapshot_sha256 for entry in entries})
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
    latest_paid = max(paid, key=lambda item: (item.source_timestamp, item.bundle_sha256)) if paid else None
    return {
        "platform": latest.platform, "observation_count": len(entries),
        "distinct_request_snapshot_count": distinct_request_snapshots,
        "latest_source_timestamp": latest.source_timestamp,
        "latest_demand_state": latest.demand_state, "latest_open_item_count": latest.open_item_count,
        "positive_open_observation_count": len(positive), "zero_open_observation_count": len(zero),
        "paid_utilization_observation_count": len(paid),
        "max_evidence_strength": max(entry.evidence_strength for entry in entries),
        "evidence_status": status,
        "latest_paid_transaction_count": latest_paid.paid_transaction_count if latest_paid else None,
        "latest_paid_value_usd": latest_paid.paid_value_usd if latest_paid else None,
        "paid_value_aggregation": "none_across_snapshots",
    }


def cross_market_scorecard(registry: BundleRegistry) -> dict[str, Any]:
    grouped: dict[str, list[BundleIndexEntry]] = {}
    for entry in registry.entries:
        grouped.setdefault(entry.platform, []).append(entry)
    platforms = [_platform_score(grouped[name]) for name in sorted(grouped)]
    return {"schema_version": 1, "platform_count": len(platforms),
            "observation_count": len(registry.entries), "platforms": platforms,
            "cross_snapshot_paid_value_sum_usd": None, "cross_snapshot_extrapolation": False,
            "dry_run_only": True, "action_enabled": False}
