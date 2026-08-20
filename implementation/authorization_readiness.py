"""Deterministic authorization-readiness decision packet for I038.

Offline-only. Combines I037 capture-integrity quality output with the exact I036
history and I028-I030 readiness/session/preflight contracts. It selects at most
one exact GET as the minimal next integrity observation, or emits a no-capture
state. It never grants authorization or performs network activity.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

QUALITY_MODE = "longitudinal_capture_integrity_gate"
HISTORY_MODE = "capture_session_attestation_history"
READINESS_MODE = "deterministic_no_network_capture_readiness_packet"
SESSION_MODE = "deterministic_no_network_capture_session_plan"
PREFLIGHT_MODE = "deterministic_read_only_transport_preflight"
OUTPUT_MODE = "deterministic_authorization_readiness_decision_packet"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _parse_utc(value: Any, code: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(code)
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(code) from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError(f"{code}_not_utc")
    return dt.astimezone(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _validate_hash_record(record: Mapping[str, Any], *, mode: str, hash_field: str, prefix: str) -> str:
    if not isinstance(record, Mapping) or record.get("schema_version") != 1 or record.get("mode") != mode:
        raise ValueError(f"{prefix}_schema_or_mode_invalid")
    supplied = record.get(hash_field)
    if not isinstance(supplied, str) or len(supplied) != 64:
        raise ValueError(f"{prefix}_hash_invalid")
    core = dict(record)
    core.pop(hash_field, None)
    if _hash(core) != supplied:
        raise ValueError(f"{prefix}_hash_mismatch")
    return supplied


def _require_inert_flags(record: Mapping[str, Any], prefix: str, *, require_authorization_false: bool = False) -> None:
    expected = {"network_calls_performed": False, "dry_run_only": True, "action_enabled": False}
    if "credentials_allowed" in record:
        expected["credentials_allowed"] = False
    if "credentials_used" in record:
        expected["credentials_used"] = False
    if require_authorization_false:
        expected["authorization_granted"] = False
    for key, wanted in expected.items():
        if record.get(key) is not wanted:
            raise ValueError(f"{prefix}_{key}_invalid")


def _validate_quality(quality: Mapping[str, Any]) -> str:
    qhash = _validate_hash_record(quality, mode=QUALITY_MODE, hash_field="quality_gate_sha256", prefix="authorization_readiness_quality")
    _require_inert_flags(quality, "authorization_readiness_quality")
    if quality.get("authorization_required") is not True:
        raise ValueError("authorization_readiness_quality_authorization_required_invalid")
    if quality.get("economic_evidence_classification") != "not_evaluated_capture_integrity_is_not_demand":
        raise ValueError("authorization_readiness_quality_demand_boundary_invalid")
    return qhash


def _validate_history(history: Mapping[str, Any]) -> str:
    hhash = _validate_hash_record(history, mode=HISTORY_MODE, hash_field="history_sha256", prefix="authorization_readiness_history")
    _require_inert_flags(history, "authorization_readiness_history")
    return hhash


def _validate_contracts(packet: Mapping[str, Any], plan: Mapping[str, Any], preflight: Mapping[str, Any]) -> tuple[str, str, str]:
    if not isinstance(packet, Mapping) or packet.get("schema_version") != 1 or packet.get("mode") != READINESS_MODE:
        raise ValueError("authorization_readiness_packet_invalid")
    _require_inert_flags(packet, "authorization_readiness_packet", require_authorization_false=True)
    if packet.get("missing_evidence_is_negative_demand") is not False:
        raise ValueError("authorization_readiness_packet_missing_semantics_invalid")
    if not isinstance(plan, Mapping) or plan.get("schema_version") != 1 or plan.get("mode") != SESSION_MODE:
        raise ValueError("authorization_readiness_session_invalid")
    _require_inert_flags(plan, "authorization_readiness_session", require_authorization_false=True)
    if plan.get("missing_evidence_is_negative_demand") is not False:
        raise ValueError("authorization_readiness_session_missing_semantics_invalid")
    if not isinstance(preflight, Mapping) or preflight.get("schema_version") != 1 or preflight.get("mode") != PREFLIGHT_MODE:
        raise ValueError("authorization_readiness_preflight_invalid")
    _require_inert_flags(preflight, "authorization_readiness_preflight", require_authorization_false=True)
    if preflight.get("transport_enabled") is not False:
        raise ValueError("authorization_readiness_preflight_transport_enabled")
    if preflight.get("missing_evidence_is_negative_demand") is not False:
        raise ValueError("authorization_readiness_preflight_missing_semantics_invalid")
    packet_hash = _hash(packet)
    plan_hash = _hash(plan)
    envelope_set = preflight.get("transport_envelope_set_sha256")
    if preflight.get("readiness_packet_sha256") != packet_hash:
        raise ValueError("authorization_readiness_packet_hash_binding_mismatch")
    if preflight.get("session_plan_sha256") != plan_hash:
        raise ValueError("authorization_readiness_session_hash_binding_mismatch")
    if not isinstance(envelope_set, str) or len(envelope_set) != 64:
        raise ValueError("authorization_readiness_envelope_set_hash_invalid")
    envelopes = preflight.get("transport_envelopes")
    if not isinstance(envelopes, list) or preflight.get("planned_request_count") != len(envelopes):
        raise ValueError("authorization_readiness_envelope_count_invalid")
    if _hash(envelopes) != envelope_set:
        raise ValueError("authorization_readiness_envelope_set_hash_mismatch")
    if packet.get("manifest_sha256") != plan.get("manifest_sha256") or plan.get("manifest_sha256") != preflight.get("manifest_sha256"):
        raise ValueError("authorization_readiness_manifest_binding_mismatch")
    return packet_hash, plan_hash, envelope_set


def _validate_history_binding(history: Mapping[str, Any], quality: Mapping[str, Any], plan_hash: str, envelope_set_hash: str) -> None:
    if quality.get("history_sha256") != history.get("history_sha256"):
        raise ValueError("authorization_readiness_quality_history_binding_mismatch")
    if history.get("session_plan_sha256") != plan_hash:
        raise ValueError("authorization_readiness_history_session_binding_mismatch")
    if history.get("transport_envelope_set_sha256") != envelope_set_hash:
        raise ValueError("authorization_readiness_history_transport_binding_mismatch")


def _candidate(envelope: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(envelope, Mapping):
        raise ValueError("authorization_readiness_envelope_invalid")
    if envelope.get("method") != "GET" or envelope.get("required_environment") != "production":
        raise ValueError("authorization_readiness_envelope_scope_invalid")
    for key, wanted in {"credentials_allowed": False, "action_enabled": False, "transport_enabled": False, "authorization_granted": False, "network_calls_performed": False, "dry_run_only": True}.items():
        if envelope.get(key) is not wanted:
            raise ValueError(f"authorization_readiness_envelope_{key}_invalid")
    request_hash = envelope.get("request_binding_sha256")
    if not isinstance(request_hash, str) or len(request_hash) != 64:
        raise ValueError("authorization_readiness_request_binding_hash_invalid")
    binding = dict(envelope)
    for extra in ("request_binding_sha256", "transport_interface", "transport_enabled", "authorization_granted", "network_calls_performed", "dry_run_only"):
        binding.pop(extra, None)
    if _hash(binding) != request_hash:
        raise ValueError("authorization_readiness_request_binding_hash_mismatch")
    evidence = envelope.get("expected_evidence_classes")
    provenance = envelope.get("provenance_checklist")
    if not isinstance(evidence, list) or not evidence or not isinstance(provenance, list) or not provenance:
        raise ValueError("authorization_readiness_envelope_evidence_or_provenance_invalid")
    return {"sequence": int(envelope["sequence"]), "priority_index": int(envelope["priority_index"]), "platform": str(envelope["platform"]), "item_index": int(envelope["item_index"]), "source_url": str(envelope["source_url"]), "host": str(envelope["host"]), "method": "GET", "manifest_item_sha256": str(envelope["manifest_item_sha256"]), "request_binding_sha256": request_hash, "expected_evidence_classes": list(evidence), "provenance_checklist": list(provenance), "required_environment": "production", "rate_limit": dict(envelope["rate_limit"]), "timeout_seconds": float(envelope["timeout_seconds"])}


def build_authorization_readiness_packet(quality_gate: Mapping[str, Any], attestation_history: Mapping[str, Any], readiness_packet: Mapping[str, Any], session_plan: Mapping[str, Any], transport_preflight: Mapping[str, Any], *, decision_time_utc: str, proposed_ttl_seconds: int = 600) -> dict[str, Any]:
    """Build an inert decision packet for the smallest useful future read-only capture."""
    qhash = _validate_quality(quality_gate)
    hhash = _validate_history(attestation_history)
    packet_hash, plan_hash, envelope_set_hash = _validate_contracts(readiness_packet, session_plan, transport_preflight)
    _validate_history_binding(attestation_history, quality_gate, plan_hash, envelope_set_hash)
    now = _parse_utc(decision_time_utc, "authorization_readiness_decision_time_invalid")
    if not isinstance(proposed_ttl_seconds, int) or isinstance(proposed_ttl_seconds, bool) or not 60 <= proposed_ttl_seconds <= 3600:
        raise ValueError("authorization_readiness_ttl_invalid")
    expiry = now + timedelta(seconds=proposed_ttl_seconds)
    wants_repeat = quality_gate.get("future_read_only_capture_worth_repeating_for_integrity") is True
    recommendation = quality_gate.get("future_read_only_capture_recommendation")
    envelopes = transport_preflight["transport_envelopes"]
    target = None
    if wants_repeat and envelopes:
        validated = [_candidate(env) for env in envelopes]
        validated.sort(key=lambda row: (row["priority_index"], row["sequence"], row["request_binding_sha256"]))
        target = validated[0]
    if not wants_repeat:
        decision, reason, next_action = "no_capture_needed_for_integrity_only", "i037_quality_gate_does_not_recommend_repeat", "none"
    elif target is None:
        decision, reason, next_action = "capture_recommended_but_no_exact_ready_request_available", "i037_recommends_repeat_but_i030_has_no_transport_envelope", "repair_readiness_or_observability_offline_before_authorization"
    elif len(envelopes) == 1:
        decision, reason, next_action = "single_request_exact_plan_ready_for_user_authorization", str(recommendation), "request_explicit_user_authorization_for_exact_existing_single_get_plan"
    else:
        decision, reason, next_action = "minimal_single_request_replan_required_before_user_authorization", str(recommendation), "rebuild_i029_i030_as_one_request_plan_bound_to_selected_request_hash"
    minimal = None
    if target is not None:
        minimal = {**target, "selection_rule": "highest_upstream_priority_then_sequence_exactly_one_get", "minimal_request_count": 1, "original_session_plan_sha256": plan_hash, "original_transport_envelope_set_sha256": envelope_set_hash, "authorization_scope_required": "exact_plan_only", "authorization_must_not_widen_to_other_requests": True}
    auth_draft = None
    if target is not None and len(envelopes) == 1:
        auth_draft = {"schema_version": 1, "mode": "explicit_read_only_network_authorization", "authorization_granted": False, "scope": "exact_preflight_plan", "session_plan_sha256": plan_hash, "allowed_methods": ["GET"], "max_requests": 1, "credentials_allowed": False, "action_enabled": False, "authorization_nonce": None, "not_before_utc": _iso(now), "expires_at_utc": _iso(expiry), "user_authorization_required": True}
    core = {"schema_version": 1, "mode": OUTPUT_MODE, "decision_time_utc": _iso(now), "quality_gate_sha256": qhash, "history_sha256": hhash, "readiness_packet_sha256": packet_hash, "session_plan_sha256": plan_hash, "transport_envelope_set_sha256": envelope_set_hash, "capture_integrity_label": quality_gate.get("capture_integrity_label"), "economic_evidence_classification": "not_evaluated_capture_integrity_is_not_demand", "decision": decision, "decision_reason": reason, "next_action": next_action, "minimal_future_read_only_capture": minimal, "proposed_authorization_draft": auth_draft, "proposed_ttl_seconds": proposed_ttl_seconds, "authorization_required": True, "authorization_granted": False, "credentials_allowed": False, "network_calls_performed": False, "dry_run_only": True, "action_enabled": False, "missing_capture_interpretation": "unknown_not_negative_demand"}
    return {**core, "authorization_readiness_sha256": _hash(core)}
