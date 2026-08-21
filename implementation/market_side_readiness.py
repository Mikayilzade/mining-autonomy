"""I068 deterministic market-side readiness checkpoint.

Joins compliance-review readiness and current resource-routing readiness into a
human-reviewable packet. It never performs transport or grants authorization.
"""
from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_market_side_readiness_checkpoint"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def build_market_side_readiness_packet(
    compliance_bridge: Mapping[str, Any],
    materialized_route: Mapping[str, Any],
    *,
    candidate: str,
    built_at_utc: str,
) -> dict[str, Any]:
    blockers: list[str] = []
    if compliance_bridge.get("bridge_state") != "ready_for_human_decision":
        blockers.append("source_compliance_not_ready")
    if compliance_bridge.get("human_decision_requested") is not True:
        blockers.append("exact_read_only_authorization_decision_not_ready")
    scope = compliance_bridge.get("exact_scope")
    if not isinstance(scope, Mapping):
        blockers.append("exact_scope_missing")
        scope = {}
    elif not (
        scope.get("method") == "GET"
        and scope.get("required_environment") == "production"
        and scope.get("request_count") == 1
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
    ):
        blockers.append("exact_scope_not_single_anonymous_read_only_get")

    route_state = materialized_route.get("state") or materialized_route.get("route_state")
    selected = materialized_route.get("selected_backend_id") or materialized_route.get("selected_backend_after")
    if route_state not in {"route_dry_run", "materialized_route_dry_run", "rerouted_dry_run"}:
        blockers.append("current_resource_route_not_ready")
    if not selected:
        blockers.append("current_resource_backend_missing")
    for flag in ("execution_enabled", "network_enabled", "value_movement_enabled"):
        if materialized_route.get(flag, False) is not False:
            blockers.append(f"unsafe_resource_route_{flag}")

    observation = {
        "candidate": candidate,
        "purpose": "measure_real_open_paid_demand_and_fill_without_accepting_or_submitting_work",
        "method": scope.get("method"),
        "request_count": scope.get("request_count"),
        "required_environment": scope.get("required_environment"),
        "target_fingerprint": scope.get("target_fingerprint"),
        "credentials_allowed": False,
        "action_enabled": False,
    }
    unresolved = list(dict.fromkeys(blockers + [
        "fresh_explicit_real_user_authorization_still_required",
        "reviewed_real_transport_implementation_still_required",
        "dns_redirect_response_limit_gates_still_required",
        "durable_real_response_receipt_still_required",
        "real_market_demand_fill_acceptance_payment_economics_unmeasured",
    ]))
    core = {
        "schema_version": 1,
        "mode": MODE,
        "built_at_utc": built_at_utc,
        "checkpoint_state": "ready_for_human_review_only" if not blockers else "blocked_before_human_review",
        "dominant_unknown": "real_market_demand_and_fill_rate",
        "single_observation_needed": observation,
        "current_resource_route": {
            "selected_backend_id": selected,
            "route_state": route_state,
            "history_tip_hash": materialized_route.get("history_tip_hash"),
            "materialization_hash": materialized_route.get("materialization_hash"),
        },
        "compliance_review_bridge_sha256": compliance_bridge.get("compliance_review_bridge_sha256"),
        "exact_scope_sha256": compliance_bridge.get("exact_scope_sha256"),
        "unresolved_gates": unresolved,
        "authorization_granted": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "packet_is_authorization": False,
        "packet_is_execution_token": False,
    }
    return {**core, "market_side_readiness_sha256": _hash(core)}
