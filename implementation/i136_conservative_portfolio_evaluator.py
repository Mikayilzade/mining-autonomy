"""I136 conservative portfolio evaluator.

Applies current I123 production-evidence blockers and I133 conservative economics
(including I130 stress and I131 watcher overhead) across the already-defined backend
portfolio. Offline only: no network, credentials, workflow dispatch, spend, task
acceptance, submission, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Optional

from i123_execution_backend_portfolio import BackendEvidence, production_blockers
from i131_watcher_cost_budget import WatcherBudget
from i133_conservative_route_gate import ConservativeRouteGate, assess_conservative_route
from resource_router import ExecutionBackend, TaskEconomics


@dataclass(frozen=True)
class ConservativePortfolioRow:
    backend_id: str
    family: str
    evidence_blockers: tuple[str, ...]
    economics_state: str
    economics_survives: bool
    worst_adjusted_margin_usd: float | None
    production_candidate: bool


@dataclass(frozen=True)
class ConservativePortfolioDecision:
    task_id: str
    state: str
    selected_backend_id: Optional[str]
    rows: tuple[ConservativePortfolioRow, ...]
    route_gates: tuple[ConservativeRouteGate, ...]
    deterministic_first: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    spend_enabled: bool = False
    value_movement_enabled: bool = False


def evaluate_portfolio(
    task: TaskEconomics,
    backends: Iterable[ExecutionBackend],
    evidence: Iterable[BackendEvidence],
    watcher_budgets: Mapping[str, WatcherBudget],
) -> ConservativePortfolioDecision:
    bs = tuple(backends)
    es = tuple(evidence)
    em = {e.backend_id: e for e in es}
    if len(em) != len(es):
        raise ValueError("duplicate_backend_evidence")

    rows=[]
    gates=[]
    candidates=[]
    for backend in bs:
        blockers = production_blockers(backend, em.get(backend.backend_id))
        budget = watcher_budgets.get(backend.backend_id)
        if budget is None:
            rows.append(ConservativePortfolioRow(
                backend_id=backend.backend_id,
                family=backend.family,
                evidence_blockers=tuple(dict.fromkeys((*blockers, "watcher_budget_missing"))),
                economics_state="NOT_EVALUATED",
                economics_survives=False,
                worst_adjusted_margin_usd=None,
                production_candidate=False,
            ))
            continue
        gate = assess_conservative_route(task, backend, budget)
        gates.append(gate)
        candidate = not blockers and gate.conservative_route_survives
        rows.append(ConservativePortfolioRow(
            backend_id=backend.backend_id,
            family=backend.family,
            evidence_blockers=blockers,
            economics_state=gate.state,
            economics_survives=gate.conservative_route_survives,
            worst_adjusted_margin_usd=gate.worst_adjusted_margin_usd,
            production_candidate=candidate,
        ))
        if candidate:
            candidates.append((backend, gate))

    if candidates:
        deterministic = [x for x in candidates if x[0].family not in {
            "local_cpu_gpu_model", "chatgpt_codex_subscription",
            "cheap_external_llm_api", "strong_external_llm_api",
        }]
        pool = deterministic or candidates
        pool.sort(key=lambda x: (
            x[0].marginal_cost_usd(),
            -(x[1].worst_adjusted_margin_usd if x[1].worst_adjusted_margin_usd is not None else -1e18),
            -x[0].effective_success_probability(),
            x[0].latency_seconds,
            x[0].backend_id,
        ))
        selected = pool[0][0].backend_id
        state = "CONSERVATIVE_PORTFOLIO_ROUTE_READY"
    else:
        selected = None
        state = "HOLD"

    return ConservativePortfolioDecision(
        task_id=task.task_id,
        state=state,
        selected_backend_id=selected,
        rows=tuple(rows),
        route_gates=tuple(gates),
    )


def payload(result: ConservativePortfolioDecision) -> dict:
    body=asdict(result)
    body.update({
        "schema":"mining-autonomy/i136-conservative-portfolio-evaluator/v1",
        "run":"I136",
        "production_observation_performed":False,
        "task_acceptance_performed":False,
        "spend_or_value_movement":False,
    })
    return body
