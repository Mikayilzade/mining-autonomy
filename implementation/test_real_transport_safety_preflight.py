from hashlib import sha256
import json
from real_transport_safety_preflight import build_real_transport_safety_preflight as build

def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def rh(o,k): o[k]=h({a:b for a,b in o.items() if a!=k})

def fixture():
    s={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target-abc","credentials_allowed":False,"action_enabled":False}; sh=h(s)
    lin={"implementation_binding_audit_sha256":"a","implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c","adapter_contract_readiness_sha256":"d","real_network_activation_authorization_sha256":"e","real_network_activation_request_sha256":"f"}
    ec={"schema_version":1,"mode":"single_attempt_exact_real_read_only_invocation_envelope","envelope_state":"one_attempt_bound_no_network","created_at":"2026-08-22T05:50:00Z","exact_real_read_only_invocation_request_sha256":"r"*64,"exact_real_read_only_invocation_decision_sha256":"d"*64,"exact_real_read_only_invocation_authorization_sha256":"a"*64,"activation_envelope_invocation_gate_sha256":"g","synthetic_adapter_invocation_receipt_sha256":"s","real_network_activation_consumption_preflight_sha256":"p","real_network_activation_envelope_sha256":"n","adapter_id":"future_https_json","exact_scope_sha256":sh,"exact_scope":s,"source_lineage":lin,"max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"adapter_invoked":False,"envelope_is_execution_result":False}
    e={**ec,"exact_real_read_only_invocation_envelope_sha256":h(ec)}
    rc={"schema_version":1,"mode":"single_use_exact_real_read_only_invocation_consumption_receipt","consumption_state":"consumed_once_no_network","consumed_at":"2026-08-22T05:50:00Z","exact_real_read_only_invocation_request_sha256":"r"*64,"exact_real_read_only_invocation_decision_sha256":"d"*64,"exact_real_read_only_invocation_authorization_sha256":"a"*64,"exact_real_read_only_invocation_envelope_sha256":e["exact_real_read_only_invocation_envelope_sha256"],"adapter_id":"future_https_json","exact_scope_sha256":sh,"authorization_consumed":True,"network_capable_adapter_reachable":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"receipt_is_execution_token":False}
    r={**rc,"exact_real_read_only_invocation_consumption_receipt_sha256":h(rc)}
    ic={"schema_version":1,"mode":"deterministic_exact_real_read_only_invocation_authorization_consumption_preflight","consumption_state":"authorization_consumed_once_envelope_ready_no_network","exact_real_read_only_invocation_request_sha256":"r"*64,"exact_real_read_only_invocation_decision_sha256":"d"*64,"exact_real_read_only_invocation_authorization_sha256":"a"*64,"real_read_only_invocation_envelope":e,"consumption_receipt":r,"blockers":[],"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"consumption_record_is_execution_token":False}
    i={**ic,"exact_real_read_only_invocation_consumption_preflight_sha256":h(ic)}
    common={"target_fingerprint":"target-abc","adapter_id":"future_https_json","exact_scope_sha256":sh,"implementation_source_sha256":"b"*64}
    pc={"schema_version":1,"mode":"first_party_anonymous_read_only_policy_evidence",**common,"source_kind":"provider_first_party","source_ref":"https://example.com/terms","source_content_sha256":"1"*64,"observed_at":"2026-08-22T05:54:00Z","max_age_seconds":3600,"anonymous_read_only_get_allowed":True,"credentials_required":False,"automated_access_prohibited":False}
    dc={"schema_version":1,"mode":"offline_dns_resolution_evidence",**common,"source_kind":"system_probe","source_content_sha256":"2"*64,"observed_at":"2026-08-22T05:54:30Z","max_age_seconds":300,"hostname":"example.com","canonical_name":"example.com","aliases":[],"resolved_addresses":["8.8.8.8"],"pinned_addresses":["8.8.8.8"],"all_addresses_public":True,"alias_chain_checked":True,"rebinding_check_passed":True,"address_pinning_required":True}
    tc={"schema_version":1,"mode":"offline_https_json_transport_contract",**common,"hostname":"example.com","scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":1048576,"reject_content_encoding_expansion_over_limit":True,"pin_resolved_addresses":True,"reuse_dns_after_connect":False,"credentials_allowed":False,"action_enabled":False}
    return i,{**pc,"policy_evidence_sha256":h(pc)},{**dc,"dns_evidence_sha256":h(dc)},{**tc,"transport_contract_sha256":h(tc)}

def run(i,p,d,t,at="2026-08-22T05:55:00Z"):
    return build(i,policy_evidence=p,dns_evidence=d,transport_contract=t,checked_at=at)

def test_clean_is_inert():
    i,p,d,t=fixture(); o=run(i,p,d,t); e=o["real_transport_safety_envelope"]
    assert o["preflight_state"]=="real_transport_safety_evidence_ready_no_network"
    assert e["pinned_addresses"]==["8.8.8.8"] and e["max_network_requests"]==1
    assert o["network_enabled"] is False and o["network_capable_adapter_reachable"] is False and e["safety_envelope_is_execution_token"] is False

def test_i084_tamper_and_widening_fail_closed():
    i,p,d,t=fixture(); i["network_enabled"]=True
    assert "i084_preflight_hash_invalid" in run(i,p,d,t)["blockers"]
    i,p,d,t=fixture(); e=i["real_read_only_invocation_envelope"]; e["max_network_requests"]=2; rh(e,"exact_real_read_only_invocation_envelope_sha256"); i["consumption_receipt"]["exact_real_read_only_invocation_envelope_sha256"]=e["exact_real_read_only_invocation_envelope_sha256"]; rh(i["consumption_receipt"],"exact_real_read_only_invocation_consumption_receipt_sha256"); rh(i,"exact_real_read_only_invocation_consumption_preflight_sha256")
    assert "i084_one_attempt_limits_invalid" in run(i,p,d,t)["blockers"]

def test_policy_fresh_first_party_and_bound():
    i,p,d,t=fixture(); p.update(source_kind="community_post",anonymous_read_only_get_allowed=False,automated_access_prohibited=True,implementation_source_sha256="9"*64); rh(p,"policy_evidence_sha256"); b=set(run(i,p,d,t)["blockers"])
    assert {"policy_evidence_not_first_party","policy_anonymous_read_only_get_not_allowed","policy_automated_access_prohibited","policy_evidence_implementation_source_sha256_binding_invalid"}<=b
    i,p,d,t=fixture(); p["observed_at"]="2026-08-20T05:54:00Z"; rh(p,"policy_evidence_sha256")
    assert "policy_evidence_stale" in run(i,p,d,t)["blockers"]

def test_dns_public_pinned_and_antirebinding():
    i,p,d,t=fixture(); d.update(resolved_addresses=["127.0.0.1"],pinned_addresses=["127.0.0.1"],all_addresses_public=True,rebinding_check_passed=False,alias_chain_checked=False); rh(d,"dns_evidence_sha256"); b=set(run(i,p,d,t)["blockers"])
    assert {"dns_resolution_contains_non_public_address","dns_rebinding_check_not_passed","dns_alias_chain_not_checked"}<=b
    i,p,d,t=fixture(); d["pinned_addresses"]=["1.1.1.1"]; rh(d,"dns_evidence_sha256")
    assert "dns_pinned_addresses_do_not_match_resolution" in run(i,p,d,t)["blockers"]

def test_transport_https_zero_redirect_bounded_json():
    i,p,d,t=fixture(); t.update(scheme="http",tls_required=False,allow_redirects=True,max_redirects=1,allowed_content_types=["text/html"],max_response_bytes=1048577); rh(t,"transport_contract_sha256"); b=set(run(i,p,d,t)["blockers"])
    assert {"transport_scheme_not_https","transport_tls_not_required","transport_redirects_not_zero","transport_content_type_not_json_only","transport_response_bound_invalid"}<=b

def test_target_hostname_binding():
    i,p,d,t=fixture(); t.update(target_fingerprint="other",hostname="other.example"); rh(t,"transport_contract_sha256"); b=set(run(i,p,d,t)["blockers"])
    assert {"transport_contract_target_fingerprint_binding_invalid","dns_transport_hostname_binding_invalid"}<=b

def test_future_or_non_utc_evidence_fails():
    i,p,d,t=fixture(); p["observed_at"]=d["observed_at"]="2026-08-22T05:56:00Z"; rh(p,"policy_evidence_sha256"); rh(d,"dns_evidence_sha256"); b=set(run(i,p,d,t)["blockers"])
    assert {"policy_evidence_from_future","dns_evidence_from_future"}<=b
    i,p,d,t=fixture(); o=run(i,p,d,t,"2026-08-22T09:55:00+04:00")
    assert "checked_at_invalid_or_not_utc" in o["blockers"] and o["real_transport_safety_envelope"] is None
