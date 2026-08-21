"""I062 merge verified benchmark feedback into an existing resource evidence bundle."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Any

from resource_profile_evidence import ResourceEvidence, ResourceProfileAttestation, attest_resource_profile
from receipt_replay_calibration import CalibrationFeedback
from resource_router import ExecutionBackend, TaskEconomics
from resource_routing_attestation import AttestedRoutingDecision, route_task_with_attested_resources

@dataclass(frozen=True)
class FeedbackMergeResult:
    state: str
    reasons: tuple[str, ...]
    backend_id: str
    merged_evidence: tuple[ResourceEvidence, ...]
    attestation: ResourceProfileAttestation | None
    routing: AttestedRoutingDecision | None
    replaced_parameters: tuple[str, ...]
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def merge_verified_feedback(
    reference_backend: ExecutionBackend,
    existing_evidence: Iterable[ResourceEvidence],
    feedback: CalibrationFeedback,
    task: TaskEconomics,
    *,
    now: datetime,
) -> FeedbackMergeResult:
    """Replace only parameters explicitly measured by verified I061 feedback.

    Existing unrelated evidence is preserved. Multiple feedback records for the same
    parameter or feedback not in a verified-ready state fails closed rather than
    silently choosing a value.
    """
    reasons: list[str] = []
    if feedback.state not in {"measured_feedback_ready", "verified_but_no_calibratable_facts"}:
        reasons.append("feedback_not_verified_ready")
    if feedback.backend_id != reference_backend.backend_id:
        reasons.append("feedback_backend_mismatch")
    if feedback.execution_authorized or not feedback.dry_run_only or feedback.network_enabled or feedback.value_movement_enabled:
        reasons.append("feedback_not_inert")

    feedback_by_parameter: dict[str, ResourceEvidence] = {}
    for record in feedback.evidence_records:
        if record.backend_id != reference_backend.backend_id:
            reasons.append("feedback_record_backend_mismatch")
        if record.parameter in feedback_by_parameter:
            reasons.append(f"duplicate_feedback_parameter:{record.parameter}")
        feedback_by_parameter[record.parameter] = record

    if reasons:
        return FeedbackMergeResult("hold", tuple(dict.fromkeys(reasons)), reference_backend.backend_id, (), None, None, ())

    replaced = set(feedback_by_parameter)
    merged = [x for x in existing_evidence if x.parameter not in replaced]
    merged.extend(feedback_by_parameter.values())
    attestation = attest_resource_profile(reference_backend.__dict__, merged, now=now)
    if attestation.state == "planning_only":
        return FeedbackMergeResult(
            "planning_only", attestation.reasons, reference_backend.backend_id,
            tuple(merged), attestation, None, tuple(sorted(replaced))
        )
    routing = route_task_with_attested_resources(task, [reference_backend], [attestation])
    state = "feedback_integrated_route_dry_run" if routing.state == "route_dry_run" else "feedback_integrated_hold"
    return FeedbackMergeResult(
        state, (), reference_backend.backend_id, tuple(merged), attestation, routing,
        tuple(sorted(replaced))
    )


def routing_delta(before: AttestedRoutingDecision, after: AttestedRoutingDecision) -> dict[str, Any]:
    def q(d: AttestedRoutingDecision):
        return d.selected_quote
    b, a = q(before), q(after)
    return {
        "before_state": before.state,
        "after_state": after.state,
        "before_backend": before.selected_backend_id,
        "after_backend": after.selected_backend_id,
        "before_latency_seconds": None if b is None else b.latency_seconds,
        "after_latency_seconds": None if a is None else a.latency_seconds,
        "before_marginal_cost_usd": None if b is None else b.marginal_cost_usd,
        "after_marginal_cost_usd": None if a is None else a.marginal_cost_usd,
        "dry_run_only": True,
        "execution_enabled": False,
        "network_enabled": False,
        "value_movement_enabled": False,
    }
