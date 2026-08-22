from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_real_network_activation_request_builder"
_REQUEST_MODE = "real_network_activation_human_review_request"
_EXPECTED_AUDIT_MODE = "deterministic_network_adapter_implementation_binding_audit"
_EXPECTED_VALIDATION_MODE = "deterministic_network_capable_adapter_contract_validator"
_EXPECTED_READINESS_MODE = "network_capable_adapter_contract_readiness_artifact"


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


def _expected_interface(scope: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "interface_name": "execute_single_authorized_get",
        "activation_state": "defined_but_unreachable",
        "method": "GET",
        "max_network_requests": 1,
        "required_environment": "production",
        "target_fingerprint": scope.get("target_fingerprint"),
        "credentials_allowed": False,
        "action_enabled": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }


def build_real_network_activation_request(
    implementation_audit: Mapping[str, Any],
    contract_validation: Mapping[str, Any],
    *,
    requested_at: str,
    ttl_seconds: int = 300,
) -> dict[str, Any]:
    """Build a human-reviewable request only; never activates or invokes transport."""
    blockers: list[str] = []

    try:
        requested_dt = _parse_utc(requested_at)
    except Exception:
        requested_dt = None
        blockers.append("requested_at_invalid_or_not_utc")
    if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int) or not 60 <= ttl_seconds <= 900:
        blockers.append("ttl_out_of_range")

    audit_hash = implementation_audit.get("implementation_binding_audit_sha256")
    audit_core = dict(implementation_audit)
    audit_core.pop("implementation_binding_audit_sha256", None)
    if not isinstance(audit_hash, str) or audit_hash != _hash(audit_core):
        blockers.append("i077_audit_hash_invalid")
    if implementation_audit.get("mode") != _EXPECTED_AUDIT_MODE:
        blockers.append("i077_audit_mode_invalid")
    if (
        implementation_audit.get("audit_state") != "implementation_bound_review_ready_no_execution"
        or implementation_audit.get("blockers")
        or implementation_audit.get("implementation_binding_validated") is not True
    ):
        blockers.append("i077_audit_not_ready")

    for key, required in {
        "activation_reachable": False,
        "transport_callable_attached": False,
        "execution_entrypoint_reachable": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "audit_record_is_execution_token": False,
        "separate_real_network_activation_authorization_required": True,
    }.items():
        if implementation_audit.get(key) is not required:
            blockers.append(f"unsafe_or_missing_i077_{key}")

    validation_hash = contract_validation.get("network_adapter_contract_validation_sha256")
    validation_core = dict(contract_validation)
    validation_core.pop("network_adapter_contract_validation_sha256", None)
    if not isinstance(validation_hash, str) or validation_hash != _hash(validation_core):
        blockers.append("i076_validation_hash_invalid")
    if contract_validation.get("mode") != _EXPECTED_VALIDATION_MODE:
        blockers.append("i076_validation_mode_invalid")
    if (
        contract_validation.get("validation_state") != "adapter_contract_ready_for_separate_review_no_execution"
        or contract_validation.get("blockers")
        or contract_validation.get("adapter_contract_validated") is not True
    ):
        blockers.append("i076_validation_not_ready")
    if implementation_audit.get("network_adapter_contract_validation_sha256") != validation_hash:
        blockers.append("i077_i076_validation_binding_invalid")

    readiness = contract_validation.get("adapter_readiness_artifact")
    if not isinstance(readiness, Mapping):
        readiness = {}
        blockers.append("i076_readiness_missing")
    readiness_hash = readiness.get("adapter_contract_readiness_sha256")
    readiness_core = dict(readiness)
    readiness_core.pop("adapter_contract_readiness_sha256", None)
    if not isinstance(readiness_hash, str) or readiness_hash != _hash(readiness_core):
        blockers.append("i076_readiness_hash_invalid")
    if readiness.get("mode") != _EXPECTED_READINESS_MODE:
        blockers.append("i076_readiness_mode_invalid")
    if (
        readiness.get("readiness_state") != "adapter_contract_ready_for_separate_review_no_execution"
        or readiness.get("ready_for_real_network_execution") is not False
        or readiness.get("separate_human_review_required") is not True
    ):
        blockers.append("i076_readiness_not_review_only")
    if implementation_audit.get("adapter_contract_readiness_sha256") != readiness_hash:
        blockers.append("i077_readiness_binding_invalid")

    scope = readiness.get("exact_scope") if isinstance(readiness.get("exact_scope"), Mapping) else {}
    if not _exact_scope(scope):
        blockers.append("scope_not_exact_single_anonymous_production_get")
    interface = implementation_audit.get("future_activation_interface")
    expected_interface = _expected_interface(scope)
    if interface != expected_interface:
        blockers.append("i077_future_activation_interface_not_exact")
    if implementation_audit.get("adapter_id") != readiness.get("adapter_id"):
        blockers.append("adapter_id_binding_invalid")
    source_digest = implementation_audit.get("implementation_source_sha256")
    if not isinstance(source_digest, str) or len(source_digest) != 64:
        blockers.append("implementation_source_digest_invalid")

    lineage_keys = (
        "real_transport_authorization_consumption_sha256",
        "authorized_attempt_envelope_sha256",
        "real_transport_authorization_sha256",
        "pre_real_transport_review_sha256",
        "real_transport_decision_sha256",
        "exact_scope_sha256",
    )
    lineage = {key: readiness.get(key) for key in lineage_keys}
    for key, value in lineage.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"missing_lineage_{key}")

    blockers = list(dict.fromkeys(blockers))
    ready = not blockers
    request = None
    if ready and requested_dt is not None:
        expires_dt = requested_dt + timedelta(seconds=ttl_seconds)
        request_core = {
            "schema_version": 1,
            "mode": _REQUEST_MODE,
            "request_state": "ready_for_explicit_human_real_network_activation_decision",
            "requested_at": requested_dt.isoformat().replace("+00:00", "Z"),
            "expires_at": expires_dt.isoformat().replace("+00:00", "Z"),
            "ttl_seconds": ttl_seconds,
            "implementation_binding_audit_sha256": audit_hash,
            "implementation_source_sha256": source_digest,
            "network_adapter_contract_validation_sha256": validation_hash,
            "adapter_contract_readiness_sha256": readiness_hash,
            "adapter_id": readiness.get("adapter_id"),
            "exact_scope_sha256": readiness.get("exact_scope_sha256"),
            "exact_scope": dict(scope),
            "activation_interface": expected_interface,
            "authorization_lineage": lineage,
            "human_summary": {
                "operation": "one anonymous production GET only",
                "target_fingerprint": scope.get("target_fingerprint"),
                "credentials": "forbidden",
                "task_acceptance_or_submission": "forbidden",
                "value_movement": "forbidden",
                "adapter_source_digest": source_digest,
            },
            "explicit_human_decision_required": True,
            "activation_authorized": False,
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
        request = {**request_core, "real_network_activation_request_sha256": _hash(request_core)}

    core = {
        "schema_version": 1,
        "mode": MODE,
        "builder_state": "activation_request_ready_no_network" if ready else "activation_request_rejected",
        "implementation_binding_audit_sha256": audit_hash if isinstance(audit_hash, str) else None,
        "network_adapter_contract_validation_sha256": validation_hash if isinstance(validation_hash, str) else None,
        "adapter_contract_readiness_sha256": readiness_hash if isinstance(readiness_hash, str) else None,
        "real_network_activation_request": request,
        "blockers": blockers,
        "activation_authorized": False,
        "adapter_invoked": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "builder_record_is_execution_token": False,
    }
    return {**core, "real_network_activation_request_builder_sha256": _hash(core)}
