"""End-to-end observation -> attested resource routing bridge (I052).

Upstream policy/capability/quality/demand acceptance is authoritative. Resource
attestation can only narrow an accepted dry-run candidate; it can never rescue a
held/rejected task. No execution, network, credentials, or value movement occurs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Optional

from evaluator import CapabilityProfile, CostProfile
from orchestrator import observe_task
from execution_routing_integration import task_economics_from_payload
from resource_profile_evidence import ResourceProfileAttestation
from resource_router import ExecutionBackend, TaskEconomics
from resource_routing_attestation import AttestedRoutingDecision, route_task_with_attested_resources


@dataclass(frozen=True)
class AttestedTaskObservation:
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
    attested_routing: Optional[AttestedRoutingDecision]
    selected_backend_id: Optional[str]
    selected_calibration_state: Optional[str]
    selected_evidence_bundle_hash: Optional[str]
    upstream_gate_passed: bool
    resource_gate_passed: bool
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def observe_and_route_with_attested_resources(
    platform: str,
    payload: Mapping,
    *,
    demand_evidence_class: str = "unknown",
    observed_at: str | None = None,
    capabilities: CapabilityProfile | None = None,
    cost: CostProfile | None = None,
    reference_backends: Iterable[ExecutionBackend] = (),
    attestations: Iterable[ResourceProfileAttestation] = (),
) -> AttestedTaskObservation:
    observation = observe_task(
        platform, dict(payload), demand_evidence_class=demand_evidence_class,
        observed_at=observed_at, capabilities=capabilities, cost=cost,
    )
    if observation.state != "accept_dry_run":
        return AttestedTaskObservation(
            observation.platform, observation.external_id, observation.state,
            observation.reasons, observation.state, observation.expected_margin_usd,
            observation.demand_evidence_class, observation.evidence_strength,
            observation.open_paid_demand_proven, None, None, None, None, None,
            False, False,
        )

    economics = task_economics_from_payload(platform, payload, observed_at=observed_at)
    routing = route_task_with_attested_resources(economics, tuple(reference_backends), tuple(attestations))
    reasons = list(observation.reasons)
    state = routing.state
    if routing.state != "route_dry_run":
        state = "hold"
        reasons.append("attested_resource_route_unavailable")
        if routing.state == "resource_evidence_missing":
            reasons.append("resource_evidence_missing")

    selected_hash = None
    if routing.selected_backend_id is not None:
        for entry in routing.entries:
            if entry.backend_id == routing.selected_backend_id:
                selected_hash = entry.evidence_bundle_hash
                break

    return AttestedTaskObservation(
        observation.platform, observation.external_id, state,
        tuple(dict.fromkeys(reasons)), observation.state, observation.expected_margin_usd,
        observation.demand_evidence_class, observation.evidence_strength,
        observation.open_paid_demand_proven, economics, routing,
        routing.selected_backend_id, routing.selected_calibration_state, selected_hash,
        True, routing.state == "route_dry_run",
    )


def attested_task_record(item: AttestedTaskObservation) -> dict:
    record = asdict(item)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["value_movement_enabled"] = False
    return record
