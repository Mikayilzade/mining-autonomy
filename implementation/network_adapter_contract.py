from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_network_capable_adapter_contract_validator"
_EXPECTED_CONSUMPTION_MODE = "deterministic_real_transport_authorization_consumption_preflight"
_EXPECTED_ENVELOPE_MODE = "single_use_real_transport_authorized_attempt_envelope"
_EXPECTED_ADAPTER_MODE = "network_capable_adapter_contract_declaration"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


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


def _required_transport_gates() -> dict[str, Any]:
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


def _required_request_contract(scope: Mapping[str, Any]) -> dict[str, Any]:
    return {
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


def validate_network_capable_adapter_contract(consumption: Mapping[str, Any], adapter_declaration: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []

    consumption_hash = consumption.get("real_transport_authorization_consumption_sha256")
    consumption_core = dict(consumption)
    consumption_core.pop("real_transport_authorization_consumption_sha256", None)
    if not isinstance(consumption_hash, str) or consumption_hash != _hash(consumption_core):
        blockers.append("i075_consumption_hash_invalid")
    if consumption.get("mode") != _EXPECTED_CONSUMPTION_MODE:
        blockers.append("i075_consumption_mode_invalid")
    if (
        consumption.get("consumption_state") != "authorization_consumed_preflight_ready_no_network"
        or consumption.get("blockers")
        or consumption.get("authorization_consumed") is not True
        or consumption.get("authorization_reusable") is not False
    ):
        blockers.append("i075_consumption_not_ready")

    consumption_inert = {
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
    for key, required in consumption_inert.items():
        if consumption.get(key) is not required:
            blockers.append(f"unsafe_or_missing_consumption_{key}")

    envelope = consumption.get("authorized_attempt_envelope")
    if not isinstance(envelope, Mapping):
        envelope = {}
        blockers.append("authorized_attempt_envelope_missing")

    envelope_hash = envelope.get("authorized_attempt_envelope_sha256")
    envelope_core = dict(envelope)
    envelope_core.pop("authorized_attempt_envelope_sha256", None)
    if not isinstance(envelope_hash, str) or envelope_hash != _hash(envelope_core):
        blockers.append("authorized_attempt_envelope_hash_invalid")
    if envelope.get("mode") != _EXPECTED_ENVELOPE_MODE:
        blockers.append("authorized_attempt_envelope_mode_invalid")
    if envelope.get("attempt_state") != "authorized_attempt_preflight_ready_no_network":
        blockers.append("authorized_attempt_envelope_state_invalid")
    if (
        envelope.get("authorization_consumed") is not True
        or envelope.get("authorization_reusable") is not False
        or envelope.get("max_network_requests") != 1
    ):
        blockers.append("authorized_attempt_single_use_or_request_limit_invalid")

    scope = envelope.get("exact_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("authorized_attempt_scope_missing")
    if not _exact_scope(scope):
        blockers.append("authorized_attempt_scope_not_exact_anonymous_get")

    for key in (
        "real_transport_authorization_verification_sha256",
        "real_transport_authorization_sha256",
        "pre_real_transport_review_sha256",
        "real_transport_decision_sha256",
        "exact_scope_sha256",
    ):
        if envelope.get(key) != consumption.get(key):
            blockers.append(f"authorized_attempt_{key}_binding_invalid")

    required_gates = _required_transport_gates()
    if envelope.get("mandatory_transport_gates") != required_gates:
        blockers.append("i075_mandatory_transport_gates_invalid")

    envelope_inert = {
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
    for key, required in envelope_inert.items():
        if envelope.get(key) is not required:
            blockers.append(f"unsafe_or_missing_envelope_{key}")

    declaration_hash = adapter_declaration.get("adapter_contract_sha256")
    declaration_core = dict(adapter_declaration)
    declaration_core.pop("adapter_contract_sha256", None)
    if not isinstance(declaration_hash, str) or declaration_hash != _hash(declaration_core):
        blockers.append("adapter_declaration_hash_invalid")
    if adapter_declaration.get("mode") != _EXPECTED_ADAPTER_MODE:
        blockers.append("adapter_declaration_mode_invalid")
    if not isinstance(adapter_declaration.get("adapter_id"), str) or not adapter_declaration.get("adapter_id"):
        blockers.append("adapter_id_missing")
    if adapter_declaration.get("network_capable") is not True:
        blockers.append("adapter_not_declared_network_capable")

    declaration_inert = {
        "execution_entrypoint_present": False,
        "execution_entrypoint_reachable": False,
        "transport_callable_attached": False,
        "execution_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_embedded": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }
    for key, required in declaration_inert.items():
        if adapter_declaration.get(key) is not required:
            blockers.append(f"unsafe_or_missing_adapter_{key}")

    if adapter_declaration.get("request_contract") != _required_request_contract(scope):
        blockers.append("adapter_request_contract_not_exact")
    if adapter_declaration.get("enforced_transport_gates") != required_gates:
        blockers.append("adapter_transport_gates_not_exact")
    if adapter_declaration.get("bound_authorized_attempt_envelope_sha256") != envelope_hash:
        blockers.append("adapter_envelope_hash_binding_invalid")
    if adapter_declaration.get("bound_exact_scope_sha256") != envelope.get("exact_scope_sha256"):
        blockers.append("adapter_scope_hash_binding_invalid")

    blockers = list(dict.fromkeys(blockers))
    ready = not blockers

    readiness = None
    if ready:
        readiness_core = {
            "schema_version": 1,
            "mode": "network_capable_adapter_contract_readiness_artifact",
            "readiness_state": "adapter_contract_ready_for_separate_review_no_execution",
            "adapter_id": adapter_declaration.get("adapter_id"),
            "adapter_contract_sha256": declaration_hash,
            "real_transport_authorization_consumption_sha256": consumption_hash,
            "authorized_attempt_envelope_sha256": envelope_hash,
            "real_transport_authorization_sha256": consumption.get("real_transport_authorization_sha256"),
            "pre_real_transport_review_sha256": consumption.get("pre_real_transport_review_sha256"),
            "real_transport_decision_sha256": consumption.get("real_transport_decision_sha256"),
            "exact_scope_sha256": consumption.get("exact_scope_sha256"),
            "exact_scope": dict(scope),
            "request_contract": _required_request_contract(scope),
            "enforced_transport_gates": required_gates,
            "network_capable_contract_declared": True,
            "execution_entrypoint_present": False,
            "execution_entrypoint_reachable": False,
            "transport_callable_attached": False,
            "ready_for_real_network_execution": False,
            "separate_human_review_required": True,
            "credentials_allowed": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "execution_enabled": False,
            "value_movement_enabled": False,
            "transport_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "readiness_artifact_is_execution_token": False,
        }
        readiness = {**readiness_core, "adapter_contract_readiness_sha256": _hash(readiness_core)}

    core = {
        "schema_version": 1,
        "mode": MODE,
        "validation_state": "adapter_contract_ready_for_separate_review_no_execution" if ready else "adapter_contract_rejected",
        "real_transport_authorization_consumption_sha256": consumption_hash if isinstance(consumption_hash, str) else None,
        "authorized_attempt_envelope_sha256": envelope_hash if isinstance(envelope_hash, str) else None,
        "adapter_contract_sha256": declaration_hash if isinstance(declaration_hash, str) else None,
        "adapter_id": adapter_declaration.get("adapter_id"),
        "adapter_readiness_artifact": readiness,
        "blockers": blockers,
        "adapter_contract_validated": ready,
        "execution_entrypoint_present": False,
        "execution_entrypoint_reachable": False,
        "transport_callable_attached": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "validation_record_is_execution_token": False,
    }
    return {**core, "network_adapter_contract_validation_sha256": _hash(core)}
