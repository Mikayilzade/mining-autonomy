"""I130 deterministic sensitivity envelope for Resource / Execution Router economics.

Offline only. Converts uncertainty in electricity, opportunity cost, acceptance,
dispute/nonpayment and fees into a conservative route envelope. It does not create
market evidence or authorize execution.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Iterable
from resource_router import ExecutionBackend, TaskEconomics, quote_backend

@dataclass(frozen=True)
class SensitivityCase:
    name: str
    electricity_multiplier: float = 1.0
    opportunity_cost_multiplier: float = 1.0
    acceptance_multiplier: float = 1.0
    dispute_add: float = 0.0
    nonpayment_add: float = 0.0
    fee_add_usd: float = 0.0

@dataclass(frozen=True)
class SensitivityResult:
    case: str
    expected_margin_usd: float
    margin_ratio: float
    success_probability: float
    planning_reasons: tuple[str, ...]

DEFAULT_CASES = (
    SensitivityCase("base"),
    SensitivityCase("energy_x2", electricity_multiplier=2.0),
    SensitivityCase("opportunity_x2", opportunity_cost_multiplier=2.0),
    SensitivityCase("acceptance_minus_20pct", acceptance_multiplier=0.8),
    SensitivityCase("payment_stress", dispute_add=0.05, nonpayment_add=0.05),
    SensitivityCase("combined_conservative", electricity_multiplier=2.0, opportunity_cost_multiplier=2.0, acceptance_multiplier=0.8, dispute_add=0.05, nonpayment_add=0.05, fee_add_usd=0.02),
)

def evaluate(task: TaskEconomics, backend: ExecutionBackend, cases: Iterable[SensitivityCase] = DEFAULT_CASES) -> tuple[SensitivityResult, ...]:
    out=[]
    for c in cases:
        b=replace(backend,
            electricity_per_task_usd=backend.electricity_per_task_usd*c.electricity_multiplier,
            opportunity_cost_per_task_usd=backend.opportunity_cost_per_task_usd*c.opportunity_cost_multiplier)
        t=replace(task,
            acceptance_probability=max(0.0,min(1.0,task.acceptance_probability*c.acceptance_multiplier)),
            dispute_probability=max(0.0,min(1.0,task.dispute_probability+c.dispute_add)),
            nonpayment_probability=max(0.0,min(1.0,task.nonpayment_probability+c.nonpayment_add)),
            platform_fee_usd=task.platform_fee_usd+c.fee_add_usd)
        q=quote_backend(t,b)
        out.append(SensitivityResult(c.name,q.expected_margin_before_fixed_allocation_usd,q.expected_margin_ratio,q.success_probability,q.planning_reasons))
    return tuple(out)

def conservative_route_survives(results: Iterable[SensitivityResult]) -> bool:
    rows=tuple(results)
    return bool(rows) and all("insufficient_conservative_expected_margin" not in r.planning_reasons for r in rows)
