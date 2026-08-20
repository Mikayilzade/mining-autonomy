from dataclasses import asdict
from datetime import datetime, timezone

from evaluator import CapabilityProfile
from attested_execution_bridge import observe_and_route_with_attested_resources, attested_task_record
from resource_router import ExecutionBackend
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile, make_evidence, reference_backend_hash

NOW = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
POLICY = dict(rights_status="confirmed", tos_status="confirmed", automation_allowed="allowed", source_data_permission="confirmed")


def backend():
    return ExecutionBackend(backend_id="local", family="synthetic", capabilities=frozenset({"extract"}), automation_role="autonomous", programmatic_access=True, policy_allowed=True, currently_available=True, requires_credentials=False, requires_paid_account=False, requires_new_spend=False, fixed_monthly_cost_usd=0.0, sunk_or_already_committed=True, allocation_basis_tasks_per_month=None, quota_units_monthly=None, quota_units_remaining=None, unit_name="task", marginal_cost_per_unit_usd=0.0, units_per_task=1.0, electricity_per_task_usd=0.01, external_api_per_task_usd=0.0, retry_failure_expected_cost_usd=0.01, maintenance_minutes_per_task=0.0, human_time_value_per_hour_usd=10.0, opportunity_cost_per_task_usd=0.0, latency_seconds=1.0, reliability_probability=0.99, quality_probability=0.99, max_parallelism=1, rate_limit_per_minute=60.0, notes="reference")


def attestation_for(b):
    ref=asdict(b); rh=reference_backend_hash(ref); records=[]
    for i,p in enumerate(CRITICAL_PARAMETERS):
        records.append(make_evidence(evidence_id=f"e{i}", backend_id=b.backend_id, parameter=p, value=ref[p], source_kind="measured_local", source_ref=f"fixture:{p}", observed_at="2026-08-20T23:55:00Z", max_age_seconds=3600, reference_hash=rh, source_content_digest="a"*64))
    return attest_resource_profile(ref, records, now=NOW)


def payload(title="extract data"):
    return {"id":"t1","title":title,"bounty_usd":5.0,"currency":"USD","skills":["extract"],"observed_at":"2026-08-21T00:00:00Z","metadata":{**POLICY,"estimated_input_tokens":1000,"estimated_output_tokens":1000,"estimated_duration_seconds":120,"estimate_confidence":.9,"external_cost_cap_usd":0}}


def test_upstream_hold_never_reaches_resource_gate():
    b=backend(); a=attestation_for(b)
    r=observe_and_route_with_attested_resources("payanagent", payload(), demand_evidence_class="listing_only", capabilities=CapabilityProfile({"extract"}), reference_backends=[b], attestations=[a])
    assert r.state=="hold" and r.upstream_gate_passed is False and r.attested_routing is None


def test_upstream_reject_never_reaches_resource_gate():
    b=backend(); a=attestation_for(b)
    r=observe_and_route_with_attested_resources("payanagent", payload("spam automation"), demand_evidence_class="open_paid_request", capabilities=CapabilityProfile({"extract"}), reference_backends=[b], attestations=[a])
    assert r.state=="reject" and r.attested_routing is None


def test_accepted_task_without_resource_evidence_is_held():
    b=backend()
    r=observe_and_route_with_attested_resources("payanagent", payload(), demand_evidence_class="open_paid_request", capabilities=CapabilityProfile({"extract"}), reference_backends=[b])
    assert r.upstream_state=="accept_dry_run" and r.state=="hold"
    assert "resource_evidence_missing" in r.reasons and r.selected_backend_id is None


def test_accepted_task_with_reproducible_attestation_routes_dry_run():
    b=backend(); a=attestation_for(b)
    r=observe_and_route_with_attested_resources("payanagent", payload(), demand_evidence_class="open_paid_request", capabilities=CapabilityProfile({"extract"}), reference_backends=[b], attestations=[a])
    assert r.state=="route_dry_run" and r.selected_backend_id=="local"
    assert r.selected_calibration_state=="calibrated_reproducible"
    assert r.selected_evidence_bundle_hash==a.evidence_bundle_hash
    assert r.resource_gate_passed is True


def test_combined_record_remains_inert():
    b=backend(); a=attestation_for(b)
    r=observe_and_route_with_attested_resources("payanagent", payload(), demand_evidence_class="open_paid_request", capabilities=CapabilityProfile({"extract"}), reference_backends=[b], attestations=[a])
    rec=attested_task_record(r)
    assert rec["dry_run_only"] is True and rec["execution_enabled"] is False
    assert rec["network_enabled"] is False and rec["value_movement_enabled"] is False
