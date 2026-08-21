"""I069 deterministic human-decision request over I068 market readiness.

Builds a short, exact-scope request for a future human decision. This module
cannot grant authorization, enable transport, or perform network/value actions.
"""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_market_observation_human_decision_request"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def build_human_decision_request(
    readiness: Mapping[str, Any],
    *,
    requested_at_utc: str,
    upstream_review_expires_at_utc: str,
) -> dict[str, Any]:
    """Create an inert decision request bound to one exact I068 checkpoint.

    The caller must supply the exact upstream review-scope expiry. The request
    inherits that expiry verbatim; it cannot extend or replace it.
    """
    blockers: list[str] = []

    expected = readiness.get("market_side_readiness_sha256")
    core = dict(readiness)
    core.pop("market_side_readiness_sha256", None)
    if not isinstance(expected, str) or expected != _hash(core):
        blockers.append("market_side_readiness_hash_invalid")

    if readiness.get("checkpoint_state") != "ready_for_human_review_only":
        blockers.append("market_side_readiness_not_ready")

    observation = readiness.get("single_observation_needed")
    if not isinstance(observation, Mapping):
        observation = {}
        blockers.append("single_observation_missing")
    elif not (
        observation.get("method") == "GET"
        and observation.get("request_count") == 1
        and observation.get("required_environment") == "production"
        and observation.get("credentials_allowed") is False
        and observation.get("action_enabled") is False
        and observation.get("target_fingerprint")
    ):
        blockers.append("single_observation_scope_not_exact_anonymous_get")

    route = readiness.get("current_resource_route")
    if not isinstance(route, Mapping) or not route.get("selected_backend_id"):
        blockers.append("current_resource_route_missing")

    inert_flags = {
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
    for key, required in inert_flags.items():
        if readiness.get(key) is not required:
            blockers.append(f"unsafe_or_missing_readiness_{key}")

    try:
        requested_at = _utc(requested_at_utc)
        expires_at = _utc(upstream_review_expires_at_utc)
        if requested_at >= expires_at:
            blockers.append("upstream_review_scope_expired_or_nonpositive")
    except Exception:
        blockers.append("invalid_request_or_expiry_timestamp")

    exact_scope_sha = readiness.get("exact_scope_sha256")
    if not isinstance(exact_scope_sha, str) or len(exact_scope_sha) != 64:
        blockers.append("exact_scope_hash_missing")

    decision_scope = {
        "allowed_decisions": ["authorize_one_read_only_observation", "deny"],
        "authorization_target": {
            "market_side_readiness_sha256": expected,
            "exact_scope_sha256": exact_scope_sha,
            "candidate": observation.get("candidate"),
            "method": observation.get("method"),
            "request_count": observation.get("request_count"),
            "required_environment": observation.get("required_environment"),
            "target_fingerprint": observation.get("target_fingerprint"),
            "credentials_allowed": False,
            "action_enabled": False,
        },
        "explicitly_not_authorized": [
            "credentials_or_login",
            "task_acceptance",
            "task_submission",
            "payment_or_purchase",
            "wallet_or_settlement",
            "value_movement",
            "additional_requests",
            "non_GET_methods",
        ],
    }

    request_core = {
        "schema_version": 1,
        "mode": MODE,
        "request_state": "decision_requested" if not blockers else "blocked_before_decision_request",
        "requested_at_utc": requested_at_utc,
        "expires_at_utc": upstream_review_expires_at_utc,
        "expiry_source": "upstream_review_scope_exact_expiry",
        "market_side_readiness_sha256": expected,
        "exact_scope_sha256": exact_scope_sha,
        "current_resource_backend_id": route.get("selected_backend_id") if isinstance(route, Mapping) else None,
        "decision_scope": decision_scope,
        "blockers": list(dict.fromkeys(blockers)),
        "human_decision_recorded": False,
        "authorization_granted": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "request_is_authorization": False,
        "request_is_execution_token": False,
    }
    return {**request_core, "human_decision_request_sha256": _hash(request_core)}
