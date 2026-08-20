from datetime import datetime, timezone
import pytest

from resource_profile_evidence import (
    CRITICAL_PARAMETERS,
    attest_resource_profile,
    make_evidence,
    materialize_calibrated_backend_fields,
    reference_backend_hash,
)

NOW = datetime(2026, 8, 21, 0, 30, tzinfo=timezone.utc)


def reference():
    return {
        "backend_id": "owned_pc",
        "currently_available": False,
        "programmatic_access": True,
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "fixed_monthly_cost_usd": 0.0,
        "sunk_or_already_committed": True,
        "quota_units_remaining": None,
        "electricity_per_task_usd": 0.04,
        "latency_seconds": 5.0,
        "reliability_probability": 0.97,
        "quality_probability": 0.94,
        "max_parallelism": 2,
        "rate_limit_per_minute": 60.0,
    }


def evidence_set(*, source_kind="measured_local", observed_at="2026-08-21T00:00:00Z"):
    r = reference()
    h = reference_backend_hash(r)
    values = {
        "currently_available": True,
        "programmatic_access": True,
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "fixed_monthly_cost_usd": 0.0,
        "sunk_or_already_committed": True,
        "quota_units_remaining": None,
        "electricity_per_task_usd": 0.025,
        "latency_seconds": 3.2,
        "reliability_probability": 0.99,
        "quality_probability": 0.96,
        "max_parallelism": 2,
        "rate_limit_per_minute": 30.0,
    }
    return [
        make_evidence(
            evidence_id=f"e-{p}",
            backend_id="owned_pc",
            parameter=p,
            value=values[p],
            source_kind=source_kind,
            source_ref=f"fixture://{p}",
            observed_at=observed_at,
            max_age_seconds=3600,
            reference_hash=h,
            source_content_digest=(None if source_kind == "user_declared" else "a"*64),
        )
        for p in CRITICAL_PARAMETERS
    ]


def test_complete_reproducible_evidence_calibrates_profile():
    a = attest_resource_profile(reference(), evidence_set(), now=NOW)
    assert a.state == "calibrated_reproducible"
    assert a.all_current_evidence_reproducible is True
    assert a.contains_user_declaration is False
    assert len(a.calibrated_values) == len(CRITICAL_PARAMETERS)
    assert a.planning_only is True
    assert a.execution_enabled is False


def test_user_declared_complete_profile_is_separate_state_not_measured_claim():
    a = attest_resource_profile(reference(), evidence_set(source_kind="user_declared"), now=NOW)
    assert a.state == "calibrated_declared"
    assert a.contains_user_declaration is True
    assert a.all_current_evidence_reproducible is False


def test_synthetic_reference_values_never_satisfy_live_calibration():
    records = evidence_set(source_kind="user_declared")
    h = reference_backend_hash(reference())
    records[0] = make_evidence(
        evidence_id="synthetic-availability",
        backend_id="owned_pc",
        parameter=CRITICAL_PARAMETERS[0],
        value=True,
        source_kind="synthetic_reference",
        source_ref="router-default",
        observed_at="2026-08-21T00:00:00Z",
        max_age_seconds=3600,
        reference_hash=h,
    )
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("synthetic_reference_not_live_evidence" in r for r in a.reasons)


def test_missing_parameter_fails_closed():
    records = evidence_set()[:-1]
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("rate_limit_per_minute:missing_evidence" == r for r in a.reasons)


def test_stale_or_future_evidence_fails_closed():
    stale = evidence_set(observed_at="2026-08-20T22:00:00Z")
    a = attest_resource_profile(reference(), stale, now=NOW)
    assert a.state == "planning_only"
    assert any("stale_evidence" in r for r in a.reasons)

    future = evidence_set(observed_at="2026-08-21T00:31:00Z")
    b = attest_resource_profile(reference(), future, now=NOW)
    assert b.state == "planning_only"
    assert any("future_dated_evidence" in r for r in b.reasons)


def test_hash_tamper_and_reference_binding_fail_closed():
    records = evidence_set()
    first = records[0]
    records[0] = first.__class__(**{**first.__dict__, "value": False})
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("evidence_hash_mismatch" in r for r in a.reasons)

    records = evidence_set()
    second = records[1]
    records[1] = second.__class__(**{**second.__dict__, "reference_backend_hash": "bad"})
    b = attest_resource_profile(reference(), records, now=NOW)
    assert b.state == "planning_only"
    assert any("reference_backend_hash_mismatch" in r for r in b.reasons)


def test_conflicting_current_evidence_fails_closed():
    records = evidence_set(source_kind="user_declared")
    h = reference_backend_hash(reference())
    records.append(make_evidence(
        evidence_id="e-conflict",
        backend_id="owned_pc",
        parameter="currently_available",
        value=False,
        source_kind="user_declared",
        source_ref="fixture://conflict",
        observed_at="2026-08-21T00:10:00Z",
        max_age_seconds=3600,
        reference_hash=h,
    ))
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("conflicting_current_evidence" in r for r in a.reasons)


def test_reproducible_sources_require_content_digest():
    records = evidence_set()
    first = records[0]
    records[0] = make_evidence(
        evidence_id=first.evidence_id,
        backend_id=first.backend_id,
        parameter=first.parameter,
        value=first.value,
        source_kind=first.source_kind,
        source_ref=first.source_ref,
        observed_at=first.observed_at,
        max_age_seconds=first.max_age_seconds,
        reference_hash=first.reference_backend_hash,
        source_content_digest=None,
    )
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("reproducible_source_digest_required" in r for r in a.reasons)


def test_materialization_overrides_reference_only_after_complete_attestation():
    r = reference()
    a = attest_resource_profile(r, evidence_set(), now=NOW)
    out = materialize_calibrated_backend_fields(r, a)
    assert out["currently_available"] is True
    assert out["electricity_per_task_usd"] == pytest.approx(0.025)
    assert out["_resource_attestation"]["execution_enabled"] is False

    incomplete = attest_resource_profile(r, evidence_set()[:-1], now=NOW)
    with pytest.raises(ValueError, match="resource_profile_not_live_calibrated"):
        materialize_calibrated_backend_fields(r, incomplete)


def test_invalid_probability_and_parallelism_fail_closed():
    records = evidence_set(source_kind="user_declared")
    h = reference_backend_hash(reference())
    by_param = {r.parameter: r for r in records}
    q = by_param["quality_probability"]
    records[records.index(q)] = make_evidence(
        evidence_id=q.evidence_id, backend_id=q.backend_id, parameter=q.parameter,
        value=1.2, source_kind=q.source_kind, source_ref=q.source_ref,
        observed_at=q.observed_at, max_age_seconds=q.max_age_seconds,
        reference_hash=h,
    )
    p = by_param["max_parallelism"]
    records[records.index(p)] = make_evidence(
        evidence_id=p.evidence_id, backend_id=p.backend_id, parameter=p.parameter,
        value=0, source_kind=p.source_kind, source_ref=p.source_ref,
        observed_at=p.observed_at, max_age_seconds=p.max_age_seconds,
        reference_hash=h,
    )
    a = attest_resource_profile(reference(), records, now=NOW)
    assert a.state == "planning_only"
    assert any("invalid_probability_value" in r for r in a.reasons)
    assert any("invalid_parallelism_value" in r for r in a.reasons)
