"""I072 lease-bound, dependency-injected, network-incapable transport handoff.

Offline only. Validates one fresh I071 consumption receipt against its exact lease
and emits one immutable GET envelope to an injected adapter that must explicitly
declare itself network-incapable. No DNS/HTTP implementation exists here.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping, Protocol

HANDOFF_MODE = "deterministic_lease_bound_transport_handoff"
ENVELOPE_MODE = "immutable_anonymous_get_envelope"
RESULT_MODE = "network_incapable_transport_result"

def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt

class InertTransportAdapter(Protocol):
    network_capable: bool
    def submit(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]: ...

@dataclass(frozen=True)
class NetworkIncapableRecorder:
    network_capable: bool = False
    def submit(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]:
        core = {"schema_version": 1, "mode": RESULT_MODE, "adapter": "network_incapable_recorder", "envelope_sha256": _hash(dict(envelope)), "network_calls_performed": False, "response_body_present": False, "status_code": None}
        return {**core, "transport_result_sha256": _hash(core)}

def build_lease_bound_transport_handoff(lease: Mapping[str, Any], consumption_receipt: Mapping[str, Any], *, handed_off_at_utc: str, adapter: InertTransportAdapter) -> dict[str, Any]:
    blockers: list[str] = []
    lease_hash = lease.get("observation_authorization_lease_sha256")
    lease_core = dict(lease); lease_core.pop("observation_authorization_lease_sha256", None)
    if not isinstance(lease_hash, str) or lease_hash != _hash(lease_core): blockers.append("observation_authorization_lease_hash_invalid")
    if lease.get("lease_state") != "single_use_observation_lease_ready" or lease.get("blockers"): blockers.append("lease_not_ready")
    receipt_hash = consumption_receipt.get("observation_lease_consumption_sha256")
    receipt_core = dict(consumption_receipt); receipt_core.pop("observation_lease_consumption_sha256", None)
    if not isinstance(receipt_hash, str) or receipt_hash != _hash(receipt_core): blockers.append("consumption_receipt_hash_invalid")
    if consumption_receipt.get("consumption_state") != "lease_consumed": blockers.append("consumption_receipt_not_consumed")
    if consumption_receipt.get("lease_consumed") is not True or consumption_receipt.get("remaining_consumptions") != 0: blockers.append("consumption_receipt_single_use_state_invalid")
    if consumption_receipt.get("observation_authorization_lease_sha256") != lease_hash: blockers.append("consumption_receipt_lease_binding_invalid")
    for field in ("human_decision_verification_sha256", "human_decision_request_sha256", "exact_scope_sha256"):
        if consumption_receipt.get(field) != lease.get(field): blockers.append(f"consumption_receipt_{field}_binding_invalid")
    scope = lease.get("lease_scope")
    if not isinstance(scope, Mapping): scope = {}; blockers.append("lease_scope_missing")
    if not (scope.get("method") == "GET" and scope.get("request_count") == 1 and scope.get("required_environment") == "production" and scope.get("credentials_allowed") is False and scope.get("action_enabled") is False and isinstance(scope.get("target_fingerprint"), str) and scope.get("target_fingerprint")): blockers.append("lease_scope_not_exact_anonymous_get")
    for field in ("transport_enabled", "network_enabled", "network_calls_performed", "credentials_used", "task_acceptance_enabled", "submission_enabled", "execution_enabled", "value_movement_enabled"):
        if consumption_receipt.get(field) is not False: blockers.append(f"unsafe_or_missing_consumption_{field}")
    try:
        handoff_time, consumed_at, expires_at = _utc(handed_off_at_utc), _utc(str(consumption_receipt.get("consumed_at_utc"))), _utc(str(lease.get("expires_at_utc")))
        if handoff_time < consumed_at: blockers.append("handoff_before_consumption")
        if handoff_time >= expires_at: blockers.append("lease_expired_before_handoff")
    except Exception: blockers.append("invalid_handoff_or_lease_timestamp")
    if getattr(adapter, "network_capable", None) is not False: blockers.append("adapter_must_be_explicitly_network_incapable")
    if not callable(getattr(adapter, "submit", None)): blockers.append("adapter_submit_missing")
    blockers = list(dict.fromkeys(blockers)); envelope = adapter_result = None
    if not blockers:
        envelope_core = {"schema_version": 1, "mode": ENVELOPE_MODE, "method": "GET", "request_count": 1, "required_environment": "production", "target_fingerprint": scope["target_fingerprint"], "credentials_allowed": False, "action_enabled": False, "observation_authorization_lease_sha256": lease_hash, "observation_lease_consumption_sha256": receipt_hash, "human_decision_verification_sha256": lease.get("human_decision_verification_sha256"), "human_decision_request_sha256": lease.get("human_decision_request_sha256"), "exact_scope_sha256": lease.get("exact_scope_sha256"), "handed_off_at_utc": handed_off_at_utc, "network_enabled": False, "network_calls_allowed": 0}
        envelope = {**envelope_core, "transport_envelope_sha256": _hash(envelope_core)}
        adapter_result = dict(adapter.submit(envelope)); result_hash = adapter_result.get("transport_result_sha256"); result_core = dict(adapter_result); result_core.pop("transport_result_sha256", None)
        if not (isinstance(result_hash, str) and result_hash == _hash(result_core) and adapter_result.get("mode") == RESULT_MODE and adapter_result.get("envelope_sha256") == _hash(envelope) and adapter_result.get("network_calls_performed") is False and adapter_result.get("response_body_present") is False): blockers.append("network_incapable_adapter_result_invalid"); envelope = adapter_result = None
    ready = not blockers
    core = {"schema_version": 1, "mode": HANDOFF_MODE, "handoff_state": "inert_transport_handoff_recorded" if ready else "handoff_rejected", "handed_off_at_utc": handed_off_at_utc, "observation_authorization_lease_sha256": lease_hash, "observation_lease_consumption_sha256": receipt_hash, "human_decision_verification_sha256": lease.get("human_decision_verification_sha256"), "human_decision_request_sha256": lease.get("human_decision_request_sha256"), "exact_scope_sha256": lease.get("exact_scope_sha256"), "transport_envelope": envelope, "adapter_result": adapter_result, "blockers": blockers, "transport_enabled": False, "network_enabled": False, "network_calls_performed": False, "credentials_used": False, "task_acceptance_enabled": False, "submission_enabled": False, "execution_enabled": False, "value_movement_enabled": False, "handoff_is_execution_token": False}
    return {**core, "lease_bound_transport_handoff_sha256": _hash(core)}
