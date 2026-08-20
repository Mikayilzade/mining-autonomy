from hashlib import sha256
import json
import pytest
from exact_authorization_request import build_exact_authorization_request


def h(v): return sha256(json.dumps(v, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()).hexdigest()

def env():
    b={"sequence":1,"priority_index":0,"platform":"payanagent","item_index":0,"source_url":"https://api.example.com/open/0","host":"api.example.com","port":None,"method":"GET","scheduled_at_utc":"2026-08-20T10:00:00.000Z","offset_seconds":0.0,"manifest_item_sha256":"sha-0","manifest_sha256":"m"*64,"expected_evidence_classes":["open_demand_snapshot"],"required_environment":"production","provenance_checklist":["record_exact_source_url","record_capture_timestamp_utc"],"rate_limit":{"min_interval_seconds":10.0,"max_requests_per_window":2,"window_seconds":60.0,"budget_basis":"project_conservative_self_limit"},"timeout_seconds":20.0,"allowed_request_headers":["Accept","User-Agent"],"forbidden_request_headers":["Authorization","Cookie","Proxy-Authorization"],"redirect_policy":"disabled_until_explicit_authorized_transport","dns_policy":"resolve_at_execution_and_reject_non_global_addresses","credentials_allowed":False,"action_enabled":False}
    return {**b,"request_binding_sha256":h(b),"transport_interface":"ReadOnlyGetTransportV1","transport_enabled":False,"authorization_granted":False,"network_calls_performed":False,"dry_run_only":True}

def reduction(outcome="reduced_to_exact_single_get_plan"):
    rp=rf=None
    if outcome=="reduced_to_exact_single_get_plan":
        e=env(); step={k:e[k] for k in ("sequence","priority_index","platform","item_index","source_url","host","method","scheduled_at_utc","offset_seconds","expected_evidence_classes","required_environment","provenance_checklist","manifest_item_sha256","credentials_allowed","network_calls_performed","dry_run_only","action_enabled")}; step["authorization_state"]="explicit_read_only_network_authorization_required"
        rp={"schema_version":1,"mode":"deterministic_no_network_capture_session_plan","manifest_sha256":"m"*64,"start_time_utc":"2026-08-20T10:00:00.000Z","total_request_budget":1,"total_time_budget_seconds":120.0,"planned_request_count":1,"deferred_ready_count":0,"blocked_remediation_count":0,"chronological_session_plan":[step],"host_groups":[{"host":"api.example.com","request_count":1,"sequence_numbers":[1]}],"deferred_ready_items":[],"blocked_remediation_queue":[],"authorization_state":"explicit_read_only_network_authorization_required","authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,"action_enabled":False,"missing_evidence_is_negative_demand":False}
        rf={"schema_version":1,"mode":"deterministic_read_only_transport_preflight","manifest_sha256":"m"*64,"session_plan_sha256":h(rp),"readiness_packet_sha256":"r"*64,"transport_envelope_set_sha256":h([e]),"planned_request_count":1,"transport_envelopes":[e],"authorization_contract":{"required_mode":"explicit_read_only_network_authorization","required_scope":"exact_preflight_plan","required_session_plan_sha256":h(rp),"allowed_methods":["GET"],"required_max_requests":1,"credentials_allowed":False,"action_enabled":False},"transport_enabled":False,"authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,"dry_run_only":True,"action_enabled":False,"missing_evidence_is_negative_demand":False}
    core={"schema_version":1,"mode":"deterministic_minimal_single_request_plan_reduction","authorization_readiness_sha256":"a"*64,"original_readiness_packet_sha256":"b"*64,"original_session_plan_sha256":"c"*64,"original_transport_envelope_set_sha256":"d"*64,"selected_original_request_binding_sha256":None,"outcome":outcome,"outcome_reason":"fixture","reduced_session_plan":rp,"reduced_session_plan_sha256":h(rp) if rp is not None else None,"reduced_transport_preflight":rf,"reduced_transport_envelope_set_sha256":rf["transport_envelope_set_sha256"] if rf else None,"authorization_required":True,"authorization_granted":False,"credentials_allowed":False,"network_calls_performed":False,"dry_run_only":True,"action_enabled":False,"authorization_scope_widened":False,"economic_evidence_classification":"not_evaluated_capture_integrity_is_not_demand","missing_capture_interpretation":"unknown_not_negative_demand"}
    return {**core,"minimal_plan_reduction_sha256":h(core)}

def test_reduced_plan_builds_exact_inert_authorization_request():
    out=build_exact_authorization_request(reduction(),request_time_utc="2026-08-20T10:30:00Z",ttl_seconds=300); req=out["exact_authorization_request"]
    assert out["state"]=="exact_single_get_ready_for_explicit_user_authorization" and req["scope"]["method"]=="GET" and req["scope"]["max_requests"]==1
    assert req["authorization_granted"] is False and req["authorization_nonce"] is None and req["authorization_token"] is None and req["expires_at_utc"]=="2026-08-20T10:35:00Z"

def test_scope_is_hash_bound_to_reduced_plan_and_preflight():
    r=reduction(); req=build_exact_authorization_request(r,request_time_utc="2026-08-20T10:30:00Z")["exact_authorization_request"]
    assert req["reduced_session_plan_sha256"]==h(r["reduced_session_plan"]) and req["reduced_transport_preflight_sha256"]==h(r["reduced_transport_preflight"]) and req["scope_sha256"]==h(req["scope"])

def test_no_capture_preserves_no_request_state():
    out=build_exact_authorization_request(reduction("no_op_no_capture_needed"),request_time_utc="2026-08-20T10:30:00Z"); assert out["state"]=="no_authorization_request_needed" and out["exact_authorization_request"] is None

def test_already_minimal_does_not_invent_embedded_plan():
    out=build_exact_authorization_request(reduction("already_minimal_exact_plan_no_reduction_needed"),request_time_utc="2026-08-20T10:30:00Z"); assert out["state"]=="already_minimal_but_exact_embedded_plan_absent" and out["exact_authorization_request"] is None

def test_blocked_stays_blocked():
    out=build_exact_authorization_request(reduction("blocked_no_exact_request_to_reduce"),request_time_utc="2026-08-20T10:30:00Z"); assert out["state"]=="authorization_request_blocked" and out["exact_authorization_request"] is None

def test_reduction_hash_tamper_fails_closed():
    r=reduction(); r["outcome_reason"]="tamper"
    with pytest.raises(ValueError,match="reduction_hash_mismatch"): build_exact_authorization_request(r,request_time_utc="2026-08-20T10:30:00Z")

def test_scope_tamper_fails_closed_even_if_outer_hash_recomputed():
    r=reduction(); r["reduced_transport_preflight"]["transport_envelopes"][0]["source_url"]="https://evil.example/x"; core=dict(r); core.pop("minimal_plan_reduction_sha256"); r["minimal_plan_reduction_sha256"]=h(core)
    with pytest.raises(ValueError,match="envelope_set_hash_mismatch|binding_invalid"): build_exact_authorization_request(r,request_time_utc="2026-08-20T10:30:00Z")

def test_ttl_and_time_fail_closed():
    with pytest.raises(ValueError,match="ttl_invalid"): build_exact_authorization_request(reduction(),request_time_utc="2026-08-20T10:30:00Z",ttl_seconds=30)
    with pytest.raises(ValueError,match="not_utc"): build_exact_authorization_request(reduction(),request_time_utc="2026-08-20T10:30:00")
