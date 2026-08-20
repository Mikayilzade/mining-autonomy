"""Deterministic minimal one-request plan reducer for I039.

Offline-only. Narrows an I038-selected request from a multi-request I029/I030
contract to one exact GET without changing source/evidence/provenance/rate/timeout
semantics. It never grants authorization or performs network activity.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any, Mapping

AUTH_READY_MODE = "deterministic_authorization_readiness_decision_packet"
READINESS_MODE = "deterministic_no_network_capture_readiness_packet"
SESSION_MODE = "deterministic_no_network_capture_session_plan"
PREFLIGHT_MODE = "deterministic_read_only_transport_preflight"
OUTPUT_MODE = "deterministic_minimal_single_request_plan_reduction"
REPLAN_DECISION = "minimal_single_request_replan_required_before_user_authorization"
NO_CAPTURE_DECISION = "no_capture_needed_for_integrity_only"
SINGLE_READY_DECISION = "single_request_exact_plan_ready_for_user_authorization"
BLOCKED_DECISION = "capture_recommended_but_no_exact_ready_request_available"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _validate_record_hash(record: Mapping[str, Any], field: str, mode: str, prefix: str) -> str:
    if not isinstance(record, Mapping) or record.get("schema_version") != 1 or record.get("mode") != mode:
        raise ValueError(f"{prefix}_schema_or_mode_invalid")
    supplied = record.get(field)
    if not isinstance(supplied, str) or len(supplied) != 64:
        raise ValueError(f"{prefix}_hash_invalid")
    core = dict(record)
    core.pop(field, None)
    if _hash(core) != supplied:
        raise ValueError(f"{prefix}_hash_mismatch")
    return supplied


def _inert(record: Mapping[str, Any], prefix: str) -> None:
    for key, expected in {
        "authorization_granted": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }.items():
        if key in record and record.get(key) is not expected:
            raise ValueError(f"{prefix}_{key}_invalid")
    if record.get("missing_evidence_is_negative_demand", False) is not False:
        raise ValueError(f"{prefix}_missing_evidence_semantics_invalid")


def _request_binding(envelope: Mapping[str, Any]) -> str:
    core = dict(envelope)
    for key in (
        "request_binding_sha256", "transport_interface", "transport_enabled",
        "authorization_granted", "network_calls_performed", "dry_run_only",
    ):
        core.pop(key, None)
    return _hash(core)


def _validate_upstream(
    decision: Mapping[str, Any], packet: Mapping[str, Any], plan: Mapping[str, Any], preflight: Mapping[str, Any]
) -> tuple[str, str, str, str]:
    d_hash = _validate_record_hash(decision, "authorization_readiness_sha256", AUTH_READY_MODE, "minimal_reducer_decision")
    _inert(decision, "minimal_reducer_decision")
    if not isinstance(packet, Mapping) or packet.get("schema_version") != 1 or packet.get("mode") != READINESS_MODE:
        raise ValueError("minimal_reducer_readiness_invalid")
    _inert(packet, "minimal_reducer_readiness")
    if not isinstance(plan, Mapping) or plan.get("schema_version") != 1 or plan.get("mode") != SESSION_MODE:
        raise ValueError("minimal_reducer_plan_invalid")
    _inert(plan, "minimal_reducer_plan")
    if not isinstance(preflight, Mapping) or preflight.get("schema_version") != 1 or preflight.get("mode") != PREFLIGHT_MODE:
        raise ValueError("minimal_reducer_preflight_invalid")
    _inert(preflight, "minimal_reducer_preflight")
    if preflight.get("transport_enabled") is not False:
        raise ValueError("minimal_reducer_transport_enabled_invalid")

    p_hash = _hash(packet)
    s_hash = _hash(plan)
    envs = preflight.get("transport_envelopes")
    if not isinstance(envs, list) or preflight.get("planned_request_count") != len(envs):
        raise ValueError("minimal_reducer_envelope_count_invalid")
    e_hash = _hash(envs)
    if preflight.get("readiness_packet_sha256") != p_hash:
        raise ValueError("minimal_reducer_readiness_binding_mismatch")
    if preflight.get("session_plan_sha256") != s_hash:
        raise ValueError("minimal_reducer_plan_binding_mismatch")
    if preflight.get("transport_envelope_set_sha256") != e_hash:
        raise ValueError("minimal_reducer_envelope_set_hash_mismatch")
    if decision.get("readiness_packet_sha256") != p_hash:
        raise ValueError("minimal_reducer_decision_readiness_binding_mismatch")
    if decision.get("session_plan_sha256") != s_hash:
        raise ValueError("minimal_reducer_decision_plan_binding_mismatch")
    if decision.get("transport_envelope_set_sha256") != e_hash:
        raise ValueError("minimal_reducer_decision_preflight_binding_mismatch")
    if packet.get("manifest_sha256") != plan.get("manifest_sha256") or plan.get("manifest_sha256") != preflight.get("manifest_sha256"):
        raise ValueError("minimal_reducer_manifest_binding_mismatch")
    return d_hash, p_hash, s_hash, e_hash


def _find_exact_target(decision: Mapping[str, Any], plan: Mapping[str, Any], preflight: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    target = decision.get("minimal_future_read_only_capture")
    if not isinstance(target, Mapping):
        raise ValueError("minimal_reducer_target_missing")
    binding = target.get("request_binding_sha256")
    if not isinstance(binding, str) or len(binding) != 64:
        raise ValueError("minimal_reducer_target_binding_invalid")

    matches = []
    for env in preflight["transport_envelopes"]:
        if not isinstance(env, Mapping):
            raise ValueError("minimal_reducer_envelope_invalid")
        supplied = env.get("request_binding_sha256")
        if not isinstance(supplied, str) or _request_binding(env) != supplied:
            raise ValueError("minimal_reducer_original_request_binding_mismatch")
        if supplied == binding:
            matches.append(dict(env))
    if len(matches) != 1:
        raise ValueError("minimal_reducer_target_not_unique_in_preflight")
    env = matches[0]

    keys = ("platform", "item_index", "source_url", "host", "method", "manifest_item_sha256", "required_environment")
    if any(target.get(k) != env.get(k) for k in keys):
        raise ValueError("minimal_reducer_target_semantics_mismatch")
    if list(target.get("expected_evidence_classes", [])) != list(env.get("expected_evidence_classes", [])):
        raise ValueError("minimal_reducer_target_evidence_mismatch")
    if list(target.get("provenance_checklist", [])) != list(env.get("provenance_checklist", [])):
        raise ValueError("minimal_reducer_target_provenance_mismatch")
    if dict(target.get("rate_limit", {})) != dict(env.get("rate_limit", {})):
        raise ValueError("minimal_reducer_target_rate_mismatch")
    if float(target.get("timeout_seconds")) != float(env.get("timeout_seconds")):
        raise ValueError("minimal_reducer_target_timeout_mismatch")

    steps = plan.get("chronological_session_plan")
    if not isinstance(steps, list):
        raise ValueError("minimal_reducer_steps_invalid")
    step_matches = [s for s in steps if isinstance(s, Mapping) and s.get("manifest_item_sha256") == env.get("manifest_item_sha256")]
    if len(step_matches) != 1:
        raise ValueError("minimal_reducer_target_not_unique_in_plan")
    step = dict(step_matches[0])
    for k in ("platform", "item_index", "source_url", "host", "method", "required_environment"):
        if step.get(k) != env.get(k):
            raise ValueError(f"minimal_reducer_plan_{k}_mismatch")
    if list(step.get("expected_evidence_classes", [])) != list(env.get("expected_evidence_classes", [])):
        raise ValueError("minimal_reducer_plan_evidence_mismatch")
    if list(step.get("provenance_checklist", [])) != list(env.get("provenance_checklist", [])):
        raise ValueError("minimal_reducer_plan_provenance_mismatch")
    return step, env


def _build_reduced_plan(original: Mapping[str, Any], selected_step: Mapping[str, Any]) -> dict[str, Any]:
    step = deepcopy(dict(selected_step))
    original_sequence = int(step.get("sequence"))
    step["sequence"] = 1
    others = []
    for row in original.get("chronological_session_plan", []):
        if isinstance(row, Mapping) and row.get("manifest_item_sha256") != selected_step.get("manifest_item_sha256"):
            others.append({
                "priority_index": int(row.get("priority_index")), "platform": str(row.get("platform")),
                "item_index": int(row.get("item_index")), "source_url": str(row.get("source_url")),
                "reason": "minimal_authorization_scope_reduction",
                "original_sequence": int(row.get("sequence")),
            })
    deferred = list(deepcopy(original.get("deferred_ready_items", []))) + others
    host = str(step["host"])
    return {
        "schema_version": 1,
        "mode": SESSION_MODE,
        "manifest_sha256": original.get("manifest_sha256"),
        "start_time_utc": original.get("start_time_utc"),
        "total_request_budget": 1,
        "total_time_budget_seconds": original.get("total_time_budget_seconds"),
        "planned_request_count": 1,
        "deferred_ready_count": len(deferred),
        "blocked_remediation_count": len(original.get("blocked_remediation_queue", [])),
        "chronological_session_plan": [step],
        "host_groups": [{"host": host, "request_count": 1, "sequence_numbers": [1]}],
        "deferred_ready_items": deferred,
        "blocked_remediation_queue": deepcopy(original.get("blocked_remediation_queue", [])),
        "authorization_state": "explicit_read_only_network_authorization_required",
        "authorization_granted": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "missing_evidence_is_negative_demand": False,
        "reduction_provenance": {
            "original_sequence": original_sequence,
            "selection_rule": "exact_i038_selected_request_only",
            "authorization_scope_widened": False,
        },
    }


def _build_reduced_preflight(original: Mapping[str, Any], packet_hash: str, plan: Mapping[str, Any], selected_env: Mapping[str, Any]) -> dict[str, Any]:
    env = deepcopy(dict(selected_env))
    original_binding = str(env["request_binding_sha256"])
    original_sequence = int(env["sequence"])
    env["sequence"] = 1
    env["request_binding_sha256"] = _request_binding(env)
    envs = [env]
    plan_hash = _hash(plan)
    return {
        "schema_version": 1,
        "mode": PREFLIGHT_MODE,
        "manifest_sha256": original.get("manifest_sha256"),
        "session_plan_sha256": plan_hash,
        "readiness_packet_sha256": packet_hash,
        "transport_envelope_set_sha256": _hash(envs),
        "planned_request_count": 1,
        "transport_envelopes": envs,
        "authorization_contract": {
            "required_mode": "explicit_read_only_network_authorization",
            "required_scope": "exact_preflight_plan",
            "required_session_plan_sha256": plan_hash,
            "allowed_methods": ["GET"],
            "required_max_requests": 1,
            "credentials_allowed": False,
            "action_enabled": False,
        },
        "reduction_provenance": {
            "original_request_binding_sha256": original_binding,
            "original_sequence": original_sequence,
            "authorization_scope_widened": False,
        },
        "transport_enabled": False,
        "authorization_granted": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "missing_evidence_is_negative_demand": False,
    }


def build_minimal_plan_reduction(
    authorization_readiness: Mapping[str, Any], readiness_packet: Mapping[str, Any],
    original_session_plan: Mapping[str, Any], original_transport_preflight: Mapping[str, Any],
) -> dict[str, Any]:
    """Reduce a multi-request I029/I030 plan to the exact single request selected by I038."""
    d_hash, p_hash, s_hash, e_hash = _validate_upstream(
        authorization_readiness, readiness_packet, original_session_plan, original_transport_preflight
    )
    decision = authorization_readiness.get("decision")
    reduced_plan = None
    reduced_preflight = None
    selected_original_binding = None

    if decision == NO_CAPTURE_DECISION:
        outcome = "no_op_no_capture_needed"
        reason = "i038_did_not_recommend_another_integrity_capture"
    elif decision == SINGLE_READY_DECISION:
        if original_transport_preflight.get("planned_request_count") != 1:
            raise ValueError("minimal_reducer_single_ready_count_invalid")
        _find_exact_target(authorization_readiness, original_session_plan, original_transport_preflight)
        outcome = "already_minimal_exact_plan_no_reduction_needed"
        reason = "i038_existing_plan_is_already_one_exact_get"
    elif decision == BLOCKED_DECISION:
        if authorization_readiness.get("minimal_future_read_only_capture") is not None:
            raise ValueError("minimal_reducer_blocked_target_must_be_none")
        outcome = "blocked_no_exact_request_to_reduce"
        reason = "i038_has_no_exact_ready_request"
    elif decision == REPLAN_DECISION:
        if original_transport_preflight.get("planned_request_count", 0) <= 1:
            raise ValueError("minimal_reducer_replan_requires_multi_request_source")
        step, env = _find_exact_target(authorization_readiness, original_session_plan, original_transport_preflight)
        selected_original_binding = str(env["request_binding_sha256"])
        reduced_plan = _build_reduced_plan(original_session_plan, step)
        reduced_preflight = _build_reduced_preflight(original_transport_preflight, p_hash, reduced_plan, env)
        outcome = "reduced_to_exact_single_get_plan"
        reason = "i038_selected_one_request_from_multi_request_plan"
    else:
        raise ValueError("minimal_reducer_decision_unsupported")

    core = {
        "schema_version": 1,
        "mode": OUTPUT_MODE,
        "authorization_readiness_sha256": d_hash,
        "original_readiness_packet_sha256": p_hash,
        "original_session_plan_sha256": s_hash,
        "original_transport_envelope_set_sha256": e_hash,
        "selected_original_request_binding_sha256": selected_original_binding,
        "outcome": outcome,
        "outcome_reason": reason,
        "reduced_session_plan": reduced_plan,
        "reduced_session_plan_sha256": _hash(reduced_plan) if reduced_plan is not None else None,
        "reduced_transport_preflight": reduced_preflight,
        "reduced_transport_envelope_set_sha256": (
            reduced_preflight["transport_envelope_set_sha256"] if reduced_preflight is not None else None
        ),
        "authorization_required": True,
        "authorization_granted": False,
        "credentials_allowed": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "authorization_scope_widened": False,
        "economic_evidence_classification": "not_evaluated_capture_integrity_is_not_demand",
        "missing_capture_interpretation": "unknown_not_negative_demand",
    }
    return {**core, "minimal_plan_reduction_sha256": _hash(core)}
