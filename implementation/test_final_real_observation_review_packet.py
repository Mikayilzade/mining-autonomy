from copy import deepcopy
from hashlib import sha256
import json
from final_real_observation_review_packet import build_final_real_observation_review_packet as build

def h(v):return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def seal(c,k):return {**c,k:h(c)}
def fx():
    s={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target:abc","credentials_allowed":False,"action_enabled":False,"https_path_query":"/v1/tasks?state=open"};sh=h(s)
    env=seal({"mode":"single_attempt_exact_real_read_only_invocation_envelope","envelope_state":"one_attempt_bound_no_network","adapter_id":"payanagent-public-feed-v1","exact_scope":s,"exact_scope_sha256":sh,"source_lineage":{"implementation_source_sha256":"2"*64},"max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"adapter_invoked":False,"envelope_is_execution_result":False},"exact_real_read_only_invocation_envelope_sha256")
    rec=seal({"mode":"single_use_exact_real_read_only_invocation_consumption_receipt","consumption_state":"consumed_once_no_network","authorization_consumed":True,"exact_real_read_only_invocation_envelope_sha256":env["exact_real_read_only_invocation_envelope_sha256"],"adapter_id":env["adapter_id"],"exact_scope_sha256":sh},"exact_real_read_only_invocation_consumption_receipt_sha256")
    inert={"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False}
    i84=seal({"mode":"deterministic_exact_real_read_only_invocation_authorization_consumption_preflight","consumption_state":"authorization_consumed_once_envelope_ready_no_network","real_read_only_invocation_envelope":env,"consumption_receipt":rec,"blockers":[],**inert,"consumption_record_is_execution_token":False},"exact_real_read_only_invocation_consumption_preflight_sha256")
    safe=seal({"mode":"single_attempt_real_transport_safety_envelope","safety_state":"safety_prerequisites_attested_no_network","checked_at":"2026-08-22T06:01:00Z","i084_consumption_preflight_sha256":i84["exact_real_read_only_invocation_consumption_preflight_sha256"],"i084_invocation_envelope_sha256":env["exact_real_read_only_invocation_envelope_sha256"],"i084_consumption_receipt_sha256":rec["exact_real_read_only_invocation_consumption_receipt_sha256"],"policy_evidence_sha256":"e"*64,"dns_evidence_sha256":"f"*64,"transport_contract_sha256":"0"*64,"adapter_id":env["adapter_id"],"target_fingerprint":s["target_fingerprint"],"exact_scope_sha256":sh,"implementation_source_sha256":"2"*64,"hostname":"tasks.example.com","pinned_addresses":["8.8.8.8","1.1.1.1"],"scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":1048576,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"safety_envelope_is_execution_token":False},"real_transport_safety_envelope_sha256")
    i85=seal({"mode":"deterministic_real_transport_safety_preflight","preflight_state":"real_transport_safety_evidence_ready_no_network","i084_consumption_preflight_sha256":i84["exact_real_read_only_invocation_consumption_preflight_sha256"],"i084_invocation_envelope_sha256":env["exact_real_read_only_invocation_envelope_sha256"],"policy_evidence_sha256":safe["policy_evidence_sha256"],"dns_evidence_sha256":safe["dns_evidence_sha256"],"transport_contract_sha256":safe["transport_contract_sha256"],"real_transport_safety_envelope":safe,"blockers":[],**inert,"preflight_record_is_execution_token":False},"real_transport_safety_preflight_sha256")
    return i84,i85

def reseal85(i):
    s=dict(i["real_transport_safety_envelope"]);s.pop("real_transport_safety_envelope_sha256");i["real_transport_safety_envelope"]=seal(s,"real_transport_safety_envelope_sha256");c=dict(i);c.pop("real_transport_safety_preflight_sha256");return seal(c,"real_transport_safety_preflight_sha256")
def test_valid():
    a,b=fx();r=build(a,b,requested_at="2026-08-22T06:02:00Z",ttl_seconds=180);p=r["final_real_observation_review_packet"]
    assert r["builder_state"].endswith("ready_no_network") and not r["blockers"]
    assert p["path_query"]=="/v1/tasks?state=open" and p["exact_scope"]["https_path_query"]==p["path_query"]
    assert p["pinned_addresses"]==["1.1.1.1","8.8.8.8"] and p["explicit_final_human_decision_required"] and not p["final_real_observation_authorized"] and not p["network_capable_adapter_reachable"]
def test_missing_exact_path_fails_closed_native():
    a,b=fx();a["real_read_only_invocation_envelope"]["exact_scope"].pop("https_path_query")
    r=build(a,b,requested_at="2026-08-22T06:02:00Z")
    assert r["final_real_observation_review_packet"] is None and "native_https_path_query_missing" in r["blockers"]
def test_tamper_hash():
    a,b=fx();b["preflight_state"]="x";r=build(a,b,requested_at="2026-08-22T06:02:00Z");assert "i085_hash_invalid" in r["blockers"] and r["final_real_observation_review_packet"] is None
def test_cross_binding():
    a,b=fx();c=dict(a);c.pop("exact_real_read_only_invocation_consumption_preflight_sha256");c["x"]=1;a2=seal(c,"exact_real_read_only_invocation_consumption_preflight_sha256");r=build(a2,b,requested_at="2026-08-22T06:02:00Z");assert "i085_i084_binding_invalid" in r["blockers"]
def test_private_duplicate_pins():
    a,b=fx();s=dict(b["real_transport_safety_envelope"]);s["pinned_addresses"]=["127.0.0.1","127.0.0.1"];s.pop("real_transport_safety_envelope_sha256");b["real_transport_safety_envelope"]=seal(s,"real_transport_safety_envelope_sha256");b=reseal85(b);r=build(a,b,requested_at="2026-08-22T06:02:00Z");assert "pinned_addresses_duplicate" in r["blockers"] and "pinned_addresses_non_public" in r["blockers"]
def test_transport_widening():
    a,b=fx();s=dict(b["real_transport_safety_envelope"]);s.update(allow_redirects=True,max_redirects=2,max_network_requests=2,allowed_content_types=["application/json","text/html"]);s.pop("real_transport_safety_envelope_sha256");b["real_transport_safety_envelope"]=seal(s,"real_transport_safety_envelope_sha256");b=reseal85(b);r=build(a,b,requested_at="2026-08-22T06:02:00Z");assert {"redirect_contract_invalid","json_only_invalid","one_get_invalid"}<=set(r["blockers"])
def test_widened_flag():
    a,b=fx();s=dict(b["real_transport_safety_envelope"]);s["network_capable_adapter_reachable"]=True;s.pop("real_transport_safety_envelope_sha256");b["real_transport_safety_envelope"]=seal(s,"real_transport_safety_envelope_sha256");b=reseal85(b);r=build(a,b,requested_at="2026-08-22T06:02:00Z");assert "i085_safety_network_capable_adapter_reachable_must_be_false" in r["blockers"]
def test_time_ttl():
    a,b=fx();assert "ttl_out_of_range" in build(a,b,requested_at="2026-08-22T06:02:00Z",ttl_seconds=901)["blockers"]
    assert "requested_at_invalid_or_not_utc" in build(a,b,requested_at="2026-08-22T10:02:00+04:00")["blockers"]
    f=deepcopy(b);s=dict(f["real_transport_safety_envelope"]);s["checked_at"]="2026-08-22T06:10:00Z";s.pop("real_transport_safety_envelope_sha256");f["real_transport_safety_envelope"]=seal(s,"real_transport_safety_envelope_sha256");f=reseal85(f);assert "safety_check_from_future" in build(a,f,requested_at="2026-08-22T06:02:00Z")["blockers"]
