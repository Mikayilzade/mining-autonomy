from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping
from urllib.parse import urlsplit

MODE = "deterministic_exact_https_target_binding_repair"
BOUND_MODE = "canonical_exact_https_path_query_binding"


def _h(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _hash_ok(obj: Mapping[str, Any], key: str) -> bool:
    core = dict(obj)
    got = core.pop(key, None)
    return isinstance(got, str) and got == _h(core)


def canonical_path_query(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("path_query_must_be_string")
    if not value:
        return "/"
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in value):
        raise ValueError("path_query_control_character")
    if any(c.isspace() for c in value):
        raise ValueError("path_query_whitespace")
    if "\\" in value or "#" in value:
        raise ValueError("path_query_forbidden_character")
    if not value.startswith("/") or value.startswith("//"):
        raise ValueError("path_query_must_be_origin_form")
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or parsed.fragment:
        raise ValueError("path_query_not_relative_origin_form")
    path = parsed.path or "/"
    return path + (("?" + parsed.query) if parsed.query else "")


def build_exact_https_target_binding(*, hostname: str, path_query: str, target_fingerprint: str, adapter_id: str, exact_scope: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    host = str(hostname).strip().lower().rstrip(".") if isinstance(hostname, str) else ""
    if not host or any(c.isspace() for c in host) or any(x in host for x in "/:@?#"):
        blockers.append("hostname_invalid")
    try:
        pq = canonical_path_query(path_query)
    except ValueError as exc:
        pq = None
        blockers.append(str(exc))
    if not isinstance(target_fingerprint, str) or not target_fingerprint:
        blockers.append("target_fingerprint_invalid")
    if not isinstance(adapter_id, str) or not adapter_id:
        blockers.append("adapter_id_invalid")
    scope = dict(exact_scope) if isinstance(exact_scope, Mapping) else {}
    if not (scope.get("method") == "GET" and scope.get("request_count") == 1 and scope.get("required_environment") == "production" and scope.get("credentials_allowed") is False and scope.get("action_enabled") is False and scope.get("target_fingerprint") == target_fingerprint):
        blockers.append("exact_scope_not_one_readonly_production_get")
    binding = None
    if not blockers and pq is not None:
        bound_scope = dict(scope)
        bound_scope["https_path_query"] = pq
        bound_scope_sha = _h(bound_scope)
        core = {"schema_version":1,"mode":BOUND_MODE,"scheme":"https","hostname":host,"path_query":pq,"request_target":f"https://{host}{pq}","adapter_id":adapter_id,"target_fingerprint":target_fingerprint,"bound_exact_scope":bound_scope,"bound_exact_scope_sha256":bound_scope_sha,"userinfo_allowed":False,"fragment_allowed":False,"out_of_band_target_components_allowed":False}
        binding = {**core,"exact_https_target_binding_sha256":_h(core)}
    out = {"schema_version":1,"mode":MODE,"binding_state":"canonical_exact_target_bound" if binding else "rejected","target_binding":binding,"blockers":list(dict.fromkeys(blockers)),"network_enabled":False,"network_calls_performed":False,"value_movement_enabled":False}
    return {**out,"exact_https_target_binding_repair_sha256":_h(out)}


def propagate_binding(binding: Mapping[str, Any], *, review_packet: Mapping[str, Any], authorization: Mapping[str, Any], execution_envelope: Mapping[str, Any], adapter_manifest: Mapping[str, Any], i089_gate: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if not _hash_ok(binding, "exact_https_target_binding_sha256") or binding.get("mode") != BOUND_MODE:
        blockers.append("binding_invalid")
    pq = binding.get("path_query"); host = binding.get("hostname"); scope_hash = binding.get("bound_exact_scope_sha256"); target = binding.get("target_fingerprint"); adapter = binding.get("adapter_id")
    artifacts = {"review_packet":review_packet,"authorization":authorization,"execution_envelope":execution_envelope,"adapter_manifest":adapter_manifest}
    for name, obj in artifacts.items():
        if not isinstance(obj, Mapping):
            blockers.append(f"{name}_missing"); continue
        for key, expected in (("hostname",host),("path_query",pq),("target_fingerprint",target),("adapter_id",adapter),("exact_scope_sha256",scope_hash)):
            if obj.get(key) != expected: blockers.append(f"{name}_{key}_binding_invalid")
        scope = obj.get("exact_scope")
        if name != "adapter_manifest" and (not isinstance(scope, Mapping) or scope.get("https_path_query") != pq or _h(dict(scope)) != scope_hash):
            blockers.append(f"{name}_exact_scope_binding_invalid")
        if obj.get("userinfo_allowed", False) is not False: blockers.append(f"{name}_userinfo_widened")
        if obj.get("fragment_allowed", False) is not False: blockers.append(f"{name}_fragment_widened")
    request = i089_gate.get("request_spec") if isinstance(i089_gate, Mapping) else None
    if not isinstance(request, Mapping): blockers.append("i089_request_spec_missing")
    else:
        for key, expected in (("hostname",host),("path",pq),("target_fingerprint",target),("adapter_id",adapter),("exact_scope_sha256",scope_hash)):
            if request.get(key) != expected: blockers.append(f"i089_request_spec_{key}_binding_invalid")
        try:
            if canonical_path_query(request.get("path")) != pq: blockers.append("i089_request_spec_path_not_canonical")
        except ValueError: blockers.append("i089_request_spec_path_not_canonical")
    core = {"schema_version":1,"mode":"deterministic_exact_target_lineage_validation","validation_state":"exact_target_unchanged_ready_for_i090" if not blockers else "rejected","exact_https_target_binding_sha256":binding.get("exact_https_target_binding_sha256"),"path_query":pq,"hostname":host,"bound_exact_scope_sha256":scope_hash,"blockers":list(dict.fromkeys(blockers)),"network_enabled":False,"network_calls_performed":False,"value_movement_enabled":False}
    return {**core,"exact_target_lineage_validation_sha256":_h(core)}


def validate_i090_request_unchanged(validation: Mapping[str, Any], request_spec: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if not _hash_ok(validation, "exact_target_lineage_validation_sha256") or validation.get("validation_state") != "exact_target_unchanged_ready_for_i090":
        return ["lineage_validation_not_ready"]
    expected = validation.get("path_query")
    if request_spec.get("path") != expected: blockers.append("i090_path_query_drift")
    try:
        if canonical_path_query(request_spec.get("path")) != expected: blockers.append("i090_path_query_not_canonical")
    except ValueError: blockers.append("i090_path_query_not_canonical")
    if request_spec.get("hostname") != validation.get("hostname"): blockers.append("i090_hostname_drift")
    if request_spec.get("exact_scope_sha256") != validation.get("bound_exact_scope_sha256"): blockers.append("i090_exact_scope_drift")
    return list(dict.fromkeys(blockers))
