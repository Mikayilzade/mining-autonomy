"""Deterministic no-network capture-readiness packets for I027 observations.

This module converts selected production-gap observations into exact future
read-only capture intents. It does not perform HTTP, use credentials, accept
work, publish services, or move value.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from sampling_receipt import manifest_item_sha256, verify_sampling_manifest_envelope


BLOCKING_EVIDENCE_CLASSES = frozenset({
    "public_observability_gate",
    "monetization_mechanics",
})


@dataclass(frozen=True)
class CaptureReadinessItem:
    platform: str
    item_index: int
    source_url: str
    manifest_item_sha256: str
    method: str
    expected_evidence_classes: tuple[str, ...]
    required_environment: str
    provenance_checklist: tuple[str, ...]
    rate_limit: Mapping[str, Any]
    rate_budget_score: int
    unresolved_gaps: tuple[str, ...]
    readiness_state: str
    readiness_reasons: tuple[str, ...]
    authorization_state: str = "explicit_read_only_network_authorization_required"
    credentials_allowed: bool = False
    network_calls_performed: bool = False
    dry_run_only: bool = True
    action_enabled: bool = False


def _validate_priority_plan(plan: Mapping[str, Any]) -> None:
    if plan.get("schema_version") != 1:
        raise ValueError("capture_readiness_plan_schema_invalid")
    if plan.get("mode") != "deterministic_plan_only_production_gap_priority":
        raise ValueError("capture_readiness_plan_mode_invalid")
    if plan.get("network_calls_performed") is not False:
        raise ValueError("capture_readiness_plan_network_flag_invalid")
    if plan.get("credentials_allowed") is not False:
        raise ValueError("capture_readiness_plan_credentials_flag_invalid")
    if plan.get("action_enabled") is not False:
        raise ValueError("capture_readiness_plan_action_flag_invalid")
    if plan.get("dry_run_only") is not True:
        raise ValueError("capture_readiness_plan_dry_run_flag_invalid")
    if plan.get("missing_evidence_is_negative_demand") is not False:
        raise ValueError("capture_readiness_missing_evidence_semantics_invalid")
    if not isinstance(plan.get("selected_read_only_observations"), list):
        raise ValueError("capture_readiness_selected_observations_invalid")


def _scheduled_manifest_items(envelope: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    verify_sampling_manifest_envelope(envelope)
    manifest = envelope["manifest"]
    if manifest.get("network_calls_performed") is not False:
        raise ValueError("capture_readiness_manifest_network_flag_invalid")
    if manifest.get("credentials_allowed") is not False:
        raise ValueError("capture_readiness_manifest_credentials_flag_invalid")
    if manifest.get("action_enabled") is not False:
        raise ValueError("capture_readiness_manifest_action_flag_invalid")
    return {
        index: item
        for index, item in enumerate(manifest["items"])
        if item.get("scheduled") is True
    }


def _validate_rate_limit(rate_limit: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(rate_limit, Mapping):
        raise ValueError("capture_readiness_rate_limit_missing")
    required = (
        "min_interval_seconds",
        "max_requests_per_window",
        "window_seconds",
        "budget_basis",
    )
    if any(key not in rate_limit for key in required):
        raise ValueError("capture_readiness_rate_limit_invalid")
    try:
        min_interval = float(rate_limit["min_interval_seconds"])
        max_requests = int(rate_limit["max_requests_per_window"])
        window = float(rate_limit["window_seconds"])
    except (TypeError, ValueError) as exc:
        raise ValueError("capture_readiness_rate_limit_invalid") from exc
    if min_interval < 0 or max_requests <= 0 or window <= 0:
        raise ValueError("capture_readiness_rate_limit_invalid")
    if rate_limit["budget_basis"] != "project_conservative_self_limit":
        raise ValueError("capture_readiness_rate_limit_basis_invalid")
    return dict(rate_limit)


def _readiness(
    *,
    expected_evidence_classes: tuple[str, ...],
    environment: str,
) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    if environment != "production":
        reasons.append("production_environment_not_predeclared")
    if not expected_evidence_classes:
        reasons.append("expected_evidence_class_missing")
    if expected_evidence_classes and set(expected_evidence_classes).issubset(BLOCKING_EVIDENCE_CLASSES):
        reasons.append("source_observability_cannot_close_demand_gap_by_itself")
    if reasons:
        return "blocked_by_observability_or_environment_requirement", tuple(reasons)
    return "ready_for_future_explicit_read_only_capture", (
        "scheduled_get_no_credentials",
        "production_environment_declared",
        "demand_or_utilization_evidence_class_requested",
    )


def build_capture_readiness_packet(
    priority_plan: Mapping[str, Any],
    manifest_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    """Build an exact no-network future-capture packet for selected I027 work."""
    _validate_priority_plan(priority_plan)
    scheduled = _scheduled_manifest_items(manifest_envelope)
    if priority_plan.get("manifest_sha256") != manifest_envelope.get("manifest_sha256"):
        raise ValueError("capture_readiness_manifest_hash_mismatch")

    packet_items: list[CaptureReadinessItem] = []
    seen: set[tuple[int, str]] = set()

    for selected in priority_plan["selected_read_only_observations"]:
        if not isinstance(selected, Mapping):
            raise ValueError("capture_readiness_selected_row_invalid")
        item_index = selected.get("item_index")
        if not isinstance(item_index, int) or isinstance(item_index, bool):
            raise ValueError("capture_readiness_item_index_invalid")
        item = scheduled.get(item_index)
        if item is None:
            raise ValueError("capture_readiness_item_not_scheduled")

        key = (item_index, str(selected.get("source_url")))
        if key in seen:
            raise ValueError("capture_readiness_duplicate_selected_item")
        seen.add(key)

        expected_sha = manifest_item_sha256(manifest_envelope, item_index)
        if (
            selected.get("platform") != item.get("platform")
            or selected.get("source_url") != item.get("source_url")
            or selected.get("manifest_item_sha256") != expected_sha
        ):
            raise ValueError("capture_readiness_manifest_identity_mismatch")
        if item.get("method") != "GET":
            raise ValueError("capture_readiness_non_get_forbidden")
        if item.get("credentials_allowed") is not False:
            raise ValueError("capture_readiness_credentials_forbidden")
        if item.get("network_calls_performed") is not False or item.get("action_enabled") is not False:
            raise ValueError("capture_readiness_action_boundary_invalid")

        evidence_classes = tuple(str(v) for v in item.get("expected_evidence_classes", ()))
        environment = str(item.get("environment", "unknown"))
        provenance = tuple(str(v) for v in item.get("provenance_requirements", ()))
        if not provenance:
            raise ValueError("capture_readiness_provenance_missing")
        rate_limit = _validate_rate_limit(item.get("rate_limit", {}))
        readiness_state, readiness_reasons = _readiness(
            expected_evidence_classes=evidence_classes,
            environment=environment,
        )

        packet_items.append(CaptureReadinessItem(
            platform=str(item.get("platform")),
            item_index=item_index,
            source_url=str(item.get("source_url")),
            manifest_item_sha256=expected_sha,
            method="GET",
            expected_evidence_classes=evidence_classes,
            required_environment=environment,
            provenance_checklist=provenance,
            rate_limit=rate_limit,
            rate_budget_score=int(selected.get("rate_budget_score", 0)),
            unresolved_gaps=tuple(str(v) for v in selected.get("unresolved_gaps", ())),
            readiness_state=readiness_state,
            readiness_reasons=readiness_reasons,
        ))

    ready = [item for item in packet_items if item.readiness_state == "ready_for_future_explicit_read_only_capture"]
    blocked = [item for item in packet_items if item.readiness_state == "blocked_by_observability_or_environment_requirement"]

    return {
        "schema_version": 1,
        "mode": "deterministic_no_network_capture_readiness_packet",
        "manifest_sha256": manifest_envelope["manifest_sha256"],
        "selected_count": len(packet_items),
        "ready_count": len(ready),
        "blocked_count": len(blocked),
        "items": [asdict(item) for item in packet_items],
        "ready_for_future_explicit_read_only_capture": [asdict(item) for item in ready],
        "blocked_by_observability_or_environment_requirement": [asdict(item) for item in blocked],
        "authorization_state": "explicit_read_only_network_authorization_required",
        "authorization_granted": False,
        "rate_budget_is_self_imposed_ceiling": True,
        "missing_evidence_is_negative_demand": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }
