from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_network_adapter_implementation_binding_audit"
_EXPECTED_VALIDATION_MODE = "deterministic_network_capable_adapter_contract_validator"
_EXPECTED_READINESS_MODE = "network_capable_adapter_contract_readiness_artifact"
_EXPECTED_MANIFEST_MODE = "inert_https_json_adapter_implementation_manifest"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _source_hash(source_text: str) -> str:
    return sha256(source_text.encode("utf-8")).hexdigest()


def _future_interface(scope: Mapping[str, Any]) -> dict[str, Any]:
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


def build_inert_implementation_manifest(readiness: Mapping[str, Any], source_text: str, *, module_path: str = "implementation/future_https_json_adapter.py") -> dict[str, Any]:
    scope = readiness.get("exact_scope") if isinstance(readiness.get("exact_scope"), Mapping) else {}
    core = {
        "schema_version": 1,
        "mode": _EXPECTED_MANIFEST_MODE,
        "adapter_id": readiness.get("adapter_id"),
        "module_path": module_path,
        "language": "python",
        "source_sha256": _source_hash(source_text),
        "bound_adapter_contract_readiness_sha256": readiness.get("adapter_contract_readiness_sha256"),
        "bound_adapter_contract_sha256": readiness.get("adapter_contract_sha256"),
        "bound_authorized_attempt_envelope_sha256": readiness.get("authorized_attempt_envelope_sha256"),
        "bound_exact_scope_sha256": readiness.get("exact_scope_sha256"),
        "future_activation_interface": _future_interface(scope),
        "import_side_effects_allowed": False,
        "network_library_imported": False,
        "transport_callable_attached": False,
        "execution_entrypoint_present": False,
        "execution_entrypoint_reachable": False,
        "activation_reachable": False,
        "credentials_embedded": False,
        "execution_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }
    return {**core, "implementation_manifest_sha256": _hash(core)}


def audit_adapter_implementation_binding(validation: Mapping[str, Any], manifest: Mapping[str, Any], source_text: str) -> dict[str, Any]:
    blockers: list[str] = []

    validation_hash = validation.get("network_adapter_contract_validation_sha256")
    validation_core = dict(validation)
    validation_core.pop("network_adapter_contract_validation_sha256", None)
    if not isinstance(validation_hash, str) or validation_hash != _hash(validation_core):
        blockers.append("i076_validation_hash_invalid")
    if validation.get("mode") != _EXPECTED_VALIDATION_MODE:
        blockers.append("i076_validation_mode_invalid")
    if validation.get("validation_state") != "adapter_contract_ready_for_separate_review_no_execution" or validation.get("blockers") or validation.get("adapter_contract_validated") is not True:
        blockers.append("i076_validation_not_ready")

    readiness = validation.get("adapter_readiness_artifact")
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
    if readiness.get("readiness_state") != "adapter_contract_ready_for_separate_review_no_execution" or readiness.get("ready_for_real_network_execution") is not False:
        blockers.append("i076_readiness_state_invalid")

    for key in ("adapter_id", "adapter_contract_sha256", "authorized_attempt_envelope_sha256"):
        if readiness.get(key) != validation.get(key):
            blockers.append(f"i076_{key}_binding_invalid")

    scope = readiness.get("exact_scope") if isinstance(readiness.get("exact_scope"), Mapping) else {}
    if not (
        scope.get("method") == "GET" and scope.get("request_count") == 1 and scope.get("required_environment") == "production"
        and isinstance(scope.get("target_fingerprint"), str) and bool(scope.get("target_fingerprint"))
        and scope.get("credentials_allowed") is False and scope.get("action_enabled") is False
    ):
        blockers.append("i076_scope_not_exact_anonymous_get")

    manifest_hash = manifest.get("implementation_manifest_sha256")
    manifest_core = dict(manifest)
    manifest_core.pop("implementation_manifest_sha256", None)
    if not isinstance(manifest_hash, str) or manifest_hash != _hash(manifest_core):
        blockers.append("implementation_manifest_hash_invalid")
    if manifest.get("mode") != _EXPECTED_MANIFEST_MODE:
        blockers.append("implementation_manifest_mode_invalid")
    if manifest.get("adapter_id") != readiness.get("adapter_id"):
        blockers.append("implementation_adapter_id_binding_invalid")
    if manifest.get("bound_adapter_contract_readiness_sha256") != readiness_hash:
        blockers.append("implementation_readiness_hash_binding_invalid")
    if manifest.get("bound_adapter_contract_sha256") != readiness.get("adapter_contract_sha256"):
        blockers.append("implementation_contract_hash_binding_invalid")
    if manifest.get("bound_authorized_attempt_envelope_sha256") != readiness.get("authorized_attempt_envelope_sha256"):
        blockers.append("implementation_envelope_hash_binding_invalid")
    if manifest.get("bound_exact_scope_sha256") != readiness.get("exact_scope_sha256"):
        blockers.append("implementation_scope_hash_binding_invalid")
    if manifest.get("source_sha256") != _source_hash(source_text):
        blockers.append("implementation_source_digest_mismatch")
    if not isinstance(manifest.get("module_path"), str) or not manifest.get("module_path"):
        blockers.append("implementation_module_path_missing")
    if manifest.get("language") != "python":
        blockers.append("implementation_language_not_python")
    if manifest.get("future_activation_interface") != _future_interface(scope):
        blockers.append("future_activation_interface_not_exact")

    required_inert = {
        "import_side_effects_allowed": False,
        "network_library_imported": False,
        "transport_callable_attached": False,
        "execution_entrypoint_present": False,
        "execution_entrypoint_reachable": False,
        "activation_reachable": False,
        "credentials_embedded": False,
        "execution_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }
    for key, required in required_inert.items():
        if manifest.get(key) is not required:
            blockers.append(f"unsafe_or_missing_manifest_{key}")

    forbidden_source_markers = (
        "import requests", "from requests", "import httpx", "from httpx", "import aiohttp", "from aiohttp",
        "import socket", "from socket", "urllib.request", "http.client", "subprocess.", "os.system(",
    )
    lowered = source_text.lower()
    if any(marker in lowered for marker in forbidden_source_markers):
        blockers.append("network_or_process_transport_surface_present_in_source")
    if "def execute_single_authorized_get" not in source_text:
        blockers.append("future_activation_interface_definition_missing")
    if "raise RuntimeError(\"real_network_activation_not_enabled\")" not in source_text:
        blockers.append("future_activation_interface_not_fail_closed")

    blockers = list(dict.fromkeys(blockers))
    ready = not blockers
    audit_core = {
        "schema_version": 1,
        "mode": MODE,
        "audit_state": "implementation_bound_review_ready_no_execution" if ready else "implementation_binding_rejected",
        "network_adapter_contract_validation_sha256": validation_hash if isinstance(validation_hash, str) else None,
        "adapter_contract_readiness_sha256": readiness_hash if isinstance(readiness_hash, str) else None,
        "implementation_manifest_sha256": manifest_hash if isinstance(manifest_hash, str) else None,
        "implementation_source_sha256": _source_hash(source_text),
        "adapter_id": manifest.get("adapter_id"),
        "future_activation_interface": _future_interface(scope) if ready else None,
        "blockers": blockers,
        "implementation_binding_validated": ready,
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
    }
    return {**audit_core, "implementation_binding_audit_sha256": _hash(audit_core)}
