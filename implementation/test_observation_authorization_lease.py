from hashlib import sha256
import json

from observation_authorization_lease import (
    ATTEMPT_MODE,
    build_observation_authorization_lease,
    consume_observation_authorization_lease,
)


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def request():
    core = {
        "schema_version": 1,
        "mode": "deterministic_market_observation_human_decision_request",
        "request_state": "decision_requested",
        "requested_at_utc": "2026-08-21T15:00:00Z",
        "expires_at_utc": "2026-08-21T15:05:00Z",
        "market_side_readiness_sha256": "a" * 64,
        "exact_scope_sha256": "b" * 64,
        "current_resource_backend_id": "python_local",
        "decision_scope": {
            "allowed_decisions": ["authorize_one_read_only_observation", "deny"],
            "authorization_target": {
                "method": "GET",
                "request_count": 1,
                "required_environment": "production",
                "target_fingerprint": "payan-public-feed",
                "credentials_allowed": False,
                "action_enabled": False,
                "market_side_readiness_sha256": "a" * 64,
                "exact_scope_sha256": "b" * 64,
            },
        },
        "blockers": [],
        "authorization_granted": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "request_is_authorization": False,
        "request_is_execution_token": False,
    }
    return {**core, "human_decision_request_sha256": h(core)}


def verification(r=None, authorized=True):
    r = r or request()
    core = {
        "schema_version": 1,
        "mode": "deterministic_human_decision_record_verifier",
        "verification_state": "explicit_read_only_authorization_verified" if authorized else "explicit_deny_verified",
        "verified_at_utc": "2026-08-21T15:02:00Z",
        "decision": "authorize_one_read_only_observation" if authorized else "deny",
        "human_decision_request_sha256": r["human_decision_request_sha256"],
        "market_side_readiness_sha256": r["market_side_readiness_sha256"],
        "exact_scope_sha256": r["exact_scope_sha256"],
        "current_resource_backend_id": "python_local",
        "authorization_scope": {
            "method": "GET",
            "request_count": 1,
            "required_environment": "production",
            "target_fingerprint": "payan-public-feed",
            "credentials_allowed": False,
            "action_enabled": False,
        } if authorized else None,
        "blockers": [],
        "human_decision_recorded": True,
        "explicit_authorization_verified": authorized,
        "explicit_deny_verified": not authorized,
        "real_user_consent_inferred_from_chat_history": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "record_is_execution_token": False,
        "record_is_transport_lease": False,
    }
    return {**core, "human_decision_verification_sha256": h(core)}


def attempt(**overrides):
    a = {
        "mode": ATTEMPT_MODE,
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": "payan-public-feed",
        "credentials_used": False,
        "action_enabled": False,
        "network_transport_callback_present": False,
    }
    a.update(overrides)
    return a


def test_exact_authorization_builds_short_lived_single_use_lease():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z", lease_ttl_seconds=120)
    assert lease["lease_state"] == "single_use_observation_lease_ready"
    assert lease["expires_at_utc"] == "2026-08-21T15:04:30Z"
    assert lease["max_consumptions"] == 1
    assert lease["network_enabled"] is False and lease["transport_enabled"] is False


def test_lease_never_outlives_request_expiry():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:04:30Z", lease_ttl_seconds=120)
    assert lease["lease_state"] == "single_use_observation_lease_ready"
    assert lease["expires_at_utc"] == "2026-08-21T15:05:00Z"


def test_deny_record_cannot_issue_lease():
    r = request(); v = verification(r, authorized=False)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    assert lease["lease_state"] == "lease_rejected"
    assert "explicit_read_only_authorization_not_verified" in lease["blockers"]


def test_tampered_verification_or_widened_request_rejected():
    r = request(); v = verification(r)
    v["current_resource_backend_id"] = "other"
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    assert "human_decision_verification_hash_invalid" in lease["blockers"]
    r = request(); v = verification(r)
    r["decision_scope"]["authorization_target"]["request_count"] = 2
    c = dict(r); c.pop("human_decision_request_sha256")
    r["human_decision_request_sha256"] = h(c)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    assert "request_scope_not_exact_anonymous_get" in lease["blockers"]


def test_exact_synthetic_attempt_consumes_once_without_network():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    receipt = consume_observation_authorization_lease(lease, attempt(), consumed_at_utc="2026-08-21T15:03:00Z")
    assert receipt["consumption_state"] == "lease_consumed"
    assert receipt["lease_consumed"] is True
    assert receipt["remaining_consumptions"] == 0
    assert receipt["network_enabled"] is False and receipt["transport_enabled"] is False


def test_replay_double_consumption_rejected():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    first = consume_observation_authorization_lease(lease, attempt(), consumed_at_utc="2026-08-21T15:03:00Z")
    second = consume_observation_authorization_lease(
        lease, attempt(), consumed_at_utc="2026-08-21T15:03:10Z", prior_consumption_receipts=[first]
    )
    assert second["consumption_state"] == "consumption_rejected"
    assert "lease_replay_or_double_consumption" in second["blockers"]


def test_expired_or_scope_widened_attempt_rejected():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z", lease_ttl_seconds=30)
    expired = consume_observation_authorization_lease(lease, attempt(), consumed_at_utc="2026-08-21T15:03:00Z")
    assert "lease_expired_or_not_yet_valid" in expired["blockers"]
    widened = consume_observation_authorization_lease(
        lease, attempt(request_count=2, action_enabled=True), consumed_at_utc="2026-08-21T15:02:45Z"
    )
    assert "attempt_request_count_not_one" in widened["blockers"]
    assert "attempt_action_forbidden" in widened["blockers"]


def test_network_callback_or_tampered_prior_receipt_fail_closed():
    r = request(); v = verification(r)
    lease = build_observation_authorization_lease(v, r, issued_at_utc="2026-08-21T15:02:30Z")
    bad_attempt = consume_observation_authorization_lease(
        lease, attempt(network_transport_callback_present=True), consumed_at_utc="2026-08-21T15:03:00Z"
    )
    assert "network_transport_callback_forbidden_in_i071" in bad_attempt["blockers"]
    first = consume_observation_authorization_lease(lease, attempt(), consumed_at_utc="2026-08-21T15:03:00Z")
    first["consumed_at_utc"] = "2026-08-21T15:03:01Z"
    out = consume_observation_authorization_lease(
        lease, attempt(), consumed_at_utc="2026-08-21T15:03:10Z", prior_consumption_receipts=[first]
    )
    assert "prior_consumption_receipt_hash_invalid" in out["blockers"]
