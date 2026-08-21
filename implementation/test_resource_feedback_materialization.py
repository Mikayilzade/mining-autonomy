from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
import json

from resource_feedback_materialization import materialize_resource_feedback_snapshot, verify_resource_evidence_materialization
from resource_feedback_summary import BackendEvidenceState, LatestParameterEvidenceRef, ResourceFeedbackHistorySnapshot
from resource_profile_evidence import CRITICAL_PARAMETERS, attest_resource_profile, make_evidence, reference_backend_hash

NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)

def h(value): return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def reference():
    return {"backend_id":"python_local","currently_available":True,"programmatic_access":True,"requires_credentials":False,"requires_paid_account":False,"requires_new_spend":False,"fixed_monthly_cost_usd":0.0,"sunk_or_already_committed":True,"quota_units_remaining":None,"electricity_per_task_usd":0.01,"latency_seconds":1.0,"reliability_probability":0.995,"quality_probability":0.995,"max_parallelism":4,"rate_limit_per_minute":120.0}

def evidence_set(*, observed="2026-08-21T11:30:00Z", source_kind="measured_local", overrides=None):
    values={"currently_available":True,"programmatic_access":True,"requires_credentials":False,"requires_paid_account":False,"requires_new_spend":False,"fixed_monthly_cost_usd":0.0,"sunk_or_already_committed":True,"quota_units_remaining":None,"electricity_per_task_usd":0.02,"latency_seconds":2.5,"reliability_probability":0.995,"quality_probability":0.995,"max_parallelism":4,"rate_limit_per_minute":120.0}
    values.update(overrides or {}); rh=reference_backend_hash(reference())
    return [make_evidence(evidence_id=f"e-{p}-{observed}",backend_id="python_local",parameter=p,value=values[p],source_kind=source_kind,source_ref=f"fixture://{p}/{observed}",observed_at=observed,max_age_seconds=7200,reference_hash=rh,source_content_digest=None if source_kind=="user_declared" else "a"*64) for p in CRITICAL_PARAMETERS]

def bundle(records):
    a=attest_resource_profile(reference(),records,now=NOW); assert a.state in {"calibrated_reproducible","calibrated_declared"}; return a.evidence_bundle_hash

def snapshot(refs, *, last_sequence=1):
    state=BackendEvidenceState("python_local",tuple(refs),last_sequence,last_sequence,max(r.observed_at for r in refs))
    kwargs=dict(state="verified_history_snapshot",reasons=(),history_length=last_sequence,history_tip_hash="t"*64,task_id="task-1",platform="payanagent",external_id="task-1",current_selected_backend_id="python_local",latest_routing_hash="r"*64,backend_states=(state,),routing_transitions=(),selected_backend_switch_count=0,selected_backend_oscillation_detected=False,parameter_churn_indicators=(),anomaly_indicators=(),limitations=("parameter_values_not_stored_in_i064_history",),snapshot_hash="")
    draft=ResourceFeedbackHistorySnapshot(**kwargs); return replace(draft,snapshot_hash=h(draft.hash_body()))

def ref(parameter,evidence_hashes,bundle_hash,*,sequence=1,precision="exact_single_parameter",observed="2026-08-21T11:30:00Z"):
    return LatestParameterEvidenceRef("python_local",parameter,observed,tuple(evidence_hashes),precision,sequence,f"{sequence}"*64,f"q{sequence}"*32,bundle_hash)

def test_exact_single_parameter_materializes_full_anchor_profile():
    records=evidence_set(); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh)])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    assert result.state=="materialized_reproducible" and result.quantitative_values_complete
    assert result.backend_profiles[0].calibrated_values["latency_seconds"]==2.5
    assert verify_resource_evidence_materialization(result)

