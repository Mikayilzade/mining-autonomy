"""I059 session-import -> attested-routing provenance bridge for python_local.

Consumes an I058 session import candidate, routes an already policy/demand-eligible
opportunity through I052, and seals the selected dry-run route to the exact I057
session/transcript and I050 evidence bundle. No execution, network access,
credentials, spend, or value movement is enabled.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Mapping, Optional

from attested_execution_bridge import AttestedTaskObservation, observe_and_route_with_attested_resources
from evaluator import CapabilityProfile, CostProfile
from resource_router import ExecutionBackend
from session_attestation_import import SessionAttestationImport, import_session_attestation


@dataclass(frozen=True)
class SessionRoutedProvenance:
    backend_id: str
    state: str
    reasons: tuple[str, ...]
    session_import_state: str
    session_digest: str
    transcript_digest: str
    transcript_file_digest: str
    evidence_hashes: tuple[str, ...]
    attestation_state: Optional[str]
    attestation_evidence_bundle_hash: Optional[str]
    routed_task: AttestedTaskObservation
    selected_backend_id: Optional[str]
    selected_calibration_state: Optional[str]
    selected_evidence_bundle_hash: Optional[str]
    provenance_binding_hash: str
    provenance_verified: bool
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _stable_hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def _binding_payload(*, backend_id: str, session_digest: str, transcript_digest: str,
                     transcript_file_digest: str, evidence_hashes: tuple[str, ...],
                     attestation_state: Optional[str], attestation_evidence_bundle_hash: Optional[str],
                     selected_backend_id: Optional[str], selected_calibration_state: Optional[str],
                     selected_evidence_bundle_hash: Optional[str], routed_state: str,
                     routed_external_id: str) -> dict[str, Any]:
    return {
        "backend_id": backend_id,
        "session_digest": session_digest,
        "transcript_digest": transcript_digest,
        "transcript_file_digest": transcript_file_digest,
        "evidence_hashes": list(evidence_hashes),
        "attestation_state": attestation_state,
        "attestation_evidence_bundle_hash": attestation_evidence_bundle_hash,
        "selected_backend_id": selected_backend_id,
        "selected_calibration_state": selected_calibration_state,
        "selected_evidence_bundle_hash": selected_evidence_bundle_hash,
        "routed_state": routed_state,
        "routed_external_id": routed_external_id,
    }


def _verify_selected_route(imported: SessionAttestationImport, routed: AttestedTaskObservation) -> None:
    if routed.selected_backend_id is None:
        return
    if not imported.attestation_candidate or imported.attestation is None:
        raise ValueError("selected_route_without_session_attestation_candidate")
    if routed.selected_backend_id != imported.backend_id:
        raise ValueError("selected_backend_session_mismatch")
    if routed.selected_calibration_state != imported.attestation_state:
        raise ValueError("selected_calibration_state_session_mismatch")
    if routed.selected_evidence_bundle_hash != imported.attestation_evidence_bundle_hash:
        raise ValueError("selected_evidence_bundle_hash_session_mismatch")


def route_python_local_session(reference_backend: ExecutionBackend, raw_session_json: str, *, now: datetime,
                               platform: str, task_payload: Mapping[str, Any], demand_evidence_class: str,
                               observed_at: str | None = None, capabilities: CapabilityProfile | None = None,
                               cost: CostProfile | None = None) -> SessionRoutedProvenance:
    if reference_backend.backend_id != "python_local":
        raise ValueError("i059_python_local_only")

    imported = import_session_attestation(reference_backend, raw_session_json, now=now)
    attestations = (imported.attestation,) if imported.attestation_candidate and imported.attestation else ()
    routed = observe_and_route_with_attested_resources(
        platform, task_payload, demand_evidence_class=demand_evidence_class, observed_at=observed_at,
        capabilities=capabilities, cost=cost, reference_backends=(reference_backend,), attestations=attestations,
    )
    _verify_selected_route(imported, routed)

    reasons = list(routed.reasons)
    state = routed.state
    provenance_verified = False
    if routed.upstream_state == "accept_dry_run" and not imported.attestation_candidate:
        state = "hold"
        reasons.append("session_attestation_not_routable")
        reasons.extend(imported.reasons)
    elif routed.selected_backend_id is not None:
        provenance_verified = True

    binding_hash = _stable_hash(_binding_payload(
        backend_id=imported.backend_id, session_digest=imported.session_digest,
        transcript_digest=imported.transcript_digest, transcript_file_digest=imported.transcript_file_digest,
        evidence_hashes=imported.evidence_hashes, attestation_state=imported.attestation_state,
        attestation_evidence_bundle_hash=imported.attestation_evidence_bundle_hash,
        selected_backend_id=routed.selected_backend_id, selected_calibration_state=routed.selected_calibration_state,
        selected_evidence_bundle_hash=routed.selected_evidence_bundle_hash, routed_state=state,
        routed_external_id=routed.external_id,
    ))
    return SessionRoutedProvenance(
        backend_id=imported.backend_id, state=state, reasons=tuple(dict.fromkeys(reasons)),
        session_import_state=imported.state, session_digest=imported.session_digest,
        transcript_digest=imported.transcript_digest, transcript_file_digest=imported.transcript_file_digest,
        evidence_hashes=imported.evidence_hashes, attestation_state=imported.attestation_state,
        attestation_evidence_bundle_hash=imported.attestation_evidence_bundle_hash, routed_task=routed,
        selected_backend_id=routed.selected_backend_id, selected_calibration_state=routed.selected_calibration_state,
        selected_evidence_bundle_hash=routed.selected_evidence_bundle_hash, provenance_binding_hash=binding_hash,
        provenance_verified=provenance_verified,
    )


def session_routed_record(packet: SessionRoutedProvenance) -> dict[str, Any]:
    record = asdict(packet)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["value_movement_enabled"] = False
    return record


def verify_session_routed_record(record: Mapping[str, Any]) -> bool:
    if record.get("dry_run_only") is not True:
        raise ValueError("record_not_dry_run_only")
    if any(record.get(k) is not False for k in ("execution_enabled", "network_enabled", "value_movement_enabled")):
        raise ValueError("record_inertness_violation")
    routed = record.get("routed_task")
    if not isinstance(routed, Mapping):
        raise ValueError("routed_task_record_missing")
    selected_backend = record.get("selected_backend_id")
    selected_calibration = record.get("selected_calibration_state")
    selected_bundle = record.get("selected_evidence_bundle_hash")
    if selected_backend is not None:
        if selected_backend != routed.get("selected_backend_id"):
            raise ValueError("record_selected_backend_drift")
        if selected_calibration != routed.get("selected_calibration_state"):
            raise ValueError("record_selected_calibration_drift")
        if selected_bundle != routed.get("selected_evidence_bundle_hash"):
            raise ValueError("record_selected_evidence_bundle_drift")
        if selected_backend != record.get("backend_id"):
            raise ValueError("record_session_backend_drift")
        if selected_calibration != record.get("attestation_state"):
            raise ValueError("record_attestation_state_drift")
        if selected_bundle != record.get("attestation_evidence_bundle_hash"):
            raise ValueError("record_attestation_bundle_drift")
    expected = _stable_hash(_binding_payload(
        backend_id=str(record.get("backend_id")), session_digest=str(record.get("session_digest")),
        transcript_digest=str(record.get("transcript_digest")), transcript_file_digest=str(record.get("transcript_file_digest")),
        evidence_hashes=tuple(record.get("evidence_hashes") or ()), attestation_state=record.get("attestation_state"),
        attestation_evidence_bundle_hash=record.get("attestation_evidence_bundle_hash"), selected_backend_id=selected_backend,
        selected_calibration_state=selected_calibration, selected_evidence_bundle_hash=selected_bundle,
        routed_state=str(record.get("state")), routed_external_id=str(routed.get("external_id")),
    ))
    if expected != record.get("provenance_binding_hash"):
        raise ValueError("record_provenance_binding_hash_mismatch")
    return True
