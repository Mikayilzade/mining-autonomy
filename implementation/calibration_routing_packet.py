"""I055 end-to-end offline calibration packet.

Composes I053 acquisition -> I054 evidence -> I050 attestation -> I052 attested
routing without executing probes or enabling network/value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable, Mapping, Optional, Any

from attested_execution_bridge import AttestedTaskObservation, observe_and_route_with_attested_resources
from evaluator import CapabilityProfile, CostProfile
from resource_calibration_acquisition import CalibrationAcquisitionPlan, ProbeSummary, build_local_no_spend_plan
from resource_evidence_adapter import EnergyMeasurement, EvidenceBuildResult, ExplicitDeclaration, build_resource_evidence, normalize_probe_summary_for_evidence
from resource_profile_evidence import ResourceProfileAttestation, attest_resource_profile
from resource_router import ExecutionBackend

@dataclass(frozen=True)
class CalibrationRoutingPacket:
    backend_id: str
    acquisition_plan: CalibrationAcquisitionPlan
    evidence_build: EvidenceBuildResult
    resource_attestation: ResourceProfileAttestation
    routed_task: AttestedTaskObservation
    calibration_state: str
    evidence_bundle_hash: Optional[str]
    emitted_parameters: tuple[str, ...]
    missing_parameters: tuple[str, ...]
    state: str
    reasons: tuple[str, ...]
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False

def build_calibration_routing_packet(reference_backend: ExecutionBackend, *, benchmark_id: str, expected_output_digest: str, now: datetime, platform: str, task_payload: Mapping[str, Any], demand_evidence_class: str, probe_summary: Optional[ProbeSummary] = None, probe_observed_at_utc: Optional[str] = None, declarations: Iterable[ExplicitDeclaration] = (), energy_measurement: Optional[EnergyMeasurement] = None, capabilities: CapabilityProfile | None = None, cost: CostProfile | None = None) -> CalibrationRoutingPacket:
    reference = asdict(reference_backend)
    plan = build_local_no_spend_plan(reference, benchmark_id=benchmark_id, expected_output_digest=expected_output_digest)
    normalized_probe = probe_summary
    if probe_summary is not None:
        if not probe_observed_at_utc:
            raise ValueError("probe_observed_at_utc_required")
        normalized_probe = normalize_probe_summary_for_evidence(probe_summary, observed_at_utc=probe_observed_at_utc)
    elif probe_observed_at_utc is not None:
        raise ValueError("probe_timestamp_without_probe_summary")
    evidence = build_resource_evidence(plan, probe_summary=normalized_probe, declarations=tuple(declarations), energy_measurement=energy_measurement)
    attestation = attest_resource_profile(reference, evidence.records, now=now)
    routed = observe_and_route_with_attested_resources(platform, task_payload, demand_evidence_class=demand_evidence_class, capabilities=capabilities, cost=cost, reference_backends=(reference_backend,), attestations=(attestation,))
    reasons = list(routed.reasons)
    if evidence.missing_parameters:
        reasons.append("resource_calibration_evidence_incomplete")
    if attestation.state == "planning_only":
        reasons.append("resource_attestation_planning_only")
    if routed.selected_evidence_bundle_hash and routed.selected_evidence_bundle_hash != attestation.evidence_bundle_hash:
        raise ValueError("routed_evidence_bundle_hash_mismatch")
    if routed.selected_calibration_state and routed.selected_calibration_state != attestation.state:
        raise ValueError("routed_calibration_state_mismatch")
    return CalibrationRoutingPacket(reference_backend.backend_id, plan, evidence, attestation, routed, attestation.state, attestation.evidence_bundle_hash, evidence.emitted_parameters, evidence.missing_parameters, routed.state, tuple(dict.fromkeys(reasons)))

def calibration_routing_record(packet: CalibrationRoutingPacket) -> dict[str, Any]:
    record = asdict(packet)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["value_movement_enabled"] = False
    return record
