"""Unified offline observation orchestrator.

Combines paid-task and passive-service dry-run decisions into one observation
queue. It never executes tasks, publishes services, authenticates, or settles.
Demand evidence is explicit: listings/marketing cannot become utilization.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Iterable

from demand_evidence import classify_demand_evidence
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
    demand_evidence_class: str = "unknown"
    evidence_strength: int = 0
    paid_utilization_proven: bool = False
    open_paid_demand_proven: bool = False
    dry_run_only: bool = True
    action_enabled: bool = False


def observe_task(platform: str, payload: dict[str, Any], *,
                 demand_evidence_class: str = "unknown",
                 capabilities: CapabilityProfile | None = None,
                 cost: CostProfile | None = None) -> ObservationItem:
    evidence = classify_demand_evidence(demand_evidence_class)
    opportunity = ADAPTERS[platform].adapt(payload)
    decision = evaluate(opportunity, capabilities or CapabilityProfile(), cost)
    reasons = list(decision.reject_reasons)
    state = decision.decision
    if state == "accept_dry_run" and not evidence.proves_open_paid_demand:
        state = "hold"
        reasons.append("open_paid_demand_unproven")
    return ObservationItem(
        source_type="task", platform=decision.platform,
        external_id=decision.opportunity_id, state=state,
        expected_monthly_value_usd=None,
        expected_margin_usd=decision.expected_margin_usd,
        reasons=tuple(dict.fromkeys(reasons)),
        demand_evidence_class=evidence.evidence_class,
        evidence_strength=evidence.strength,
        paid_utilization_proven=evidence.proves_paid_utilization,
        open_paid_demand_proven=evidence.proves_open_paid_demand,
    )


def observe_passive(offer: PassiveServiceOffer, *,
                    demand_evidence_class: str = "unknown") -> ObservationItem:
    evidence = classify_demand_evidence(demand_evidence_class)
    decision = evaluate_passive_offer(offer)
    reasons = list(decision.reject_reasons)
    state = decision.decision
    if state == "ready_for_observation" and not evidence.proves_paid_utilization:
        state = "hold"
        reasons.append("paid_utilization_unproven")
    return ObservationItem(
        source_type="passive_service", platform=decision.platform,
        external_id=decision.capability, state=state,
        expected_monthly_value_usd=decision.projected_net_month_usd,
        expected_margin_usd=decision.contribution_per_call_usd,
        reasons=tuple(dict.fromkeys(reasons)),
        demand_evidence_class=evidence.evidence_class,
        evidence_strength=evidence.strength,
        paid_utilization_proven=evidence.proves_paid_utilization,
        open_paid_demand_proven=evidence.proves_open_paid_demand,
    )


def _rank_key(item: ObservationItem) -> tuple[int, float, float, int]:
    if item.source_type == "passive_service":
        if item.expected_monthly_value_usd is None:
            return (0, float("-inf"), item.expected_margin_usd or float("-inf"), item.evidence_strength)
        return (
            2 if item.state == "ready_for_observation" else 1,
            item.expected_monthly_value_usd,
            item.expected_margin_usd or 0.0,
            item.evidence_strength,
        )
    if item.state == "accept_dry_run" and item.expected_margin_usd is not None:
        return (3, item.expected_margin_usd, 0.0, item.evidence_strength)
    return (0, item.expected_margin_usd or float("-inf"), 0.0, item.evidence_strength)


def rank_observations(items: Iterable[ObservationItem]) -> list[ObservationItem]:
    return sorted(items, key=_rank_key, reverse=True)


def build_observation_queue(task_payloads: Iterable[tuple],
                            passive_offers: Iterable,
                            *, capabilities: CapabilityProfile | None = None,
                            cost: CostProfile | None = None) -> list[ObservationItem]:
    items: list[ObservationItem] = []
    for entry in task_payloads:
        if len(entry) == 2:
            platform, payload = entry
            evidence_class = "unknown"
        elif len(entry) == 3:
            platform, payload, evidence_class = entry
        else:
            raise ValueError("task_observation_tuple_must_have_2_or_3_items")
        items.append(observe_task(platform, payload, demand_evidence_class=evidence_class,
                                  capabilities=capabilities, cost=cost))
    for entry in passive_offers:
        if isinstance(entry, PassiveServiceOffer):
            offer, evidence_class = entry, "unknown"
        elif isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], PassiveServiceOffer):
            offer, evidence_class = entry
        else:
            raise ValueError("passive_observation_must_be_offer_or_offer_evidence_tuple")
        items.append(observe_passive(offer, demand_evidence_class=evidence_class))
    return rank_observations(items)


def queue_records(items: Iterable[ObservationItem]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]


def audit_export(items: Iterable[ObservationItem], *, generated_at: str | None = None) -> dict[str, Any]:
    """Machine-readable audit summary; never changes execution state."""
    records = queue_records(items)
    counts = {"accepted": 0, "held": 0, "rejected": 0}
    reason_counts: dict[str, int] = {}
    evidence_counts: dict[str, int] = {}
    paid_utilization_proven_count = 0
    open_paid_demand_proven_count = 0
    for record in records:
        state = record["state"]
        if state in {"accept_dry_run", "ready_for_observation"}:
            counts["accepted"] += 1
        elif state == "reject":
            counts["rejected"] += 1
        else:
            counts["held"] += 1
        evidence_class = record["demand_evidence_class"]
        evidence_counts[evidence_class] = evidence_counts.get(evidence_class, 0) + 1
        paid_utilization_proven_count += int(record["paid_utilization_proven"])
        open_paid_demand_proven_count += int(record["open_paid_demand_proven"])
        for reason in record["reasons"]:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    return {
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "dry_run_only": True,
        "action_enabled": False,
        "counts": counts,
        "evidence_counts": dict(sorted(evidence_counts.items())),
        "paid_utilization_proven_count": paid_utilization_proven_count,
        "open_paid_demand_proven_count": open_paid_demand_proven_count,
        "reason_counts": dict(sorted(reason_counts.items())),
        "observations": records,
    }
