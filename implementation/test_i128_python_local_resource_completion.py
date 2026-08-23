from dataclasses import asdict
from datetime import datetime, timezone

import i128_python_local_resource_completion as m
from resource_calibration_acquisition import ProbeObservation, evaluate_probe_transcript
from resource_evidence_adapter import EnergyMeasurement

NOW = datetime(2026, 8, 23, 21, 0, tzinfo=timezone.utc)
OBSERVED = "2026-08-23T20:55:00Z"


def reference():
    return m.python_local_reference()


def good_summary():
    ref = reference()
    plan = m.build_local_no_spend_plan(
        asdict(ref), benchmark_id=m.BENCHMARK_ID,
        expected_output_digest=m.EXPECTED_OUTPUT_DIGEST,
    )
    rows = tuple(
        ProbeObservation(
            run_id=f"t-{i}", latency_seconds=0.01,
            execution_succeeded=True,
            output_digest=m.EXPECTED_OUTPUT_DIGEST,
            quality_passed=True,
        )
        for i in range(20)
    )
    return evaluate_probe_transcript(
        plan.probe_contract, rows,
        max_parallelism_observed=1,
        rate_limit_per_minute_observed=None,
    )


def energy():
    return EnergyMeasurement(
        energy_kwh_per_task=0.00001,
        tariff_usd_per_kwh=0.10,
        observed_at=OBSERVED,
        max_age_seconds=604800,
        source_ref="test:meter+tariff",
        source_content_digest="e" * 64,
        notes="synthetic test fixture only",
    )


def test_interface_semantics_are_python_local_only_and_do_not_claim_capacity():
    records = m.build_local_interface_semantic_evidence(reference(), observed_at=OBSERVED)
    assert {r.parameter for r in records} == {"quota_units_remaining", "rate_limit_per_minute"}
    assert all(r.value is None for r in records)
    assert all(r.source_kind == "system_probe" for r in records)
    assert all("not an infinite-capacity claim" in r.notes for r in records)


def test_interface_semantics_refuse_other_backend_families():
    for backend in m.default_backend_families():
        if backend.backend_id == "python_local":
            continue
        try:
            m.build_local_interface_semantic_evidence(backend, observed_at=OBSERVED)
        except ValueError as exc:
            assert "python_local" in str(exc)
        else:
            raise AssertionError(f"unexpected interface semantic widening to {backend.backend_id}")


def test_without_energy_exactly_energy_fact_remains_missing():
    packet, att = m.assemble_python_local_evidence(
        reference(), good_summary(), observed_at=OBSERVED, now=NOW,
    )
    assert packet.state == "PASS_BLOCKED"
    assert packet.missing_parameters == ("electricity_per_task_usd",)
    assert set(packet.emitted_parameters) == set(m.CRITICAL_PARAMETERS) - {"electricity_per_task_usd"}
    assert att.state == "planning_only"
    assert packet.strict_resource_promotion_ready is False
    assert packet.i123_evidence.provenance_class == "measured_partial"


def test_explicit_energy_closes_i050_i066_i123_resource_path():
    packet, att = m.assemble_python_local_evidence(
        reference(), good_summary(), observed_at=OBSERVED, now=NOW,
        energy_measurement=energy(),
    )
    assert packet.missing_parameters == ()
    assert set(packet.emitted_parameters) == set(m.CRITICAL_PARAMETERS)
    assert att.state == "calibrated_reproducible"
    assert att.all_current_evidence_reproducible
    assert packet.i066_state == "materialized_reproducible"
    assert packet.i123_evidence.provenance_class == "measured_reproducible"
    assert packet.strict_resource_promotion_ready is True
    assert packet.state == "RESOURCE_EVIDENCE_COMPLETE"


def test_resource_completion_does_not_create_market_route_or_authorization():
    packet, _ = m.assemble_python_local_evidence(
        reference(), good_summary(), observed_at=OBSERVED, now=NOW,
        energy_measurement=energy(),
    )
    assert packet.production_route_created is False
    assert packet.fresh_real_market_evidence_created is False
    assert packet.authorization_created is False
    assert packet.network_enabled is False
    assert packet.credentials_used is False
    assert packet.spend_performed is False
    assert packet.value_movement_enabled is False


def test_energy_and_tariff_must_be_supplied_together(tmp_path):
    try:
        m.run_no_spend_bundle(tmp_path, energy_kwh_per_task=0.1, tariff_usd_per_kwh=None)
    except ValueError as exc:
        assert "together" in str(exc)
    else:
        raise AssertionError("partial energy input must fail closed")


def test_payload_keeps_independent_market_and_authorization_gates_false():
    packet, _ = m.assemble_python_local_evidence(
        reference(), good_summary(), observed_at=OBSERVED, now=NOW,
        energy_measurement=energy(),
    )
    body = m.payload(packet)
    assert body["run"] == "I128"
    assert body["remaining_independent_gates"]["fresh_real_market_evidence"] is False
    assert body["remaining_independent_gates"]["exact_explicit_authorization"] is False
    assert body["remaining_independent_gates"]["production_route"] is False
    assert body["interface_none_semantics"] == "not_applicable_external_provider_limit_not_infinite_host_capacity"
