"""Evidence-backed Resource Router integration (I051).

Synthetic/default router profiles are planning references only. Calibrated routing
requires a complete current I050 attestation bound to the exact reference backend.
No execution, network access, credentials, or value movement is enabled here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Optional

from resource_router import BackendQuote, ExecutionBackend, RoutingDecision, TaskEconomics, quote_backend, route_task
from resource_profile_evidence import ResourceProfileAttestation, materialize_calibrated_backend_fields


@dataclass(frozen=True)
class ResourceRouteEntry:
    backend_id: str
    calibration_state: str
    route_state: str
    reference_quote: BackendQuote
    calibrated_quote: Optional[BackendQuote]
    evidence_bundle_hash: Optional[str]
    selectable: bool = False


@dataclass(frozen=True)
class AttestedRoutingDecision:
    task_id: str
    state: str
    selected_backend_id: Optional[str]
    selected_calibration_state: Optional[str]
    selected_quote: Optional[BackendQuote]
    entries: tuple[ResourceRouteEntry, ...]
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _backend_map(backends: Iterable[ExecutionBackend]) -> dict[str, ExecutionBackend]:
    out: dict[str, ExecutionBackend] = {}
    for backend in backends:
        if backend.backend_id in out:
            raise ValueError("duplicate_reference_backend_id")
        out[backend.backend_id] = backend
    return out


def _attestation_map(attestations: Iterable[ResourceProfileAttestation]) -> dict[str, ResourceProfileAttestation]:
    out: dict[str, ResourceProfileAttestation] = {}
    for attestation in attestations:
        if attestation.backend_id in out:
            raise ValueError("duplicate_resource_attestation")
        out[attestation.backend_id] = attestation
    return out


def _materialize_backend(reference: ExecutionBackend, attestation: ResourceProfileAttestation) -> ExecutionBackend:
    fields = materialize_calibrated_backend_fields(asdict(reference), attestation)
    fields.pop("_resource_attestation", None)
    return ExecutionBackend(**fields)


def route_task_with_attested_resources(
    task: TaskEconomics,
    reference_backends: Iterable[ExecutionBackend],
    attestations: Iterable[ResourceProfileAttestation] = (),
) -> AttestedRoutingDecision:
    """Route only across complete current I050-calibrated resources."""
    refs = _backend_map(reference_backends)
    attested = _attestation_map(attestations)
    if sorted(set(attested) - set(refs)):
        raise ValueError("attestation_without_reference_backend")

    entries: list[ResourceRouteEntry] = []
    calibrated_backends: list[ExecutionBackend] = []
    calibration_states: dict[str, str] = {}

    for backend_id in sorted(refs):
        reference = refs[backend_id]
        reference_quote = quote_backend(task, reference)
        attestation = attested.get(backend_id)

        if attestation is None or attestation.state == "planning_only":
            entries.append(ResourceRouteEntry(
                backend_id=backend_id,
                calibration_state="reference_only",
                route_state="resource_evidence_missing",
                reference_quote=reference_quote,
                calibrated_quote=None,
                evidence_bundle_hash=None if attestation is None else attestation.evidence_bundle_hash,
                selectable=False,
            ))
            continue

        if attestation.state not in {"calibrated_declared", "calibrated_reproducible"}:
            raise ValueError("unsupported_resource_attestation_state")

        calibrated = _materialize_backend(reference, attestation)
        calibrated_quote = quote_backend(task, calibrated)
        route_state = "calibrated_declared_route" if attestation.state == "calibrated_declared" else "calibrated_reproducible_route"
        entries.append(ResourceRouteEntry(
            backend_id=backend_id,
            calibration_state=attestation.state,
            route_state=route_state,
            reference_quote=reference_quote,
            calibrated_quote=calibrated_quote,
            evidence_bundle_hash=attestation.evidence_bundle_hash,
            selectable=calibrated_quote.planning_state == "eligible_dry_run",
        ))
        calibrated_backends.append(calibrated)
        calibration_states[backend_id] = attestation.state

    if not calibrated_backends:
        return AttestedRoutingDecision(task.task_id, "resource_evidence_missing", None, None, None, tuple(entries))

    routed: RoutingDecision = route_task(task, calibrated_backends)
    if routed.state != "route_dry_run" or routed.selected_backend_id is None:
        return AttestedRoutingDecision(task.task_id, "hold", None, None, None, tuple(entries))

    return AttestedRoutingDecision(
        task_id=task.task_id,
        state="route_dry_run",
        selected_backend_id=routed.selected_backend_id,
        selected_calibration_state=calibration_states[routed.selected_backend_id],
        selected_quote=routed.selected_quote,
        entries=tuple(entries),
    )


def attested_route_record(decision: AttestedRoutingDecision) -> dict:
    record = asdict(decision)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["value_movement_enabled"] = False
    return record
