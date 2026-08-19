import json
import pytest

from evidence_archive import EvidenceArchive, append_capture_report, archive_record, parse_archive, production_scorecard, require_append_only, serialize_archive


def _report(*, suffix="1", platform="payanagent", demand="zero_open_observation", count=0, utilization="unproven", tx=None, paid=None):
    bundle = suffix * 64
    request = ("a" if suffix != "a" else "b") * 64
    delta = {
        "platform": platform,
        "source_url": f"https://example.test/{platform}/requests",
        "source_timestamp": "2026-08-19T12:00:00+00:00",
        "captured_at": "2026-08-19T12:01:00+00:00",
        "bundle_sha256": bundle,
        "request_snapshot_sha256": request,
        "demand_state": demand,
        "open_item_count": count,
        "paid_utilization_state": utilization,
        "paid_transaction_count": tx,
        "paid_value_usd": paid,
    }
    return {"schema_version": 1, "deltas": [delta], "registry": {"schema_version": 1, "bundle_hashes": [bundle], "dry_run_only": True, "action_enabled": False}, "dry_run_only": True, "action_enabled": False}


def test_testnet_zero_never_enters_production_scorecard():
    archive = append_capture_report(EvidenceArchive(), _report(), environment_by_bundle_sha256={"1" * 64: "testnet"})
    score = production_scorecard(archive)
    assert score["production_observation_count"] == 0
    assert score["excluded_testnet_observation_count"] == 1
    assert score["platforms"] == []


def test_unknown_environment_is_excluded_by_default():
    archive = append_capture_report(EvidenceArchive(), _report())
    score = production_scorecard(archive)
    assert archive.entries[0].environment == "unknown"
    assert score["excluded_unknown_observation_count"] == 1
    assert score["production_observation_count"] == 0


def test_production_observation_is_included_without_cross_snapshot_sum():
    report = _report(suffix="2", demand="positive_open_demand", count=2, utilization="positive_paid_utilization", tx=3, paid=7.5)
    archive = append_capture_report(EvidenceArchive(), report, environment_by_bundle_sha256={"2" * 64: "production"})
    score = production_scorecard(archive)
    assert score["production_observation_count"] == 1
    assert score["platforms"][0]["latest_paid_value_usd"] == 7.5
    assert score["cross_snapshot_paid_value_sum_usd"] is None
    assert score["cross_snapshot_extrapolation"] is False


def test_serialization_roundtrip_is_deterministic_and_hash_verified():
    archive = append_capture_report(EvidenceArchive(), _report(suffix="3"), environment_by_bundle_sha256={"3" * 64: "production"})
    first = serialize_archive(archive)
    loaded = parse_archive(first)
    assert first == serialize_archive(loaded)
    assert archive == loaded


def test_tampered_archive_fails_hash_validation():
    archive = append_capture_report(EvidenceArchive(), _report(suffix="4"))
    document = json.loads(serialize_archive(archive))
    document["entries"][0]["environment"] = "production"
    with pytest.raises(ValueError, match="archive_sha256_mismatch"):
        parse_archive(document)


def test_duplicate_bundle_hash_rejected():
    report = _report(suffix="5")
    archive = append_capture_report(EvidenceArchive(), report)
    with pytest.raises(ValueError, match="archive_duplicate_bundle_hash"):
        append_capture_report(archive, report)


def test_append_only_accepts_extension_and_rejects_rewrite():
    base = append_capture_report(EvidenceArchive(), _report(suffix="6"))
    extended = append_capture_report(base, _report(suffix="7"))
    require_append_only(base, extended)
    with pytest.raises(ValueError, match="archive_append_only_rewrite"):
        require_append_only(base, EvidenceArchive((extended.entries[1],)))


def test_invalid_environment_fails_closed():
    with pytest.raises(ValueError, match="archive_environment_invalid"):
        append_capture_report(EvidenceArchive(), _report(suffix="8"), environment_by_bundle_sha256={"8" * 64: "mainnet-ish"})
