"""Deterministic exact read-only authorization request packet for I040.

Offline-only. Converts an I039 reduced one-request plan into a human-reviewable,
hash-bound authorization request. It never grants authorization, emits no usable
nonce or credential, and performs no network activity.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

REDUCTION_MODE = "deterministic_minimal_single_request_plan_reduction"
SESSION_MODE = "deterministic_no_network_capture_session_plan"
PREFLIGHT_MODE = "deterministic_read_only_transport_preflight"
OUTPUT_MODE = "deterministic_exact_read_only_authorization_request"
REDUCED_OUTCOME = "reduced_to_exact_single_get_plan"
NO_CAPTURE_OUTCOME = "no_op_no_capture_needed"
ALREADY_MINIMAL_OUTCOME = "already_minimal_exact_plan_no_reduction_needed"
BLOCKED_OUTCOME = "blocked_no_exact_request_to_reduce"


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


def _validate_reduction(reduction: Mapping[str, Any]) -> str:
    if not isinstance(reduction, Mapping) or reduction.get("schema_version") != 1 or reduction.get("mode") != REDUCTION_MODE:
        raise ValueError("authorization_request_reduction_schema_or_mode_invalid")
    supplied = reduction.get("minimal_plan_reduction_sha256")
    if not isinstance(supplied, str) or len(supplied) != 64:
        raise ValueError("authorization_request_reduction_hash_invalid")
    core = dict(reduction)
    core.pop("minimal_plan_reduction_sha256", None)
    if _hash(core) != supplied:
        raise ValueError("authorization_request_reduction_hash_mismatch")
    for key, wanted in {
        "authorization_granted": False,
        "credentials_allowed": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "authorization_scope_widened": False,
    }.items():
        if reduction.get(key) is not wanted:
            raise ValueError(f"authorization_request_reduction_{key}_invalid")
    return supplied


def _request_binding(envelope: Mapping[str, Any]) -> str:
    core = dict(envelope)
    for key in (
        "request_binding_sha256", "transport_interface", "transport_enabled",
        "authorization_granted", "network_calls_performed", "dry_run_only",
    ):
        core.pop(key, None)
    return _hash(core)


def _exact_scope(reduction: Mapping[str, Any]) -> tuple[dict[str, Any], str, str]:
    plan = reduction.get("reduced_session_plan")
    preflight = reduction.get("reduced_transport_preflight")
    if not isinstance(plan, Mapping) or plan.get("schema_version") != 1 or plan.get("mode") != SESSION_MODE:
        raise ValueError("authorization_request_reduced_plan_invalid")
    if not isinstance(preflight, Mapping) or preflight.get("schema_version") != 1 or preflight.get("mode") != PREFLIGHT_MODE:
        raise ValueError("authorization_request_reduced_preflight_invalid")
    for prefix, record in (("plan", plan), ("preflight", preflight)):
        for key, wanted in {
            "authorization_granted": False, "credentials_allowed": False,
            "network_calls_performed": False, "dry_run_only": True, "action_enabled": False,
        }.items():
            if record.get(key) is not wanted:
                raise ValueError(f"authorization_request_{prefix}_{key}_invalid")
    if preflight.get("transport_enabled") is not False:
        raise ValueError("authorization_request_transport_enabled_invalid")
    if plan.get("planned_request_count") != 1 or preflight.get("planned_request_count") != 1:
        raise ValueError("authorization_request_exactly_one_request_required")
    steps = plan.get("chronological_session_plan")
    envs = preflight.get("transport_envelopes")
    if not isinstance(steps, list) or len(steps) != 1 or not isinstance(envs, list) or len(envs) != 1:
        raise ValueError("authorization_request_single_step_envelope_required")
    plan_hash = _hash(plan)
    if reduction.get("reduced_session_plan_sha256") != plan_hash or preflight.get("session_plan_sha256") != plan_hash:
        raise ValueError("authorization_request_reduced_plan_hash_mismatch")
    envelope_set_hash = _hash(envs)
    if reduction.get("reduced_transport_envelope_set_sha256") != envelope_set_hash or preflight.get("transport_envelope_set_sha256") != envelope_set_hash:
        raise ValueError("authorization_request_reduced_envelope_set_hash_mismatch")
    env = envs[0]
    if not isinstance(env, Mapping) or env.get("method") != "GET" or env.get("required_environment") != "production":
        raise ValueError("authorization_request_get_production_scope_required")
    if env.get("credentials_allowed") is not False or env.get("action_enabled") is not False or env.get("transport_enabled") is not False:
        raise ValueError("authorization_request_envelope_inert_flags_invalid")
    binding = env.get("request_binding_sha256")
    if not isinstance(binding, str) or len(binding) != 64 or _request_binding(env) != binding:
        raise ValueError("authorization_request_binding_invalid")
    step = steps[0]
    for key in ("sequence", "priority_index", "platform", "item_index", "source_url", "host", "method", "manifest_item_sha256", "required_environment"):
        if step.get(key) != env.get(key):
            raise ValueError(f"authorization_request_step_{key}_mismatch")
    scope = {
        "platform": str(env["platform"]),
        "source_url": str(env["source_url"]),
        "host": str(env["host"]),
        "method": "GET",
        "required_environment": "production",
        "manifest_item_sha256": str(env["manifest_item_sha256"]),
        "request_binding_sha256": binding,
        "expected_evidence_classes": list(env.get("expected_evidence_classes", [])),
        "provenance_checklist": list(env.get("provenance_checklist", [])),
        "rate_limit": dict(env.get("rate_limit", {})),
        "timeout_seconds": float(env.get("timeout_seconds")),
        "max_requests": 1,
        "credentials_allowed": False,
        "action_enabled": False,
        "redirect_policy": env.get("redirect_policy"),
        "dns_policy": env.get("dns_policy"),
    }
    return scope, plan_hash, _hash(preflight)


def build_exact_authorization_request(
    minimal_plan_reduction: Mapping[str, Any], *, request_time_utc: str, ttl_seconds: int = 300
) -> dict[str, Any]:
    """Build an inert, exact-scope human authorization request over I039 output."""
    reduction_hash = _validate_reduction(minimal_plan_reduction)
    now = _parse_utc(request_time_utc, "authorization_request_time_invalid")
    if not isinstance(ttl_seconds, int) or isinstance(ttl_seconds, bool) or not 60 <= ttl_seconds <= 900:
        raise ValueError("authorization_request_ttl_invalid")
    expires = now + timedelta(seconds=ttl_seconds)
    outcome = minimal_plan_reduction.get("outcome")
    request_packet = None

    if outcome == REDUCED_OUTCOME:
        scope, plan_hash, preflight_hash = _exact_scope(minimal_plan_reduction)
        summary = (
            f"Authorize at most 1 read-only production GET to {scope['source_url']} "
            f"(host {scope['host']}); no credentials, no action, no redirects; "
            f"expires {_iso(expires)}."
        )
        scope_hash = _hash(scope)
        request_packet = {
            "schema_version": 1,
            "mode": "exact_read_only_network_authorization_request",
            "human_summary": summary,
            "scope": scope,
            "scope_sha256": scope_hash,
            "reduced_session_plan_sha256": plan_hash,
            "reduced_transport_preflight_sha256": preflight_hash,
            "not_before_utc": _iso(now),
            "expires_at_utc": _iso(expires),
            "ttl_seconds": ttl_seconds,
            "authorization_granted": False,
            "authorization_nonce": None,
            "authorization_token": None,
            "credentials_allowed": False,
            "network_calls_performed": False,
            "transport_enabled": False,
            "dry_run_only": True,
            "action_enabled": False,
            "user_authorization_required": True,
            "authorization_scope_widened": False,
        }
        packet_core = dict(request_packet)
        request_packet["authorization_request_sha256"] = _hash(packet_core)
        state = "exact_single_get_ready_for_explicit_user_authorization"
        reason = "i039_reduced_plan_binds_one_exact_production_get"
    elif outcome == NO_CAPTURE_OUTCOME:
        state = "no_authorization_request_needed"
        reason = "i039_no_capture_needed"
    elif outcome == ALREADY_MINIMAL_OUTCOME:
        state = "already_minimal_but_exact_embedded_plan_absent"
        reason = "i039_preserved_existing_single_request_without_embedding_rebuilt_plan"
    elif outcome == BLOCKED_OUTCOME:
        state = "authorization_request_blocked"
        reason = "i039_has_no_exact_request_to_authorize"
    else:
        raise ValueError("authorization_request_reduction_outcome_unsupported")

    core = {
        "schema_version": 1,
        "mode": OUTPUT_MODE,
        "minimal_plan_reduction_sha256": reduction_hash,
        "request_time_utc": _iso(now),
        "ttl_seconds": ttl_seconds,
        "state": state,
        "state_reason": reason,
        "exact_authorization_request": request_packet,
        "authorization_required": request_packet is not None,
        "authorization_granted": False,
        "authorization_nonce": None,
        "credentials_allowed": False,
        "network_calls_performed": False,
        "transport_enabled": False,
        "dry_run_only": True,
        "action_enabled": False,
        "authorization_scope_widened": False,
        "economic_evidence_classification": "not_evaluated_capture_integrity_is_not_demand",
        "missing_capture_interpretation": "unknown_not_negative_demand",
    }
    return {**core, "exact_authorization_request_packet_sha256": _hash(core)}
