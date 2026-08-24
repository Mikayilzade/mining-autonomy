from dataclasses import replace

import pytest

import resource_router as rr


def _backend():
    return rr.default_backend_families()[0]


def _task():
    return rr.TaskEconomics(
        task_id="i188",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=1.0,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.01,
        minimum_expected_margin_ratio=0.01,
    )


def test_valid_default_numeric_path_remains_finite_and_routable_dry_run():
    quote = rr.quote_backend(_task(), _backend())
    assert quote.planning_state == "eligible_dry_run"
    assert quote.marginal_cost_usd >= 0
    assert 0 <= quote.success_probability <= 1
    assert quote.expected_margin_before_fixed_allocation_usd > 0
    decision = rr.route_task(_task(), (_backend(),))
    assert decision.state == "route_dry_run"
    assert decision.execution_enabled is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("electricity_per_task_usd", float("nan")),
        ("external_api_per_task_usd", float("inf")),
        ("retry_failure_expected_cost_usd", float("-inf")),
        ("opportunity_cost_per_task_usd", True),
        ("maintenance_minutes_per_task", "bad"),
        ("human_time_value_per_hour_usd", float("nan")),
    ],
)
def test_nonfinite_or_nonnumeric_backend_costs_fail_closed(field, value):
    with pytest.raises(ValueError):
        rr.quote_backend(_task(), replace(_backend(), **{field: value}))


def test_backend_cost_multiplication_overflow_fails_closed():
    backend = replace(
        _backend(),
        units_per_task=1e308,
        marginal_cost_per_unit_usd=1e308,
    )
    with pytest.raises(ValueError, match="unit_cost_must_be_finite"):
        rr.quote_backend(_task(), backend)


@pytest.mark.parametrize(
    "field,value",
    [
        ("fixed_monthly_cost_usd", float("nan")),
        ("allocation_basis_tasks_per_month", float("inf")),
        ("quota_units_monthly", float("nan")),
        ("quota_units_remaining", float("inf")),
        ("latency_seconds", float("nan")),
        ("rate_limit_per_minute", float("inf")),
        ("reliability_probability", float("nan")),
        ("quality_probability", True),
    ],
)
def test_nonfinite_capacity_probability_and_fixed_fields_fail_closed(field, value):
    base = replace(
        _backend(),
        fixed_monthly_cost_usd=1.0,
        allocation_basis_tasks_per_month=100.0,
    )
    backend = replace(base, **{field: value})
    with pytest.raises(ValueError):
        rr.quote_backend(_task(), backend)


@pytest.mark.parametrize(
    "field,value",
    [
        ("gross_payout_usd", float("nan")),
        ("platform_fee_usd", float("inf")),
        ("platform_fee_rate", float("nan")),
        ("transaction_fee_usd", True),
        ("gas_fee_usd", "bad"),
        ("withdrawal_conversion_fee_usd", float("-inf")),
        ("acceptance_probability", float("nan")),
        ("dispute_probability", float("inf")),
        ("nonpayment_probability", True),
        ("minimum_success_probability", float("nan")),
        ("minimum_expected_margin_usd", float("inf")),
        ("minimum_expected_margin_ratio", float("nan")),
    ],
)
def test_nonfinite_or_nonnumeric_task_economics_fail_closed(field, value):
    with pytest.raises(ValueError):
        rr.quote_backend(replace(_task(), **{field: value}), _backend())


def test_platform_fee_multiplication_overflow_fails_closed():
    task = replace(_task(), gross_payout_usd=1e308, platform_fee_rate=1e308)
    with pytest.raises(ValueError, match="platform_rate_fee_must_be_finite"):
        rr.quote_backend(task, _backend())


def test_max_parallelism_bool_is_not_treated_as_one():
    with pytest.raises(ValueError, match="max_parallelism_must_be_integer"):
        rr.quote_backend(_task(), replace(_backend(), max_parallelism=True))


def test_watcher_interval_bool_and_invalid_platform_limit_fail_closed():
    result = rr.validate_watcher_policy(
        rr.WatcherPolicy(polling_interval_seconds=True, mode="poll"),
        platform_min_interval_seconds=-1,
    )
    assert result["state"] == "hold"
    assert "invalid_poll_interval" in result["reasons"]
    assert "invalid_platform_min_interval" in result["reasons"]
