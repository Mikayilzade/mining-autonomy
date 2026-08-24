import i165_user_pc_one_shot_materializer as i165


def test_no_external_facts_stays_blocked_and_inert():
    result = i165.materialize(repetitions=10, inner_iterations=1, parallelism_cap=1)
    assert result.state == "PASS_BLOCKED"
    assert result.benchmark_session_state == "BENCHMARK_SESSION_COMPLETE"
    missing = set(result.i162_packet["missing_evidence"])
    assert "ownership_bound_identity" in missing
    assert "measured_availability" in missing
    assert "measured_energy_plus_explicit_tariff" in missing
    assert "explicit_opportunity_cost" in missing
    assert result.network_enabled is False
    assert result.spend_or_value_movement is False


def test_complete_explicit_fixture_can_complete_evidence_assembly_only():
    external = {
        "measured_available_hours_per_day": 8.0,
        "availability_source_ref": "test-fixture:availability",
        "energy_before_joules": 1000.0,
        "energy_after_joules": 4600.0,
        "energy_task_count": 10,
        "energy_source_ref": "test-fixture:joule-counter",
        "tariff_usd_per_kwh": 0.1,
        "tariff_source_ref": "test-fixture:tariff",
        "opportunity_cost_usd_per_hour": 0.01,
        "opportunity_cost_source_ref": "test-fixture:opportunity-cost",
    }
    result = i165.materialize(
        external_facts=external,
        confirm_user_owned_pc=True,
        repetitions=10,
        inner_iterations=1,
        parallelism_cap=1,
    )
    assert result.state == "USER_PC_MATERIALIZED"
    assert result.i162_packet["state"] == "USER_PC_PACKET_COMPLETE"
    assert result.i162_packet["i159_evaluation"]["production_evidence_ready"] is True
    assert result.production_route_created is False
    assert result.task_acceptance_or_submission is False


def test_external_benchmark_override_is_rejected():
    try:
        i165.materialize(
            external_facts={"latency_seconds": 0.0},
            repetitions=10,
            inner_iterations=1,
            parallelism_cap=1,
        )
    except ValueError as exc:
        assert "unsupported_or_benchmark_override_fields" in str(exc)
    else:
        raise AssertionError("benchmark override must fail closed")
