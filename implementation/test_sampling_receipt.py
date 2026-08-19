import copy
import pytest

from sampling_receipt import (
    InjectedTransport,
    TransportResult,
    capture_with_injected_transport,
    manifest_item_sha256,
    seal_sampling_manifest,
    verify_capture_receipt,
    verify_sampling_manifest_envelope,
)


def _manifest(environment="production", scheduled=True):
    return {
        "schema_version": 1,
        "generated_at": "2026-08-19T17:00:00+00:00",
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "scheduled_source_count": 1 if scheduled else 0,
        "source_count": 1,
        "items": [{
            "platform": "payanagent",
            "source_url": "https://payanagent.com/api/v1/discover",
            "method": "GET",
            "scheduled": scheduled,
            "plan_score": 100,
            "planner_reasons": ["missing_production_evidence"],
            "expected_evidence_classes": ["open_demand_snapshot"],
            "environment": environment,
            "capture_deadline": "2026-08-19T19:00:00+00:00",
            "max_source_age_hours": 6.0,
            "rate_limit": {"min_interval_seconds": 900.0, "max_requests_per_window": 1, "window_seconds": 900.0, "budget_basis": "project_conservative_self_limit"},
            "provenance_requirements": ["record_exact_source_url"],
            "credentials_allowed": False,
            "network_calls_performed": False,
            "action_enabled": False,
        }],
        "capture_bridge": {"execution_authorization_from_evidence": False},
    }


def _result(**overrides):
    data = dict(
        sanitized_bundle_sha256="a" * 64,
        capture_started_at="2026-08-19T17:01:00+00:00",
        capture_finished_at="2026-08-19T17:01:01+00:00",
        captured_environment="production",
        network_performed=False,
    )
    data.update(overrides)
    return TransportResult(**data)


def test_seal_is_deterministic_and_hmac_verifies():
    one = seal_sampling_manifest(_manifest(), signing_key=b"secret", key_id="local-test")
    two = seal_sampling_manifest(_manifest(), signing_key=b"secret", key_id="local-test")
    assert one == two
    assert verify_sampling_manifest_envelope(one, signing_key=b"secret", require_signature=True)


def test_manifest_mutation_breaks_hash_and_signature():
    envelope = seal_sampling_manifest(_manifest(), signing_key=b"secret", key_id="local-test")
    tampered = copy.deepcopy(envelope)
    tampered["manifest"]["items"][0]["source_url"] = "https://payanagent.com/other"
    with pytest.raises(ValueError, match="sealed_manifest_hash_mismatch"):
        verify_sampling_manifest_envelope(tampered, signing_key=b"secret", require_signature=True)


def test_item_hash_is_bound_to_manifest_and_index():
    first = seal_sampling_manifest(_manifest())
    changed = _manifest()
    changed["generated_at"] = "2026-08-19T17:05:00+00:00"
    second = seal_sampling_manifest(changed)
    assert manifest_item_sha256(first, 0) != manifest_item_sha256(second, 0)


def test_missing_transport_and_network_capable_transport_fail_closed():
    envelope = seal_sampling_manifest(_manifest())
    with pytest.raises(RuntimeError, match="capture_transport_not_injected"):
        capture_with_injected_transport(envelope, item_index=0)
    network_transport = InjectedTransport("network", lambda item: _result(network_performed=True), network_capable=True)
    with pytest.raises(RuntimeError, match="capture_network_transport_disabled"):
        capture_with_injected_transport(envelope, item_index=0, transport=network_transport)


def test_mock_transport_creates_verifiable_receipt_without_authority():
    envelope = seal_sampling_manifest(_manifest())
    transport = InjectedTransport("fixture", lambda item: _result(), network_capable=False)
    receipt = capture_with_injected_transport(envelope, item_index=0, transport=transport)
    assert receipt["manifest_sha256"] == envelope["manifest_sha256"]
    assert receipt["manifest_item_sha256"] == manifest_item_sha256(envelope, 0)
    assert receipt["transport"]["network_performed"] is False
    assert receipt["execution_authority_granted"] is False
    assert verify_capture_receipt(envelope, receipt)


def test_receipt_tampering_is_detected():
    envelope = seal_sampling_manifest(_manifest())
    receipt = capture_with_injected_transport(envelope, item_index=0, transport=InjectedTransport("fixture", lambda item: _result()))
    receipt["source_url"] = "https://example.com/"
    with pytest.raises(ValueError, match="capture_receipt_source_url_mismatch"):
        verify_capture_receipt(envelope, receipt)


def test_unknown_to_production_requires_environment_evidence():
    envelope = seal_sampling_manifest(_manifest(environment="unknown"))
    transport = InjectedTransport("fixture", lambda item: _result(captured_environment="production"))
    with pytest.raises(ValueError, match="capture_production_promotion_requires_evidence"):
        capture_with_injected_transport(envelope, item_index=0, transport=transport)

    transport2 = InjectedTransport("fixture", lambda item: _result(
        captured_environment="production",
        environment_evidence_sha256="b" * 64,
    ))
    receipt = capture_with_injected_transport(envelope, item_index=0, transport=transport2)
    assert receipt["captured_environment"] == "production"
    assert receipt["environment_evidence_sha256"] == "b" * 64


def test_credentials_actions_and_unscheduled_items_are_rejected():
    envelope = seal_sampling_manifest(_manifest())
    with pytest.raises(ValueError, match="capture_credentials_forbidden"):
        capture_with_injected_transport(envelope, item_index=0, transport=InjectedTransport("fixture", lambda item: _result(credentials_used=True)))
    with pytest.raises(ValueError, match="capture_action_forbidden"):
        capture_with_injected_transport(envelope, item_index=0, transport=InjectedTransport("fixture", lambda item: _result(action_performed=True)))
    unscheduled = seal_sampling_manifest(_manifest(scheduled=False))
    with pytest.raises(ValueError, match="capture_manifest_item_not_scheduled"):
        capture_with_injected_transport(unscheduled, item_index=0, transport=InjectedTransport("fixture", lambda item: _result()))
