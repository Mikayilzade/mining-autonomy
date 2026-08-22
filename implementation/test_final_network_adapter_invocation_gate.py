from hashlib import sha256
import json
from final_network_adapter_invocation_gate import build_final_network_adapter_invocation_gate as build

def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def rh(o,k): o[k]=h({a:b for a,b in o.items() if a!=k})

def fixture():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target-1","credentials_allowed":False,"action_enabled":False}; sh=h(scope)
    limits={"scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":1048576,"credentials_allowed":False,"action_enabled":False}
    packet="1"*64; auth="2"*64; pol="3"*64; dns="4"*64; tx="5"*64; src="6"*64
    ec={"schema_version":1,"mode":"single_attempt_final_real_observation_execution_envelope","envelope_state":"one_attempt_final_real_observation_ready_no_network","created_at":"2026-08-22T07:50:00Z","final_real_observation_review_packet_sha256":packet,"final_real_observation_authorization_sha256":auth,"adapter_id":"payan_readonly","target_fingerprint":"target-1","exact_scope_sha256":sh,"exact_scope":scope,"implementation_source_sha256":src,"hostname":"example.com","pinned_addresses":["93.184.216.34"],"policy_evidence_sha256":pol,"dns_evidence_sha256":dns,"transport_contract_sha256":tx,"transport_limits":limits,"max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"envelope_is_execution_result":False}
    e={**ec,"final_real_observation_execution_envelope_sha256":h(ec)}
    rc={"schema_version":1,"mode":"single_use_final_real_observation_consumption_receipt","consumption_state":"authorization_consumed_once_no_network","consumed_at":"2026-08-22T07:50:00Z","authorization_consumed":True,"final_real_observation_review_packet_sha256":packet,"final_real_observation_authorization_sha256":auth,"final_real_observation_execution_envelope_sha256":e["final_real_observation_execution_envelope_sha256"],"policy_evidence_sha256":pol,"dns_evidence_sha256":dns,"transport_contract_sha256":tx,"adapter_id":"payan_readonly","target_fingerprint":"target-1","exact_scope_sha256":sh,"network_capable_adapter_reachable":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"receipt_is_execution_token":False}
    r={**rc,"final_real_observation_consumption_receipt_sha256":h(rc)}
    ic={"schema_version":1,"mode":"deterministic_final_real_observation_authorization_consumption_preflight","consumption_state":"authorization_consumed_once_envelope_ready_no_network","final_real_observation_review_packet_sha256":packet,"final_real_observation_authorization_sha256":auth,"fresh_policy_evidence_sha256":pol,"fresh_dns_evidence_sha256":dns,"fresh_transport_contract_sha256":tx,"real_observation_execution_envelope":e,"consumption_receipt":r,"blockers":[],"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"consumption_record_is_execution_token":False}
    i={**ic,"final_real_observation_authorization_consumption_preflight_sha256":h(ic)}
    mc={"schema_version":1,"mode":"bound_network_capable_https_json_adapter_manifest","adapter_id":"payan_readonly","target_fingerprint":"target-1","exact_scope_sha256":sh,"implementation_source_sha256":src,"hostname":"example.com","pinned_addresses":["93.184.216.34"],"scheme":"https","tls_required":True,"method":"GET","max_network_requests_per_invocation":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":1048576,"credentials_allowed":False,"action_enabled":False,"network_capable":True,"dependency_injected_boundary":True,"uses_address_pinning":True,"uses_tls_server_name":True,"rejects_dns_reresolution_after_connect":True,"rejects_response_over_limit_after_decompression":True}
    m={**mc,"network_adapter_manifest_sha256":h(mc)}
    return i,m

def run(fx,at="2026-08-22T07:50:30Z",prior=()): return build(fx[0],fx[1],gated_at=at,prior_invocation_receipts=prior)

def test_clean_ready_no_call():
    o=run(fixture()); g=o["invocation_gate"]
    assert o["gate_state"]=="final_network_adapter_invocation_gate_ready_no_call" and g["request_spec"]["method"]=="GET"
    assert g["request_spec"]["pinned_addresses"]==["93.184.216.34"] and o["network_calls_performed"] is False

def test_i088_tamper():
    fx=list(fixture()); fx[0]["network_enabled"]=True; rh(fx[0],"final_real_observation_authorization_consumption_preflight_sha256")
    assert "i088_network_enabled_must_be_false" in run(tuple(fx))["blockers"]

def test_receipt_binding_drift():
    fx=list(fixture()); r=fx[0]["consumption_receipt"]; r["target_fingerprint"]="other"; rh(r,"final_real_observation_consumption_receipt_sha256"); rh(fx[0],"final_real_observation_authorization_consumption_preflight_sha256")
    assert "i088_receipt_target_fingerprint_binding_invalid" in run(tuple(fx))["blockers"]

def test_manifest_binding_drift():
    fx=list(fixture()); m=fx[1]; m["hostname"]="evil.example"; m["implementation_source_sha256"]="7"*64; m["pinned_addresses"]=["8.8.8.8"]; rh(m,"network_adapter_manifest_sha256"); b=set(run(tuple(fx))["blockers"])
    assert {"adapter_manifest_hostname_binding_invalid","adapter_manifest_implementation_source_sha256_binding_invalid","adapter_manifest_pinned_addresses_binding_invalid"}<=b

def test_manifest_transport_widening():
    fx=list(fixture()); m=fx[1]; m["allow_redirects"]=True; m["max_network_requests_per_invocation"]=2; m["credentials_allowed"]=True; rh(m,"network_adapter_manifest_sha256"); b=set(run(tuple(fx))["blockers"])
    assert {"adapter_manifest_allow_redirects_binding_invalid","adapter_manifest_max_network_requests_per_invocation_binding_invalid","adapter_manifest_credentials_allowed_binding_invalid"}<=b

def test_manifest_must_be_network_capable_and_pinned():
    fx=list(fixture()); m=fx[1]; m["network_capable"]=False; m["uses_address_pinning"]=False; rh(m,"network_adapter_manifest_sha256"); b=set(run(tuple(fx))["blockers"])
    assert {"adapter_manifest_not_network_capable","adapter_manifest_address_pinning_not_required"}<=b

def test_stale_envelope():
    assert "i088_envelope_too_old_for_network_gate" in run(fixture(),"2026-08-22T07:52:01Z")["blockers"]

def test_prior_attempt_consumes_one_shot():
    fx=fixture(); first=run(fx); g=first["invocation_gate"]
    pc={"schema_version":1,"mode":"single_use_final_network_adapter_invocation_receipt","invocation_state":"attempted_once_transport_error","final_real_observation_execution_envelope_sha256":g["i088_execution_envelope_sha256"],"final_real_observation_authorization_sha256":g["final_real_observation_authorization_sha256"],"one_shot_consumed":True}; p={**pc,"final_network_adapter_invocation_receipt_sha256":h(pc)}
    assert "final_network_adapter_invocation_replay_detected" in run(fx,prior=[p])["blockers"]

def test_private_pin_rejected():
    fx=list(fixture()); e=fx[0]["real_observation_execution_envelope"]; e["pinned_addresses"]=["127.0.0.1"]; rh(e,"final_real_observation_execution_envelope_sha256"); r=fx[0]["consumption_receipt"]; r["final_real_observation_execution_envelope_sha256"]=e["final_real_observation_execution_envelope_sha256"]; rh(r,"final_real_observation_consumption_receipt_sha256"); rh(fx[0],"final_real_observation_authorization_consumption_preflight_sha256"); m=fx[1]; m["pinned_addresses"]=["127.0.0.1"]; rh(m,"network_adapter_manifest_sha256")
    assert "i088_pinned_addresses_invalid" in run(tuple(fx))["blockers"]
