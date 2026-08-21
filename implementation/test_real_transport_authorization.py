from copy import deepcopy
from real_transport_authorization import verify_real_transport_authorization, _hash


def review_fixture():
    scope = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": "payanagent:public-task-feed:v1",
        "credentials_allowed": False,
        "action_enabled": False,
    }
    core = {
        "schema_version": 1,
        "mode": "deterministic_pre_real_transport_review",
        "review_state": "ready_for_explicit_real_transport_decision",
        "reviewed_at_utc": "2026-08-21T20:00:00Z",
        "lease_bound_transport_handoff_sha256": "h" * 64,
        "observation_authorization_lease_sha256": "l" * 64,
        "human_decision_verification_sha256": "v" * 64,
        "human_decision_request_sha256": "r" * 64,
        "exact_scope_sha256": "s" * 64,
        "exact_scope": scope,
        "market_readiness_snapshot": {"state": "ready_for_observation_request"},
        "resource_readiness_snapshot": {"state": "ready", "backend_id": "python_local"},
        "unresolved_blockers": [],
        "explicit_user_authorization_prerequisites": (),
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


def decision_fixture(review, *, choice="authorize_exact_read_only_transport", decided_at="2026-08-21T20:00:30Z"):
    core = {
        "mode": "explicit_human_real_transport_authorization_decision",
        "decision": choice,
        "decided_at_utc": decided_at,
        "human_scope_acknowledged": True,
        "pre_real_transport_review_sha256": review["pre_real_transport_review_sha256"],
        "exact_scope_sha256": review["exact_scope_sha256"],
        "authorized_scope": deepcopy(review["exact_scope"]) if choice == "authorize_exact_read_only_transport" else None,
    }
    return {**core, "real_transport_decision_sha256": _hash(core)}


def rehash(obj, field):
    core = deepcopy(obj)
    core.pop(field, None)
    core[field] = _hash(core)
    return core


def test_valid_exact_authorize_emits_short_lived_single_use_record_but_no_transport():
    review = review_fixture()
    decision = decision_fixture(review)
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z", authorization_ttl_seconds=60)
    assert out["verification_state"] == "explicit_real_transport_authorization_verified"
    assert out["blockers"] == []
    record = out["authorization_record"]
    assert record["authorization_scope"] == review["exact_scope"]
    assert record["max_consumptions"] == 1
    assert record["authorization_is_single_use"] is True
    assert record["expires_at_utc"] == "2026-08-21T20:02:00Z"
    assert record["network_enabled"] is False
    assert out["transport_enabled"] is False
    assert out["value_movement_enabled"] is False


def test_explicit_deny_is_verified_without_authorization_record():
    review = review_fixture()
    decision = decision_fixture(review, choice="deny")
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert out["verification_state"] == "explicit_real_transport_deny_verified"
    assert out["authorization_record"] is None
    assert out["explicit_real_transport_deny_verified"] is True


def test_review_hash_tamper_fails_closed():
    review = review_fixture()
    decision = decision_fixture(review)
    review["network_enabled"] = True
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert "pre_real_transport_review_hash_invalid" in out["blockers"]
    assert out["authorization_record"] is None


def test_review_not_ready_fails_closed_even_if_rehashed():
    review = review_fixture()
    review["review_state"] = "blocked_before_explicit_real_transport_decision"
    review["unresolved_blockers"] = ["market_not_currently_ready"]
    review = rehash(review, "pre_real_transport_review_sha256")
    decision = decision_fixture(review)
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert "pre_real_transport_review_not_ready" in out["blockers"]


def test_decision_binding_tamper_rejected():
    review = review_fixture()
    decision = decision_fixture(review)
    decision["pre_real_transport_review_sha256"] = "x" * 64
    decision = rehash(decision, "real_transport_decision_sha256")
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert "decision_review_hash_binding_invalid" in out["blockers"]


def test_rehashed_scope_widening_rejected():
    review = review_fixture()
    decision = decision_fixture(review)
    decision["authorized_scope"]["request_count"] = 2
    decision = rehash(decision, "real_transport_decision_sha256")
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert "authorized_scope_widened_or_changed" in out["blockers"]


def test_missing_human_ack_rejected():
    review = review_fixture()
    decision = decision_fixture(review)
    decision["human_scope_acknowledged"] = False
    decision = rehash(decision, "real_transport_decision_sha256")
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z")
    assert "human_scope_acknowledgement_required" in out["blockers"]


def test_stale_decision_rejected():
    review = review_fixture()
    decision = decision_fixture(review, decided_at="2026-08-21T20:00:10Z")
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:06:00Z", max_decision_age_seconds=300)
    assert "real_transport_decision_stale" in out["blockers"]


def test_replay_guard_rejects_seen_decision_hash():
    review = review_fixture()
    decision = decision_fixture(review)
    out = verify_real_transport_authorization(
        review, decision,
        verified_at_utc="2026-08-21T20:01:00Z",
        seen_decision_sha256={decision["real_transport_decision_sha256"]},
    )
    assert "real_transport_decision_replay_detected" in out["blockers"]
    assert out["authorization_record"] is None


def test_ttl_out_of_bounds_rejected():
    review = review_fixture()
    decision = decision_fixture(review)
    out = verify_real_transport_authorization(review, decision, verified_at_utc="2026-08-21T20:01:00Z", authorization_ttl_seconds=600)
    assert "authorization_ttl_out_of_bounds" in out["blockers"]
    assert out["authorization_record"] is None


def test_decision_before_review_and_future_both_fail_closed():
    review = review_fixture()
    before = decision_fixture(review, decided_at="2026-08-21T19:59:59Z")
    out1 = verify_real_transport_authorization(review, before, verified_at_utc="2026-08-21T20:01:00Z")
    assert "decision_precedes_review" in out1["blockers"]
    future = decision_fixture(review, decided_at="2026-08-21T20:02:00Z")
    out2 = verify_real_transport_authorization(review, future, verified_at_utc="2026-08-21T20:01:00Z")
    assert "decision_timestamp_in_future" in out2["blockers"]
