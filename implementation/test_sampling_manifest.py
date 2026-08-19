from datetime import datetime, timezone

from evidence_archive import ArchiveEntry, EvidenceArchive
from sampling_manifest import (
    SourcePolicy,
    SourceRateLimit,
    SamplingManifestItem,
    build_sampling_manifest,
    capture_bridge_spec,
)
from sampling_planner import WatchTarget

NOW = datetime(2026, 8, 19, 16, 48, tzinfo=timezone.utc)


def _entry(*, platform="payanagent", env="production", timestamp="2026-08-19T16:00:00+00:00",
           demand="positive_open_demand", utilization="positive_paid_utilization"):
    return ArchiveEntry(
        sequence=1,
        environment=env,
        platform=platform,
        source_url=f"https://example.test/{platform}",
        source_timestamp=timestamp,
        captured_at=timestamp,
        bundle_sha256="a" * 64,
        request_snapshot_sha256="b" * 64,
        demand_state=demand,
        open_item_count=1 if demand == "positive_open_demand" else 0,
        paid_utilization_state=utilization,
        paid_transaction_count=1 if utilization == "positive_paid_utilization" else None,
        paid_value_usd=1.0 if utilization == "positive_paid_utilization" else None,
        source_report_sha256="c" * 64,
        previous_entry_sha256=None,
        entry_sha256="d" * 64,
    )


def _item(raw):
    return SamplingManifestItem(**{
        **raw,
        "rate_limit": SourceRateLimit(**raw["rate_limit"]),
    })


def test_empty_archive_builds_inert_due_manifest_with_payan_first():
    report = build_sampling_manifest(EvidenceArchive(), now=NOW)
    assert report["mode"] == "inert_read_only_sampling_contract"
    assert report["network_calls_performed"] is False
    assert report["action_enabled"] is False
    assert report["credentials_allowed"] is False
    assert report["scheduled_source_count"] == report["source_count"]
    assert report["items"][0]["platform"] == "payanagent"
    assert report["items"][0]["method"] == "GET"


def test_payan_deadline_and_self_imposed_rate_budget_are_deterministic():
    report = build_sampling_manifest(EvidenceArchive(), now=NOW)
    discover = next(item for item in report["items"] if item["source_url"].endswith("/discover"))
    assert discover["capture_deadline"] == "2026-08-19T18:48:00+00:00"
    assert discover["rate_limit"]["min_interval_seconds"] == 900.0
    assert discover["rate_limit"]["budget_basis"] == "project_conservative_self_limit"


def test_fresh_complete_platform_sources_are_not_scheduled():
    target = WatchTarget("payanagent", 5, 6.0, ("open", "receipts"), ("https://payanagent.com/",))
    archive = EvidenceArchive((_entry(),))
    report = build_sampling_manifest(archive, now=NOW, targets=(target,), source_policies=(
        SourcePolicy("payanagent", "https://payanagent.com/api/v1/discover", ("open_demand_snapshot",),
                     2.0, 6.0, SourceRateLimit(900.0, 1, 900.0)),
    ))
    assert report["scheduled_source_count"] == 0
    assert report["items"][0]["scheduled"] is False
    assert report["items"][0]["capture_deadline"] is None


def test_testnet_evidence_cannot_cancel_production_schedule():
    archive = EvidenceArchive((_entry(env="testnet"),))
    report = build_sampling_manifest(archive, now=NOW)
    payan = [item for item in report["items"] if item["platform"] == "payanagent"]
    assert all(item["scheduled"] is True for item in payan)


def test_unknown_environment_bridge_never_promotes_to_production():
    report = build_sampling_manifest(EvidenceArchive(), now=NOW)
    raw = next(item for item in report["items"] if item["platform"] == "agent2agent.market")
    bridge = capture_bridge_spec(_item(raw), bundle_sha256="e" * 64)
    assert bridge["environment_by_bundle_sha256"] == {}
    assert bridge["default_environment"] == "unknown"
    assert bridge["action_enabled"] is False


def test_production_bridge_is_explicit_and_reuses_capture_rate_limit():
    report = build_sampling_manifest(EvidenceArchive(), now=NOW)
    raw = next(item for item in report["items"] if item["source_url"].endswith("/receipts"))
    bridge = capture_bridge_spec(_item(raw), bundle_sha256="f" * 64)
    assert bridge["environment_by_bundle_sha256"] == {"f" * 64: "production"}
    assert bridge["capture_policy"]["min_interval_seconds"] == 900.0
    assert bridge["route"] == ("observation_capture", "evidence_archive", "archive_replay")


def test_non_get_or_off_host_policy_fails_closed():
    target = WatchTarget("payanagent", 5, 6.0, ("open",), ("https://payanagent.com/",))
    post = SourcePolicy("payanagent", "https://payanagent.com/x", ("open_demand_snapshot",),
                        1.0, 6.0, SourceRateLimit(1.0, 1, 1.0), method="POST")
    try:
        build_sampling_manifest(EvidenceArchive(), now=NOW, targets=(target,), source_policies=(post,))
    except ValueError as exc:
        assert str(exc) == "manifest_only_get_allowed"
    else:
        raise AssertionError("POST policy accepted")

    off_host = SourcePolicy("payanagent", "https://example.com/x", ("open_demand_snapshot",),
                            1.0, 6.0, SourceRateLimit(1.0, 1, 1.0))
    try:
        build_sampling_manifest(EvidenceArchive(), now=NOW, targets=(target,), source_policies=(off_host,))
    except ValueError as exc:
        assert str(exc) == "manifest_source_host_not_in_watch_target"
    else:
        raise AssertionError("off-host policy accepted")
