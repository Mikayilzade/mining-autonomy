from datetime import datetime, timezone

from archive_replay import archive_observation_items, archive_replay_report, evidence_freshness
from evidence_archive import EvidenceArchive, append_capture_report
from observation_capture import run_verified_capture_batch
from sampling_receipt import TransportResult, bind_capture_result, seal_sampling_manifest

NOW = datetime(2026, 8, 19, 14, 0, tzinfo=timezone.utc)


def _verified_report(*, suffix="1", platform="payanagent", source_timestamp="2026-08-19T13:00:00+00:00", demand="positive_open_demand", count=2, utilization="unproven", tx=None, paid=None, environment="production"):
    source_url = f"https://example.test/{platform}/requests"
    captured_at = "2026-08-19T13:01:00+00:00"
    evidence = "open_paid_request" if demand == "positive_open_demand" else "unknown"
    items = [{"id": f"item-{suffix}-{index}"} for index in range(count)]
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
    manifest = {"schema_version": 1, "generated_at": "2026-08-19T12:59:00+00:00",
        "mode": "inert_read_only_sampling_contract", "network_calls_performed": False,
        "action_enabled": False, "credentials_allowed": False, "scheduled_source_count": 1,
        "source_count": 1, "items": [{"platform": platform, "source_url": source_url,
            "method": "GET", "scheduled": True, "expected_evidence_classes": ["open_demand_snapshot"],
            "environment": environment, "credentials_allowed": False, "network_calls_performed": False,
            "action_enabled": False}]}
    envelope = seal_sampling_manifest(manifest)
    receipt = bind_capture_result(envelope, item_index=0,
        result=TransportResult(sanitized_bundle_sha256=bundle["manifest_sha256"],
            capture_started_at="2026-08-19T13:00:59+00:00", capture_finished_at=captured_at,
            captured_environment=environment, source_timestamp=source_timestamp),
        transport_name="fixture", transport_network_capable=False)
    return run_verified_capture_batch([{"bundle": bundle, "manifest_envelope": envelope, "receipt": receipt}])


def _append(archive, report):
    return append_capture_report(archive, report)


def test_testnet_and_unknown_never_replay_into_orchestrator():
    archive = _append(EvidenceArchive(), _verified_report(suffix="1", environment="testnet"))
    archive = _append(archive, _verified_report(suffix="2", platform="mcpize", environment="unknown"))
    assert archive_observation_items(archive, now=NOW) == []
    report = archive_replay_report(archive, now=NOW)
    assert report["production_platform_count"] == 0
    assert report["excluded_testnet_observation_count"] == 1
    assert report["excluded_unknown_observation_count"] == 1


def test_fresh_production_open_demand_replays_as_hold_only():
    capture = _verified_report(suffix="3")
    archive = _append(EvidenceArchive(), capture)
    item = archive_observation_items(archive, now=NOW)[0]
    assert item.platform == "payanagent"
    assert item.state == "hold"
    assert item.demand_evidence_class == "open_paid_request"
    assert item.open_paid_demand_proven is True
    assert item.action_enabled is False
    assert "archive_evidence_only_no_raw_payload" in item.reasons


def test_paid_utilization_is_reported_but_cannot_enable_action():
    capture = _verified_report(suffix="4", platform="mcpize", utilization="positive_paid_utilization", tx=5, paid=12.5)
    archive = _append(EvidenceArchive(), capture)
    item = archive_observation_items(archive, now=NOW)[0]
    assert item.paid_utilization_proven is True
    assert item.demand_evidence_class == "settled_receipt"
    assert item.state == "hold" and item.action_enabled is False
    report = archive_replay_report(archive, now=NOW, receipt_capture_reports=[capture])
    row = report["platforms"][0]
    assert row["paid_value_usd"] == 12.5
    assert row["receipt_provenance_verified"] is True
    assert row["receipt_provenance"]["receipt_sha256"]
    assert row["receipt_provenance"]["manifest_item_sha256"]
    assert report["cross_snapshot_paid_value_sum_usd"] is None
    assert report["receipt_provenance_can_authorize_action"] is False


def test_stale_evidence_is_explicit_and_held():
    capture = _verified_report(suffix="5", source_timestamp="2026-08-17T13:00:00+00:00")
    archive = _append(EvidenceArchive(), capture)
    item = archive_observation_items(archive, now=NOW, max_age_hours=24)[0]
    assert "evidence_stale" in item.reasons
    report = archive_replay_report(archive, now=NOW, max_age_hours=24)
    assert report["stale_platform_count"] == 1
    assert report["fresh_platform_count"] == 0


def test_future_clock_skew_fails_freshness():
    fresh = evidence_freshness("2026-08-19T14:10:00+00:00", now=NOW, max_future_skew_minutes=5)
    assert fresh.state == "future_invalid"


def test_latest_production_observation_wins_per_platform():
    first = _verified_report(suffix="6", demand="positive_open_demand", count=3, source_timestamp="2026-08-19T12:00:00+00:00")
    second = _verified_report(suffix="7", demand="zero_open_observation", count=0, source_timestamp="2026-08-19T13:30:00+00:00")
    archive = _append(EvidenceArchive(), first)
    archive = _append(archive, second)
    report = archive_replay_report(archive, now=NOW, receipt_capture_reports=[first, second])
    assert report["production_platform_count"] == 1
    assert report["platforms"][0]["demand_state"] == "zero_open_observation"
    assert report["platforms"][0]["open_item_count"] == 0
    assert report["receipt_provenance_verified_platform_count"] == 1


def test_missing_receipt_report_is_explicit_not_inferred():
    capture = _verified_report(suffix="8")
    archive = _append(EvidenceArchive(), capture)
    report = archive_replay_report(archive, now=NOW)
    assert report["receipt_provenance_verified_platform_count"] == 0
    assert report["receipt_provenance_missing_platform_count"] == 1
    assert report["platforms"][0]["receipt_provenance"] is None


def test_archive_replay_never_claims_economic_authorization():
    capture = _verified_report(suffix="9")
    archive = _append(EvidenceArchive(), capture)
    report = archive_replay_report(archive, now=NOW, receipt_capture_reports=[capture])
    assert report["archive_evidence_can_authorize_action"] is False
    assert report["receipt_provenance_can_authorize_action"] is False
    assert report["dry_run_only"] is True
    assert report["action_enabled"] is False
