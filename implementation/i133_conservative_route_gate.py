"""I133 integrated conservative route gate.

Combines I123 per-task backend economics, I130 stress cases, and I131 watcher
acquisition overhead. Offline only: no polling, network, credentials, spend,
authorization creation, task acceptance, or value movement.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Iterable

from i130_resource_economics_sensitivity import DEFAULT_CASES, SensitivityCase, evaluate
from i131_watcher_cost_budget import WatcherBudget, estimate
from resource_router import ExecutionBackend, TaskEconomics, quote_backend


@dataclass(frozen=True)
class StressMargin:
    case: str
    raw_expected_margin_usd: float
    acquisition_overhead_per_candidate_usd: float
    adjusted_expected_margin_usd: float
    adjusted_margin_ratio: float
    survives: bool
    blockers: tuple[str, ...]


@dataclass(frozen=True)
class ConservativeRouteGate:
    backend_id: str
    task_id: str
    state: str
    base_planning_state: str
    base_planning_reasons: tuple[str, ...]
    watcher_daily_cost_usd: float
    watcher_daily_candidates: float
    acquisition_overhead_per_candidate_usd: float
    stress_margins: tuple[StressMargin, ...]
    worst_adjusted_margin_usd: float | None
    conservative_route_survives: bool
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def assess_conservative_route(
    task: TaskEconomics,
    backend: ExecutionBackend,
    watcher_budget: WatcherBudget,
    *,
    cases: Iterable[SensitivityCase] = DEFAULT_CASES,
) -> ConservativeRouteGate:
    base = quote_backend(task, backend)
    watcher = estimate(watcher_budget)
    overhead = (
        watcher.daily_incremental_cost_usd / watcher.daily_candidates
        if watcher.daily_candidates > 0 else float("inf")
    )
    rows = []
    for stress in evaluate(task, backend, cases):
        blockers = list(stress.planning_reasons)
        if watcher.daily_candidates <= 0:
            blockers.append("watcher_has_no_candidate_throughput")
            adjusted = float("-inf")
            ratio = float("-inf")
        else:
            adjusted = stress.expected_margin_usd - overhead
            ratio = adjusted / task.gross_payout_usd if task.gross_payout_usd > 0 else -1.0
            if adjusted < task.minimum_expected_margin_usd or ratio < task.minimum_expected_margin_ratio:
                blockers.append("watcher_adjusted_margin_below_threshold")
        survives = not blockers
        rows.append(StressMargin(
            case=stress.case,
            raw_expected_margin_usd=stress.expected_margin_usd,
            acquisition_overhead_per_candidate_usd=round(overhead, 8) if overhead != float("inf") else overhead,
            adjusted_expected_margin_usd=round(adjusted, 8) if adjusted != float("-inf") else adjusted,
            adjusted_margin_ratio=round(ratio, 8) if ratio != float("-inf") else ratio,
            survives=survives,
            blockers=tuple(dict.fromkeys(blockers)),
        ))
    survives_all = bool(rows) and not base.planning_reasons and all(r.survives for r in rows)
    finite = [r.adjusted_expected_margin_usd for r in rows if r.adjusted_expected_margin_usd != float("-inf")]
    return ConservativeRouteGate(
        backend_id=backend.backend_id,
        task_id=task.task_id,
        state="CONSERVATIVE_ROUTE_ECONOMICS_PASS" if survives_all else "HOLD",
        base_planning_state=base.planning_state,
        base_planning_reasons=base.planning_reasons,
        watcher_daily_cost_usd=watcher.daily_incremental_cost_usd,
        watcher_daily_candidates=watcher.daily_candidates,
        acquisition_overhead_per_candidate_usd=(round(overhead, 8) if overhead != float("inf") else overhead),
        stress_margins=tuple(rows),
        worst_adjusted_margin_usd=(round(min(finite), 8) if finite else None),
        conservative_route_survives=survives_all,
    )


def to_payload(result: ConservativeRouteGate) -> dict:
    payload = asdict(result)
    payload.update({
        "schema": "mining-autonomy/i133-conservative-route-gate/v1",
        "run": "I133",
        "fresh_real_market_evidence_created": False,
        "authorization_created": False,
        "production_route_created": False,
        "spend_or_value_movement": False,
    })
    return payload
