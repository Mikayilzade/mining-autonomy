"""Offline bridge from task observation gates to Resource / Execution Router (I049).

This module never executes work. Upstream policy/capability/demand decisions are
authoritative: resource cost can refine an already-permitted dry-run candidate,
but can never rescue a held or rejected opportunity.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Optional

from evaluator import ADAPTERS, CapabilityProfile, CostProfile
from orchestrator import ObservationItem, observe_task
from resource_router import (
    ExecutionBackend,
    RoutingDecision,
    TaskEconomics,
    default_backend_families,
    route_task,
)

_ROUTING_FIELDS = {
    "platform_fee_usd",
    "platform_fee_rate",
    "transaction_fee_usd",
    "gas_fee_usd",
    "withdrawal_conversion_fee_usd",
    "dispute_probability",
    "nonpayment_probability",
    "acceptance_probability",
    "minimum_success_probability",
    "minimum_expected_margin_usd",
    "minimum_expected_margin_ratio",
}


@dataclass(frozen=True)
class RoutedTaskObservation:
    platform: str
    external_id: str
    state: str
    reasons: tuple[str, ...]
    upstream_state: str
    upstream_expected_margin_usd: Optional[float]
    demand_evidence_class: str
    evidence_strength: int
    open_paid_demand_proven: bool
    task_economics: Optional[TaskEconomics]
    routing_decision: Optional[RoutingDecision]
    selected_backend_id: Optional[str]
    upstream_gate_passed: bool
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _routing_overrides(payload: Mapping[str, Any]) -> dict[str, float]:
    raw = payload.get("routing_economics", {})
    if raw is None:
        return {}
    if not isinstance(raw, Mapping):
        raise ValueError("routing_economics_must_be_mapping")
    out: dict[str, float] = {}
    for key in _ROUTING_FIELDS:
        if key not in raw:
            continue
        value = raw[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"routing_economics_{key}_must_be_numeric")
        out[key] = float(value)
    return out


def task_economics_from_payload(
    platform: str,
    payload: Mapping[str, Any],
    *,
    observed_at: str | None = None,
) -> TaskEconomics:
    """Re-adapt an already observed payload into router economics.

    Risk/fee overrides must be supplied under ``routing_economics`` so ordinary
    task metadata cannot silently change the economic model.
    """
    adapter = ADAPTERS.get(platform)
    if adapter is None:
        raise ValueError("unknown_task_platform")
    opportunity = adapter.adapt(dict(payload), observed_at=observed_at)
    payout = opportunity.fixed_payout_usd
    if payout is None or payout <= 0:
        raise ValueError("positive_fixed_payout_required_for_routing")
    required = frozenset(opportunity.metadata.get("required_capabilities", []))
    return TaskEconomics(
        task_id=opportunity.external_id,
        required_capabilities=required,
        gross_payout_usd=float(payout),
        **_routing_overrides(payload),
    )


def observe_and_route_task(
    platform: str,
    payload: Mapping[str, Any],
    *,
    demand_evidence_class: str = "unknown",
    observed_at: str | None = None,
    capabilities: CapabilityProfile | None = None,
    cost: CostProfile | None = None,
    backends: Iterable[ExecutionBackend] | None = None,
) -> RoutedTaskObservation:
    """Apply upstream observation gates first, then resource routing if allowed."""
    observation = observe_task(
        platform,
        dict(payload),
        demand_evidence_class=demand_evidence_class,
        observed_at=observed_at,
        capabilities=capabilities,
        cost=cost,
    )
    if observation.state != "accept_dry_run":
        return RoutedTaskObservation(
            platform=observation.platform,
            external_id=observation.external_id,
            state=observation.state,
            reasons=observation.reasons,
            upstream_state=observation.state,
            upstream_expected_margin_usd=observation.expected_margin_usd,
            demand_evidence_class=observation.demand_evidence_class,
            evidence_strength=observation.evidence_strength,
            open_paid_demand_proven=observation.open_paid_demand_proven,
            task_economics=None,
            routing_decision=None,
            selected_backend_id=None,
            upstream_gate_passed=False,
        )

    economics = task_economics_from_payload(platform, payload, observed_at=observed_at)
    routing = route_task(economics, tuple(backends) if backends is not None else default_backend_families())
    reasons = list(observation.reasons)
    state = routing.state
    if routing.state != "route_dry_run":
        state = "hold"
        reasons.append("resource_route_unavailable")
    return RoutedTaskObservation(
        platform=observation.platform,
        external_id=observation.external_id,
        state=state,
        reasons=tuple(dict.fromkeys(reasons)),
        upstream_state=observation.state,
        upstream_expected_margin_usd=observation.expected_margin_usd,
        demand_evidence_class=observation.demand_evidence_class,
        evidence_strength=observation.evidence_strength,
        open_paid_demand_proven=observation.open_paid_demand_proven,
        task_economics=economics,
        routing_decision=routing,
        selected_backend_id=routing.selected_backend_id,
        upstream_gate_passed=True,
    )


def build_routed_task_queue(
    task_payloads: Iterable[tuple],
    *,
    capabilities: CapabilityProfile | None = None,
    cost: CostProfile | None = None,
    backends: Iterable[ExecutionBackend] | None = None,
) -> list[RoutedTaskObservation]:
    """Build a combined inert queue from the orchestrator's task tuple contract."""
    out: list[RoutedTaskObservation] = []
    for entry in task_payloads:
        if len(entry) == 2:
            platform, payload = entry
            evidence_class = "unknown"
        elif len(entry) == 3:
            platform, payload, evidence_class = entry
        else:
            raise ValueError("task_observation_tuple_must_have_2_or_3_items")
        out.append(
            observe_and_route_task(
                platform,
                payload,
                demand_evidence_class=evidence_class,
                capabilities=capabilities,
                cost=cost,
                backends=backends,
            )
        )
    out.sort(
        key=lambda item: (
            1 if item.state == "route_dry_run" else 0,
            (
                item.routing_decision.selected_quote.expected_margin_before_fixed_allocation_usd
                if item.routing_decision is not None
                and item.routing_decision.selected_quote is not None
                else float("-inf")
            ),
            item.evidence_strength,
        ),
        reverse=True,
    )
    return out


def routed_task_record(item: RoutedTaskObservation) -> dict[str, Any]:
    record = asdict(item)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["value_movement_enabled"] = False
    return record
