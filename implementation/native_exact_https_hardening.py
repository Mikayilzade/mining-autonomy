from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Callable, Mapping

from exact_https_target_binding import canonical_path_query


def _h(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _reseal(obj: Mapping[str, Any], key: str) -> dict[str, Any]:
    core = dict(obj)
    core.pop(key, None)
    return {**core, key: _h(core)}


def _bound_path(scope: Any, scope_hash: Any) -> tuple[str | None, str | None]:
    if not isinstance(scope, Mapping):
        return None, "exact_scope_missing"
    raw = scope.get("https_path_query")
    if not isinstance(raw, str):
        return None, "https_path_query_missing"
    try:
        path = canonical_path_query(raw)
    except ValueError:
        return None, "https_path_query_not_canonical"
    if path != raw:
        return None, "https_path_query_not_canonical"
    if scope_hash != _h(dict(scope)):
        return None, "exact_scope_hash_invalid"
    return path, None


def _reject_builder(result: Mapping[str, Any], *, blocker: str, builder_hash_key: str, packet_key: str | None = None, state_key: str | None = None, state_value: str | None = None) -> dict[str, Any]:
    out = dict(result)
    blockers = list(out.get("blockers", [])) if isinstance(out.get("blockers"), list) else []
    if blocker not in blockers:
        blockers.append(blocker)
    out["blockers"] = blockers
    if packet_key is not None:
        out[packet_key] = None
    if state_key is not None and state_value is not None:
        out[state_key] = state_value
    return _reseal(out, builder_hash_key)


def wrap_i086(original: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    def hardened(i084: Mapping[str, Any], i085: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
        env = i084.get("real_read_only_invocation_envelope") if isinstance(i084, Mapping) else None
        scope = env.get("exact_scope") if isinstance(env, Mapping) else None
        scope_hash = env.get("exact_scope_sha256") if isinstance(env, Mapping) else None
        path, error = _bound_path(scope, scope_hash)
        result = original(i084, i085, **kwargs)
        if error:
            return _reject_builder(result, blocker=f"native_{error}", builder_hash_key="final_real_observation_review_packet_builder_sha256", packet_key="final_real_observation_review_packet", state_key="builder_state", state_value="final_real_observation_review_packet_rejected")
        packet = result.get("final_real_observation_review_packet")
        if not isinstance(packet, Mapping) or result.get("blockers"):
            return result
        p = dict(packet)
        p["path_query"] = path
        p["userinfo_allowed"] = False
        p["fragment_allowed"] = False
        p = _reseal(p, "final_real_observation_review_packet_sha256")
        out = dict(result)
        out["final_real_observation_review_packet"] = p
        return _reseal(out, "final_real_observation_review_packet_builder_sha256")
    return hardened


def wrap_i087(original: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    def hardened(packet: Mapping[str, Any], decision: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
        scope = packet.get("exact_scope") if isinstance(packet, Mapping) else None
        path, error = _bound_path(scope, packet.get("exact_scope_sha256") if isinstance(packet, Mapping) else None)
        if error is None and packet.get("path_query") != path:
            error = "packet_path_query_binding_invalid"
        if error is None and decision.get("path_query") != path:
            error = "decision_path_query_binding_invalid"
        result = original(packet, decision, **kwargs)
        if error:
            return _reject_builder(result, blocker=f"native_{error}", builder_hash_key="final_real_observation_decision_verification_sha256", packet_key="final_real_observation_authorization", state_key="verification_state", state_value="decision_rejected")
        auth = result.get("final_real_observation_authorization")
        if not isinstance(auth, Mapping) or result.get("blockers"):
            return result
        a = dict(auth)
        a["path_query"] = path
        a["userinfo_allowed"] = False
        a["fragment_allowed"] = False
        a = _reseal(a, "final_real_observation_authorization_sha256")
        out = dict(result)
        out["final_real_observation_authorization"] = a
        return _reseal(out, "final_real_observation_decision_verification_sha256")
    return hardened


def wrap_i089(original: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    def hardened(i088: Mapping[str, Any], adapter_manifest: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
        env = i088.get("real_observation_execution_envelope") if isinstance(i088, Mapping) else None
        scope = env.get("exact_scope") if isinstance(env, Mapping) else None
        path, error = _bound_path(scope, env.get("exact_scope_sha256") if isinstance(env, Mapping) else None)
        if error is None and adapter_manifest.get("path_query") != path:
            error = "adapter_manifest_path_query_binding_invalid"
        result = original(i088, adapter_manifest, **kwargs)
        if error:
            return _reject_builder(result, blocker=f"native_{error}", builder_hash_key="final_network_adapter_invocation_gate_builder_sha256", packet_key="invocation_gate", state_key="gate_state", state_value="final_network_adapter_invocation_gate_rejected")
        gate = result.get("invocation_gate")
        if not isinstance(gate, Mapping) or result.get("blockers"):
            return result
        request = gate.get("request_spec")
        if not isinstance(request, Mapping):
            return _reject_builder(result, blocker="native_i089_request_spec_missing", builder_hash_key="final_network_adapter_invocation_gate_builder_sha256", packet_key="invocation_gate", state_key="gate_state", state_value="final_network_adapter_invocation_gate_rejected")
        req = dict(request)
        req["path"] = path
        g = dict(gate)
        g["request_spec"] = req
        g = _reseal(g, "final_network_adapter_invocation_gate_sha256")
        out = dict(result)
        out["invocation_gate"] = g
        return _reseal(out, "final_network_adapter_invocation_gate_builder_sha256")
    return hardened


def wrap_i090(original: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    def hardened(i089: Mapping[str, Any], transport: Callable[[Mapping[str, Any]], Mapping[str, Any]], **kwargs: Any) -> dict[str, Any]:
        gate = i089.get("invocation_gate") if isinstance(i089, Mapping) else None
        request = gate.get("request_spec") if isinstance(gate, Mapping) else None
        error = None
        if not isinstance(request, Mapping):
            error = "i089_request_spec_missing"
        else:
            raw = request.get("path")
            if not isinstance(raw, str):
                error = "https_path_query_missing"
            else:
                try:
                    if canonical_path_query(raw) != raw:
                        error = "https_path_query_not_canonical"
                except ValueError:
                    error = "https_path_query_not_canonical"
        if error:
            core = {
                "schema_version": 1,
                "mode": "deterministic_single_use_dependency_injected_transport_executor",
                "execution_state": "rejected_before_transport",
                "attempt_consumed": False,
                "invocation_receipt": None,
                "response_attestation": None,
                "blockers": [f"native_{error}"],
                "transport_callable_invoked": False,
                "network_requests_reported": 0,
                "credentials_used": False,
                "task_acceptance_enabled": False,
                "submission_enabled": False,
                "value_movement_enabled": False,
                "executor_is_payment_or_task_permission": False,
            }
            return {**core, "single_use_transport_executor_sha256": _h(core)}
        return original(i089, transport, **kwargs)
    return hardened
