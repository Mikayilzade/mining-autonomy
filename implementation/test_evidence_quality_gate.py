from hashlib import sha256
import json

import pytest

from evidence_quality_gate import evaluate_longitudinal_capture_integrity


def _hash(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def make_history(rows, transitions=None):
    timeline = []
    for observed_at, captured, missing, rejected, gaps, complete in rows:
        timeline.append({
            "observed_at": observed_at,
            "attestation_sha256": _hash([observed_at, captured, missing, rejected, gaps]),
            "coverage_complete": complete,
            "captured_count": captured,
            "missing_count": missing,
            "rejected_planned_count": rejected,
            "production_gap_count": gaps,
        })
    first, last = timeline[0], timeline[-1]
    core = {
        "schema_version": 1,
        "mode": "capture_session_attestation_history",
        "session_plan_sha256": "1" * 64,
        "transport_envelope_set_sha256": "2" * 64,
        "planned_request_binding_sha256s": ["3" * 64],
        "observation_count": len(timeline),
        "first_observed_at": first["observed_at"],
        "last_observed_at": last["observed_at"],
        "attestation_sha256s": [row["attestation_sha256"] for row in timeline],
        "adjacent_delta_refs": [],
        "coverage_timeline": timeline,
        "transition_frequencies": transitions or {},
        "coverage_evolution": {
            "captured_count_change": last["captured_count"] - first["captured_count"],
            "missing_count_change": last["missing_count"] - first["missing_count"],
            "rejected_planned_count_change": last["rejected_planned_count"] - first["rejected_planned_count"],
            "production_gap_count_change": last["production_gap_count"] - first["production_gap_count"],
            "coverage_complete_observation_count": sum(1 for row in timeline if row["coverage_complete"]),
        },
        "demand_interpretation": "none_missing_or_failed_capture_is_not_negative_demand_evidence",
        "aggregation_scope": "evidence_integrity_and_coverage_only_no_demand_extrapolation",
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "history_sha256": _hash(core)}


def test_insufficient_history_recommends_repeat_only_after_authorization():
    history = make_history([
        ("2026-08-20T06:00:00Z", 1, 1, 0, 1, False),
        ("2026-08-20T06:30:00Z", 1, 1, 0, 1, False),
    ])
    result = evaluate_longitudinal_capture_integrity(history)
    assert result["capture_integrity_label"] == "insufficient_history"
    assert result["future_read_only_capture_worth_repeating_for_integrity"] is True
    assert result["authorization_required"] is True
    assert result["action_enabled"] is False


def test_improving_history():
    history = make_history([
        ("2026-08-20T06:00:00Z", 1, 2, 0, 2, False),
        ("2026-08-20T07:00:00Z", 2, 1, 0, 1, False),
        ("2026-08-20T08:00:00Z", 3, 0, 0, 0, True),
    ], {"missing->captured": 2})
    result = evaluate_longitudinal_capture_integrity(history)
    assert result["capture_integrity_label"] == "improving"
    assert result["unresolved_capture_gap"] is False
    assert result["future_read_only_capture_worth_repeating_for_integrity"] is False


def test_regressing_history_recommends_diagnostic_repeat():
    history = make_history([
        ("2026-08-20T06:00:00Z", 3, 0, 0, 0, True),
        ("2026-08-20T07:00:00Z", 2, 1, 0, 1, False),
        ("2026-08-20T08:00:00Z", 1, 2, 0, 2, False),
    ], {"captured->missing": 2})
    result = evaluate_longitudinal_capture_integrity(history)
    assert result["capture_integrity_label"] == "regressing"
    assert result["future_read_only_capture_worth_repeating_for_integrity"] is True
    assert result["recommendation_reason"] == "capture_integrity_regressing"


def test_stable_complete_history_does_not_request_integrity_repeat():
    history = make_history([
        ("2026-08-20T06:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T07:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T08:00:00Z", 2, 0, 0, 0, True),
    ])
    result = evaluate_longitudinal_capture_integrity(history)
    assert result["capture_integrity_label"] == "stable"
    assert result["future_read_only_capture_worth_repeating_for_integrity"] is False


def test_stable_but_incomplete_history_recommends_gap_repeat():
    history = make_history([
        ("2026-08-20T06:00:00Z", 1, 1, 0, 1, False),
        ("2026-08-20T07:00:00Z", 1, 1, 0, 1, False),
        ("2026-08-20T08:00:00Z", 1, 1, 0, 1, False),
    ])
    result = evaluate_longitudinal_capture_integrity(history)
    assert result["capture_integrity_label"] == "stable"
    assert result["unresolved_capture_gap"] is True
    assert result["future_read_only_capture_worth_repeating_for_integrity"] is True


def test_tampered_history_hash_fails_closed():
    history = make_history([
        ("2026-08-20T06:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T07:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T08:00:00Z", 2, 0, 0, 0, True),
    ])
    history["coverage_timeline"][0]["missing_count"] = 9
    with pytest.raises(ValueError, match="quality_history_hash_mismatch"):
        evaluate_longitudinal_capture_integrity(history)


def test_rehashed_inconsistent_evolution_fails_closed():
    history = make_history([
        ("2026-08-20T06:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T07:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T08:00:00Z", 2, 0, 0, 0, True),
    ])
    history["coverage_evolution"]["missing_count_change"] = 1
    core = dict(history)
    core.pop("history_sha256")
    history["history_sha256"] = _hash(core)
    with pytest.raises(ValueError, match="quality_coverage_evolution_mismatch"):
        evaluate_longitudinal_capture_integrity(history)


def test_noncanonical_timeline_fails_even_when_rehashed():
    history = make_history([
        ("2026-08-20T06:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T07:00:00Z", 2, 0, 0, 0, True),
        ("2026-08-20T08:00:00Z", 2, 0, 0, 0, True),
    ])
    history["coverage_timeline"][1]["observed_at"] = "2026-08-20T07:00:00+00:00"
    core = dict(history)
    core.pop("history_sha256")
    history["history_sha256"] = _hash(core)
    with pytest.raises(ValueError, match="not_canonical"):
        evaluate_longitudinal_capture_integrity(history)
