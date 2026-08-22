from copy import deepcopy
from hashlib import sha256
import json

from exact_real_read_only_invocation_decision import verify_exact_real_read_only_invocation_decision
from exact_real_read_only_invocation_consumption import consume_exact_real_read_only_invocation_authorization


def h(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def request():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target-abc","credentials_allowed":False,"action_enabled":False}
    source={"implementation_binding_audit_sha256":"a","implementation_source_sha256":"b"*64,"network_adapter_contract_validation_sha256":"c","adapter_contract_readiness_sha256":"d","real_network_activation_authorization_sha256":"e","real_network_activation_request_sha256":"f"}
    core={"schema_version":1,"mode":"exact_real_read_only_invocation_human_review_request","request_state":"ready_for_fresh_explicit_human_real_read_only_invocation_decision","requested_at":"2026-08-22T05:00:00Z","expires_at":"2026-08-22T05:05:00Z","ttl_seconds":300,"activation_envelope_invocation_gate_sha256":"g","synthetic_adapter_invocation_receipt_sha256":"h","real_network_activation_consumption_preflight_sha256":"i","real_network_activation_envelope_sha256":"j","adapter_id":"future_https_json","exact_scope_sha256":h(scope),"exact_scope":scope,"source_lineage":source,"remaining_prerequisites":{},"human_summary":{},"explicit_human_decision_required":True,"real_invocation_authorized":False,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"request_is_execution_token":False}
    return {**core,"exact_real_read_only_invocation_request_sha256":h(core)}


def decision(req, value="authorize"):
    fields=("activation_envelope_invocation_gate_sha256","synthetic_adapter_invocation_receipt_sha256","real_network_activation_consumption_preflight_sha256","real_network_activation_envelope_sha256","adapter_id","exact_scope_sha256")
    core={"schema_version":1,"mode":"explicit_exact_real_read_only_invocation_human_decision","decision_id":"decision-1","decision":value,"decided_at":"2026-08-22T05:01:00Z","single_use":True,"exact_real_read_only_invocation_request_sha256":req["exact_real_read_only_invocation_request_sha256"],**{k:req[k] for k in fields},"exact_scope":deepcopy(req["exact_scope"]),"source_lineage":deepcopy(req["source_lineage"]),"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False}
    return {**core,"exact_real_read_only_invocation_decision_sha256":h(core)}


def chain():
    req=request(); dec=decision(req)
    verified=verify_exact_real_read_only_invocation_decision(req,dec,verified_at="2026-08-22T05:02:00Z",authorization_ttl_seconds=120)
    assert verified["verification_state"]=="real_read_only_invocation_authorization_issued_not_consumed"
    return req,dec,verified["real_read_only_invocation_authorization"]


def rehash(obj, field):
    obj[field]=h({k:v for k,v in obj.items() if k!=field})


def test_clean_consumption_emits_inert_one_attempt_envelope_and_receipt():
    req,dec,auth=chain(); out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert out["consumption_state"]=="authorization_consumed_once_envelope_ready_no_network"
    env=out["real_read_only_invocation_envelope"]; receipt=out["consumption_receipt"]
    assert env["max_adapter_invocations"]==1 and env["max_network_requests"]==1
    assert env["network_capable_adapter_reachable"] is False and env["network_enabled"] is False
    assert receipt["authorization_consumed"] is True and receipt["receipt_is_execution_token"] is False
    assert out["network_calls_performed"] is False and out["value_movement_enabled"] is False


def test_request_hash_tamper_rejected():
    req,dec,auth=chain(); req["adapter_id"]="other"
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_request_hash_invalid" in out["blockers"]


def test_request_scope_widening_rejected_even_if_rehashed():
    req,dec,auth=chain(); req["exact_scope"]["request_count"]=2; req["exact_scope_sha256"]=h(req["exact_scope"]); rehash(req,"exact_real_read_only_invocation_request_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_request_scope_not_exact" in out["blockers"]


def test_decision_hash_tamper_rejected():
    req,dec,auth=chain(); dec["decision_id"]="tampered"
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_decision_hash_invalid" in out["blockers"]


def test_deny_decision_rejected_even_if_rehashed():
    req,dec,auth=chain(); dec["decision"]="deny"; rehash(dec,"exact_real_read_only_invocation_decision_sha256"); auth["exact_real_read_only_invocation_decision_sha256"]=dec["exact_real_read_only_invocation_decision_sha256"]; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_decision_not_authorize" in out["blockers"]


def test_authorization_hash_tamper_rejected():
    req,dec,auth=chain(); auth["adapter_id"]="other"
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_hash_invalid" in out["blockers"]


def test_authorization_scope_widening_rejected_even_if_rehashed():
    req,dec,auth=chain(); auth["exact_scope"]["request_count"]=2; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_scope_not_exact" in out["blockers"]


def test_authorization_network_widening_rejected_even_if_rehashed():
    req,dec,auth=chain(); auth["network_enabled"]=True; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_network_enabled_widened" in out["blockers"]


def test_authorization_decision_binding_substitution_rejected():
    req,dec,auth=chain(); auth["exact_real_read_only_invocation_decision_sha256"]="other"; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_decision_binding_invalid" in out["blockers"]


def test_expired_authorization_rejected():
    req,dec,auth=chain(); out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:04:01Z")
    assert "invocation_authorization_expired_or_not_yet_valid" in out["blockers"]


def test_consumed_flag_rejected_even_if_rehashed():
    req,dec,auth=chain(); auth["consumed"]=True; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_already_consumed" in out["blockers"]


def test_prior_valid_receipt_rejects_replay():
    req,dec,auth=chain(); first=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    second=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:40Z",prior_consumption_receipts=[first["consumption_receipt"]])
    assert "invocation_authorization_replay_detected" in second["blockers"]
    assert second["real_read_only_invocation_envelope"] is None


def test_tampered_prior_receipt_fails_closed():
    req,dec,auth=chain(); first=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    prior=deepcopy(first["consumption_receipt"]); prior["adapter_id"]="other"
    second=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:40Z",prior_consumption_receipts=[prior])
    assert "prior_consumption_receipt_hash_invalid" in second["blockers"]


def test_non_utc_consumed_at_fails_closed():
    req,dec,auth=chain(); out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T09:02:30+04:00")
    assert "consumed_at_invalid_or_not_utc" in out["blockers"] and out["real_read_only_invocation_envelope"] is None


def test_source_lineage_substitution_rejected():
    req,dec,auth=chain(); auth["source_lineage"]["implementation_source_sha256"]="x"*64; rehash(auth,"exact_real_read_only_invocation_authorization_sha256")
    out=consume_exact_real_read_only_invocation_authorization(req,dec,auth,consumed_at="2026-08-22T05:02:30Z")
    assert "invocation_authorization_source_lineage_binding_invalid" in out["blockers"]
