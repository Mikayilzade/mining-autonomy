from hashlib import sha256
import json
from copy import deepcopy
import pytest
from authorization_readiness import build_authorization_readiness_packet


def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def quality(history_hash, repeat=True, label="regressing"):
    core={"schema_version":1,"mode":"longitudinal_capture_integrity_gate","history_sha256":history_hash,
          "capture_integrity_label":label,"economic_evidence_classification":"not_evaluated_capture_integrity_is_not_demand",
          "future_read_only_capture_worth_repeating_for_integrity":repeat,
          "future_read_only_capture_recommendation":"repeat_may_diagnose_capture_regression_after_explicit_authorization" if repeat else "no_repeat_needed_for_capture_integrity_only",
          "authorization_required":True,"dry_run_only":True,"action_enabled":False,"network_calls_performed":False,"credentials_used":False}
    return {**core,"quality_gate_sha256":h(core)}

def packet():
    return {"schema_version":1,"mode":"deterministic_no_network_capture_readiness_packet","manifest_sha256":"m"*64,
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def plan():
    return {"schema_version":1,"mode":"deterministic_no_network_capture_session_plan","manifest_sha256":"m"*64,
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def envelope(seq=1, priority=0, item=0):
    b={"sequence":seq,"priority_index":priority,"platform":"payanagent","item_index":item,
       "source_url":f"https://api.example.com/open/{item}","host":"api.example.com","port":None,"method":"GET",
       "scheduled_at_utc":"2026-08-20T10:00:00.000Z","offset_seconds":0.0,"manifest_item_sha256":f"sha-{item}",
       "manifest_sha256":"m"*64,"expected_evidence_classes":["open_demand_snapshot"],"required_environment":"production",
       "provenance_checklist":["record_exact_source_url","record_capture_timestamp_utc"],
       "rate_limit":{"min_interval_seconds":10.0,"max_requests_per_window":2,"window_seconds":60.0,"budget_basis":"project_conservative_self_limit"},
       "timeout_seconds":20.0,"allowed_request_headers":["Accept","User-Agent"],
       "forbidden_request_headers":["Authorization","Cookie","Proxy-Authorization"],
       "redirect_policy":"disabled_until_explicit_authorized_transport","dns_policy":"resolve_at_execution_and_reject_non_global_addresses",
       "credentials_allowed":False,"action_enabled":False}
    return {**b,"request_binding_sha256":h(b),"transport_interface":"ReadOnlyGetTransportV1","transport_enabled":False,
            "authorization_granted":False,"network_calls_performed":False,"dry_run_only":True}

def preflight(p, pk, envs):
    return {"schema_version":1,"mode":"deterministic_read_only_transport_preflight","manifest_sha256":"m"*64,
            "session_plan_sha256":h(p),"readiness_packet_sha256":h(pk),"transport_envelope_set_sha256":h(envs),
            "planned_request_count":len(envs),"transport_envelopes":envs,"transport_enabled":False,
            "authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,
            "action_enabled":False,"missing_evidence_is_negative_demand":False}

def history(plan_hash, env_hash):
    core={"schema_version":1,"mode":"capture_session_attestation_history","session_plan_sha256":plan_hash,
          "transport_envelope_set_sha256":env_hash,"network_calls_performed":False,"credentials_used":False,
          "dry_run_only":True,"action_enabled":False}
    return {**core,"history_sha256":h(core)}

def bundle(envs=None, repeat=True):
    pk=packet(); p=plan(); envs=[envelope()] if envs is None else envs; pf=preflight(p,pk,envs); hist=history(h(p),h(envs)); q=quality(hist["history_sha256"],repeat=repeat)
    return q,hist,pk,p,pf

def test_single_exact_get_ready_packet_is_inert():
    args=bundle(); out=build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")
    assert out["decision"]=="single_request_exact_plan_ready_for_user_authorization"
    assert out["minimal_future_read_only_capture"]["method"]=="GET"
    assert out["proposed_authorization_draft"]["authorization_granted"] is False
    assert out["network_calls_performed"] is False and out["action_enabled"] is False

def test_no_repeat_emits_no_capture_needed():
    args=bundle(repeat=False); out=build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")
    assert out["decision"]=="no_capture_needed_for_integrity_only"
    assert out["minimal_future_read_only_capture"] is None

def test_multiple_envelopes_selects_one_but_requires_replan():
    args=bundle([envelope(1,0,0),envelope(2,1,1)]); out=build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")
    assert out["decision"]=="minimal_single_request_replan_required_before_user_authorization"
    assert out["minimal_future_read_only_capture"]["item_index"]==0
    assert out["proposed_authorization_draft"] is None

def test_empty_preflight_when_repeat_recommended_is_blocked():
    args=bundle([]); out=build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")
    assert out["decision"]=="capture_recommended_but_no_exact_ready_request_available"

def test_quality_hash_tamper_fails_closed():
    args=list(bundle()); args[0]["capture_integrity_label"]="stable"
    with pytest.raises(ValueError,match="quality_hash_mismatch"):
        build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")

def test_history_plan_binding_mismatch_fails_closed():
    args=list(bundle()); hist=deepcopy(args[1]); core=dict(hist); core.pop("history_sha256"); core["session_plan_sha256"]="9"*64; hist={**core,"history_sha256":h(core)}; args[1]=hist
    q=quality(hist["history_sha256"]); args[0]=q
    with pytest.raises(ValueError,match="history_session_binding_mismatch"):
        build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")

def test_envelope_request_hash_tamper_fails_closed_even_if_set_rehashed():
    args=list(bundle()); pf=deepcopy(args[4]); pf["transport_envelopes"][0]["source_url"]="https://api.example.com/tampered"; pf["transport_envelope_set_sha256"]=h(pf["transport_envelopes"]); args[4]=pf
    with pytest.raises(ValueError,match="history_transport_binding_mismatch|request_binding_hash_mismatch"):
        build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z")

def test_ttl_bounds_fail_closed():
    args=bundle()
    with pytest.raises(ValueError,match="ttl_invalid"):
        build_authorization_readiness_packet(*args,decision_time_utc="2026-08-20T10:05:00Z",proposed_ttl_seconds=30)
