from datetime import datetime, timezone

from evidence_archive import ArchiveEntry, EvidenceArchive
from sampling_planner import WatchTarget, build_sampling_plan, sampling_plan_report

NOW = datetime(2026, 8, 19, 15, 0, tzinfo=timezone.utc)


def _entry(*, platform="payanagent", env="production", timestamp="2026-08-19T14:00:00+00:00",
           demand="unproven", utilization="unproven", suffix="a"):
    return ArchiveEntry(
        sequence=1,
        environment=env,
        platform=platform,
        source_url=f"https://example.test/{platform}",
        source_timestamp=timestamp,
        captured_at=timestamp,
        bundle_sha256=suffix * 64,
        request_snapshot_sha256=("b" if suffix != "b" else "c") * 64,
        demand_state=demand,
        open_item_count=1 if demand == "positive_open_demand" else 0,
        paid_utilization_state=utilization,
        paid_transaction_count=1 if utilization == "positive_paid_utilization" else None,
        paid_value_usd=1.0 if utilization == "positive_paid_utilization" else None,
        source_report_sha256="d" * 64,
        previous_entry_sha256=None,
        entry_sha256=("e" if suffix != "e" else "f") * 64,
    )


def test_empty_archive_prioritizes_primary_platform_and_marks_never_observed():
    plan = build_sampling_plan(EvidenceArchive(), now=NOW)
    assert plan[0].platform == "payanagent"
    assert plan[0].freshness_state == "never_observed"
    assert plan[0].due is True
    assert plan[0].network_calls_performed is False
    assert plan[0].action_enabled is False


def test_testnet_observation_does_not_satisfy_production_gap():
    archive = EvidenceArchive((_entry(env="testnet"),))
    item = next(x for x in build_sampling_plan(archive, now=NOW) if x.platform == "payanagent")
    assert item.production_observation_present is False
    assert "no_production_observation" in item.reasons


def test_stale_high_priority_target_outranks_fresh_lower_priority_target():
    high = WatchTarget("high", 5, 6.0, ("open",), ("https://example.test/high",))
    low = WatchTarget("low", 3, 24.0, ("open",), ("https://example.test/low",))
    archive = EvidenceArchive((
        _entry(platform="high", timestamp="2026-08-18T00:00:00+00:00", suffix="1"),
        _entry(platform="low", timestamp="2026-08-19T14:30:00+00:00",
               demand="positive_open_demand", utilization="positive_paid_utilization", suffix="2"),
    ))
    plan = build_sampling_plan(archive, now=NOW, targets=(low, high))
    assert plan[0].platform == "high"
    assert plan[0].freshness_state == "stale"
    low_item = next(x for x in plan if x.platform == "low")
    assert low_item.due is False


def test_positive_open_demand_still_keeps_paid_utilization_gap_due():
    archive = EvidenceArchive((_entry(demand="positive_open_demand"),))
    item = next(x for x in build_sampling_plan(archive, now=NOW) if x.platform == "payanagent")
    assert item.demand_gap is False
    assert item.paid_utilization_gap is True
    assert item.due is True


def test_fresh_complete_evidence_is_not_due():
    target = WatchTarget("complete", 4, 24.0, ("open", "receipts"), ("https://example.test/complete",))
    archive = EvidenceArchive((_entry(platform="complete", demand="positive_open_demand",
                                      utilization="positive_paid_utilization"),))
    item = build_sampling_plan(archive, now=NOW, targets=(target,))[0]
    assert item.due is False
    assert item.reasons == ("fresh_required_evidence_present",)


def test_future_invalid_evidence_is_due_and_explicit():
    target = WatchTarget("future", 4, 24.0, ("open",), ("https://example.test/future",))
    archive = EvidenceArchive((_entry(platform="future", timestamp="2026-08-19T16:00:00+00:00"),))
    item = build_sampling_plan(archive, now=NOW, targets=(target,))[0]
    assert item.freshness_state == "future_invalid"
    assert "evidence_future_invalid" in item.reasons
    assert item.due is True


def test_report_is_plan_only_and_performs_no_network_or_actions():
    report = sampling_plan_report(EvidenceArchive(), now=NOW)
    assert report["planner_mode"] == "read_only_plan_only"
    assert report["network_calls_performed"] is False
    assert report["action_enabled"] is False
    assert report["due_count"] == report["platform_count"]
