from hashlib import sha256
import json
import pytest
from authorization_consent import verify_explicit_authorization_consent

def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def wrapper():
    scope={"platform":"payanagent","source_url":"https://api.example.com/open/0","host":"api.example.com","method":"GET",
           "required_environment":"production","manifest_item_sha256":"sha-0","request_binding_sha256":"r"*64,
           "expected_evidence_classes":["open_demand_snapshot"],"provenance_checklist":["record_exact_source_url"],
           "rate_limit":{"min_interval_seconds":10.0},"timeout_seconds":20.0,"max_requests":1,
           "credentials_allowed":False,"action_enabled":False,"redirect_policy":"disabled_until_explicit_authorized_transport",
           "dns_policy":"resolve_at_execution_and_reject_non_global_addresses"}
    req={"schema_version":1,"mode":"exact_read_only_network_authorization_request","human_summary":"one GET only",
         "scope":scope,"scope_sha256":h(scope),"reduced_session_plan_sha256":"a"*64,
         "reduced_transport_preflight_sha256":"b"*64,"not_before_utc":"2026-08-20T10:30:00Z",
         "expires_at_utc":"2026-08-20T10:35:00Z","ttl_seconds":300,"authorization_granted":False,
         "authorization_nonce":None,"authorization_token":None,"credentials_allowed":False,
         "network_calls_performed":False,"transport_enabled":False,"dry_run_only":True,"action_enabled":False,
         "user_authorization_required":True,"authorization_scope_widened":False}
    req["authorization_request_sha256"]=h(req)
    core={"schema_version":1,"mode":"deterministic_exact_read_only_authorization_request",
          "minimal_plan_reduction_sha256":"c"*64,"request_time_utc":"2026-08-20T10:30:00Z","ttl_seconds":300,
          "state":"exact_single_get_ready_for_explicit_user_authorization",
          "state_reason":"fixture","exact_authorization_request":req,"authorization_required":True,
          "authorization_granted":False,"authorization_nonce":None,"credentials_allowed":False,
          "network_calls_performed":False,"transport_enabled":False,"dry_run_only":True,"action_enabled":False,
          "authorization_scope_widened":False,"economic_evidence_classification":"not_evaluated_capture_integrity_is_not_demand",
          "missing_capture_interpretation":"unknown_not_negative_demand"}
    return {**core,"exact_authorization_request_packet_sha256":h(core)}

def decision(w, value="authorize", when="2026-08-20T10:31:00Z", synthetic=True):
    req=w["exact_authorization_request"]
    core={"schema_version":1,"mode":"explicit_human_read_only_authorization_decision","decision":value,
          "decided_at_utc":when,"exact_authorization_request_packet_sha256":w["exact_authorization_request_packet_sha256"],
          "authorization_request_sha256":req["authorization_request_sha256"],"scope_sha256":req["scope_sha256"],
          "human_scope_acknowledged":True,"max_requests":1,"method":"GET","credentials_allowed":False,
          "action_enabled":False,"synthetic_fixture":synthetic}
    return {**core,"decision_sha256":h(core)}

def test_explicit_authorize_emits_bound_offline_authorization():
    w=wrapper(); d=decision(w)
    out=verify_explicit_authorization_consent(w,d,verification_time_utc="2026-08-20T10:32:00Z")
    a=out["execution_authorization"]
    assert out["authorization_valid"] is True and a["authorization_granted"] is True
    assert a["transport_enabled"] is False and a["offline_verification_only"] is True
    assert a["scope_sha256"]==w["exact_authorization_request"]["scope_sha256"]
    assert a["synthetic_fixture_not_real_consent"] is True

def test_deny_is_valid_decision_but_no_execution_authorization():
    w=wrapper(); out=verify_explicit_authorization_consent(w,decision(w,"deny"),verification_time_utc="2026-08-20T10:32:00Z")
    assert out["authorization_valid"] is False and out["execution_authorization"] is None

def test_expired_request_fails_closed():
    w=wrapper()
    with pytest.raises(ValueError,match="outside_validity_window"):
        verify_explicit_authorization_consent(w,decision(w),verification_time_utc="2026-08-20T10:36:00Z")

def test_scope_binding_tamper_fails_closed_even_if_decision_rehashed():
    w=wrapper(); d=decision(w); d["scope_sha256"]="0"*64
    dc=dict(d); dc.pop("decision_sha256"); d["decision_sha256"]=h(dc)
    with pytest.raises(ValueError,match="scope_binding_mismatch"):
        verify_explicit_authorization_consent(w,d,verification_time_utc="2026-08-20T10:32:00Z")

def test_wrapper_tamper_fails_closed():
    w=wrapper(); w["state_reason"]="tamper"
    with pytest.raises(ValueError,match="wrapper_hash_mismatch"):
        verify_explicit_authorization_consent(w,decision(wrapper()),verification_time_utc="2026-08-20T10:32:00Z")

def test_scope_widening_fails_closed():
    w=wrapper(); d=decision(w); d["max_requests"]=2
    dc=dict(d); dc.pop("decision_sha256"); d["decision_sha256"]=h(dc)
    with pytest.raises(ValueError,match="scope_widened"):
        verify_explicit_authorization_consent(w,d,verification_time_utc="2026-08-20T10:32:00Z")

def test_missing_human_acknowledgement_fails_closed():
    w=wrapper(); d=decision(w); d["human_scope_acknowledged"]=False
    dc=dict(d); dc.pop("decision_sha256"); d["decision_sha256"]=h(dc)
    with pytest.raises(ValueError,match="acknowledgement_required"):
        verify_explicit_authorization_consent(w,d,verification_time_utc="2026-08-20T10:32:00Z")

def test_decision_time_must_be_inside_request_window_and_not_future():
    w=wrapper()
    with pytest.raises(ValueError,match="decision_time_invalid"):
        verify_explicit_authorization_consent(w,decision(w,when="2026-08-20T10:29:59Z"),verification_time_utc="2026-08-20T10:32:00Z")
    with pytest.raises(ValueError,match="decision_time_invalid"):
        verify_explicit_authorization_consent(w,decision(w,when="2026-08-20T10:33:00Z"),verification_time_utc="2026-08-20T10:32:00Z")
