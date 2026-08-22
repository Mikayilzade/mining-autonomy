from copy import deepcopy
from hashlib import sha256
import json
from real_network_activation_request import build_real_network_activation_request


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def fixture():
    scope = {"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"abc123","credentials_allowed":False,"action_enabled":False}
    readiness_core = {
        "schema_version":1,"mode":"network_capable_adapter_contract_readiness_artifact","readiness_state":"adapter_contract_ready_for_separate_review_no_execution",
        "adapter_id":"https_json_v1","adapter_contract_sha256":"c"*64,"real_transport_authorization_consumption_sha256":"d"*64,
        "authorized_attempt_envelope_sha256":"e"*64,"real_transport_authorization_sha256":"f"*64,"pre_real_transport_review_sha256":"a"*64,
        "real_transport_decision_sha256":"b"*64,"exact_scope_sha256":h(scope),"exact_scope":scope,"request_contract":{},"enforced_transport_gates":{},
        "network_capable_contract_declared":True,"execution_entrypoint_present":False,"execution_entrypoint_reachable":False,"transport_callable_attached":False,
        "ready_for_real_network_execution":False,"separate_human_review_required":True,"credentials_allowed":False,"task_acceptance_enabled":False,
        "submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "readiness_artifact_is_execution_token":False,
    }
    readiness = {**readiness_core,"adapter_contract_readiness_sha256":h(readiness_core)}
    validation_core = {
        "schema_version":1,"mode":"deterministic_network_capable_adapter_contract_validator","validation_state":"adapter_contract_ready_for_separate_review_no_execution",
        "real_transport_authorization_consumption_sha256":readiness["real_transport_authorization_consumption_sha256"],"authorized_attempt_envelope_sha256":readiness["authorized_attempt_envelope_sha256"],
        "adapter_contract_sha256":readiness["adapter_contract_sha256"],"adapter_id":"https_json_v1","adapter_readiness_artifact":readiness,"blockers":[],
        "adapter_contract_validated":True,"execution_entrypoint_present":False,"execution_entrypoint_reachable":False,"transport_callable_attached":False,
        "transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,
        "submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"validation_record_is_execution_token":False,
    }
    validation={**validation_core,"network_adapter_contract_validation_sha256":h(validation_core)}
    iface={"interface_name":"execute_single_authorized_get","activation_state":"defined_but_unreachable","method":"GET","max_network_requests":1,
           "required_environment":"production","target_fingerprint":"abc123","credentials_allowed":False,"action_enabled":False,"task_acceptance_enabled":False,
           "submission_enabled":False,"value_movement_enabled":False}
    audit_core={
        "schema_version":1,"mode":"deterministic_network_adapter_implementation_binding_audit","audit_state":"implementation_bound_review_ready_no_execution",
        "network_adapter_contract_validation_sha256":validation["network_adapter_contract_validation_sha256"],"adapter_contract_readiness_sha256":readiness["adapter_contract_readiness_sha256"],
        "implementation_manifest_sha256":"1"*64,"implementation_source_sha256":"2"*64,"adapter_id":"https_json_v1","future_activation_interface":iface,"blockers":[],
        "implementation_binding_validated":True,"activation_reachable":False,"transport_callable_attached":False,"execution_entrypoint_reachable":False,
        "transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,
        "submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"audit_record_is_execution_token":False,
        "separate_real_network_activation_authorization_required":True,
    }
    audit={**audit_core,"implementation_binding_audit_sha256":h(audit_core)}
    return audit, validation


def build(a=None,v=None,**kw):
    aa,vv=fixture()
    return build_real_network_activation_request(a or aa,v or vv,requested_at=kw.pop("requested_at","2026-08-22T00:50:00Z"),**kw)


def test_exact_request_is_short_lived_and_inert():
    r=build(); q=r["real_network_activation_request"]
    assert r["builder_state"]=="activation_request_ready_no_network" and not r["blockers"]
    assert q["request_state"]=="ready_for_explicit_human_real_network_activation_decision"
    assert q["ttl_seconds"]==300 and q["activation_authorized"] is False and q["adapter_invoked"] is False
    assert q["network_enabled"] is False and q["request_is_execution_token"] is False


def test_binds_i077_source_and_i076_i075_lineage():
    a,v=fixture(); r=build(a,v); q=r["real_network_activation_request"]
    assert q["implementation_binding_audit_sha256"]==a["implementation_binding_audit_sha256"]
    assert q["implementation_source_sha256"]==a["implementation_source_sha256"]
    assert q["authorization_lineage"]["real_transport_authorization_consumption_sha256"]==v["adapter_readiness_artifact"]["real_transport_authorization_consumption_sha256"]
    assert q["authorization_lineage"]["authorized_attempt_envelope_sha256"]==v["adapter_readiness_artifact"]["authorized_attempt_envelope_sha256"]


def test_i077_tamper_rejected():
    a,v=fixture(); a["adapter_id"]="evil"
    r=build(a,v); assert r["builder_state"]=="activation_request_rejected" and "i077_audit_hash_invalid" in r["blockers"]


def test_rehashed_i077_scope_interface_widening_rejected():
    a,v=fixture(); a["future_activation_interface"]["max_network_requests"]=2
    core=dict(a); core.pop("implementation_binding_audit_sha256"); a["implementation_binding_audit_sha256"]=h(core)
    r=build(a,v); assert "i077_future_activation_interface_not_exact" in r["blockers"]


def test_i076_validation_tamper_rejected():
    a,v=fixture(); v["adapter_id"]="other"
    r=build(a,v); assert "i076_validation_hash_invalid" in r["blockers"]


def test_rehashed_scope_widening_rejected():
    a,v=fixture(); rd=v["adapter_readiness_artifact"]; rd["exact_scope"]["credentials_allowed"]=True
    rc=dict(rd); rc.pop("adapter_contract_readiness_sha256"); rd["adapter_contract_readiness_sha256"]=h(rc)
    vc=dict(v); vc.pop("network_adapter_contract_validation_sha256"); v["network_adapter_contract_validation_sha256"]=h(vc)
    a["network_adapter_contract_validation_sha256"]=v["network_adapter_contract_validation_sha256"]
    a["adapter_contract_readiness_sha256"]=rd["adapter_contract_readiness_sha256"]
    ac=dict(a); ac.pop("implementation_binding_audit_sha256"); a["implementation_binding_audit_sha256"]=h(ac)
    r=build(a,v); assert "scope_not_exact_single_anonymous_production_get" in r["blockers"]


def test_missing_i075_lineage_rejected():
    a,v=fixture(); rd=v["adapter_readiness_artifact"]; rd["real_transport_authorization_consumption_sha256"]=None
    rc=dict(rd); rc.pop("adapter_contract_readiness_sha256"); rd["adapter_contract_readiness_sha256"]=h(rc)
    vc=dict(v); vc.pop("network_adapter_contract_validation_sha256"); v["network_adapter_contract_validation_sha256"]=h(vc)
    a["network_adapter_contract_validation_sha256"]=v["network_adapter_contract_validation_sha256"]; a["adapter_contract_readiness_sha256"]=rd["adapter_contract_readiness_sha256"]
    ac=dict(a); ac.pop("implementation_binding_audit_sha256"); a["implementation_binding_audit_sha256"]=h(ac)
    r=build(a,v); assert "missing_lineage_real_transport_authorization_consumption_sha256" in r["blockers"]


def test_ttl_bounds_fail_closed():
    assert "ttl_out_of_range" in build(ttl_seconds=59)["blockers"]
    assert "ttl_out_of_range" in build(ttl_seconds=901)["blockers"]


def test_non_utc_time_rejected():
    r=build(requested_at="2026-08-22T04:50:00+04:00")
    assert "requested_at_invalid_or_not_utc" in r["blockers"] and r["real_network_activation_request"] is None


def test_hash_tamper_on_finished_request_detectable():
    r=build(); q=deepcopy(r["real_network_activation_request"]); digest=q.pop("real_network_activation_request_sha256")
    assert h(q)==digest
    q["ttl_seconds"]=600
    assert h(q)!=digest
