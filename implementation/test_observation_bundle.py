from datetime import datetime, timezone

import pytest

from observation_bundle import (
    build_payan_observation_bundle,
    build_payan_receipt_envelope,
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
        "metadata": {
            "tos_status": "allowed",
            "automation_allowed": "allowed",
        },
    }


def receipts_current():
    return [
        {
            "id": "rcpt-2a",
            "amountUsd": 1.0,
            "currency": "USDC",
            "settledAt": "2026-08-19T09:00:00Z",
            "buyerAddress": "0xAAA",
        },
        {
            "id": "rcpt-2b",
            "amountUsd": 2.0,
            "currency": "USDC",
            "settledAt": "2026-08-19T09:30:00Z",
            "buyerAddress": "0xAAA",
        },
    ]


def prior_receipt_envelope():
    return build_payan_receipt_envelope(
        [
            {
                "id": "rcpt-1a",
                "amountUsd": 0.5,
                "currency": "USDC",
                "settledAt": "2026-08-19T08:00:00Z",
                "buyerAddress": "0xBBB",
            },
            {
                "id": "rcpt-1b",
                "amountUsd": 1.0,
                "currency": "USDC",
                "settledAt": "2026-08-19T08:30:00Z",
                "buyerAddress": "0xBBB",
            },
        ],
        source_url="https://payanagent.com/api/v1/receipts",
        source_timestamp="2026-08-19T09:00:00Z",
        captured_at="2026-08-19T09:01:00Z",
    )


def test_bundle_end_to_end_replays_tasks_aggregates_receipts_and_signs():
    bundle = build_payan_observation_bundle(
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
    assert bundle.manifest["dry_run_only"] is True
    assert bundle.manifest["action_enabled"] is False


def test_platform_metadata_cannot_self_authorize_bundle_task():
    bundle = build_payan_observation_bundle(
        raw_requests=[request_fixture()],
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY,
        now=NOW,
    )
    assert bundle.task_audit["counts"]["accepted"] == 0
    assert bundle.task_audit["counts"]["rejected"] == 1
    assert "policy_evidence_insufficient" in bundle.task_audit["reason_counts"]


def test_tampered_manifest_breaks_signature_verification():
    bundle = build_payan_observation_bundle(
        raw_requests=[request_fixture()],
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY,
        trusted_policy_by_request_id={"req-1": POLICY},
        trusted_estimates_by_request_id={"req-1": ESTIMATES},
        now=NOW,
    )
    object.__setattr__(bundle, "manifest", {**bundle.manifest, "action_enabled": True})
    assert verify_observation_bundle(bundle, KEY) is False


def test_empty_request_snapshot_is_recorded_without_false_open_demand_claim():
    bundle = build_payan_observation_bundle(
        raw_requests=[],
        request_source_url="https://payanagent.com/api/v1/discover",
        request_source_timestamp="2026-08-19T10:00:00Z",
        captured_at="2026-08-19T10:00:30Z",
        signing_key=KEY,
        now=NOW,
    )
    assert bundle.request_envelope["demand_evidence_class"] == "unknown"
    assert bundle.task_audit["counts"] == {"accepted": 0, "held": 0, "rejected": 0}
    assert bundle.task_audit["open_paid_demand_proven_count"] == 0
    assert verify_observation_bundle(bundle, KEY)


def test_receipts_require_explicit_provenance():
    with pytest.raises(ValueError, match="receipt_source_provenance_required"):
        build_payan_observation_bundle(
            raw_requests=[request_fixture()],
            raw_receipts=receipts_current(),
            request_source_url="https://payanagent.com/api/v1/discover",
            request_source_timestamp="2026-08-19T10:00:00Z",
            captured_at="2026-08-19T10:00:30Z",
            signing_key=KEY,
            trusted_policy_by_request_id={"req-1": POLICY},
            trusted_estimates_by_request_id={"req-1": ESTIMATES},
            now=NOW,
        )
