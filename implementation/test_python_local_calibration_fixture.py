import json
from datetime import datetime, timezone

import pytest

from evaluator import CapabilityProfile
from python_local_calibration_fixture import (
    BENCHMARK_ID, EXPECTED_OUTPUT_DIGEST, benchmark_transform,
    build_python_local_plan, replay_python_local_transcript,
    replay_transcript_through_i055, run_python_local_fixture,
    transcript_from_json, transcript_to_json,
)
from resource_evidence_adapter import ExplicitDeclaration
from resource_router import default_backend_families

NOW = datetime(2026, 8, 21, 2, 40, tzinfo=timezone.utc)
NOW_ISO = NOW.isoformat()
POLICY = dict(
    rights_status="confirmed", tos_status="confirmed",
    automation_allowed="allowed", source_data_permission="confirmed",
)

def ref():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")

def payload():
    return {
        "id": "t-i056", "title": "extract data", "bounty_usd": 5.0,
        "currency": "USD", "skills": ["extract"], "observed_at": NOW_ISO,
        "metadata": dict(
            POLICY, estimated_input_tokens=1000, estimated_output_tokens=1000,
            estimated_duration_seconds=60, estimate_confidence=.9,
            external_cost_cap_usd=0,
        ),
    }

def test_fixed_benchmark_is_deterministic_and_has_stable_digest():
    a = benchmark_transform()
    b = benchmark_transform()
    assert a == b
    assert len(EXPECTED_OUTPUT_DIGEST) == 64
    assert BENCHMARK_ID == "python-local-fixed-json-transform-v1"

def test_runner_is_opt_in_and_never_runs_by_default():
    with pytest.raises(RuntimeError, match="benchmark_runner_opt_in_required"):
        run_python_local_fixture(ref())

def test_opted_in_runner_emits_inert_portable_transcript():
    transcript = run_python_local_fixture(ref(), enabled=True, repetitions=10)
    assert len(transcript.observations) == 10
    assert all(x.execution_succeeded and x.quality_passed for x in transcript.observations)
    assert all(x.output_digest == EXPECTED_OUTPUT_DIGEST for x in transcript.observations)
    assert transcript.max_parallelism_observed == 1
    assert transcript.rate_limit_per_minute_observed is None
    assert transcript.network_enabled is False
    assert transcript.credentials_used is False
    assert transcript.spend_performed is False
    assert transcript.value_movement_enabled is False

def test_json_round_trip_and_replay_verify_exact_i053_digest():
    transcript = run_python_local_fixture(ref(), enabled=True)
    raw = transcript_to_json(transcript)
    replay = replay_python_local_transcript(ref(), raw)
    assert transcript_from_json(raw) == transcript
    assert replay.verified is True
    assert replay.probe_summary.transcript_digest == transcript.i053_transcript_digest
    measured = replay.probe_summary.measured_parameters
    assert set(measured) == {
        "currently_available", "programmatic_access", "latency_seconds",
        "reliability_probability", "quality_probability", "max_parallelism",
    }
    assert "electricity_per_task_usd" not in measured
    assert "quota_units_remaining" not in measured
    assert "fixed_monthly_cost_usd" not in measured

def test_tampered_portable_transcript_fails_closed():
    raw = json.loads(transcript_to_json(run_python_local_fixture(ref(), enabled=True)))
    raw["observations"][0]["output_digest"] = "0" * 64
    with pytest.raises(ValueError, match="transcript_output_digest_mismatch"):
        replay_python_local_transcript(ref(), json.dumps(raw))

def test_reference_backend_binding_is_exact():
    transcript = run_python_local_fixture(ref(), enabled=True)
    raw = json.loads(transcript_to_json(transcript))
    raw["reference_backend_hash"] = "f" * 64
    with pytest.raises(ValueError, match="transcript_reference_hash_mismatch"):
        replay_python_local_transcript(ref(), json.dumps(raw))

def test_replay_through_i055_stays_hold_without_accounting_energy_evidence():
    transcript = run_python_local_fixture(ref(), enabled=True)
    packet = replay_transcript_through_i055(
        ref(), transcript_to_json(transcript),
        probe_observed_at_utc=NOW_ISO, now=NOW,
        platform="payanagent", task_payload=payload(),
        demand_evidence_class="open_paid_request",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert packet.routed_task.upstream_state == "accept_dry_run"
    assert packet.calibration_state == "planning_only"
    assert packet.state == "hold"
    assert "electricity_per_task_usd" in packet.missing_parameters
    assert "fixed_monthly_cost_usd" in packet.missing_parameters
    assert packet.execution_enabled is False
    assert packet.network_enabled is False
    assert packet.value_movement_enabled is False

def test_declarations_do_not_override_probe_derived_fields():
    transcript = run_python_local_fixture(ref(), enabled=True)
    declaration = ExplicitDeclaration(
        "latency_seconds", 999.0, NOW_ISO, 86400, "fixture:bad-override"
    )
    with pytest.raises(ValueError, match="duplicate_parameter_input:latency_seconds"):
        replay_transcript_through_i055(
            ref(), transcript_to_json(transcript),
            probe_observed_at_utc=NOW_ISO, now=NOW,
            platform="payanagent", task_payload=payload(),
            demand_evidence_class="open_paid_request",
            declarations=(declaration,), capabilities=CapabilityProfile({"extract"}),
        )
