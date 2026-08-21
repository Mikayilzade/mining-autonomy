import json
import pytest
from local_calibration_session import DECLARATION_PARAMETERS,build_session_bundle,replay_session_bundle,session_to_json
from python_local_calibration_fixture import run_python_local_fixture,transcript_to_json
from resource_router import default_backend_families

def ref(): return next(x for x in default_backend_families() if x.backend_id=="python_local")
def bundle():
    r=ref(); t=run_python_local_fixture(r,enabled=True,repetitions=10)
    return build_session_bundle(r,transcript_to_json(t),collector_observed_at_utc="2026-08-21T03:45:00Z")

def test_session_binds_transcript_and_collector_time():
    s=bundle(); assert s.backend_id=="python_local"; assert len(s.transcript_file_digest)==64; assert len(s.immutable_session_digest)==64; assert not s.network_enabled

def test_template_only_contains_non_probe_declarations():
    s=bundle(); assert tuple(x.parameter for x in s.declaration_slots)==DECLARATION_PARAMETERS; assert "latency_seconds" not in DECLARATION_PARAMETERS; assert s.energy_slot.energy_kwh_per_task is None

def test_unfilled_bundle_replays_planning_only():
    report=replay_session_bundle(ref(),session_to_json(bundle())); assert report.transcript_verified; assert report.state=="planning_only"; assert not report.complete_for_attestation; assert "electricity_per_task_usd" in report.missing_parameters; assert "latency_seconds" in report.emitted_parameters

def test_transcript_tamper_fails_closed():
    d=json.loads(session_to_json(bundle())); d["transcript_json"]+=" "
    with pytest.raises(ValueError,match="transcript_file_digest_mismatch"): replay_session_bundle(ref(),json.dumps(d))

def test_collector_time_tamper_breaks_session_identity():
    d=json.loads(session_to_json(bundle())); d["collector_observed_at_utc"]="2026-08-21T03:46:00Z"
    with pytest.raises(ValueError,match="immutable_session_digest_mismatch"): replay_session_bundle(ref(),json.dumps(d))

def test_partial_declaration_rejected_not_guessed():
    d=json.loads(session_to_json(bundle())); d["declaration_slots"][0]["value"]=False
    with pytest.raises(ValueError,match="incomplete_declaration_slot"): replay_session_bundle(ref(),json.dumps(d))

def test_partial_energy_rejected_not_guessed():
    d=json.loads(session_to_json(bundle())); d["energy_slot"]["energy_kwh_per_task"]=0.0001
    with pytest.raises(ValueError,match="incomplete_energy_slot"): replay_session_bundle(ref(),json.dumps(d))

def test_non_z_time_rejected():
    r=ref(); t=run_python_local_fixture(r,enabled=True,repetitions=10)
    with pytest.raises(ValueError,match="utc_timestamp_z_required"): build_session_bundle(r,transcript_to_json(t),collector_observed_at_utc="2026-08-21T03:45:00+00:00")
