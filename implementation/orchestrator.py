"""Unified offline observation orchestrator (I009).

Combines paid-task and passive-service dry-run decisions into one observation
queue. It never executes tasks, publishes services, authenticates, or settles.
Unknown passive demand is deliberately held and is never assigned invented EV.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Iterable

from evaluator import ADAPTERS, CapabilityProfile, CostProfile, evaluate
from passive_service import PassiveServiceOffer, evaluate_passive_offer


@dataclass(frozen=True)
class ObservationItem:
    source_type: str
    platform: str
    external_id: str
    state: str
    expected_monthly_value_usd: float | None
    expected_margin_usd: float | None
    reasons: tuple[str, ...]
    dry_run_only: bool = True
    action_enabled: bool = False


def observe_task(platform: str, payload: dict[str, Any], *, capabilities: CapabilityProfile | None = None,
                 cost: CostProfile | None = None) -> ObservationItem:
    opportunity = ADAPTERS[platform].adapt(payload)
    decision = evaluate(opportunity, capabilities or CapabilityProfile(), cost)
    return ObservationItem(
        source_type="task",
        platform=decision.platform,
        external_id=decision.opportunity_id,
        state=decision.decision,
        expected_monthly_value_usd=None,  # one-off task != monthly demand
        expected_margin_usd=decision.expected_margin_usd,
        reasons=tuple(decision.reject_reasons),
    )


def observe_passive(offer: PassiveServiceOffer) -> ObservationItem:
    decision = evaluate_passive_offer(offer)
    return ObservationItem(
        source_type="passive_service",
        platform=decision.platform,
        external_id=decision.capability,
        state=decision.decision,
        expected_monthly_value_usd=decision.projected_net_month_usd,
        expected_margin_usd=decision.contribution_per_call_usd,
        reasons=decision.reject_reasons,
    )


def _rank_key(item: ObservationItem) -> tuple[int, float, float]:
    """Rank only comparable evidence; unknown demand never receives synthetic EV."""
    if item.source_type == "passive_service":
        if item.expected_monthly_value_usd is None:
            return (0, float("-inf"), item.expected_margin_usd or float("-inf"))
        return (2 if item.state == "ready_for_observation" else 1,
                item.expected_monthly_value_usd, item.expected_margin_usd or 0.0)
    # Task margins are observable per opportunity, not comparable to monthly passive EV.
    if item.state == "accept_dry_run" and item.expected_margin_usd is not None:
        return (3, item.expected_margin_usd, 0.0)
    return (0, item.expected_margin_usd or float("-inf"), 0.0)


def rank_observations(items: Iterable[ObservationItem]) -> list[ObservationItem]:
    return sorted(items, key=_rank_key, reverse=True)


def build_observation_queue(task_payloads: Iterable[tuple[str, dict[str, Any]]],
                            passive_offers: Iterable[PassiveServiceOffer], *,
                            capabilities: CapabilityProfile | None = None,
                            cost: CostProfile | None = None) -> list[ObservationItem]:
    items = [observe_task(platform, payload, capabilities=capabilities, cost=cost)
             for platform, payload in task_payloads]
    items.extend(observe_passive(offer) for offer in passive_offers)
    return rank_observations(items)


def queue_records(items: Iterable[ObservationItem]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]
