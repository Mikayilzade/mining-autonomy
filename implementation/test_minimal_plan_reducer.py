from copy import deepcopy
from hashlib import sha256
import json
import pytest
from minimal_plan_reducer import build_minimal_plan_reduction


def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def packet():
    return {"schema_version":1,"mode":"deterministic_no_network_capture_readiness_packet","manifest_sha256":"m"*64,
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def step(seq=1,priority=0,item=0,offset=0.0):
    return {"sequence":seq,"priority_index":priority,"platform":"payanagent","item_index":item,
            "source_url":f"https://api.example.com/open/{item}","host":"api.example.com","method":"GET",
            "scheduled_at_utc":"2026-08-20T10:00:00.000Z","offset_seconds":offset,
            "expected_evidence_classes":["open_demand_snapshot"],"required_environment":"production",
            "provenance_checklist":["record_exact_source_url","record_capture_timestamp_utc"],
            "manifest_item_sha256":f"sha-{item}","authorization_state":"explicit_read_only_network_authorization_required",
            "credentials_allowed":False,"network_calls_performed":False,"dry_run_only":True,"action_enabled":False}

def plan(steps):
    return {"schema_version":1,"mode":"deterministic_no_network_capture_session_plan","manifest_sha256":"m"*64,
            "start_time_utc":"2026-08-20T10:00:00.000Z","total_request_budget":len(steps),"total_time_budget_seconds":120.0,
            "planned_request_count":len(steps),"deferred_ready_count":0,"blocked_remediation_count":0,
            "chronological_session_plan":steps,"host_groups":[{"host":"api.example.com","request_count":len(steps),"sequence_numbers":[s["sequence"] for s in steps]}],
            "deferred_ready_items":[],"blocked_remediation_queue":[],"authorization_state":"explicit_read_only_network_authorization_required",
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def env(s):
    b={"sequence":s["sequence"],"priority_index":s["priority_index"],"platform":s["platform"],"item_index":s["item_index"],
       "source_url":s["source_url"],"host":s["host"],"port":None,"method":"GET","scheduled_at_utc":s["scheduled_at_utc"],
       "offset_seconds":s["offset_seconds"],"manifest_item_sha256":s["manifest_item_sha256"],"manifest_sha256":"m"*64,
       "expected_evidence_classes":list(s["expected_evidence_classes"]),"required_environment":"production",
       "provenance_checklist":list(s["provenance_checklist"]),
       "rate_limit":{"min_interval_seconds":10.0,"max_requests_per_window":2,"window_seconds":60.0,"budget_basis":"project_conservative_self_limit"},
       "timeout_seconds":20.0,"allowed_request_headers":["Accept","User-Agent"],"forbidden_request_headers":["Authorization","Cookie","Proxy-Authorization"],
       "redirect_policy":"disabled_until_explicit_authorized_transport","dns_policy":"resolve_at_execution_and_reject_non_global_addresses",
       "credentials_allowed":False,"action_enabled":False}
    return {**b,"request_binding_sha256":h(b),"transport_interface":"ReadOnlyGetTransportV1","transport_enabled":False,
            "authorization_granted":False,"network_calls_performed":False,"dry_run_only":True}

def preflight(p,pk,envs):
    return {"schema_version":1,"mode":"deterministic_read_only_transport_preflight","manifest_sha256":"m"*64,
            "session_plan_sha256":h(p),"readiness_packet_sha256":h(pk),"transport_envelope_set_sha256":h(envs),
            "planned_request_count":len(envs),"transport_envelopes":envs,"transport_enabled":False,
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def decision(pk,p,pf,kind="minimal_single_request_replan_required_before_user_authorization",target=None):
    if target is None and kind not in ("no_capture_needed_for_integrity_only","capture_recommended_but_no_exact_ready_request_available"):
        e=pf["transport_envelopes"][0]
        target={k:e[k] for k in ("sequence","priority_index","platform","item_index","source_url","host","method","manifest_item_sha256","request_binding_sha256","expected_evidence_classes","provenance_checklist","required_environment","rate_limit","timeout_seconds")}
    core={"schema_version":1,"mode":"deterministic_authorization_readiness_decision_packet",
          "readiness_packet_sha256":h(pk),"session_plan_sha256":h(p),"transport_envelope_set_sha256":h(pf["transport_envelopes"]),
          "decision":kind,"minimal_future_read_only_capture":target,"authorization_granted":False,"credentials_allowed":False,
          "network_calls_performed":False,"dry_run_only":True,"action_enabled":False}
    return {**core,"authorization_readiness_sha256":h(core)}

def bundle(n=2,kind="minimal_single_request_replan_required_before_user_authorization"):
    pk=packet(); steps=[step(i+1,i,i,10.0*i) for i in range(n)]; p=plan(steps); envs=[env(s) for s in steps]; pf=preflight(p,pk,envs); d=decision(pk,p,pf,kind)
    return d,pk,p,pf

def test_multi_request_reduces_to_exact_single_get_and_preserves_semantics():
    d,pk,p,pf=bundle(2); out=build_minimal_plan_reduction(d,pk,p,pf)
    assert out["outcome"]=="reduced_to_exact_single_get_plan"
    rp=out["reduced_session_plan"]; rf=out["reduced_transport_preflight"]
    assert rp["planned_request_count"]==1 and rf["planned_request_count"]==1
    assert rp["chronological_session_plan"][0]["source_url"]==pf["transport_envelopes"][0]["source_url"]
    re=rf["transport_envelopes"][0]; oe=pf["transport_envelopes"][0]
    for k in ("source_url","host","method","manifest_item_sha256","expected_evidence_classes","provenance_checklist","rate_limit","timeout_seconds"):
        assert re[k]==oe[k]
    assert rf["readiness_packet_sha256"]==h(pk)
    assert rf["session_plan_sha256"]==h(rp)
    assert out["authorization_granted"] is False and out["network_calls_performed"] is False

def test_unselected_request_does_not_leak_into_reduced_plan():
    d,pk,p,pf=bundle(3); out=build_minimal_plan_reduction(d,pk,p,pf)
    urls=json.dumps(out["reduced_transport_preflight"]["transport_envelopes"])
    assert "/open/0" in urls and "/open/1" not in urls and "/open/2" not in urls
    assert len(out["reduced_session_plan"]["deferred_ready_items"])==2

def test_no_capture_is_inert_noop():
    d,pk,p,pf=bundle(2,"no_capture_needed_for_integrity_only")
    out=build_minimal_plan_reduction(d,pk,p,pf)
    assert out["outcome"]=="no_op_no_capture_needed"
    assert out["reduced_session_plan"] is None and out["reduced_transport_preflight"] is None

def test_single_ready_is_already_minimal_no_rebuild():
    d,pk,p,pf=bundle(1,"single_request_exact_plan_ready_for_user_authorization")
    out=build_minimal_plan_reduction(d,pk,p,pf)
    assert out["outcome"]=="already_minimal_exact_plan_no_reduction_needed"
    assert out["reduced_session_plan"] is None

def test_blocked_is_no_reduction():
    pk=packet(); p=plan([]); pf=preflight(p,pk,[]); d=decision(pk,p,pf,"capture_recommended_but_no_exact_ready_request_available")
    out=build_minimal_plan_reduction(d,pk,p,pf)
    assert out["outcome"]=="blocked_no_exact_request_to_reduce"

def test_decision_hash_tamper_fails_closed():
    d,pk,p,pf=bundle(2); d["decision"]="no_capture_needed_for_integrity_only"
    with pytest.raises(ValueError,match="decision_hash_mismatch"):
        build_minimal_plan_reduction(d,pk,p,pf)

def test_original_plan_binding_tamper_fails_closed():
    d,pk,p,pf=bundle(2); p=deepcopy(p); p["total_time_budget_seconds"]=999
    with pytest.raises(ValueError,match="plan_binding_mismatch|decision_plan_binding_mismatch"):
        build_minimal_plan_reduction(d,pk,p,pf)

def test_selected_request_binding_tamper_fails_closed():
    d,pk,p,pf=bundle(2); pf=deepcopy(pf); pf["transport_envelopes"][0]["source_url"]="https://api.example.com/tampered"
    pf["transport_envelope_set_sha256"]=h(pf["transport_envelopes"]); d=decision(pk,p,pf)
    with pytest.raises(ValueError,match="original_request_binding_mismatch"):
        build_minimal_plan_reduction(d,pk,p,pf)
