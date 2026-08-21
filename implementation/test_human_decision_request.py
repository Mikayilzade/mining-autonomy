from human_decision_request import build_human_decision_request
from hashlib import sha256
import json


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def ready():
    core = {
        "schema_version": 1,
        "mode": "deterministic_market_side_readiness_checkpoint",
        "built_at_utc": "2026-08-21T14:53:00Z",
        "checkpoint_state": "ready_for_human_review_only",
        "dominant_unknown": "real_market_demand_and_fill_rate",
        "single_observation_needed": {
            "candidate": "PayanAgent",
            "purpose": "measure_real_open_paid_demand_and_fill_without_accepting_or_submitting_work",
            "method": "GET",
            "request_count": 1,
            "required_environment": "production",
            "target_fingerprint": "payan-public-feed",
            "credentials_allowed": False,
            "action_enabled": False,
        },
        "current_resource_route": {
            "selected_backend_id": "python_local",
            "route_state": "rerouted_dry_run",
            "history_tip_hash": "c" * 64,
            "materialization_hash": "d" * 64,
        },
        "compliance_review_bridge_sha256": "a" * 64,
        "exact_scope_sha256": "b" * 64,
        "unresolved_gates": ["fresh_explicit_real_user_authorization_still_required"],
        "authorization_granted": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "packet_is_authorization": False,
        "packet_is_execution_token": False,
    }
    return {**core, "market_side_readiness_sha256": h(core)}


def build(r):
    return build_human_decision_request(
        r,
        requested_at_utc="2026-08-21T15:00:00Z",
        upstream_review_expires_at_utc="2026-08-21T15:05:00Z",
    )


def rehash(r):
    core = dict(r)
    core.pop("market_side_readiness_sha256", None)
    r["market_side_readiness_sha256"] = h(core)


def test_ready_request_is_short_lived_inert_and_exact_scope_bound():
    p = build(ready())
    assert p["request_state"] == "decision_requested"
    assert p["expires_at_utc"] == "2026-08-21T15:05:00Z"
    assert p["expiry_source"] == "upstream_review_scope_exact_expiry"
    assert p["authorization_granted"] is False
    assert p["network_enabled"] is False
    assert p["decision_scope"]["authorization_target"]["request_count"] == 1
    assert p["decision_scope"]["authorization_target"]["method"] == "GET"
    assert "task_acceptance" in p["decision_scope"]["explicitly_not_authorized"]
    assert "value_movement" in p["decision_scope"]["explicitly_not_authorized"]


def test_i068_hash_tamper_fails_closed():
    r = ready()
    r["single_observation_needed"]["candidate"] = "Other"
    p = build(r)
    assert p["request_state"] == "blocked_before_decision_request"
    assert "market_side_readiness_hash_invalid" in p["blockers"]


def test_expired_upstream_review_scope_fails_closed():
    p = build_human_decision_request(
        ready(),
        requested_at_utc="2026-08-21T15:05:00Z",
        upstream_review_expires_at_utc="2026-08-21T15:05:00Z",
    )
    assert "upstream_review_scope_expired_or_nonpositive" in p["blockers"]


def test_scope_widening_fails_even_with_rehashed_i068_packet():
    r = ready()
    r["single_observation_needed"]["request_count"] = 2
    rehash(r)
    p = build(r)
    assert "single_observation_scope_not_exact_anonymous_get" in p["blockers"]


def test_blocked_i068_checkpoint_cannot_request_decision():
    r = ready()
    r["checkpoint_state"] = "blocked_before_human_review"
    rehash(r)
    p = build(r)
    assert "market_side_readiness_not_ready" in p["blockers"]


def test_unsafe_readiness_flag_cannot_be_laundered_into_request():
    r = ready()
    r["network_enabled"] = True
    rehash(r)
    p = build(r)
    assert "unsafe_or_missing_readiness_network_enabled" in p["blockers"]


def test_current_resource_route_is_required_for_decision_context():
    r = ready()
    r["current_resource_route"]["selected_backend_id"] = None
    rehash(r)
    p = build(r)
    assert "current_resource_route_missing" in p["blockers"]
