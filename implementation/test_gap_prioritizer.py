from gap_prioritizer import prioritize_production_gaps
from sampling_receipt import manifest_item_sha256, seal_sampling_manifest


def _manifest():
    manifest = {
        "schema_version": 1,
        "generated_at": "2026-08-20T00:00:00+00:00",
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "scheduled_source_count": 4,
        "source_count": 4,
        "items": [
            {
                "platform": "payanagent",
                "source_url": "https://payanagent.com/api/v1/discover",
                "method": "GET",
                "scheduled": True,
                "expected_evidence_classes": ["open_demand_snapshot"],
                "environment": "production",
                "rate_limit": {
                    "min_interval_seconds": 900.0,
                    "max_requests_per_window": 1,
                    "window_seconds": 900.0,
                },
                "credentials_allowed": False,
                "network_calls_performed": False,
                "action_enabled": False,
            },
            {
                "platform": "mcpize",
                "source_url": "https://mcpize.com/developers",
                "method": "GET",
                "scheduled": True,
                "expected_evidence_classes": ["public_observability_gate"],
                "environment": "production",
                "rate_limit": {
                    "min_interval_seconds": 3600.0,
                    "max_requests_per_window": 1,
                    "window_seconds": 3600.0,
                },
                "credentials_allowed": False,
                "network_calls_performed": False,
                "action_enabled": False,
            },
            {
                "platform": "agent2agent.market",
                "source_url": "https://agent2agent.market/",
                "method": "GET",
                "scheduled": True,
                "expected_evidence_classes": ["open_demand_snapshot", "environment_marker"],
                "environment": "unknown",
                "rate_limit": {
                    "min_interval_seconds": 1800.0,
                    "max_requests_per_window": 1,
                    "window_seconds": 1800.0,
                },
                "credentials_allowed": False,
                "network_calls_performed": False,
                "action_enabled": False,
            },
            {
                "platform": "agentgigs.io",
                "source_url": "https://agentgigs.io/",
                "method": "GET",
                "scheduled": True,
                "expected_evidence_classes": ["open_demand_snapshot"],
                "environment": "production",
                "rate_limit": {
                    "min_interval_seconds": 3600.0,
                    "max_requests_per_window": 1,
                    "window_seconds": 3600.0,
                },
                "credentials_allowed": False,
                "network_calls_performed": False,
                "action_enabled": False,
            },
        ],
    }
    return seal_sampling_manifest(manifest)


def _audit(envelope, rows):
    for row in rows:
        index = row["item_index"]
        row.setdefault("platform", envelope["manifest"]["items"][index]["platform"])
        row.setdefault("source_url", envelope["manifest"]["items"][index]["source_url"])
        row.setdefault("manifest_item_sha256", manifest_item_sha256(envelope, index))
        row.setdefault("replay_freshness_state", None)
    return {
        "schema_version": 1,
        "manifest_sha256": envelope["manifest_sha256"],
        "sources": rows,
        "missing_capture_is_not_zero_demand": True,
        "network_calls_performed": False,
        "action_enabled": False,
    }


def test_primary_platform_and_missing_capture_rank_first():
    envelope = _manifest()
    audit = _audit(envelope, [
        {"item_index": 1, "unresolved_production_gaps": ["production_capture_missing"]},
        {"item_index": 0, "unresolved_production_gaps": ["production_capture_missing"]},
    ])
    report = prioritize_production_gaps(audit, envelope, max_observations=2)
    assert [item["platform"] for item in report["selected_read_only_observations"]] == [
        "payanagent",
        "mcpize",
    ]
    assert report["missing_evidence_is_negative_demand"] is False
    assert all(item["action_enabled"] is False for item in report["selected_read_only_observations"])


def test_stale_capture_is_observation_and_rate_budget_is_exposed():
    envelope = _manifest()
    audit = _audit(envelope, [{
        "item_index": 2,
        "unresolved_production_gaps": ["replay_evidence_stale"],
        "replay_freshness_state": "stale",
    }])
    report = prioritize_production_gaps(audit, envelope)
    item = report["selected_read_only_observations"][0]
    assert item["next_step"] == "read_only_observation"
    assert item["freshness_urgency"] == 80
    assert item["rate_limit"]["max_requests_per_window"] == 1
    assert report["network_calls_performed"] is False


def test_offline_integrity_gap_does_not_consume_observation_budget():
    envelope = _manifest()
    audit = _audit(envelope, [
        {"item_index": 0, "unresolved_production_gaps": ["replay_receipt_provenance_missing"]},
        {"item_index": 3, "unresolved_production_gaps": ["production_capture_missing"]},
    ])
    report = prioritize_production_gaps(audit, envelope, max_observations=1)
    assert report["offline_repair_count"] == 1
    assert report["offline_repairs"][0]["platform"] == "payanagent"
    assert report["selected_read_only_observations"][0]["platform"] == "agentgigs.io"


def test_non_production_receipt_requires_new_read_only_observation():
    envelope = _manifest()
    audit = _audit(envelope, [{
        "item_index": 2,
        "unresolved_production_gaps": ["production_receipt_missing"],
    }])
    report = prioritize_production_gaps(audit, envelope)
    assert report["selected_read_only_observations"][0]["declared_environment"] == "unknown"
    assert report["selected_read_only_observations"][0]["next_step"] == "read_only_observation"


def test_global_observation_cap_defers_lower_ranked_sources():
    envelope = _manifest()
    audit = _audit(envelope, [
        {"item_index": 0, "unresolved_production_gaps": ["production_capture_missing"]},
        {"item_index": 1, "unresolved_production_gaps": ["production_capture_missing"]},
        {"item_index": 3, "unresolved_production_gaps": ["production_capture_missing"]},
    ])
    report = prioritize_production_gaps(audit, envelope, max_observations=2)
    assert report["selected_read_only_observation_count"] == 2
    assert len(report["deferred_read_only_observations"]) == 1


def test_manifest_hash_mismatch_fails_closed():
    envelope = _manifest()
    audit = _audit(envelope, [{
        "item_index": 0,
        "unresolved_production_gaps": ["production_capture_missing"],
    }])
    audit["manifest_sha256"] = "0" * 64
    try:
        prioritize_production_gaps(audit, envelope)
    except ValueError as exc:
        assert str(exc) == "gap_priority_manifest_hash_mismatch"
    else:
        raise AssertionError("expected manifest mismatch")


def test_manifest_item_identity_mismatch_fails_closed():
    envelope = _manifest()
    audit = _audit(envelope, [{
        "item_index": 0,
        "unresolved_production_gaps": ["production_capture_missing"],
        "source_url": "https://example.invalid/",
    }])
    try:
        prioritize_production_gaps(audit, envelope)
    except ValueError as exc:
        assert str(exc) == "gap_priority_manifest_source_mismatch"
    else:
        raise AssertionError("expected source mismatch")


def test_zero_budget_returns_plan_without_network():
    envelope = _manifest()
    audit = _audit(envelope, [{
        "item_index": 0,
        "unresolved_production_gaps": ["production_capture_missing"],
    }])
    report = prioritize_production_gaps(audit, envelope, max_observations=0)
    assert report["selected_read_only_observations"] == []
    assert len(report["deferred_read_only_observations"]) == 1
    assert report["network_calls_performed"] is False
    assert report["action_enabled"] is False
