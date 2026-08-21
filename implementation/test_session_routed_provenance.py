from dataclasses import replace
from datetime import datetime, timezone

import pytest

from evaluator import CapabilityProfile
from local_calibration_session import EnergySlot, build_session_bundle, replay_session_bundle, session_to_json
from python_local_calibration_fixture import run_python_local_fixture, transcript_to_json
from resource_router import default_backend_families
from session_routed_provenance import route_python_local_session, session_routed_record, verify_session_routed_record

NOW = datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc)
OBSERVED = "2026-08-21T04:00:00Z"
POLICY = dict(rights_status="confirmed", tos_status="confirmed", automation_allowed="allowed", source_data_permission="confirmed")


def ref():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")


def complete_session():
    r = ref()
    transcript = run_python_local_fixture(r, enabled=True, repetitions=3)
    session = build_session_bundle(r, transcript_to_json(transcript), collector_observed_at_utc=OBSERVED)
    report = replay_session_bundle(r, session_to_json(session))
    values = {
        "requires_credentials": False, "requires_paid_account": False, "requires_new_spend": False,
        "fixed_monthly_cost_usd": 0.0, "sunk_or_already_committed": True,
        "quota_units_remaining": None, "rate_limit_per_minute": 120.0,
    }
    missing = set(report.missing_parameters)
    slots = tuple(
        replace(slot, value=values[slot.parameter], observed_at=OBSERVED, source_ref=f"session-declaration:{slot.parameter}")
        if slot.parameter in missing else slot for slot in session.declaration_slots
    )
    energy = session.energy_slot
    if "electricity_per_task_usd" in missing:
        energy = EnergySlot(0.001, 0.12, OBSERVED, "local-meter-fixture", "1" * 64)
    return replace(session, declaration_slots=slots, energy_slot=energy)


def incomplete_session():
    r = ref()
    transcript = run_python_local_fixture(r, enabled=True, repetitions=3)
    return build_session_bundle(r, transcript_to_json(transcript), collector_observed_at_utc=OBSERVED)


def payload(title="extract data"):
    return {
        "id": "t-i059", "title": title, "bounty_usd": 5.0, "currency": "USD",
        "skills": ["extract"], "observed_at": OBSERVED,
        "metadata": {**POLICY, "estimated_input_tokens": 1000, "estimated_output_tokens": 1000,
                     "estimated_duration_seconds": 120, "estimate_confidence": .9, "external_cost_cap_usd": 0},
    }


def route(session, demand="open_paid_request", title="extract data"):
    return route_python_local_session(
        ref(), session_to_json(session), now=NOW, platform="payanagent", task_payload=payload(title),
        demand_evidence_class=demand, capabilities=CapabilityProfile({"extract"}),
    )


def test_complete_session_selected_route_carries_exact_session_and_i050_provenance():
    session = complete_session(); out = route(session)
    assert out.state == "route_dry_run" and out.selected_backend_id == "python_local"
    assert out.session_digest == session.immutable_session_digest
    assert out.selected_evidence_bundle_hash == out.attestation_evidence_bundle_hash
    assert out.selected_calibration_state == out.attestation_state and out.provenance_verified is True
    assert verify_session_routed_record(session_routed_record(out)) is True


def test_upstream_demand_hold_remains_authoritative_even_with_complete_session():
    out = route(complete_session(), demand="listing_only")
    assert out.routed_task.upstream_state == "hold" and out.state == "hold"
    assert out.selected_backend_id is None and out.provenance_verified is False


def test_incomplete_session_cannot_become_selected_resource():
    out = route(incomplete_session())
    assert out.routed_task.upstream_state == "accept_dry_run" and out.state == "hold"
    assert "session_attestation_not_routable" in out.reasons and out.selected_backend_id is None


def test_prohibited_task_is_not_rescued_by_calibrated_session():
    out = route(complete_session(), title="spam automation")
    assert out.routed_task.upstream_state == "reject" and out.state == "reject" and out.selected_backend_id is None


def test_serialized_session_digest_tampering_fails_binding_verification():
    record = session_routed_record(route(complete_session())); record["session_digest"] = "0" * 64
    with pytest.raises(ValueError, match="record_provenance_binding_hash_mismatch"):
        verify_session_routed_record(record)


def test_serialized_selected_evidence_bundle_drift_fails_closed():
    record = session_routed_record(route(complete_session())); record["selected_evidence_bundle_hash"] = "f" * 64
    with pytest.raises(ValueError, match="record_selected_evidence_bundle_drift"):
        verify_session_routed_record(record)


def test_serialized_inertness_cannot_be_widened():
    record = session_routed_record(route(complete_session())); record["network_enabled"] = True
    with pytest.raises(ValueError, match="record_inertness_violation"):
        verify_session_routed_record(record)


def test_non_python_local_reference_is_rejected():
    other = next(x for x in default_backend_families() if x.backend_id != "python_local")
    with pytest.raises(ValueError, match="i059_python_local_only"):
        route_python_local_session(other, "{}", now=NOW, platform="payanagent", task_payload=payload(), demand_evidence_class="open_paid_request")
