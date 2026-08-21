from dataclasses import replace
from datetime import datetime, timezone
import json
import pytest

from local_calibration_session import (
    EnergySlot, build_session_bundle, replay_session_bundle, session_to_json,
)
from python_local_calibration_fixture import run_python_local_fixture, transcript_to_json
from resource_router import default_backend_families
from session_attestation_import import import_session_attestation


def ref():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")


def base_session(observed="2026-08-21T04:00:00Z"):
    r = ref()
    transcript = run_python_local_fixture(r, enabled=True, repetitions=3)
    return build_session_bundle(r, transcript_to_json(transcript), collector_observed_at_utc=observed)


def complete_session(observed="2026-08-21T04:00:00Z"):
    s = base_session(observed)
    report = replay_session_bundle(ref(), session_to_json(s))
    values = {
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "fixed_monthly_cost_usd": 0.0,
        "sunk_or_already_committed": True,
        "quota_units_remaining": None,
        "rate_limit_per_minute": 120.0,
    }
    missing = set(report.missing_parameters)
    slots = tuple(
        replace(x, value=values[x.parameter], observed_at=observed, source_ref=f"session-declaration:{x.parameter}")
        if x.parameter in missing else x
        for x in s.declaration_slots
    )
    energy = s.energy_slot
    if "electricity_per_task_usd" in missing:
        energy = EnergySlot(
            energy_kwh_per_task=0.001,
            tariff_usd_per_kwh=0.12,
            observed_at=observed,
            source_ref="local-meter-fixture",
            source_content_digest="1234567890abcdef1234567890abcdef",
        )
    return replace(s, declaration_slots=slots, energy_slot=energy)


def test_incomplete_session_never_becomes_attestation_candidate():
    s = base_session()
    out = import_session_attestation(ref(), session_to_json(s), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))
    assert out.state == "planning_only_incomplete_session"
    assert out.attestation is None
    assert out.attestation_candidate is False
    assert out.execution_enabled is False


def test_complete_current_session_becomes_declared_attestation_candidate():
    s = complete_session()
    out = import_session_attestation(ref(), session_to_json(s), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))
    assert out.state == "attestation_candidate_declared"
    assert out.attestation_state == "calibrated_declared"
    assert out.attestation_candidate is True
    assert out.attestation_evidence_bundle_hash
    assert "system_probe" in out.source_kinds
    assert "user_declared" in out.source_kinds
    assert "measured_local" in out.source_kinds


def test_stale_complete_session_fails_at_i050_boundary():
    s = complete_session("2026-08-19T04:00:00Z")
    out = import_session_attestation(ref(), session_to_json(s), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))
    assert out.state == "planning_only_attestation_rejected"
    assert out.attestation_state == "planning_only"
    assert out.attestation_candidate is False
    assert any("stale_evidence" in reason for reason in out.reasons)


def test_session_and_transcript_provenance_are_preserved_exactly():
    s = complete_session()
    out = import_session_attestation(ref(), session_to_json(s), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))
    assert out.session_digest == s.immutable_session_digest
    assert out.transcript_file_digest == s.transcript_file_digest
    assert len(out.transcript_digest) >= 16
    assert all(len(h) >= 16 for h in out.evidence_hashes)


def test_tampered_transcript_fails_before_attestation():
    s = complete_session()
    data = json.loads(session_to_json(s))
    data["transcript_json"] += " "
    with pytest.raises(ValueError, match="transcript_file_digest_mismatch"):
        import_session_attestation(ref(), json.dumps(data), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))


def test_wrong_reference_backend_fails_closed():
    s = complete_session()
    other = replace(ref(), latency_seconds=ref().latency_seconds + 1)
    with pytest.raises(ValueError):
        import_session_attestation(other, session_to_json(s), now=datetime(2026, 8, 21, 4, 5, tzinfo=timezone.utc))


def test_now_timezone_requirement_is_strict():
    s = complete_session()
    with pytest.raises(ValueError, match="now_must_be_utc"):
        import_session_attestation(ref(), session_to_json(s), now=datetime(2026, 8, 21, 4, 5))