def test_multi_parameter_set_binding_resolves_from_bundle_contents():
    records=evidence_set(); bh=bundle(records); latency=next(x for x in records if x.parameter=="latency_seconds"); energy=next(x for x in records if x.parameter=="electricity_per_task_usd"); hashes=(latency.evidence_hash,energy.evidence_hash)
    s=snapshot([ref("latency_seconds",hashes,bh,precision="entry_set_only"),ref("electricity_per_task_usd",hashes,bh,precision="entry_set_only")])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    values={x.parameter:x.value for x in result.backend_profiles[0].latest_parameter_values}; assert values=={"electricity_per_task_usd":0.02,"latency_seconds":2.5}

def test_missing_bound_bundle_fails_closed_and_exposes_no_numeric_profile():
    records=evidence_set(); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh)])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={},now=NOW)
    assert result.state=="hold_unresolved_evidence" and result.backend_profiles==(); assert any("missing_evidence_bundle" in r for r in result.reasons)

def test_missing_hash_inside_bound_bundle_fails_closed():
    records=evidence_set(); bh=bundle(records); s=snapshot([ref("latency_seconds",["f"*64],bh)])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    assert any("bound_evidence_hash_missing_from_bundle" in r for r in result.reasons)

def test_tampered_evidence_recomputes_to_different_bundle_and_fails():
    records=evidence_set(); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); tampered=list(records); tampered[tampered.index(target)]=replace(target,value=999.0); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh)])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:tampered},now=NOW)
    assert result.state=="hold_unresolved_evidence"

def test_stale_bundle_fails_current_materialization():
    records=evidence_set(observed="2026-08-21T08:00:00Z"); old_now=datetime(2026,8,21,8,30,tzinfo=timezone.utc); bh=attest_resource_profile(reference(),records,now=old_now).evidence_bundle_hash; target=next(x for x in records if x.parameter=="latency_seconds"); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh,observed="2026-08-21T08:00:00Z")])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    assert any("bundle_not_currently_calibrated" in r for r in result.reasons)

def test_reference_backend_identity_mismatch_fails_closed():
    records=evidence_set(); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh)]); wrong=dict(reference()); wrong["backend_id"]="other"
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":wrong},evidence_bundles={bh:records},now=NOW)
    assert any("reference_backend_identity_mismatch" in r for r in result.reasons)

def test_latest_old_parameter_must_be_carried_into_new_anchor_bundle():
    first=evidence_set(observed="2026-08-21T11:00:00Z"); b1=bundle(first); old_energy=next(x for x in first if x.parameter=="electricity_per_task_usd")
    second=evidence_set(observed="2026-08-21T11:30:00Z",overrides={"electricity_per_task_usd":0.03}); b2=bundle(second); new_latency=next(x for x in second if x.parameter=="latency_seconds")
    s=snapshot([ref("electricity_per_task_usd",[old_energy.evidence_hash],b1,sequence=1,observed="2026-08-21T11:00:00Z"),ref("latency_seconds",[new_latency.evidence_hash],b2,sequence=2,observed="2026-08-21T11:30:00Z")],last_sequence=2)
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={b1:first,b2:second},now=NOW)
    assert any("latest_evidence_not_carried_into_anchor_bundle" in r for r in result.reasons)

def test_invalid_snapshot_hash_fails_before_evidence_resolution():
    records=evidence_set(); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); s=replace(snapshot([ref("latency_seconds",[target.evidence_hash],bh)]),snapshot_hash="bad")
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    assert "snapshot_hash_invalid" in result.reasons and result.backend_profiles==()

def test_user_declared_bundle_stays_visibly_non_reproducible():
    records=evidence_set(source_kind="user_declared"); bh=bundle(records); target=next(x for x in records if x.parameter=="latency_seconds"); s=snapshot([ref("latency_seconds",[target.evidence_hash],bh)])
    result=materialize_resource_feedback_snapshot(s,reference_backends={"python_local":reference()},evidence_bundles={bh:records},now=NOW)
    assert result.state=="materialized_with_declarations" and result.backend_profiles[0].state=="materialized_declared"
    assert result.execution_enabled is False and result.network_enabled is False
