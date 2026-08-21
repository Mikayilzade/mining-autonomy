from copy import deepcopy
from pre_real_transport_review import build_pre_real_transport_review, _hash

def fixture(now="2026-08-21T19:40:00Z"):
    scope = {
        "method": "GET", "request_count": 1, "required_environment": "production",
        "target_fingerprint": "payanagent:public-task-feed:v1",
        "credentials_allowed": False, "action_enabled": False,
    }
    lease_core = {
        "schema_version": 1,
        "mode": "deterministic_single_use_observation_authorization_lease",
        "lease_state": "single_use_observation_lease_ready",
        "issued_at_utc": "2026-08-21T19:39:00Z",
        "expires_at_utc": "2026-08-21T19:42:00Z",
        "human_decision_verification_sha256": "v"*64,
        "human_decision_request_sha256": "r"*64,
        "market_side_readiness_sha256": "m"*64,
        "exact_scope_sha256": "s"*64,
        "current_resource_backend_id": "python_local",
        "lease_scope": scope,
        "max_consumptions": 1,
        "blockers": [],
        "authorization_verified": True,
        "lease_is_single_use": True,
        "transport_enabled": False, "network_enabled": False,
        "network_calls_performed": False, "credentials_allowed": False,
        "task_acceptance_enabled": False, "submission_enabled": False,
        "execution_enabled": False, "value_movement_enabled": False,
        "lease_is_execution_token": False,
    }
    lease = {**lease_core, "observation_authorization_lease_sha256": _hash(lease_core)}
    receipt_hash = "c"*64
    env_core = {
        "schema_version": 1, "mode": "immutable_anonymous_get_envelope",
        "method": "GET", "request_count": 1, "required_environment": "production",
        "target_fingerprint": scope["target_fingerprint"],
        "credentials_allowed": False, "action_enabled": False,
        "observation_authorization_lease_sha256": lease["observation_authorization_lease_sha256"],
        "observation_lease_consumption_sha256": receipt_hash,
        "human_decision_verification_sha256": lease["human_decision_verification_sha256"],
        "human_decision_request_sha256": lease["human_decision_request_sha256"],
        "exact_scope_sha256": lease["exact_scope_sha256"],
        "handed_off_at_utc": "2026-08-21T19:39:30Z",
        "network_enabled": False, "network_calls_allowed": 0,
    }
    env = {**env_core, "transport_envelope_sha256": _hash(env_core)}
    result_core = {
        "schema_version": 1, "mode": "network_incapable_transport_result",
        "adapter": "network_incapable_recorder", "envelope_sha256": _hash(env),
        "network_calls_performed": False, "response_body_present": False,
        "status_code": None,
    }
    result = {**result_core, "transport_result_sha256": _hash(result_core)}
    handoff_core = {
        "schema_version": 1, "mode": "deterministic_lease_bound_transport_handoff",
        "handoff_state": "inert_transport_handoff_recorded",
        "handed_off_at_utc": "2026-08-21T19:39:30Z",
        "observation_authorization_lease_sha256": lease["observation_authorization_lease_sha256"],
        "observation_lease_consumption_sha256": receipt_hash,
        "human_decision_verification_sha256": lease["human_decision_verification_sha256"],
        "human_decision_request_sha256": lease["human_decision_request_sha256"],
        "exact_scope_sha256": lease["exact_scope_sha256"],
        "transport_envelope": env, "adapter_result": result, "blockers": [],
        "transport_enabled": False, "network_enabled": False,
        "network_calls_performed": False, "credentials_used": False,
        "task_acceptance_enabled": False, "submission_enabled": False,
        "execution_enabled": False, "value_movement_enabled": False,
        "handoff_is_execution_token": False,
    }
    handoff = {**handoff_core, "lease_bound_transport_handoff_sha256": _hash(handoff_core)}
    market = {
        "state": "ready_for_observation_request", "hard_blockers": [],
        "checked_at_utc": "2026-08-21T19:38:00Z",
        "candidate": "payanagent", "evidence_class": "first_party_public_read_only",
    }
    resource = {
        "state": "ready", "hard_blockers": [],
        "checked_at_utc": "2026-08-21T19:38:30Z",
        "backend_id": "python_local", "calibration_state": "calibrated_reproducible",
    }
    return handoff, lease, market, resource, now

