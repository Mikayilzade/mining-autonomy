from datetime import datetime, timezone
import json

import pytest

from observation_bundle import (
    build_agent2agent_observation_bundle,
    build_payan_observation_bundle,
    build_payan_receipt_envelope,
    load_observation_bundle,
    serialize_observation_bundle,
    verify_observation_bundle,
)

NOW = datetime(2026, 8, 19, 10, 1, tzinfo=timezone.utc)
KEY = b"offline-test-signing-key-32bytes!!"

POLICY = {
    "rights_status": "confirmed",
    "tos_status": "confirmed",
    "automation_allowed": "allowed",
    "source_data_permission": "confirmed",
}
ESTIMATES = {
    "estimated_input_tokens": 1000,
    "estimated_output_tokens": 500,
    "estimated_duration_seconds": 60,
    "estimate_confidence": 0.9,
    "external_cost_cap_usd": 0.10,
}


def request_fixture():
    return {
        "id": "req-1",
        "status": "open",
        "title": "Extract structured fields",
        "description": "Extract invoice number and amount from supplied text.",
        "bountyUsd": 2.0,
        "currency": "USDC",
        "skills": ["extract"],
        "deadlineAt": "2026-08-19T11:00:00Z",
        "metadata": {"tos_status": "allowed", "automation_allowed": "allowed"},
    }


def agent2agent_fixture():
    return {
        "id": "a2a-1",
        "state": "OPEN",
        "title": "Extract structured fields",
        "acceptance_criteria": "Return schema-valid items.",
        "bounty_usd": 3.0,
        "currency": "USDC",
        "skills": ["extract"],
        "deadline": "2026-08-19T11:00:00Z",
        "metadata": {"tos_status": "allowed", "automation_allowed": "allowed"},
    }


def receipts_current():
    return [
        {"id": "rcpt-2a", "amountUsd": 1.0, "currency": "USDC",
         "settledAt": "2026-08-19T09:00:00Z", "buyerAddress": "0xAAA"},
        {"id": "rcpt-2b", "amountUsd": 2.0, "currency": "USDC",
         "settledAt": "2026-08-19T09:30:00Z", "buyerAddress": "0xAAA"},
    ]


def prior_receipt_envelope():
    return build_payan_receipt_envelope(
        [
            {"id": "rcpt-1a", "amountUsd": 0.5, "currency": "USDC",
             "settledAt": "2026-08-19T08:00:00Z", "buyerAddress": "0xBBB"},
            {"id": "rcpt-1b", "amountUsd": 1.0, "currency": "USDC",
             "settledAt": "2026-08-19T08:30:00Z", "buyerAddress": "0xBBB"},
        ],
        source_url="https://payanagent.com/api/v1/receipts",
        source_timestamp="2026-08-19T09:00:00Z",
        captured_at="2026-08-19T09:01:00Z",
    )


def build_fixture_bundle():
    return build_payan_observation_bundle(
        raw_requests=[request_fixture()],
        raw_receipts=receipts_current(),
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        receipt_source_url="https://payanagent.com/api/v1/receipts",
        receipt_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY,
        trusted_policy_by_request_id={"req-1": POLICY},
        trusted_estimates_by_request_id={"req-1": ESTIMATES},
        prior_receipt_envelopes=[prior_receipt_envelope()],
        now=NOW,
    )


def test_bundle_end_to_end_replays_tasks_aggregates_receipts_and_signs():
    bundle = build_fixture_bundle()
    assert verify_observation_bundle(bundle, KEY)
    assert bundle.task_audit["counts"]["accepted"] == 1
    assert bundle.task_audit["action_enabled"] is False
    assert bundle.utilization["transaction_count"] == 2
    assert bundle.utilization["total_value_usd"] == 3.0
    assert bundle.utilization["unique_hashed_buyers"] == 1
    assert bundle.utilization["repeat_hashed_buyers"] == 1
    comparison = bundle.utilization_history["comparisons"][0]
    assert comparison["comparable_window"] is True
    assert comparison["transaction_delta"] == 0
    assert comparison["value_delta_usd"] == 1.5


