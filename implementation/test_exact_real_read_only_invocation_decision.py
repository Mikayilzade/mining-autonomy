from copy import deepcopy
from hashlib import sha256
import json

from exact_real_read_only_invocation_decision import (
    verify_exact_real_read_only_invocation_decision,
)


def h(value):
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def request():
    scope = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": "target-abc",
        "credentials_allowed": False,
        "action_enabled": False,
    }
    source_lineage = {
        "implementation_binding_audit_sha256": "a",
        "implementation_source_sha256": "b" * 64,
        "network_adapter_contract_validation_sha256": "c",
        "adapter_contract_readiness_sha256": "d",
        "real_network_activation_authorization_sha256": "e",
        "real_network_activation_request_sha256": "f",
    }
    core = {
        "schema_version": 1,
        "mode": "exact_real_read_only_invocation_human_review_request",
        "request_state": "ready_for_fresh_explicit_human_real_read_only_invocation_decision",
        "requested_at": "2026-08-22T05:00:00Z",
        "expires_at": "2026-08-22T05:05:00Z",
        "ttl_seconds": 300,
        "activation_envelope_invocation_gate_sha256": "g",
        "synthetic_adapter_invocation_receipt_sha256": "h",
        "real_network_activation_consumption_preflight_sha256": "i",
        "real_network_activation_envelope_sha256": "j",
        "adapter_id": "future_https_json",
        "exact_scope_sha256": h(scope),
        "exact_scope": scope,
        "source_lineage": source_lineage,
        "remaining_prerequisites": {
            "fresh_explicit_human_decision_bound_to_request_hash": True,
            "network_capable_adapter_still_unreachable": True,
            "dns_private_address_pinning_rebinding_gate_required": True,
            "zero_redirect_required": True,
            "bounded_json_only_response_required": True,
            "fresh_first_party_anonymous_read_only_policy_evidence_required": True,
        },
        "human_summary": {},
        "explicit_human_decision_required": True,
        "real_invocation_authorized": False,
        "network_capable_adapter_reachable": False,
        "adapter_invoked": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "request_is_execution_token": False,
    }
    return {**core, "exact_real_read_only_invocation_request_sha256": h(core)}


def decision(req, value="authorize", decided_at="2026-08-22T05:01:00Z"):
    core = {
        "schema_version": 1,
        "mode": "explicit_exact_real_read_only_invocation_human_decision",
        "decision_id": "decision-1",
        "decision": value,
        "decided_at": decided_at,
        "single_use": True,
        "exact_real_read_only_invocation_request_sha256": req[
            "exact_real_read_only_invocation_request_sha256"
        ],
        **{
            key: req[key]
            for key in (
                "activation_envelope_invocation_gate_sha256",
                "synthetic_adapter_invocation_receipt_sha256",
                "real_network_activation_consumption_preflight_sha256",
                "real_network_activation_envelope_sha256",
                "adapter_id",
                "exact_scope_sha256",
            )
        },
        "exact_scope": deepcopy(req["exact_scope"]),
        "source_lineage": deepcopy(req["source_lineage"]),
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }
    return {
        **core,
        "exact_real_read_only_invocation_decision_sha256": h(core),
    }


def rehash_decision(value):
    value["exact_real_read_only_invocation_decision_sha256"] = h(
        {
            key: item
            for key, item in value.items()
            if key != "exact_real_read_only_invocation_decision_sha256"
        }
    )


def rehash_request(value):
    value["exact_real_read_only_invocation_request_sha256"] = h(
        {
            key: item
            for key, item in value.items()
            if key != "exact_real_read_only_invocation_request_sha256"
        }
    )


def test_authorize_emits_inert_single_use_record():
    req = request()
    out = verify_exact_real_read_only_invocation_decision(
        req, decision(req), verified_at="2026-08-22T05:02:00Z"
    )
    assert out["verification_state"] == "real_read_only_invocation_authorization_issued_not_consumed"
    auth = out["real_read_only_invocation_authorization"]
    assert auth["single_use"] is True and auth["consumed"] is False
    assert auth["max_network_requests"] == 1
    assert auth["real_read_only_invocation_authorized"] is True
    assert auth["network_capable_adapter_reachable"] is False
    assert auth["network_enabled"] is False
    assert auth["authorization_is_payment_or_task_permission"] is False
    assert out["network_enabled"] is False and out["adapter_invoked"] is False


