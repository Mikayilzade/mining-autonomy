from i159_owned_pc_evidence_packet import OwnedPcObservation, evaluate


def test_empty_requires_local_materialization():
    result = evaluate(OwnedPcObservation())
    assert result["state"] == "LOCAL_MATERIALIZATION_REQUIRED"
    assert not result["production_evidence_ready"]


def test_unbound_measurements_fail_closed():
    result = evaluate(OwnedPcObservation(quality_acceptance_probability=0.9))
    assert result["state"] == "PASS_BLOCKED"
    assert "measurements_not_bound_to_user_owned_pc" in result["errors"]


def test_complete_packet_can_promote_evidence_only():
    observation = OwnedPcObservation(
        hardware_identity="cpu:model-x;ram:32gb",
        os_identity="linux-x86_64",
        execution_interface="python3",
        deterministic_programmatic_access_verified=True,
        benchmark_id="fixture-v1",
        benchmark_source_ref="sha256:abc",
        quality_acceptance_probability=0.99,
        latency_seconds=0.2,
        reliability_probability=0.999,
        max_parallelism=4,
        measured_available_hours_per_day=8,
        availability_source_ref="local-log:7d",
        energy_kwh_per_task=0.0002,
        energy_source_ref="meter:joules",
        tariff_usd_per_kwh=0.07,
        tariff_source_ref="utility-tariff:2026-08",
        opportunity_cost_usd_per_hour=0.05,
        opportunity_cost_source_ref="user-policy:v1",
        measurement_environment_ref="owned-pc-session:fixture-v1",
        measurements_from_user_owned_pc=True,
    )
    result = evaluate(observation)
    assert result["state"] == "OWNED_PC_EVIDENCE_COMPLETE"
    assert result["production_evidence_ready"]
    assert not result["execution_enabled"]


def test_forbidden_probe_effects_block():
    result = evaluate(OwnedPcObservation(network_used=True))
    assert result["state"] == "PASS_BLOCKED"
    assert result["errors"] == ["measurement_packet_not_local_no_spend"]
