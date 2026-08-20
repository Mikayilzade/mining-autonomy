from hashlib import sha256
import json
import pytest
from execution_wrapper import DeterministicSyntheticTransport, execute_with_single_use_lease


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def lease():
    core = {
        "schema_version":1,"mode":"deterministic_single_use_read_only_authorization_lease",
        "consent_verification_sha256":"a"*64,"execution_authorization_sha256":"b"*64,
        "authorization_request_sha256":"c"*64,"scope_sha256":"d"*64,"decision_sha256":"e"*64,
        "issued_at_utc":"2026-08-20T12:01:00Z","expires_at_utc":"2026-08-20T12:10:00Z",
        "max_requests":1,"remaining_requests":1,"method":"GET","required_environment":"production",
        "credentials_allowed":False,"action_enabled":False,"transport_enabled":False,
        "network_calls_performed":False,"offline_consumption_only":True,"single_use":True,
        "synthetic_fixture_not_real_consent":True,
    }
    return {**core,"authorization_lease_sha256":h(core)}


def request(l):
    core = {
        "schema_version":1,"mode":"dependency_injected_single_get_execution_request",
        "authorization_lease_sha256":l["authorization_lease_sha256"],
        "execution_authorization_sha256":l["execution_authorization_sha256"],
        "method":"GET","required_environment":"production","request_count":1,
        "credentials_used":False,"action_enabled":False,"target_fingerprint":"fixture.example/api/tasks",
    }
    return {**core,"execution_request_sha256":h(core)}


class CountingSyntheticTransport(DeterministicSyntheticTransport):
    def __init__(self): self.calls = 0
    def execute(self, req):
        self.calls += 1
        return super().execute(req)


class FakeRealTransport:
    transport_kind = "http"
    network_capable = True
    def execute(self, req):
        raise AssertionError("must never run")


def test_default_transport_is_synthetic_and_inert():
    l=lease(); out=execute_with_single_use_lease(l,request(l),attempted_at_utc="2026-08-20T12:02:00Z")
    assert out["transport_kind"] == "synthetic_stub"
    assert out["network_calls_performed"] is False
    assert out["remaining_requests"] == 0
    assert out["synthetic_response"]["body"]["synthetic"] is True


def test_consumption_happens_before_transport_call():
    l=lease(); t=CountingSyntheticTransport()
    out=execute_with_single_use_lease(l,request(l),attempted_at_utc="2026-08-20T12:02:00Z",transport=t)
    assert t.calls == 1 and out["lease_consumed_before_transport"] is True


def test_expired_lease_prevents_transport_invocation():
    l=lease(); t=CountingSyntheticTransport()
    with pytest.raises(ValueError, match="lease_attempt_outside_validity_window"):
        execute_with_single_use_lease(l,request(l),attempted_at_utc="2026-08-20T12:10:00Z",transport=t)
    assert t.calls == 0


def test_prior_receipt_replay_prevents_transport_invocation():
    l=lease(); req=request(l); t=CountingSyntheticTransport()
    execute_with_single_use_lease(l,req,attempted_at_utc="2026-08-20T12:02:00Z",transport=t)
    receipt={
        "schema_version":1,"mode":"deterministic_offline_authorization_lease_consumption",
        "authorization_lease_sha256":l["authorization_lease_sha256"],"execution_authorization_sha256":l["execution_authorization_sha256"],
        "attempt_sha256":"f"*64,"consumed_at_utc":"2026-08-20T12:02:00Z","consumed":True,"requests_consumed":1,
        "remaining_requests":0,"replay_allowed":False,"transport_enabled":False,"network_calls_performed":False,
        "credentials_used":False,"action_enabled":False,"offline_consumption_only":True,"synthetic_fixture_not_real_consent":True,
    }
    receipt["lease_consumption_sha256"]=h(receipt)
    before=t.calls
    with pytest.raises(ValueError, match="lease_replay_or_double_consumption"):
        execute_with_single_use_lease(l,req,attempted_at_utc="2026-08-20T12:03:00Z",transport=t,prior_consumption_receipts=[receipt])
    assert t.calls == before


def test_real_transport_flag_fails_closed_before_any_transport():
    l=lease(); t=CountingSyntheticTransport()
    with pytest.raises(ValueError, match="real_transport_not_supported_in_i043"):
        execute_with_single_use_lease(l,request(l),attempted_at_utc="2026-08-20T12:02:00Z",transport=t,allow_real_transport=True)
    assert t.calls == 0


def test_network_capable_transport_is_rejected():
    l=lease()
    with pytest.raises(ValueError, match="non_synthetic_transport_rejected"):
        execute_with_single_use_lease(l,request(l),attempted_at_utc="2026-08-20T12:02:00Z",transport=FakeRealTransport())


def test_scope_widening_is_rejected_before_transport():
    l=lease(); r=request(l); r["request_count"]=2; core=dict(r); core.pop("execution_request_sha256"); r["execution_request_sha256"]=h(core)
    t=CountingSyntheticTransport()
    with pytest.raises(ValueError, match="execution_request_scope_widened"):
        execute_with_single_use_lease(l,r,attempted_at_utc="2026-08-20T12:02:00Z",transport=t)
    assert t.calls == 0


def test_tampered_request_is_rejected_before_transport():
    l=lease(); r=request(l); r["target_fingerprint"]="tampered"; t=CountingSyntheticTransport()
    with pytest.raises(ValueError, match="execution_request_hash_mismatch"):
        execute_with_single_use_lease(l,r,attempted_at_utc="2026-08-20T12:02:00Z",transport=t)
    assert t.calls == 0
