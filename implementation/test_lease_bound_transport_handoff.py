from copy import deepcopy
from hashlib import sha256
import json
from lease_bound_transport_handoff import NetworkIncapableRecorder, build_lease_bound_transport_handoff

def h(v): return sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def fixture():
    lease_core={"lease_state":"single_use_observation_lease_ready","blockers":[],"expires_at_utc":"2026-08-21T19:10:00Z","lease_scope":{"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target-x","credentials_allowed":False,"action_enabled":False},"human_decision_verification_sha256":"v","human_decision_request_sha256":"r","exact_scope_sha256":"s"}
    lease={**lease_core,"observation_authorization_lease_sha256":h(lease_core)}
    receipt_core={"consumption_state":"lease_consumed","consumed_at_utc":"2026-08-21T19:05:00Z","observation_authorization_lease_sha256":lease["observation_authorization_lease_sha256"],"human_decision_verification_sha256":"v","human_decision_request_sha256":"r","exact_scope_sha256":"s","lease_consumed":True,"remaining_consumptions":0,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False}
    receipt={**receipt_core,"observation_lease_consumption_sha256":h(receipt_core)}
    return lease,receipt

def run(lease,receipt,at="2026-08-21T19:06:00Z",adapter=None): return build_lease_bound_transport_handoff(lease,receipt,handed_off_at_utc=at,adapter=adapter or NetworkIncapableRecorder())
def test_exact_consumed_receipt_builds_one_inert_envelope():
    l,r=fixture(); x=run(l,r); assert x["handoff_state"]=="inert_transport_handoff_recorded"; assert x["transport_envelope"]["method"]=="GET"; assert x["transport_envelope"]["request_count"]==1; assert x["network_calls_performed"] is False

def test_tampered_receipt_rejected():
    l,r=fixture(); r["remaining_consumptions"]=1; assert run(l,r)["handoff_state"]=="handoff_rejected"
def test_unbound_receipt_rejected_even_if_rehashed():
    l,r=fixture(); r["human_decision_request_sha256"]="other"; core=dict(r); core.pop("observation_lease_consumption_sha256"); r["observation_lease_consumption_sha256"]=h(core); assert "consumption_receipt_human_decision_request_sha256_binding_invalid" in run(l,r)["blockers"]
def test_expired_handoff_rejected():
    l,r=fixture(); assert "lease_expired_before_handoff" in run(l,r,"2026-08-21T19:10:00Z")["blockers"]
def test_handoff_before_consumption_rejected():
    l,r=fixture(); assert "handoff_before_consumption" in run(l,r,"2026-08-21T19:04:59Z")["blockers"]
def test_network_capable_adapter_rejected_before_submit():
    class Bad:
        network_capable=True
        def submit(self,envelope): raise AssertionError("must not run")
    l,r=fixture(); assert "adapter_must_be_explicitly_network_incapable" in run(l,r,adapter=Bad())["blockers"]
def test_widened_lease_scope_rejected_even_if_rehashed():
    l,r=fixture(); l["lease_scope"]["request_count"]=2; core=dict(l); core.pop("observation_authorization_lease_sha256"); l["observation_authorization_lease_sha256"]=h(core); r["observation_authorization_lease_sha256"]=l["observation_authorization_lease_sha256"]; rc=dict(r); rc.pop("observation_lease_consumption_sha256"); r["observation_lease_consumption_sha256"]=h(rc); assert "lease_scope_not_exact_anonymous_get" in run(l,r)["blockers"]
def test_adapter_result_must_prove_zero_network_calls():
    class Liar:
        network_capable=False
        def submit(self,envelope):
            core={"schema_version":1,"mode":"network_incapable_transport_result","envelope_sha256":h(dict(envelope)),"network_calls_performed":True,"response_body_present":False}; return {**core,"transport_result_sha256":h(core)}
    l,r=fixture(); assert "network_incapable_adapter_result_invalid" in run(l,r,adapter=Liar())["blockers"]
