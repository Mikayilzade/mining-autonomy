from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import ipaddress
import json
from typing import Any, Iterable, Mapping

MODE = "deterministic_final_network_adapter_invocation_gate"
I088_MODE = "deterministic_final_real_observation_authorization_consumption_preflight"
I088_ENV_MODE = "single_attempt_final_real_observation_execution_envelope"
I088_RECEIPT_MODE = "single_use_final_real_observation_consumption_receipt"
ADAPTER_MANIFEST_MODE = "bound_network_capable_https_json_adapter_manifest"
GATE_MODE = "single_attempt_dependency_injected_network_adapter_gate"
PRIOR_INVOCATION_RECEIPT_MODE = "single_use_final_network_adapter_invocation_receipt"
MAX_BYTES = 1_048_576
MAX_GATE_AGE_SECONDS = 60


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


def _sha(value: Any) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def _public_ip(value: Any) -> bool:
    try:
        addr = ipaddress.ip_address(str(value))
        return addr.is_global and not any(
            (addr.is_private, addr.is_loopback, addr.is_link_local, addr.is_multicast, addr.is_reserved, addr.is_unspecified)
        )
    except ValueError:
        return False


def _false(obj: Mapping[str, Any], keys: Iterable[str], prefix: str, blockers: list[str]) -> None:
    for key in keys:
        if obj.get(key) is not False:
            blockers.append(f"{prefix}_{key}_must_be_false")


def _strict_limits(limits: Mapping[str, Any]) -> bool:
    max_bytes = limits.get("max_response_bytes")
    return (
        limits.get("scheme") == "https"
        and limits.get("tls_required") is True
        and limits.get("method") == "GET"
        and limits.get("max_network_requests") == 1
        and limits.get("allow_redirects") is False
        and limits.get("max_redirects") == 0
        and limits.get("allowed_content_types") == ["application/json"]
        and isinstance(max_bytes, int)
        and not isinstance(max_bytes, bool)
        and 1 <= max_bytes <= MAX_BYTES
        and limits.get("credentials_allowed") is False
        and limits.get("action_enabled") is False
    )


def _prior_receipt_consumes(receipt: Mapping[str, Any], envelope_hash: str, authorization_hash: str) -> bool:
    return (
        receipt.get("mode") == PRIOR_INVOCATION_RECEIPT_MODE
        and receipt.get("invocation_state") in {"invoked_once", "attempted_once_result_rejected", "attempted_once_transport_error"}
        and receipt.get("final_real_observation_execution_envelope_sha256") == envelope_hash
        and receipt.get("final_real_observation_authorization_sha256") == authorization_hash
        and receipt.get("one_shot_consumed") is True
    )


