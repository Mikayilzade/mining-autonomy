from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Protocol

MODE = "deterministic_activation_envelope_adapter_invocation_gate"
_EXPECTED_PREFLIGHT_MODE = "deterministic_real_network_activation_authorization_consumption_preflight"
_EXPECTED_ENVELOPE_MODE = "single_attempt_real_network_activation_envelope"
_EXPECTED_RECEIPT_MODE = "single_use_real_network_activation_consumption_receipt"
_INVOCATION_RECEIPT_MODE = "single_use_synthetic_adapter_invocation_receipt"
_SYNTHETIC_RESULT_MODE = "network_incapable_synthetic_adapter_result"


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


class NetworkIncapableAdapter(Protocol):
    adapter_id: str
    network_capable: bool

    def invoke_synthetic(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]: ...


class SyntheticNetworkIncapableAdapter:
    """Reference dependency-injected adapter that cannot perform DNS/HTTP."""

    network_capable = False

    def __init__(self, adapter_id: str):
        self.adapter_id = adapter_id
        self.invocation_count = 0

    def invoke_synthetic(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]:
        self.invocation_count += 1
        return {
            "schema_version": 1,
            "mode": _SYNTHETIC_RESULT_MODE,
            "adapter_id": self.adapter_id,
            "invocation_count": self.invocation_count,
            "exact_scope": dict(envelope.get("exact_scope", {})),
            "exact_scope_sha256": envelope.get("exact_scope_sha256"),
            "real_network_activation_envelope_sha256": envelope.get("real_network_activation_envelope_sha256"),
            "network_capable": False,
            "transport_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "credentials_used": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
            "synthetic_only": True,
        }


def _receipt_consumes_envelope(receipt: Mapping[str, Any], envelope_hash: str) -> bool:
    return (
        receipt.get("mode") == _INVOCATION_RECEIPT_MODE
        and receipt.get("real_network_activation_envelope_sha256") == envelope_hash
        and receipt.get("invocation_state") == "synthetic_adapter_invoked_once_no_network"
    )


