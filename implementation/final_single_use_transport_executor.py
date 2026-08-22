from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import ipaddress
import json
from typing import Any, Callable, Iterable, Mapping

MODE = "deterministic_single_use_dependency_injected_transport_executor"
I089_MODE = "deterministic_final_network_adapter_invocation_gate"
I089_GATE_MODE = "single_attempt_dependency_injected_network_adapter_gate"
RECEIPT_MODE = "single_use_final_network_adapter_invocation_receipt"
ATTESTATION_MODE = "single_use_readonly_json_response_attestation"
MAX_CLOCK_SKEW_SECONDS = 5


def _h(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _hash_ok(obj: Mapping[str, Any], key: str) -> bool:
    core = dict(obj)
    got = core.pop(key, None)
    return isinstance(got, str) and got == _h(core)


def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise ValueError("timestamp_must_be_utc")
    return dt.astimezone(timezone.utc)


def _public_ip(value: Any) -> bool:
    try:
        addr = ipaddress.ip_address(str(value))
        return addr.is_global and not any(
            (addr.is_private, addr.is_loopback, addr.is_link_local, addr.is_multicast, addr.is_reserved, addr.is_unspecified)
        )
    except ValueError:
        return False


def _prior_consumes(receipt: Mapping[str, Any], envelope_hash: str, authorization_hash: str) -> bool:
    return (
        receipt.get("mode") == RECEIPT_MODE
        and receipt.get("invocation_state") in {"invoked_once", "attempted_once_result_rejected", "attempted_once_transport_error"}
        and receipt.get("final_real_observation_execution_envelope_sha256") == envelope_hash
        and receipt.get("final_real_observation_authorization_sha256") == authorization_hash
        and receipt.get("one_shot_consumed") is True
    )


def _make_receipt(gate: Mapping[str, Any], *, invoked_at: str, state: str, outcome: str) -> dict[str, Any]:
    core = {
        "schema_version": 1,
        "mode": RECEIPT_MODE,
        "invocation_state": state,
        "invoked_at": invoked_at,
        "final_network_adapter_invocation_gate_sha256": gate.get("final_network_adapter_invocation_gate_sha256"),
        "final_real_observation_execution_envelope_sha256": gate.get("i088_execution_envelope_sha256"),
        "final_real_observation_authorization_sha256": gate.get("final_real_observation_authorization_sha256"),
        "network_adapter_manifest_sha256": gate.get("network_adapter_manifest_sha256"),
        "target_fingerprint": gate.get("request_spec", {}).get("target_fingerprint"),
        "attempt_outcome": outcome,
        "one_shot_consumed": True,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
        "receipt_is_payment_or_task_permission": False,
    }
    return {**core, "final_network_adapter_invocation_receipt_sha256": _h(core)}


def execute_single_use_dependency_injected_transport(
    i089: Mapping[str, Any],
    transport: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    *,
    invoked_at: str,
    prior_invocation_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Consume one I089 gate attempt through an injected transport boundary.

    This function never performs DNS/HTTP itself. The caller supplies the transport callable.
    Tests use a synthetic injected transport; any future real transport remains outside this
    module's authorization authority and must come from a fresh separately authorized chain.
    """
    blockers: list[str] = []
    try:
        now = _utc(invoked_at)
    except Exception:
        now = None
        blockers.append("invoked_at_invalid_or_not_utc")

    if not _hash_ok(i089, "final_network_adapter_invocation_gate_builder_sha256"):
        blockers.append("i089_builder_hash_invalid")
    if i089.get("mode") != I089_MODE or i089.get("gate_state") != "final_network_adapter_invocation_gate_ready_no_call":
        blockers.append("i089_not_ready")
    if i089.get("blockers"):
        blockers.append("i089_has_blockers")
    for key in ("network_transport_invoked", "network_calls_performed", "credentials_used", "task_acceptance_enabled", "submission_enabled", "execution_enabled", "value_movement_enabled", "gate_record_is_execution_token"):
        if i089.get(key) is not False:
            blockers.append(f"i089_{key}_must_be_false")

    gate = i089.get("invocation_gate")
    if not isinstance(gate, Mapping):
        blockers.append("i089_invocation_gate_missing")
        gate = {}
    if not _hash_ok(gate, "final_network_adapter_invocation_gate_sha256"):
        blockers.append("i089_invocation_gate_hash_invalid")
    if gate.get("mode") != I089_GATE_MODE or gate.get("gate_state") != "validated_ready_for_single_dependency_injected_network_invocation":
        blockers.append("i089_invocation_gate_state_invalid")
    if gate.get("max_adapter_invocations") != 1 or gate.get("max_network_requests") != 1:
        blockers.append("i089_invocation_limits_invalid")
    if gate.get("dependency_injected_transport_boundary_required") is not True:
        blockers.append("i089_dependency_injected_boundary_not_required")
    for key in ("network_transport_invoked", "network_calls_performed", "credentials_used", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled", "gate_is_execution_result", "gate_is_payment_or_task_permission"):
        if gate.get(key) is not False:
            blockers.append(f"i089_gate_{key}_must_be_false")

    request = gate.get("request_spec")
    if not isinstance(request, Mapping):
        blockers.append("i089_request_spec_missing")
        request = {}
    required_request = {
        "scheme": "https", "tls_required": True, "method": "GET", "max_network_requests": 1,
        "allow_redirects": False, "max_redirects": 0, "allowed_content_types": ["application/json"],
        "credentials_allowed": False, "action_enabled": False,
    }
    for key, value in required_request.items():
        if request.get(key) != value:
            blockers.append(f"request_spec_{key}_invalid")
    max_bytes = request.get("max_response_bytes")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or not 1 <= max_bytes <= 1_048_576:
        blockers.append("request_spec_max_response_bytes_invalid")
    hostname = request.get("hostname")
    if not isinstance(hostname, str) or not hostname or any(c.isspace() for c in hostname):
        blockers.append("request_spec_hostname_invalid")
    pins = request.get("pinned_addresses")
    if not isinstance(pins, list) or not pins or len({str(x) for x in pins}) != len(pins) or any(not _public_ip(x) for x in pins):
        blockers.append("request_spec_pinned_addresses_invalid")
        pins = []

    if now is not None:
        try:
            gated_at = _utc(str(gate.get("gated_at")))
            expires_at = _utc(str(gate.get("expires_at")))
            if now + timedelta(seconds=MAX_CLOCK_SKEW_SECONDS) < gated_at:
                blockers.append("invocation_before_gate_time")
            if now > expires_at:
                blockers.append("invocation_gate_expired")
        except Exception:
            blockers.append("invocation_gate_time_invalid")

    envelope_hash = str(gate.get("i088_execution_envelope_sha256", ""))
    authorization_hash = str(gate.get("final_real_observation_authorization_sha256", ""))
    for prior in prior_invocation_receipts:
        if not isinstance(prior, Mapping):
            blockers.append("prior_invocation_receipt_malformed")
            continue
        if not _hash_ok(prior, "final_network_adapter_invocation_receipt_sha256"):
            blockers.append("prior_invocation_receipt_hash_invalid")
            continue
        if _prior_consumes(prior, envelope_hash, authorization_hash):
            blockers.append("final_network_adapter_invocation_replay_detected")

    blockers = list(dict.fromkeys(blockers))
    if blockers or now is None:
        core = {
            "schema_version": 1, "mode": MODE, "execution_state": "rejected_before_transport",
            "attempt_consumed": False, "invocation_receipt": None, "response_attestation": None,
            "blockers": blockers, "transport_callable_invoked": False, "network_requests_reported": 0,
            "credentials_used": False, "task_acceptance_enabled": False, "submission_enabled": False,
            "value_movement_enabled": False, "executor_is_payment_or_task_permission": False,
        }
        return {**core, "single_use_transport_executor_sha256": _h(core)}

    invoked_iso = now.isoformat().replace("+00:00", "Z")
    try:
        result = transport(dict(request))
    except Exception as exc:
        receipt = _make_receipt(gate, invoked_at=invoked_iso, state="attempted_once_transport_error", outcome=type(exc).__name__)
        core = {
            "schema_version": 1, "mode": MODE, "execution_state": "attempted_once_transport_error",
            "attempt_consumed": True, "invocation_receipt": receipt, "response_attestation": None,
            "blockers": ["transport_callable_raised"], "transport_callable_invoked": True, "network_requests_reported": None,
            "credentials_used": False, "task_acceptance_enabled": False, "submission_enabled": False,
            "value_movement_enabled": False, "executor_is_payment_or_task_permission": False,
        }
        return {**core, "single_use_transport_executor_sha256": _h(core)}

    result_blockers: list[str] = []
    if not isinstance(result, Mapping):
        result_blockers.append("transport_result_not_mapping")
        result = {}
    request_count = result.get("network_requests_performed")
    if request_count != 1:
        result_blockers.append("transport_request_count_must_equal_one")
    peer_ip = str(result.get("peer_ip", ""))
    if peer_ip not in {str(x) for x in pins} or not _public_ip(peer_ip):
        result_blockers.append("transport_peer_ip_not_pinned_public_address")
    if result.get("tls_verified") is not True:
        result_blockers.append("transport_tls_not_verified")
    if result.get("tls_server_name") != hostname:
        result_blockers.append("transport_tls_server_name_mismatch")
    if result.get("dns_reresolved_after_connect") is not False:
        result_blockers.append("transport_dns_reresolution_detected")
    if result.get("redirect_count") != 0:
        result_blockers.append("transport_redirect_detected")
    content_type = str(result.get("content_type", "")).split(";", 1)[0].strip().lower()
    if content_type != "application/json":
        result_blockers.append("transport_content_type_not_json")
    compressed = result.get("compressed_response_bytes")
    decompressed = result.get("decompressed_response_bytes")
    for name, value in (("compressed", compressed), ("decompressed", decompressed)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0 or value > max_bytes:
            result_blockers.append(f"transport_{name}_response_size_invalid_or_over_limit")
    body = result.get("body_utf8")
    if not isinstance(body, str):
        result_blockers.append("transport_body_utf8_missing")
        body_bytes = b""
    else:
        body_bytes = body.encode("utf-8")
        if isinstance(decompressed, int) and decompressed != len(body_bytes):
            result_blockers.append("transport_decompressed_size_mismatch")
        try:
            json.loads(body)
        except Exception:
            result_blockers.append("transport_body_invalid_json")
    status_code = result.get("status_code")
    if not isinstance(status_code, int) or isinstance(status_code, bool) or not 100 <= status_code <= 599:
        result_blockers.append("transport_status_code_invalid")

    result_blockers = list(dict.fromkeys(result_blockers))
    if result_blockers:
        receipt = _make_receipt(gate, invoked_at=invoked_iso, state="attempted_once_result_rejected", outcome="result_rejected")
        core = {
            "schema_version": 1, "mode": MODE, "execution_state": "attempted_once_result_rejected",
            "attempt_consumed": True, "invocation_receipt": receipt, "response_attestation": None,
            "blockers": result_blockers, "transport_callable_invoked": True,
            "network_requests_reported": request_count if isinstance(request_count, int) else None,
            "credentials_used": False, "task_acceptance_enabled": False, "submission_enabled": False,
            "value_movement_enabled": False, "executor_is_payment_or_task_permission": False,
        }
        return {**core, "single_use_transport_executor_sha256": _h(core)}

    att_core = {
        "schema_version": 1, "mode": ATTESTATION_MODE, "attestation_state": "accepted_readonly_json_response",
        "attested_at": invoked_iso,
        "final_network_adapter_invocation_gate_sha256": gate.get("final_network_adapter_invocation_gate_sha256"),
        "final_real_observation_execution_envelope_sha256": envelope_hash,
        "final_real_observation_authorization_sha256": authorization_hash,
        "target_fingerprint": request.get("target_fingerprint"), "hostname": hostname, "peer_ip": peer_ip,
        "tls_verified": True, "tls_server_name": hostname, "dns_reresolved_after_connect": False,
        "redirect_count": 0, "network_requests_performed": 1, "status_code": status_code,
        "content_type": "application/json", "compressed_response_bytes": compressed,
        "decompressed_response_bytes": decompressed, "response_body_sha256": sha256(body_bytes).hexdigest(),
        "response_json_sha256": _h(json.loads(body)), "credentials_used": False, "action_performed": False,
        "attestation_is_payment_or_task_permission": False,
    }
    attestation = {**att_core, "readonly_json_response_attestation_sha256": _h(att_core)}
    receipt = _make_receipt(gate, invoked_at=invoked_iso, state="invoked_once", outcome="accepted_readonly_json_response")
    core = {
        "schema_version": 1, "mode": MODE, "execution_state": "invoked_once_response_attested",
        "attempt_consumed": True, "invocation_receipt": receipt, "response_attestation": attestation,
        "blockers": [], "transport_callable_invoked": True, "network_requests_reported": 1,
        "credentials_used": False, "task_acceptance_enabled": False, "submission_enabled": False,
        "value_movement_enabled": False, "executor_is_payment_or_task_permission": False,
    }
    return {**core, "single_use_transport_executor_sha256": _h(core)}


from native_exact_https_hardening import wrap_i090
execute_single_use_dependency_injected_transport = wrap_i090(execute_single_use_dependency_injected_transport)
