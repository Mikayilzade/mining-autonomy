"""Deterministic read-only capture registry runner for saved observation bundles.

This module performs no network, authentication, publication, task acceptance, wallet,
payment, or settlement action. It validates provenance/freshness/rate limits for
already-captured public observation bundles. Durable-ingestion reports must additionally
carry a verified sealed-manifest capture receipt for every bundle.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from bundle_registry import (
    BundleRegistry,
    add_bundle,
    cross_market_scorecard,
    index_bundle,
    registry_record,
)
from sampling_receipt import verify_capture_receipt


@dataclass(frozen=True)
class CapturePolicy:
    max_age_hours: float = 24.0
    min_interval_seconds: float = 300.0
    max_future_skew_seconds: float = 120.0


@dataclass(frozen=True)
class CaptureState:
    last_capture_by_source: tuple[tuple[str, str], ...] = ()

    def as_dict(self) -> dict[str, str]:
        return dict(self.last_capture_by_source)


@dataclass(frozen=True)
class RegistryDelta:
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
    distinct_request_snapshot_added: bool
    prior_latest_demand_state: str | None
    latest_demand_state: str


def _parse_timestamp(value: str, error: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None:
        raise ValueError(error)
    return parsed.astimezone(timezone.utc)


def _source_key(platform: str, source_url: str) -> str:
    return f"{platform}\n{source_url}"


def _validate_policy(policy: CapturePolicy) -> None:
    if policy.max_age_hours <= 0:
        raise ValueError("capture_policy_max_age_hours_must_be_positive")
    if policy.min_interval_seconds < 0:
        raise ValueError("capture_policy_min_interval_seconds_invalid")
    if policy.max_future_skew_seconds < 0:
        raise ValueError("capture_policy_future_skew_invalid")


def _validate_freshness(source_timestamp: str, captured_at: str, policy: CapturePolicy) -> None:
    source = _parse_timestamp(source_timestamp, "capture_source_timestamp_invalid")
    captured = _parse_timestamp(captured_at, "capture_captured_at_invalid")
    age_seconds = (captured - source).total_seconds()
    if age_seconds < -policy.max_future_skew_seconds:
        raise ValueError("capture_source_timestamp_too_far_in_future")
    if age_seconds > policy.max_age_hours * 3600.0:
        raise ValueError("capture_source_snapshot_stale")


def _platform_latest_state(registry: BundleRegistry, platform: str) -> str | None:
    candidates = [entry for entry in registry.entries if entry.platform == platform]
    if not candidates:
        return None
    latest = max(candidates, key=lambda item: (item.source_timestamp, item.bundle_sha256))
    return latest.demand_state


def _next_state(state: CaptureState, key: str, captured_at: str) -> CaptureState:
    values = state.as_dict()
    values[key] = captured_at
    return CaptureState(tuple(sorted(values.items())))


def apply_captured_bundle(registry: BundleRegistry, state: CaptureState, bundle: Any, *, policy: CapturePolicy = CapturePolicy()) -> tuple[BundleRegistry, CaptureState, RegistryDelta]:
    """Validate/add one bundle to the transient registry; not durable evidence alone."""
    _validate_policy(policy)
    entry = index_bundle(bundle)
    if not entry.source_url.startswith("https://"):
        raise ValueError("capture_public_source_must_use_https")
    _validate_freshness(entry.source_timestamp, entry.captured_at, policy)
    key = _source_key(entry.platform, entry.source_url)
    prior_capture = state.as_dict().get(key)
    if prior_capture is not None:
        prior_dt = _parse_timestamp(prior_capture, "capture_state_timestamp_invalid")
        current_dt = _parse_timestamp(entry.captured_at, "capture_captured_at_invalid")
        interval = (current_dt - prior_dt).total_seconds()
        if interval < 0:
            raise ValueError("capture_time_regressed_for_source")
        if interval < policy.min_interval_seconds:
            raise ValueError("capture_rate_limit_guard")
    prior_latest = _platform_latest_state(registry, entry.platform)
    prior_request_hashes = {item.request_snapshot_sha256 for item in registry.entries if item.platform == entry.platform}
    updated = add_bundle(registry, bundle)
    latest_state = _platform_latest_state(updated, entry.platform)
    delta = RegistryDelta(
        platform=entry.platform, source_url=entry.source_url, source_timestamp=entry.source_timestamp,
        captured_at=entry.captured_at, bundle_sha256=entry.bundle_sha256,
        request_snapshot_sha256=entry.request_snapshot_sha256, demand_state=entry.demand_state,
        open_item_count=entry.open_item_count, paid_utilization_state=entry.paid_utilization_state,
        paid_transaction_count=entry.paid_transaction_count, paid_value_usd=entry.paid_value_usd,
        distinct_request_snapshot_added=entry.request_snapshot_sha256 not in prior_request_hashes,
        prior_latest_demand_state=prior_latest, latest_demand_state=latest_state or entry.demand_state,
    )
    return updated, _next_state(state, key, entry.captured_at), delta


def _verified_attestation(bundle: Any, envelope: Mapping[str, Any], receipt: Mapping[str, Any]) -> dict[str, Any]:
    verify_capture_receipt(envelope, receipt)
    entry = index_bundle(bundle)
    if receipt.get("sanitized_bundle_sha256") != entry.bundle_sha256:
        raise ValueError("capture_receipt_bundle_mismatch")
    if receipt.get("platform") != entry.platform:
        raise ValueError("capture_receipt_bundle_platform_mismatch")
    if receipt.get("source_url") != entry.source_url:
        raise ValueError("capture_receipt_bundle_source_mismatch")
    if receipt.get("method") != "GET":
        raise ValueError("capture_receipt_method_not_read_only")
    if _parse_timestamp(receipt.get("capture_finished_at"), "capture_receipt_finished_at_invalid") != _parse_timestamp(entry.captured_at, "capture_captured_at_invalid"):
        raise ValueError("capture_receipt_bundle_capture_time_mismatch")
    receipt_source_ts = receipt.get("source_timestamp")
    if receipt_source_ts is not None and _parse_timestamp(receipt_source_ts, "capture_receipt_source_timestamp_invalid") != _parse_timestamp(entry.source_timestamp, "capture_source_timestamp_invalid"):
        raise ValueError("capture_receipt_bundle_source_time_mismatch")
    if receipt.get("captured_environment") not in {"production", "testnet", "unknown"}:
        raise ValueError("capture_receipt_environment_invalid")
    return {"bundle_sha256": entry.bundle_sha256, "manifest_envelope": dict(envelope), "receipt": dict(receipt)}


def time_series_scorecard(registry: BundleRegistry) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in registry.entries:
        grouped.setdefault(entry.platform, []).append({
            "source_timestamp": entry.source_timestamp, "captured_at": entry.captured_at,
            "source_url": entry.source_url, "bundle_sha256": entry.bundle_sha256,
            "request_snapshot_sha256": entry.request_snapshot_sha256, "demand_state": entry.demand_state,
            "open_item_count": entry.open_item_count, "paid_utilization_state": entry.paid_utilization_state,
            "paid_transaction_count": entry.paid_transaction_count, "paid_value_usd": entry.paid_value_usd,
            "evidence_strength": entry.evidence_strength,
        })
    return {"schema_version": 1, "platforms": [{"platform": p, "points": grouped[p]} for p in sorted(grouped)],
            "paid_value_aggregation": "none_across_observations", "paid_value_extrapolation": False,
            "dry_run_only": True, "action_enabled": False}


def run_capture_batch(bundles: Iterable[Any], *, registry: BundleRegistry | None = None, state: CaptureState | None = None, policy: CapturePolicy = CapturePolicy()) -> dict[str, Any]:
    """Transient/local-only batch; explicitly not archive-ingestion eligible."""
    current_registry = registry or BundleRegistry()
    current_state = state or CaptureState()
    indexed = [(index_bundle(bundle), bundle) for bundle in bundles]
    indexed.sort(key=lambda pair: (pair[0].captured_at, pair[0].platform, pair[0].bundle_sha256))
    deltas: list[RegistryDelta] = []
    for _, bundle in indexed:
        current_registry, current_state, delta = apply_captured_bundle(current_registry, current_state, bundle, policy=policy)
        deltas.append(delta)
    return {"schema_version": 1, "capture_policy": asdict(policy), "capture_state": dict(current_state.last_capture_by_source),
            "deltas": [asdict(delta) for delta in deltas], "registry": registry_record(current_registry),
            "cross_market_scorecard": cross_market_scorecard(current_registry), "time_series_scorecard": time_series_scorecard(current_registry),
            "capture_attestations": [], "receipt_required_for_durable_ingestion": False,
            "dry_run_only": True, "action_enabled": False}


def run_verified_capture_batch(captures: Iterable[Mapping[str, Any]], *, registry: BundleRegistry | None = None, state: CaptureState | None = None, policy: CapturePolicy = CapturePolicy()) -> dict[str, Any]:
    """Create archive-eligible report only from receipt-bound sanitized bundles; no network."""
    verified: list[tuple[Any, dict[str, Any]]] = []
    for capture in captures:
        if not isinstance(capture, Mapping):
            raise ValueError("verified_capture_must_be_object")
        bundle = capture.get("bundle")
        envelope = capture.get("manifest_envelope")
        receipt = capture.get("receipt")
        if not isinstance(envelope, Mapping) or not isinstance(receipt, Mapping):
            raise ValueError("verified_capture_attestation_required")
        verified.append((bundle, _verified_attestation(bundle, envelope, receipt)))
    report = run_capture_batch([bundle for bundle, _ in verified], registry=registry, state=state, policy=policy)
    attestations = [item for _, item in verified]
    attestations.sort(key=lambda item: item["bundle_sha256"])
    report["capture_attestations"] = attestations
    report["receipt_required_for_durable_ingestion"] = True
    return report
