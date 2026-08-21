"""I066 exact evidence-bundle materialization for verified I065 snapshots.

This layer converts provenance-only I065 state into quantitative current resource
profiles only when every latest evidence reference resolves against its exact,
fresh I050 evidence bundle. It stays fail-closed and never enables execution,
network access, credentials, submission, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Optional

from resource_feedback_summary import (
    BackendEvidenceState,
    LatestParameterEvidenceRef,
    ResourceFeedbackHistorySnapshot,
    verify_resource_feedback_history_snapshot,
)
from resource_profile_evidence import (
    CRITICAL_PARAMETERS,
    ResourceEvidence,
    ResourceProfileAttestation,
    attest_resource_profile,
    reference_backend_hash,
)


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class MaterializedParameterValue:
    backend_id: str
    parameter: str
    value: Any
    evidence_id: str
    evidence_hash: str
    source_kind: str
    observed_at: str
    bound_evidence_bundle_hash: str
    evidence_binding_precision: str
    source_content_digest: Optional[str]


@dataclass(frozen=True)
class MaterializedBackendProfile:
    backend_id: str
    state: str
    reference_backend_hash: str
    anchor_evidence_bundle_hash: str
    anchor_sequence: int
    attestation_state: str
    calibrated_values: Mapping[str, Any]
    latest_parameter_values: tuple[MaterializedParameterValue, ...]
    all_current_evidence_reproducible: bool
    contains_user_declaration: bool
    quantitative_values_complete: bool


@dataclass(frozen=True)
class ResourceEvidenceMaterializationResult:
    state: str
    reasons: tuple[str, ...]
    snapshot_hash: str
    history_tip_hash: str
    backend_profiles: tuple[MaterializedBackendProfile, ...]
    quantitative_values_complete: bool
    materialization_hash: str
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("materialization_hash", None)
        return body


def _finalize(**kwargs: Any) -> ResourceEvidenceMaterializationResult:
    provisional = ResourceEvidenceMaterializationResult(materialization_hash="", **kwargs)
    return ResourceEvidenceMaterializationResult(materialization_hash=_hash(provisional.hash_body()), **kwargs)


def _bundle_records(evidence_bundles: Mapping[str, Iterable[ResourceEvidence]], bundle_hash: str) -> tuple[ResourceEvidence, ...]:
    records = evidence_bundles.get(bundle_hash)
    return () if records is None else tuple(records)


def _attest_exact_bundle(backend_id: str, reference_backend: Mapping[str, Any], expected_bundle_hash: str, records: tuple[ResourceEvidence, ...], *, now: datetime) -> tuple[Optional[ResourceProfileAttestation], tuple[str, ...]]:
    reasons: list[str] = []
    if not records:
        return None, (f"{backend_id}:missing_evidence_bundle:{expected_bundle_hash}",)
    try:
        attestation = attest_resource_profile(reference_backend, records, now=now)
    except Exception as exc:
        return None, (f"{backend_id}:bundle_attestation_error:{type(exc).__name__}",)
    if attestation.state not in {"calibrated_declared", "calibrated_reproducible"}:
        reasons.append(f"{backend_id}:bundle_not_currently_calibrated:{expected_bundle_hash}")
    if attestation.evidence_bundle_hash != expected_bundle_hash:
        reasons.append(f"{backend_id}:evidence_bundle_hash_mismatch:{expected_bundle_hash}")
    if attestation.backend_id != backend_id:
        reasons.append(f"{backend_id}:bundle_backend_mismatch")
    if len(attestation.calibrated_values) != len(CRITICAL_PARAMETERS):
        reasons.append(f"{backend_id}:bundle_missing_critical_values")
    return attestation, tuple(reasons)


def _resolve_ref(ref: LatestParameterEvidenceRef, records: tuple[ResourceEvidence, ...]) -> tuple[Optional[MaterializedParameterValue], tuple[str, ...]]:
    reasons: list[str] = []
    by_hash = {(record.evidence_hash or record.computed_hash()): record for record in records}
    if not ref.evidence_hashes:
        return None, (f"{ref.backend_id}:{ref.parameter}:empty_evidence_hash_binding",)
    if any(evidence_hash not in by_hash for evidence_hash in ref.evidence_hashes):
        reasons.append(f"{ref.backend_id}:{ref.parameter}:bound_evidence_hash_missing_from_bundle")
    if ref.evidence_binding_precision == "exact_single_parameter":
        if len(ref.evidence_hashes) != 1:
            reasons.append(f"{ref.backend_id}:{ref.parameter}:invalid_exact_single_parameter_binding")
    elif ref.evidence_binding_precision != "entry_set_only":
        reasons.append(f"{ref.backend_id}:{ref.parameter}:unsupported_evidence_binding_precision")
    candidates = [
        by_hash[evidence_hash]
        for evidence_hash in ref.evidence_hashes
        if evidence_hash in by_hash
        and by_hash[evidence_hash].backend_id == ref.backend_id
        and by_hash[evidence_hash].parameter == ref.parameter
        and by_hash[evidence_hash].observed_at == ref.observed_at
    ]
    if len(candidates) != 1:
        reasons.append(f"{ref.backend_id}:{ref.parameter}:parameter_evidence_mapping_not_exact")
    if reasons:
        return None, tuple(dict.fromkeys(reasons))
    evidence = candidates[0]
    evidence_hash = evidence.evidence_hash or evidence.computed_hash()
    return MaterializedParameterValue(
        backend_id=ref.backend_id, parameter=ref.parameter, value=evidence.value,
        evidence_id=evidence.evidence_id, evidence_hash=evidence_hash,
        source_kind=evidence.source_kind, observed_at=evidence.observed_at,
        bound_evidence_bundle_hash=ref.evidence_bundle_hash,
        evidence_binding_precision=ref.evidence_binding_precision,
        source_content_digest=evidence.source_content_digest,
    ), ()


def _materialize_backend(backend_state: BackendEvidenceState, reference_backend: Mapping[str, Any], evidence_bundles: Mapping[str, Iterable[ResourceEvidence]], *, now: datetime) -> tuple[Optional[MaterializedBackendProfile], tuple[str, ...]]:
    backend_id = backend_state.backend_id
    reasons: list[str] = []
    if str(reference_backend.get("backend_id") or "") != backend_id:
        return None, (f"{backend_id}:reference_backend_identity_mismatch",)
    if not backend_state.latest_parameters:
        return None, (f"{backend_id}:no_latest_parameter_references",)
    attestations: dict[str, ResourceProfileAttestation] = {}
    bundle_records: dict[str, tuple[ResourceEvidence, ...]] = {}
    resolved: list[MaterializedParameterValue] = []
    for ref in backend_state.latest_parameters:
        if ref.backend_id != backend_id:
            reasons.append(f"{backend_id}:snapshot_backend_reference_mismatch")
            continue
        records = _bundle_records(evidence_bundles, ref.evidence_bundle_hash)
        bundle_records[ref.evidence_bundle_hash] = records
        if ref.evidence_bundle_hash not in attestations:
            attestation, attestation_reasons = _attest_exact_bundle(backend_id, reference_backend, ref.evidence_bundle_hash, records, now=now)
            reasons.extend(attestation_reasons)
            if attestation is not None:
                attestations[ref.evidence_bundle_hash] = attestation
        value, ref_reasons = _resolve_ref(ref, records)
        reasons.extend(ref_reasons)
        if value is not None:
            resolved.append(value)
    anchor_refs = [ref for ref in backend_state.latest_parameters if ref.sequence == backend_state.last_update_sequence]
    anchor_hashes = {ref.evidence_bundle_hash for ref in anchor_refs}
    if len(anchor_hashes) != 1:
        reasons.append(f"{backend_id}:anchor_bundle_not_unique")
        anchor_hash = ""
    else:
        anchor_hash = next(iter(anchor_hashes))
    anchor_attestation = attestations.get(anchor_hash)
    if anchor_attestation is not None:
        anchor_records = bundle_records.get(anchor_hash, ())
        anchor_by_hash = {(record.evidence_hash or record.computed_hash()): record for record in anchor_records}
        for value in resolved:
            if value.evidence_hash not in anchor_by_hash:
                reasons.append(f"{backend_id}:{value.parameter}:latest_evidence_not_carried_into_anchor_bundle")
    if len(resolved) != len(backend_state.latest_parameters):
        reasons.append(f"{backend_id}:latest_parameter_resolution_incomplete")
    if reasons or anchor_attestation is None:
        return None, tuple(dict.fromkeys(reasons))
    profile = MaterializedBackendProfile(
        backend_id=backend_id,
        state="materialized_reproducible" if anchor_attestation.state == "calibrated_reproducible" else "materialized_declared",
        reference_backend_hash=reference_backend_hash(reference_backend),
        anchor_evidence_bundle_hash=anchor_hash,
        anchor_sequence=backend_state.last_update_sequence,
        attestation_state=anchor_attestation.state,
        calibrated_values=dict(anchor_attestation.calibrated_values),
        latest_parameter_values=tuple(sorted(resolved, key=lambda item: item.parameter)),
        all_current_evidence_reproducible=anchor_attestation.all_current_evidence_reproducible,
        contains_user_declaration=anchor_attestation.contains_user_declaration,
        quantitative_values_complete=True,
    )
    return profile, ()


def materialize_resource_feedback_snapshot(snapshot: ResourceFeedbackHistorySnapshot, *, reference_backends: Mapping[str, Mapping[str, Any]], evidence_bundles: Mapping[str, Iterable[ResourceEvidence]], now: datetime) -> ResourceEvidenceMaterializationResult:
    """Resolve I065 provenance into numeric resource profiles, fail-closed."""
    reasons: list[str] = []
    if not verify_resource_feedback_history_snapshot(snapshot):
        reasons.append("snapshot_hash_invalid")
    if snapshot.state != "verified_history_snapshot":
        reasons.append("snapshot_not_materializable")
    if not snapshot.backend_states:
        reasons.append("snapshot_has_no_backend_state")
    profiles: list[MaterializedBackendProfile] = []
    if not reasons:
        for backend_state in snapshot.backend_states:
            reference = reference_backends.get(backend_state.backend_id)
            if reference is None:
                reasons.append(f"{backend_state.backend_id}:reference_backend_missing")
                continue
            profile, backend_reasons = _materialize_backend(backend_state, reference, evidence_bundles, now=now)
            reasons.extend(backend_reasons)
            if profile is not None:
                profiles.append(profile)
    if reasons or len(profiles) != len(snapshot.backend_states):
        return _finalize(
            state="hold_unresolved_evidence", reasons=tuple(dict.fromkeys(reasons)),
            snapshot_hash=snapshot.snapshot_hash, history_tip_hash=snapshot.history_tip_hash,
            backend_profiles=(), quantitative_values_complete=False,
        )
    state = "materialized_reproducible" if all(profile.all_current_evidence_reproducible for profile in profiles) else "materialized_with_declarations"
    return _finalize(
        state=state, reasons=(), snapshot_hash=snapshot.snapshot_hash,
        history_tip_hash=snapshot.history_tip_hash,
        backend_profiles=tuple(sorted(profiles, key=lambda profile: profile.backend_id)),
        quantitative_values_complete=True,
    )


def verify_resource_evidence_materialization(result: ResourceEvidenceMaterializationResult) -> bool:
    return result.materialization_hash == _hash(result.hash_body())
