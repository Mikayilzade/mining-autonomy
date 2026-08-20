from hashlib import sha256
import json
import pytest
from authorization_lease import issue_single_use_authorization_lease, consume_single_use_authorization_lease


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def consent(authorize=True):
    auth_core = {
        "schema_version":1,"mode":"verified_exact_read_only_execution_authorization",
        "exact_authorization_request_packet_sha256":"a"*64,
        "authorization_request_sha256":"b"*64,"scope_sha256":"c"*64,"decision_sha256":"d"*64,
        "verified_at_utc":"2026-08-20T12:00:00Z","expires_at_utc":"2026-08-20T12:10:00Z",
        "max_requests":1,"method":"GET","required_environment":"production",
        "credentials_allowed":False,"action_enabled":False,"authorization_granted":True,
        "transport_enabled":False,"network_calls_performed":False,"offline_verification_only":True,
        "synthetic_fixture_not_real_consent":True,
    }
    auth = {**auth_core, "execution_authorization_sha256": h(auth_core)} if authorize else None
    core = {
        "schema_version":1,"mode":"deterministic_offline_authorization_consent_verification",
        "verified_at_utc":"2026-08-20T12:00:00Z","decision":"authorize" if authorize else "deny",
        "decision_sha256":"d"*64,"authorization_valid":authorize,"execution_authorization":auth,
        "transport_enabled":False,"network_calls_performed":False,"credentials_allowed":False,
        "action_enabled":False,"offline_only":True,"real_user_consent_inferred":False,"scope_widened":False,
    }
    return {**core, "consent_verification_sha256": h(core)}


def attempt(lease):
    core = {
        "schema_version":1,"mode":"offline_single_request_execution_attempt",
        "authorization_lease_sha256":lease["authorization_lease_sha256"],
        "execution_authorization_sha256":lease["execution_authorization_sha256"],
        "method":"GET","required_environment":"production","request_count":1,
        "credentials_used":False,"action_enabled":False,"transport_requested":False,
        "target_fingerprint":"synthetic-read-only-fixture",
    }
    return {**core, "attempt_sha256": h(core)}


def test_issue_binds_exact_execution_authorization_and_is_inert():
    c = consent(); lease = issue_single_use_authorization_lease(c, issued_at_utc="2026-08-20T12:01:00Z")
    assert lease["execution_authorization_sha256"] == c["execution_authorization"]["execution_authorization_sha256"]
    assert lease["remaining_requests"] == 1 and lease["transport_enabled"] is False
    assert lease["synthetic_fixture_not_real_consent"] is True


def test_consume_once_exhausts_budget_without_transport():
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z")
    receipt = consume_single_use_authorization_lease(lease, attempt(lease), attempted_at_utc="2026-08-20T12:02:00Z")
    assert receipt["consumed"] is True and receipt["remaining_requests"] == 0
    assert receipt["network_calls_performed"] is False


def test_replay_with_prior_receipt_is_rejected():
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z"); a = attempt(lease)
    receipt = consume_single_use_authorization_lease(lease, a, attempted_at_utc="2026-08-20T12:02:00Z")
    with pytest.raises(ValueError, match="lease_replay_or_double_consumption"):
        consume_single_use_authorization_lease(lease, a, attempted_at_utc="2026-08-20T12:03:00Z", prior_consumption_receipts=[receipt])


def test_expired_lease_is_rejected():
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z")
    with pytest.raises(ValueError, match="lease_attempt_outside_validity_window"):
        consume_single_use_authorization_lease(lease, attempt(lease), attempted_at_utc="2026-08-20T12:10:00Z")


def test_tampered_consent_is_rejected():
    c = consent(); c["scope_widened"] = True
    with pytest.raises(ValueError, match="lease_consent_hash_mismatch"):
        issue_single_use_authorization_lease(c, issued_at_utc="2026-08-20T12:01:00Z")


def test_scope_widening_attempt_is_rejected_even_if_rehashed():
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z"); a = attempt(lease)
    a["request_count"] = 2; core = dict(a); core.pop("attempt_sha256"); a["attempt_sha256"] = h(core)
    with pytest.raises(ValueError, match="lease_attempt_scope_widened"):
        consume_single_use_authorization_lease(lease, a, attempted_at_utc="2026-08-20T12:02:00Z")


def test_attempt_bound_to_other_lease_is_rejected():
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z"); a = attempt(lease)
    a["authorization_lease_sha256"] = "e"*64; core = dict(a); core.pop("attempt_sha256"); a["attempt_sha256"] = h(core)
    with pytest.raises(ValueError, match="lease_attempt_binding_mismatch"):
        consume_single_use_authorization_lease(lease, a, attempted_at_utc="2026-08-20T12:02:00Z")


def test_deny_cannot_issue_lease_and_transport_request_is_rejected():
    with pytest.raises(ValueError, match="lease_authorization_not_valid"):
        issue_single_use_authorization_lease(consent(False), issued_at_utc="2026-08-20T12:01:00Z")
    lease = issue_single_use_authorization_lease(consent(), issued_at_utc="2026-08-20T12:01:00Z"); a = attempt(lease)
    a["transport_requested"] = True; core = dict(a); core.pop("attempt_sha256"); a["attempt_sha256"] = h(core)
    with pytest.raises(ValueError, match="lease_transport_must_remain_disabled_in_i042"):
        consume_single_use_authorization_lease(lease, a, attempted_at_utc="2026-08-20T12:02:00Z")
