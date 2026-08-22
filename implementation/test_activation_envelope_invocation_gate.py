from hashlib import sha256
import json
from activation_envelope_invocation_gate import (
    SyntheticNetworkIncapableAdapter,
    invoke_activation_envelope_synthetic,
)


def h(v):
    return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def preflight():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"abc","credentials_allowed":False,"action_enabled":False}
    envelope_core={
        "schema_version":1,"mode":"single_attempt_real_network_activation_envelope","envelope_state":"one_attempt_bound_no_network",
        "created_at":"2026-08-22T01:03:00Z","real_network_activation_authorization_sha256":"authhash",
        "real_network_activation_request_sha256":"reqhash","implementation_binding_audit_sha256":"a",
        "implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c",
        "adapter_contract_readiness_sha256":"d","adapter_id":"future_https_json","exact_scope_sha256":"e",
        "exact_scope":scope,"authorization_lineage":{"real_transport_authorization_sha256":"x"},
        "max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,
        "task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,
        "transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "adapter_invoked":False,"envelope_is_execution_result":False
    }
    envelope={**envelope_core,"real_network_activation_envelope_sha256":h(envelope_core)}
    receipt_core={
        "schema_version":1,"mode":"single_use_real_network_activation_consumption_receipt",
        "consumption_state":"consumed_once_no_network","consumed_at":"2026-08-22T01:03:00Z",
        "real_network_activation_authorization_sha256":"authhash","real_network_activation_request_sha256":"reqhash",
        "real_network_activation_envelope_sha256":envelope["real_network_activation_envelope_sha256"],
        "adapter_id":"future_https_json","exact_scope_sha256":"e","authorization_consumed":True,
        "network_enabled":False,"network_calls_performed":False,"value_movement_enabled":False,
        "receipt_is_execution_token":False
    }
    receipt={**receipt_core,"real_network_activation_consumption_receipt_sha256":h(receipt_core)}
    core={
        "schema_version":1,"mode":"deterministic_real_network_activation_authorization_consumption_preflight",
        "consumption_state":"authorization_consumed_once_envelope_ready_no_network",
        "real_network_activation_authorization_sha256":"authhash","real_network_activation_request_sha256":"reqhash",
        "activation_envelope":envelope,"consumption_receipt":receipt,"blockers":[],
        "adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,
        "credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,
        "value_movement_enabled":False,"consumption_record_is_execution_token":False
    }
    return {**core,"real_network_activation_consumption_preflight_sha256":h(core)}


def rehash_preflight(p):
    p["real_network_activation_consumption_preflight_sha256"] = h({k:v for k,v in p.items() if k!="real_network_activation_consumption_preflight_sha256"})


def rehash_envelope_and_preflight(p):
    e=p["activation_envelope"]
    e["real_network_activation_envelope_sha256"] = h({k:v for k,v in e.items() if k!="real_network_activation_envelope_sha256"})
    p["consumption_receipt"]["real_network_activation_envelope_sha256"] = e["real_network_activation_envelope_sha256"]
    rec=p["consumption_receipt"]
    rec["real_network_activation_consumption_receipt_sha256"] = h({k:v for k,v in rec.items() if k!="real_network_activation_consumption_receipt_sha256"})
    rehash_preflight(p)


def test_clean_invocation_exercises_one_network_incapable_adapter_only():
    p=preflight(); adapter=SyntheticNetworkIncapableAdapter("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert out["invocation_state"]=="synthetic_adapter_invoked_once_scope_preserved_no_network"
    assert adapter.invocation_count==1
    assert out["adapter_result"]["network_calls_performed"] is False
    assert out["invocation_receipt"]["real_network_adapter_reachable"] is False


def test_preflight_hash_tamper_rejected_before_callback():
    p=preflight(); p["network_enabled"]=True; adapter=SyntheticNetworkIncapableAdapter("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "consumption_preflight_hash_invalid" in out["blockers"]
    assert adapter.invocation_count==0


def test_envelope_scope_widening_rejected_even_if_rehashed():
    p=preflight(); p["activation_envelope"]["exact_scope"]["request_count"]=2; rehash_envelope_and_preflight(p)
    adapter=SyntheticNetworkIncapableAdapter("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "activation_envelope_scope_not_exact" in out["blockers"]
    assert adapter.invocation_count==0


def test_receipt_envelope_binding_mismatch_rejected():
    p=preflight(); p["consumption_receipt"]["real_network_activation_envelope_sha256"]="wrong"
    rec=p["consumption_receipt"]; rec["real_network_activation_consumption_receipt_sha256"]=h({k:v for k,v in rec.items() if k!="real_network_activation_consumption_receipt_sha256"}); rehash_preflight(p)
    adapter=SyntheticNetworkIncapableAdapter("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "consumption_receipt_envelope_binding_invalid" in out["blockers"]
    assert adapter.invocation_count==0


def test_adapter_id_mismatch_rejected_before_callback():
    p=preflight(); adapter=SyntheticNetworkIncapableAdapter("other")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "adapter_id_binding_invalid" in out["blockers"]
    assert adapter.invocation_count==0


def test_network_capable_adapter_rejected_before_callback():
    class Bad(SyntheticNetworkIncapableAdapter):
        network_capable=True
    p=preflight(); adapter=Bad("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "network_capable_adapter_rejected" in out["blockers"]
    assert adapter.invocation_count==0


def test_adapter_result_scope_widening_fails_closed():
    class Widen(SyntheticNetworkIncapableAdapter):
        def invoke_synthetic(self,envelope):
            r=dict(super().invoke_synthetic(envelope)); r["exact_scope"]=dict(r["exact_scope"]); r["exact_scope"]["request_count"]=2; return r
    p=preflight(); adapter=Widen("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "synthetic_adapter_result_scope_widened" in out["blockers"]
    assert out["invocation_receipt"] is None


def test_adapter_claiming_network_activity_fails_closed():
    class Liar(SyntheticNetworkIncapableAdapter):
        def invoke_synthetic(self,envelope):
            r=dict(super().invoke_synthetic(envelope)); r["network_calls_performed"]=True; return r
    p=preflight(); adapter=Liar("future_https_json")
    out=invoke_activation_envelope_synthetic(p,adapter)
    assert "synthetic_adapter_result_network_calls_performed_must_be_false" in out["blockers"]
    assert out["invocation_receipt"] is None


def test_replay_receipt_rejected_before_second_callback():
    p=preflight(); a1=SyntheticNetworkIncapableAdapter("future_https_json")
    first=invoke_activation_envelope_synthetic(p,a1)
    a2=SyntheticNetworkIncapableAdapter("future_https_json")
    out=invoke_activation_envelope_synthetic(p,a2,prior_invocation_receipts=[first["invocation_receipt"]])
    assert "activation_envelope_replay_detected" in out["blockers"]
    assert a2.invocation_count==0


def test_malformed_prior_invocation_receipt_fails_closed():
    p=preflight(); adapter=SyntheticNetworkIncapableAdapter("future_https_json")
    prior={"mode":"single_use_synthetic_adapter_invocation_receipt","invocation_state":"synthetic_adapter_invoked_once_no_network","real_network_activation_envelope_sha256":p["activation_envelope"]["real_network_activation_envelope_sha256"],"synthetic_adapter_invocation_receipt_sha256":"bad"}
    out=invoke_activation_envelope_synthetic(p,adapter,prior_invocation_receipts=[prior])
    assert "prior_invocation_receipt_hash_invalid" in out["blockers"]
    assert adapter.invocation_count==0
