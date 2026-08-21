"""I067 verified current-resource snapshot -> attested routing replay bridge.

Re-materializes the I066 quantitative resource snapshot from its exact I065
history snapshot and bound I050 evidence bundles before allowing those resource
values to participate in the existing I052 dry-run routing path.

Upstream policy/capability/quality/demand gates remain authoritative. This module
never enables execution, network access, credentials, submission, or value
movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Optional

from evaluator import CapabilityProfile, CostProfile
from orchestrator import observe_task
from attested_execution_bridge import (
    AttestedTaskObservation,
    observe_and_route_with_attested_resources,
)
from resource_feedback_materialization import (
    ResourceEvidenceMaterializationResult,
    materialize_resource_feedback_snapshot,
    verify_resource_evidence_materialization,
)
from resource_feedback_summary import ResourceFeedbackHistorySnapshot
from resource_profile_evidence import ResourceEvidence, ResourceProfileAttestation
from resource_router import ExecutionBackend


def _hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True)
class RouteDrift:
    backend_id: str
    reference_marginal_cost_usd: float
    calibrated_marginal_cost_usd: float
    marginal_cost_delta_usd: float
    reference_success_probability: float
    calibrated_success_probability: float
    success_probability_delta: float
    reference_latency_seconds: float
    calibrated_latency_seconds: float
    latency_delta_seconds: float
    reference_planning_state: str
    calibrated_planning_state: str


@dataclass(frozen=True)
class MaterializedRoutingReplay:
    platform: str
    external_id: str
    state: str
    reasons: tuple[str, ...]
    upstream_state: str
    history_tip_hash: Optional[str]
    materialization_hash: Optional[str]
    materialization_state: Optional[str]
    selected_backend_before: Optional[str]
    selected_backend_after: Optional[str]
    selected_backend_changed: bool
    selected_calibration_state: Optional[str]
    route_drifts: tuple[RouteDrift, ...]
    attested_observation: Optional[AttestedTaskObservation]
    replay_hash: str
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("replay_hash", None)
        return body


def _finalize(**kwargs: Any) -> MaterializedRoutingReplay:
    draft = MaterializedRoutingReplay(replay_hash="", **kwargs)
    return MaterializedRoutingReplay(replay_hash=_hash(draft.hash_body()), **kwargs)


def verify_materialized_routing_replay(result: MaterializedRoutingReplay) -> bool:
    return result.replay_hash == _hash(result.hash_body())


def _reference_maps(
    reference_backends: Mapping[str, ExecutionBackend] | Iterable[ExecutionBackend],
) -> tuple[dict[str, ExecutionBackend], dict[str, dict[str, Any]]]:
    if isinstance(reference_backends, Mapping):
        objects = dict(reference_backends)
    else:
        objects = {}
        for backend in reference_backends:
            if backend.backend_id in objects:
                raise ValueError("duplicate_reference_backend_id")
            objects[backend.backend_id] = backend
    for backend_id, backend in objects.items():
        if backend.backend_id != backend_id:
            raise ValueError("reference_backend_mapping_identity_mismatch")
    return objects, {backend_id: asdict(backend) for backend_id, backend in objects.items()}


def _attestations_from_materialization(
    materialization: ResourceEvidenceMaterializationResult,
) -> tuple[ResourceProfileAttestation, ...]:
    attestations: list[ResourceProfileAttestation] = []
    for profile in materialization.backend_profiles:
        if (
            profile.state != "materialized_reproducible"
            or profile.attestation_state != "calibrated_reproducible"
            or not profile.all_current_evidence_reproducible
            or profile.contains_user_declaration
            or not profile.quantitative_values_complete
        ):
            continue
        attestations.append(
            ResourceProfileAttestation(
                backend_id=profile.backend_id,
                reference_backend_hash=profile.reference_backend_hash,
                state="calibrated_reproducible",
                reasons=(),
                parameter_calibrations=(),
                calibrated_values=dict(profile.calibrated_values),
                evidence_bundle_hash=profile.anchor_evidence_bundle_hash,
                contains_user_declaration=False,
                all_current_evidence_reproducible=True,
            )
        )
    return tuple(attestations)


def _drifts(observation: AttestedTaskObservation) -> tuple[RouteDrift, ...]:
    routing = observation.attested_routing
    if routing is None:
        return ()
    out: list[RouteDrift] = []
    for entry in routing.entries:
        calibrated = entry.calibrated_quote
        if calibrated is None:
            continue
        reference = entry.reference_quote
        out.append(
            RouteDrift(
                backend_id=entry.backend_id,
                reference_marginal_cost_usd=reference.marginal_cost_usd,
                calibrated_marginal_cost_usd=calibrated.marginal_cost_usd,
                marginal_cost_delta_usd=round(
                    calibrated.marginal_cost_usd - reference.marginal_cost_usd, 6
                ),
                reference_success_probability=reference.success_probability,
                calibrated_success_probability=calibrated.success_probability,
                success_probability_delta=round(
                    calibrated.success_probability - reference.success_probability, 6
                ),
                reference_latency_seconds=reference.latency_seconds,
                calibrated_latency_seconds=calibrated.latency_seconds,
                latency_delta_seconds=round(
                    calibrated.latency_seconds - reference.latency_seconds, 6
                ),
                reference_planning_state=reference.planning_state,
                calibrated_planning_state=calibrated.planning_state,
            )
        )
    return tuple(sorted(out, key=lambda item: item.backend_id))


def observe_and_route_with_materialized_resources(
    platform: str,
    payload: Mapping[str, Any],
    *,
    history_snapshot: ResourceFeedbackHistorySnapshot,
    reference_backends: Mapping[str, ExecutionBackend] | Iterable[ExecutionBackend],
    evidence_bundles: Mapping[str, Iterable[ResourceEvidence]],
    now: datetime,
    demand_evidence_class: str = "unknown",
    observed_at: str | None = None,
    capabilities: CapabilityProfile | None = None,
    cost: CostProfile | None = None,
) -> MaterializedRoutingReplay:
    """Replay routing against an exact fresh I066 resource materialization.

    The task observation gate is evaluated before resource materialization. Thus
    resource-side measurements cannot rescue policy-insufficient or demand-unproven
    work. Only reproducible I066 profiles are converted into I051 attestations.
    """
    upstream = observe_task(
        platform,
        dict(payload),
        demand_evidence_class=demand_evidence_class,
        observed_at=observed_at,
        capabilities=capabilities,
        cost=cost,
    )
    if upstream.state != "accept_dry_run":
        return _finalize(
            platform=upstream.platform,
            external_id=upstream.external_id,
            state=upstream.state,
            reasons=upstream.reasons,
            upstream_state=upstream.state,
            history_tip_hash=None,
            materialization_hash=None,
            materialization_state=None,
            selected_backend_before=None,
            selected_backend_after=None,
            selected_backend_changed=False,
            selected_calibration_state=None,
            route_drifts=(),
            attested_observation=None,
        )

    backend_objects, backend_payloads = _reference_maps(reference_backends)
    materialization = materialize_resource_feedback_snapshot(
        history_snapshot,
        reference_backends=backend_payloads,
        evidence_bundles=evidence_bundles,
        now=now,
    )
    materialization_reasons = list(materialization.reasons)
    if not verify_resource_evidence_materialization(materialization):
        materialization_reasons.append("materialization_hash_invalid")

    if (
        materialization.state != "materialized_reproducible"
        or materialization_reasons
        or not materialization.quantitative_values_complete
    ):
        reasons = tuple(
            dict.fromkeys(
                [
                    *upstream.reasons,
                    "verified_current_resource_snapshot_unavailable",
                    *materialization_reasons,
                ]
            )
        )
        return _finalize(
            platform=upstream.platform,
            external_id=upstream.external_id,
            state="hold",
            reasons=reasons,
            upstream_state=upstream.state,
            history_tip_hash=history_snapshot.history_tip_hash,
            materialization_hash=materialization.materialization_hash,
            materialization_state=materialization.state,
            selected_backend_before=history_snapshot.current_selected_backend_id,
            selected_backend_after=None,
            selected_backend_changed=False,
            selected_calibration_state=None,
            route_drifts=(),
            attested_observation=None,
        )

    attestations = _attestations_from_materialization(materialization)
    materialized_ids = {profile.backend_id for profile in materialization.backend_profiles}
    attested_ids = {attestation.backend_id for attestation in attestations}
    if materialized_ids != attested_ids:
        return _finalize(
            platform=upstream.platform,
            external_id=upstream.external_id,
            state="hold",
            reasons=tuple(
                dict.fromkeys(
                    [
                        *upstream.reasons,
                        "materialized_resource_not_fully_reproducible",
                    ]
                )
            ),
            upstream_state=upstream.state,
            history_tip_hash=history_snapshot.history_tip_hash,
            materialization_hash=materialization.materialization_hash,
            materialization_state=materialization.state,
            selected_backend_before=history_snapshot.current_selected_backend_id,
            selected_backend_after=None,
            selected_backend_changed=False,
            selected_calibration_state=None,
            route_drifts=(),
            attested_observation=None,
        )

    attested = observe_and_route_with_attested_resources(
        platform,
        payload,
        demand_evidence_class=demand_evidence_class,
        observed_at=observed_at,
        capabilities=capabilities,
        cost=cost,
        reference_backends=tuple(backend_objects.values()),
        attestations=attestations,
    )
    selected_after = attested.selected_backend_id
    selected_before = history_snapshot.current_selected_backend_id
    reasons = list(attested.reasons)
    state = attested.state
    if state != "route_dry_run":
        reasons.append("materialized_attested_route_unavailable")
        state = "hold"

    return _finalize(
        platform=attested.platform,
        external_id=attested.external_id,
        state=state,
        reasons=tuple(dict.fromkeys(reasons)),
        upstream_state=attested.upstream_state,
        history_tip_hash=history_snapshot.history_tip_hash,
        materialization_hash=materialization.materialization_hash,
        materialization_state=materialization.state,
        selected_backend_before=selected_before,
        selected_backend_after=selected_after,
        selected_backend_changed=(
            selected_after is not None
            and selected_before is not None
            and selected_after != selected_before
        ),
        selected_calibration_state=attested.selected_calibration_state,
        route_drifts=_drifts(attested),
        attested_observation=attested,
    )


def materialized_routing_record(result: MaterializedRoutingReplay) -> dict[str, Any]:
    record = asdict(result)
    record["dry_run_only"] = True
    record["execution_enabled"] = False
    record["network_enabled"] = False
    record["credentials_enabled"] = False
    record["submission_enabled"] = False
    record["value_movement_enabled"] = False
    return record
