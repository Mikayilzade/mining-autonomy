from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from i131_watcher_cost_budget import WatcherBudget
from i134_backend_evidence_acquisition_planner import plan
from i136_conservative_portfolio_evaluator import evaluate_portfolio
from i137_resource_fallback_ladder import choose_next
from i138_experiment_readiness_orchestrator import assess
from resource_router import TaskEconomics, default_backend_families


def task():
    return TaskEconomics(
        task_id="test-paid-task",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=5.0,
        platform_fee_rate=0.05,
        dispute_probability=0.02,
        nonpayment_probability=0.02,
        acceptance_probability=0.95,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.25,
        minimum_expected_margin_ratio=0.10,
    )


def watcher():
    return WatcherBudget(
        polls_per_hour=60,
        polling_cost_usd=0.0,
        candidates_per_poll=0.1,
        dedupe_survival_probability=0.5,
        deterministic_survival_probability=0.5,
        ai_escalation_probability=0.0,
        ai_cost_per_call_usd=0.0,
    )


def measured_python_local():
    return BackendEvidence(
        backend_id="python_local",
        provenance_class=MEASURED,
        current_reproducible=True,
        non_synthetic=True,
        capacity_verified=True,
        policy_evidence_current=True,
    )


def test_i136_requires_evidence_and_economics_together():
    backends=default_backend_families()
    result=evaluate_portfolio(task(), backends, (), {"python_local": watcher()})
    assert result.state == "HOLD"
    row=next(x for x in result.rows if x.backend_id == "python_local")
    assert row.economics_survives is True
    assert row.production_candidate is False
    assert "backend_evidence_missing" in row.evidence_blockers


def test_i136_selects_measured_deterministic_backend_when_conservative_margin_survives():
    result=evaluate_portfolio(
        task(), default_backend_families(), (measured_python_local(),),
        {"python_local": watcher()},
    )
    assert result.state == "CONSERVATIVE_PORTFOLIO_ROUTE_READY"
    assert result.selected_backend_id == "python_local"
    row=next(x for x in result.rows if x.backend_id == "python_local")
    assert row.production_candidate is True
    assert row.worst_adjusted_margin_usd is not None and row.worst_adjusted_margin_usd > 0


def test_i137_fallback_stays_inside_existing_no_spend_branches():
    steps=plan()
    first=choose_next(steps)
    assert first.state == "NEXT_NO_SPEND_EVIDENCE_BRANCH"
    assert first.selected_backend_id == "python_local"
    assert first.discovery_reopened is False

    second=choose_next(steps, attempted_backend_ids=("python_local",))
    assert second.state == "NEXT_NO_SPEND_EVIDENCE_BRANCH"
    assert second.selected_backend_id == "free_tier_ci"
    assert "python_local" in second.exhausted_no_spend_backend_ids


def test_i138_progresses_gate_by_gate_but_never_enables_action():
    portfolio=evaluate_portfolio(
        task(), default_backend_families(), (measured_python_local(),),
        {"python_local": watcher()},
    )
    fallback=choose_next(plan(), portfolio=portfolio)

    r1=assess(
        runtime_receipt_current=False, portfolio=portfolio, fallback=fallback,
        fresh_market_policy_evidence_ready=False,
        exact_observation_authorization_present=False,
    )
    assert r1.state == "RUNTIME_RECEIPT_REQUIRED"

    r2=assess(
        runtime_receipt_current=True, portfolio=portfolio, fallback=fallback,
        fresh_market_policy_evidence_ready=False,
        exact_observation_authorization_present=False,
    )
    assert r2.state == "FRESH_MARKET_POLICY_EVIDENCE_REQUIRED"

    r3=assess(
        runtime_receipt_current=True, portfolio=portfolio, fallback=fallback,
        fresh_market_policy_evidence_ready=True,
        exact_observation_authorization_present=False,
    )
    assert r3.state == "OBSERVATION_AUTHORIZATION_REQUIRED"

    r4=assess(
        runtime_receipt_current=True, portfolio=portfolio, fallback=fallback,
        fresh_market_policy_evidence_ready=True,
        exact_observation_authorization_present=True,
    )
    assert r4.state == "READY_FOR_SINGLE_READ_ONLY_OBSERVATION"
    assert r4.observation_enabled is False
    assert r4.execution_enabled is False
    assert r4.spend_enabled is False
    assert r4.value_movement_enabled is False


def test_i138_when_route_absent_selects_resource_measurement_before_market_or_auth():
    portfolio=evaluate_portfolio(task(), default_backend_families(), (), {"python_local": watcher()})
    fallback=choose_next(plan(), portfolio=portfolio)
    result=assess(
        runtime_receipt_current=False, portfolio=portfolio, fallback=fallback,
        fresh_market_policy_evidence_ready=False,
        exact_observation_authorization_present=False,
    )
    assert result.state == "MEASURE_NEXT_RESOURCE_BRANCH"
    assert result.selected_backend_id == "python_local"
    assert result.next_action == "acquire_no_spend_evidence_for:python_local"
