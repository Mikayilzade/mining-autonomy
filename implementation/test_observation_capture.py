from datetime import datetime, timezone

import pytest

from bundle_registry import BundleRegistry
from observation_capture import (
    CapturePolicy,
    CaptureState,
    apply_captured_bundle,
    run_capture_batch,
    time_series_scorecard,
)


def _bundle(*, platform="payanagent", suffix="1", source_timestamp="2026-08-19T12:00:00+00:00",
            captured_at="2026-08-19T12:01:00+00:00", items=None, evidence="unknown",
            source_url="https://example.test/requests", utilization=None):
    items = [] if items is None else items
    digit = suffix[-1].lower()
    if digit not in "0123456789abcdef":
        digit = "a"
    return {
        "platform": platform,
        "request_envelope": {
            "demand_evidence_class": evidence,
            "records_key": "items",
            "snapshot": {
                "platform": platform,
                "source_url": source_url,
                "source_timestamp": source_timestamp,
                "captured_at": captured_at,
                "payload_sha256": digit * 64,
                "payload": {"items": items},
            },
        },
        "utilization": utilization,
        "manifest": {"platform": platform, "dry_run_only": True, "action_enabled": False},
        "manifest_sha256": ("f" if digit == "e" else "e") * 63 + digit,
    }


def test_fresh_zero_open_bundle_is_registered():
    bundle = _bundle()
    registry, state, delta = apply_captured_bundle(BundleRegistry(), CaptureState(), bundle)
    assert len(registry.entries) == 1
    assert delta.demand_state == "zero_open_observation"
    assert delta.distinct_request_snapshot_added is True
    assert state.last_capture_by_source


def test_stale_source_snapshot_fails_closed():
    bundle = _bundle(source_timestamp="2026-08-17T12:00:00+00:00", captured_at="2026-08-19T12:00:00+00:00")
    with pytest.raises(ValueError, match="capture_source_snapshot_stale"):
        apply_captured_bundle(BundleRegistry(), CaptureState(), bundle, policy=CapturePolicy(max_age_hours=24))


def test_future_source_timestamp_beyond_skew_fails_closed():
    bundle = _bundle(source_timestamp="2026-08-19T12:10:00+00:00", captured_at="2026-08-19T12:00:00+00:00")
    with pytest.raises(ValueError, match="capture_source_timestamp_too_far_in_future"):
        apply_captured_bundle(BundleRegistry(), CaptureState(), bundle)


def test_non_https_public_source_rejected():
    bundle = _bundle(source_url="http://example.test/requests")
    with pytest.raises(ValueError, match="capture_public_source_must_use_https"):
        apply_captured_bundle(BundleRegistry(), CaptureState(), bundle)


def test_rate_limit_guard_is_per_platform_and_source():
    first = _bundle(suffix="1", captured_at="2026-08-19T12:01:00+00:00")
    second = _bundle(suffix="2", source_timestamp="2026-08-19T12:02:00+00:00", captured_at="2026-08-19T12:03:00+00:00")
    registry, state, _ = apply_captured_bundle(BundleRegistry(), CaptureState(), first)
    with pytest.raises(ValueError, match="capture_rate_limit_guard"):
        apply_captured_bundle(registry, state, second, policy=CapturePolicy(min_interval_seconds=300))


def test_same_request_snapshot_later_does_not_claim_distinct_market_state():
    first = _bundle(suffix="1", captured_at="2026-08-19T12:01:00+00:00")
    second = _bundle(suffix="2", source_timestamp="2026-08-19T12:10:00+00:00", captured_at="2026-08-19T12:11:00+00:00")
    second["request_envelope"]["snapshot"]["payload_sha256"] = first["request_envelope"]["snapshot"]["payload_sha256"]
    registry, state, _ = apply_captured_bundle(BundleRegistry(), CaptureState(), first)
    registry, _, delta = apply_captured_bundle(registry, state, second)
    assert delta.distinct_request_snapshot_added is False
    assert len(registry.entries) == 2


def test_time_series_preserves_exact_paid_observation_without_sum():
    bundle = _bundle(
        suffix="3", items=[{"id": "r1"}], evidence="open_paid_request",
        utilization={"transaction_count": 2, "total_value_usd": 4.5},
    )
    registry, _, _ = apply_captured_bundle(BundleRegistry(), CaptureState(), bundle)
    scorecard = time_series_scorecard(registry)
    point = scorecard["platforms"][0]["points"][0]
    assert point["paid_value_usd"] == 4.5
    assert scorecard["paid_value_aggregation"] == "none_across_observations"
    assert scorecard["paid_value_extrapolation"] is False


def test_batch_is_deterministic_and_action_disabled():
    later = _bundle(suffix="4", platform="agent2agent_market", source_url="https://example.test/tasks",
                    source_timestamp="2026-08-19T12:20:00+00:00", captured_at="2026-08-19T12:21:00+00:00")
    earlier = _bundle(suffix="5", source_timestamp="2026-08-19T12:00:00+00:00", captured_at="2026-08-19T12:01:00+00:00")
    report = run_capture_batch([later, earlier])
    assert [d["platform"] for d in report["deltas"]] == ["payanagent", "agent2agent_market"]
    assert report["action_enabled"] is False
    assert report["dry_run_only"] is True
    assert report["time_series_scorecard"]["action_enabled"] is False
