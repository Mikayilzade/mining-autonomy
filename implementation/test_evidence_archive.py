import copy
import json
import pytest

from evidence_archive import EvidenceArchive, append_capture_report, parse_archive, production_scorecard, require_append_only, serialize_archive
from observation_capture import run_verified_capture_batch
from sampling_receipt import TransportResult, bind_capture_result, seal_sampling_manifest


def _bundle(*, suffix="1", platform="payanagent", demand="zero_open_observation", count=0,
            utilization="unproven", tx=None, paid=None, environment="production"):
    source_url = f"https://example.test/{platform}/requests"
    source_timestamp = "2026-08-19T12:00:00+00:00"
    captured_at = "2026-08-19T12:01:00+00:00"
    evidence = "open_paid_request" if demand == "positive_open_demand" else "unknown"
    items = [{"id": f"item-{suffix}"} for _ in range(count)]
    util = None if utilization == "unproven" else {"transaction_count": tx, "total_value_usd": paid}
    bundle = {
        "platform": platform,
        "request_envelope": {"demand_evidence_class": evidence, "records_key": "items", "snapshot": {
            "platform": platform, "source_url": source_url, "source_timestamp": source_timestamp,
            "captured_at": captured_at, "payload_sha256": ("a" if suffix != "a" else "b") * 64,
            "payload": {"items": items}}},
        "utilization": util,
        "manifest": {"platform": platform, "dry_run_only": True, "action_enabled": False},
        "manifest_sha256": suffix * 64,
    }
    manifest = {"schema_version": 1, "generated_at": "2026-08-19T11:59:00+00:00",
        "mode": "inert_read_only_sampling_contract", "network_calls_performed": False,
        "action_enabled": False, "credentials_allowed": False, "scheduled_source_count": 1,
        "source_count": 1, "items": [{"platform": platform, "source_url": source_url,
            "method": "GET", "scheduled": True, "expected_evidence_classes": ["open_demand_snapshot"],
            "environment": environment, "credentials_allowed": False, "network_calls_performed": False,
            "action_enabled": False}]}
    envelope = seal_sampling_manifest(manifest)
    receipt = bind_capture_result(envelope, item_index=0,
        result=TransportResult(sanitized_bundle_sha256=bundle["manifest_sha256"],
            capture_started_at="2026-08-19T12:00:59+00:00", capture_finished_at=captured_at,
            captured_environment=environment, source_timestamp=source_timestamp),
        transport_name="fixture", transport_network_capable=False)
    return bundle, envelope, receipt


def _report(**kwargs):
    bundle, envelope, receipt = _bundle(**kwargs)
    return run_verified_capture_batch([{"bundle": bundle, "manifest_envelope": envelope, "receipt": receipt}])


def test_unverified_report_cannot_enter_archive():
    report = _report()
    report["capture_attestations"] = []
    report["receipt_required_for_durable_ingestion"] = False
    with pytest.raises(ValueError, match="capture_report_verified_receipts_required"):
        append_capture_report(EvidenceArchive(), report)


def test_testnet_zero_never_enters_production_scorecard():
    archive = append_capture_report(EvidenceArchive(), _report(environment="testnet"))
    score = production_scorecard(archive)
    assert score["production_observation_count"] == 0
    assert score["excluded_testnet_observation_count"] == 1


def test_production_observation_is_included_without_cross_snapshot_sum():
    report = _report(suffix="2", demand="positive_open_demand", count=2,
                     utilization="positive_paid_utilization", tx=3, paid=7.5)
    archive = append_capture_report(EvidenceArchive(), report)
    score = production_scorecard(archive)
    assert score["production_observation_count"] == 1
    assert score["platforms"][0]["latest_paid_value_usd"] == 7.5
    assert score["cross_snapshot_paid_value_sum_usd"] is None


def test_receipt_tampering_fails_archive_ingestion():
    report = _report(suffix="3")
    tampered = copy.deepcopy(report)
    tampered["capture_attestations"][0]["receipt"]["captured_environment"] = "testnet"
    with pytest.raises(ValueError, match="capture_receipt_hash_mismatch"):
        append_capture_report(EvidenceArchive(), tampered)


def test_receipt_bundle_mismatch_fails_archive_ingestion():
    report = _report(suffix="4")
    tampered = copy.deepcopy(report)
    tampered["capture_attestations"][0]["bundle_sha256"] = "5" * 64
    with pytest.raises(ValueError, match="capture_attestation_unmatched_bundle"):
        append_capture_report(EvidenceArchive(), tampered)


def test_environment_override_cannot_promote_or_relabel_receipt():
    report = _report(suffix="6", environment="testnet")
    with pytest.raises(ValueError, match="archive_environment_override_mismatch"):
        append_capture_report(EvidenceArchive(), report,
            environment_by_bundle_sha256={"6" * 64: "production"})


def test_serialization_roundtrip_is_deterministic_and_receipt_policy_persisted():
    archive = append_capture_report(EvidenceArchive(), _report(suffix="7"))
    first = serialize_archive(archive)
    loaded = parse_archive(first)
    assert first == serialize_archive(loaded)
    assert archive == loaded
    assert json.loads(first)["verified_capture_receipt_required"] is True


def test_duplicate_and_append_only_guards_remain_active():
    first = _report(suffix="8")
    archive = append_capture_report(EvidenceArchive(), first)
    with pytest.raises(ValueError, match="archive_duplicate_bundle_hash"):
        append_capture_report(archive, first)
    extended = append_capture_report(archive, _report(suffix="9"))
    require_append_only(archive, extended)
    with pytest.raises(ValueError, match="archive_append_only_rewrite"):
        require_append_only(archive, EvidenceArchive((extended.entries[1],)))
