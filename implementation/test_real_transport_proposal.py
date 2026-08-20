from hashlib import sha256
import json
import socket
import pytest

from real_transport_proposal import build_real_transport_integration_proposal


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


def test_proposal_is_exact_inert_and_hash_bound():
    l=lease(); r=request(l)
    out=build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00Z")
    assert out["exact_scope"]["execution_request_sha256"] == r["execution_request_sha256"]
    assert out["authorization_granted"] is False
    assert out["transport_enabled"] is False
    assert out["network_capable"] is False
    assert out["network_calls_performed"] is False
    assert out["executable_callback_present"] is False
    core=dict(out); supplied=core.pop("real_transport_proposal_sha256")
    assert h(core) == supplied


def test_required_gates_cover_authorization_destination_limits_and_receipt():
    l=lease(); out=build_real_transport_integration_proposal(l,request(l),proposed_at_utc="2026-08-20T12:02:00Z")
    gates={g["gate"] for g in out["required_gates"]}
    assert {"fresh_explicit_real_user_authorization","transport_implementation_review","dns_and_destination_policy","redirect_policy","response_resource_limits","current_source_compliance","durable_receipt_binding"} <= gates


def test_build_does_not_touch_network(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("network primitive must not be called")
    monkeypatch.setattr(socket, "socket", fail)
    monkeypatch.setattr(socket, "getaddrinfo", fail)
    l=lease(); out=build_real_transport_integration_proposal(l,request(l),proposed_at_utc="2026-08-20T12:02:00Z")
    assert out["network_calls_performed"] is False


def test_tampered_lease_rejected():
    l=lease(); r=request(l); l["remaining_requests"]=0
    with pytest.raises(ValueError, match="authorization_lease_hash_mismatch"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00Z")


def test_scope_widened_request_rejected_even_if_rehashed():
    l=lease(); r=request(l); r["request_count"]=2
    core=dict(r); core.pop("execution_request_sha256"); r["execution_request_sha256"]=h(core)
    with pytest.raises(ValueError, match="execution_request_scope_widened"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00Z")


def test_credentials_or_action_rejected_even_if_rehashed():
    l=lease(); r=request(l); r["credentials_used"]=True
    core=dict(r); core.pop("execution_request_sha256"); r["execution_request_sha256"]=h(core)
    with pytest.raises(ValueError, match="execution_request_unsafe"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00Z")


def test_request_lease_binding_mismatch_rejected():
    l=lease(); r=request(l); r["authorization_lease_sha256"]="f"*64
    core=dict(r); core.pop("execution_request_sha256"); r["execution_request_sha256"]=h(core)
    with pytest.raises(ValueError, match="execution_request_lease_binding_mismatch"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00Z")


def test_proposal_time_must_be_inside_lease_window():
    l=lease(); r=request(l)
    with pytest.raises(ValueError, match="proposal_outside_lease_validity_window"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:10:00Z")
    with pytest.raises(ValueError, match="timestamp_must_be_utc_z"):
        build_real_transport_integration_proposal(l,r,proposed_at_utc="2026-08-20T12:02:00+00:00")
