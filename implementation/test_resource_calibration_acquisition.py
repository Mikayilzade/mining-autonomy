import pytest

from resource_calibration_acquisition import (
    OfflineProbeContract,
    ProbeObservation,
    build_local_no_spend_plan,
    evaluate_probe_transcript,
)
from resource_profile_evidence import CRITICAL_PARAMETERS


def reference(backend_id="python_local", family="deterministic_python"):
    return {"backend_id": backend_id, "family": family, "notes": "synthetic reference"}


def observations(n=10, *, failures=0, bad_quality=0):
    rows = []
    for i in range(n):
        succeeded = i >= failures
        quality = succeeded and i >= failures + bad_quality
        rows.append(ProbeObservation(
            run_id=f"r{i:02d}",
            latency_seconds=0.01 + i * 0.001,
            execution_succeeded=succeeded,
            output_digest=("a" * 64) if succeeded else None,
            quality_passed=quality,
        ))
    return rows


def test_plan_covers_exact_i050_critical_parameters():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture-v1", expected_output_digest="a" * 64)
    assert {r.parameter for r in plan.requirements} == set(CRITICAL_PARAMETERS)
    assert plan.planning_only_until_attested is True
    assert plan.execution_enabled is False


def test_plan_rejects_nonpriority_external_backend():
    with pytest.raises(ValueError, match="backend_not_local_no_spend_priority"):
        build_local_no_spend_plan(reference(family="cheap_external_llm_api"), benchmark_id="fixture", expected_output_digest="a" * 64)


def test_probe_contract_is_inert_and_no_network_credentials_or_spend():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    contract = plan.probe_contract
    assert contract.network_allowed is False
    assert contract.credentials_allowed is False
    assert contract.paid_service_allowed is False
    assert contract.value_movement_allowed is False


def test_probe_summary_measures_only_observable_fields():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    summary = evaluate_probe_transcript(plan.probe_contract, observations(), max_parallelism_observed=2)
    assert summary.reliability_probability == 1.0
    assert summary.quality_probability == 1.0
    assert summary.measured_parameters["currently_available"] is True
    assert summary.measured_parameters["programmatic_access"] is True
    assert summary.measured_parameters["max_parallelism"] == 2
    for forbidden in {
        "fixed_monthly_cost_usd", "sunk_or_already_committed", "quota_units_remaining",
        "electricity_per_task_usd", "requires_credentials", "requires_paid_account", "requires_new_spend",
    }:
        assert forbidden not in summary.measured_parameters


def test_reliability_and_quality_are_distinct():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    summary = evaluate_probe_transcript(
        plan.probe_contract,
        observations(10, failures=2, bad_quality=2),
        max_parallelism_observed=1,
    )
    assert summary.reliability_probability == 0.8
    assert summary.quality_probability == 0.75


def test_insufficient_repetitions_fail_closed():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    with pytest.raises(ValueError, match="insufficient_probe_repetitions"):
        evaluate_probe_transcript(plan.probe_contract, observations(9), max_parallelism_observed=1)


def test_duplicate_run_ids_rejected():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    rows = observations()
    rows[-1] = ProbeObservation("r00", 0.02, True, "a" * 64, True)
    with pytest.raises(ValueError, match="duplicate_or_missing_run_id"):
        evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=1)


def test_false_quality_claim_rejected():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    rows = observations()
    rows[-1] = ProbeObservation("r09", 0.02, True, "b" * 64, True)
    with pytest.raises(ValueError, match="invalid_quality_pass_claim"):
        evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=1)


def test_noninert_contract_rejected():
    contract = OfflineProbeContract(
        backend_id="python_local",
        reference_backend_hash="x" * 64,
        benchmark_id="fixture",
        expected_output_digest="a" * 64,
        network_allowed=True,
    )
    with pytest.raises(ValueError, match="probe_contract_not_inert"):
        evaluate_probe_transcript(contract, observations(), max_parallelism_observed=1)


def test_transcript_digest_is_order_invariant_by_run_id():
    plan = build_local_no_spend_plan(reference(), benchmark_id="fixture", expected_output_digest="a" * 64)
    rows = observations()
    a = evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=2)
    b = evaluate_probe_transcript(plan.probe_contract, list(reversed(rows)), max_parallelism_observed=2)
    assert a.transcript_digest == b.transcript_digest
