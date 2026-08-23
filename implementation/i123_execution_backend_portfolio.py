#!/usr/bin/env python3
"""I123 portfolio-level Resource / Execution Router.

Extends I048's resource_router without enabling execution. Production selection requires
current reproducible non-synthetic backend evidence in addition to the existing capability,
policy, quota, reliability/quality and conservative-margin gates.

No DNS/HTTP, credentials, CI dispatch, spend, task action, or value movement occurs here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Iterable, Optional

from resource_router import (
    BackendQuote,
    ExecutionBackend,
    TaskEconomics,
    default_backend_families,
    quote_backend,
)

MEASURED = "measured_reproducible"
AI_FAMILIES = frozenset({
    "local_cpu_gpu_model",
    "chatgpt_codex_subscription",
    "cheap_external_llm_api",
    "strong_external_llm_api",
})


@dataclass(frozen=True)
class BackendEvidence:
    backend_id: str
    provenance_class: str
    current_reproducible: bool
    non_synthetic: bool
    capacity_verified: bool
    policy_evidence_current: bool
    credentials_authorized: bool = False
    spend_authorized: bool = False
    infrastructure_authorized: bool = False
    evidence_note: str = ""


@dataclass(frozen=True)
class PortfolioQuote:
    backend_id: str
    family: str
    ai_backend: bool
    base_quote: BackendQuote
    production_blockers: tuple[str, ...]


@dataclass(frozen=True)
class PortfolioDecision:
    task_id: str
    task_kind: str
    state: str
    selected_backend_id: Optional[str]
    escalation_stage: str
    quotes: tuple[PortfolioQuote, ...]
    production_execution_enabled: bool = False
    value_movement_enabled: bool = False


def _evidence_map(items: Iterable[BackendEvidence]) -> dict[str, BackendEvidence]:
    result: dict[str, BackendEvidence] = {}
    for item in items:
        if item.backend_id in result:
            raise ValueError(f"duplicate backend evidence: {item.backend_id}")
        result[item.backend_id] = item
    return result


def production_blockers(
    backend: ExecutionBackend,
    evidence: Optional[BackendEvidence],
) -> tuple[str, ...]:
    blockers: list[str] = []
    if backend.automation_role != "autonomous" or not backend.programmatic_access:
        blockers.append("no_autonomous_programmatic_path")
    if not backend.policy_allowed:
        blockers.append("backend_policy_not_allowed")
    if not backend.currently_available:
        blockers.append("backend_not_currently_available")
    if backend.max_parallelism < 1:
        blockers.append("no_parallel_capacity")
    if (
        backend.quota_units_remaining is not None
        and backend.quota_units_remaining < backend.units_per_task
    ):
        blockers.append("quota_insufficient")
    if backend.allocated_fixed_cost_per_task_usd() is None:
        blockers.append("fixed_cost_allocation_basis_unknown")

    if evidence is None:
        blockers.append("backend_evidence_missing")
    else:
        if evidence.backend_id != backend.backend_id:
            blockers.append("backend_evidence_identity_mismatch")
        if evidence.provenance_class != MEASURED:
            blockers.append("backend_not_measured_reproducible")
        if not evidence.current_reproducible:
            blockers.append("backend_evidence_not_current_reproducible")
        if not evidence.non_synthetic:
            blockers.append("backend_evidence_synthetic")
        if not evidence.capacity_verified:
            blockers.append("backend_capacity_not_verified")
        if not evidence.policy_evidence_current:
            blockers.append("backend_policy_evidence_not_current")
        if backend.requires_credentials and not evidence.credentials_authorized:
            blockers.append("credentials_not_authorized")
        if backend.requires_new_spend and not evidence.spend_authorized:
            blockers.append("new_spend_not_authorized")
        if backend.family == "paid_vps_server" and not evidence.infrastructure_authorized:
            blockers.append("infrastructure_not_authorized")

    return tuple(dict.fromkeys(blockers))


def portfolio_quotes(
    task: TaskEconomics,
    backends: Iterable[ExecutionBackend],
    evidence: Iterable[BackendEvidence],
) -> tuple[PortfolioQuote, ...]:
    evidence_by_id = _evidence_map(evidence)
    return tuple(
        PortfolioQuote(
            backend_id=backend.backend_id,
            family=backend.family,
            ai_backend=backend.family in AI_FAMILIES,
            base_quote=quote_backend(task, backend),
            production_blockers=production_blockers(
                backend, evidence_by_id.get(backend.backend_id)
            ),
        )
        for backend in backends
    )


def _eligible(quotes: Iterable[PortfolioQuote], *, ai: bool) -> list[PortfolioQuote]:
    return [
        q for q in quotes
        if q.ai_backend is ai
        and not q.base_quote.planning_reasons
        and not q.production_blockers
    ]


def _cheapest(quotes: list[PortfolioQuote]) -> PortfolioQuote:
    return sorted(
        quotes,
        key=lambda q: (
            q.base_quote.marginal_cost_usd,
            -q.base_quote.expected_margin_before_fixed_allocation_usd,
            -q.base_quote.success_probability,
            q.base_quote.latency_seconds,
            q.backend_id,
        ),
    )[0]


def route_portfolio(
    task: TaskEconomics,
    backends: Iterable[ExecutionBackend],
    evidence: Iterable[BackendEvidence],
    *,
    task_kind: str = "paid_task",
    ai_allowed: bool = True,
) -> PortfolioDecision:
    if task_kind not in {"paid_task", "observation"}:
        raise ValueError("task_kind must be paid_task or observation")
    quotes = portfolio_quotes(task, backends, evidence)

    deterministic = _eligible(quotes, ai=False)
    if deterministic:
        selected = _cheapest(deterministic)
        return PortfolioDecision(
            task.task_id, task_kind, "production_route_ready",
            selected.backend_id, "deterministic_first", quotes
        )

    if ai_allowed:
        ai_quotes = _eligible(quotes, ai=True)
        if ai_quotes:
            selected = _cheapest(ai_quotes)
            return PortfolioDecision(
                task.task_id, task_kind, "production_route_ready",
                selected.backend_id,
                "ai_only_after_deterministic_paths_fail_acceptance_or_materialization",
                quotes,
            )

    planning = [q for q in quotes if not q.base_quote.planning_reasons]
    return PortfolioDecision(
        task.task_id,
        task_kind,
        "hold",
        None,
        (
            "planning_candidates_exist_but_no_current_production_materialization"
            if planning
            else "no_backend_meets_task_acceptance_and_economics"
        ),
        quotes,
    )


def current_backend_evidence() -> tuple[BackendEvidence, ...]:
    """Repository checkpoint facts only; none are production materialization."""
    notes = {
        "python_local": "Preferred deterministic no-spend family; exact executable current-checkout measurement is absent.",
        "local_model": "Local CPU/GPU/model hardware, energy, quality and availability are unmeasured.",
        "subscription_assistant": "Fixed/sunk limited support only; no autonomous programmatic API is assumed.",
        "cheap_external_api": "No current vendor/credential/pricing/spend authorization materialization.",
        "strong_external_api": "No current vendor/credential/pricing/spend authorization materialization.",
        "free_tier_ci": "Manual GitHub-hosted runtime path exists, but current connector exposes no workflow_dispatch.",
        "owned_pc": "Owned-PC power/capacity/reliability/quality evidence is not materialized.",
        "future_paid_vps": "Future paid infrastructure requires separate authorization and spend.",
    }
    return tuple(
        BackendEvidence(
            backend_id=backend.backend_id,
            provenance_class="planning_reference",
            current_reproducible=False,
            non_synthetic=False,
            capacity_verified=False,
            policy_evidence_current=False,
            evidence_note=notes[backend.backend_id],
        )
        for backend in default_backend_families()
    )


def current_snapshot() -> dict:
    backends = default_backend_families()
    evidence = current_backend_evidence()
    paid_probe = TaskEconomics(
        task_id="synthetic_paid_probe",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=1.0,
        platform_fee_rate=0.05,
        dispute_probability=0.05,
        nonpayment_probability=0.05,
        acceptance_probability=0.80,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.10,
        minimum_expected_margin_ratio=0.10,
    )
    observation_probe = TaskEconomics(
        task_id="synthetic_observation_value_probe",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=0.10,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.01,
        minimum_expected_margin_ratio=0.05,
    )
    decisions = (
        route_portfolio(paid_probe, backends, evidence, task_kind="paid_task"),
        route_portfolio(
            observation_probe, backends, evidence,
            task_kind="observation", ai_allowed=False
        ),
    )
    return {
        "schema": "mining-autonomy/i123-execution-backend-portfolio/v1",
        "run": "I123",
        "artifact_class": "planning_reference",
        "synthetic_fixture": True,
        "production_route_created": False,
        "authorization_created": False,
        "network_observation_performed": False,
        "credentials_used": False,
        "paid_infrastructure_created": False,
        "spend_or_value_movement": False,
        "routing_rule": "deterministic_first_then_ai_only_if_needed_then_cheapest_qualifying_positive_margin",
        "fixed_vs_marginal_rule": "fixed/sunk cost remains separate; full monthly subscription cost is not charged to each task and finite capacity/opportunity cost is not treated as free",
        "task_kind_separation": "observation economics never prove paid-task fulfillment economics",
        "backend_evidence": [asdict(x) for x in evidence],
        "decisions": [asdict(x) for x in decisions],
        "current_route_summary": {
            "eligible_non_synthetic_route_exists": False,
            "reason": "No backend has current measured_reproducible non-synthetic evidence in the current checkpoint.",
            "priority": [
                "exact current-main I113 runtime receipt",
                "materialize one no-spend backend with current capacity/reliability/quality/cost evidence",
                "later acquire separately authorized fresh real market observation evidence",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(Path(__file__).with_name("I123_EXECUTION_BACKEND_PORTFOLIO.json")),
    )
    args = parser.parse_args()
    payload = current_snapshot()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
