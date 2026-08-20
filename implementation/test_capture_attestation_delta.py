from copy import deepcopy
from hashlib import sha256
import json
import pytest

from capture_attestation_delta import compare_capture_session_attestations


def _h(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _att(states=("captured", "missing"), plan="1" * 64, env="2" * 64, receipt1="c" * 64, receipt2="d" * 64):
    bindings = ["a" * 64, "b" * 64]
    rows = []
    receipts = []
    for i, (binding, state, receipt) in enumerate(zip(bindings, states, (receipt1, receipt2)), 1):
        row = {
            "sequence": i,
            "platform": "payanagent",
            "source_url": f"https://example.com/{i}",
            "request_binding_sha256": binding,
            "expected_evidence_classes": ["open_paid_request"],
            "state": state,
        }
        if state == "captured":
            row.update(error_code=None, response_receipt_sha256=("e" if i == 1 else "f") * 64, capture_receipt_sha256=receipt)
            receipts.append(receipt)
        elif state == "missing":
            row.update(error_code="session_missing_scheduled_response", response_receipt_sha256=None, capture_receipt_sha256=None)
        else:
            row.update(error_code="synthetic_rejected", response_receipt_sha256="7" * 64, capture_receipt_sha256=None)
        rows.append(row)
    coverage = {
        "planned_request_count": 2,
        "captured_count": sum(s == "captured" for s in states),
        "missing_count": sum(s == "missing" for s in states),
        "rejected_planned_count": sum(s == "rejected" for s in states),
        "rejected_extra_input_count": 0,
        "production_gap_count": sum(s != "captured" for s in states),
        "coverage_complete": all(s == "captured" for s in states),
        "planned_request_audit": rows,
        "rejected_response_inputs_sha256": "8" * 64,
        "verified_capture_receipt_sha256s": sorted(receipts),
        "capture_report_receipt_sha256s": sorted(receipts),
        "missing_means_zero_demand": False,
    }
    core = {
        "schema_version": 1,
        "mode": "capture_session_replay_coverage_attestation",
        "session_plan_sha256": plan,
        "transport_envelope_set_sha256": env,
        "preflight_sha256": "3" * 64,
        "planned_request_binding_sha256s": bindings,
        "coverage": coverage,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "coverage_sha256": _h(coverage), "attestation_sha256": _h(core)}


def test_identical_attestations_have_zero_delta():
    a = _att()
    delta = compare_capture_session_attestations(a, deepcopy(a))
    assert delta["coverage_delta"] == {"captured_count": 0, "missing_count": 0, "rejected_planned_count": 0, "production_gap_count": 0}
    assert delta["request_state_changes"] == []
    assert delta["verified_capture_receipts_added"] == []
    assert delta["missing_evidence_semantics"] == "unknown_not_negative_demand"


def test_missing_to_captured_is_explicit_and_closes_gap():
    delta = compare_capture_session_attestations(_att(("captured", "missing")), _att(("captured", "captured")))
    assert delta["coverage_delta"]["captured_count"] == 1
    assert delta["coverage_delta"]["missing_count"] == -1
    assert delta["coverage_delta"]["production_gap_count"] == -1
    assert delta["request_state_changes"][0]["from_state"] == "missing"
    assert delta["request_state_changes"][0]["to_state"] == "captured"
    assert delta["coverage_complete_transition"] == {"from": False, "to": True}


def test_captured_to_missing_does_not_mean_negative_demand():
    delta = compare_capture_session_attestations(_att(("captured", "captured")), _att(("captured", "missing")))
    assert delta["coverage_delta"]["production_gap_count"] == 1
    assert delta["missing_evidence_semantics"] == "unknown_not_negative_demand"


def test_receipt_change_is_reported_even_when_state_stays_captured():
    delta = compare_capture_session_attestations(_att(("captured", "captured"), receipt2="d" * 64), _att(("captured", "captured"), receipt2="9" * 64))
    assert delta["request_state_changes"][0]["from_state"] == "captured"
    assert delta["request_state_changes"][0]["to_state"] == "captured"
    assert delta["request_state_changes"][0]["capture_receipt_changed"] is True
    assert delta["verified_capture_receipts_added"] == ["9" * 64]
    assert delta["verified_capture_receipts_removed"] == ["d" * 64]


def test_cross_plan_fails_closed():
    with pytest.raises(ValueError, match="capture_delta_cross_plan_comparison"):
        compare_capture_session_attestations(_att(), _att(plan="4" * 64))


def test_cross_envelope_set_fails_closed():
    with pytest.raises(ValueError, match="capture_delta_cross_envelope_set_comparison"):
        compare_capture_session_attestations(_att(), _att(env="5" * 64))


def test_tampered_attestation_hash_fails_closed():
    target = _att()
    target["coverage"]["missing_count"] = 99
    with pytest.raises(ValueError, match="coverage_hash_mismatch"):
        compare_capture_session_attestations(_att(), target)


def test_rehashed_counter_tamper_still_fails_internal_replay():
    target = _att()
    target["coverage"]["missing_count"] = 99
    target["coverage_sha256"] = _h(target["coverage"])
    core = {key: target[key] for key in ("schema_version", "mode", "session_plan_sha256", "transport_envelope_set_sha256", "preflight_sha256", "planned_request_binding_sha256s", "coverage", "dry_run_only", "action_enabled", "network_calls_performed", "credentials_used")}
    target["attestation_sha256"] = _h(core)
    with pytest.raises(ValueError, match="missing_count_mismatch"):
        compare_capture_session_attestations(_att(), target)
