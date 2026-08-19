from datetime import datetime, timezone
import hashlib

import pytest

from payan_sanitizer import sanitize_payan_receipt, sanitize_payan_request


POLICY = {
    "rights_status": "confirmed",
    "tos_status": "allowed",
    "automation_allowed": "allowed",
    "source_data_permission": "confirmed",
}
ESTIMATES = {
    "estimated_input_tokens": 1000,
    "estimated_output_tokens": 500,
    "estimated_duration_seconds": 60,
    "estimate_confidence": 0.8,
    "external_cost_cap_usd": 0.0,
}


def test_request_sanitizer_normalizes_and_uses_only_trusted_policy():
    raw = {
        "requestId": "req-1",
        "title": "Summarize a document",
        "budgetUsd": "2.50",
        "currency": "USDC",
        "skills": ["Summarize"],
        "status": "open",
        "metadata": {"tos_status": "allowed", "automation_allowed": "allowed"},
    }
    out = sanitize_payan_request(raw, trusted_policy=POLICY, trusted_estimates=ESTIMATES)
    assert out["id"] == "req-1"
    assert out["bounty_usd"] == 2.5
    assert out["skills"] == ["summarize"]
    assert out["metadata"]["tos_status"] == "allowed"
    assert out["metadata"]["estimate_confidence"] == 0.8


def test_request_platform_metadata_cannot_self_authorize_policy():
    out = sanitize_payan_request({
        "id": "req-2", "description": "Extract fields", "bounty_usd": 1,
        "metadata": {"tos_status": "allowed", "automation_allowed": "allowed"},
    })
    assert out["metadata"]["tos_status"] == "unknown"
    assert out["metadata"]["automation_allowed"] == "unknown"


def test_request_rejects_closed_or_conflicting_aliases():
    with pytest.raises(ValueError, match="request_not_open"):
        sanitize_payan_request({"id": "x", "description": "x", "bounty_usd": 1, "status": "closed"})
    with pytest.raises(ValueError, match="conflicting_request_id_required"):
        sanitize_payan_request({"id": "x", "requestId": "y", "description": "x", "bounty_usd": 1})


def test_receipt_hashes_identity_and_drops_raw_fields():
    raw = {
        "receiptId": "r-1",
        "amountCents": 125,
        "settledAt": "2026-08-19T08:00:00Z",
        "buyerAddress": "0xAbCDEF",
        "currency": "USDC",
    }
    out = sanitize_payan_receipt(raw)
    assert out["amount_usd"] == 1.25
    assert out["occurred_at"].endswith("+00:00")
    assert out["buyer_hash"] == hashlib.sha256(b"0xabcdef").hexdigest()
    assert not any(k in out for k in ("buyerAddress", "buyer", "wallet", "payer"))


def test_receipt_rejects_ambiguous_amount_and_naive_time():
    with pytest.raises(ValueError, match="exactly_one_receipt_amount_representation_required"):
        sanitize_payan_receipt({
            "id": "r", "amountUsd": 1, "amountCents": 100,
            "settledAt": "2026-08-19T08:00:00Z",
        })
    with pytest.raises(ValueError, match="timestamp_must_be_timezone_aware"):
        sanitize_payan_receipt({"id": "r", "amountUsd": 1, "settledAt": "2026-08-19T08:00:00"})
