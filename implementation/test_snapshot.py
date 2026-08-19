from dataclasses import replace
from datetime import datetime, timezone
import pytest

from snapshot import (canonical_payload_hash, ingest_snapshot, verify_snapshot,
    validate_snapshot, records_from_snapshot, replay_task_snapshot)

CAPTURED="2026-08-19T04:00:00+00:00"
NOW=datetime(2026,8,19,4,30,tzinfo=timezone.utc)


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
    tampered=replace(s,payload={"calls":999})
    assert not verify_snapshot(tampered)
    with pytest.raises(ValueError,match="snapshot_hash_mismatch"):
        validate_snapshot(tampered,now=NOW)


def test_stale_snapshot_fails_closed_on_ingest_and_replay():
    with pytest.raises(ValueError,match="stale_snapshot"):
        ingest_snapshot(platform="payanagent",source_url="https://example.org/api/tasks",
            source_timestamp="2026-08-17T00:00:00Z",captured_at=CAPTURED,
            evidence_class="official_api",payload={})
    s=ingest_snapshot(platform="payanagent",source_url="https://example.org/api/tasks",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_api",payload={"items":[]})
    with pytest.raises(ValueError,match="stale_snapshot"):
        records_from_snapshot(s,now=datetime(2026,8,21,tzinfo=timezone.utc))


def test_non_https_and_unknown_evidence_fail_closed():
    with pytest.raises(ValueError,match="https_source_required"):
        ingest_snapshot(platform="x",source_url="http://example.org",source_timestamp="2026-08-19T03:30:00Z",
            captured_at=CAPTURED,evidence_class="official_api",payload={})
    with pytest.raises(ValueError,match="unsupported_evidence_class"):
        ingest_snapshot(platform="x",source_url="https://example.org",source_timestamp="2026-08-19T03:30:00Z",
            captured_at=CAPTURED,evidence_class="rumor",payload={})


def test_records_contract_fails_closed():
    s=ingest_snapshot(platform="payanagent",source_url="https://example.org/api/tasks",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_api",payload={"items":{"id":"x"}})
    with pytest.raises(ValueError,match="snapshot_records_must_be_list"):
        records_from_snapshot(s,now=NOW)


def test_verified_replay_overrides_untrusted_record_timestamp():
    class FakeAdapter:
        def adapt(self,record,observed_at=None):
            return {"id":record["id"],"observed_at":observed_at,"raw_observed_at":record.get("observed_at")}
    s=ingest_snapshot(platform="payanagent",source_url="https://payanagent.com/api/v1/discover",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_api",payload={"items":[{"id":"p1","observed_at":"1999-01-01T00:00:00Z"}]})
    rows=replay_task_snapshot(s,now=NOW,adapters={"payanagent":FakeAdapter()})
    assert rows[0]["observed_at"]==s.source_timestamp
    assert rows[0]["raw_observed_at"]=="1999-01-01T00:00:00Z"


def test_unknown_snapshot_platform_rejected():
    s=ingest_snapshot(platform="unknown",source_url="https://example.org/api/tasks",
        source_timestamp="2026-08-19T03:30:00Z",captured_at=CAPTURED,
        evidence_class="official_api",payload={"items":[]})
    with pytest.raises(ValueError,match="unknown_snapshot_platform"):
        replay_task_snapshot(s,now=NOW,adapters={})
