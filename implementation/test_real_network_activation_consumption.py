from hashlib import sha256
import json
from real_network_activation_consumption import consume_real_network_activation_authorization

def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def request():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"abc","credentials_allowed":False,"action_enabled":False}
    core={"schema_version":1,"mode":"real_network_activation_human_review_request","request_state":"ready_for_explicit_human_real_network_activation_decision","requested_at":"2026-08-22T01:00:00Z","expires_at":"2026-08-22T01:05:00Z","ttl_seconds":300,"implementation_binding_audit_sha256":"a","implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c","adapter_contract_readiness_sha256":"d","adapter_id":"future_https_json","exact_scope_sha256":"e","exact_scope":scope,"activation_interface":{},"authorization_lineage":{"real_transport_authorization_sha256":"x"},"human_summary":{},"explicit_human_decision_required":True,"activation_authorized":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"request_is_execution_token":False}
    return {**core,"real_network_activation_request_sha256":h(core)}

def authorization(req):
    core={"schema_version":1,"mode":"single_use_real_network_activation_authorization","authorization_state":"authorized_single_use_not_consumed","issued_at":"2026-08-22T01:02:00Z","expires_at":"2026-08-22T01:04:00Z","single_use":True,"consumed":False,"decision_id":"d1","real_network_activation_decision_sha256":"decisionhash","real_network_activation_request_sha256":req["real_network_activation_request_sha256"],**{k:req[k] for k in ("implementation_binding_audit_sha256","implementation_source_sha256","network_adapter_contract_validation_sha256","adapter_contract_readiness_sha256","adapter_id","exact_scope_sha256")},"exact_scope":req["exact_scope"],"authorization_lineage":req["authorization_lineage"],"adapter_invocation_authorized":True,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"authorization_is_payment_or_task_permission":False}
    return {**core,"real_network_activation_authorization_sha256":h(core)}

def test_clean_consumption_emits_one_attempt_zero_network_envelope():
    r=request(); a=authorization(r)
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert out["consumption_state"]=="authorization_consumed_once_envelope_ready_no_network"
    e=out["activation_envelope"]; rec=out["consumption_receipt"]
    assert e["max_adapter_invocations"]==1 and e["max_network_requests"]==1
    assert e["network_enabled"] is False and e["adapter_invoked"] is False
    assert rec["authorization_consumed"] is True and rec["network_calls_performed"] is False

def test_expired_authorization_rejected():
    r=request(); a=authorization(r)
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:04:01Z")
    assert "activation_authorization_expired_or_not_yet_valid" in out["blockers"]

def test_request_tamper_rejected():
    r=request(); a=authorization(r); r["adapter_id"]="tampered"
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_request_hash_invalid" in out["blockers"]

def test_authorization_hash_tamper_rejected():
    r=request(); a=authorization(r); a["adapter_id"]="tampered"
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_authorization_hash_invalid" in out["blockers"]

def test_request_binding_mismatch_rejected_even_with_rehash():
    r=request(); a=authorization(r); a["real_network_activation_request_sha256"]="wrong"
    a["real_network_activation_authorization_sha256"]=h({k:v for k,v in a.items() if k!="real_network_activation_authorization_sha256"})
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_authorization_request_binding_invalid" in out["blockers"]

def test_scope_widening_rejected():
    r=request(); a=authorization(r); a["exact_scope"]=dict(a["exact_scope"]); a["exact_scope"]["request_count"]=2
    a["real_network_activation_authorization_sha256"]=h({k:v for k,v in a.items() if k!="real_network_activation_authorization_sha256"})
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_authorization_scope_not_exact" in out["blockers"]

def test_credentials_widening_rejected():
    r=request(); a=authorization(r); a["credentials_allowed"]=True
    a["real_network_activation_authorization_sha256"]=h({k:v for k,v in a.items() if k!="real_network_activation_authorization_sha256"})
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_authorization_credentials_allowed_widened" in out["blockers"]

def test_preconsumed_authorization_rejected():
    r=request(); a=authorization(r); a["consumed"]=True; a["authorization_state"]="consumed"
    a["real_network_activation_authorization_sha256"]=h({k:v for k,v in a.items() if k!="real_network_activation_authorization_sha256"})
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    assert "activation_authorization_already_consumed" in out["blockers"]

def test_replay_receipt_rejected():
    r=request(); a=authorization(r)
    first=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z")
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:10Z",prior_consumption_receipts=[first["consumption_receipt"]])
    assert "activation_authorization_replay_detected" in out["blockers"]

def test_malformed_prior_receipt_fails_closed():
    r=request(); a=authorization(r)
    bad={"mode":"single_use_real_network_activation_consumption_receipt","real_network_activation_authorization_sha256":a["real_network_activation_authorization_sha256"],"consumption_state":"consumed_once_no_network","real_network_activation_consumption_receipt_sha256":"bad"}
    out=consume_real_network_activation_authorization(r,a,consumed_at="2026-08-22T01:03:00Z",prior_consumption_receipts=[bad])
    assert "prior_consumption_receipt_hash_invalid" in out["blockers"]
