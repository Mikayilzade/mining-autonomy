from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

MODE = "deterministic_real_network_activation_authorization_consumption_preflight"
_ENVELOPE_MODE = "single_attempt_real_network_activation_envelope"
_RECEIPT_MODE = "single_use_real_network_activation_consumption_receipt"
_EXPECTED_AUTH_MODE = "single_use_real_network_activation_authorization"
_EXPECTED_REQUEST_MODE = "real_network_activation_human_review_request"


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
        and receipt.get("real_network_activation_authorization_sha256") == authorization_hash
        and receipt.get("consumption_state") == "consumed_once_no_network"
    )


def consume_real_network_activation_authorization(
    activation_request: Mapping[str, Any],
    activation_authorization: Mapping[str, Any],
    *,
    consumed_at: str,
    prior_consumption_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Consume one exact I079 authorization into a zero-network, one-attempt envelope."""
    blockers: list[str] = []

    try:
        consumed_dt = _parse_utc(consumed_at)
    except Exception:
        consumed_dt = None
        blockers.append("consumed_at_invalid_or_not_utc")

    request_hash = activation_request.get("real_network_activation_request_sha256")
    request_core = dict(activation_request)
    request_core.pop("real_network_activation_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(request_core):
        blockers.append("activation_request_hash_invalid")
    if activation_request.get("mode") != _EXPECTED_REQUEST_MODE:
        blockers.append("activation_request_mode_invalid")
    if activation_request.get("request_state") != "ready_for_explicit_human_real_network_activation_decision":
        blockers.append("activation_request_not_ready")

    request_scope = activation_request.get("exact_scope")
    if not isinstance(request_scope, Mapping) or not _exact_scope(request_scope):
        blockers.append("activation_request_scope_not_exact")
        request_scope = {}

    auth_hash = activation_authorization.get("real_network_activation_authorization_sha256")
    auth_core = dict(activation_authorization)
    auth_core.pop("real_network_activation_authorization_sha256", None)
    if not isinstance(auth_hash, str) or auth_hash != _hash(auth_core):
        blockers.append("activation_authorization_hash_invalid")
    if activation_authorization.get("mode") != _EXPECTED_AUTH_MODE:
        blockers.append("activation_authorization_mode_invalid")
    if activation_authorization.get("authorization_state") != "authorized_single_use_not_consumed":
        blockers.append("activation_authorization_state_invalid")
    if activation_authorization.get("single_use") is not True:
        blockers.append("activation_authorization_not_single_use")
    if activation_authorization.get("consumed") is not False:
        blockers.append("activation_authorization_already_consumed")
    if activation_authorization.get("max_network_requests") != 1:
        blockers.append("activation_authorization_request_limit_invalid")
    if activation_authorization.get("adapter_invocation_authorized") is not True:
        blockers.append("adapter_invocation_not_authorized")
    for key in ("credentials_allowed", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled"):
        if activation_authorization.get(key) is not False:
            blockers.append(f"activation_authorization_{key}_widened")
    if activation_authorization.get("authorization_is_payment_or_task_permission") is not False:
        blockers.append("authorization_payment_or_task_scope_invalid")

    if activation_authorization.get("real_network_activation_request_sha256") != request_hash:
        blockers.append("activation_authorization_request_binding_invalid")

    binding_fields = (
        "implementation_binding_audit_sha256",
        "implementation_source_sha256",
        "network_adapter_contract_validation_sha256",
        "adapter_contract_readiness_sha256",
        "adapter_id",
        "exact_scope_sha256",
    )
    for key in binding_fields:
        if activation_authorization.get(key) != activation_request.get(key):
            blockers.append(f"activation_authorization_{key}_binding_invalid")

    auth_scope = activation_authorization.get("exact_scope")
    if not isinstance(auth_scope, Mapping) or dict(auth_scope) != dict(request_scope) or not _exact_scope(auth_scope):
        blockers.append("activation_authorization_scope_not_exact")

    request_lineage = activation_request.get("authorization_lineage")
    auth_lineage = activation_authorization.get("authorization_lineage")
    if not isinstance(request_lineage, Mapping) or not request_lineage:
        blockers.append("activation_request_lineage_missing")
        request_lineage = {}
    if not isinstance(auth_lineage, Mapping) or dict(auth_lineage) != dict(request_lineage):
        blockers.append("activation_authorization_lineage_binding_invalid")

    try:
        issued_dt = _parse_utc(str(activation_authorization.get("issued_at")))
        expires_dt = _parse_utc(str(activation_authorization.get("expires_at")))
        if expires_dt <= issued_dt:
            blockers.append("activation_authorization_expiry_invalid")
        if consumed_dt is not None and not (issued_dt <= consumed_dt <= expires_dt):
            blockers.append("activation_authorization_expired_or_not_yet_valid")
    except Exception:
        issued_dt = expires_dt = None
        blockers.append("activation_authorization_time_invalid")

    try:
        request_expires_dt = _parse_utc(str(activation_request.get("expires_at")))
        if expires_dt is not None and expires_dt > request_expires_dt:
            blockers.append("activation_authorization_outlives_request")
        if consumed_dt is not None and consumed_dt > request_expires_dt:
            blockers.append("activation_request_expired_at_consumption")
    except Exception:
        blockers.append("activation_request_time_invalid")

    for receipt in prior_consumption_receipts:
        if not isinstance(receipt, Mapping):
            blockers.append("prior_consumption_receipt_malformed")
            continue
        receipt_hash = receipt.get("real_network_activation_consumption_receipt_sha256")
        receipt_core = dict(receipt)
        receipt_core.pop("real_network_activation_consumption_receipt_sha256", None)
        if not isinstance(receipt_hash, str) or receipt_hash != _hash(receipt_core):
            blockers.append("prior_consumption_receipt_hash_invalid")
            continue
        if _receipt_consumes_authorization(receipt, str(auth_hash)):
            blockers.append("activation_authorization_replay_detected")

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
            "real_network_activation_authorization_sha256": auth_hash,
            "real_network_activation_request_sha256": request_hash,
            **{key: activation_request.get(key) for key in binding_fields},
            "exact_scope": dict(request_scope),
            "authorization_lineage": dict(request_lineage),
            "max_adapter_invocations": 1,
            "max_network_requests": 1,
            "credentials_allowed": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
            "transport_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "adapter_invoked": False,
            "envelope_is_execution_result": False,
        }
        envelope = {**envelope_core, "real_network_activation_envelope_sha256": _hash(envelope_core)}
        receipt_core = {
            "schema_version": 1,
            "mode": _RECEIPT_MODE,
            "consumption_state": "consumed_once_no_network",
            "consumed_at": consumed_dt.isoformat().replace("+00:00", "Z"),
            "real_network_activation_authorization_sha256": auth_hash,
            "real_network_activation_request_sha256": request_hash,
            "real_network_activation_envelope_sha256": envelope["real_network_activation_envelope_sha256"],
            "adapter_id": activation_request.get("adapter_id"),
            "exact_scope_sha256": activation_request.get("exact_scope_sha256"),
            "authorization_consumed": True,
            "network_enabled": False,
            "network_calls_performed": False,
            "value_movement_enabled": False,
            "receipt_is_execution_token": False,
        }
        receipt = {**receipt_core, "real_network_activation_consumption_receipt_sha256": _hash(receipt_core)}
        state = "authorization_consumed_once_envelope_ready_no_network"

    core = {
        "schema_version": 1,
        "mode": MODE,
        "consumption_state": state,
        "real_network_activation_authorization_sha256": auth_hash if isinstance(auth_hash, str) else None,
        "real_network_activation_request_sha256": request_hash if isinstance(request_hash, str) else None,
        "activation_envelope": envelope,
        "consumption_receipt": receipt,
        "blockers": blockers,
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
    return {**core, "real_network_activation_consumption_preflight_sha256": _hash(core)}
