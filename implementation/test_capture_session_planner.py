from copy import deepcopy

import pytest

from capture_session_planner import build_capture_session_plan


def _row(
    *,
    platform="payanagent",
    index=0,
    url="https://api.example.com/open",
    min_interval=10.0,
    max_requests=2,
    window=60.0,
    ready=True,
):
    return {
        "platform": platform,
        "item_index": index,
        "source_url": url,
        "manifest_item_sha256": f"sha-{index}",
        "method": "GET",
        "expected_evidence_classes": ["open_demand_snapshot"],
        "required_environment": "production",
        "provenance_checklist": ["record_exact_source_url", "record_capture_timestamp_utc"],
        "rate_limit": {
            "min_interval_seconds": min_interval,
            "max_requests_per_window": max_requests,
            "window_seconds": window,
            "budget_basis": "project_conservative_self_limit",
        },
        "rate_budget_score": 10,
        "unresolved_gaps": ["production_capture_missing"],
        "readiness_state": (
            "ready_for_future_explicit_read_only_capture"
            if ready else "blocked_by_observability_or_environment_requirement"
        ),
        "readiness_reasons": (
            ["scheduled_get_no_credentials"]
            if ready else ["production_environment_not_predeclared"]
        ),
        "authorization_state": "explicit_read_only_network_authorization_required",
        "credentials_allowed": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }


def _packet(ready, blocked=()):
    return {
        "schema_version": 1,
        "mode": "deterministic_no_network_capture_readiness_packet",
        "manifest_sha256": "m" * 64,
        "ready_for_future_explicit_read_only_capture": list(ready),
        "blocked_by_observability_or_environment_requirement": list(blocked),
        "authorization_granted": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "missing_evidence_is_negative_demand": False,
    }


def _plan(packet, requests=10, seconds=600):
    return build_capture_session_plan(
        packet,
        start_time_utc="2026-08-20T00:00:00Z",
        total_request_budget=requests,
        total_time_budget_seconds=seconds,
    )


def test_same_host_respects_min_interval_and_chronological_order():
    rows = [_row(index=0), _row(index=1, url="https://api.example.com/two")]
    plan = _plan(_packet(rows))
    assert [s["offset_seconds"] for s in plan["chronological_session_plan"]] == [0.0, 10.0]
    assert [s["sequence"] for s in plan["chronological_session_plan"]] == [1, 2]
    assert plan["host_groups"][0]["request_count"] == 2


def test_window_cap_delays_third_request():
    rows = [
        _row(index=0, min_interval=0, max_requests=2, window=60),
        _row(index=1, url="https://api.example.com/2", min_interval=0, max_requests=2, window=60),
        _row(index=2, url="https://api.example.com/3", min_interval=0, max_requests=2, window=60),
    ]
    plan = _plan(_packet(rows))
    assert [s["offset_seconds"] for s in plan["chronological_session_plan"]] == [0.0, 0.0, 60.0]


def test_different_hosts_can_share_same_slot():
    rows = [
        _row(index=0, url="https://a.example.com/open"),
        _row(index=1, url="https://b.example.com/open"),
    ]
    plan = _plan(_packet(rows))
    assert [s["offset_seconds"] for s in plan["chronological_session_plan"]] == [0.0, 0.0]
    assert [g["host"] for g in plan["host_groups"]] == ["a.example.com", "b.example.com"]


def test_global_request_budget_defers_remaining_ready_items():
    rows = [_row(index=i, url=f"https://h{i}.example.com/open") for i in range(3)]
    plan = _plan(_packet(rows), requests=2)
    assert plan["planned_request_count"] == 2
    assert plan["deferred_ready_count"] == 1
    assert plan["deferred_ready_items"][0]["reason"] == "global_request_budget_exhausted"


def test_time_budget_defers_host_rate_limited_item():
    rows = [
        _row(index=0, min_interval=120),
        _row(index=1, url="https://api.example.com/two", min_interval=120),
    ]
    plan = _plan(_packet(rows), seconds=30)
    assert plan["planned_request_count"] == 1
    assert plan["deferred_ready_items"][0]["reason"] == "global_time_budget_exceeded_by_host_rate_contract"
    assert plan["deferred_ready_items"][0]["earliest_offset_seconds"] == 120.0


def test_blocked_items_are_kept_in_separate_remediation_queue():
    blocked = _row(platform="mcpize", index=8, url="https://mcp.example.com/stats", ready=False)
    blocked["required_environment"] = "unknown"
    plan = _plan(_packet([_row()], [blocked]))
    assert plan["blocked_remediation_count"] == 1
    assert plan["blocked_remediation_queue"][0]["platform"] == "mcpize"
    assert plan["blocked_remediation_queue"][0]["remediation_state"] == "resolve_observability_or_environment_before_capture"
    assert all(step["platform"] != "mcpize" for step in plan["chronological_session_plan"])


def test_non_https_ready_source_fails_closed():
    row = _row(url="http://api.example.com/open")
    with pytest.raises(ValueError, match="capture_session_source_url_invalid"):
        _plan(_packet([row]))


def test_packet_or_item_cannot_self_authorize_action():
    packet = _packet([_row()])
    packet["authorization_granted"] = True
    with pytest.raises(ValueError, match="capture_session_packet_authorization_invalid"):
        _plan(packet)

    packet = _packet([_row()])
    packet["ready_for_future_explicit_read_only_capture"][0]["action_enabled"] = True
    with pytest.raises(ValueError, match="capture_session_action_boundary_invalid"):
        _plan(packet)


def test_deterministic_replay_and_no_network_flags():
    rows = [
        _row(index=0),
        _row(index=1, url="https://other.example.com/open"),
    ]
    packet = _packet(rows)
    first = _plan(packet)
    second = _plan(deepcopy(packet))
    assert first == second
    assert first["authorization_granted"] is False
    assert first["network_calls_performed"] is False
    assert first["credentials_allowed"] is False
    assert first["action_enabled"] is False
    assert all(step["network_calls_performed"] is False for step in first["chronological_session_plan"])
