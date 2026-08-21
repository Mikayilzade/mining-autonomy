"""I073 deterministic pre-real-transport human-review packet.

Offline only. Compiles one exact I072 inert handoff plus current market/resource
readiness into a fail-closed review artifact. It never grants authorization,
never enables transport, and contains no DNS/HTTP implementation.
"""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

REVIEW_MODE = "deterministic_pre_real_transport_review"
_READY_MARKET_STATES = {"ready", "ready_for_observation_request"}
_READY_RESOURCE_STATES = {"ready", "calibrated_ready", "ready_for_routing"}
_INERT_FALSE_FIELDS = (
    "transport_enabled", "network_enabled", "network_calls_performed",
    "credentials_used", "task_acceptance_enabled", "submission_enabled",
    "execution_enabled", "value_movement_enabled",
)

def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt

def _verify_hashed(obj: Mapping[str, Any], hash_field: str, blocker: str, blockers: list[str]) -> str | None:
    supplied = obj.get(hash_field)
    core = dict(obj); core.pop(hash_field, None)
    if not isinstance(supplied, str) or supplied != _hash(core):
        blockers.append(blocker)
        return supplied if isinstance(supplied, str) else None
    return supplied

def _freshness_blockers(readiness: Mapping[str, Any], *, now: datetime, prefix: str, max_age_seconds: int) -> list[str]:
    out: list[str] = []
    candidates = (
        readiness.get("checked_at_utc"), readiness.get("observed_at_utc"),
        readiness.get("verified_at_utc"), readiness.get("attested_at_utc"),
        readiness.get("generated_at_utc"), readiness.get("updated_at_utc"),
    )
    stamp = next((x for x in candidates if isinstance(x, str) and x), None)
    if stamp is None:
        return [f"{prefix}_freshness_timestamp_missing"]
    try:
        ts = _utc(stamp)
        age = (now - ts).total_seconds()
        if age < 0:
            out.append(f"{prefix}_freshness_timestamp_in_future")
        elif age > max_age_seconds:
            out.append(f"{prefix}_readiness_stale")
    except Exception:
        out.append(f"{prefix}_freshness_timestamp_invalid")
    return out

