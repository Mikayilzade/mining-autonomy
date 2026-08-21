from dataclasses import asdict, replace
from datetime import datetime, timezone

from evaluator import CapabilityProfile
from attested_execution_bridge import observe_and_route_with_attested_resources
from feedback_attested_observation import apply_feedback_to_attested_observation, feedback_attested_task_record
from receipt_replay_calibration import CalibrationFeedback
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile, make_evidence, reference_backend_hash
from resource_router import ExecutionBackend

NOW = datetime(2026, 8, 21, 9, 30, tzinfo=timezone.utc)
OBSERVED = "2026-08-21T09:25:00Z"
POLICY = dict(rights_status="confirmed", tos_status="confirmed", automation_allowed="allowed", source_data_permission="confirmed")


def backend(backend_id, electricity):
    return ExecutionBackend(backend_id=backend_id, family="local", capabilities=frozenset({"extract"}), automation_role="autonomous",
        programmatic_access=True, policy_allowed=True, currently_available=True, requires_credentials=False, requires_paid_account=False,
        requires_new_spend=False, fixed_monthly_cost_usd=0.0, sunk_or_already_committed=True, allocation_basis_tasks_per_month=None,
        quota_units_monthly=None, quota_units_remaining=None, unit_name="task", marginal_cost_per_unit_usd=0.0, units_per_task=1.0,
        electricity_per_task_usd=electricity, external_api_per_task_usd=0.0, retry_failure_expected_cost_usd=0.01,
        maintenance_minutes_per_task=0.0, human_time_value_per_hour_usd=10.0, opportunity_cost_per_task_usd=0.0,
        latency_seconds=2.0, reliability_probability=0.99, quality_probability=0.99, max_parallelism=2,
        rate_limit_per_minute=60.0, notes="reference")


def evidence_bundle(b):
    ref=asdict(b); rh=reference_backend_hash(ref); out=[]
    for i,p in enumerate(CRITICAL_PARAMETERS):
        out.append(make_evidence(evidence_id=f"{b.backend_id}-{i}", backend_id=b.backend_id, parameter=p, value=ref[p],
            source_kind="measured_local", source_ref=f"fixture:{b.backend_id}:{p}", observed_at=OBSERVED, max_age_seconds=3600,
            reference_hash=rh, source_content_digest=("a" if b.backend_id=="target" else "b")*64))
    return tuple(out)


def attestation(b,evidence): return attest_resource_profile(asdict(b),evidence,now=NOW)


def payload():
    return {"id":"task-1","title":"extract data","bounty_usd":5.0,"currency":"USD","skills":["extract"],"observed_at":OBSERVED,
        "metadata":{**POLICY,"estimated_input_tokens":1000,"estimated_output_tokens":1000,"estimated_duration_seconds":120,
                    "estimate_confidence":.95,"external_cost_cap_usd":0}}


def setup_original():
    target=backend("target",.40); alternate=backend("alternate",.10)
    te,ae=evidence_bundle(target),evidence_bundle(alternate); ta,aa=attestation(target,te),attestation(alternate,ae)
    original=observe_and_route_with_attested_resources("payanagent",payload(),demand_evidence_class="open_paid_request",
        capabilities=CapabilityProfile({"extract"}),reference_backends=[target,alternate],attestations=[ta,aa])
    assert original.state=="route_dry_run" and original.selected_backend_id=="alternate"
    return original,target,alternate,te,ae,ta,aa


def feedback_for(target,*,value=.01,state="measured_feedback_ready"):
    e=make_evidence(evidence_id="receipt-energy",backend_id=target.backend_id,parameter="electricity_per_task_usd",value=value,
        source_kind="measured_local",source_ref="receipt:r-1",observed_at="2026-08-21T09:29:00Z",max_age_seconds=3600,
        reference_hash=reference_backend_hash(asdict(target)),source_content_digest="c"*64)
    return CalibrationFeedback(state=state,reasons=(),backend_id=target.backend_id,receipt_hash="r"*64,evidence_records=(e,),
        runtime_evidence_emitted=False,electricity_evidence_emitted=True,total_incremental_cost_observed_usd=value)


def test_measured_resource_fact_can_change_ranking_only_after_reattestation():
    original,target,alternate,te,ae,ta,aa=setup_original()
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te,"alternate":ae},feedback=feedback_for(target),now=NOW)
    assert u.state=="feedback_refreshed_route_dry_run" and u.before_selected_backend_id=="alternate" and u.after_selected_backend_id=="target"
    assert u.replaced_parameters==("electricity_per_task_usd",) and u.before_target_evidence_bundle_hash==ta.evidence_bundle_hash
    assert u.after_target_evidence_bundle_hash!=ta.evidence_bundle_hash
    assert u.route_delta["before_marginal_cost_usd"]>u.route_delta["after_marginal_cost_usd"]


def test_original_market_observation_economics_and_demand_are_preserved_exactly():
    original,target,alternate,te,ae,ta,aa=setup_original(); before=asdict(original)
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te},feedback=feedback_for(target),now=NOW)
    assert asdict(u.original_observation)==before and u.original_observation.demand_evidence_class=="open_paid_request"
    assert u.original_observation.task_economics==original.task_economics


def test_task_identity_mismatch_fails_closed_before_feedback():
    original,target,alternate,te,ae,ta,aa=setup_original(); bad=replace(original,external_id="different-task")
    u=apply_feedback_to_attested_observation(bad,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te},feedback=feedback_for(target),now=NOW)
    assert u.state=="hold" and "original_task_identity_mismatch" in u.reasons and u.refreshed_routing is None


def test_prior_attestation_evidence_provenance_mismatch_fails_closed():
    original,target,alternate,te,ae,ta,aa=setup_original(); wrong=list(te)
    wrong[0]=make_evidence(evidence_id="wrong",backend_id="target",parameter=CRITICAL_PARAMETERS[0],value=False,
        source_kind="measured_local",source_ref="fixture:wrong",observed_at=OBSERVED,max_age_seconds=3600,
        reference_hash=reference_backend_hash(asdict(target)),source_content_digest="d"*64)
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":wrong},feedback=feedback_for(target),now=NOW)
    assert u.state=="hold" and "target_evidence_provenance_mismatch" in u.reasons


def test_unverified_feedback_fails_closed():
    original,target,alternate,te,ae,ta,aa=setup_original()
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te},feedback=feedback_for(target,state="hold"),now=NOW)
    assert u.state=="hold" and any(x.startswith("feedback_merge_not_routable") for x in u.reasons)
    assert "feedback_not_verified_ready" in u.reasons


def test_feedback_backend_without_exact_reference_fails_closed():
    original,target,alternate,te,ae,ta,aa=setup_original(); fb=replace(feedback_for(target),backend_id="missing")
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te},feedback=fb,now=NOW)
    assert u.state=="hold" and "feedback_backend_without_reference" in u.reasons


def test_record_remains_inert_and_hash_bound():
    original,target,alternate,te,ae,ta,aa=setup_original()
    u=apply_feedback_to_attested_observation(original,reference_backends=[target,alternate],attestations=[ta,aa],
        existing_evidence_by_backend={"target":te},feedback=feedback_for(target),now=NOW)
    r=feedback_attested_task_record(u)
    assert u.provenance_binding_hash is not None and r["dry_run_only"] is True
    assert r["execution_enabled"] is False and r["network_enabled"] is False and r["credentials_enabled"] is False
    assert r["submission_enabled"] is False and r["value_movement_enabled"] is False
