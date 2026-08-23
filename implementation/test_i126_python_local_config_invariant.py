from dataclasses import asdict, replace
from datetime import datetime, timezone

import i126_python_local_config_invariant as m
from resource_profile_evidence import (
    BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
    CRITICAL_PARAMETERS,
    PYTHON_LOCAL_CONFIG_INVARIANTS,
    attest_resource_profile,
    backend_config_invariant_digest,
    backend_config_invariant_source_ref,
    make_evidence,
    reference_backend_hash,
)
from resource_router import default_backend_families

NOW = datetime(2026, 8, 23, 20, 0, tzinfo=timezone.utc)
OBSERVED = "2026-08-23T19:55:00Z"


def refs():
    return {x.backend_id: asdict(x) for x in default_backend_families()}


def dynamic_records(reference):
    values = {
        "currently_available": True,
        "programmatic_access": True,
        "quota_units_remaining": None,
        "electricity_per_task_usd": 0.001,
        "latency_seconds": 0.01,
        "reliability_probability": 1.0,
        "quality_probability": 1.0,
        "max_parallelism": 1,
        "rate_limit_per_minute": None,
    }
    rh = reference_backend_hash(reference)
    return tuple(make_evidence(
        evidence_id=f"test-dynamic-{parameter}", backend_id="python_local",
        parameter=parameter, value=value, source_kind="system_probe",
        source_ref=f"test-probe:{parameter}", observed_at=OBSERVED,
        max_age_seconds=3600, reference_hash=rh,
        source_content_digest="a" * 64,
    ) for parameter, value in values.items())


def test_builder_emits_only_allowlisted_python_local_intrinsic_facts():
    result = m.build_python_local_config_invariants(refs()["python_local"], observed_at=OBSERVED)
    assert result.state == "REPRODUCIBLE_CONFIG_INVARIANTS_READY"
    assert set(result.emitted_parameters) == set(PYTHON_LOCAL_CONFIG_INVARIANTS)
    assert set(result.emitted_parameters).isdisjoint({
        "quota_units_remaining", "rate_limit_per_minute", "electricity_per_task_usd",
        "latency_seconds", "reliability_probability", "quality_probability", "max_parallelism",
    })
    assert all(r.source_kind == BACKEND_CONFIG_INVARIANT_SOURCE_KIND for r in result.evidence_records)


def test_builder_refuses_all_non_python_local_backend_families():
    references = refs()
    for backend_id in (
        "local_model", "subscription_assistant", "cheap_external_api",
        "strong_external_api", "free_tier_ci", "owned_pc", "future_paid_vps",
    ):
        try:
            m.build_python_local_config_invariants(references[backend_id], observed_at=OBSERVED)
        except ValueError as exc:
            assert "python_local" in str(exc)
        else:
            raise AssertionError(f"unexpected invariant widening to {backend_id}")


def test_reference_drift_is_refused_even_for_python_local_identity():
    reference = refs()["python_local"]
    drifted = dict(reference)
    drifted["fixed_monthly_cost_usd"] = 1.0
    try:
        m.build_python_local_config_invariants(drifted, observed_at=OBSERVED)
    except ValueError as exc:
        assert "fixed_monthly_cost_usd" in str(exc)
    else:
        raise AssertionError("reference drift must fail closed")


def test_generic_i050_rejects_tampered_invariant_value_and_digest():
    reference = refs()["python_local"]
    rh = reference_backend_hash(reference)
    bad_value = make_evidence(
        evidence_id="bad-value", backend_id="python_local",
        parameter="fixed_monthly_cost_usd", value=1.0,
        source_kind=BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
        source_ref=backend_config_invariant_source_ref("python_local", "fixed_monthly_cost_usd"),
        observed_at=OBSERVED, max_age_seconds=3600, reference_hash=rh,
        source_content_digest=backend_config_invariant_digest("python_local", "fixed_monthly_cost_usd", 1.0),
    )
    att = attest_resource_profile(reference, (bad_value,), now=NOW)
    row = next(x for x in att.parameter_calibrations if x.parameter == "fixed_monthly_cost_usd")
    assert row.state == "invalid_or_stale" and "value_mismatch" in row.reason

    good = m.build_python_local_config_invariants(reference, observed_at=OBSERVED).evidence_records[0]
    bad_digest = replace(good, source_content_digest="f" * 64, evidence_hash=None)
    bad_digest = replace(bad_digest, evidence_hash=bad_digest.computed_hash())
    att2 = attest_resource_profile(reference, (bad_digest,), now=NOW)
    row2 = next(x for x in att2.parameter_calibrations if x.parameter == good.parameter)
    assert row2.state == "invalid_or_stale" and "digest_mismatch" in row2.reason


def test_generic_i050_rejects_config_invariant_for_quota_capacity():
    reference = refs()["python_local"]
    record = make_evidence(
        evidence_id="bad-quota", backend_id="python_local",
        parameter="quota_units_remaining", value=None,
        source_kind=BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
        source_ref=backend_config_invariant_source_ref("python_local", "quota_units_remaining"),
        observed_at=OBSERVED, max_age_seconds=3600,
        reference_hash=reference_backend_hash(reference),
        source_content_digest=backend_config_invariant_digest("python_local", "quota_units_remaining", None),
    )
    att = attest_resource_profile(reference, (record,), now=NOW)
    row = next(x for x in att.parameter_calibrations if x.parameter == "quota_units_remaining")
    assert row.state == "invalid_or_stale" and "parameter_not_allowed" in row.reason


def test_partial_dynamic_evidence_stays_planning_only_and_i123_partial():
    reference = refs()["python_local"]
    config = m.build_python_local_config_invariants(reference, observed_at=OBSERVED)
    att = attest_resource_profile(reference, config.evidence_records, now=NOW)
    assert att.state == "planning_only"
    assert not att.all_current_evidence_reproducible
    ev = m.project_i050_attestation_to_i123(att)
    assert ev.provenance_class == "measured_partial"
    assert not ev.capacity_verified


def test_complete_independent_dynamic_evidence_reaches_i050_i066_then_i123_projection():
    reference = refs()["python_local"]
    att, records = m.attest_with_python_local_invariants(
        reference, dynamic_records(reference), observed_at=OBSERVED, now=NOW,
    )
    assert {r.parameter for r in records} == set(CRITICAL_PARAMETERS)
    assert att.state == "calibrated_reproducible"
    assert att.all_current_evidence_reproducible

    materialized = m.verify_i066_compatibility(reference, records, now=NOW)
    assert materialized.state == "materialized_reproducible"
    assert materialized.quantitative_values_complete
    assert materialized.execution_enabled is False
    assert materialized.network_enabled is False

    ev = m.project_i050_attestation_to_i123(att)
    assert ev.provenance_class == m.MEASURED
    assert ev.current_reproducible and ev.non_synthetic and ev.capacity_verified


def test_i126_never_creates_route_authorization_network_or_value_movement():
    result = m.build_python_local_config_invariants(refs()["python_local"], observed_at=OBSERVED)
    payload = m.result_payload(result)
    assert payload["production_route_created"] is False
    assert payload["authorization_created"] is False
    assert payload["network_enabled"] is False
    assert payload["spend_performed"] is False
    assert payload["value_movement_enabled"] is False
    assert payload["owned_pc_cost_inferred"] is False
    assert payload["free_ci_capacity_inferred"] is False
