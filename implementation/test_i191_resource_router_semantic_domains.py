from dataclasses import replace
import pytest
import resource_router as rr


def backend(): return rr.default_backend_families()[0]
def task(): return rr.TaskEconomics(task_id='i191', required_capabilities=frozenset({'extract','validate'}), gross_payout_usd=1.0, minimum_expected_margin_usd=0.01, minimum_expected_margin_ratio=0.01)

@pytest.mark.parametrize('field,value', [('reliability_probability',1.0001),('reliability_probability',-0.01),('quality_probability',2.0)])
def test_backend_probabilities_out_of_domain_fail_closed(field,value):
    with pytest.raises(ValueError, match='must_be_probability'):
        rr.quote_backend(task(), replace(backend(), **{field:value}))

@pytest.mark.parametrize('field,value', [('acceptance_probability',2.0),('acceptance_probability',-0.1),('dispute_probability',-1.0),('nonpayment_probability',1.1),('minimum_success_probability',2.0),('platform_fee_rate',1.1)])
def test_task_probabilities_and_fractional_fee_rate_fail_closed(field,value):
    with pytest.raises(ValueError, match='must_be_probability'):
        rr.quote_backend(replace(task(), **{field:value}), backend())

@pytest.mark.parametrize('field', ['marginal_cost_per_unit_usd','units_per_task','electricity_per_task_usd','external_api_per_task_usd','retry_failure_expected_cost_usd','maintenance_minutes_per_task','human_time_value_per_hour_usd','opportunity_cost_per_task_usd','fixed_monthly_cost_usd','latency_seconds'])
def test_negative_backend_economics_fail_closed(field):
    with pytest.raises(ValueError, match='must_be_nonnegative'):
        rr.quote_backend(task(), replace(backend(), **{field:-0.01}))

@pytest.mark.parametrize('field', ['gross_payout_usd','platform_fee_usd','transaction_fee_usd','gas_fee_usd','withdrawal_conversion_fee_usd'])
def test_negative_task_money_fields_fail_closed(field):
    with pytest.raises(ValueError, match='must_be_nonnegative'):
        rr.quote_backend(replace(task(), **{field:-0.01}), backend())

@pytest.mark.parametrize('field', ['quota_units_monthly','quota_units_remaining','rate_limit_per_minute'])
def test_negative_optional_capacity_fields_fail_closed(field):
    with pytest.raises(ValueError, match='must_be_nonnegative'):
        rr.quote_backend(task(), replace(backend(), **{field:-1.0}))

def test_negative_allocation_basis_fails_closed_when_fixed_cost_requires_allocation():
    b=replace(backend(), fixed_monthly_cost_usd=1.0, sunk_or_already_committed=False, allocation_basis_tasks_per_month=-1.0)
    with pytest.raises(ValueError, match='allocation_basis_tasks_per_month_must_be_positive'):
        rr.quote_backend(task(), b)

def test_valid_route_is_unchanged_and_execution_stays_disabled():
    q=rr.quote_backend(task(), backend())
    assert q.planning_state=='eligible_dry_run'
    assert q.action_enabled is False
    d=rr.route_task(task(), (backend(),))
    assert d.state=='route_dry_run' and d.execution_enabled is False
