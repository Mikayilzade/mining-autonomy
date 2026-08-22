from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

MODE = "deterministic_exact_real_read_only_invocation_authorization_consumption_preflight"
_ENVELOPE_MODE = "single_attempt_exact_real_read_only_invocation_envelope"
_RECEIPT_MODE = "single_use_exact_real_read_only_invocation_consumption_receipt"
_EXPECTED_AUTH_MODE = "single_use_exact_real_read_only_invocation_authorization"
_EXPECTED_DECISION_MODE = "explicit_exact_real_read_only_invocation_human_decision"
_EXPECTED_REQUEST_MODE = "exact_real_read_only_invocation_human_review_request"
_EXPECTED_REQUEST_STATE = "ready_for_fresh_explicit_human_real_read_only_invocation_decision"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


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


def _receipt_consumes_authorization(receipt: Mapping[str, Any], authorization_hash: str) -> bool:
    return (
        receipt.get("mode") == _RECEIPT_MODE
        and receipt.get("exact_real_read_only_invocation_authorization_sha256") == authorization_hash
        and receipt.get("consumption_state") == "consumed_once_no_network"
        and receipt.get("authorization_consumed") is True
    )


def consume_exact_real_read_only_invocation_authorization(
    invocation_request: Mapping[str, Any],
    invocation_decision: Mapping[str, Any],
    invocation_authorization: Mapping[str, Any],
    *,
    consumed_at: str,
    prior_consumption_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Consume one exact I083 authorization into an immutable zero-network one-attempt envelope."""
    blockers: list[str] = []

    try:
        consumed_dt = _parse_utc(consumed_at)
    except Exception:
        consumed_dt = None
        blockers.append("consumed_at_invalid_or_not_utc")

    request_hash = invocation_request.get("exact_real_read_only_invocation_request_sha256")
    request_core = dict(invocation_request)
    request_core.pop("exact_real_read_only_invocation_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(request_core):
        blockers.append("invocation_request_hash_invalid")
    if invocation_request.get("mode") != _EXPECTED_REQUEST_MODE:
        blockers.append("invocation_request_mode_invalid")
    if invocation_request.get("request_state") != _EXPECTED_REQUEST_STATE:
        blockers.append("invocation_request_not_ready")

    for key, required in {
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
    }.items():
        if invocation_request.get(key) is not required:
            blockers.append(f"unsafe_or_missing_request_{key}")

    request_scope = invocation_request.get("exact_scope")
    if not isinstance(request_scope, Mapping) or not _exact_scope(request_scope):
        blockers.append("invocation_request_scope_not_exact")
        request_scope = {}
    request_scope_hash = invocation_request.get("exact_scope_sha256")
    if not isinstance(request_scope_hash, str) or request_scope_hash != _hash(dict(request_scope)):
        blockers.append("invocation_request_scope_hash_invalid")

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
    digest = source_lineage.get("implementation_source_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
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
        request_expires_dt = _parse_utc(str(invocation_request.get("expires_at")))
        ttl = invocation_request.get("ttl_seconds")
        if request_expires_dt <= requested_dt:
            blockers.append("invocation_request_expiry_invalid")
        if isinstance(ttl, bool) or not isinstance(ttl, int) or not 60 <= ttl <= 900 or request_expires_dt != requested_dt + timedelta(seconds=ttl):
            blockers.append("invocation_request_ttl_invalid")
        if consumed_dt is not None and not (requested_dt <= consumed_dt <= request_expires_dt):
            blockers.append("invocation_request_expired_or_not_yet_valid_at_consumption")
    except Exception:
        requested_dt = request_expires_dt = None
        blockers.append("invocation_request_time_invalid")

    decision_hash = invocation_decision.get("exact_real_read_only_invocation_decision_sha256")
    decision_core = dict(invocation_decision)
    decision_core.pop("exact_real_read_only_invocation_decision_sha256", None)
    if not isinstance(decision_hash, str) or decision_hash != _hash(decision_core):
        blockers.append("invocation_decision_hash_invalid")
    if invocation_decision.get("mode") != _EXPECTED_DECISION_MODE:
        blockers.append("invocation_decision_mode_invalid")
    if invocation_decision.get("decision") != "authorize":
        blockers.append("invocation_decision_not_authorize")
    if invocation_decision.get("single_use") is not True:
        blockers.append("invocation_decision_not_single_use")
    if invocation_decision.get("exact_real_read_only_invocation_request_sha256") != request_hash:
        blockers.append("invocation_decision_request_binding_invalid")
    for key in binding_fields:
        if invocation_decision.get(key) != invocation_request.get(key):
            blockers.append(f"invocation_decision_{key}_binding_invalid")
    if invocation_decision.get("exact_scope") != dict(request_scope):
        blockers.append("invocation_decision_scope_binding_invalid")
    if invocation_decision.get("source_lineage") != dict(source_lineage):
        blockers.append("invocation_decision_source_lineage_binding_invalid")
    for key in ("credentials_allowed", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled"):
        if invocation_decision.get(key) is not False:
            blockers.append(f"invocation_decision_{key}_widened")
    try:
        decided_dt = _parse_utc(str(invocation_decision.get("decided_at")))
        if requested_dt is not None and request_expires_dt is not None and not (requested_dt <= decided_dt <= request_expires_dt):
            blockers.append("invocation_decision_outside_request_window")
        if consumed_dt is not None and decided_dt > consumed_dt:
            blockers.append("invocation_decision_from_future_at_consumption")
    except Exception:
        blockers.append("invocation_decision_time_invalid")

    auth_hash = invocation_authorization.get("exact_real_read_only_invocation_authorization_sha256")
    auth_core = dict(invocation_authorization)
    auth_core.pop("exact_real_read_only_invocation_authorization_sha256", None)
    if not isinstance(auth_hash, str) or auth_hash != _hash(auth_core):
        blockers.append("invocation_authorization_hash_invalid")
    if invocation_authorization.get("mode") != _EXPECTED_AUTH_MODE:
        blockers.append("invocation_authorization_mode_invalid")
    if invocation_authorization.get("authorization_state") != "authorized_single_use_not_consumed":
        blockers.append("invocation_authorization_state_invalid")
    if invocation_authorization.get("single_use") is not True:
        blockers.append("invocation_authorization_not_single_use")
    if invocation_authorization.get("consumed") is not False:
        blockers.append("invocation_authorization_already_consumed")
    if invocation_authorization.get("real_read_only_invocation_authorized") is not True:
        blockers.append("real_read_only_invocation_not_authorized")
    if invocation_authorization.get("max_network_requests") != 1:
        blockers.append("invocation_authorization_request_limit_invalid")
    if invocation_authorization.get("network_capable_adapter_reachable") is not False:
        blockers.append("invocation_authorization_adapter_reachability_widened")
    for key in ("transport_enabled", "network_enabled", "network_calls_performed", "credentials_allowed", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled"):
        if invocation_authorization.get(key) is not False:
            blockers.append(f"invocation_authorization_{key}_widened")
    if invocation_authorization.get("authorization_is_payment_or_task_permission") is not False:
        blockers.append("authorization_payment_or_task_scope_invalid")
    if invocation_authorization.get("authorization_is_execution_result") is not False:
        blockers.append("authorization_execution_result_invalid")
    if invocation_authorization.get("exact_real_read_only_invocation_request_sha256") != request_hash:
        blockers.append("invocation_authorization_request_binding_invalid")
    if invocation_authorization.get("exact_real_read_only_invocation_decision_sha256") != decision_hash:
        blockers.append("invocation_authorization_decision_binding_invalid")
    if invocation_authorization.get("decision_id") != invocation_decision.get("decision_id"):
        blockers.append("invocation_authorization_decision_id_binding_invalid")
    for key in binding_fields:
        if invocation_authorization.get(key) != invocation_request.get(key):
            blockers.append(f"invocation_authorization_{key}_binding_invalid")
    auth_scope = invocation_authorization.get("exact_scope")
    if not isinstance(auth_scope, Mapping) or dict(auth_scope) != dict(request_scope) or not _exact_scope(auth_scope):
        blockers.append("invocation_authorization_scope_not_exact")
    if invocation_authorization.get("source_lineage") != dict(source_lineage):
        blockers.append("invocation_authorization_source_lineage_binding_invalid")

    try:
        issued_dt = _parse_utc(str(invocation_authorization.get("issued_at")))
        auth_expires_dt = _parse_utc(str(invocation_authorization.get("expires_at")))
        if auth_expires_dt <= issued_dt:
            blockers.append("invocation_authorization_expiry_invalid")
        if consumed_dt is not None and not (issued_dt <= consumed_dt <= auth_expires_dt):
            blockers.append("invocation_authorization_expired_or_not_yet_valid")
        if request_expires_dt is not None and auth_expires_dt > request_expires_dt:
            blockers.append("invocation_authorization_outlives_request")
        if consumed_dt is not None and request_expires_dt is not None and consumed_dt > request_expires_dt:
            blockers.append("invocation_request_expired_at_consumption")
    except Exception:
        blockers.append("invocation_authorization_time_invalid")

    for prior in prior_consumption_receipts:
        if not isinstance(prior, Mapping):
            blockers.append("prior_consumption_receipt_malformed")
            continue
        prior_hash = prior.get("exact_real_read_only_invocation_consumption_receipt_sha256")
        prior_core = dict(prior)
        prior_core.pop("exact_real_read_only_invocation_consumption_receipt_sha256", None)
        if not isinstance(prior_hash, str) or prior_hash != _hash(prior_core):
            blockers.append("prior_consumption_receipt_hash_invalid")
            continue
        if _receipt_consumes_authorization(prior, str(auth_hash)):
            blockers.append("invocation_authorization_replay_detected")

    blockers = list(dict.fromkeys(blockers))
    envelope = None
    receipt = None
    state = "consumption_rejected"

    if not blockers and consumed_dt is not None:
        envelope_core = {
            "schema_version": 1,
            "mode": _ENVELOPE_MODE,
            "envelope_state": "one_attempt_bound_no_network",
            "created_at": consumed_dt.isoformat().replace("+00:00", "Z"),
            "exact_real_read_only_invocation_request_sha256": request_hash,
            "exact_real_read_only_invocation_decision_sha256": decision_hash,
            "exact_real_read_only_invocation_authorization_sha256": auth_hash,
            **{key: invocation_request.get(key) for key in binding_fields},
            "exact_scope": dict(request_scope),
            "source_lineage": dict(source_lineage),
            "max_adapter_invocations": 1,
            "max_network_requests": 1,
            "credentials_allowed": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
            "network_capable_adapter_reachable": False,
            "transport_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "adapter_invoked": False,
            "envelope_is_execution_result": False,
        }
        envelope = {
            **envelope_core,
            "exact_real_read_only_invocation_envelope_sha256": _hash(envelope_core),
        }
        receipt_core = {
            "schema_version": 1,
            "mode": _RECEIPT_MODE,
            "consumption_state": "consumed_once_no_network",
            "consumed_at": consumed_dt.isoformat().replace("+00:00", "Z"),
            "exact_real_read_only_invocation_request_sha256": request_hash,
            "exact_real_read_only_invocation_decision_sha256": decision_hash,
            "exact_real_read_only_invocation_authorization_sha256": auth_hash,
            "exact_real_read_only_invocation_envelope_sha256": envelope["exact_real_read_only_invocation_envelope_sha256"],
            "adapter_id": invocation_request.get("adapter_id"),
            "exact_scope_sha256": invocation_request.get("exact_scope_sha256"),
            "authorization_consumed": True,
            "network_capable_adapter_reachable": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "credentials_used": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
            "receipt_is_execution_token": False,
        }
        receipt = {
            **receipt_core,
            "exact_real_read_only_invocation_consumption_receipt_sha256": _hash(receipt_core),
        }
        state = "authorization_consumed_once_envelope_ready_no_network"

    core = {
        "schema_version": 1,
        "mode": MODE,
        "consumption_state": state,
        "exact_real_read_only_invocation_request_sha256": request_hash if isinstance(request_hash, str) else None,
        "exact_real_read_only_invocation_decision_sha256": decision_hash if isinstance(decision_hash, str) else None,
        "exact_real_read_only_invocation_authorization_sha256": auth_hash if isinstance(auth_hash, str) else None,
        "real_read_only_invocation_envelope": envelope,
        "consumption_receipt": receipt,
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
        "consumption_record_is_execution_token": False,
    }
    return {
        **core,
        "exact_real_read_only_invocation_consumption_preflight_sha256": _hash(core),
    }
