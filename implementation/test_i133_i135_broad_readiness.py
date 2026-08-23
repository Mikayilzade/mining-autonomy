from dataclasses import replace

import i133_conservative_route_gate as i133
import i134_backend_evidence_acquisition_planner as i134
import i135_pre_observation_readiness_packet as i135
from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from i131_watcher_cost_budget import WatcherBudget
from resource_router import TaskEconomics, default_backend_families


def python_backend():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")


def task():
    return TaskEconomics(
        task_id="t", required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=2.0, acceptance_probability=0.95,
        dispute_probability=0.01, nonpayment_probability=0.01,
        minimum_success_probability=0.90, minimum_expected_margin_usd=0.20,
        minimum_expected_margin_ratio=0.10,
    )


def cheap_watcher():
    return WatcherBudget(
        polls_per_hour=12, polling_cost_usd=0.0, candidates_per_poll=0.5,
        dedupe_survival_probability=0.5, deterministic_survival_probability=0.5,
        ai_escalation_probability=0.1, ai_cost_per_call_usd=0.001,
        local_energy_per_poll_usd=0.00001,
    )


def test_i133_combines_stress_and_watcher_overhead():
    result=i133.assess_conservative_route(task(), python_backend(), cheap_watcher())
    assert result.watcher_daily_candidates > 0
    assert len(result.stress_margins) >= 6
    assert all(r.acquisition_overhead_per_candidate_usd >= 0 for r in result.stress_margins)
    assert result.execution_enabled is False and result.network_enabled is False


def test_i133_large_watcher_overhead_can_destroy_nominal_margin():
    expensive=replace(cheap_watcher(), polling_cost_usd=1.0)
    result=i133.assess_conservative_route(task(), python_backend(), expensive)
    assert result.state == "HOLD"
    assert any("watcher_adjusted_margin_below_threshold" in r.blockers for r in result.stress_margins)


def test_i134_prioritizes_python_local_and_isolates_support_paid_paths():
    rows=i134.plan()
    assert rows[0].backend_id == "python_local"
    sub=next(x for x in rows if x.backend_id == "subscription_assistant")
    assert sub.state == "DEFER_OR_SUPPORT_ONLY"
    assert "not_an_autonomous_api_backend" in sub.disqualifiers
    vps=next(x for x in rows if x.backend_id == "future_paid_vps")
    assert "infrastructure_rental_authorization" in vps.authorization_needed_before_execution
    assert vps.no_new_spend_evidence_work_possible is False


def measured_evidence():
    return BackendEvidence(
        backend_id="python_local", provenance_class=MEASURED,
        current_reproducible=True, non_synthetic=True, capacity_verified=True,
        policy_evidence_current=True,
    )


def test_i135_current_false_gates_hold_without_enabling_observation():
    r=i135.assess(
        runtime_receipt_current=False, backend_evidence=None, route_gate=None,
        fresh_market_policy_evidence_ready=False,
        exact_observation_authorization_present=False,
    )
    assert r.state == "HOLD"
    assert len(r.blockers) == 6
    assert r.observation_enabled is False and r.value_movement_enabled is False


def test_i135_ready_state_still_does_not_execute_observation():
    gate=i133.assess_conservative_route(task(), python_backend(), cheap_watcher())
    if not gate.conservative_route_survives:
        # make a deliberately very high value task so the integration gate itself can be tested
        high=replace(task(), gross_payout_usd=100.0, minimum_expected_margin_usd=0.01, minimum_expected_margin_ratio=0.001)
        gate=i133.assess_conservative_route(high, python_backend(), cheap_watcher())
    assert gate.conservative_route_survives
    r=i135.assess(
        runtime_receipt_current=True, backend_evidence=measured_evidence(), route_gate=gate,
        fresh_market_policy_evidence_ready=True,
        exact_observation_authorization_present=True,
    )
    assert r.state == "READY_FOR_SINGLE_READ_ONLY_OBSERVATION"
    assert r.blockers == ()
    assert r.observation_enabled is False
