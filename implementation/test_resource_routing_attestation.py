from dataclasses import asdict
from datetime import datetime, timezone

from resource_router import ExecutionBackend, TaskEconomics
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile, make_evidence, reference_backend_hash
from resource_routing_attestation import route_task_with_attested_resources

NOW = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)


def backend(backend_id="local", **overrides):
    base = dict(backend_id=backend_id, family="synthetic", capabilities=frozenset({"extract"}), automation_role="autonomous", programmatic_access=True, policy_allowed=True, currently_available=True, requires_credentials=False, requires_paid_account=False, requires_new_spend=False, fixed_monthly_cost_usd=0.0, sunk_or_already_committed=True, allocation_basis_tasks_per_month=None, quota_units_monthly=None, quota_units_remaining=None, unit_name="task", marginal_cost_per_unit_usd=0.0, units_per_task=1.0, electricity_per_task_usd=0.01, external_api_per_task_usd=0.0, retry_failure_expected_cost_usd=0.01, maintenance_minutes_per_task=0.0, human_time_value_per_hour_usd=10.0, opportunity_cost_per_task_usd=0.0, latency_seconds=1.0, reliability_probability=0.99, quality_probability=0.99, max_parallelism=1, rate_limit_per_minute=60.0, notes="reference")
    base.update(overrides)
    return ExecutionBackend(**base)


def task():
    return TaskEconomics(task_id="t1", required_capabilities=frozenset({"extract"}), gross_payout_usd=10.0, acceptance_probability=0.95, dispute_probability=0.02, nonpayment_probability=0.01, minimum_success_probability=0.90, minimum_expected_margin_usd=0.25, minimum_expected_margin_ratio=0.30)


def attestation_for(b, source_kind="measured_local"):
    ref = asdict(b); rh = reference_backend_hash(ref); records = []
    for i, p in enumerate(CRITICAL_PARAMETERS):
        records.append(make_evidence(evidence_id=f"e{i}", backend_id=b.backend_id, parameter=p, value=ref[p], source_kind=source_kind, source_ref=f"fixture:{p}", observed_at="2026-08-20T23:55:00Z", max_age_seconds=3600, reference_hash=rh, source_content_digest=None if source_kind == "user_declared" else "a"*64))
    return attest_resource_profile(ref, records, now=NOW)


def test_reference_profile_never_selected_without_attestation():
    d = route_task_with_attested_resources(task(), [backend()])
    assert d.state == "resource_evidence_missing" and d.selected_backend_id is None
    assert d.entries[0].route_state == "resource_evidence_missing"


def test_reproducible_attestation_enters_route_set():
    b = backend(); a = attestation_for(b); d = route_task_with_attested_resources(task(), [b], [a])
    assert a.state == "calibrated_reproducible"
    assert d.state == "route_dry_run" and d.selected_backend_id == "local"
    assert d.selected_calibration_state == "calibrated_reproducible"
    assert d.execution_enabled is False and d.network_enabled is False


def test_user_declared_stays_visibly_declared():
    b = backend(); a = attestation_for(b, "user_declared"); d = route_task_with_attested_resources(task(), [b], [a])
    assert a.state == "calibrated_declared"
    assert d.selected_calibration_state == "calibrated_declared"
    assert d.entries[0].route_state == "calibrated_declared_route"


def test_planning_only_attestation_cannot_route():
    b = backend(); a = attest_resource_profile(asdict(b), [], now=NOW)
    d = route_task_with_attested_resources(task(), [b], [a])
    assert d.state == "resource_evidence_missing" and d.selected_backend_id is None


def test_unproven_cheaper_reference_cannot_beat_calibrated_backend():
    cheap_unproven = backend("unproven", electricity_per_task_usd=0.0)
    proven = backend("proven", electricity_per_task_usd=0.02)
    d = route_task_with_attested_resources(task(), [cheap_unproven, proven], [attestation_for(proven)])
    assert d.selected_backend_id == "proven"
    assert next(x for x in d.entries if x.backend_id == "unproven").selectable is False


def test_calibrated_backend_still_obeys_quality_gate():
    b = backend(reliability_probability=0.95, quality_probability=0.80); a = attestation_for(b)
    d = route_task_with_attested_resources(task(), [b], [a])
    assert d.state == "hold" and d.selected_backend_id is None
    assert "success_probability_below_threshold" in d.entries[0].calibrated_quote.planning_reasons


def test_attestation_without_reference_rejected():
    known = backend("known"); other = backend("other"); a = attestation_for(other)
    try: route_task_with_attested_resources(task(), [known], [a])
    except ValueError as e: assert str(e) == "attestation_without_reference_backend"
    else: raise AssertionError("expected rejection")
