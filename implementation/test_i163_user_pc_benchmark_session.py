import i163_user_pc_benchmark_session as i163


def test_parallelism_candidates_are_bounded_and_include_one():
    values = i163._candidate_parallelism(16, 6)
    assert values[0] == 1
    assert values[-1] == 6
    assert all(1 <= x <= 6 for x in values)


def test_session_measures_benchmark_but_keeps_external_facts_blocked():
    result = i163.run_session(repetitions=10, inner_iterations=2, parallelism_cap=2)
    assert result["state"] == "BENCHMARK_SESSION_COMPLETE"
    assert result["measured_safe_parallelism"] >= 1
    assert result["i162_projection"]["state"] == "PASS_BLOCKED"
    missing = set(result["i162_projection"]["missing_evidence"])
    assert "measured_availability" in missing
    assert "measured_energy_plus_explicit_tariff" in missing
    assert "explicit_opportunity_cost" in missing
    assert result["network_enabled"] is False
    assert result["spend_or_value_movement"] is False


def test_ownership_flag_does_not_complete_missing_economics():
    result = i163.run_session(
        repetitions=10,
        inner_iterations=1,
        parallelism_cap=1,
        confirm_user_owned_pc=True,
    )
    assert result["ownership_confirmation_supplied"] is True
    assert result["i162_projection"]["i159_evaluation"]["identity_ready"] is True
    assert result["i162_projection"]["i159_evaluation"]["benchmark_ready"] is True
    assert result["i162_projection"]["i159_evaluation"]["production_evidence_ready"] is False


def test_invalid_session_parameters_fail_closed():
    for kwargs in (
        {"repetitions": 9},
        {"inner_iterations": 0},
        {"parallelism_cap": 0},
    ):
        try:
            i163.run_session(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {kwargs}")
