import pytest
from resource_router import (
    ExecutionBackend, TaskEconomics, WatcherPolicy,
    default_backend_families, quote_backend, route_task, validate_watcher_policy,
)


def task(**overrides):
    base = dict(
        task_id="task-1",
        required_capabilities=frozenset({"extract"}),
        gross_payout_usd=10.0,
        platform_fee_rate=0.10,
        acceptance_probability=0.95,
        dispute_probability=0.05,
        nonpayment_probability=0.02,
        minimum_success_probability=0.85,
        minimum_expected_margin_usd=0.25,
        minimum_expected_margin_ratio=0.30,
    )
    base.update(overrides)
    return TaskEconomics(**base)


def backend(backend_id="b", **overrides):
    base = dict(
        backend_id=backend_id,
        family="synthetic",
        capabilities=frozenset({"extract"}),
        automation_role="autonomous",
        programmatic_access=True,
        policy_allowed=True,
        currently_available=True,
        requires_credentials=False,
        requires_paid_account=False,
        requires_new_spend=False,
        fixed_monthly_cost_usd=0.0,
        sunk_or_already_committed=True,
        allocation_basis_tasks_per_month=None,
        quota_units_monthly=None,
        quota_units_remaining=None,
        unit_name="task",
        marginal_cost_per_unit_usd=0.0,
        units_per_task=1.0,
        electricity_per_task_usd=0.01,
        external_api_per_task_usd=0.0,
        retry_failure_expected_cost_usd=0.01,
        maintenance_minutes_per_task=0.0,
        human_time_value_per_hour_usd=10.0,
        opportunity_cost_per_task_usd=0.0,
        latency_seconds=1.0,
        reliability_probability=0.99,
        quality_probability=0.99,
        max_parallelism=1,
        rate_limit_per_minute=60.0,
        notes="synthetic",
    )
    base.update(overrides)
    return ExecutionBackend(**base)


def test_router_prefers_available_lowest_marginal_cost():
    cheap = backend("cheap", electricity_per_task_usd=0.01)
    expensive = backend("expensive", external_api_per_task_usd=0.40)
    decision = route_task(task(), [expensive, cheap])
    assert decision.state == "route_dry_run"
    assert decision.selected_backend_id == "cheap"
    assert decision.execution_enabled is False


def test_subscription_resource_is_visible_but_not_treated_as_free_api():
    profile = next(x for x in default_backend_families() if x.backend_id == "subscription_assistant")
    quote = quote_backend(task(), profile)
    assert profile.fixed_monthly_cost_usd > 0
    assert profile.sunk_or_already_committed is True
    assert profile.programmatic_access is False
    assert quote.allocated_fixed_cost_per_task_usd == 0.0
    assert quote.planning_state == "hold"
    assert "no_autonomous_programmatic_execution_path" in quote.planning_reasons


def test_credentials_backend_is_planning_only_not_live_selected():
    api = backend("api", currently_available=False, requires_credentials=True, external_api_per_task_usd=0.001)
    local = backend("local", electricity_per_task_usd=0.02)
    decision = route_task(task(), [api, local])
    api_quote = next(q for q in decision.quotes if q.backend_id == "api")
    assert api_quote.planning_state == "planning_only"
    assert "credentials_required_before_live_execution" in api_quote.live_blockers
    assert decision.selected_backend_id == "local"


def test_future_paid_vps_keeps_fixed_cost_unknown_and_needs_authorization():
    vps = backend(
        "vps", currently_available=False, requires_paid_account=True, requires_new_spend=True,
        fixed_monthly_cost_usd=12.0, sunk_or_already_committed=False,
        allocation_basis_tasks_per_month=None,
    )
    quote = quote_backend(task(), vps)
    assert quote.allocated_fixed_cost_per_task_usd is None
    assert quote.planning_state == "planning_only"
    assert "new_spend_requires_explicit_authorization" in quote.live_blockers
    assert "fixed_cost_allocation_basis_unknown" in quote.live_blockers


def test_non_sunk_fixed_cost_can_be_allocated_without_charging_full_month_per_task():
    shared = backend(
        "shared", fixed_monthly_cost_usd=30.0, sunk_or_already_committed=False,
        allocation_basis_tasks_per_month=300.0,
    )
    quote = quote_backend(task(), shared)
    assert quote.allocated_fixed_cost_per_task_usd == pytest.approx(0.10)
    assert quote.expected_margin_after_fixed_allocation_usd == pytest.approx(
        quote.expected_margin_before_fixed_allocation_usd - 0.10
    )


def test_acceptance_dispute_nonpayment_reduce_expected_revenue():
    clean = quote_backend(task(acceptance_probability=1.0, dispute_probability=0.0, nonpayment_probability=0.0), backend())
    risky = quote_backend(task(acceptance_probability=0.8, dispute_probability=0.1, nonpayment_probability=0.1), backend())
    assert risky.expected_revenue_usd < clean.expected_revenue_usd
    assert risky.expected_margin_before_fixed_allocation_usd < clean.expected_margin_before_fixed_allocation_usd


def test_quality_threshold_can_hold_cheaper_backend():
    weak = backend("weak", reliability_probability=0.99, quality_probability=0.70, electricity_per_task_usd=0.0)
    strong = backend("strong", reliability_probability=0.99, quality_probability=0.99, external_api_per_task_usd=0.10)
    decision = route_task(task(minimum_success_probability=0.90), [weak, strong])
    weak_quote = next(q for q in decision.quotes if q.backend_id == "weak")
    assert weak_quote.planning_state == "hold"
    assert "success_probability_below_threshold" in weak_quote.planning_reasons
    assert decision.selected_backend_id == "strong"


def test_quota_shortage_holds_backend():
    limited = backend("limited", quota_units_remaining=0.5, units_per_task=1.0)
    quote = quote_backend(task(), limited)
    assert quote.planning_state == "hold"
    assert "quota_insufficient" in quote.planning_reasons


def test_watcher_allows_fast_polling_when_inside_platform_limit_and_keeps_network_off():
    plan = WatcherPolicy(polling_interval_seconds=30, mode="poll")
    result = validate_watcher_policy(plan, platform_min_interval_seconds=10)
    assert result["state"] == "valid_inert_watcher_plan"
    assert result["network_enabled"] is False
    assert result["local_filtering_before_ai"] is True


def test_watcher_rejects_rate_limit_bypass_and_llm_on_every_poll():
    plan = WatcherPolicy(
        polling_interval_seconds=1,
        mode="poll",
        llm_on_every_poll=True,
        obey_platform_rate_limits=False,
        bypass_product_limits=True,
    )
    result = validate_watcher_policy(plan, platform_min_interval_seconds=10)
    assert result["state"] == "hold"
    assert "polling_faster_than_platform_limit" in result["reasons"]
    assert "llm_on_every_poll_disallowed_by_default" in result["reasons"]
    assert "rate_limit_or_product_limit_bypass" in result["reasons"]
