from dataclasses import replace
import pytest
import resource_router as rr


def backend(): return rr.default_backend_families()[0]
def task(**kw):
    base = rr.TaskEconomics(task_id='i192', required_capabilities=frozenset({'extract','validate'}), gross_payout_usd=1.0, minimum_expected_margin_usd=0.0, minimum_expected_margin_ratio=0.0)
    return replace(base, **kw)

@pytest.mark.parametrize('field,value', [
    ('minimum_expected_margin_usd', -0.01),
    ('minimum_expected_margin_ratio', -0.01),
])
def test_negative_minimum_margin_policy_cannot_weaken_positive_economics(field, value):
    with pytest.raises(ValueError, match=f'{field}_must_be_nonnegative'):
        rr.quote_backend(task(**{field:value}), backend())

@pytest.mark.parametrize('field,value', [
    ('minimum_expected_margin_usd', True),
    ('minimum_expected_margin_ratio', False),
    ('minimum_expected_margin_usd', float('nan')),
    ('minimum_expected_margin_ratio', float('inf')),
])
def test_invalid_minimum_margin_policy_fails_closed(field, value):
    with pytest.raises(ValueError, match=f'{field}_must_be_finite_number'):
        rr.quote_backend(task(**{field:value}), backend())

def test_zero_expected_margin_is_not_routable_even_with_zero_thresholds():
    b = replace(backend(), electricity_per_task_usd=0.0, external_api_per_task_usd=0.990025, retry_failure_expected_cost_usd=0.0, maintenance_minutes_per_task=0.0, opportunity_cost_per_task_usd=0.0)
    q = rr.quote_backend(task(), b)
    assert q.expected_margin_before_fixed_allocation_usd == 0.0
    assert q.planning_state == 'hold'
    assert 'insufficient_conservative_expected_margin' in q.planning_reasons
    d = rr.route_task(task(), (b,))
    assert d.state == 'hold' and d.selected_backend_id is None


def test_positive_margin_still_routes_and_sunk_fixed_cost_is_not_charged_per_task():
    b = replace(backend(), fixed_monthly_cost_usd=20.0, sunk_or_already_committed=True)
    positive = task(minimum_expected_margin_usd=0.01, minimum_expected_margin_ratio=0.01)
    q = rr.quote_backend(positive, b)
    assert q.allocated_fixed_cost_per_task_usd == 0.0
    assert q.expected_margin_before_fixed_allocation_usd > 0
    assert q.planning_state == 'eligible_dry_run'
    d = rr.route_task(positive, (b,))
    assert d.state == 'route_dry_run' and d.execution_enabled is False


def test_cheapest_positive_margin_backend_remains_selected():
    cheap = replace(backend(), backend_id='cheap', electricity_per_task_usd=0.01)
    costly = replace(backend(), backend_id='costly', electricity_per_task_usd=0.20)
    positive = task(minimum_expected_margin_usd=0.01, minimum_expected_margin_ratio=0.01)
    d = rr.route_task(positive, (costly, cheap))
    assert d.selected_backend_id == 'cheap'
    assert d.execution_enabled is False