def build_final_network_adapter_invocation_gate(
    i088: Mapping[str, Any],
    adapter_manifest: Mapping[str, Any],
    *,
    gated_at: str,
    prior_invocation_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build the final dependency-injected one-shot network gate. Never invokes transport itself."""
    blockers: list[str] = []
    try:
        now = _utc(gated_at)
    except Exception:
        now = None
        blockers.append("gated_at_invalid_or_not_utc")

    i088_hash = i088.get("final_real_observation_authorization_consumption_preflight_sha256")
    if not _hash_ok(i088, "final_real_observation_authorization_consumption_preflight_sha256"):
        blockers.append("i088_hash_invalid")
    if i088.get("mode") != I088_MODE or i088.get("consumption_state") != "authorization_consumed_once_envelope_ready_no_network":
        blockers.append("i088_not_ready")
    if i088.get("blockers"):
        blockers.append("i088_has_blockers")
    _false(i088,("network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","consumption_record_is_execution_token"),"i088",blockers)

    envelope = i088.get("real_observation_execution_envelope")
    if not isinstance(envelope, Mapping):
        blockers.append("i088_execution_envelope_missing"); envelope = {}
    envelope_hash = envelope.get("final_real_observation_execution_envelope_sha256")
    if not _hash_ok(envelope, "final_real_observation_execution_envelope_sha256"):
        blockers.append("i088_execution_envelope_hash_invalid")
    if envelope.get("mode") != I088_ENV_MODE or envelope.get("envelope_state") != "one_attempt_final_real_observation_ready_no_network":
        blockers.append("i088_execution_envelope_state_invalid")
    if envelope.get("max_adapter_invocations") != 1 or envelope.get("max_network_requests") != 1:
        blockers.append("i088_execution_envelope_limits_invalid")
    _false(envelope,("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled","network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","envelope_is_execution_result"),"i088_envelope",blockers)

    receipt = i088.get("consumption_receipt")
    if not isinstance(receipt, Mapping):
        blockers.append("i088_consumption_receipt_missing"); receipt = {}
    receipt_hash = receipt.get("final_real_observation_consumption_receipt_sha256")
    if not _hash_ok(receipt, "final_real_observation_consumption_receipt_sha256"):
        blockers.append("i088_consumption_receipt_hash_invalid")
    if receipt.get("mode") != I088_RECEIPT_MODE or receipt.get("consumption_state") != "authorization_consumed_once_no_network":
        blockers.append("i088_consumption_receipt_state_invalid")
    if receipt.get("authorization_consumed") is not True:
        blockers.append("i088_authorization_not_consumed")
    _false(receipt,("network_capable_adapter_reachable","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","value_movement_enabled","receipt_is_execution_token"),"i088_receipt",blockers)

    packet_hash = envelope.get("final_real_observation_review_packet_sha256")
    authorization_hash = envelope.get("final_real_observation_authorization_sha256")
    if not _sha(packet_hash) or i088.get("final_real_observation_review_packet_sha256") != packet_hash:
        blockers.append("i088_packet_lineage_invalid")
    if not _sha(authorization_hash) or i088.get("final_real_observation_authorization_sha256") != authorization_hash:
        blockers.append("i088_authorization_lineage_invalid")
    if receipt.get("final_real_observation_review_packet_sha256") != packet_hash:
        blockers.append("i088_receipt_packet_binding_invalid")
    if receipt.get("final_real_observation_authorization_sha256") != authorization_hash:
        blockers.append("i088_receipt_authorization_binding_invalid")
    if receipt.get("final_real_observation_execution_envelope_sha256") != envelope_hash:
        blockers.append("i088_receipt_envelope_binding_invalid")

    for key in ("adapter_id","target_fingerprint","exact_scope_sha256","policy_evidence_sha256","dns_evidence_sha256","transport_contract_sha256"):
        if receipt.get(key) != envelope.get(key):
            blockers.append(f"i088_receipt_{key}_binding_invalid")
    if i088.get("fresh_policy_evidence_sha256") != envelope.get("policy_evidence_sha256"):
        blockers.append("i088_fresh_policy_binding_invalid")
    if i088.get("fresh_dns_evidence_sha256") != envelope.get("dns_evidence_sha256"):
        blockers.append("i088_fresh_dns_binding_invalid")
    if i088.get("fresh_transport_contract_sha256") != envelope.get("transport_contract_sha256"):
        blockers.append("i088_fresh_transport_binding_invalid")

    scope = envelope.get("exact_scope") if isinstance(envelope.get("exact_scope"), Mapping) else {}
    if not (scope.get("method")=="GET" and scope.get("request_count")==1 and scope.get("required_environment")=="production" and scope.get("credentials_allowed") is False and scope.get("action_enabled") is False and scope.get("target_fingerprint")==envelope.get("target_fingerprint") and envelope.get("exact_scope_sha256")==_h(dict(scope))):
        blockers.append("i088_exact_scope_invalid")
    if not _sha(envelope.get("implementation_source_sha256")):
        blockers.append("i088_implementation_source_sha256_invalid")
    hostname = envelope.get("hostname")
    if not isinstance(hostname, str) or not hostname or any(c.isspace() for c in hostname):
        blockers.append("i088_hostname_invalid")
    pinned = envelope.get("pinned_addresses")
    if not isinstance(pinned, list) or not pinned:
        blockers.append("i088_pinned_addresses_missing"); pinned = []
    pinned_s = [str(x) for x in pinned]
    if len(pinned_s) != len(set(pinned_s)) or any(not _public_ip(x) for x in pinned_s):
        blockers.append("i088_pinned_addresses_invalid")
    limits = envelope.get("transport_limits") if isinstance(envelope.get("transport_limits"), Mapping) else {}
    if not _strict_limits(limits):
        blockers.append("i088_transport_limits_invalid")

    try:
        created = _utc(str(envelope.get("created_at")))
        if now is not None:
            age = (now - created).total_seconds()
            if age < 0: blockers.append("i088_envelope_from_future")
            elif age > MAX_GATE_AGE_SECONDS: blockers.append("i088_envelope_too_old_for_network_gate")
    except Exception:
        blockers.append("i088_envelope_created_at_invalid")

    manifest_hash = adapter_manifest.get("network_adapter_manifest_sha256")
    if not _hash_ok(adapter_manifest, "network_adapter_manifest_sha256"):
        blockers.append("adapter_manifest_hash_invalid")
    if adapter_manifest.get("mode") != ADAPTER_MANIFEST_MODE:
        blockers.append("adapter_manifest_mode_invalid")
    manifest_expected = {
        "adapter_id": envelope.get("adapter_id"), "target_fingerprint": envelope.get("target_fingerprint"),
        "exact_scope_sha256": envelope.get("exact_scope_sha256"), "implementation_source_sha256": envelope.get("implementation_source_sha256"),
        "hostname": hostname, "pinned_addresses": sorted(pinned_s), "scheme": limits.get("scheme"),
        "tls_required": limits.get("tls_required"), "method": limits.get("method"),
        "max_network_requests_per_invocation": limits.get("max_network_requests"), "allow_redirects": limits.get("allow_redirects"),
        "max_redirects": limits.get("max_redirects"), "allowed_content_types": limits.get("allowed_content_types"),
        "max_response_bytes": limits.get("max_response_bytes"), "credentials_allowed": False, "action_enabled": False,
    }
    for key, value in manifest_expected.items():
        actual = adapter_manifest.get(key)
        if key == "pinned_addresses" and isinstance(actual, list): actual = sorted(str(x) for x in actual)
        if actual != value: blockers.append(f"adapter_manifest_{key}_binding_invalid")
    if adapter_manifest.get("network_capable") is not True: blockers.append("adapter_manifest_not_network_capable")
    if adapter_manifest.get("dependency_injected_boundary") is not True: blockers.append("adapter_manifest_not_dependency_injected")
    if adapter_manifest.get("uses_address_pinning") is not True: blockers.append("adapter_manifest_address_pinning_not_required")
    if adapter_manifest.get("uses_tls_server_name") is not True: blockers.append("adapter_manifest_tls_server_name_not_required")
    if adapter_manifest.get("rejects_dns_reresolution_after_connect") is not True: blockers.append("adapter_manifest_dns_reresolution_not_rejected")
    if adapter_manifest.get("rejects_response_over_limit_after_decompression") is not True: blockers.append("adapter_manifest_decompression_limit_not_required")

    for prior in prior_invocation_receipts:
        if not isinstance(prior, Mapping): blockers.append("prior_invocation_receipt_malformed"); continue
        if not _hash_ok(prior, "final_network_adapter_invocation_receipt_sha256"):
            blockers.append("prior_invocation_receipt_hash_invalid"); continue
        if _prior_receipt_consumes(prior, str(envelope_hash), str(authorization_hash)):
            blockers.append("final_network_adapter_invocation_replay_detected")

    blockers = list(dict.fromkeys(blockers)); gate = None
    if not blockers and now is not None:
        request_spec = {
            "adapter_id": envelope.get("adapter_id"), "target_fingerprint": envelope.get("target_fingerprint"),
            "exact_scope_sha256": envelope.get("exact_scope_sha256"), "implementation_source_sha256": envelope.get("implementation_source_sha256"),
            "hostname": hostname, "pinned_addresses": sorted(pinned_s), "scheme": "https", "tls_required": True,
            "method": "GET", "max_network_requests": 1, "allow_redirects": False, "max_redirects": 0,
            "allowed_content_types": ["application/json"], "max_response_bytes": limits.get("max_response_bytes"),
            "credentials_allowed": False, "action_enabled": False,
        }
        gate_core = {
            "schema_version":1,"mode":GATE_MODE,"gate_state":"validated_ready_for_single_dependency_injected_network_invocation",
            "gated_at":now.isoformat().replace("+00:00","Z"),"expires_at":(now+timedelta(seconds=MAX_GATE_AGE_SECONDS)).isoformat().replace("+00:00","Z"),
            "max_gate_age_seconds":MAX_GATE_AGE_SECONDS,"i088_consumption_preflight_sha256":i088_hash,
            "i088_execution_envelope_sha256":envelope_hash,"i088_consumption_receipt_sha256":receipt_hash,
            "final_real_observation_review_packet_sha256":packet_hash,"final_real_observation_authorization_sha256":authorization_hash,
            "network_adapter_manifest_sha256":manifest_hash,"policy_evidence_sha256":envelope.get("policy_evidence_sha256"),
            "dns_evidence_sha256":envelope.get("dns_evidence_sha256"),"transport_contract_sha256":envelope.get("transport_contract_sha256"),
            "request_spec":request_spec,"max_adapter_invocations":1,"max_network_requests":1,
            "dependency_injected_transport_boundary_required":True,"network_transport_invoked":False,"network_calls_performed":False,
            "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,
            "gate_is_execution_result":False,"gate_is_payment_or_task_permission":False,
        }
        gate = {**gate_core,"final_network_adapter_invocation_gate_sha256":_h(gate_core)}

    core = {
        "schema_version":1,"mode":MODE,"gate_state":"final_network_adapter_invocation_gate_ready_no_call" if gate else "final_network_adapter_invocation_gate_rejected",
        "i088_consumption_preflight_sha256":i088_hash if isinstance(i088_hash,str) else None,
        "i088_execution_envelope_sha256":envelope_hash if isinstance(envelope_hash,str) else None,
        "i088_consumption_receipt_sha256":receipt_hash if isinstance(receipt_hash,str) else None,
        "network_adapter_manifest_sha256":manifest_hash if isinstance(manifest_hash,str) else None,"invocation_gate":gate,"blockers":blockers,
        "dependency_injected_transport_boundary_exposed":gate is not None,"network_transport_invoked":False,"network_calls_performed":False,
        "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,
        "gate_record_is_execution_token":False,
    }
    return {**core,"final_network_adapter_invocation_gate_builder_sha256":_h(core)}


from native_exact_https_hardening import wrap_i089
build_final_network_adapter_invocation_gate = wrap_i089(build_final_network_adapter_invocation_gate)
