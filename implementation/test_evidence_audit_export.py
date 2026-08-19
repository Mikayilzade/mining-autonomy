from datetime import datetime, timezone

from evidence_audit_export import evidence_audit_export
from evidence_archive import EvidenceArchive, append_capture_report
from observation_capture import run_verified_capture_batch
from sampling_receipt import TransportResult, bind_capture_result, seal_sampling_manifest

NOW = datetime(2026, 8, 20, 0, 0, tzinfo=timezone.utc)


def _capture(*, platform, suffix, environment="production", demand="positive_open_demand",
             count=1, source_timestamp="2026-08-19T23:00:00+00:00"):
    source_url = f"https://example.test/{platform}/requests"
    captured_at = "2026-08-19T23:01:00+00:00"
    evidence = "open_paid_request" if demand == "positive_open_demand" else "unknown"
    items = [{"id": f"{platform}-{suffix}-{index}"} for index in range(count)]
    bundle = {
        "platform": platform,
        "request_envelope": {
            "demand_evidence_class": evidence,
            "records_key": "items",
            "snapshot": {
                "platform": platform,
                "source_url": source_url,
                "source_timestamp": source_timestamp,
                "captured_at": captured_at,
                "payload_sha256": suffix * 64,
                "payload": {"items": items},
            },
        },
        "utilization": None,
        "manifest": {"platform": platform, "dry_run_only": True, "action_enabled": False},
        "manifest_sha256": suffix * 64,
    }
    manifest = {
        "schema_version": 1,
        "generated_at": "2026-08-19T22:59:00+00:00",
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "scheduled_source_count": 1,
        "source_count": 1,
        "items": [{
            "platform": platform,
            "source_url": source_url,
            "method": "GET",
            "scheduled": True,
            "expected_evidence_classes": ["open_demand_snapshot"],
            "environment": environment,
            "credentials_allowed": False,
            "network_calls_performed": False,
            "action_enabled": False,
        }],
    }
    envelope = seal_sampling_manifest(manifest)
    receipt = bind_capture_result(
        envelope,
        item_index=0,
        result=TransportResult(
            sanitized_bundle_sha256=bundle["manifest_sha256"],
            capture_started_at="2026-08-19T23:00:59+00:00",
            capture_finished_at=captured_at,
            captured_environment=environment,
            source_timestamp=source_timestamp,
        ),
        transport_name="fixture",
        transport_network_capable=False,
    )
    report = run_verified_capture_batch([
        {"bundle": bundle, "manifest_envelope": envelope, "receipt": receipt}
    ])
    return envelope, receipt, report


def test_complete_production_chain_is_joined_end_to_end():
    envelope, receipt, capture = _capture(platform="payanagent", suffix="1")
    archive = append_capture_report(EvidenceArchive(), capture)
    report = evidence_audit_export(
        envelope, [receipt], archive, receipt_capture_reports=[capture], now=NOW
    )
    assert report["production_complete_source_count"] == 1
    assert report["unresolved_production_source_count"] == 0
    row = report["sources"][0]
    assert row["receipt_state"] == "receipt_valid_production"
    assert row["archive_member"] is True
    assert row["replay_member"] is True
    assert row["replay_receipt_provenance_verified"] is True
    assert row["production_evidence_complete"] is True
    assert row["action_enabled"] is False


def test_missing_capture_is_explicit_gap_not_zero_demand():
    envelope, _, _ = _capture(platform="payanagent", suffix="2")
    report = evidence_audit_export(envelope, [], EvidenceArchive(), now=NOW)
    row = report["sources"][0]
    assert row["receipt_state"] == "scheduled_but_uncaptured"
    assert row["unresolved_production_gaps"] == ["production_capture_missing"]
    assert row["demand_state"] is None
    assert report["missing_capture_is_not_zero_demand"] is True


def test_valid_testnet_receipt_cannot_close_production_gap():
    envelope, receipt, _ = _capture(
        platform="agent2agent.market", suffix="3", environment="testnet"
    )
    report = evidence_audit_export(envelope, [receipt], EvidenceArchive(), now=NOW)
    row = report["sources"][0]
    assert row["receipt_state"] == "receipt_valid_non_production"
    assert row["production_evidence_complete"] is False
    assert "production_receipt_missing" in row["unresolved_production_gaps"]
    assert report["non_production_can_close_production_gap"] is False


def test_archive_without_supplied_replay_receipt_provenance_stays_incomplete():
    envelope, receipt, capture = _capture(platform="mcpize", suffix="4")
    archive = append_capture_report(EvidenceArchive(), capture)
    report = evidence_audit_export(envelope, [receipt], archive, now=NOW)
    row = report["sources"][0]
    assert row["archive_member"] is True
    assert row["replay_member"] is True
    assert row["replay_receipt_provenance_verified"] is False
    assert "replay_receipt_provenance_missing" in row["unresolved_production_gaps"]
    assert row["production_evidence_complete"] is False


def test_stale_replay_is_reported_as_unresolved_production_gap():
    envelope, receipt, capture = _capture(
        platform="payanagent", suffix="5",
        source_timestamp="2026-08-17T23:00:00+00:00",
    )
    archive = append_capture_report(EvidenceArchive(), capture)
    report = evidence_audit_export(
        envelope, [receipt], archive, receipt_capture_reports=[capture],
        now=NOW, max_age_hours=24,
    )
    row = report["sources"][0]
    assert row["replay_freshness_state"] == "stale"
    assert "replay_evidence_stale" in row["unresolved_production_gaps"]
    assert row["production_evidence_complete"] is False


def test_platform_summary_rolls_up_unresolved_source_gap_types():
    envelope, receipt, capture = _capture(platform="payanagent", suffix="6")
    archive = append_capture_report(EvidenceArchive(), capture)
    report = evidence_audit_export(envelope, [receipt], archive, now=NOW)
    summary = report["platforms"][0]
    assert summary["platform"] == "payanagent"
    assert summary["unresolved_source_count"] == 1
    assert summary["unresolved_gap_types"] == ["replay_receipt_provenance_missing"]
    assert report["archive_or_receipt_can_authorize_action"] is False
    assert report["network_calls_performed"] is False
    assert report["dry_run_only"] is True
    assert report["action_enabled"] is False
