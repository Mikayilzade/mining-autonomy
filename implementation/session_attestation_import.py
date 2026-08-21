"""I058 explicit I057 session -> I050 resource-attestation import boundary.

The import is offline and fail-closed. It preserves the exact I057 session and
transcript identities, rebuilds I054 evidence, and only emits an attestation
candidate when the session is complete and the I050 attestation is current.
No execution, network access, credentials, spend, or value movement is enabled.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from local_calibration_session import (
    LocalCalibrationSession,
    replay_session_bundle,
    session_from_json,
    _declarations,
    _energy,
)
from python_local_calibration_fixture import replay_python_local_transcript
from resource_evidence_adapter import build_resource_evidence, normalize_probe_summary_for_evidence
from resource_profile_evidence import ResourceProfileAttestation, attest_resource_profile
from resource_router import ExecutionBackend


@dataclass(frozen=True)
class SessionAttestationImport:
    backend_id: str
    state: str
    reasons: tuple[str, ...]
    session_digest: str
    transcript_digest: str
    transcript_file_digest: str
    collector_observed_at_utc: str
    source_kinds: tuple[str, ...]
    emitted_parameters: tuple[str, ...]
    missing_parameters: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    attestation_state: Optional[str]
    attestation_evidence_bundle_hash: Optional[str]
    attestation: Optional[ResourceProfileAttestation]
    attestation_candidate: bool
    planning_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _reference_mapping(reference_backend: ExecutionBackend | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(reference_backend, ExecutionBackend):
        return asdict(reference_backend)
    return dict(reference_backend)


def _rebuild_session_evidence(reference_backend: ExecutionBackend, session: LocalCalibrationSession):
    replay = replay_python_local_transcript(reference_backend, session.transcript_json)
    summary = normalize_probe_summary_for_evidence(
        replay.probe_summary,
        observed_at_utc=session.collector_observed_at_utc,
    )
    return replay, build_resource_evidence(
        replay.plan,
        probe_summary=summary,
        declarations=_declarations(session),
        energy_measurement=_energy(session),
    )


def import_session_attestation(
    reference_backend: ExecutionBackend,
    raw_session_json: str,
    *,
    now: datetime,
) -> SessionAttestationImport:
    """Replay one I057 bundle and cross the I050 boundary only if complete/current."""
    if now.tzinfo is None or now.utcoffset() != timezone.utc.utcoffset(now):
        raise ValueError("now_must_be_utc")

    report = replay_session_bundle(reference_backend, raw_session_json)
    session = session_from_json(raw_session_json)
    replay, evidence = _rebuild_session_evidence(reference_backend, session)

    if evidence.backend_id != report.backend_id:
        raise ValueError("session_evidence_backend_mismatch")
    if evidence.emitted_parameters != report.emitted_parameters:
        raise ValueError("session_evidence_emitted_parameter_mismatch")
    if evidence.missing_parameters != report.missing_parameters:
        raise ValueError("session_evidence_missing_parameter_mismatch")
    if evidence.source_kinds != report.source_kinds:
        raise ValueError("session_evidence_source_kind_mismatch")
    if evidence.complete_for_attestation != report.complete_for_attestation:
        raise ValueError("session_evidence_completeness_mismatch")

    transcript_digest = replay.probe_summary.transcript_digest
    evidence_hashes = tuple(record.evidence_hash or "" for record in evidence.records)
    base = dict(
        backend_id=session.backend_id,
        session_digest=session.immutable_session_digest,
        transcript_digest=transcript_digest,
        transcript_file_digest=session.transcript_file_digest,
        collector_observed_at_utc=session.collector_observed_at_utc,
        source_kinds=evidence.source_kinds,
        emitted_parameters=evidence.emitted_parameters,
        missing_parameters=evidence.missing_parameters,
        evidence_hashes=evidence_hashes,
    )

    if not evidence.complete_for_attestation:
        return SessionAttestationImport(
            state="planning_only_incomplete_session",
            reasons=tuple(f"missing_resource_evidence:{p}" for p in evidence.missing_parameters),
            attestation_state=None,
            attestation_evidence_bundle_hash=None,
            attestation=None,
            attestation_candidate=False,
            **base,
        )

    attestation = attest_resource_profile(
        _reference_mapping(reference_backend),
        evidence.records,
        now=now,
    )
    if attestation.state not in {"calibrated_declared", "calibrated_reproducible"}:
        return SessionAttestationImport(
            state="planning_only_attestation_rejected",
            reasons=attestation.reasons or ("resource_attestation_not_current",),
            attestation_state=attestation.state,
            attestation_evidence_bundle_hash=attestation.evidence_bundle_hash,
            attestation=attestation,
            attestation_candidate=False,
            **base,
        )

    state = (
        "attestation_candidate_reproducible"
        if attestation.state == "calibrated_reproducible"
        else "attestation_candidate_declared"
    )
    return SessionAttestationImport(
        state=state,
        reasons=(),
        attestation_state=attestation.state,
        attestation_evidence_bundle_hash=attestation.evidence_bundle_hash,
        attestation=attestation,
        attestation_candidate=True,
        **base,
    )
