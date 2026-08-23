from dataclasses import replace

from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from i131_watcher_cost_budget import WatcherBudget
from i136_conservative_portfolio_evaluator import evaluate_portfolio
from i138_experiment_readiness_orchestrator import ExperimentReadiness
from i140_readonly_observation_design import ObservationDesignInput, design_observation
from i141_economic_test_packet import build_packet
from resource_router import TaskEconomics, default_backend_families


def task():
    return TaskEconomics(
        task_id="broad-test-task",
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
        polls_per_hour=12,
        polling_cost_usd=0.0,
        candidates_per_poll=0.2,
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


def good_design_input():
    return ObservationDesignInput(
        platform="test-platform",
        source_ref="https://example.invalid/public-feed",
        policy_evidence_ref="fixture:current-policy",
        public_read_only_allowed=True,
        credentials_required=False,
        paid_account_required=False,
        captcha_or_human_challenge_required=False,
        geography_allowed=True,
        requested_poll_interval_seconds=60,
        minimum_allowed_interval_seconds=30,
        planned_duration_seconds=600,
        max_requests=10,
        hard_request_cap=20,
        expected_candidates_per_request=0.2,
        external_request_cost_usd=0.0,
        local_processing_cost_per_request_usd=0.0001,
        ai_escalation_probability=0.0,
        ai_cost_per_call_usd=0.0,
    )


def ready(portfolio):
    return ExperimentReadiness(
        state="READY_FOR_SINGLE_READ_ONLY_OBSERVATION",
        selected_backend_id=portfolio.selected_backend_id,
        next_action="separately_authorized_runner_only",
        runtime_receipt_current=True,
        conservative_route_ready=True,
        fresh_market_policy_evidence_ready=True,
        exact_observation_authorization_present=True,
        fallback_state="CURRENT_ROUTE_EXISTS",
        blockers=(),
    )


def test_i139_generator_evidence_is_not_lost_and_duplicate_backend_definitions_fail_closed():
    result=evaluate_portfolio(
        task(), default_backend_families(),
        (x for x in (measured_python_local(),)),
        {"python_local": watcher()},
    )
    assert result.state == "CONSERVATIVE_PORTFOLIO_ROUTE_READY"
    assert result.selected_backend_id == "python_local"

    backends=default_backend_families()
    try:
        evaluate_portfolio(task(), (backends[0], backends[0]), (), {"python_local": watcher()})
    except ValueError as exc:
        assert "duplicate_backend_definition" in str(exc)
    else:
        raise AssertionError("duplicate backend definitions must fail closed")


def test_i140_builds_bounded_no_spend_plan_but_never_enables_network():
    plan=design_observation(good_design_input())
    assert plan.state == "PLAN_READY_FOR_SEPARATE_AUTHORIZED_RUNNER"
    assert plan.planned_requests == 10
    assert plan.network_enabled is False
    assert plan.credentials_enabled is False
    assert plan.spend_enabled is False
    assert plan.task_acceptance_enabled is False
    assert "never_accept_or_submit_paid_work" in plan.stop_rules


def test_i140_rejects_rate_limit_bypass_paid_request_and_captcha_paths():
    base=good_design_input()
    bad=replace(
        base,
        requested_poll_interval_seconds=5,
        minimum_allowed_interval_seconds=30,
        external_request_cost_usd=0.01,
        captcha_or_human_challenge_required=True,
    )
    plan=design_observation(bad)
    assert plan.state == "HOLD"
    assert "requested_polling_faster_than_allowed_limit" in plan.blockers
    assert "external_paid_request_cost_not_allowed_in_no_spend_observation" in plan.blockers
    assert "captcha_or_human_challenge_present" in plan.blockers


def test_i141_requires_both_full_readiness_and_ready_bounded_observation_plan():
    portfolio=evaluate_portfolio(
        task(), default_backend_families(), (measured_python_local(),),
        {"python_local": watcher()},
    )
    plan=design_observation(good_design_input())
    packet=build_packet(readiness=ready(portfolio), portfolio=portfolio, observation_plan=plan)
    assert packet.state == "READY_FOR_SEPARATELY_AUTHORIZED_READONLY_ECONOMIC_TEST"
    assert packet.observation_enabled is False
    assert packet.paid_task_acceptance_enabled is False
    assert packet.spend_enabled is False
    assert packet.value_movement_enabled is False

    not_ready=replace(ready(portfolio), state="FRESH_MARKET_POLICY_EVIDENCE_REQUIRED")
    held=build_packet(readiness=not_ready, portfolio=portfolio, observation_plan=plan)
    assert held.state == "HOLD"
    assert "experiment_readiness_not_complete" in held.blockers
