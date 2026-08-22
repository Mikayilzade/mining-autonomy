from hashlib import sha256
import json
from exact_real_read_only_invocation_request import build_exact_real_read_only_invocation_request


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def fixture():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"abc","credentials_allowed":False,"action_enabled":False}
    scope_hash=h(scope)
    envelope_core={
        "schema_version":1,"mode":"single_attempt_real_network_activation_envelope","envelope_state":"one_attempt_bound_no_network",
        "created_at":"2026-08-22T01:03:00Z","real_network_activation_authorization_sha256":"authhash",
        "real_network_activation_request_sha256":"reqhash","implementation_binding_audit_sha256":"a",
        "implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c",
        "adapter_contract_readiness_sha256":"d","adapter_id":"future_https_json","exact_scope_sha256":scope_hash,
        "exact_scope":scope,"authorization_lineage":{"real_transport_authorization_sha256":"x"},
        "max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,
        "task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,
        "transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "adapter_invoked":False,"envelope_is_execution_result":False
    }
    envelope={**envelope_core,"real_network_activation_envelope_sha256":h(envelope_core)}
    c_receipt_core={
        "schema_version":1,"mode":"single_use_real_network_activation_consumption_receipt","consumption_state":"consumed_once_no_network",
        "consumed_at":"2026-08-22T01:03:00Z","real_network_activation_authorization_sha256":"authhash",
        "real_network_activation_request_sha256":"reqhash","real_network_activation_envelope_sha256":envelope["real_network_activation_envelope_sha256"],
        "adapter_id":"future_https_json","exact_scope_sha256":scope_hash,"authorization_consumed":True,
        "network_enabled":False,"network_calls_performed":False,"value_movement_enabled":False,"receipt_is_execution_token":False
    }
    c_receipt={**c_receipt_core,"real_network_activation_consumption_receipt_sha256":h(c_receipt_core)}
    p_core={
        "schema_version":1,"mode":"deterministic_real_network_activation_authorization_consumption_preflight",
        "consumption_state":"authorization_consumed_once_envelope_ready_no_network",
        "real_network_activation_authorization_sha256":"authhash","real_network_activation_request_sha256":"reqhash",
        "activation_envelope":envelope,"consumption_receipt":c_receipt,"blockers":[],
        "adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,
        "value_movement_enabled":False,"consumption_record_is_execution_token":False
    }
    preflight={**p_core,"real_network_activation_consumption_preflight_sha256":h(p_core)}
    result={
        "schema_version":1,"mode":"network_incapable_synthetic_adapter_result","adapter_id":"future_https_json",
        "invocation_count":1,"exact_scope":scope,"exact_scope_sha256":scope_hash,
        "real_network_activation_envelope_sha256":envelope["real_network_activation_envelope_sha256"],
        "network_capable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,
        "synthetic_only":True
    }
    i_receipt_core={
        "schema_version":1,"mode":"single_use_synthetic_adapter_invocation_receipt","invocation_state":"synthetic_adapter_invoked_once_no_network",
        "real_network_activation_envelope_sha256":envelope["real_network_activation_envelope_sha256"],
        "real_network_activation_consumption_receipt_sha256":c_receipt["real_network_activation_consumption_receipt_sha256"],
        "adapter_id":"future_https_json","exact_scope_sha256":scope_hash,"synthetic_adapter_result_sha256":h(result),
        "adapter_invoked_once":True,"real_network_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,
        "network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,
        "value_movement_enabled":False,"receipt_is_real_execution_token":False
    }
    i_receipt={**i_receipt_core,"synthetic_adapter_invocation_receipt_sha256":h(i_receipt_core)}
    g_core={
        "schema_version":1,"mode":"deterministic_activation_envelope_adapter_invocation_gate",
        "invocation_state":"synthetic_adapter_invoked_once_scope_preserved_no_network",
        "real_network_activation_consumption_preflight_sha256":preflight["real_network_activation_consumption_preflight_sha256"],
        "real_network_activation_envelope_sha256":envelope["real_network_activation_envelope_sha256"],
        "real_network_activation_consumption_receipt_sha256":c_receipt["real_network_activation_consumption_receipt_sha256"],
        "adapter_id":"future_https_json","exact_scope_sha256":scope_hash,
        "adapter_result":result,"invocation_receipt":i_receipt,"blockers":[],
        "real_network_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,
        "value_movement_enabled":False,"invocation_record_is_real_execution_token":False
    }
    gate={**g_core,"activation_envelope_invocation_gate_sha256":h(g_core)}
    return gate,preflight


