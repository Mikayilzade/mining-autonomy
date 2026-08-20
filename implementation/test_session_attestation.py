from copy import deepcopy
from hashlib import sha256
import json

import pytest

from session_attestation import build_capture_session_attestation, verify_capture_session_attestation


def _h(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _base():
    steps = []
    envs = []
    rows = []
    captures = []
    report_attestations = []
    for i, ch in enumerate(("a", "b"), 1):
        binding = ch * 64
        manifest_item = str(i) * 64
        step = {
            "sequence": i,
            "platform": "payanagent",
            "source_url": f"https://example.com/{i}",
            "manifest_item_sha256": manifest_item,
            "expected_evidence_classes": ["open_paid_request"],
        }
        env = {**step, "request_binding_sha256": binding}
        receipt_hash = ("c" if i == 1 else "d") * 64
        response_hash = ("e" if i == 1 else "f") * 64
        rows.append({
            "sequence": i,
            "platform": "payanagent",
            "source_url": f"https://example.com/{i}",
            "request_binding_sha256": binding,
            "expected_evidence_classes": ["open_paid_request"],
            "state": "captured",
            "error_code": None,
            "response_receipt_sha256": response_hash,
            "capture_receipt_sha256": receipt_hash,
        })
        capture = {"receipt": {"receipt_sha256": receipt_hash}, "bundle": {"i": i}}
        captures.append(capture)
        report_attestations.append({"receipt": {"receipt_sha256": receipt_hash}, "bundle_sha256": str(i + 2) * 64})
        steps.append(step)
        envs.append(env)

    plan = {
        "schema_version": 1,
        "mode": "deterministic_no_network_capture_session_plan",
        "planned_request_count": 2,
        "chronological_session_plan": steps,
    }
    preflight = {
        "schema_version": 1,
        "mode": "deterministic_read_only_transport_preflight",
        "session_plan_sha256": _h(plan),
        "planned_request_count": 2,
        "transport_envelopes": envs,
    }
    preflight["transport_envelope_set_sha256"] = _h(envs)
    result = {
        "schema_version": 1,
        "mode": "synthetic_capture_session_audit",
        "planned_request_count": 2,
        "supplied_response_count": 2,
        "captured_count": 2,
        "missing_count": 0,
        "rejected_planned_count": 0,
        "rejected_extra_input_count": 0,
        "coverage_complete": True,
        "production_gap_count": 0,
        "planned_request_audit": rows,
        "rejected_response_inputs": [],
        "verified_captures": captures,
        "verified_capture_report": {"capture_attestations": report_attestations},
        "missing_means_zero_demand": False,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return plan, preflight, result


def test_build_and_verify_attestation_is_deterministic():
    plan, preflight, result = _base()
    first = build_capture_session_attestation(plan, preflight, result)
    second = build_capture_session_attestation(deepcopy(plan), deepcopy(preflight), deepcopy(result))
    assert first == second
    assert len(first["attestation_sha256"]) == 64
    assert first["coverage"]["coverage_complete"] is True
    assert verify_capture_session_attestation(plan, preflight, result, first) == first


def test_plan_drift_fails_closed_against_preflight_hash():
    plan, preflight, result = _base()
    plan["chronological_session_plan"][0]["source_url"] = "https://example.net/drift"
    with pytest.raises(ValueError, match="capture_attestation_session_plan_hash_mismatch"):
        build_capture_session_attestation(plan, preflight, result)


def test_transport_envelope_set_tamper_fails_closed():
    plan, preflight, result = _base()
    preflight["transport_envelopes"][0]["platform"] = "tampered"
    with pytest.raises(ValueError, match="capture_attestation_envelope_set_hash_mismatch"):
        build_capture_session_attestation(plan, preflight, result)


def test_audit_row_mutation_is_detected():
    plan, preflight, result = _base()
    result["planned_request_audit"][0]["source_url"] = "https://example.com/changed"
    with pytest.raises(ValueError, match="capture_attestation_audit_source_url_mismatch"):
        build_capture_session_attestation(plan, preflight, result)


def test_successful_capture_must_match_verified_report_membership():
    plan, preflight, result = _base()
    result["verified_capture_report"]["capture_attestations"][0]["receipt"]["receipt_sha256"] = "9" * 64
    with pytest.raises(ValueError, match="capture_attestation_capture_report_mismatch"):
        build_capture_session_attestation(plan, preflight, result)


def test_production_gap_count_cannot_be_manipulated():
    plan, preflight, result = _base()
    row = result["planned_request_audit"][1]
    row.update({
        "state": "missing",
        "error_code": "session_missing_scheduled_response",
        "response_receipt_sha256": None,
        "capture_receipt_sha256": None,
    })
    result["captured_count"] = 1
    result["missing_count"] = 1
    result["coverage_complete"] = False
    result["verified_captures"] = result["verified_captures"][:1]
    result["verified_capture_report"]["capture_attestations"] = result["verified_capture_report"]["capture_attestations"][:1]
    result["production_gap_count"] = 0
    with pytest.raises(ValueError, match="capture_attestation_production_gap_count_mismatch"):
        build_capture_session_attestation(plan, preflight, result)


def test_missing_row_produces_exact_gap_attestation():
    plan, preflight, result = _base()
    row = result["planned_request_audit"][1]
    row.update({
        "state": "missing",
        "error_code": "session_missing_scheduled_response",
        "response_receipt_sha256": None,
        "capture_receipt_sha256": None,
    })
    result["captured_count"] = 1
    result["missing_count"] = 1
    result["coverage_complete"] = False
    result["production_gap_count"] = 1
    result["verified_captures"] = result["verified_captures"][:1]
    result["verified_capture_report"]["capture_attestations"] = result["verified_capture_report"]["capture_attestations"][:1]
    attestation = build_capture_session_attestation(plan, preflight, result)
    assert attestation["coverage"]["production_gap_count"] == 1
    assert attestation["coverage"]["missing_means_zero_demand"] is False
