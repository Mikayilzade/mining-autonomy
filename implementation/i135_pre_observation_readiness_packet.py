"""I135 integrated pre-observation readiness packet.

Synthesizes the current state without performing the observation. A later real
read-only observation remains separately gated by fresh market/policy evidence,
a current conservative resource route, exact-current runtime evidence, and exact
user authorization. This module only combines already-supplied facts.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Optional

from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from i133_conservative_route_gate import ConservativeRouteGate


@dataclass(frozen=True)
class PreObservationReadiness:
    state: str
    backend_id: Optional[str]
    runtime_receipt_current: bool
    backend_evidence_ready: bool
    conservative_economics_ready: bool
    watcher_overhead_accounted: bool
    fresh_market_policy_evidence_ready: bool
    exact_observation_authorization_present: bool
    blockers: tuple[str, ...]
    observation_enabled: bool = False
    task_acceptance_enabled: bool = False
    spend_enabled: bool = False
    value_movement_enabled: bool = False


def assess(
    *,
    runtime_receipt_current: bool,
    backend_evidence: BackendEvidence | None,
    route_gate: ConservativeRouteGate | None,
    fresh_market_policy_evidence_ready: bool,
    exact_observation_authorization_present: bool,
) -> PreObservationReadiness:
    blockers=[]
    backend_id=backend_evidence.backend_id if backend_evidence else None
    backend_ready=bool(
        backend_evidence
        and backend_evidence.provenance_class == MEASURED
        and backend_evidence.current_reproducible
        and backend_evidence.non_synthetic
        and backend_evidence.capacity_verified
        and backend_evidence.policy_evidence_current
    )
    econ_ready=bool(route_gate and route_gate.conservative_route_survives)
    watcher_accounted=bool(route_gate and route_gate.watcher_daily_candidates > 0)
    if not runtime_receipt_current: blockers.append("exact_current_runtime_receipt_absent")
    if not backend_ready: blockers.append("measured_non_synthetic_backend_evidence_absent")
    if not econ_ready: blockers.append("conservative_route_economics_not_ready")
    if not watcher_accounted: blockers.append("watcher_acquisition_overhead_not_accounted")
    if not fresh_market_policy_evidence_ready: blockers.append("fresh_market_policy_evidence_absent")
    if not exact_observation_authorization_present: blockers.append("exact_observation_authorization_absent")
    ready=not blockers
    return PreObservationReadiness(
        state="READY_FOR_SINGLE_READ_ONLY_OBSERVATION" if ready else "HOLD",
        backend_id=backend_id,
        runtime_receipt_current=runtime_receipt_current,
        backend_evidence_ready=backend_ready,
        conservative_economics_ready=econ_ready,
        watcher_overhead_accounted=watcher_accounted,
        fresh_market_policy_evidence_ready=fresh_market_policy_evidence_ready,
        exact_observation_authorization_present=exact_observation_authorization_present,
        blockers=tuple(blockers),
    )


def payload(result: PreObservationReadiness) -> dict:
    body=asdict(result)
    body.update({
        "schema":"mining-autonomy/i135-pre-observation-readiness/v1",
        "run":"I135",
        "production_observation_performed":False,
        "credentials_used":False,
        "network_access_performed":False,
        "spend_or_value_movement":False,
    })
    return body