def build_pre_real_transport_review(
    handoff: Mapping[str, Any],
    lease: Mapping[str, Any],
    market_readiness: Mapping[str, Any],
    resource_readiness: Mapping[str, Any],
    *,
    reviewed_at_utc: str,
    readiness_max_age_seconds: int = 86400,
) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        now = _utc(reviewed_at_utc)
    except Exception:
        now = datetime.now(timezone.utc)
        blockers.append("review_timestamp_invalid")
    if not isinstance(readiness_max_age_seconds, int) or isinstance(readiness_max_age_seconds, bool) or readiness_max_age_seconds <= 0:
        blockers.append("readiness_max_age_invalid")
        readiness_max_age_seconds = 86400

    handoff_hash = _verify_hashed(
        handoff, "lease_bound_transport_handoff_sha256",
        "lease_bound_transport_handoff_hash_invalid", blockers,
    )
    lease_hash = _verify_hashed(
        lease, "observation_authorization_lease_sha256",
        "observation_authorization_lease_hash_invalid", blockers,
    )

    if handoff.get("handoff_state") != "inert_transport_handoff_recorded" or handoff.get("blockers"):
        blockers.append("i072_handoff_not_clean")
    if lease.get("lease_state") != "single_use_observation_lease_ready" or lease.get("blockers"):
        blockers.append("i071_lease_not_ready")
    if handoff.get("observation_authorization_lease_sha256") != lease_hash:
        blockers.append("handoff_lease_binding_invalid")
    for field in ("human_decision_verification_sha256", "human_decision_request_sha256", "exact_scope_sha256"):
        if handoff.get(field) != lease.get(field):
            blockers.append(f"handoff_{field}_binding_invalid")

    scope = lease.get("lease_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("lease_scope_missing")
    exact_scope_ok = (
        scope.get("method") == "GET"
        and scope.get("request_count") == 1
        and scope.get("required_environment") == "production"
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
        and isinstance(scope.get("target_fingerprint"), str)
        and bool(scope.get("target_fingerprint"))
    )
    if not exact_scope_ok:
        blockers.append("lease_scope_not_exact_anonymous_get")

    envelope = handoff.get("transport_envelope")
    if not isinstance(envelope, Mapping):
        envelope = {}
        blockers.append("transport_envelope_missing")
    else:
        env_hash = envelope.get("transport_envelope_sha256")
        env_core = dict(envelope); env_core.pop("transport_envelope_sha256", None)
        if not isinstance(env_hash, str) or env_hash != _hash(env_core):
            blockers.append("transport_envelope_hash_invalid")
        if not (
            envelope.get("method") == "GET"
            and envelope.get("request_count") == 1
            and envelope.get("required_environment") == "production"
            and envelope.get("target_fingerprint") == scope.get("target_fingerprint")
            and envelope.get("credentials_allowed") is False
            and envelope.get("action_enabled") is False
            and envelope.get("network_enabled") is False
            and envelope.get("network_calls_allowed") == 0
            and envelope.get("observation_authorization_lease_sha256") == lease_hash
            and envelope.get("human_decision_request_sha256") == lease.get("human_decision_request_sha256")
            and envelope.get("exact_scope_sha256") == lease.get("exact_scope_sha256")
        ):
            blockers.append("transport_envelope_not_exact_inert_get")

    adapter_result = handoff.get("adapter_result")
    if not isinstance(adapter_result, Mapping):
        blockers.append("adapter_result_missing")
    else:
        result_hash = adapter_result.get("transport_result_sha256")
        result_core = dict(adapter_result); result_core.pop("transport_result_sha256", None)
        if not isinstance(result_hash, str) or result_hash != _hash(result_core):
            blockers.append("adapter_result_hash_invalid")
        if not (
            adapter_result.get("mode") == "network_incapable_transport_result"
            and adapter_result.get("envelope_sha256") == _hash(dict(envelope))
            and adapter_result.get("network_calls_performed") is False
            and adapter_result.get("response_body_present") is False
        ):
            blockers.append("adapter_result_not_network_incapable")

    for field in _INERT_FALSE_FIELDS:
        if handoff.get(field) is not False:
            blockers.append(f"unsafe_or_missing_handoff_{field}")
    if handoff.get("handoff_is_execution_token") is not False:
        blockers.append("handoff_must_not_be_execution_token")

    market_state = market_readiness.get("state")
    if market_state not in _READY_MARKET_STATES:
        blockers.append("market_not_currently_ready")
    market_hard = market_readiness.get("hard_blockers", market_readiness.get("blockers", []))
    if market_hard:
        blockers.append("market_has_current_blockers")
    blockers.extend(_freshness_blockers(
        market_readiness, now=now, prefix="market", max_age_seconds=readiness_max_age_seconds
    ))

    resource_state = resource_readiness.get("state")
    if resource_state not in _READY_RESOURCE_STATES:
        blockers.append("resource_not_currently_ready")
    resource_hard = resource_readiness.get("hard_blockers", resource_readiness.get("blockers", []))
    if resource_hard:
        blockers.append("resource_has_current_blockers")
    calibration_state = resource_readiness.get("calibration_state")
    if calibration_state not in {"calibrated_declared", "calibrated_reproducible"}:
        blockers.append("resource_not_calibrated")
    if resource_readiness.get("backend_id") not in {None, lease.get("current_resource_backend_id")}:
        blockers.append("resource_backend_binding_invalid")
    blockers.extend(_freshness_blockers(
        resource_readiness, now=now, prefix="resource", max_age_seconds=readiness_max_age_seconds
    ))

    try:
        lease_expires = _utc(str(lease.get("expires_at_utc")))
        if now >= lease_expires:
            blockers.append("reviewed_lease_expired")
    except Exception:
        blockers.append("lease_expiry_invalid")

    blockers = list(dict.fromkeys(blockers))
    exact_scope = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": scope.get("target_fingerprint"),
        "credentials_allowed": False,
        "action_enabled": False,
    } if exact_scope_ok else None

    prerequisites = (
        "fresh_first_party_source_compliance_evidence",
        "current_market_readiness_without_hard_blockers",
        "current_calibrated_resource_readiness",
        "fresh_explicit_human_authorization_bound_to_this_review_packet_hash",
        "authorization_scope_must_equal_exact_one_production_get_no_credentials_no_action",
        "authorization_must_be_short_lived_and_single_use",
        "dns_and_redirect_policy_gates_before_transport",
        "response_size_and_content_type_gates_before_parsing",
        "no_task_acceptance_submission_payment_or_value_movement",
    )
    state = "ready_for_explicit_real_transport_decision" if not blockers else "blocked_before_explicit_real_transport_decision"
    core = {
        "schema_version": 1,
        "mode": REVIEW_MODE,
        "review_state": state,
        "reviewed_at_utc": reviewed_at_utc,
        "lease_bound_transport_handoff_sha256": handoff_hash,
        "observation_authorization_lease_sha256": lease_hash,
        "human_decision_verification_sha256": lease.get("human_decision_verification_sha256"),
        "human_decision_request_sha256": lease.get("human_decision_request_sha256"),
        "exact_scope_sha256": lease.get("exact_scope_sha256"),
        "exact_scope": exact_scope,
        "market_readiness_snapshot": dict(market_readiness),
        "resource_readiness_snapshot": dict(resource_readiness),
        "unresolved_blockers": blockers,
        "explicit_user_authorization_prerequisites": prerequisites,
        "future_decision_binding_rule": {
            "decision_must_reference_field": "pre_real_transport_review_sha256",
            "must_match_exact_packet_hash": True,
            "prior_synthetic_or_offline_authorization_is_not_reusable": True,
        },
        "authorization_granted": False,
        "real_user_authorization_inferred": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "review_packet_is_execution_token": False,
    }
    return {**core, "pre_real_transport_review_sha256": _hash(core)}
