from __future__ import annotations

import copy
import json
from hashlib import sha256

import pytest

from compliance_review_bridge import bridge_reproducible_compliance_to_human_review


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def proposal():
    scope = {
        "method": "GET", "required_environment": "production", "request_count": 1,
        "credentials_allowed": False, "action_enabled": False,
        "url": "https://example.test/public-feed",
    }
    gates = [
        "fresh_explicit_real_user_authorization", "transport_implementation_review",
        "dns_and_destination_policy", "redirect_policy", "response_resource_limits",
        "current_source_compliance", "durable_receipt_binding",
    ]
    p = {
        "schema_version": 1, "mode": "inert_real_transport_integration_proposal",
        "expires_at_utc": "2026-08-21T00:00:00Z", "exact_scope": scope,
        "exact_scope_sha256": h(scope),
        "required_gates": [{"gate": g, "required": True} for g in gates],
        "authorization_granted": False, "real_user_authorization_present": False,
        "transport_implementation_present": False, "transport_enabled": False,
        "network_capable": False, "network_calls_performed": False,
        "credentials_used": False, "action_enabled": False,
        "money_or_value_movement_enabled": False, "executable_callback_present": False,
        "proposal_is_authorization": False, "proposal_is_execution_token": False,
    }
    p["real_transport_proposal_sha256"] = h(p)
    return p


def evidence():
    e = {
        "platform": "synthetic", "source_url": "https://example.test/policy",
        "evidence_class": "first_party_docs", "checked_at_utc": "2026-08-20T18:00:00Z",
        "anonymous_read_only_observation_permitted": True,
        "credentials_required": False, "human_only_access_required": False,
    }
    e["evidence_sha256"] = h(e)
    return e


def replay(*, verified=True):
    r = {
        "schema_version": 1, "mode": "deterministic_offline_source_compliance_evidence_replay",
        "replayed_at_utc": "2026-08-20T18:10:00Z", "source_compliance_attestation_sha256": "a" * 64,
        "source_url": "https://example.test/policy", "source_content_sha256": "b" * 64 if verified else None,
        "provenance_class": "reproducible_captured_content" if verified else "manual_metadata_only",
        "replay_state": "reproducible_evidence_verified" if verified else "blocked_or_manual_only",
        "reproducible": verified,
        "blockers": [] if verified else ["source_compliance_evidence_not_reproducibly_captured"],
        "i045_evidence": evidence() if verified else None,
        "network_calls_performed": False, "transport_enabled": False, "authorization_granted": False,
    }
    r["source_compliance_replay_sha256"] = h(r)
    return r


def test_verified_replay_can_reach_human_decision_ready():
    out = bridge_reproducible_compliance_to_human_review(
        proposal(), replay(), reviewed_at_utc="2026-08-20T18:20:00Z"
    )
    assert out["review_state"] == "ready_for_human_decision"
    assert out["reproducible_evidence_verified"] is True
    assert out["human_decision_requested"] is True
    assert out["authorization_granted"] is False
    assert out["transport_enabled"] is False


def test_manual_only_replay_cannot_reach_ready():
    out = bridge_reproducible_compliance_to_human_review(
        proposal(), replay(verified=False), reviewed_at_utc="2026-08-20T18:20:00Z"
    )
    assert out["review_state"] == "blocked_by_missing_evidence"
    assert out["human_decision_requested"] is False


def test_replay_outer_tamper_rejected():
    r = replay(); r["reproducible"] = False
    with pytest.raises(ValueError, match="replay_hash_mismatch"):
        bridge_reproducible_compliance_to_human_review(proposal(), r, reviewed_at_utc="2026-08-20T18:20:00Z")


def test_rehashed_manual_replay_with_embedded_evidence_still_blocked():
    r = replay(verified=False); r["i045_evidence"] = evidence(); r["source_compliance_replay_sha256"] = h({k:v for k,v in r.items() if k != "source_compliance_replay_sha256"})
    out = bridge_reproducible_compliance_to_human_review(proposal(), r, reviewed_at_utc="2026-08-20T18:20:00Z")
    assert out["review_state"] == "blocked_by_missing_evidence"


def test_non_inert_replay_rejected_even_if_rehashed():
    r = replay(); r["transport_enabled"] = True; r["source_compliance_replay_sha256"] = h({k:v for k,v in r.items() if k != "source_compliance_replay_sha256"})
    with pytest.raises(ValueError, match="replay_not_inert"):
        bridge_reproducible_compliance_to_human_review(proposal(), r, reviewed_at_utc="2026-08-20T18:20:00Z")


def test_proposal_scope_tamper_rejected():
    p = proposal(); p["exact_scope"]["request_count"] = 2; p["real_transport_proposal_sha256"] = h({k:v for k,v in p.items() if k != "real_transport_proposal_sha256"})
    with pytest.raises(ValueError):
        bridge_reproducible_compliance_to_human_review(p, replay(), reviewed_at_utc="2026-08-20T18:20:00Z")


def test_bridge_hash_is_deterministic():
    a = bridge_reproducible_compliance_to_human_review(proposal(), replay(), reviewed_at_utc="2026-08-20T18:20:00Z")
    b = bridge_reproducible_compliance_to_human_review(proposal(), replay(), reviewed_at_utc="2026-08-20T18:20:00Z")
    assert a["compliance_review_bridge_sha256"] == b["compliance_review_bridge_sha256"]


def test_bridge_never_promotes_authorization_or_transport():
    out = bridge_reproducible_compliance_to_human_review(proposal(), replay(), reviewed_at_utc="2026-08-20T18:20:00Z")
    for key in ("authorization_granted", "real_user_authorization_present", "transport_enabled", "network_capable", "network_calls_performed", "credentials_used", "action_enabled", "money_or_value_movement_enabled", "bridge_is_authorization", "bridge_is_execution_token"):
        assert out[key] is False
