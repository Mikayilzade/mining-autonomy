from dataclasses import replace
import pytest

from snapshot import canonical_payload_hash, ingest_snapshot, verify_snapshot

CAPTURED="2026-08-19T04:00:00+00:00"


def test_snapshot_is_reproducible_and_verified():
    payload={"id":"x1","bounty":5,"skills":["extract"]}
    s=ingest_snapshot(platform="payanagent",source_url="https://example.org/api/tasks",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_api",payload=payload)
    assert s.payload_sha256==canonical_payload_hash(payload)
    assert verify_snapshot(s)


def test_tamper_is_detected():
    s=ingest_snapshot(platform="mcpize",source_url="https://example.org/catalog",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_page",payload={"calls":10})
    assert not verify_snapshot(replace(s,payload={"calls":999}))


def test_stale_snapshot_fails_closed():
    with pytest.raises(ValueError,match="stale_snapshot"):
        ingest_snapshot(platform="payanagent",source_url="https://example.org/api/tasks",
            source_timestamp="2026-08-17T00:00:00Z",captured_at=CAPTURED,
            evidence_class="official_api",payload={})


def test_non_https_and_unknown_evidence_fail_closed():
    with pytest.raises(ValueError,match="https_source_required"):
        ingest_snapshot(platform="x",source_url="http://example.org",source_timestamp="2026-08-19T03:30:00Z",
            captured_at=CAPTURED,evidence_class="official_api",payload={})
    with pytest.raises(ValueError,match="unsupported_evidence_class"):
        ingest_snapshot(platform="x",source_url="https://example.org",source_timestamp="2026-08-19T03:30:00Z",
            captured_at=CAPTURED,evidence_class="rumor",payload={})
