"""I141 integrated bounded economic-test packet.

Combines I138 readiness with an I140 read-only observation design and a conservative
portfolio decision. The result is only a manifest for a separately authorized runner.
It never performs network access, accepts paid work, spends money, or moves value.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from i136_conservative_portfolio_evaluator import ConservativePortfolioDecision
from i138_experiment_readiness_orchestrator import ExperimentReadiness
from i140_readonly_observation_design import ReadOnlyObservationPlan


@dataclass(frozen=True)
class EconomicTestPacket:
    state: str
    selected_backend_id: Optional[str]
    observation_platform: str
    planned_requests: int
    estimated_observation_incremental_cost_usd: float
    readiness_state: str
    observation_plan_state: str
    blockers: tuple[str, ...]
    success_criteria: tuple[str, ...]
    result_fields: tuple[str, ...]
    decision_after_observation: tuple[str, ...]
    observation_enabled: bool = False
    execution_enabled: bool = False
    credentials_enabled: bool = False
    paid_task_acceptance_enabled: bool = False
    spend_enabled: bool = False
    value_movement_enabled: bool = False


def build_packet(
    *,
    readiness: ExperimentReadiness,
    portfolio: ConservativePortfolioDecision,
    observation_plan: ReadOnlyObservationPlan,
) -> EconomicTestPacket:
    blockers=[]
    if readiness.state != "READY_FOR_SINGLE_READ_ONLY_OBSERVATION":
        blockers.append("experiment_readiness_not_complete")
    if portfolio.state != "CONSERVATIVE_PORTFOLIO_ROUTE_READY" or not portfolio.selected_backend_id:
        blockers.append("current_conservative_portfolio_route_absent")
    if readiness.selected_backend_id != portfolio.selected_backend_id:
        blockers.append("readiness_portfolio_backend_mismatch")
    if observation_plan.state != "PLAN_READY_FOR_SEPARATE_AUTHORIZED_RUNNER":
        blockers.append("read_only_observation_plan_not_ready")
    if observation_plan.planned_requests <= 0:
        blockers.append("observation_request_budget_empty")
    if observation_plan.estimated_incremental_cost_usd < 0:
        blockers.append("negative_observation_cost_invalid")

    return EconomicTestPacket(
        state="READY_FOR_SEPARATELY_AUTHORIZED_READONLY_ECONOMIC_TEST" if not blockers else "HOLD",
        selected_backend_id=portfolio.selected_backend_id,
        observation_platform=observation_plan.platform,
        planned_requests=observation_plan.planned_requests,
        estimated_observation_incremental_cost_usd=observation_plan.estimated_incremental_cost_usd,
        readiness_state=readiness.state,
        observation_plan_state=observation_plan.state,
        blockers=tuple(dict.fromkeys(blockers)),
        success_criteria=(
            "all_requests_remain_public_read_only_and_within_current_policy_limits",
            "request_cap_and_interval_are_respected",
            "stable_dedupe_keys_prevent_double_counting",
            "at_least_one_current_machine_executable_opportunity_or_explicit_zero-demand result_is_measured",
            "public_payout_fee_and_availability_fields_are_captured_when_exposed",
            "resource_route_remains_conservative_positive_after_observation_overhead",
            "no_task_is_accepted_submitted_or_settled",
        ),
        result_fields=(
            "requests_attempted",
            "requests_succeeded",
            "unique_opportunities_seen",
            "machine_executable_eligible_opportunities",
            "duplicates_filtered",
            "public_payout_samples_usd",
            "public_fee_samples_usd",
            "observation_latency_seconds",
            "parse_failures",
            "policy_rate_limit_or_access_stop_reason",
            "estimated_fill_or_arrival_rate_from_observed_window",
            "conservative_margin_samples_after_resource_and_watcher_cost",
            "evidence_window_start_utc",
            "evidence_window_end_utc",
        ),
        decision_after_observation=(
            "if_no_eligible_demand_then_keep_candidate_unproven_and_extend_only_under_new_authorization",
            "if_margin_nonpositive_then_reject_or_deprioritize_route",
            "if_positive_read_only_economics_then_design_small_real_task_test_without_implying_permission_to_accept_work",
            "real_task_acceptance_credentials_spend_or_value_movement_still_require_separate_explicit_authorization",
        ),
    )


def payload(packet: EconomicTestPacket) -> dict:
    body=asdict(packet)
    body.update({
        "schema":"mining-autonomy/i141-economic-test-packet/v1",
        "run":"I141",
        "production_observation_performed":False,
        "network_access_performed":False,
        "task_acceptance_performed":False,
        "credentials_used":False,
        "spend_or_value_movement":False,
    })
    return body
