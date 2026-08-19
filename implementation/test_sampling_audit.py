import copy

from sampling_audit import sampling_audit_summary
from sampling_receipt import TransportResult, bind_capture_result, seal_sampling_manifest


def _manifest():
    items = []
    for index, environment in enumerate(("production", "production", "testnet", "production")):
        items.append({
            "platform": f"platform-{index}",
            "source_url": f"https://example.test/{index}",
            "method": "GET",
            "scheduled": True,
            "expected_evidence_classes": ["open_demand_snapshot"],
            "environment": environment,
            "credentials_allowed": False,
            "network_calls_performed": False,
            "action_enabled": False,
        })
    return seal_sampling_manifest({
        "schema_version": 1,
        "generated_at": "2026-08-19T12:00:00+00:00",
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "scheduled_source_count": 4,
        "source_count": 4,
        "items": items,
    })


def _receipt(envelope, index, *, environment):
    return bind_capture_result(
        envelope,
        item_index=index,
        result=TransportResult(
            sanitized_bundle_sha256=str(index + 1) * 64,
            capture_started_at="2026-08-19T12:01:00+00:00",
            capture_finished_at="2026-08-19T12:01:01+00:00",
            captured_environment=environment,
            source_timestamp="2026-08-19T12:00:30+00:00",
        ),
        transport_name="fixture",
        transport_network_capable=False,
    )


def test_sampling_audit_distinguishes_all_required_states():
    envelope = _manifest()
    invalid = _receipt(envelope, 1, environment="production")
    invalid["captured_environment"] = "testnet"
    receipts = [
        invalid,
        _receipt(envelope, 2, environment="testnet"),
        _receipt(envelope, 3, environment="production"),
    ]
    report = sampling_audit_summary(envelope, receipts)
    assert report["scheduled_but_uncaptured_count"] == 1
    assert report["receipt_invalid_count"] == 1
    assert report["receipt_valid_non_production_count"] == 1
    assert report["receipt_valid_production_count"] == 1
    assert report["non_production_can_close_production_gap"] is False
    assert report["action_enabled"] is False
    states = {row["item_index"]: row["state"] for row in report["items"]}
    assert states == {
        0: "scheduled_but_uncaptured",
        1: "receipt_invalid",
        2: "receipt_valid_non_production",
        3: "receipt_valid_production",
    }


def test_duplicate_receipts_fail_closed_for_scheduled_item():
    envelope = _manifest()
    receipt = _receipt(envelope, 0, environment="production")
    report = sampling_audit_summary(envelope, [receipt, copy.deepcopy(receipt)])
    row = next(item for item in report["items"] if item["item_index"] == 0)
    assert row["state"] == "receipt_invalid"
    assert row["reason"] == "multiple_receipts_for_manifest_item"


def test_unmatched_receipt_does_not_close_any_gap():
    envelope = _manifest()
    malformed = {"item_index": -1, "receipt_sha256": "a" * 64}
    report = sampling_audit_summary(envelope, [malformed])
    assert report["unexpected_or_unmatched_receipt_count"] == 1
    assert report["scheduled_but_uncaptured_count"] == 4
