"""I137 deterministic fallback ladder over existing execution backends.

Consumes I134 acquisition priorities plus optional I136 portfolio results to decide
what evidence branch to work next. It does not discover new markets and does not
perform acquisition, network access, credential use, spend, or execution.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Optional

from i134_backend_evidence_acquisition_planner import AcquisitionStep
from i136_conservative_portfolio_evaluator import ConservativePortfolioDecision


@dataclass(frozen=True)
class FallbackChoice:
    state: str
    selected_backend_id: Optional[str]
    reason: str
    deferred_backend_ids: tuple[str, ...]
    authorization_blocked_backend_ids: tuple[str, ...]
    exhausted_no_spend_backend_ids: tuple[str, ...]
    discovery_reopened: bool = False
    execution_enabled: bool = False
    network_enabled: bool = False
    spend_enabled: bool = False
    value_movement_enabled: bool = False


def choose_next(
    acquisition_steps: Iterable[AcquisitionStep],
    *,
    portfolio: ConservativePortfolioDecision | None = None,
    attempted_backend_ids: Iterable[str] = (),
) -> FallbackChoice:
    steps=tuple(acquisition_steps)
    attempted=frozenset(attempted_backend_ids)
    if portfolio and portfolio.selected_backend_id:
        return FallbackChoice(
            state="CURRENT_ROUTE_EXISTS",
            selected_backend_id=portfolio.selected_backend_id,
            reason="conservative_portfolio_already_has_current_candidate",
            deferred_backend_ids=(),
            authorization_blocked_backend_ids=(),
            exhausted_no_spend_backend_ids=tuple(sorted(attempted)),
        )

    deferred=[]
    auth_blocked=[]
    exhausted=[]
    for step in steps:
        if step.backend_id in attempted:
            exhausted.append(step.backend_id)
            continue
        if step.state != "EVIDENCE_ACQUISITION_CANDIDATE":
            deferred.append(step.backend_id)
            continue
        if step.authorization_needed_before_execution and not step.no_new_spend_evidence_work_possible:
            auth_blocked.append(step.backend_id)
            continue
        if step.no_new_spend_evidence_work_possible:
            return FallbackChoice(
                state="NEXT_NO_SPEND_EVIDENCE_BRANCH",
                selected_backend_id=step.backend_id,
                reason="highest_priority_existing_backend_with_no_new_spend_evidence_work",
                deferred_backend_ids=tuple(deferred),
                authorization_blocked_backend_ids=tuple(auth_blocked),
                exhausted_no_spend_backend_ids=tuple(exhausted),
            )
        auth_blocked.append(step.backend_id)

    return FallbackChoice(
        state="NO_UNATTEMPTED_NO_SPEND_BRANCH",
        selected_backend_id=None,
        reason="existing_no_spend_evidence_branches_exhausted_or_deferred; do_not_reopen_discovery_automatically",
        deferred_backend_ids=tuple(deferred),
        authorization_blocked_backend_ids=tuple(auth_blocked),
        exhausted_no_spend_backend_ids=tuple(exhausted),
    )


def payload(result: FallbackChoice) -> dict:
    body=asdict(result)
    body.update({
        "schema":"mining-autonomy/i137-resource-fallback-ladder/v1",
        "run":"I137",
        "credentials_used":False,
        "production_observation_performed":False,
        "task_acceptance_performed":False,
    })
    return body
