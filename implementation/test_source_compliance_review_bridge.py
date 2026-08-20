from copy import deepcopy
from hashlib import sha256
import json
import pytest

from source_compliance_review_bridge import bridge_reproducible_compliance_to_human_review, REVIEW_MODE, REPLAY_MODE


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def evidence():
    core={"platform":"payanagent","source_url":"https://example.test/terms","evidence_class":"first_party_terms","checked_at_utc":"2026-08-20T18:00:00Z","anonymous_read_only_observation_permitted":True,"credentials_required":False,"human_only_access_required":False}
    return {**core,"evidence_sha256":h(core)}


def packet(ev=None, ready=True):
    scope={"method":"GET","url":"https://example.test/public","required_environment":"production","request_count":1,"credentials_allowed":False,"action_enabled":False}
    core={"schema_version":1,"mode":REVIEW_MODE,"review_state":"ready_for_human_decision" if ready else "blocked_by_missing_evidence","reviewed_at_utc":"2026-08-20T18:05:00Z","expires_at_utc":"2026-08-20T18:20:00Z","real_transport_proposal_sha256":"a"*64,"exact_scope_sha256":h(scope),"exact_scope":scope,"source_compliance_evidence":ev,"source_compliance_blockers":[] if ready else ["source_compliance_evidence_missing"],"gate_checklist":[],"human_decision_requested":ready,"authorization_granted":False,"real_user_authorization_present":False,"transport_enabled":False,"network_capable":False,"network_calls_performed":False,"credentials_used":False,"action_enabled":False,"money_or_value_movement_enabled":False,"review_packet_is_authorization":False,"review_packet_is_execution_token":False}
    return {**core,"human_review_packet_sha256":h(core)}


def replay(ev=None, verified=True, provenance="reproducible_captured_content"):
    core={"schema_version":1,"mode":REPLAY_MODE,"replayed_at_utc":"2026-08-20T18:06:00Z","source_compliance_attestation_sha256":"b"*64,"source_url":"https://example.test/terms","source_content_sha256":"c"*64 if provenance=="reproducible_captured_content" else None,"provenance_class":provenance,"replay_state":"reproducible_evidence_verified" if verified else "blocked_or_manual_only","reproducible":verified,"blockers":[] if verified else ["source_compliance_evidence_not_reproducibly_captured"],"i045_evidence":ev if verified else None,"network_calls_performed":False,"transport_enabled":False,"authorization_granted":False}
    return {**core,"source_compliance_replay_sha256":h(core)}


def test_verified_reproducible_evidence_preserves_ready_state():
    ev=evidence(); out=bridge_reproducible_compliance_to_human_review(packet(ev),replay(ev),bridged_at_utc="2026-08-20T18:07:00Z")
    assert out["bridge_state"]=="ready_for_human_decision" and out["human_decision_requested"] is True
    assert out["authorization_granted"] is False and out["transport_enabled"] is False


def test_manual_only_cannot_reach_ready_state():
    ev=evidence(); out=bridge_reproducible_compliance_to_human_review(packet(ev),replay(None,False,"manual_metadata_only"),bridged_at_utc="2026-08-20T18:07:00Z")
    assert out["bridge_state"].startswith("blocked") and "reproducible_source_compliance_not_verified" in out["blockers"]
    assert out["manual_metadata_sufficient"] is False


def test_evidence_binding_mismatch_blocks():
    ev=evidence(); other=deepcopy(ev); other["platform"]="other"; core=dict(other); core.pop("evidence_sha256"); other["evidence_sha256"]=h(core)
    out=bridge_reproducible_compliance_to_human_review(packet(ev),replay(other),bridged_at_utc="2026-08-20T18:07:00Z")
    assert "replay_evidence_not_bound_to_i045_packet" in out["blockers"]


def test_nonready_i045_packet_stays_blocked_even_with_verified_replay():
    ev=evidence(); out=bridge_reproducible_compliance_to_human_review(packet(ev,False),replay(ev),bridged_at_utc="2026-08-20T18:07:00Z")
    assert "i045_review_not_ready" in out["blockers"]


def test_scope_tamper_rejected():
    ev=evidence(); p=packet(ev); p["exact_scope"]["request_count"]=2; core=dict(p); core.pop("human_review_packet_sha256"); p["human_review_packet_sha256"]=h(core)
    with pytest.raises(ValueError,match="review_packet_scope_hash_mismatch"):
        bridge_reproducible_compliance_to_human_review(p,replay(ev),bridged_at_utc="2026-08-20T18:07:00Z")


def test_replay_hash_tamper_rejected():
    ev=evidence(); r=replay(ev); r["source_url"]="https://evil.test/terms"
    with pytest.raises(ValueError,match="source_compliance_replay_hash_mismatch"):
        bridge_reproducible_compliance_to_human_review(packet(ev),r,bridged_at_utc="2026-08-20T18:07:00Z")


def test_expired_packet_blocks_without_authorization():
    ev=evidence(); out=bridge_reproducible_compliance_to_human_review(packet(ev),replay(ev),bridged_at_utc="2026-08-20T18:20:00Z")
    assert "review_packet_expired" in out["blockers"] and out["authorization_granted"] is False


def test_bridge_time_cannot_precede_inputs():
    ev=evidence()
    with pytest.raises(ValueError,match="bridge_time_precedes_inputs"):
        bridge_reproducible_compliance_to_human_review(packet(ev),replay(ev),bridged_at_utc="2026-08-20T18:04:00Z")
