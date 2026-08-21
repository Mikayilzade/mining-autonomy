from copy import deepcopy
from real_transport_authorization_consumption import consume_real_transport_authorization, _hash

def verification_fixture():
    scope = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": "payanagent:public-task-feed:v1",
        "credentials_allowed": False,
        "action_enabled": False,
    }
    auth_core = {
        "schema_version": 1,
        "mode": "single_use_real_transport_authorization_record",
        "authorization_state": "authorized_exact_single_read_only_transport",
        "issued_at_utc": "2026-08-21T20:01:00Z",
        "expires_at_utc": "2026-08-21T20:03:00Z",
        "pre_real_transport_review_sha256": "r" * 64,
        "real_transport_decision_sha256": "d" * 64,
        "exact_scope_sha256": "s" * 64,
        "authorization_scope": scope,
        "max_consumptions": 1,
        "authorization_is_single_use": True,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "transport_enabled": False,
        "record_is_execution_token": False,
    }
    auth = {**auth_core, "real_transport_authorization_sha256": _hash(auth_core)}
    core = {
        "schema_version": 1,
        "mode": "deterministic_real_transport_authorization_verifier",
        "verification_state": "explicit_real_transport_authorization_verified",
        "verified_at_utc": "2026-08-21T20:01:00Z",
        "decision": "authorize_exact_read_only_transport",
        "pre_real_transport_review_sha256": "r" * 64,
        "real_transport_decision_sha256": "d" * 64,
        "exact_scope_sha256": "s" * 64,
        "authorization_record": auth,
        "blockers": [],
        "human_decision_recorded": True,
        "explicit_real_transport_authorization_verified": True,
        "explicit_real_transport_deny_verified": False,
        "real_user_authorization_inferred_from_chat_history": False,
        "authorization_is_short_lived": True,
        "authorization_is_single_use": True,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "verification_record_is_execution_token": False,
    }
    return {**core, "real_transport_authorization_verification_sha256": _hash(core)}

def rehash(obj, field):
    core = deepcopy(obj)
    core.pop(field, None)
    core[field] = _hash(core)
    return core

def rehash_auth_and_verification(v):
    v["authorization_record"] = rehash(v["authorization_record"], "real_transport_authorization_sha256")
    return rehash(v, "real_transport_authorization_verification_sha256")

def test_valid_consumption_emits_inert_attempt_envelope():
    v = verification_fixture()
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert out["consumption_state"] == "authorization_consumed_preflight_ready_no_network"
    assert out["blockers"] == []
    env = out["authorized_attempt_envelope"]
    assert env["exact_scope"] == v["authorization_record"]["authorization_scope"]
    assert env["max_network_requests"] == 1
    assert env["authorization_consumed"] is True
    assert env["authorization_reusable"] is False
    assert env["transport_adapter_present"] is False
    assert env["network_enabled"] is False

def test_mandatory_transport_gates_are_embedded():
    env = consume_real_transport_authorization(verification_fixture(), consumed_at_utc="2026-08-21T20:02:00Z")["authorized_attempt_envelope"]
    gates = env["mandatory_transport_gates"]
    assert gates["dns_policy"]["reject_loopback_private_link_local_reserved_required"] is True
    assert gates["dns_policy"]["destination_pinning_required"] is True
    assert gates["redirect_policy"]["automatic_redirects_allowed"] is False
    assert gates["redirect_policy"]["max_redirects"] == 0
    assert gates["response_policy"]["max_body_bytes"] == 1_048_576
    assert gates["response_policy"]["allowed_content_types"] == ["application/json"]
    assert gates["source_policy"]["fresh_first_party_compliance_evidence_required"] is True

def test_verification_hash_tamper_fails_closed():
    v = verification_fixture()
    v["network_enabled"] = True
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "i074_verification_hash_invalid" in out["blockers"]
    assert out["authorized_attempt_envelope"] is None

def test_unverified_state_fails_closed_even_if_rehashed():
    v = verification_fixture()
    v["verification_state"] = "explicit_real_transport_deny_verified"
    v["explicit_real_transport_authorization_verified"] = False
    v = rehash(v, "real_transport_authorization_verification_sha256")
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "i074_authorization_not_verified" in out["blockers"]

def test_authorization_hash_tamper_fails_closed():
    v = verification_fixture()
    v["authorization_record"]["expires_at_utc"] = "2026-08-21T20:04:00Z"
    v = rehash(v, "real_transport_authorization_verification_sha256")
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "authorization_record_hash_invalid" in out["blockers"]

def test_rehashed_scope_widening_fails_closed():
    v = verification_fixture()
    v["authorization_record"]["authorization_scope"]["request_count"] = 2
    v = rehash_auth_and_verification(v)
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "authorization_scope_not_exact_anonymous_get" in out["blockers"]

def test_binding_mismatch_fails_closed():
    v = verification_fixture()
    v["authorization_record"]["real_transport_decision_sha256"] = "x" * 64
    v = rehash_auth_and_verification(v)
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "decision_hash_binding_invalid" in out["blockers"]

def test_replay_or_double_consumption_rejected():
    v = verification_fixture()
    h = v["authorization_record"]["real_transport_authorization_sha256"]
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z", seen_consumed_authorization_sha256={h})
    assert "authorization_replay_or_double_consumption_detected" in out["blockers"]
    assert out["authorization_consumed"] is False

def test_expired_at_boundary_rejected():
    out = consume_real_transport_authorization(verification_fixture(), consumed_at_utc="2026-08-21T20:03:00Z")
    assert "authorization_expired_before_consumption" in out["blockers"]

def test_consumption_before_issue_rejected():
    out = consume_real_transport_authorization(verification_fixture(), consumed_at_utc="2026-08-21T20:00:59Z")
    assert "consumption_precedes_authorization_issue" in out["blockers"]

def test_non_single_use_rejected_even_if_rehashed():
    v = verification_fixture()
    v["authorization_record"]["max_consumptions"] = 2
    v = rehash_auth_and_verification(v)
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "authorization_not_single_use" in out["blockers"]

def test_unsafe_authorization_flag_rejected():
    v = verification_fixture()
    v["authorization_record"]["credentials_allowed"] = True
    v = rehash_auth_and_verification(v)
    out = consume_real_transport_authorization(v, consumed_at_utc="2026-08-21T20:02:00Z")
    assert "unsafe_or_missing_authorization_credentials_allowed" in out["blockers"]
    assert out["network_enabled"] is False
    assert out["value_movement_enabled"] is False
