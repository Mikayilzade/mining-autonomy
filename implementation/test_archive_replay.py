from datetime import datetime, timezone

from evidence_archive import EvidenceArchive, append_capture_report
from archive_replay import archive_observation_items, archive_replay_report, evidence_freshness

NOW = datetime(2026, 8, 19, 14, 0, tzinfo=timezone.utc)


def _report(*, suffix="1", platform="payanagent", source_timestamp="2026-08-19T13:00:00+00:00", demand="positive_open_demand", count=2, utilization="unproven", tx=None, paid=None):
    bundle = suffix * 64
    request = ("a" if suffix != "a" else "b") * 64
    delta = {
        "platform": platform,
        "source_url": f"https://example.test/{platform}/requests",
        "source_timestamp": source_timestamp,
        "captured_at": "2026-08-19T13:01:00+00:00",
        "bundle_sha256": bundle,
        "request_snapshot_sha256": request,
        "demand_state": demand,
        "open_item_count": count,
        "paid_utilization_state": utilization,
        "paid_transaction_count": tx,
        "paid_value_usd": paid,
    }
    return {"schema_version": 1, "deltas": [delta], "registry": {"schema_version": 1, "bundle_hashes": [bundle], "dry_run_only": True, "action_enabled": False}, "dry_run_only": True, "action_enabled": False}


def _append(archive, report, env):
    bundle = report["deltas"][0]["bundle_sha256"]
    return append_capture_report(archive, report, environment_by_bundle_sha256={bundle: env})


def test_testnet_and_unknown_never_replay_into_orchestrator():
    archive = _append(EvidenceArchive(), _report(suffix="1"), "testnet")
    archive = _append(archive, _report(suffix="2", platform="mcpize"), "unknown")
    assert archive_observation_items(archive, now=NOW) == []
    report = archive_replay_report(archive, now=NOW)
    assert report["production_platform_count"] == 0
    assert report["excluded_testnet_observation_count"] == 1
    assert report["excluded_unknown_observation_count"] == 1


def test_fresh_production_open_demand_replays_as_hold_only():
    archive = _append(EvidenceArchive(), _report(suffix="3"), "production")
    item = archive_observation_items(archive, now=NOW)[0]
    assert item.platform == "payanagent"
    assert item.state == "hold"
    assert item.demand_evidence_class == "open_paid_request"
    assert item.open_paid_demand_proven is True
    assert item.action_enabled is False
    assert "archive_evidence_only_no_raw_payload" in item.reasons


def test_paid_utilization_is_reported_but_cannot_enable_action():
    archive = _append(EvidenceArchive(), _report(suffix="4", platform="mcpize", utilization="positive_paid_utilization", tx=5, paid=12.5), "production")
    item = archive_observation_items(archive, now=NOW)[0]
    assert item.paid_utilization_proven is True
    assert item.demand_evidence_class == "settled_receipt"
    assert item.state == "hold" and item.action_enabled is False
    report = archive_replay_report(archive, now=NOW)
    assert report["platforms"][0]["paid_value_usd"] == 12.5
    assert report["cross_snapshot_paid_value_sum_usd"] is None


def test_stale_evidence_is_explicit_and_held():
    archive = _append(EvidenceArchive(), _report(suffix="5", source_timestamp="2026-08-17T13:00:00+00:00"), "production")
    item = archive_observation_items(archive, now=NOW, max_age_hours=24)[0]
    assert "evidence_stale" in item.reasons
    report = archive_replay_report(archive, now=NOW, max_age_hours=24)
    assert report["stale_platform_count"] == 1
    assert report["fresh_platform_count"] == 0


def test_future_clock_skew_fails_freshness():
    fresh = evidence_freshness("2026-08-19T14:10:00+00:00", now=NOW, max_future_skew_minutes=5)
    assert fresh.state == "future_invalid"


def test_latest_production_observation_wins_per_platform():
    archive = _append(EvidenceArchive(), _report(suffix="6", demand="positive_open_demand", count=3, source_timestamp="2026-08-19T12:00:00+00:00"), "production")
    archive = _append(archive, _report(suffix="7", demand="zero_open_observation", count=0, source_timestamp="2026-08-19T13:30:00+00:00"), "production")
    report = archive_replay_report(archive, now=NOW)
    assert report["production_platform_count"] == 1
    assert report["platforms"][0]["demand_state"] == "zero_open_observation"
    assert report["platforms"][0]["open_item_count"] == 0


def test_archive_replay_never_claims_economic_authorization():
    archive = _append(EvidenceArchive(), _report(suffix="8"), "production")
    report = archive_replay_report(archive, now=NOW)
    assert report["archive_evidence_can_authorize_action"] is False
    assert report["dry_run_only"] is True
    assert report["action_enabled"] is False
