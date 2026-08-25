#!/usr/bin/env python3
from dataclasses import replace

from i123_execution_backend_portfolio import BackendEvidence, route_portfolio
from resource_router import TaskEconomics, default_backend_families


def measured_evidence(backend_id: str) -> BackendEvidence:
    return BackendEvidence(
        backend_id=backend_id,
        provenance_class="measured_reproducible",
        current_reproducible=True,
        non_synthetic=True,
        capacity_verified=True,
        policy_evidence_current=True,
        source_class="measurement_receipt",
        source_artifact_id="i196-synthetic-regression-receipt",
        source_artifact_sha256="a" * 64,
        observed_at_utc="2026-08-25T06:45:00Z",
    )


def task() -> TaskEconomics:
    return TaskEconomics(
        task_id="i196-fixed-cost-guard",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=5.0,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.50,
        minimum_expected_margin_ratio=0.10,
    )


def test_non_sunk_fixed_cost_cannot_fail_open_after_allocation() -> None:
    base = next(b for b in default_backend_families() if b.backend_id == "python_local")
    expensive = replace(
        base,
        fixed_monthly_cost_usd=100.0,
        sunk_or_already_committed=False,
        allocation_basis_tasks_per_month=10.0,
    )
    decision = route_portfolio(task(), (expensive,), (measured_evidence(expensive.backend_id),), ai_allowed=False)
    assert decision.state == "hold"
    assert decision.selected_backend_id is None
    blockers = decision.quotes[0].production_blockers
    assert "nonpositive_margin_after_fixed_allocation" in blockers
    assert "insufficient_conservative_margin_after_fixed_allocation" in blockers


def test_small_allocated_fixed_cost_can_remain_eligible() -> None:
    base = next(b for b in default_backend_families() if b.backend_id == "python_local")
    affordable = replace(
        base,
        fixed_monthly_cost_usd=1.0,
        sunk_or_already_committed=False,
        allocation_basis_tasks_per_month=100.0,
    )
    decision = route_portfolio(task(), (affordable,), (measured_evidence(affordable.backend_id),), ai_allowed=False)
    assert decision.state == "production_route_ready"
    assert decision.selected_backend_id == affordable.backend_id
    assert decision.quotes[0].base_quote.expected_margin_after_fixed_allocation_usd > 0


if __name__ == "__main__":
    test_non_sunk_fixed_cost_cannot_fail_open_after_allocation()
    test_small_allocated_fixed_cost_can_remain_eligible()
    print("I196 fixed-cost margin regression: PASS")
