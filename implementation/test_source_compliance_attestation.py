from hashlib import sha256
import json
import pytest

from source_compliance_attestation import attest_source_compliance_evidence, replay_source_compliance_attestation


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def evidence(**changes):
    core = {
        "platform": "Fixture Market", "source_url": "https://fixture.example/terms",
        "evidence_class": "first_party_terms", "checked_at_utc": "2026-08-20T11:00:00Z",
        "anonymous_read_only_observation_permitted": True, "credentials_required": False,
        "human_only_access_required": False,
    }
    core.update(changes)
    return {**core, "evidence_sha256": h(core)}


def captured():
    return attest_source_compliance_evidence(
        evidence(), source_content="anonymous GET allowed", retrieved_at_utc="2026-08-20T11:01:00Z",
        attested_at_utc="2026-08-20T11:02:00Z"
    )


def test_captured_content_replays_as_reproducible_i045_evidence():
    a = captured()
    out = replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z")
    assert out["replay_state"] == "reproducible_evidence_verified"
    assert out["reproducible"] is True and out["i045_evidence"]["source_url"] == "https://fixture.example/terms"
    assert out["network_calls_performed"] is False and out["transport_enabled"] is False


def test_manual_metadata_is_distinguished_and_not_promoted_to_i045_ready_input():
    a = attest_source_compliance_evidence(evidence(), attested_at_utc="2026-08-20T11:02:00Z")
    out = replay_source_compliance_attestation(a, replayed_at_utc="2026-08-20T12:00:00Z")
    assert out["reproducible"] is False and out["i045_evidence"] is None
    assert "source_compliance_evidence_not_reproducibly_captured" in out["blockers"]


def test_captured_content_requires_exact_bytes_for_replay():
    a = captured()
    missing = replay_source_compliance_attestation(a, replayed_at_utc="2026-08-20T12:00:00Z")
    changed = replay_source_compliance_attestation(a, source_content="changed", replayed_at_utc="2026-08-20T12:00:00Z")
    assert "captured_source_content_required_for_replay" in missing["blockers"]
    assert "captured_source_content_digest_mismatch" in changed["blockers"]


def test_stale_or_non_permitted_policy_blocks_even_with_matching_capture():
    e = evidence(checked_at_utc="2026-08-01T11:00:00Z", anonymous_read_only_observation_permitted=False)
    a = attest_source_compliance_evidence(e, source_content="x", retrieved_at_utc="2026-08-20T11:01:00Z", attested_at_utc="2026-08-20T11:02:00Z")
    out = replay_source_compliance_attestation(a, source_content="x", replayed_at_utc="2026-08-20T12:00:00Z")
    assert "source_compliance_evidence_stale" in out["blockers"]
    assert "anonymous_read_only_observation_not_confirmed" in out["blockers"]


def test_attestation_hash_tamper_is_rejected():
    a = captured(); a["source_url"] = "https://evil.example/terms"
    with pytest.raises(ValueError, match="attestation_hash_mismatch"):
        replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z")


def test_rehashed_inner_evidence_tamper_still_breaks_binding():
    a = captured(); a["normalized_i045_evidence"]["platform"] = "Other"
    inner = dict(a["normalized_i045_evidence"]); inner.pop("evidence_sha256")
    a["normalized_i045_evidence"]["evidence_sha256"] = h(inner)
    core = dict(a); core.pop("source_compliance_attestation_sha256")
    a["source_compliance_attestation_sha256"] = h(core)
    with pytest.raises(ValueError, match="attestation_evidence_binding_mismatch"):
        replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z")


def test_capture_time_and_utc_fail_closed():
    with pytest.raises(ValueError, match="captured_content_requires_retrieved_time"):
        attest_source_compliance_evidence(evidence(), source_content="x", attested_at_utc="2026-08-20T11:02:00Z")
    with pytest.raises(ValueError, match="retrieved_after_attestation"):
        attest_source_compliance_evidence(evidence(), source_content="x", retrieved_at_utc="2026-08-20T11:03:00Z", attested_at_utc="2026-08-20T11:02:00Z")
    with pytest.raises(ValueError, match="timestamp_must_be_utc_z"):
        attest_source_compliance_evidence(evidence(), attested_at_utc="2026-08-20T11:02:00+00:00")


def test_replay_hash_is_deterministic_and_max_age_is_bounded():
    a = captured()
    one = replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z")
    two = replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z")
    assert one["source_compliance_replay_sha256"] == two["source_compliance_replay_sha256"]
    with pytest.raises(ValueError, match="source_evidence_max_age_invalid"):
        replay_source_compliance_attestation(a, source_content="anonymous GET allowed", replayed_at_utc="2026-08-20T12:00:00Z", max_age_hours=0)
