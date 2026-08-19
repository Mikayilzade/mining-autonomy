"""Passive paid-service decision layer (I008).

Offline and publication-disabled. This converts bounded local capabilities into a
common decision contract without creating accounts, publishing endpoints, or
moving value.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
from mcp_benchmark import CAPABILITIES, CapabilityEconomics

@dataclass(frozen=True)
class HostingTier:
    name: str
    monthly_fixed_cost_usd: float
    included_calls: int | None = None

@dataclass(frozen=True)
class PassiveServiceOffer:
    platform: str
    capability: str
    price_per_call_usd: float
    creator_share: float
    variable_cost_per_call_usd: float
    hosting: HostingTier
    minimum_margin_usd: float = 0.001
    minimum_margin_ratio: float = 0.25
    demand_calls_per_month: int | None = None
    policy_confirmed: bool = True
    publication_authorized: bool = False

@dataclass(frozen=True)
class PassiveServiceDecision:
    platform: str
    capability: str
    decision: str
    reject_reasons: tuple[str, ...]
    creator_revenue_per_call_usd: float
    contribution_per_call_usd: float
    break_even_calls_month: int | None
    projected_net_month_usd: float | None
    dry_run_only: bool = True
    publication_enabled: bool = False


def _ceil_div_cost(fixed: float, contribution: float) -> int | None:
    if contribution <= 0:
        return None
    if fixed <= 0:
        return 0
    import math
    return math.ceil(fixed / contribution)


def evaluate_passive_offer(offer: PassiveServiceOffer) -> PassiveServiceDecision:
    reasons: list[str] = []
    if offer.capability not in CAPABILITIES:
        reasons.append("unsupported_capability")
    if not offer.policy_confirmed:
        reasons.append("policy_evidence_insufficient")
    if offer.price_per_call_usd <= 0 or not 0 < offer.creator_share <= 1:
        reasons.append("invalid_pricing")
    if offer.variable_cost_per_call_usd < 0 or offer.hosting.monthly_fixed_cost_usd < 0:
        reasons.append("invalid_cost")

    revenue = max(0.0, offer.price_per_call_usd * offer.creator_share)
    contribution = revenue - max(0.0, offer.variable_cost_per_call_usd)
    ratio = contribution / revenue if revenue > 0 else -1.0
    if contribution < offer.minimum_margin_usd or ratio < offer.minimum_margin_ratio:
        reasons.append("insufficient_expected_margin")

    break_even = _ceil_div_cost(offer.hosting.monthly_fixed_cost_usd, contribution)
    projected = None
    if offer.demand_calls_per_month is None:
        reasons.append("demand_unproven")
    else:
        projected = round(offer.demand_calls_per_month * contribution - offer.hosting.monthly_fixed_cost_usd, 6)
        if projected <= 0:
            reasons.append("negative_projected_month")
        if offer.hosting.included_calls is not None and offer.demand_calls_per_month > offer.hosting.included_calls:
            reasons.append("hosting_capacity_exceeded")

    # Publication is deliberately impossible in this phase even if the caller
    # accidentally sets publication_authorized=True. A later live adapter must
    # be a separate explicitly authorized component.
    decision = "ready_for_observation" if not reasons else "hold"
    return PassiveServiceDecision(
        offer.platform, offer.capability, decision, tuple(dict.fromkeys(reasons)),
        round(revenue, 6), round(contribution, 6), break_even, projected,
        dry_run_only=True, publication_enabled=False,
    )


def execute_local_capability(capability: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Execute only the bounded local capability registry; no network side effects."""
    if capability not in CAPABILITIES:
        raise ValueError("unsupported capability")
    return CAPABILITIES[capability](payload)


def decision_record(offer: PassiveServiceOffer) -> dict[str, Any]:
    return {"offer": asdict(offer), "decision": asdict(evaluate_passive_offer(offer))}
