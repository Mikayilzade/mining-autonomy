from copy import deepcopy
import pytest
from transport_preflight import build_transport_preflight, validate_explicit_read_only_authorization

def row(index=0,url="https://api.example.com/open"):
    return {"platform":"payanagent","item_index":index,"source_url":url,"manifest_item_sha256":f"sha-{index}","method":"GET",
    "expected_evidence_classes":["open_demand_snapshot"],"required_environment":"production",
    "provenance_checklist":["record_exact_source_url","record_capture_timestamp_utc"],
    "rate_limit":{"min_interval_seconds":10.0,"max_requests_per_window":2,"window_seconds":60.0,"budget_basis":"project_conservative_self_limit"},
    "readiness_state":"ready_for_future_explicit_read_only_capture","authorization_state":"explicit_read_only_network_authorization_required",
    "credentials_allowed":False,"network_calls_performed":False,"dry_run_only":True,"action_enabled":False}

def packet(rows):
    return {"schema_version":1,"mode":"deterministic_no_network_capture_readiness_packet","manifest_sha256":"m"*64,
    "ready_for_future_explicit_read_only_capture":rows,"blocked_by_observability_or_environment_requirement":[],
    "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
    "action_enabled":False,"missing_evidence_is_negative_demand":False}

def step(index=0,url="https://api.example.com/open",sequence=1,offset=0.0,host="api.example.com"):
    return {"sequence":sequence,"priority_index":index,"platform":"payanagent","item_index":index,"source_url":url,"host":host,"method":"GET",
    "scheduled_at_utc":"2026-08-20T01:00:00.000Z" if offset==0 else "2026-08-20T01:00:10.000Z","offset_seconds":offset,
    "expected_evidence_classes":["open_demand_snapshot"],"required_environment":"production",
    "provenance_checklist":["record_exact_source_url","record_capture_timestamp_utc"],"manifest_item_sha256":f"sha-{index}",
    "authorization_state":"explicit_read_only_network_authorization_required","credentials_allowed":False,
    "network_calls_performed":False,"dry_run_only":True,"action_enabled":False}

def plan(steps):
    return {"schema_version":1,"mode":"deterministic_no_network_capture_session_plan","manifest_sha256":"m"*64,
    "start_time_utc":"2026-08-20T01:00:00.000Z","total_request_budget":5,"total_time_budget_seconds":600.0,
    "planned_request_count":len(steps),"deferred_ready_count":0,"blocked_remediation_count":0,"chronological_session_plan":steps,
    "host_groups":[],"deferred_ready_items":[],"blocked_remediation_queue":[],
    "authorization_state":"explicit_read_only_network_authorization_required","authorization_granted":False,
    "network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,"action_enabled":False,
    "missing_evidence_is_negative_demand":False}

def preflight():
    return build_transport_preflight(plan([step()]),packet([row()]))

def auth(p):
    return {"schema_version":1,"mode":"explicit_read_only_network_authorization","authorization_granted":True,
    "scope":"exact_preflight_plan","session_plan_sha256":p["session_plan_sha256"],"allowed_methods":["GET"],
    "max_requests":p["planned_request_count"],"credentials_allowed":False,"action_enabled":False,
    "authorization_nonce":"synthetic-test","expires_at_utc":"2026-08-20T01:10:00Z"}

def test_exact_binding_and_inert_flags():
    p=preflight(); e=p["transport_envelopes"][0]
    assert e["source_url"]=="https://api.example.com/open"
    assert e["manifest_item_sha256"]=="sha-0"
    assert e["rate_limit"]["min_interval_seconds"]==10.0
    assert len(e["request_binding_sha256"])==64
    assert e["transport_enabled"] is False and p["network_calls_performed"] is False

def test_deterministic():
    a=plan([step()]); b=packet([row()])
    assert build_transport_preflight(a,b)==build_transport_preflight(deepcopy(a),deepcopy(b))

def test_manifest_and_source_tamper_fail():
    a=plan([step()]); b=packet([row()]); b["manifest_sha256"]="x"*64
    with pytest.raises(ValueError,match="manifest_hash_mismatch"): build_transport_preflight(a,b)
    with pytest.raises(ValueError,match="source_url_binding_mismatch"):
        build_transport_preflight(plan([step()]),packet([row(url="https://api.example.com/changed")]))

def test_host_and_schedule_fail():
    a=plan([step()]); a["chronological_session_plan"][0]["host"]="evil.example.com"
    with pytest.raises(ValueError,match="host_binding_mismatch"): build_transport_preflight(a,packet([row()]))
    a=plan([step()]); a["chronological_session_plan"][0]["scheduled_at_utc"]="2026-08-20T01:00:05Z"
    with pytest.raises(ValueError,match="schedule_offset_mismatch"): build_transport_preflight(a,packet([row()]))

def test_non_get_credentials_action_fail():
    for k,v,err in [("method","POST","non_get_forbidden"),("credentials_allowed",True,"credentials_allowed_invalid"),("action_enabled",True,"action_enabled_invalid")]:
        a=plan([step()]); a["chronological_session_plan"][0][k]=v
        with pytest.raises(ValueError,match=err): build_transport_preflight(a,packet([row()]))

def test_private_endpoints_fail():
    for url,h in [("https://127.0.0.1/x","127.0.0.1"),("https://10.0.0.1/x","10.0.0.1"),("https://localhost/x","localhost"),("https://service.internal/x","service.internal")]:
        with pytest.raises(ValueError,match="private_endpoint_forbidden"):
            build_transport_preflight(plan([step(url=url,host=h)]),packet([row(url=url)]))

def test_duplicate_item_fails():
    ss=[step(sequence=1),step(sequence=2,offset=10.0)]
    with pytest.raises(ValueError,match="duplicate_planned_item"): build_transport_preflight(plan(ss),packet([row()]))

def test_authorization_separate_and_hash_bound():
    p=preflight()
    with pytest.raises(ValueError,match="authorization_missing"): validate_explicit_read_only_authorization(p,None)
    a=auth(p); a["session_plan_sha256"]="0"*64
    with pytest.raises(ValueError,match="plan_hash_mismatch"): validate_explicit_read_only_authorization(p,a)

def test_authorization_cannot_enable_credentials_or_actions():
    p=preflight(); a=auth(p); a["credentials_allowed"]=True
    with pytest.raises(ValueError,match="credentials_forbidden"): validate_explicit_read_only_authorization(p,a)
    a=auth(p); a["action_enabled"]=True
    with pytest.raises(ValueError,match="action_forbidden"): validate_explicit_read_only_authorization(p,a)

def test_valid_synthetic_auth_validation_is_still_inert():
    p=preflight(); r=validate_explicit_read_only_authorization(p,auth(p))
    assert r["authorization_valid"] is True and r["validation_only"] is True
    assert r["transport_enabled"] is False and r["network_calls_performed"] is False
