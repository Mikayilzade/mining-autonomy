from hashlib import sha256
import json
from real_network_activation_decision import verify_real_network_activation_decision


def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def request():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"abc","credentials_allowed":False,"action_enabled":False}
    core={"schema_version":1,"mode":"real_network_activation_human_review_request","request_state":"ready_for_explicit_human_real_network_activation_decision","requested_at":"2026-08-22T01:00:00Z","expires_at":"2026-08-22T01:05:00Z","ttl_seconds":300,"implementation_binding_audit_sha256":"a","implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c","adapter_contract_readiness_sha256":"d","adapter_id":"future_https_json","exact_scope_sha256":"e","exact_scope":scope,"activation_interface":{},"authorization_lineage":{"x":"y"},"human_summary":{},"explicit_human_decision_required":True,"activation_authorized":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"request_is_execution_token":False}
    return {**core,"real_network_activation_request_sha256":h(core)}

def decision(req, value="authorize"):
    core={"mode":"explicit_real_network_activation_human_decision","decision_id":"d1","decision":value,"decided_at":"2026-08-22T01:01:00Z","single_use":True,"real_network_activation_request_sha256":req["real_network_activation_request_sha256"],**{k:req[k] for k in ("implementation_binding_audit_sha256","implementation_source_sha256","network_adapter_contract_validation_sha256","adapter_contract_readiness_sha256","adapter_id","exact_scope_sha256")},"exact_scope":req["exact_scope"],"authorization_lineage":req["authorization_lineage"],"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False}
    return {**core,"real_network_activation_decision_sha256":h(core)}

def test_authorize_emits_inert_single_use_record():
    r=request(); out=verify_real_network_activation_decision(r,decision(r),verified_at="2026-08-22T01:02:00Z")
    assert out["verification_state"]=="activation_authorization_issued_not_consumed"
    a=out["activation_authorization"]; assert a["single_use"] and not a["consumed"] and a["max_network_requests"]==1
    assert out["network_enabled"] is False and out["adapter_invoked"] is False

def test_deny_emits_no_authorization():
    r=request(); out=verify_real_network_activation_decision(r,decision(r,"deny"),verified_at="2026-08-22T01:02:00Z")
    assert out["verification_state"]=="denied_no_activation_authorization" and out["activation_authorization"] is None

def test_request_hash_tamper_rejected():
    r=request(); d=decision(r); r["adapter_id"]="widened"
    assert verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["verification_state"]=="decision_rejected"

def test_stale_request_rejected():
    r=request(); assert "activation_request_stale_or_not_yet_valid" in verify_real_network_activation_decision(r,decision(r),verified_at="2026-08-22T01:06:00Z")["blockers"]

def test_wrong_request_binding_rejected():
    r=request(); d=decision(r); d["real_network_activation_request_sha256"]="wrong"; d["real_network_activation_decision_sha256"]=h({k:v for k,v in d.items() if k!="real_network_activation_decision_sha256"})
    assert "human_decision_request_binding_invalid" in verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["blockers"]

def test_scope_widening_rejected():
    r=request(); d=decision(r); d["exact_scope"]["request_count"]=2; d["real_network_activation_decision_sha256"]=h({k:v for k,v in d.items() if k!="real_network_activation_decision_sha256"})
    assert verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["verification_state"]=="decision_rejected"

def test_credentials_widening_rejected():
    r=request(); d=decision(r); d["credentials_allowed"]=True; d["real_network_activation_decision_sha256"]=h({k:v for k,v in d.items() if k!="real_network_activation_decision_sha256"})
    assert "human_decision_credentials_allowed_widened" in verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["blockers"]

def test_future_decision_rejected():
    r=request(); d=decision(r); d["decided_at"]="2026-08-22T01:03:00Z"; d["real_network_activation_decision_sha256"]=h({k:v for k,v in d.items() if k!="real_network_activation_decision_sha256"})
    assert "human_decision_from_future" in verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["blockers"]

def test_bad_decision_hash_rejected():
    r=request(); d=decision(r); d["real_network_activation_decision_sha256"]="bad"
    assert "human_decision_hash_invalid" in verify_real_network_activation_decision(r,d,verified_at="2026-08-22T01:02:00Z")["blockers"]

def test_ttl_bounds_rejected():
    r=request(); out=verify_real_network_activation_decision(r,decision(r),verified_at="2026-08-22T01:02:00Z",authorization_ttl_seconds=301)
    assert "authorization_ttl_out_of_range" in out["blockers"]
