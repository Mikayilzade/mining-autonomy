import math
from datetime import datetime, timezone

import pytest

from resource_calibration_acquisition import ProbeObservation, build_local_no_spend_plan, evaluate_probe_transcript
from resource_evidence_adapter import (
    EnergyMeasurement,
    ExplicitDeclaration,
    build_resource_evidence,
    normalize_probe_summary_for_evidence,
)
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile


def reference():
    return {"backend_id": "python_local", "family": "deterministic_python", "notes": "synthetic reference"}


def summary(*, observed_at="2026-08-21T00:00:00+00:00"):
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture-v1", expected_output_digest="a" * 64)
    rows = [
        ProbeObservation(f"r{i:02d}", 0.01 + i * 0.001, True, "a" * 64, True)
        for i in range(10)
    ]
    raw = evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=2)
    return plan, normalize_probe_summary_for_evidence(raw, observed_at_utc=observed_at)


def decl(parameter, value, *, n=1):
    return ExplicitDeclaration(
        parameter=parameter,
        value=value,
        observed_at="2026-08-21T00:00:00+00:00",
        max_age_seconds=86400,
        source_ref=f"user-declaration:{n}:{parameter}",
    )


def energy_measurement(energy=0.05, tariff=0.12):
    return EnergyMeasurement(
        energy_kwh_per_task=energy,
        tariff_usd_per_kwh=tariff,
        observed_at="2026-08-21T00:00:00+00:00",
        max_age_seconds=86400,
        source_ref="meter+tariff:synthetic",
        source_content_digest="b" * 64,
    )


def test_probe_emits_only_observed_i050_fields_and_keeps_rest_missing():
    plan, probe = summary()
    result = build_resource_evidence(plan, probe_summary=probe)
    assert set(result.emitted_parameters) == {
        "currently_available", "programmatic_access", "latency_seconds",
        "reliability_probability", "quality_probability", "max_parallelism",
    }
    assert "fixed_monthly_cost_usd" in result.missing_parameters
    assert result.complete_for_attestation is False
    assert {r.source_kind for r in result.records} == {"system_probe"}
    assert all(r.source_content_digest == probe.transcript_digest for r in result.records)


def test_probe_timestamp_is_required_not_inferred_from_current_time():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture-v1", expected_output_digest="a" * 64)
    rows = [ProbeObservation(f"r{i}", 0.01, True, "a" * 64, True) for i in range(10)]
    raw = evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=1)
    with pytest.raises(ValueError, match="probe_observed_at_utc_required"):
        build_resource_evidence(plan, probe_summary=raw)


def test_declarations_preserve_user_declared_kind_and_never_get_digest_fabricated():
    plan, probe = summary()
    result = build_resource_evidence(
        plan,
        probe_summary=probe,
        declarations=[decl("requires_credentials", False)],
    )
    record = next(r for r in result.records if r.parameter == "requires_credentials")
    assert record.source_kind == "user_declared"
    assert record.source_content_digest is None


def test_energy_measurement_derives_only_electricity_cost_with_measured_local_provenance():
    plan, probe = summary()
    result = build_resource_evidence(plan, probe_summary=probe, energy_measurement=energy_measurement())
    record = next(r for r in result.records if r.parameter == "electricity_per_task_usd")
    assert record.value == pytest.approx(0.006)
    assert record.source_kind == "measured_local"
    assert record.source_content_digest == "b" * 64


def test_duplicate_parameter_across_probe_and_declaration_fails_closed():
    plan, probe = summary()
    with pytest.raises(ValueError, match="duplicate_parameter_input:latency_seconds"):
        build_resource_evidence(plan, probe_summary=probe, declarations=[decl("latency_seconds", 0.5)])


def test_missing_parameters_are_not_backfilled_from_reference_backend():
    plan, _ = summary()
    result = build_resource_evidence(plan, declarations=[decl("requires_new_spend", False)])
    assert result.emitted_parameters == ("requires_new_spend",)
    assert len(result.missing_parameters) == len(CRITICAL_PARAMETERS) - 1


