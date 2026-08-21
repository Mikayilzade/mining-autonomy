"""I070 deterministic explicit human decision-record verifier over I069.

Offline only. Verifies an explicit decision bound to the exact I069 request,
I068 readiness, exact scope and unexpired window. It never infers consent,
enables transport, or creates an execution token.
"""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_human_decision_record_verifier"
DECISION_MODE = "explicit_human_read_only_observation_decision"
_ALLOWED = {"authorize_one_read_only_observation", "deny"}


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def verify_human_decision_record(request: Mapping[str, Any], decision: Mapping[str, Any], *, verified_at_utc: str) -> dict[str, Any]:
    blockers: list[str] = []

    request_hash = request.get("human_decision_request_sha256")
    request_core = dict(request)
    request_core.pop("human_decision_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(request_core):
        blockers.append("human_decision_request_hash_invalid")
    if request.get("request_state") != "decision_requested" or request.get("blockers"):
        blockers.append("human_decision_request_not_open")
    if request.get("mode") != "deterministic_market_observation_human_decision_request":
        blockers.append("human_decision_request_mode_invalid")

    scope = request.get("decision_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("decision_scope_missing")
    target = scope.get("authorization_target")
    if not isinstance(target, Mapping):
        target = {}
        blockers.append("authorization_target_missing")
    if scope.get("allowed_decisions") != ["authorize_one_read_only_observation", "deny"]:
        blockers.append("allowed_decisions_scope_invalid")
    if not (
        target.get("method") == "GET"
        and target.get("request_count") == 1
        and target.get("required_environment") == "production"
        and target.get("credentials_allowed") is False
        and target.get("action_enabled") is False
        and target.get("target_fingerprint")
    ):
        blockers.append("authorization_target_not_exact_anonymous_get")

    readiness_hash = request.get("market_side_readiness_sha256")
    exact_scope_hash = request.get("exact_scope_sha256")
    if target.get("market_side_readiness_sha256") != readiness_hash:
        blockers.append("readiness_hash_binding_invalid")
    if target.get("exact_scope_sha256") != exact_scope_hash:
        blockers.append("exact_scope_hash_binding_invalid")
    if not isinstance(readiness_hash, str) or len(readiness_hash) != 64:
        blockers.append("readiness_hash_missing")
    if not isinstance(exact_scope_hash, str) or len(exact_scope_hash) != 64:
        blockers.append("exact_scope_hash_missing")

    inert_request_flags = {
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
    for key, required in inert_request_flags.items():
        if request.get(key) is not required:
            blockers.append(f"unsafe_or_missing_request_{key}")

    choice = decision.get("decision")
    if decision.get("mode") != DECISION_MODE:
        blockers.append("explicit_human_decision_mode_required")
    if choice not in _ALLOWED:
        blockers.append("decision_value_invalid")
    if decision.get("human_scope_acknowledged") is not True:
        blockers.append("human_scope_acknowledgement_required")
    if decision.get("human_decision_request_sha256") != request_hash:
        blockers.append("decision_request_hash_binding_invalid")
    if decision.get("market_side_readiness_sha256") != readiness_hash:
        blockers.append("decision_readiness_hash_binding_invalid")
    if decision.get("exact_scope_sha256") != exact_scope_hash:
        blockers.append("decision_scope_hash_binding_invalid")

    try:
        requested_at = _utc(str(request.get("requested_at_utc")))
        expires_at = _utc(str(request.get("expires_at_utc")))
        decided_at = _utc(str(decision.get("decided_at_utc")))
        verified_at = _utc(verified_at_utc)
        if not (requested_at <= decided_at < expires_at):
            blockers.append("decision_outside_request_window")
        if verified_at >= expires_at:
            blockers.append("request_expired_at_verification")
        if decided_at > verified_at:
            blockers.append("decision_timestamp_in_future")
    except Exception:
        blockers.append("invalid_decision_or_request_timestamp")

    blockers = list(dict.fromkeys(blockers))
    accepted = not blockers
    authorization_verified = accepted and choice == "authorize_one_read_only_observation"
    denied = accepted and choice == "deny"

    record_core = {
        "schema_version": 1,
        "mode": MODE,
        "verification_state": (
            "explicit_read_only_authorization_verified"
            if authorization_verified
            else "explicit_deny_verified"
            if denied
            else "decision_rejected"
        ),
        "verified_at_utc": verified_at_utc,
        "decision": choice if accepted else None,
        "human_decision_request_sha256": request_hash,
        "market_side_readiness_sha256": readiness_hash,
        "exact_scope_sha256": exact_scope_hash,
        "current_resource_backend_id": request.get("current_resource_backend_id"),
        "authorization_scope": {
            "method": "GET",
            "request_count": 1,
            "required_environment": "production",
            "target_fingerprint": target.get("target_fingerprint"),
            "credentials_allowed": False,
            "action_enabled": False,
        } if authorization_verified else None,
        "blockers": blockers,
        "human_decision_recorded": accepted,
        "explicit_authorization_verified": authorization_verified,
        "explicit_deny_verified": denied,
        "real_user_consent_inferred_from_chat_history": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "record_is_execution_token": False,
        "record_is_transport_lease": False,
    }
    return {**record_core, "human_decision_verification_sha256": _hash(record_core)}
