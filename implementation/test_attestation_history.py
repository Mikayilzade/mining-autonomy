from copy import deepcopy

import pytest

import attestation_history as history


def _replay(name, states=("captured", "missing"), plan="a" * 64, env="b" * 64):
    bindings = ["1" * 64, "2" * 64]
    rows = {}
    captured = []
    counts = {"captured": 0, "missing": 0, "rejected": 0}
    for idx, (binding, state) in enumerate(zip(bindings, states), start=1):
        counts[state] += 1
        capture = (str(idx + 2) * 64)[:64] if state == "captured" else None
        if capture:
            captured.append(capture)
        rows[binding] = {
            "sequence": idx,
            "platform": "payanagent",
            "source_url": f"https://example.test/{idx}",
            "request_binding_sha256": binding,
            "expected_evidence_classes": ["open_task_count"],
            "state": state,
            "error_code": None if state == "captured" else ("session_missing_scheduled_response" if state == "missing" else "synthetic_rejected"),
            "response_receipt_sha256": (str(idx + 4) * 64)[:64] if state != "missing" else None,
            "capture_receipt_sha256": capture,
        }
    return {
        "plan_hash": plan,
        "envelope_hash": env,
        "attestation_hash": name * 64,
        "bindings": bindings,
        "rows": rows,
        "coverage": {
            "planned_request_count": 2,
            "captured_count": counts["captured"],
            "missing_count": counts["missing"],
            "rejected_planned_count": counts["rejected"],
            "production_gap_count": counts["missing"] + counts["rejected"],
            "coverage_complete": counts["captured"] == 2,
        },
        "verified_receipts": sorted(captured),
    }


def _delta(left, right):
    changes = []
    for binding in left["bindings"]:
        before, after = left["rows"][binding], right["rows"][binding]
        if before != after:
            changes.append({
                "from_state": before["state"],
                "to_state": after["state"],
            })
    return {
        "schema_version": 1,
        "mode": "capture_session_attestation_delta",
        "session_plan_sha256": left["plan_hash"],
        "transport_envelope_set_sha256": left["envelope_hash"],
        "baseline_attestation_sha256": left["attestation_hash"],
        "target_attestation_sha256": right["attestation_hash"],
        "request_state_changes": changes,
        "delta_sha256": (left["attestation_hash"][0] + right["attestation_hash"][0]) * 32,
    }


def _install(monkeypatch, replays):
    by_obj = {id(obj): replay for obj, replay in replays}

    def fake_validate(obj, _label):
        return deepcopy(by_obj[id(obj)])

    def fake_compare(left, right):
        return _delta(by_obj[id(left)], by_obj[id(right)])

    monkeypatch.setattr(history, "_validate_attestation", fake_validate)
    monkeypatch.setattr(history, "compare_capture_session_attestations", fake_compare)


def test_three_point_history_summarizes_transitions(monkeypatch):
    a, b, c = {}, {}, {}
    ra = _replay("a", ("missing", "missing"))
    rb = _replay("b", ("captured", "missing"))
    rc = _replay("c", ("captured", "captured"))
    _install(monkeypatch, [(a, ra), (b, rb), (c, rc)])
    out = history.build_attestation_history([
        {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
        {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        {"observed_at": "2026-08-20T08:00:00Z", "attestation": c},
    ])
    assert out["observation_count"] == 3
    assert out["transition_frequencies"] == {"missing->captured": 2}
    assert out["coverage_evolution"]["production_gap_count_change"] == -2
    assert out["coverage_evolution"]["coverage_complete_observation_count"] == 1
    assert out["demand_interpretation"].startswith("none_")
    assert len(out["history_sha256"]) == 64


def test_non_monotonic_time_fails(monkeypatch):
    a, b = {}, {}
    _install(monkeypatch, [(a, _replay("a")), (b, _replay("b"))])
    with pytest.raises(ValueError, match="non_monotonic"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ])


def test_noncanonical_or_non_utc_time_fails(monkeypatch):
    a, b = {}, {}
    _install(monkeypatch, [(a, _replay("a")), (b, _replay("b"))])
    with pytest.raises(ValueError, match="not_utc"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T06:00:00+04:00", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ])


def test_duplicate_attestation_identity_fails(monkeypatch):
    a, b = {}, {}
    _install(monkeypatch, [(a, _replay("a")), (b, _replay("a"))])
    with pytest.raises(ValueError, match="duplicate_attestation"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ])


def test_cross_plan_fails_closed(monkeypatch):
    a, b = {}, {}
    _install(monkeypatch, [(a, _replay("a")), (b, _replay("b", plan="c" * 64))])
    with pytest.raises(ValueError, match="cross_plan"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ])


def test_cross_envelope_fails_closed(monkeypatch):
    a, b = {}, {}
    _install(monkeypatch, [(a, _replay("a")), (b, _replay("b", env="d" * 64))])
    with pytest.raises(ValueError, match="cross_envelope"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ])


def test_supplied_delta_must_exactly_match_replay(monkeypatch):
    a, b = {}, {}
    ra, rb = _replay("a"), _replay("b", ("captured", "captured"))
    _install(monkeypatch, [(a, ra), (b, rb)])
    good = _delta(ra, rb)
    out = history.build_attestation_history([
        {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
        {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
    ], [good])
    assert out["adjacent_delta_refs"][0]["delta_sha256"] == good["delta_sha256"]
    bad = deepcopy(good)
    bad["target_attestation_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="delta_0_mismatch"):
        history.build_attestation_history([
            {"observed_at": "2026-08-20T06:00:00Z", "attestation": a},
            {"observed_at": "2026-08-20T07:00:00Z", "attestation": b},
        ], [bad])


def test_requires_multiple_observations():
    with pytest.raises(ValueError, match="requires_multiple"):
        history.build_attestation_history([])
