from copy import deepcopy

import pytest

import capture_readiness


PROVENANCE = (
    "record_exact_source_url",
    "record_capture_timestamp_utc",
)


def _manifest_item(*, platform="payanagent", url="https://example.com/open", env="production", classes=("open_demand_snapshot",), scheduled=True):
    return {
        "platform": platform,
        "source_url": url,
        "method": "GET",
        "scheduled": scheduled,
        "expected_evidence_classes": list(classes),
        "environment": env,
        "rate_limit": {
            "min_interval_seconds": 900.0,
            "max_requests_per_window": 1,
            "window_seconds": 900.0,
            "budget_basis": "project_conservative_self_limit",
        },
        "provenance_requirements": list(PROVENANCE),
        "credentials_allowed": False,
        "network_calls_performed": False,
        "action_enabled": False,
    }


def _envelope(items):
    return {
        "manifest": {
            "schema_version": 1,
            "network_calls_performed": False,
            "credentials_allowed": False,
            "action_enabled": False,
            "items": items,
        },
        "manifest_sha256": "m" * 64,
    }


def _plan(envelope, selected):
    return {
        "schema_version": 1,
        "mode": "deterministic_plan_only_production_gap_priority",
        "manifest_sha256": envelope["manifest_sha256"],
        "selected_read_only_observations": selected,
        "missing_evidence_is_negative_demand": False,
        "credentials_allowed": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }


def _selected(item, index=0):
    return {
        "platform": item["platform"],
        "item_index": index,
        "source_url": item["source_url"],
        "manifest_item_sha256": f"sha-{index}",
        "rate_budget_score": 10,
        "unresolved_gaps": ["production_capture_missing"],
    }


def test_production_demand_source_is_ready(monkeypatch):
    item = _manifest_item()
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    packet = capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)
    assert packet["ready_count"] == 1
    assert packet["blocked_count"] == 0
    assert packet["authorization_granted"] is False
    assert packet["network_calls_performed"] is False


def test_unknown_environment_is_blocked(monkeypatch):
    item = _manifest_item(env="unknown", classes=("open_demand_snapshot", "environment_marker"))
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    packet = capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)
    assert packet["blocked_count"] == 1
    assert "production_environment_not_predeclared" in packet["items"][0]["readiness_reasons"]


def test_observability_gate_only_is_blocked(monkeypatch):
    item = _manifest_item(platform="mcpize", classes=("public_observability_gate",))
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    packet = capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)
    assert packet["blocked_count"] == 1
    assert "source_observability_cannot_close_demand_gap_by_itself" in packet["items"][0]["readiness_reasons"]


def test_manifest_identity_mismatch_fails_closed(monkeypatch):
    item = _manifest_item()
    env = _envelope([item])
    selected = _selected(item)
    selected["source_url"] = "https://evil.invalid/"
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    with pytest.raises(ValueError, match="capture_readiness_manifest_identity_mismatch"):
        capture_readiness.build_capture_readiness_packet(_plan(env, [selected]), env)


def test_non_get_is_rejected(monkeypatch):
    item = _manifest_item()
    item["method"] = "POST"
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    with pytest.raises(ValueError, match="capture_readiness_non_get_forbidden"):
        capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)


def test_bad_rate_limit_is_rejected(monkeypatch):
    item = _manifest_item()
    item["rate_limit"]["max_requests_per_window"] = 0
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    with pytest.raises(ValueError, match="capture_readiness_rate_limit_invalid"):
        capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)


def test_duplicate_selected_item_is_rejected(monkeypatch):
    item = _manifest_item()
    env = _envelope([item])
    row = _selected(item)
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    with pytest.raises(ValueError, match="capture_readiness_duplicate_selected_item"):
        capture_readiness.build_capture_readiness_packet(_plan(env, [row, deepcopy(row)]), env)


def test_packet_preserves_provenance_and_no_action(monkeypatch):
    item = _manifest_item()
    env = _envelope([item])
    monkeypatch.setattr(capture_readiness, "verify_sampling_manifest_envelope", lambda _: None)
    monkeypatch.setattr(capture_readiness, "manifest_item_sha256", lambda _e, i: f"sha-{i}")
    packet = capture_readiness.build_capture_readiness_packet(_plan(env, [_selected(item)]), env)
    row = packet["items"][0]
    assert tuple(row["provenance_checklist"]) == PROVENANCE
    assert row["method"] == "GET"
    assert row["credentials_allowed"] is False
    assert row["action_enabled"] is False
    assert row["dry_run_only"] is True
