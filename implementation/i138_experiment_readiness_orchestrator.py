"""I138 experiment-readiness orchestrator.

Combines runtime, conservative portfolio, acquisition fallback, market/policy evidence,
and exact observation authorization into one fail-closed next-action state. This module
never performs the observation or any external/paid action.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from i136_conservative_portfolio_evaluator import ConservativePortfolioDecision
from i137_resource_fallback_ladder import FallbackChoice


@dataclass(frozen=True)
class ExperimentReadiness:
    state: str
    selected_backend_id: Optional[str]
    next_action: str
    runtime_receipt_current: bool
    conservative_route_ready: bool
    fresh_market_policy_evidence_ready: bool
    exact_observation_authorization_present: bool
    fallback_state: str
    blockers: tuple[str, ...]
    observation_enabled: bool = False
    execution_enabled: bool = False
    credentials_enabled: bool = False
    spend_enabled: bool = False
    task_acceptance_enabled: bool = False
    value_movement_enabled: bool = False


def assess(
    *,
    runtime_receipt_current: bool,
    portfolio: ConservativePortfolioDecision,
    fallback: FallbackChoice,
    fresh_market_policy_evidence_ready: bool,
    exact_observation_authorization_present: bool,
) -> ExperimentReadiness:
    route_ready = portfolio.state == "CONSERVATIVE_PORTFOLIO_ROUTE_READY" and bool(portfolio.selected_backend_id)
    blockers=[]
    if not runtime_receipt_current:
        blockers.append("exact_current_runtime_receipt_absent")
    if not route_ready:
        blockers.append("current_conservative_resource_route_absent")
    if not fresh_market_policy_evidence_ready:
        blockers.append("fresh_market_policy_evidence_absent")
    if not exact_observation_authorization_present:
        blockers.append("exact_observation_authorization_absent")

    selected = portfolio.selected_backend_id
    if not route_ready:
        selected = fallback.selected_backend_id
        if fallback.state == "NEXT_NO_SPEND_EVIDENCE_BRANCH":
            state="MEASURE_NEXT_RESOURCE_BRANCH"
            next_action=f"acquire_no_spend_evidence_for:{fallback.selected_backend_id}"
        else:
            state="HOLD_RESOURCE_EXHAUSTION_REVIEW"
            next_action="review_existing_backend_exhaustion_before_any_discovery_reopen"
    elif not runtime_receipt_current:
        state="RUNTIME_RECEIPT_REQUIRED"
        next_action="obtain_one_exact_current_runtime_receipt_without_restoring_automatic_ci"
    elif not fresh_market_policy_evidence_ready:
        state="FRESH_MARKET_POLICY_EVIDENCE_REQUIRED"
        next_action="prepare_fresh_read_only_market_policy_evidence_acquisition_under_existing_gates"
    elif not exact_observation_authorization_present:
        state="OBSERVATION_AUTHORIZATION_REQUIRED"
        next_action="request_exact_single_read_only_observation_authorization"
    else:
        state="READY_FOR_SINGLE_READ_ONLY_OBSERVATION"
        next_action="observation_remains_external_and_must_be_executed_only_by_separately_authorized_runner"

    return ExperimentReadiness(
        state=state,
        selected_backend_id=selected,
        next_action=next_action,
        runtime_receipt_current=runtime_receipt_current,
        conservative_route_ready=route_ready,
        fresh_market_policy_evidence_ready=fresh_market_policy_evidence_ready,
        exact_observation_authorization_present=exact_observation_authorization_present,
        fallback_state=fallback.state,
        blockers=tuple(blockers),
    )


def payload(result: ExperimentReadiness) -> dict:
    body=asdict(result)
    body.update({
        "schema":"mining-autonomy/i138-experiment-readiness-orchestrator/v1",
        "run":"I138",
        "production_observation_performed":False,
        "network_access_performed":False,
        "spend_or_value_movement":False,
    })
    return body
