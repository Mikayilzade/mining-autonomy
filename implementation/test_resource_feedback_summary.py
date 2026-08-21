from dataclasses import asdict, replace
from hashlib import sha256
import json
import pytest
from resource_feedback_history import ResourceFeedbackHistoryEntry
from resource_feedback_summary import summarize_resource_feedback_history, verify_resource_feedback_history_snapshot

def h(value): return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
def entry(sequence=1, previous='GENESIS', before='a'*64, after='b'*64, target='python_local', parameter='electricity_per_task_usd', observed='2026-08-21T10:40:00Z', before_sel='api', after_sel='python_local', evidence='e'*64, receipt='r'*64):
    kwargs=dict(sequence=sequence,task_id='task-1',platform='payanagent',external_id='task-1',target_backend_id=target,previous_entry_hash=previous,original_observation_hash='1'*64,before_routing_hash=before,after_routing_hash=after,before_target_evidence_bundle_hash='2'*64,after_target_evidence_bundle_hash='3'*64,feedback_receipt_hash=receipt,feedback_evidence_hashes=(evidence,),feedback_parameter_times=((parameter,observed),),replaced_parameters=(parameter,),before_selected_backend_id=before_sel,after_selected_backend_id=after_sel,update_provenance_binding_hash='4'*64,appended_at='2026-08-21T10:45:00Z',entry_hash='')
    row=ResourceFeedbackHistoryEntry(**kwargs); return replace(row,entry_hash=h(row.hash_body()))
def next_entry(prev, **kw):
    return entry(sequence=prev.sequence+1,previous=prev.entry_hash,before=prev.after_routing_hash,**kw)

def test_empty_history_is_verified_but_not_planner_fact():
    s=summarize_resource_feedback_history([])
    assert s.state=='empty_verified_history' and s.history_tip_hash=='GENESIS'
    assert verify_resource_feedback_history_snapshot(s)

def test_latest_parameter_reference_is_provenance_only_not_value():
    e1=entry(); e2=next_entry(e1,after='c'*64,observed='2026-08-21T10:42:00Z',evidence='f'*64,receipt='s'*64,before_sel='python_local',after_sel='python_local')
    s=summarize_resource_feedback_history([e1,e2])
    ref=s.backend_states[0].latest_parameters[0]
    assert ref.observed_at=='2026-08-21T10:42:00Z' and ref.evidence_hashes==('f'*64,)
    assert s.backend_states[0].parameter_values_stored_in_history is False
    assert 'parameter_values_not_stored_in_i064_history' in s.limitations

def test_backend_switch_and_oscillation_are_derived_not_guessed():
    e1=entry(before_sel='api',after_sel='python_local')
    e2=next_entry(e1,after='c'*64,observed='2026-08-21T10:41:00Z',evidence='f'*64,receipt='s'*64,before_sel='python_local',after_sel='api')
    e3=next_entry(e2,after='d'*64,observed='2026-08-21T10:42:00Z',evidence='9'*64,receipt='t'*64,before_sel='api',after_sel='python_local')
    s=summarize_resource_feedback_history([e1,e2,e3],parameter_churn_threshold=4)
    assert s.selected_backend_switch_count==3
    assert s.selected_backend_oscillation_detected is True
    assert 'selected_backend_oscillation' in s.anomaly_indicators

def test_parameter_churn_is_counted_without_averaging_values():
    e1=entry(); e2=next_entry(e1,after='c'*64,observed='2026-08-21T10:41:00Z',evidence='f'*64,receipt='s'*64,before_sel='python_local',after_sel='python_local'); e3=next_entry(e2,after='d'*64,observed='2026-08-21T10:42:00Z',evidence='9'*64,receipt='t'*64,before_sel='python_local',after_sel='python_local')
    s=summarize_resource_feedback_history([e1,e2,e3],parameter_churn_threshold=3)
    assert s.parameter_churn_indicators==('frequent_parameter_updates:python_local:electricity_per_task_usd:3',)

def test_invalid_history_withholds_all_derived_state():
    e=entry(); bad=replace(e,entry_hash='0'*64)
    s=summarize_resource_feedback_history([bad])
    assert s.state=='hold_invalid_history' and s.backend_states==() and s.current_selected_backend_id is None
    assert any('history_entry_hash_mismatch' in x for x in s.anomaly_indicators)

def test_stale_parameter_regression_surfaces_as_verified_history_failure():
    e1=entry(observed='2026-08-21T10:42:00Z'); e2=next_entry(e1,after='c'*64,observed='2026-08-21T10:41:00Z',evidence='f'*64,receipt='s'*64,before_sel='python_local',after_sel='python_local')
    s=summarize_resource_feedback_history([e1,e2])
    assert s.state=='hold_invalid_history'
    assert any('history_stale_parameter_regression' in x for x in s.reasons)

def test_snapshot_hash_detects_tamper():
    s=summarize_resource_feedback_history([entry()]); assert verify_resource_feedback_history_snapshot(s)
    assert not verify_resource_feedback_history_snapshot(replace(s,current_selected_backend_id='tampered'))

def test_multi_parameter_entry_preserves_set_binding_without_guessing_order():
    e=entry()
    base=replace(e, feedback_evidence_hashes=('e'*64,'f'*64), feedback_parameter_times=(("electricity_per_task_usd","2026-08-21T10:40:00Z"),("latency_seconds","2026-08-21T10:40:00Z")), replaced_parameters=("electricity_per_task_usd","latency_seconds"), entry_hash='')
    e=replace(base,entry_hash=h(base.hash_body()))
    s=summarize_resource_feedback_history([e])
    refs={r.parameter:r for r in s.backend_states[0].latest_parameters}
    assert refs['latency_seconds'].evidence_hashes==('e'*64,'f'*64)
    assert refs['latency_seconds'].evidence_binding_precision=='entry_set_only'

def test_invalid_churn_threshold_rejected():
    with pytest.raises(ValueError): summarize_resource_feedback_history([],parameter_churn_threshold=1)
