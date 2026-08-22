from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Collection, Mapping

MODE = "deterministic_exact_real_read_only_invocation_decision_verifier"
_DECISION_MODE = "explicit_exact_real_read_only_invocation_human_decision"
_AUTH_MODE = "single_use_exact_real_read_only_invocation_authorization"
_EXPECTED_REQUEST_MODE = "exact_real_read_only_invocation_human_review_request"
_EXPECTED_REQUEST_STATE = "ready_for_fresh_explicit_human_real_read_only_invocation_decision"


def _hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise ValueError("timestamp_must_be_utc")
    return dt.astimezone(timezone.utc)


def _exact_scope(scope: Mapping[str, Any]) -> bool:
    return (
        scope.get("method") == "GET"
        and scope.get("request_count") == 1
        and scope.get("required_environment") == "production"
        and isinstance(scope.get("target_fingerprint"), str)
        and bool(scope.get("target_fingerprint"))
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
    )


def verify_exact_real_read_only_invocation_decision(
    invocation_request: Mapping[str, Any],
    human_decision: Mapping[str, Any],
    *,
    verified_at: str,
    authorization_ttl_seconds: int = 180,
    prior_decision_sha256s: Collection[str] = (),
) -> dict[str, Any]:
    """Verify a fresh exact human decision and emit at most an inert single-use authorization."""
    blockers: list[str] = []

    try:
        verified_dt = _parse_utc(verified_at)
    except Exception:
        verified_dt = None
        blockers.append("verified_at_invalid_or_not_utc")

    request_hash = invocation_request.get("exact_real_read_only_invocation_request_sha256")
    request_core = dict(invocation_request)
    request_core.pop("exact_real_read_only_invocation_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(request_core):
        blockers.append("invocation_request_hash_invalid")
    if invocation_request.get("mode") != _EXPECTED_REQUEST_MODE:
        blockers.append("invocation_request_mode_invalid")
    if invocation_request.get("request_state") != _EXPECTED_REQUEST_STATE:
        blockers.append("invocation_request_not_ready")

    request_safety = {
        "explicit_human_decision_required": True,
        "real_invocation_authorized": False,
        "network_capable_adapter_reachable": False,
        "adapter_invoked": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "request_is_execution_token": False,
    }
    for key, required in request_safety.items():
        if invocation_request.get(key) is not required:
            blockers.append(f"unsafe_or_missing_request_{key}")

    scope = invocation_request.get("exact_scope")
    if not isinstance(scope, Mapping) or not _exact_scope(scope):
        blockers.append("scope_not_exact_single_anonymous_production_get")
        scope = {}
    scope_hash = invocation_request.get("exact_scope_sha256")
    if not isinstance(scope_hash, str) or scope_hash != _hash(dict(scope)):
        blockers.append("exact_scope_hash_invalid")

    source_lineage = invocation_request.get("source_lineage")
    if not isinstance(source_lineage, Mapping) or not source_lineage:
        blockers.append("invocation_request_source_lineage_missing")
        source_lineage = {}
    required_source_keys = (
        "implementation_binding_audit_sha256",
        "implementation_source_sha256",
        "network_adapter_contract_validation_sha256",
        "adapter_contract_readiness_sha256",
        "real_network_activation_authorization_sha256",
        "real_network_activation_request_sha256",
    )
    for key in required_source_keys:
        value = source_lineage.get(key)
        if not isinstance(value, str) or not value:
            blockers.append(f"missing_request_source_lineage_{key}")
    implementation_digest = source_lineage.get("implementation_source_sha256")
    if not isinstance(implementation_digest, str) or len(implementation_digest) != 64:
        blockers.append("implementation_source_digest_invalid")

    binding_fields = (
        "activation_envelope_invocation_gate_sha256",
        "synthetic_adapter_invocation_receipt_sha256",
        "real_network_activation_consumption_preflight_sha256",
        "real_network_activation_envelope_sha256",
        "adapter_id",
        "exact_scope_sha256",
    )
    for key in binding_fields:
        if not isinstance(invocation_request.get(key), str) or not invocation_request.get(key):
            blockers.append(f"missing_request_binding_{key}")

    try:
        requested_dt = _parse_utc(str(invocation_request.get("requested_at")))
        expires_dt = _parse_utc(str(invocation_request.get("expires_at")))
        if expires_dt <= requested_dt:
            blockers.append("invocation_request_expiry_invalid")
        if verified_dt is not None and not (requested_dt <= verified_dt <= expires_dt):
            blockers.append("invocation_request_stale_or_not_yet_valid")
    except Exception:
        requested_dt = None
        expires_dt = None
        blockers.append("invocation_request_time_invalid")

    ttl = invocation_request.get("ttl_seconds")
    if (
        isinstance(ttl, bool)
        or not isinstance(ttl, int)
        or not 60 <= ttl <= 900
        or (
            requested_dt is not None
            and expires_dt is not None
            and expires_dt != requested_dt + timedelta(seconds=ttl)
        )
    ):
        blockers.append("invocation_request_ttl_invalid")

    if (
        isinstance(authorization_ttl_seconds, bool)
        or not isinstance(authorization_ttl_seconds, int)
        or not 30 <= authorization_ttl_seconds <= 300
    ):
        blockers.append("authorization_ttl_out_of_range")

    if human_decision.get("mode") != _DECISION_MODE:
        blockers.append("human_decision_mode_invalid")
    decision = human_decision.get("decision")
    if decision not in {"authorize", "deny"}:
        blockers.append("human_decision_value_invalid")
    if human_decision.get("exact_real_read_only_invocation_request_sha256") != request_hash:
        blockers.append("human_decision_request_binding_invalid")

    for key in binding_fields:
        if human_decision.get(key) != invocation_request.get(key):
            blockers.append(f"human_decision_{key}_binding_invalid")
    if human_decision.get("exact_scope") != dict(scope):
        blockers.append("human_decision_scope_not_exact")
    if human_decision.get("source_lineage") != dict(source_lineage):
        blockers.append("human_decision_source_lineage_binding_invalid")

    decision_id = human_decision.get("decision_id")
    if not isinstance(decision_id, str) or not decision_id.strip():
        blockers.append("human_decision_id_missing")
    if human_decision.get("single_use") is not True:
        blockers.append("human_decision_not_single_use")

    for key in (
        "credentials_allowed",
        "task_acceptance_enabled",
        "submission_enabled",
        "value_movement_enabled",
    ):
        if human_decision.get(key) is not False:
            blockers.append(f"human_decision_{key}_widened")

    try:
        decided_dt = _parse_utc(str(human_decision.get("decided_at")))
        if verified_dt is not None and decided_dt > verified_dt:
            blockers.append("human_decision_from_future")
        if (
            requested_dt is not None
            and expires_dt is not None
            and not (requested_dt <= decided_dt <= expires_dt)
        ):
            blockers.append("human_decision_outside_request_window")
    except Exception:
        decided_dt = None
        blockers.append("human_decision_time_invalid")

    decision_hash = human_decision.get("exact_real_read_only_invocation_decision_sha256")
    decision_core = dict(human_decision)
    decision_core.pop("exact_real_read_only_invocation_decision_sha256", None)
    if not isinstance(decision_hash, str) or decision_hash != _hash(decision_core):
        blockers.append("human_decision_hash_invalid")
    elif decision_hash in set(prior_decision_sha256s):
        blockers.append("human_decision_replay_detected")

    blockers = list(dict.fromkeys(blockers))
    authorization = None
    state = "decision_rejected"

    if not blockers and decision == "deny":
        state = "denied_no_real_read_only_invocation_authorization"
    elif (
        not blockers
        and decision == "authorize"
        and verified_dt is not None
        and decided_dt is not None
        and expires_dt is not None
    ):
        auth_expires = min(
            verified_dt + timedelta(seconds=authorization_ttl_seconds),
            expires_dt,
        )
        if auth_expires <= verified_dt:
            blockers.append("authorization_would_be_expired")
        else:
            auth_core = {
                "schema_version": 1,
                "mode": _AUTH_MODE,
                "authorization_state": "authorized_single_use_not_consumed",
                "issued_at": verified_dt.isoformat().replace("+00:00", "Z"),
                "expires_at": auth_expires.isoformat().replace("+00:00", "Z"),
                "single_use": True,
                "consumed": False,
                "decision_id": decision_id,
                "exact_real_read_only_invocation_decision_sha256": decision_hash,
                "exact_real_read_only_invocation_request_sha256": request_hash,
                **{key: invocation_request.get(key) for key in binding_fields},
                "exact_scope": dict(scope),
                "source_lineage": dict(source_lineage),
                "real_read_only_invocation_authorized": True,
                "max_network_requests": 1,
                "credentials_allowed": False,
                "task_acceptance_enabled": False,
                "submission_enabled": False,
                "value_movement_enabled": False,
                "network_capable_adapter_reachable": False,
                "transport_enabled": False,
                "network_enabled": False,
                "network_calls_performed": False,
                "authorization_is_payment_or_task_permission": False,
                "authorization_is_execution_result": False,
            }
            authorization = {
                **auth_core,
                "exact_real_read_only_invocation_authorization_sha256": _hash(auth_core),
            }
            state = "real_read_only_invocation_authorization_issued_not_consumed"

    core = {
        "schema_version": 1,
        "mode": MODE,
        "verification_state": state if not blockers else "decision_rejected",
        "exact_real_read_only_invocation_request_sha256": request_hash
        if isinstance(request_hash, str)
        else None,
        "exact_real_read_only_invocation_decision_sha256": decision_hash
        if isinstance(decision_hash, str)
        else None,
        "real_read_only_invocation_authorization": authorization if not blockers else None,
        "blockers": blockers,
        "network_capable_adapter_reachable": False,
        "adapter_invoked": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "verification_record_is_execution_token": False,
    }
    return {
        **core,
        "exact_real_read_only_invocation_decision_verification_sha256": _hash(core),
    }