def test_platform_metadata_cannot_self_authorize_bundle_task():
    bundle = build_payan_observation_bundle(
        raw_requests=[request_fixture()],
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z", signing_key=KEY, now=NOW,
    )
    assert bundle.task_audit["counts"]["accepted"] == 0
    assert "policy_evidence_insufficient" in bundle.task_audit["reason_counts"]


def test_tampered_manifest_breaks_signature_verification():
    bundle = build_fixture_bundle()
    object.__setattr__(bundle, "manifest", {**bundle.manifest, "action_enabled": True})
    assert verify_observation_bundle(bundle, KEY) is False


def test_empty_request_snapshot_is_recorded_without_false_open_demand_claim():
    bundle = build_payan_observation_bundle(
        raw_requests=[],
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z", signing_key=KEY, now=NOW,
    )
    assert bundle.request_envelope["demand_evidence_class"] == "unknown"
    assert bundle.task_audit["counts"] == {"accepted": 0, "held": 0, "rejected": 0}
    assert bundle.task_audit["open_paid_demand_proven_count"] == 0
    assert verify_observation_bundle(bundle, KEY)


def test_receipts_require_explicit_provenance():
    with pytest.raises(ValueError, match="receipt_source_provenance_required"):
        build_payan_observation_bundle(
            raw_requests=[request_fixture()], raw_receipts=receipts_current(),
            request_source_url="https://payanagent.com/api/v1/discover",
            request_source_timestamp="2026-08-19T10:00:00Z",
            captured_at="2026-08-19T10:00:30Z", signing_key=KEY,
            trusted_policy_by_request_id={"req-1": POLICY},
            trusted_estimates_by_request_id={"req-1": ESTIMATES}, now=NOW,
        )


def test_serialization_roundtrip_is_deterministic_and_verified():
    bundle = build_fixture_bundle()
    raw = serialize_observation_bundle(bundle)
    loaded = load_observation_bundle(raw, signing_key=KEY)
    assert loaded == bundle
    assert serialize_observation_bundle(loaded) == raw
    assert verify_observation_bundle(loaded, KEY)


def test_bundle_schema_version_corruption_fails_closed():
    parsed = json.loads(serialize_observation_bundle(build_fixture_bundle()))
    parsed["manifest"]["schema_version"] = 999
    with pytest.raises(ValueError, match="schema_version_unsupported"):
        load_observation_bundle(parsed, signing_key=KEY)


def test_bundle_unknown_top_level_field_fails_closed():
    parsed = json.loads(serialize_observation_bundle(build_fixture_bundle()))
    parsed["unexpected"] = True
    with pytest.raises(ValueError, match="schema_mismatch"):
        load_observation_bundle(parsed, signing_key=KEY)


def test_child_snapshot_tamper_fails_even_if_manifest_and_signature_unchanged():
    parsed = json.loads(serialize_observation_bundle(build_fixture_bundle()))
    parsed["request_envelope"]["snapshot"]["payload"]["items"][0]["title"] = "tampered"
    with pytest.raises(ValueError, match="integrity_verification_failed"):
        load_observation_bundle(parsed, signing_key=KEY)


def test_agent2agent_bundle_reuses_same_fail_closed_evidence_contract():
    bundle = build_agent2agent_observation_bundle(
        raw_tasks=[agent2agent_fixture()],
        source_url="https://api.agent2agent.market/api/tasks/nlp",
        source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY,
        trusted_policy_by_task_id={"a2a-1": POLICY},
        trusted_estimates_by_task_id={"a2a-1": ESTIMATES},
        now=NOW,
    )
    assert bundle.platform == "agent2agent_market"
    assert bundle.task_audit["counts"]["accepted"] == 1
    assert bundle.manifest["dry_run_only"] is True
    assert bundle.manifest["action_enabled"] is False
    assert verify_observation_bundle(bundle, KEY)


def test_agent2agent_payload_metadata_cannot_self_authorize():
    bundle = build_agent2agent_observation_bundle(
        raw_tasks=[agent2agent_fixture()],
        source_url="https://api.agent2agent.market/api/tasks/nlp",
        source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY, now=NOW,
    )
    assert bundle.task_audit["counts"]["accepted"] == 0
    assert "policy_evidence_insufficient" in bundle.task_audit["reason_counts"]
