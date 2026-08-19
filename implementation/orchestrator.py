"""Unified offline observation orchestrator.

Combines paid-task and passive-service dry-run decisions into one observation
queue. It never executes tasks, publishes services, authenticates, or settles.
Unknown passive demand is deliberately held and is never assigned invented EV.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
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
    return ObservationItem(source_type="task",platform=decision.platform,
        external_id=decision.opportunity_id,state=decision.decision,
        expected_monthly_value_usd=None,expected_margin_usd=decision.expected_margin_usd,
        reasons=tuple(decision.reject_reasons))


def observe_passive(offer: PassiveServiceOffer) -> ObservationItem:
    decision = evaluate_passive_offer(offer)
    return ObservationItem(source_type="passive_service",platform=decision.platform,
        external_id=decision.capability,state=decision.decision,
        expected_monthly_value_usd=decision.projected_net_month_usd,
        expected_margin_usd=decision.contribution_per_call_usd,reasons=decision.reject_reasons)


def _rank_key(item: ObservationItem) -> tuple[int, float, float]:
    if item.source_type == "passive_service":
        if item.expected_monthly_value_usd is None:
            return (0,float("-inf"),item.expected_margin_usd or float("-inf"))
        return (2 if item.state == "ready_for_observation" else 1,
                item.expected_monthly_value_usd,item.expected_margin_usd or 0.0)
    if item.state == "accept_dry_run" and item.expected_margin_usd is not None:
        return (3,item.expected_margin_usd,0.0)
    return (0,item.expected_margin_usd or float("-inf"),0.0)


def rank_observations(items: Iterable[ObservationItem]) -> list[ObservationItem]:
    return sorted(items,key=_rank_key,reverse=True)


def build_observation_queue(task_payloads: Iterable[tuple[str, dict[str, Any]]],
                            passive_offers: Iterable[PassiveServiceOffer], *,
                            capabilities: CapabilityProfile | None = None,
                            cost: CostProfile | None = None) -> list[ObservationItem]:
    items=[observe_task(platform,payload,capabilities=capabilities,cost=cost)
           for platform,payload in task_payloads]
    items.extend(observe_passive(offer) for offer in passive_offers)
    return rank_observations(items)


def queue_records(items: Iterable[ObservationItem]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]


def audit_export(items: Iterable[ObservationItem], *, generated_at: str | None = None) -> dict[str, Any]:
    """Machine-readable audit summary; never changes execution state."""
    records=queue_records(items)
    counts={"accepted":0,"held":0,"rejected":0}
    reason_counts: dict[str,int]={}
    for r in records:
        state=r["state"]
        if state in {"accept_dry_run","ready_for_observation"}: counts["accepted"]+=1
        elif state == "reject": counts["rejected"]+=1
        else: counts["held"]+=1
        for reason in r["reasons"]:
            reason_counts[reason]=reason_counts.get(reason,0)+1
    return {"generated_at":generated_at or datetime.now(timezone.utc).isoformat(),
        "dry_run_only":True,"action_enabled":False,"counts":counts,
        "reason_counts":dict(sorted(reason_counts.items())),"observations":records}
