from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_exact_real_read_only_invocation_request_builder"
_REQUEST_MODE = "exact_real_read_only_invocation_human_review_request"
_EXPECTED_I081_MODE = "deterministic_activation_envelope_adapter_invocation_gate"
_EXPECTED_I081_RECEIPT_MODE = "single_use_synthetic_adapter_invocation_receipt"
_EXPECTED_I080_MODE = "deterministic_real_network_activation_authorization_consumption_preflight"
_EXPECTED_ENVELOPE_MODE = "single_attempt_real_network_activation_envelope"


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


def build_exact_real_read_only_invocation_request(
    invocation_gate: Mapping[str, Any],
    consumption_preflight: Mapping[str, Any],
    *,
    requested_at: str,
    ttl_seconds: int = 300,
) -> dict[str, Any]:
    """Build a human-reviewable request only; never authorize or expose real transport."""
    blockers: list[str] = []

    try:
        requested_dt = _parse_utc(requested_at)
    except Exception:
        requested_dt = None
        blockers.append("requested_at_invalid_or_not_utc")
    if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int) or not 60 <= ttl_seconds <= 900:
        blockers.append("ttl_out_of_range")

    gate_hash = invocation_gate.get("activation_envelope_invocation_gate_sha256")
    gate_core = dict(invocation_gate)
    gate_core.pop("activation_envelope_invocation_gate_sha256", None)
    if not isinstance(gate_hash, str) or gate_hash != _hash(gate_core):
        blockers.append("i081_gate_hash_invalid")
    if invocation_gate.get("mode") != _EXPECTED_I081_MODE:
        blockers.append("i081_gate_mode_invalid")
    if invocation_gate.get("invocation_state") != "synthetic_adapter_invoked_once_scope_preserved_no_network":
        blockers.append("i081_gate_not_successful")
    if invocation_gate.get("blockers"):
        blockers.append("i081_gate_has_blockers")
    for key in (
        "real_network_adapter_reachable", "transport_enabled", "network_enabled", "network_calls_performed",
        "credentials_used", "task_acceptance_enabled", "submission_enabled", "execution_enabled",
        "value_movement_enabled", "invocation_record_is_real_execution_token",
    ):
        if invocation_gate.get(key) is not False:
            blockers.append(f"i081_{key}_must_be_false")

    invocation_receipt = invocation_gate.get("invocation_receipt")
    if not isinstance(invocation_receipt, Mapping):
        blockers.append("i081_invocation_receipt_missing")
        invocation_receipt = {}
    invocation_receipt_hash = invocation_receipt.get("synthetic_adapter_invocation_receipt_sha256")
    receipt_core = dict(invocation_receipt)
    receipt_core.pop("synthetic_adapter_invocation_receipt_sha256", None)
    if not isinstance(invocation_receipt_hash, str) or invocation_receipt_hash != _hash(receipt_core):
        blockers.append("i081_invocation_receipt_hash_invalid")
    if (
        invocation_receipt.get("mode") != _EXPECTED_I081_RECEIPT_MODE
        or invocation_receipt.get("invocation_state") != "synthetic_adapter_invoked_once_no_network"
        or invocation_receipt.get("adapter_invoked_once") is not True
    ):
        blockers.append("i081_invocation_receipt_state_invalid")
    for key in (
        "real_network_adapter_reachable", "transport_enabled", "network_enabled", "network_calls_performed",
        "credentials_used", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled",
        "receipt_is_real_execution_token",
    ):
        if invocation_receipt.get(key) is not False:
            blockers.append(f"i081_receipt_{key}_must_be_false")

    preflight_hash = consumption_preflight.get("real_network_activation_consumption_preflight_sha256")
    preflight_core = dict(consumption_preflight)
    preflight_core.pop("real_network_activation_consumption_preflight_sha256", None)
    if not isinstance(preflight_hash, str) or preflight_hash != _hash(preflight_core):
        blockers.append("i080_preflight_hash_invalid")
    if consumption_preflight.get("mode") != _EXPECTED_I080_MODE:
        blockers.append("i080_preflight_mode_invalid")
    if consumption_preflight.get("consumption_state") != "authorization_consumed_once_envelope_ready_no_network":
        blockers.append("i080_preflight_not_ready")
    for key in (
        "adapter_invoked", "transport_enabled", "network_enabled", "network_calls_performed", "credentials_used",
        "task_acceptance_enabled", "submission_enabled", "execution_enabled", "value_movement_enabled",
        "consumption_record_is_execution_token",
    ):
        if consumption_preflight.get(key) is not False:
            blockers.append(f"i080_{key}_must_be_false")

    envelope = consumption_preflight.get("activation_envelope")
    if not isinstance(envelope, Mapping):
        blockers.append("i080_activation_envelope_missing")
        envelope = {}
    envelope_hash = envelope.get("real_network_activation_envelope_sha256")
    envelope_core = dict(envelope)
    envelope_core.pop("real_network_activation_envelope_sha256", None)
    if not isinstance(envelope_hash, str) or envelope_hash != _hash(envelope_core):
        blockers.append("i080_activation_envelope_hash_invalid")
    if envelope.get("mode") != _EXPECTED_ENVELOPE_MODE or envelope.get("envelope_state") != "one_attempt_bound_no_network":
        blockers.append("i080_activation_envelope_state_invalid")
    if envelope.get("max_adapter_invocations") != 1 or envelope.get("max_network_requests") != 1:
        blockers.append("i080_activation_envelope_limits_invalid")

    scope = envelope.get("exact_scope")
    if not isinstance(scope, Mapping) or not _exact_scope(scope):
        blockers.append("exact_scope_not_one_anonymous_production_get")
        scope = {}
    for key in (
        "credentials_allowed", "task_acceptance_enabled", "submission_enabled", "value_movement_enabled",
        "transport_enabled", "network_enabled", "network_calls_performed", "adapter_invoked",
        "envelope_is_execution_result",
    ):
        if envelope.get(key) is not False:
            blockers.append(f"i080_envelope_{key}_widened")

    if invocation_gate.get("real_network_activation_consumption_preflight_sha256") != preflight_hash:
        blockers.append("i081_i080_preflight_binding_invalid")
    if invocation_gate.get("real_network_activation_envelope_sha256") != envelope_hash:
        blockers.append("i081_i080_envelope_binding_invalid")
    if invocation_receipt.get("real_network_activation_envelope_sha256") != envelope_hash:
        blockers.append("i081_receipt_i080_envelope_binding_invalid")
    c_receipt = consumption_preflight.get("consumption_receipt")
    c_receipt_hash = c_receipt.get("real_network_activation_consumption_receipt_sha256") if isinstance(c_receipt, Mapping) else None
    if invocation_gate.get("real_network_activation_consumption_receipt_sha256") != c_receipt_hash:
        blockers.append("i081_i080_consumption_receipt_binding_invalid")

    for key in ("adapter_id", "exact_scope_sha256"):
        if invocation_gate.get(key) != envelope.get(key) or invocation_receipt.get(key) != envelope.get(key):
            blockers.append(f"invocation_lineage_{key}_binding_invalid")

    source_fields = (
        "implementation_binding_audit_sha256", "implementation_source_sha256",
        "network_adapter_contract_validation_sha256", "adapter_contract_readiness_sha256",
        "real_network_activation_authorization_sha256", "real_network_activation_request_sha256",
    )
    source_lineage: dict[str, Any] = {}
    for key in source_fields:
        value = envelope.get(key)
        source_lineage[key] = value
        if not isinstance(value, str) or not value:
            blockers.append(f"missing_envelope_lineage_{key}")
    source_digest = source_lineage.get("implementation_source_sha256")
    if not isinstance(source_digest, str) or len(source_digest) != 64:
        blockers.append("implementation_source_digest_invalid")
    if envelope.get("exact_scope_sha256") != _hash(dict(scope)):
        blockers.append("exact_scope_hash_invalid")

    blockers = list(dict.fromkeys(blockers))
    ready = not blockers
    request = None
    if ready and requested_dt is not None:
        expires_dt = requested_dt + timedelta(seconds=ttl_seconds)
        request_core = {
            "schema_version": 1,
            "mode": _REQUEST_MODE,
            "request_state": "ready_for_fresh_explicit_human_real_read_only_invocation_decision",
            "requested_at": requested_dt.isoformat().replace("+00:00", "Z"),
            "expires_at": expires_dt.isoformat().replace("+00:00", "Z"),
            "ttl_seconds": ttl_seconds,
            "activation_envelope_invocation_gate_sha256": gate_hash,
            "synthetic_adapter_invocation_receipt_sha256": invocation_receipt_hash,
            "real_network_activation_consumption_preflight_sha256": preflight_hash,
            "real_network_activation_envelope_sha256": envelope_hash,
            "adapter_id": envelope.get("adapter_id"),
            "exact_scope_sha256": envelope.get("exact_scope_sha256"),
            "exact_scope": dict(scope),
            "source_lineage": source_lineage,
            "remaining_prerequisites": {
                "fresh_explicit_human_decision_bound_to_request_hash": True,
                "network_capable_adapter_still_unreachable": True,
                "dns_private_address_pinning_rebinding_gate_required": True,
                "zero_redirect_required": True,
                "bounded_json_only_response_required": True,
                "fresh_first_party_anonymous_read_only_policy_evidence_required": True,
            },
            "human_summary": {
                "operation": "one anonymous production GET only",
                "target_fingerprint": scope.get("target_fingerprint"),
                "adapter_id": envelope.get("adapter_id"),
                "implementation_source_sha256": source_digest,
                "credentials": "forbidden",
                "task_acceptance_or_submission": "forbidden",
                "value_movement": "forbidden",
                "network_status": "still disabled; this packet only requests a fresh decision",
            },
            "explicit_human_decision_required": True,
            "real_invocation_authorized": False,
            "network_capable_adapter_reachable": False,
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
        request = {**request_core, "exact_real_read_only_invocation_request_sha256": _hash(request_core)}

    core = {
        "schema_version": 1,
        "mode": MODE,
        "builder_state": "exact_real_read_only_invocation_request_ready_no_network" if ready else "exact_real_read_only_invocation_request_rejected",
        "activation_envelope_invocation_gate_sha256": gate_hash if isinstance(gate_hash, str) else None,
        "synthetic_adapter_invocation_receipt_sha256": invocation_receipt_hash if isinstance(invocation_receipt_hash, str) else None,
        "real_network_activation_consumption_preflight_sha256": preflight_hash if isinstance(preflight_hash, str) else None,
        "real_network_activation_envelope_sha256": envelope_hash if isinstance(envelope_hash, str) else None,
        "real_read_only_invocation_request": request,
        "blockers": blockers,
        "real_invocation_authorized": False,
        "network_capable_adapter_reachable": False,
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
    return {**core, "exact_real_read_only_invocation_request_builder_sha256": _hash(core)}
