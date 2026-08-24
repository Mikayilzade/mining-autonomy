import i170_owned_pc_control_evidence_policy as i170


def _hybrid_plan():
    return {
        "requires_credentials": "system_probe",
        "requires_paid_account": "system_probe",
        "requires_new_spend": "system_probe",
        "fixed_monthly_cost_usd": "user_declared",
        "sunk_or_already_committed": "user_declared",
        "quota_units_remaining": "system_probe",
        "rate_limit_per_minute": "system_probe",
    }


def test_requirements_cover_all_controls_once():
    rows = i170.requirements()
    assert tuple(row.parameter for row in rows) == i170.CONTROL_PARAMETERS
    assert len({row.parameter for row in rows}) == 7
    assert set(i170.INTERFACE_REPRODUCIBLE_PARAMETERS).isdisjoint(i170.OWNER_ACCOUNTING_PARAMETERS)
    assert set(i170.INTERFACE_REPRODUCIBLE_PARAMETERS) | set(i170.OWNER_ACCOUNTING_PARAMETERS) == set(i170.CONTROL_PARAMETERS)


def test_hybrid_owner_accounting_plan_is_explicitly_not_strict_i123_ready():
    result = i170.evaluate_source_plan(_hybrid_plan())
    assert result.state == "HYBRID_ACCOUNTING_POLICY_REVIEW_REQUIRED"
    assert result.errors == ()
    assert result.strict_i123_measured_reproducible_possible_without_policy_change is False
    assert result.narrow_hybrid_policy_review_required is True
    assert result.i050_change_performed is False
    assert result.i123_change_performed is False
    assert result.i123_promotion_allowed is False


def test_provider_first_party_accounting_can_fit_existing_strict_source_classes():
    plan = _hybrid_plan()
    plan["fixed_monthly_cost_usd"] = "provider_first_party"
    plan["sunk_or_already_committed"] = "provider_first_party"
    result = i170.evaluate_source_plan(plan)
    assert result.state == "SOURCE_PLAN_COMPLETE"
    assert result.errors == ()
    assert result.strict_i123_measured_reproducible_possible_without_policy_change is True
    assert result.narrow_hybrid_policy_review_required is False


def test_accounting_facts_cannot_be_relabelled_system_probe():
    plan = _hybrid_plan()
    plan["fixed_monthly_cost_usd"] = "system_probe"
    plan["sunk_or_already_committed"] = "measured_local"
    result = i170.evaluate_source_plan(plan)
    assert result.state == "PASS_BLOCKED"
    assert "source_kind_not_allowed:fixed_monthly_cost_usd:system_probe" in result.errors
    assert "source_kind_not_allowed:sunk_or_already_committed:measured_local" in result.errors


def test_interface_controls_cannot_fall_back_to_user_declaration():
    plan = _hybrid_plan()
    plan["requires_credentials"] = "user_declared"
    plan["quota_units_remaining"] = "user_declared"
    result = i170.evaluate_source_plan(plan)
    assert result.state == "PASS_BLOCKED"
    assert "source_kind_not_allowed:requires_credentials:user_declared" in result.errors
    assert "source_kind_not_allowed:quota_units_remaining:user_declared" in result.errors


def test_missing_or_unknown_control_parameter_fails_closed():
    plan = _hybrid_plan()
    plan.pop("rate_limit_per_minute")
    plan["surprise"] = "system_probe"
    result = i170.evaluate_source_plan(plan)
    assert result.state == "PASS_BLOCKED"
    assert "missing_source_plan:rate_limit_per_minute" in result.errors
    assert "unknown_control_parameters:surprise" in result.errors
