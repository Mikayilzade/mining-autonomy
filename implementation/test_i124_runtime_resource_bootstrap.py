import i124_runtime_resource_bootstrap as m


def good_probe(missing=()):
    return {
        "state": "MEASURED_LOCAL_PROBE_COMPLETE",
        "repetitions": 20,
        "reliability_probability_observed": 1.0,
        "quality_probability_observed": 1.0,
        "session_replay": {"missing_parameters": list(missing)},
    }


def good_runtime():
    return {"state": "PASS_BLOCKED", "receipt": {"result": "PASS_BLOCKED"}}


def test_partial_probe_never_becomes_measured_reproducible():
    ev, blockers = m._project_i123_evidence(good_probe(("electricity_per_task_usd",)))
    assert ev.provenance_class == "measured_partial"
    assert "electricity_cost_not_measured" in blockers


def test_complete_probe_can_project_measured_reproducible():
    ev, blockers = m._project_i123_evidence(good_probe(()))
    assert ev.provenance_class == m.MEASURED
    assert ev.current_reproducible and ev.non_synthetic and ev.capacity_verified
    assert blockers == ()


def test_failed_probe_fails_closed():
    ev, blockers = m._project_i123_evidence({"state": "FAIL_CLOSED", "repetitions": 0})
    assert ev.provenance_class != m.MEASURED
    assert "python_local_probe_not_verified" in blockers


def test_i113_runtime_alone_does_not_materialize_free_ci():
    ev, blockers = m._free_ci_evidence(good_runtime())
    assert ev.current_reproducible
    assert not ev.capacity_verified
    assert "free_tier_ci_capacity_quota_not_materialized" in blockers


def test_result_keeps_independent_market_and_authorization_blockers(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "_run_i113", lambda root, timeout: good_runtime())
    monkeypatch.setattr(m, "_run_python_local_probe", lambda observed_at, repetitions: good_probe(("electricity_per_task_usd",)))
    result = m.build_result(tmp_path, repetitions=20)
    assert result["state"] == "PASS_BLOCKED"
    assert result["remaining_independent_blockers"]["fresh_real_market_evidence"] is True
    assert result["remaining_independent_blockers"]["exact_explicit_authorization"] is True
    assert result["safety"]["market_network_access"] is False
    assert result["safety"]["new_spend"] is False


def test_complete_local_resource_does_not_clear_market_or_auth(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "_run_i113", lambda root, timeout: good_runtime())
    monkeypatch.setattr(m, "_run_python_local_probe", lambda observed_at, repetitions: good_probe(()))
    result = m.build_result(tmp_path, repetitions=20)
    assert result["state"] == "READY_FOR_PORTFOLIO_MATERIALIZATION"
    assert result["backend_review"]["python_local"]["production_selectable"] is True
    assert result["remaining_independent_blockers"]["fresh_real_market_evidence"] is True
    assert result["remaining_independent_blockers"]["exact_explicit_authorization"] is True
