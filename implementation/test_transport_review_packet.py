from hashlib import sha256
import json
import socket
import pytest

from real_transport_proposal import build_real_transport_integration_proposal
from transport_review_packet import build_real_transport_human_review_packet


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def lease():
    core = {
        "schema_version": 1, "mode": "deterministic_single_use_read_only_authorization_lease",
        "consent_verification_sha256": "a"*64, "execution_authorization_sha256": "b"*64,
        "authorization_request_sha256": "c"*64, "scope_sha256": "d"*64, "decision_sha256": "e"*64,
        "issued_at_utc": "2026-08-20T12:01:00Z", "expires_at_utc": "2026-08-20T12:10:00Z",
        "max_requests": 1, "remaining_requests": 1, "method": "GET", "required_environment": "production",
        "credentials_allowed": False, "action_enabled": False, "transport_enabled": False,
        "network_calls_performed": False, "offline_consumption_only": True, "single_use": True,
        "synthetic_fixture_not_real_consent": True,
    }
    return {**core, "authorization_lease_sha256": h(core)}


def request(l):
    core = {
        "schema_version": 1, "mode": "dependency_injected_single_get_execution_request",
        "authorization_lease_sha256": l["authorization_lease_sha256"],
        "execution_authorization_sha256": l["execution_authorization_sha256"],
        "method": "GET", "required_environment": "production", "request_count": 1,
        "credentials_used": False, "action_enabled": False, "target_fingerprint": "fixture.example/api/tasks",
    }
    return {**core, "execution_request_sha256": h(core)}


def proposal():
    l = lease()
    return build_real_transport_integration_proposal(l, request(l), proposed_at_utc="2026-08-20T12:02:00Z")


def evidence(**changes):
    core = {
        "platform": "Fixture Market", "source_url": "https://fixture.example/terms",
        "evidence_class": "first_party_terms", "checked_at_utc": "2026-08-20T11:00:00Z",
        "anonymous_read_only_observation_permitted": True, "credentials_required": False,
        "human_only_access_required": False, "notes": "synthetic test evidence only",
    }
    core.update(changes)
    return {**core, "evidence_sha256": h(core)}


def test_current_first_party_evidence_makes_packet_ready_for_human_decision():
    out = build_real_transport_human_review_packet(proposal(), evidence(), reviewed_at_utc="2026-08-20T12:03:00Z")
    assert out["review_state"] == "ready_for_human_decision"
    assert out["human_decision_requested"] is True
    assert out["authorization_granted"] is False and out["transport_enabled"] is False and out["network_capable"] is False
    assert out["source_compliance_blockers"] == []
    core = dict(out); supplied = core.pop("human_review_packet_sha256")
    assert h(core) == supplied


def test_missing_evidence_blocks_human_decision():
    out = build_real_transport_human_review_packet(proposal(), None, reviewed_at_utc="2026-08-20T12:03:00Z")
    assert out["review_state"] == "blocked_by_missing_evidence"
    assert out["human_decision_requested"] is False
    assert "source_compliance_evidence_missing" in out["source_compliance_blockers"]


def test_stale_evidence_blocks():
    out = build_real_transport_human_review_packet(proposal(), evidence(checked_at_utc="2026-08-10T11:00:00Z"), reviewed_at_utc="2026-08-20T12:03:00Z")
    assert "source_compliance_evidence_stale" in out["source_compliance_blockers"]


def test_non_first_party_or_credentials_required_blocks():
    out = build_real_transport_human_review_packet(proposal(), evidence(evidence_class="community_report", credentials_required=True), reviewed_at_utc="2026-08-20T12:03:00Z")
    assert "source_compliance_evidence_class_not_first_party" in out["source_compliance_blockers"]
    assert "credentials_free_access_not_confirmed" in out["source_compliance_blockers"]


def test_tampered_proposal_rejected():
    p = proposal(); p["exact_scope"]["request_count"] = 2
    with pytest.raises(ValueError, match="proposal_hash_mismatch"):
        build_real_transport_human_review_packet(p, evidence(), reviewed_at_utc="2026-08-20T12:03:00Z")


def test_rehashed_widened_scope_rejected():
    p = proposal(); p["exact_scope"]["request_count"] = 2; p["exact_scope_sha256"] = h(p["exact_scope"])
    core = dict(p); core.pop("real_transport_proposal_sha256"); p["real_transport_proposal_sha256"] = h(core)
    with pytest.raises(ValueError, match="proposal_scope_invalid"):
        build_real_transport_human_review_packet(p, evidence(), reviewed_at_utc="2026-08-20T12:03:00Z")


def test_review_does_not_touch_network(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("network primitive must not be called")
    monkeypatch.setattr(socket, "socket", fail)
    monkeypatch.setattr(socket, "getaddrinfo", fail)
    out = build_real_transport_human_review_packet(proposal(), evidence(), reviewed_at_utc="2026-08-20T12:03:00Z")
    assert out["network_calls_performed"] is False


def test_expired_review_and_bad_max_age_fail_closed():
    with pytest.raises(ValueError, match="review_after_proposal_expiry"):
        build_real_transport_human_review_packet(proposal(), evidence(), reviewed_at_utc="2026-08-20T12:10:00Z")
    with pytest.raises(ValueError, match="source_evidence_max_age_invalid"):
        build_real_transport_human_review_packet(proposal(), evidence(), reviewed_at_utc="2026-08-20T12:03:00Z", max_source_evidence_age_hours=0)