def invoke_activation_envelope_synthetic(
    consumption_preflight: Mapping[str, Any],
    adapter: NetworkIncapableAdapter,
    *,
    prior_invocation_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Validate I080 and invoke exactly one dependency-injected network-incapable adapter.

    This function intentionally has no network implementation. A network-capable adapter
    is rejected before callback invocation.
    """
    blockers: list[str] = []

    preflight_hash = consumption_preflight.get("real_network_activation_consumption_preflight_sha256")
    preflight_core = dict(consumption_preflight)
    preflight_core.pop("real_network_activation_consumption_preflight_sha256", None)
    if not isinstance(preflight_hash, str) or preflight_hash != _hash(preflight_core):
        blockers.append("consumption_preflight_hash_invalid")
    if consumption_preflight.get("mode") != _EXPECTED_PREFLIGHT_MODE:
        blockers.append("consumption_preflight_mode_invalid")
    if consumption_preflight.get("consumption_state") != "authorization_consumed_once_envelope_ready_no_network":
        blockers.append("consumption_preflight_not_ready")

    for key in (
        "adapter_invoked", "transport_enabled", "network_enabled", "network_calls_performed",
        "credentials_used", "task_acceptance_enabled", "submission_enabled", "execution_enabled",
        "value_movement_enabled",
    ):
        if consumption_preflight.get(key) is not False:
            blockers.append(f"consumption_preflight_{key}_must_be_false")

    envelope = consumption_preflight.get("activation_envelope")
    receipt = consumption_preflight.get("consumption_receipt")
    if not isinstance(envelope, Mapping):
        blockers.append("activation_envelope_missing")
        envelope = {}
    if not isinstance(receipt, Mapping):
        blockers.append("consumption_receipt_missing")
        receipt = {}

    envelope_hash = envelope.get("real_network_activation_envelope_sha256")
    envelope_core = dict(envelope)
    envelope_core.pop("real_network_activation_envelope_sha256", None)
    if not isinstance(envelope_hash, str) or envelope_hash != _hash(envelope_core):
        blockers.append("activation_envelope_hash_invalid")
    if envelope.get("mode") != _EXPECTED_ENVELOPE_MODE:
        blockers.append("activation_envelope_mode_invalid")
    if envelope.get("envelope_state") != "one_attempt_bound_no_network":
        blockers.append("activation_envelope_state_invalid")
    if envelope.get("max_adapter_invocations") != 1 or envelope.get("max_network_requests") != 1:
        blockers.append("activation_envelope_limits_invalid")
    for key in (
        "credentials_allowed", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled",
        "transport_enabled", "network_enabled", "network_calls_performed", "adapter_invoked",
        "envelope_is_execution_result",
    ):
        if envelope.get(key) is not False:
            blockers.append(f"activation_envelope_{key}_widened")

    scope = envelope.get("exact_scope")
    if not isinstance(scope, Mapping) or not _exact_scope(scope):
        blockers.append("activation_envelope_scope_not_exact")
        scope = {}

    receipt_hash = receipt.get("real_network_activation_consumption_receipt_sha256")
    receipt_core = dict(receipt)
    receipt_core.pop("real_network_activation_consumption_receipt_sha256", None)
    if not isinstance(receipt_hash, str) or receipt_hash != _hash(receipt_core):
        blockers.append("consumption_receipt_hash_invalid")
    if receipt.get("mode") != _EXPECTED_RECEIPT_MODE or receipt.get("consumption_state") != "consumed_once_no_network":
        blockers.append("consumption_receipt_state_invalid")
    if receipt.get("authorization_consumed") is not True:
        blockers.append("consumption_receipt_does_not_prove_consumption")
    if receipt.get("network_enabled") is not False or receipt.get("network_calls_performed") is not False:
        blockers.append("consumption_receipt_claims_network_activity")
    if receipt.get("receipt_is_execution_token") is not False:
        blockers.append("consumption_receipt_execution_scope_invalid")

    lineage_fields = (
        "real_network_activation_authorization_sha256",
        "real_network_activation_request_sha256",
        "adapter_id",
        "exact_scope_sha256",
    )
    for key in lineage_fields:
        if envelope.get(key) != receipt.get(key):
            blockers.append(f"envelope_receipt_{key}_binding_invalid")
    if receipt.get("real_network_activation_envelope_sha256") != envelope_hash:
        blockers.append("consumption_receipt_envelope_binding_invalid")

    preflight_auth_hash = consumption_preflight.get("real_network_activation_authorization_sha256")
    preflight_request_hash = consumption_preflight.get("real_network_activation_request_sha256")
    if envelope.get("real_network_activation_authorization_sha256") != preflight_auth_hash:
        blockers.append("preflight_envelope_authorization_binding_invalid")
    if envelope.get("real_network_activation_request_sha256") != preflight_request_hash:
        blockers.append("preflight_envelope_request_binding_invalid")

    if getattr(adapter, "network_capable", None) is not False:
        blockers.append("network_capable_adapter_rejected")
    if getattr(adapter, "adapter_id", None) != envelope.get("adapter_id"):
        blockers.append("adapter_id_binding_invalid")
    if not callable(getattr(adapter, "invoke_synthetic", None)):
        blockers.append("synthetic_adapter_callback_missing")

    for prior in prior_invocation_receipts:
        if not isinstance(prior, Mapping):
            blockers.append("prior_invocation_receipt_malformed")
            continue
        prior_hash = prior.get("synthetic_adapter_invocation_receipt_sha256")
        prior_core = dict(prior)
        prior_core.pop("synthetic_adapter_invocation_receipt_sha256", None)
        if not isinstance(prior_hash, str) or prior_hash != _hash(prior_core):
            blockers.append("prior_invocation_receipt_hash_invalid")
            continue
        if _receipt_consumes_envelope(prior, str(envelope_hash)):
            blockers.append("activation_envelope_replay_detected")

    blockers = list(dict.fromkeys(blockers))
    adapter_result = None
    invocation_receipt = None
    state = "synthetic_adapter_invocation_rejected"

    if not blockers:
        raw_result = adapter.invoke_synthetic(envelope)
        if not isinstance(raw_result, Mapping):
            blockers.append("synthetic_adapter_result_malformed")
        else:
            adapter_result = dict(raw_result)
            if adapter_result.get("mode") != _SYNTHETIC_RESULT_MODE:
                blockers.append("synthetic_adapter_result_mode_invalid")
            if adapter_result.get("adapter_id") != envelope.get("adapter_id"):
                blockers.append("synthetic_adapter_result_adapter_binding_invalid")
            if adapter_result.get("invocation_count") != 1:
                blockers.append("synthetic_adapter_invocation_count_invalid")
            if adapter_result.get("real_network_activation_envelope_sha256") != envelope_hash:
                blockers.append("synthetic_adapter_result_envelope_binding_invalid")
            if adapter_result.get("exact_scope_sha256") != envelope.get("exact_scope_sha256"):
                blockers.append("synthetic_adapter_result_scope_hash_binding_invalid")
            result_scope = adapter_result.get("exact_scope")
            if not isinstance(result_scope, Mapping) or dict(result_scope) != dict(scope) or not _exact_scope(result_scope):
                blockers.append("synthetic_adapter_result_scope_widened")
            for key in (
                "network_capable", "transport_enabled", "network_enabled", "network_calls_performed",
                "credentials_used", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled",
            ):
                if adapter_result.get(key) is not False:
                    blockers.append(f"synthetic_adapter_result_{key}_must_be_false")
            if adapter_result.get("synthetic_only") is not True:
                blockers.append("synthetic_adapter_result_not_synthetic_only")

        blockers = list(dict.fromkeys(blockers))
        if not blockers and adapter_result is not None:
            result_hash = _hash(adapter_result)
            receipt_core = {
                "schema_version": 1,
                "mode": _INVOCATION_RECEIPT_MODE,
                "invocation_state": "synthetic_adapter_invoked_once_no_network",
                "real_network_activation_envelope_sha256": envelope_hash,
                "real_network_activation_consumption_receipt_sha256": receipt_hash,
                "adapter_id": envelope.get("adapter_id"),
                "exact_scope_sha256": envelope.get("exact_scope_sha256"),
                "synthetic_adapter_result_sha256": result_hash,
                "adapter_invoked_once": True,
                "real_network_adapter_reachable": False,
                "transport_enabled": False,
                "network_enabled": False,
                "network_calls_performed": False,
                "credentials_used": False,
                "task_acceptance_enabled": False,
                "submission_enabled": False,
                "value_movement_enabled": False,
                "receipt_is_real_execution_token": False,
            }
            invocation_receipt = {**receipt_core, "synthetic_adapter_invocation_receipt_sha256": _hash(receipt_core)}
            state = "synthetic_adapter_invoked_once_scope_preserved_no_network"

    core = {
        "schema_version": 1,
        "mode": MODE,
        "invocation_state": state,
        "real_network_activation_consumption_preflight_sha256": preflight_hash if isinstance(preflight_hash, str) else None,
        "real_network_activation_envelope_sha256": envelope_hash if isinstance(envelope_hash, str) else None,
        "real_network_activation_consumption_receipt_sha256": receipt_hash if isinstance(receipt_hash, str) else None,
        "adapter_id": envelope.get("adapter_id") if isinstance(envelope, Mapping) else None,
        "exact_scope_sha256": envelope.get("exact_scope_sha256") if isinstance(envelope, Mapping) else None,
        "adapter_result": adapter_result,
        "invocation_receipt": invocation_receipt,
        "blockers": blockers,
        "real_network_adapter_reachable": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "invocation_record_is_real_execution_token": False,
    }
    return {**core, "activation_envelope_invocation_gate_sha256": _hash(core)}