def rehash_gate(g):
    g["activation_envelope_invocation_gate_sha256"]=h({k:v for k,v in g.items() if k!="activation_envelope_invocation_gate_sha256"})


def rehash_envelope_preflight(p):
    e=p["activation_envelope"]
    e["real_network_activation_envelope_sha256"]=h({k:v for k,v in e.items() if k!="real_network_activation_envelope_sha256"})
    c=p["consumption_receipt"]
    c["real_network_activation_envelope_sha256"]=e["real_network_activation_envelope_sha256"]
    c["real_network_activation_consumption_receipt_sha256"]=h({k:v for k,v in c.items() if k!="real_network_activation_consumption_receipt_sha256"})
    p["real_network_activation_consumption_preflight_sha256"]=h({k:v for k,v in p.items() if k!="real_network_activation_consumption_preflight_sha256"})


def test_clean_packet_ready_and_inert():
    g,p=fixture()
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert out["builder_state"]=="exact_real_read_only_invocation_request_ready_no_network"
    req=out["real_read_only_invocation_request"]
    assert req["request_state"]=="ready_for_fresh_explicit_human_real_read_only_invocation_decision"
    assert req["network_enabled"] is False and req["real_invocation_authorized"] is False
    assert req["request_is_execution_token"] is False


def test_i081_hash_tamper_rejected():
    g,p=fixture(); g["network_enabled"]=True
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "i081_gate_hash_invalid" in out["blockers"]


def test_i081_unsuccessful_state_rejected_even_if_rehashed():
    g,p=fixture(); g["invocation_state"]="synthetic_adapter_invocation_rejected"; rehash_gate(g)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "i081_gate_not_successful" in out["blockers"]


def test_tampered_invocation_receipt_rejected():
    g,p=fixture(); g["invocation_receipt"]["adapter_id"]="other"; rehash_gate(g)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "i081_invocation_receipt_hash_invalid" in out["blockers"]


def test_i080_scope_widening_rejected_even_if_rehashed():
    g,p=fixture(); p["activation_envelope"]["exact_scope"]["request_count"]=2; rehash_envelope_preflight(p)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "exact_scope_not_one_anonymous_production_get" in out["blockers"]


def test_adapter_binding_substitution_rejected():
    g,p=fixture(); g["adapter_id"]="other"; rehash_gate(g)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "invocation_lineage_adapter_id_binding_invalid" in out["blockers"]


def test_source_digest_and_lineage_required():
    g,p=fixture(); p["activation_envelope"]["implementation_source_sha256"]="short"; rehash_envelope_preflight(p)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "implementation_source_digest_invalid" in out["blockers"]


def test_scope_hash_must_match_scope():
    g,p=fixture(); p["activation_envelope"]["exact_scope_sha256"]="wrong"; rehash_envelope_preflight(p)
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z")
    assert "exact_scope_hash_invalid" in out["blockers"]


def test_ttl_and_utc_validation_fail_closed():
    g,p=fixture()
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00+04:00",ttl_seconds=30)
    assert "requested_at_invalid_or_not_utc" in out["blockers"]
    assert "ttl_out_of_range" in out["blockers"]
    assert out["real_read_only_invocation_request"] is None


def test_request_binds_upstream_hashes_and_requires_fresh_decision():
    g,p=fixture()
    out=build_exact_real_read_only_invocation_request(g,p,requested_at="2026-08-22T04:50:00Z",ttl_seconds=120)
    req=out["real_read_only_invocation_request"]
    assert req["activation_envelope_invocation_gate_sha256"]==g["activation_envelope_invocation_gate_sha256"]
    assert req["real_network_activation_consumption_preflight_sha256"]==p["real_network_activation_consumption_preflight_sha256"]
    assert req["real_network_activation_envelope_sha256"]==p["activation_envelope"]["real_network_activation_envelope_sha256"]
    assert req["explicit_human_decision_required"] is True
    assert req["remaining_prerequisites"]["network_capable_adapter_still_unreachable"] is True
