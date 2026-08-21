from dataclasses import asdict
from datetime import datetime, timezone

from benchmark_feedback_integration import merge_verified_feedback, routing_delta
from receipt_replay_calibration import CalibrationFeedback
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile, make_evidence, reference_backend_hash
from resource_router import ExecutionBackend, TaskEconomics
from resource_routing_attestation import route_task_with_attested_resources

NOW=datetime(2026,8,21,9,30,tzinfo=timezone.utc); FRESH="2026-08-21T09:25:00Z"; STALE="2026-08-20T00:00:00Z"


def backend():
    return ExecutionBackend(backend_id="python_local",family="local",capabilities=frozenset({"extract"}),automation_role="autonomous",
        programmatic_access=True,policy_allowed=True,currently_available=True,requires_credentials=False,requires_paid_account=False,
        requires_new_spend=False,fixed_monthly_cost_usd=0.0,sunk_or_already_committed=True,allocation_basis_tasks_per_month=None,
        quota_units_monthly=None,quota_units_remaining=None,unit_name="task",marginal_cost_per_unit_usd=0.0,units_per_task=1.0,
        electricity_per_task_usd=.05,external_api_per_task_usd=0.0,retry_failure_expected_cost_usd=.01,maintenance_minutes_per_task=0.0,
        human_time_value_per_hour_usd=10.0,opportunity_cost_per_task_usd=0.0,latency_seconds=2.0,reliability_probability=.99,
        quality_probability=.99,max_parallelism=2,rate_limit_per_minute=60.0,notes="reference")


def task(gross=5.0):
    return TaskEconomics(task_id="t1",required_capabilities=frozenset({"extract"}),gross_payout_usd=gross,
        minimum_success_probability=.9,minimum_expected_margin_usd=.25,minimum_expected_margin_ratio=.3)


def existing(b,observed=FRESH):
    ref=asdict(b); rh=reference_backend_hash(ref); out=[]
    for i,p in enumerate(CRITICAL_PARAMETERS):
        out.append(make_evidence(evidence_id=f"e{i}",backend_id=b.backend_id,parameter=p,value=ref[p],source_kind="measured_local",
            source_ref=f"fixture:{p}",observed_at=observed,max_age_seconds=3600,reference_hash=rh,source_content_digest="a"*64))
    return tuple(out)


def measured(b,parameter,value,*,observed=FRESH,evidence_id="m"):
    return make_evidence(evidence_id=evidence_id,backend_id=b.backend_id,parameter=parameter,value=value,source_kind="measured_local",
        source_ref=f"receipt:{parameter}",observed_at=observed,max_age_seconds=3600,reference_hash=reference_backend_hash(asdict(b)),
        source_content_digest="b"*64)


def feedback(b,records,*,state="measured_feedback_ready",backend_id=None):
    return CalibrationFeedback(state=state,reasons=(),backend_id=backend_id or b.backend_id,receipt_hash="r"*64,evidence_records=tuple(records),
        runtime_evidence_emitted=any(x.parameter=="latency_seconds" for x in records),
        electricity_evidence_emitted=any(x.parameter=="electricity_per_task_usd" for x in records),total_incremental_cost_observed_usd=None)


def test_stale_feedback_stays_planning_only():
    b=backend(); r=merge_verified_feedback(b,existing(b),feedback(b,[measured(b,"latency_seconds",1.0,observed=STALE)]),task(),now=NOW)
    assert r.state=="planning_only" and r.routing is None


def test_backend_mismatch_fails_closed():
    b=backend(); r=merge_verified_feedback(b,existing(b),feedback(b,[measured(b,"latency_seconds",1.0)],backend_id="other"),task(),now=NOW)
    assert r.state=="hold" and "feedback_backend_mismatch" in r.reasons


def test_duplicate_feedback_parameter_fails_closed():
    b=backend(); a=measured(b,"latency_seconds",1.0,evidence_id="a"); c=measured(b,"latency_seconds",1.1,evidence_id="c")
    r=merge_verified_feedback(b,existing(b),feedback(b,[a,c]),task(),now=NOW)
    assert r.state=="hold" and "duplicate_feedback_parameter:latency_seconds" in r.reasons


def test_runtime_only_feedback_preserves_unrelated_energy_evidence():
    b=backend(); old=existing(b); old_energy=next(x for x in old if x.parameter=="electricity_per_task_usd")
    r=merge_verified_feedback(b,old,feedback(b,[measured(b,"latency_seconds",.5)]),task(),now=NOW)
    new_energy=next(x for x in r.merged_evidence if x.parameter=="electricity_per_task_usd")
    assert r.state=="feedback_integrated_route_dry_run" and new_energy.evidence_hash==old_energy.evidence_hash
    assert r.replaced_parameters==("latency_seconds",)


def test_explicit_energy_feedback_replaces_only_energy():
    b=backend(); old=existing(b); old_latency=next(x for x in old if x.parameter=="latency_seconds")
    r=merge_verified_feedback(b,old,feedback(b,[measured(b,"electricity_per_task_usd",.02)]),task(),now=NOW)
    new_energy=next(x for x in r.merged_evidence if x.parameter=="electricity_per_task_usd"); new_latency=next(x for x in r.merged_evidence if x.parameter=="latency_seconds")
    assert new_energy.value==.02 and new_latency.evidence_hash==old_latency.evidence_hash and r.replaced_parameters==("electricity_per_task_usd",)


def test_measured_cost_delta_can_turn_viable_route_into_hold():
    b=backend(); old=existing(b); att=attest_resource_profile(asdict(b),old,now=NOW)
    before=route_task_with_attested_resources(task(gross=1.0),[b],[att]); assert before.state=="route_dry_run"
    r=merge_verified_feedback(b,old,feedback(b,[measured(b,"electricity_per_task_usd",.90)]),task(gross=1.0),now=NOW)
    assert r.state=="feedback_integrated_hold" and r.routing.state=="hold"
    d=routing_delta(before,r.routing); assert d["before_marginal_cost_usd"]<d["after_marginal_cost_usd"]
