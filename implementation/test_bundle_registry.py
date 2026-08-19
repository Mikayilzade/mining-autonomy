import json
import pytest
from bundle_registry import BundleRegistry, add_bundle, build_registry, cross_market_scorecard, serialize_registry


def sha(ch): return ch * 64


def bundle(platform, bundle_sha, request_sha, ts, items, evidence="unknown", utilization=None):
    return {
        "platform": platform,
        "request_envelope": {"snapshot": {"platform": platform, "source_url": f"https://example.test/{platform}",
            "source_timestamp": ts, "captured_at": ts, "evidence_class": "official_api",
            "payload": {"items": items}, "payload_sha256": request_sha},
            "demand_evidence_class": evidence, "records_key": "items"},
        "receipt_envelope": None, "task_audit": {}, "utilization": utilization,
        "utilization_history": None,
        "manifest": {"platform": platform, "dry_run_only": True, "action_enabled": False},
        "manifest_sha256": bundle_sha, "signature_hmac_sha256": sha("f")}


def test_duplicate_bundle_hash_is_rejected_globally_even_across_platforms():
    r = add_bundle(BundleRegistry(), bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", []))
    with pytest.raises(ValueError, match="duplicate_observation_bundle_hash"):
        add_bundle(r, bundle("agent2agent_market", sha("a"), sha("2"), "2026-08-19T10:01:00Z", []))


def test_zero_and_positive_open_observations_remain_separate():
    r = build_registry([
        bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", [{"id": "x"}], "open_paid_request"),
        bundle("payanagent", sha("b"), sha("2"), "2026-08-19T11:00:00Z", [], "unknown")])
    score = cross_market_scorecard(r)["platforms"][0]
    assert score["positive_open_observation_count"] == 1
    assert score["zero_open_observation_count"] == 1
    assert score["latest_demand_state"] == "zero_open_observation"
    assert score["evidence_status"] == "zero_open_observed_latest"


def test_paid_utilization_is_preserved_as_strongest_evidence_without_summing_windows():
    r = build_registry([
        bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", [], utilization={"transaction_count": 2, "total_value_usd": 3.0}),
        bundle("payanagent", sha("b"), sha("2"), "2026-08-19T11:00:00Z", [], utilization={"transaction_count": 4, "total_value_usd": 7.0})])
    card = cross_market_scorecard(r); score = card["platforms"][0]
    assert score["evidence_status"] == "confirmed_paid_utilization_observed"
    assert score["latest_paid_transaction_count"] == 4
    assert score["latest_paid_value_usd"] == 7.0
    assert score["paid_value_aggregation"] == "none_across_snapshots"
    assert card["cross_snapshot_paid_value_sum_usd"] is None
    assert card["cross_snapshot_extrapolation"] is False


def test_cross_market_scorecard_is_deterministic_and_platform_sorted():
    a = bundle("payanagent", sha("a"), sha("1"), "2026-08-19T11:00:00Z", [])
    b = bundle("agent2agent_market", sha("b"), sha("2"), "2026-08-19T10:00:00Z", [])
    r1 = build_registry([a, b]); r2 = build_registry([b, a])
    assert serialize_registry(r1) == serialize_registry(r2)
    assert [p["platform"] for p in cross_market_scorecard(r1)["platforms"]] == ["agent2agent_market", "payanagent"]


def test_same_request_snapshot_can_be_observed_twice_but_is_counted_distinctly_in_scorecard():
    r = build_registry([bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", []),
                        bundle("payanagent", sha("b"), sha("1"), "2026-08-19T10:05:00Z", [])])
    score = cross_market_scorecard(r)["platforms"][0]
    assert score["observation_count"] == 2
    assert score["distinct_request_snapshot_count"] == 1


def test_registry_rejects_action_enabled_bundle():
    value = bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", [])
    value["manifest"]["action_enabled"] = True
    with pytest.raises(ValueError, match="dry_run_action_disabled"):
        add_bundle(BundleRegistry(), value)


def test_open_paid_evidence_cannot_be_empty():
    value = bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", [], "open_paid_request")
    with pytest.raises(ValueError, match="open_paid_request_must_have_items"):
        add_bundle(BundleRegistry(), value)


def test_serialized_registry_cannot_enable_actions():
    r = build_registry([bundle("payanagent", sha("a"), sha("1"), "2026-08-19T10:00:00Z", [])])
    parsed = json.loads(serialize_registry(r))
    assert parsed["dry_run_only"] is True
    assert parsed["action_enabled"] is False
