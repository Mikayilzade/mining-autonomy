from dataclasses import asdict
from datetime import datetime, timezone

from evaluator import CapabilityProfile
from resource_calibration_acquisition import ProbeObservation, evaluate_probe_transcript, build_local_no_spend_plan
from resource_evidence_adapter import EnergyMeasurement, ExplicitDeclaration
from resource_profile_evidence import CRITICAL_PARAMETERS
from resource_router import default_backend_families
from calibration_routing_packet import build_calibration_routing_packet, calibration_routing_record

NOW = datetime(2026, 8, 21, 1, 45, tzinfo=timezone.utc)
NOW_ISO = NOW.isoformat()
DIGEST = "d" * 64
POLICY = dict(rights_status="confirmed", tos_status="confirmed", automation_allowed="allowed", source_data_permission="confirmed")

def ref():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")

def probe(reference):
    plan = build_local_no_spend_plan(asdict(reference), benchmark_id="fixed-json-transform-v1", expected_output_digest=DIGEST)
    rows = [ProbeObservation(f"r{i}", 0.01 + i/10000, True, DIGEST, True) for i in range(10)]
    return evaluate_probe_transcript(plan.probe_contract, rows, max_parallelism_observed=2, rate_limit_per_minute_observed=120.0)

def declarations(observed_at=NOW_ISO):
    values = {"requires_credentials": False, "requires_paid_account": False, "requires_new_spend": False, "fixed_monthly_cost_usd": 0.0, "sunk_or_already_committed": True, "quota_units_remaining": None}
    return [ExplicitDeclaration(k, v, observed_at, 86400, f"fixture:{k}") for k, v in values.items()]

def energy(observed_at=NOW_ISO):
    return EnergyMeasurement(0.0001, 0.10, observed_at, 86400, "fixture:energy", "e"*64)

def payload(title="extract data"):
    return {"id":"t1", "title":title, "bounty_usd":5.0, "currency":"USD", "skills":["extract"], "observed_at":NOW_ISO, "metadata":dict(POLICY, estimated_input_tokens=1000, estimated_output_tokens=1000, estimated_duration_seconds=60, estimate_confidence=.9, external_cost_cap_usd=0)}

def build_complete(**overrides):
    r = ref()
    args = dict(reference_backend=r, benchmark_id="fixed-json-transform-v1", expected_output_digest=DIGEST, now=NOW, platform="payanagent", task_payload=payload(), demand_evidence_class="open_paid_request", probe_summary=probe(r), probe_observed_at_utc=NOW_ISO, declarations=declarations(), energy_measurement=energy(), capabilities=CapabilityProfile({"extract"}))
    args.update(overrides)
    return build_calibration_routing_packet(**args)

def test_complete_packet_preserves_calibration_and_bundle_hash_end_to_end():
    packet = build_complete()
    assert packet.evidence_build.complete_for_attestation is True
    assert packet.missing_parameters == ()
    assert set(packet.emitted_parameters) == set(CRITICAL_PARAMETERS)
    assert packet.calibration_state == "calibrated_declared"
    assert packet.evidence_bundle_hash
    assert packet.state == "route_dry_run"
    assert packet.routed_task.selected_evidence_bundle_hash == packet.evidence_bundle_hash
    assert packet.routed_task.selected_calibration_state == packet.calibration_state

def test_missing_declarations_and_energy_narrow_upstream_accept_to_hold():
    r = ref()
    packet = build_calibration_routing_packet(r, benchmark_id="fixed-json-transform-v1", expected_output_digest=DIGEST, now=NOW, platform="payanagent", task_payload=payload(), demand_evidence_class="open_paid_request", probe_summary=probe(r), probe_observed_at_utc=NOW_ISO, capabilities=CapabilityProfile({"extract"}))
    assert packet.routed_task.upstream_state == "accept_dry_run"
    assert packet.calibration_state == "planning_only"
    assert packet.missing_parameters
    assert packet.state == "hold"
    assert packet.routed_task.selected_backend_id is None
    assert "resource_calibration_evidence_incomplete" in packet.reasons

def test_stale_declared_evidence_fails_closed_to_hold():
    old = "2026-08-01T00:00:00+00:00"
    packet = build_complete(declarations=declarations(old))
    assert packet.calibration_state == "planning_only"
    assert packet.state == "hold"
    assert packet.routed_task.selected_backend_id is None

def test_upstream_prohibited_task_is_never_rescued_by_complete_calibration():
    packet = build_complete(task_payload=payload(title="spam automation"))
    assert packet.routed_task.upstream_gate_passed is False
    assert packet.state == "reject"
    assert packet.routed_task.attested_routing is None

def test_probe_timestamp_is_mandatory_and_never_replaced_by_current_time():
    r = ref()
    try:
        build_calibration_routing_packet(r, benchmark_id="fixed-json-transform-v1", expected_output_digest=DIGEST, now=NOW, platform="payanagent", task_payload=payload(), demand_evidence_class="open_paid_request", probe_summary=probe(r), capabilities=CapabilityProfile({"extract"}))
    except ValueError as exc:
        assert str(exc) == "probe_observed_at_utc_required"
    else:
        raise AssertionError("expected explicit probe time failure")

def test_record_is_inert_even_for_complete_route():
    record = calibration_routing_record(build_complete())
    assert record["dry_run_only"] is True
    assert record["execution_enabled"] is False
    assert record["network_enabled"] is False
    assert record["value_movement_enabled"] is False