def test_full_explicit_plus_probe_set_can_attest_but_remains_declared_when_declarations_exist():
    plan, probe = summary()
    declarations = [
        decl("requires_credentials", False, n=1),
        decl("requires_paid_account", False, n=2),
        decl("requires_new_spend", False, n=3),
        decl("fixed_monthly_cost_usd", 0.0, n=4),
        decl("sunk_or_already_committed", True, n=5),
        decl("quota_units_remaining", None, n=6),
        decl("electricity_per_task_usd", 0.0, n=7),
        decl("rate_limit_per_minute", None, n=8),
    ]
    result = build_resource_evidence(plan, probe_summary=probe, declarations=declarations)
    assert result.complete_for_attestation is True
    attestation = attest_resource_profile(
        reference(), result.records, now=datetime(2026, 8, 21, 1, 0, tzinfo=timezone.utc)
    )
    assert attestation.state == "calibrated_declared"
    assert attestation.contains_user_declaration is True


def test_noninert_probe_summary_is_rejected():
    plan, probe = summary()
    broken = type(probe)(**{**probe.__dict__, "network_enabled": True})
    with pytest.raises(ValueError, match="probe_summary_not_inert"):
        build_resource_evidence(plan, probe_summary=broken)


def test_probe_backend_binding_mismatch_rejected():
    plan, probe = summary()
    broken = type(probe)(**{**probe.__dict__, "backend_id": "other"})
    with pytest.raises(ValueError, match="probe_backend_mismatch"):
        build_resource_evidence(plan, probe_summary=broken)


def test_negative_energy_or_missing_digest_rejected():
    plan, _ = summary()
    with pytest.raises(ValueError, match="energy_inputs_must_be_nonnegative"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(-0.1, 0.12))
    with pytest.raises(ValueError, match="energy_source_digest_required"):
        broken = energy_measurement()
        build_resource_evidence(plan, energy_measurement=EnergyMeasurement(
            broken.energy_kwh_per_task,
            broken.tariff_usd_per_kwh,
            broken.observed_at,
            broken.max_age_seconds,
            broken.source_ref,
            "short",
        ))


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_energy_is_rejected_independently_of_i129(bad):
    plan, _ = summary()
    with pytest.raises(ValueError, match="energy_kwh_per_task_must_be_finite_number"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(bad, 0.12))


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_tariff_is_rejected_independently_of_i129(bad):
    plan, _ = summary()
    with pytest.raises(ValueError, match="tariff_usd_per_kwh_must_be_finite_number"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(0.05, bad))


@pytest.mark.parametrize("bad", [True, False, "0.05", None])
def test_boolean_or_nonnumeric_energy_is_rejected(bad):
    plan, _ = summary()
    with pytest.raises(ValueError, match="energy_kwh_per_task_must_be_finite_number"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(bad, 0.12))


@pytest.mark.parametrize("bad", [True, False, "0.12", None])
def test_boolean_or_nonnumeric_tariff_is_rejected(bad):
    plan, _ = summary()
    with pytest.raises(ValueError, match="tariff_usd_per_kwh_must_be_finite_number"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(0.05, bad))


def test_zero_measured_energy_is_rejected():
    plan, _ = summary()
    with pytest.raises(ValueError, match="energy_kwh_per_task_must_be_positive"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(0.0, 0.12))


def test_zero_tariff_stays_blocked_without_separate_zero_tariff_provenance_contract():
    plan, _ = summary()
    with pytest.raises(ValueError, match="electricity_cost_must_be_positive_at_adapter_precision"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(0.05, 0.0))


def test_multiplication_overflow_is_rejected():
    plan, _ = summary()
    assert math.isfinite(1e308)
    with pytest.raises(ValueError, match="electricity_cost_must_be_finite"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(1e308, 1e308))


def test_positive_cost_that_rounds_to_zero_is_rejected():
    plan, _ = summary()
    with pytest.raises(ValueError, match="electricity_cost_must_be_positive_at_adapter_precision"):
        build_resource_evidence(plan, energy_measurement=energy_measurement(1e-12, 1e-12))


def test_small_but_representable_positive_cost_is_preserved():
    plan, _ = summary()
    result = build_resource_evidence(plan, energy_measurement=energy_measurement(1e-5, 1e-5))
    record = next(r for r in result.records if r.parameter == "electricity_per_task_usd")
    assert record.value == 1e-10
    assert record.value > 0
    assert math.isfinite(record.value)
    assert record.source_kind == "measured_local"
