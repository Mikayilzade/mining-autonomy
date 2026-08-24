import i166_user_pc_real_evidence_gate as i166


def _real_fixture():
    return {
        "measured_available_hours_per_day": 8.0,
        "availability_source_ref": "local-log:availability-2026-08-24",
        "energy_before_joules": 1000.0,
        "energy_after_joules": 4600.0,
        "energy_task_count": 10,
        "energy_source_ref": "local-meter:session-2026-08-24",
        "tariff_usd_per_kwh": 0.1,
        "tariff_source_ref": "utility-bill:applicable-tariff-2026-08",
        "opportunity_cost_usd_per_hour": 0.01,
        "opportunity_cost_source_ref": "user-declaration:pc-occupation-cost-2026-08-24",
    }


def test_template_is_null_and_not_evidence():
    template = i166.blank_template()
    assert set(template) == set(i166.i165.EXTERNAL_FIELDS)
    assert all(value is None for value in template.values())


def test_fixture_and_placeholder_provenance_is_rejected():
    raw = _real_fixture()
    raw["tariff_source_ref"] = "test-fixture:tariff"
    result = i166.validate_external_facts(raw, confirm_user_owned_pc=True)
    assert result.state == "PASS_BLOCKED"
    assert "nonproduction_provenance:tariff_source_ref" in result.errors
    assert result.i165_invocation_allowed is False
    assert result.accepted_external_facts == {}


def test_ownership_confirmation_is_mandatory():
    result = i166.validate_external_facts(_real_fixture(), confirm_user_owned_pc=False)
    assert result.state == "PASS_BLOCKED"
    assert "explicit_user_owned_pc_confirmation_required" in result.errors
    assert result.i165_invocation_allowed is False


def test_partial_energy_group_fails_closed():
    raw = _real_fixture()
    raw.pop("energy_after_joules")
    result = i166.validate_external_facts(raw, confirm_user_owned_pc=True)
    assert result.state == "PASS_BLOCKED"
    assert any(error.startswith("partial_external_group:energy_before_joules") for error in result.errors)


def test_complete_well_formed_real_label_fixture_passes_gate_only():
    result = i166.validate_external_facts(_real_fixture(), confirm_user_owned_pc=True)
    assert result.state == "REAL_EXTERNAL_EVIDENCE_ACCEPTED"
    assert result.i165_invocation_allowed is True
    assert result.accepted_external_facts == _real_fixture()
    assert result.production_route_created is False
    assert result.spend_or_value_movement is False


def test_invalid_ranges_fail_closed():
    raw = _real_fixture()
    raw["measured_available_hours_per_day"] = 25
    raw["energy_after_joules"] = 999
    raw["energy_task_count"] = 0
    raw["tariff_usd_per_kwh"] = -1
    raw["opportunity_cost_usd_per_hour"] = -1
    result = i166.validate_external_facts(raw, confirm_user_owned_pc=True)
    assert result.state == "PASS_BLOCKED"
    assert "invalid_measured_available_hours_per_day" in result.errors
    assert "energy_counter_wrap_reset_or_negative_delta" in result.errors
    assert "invalid_energy_task_count" in result.errors
    assert "invalid_tariff_usd_per_kwh" in result.errors
    assert "invalid_opportunity_cost_usd_per_hour" in result.errors