def rebuild(obj, hash_field):
    core=deepcopy(obj); core.pop(hash_field, None)
    core[hash_field]=_hash(core)
    return core

def test_exact_inert_handoff_can_become_human_review_ready_only():
    handoff, lease, market, resource, now = fixture()
    out=build_pre_real_transport_review(handoff, lease, market, resource, reviewed_at_utc=now)
    assert out["review_state"]=="ready_for_explicit_real_transport_decision"
    assert out["unresolved_blockers"]==[]
    assert out["exact_scope"]["method"]=="GET"
    assert out["authorization_granted"] is False
    assert out["network_enabled"] is False
    assert out["review_packet_is_execution_token"] is False
    assert out["pre_real_transport_review_sha256"]==_hash({k:v for k,v in out.items() if k!="pre_real_transport_review_sha256"})

def test_handoff_hash_tamper_fails_closed():
    h,l,m,r,n=fixture(); h["network_enabled"]=True
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert out["review_state"].startswith("blocked")
    assert "lease_bound_transport_handoff_hash_invalid" in out["unresolved_blockers"]

def test_lease_hash_tamper_fails_closed():
    h,l,m,r,n=fixture(); l["current_resource_backend_id"]="other"
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "observation_authorization_lease_hash_invalid" in out["unresolved_blockers"]

def test_rehashed_widened_envelope_still_rejected():
    h,l,m,r,n=fixture()
    env=deepcopy(h["transport_envelope"]); env["request_count"]=2
    h["transport_envelope"]=rebuild(env,"transport_envelope_sha256")
    res=deepcopy(h["adapter_result"]); res["envelope_sha256"]=_hash(h["transport_envelope"])
    h["adapter_result"]=rebuild(res,"transport_result_sha256")
    h=rebuild(h,"lease_bound_transport_handoff_sha256")
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "transport_envelope_not_exact_inert_get" in out["unresolved_blockers"]

def test_rehashed_adapter_network_claim_rejected():
    h,l,m,r,n=fixture()
    res=deepcopy(h["adapter_result"]); res["network_calls_performed"]=True
    h["adapter_result"]=rebuild(res,"transport_result_sha256")
    h=rebuild(h,"lease_bound_transport_handoff_sha256")
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "adapter_result_not_network_incapable" in out["unresolved_blockers"]

def test_stale_market_readiness_blocks_review():
    h,l,m,r,n=fixture(); m["checked_at_utc"]="2026-08-19T19:38:00Z"
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "market_readiness_stale" in out["unresolved_blockers"]

def test_uncalibrated_resource_blocks_review():
    h,l,m,r,n=fixture(); r["calibration_state"]="synthetic_reference"
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "resource_not_calibrated" in out["unresolved_blockers"]

def test_wrong_resource_backend_binding_blocks_review():
    h,l,m,r,n=fixture(); r["backend_id"]="strong_external_api"
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    assert "resource_backend_binding_invalid" in out["unresolved_blockers"]

def test_prior_offline_authorization_never_becomes_real_transport_authorization():
    h,l,m,r,n=fixture()
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc=n)
    rule=out["future_decision_binding_rule"]
    assert rule["must_match_exact_packet_hash"] is True
    assert rule["prior_synthetic_or_offline_authorization_is_not_reusable"] is True
    assert out["real_user_authorization_inferred"] is False
    assert "fresh_explicit_human_authorization_bound_to_this_review_packet_hash" in out["explicit_user_authorization_prerequisites"]

def test_review_after_lease_expiry_blocks():
    h,l,m,r,_=fixture()
    out=build_pre_real_transport_review(h,l,m,r,reviewed_at_utc="2026-08-21T19:43:00Z")
    assert "reviewed_lease_expired" in out["unresolved_blockers"]
