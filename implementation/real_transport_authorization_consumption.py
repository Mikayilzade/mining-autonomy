from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Collection, Mapping

MODE = "deterministic_real_transport_authorization_consumption_preflight"
_EXPECTED_VERIFICATION_MODE = "deterministic_real_transport_authorization_verifier"
_EXPECTED_AUTH_MODE = "single_use_real_transport_authorization_record"

def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt

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

def _transport_gates() -> dict[str, Any]:
    return {
        "dns_policy": {
            "resolve_before_connect_required": True,
            "reject_loopback_private_link_local_reserved_required": True,
            "destination_pinning_required": True,
            "dns_rebinding_recheck_required": True,
        },
        "redirect_policy": {
            "automatic_redirects_allowed": False,
            "max_redirects": 0,
            "redirect_target_revalidation_required_if_ever_enabled": True,
        },
        "response_policy": {
            "max_body_bytes": 1_048_576,
            "allowed_content_types": ["application/json"],
            "content_type_match_required": True,
            "body_size_gate_before_parsing_required": True,
        },
        "source_policy": {
            "fresh_first_party_compliance_evidence_required": True,
            "anonymous_read_only_access_required": True,
            "credentials_allowed": False,
            "action_enabled": False,
        },
    }

def consume_real_transport_authorization(
    verification: Mapping[str, Any],
    *,
    consumed_at_utc: str,
    seen_consumed_authorization_sha256: Collection[str] = (),
) -> dict[str, Any]:
    blockers: list[str] = []

    verification_hash = verification.get("real_transport_authorization_verification_sha256")
    verification_core = dict(verification)
    verification_core.pop("real_transport_authorization_verification_sha256", None)
    if not isinstance(verification_hash, str) or verification_hash != _hash(verification_core):
        blockers.append("i074_verification_hash_invalid")
    if verification.get("mode") != _EXPECTED_VERIFICATION_MODE:
        blockers.append("i074_verification_mode_invalid")
    if (
        verification.get("verification_state") != "explicit_real_transport_authorization_verified"
        or verification.get("blockers")
        or verification.get("explicit_real_transport_authorization_verified") is not True
    ):
        blockers.append("i074_authorization_not_verified")

    verification_inert = {
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
    for key, required in verification_inert.items():
        if verification.get(key) is not required:
            blockers.append(f"unsafe_or_missing_verification_{key}")

    auth = verification.get("authorization_record")
    if not isinstance(auth, Mapping):
        auth = {}
        blockers.append("authorization_record_missing")

    auth_hash = auth.get("real_transport_authorization_sha256")
    auth_core = dict(auth)
    auth_core.pop("real_transport_authorization_sha256", None)
    if not isinstance(auth_hash, str) or auth_hash != _hash(auth_core):
        blockers.append("authorization_record_hash_invalid")
    if auth.get("mode") != _EXPECTED_AUTH_MODE:
        blockers.append("authorization_record_mode_invalid")
    if auth.get("authorization_state") != "authorized_exact_single_read_only_transport":
        blockers.append("authorization_record_state_invalid")
    if auth.get("max_consumptions") != 1 or auth.get("authorization_is_single_use") is not True:
        blockers.append("authorization_not_single_use")

    scope = auth.get("authorization_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("authorization_scope_missing")
    if not _exact_scope(scope):
        blockers.append("authorization_scope_not_exact_anonymous_get")

    if auth.get("pre_real_transport_review_sha256") != verification.get("pre_real_transport_review_sha256"):
        blockers.append("review_hash_binding_invalid")
    if auth.get("real_transport_decision_sha256") != verification.get("real_transport_decision_sha256"):
        blockers.append("decision_hash_binding_invalid")
    if auth.get("exact_scope_sha256") != verification.get("exact_scope_sha256"):
        blockers.append("scope_hash_binding_invalid")

    auth_inert = {
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "transport_enabled": False,
        "record_is_execution_token": False,
    }
    for key, required in auth_inert.items():
        if auth.get(key) is not required:
            blockers.append(f"unsafe_or_missing_authorization_{key}")

    if isinstance(auth_hash, str) and auth_hash in set(seen_consumed_authorization_sha256):
        blockers.append("authorization_replay_or_double_consumption_detected")

    try:
        issued_at = _utc(str(auth.get("issued_at_utc")))
        expires_at = _utc(str(auth.get("expires_at_utc")))
        consumed_at = _utc(consumed_at_utc)
        if expires_at <= issued_at:
            blockers.append("authorization_expiry_not_after_issue")
        if consumed_at < issued_at:
            blockers.append("consumption_precedes_authorization_issue")
        if consumed_at >= expires_at:
            blockers.append("authorization_expired_before_consumption")
    except Exception:
        blockers.append("invalid_authorization_or_consumption_timestamp")

    blockers = list(dict.fromkeys(blockers))
    consumed = not blockers

    envelope = None
    if consumed:
        envelope_core = {
            "schema_version": 1,
            "mode": "single_use_real_transport_authorized_attempt_envelope",
            "attempt_state": "authorized_attempt_preflight_ready_no_network",
            "consumed_at_utc": consumed_at_utc,
            "authorization_expires_at_utc": auth.get("expires_at_utc"),
            "real_transport_authorization_verification_sha256": verification_hash,
            "real_transport_authorization_sha256": auth_hash,
            "pre_real_transport_review_sha256": verification.get("pre_real_transport_review_sha256"),
            "real_transport_decision_sha256": verification.get("real_transport_decision_sha256"),
            "exact_scope_sha256": verification.get("exact_scope_sha256"),
            "exact_scope": dict(scope),
            "mandatory_transport_gates": _transport_gates(),
            "max_network_requests": 1,
            "authorization_consumed": True,
            "authorization_reusable": False,
            "credentials_allowed": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "execution_enabled": False,
            "value_movement_enabled": False,
            "transport_adapter_present": False,
            "transport_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "envelope_is_network_result": False,
        }
        envelope = {**envelope_core, "authorized_attempt_envelope_sha256": _hash(envelope_core)}

    core = {
        "schema_version": 1,
        "mode": MODE,
        "consumption_state": "authorization_consumed_preflight_ready_no_network" if consumed else "authorization_consumption_rejected",
        "consumed_at_utc": consumed_at_utc,
        "real_transport_authorization_verification_sha256": verification_hash if isinstance(verification_hash, str) else None,
        "real_transport_authorization_sha256": auth_hash if isinstance(auth_hash, str) else None,
        "pre_real_transport_review_sha256": verification.get("pre_real_transport_review_sha256"),
        "real_transport_decision_sha256": verification.get("real_transport_decision_sha256"),
        "exact_scope_sha256": verification.get("exact_scope_sha256"),
        "authorization_consumed": consumed,
        "authorization_reusable": False,
        "authorized_attempt_envelope": envelope,
        "blockers": blockers,
        "transport_adapter_present": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "consumption_record_is_network_token": False,
    }
    return {**core, "real_transport_authorization_consumption_sha256": _hash(core)}
