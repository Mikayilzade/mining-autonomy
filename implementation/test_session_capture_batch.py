from dataclasses import replace

import pytest

import session_capture_batch as scb
from session_capture_batch import SyntheticResponseInput, run_synthetic_capture_session


def _request(binding: str, sequence: int):
    return {
        "sequence": sequence,
        "platform": "payanagent",
        "source_url": f"https://example.com/{sequence}",
        "request_binding_sha256": binding,
        "expected_evidence_classes": ["open_paid_request"],
    }


def _response(receipt_hash: str, binding: str):
    return {
        "response_receipt_sha256": receipt_hash,
        "request_binding_sha256": binding,
    }


def _input(receipt_hash: str):
    return SyntheticResponseInput(
        response_receipt_sha256=receipt_hash,
        response_body=b"{}",
        source_timestamp_utc="2026-08-20T03:00:00+00:00",
        capture_started_at_utc="2026-08-20T03:00:01+00:00",
        capture_finished_at_utc="2026-08-20T03:00:02+00:00",
        payload_builder=lambda parsed, context: None,
    )


def _base():
    preflight = {
        "planned_request_count": 2,
        "transport_envelopes": [_request("a" * 64, 1), _request("b" * 64, 2)],
    }
    execution = {
        "response_receipts": [_response("1" * 64, "a" * 64), _response("2" * 64, "b" * 64)],
    }
    return preflight, execution, {"manifest": "synthetic"}


def _install_success(monkeypatch):
    def fake_bridge(preflight, execution, manifest, **kwargs):
        receipt_hash = kwargs["response_receipt_sha256"]
        return {
            "receipt": {"receipt_sha256": "c" + receipt_hash[1:]},
            "bundle": {"response": receipt_hash},
        }

    monkeypatch.setattr(scb, "bridge_response_to_verified_capture", fake_bridge)
    monkeypatch.setattr(scb, "run_verified_capture_batch", lambda captures: {"count": len(captures)})


def test_complete_session_captures_every_planned_request(monkeypatch):
    preflight, execution, manifest = _base()
    _install_success(monkeypatch)
    result = run_synthetic_capture_session(
        preflight, execution, manifest, [_input("1" * 64), _input("2" * 64)]
    )
    assert result["coverage_complete"] is True
    assert result["captured_count"] == 2
    assert result["production_gap_count"] == 0
    assert result["verified_capture_report"] == {"count": 2}
    assert all(item["state"] == "captured" for item in result["planned_request_audit"])


def test_missing_response_remains_explicit_gap(monkeypatch):
    preflight, execution, manifest = _base()
    _install_success(monkeypatch)
    result = run_synthetic_capture_session(preflight, execution, manifest, [_input("1" * 64)])
    assert result["coverage_complete"] is False
    assert result["missing_count"] == 1
    assert result["production_gap_count"] == 1
    missing = [item for item in result["planned_request_audit"] if item["state"] == "missing"]
    assert missing[0]["error_code"] == "session_missing_scheduled_response"
    assert result["missing_means_zero_demand"] is False


def test_duplicate_supplied_receipt_is_rejected_and_request_becomes_missing(monkeypatch):
    preflight, execution, manifest = _base()
    _install_success(monkeypatch)
    duplicate = _input("1" * 64)
    result = run_synthetic_capture_session(preflight, execution, manifest, [duplicate, duplicate, _input("2" * 64)])
    assert result["rejected_extra_input_count"] == 2
    assert all(item["error_code"] == "session_duplicate_response_receipt_input" for item in result["rejected_response_inputs"][:2])
    assert result["captured_count"] == 1
    assert result["missing_count"] == 1


def test_duplicate_execution_receipt_hash_fails_closed_for_that_input(monkeypatch):
    preflight, execution, manifest = _base()
    execution["response_receipts"].append(_response("1" * 64, "a" * 64))
    _install_success(monkeypatch)
    result = run_synthetic_capture_session(preflight, execution, manifest, [_input("1" * 64), _input("2" * 64)])
    assert result["captured_count"] == 1
    assert result["missing_count"] == 1
    assert result["rejected_response_inputs"][0]["error_code"] == "session_duplicate_response_receipt_execution"


def test_extra_response_not_in_planned_session_is_rejected(monkeypatch):
    preflight, execution, manifest = _base()
    execution["response_receipts"].append(_response("3" * 64, "d" * 64))
    _install_success(monkeypatch)
    result = run_synthetic_capture_session(preflight, execution, manifest, [_input("1" * 64), _input("2" * 64), _input("3" * 64)])
    assert result["captured_count"] == 2
    assert result["rejected_extra_input_count"] == 1
    assert result["rejected_response_inputs"][0]["error_code"] == "session_response_not_in_planned_session"


def test_bridge_failure_isolated_and_not_fed_to_capture_report(monkeypatch):
    preflight, execution, manifest = _base()

    def fake_bridge(preflight, execution, manifest, **kwargs):
        if kwargs["response_receipt_sha256"] == "1" * 64:
            raise ValueError("bridge_json_invalid")
        return {"receipt": {"receipt_sha256": "c" * 64}, "bundle": {}}

    seen = {}
    monkeypatch.setattr(scb, "bridge_response_to_verified_capture", fake_bridge)
    monkeypatch.setattr(scb, "run_verified_capture_batch", lambda captures: seen.setdefault("count", len(captures)) or {})
    result = run_synthetic_capture_session(preflight, execution, manifest, [_input("1" * 64), _input("2" * 64)])
    assert result["captured_count"] == 1
    assert result["rejected_planned_count"] == 1
    assert seen["count"] == 1
    failed = [item for item in result["planned_request_audit"] if item["state"] == "rejected"]
    assert failed[0]["error_code"] == "bridge_json_invalid"


def test_duplicate_responses_for_same_request_binding_reject_request(monkeypatch):
    preflight, execution, manifest = _base()
    execution["response_receipts"].append(_response("3" * 64, "a" * 64))
    _install_success(monkeypatch)
    result = run_synthetic_capture_session(preflight, execution, manifest, [_input("1" * 64), _input("3" * 64), _input("2" * 64)])
    first = result["planned_request_audit"][0]
    assert first["state"] == "rejected"
    assert first["error_code"] == "session_duplicate_response_for_request"
    assert result["captured_count"] == 1


def test_preflight_declared_count_mismatch_fails_before_processing():
    preflight, execution, manifest = _base()
    preflight["planned_request_count"] = 3
    with pytest.raises(ValueError, match="session_planned_request_count_mismatch"):
        run_synthetic_capture_session(preflight, execution, manifest, [])
