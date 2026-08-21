"""I060 inert local execution plan/receipt boundary.

Consumes only an I059-selected python_local dry-run route and a fixed deterministic
fixture. It binds task/provenance/expected-output identities and records observed
local runtime plus explicitly supplied energy/cost facts. It never submits to a
market, uses network/credentials, spends money, or moves value.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import time
from typing import Any, Callable, Mapping, Optional

from session_routed_provenance import SessionRoutedProvenance


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


@dataclass(frozen=True)
class LocalExecutionPlan:
    task_id: str
    backend_id: str
    provenance_binding_hash: str
    fixture_hash: str
    expected_output_hash: str
    router_marginal_cost_usd: float
    max_runtime_ratio: float = 2.0
    max_cost_drift_usd: float = 0.02
    dry_run_only: bool = True
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False


@dataclass(frozen=True)
class LocalExecutionReceipt:
    state: str
    reasons: tuple[str, ...]
    plan_hash: str
    task_id: str
    backend_id: str
    provenance_binding_hash: str
    fixture_hash: str
    output_hash: str
    output_matches_expected: bool
    runtime_seconds: float
    observed_energy_cost_usd: Optional[float]
    observed_total_incremental_cost_usd: Optional[float]
    router_marginal_cost_usd: float
    dry_run_only: bool = True
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False


def build_plan(packet: SessionRoutedProvenance, fixture: Mapping[str, Any], expected_output: Any) -> LocalExecutionPlan:
    if packet.state != "route_dry_run" or not packet.provenance_verified:
        raise ValueError("i059_route_not_verified")
    if packet.selected_backend_id != "python_local":
        raise ValueError("i060_python_local_only")
    quote = packet.routed_task.routing_decision.selected_quote if packet.routed_task.routing_decision else None
    if quote is None:
        raise ValueError("selected_router_quote_missing")
    return LocalExecutionPlan(
        task_id=packet.routed_task.external_id,
        backend_id="python_local",
        provenance_binding_hash=packet.provenance_binding_hash,
        fixture_hash=_hash(fixture),
        expected_output_hash=_hash(expected_output),
        router_marginal_cost_usd=float(quote.marginal_cost_usd),
    )


def execute_fixed_fixture(plan: LocalExecutionPlan, fixture: Mapping[str, Any], executor: Callable[[Mapping[str, Any]], Any], *,
                          energy_cost_usd: Optional[float] = None, other_incremental_cost_usd: float = 0.0) -> LocalExecutionReceipt:
    if any((plan.network_enabled, plan.credentials_enabled, plan.submission_enabled, plan.value_movement_enabled)):
        raise ValueError("execution_plan_not_inert")
    if _hash(fixture) != plan.fixture_hash:
        raise ValueError("fixture_identity_drift")
    if energy_cost_usd is not None and energy_cost_usd < 0:
        raise ValueError("negative_energy_cost")
    if other_incremental_cost_usd < 0:
        raise ValueError("negative_incremental_cost")
    started = time.perf_counter()
    output = executor(fixture)
    runtime = max(0.0, time.perf_counter() - started)
    output_hash = _hash(output)
    reasons = []
    matches = output_hash == plan.expected_output_hash
    if not matches:
        reasons.append("expected_output_identity_mismatch")
    observed_total = None if energy_cost_usd is None else energy_cost_usd + other_incremental_cost_usd
    if observed_total is not None and observed_total > plan.router_marginal_cost_usd + plan.max_cost_drift_usd:
        reasons.append("observed_incremental_cost_exceeds_router_quote")
    state = "receipt_verified_inert" if not reasons else "hold"
    plan_hash = _hash(asdict(plan))
    return LocalExecutionReceipt(
        state=state, reasons=tuple(reasons), plan_hash=plan_hash, task_id=plan.task_id,
        backend_id=plan.backend_id, provenance_binding_hash=plan.provenance_binding_hash,
        fixture_hash=plan.fixture_hash, output_hash=output_hash, output_matches_expected=matches,
        runtime_seconds=runtime, observed_energy_cost_usd=energy_cost_usd,
        observed_total_incremental_cost_usd=observed_total,
        router_marginal_cost_usd=plan.router_marginal_cost_usd,
    )


def receipt_record(receipt: LocalExecutionReceipt) -> dict[str, Any]:
    record = asdict(receipt)
    record.update(dry_run_only=True, network_enabled=False, credentials_enabled=False,
                  submission_enabled=False, value_movement_enabled=False)
    return record