def test_deny_emits_no_authorization():
    req = request()
    out = verify_exact_real_read_only_invocation_decision(
        req, decision(req, "deny"), verified_at="2026-08-22T05:02:00Z"
    )
    assert out["verification_state"] == "denied_no_real_read_only_invocation_authorization"
    assert out["real_read_only_invocation_authorization"] is None


def test_request_hash_tamper_rejected():
    req = request()
    dec = decision(req)
    req["adapter_id"] = "other"
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "invocation_request_hash_invalid" in out["blockers"]


def test_scope_widening_rejected_even_if_request_rehashed():
    req = request()
    req["exact_scope"]["request_count"] = 2
    req["exact_scope_sha256"] = h(req["exact_scope"])
    rehash_request(req)
    dec = decision(req)
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "scope_not_exact_single_anonymous_production_get" in out["blockers"]


def test_scope_hash_mismatch_rejected():
    req = request()
    req["exact_scope_sha256"] = "wrong"
    rehash_request(req)
    dec = decision(req)
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "exact_scope_hash_invalid" in out["blockers"]


def test_stale_request_rejected():
    req = request()
    out = verify_exact_real_read_only_invocation_decision(
        req, decision(req), verified_at="2026-08-22T05:06:00Z"
    )
    assert "invocation_request_stale_or_not_yet_valid" in out["blockers"]


def test_future_decision_rejected():
    req = request()
    dec = decision(req, decided_at="2026-08-22T05:03:00Z")
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "human_decision_from_future" in out["blockers"]


def test_wrong_request_binding_rejected():
    req = request()
    dec = decision(req)
    dec["exact_real_read_only_invocation_request_sha256"] = "wrong"
    rehash_decision(dec)
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "human_decision_request_binding_invalid" in out["blockers"]


def test_decision_scope_widening_rejected():
    req = request()
    dec = decision(req)
    dec["exact_scope"]["request_count"] = 2
    rehash_decision(dec)
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "human_decision_scope_not_exact" in out["blockers"]


def test_credentials_widening_rejected():
    req = request()
    dec = decision(req)
    dec["credentials_allowed"] = True
    rehash_decision(dec)
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "human_decision_credentials_allowed_widened" in out["blockers"]


def test_bad_decision_hash_rejected():
    req = request()
    dec = decision(req)
    dec["exact_real_read_only_invocation_decision_sha256"] = "bad"
    out = verify_exact_real_read_only_invocation_decision(
        req, dec, verified_at="2026-08-22T05:02:00Z"
    )
    assert "human_decision_hash_invalid" in out["blockers"]


def test_replayed_decision_hash_rejected():
    req = request()
    dec = decision(req)
    out = verify_exact_real_read_only_invocation_decision(
        req,
        dec,
        verified_at="2026-08-22T05:02:00Z",
        prior_decision_sha256s={dec["exact_real_read_only_invocation_decision_sha256"]},
    )
    assert "human_decision_replay_detected" in out["blockers"]


def test_authorization_expiry_is_capped_by_request_expiry():
    req = request()
    out = verify_exact_real_read_only_invocation_decision(
        req,
        decision(req),
        verified_at="2026-08-22T05:04:30Z",
        authorization_ttl_seconds=180,
    )
    auth = out["real_read_only_invocation_authorization"]
    assert auth["expires_at"] == "2026-08-22T05:05:00Z"


def test_ttl_and_utc_fail_closed():
    req = request()
    dec = decision(req)
    out = verify_exact_real_read_only_invocation_decision(
        req,
        dec,
        verified_at="2026-08-22T09:02:00+04:00",
        authorization_ttl_seconds=301,
    )
    assert "verified_at_invalid_or_not_utc" in out["blockers"]
    assert "authorization_ttl_out_of_range" in out["blockers"]
    assert out["real_read_only_invocation_authorization"] is None
