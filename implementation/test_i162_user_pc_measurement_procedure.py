from i162_user_pc_measurement_procedure import ExplicitMeasurements, build_packet, procedure_manifest

IDENTITY = {
    "system": "TestOS",
    "release": "1",
    "machine": "x86_64",
    "processor": "cpu",
    "python_implementation": "CPython",
    "python_version": "3.12",
    "logical_cpu_count": 8,
    "executable": "/python",
}


def test_template_is_inert_and_requires_local_execution():
    doc = procedure_manifest()
    assert doc["state"] == "LOCAL_USER_PC_EXECUTION_REQUIRED"
    assert doc["network_enabled"] is False
    assert doc["spend_or_value_movement"] is False


def test_empty_measurements_fail_closed():
    doc = build_packet(ExplicitMeasurements(), identity=IDENTITY)
    assert doc["state"] == "PASS_BLOCKED"
    assert doc["i159_evaluation"]["production_evidence_ready"] is False
    assert "measured_energy_plus_explicit_tariff" in doc["missing_evidence"]


def test_partial_energy_inputs_rejected():
    m = ExplicitMeasurements(energy_before_joules=1.0, energy_task_count=10, energy_source_ref="meter")
    doc = build_packet(m, identity=IDENTITY)
    assert "energy_counter_inputs_must_be_supplied_together" in doc["errors"]


def test_complete_explicit_packet_can_satisfy_i159():
    m = ExplicitMeasurements(
        benchmark_id="fixture-v1",
        benchmark_source_ref="local:fixture-v1",
        quality_acceptance_probability=0.99,
        latency_seconds=0.2,
        reliability_probability=0.98,
        max_parallelism=4,
        measured_available_hours_per_day=8.0,
        availability_source_ref="local:7day-observation",
        energy_before_joules=1000.0,
        energy_after_joules=4600.0,
        energy_task_count=10,
        energy_source_ref="local:meter:run-1",
        tariff_usd_per_kwh=0.05,
        tariff_source_ref="user:tariff-document",
        opportunity_cost_usd_per_hour=0.10,
        opportunity_cost_source_ref="user:declared-opportunity-cost",
    )
    doc = build_packet(
        m,
        confirm_user_owned_pc=True,
        measurement_environment_ref="local:user-pc:session-1",
        identity=IDENTITY,
    )
    assert doc["errors"] == []
    assert doc["state"] == "USER_PC_PACKET_COMPLETE"
    assert doc["i159_evaluation"]["production_evidence_ready"] is True
    assert doc["derived_energy_kwh_per_task"] == 0.0001
