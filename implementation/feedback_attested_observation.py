"""I063 propagate verified resource feedback into an I052 attested task record.

The original market observation/economics/demand evidence is immutable. Verified
I061/I062 resource feedback may replace only the attested resource parameters it
measured, then reroute the same task across the same reference backend set. The
bridge fails closed on task/backend/provenance mismatch and never enables execution,
network access, credentials, submission, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Optional

from attested_execution_bridge import AttestedTaskObservation
from benchmark_feedback_integration import FeedbackMergeResult, merge_verified_feedback, routing_delta
from receipt_replay_calibration import CalibrationFeedback
from resource_profile_evidence import ResourceEvidence, ResourceProfileAttestation, attest_resource_profile
from resource_router import ExecutionBackend
from resource_routing_attestation import AttestedRoutingDecision, route_task_with_attested_resources


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def _attestation_map(items: Iterable[ResourceProfileAttestation]) -> dict[str, ResourceProfileAttestation]:
    out = {}
    for item in items:
        if item.backend_id in out:
            raise ValueError("duplicate_resource_attestation")
        out[item.backend_id] = item
    return out


def _backend_map(items: Iterable[ExecutionBackend]) -> dict[str, ExecutionBackend]:
    out = {}
    for item in items:
        if item.backend_id in out:
            raise ValueError("duplicate_reference_backend_id")
        out[item.backend_id] = item
    return out


@dataclass(frozen=True)
class FeedbackAttestedTaskUpdate:
    state: str
    reasons: tuple[str, ...]
    platform: str
    external_id: str
    task_id: Optional[str]
    target_backend_id: str
    original_observation_hash: str
    original_task_economics_hash: Optional[str]
    original_routing_hash: Optional[str]
    feedback_receipt_hash: str
    feedback_evidence_hashes: tuple[str, ...]
    replaced_parameters: tuple[str, ...]
    before_target_evidence_bundle_hash: Optional[str]
    after_target_evidence_bundle_hash: Optional[str]
    before_selected_backend_id: Optional[str]
    after_selected_backend_id: Optional[str]
    route_delta: Optional[Mapping[str, Any]]
    provenance_binding_hash: Optional[str]
    original_observation: AttestedTaskObservation
    refreshed_target_attestation: Optional[ResourceProfileAttestation]
    refreshed_routing: Optional[AttestedRoutingDecision]
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False


def _hold(original, target_backend_id, feedback, reasons, *, task_hash=None, routing_hash=None, before_bundle=None):
    return FeedbackAttestedTaskUpdate(
        "hold", tuple(dict.fromkeys(reasons)), original.platform, original.external_id,
        None if original.task_economics is None else original.task_economics.task_id,
        target_backend_id, _hash(asdict(original)), task_hash, routing_hash, feedback.receipt_hash,
        tuple(x.evidence_hash or x.computed_hash() for x in feedback.evidence_records), (), before_bundle, None,
        None if original.attested_routing is None else original.attested_routing.selected_backend_id,
        None, None, None, original, None, None,
    )


def apply_feedback_to_attested_observation(
    original: AttestedTaskObservation,
    *, reference_backends: Iterable[ExecutionBackend], attestations: Iterable[ResourceProfileAttestation],
    existing_evidence_by_backend: Mapping[str, Iterable[ResourceEvidence]], feedback: CalibrationFeedback,
    now: datetime,
) -> FeedbackAttestedTaskUpdate:
    reasons: list[str] = []
    target = feedback.backend_id
    original_hash = _hash(asdict(original))
    if any((not original.dry_run_only, original.execution_enabled, original.network_enabled, original.value_movement_enabled)):
        reasons.append("original_observation_not_inert")
    if not original.upstream_gate_passed or original.task_economics is None or original.attested_routing is None:
        reasons.append("original_observation_not_resource_routable")
    task = original.task_economics
    task_hash = None if task is None else _hash(asdict(task))
    routing_hash = None if original.attested_routing is None else _hash(asdict(original.attested_routing))
    if task is not None and task.task_id != original.external_id:
        reasons.append("original_task_identity_mismatch")
    try:
        refs = _backend_map(reference_backends)
        old_atts = _attestation_map(attestations)
    except ValueError as exc:
        reasons.append(str(exc))
        return _hold(original, target, feedback, reasons, task_hash=task_hash, routing_hash=routing_hash)
    if target not in refs:
        reasons.append("feedback_backend_without_reference")
    if target not in old_atts:
        reasons.append("feedback_backend_without_prior_attestation")
    evidence = tuple(existing_evidence_by_backend.get(target, ()))
    if not evidence:
        reasons.append("feedback_backend_evidence_missing")
    before_bundle = old_atts[target].evidence_bundle_hash if target in old_atts else None
    if reasons or task is None or original.attested_routing is None:
        return _hold(original, target, feedback, reasons, task_hash=task_hash, routing_hash=routing_hash, before_bundle=before_bundle)

    replay_before = route_task_with_attested_resources(task, tuple(refs.values()), tuple(old_atts.values()))
    if _hash(asdict(replay_before)) != routing_hash:
        reasons.append("original_routing_provenance_mismatch")
    replay_target_attestation = attest_resource_profile(refs[target].__dict__, evidence, now=now)
    if _hash(asdict(replay_target_attestation)) != _hash(asdict(old_atts[target])):
        reasons.append("target_evidence_provenance_mismatch")
    if reasons:
        return _hold(original, target, feedback, reasons, task_hash=task_hash, routing_hash=routing_hash, before_bundle=before_bundle)

    merged: FeedbackMergeResult = merge_verified_feedback(refs[target], evidence, feedback, task, now=now)
    if merged.attestation is None or merged.state not in {"feedback_integrated_route_dry_run", "feedback_integrated_hold"}:
        reasons.append(f"feedback_merge_not_routable:{merged.state}")
        reasons.extend(merged.reasons)
        return _hold(original, target, feedback, reasons, task_hash=task_hash, routing_hash=routing_hash, before_bundle=before_bundle)

    refreshed_atts = dict(old_atts)
    refreshed_atts[target] = merged.attestation
    after = route_task_with_attested_resources(task, tuple(refs.values()), tuple(refreshed_atts.values()))
    delta = routing_delta(replay_before, after)
    feedback_hashes = tuple(x.evidence_hash or x.computed_hash() for x in feedback.evidence_records)
    after_bundle = merged.attestation.evidence_bundle_hash
    provenance = _hash({
        "original_observation_hash": original_hash, "original_task_economics_hash": task_hash,
        "original_routing_hash": routing_hash, "target_backend_id": target,
        "before_target_evidence_bundle_hash": before_bundle, "after_target_evidence_bundle_hash": after_bundle,
        "feedback_receipt_hash": feedback.receipt_hash, "feedback_evidence_hashes": feedback_hashes,
        "replaced_parameters": merged.replaced_parameters, "after_routing_hash": _hash(asdict(after)),
    })
    state = "feedback_refreshed_route_dry_run" if after.state == "route_dry_run" else "feedback_refreshed_hold"
    return FeedbackAttestedTaskUpdate(
        state, (), original.platform, original.external_id, task.task_id, target, original_hash, task_hash, routing_hash,
        feedback.receipt_hash, feedback_hashes, merged.replaced_parameters, before_bundle, after_bundle,
        replay_before.selected_backend_id, after.selected_backend_id, delta, provenance, original, merged.attestation, after,
    )


def feedback_attested_task_record(update: FeedbackAttestedTaskUpdate) -> dict[str, Any]:
    record = asdict(update)
    record.update(dry_run_only=True, execution_enabled=False, network_enabled=False,
                  credentials_enabled=False, submission_enabled=False, value_movement_enabled=False)
    return record
