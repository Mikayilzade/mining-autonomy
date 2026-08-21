from human_decision_request import build_human_decision_request
from human_decision_verifier import verify_human_decision_record
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


def req():
    return build_human_decision_request(
        ready(),
        requested_at_utc="2026-08-21T15:00:00Z",
        upstream_review_expires_at_utc="2026-08-21T15:05:00Z",
    )


def decision(r, choice="authorize_one_read_only_observation"):
    return {
        "mode": "explicit_human_read_only_observation_decision",
        "decision": choice,
        "decided_at_utc": "2026-08-21T15:01:00Z",
        "human_scope_acknowledged": True,
        "human_decision_request_sha256": r["human_decision_request_sha256"],
        "market_side_readiness_sha256": r["market_side_readiness_sha256"],
        "exact_scope_sha256": r["exact_scope_sha256"],
    }


def verify(r, d, at="2026-08-21T15:02:00Z"):
    return verify_human_decision_record(r, d, verified_at_utc=at)


def rehash_request(r):
    c = dict(r)
    c.pop("human_decision_request_sha256", None)
    r["human_decision_request_sha256"] = h(c)


def test_exact_authorize_verifies_but_never_enables_transport():
    r = req()
    out = verify(r, decision(r))
    assert out["verification_state"] == "explicit_read_only_authorization_verified"
    assert out["explicit_authorization_verified"] is True
    assert out["authorization_scope"]["method"] == "GET"
    assert out["authorization_scope"]["request_count"] == 1
    assert out["network_enabled"] is False and out["transport_enabled"] is False
    assert out["record_is_execution_token"] is False


def test_explicit_deny_verifies_without_authorization():
    r = req()
    out = verify(r, decision(r, "deny"))
    assert out["verification_state"] == "explicit_deny_verified"
    assert out["explicit_deny_verified"] is True
    assert out["explicit_authorization_verified"] is False
    assert out["authorization_scope"] is None


def test_request_hash_tamper_rejected():
    r = req()
    r["current_resource_backend_id"] = "other"
    out = verify(r, decision(r))
    assert "human_decision_request_hash_invalid" in out["blockers"]


def test_scope_widening_rejected_even_if_request_rehashed():
    r = req()
    r["decision_scope"]["authorization_target"]["request_count"] = 2
    rehash_request(r)
    out = verify(r, decision(r))
    assert "authorization_target_not_exact_anonymous_get" in out["blockers"]


def test_wrong_binding_rejected():
    r = req()
    d = decision(r)
    d["exact_scope_sha256"] = "e" * 64
    out = verify(r, d)
    assert "decision_scope_hash_binding_invalid" in out["blockers"]


def test_missing_human_acknowledgement_rejected():
    r = req()
    d = decision(r)
    d["human_scope_acknowledged"] = False
    out = verify(r, d)
    assert "human_scope_acknowledgement_required" in out["blockers"]


def test_expired_or_future_decision_rejected():
    r = req()
    d = decision(r)
    d["decided_at_utc"] = "2026-08-21T15:05:00Z"
    assert "decision_outside_request_window" in verify(r, d, at="2026-08-21T15:05:00Z")["blockers"]
    d = decision(r)
    d["decided_at_utc"] = "2026-08-21T15:03:00Z"
    assert "decision_timestamp_in_future" in verify(r, d, at="2026-08-21T15:02:00Z")["blockers"]


def test_chat_history_cannot_be_used_as_decision_mode():
    r = req()
    d = decision(r)
    d["mode"] = "inferred_from_chat_history"
    out = verify(r, d)
    assert "explicit_human_decision_mode_required" in out["blockers"]
    assert out["real_user_consent_inferred_from_chat_history"] is False
