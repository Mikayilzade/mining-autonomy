import pytest

import i182_external_meter_energy_bridge as i182


def _session(**overrides):
    base = dict(
        meter_source_ref="meter:wall-socket-serial-ABC123",
        meter_source_digest="a" * 64,
        meter_scope="whole_system_ac_input",
        exclusive_pc_load_confirmed=True,
        same_cumulative_counter_confirmed=True,
        reading_unit="kwh",
        reading_before=12.500,
        reading_after=12.525,
        task_count=100,
        session_ref="owned-pc-run-2026-08-24T10-45Z",
    )
    base.update(overrides)
    return i182.ExternalMeterSession(**base)


def test_kwh_session_converts_to_joules_and_i166_fields():
    result = i182.bridge_external_meter(_session())
    assert result.state == "EXTERNAL_METER_ENERGY_FIELDS_READY"
    assert result.i166_energy_fields_ready is True
    assert result.energy_before_joules == pytest.approx(45_000_000.0)
    assert result.energy_after_joules == pytest.approx(45_090_000.0)
    assert result.energy_delta_joules == pytest.approx(90_000.0)
    assert result.energy_kwh_per_task == pytest.approx(0.00025)
    fields = i182.i166_energy_fields(result)
    assert set(fields) == {"energy_before_joules", "energy_after_joules", "energy_task_count", "energy_source_ref"}
    assert fields["energy_task_count"] == 100
    assert fields["energy_source_ref"].startswith("external-meter:owned-pc-run-")
    assert result.meter_read_performed is False
    assert result.evidence_invented is False


def test_wh_and_joule_units_are_supported_without_inference():
    wh = i182.bridge_external_meter(_session(reading_unit="wh", reading_before=100.0, reading_after=125.0))
    joule = i182.bridge_external_meter(_session(reading_unit="joule", reading_before=10.0, reading_after=3610.0))
    assert wh.energy_delta_joules == pytest.approx(90_000.0)
    assert joule.energy_delta_joules == pytest.approx(3600.0)


def test_component_or_shared_load_meter_is_not_promoted():
    component = i182.bridge_external_meter(_session(meter_scope="gpu_component"))
    shared = i182.bridge_external_meter(_session(exclusive_pc_load_confirmed=False))
    assert component.state == "PASS_BLOCKED"
    assert "whole_system_ac_input_scope_required" in component.errors
    assert shared.state == "PASS_BLOCKED"
    assert "exclusive_pc_load_confirmation_required" in shared.errors


def test_placeholder_estimated_or_missing_provenance_is_blocked():
    placeholder = i182.bridge_external_meter(_session(meter_source_ref="example-meter"))
    estimated = i182.bridge_external_meter(_session(session_ref="estimated-session"))
    short_digest = i182.bridge_external_meter(_session(meter_source_digest="short"))
    assert "real_meter_source_ref_required" in placeholder.errors
    assert "real_session_ref_required" in estimated.errors
    assert "meter_source_digest_required" in short_digest.errors


def test_counter_reset_and_non_cumulative_or_bad_task_count_block():
    reset = i182.bridge_external_meter(_session(reading_before=12.5, reading_after=12.4))
    different_counter = i182.bridge_external_meter(_session(same_cumulative_counter_confirmed=False))
    bad_count = i182.bridge_external_meter(_session(task_count=0))
    assert "meter_counter_wrap_reset_or_negative_delta" in reset.errors
    assert "same_cumulative_counter_confirmation_required" in different_counter.errors
    assert "positive_task_count_required" in bad_count.errors


def test_zero_delta_is_not_allowed_to_claim_zero_electricity_cost():
    result = i182.bridge_external_meter(_session(reading_before=12.5, reading_after=12.5))
    assert result.state == "PASS_BLOCKED"
    assert "positive_measurable_energy_delta_required" in result.errors
    assert result.i166_energy_fields_ready is False


def test_safety_flags_remain_inert():
    result = i182.bridge_external_meter(_session())
    assert result.network_enabled is False
    assert result.credentials_used is False
    assert result.subprocess_used is False
    assert result.software_installed is False
    assert result.elevated_privileges_requested is False
    assert result.hardware_purchased is False
    assert result.ci_dispatched is False
    assert result.spend_or_value_movement is False
