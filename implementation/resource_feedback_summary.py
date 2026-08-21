"""I065 verified-history summarizer for resource calibration feedback.

Derives only facts already present in a verified I064 chain. It never averages,
infers, or fabricates parameter values, reliability, quality, demand, permission,
or authorization. History stores provenance references, not the calibrated values
behind those references, so this snapshot intentionally remains value-free.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Optional

from resource_feedback_history import ResourceFeedbackHistoryEntry, verify_resource_feedback_history


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


@dataclass(frozen=True)
class LatestParameterEvidenceRef:
    backend_id: str
    parameter: str
    observed_at: str
    evidence_hashes: tuple[str, ...]
    evidence_binding_precision: str
    sequence: int
    entry_hash: str
    feedback_receipt_hash: str
    evidence_bundle_hash: str


@dataclass(frozen=True)
class BackendEvidenceState:
    backend_id: str
    latest_parameters: tuple[LatestParameterEvidenceRef, ...]
    update_count: int
    last_update_sequence: int
    latest_observed_at: Optional[str]
    parameter_values_stored_in_history: bool = False


@dataclass(frozen=True)
class RoutingTransition:
    sequence: int
    from_backend_id: Optional[str]
    to_backend_id: Optional[str]
    changed: bool
    before_routing_hash: str
    after_routing_hash: str
    entry_hash: str


@dataclass(frozen=True)
class ResourceFeedbackHistorySnapshot:
    state: str
    reasons: tuple[str, ...]
    history_length: int
    history_tip_hash: str
    task_id: Optional[str]
    platform: Optional[str]
    external_id: Optional[str]
    current_selected_backend_id: Optional[str]
    latest_routing_hash: Optional[str]
    backend_states: tuple[BackendEvidenceState, ...]
    routing_transitions: tuple[RoutingTransition, ...]
    selected_backend_switch_count: int
    selected_backend_oscillation_detected: bool
    parameter_churn_indicators: tuple[str, ...]
    anomaly_indicators: tuple[str, ...]
    limitations: tuple[str, ...]
    snapshot_hash: str
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("snapshot_hash", None)
        return body


def _finalize(**kwargs: Any) -> ResourceFeedbackHistorySnapshot:
    provisional = ResourceFeedbackHistorySnapshot(snapshot_hash="", **kwargs)
    return ResourceFeedbackHistorySnapshot(snapshot_hash=_hash(provisional.hash_body()), **kwargs)


def _oscillation(states: list[Optional[str]]) -> bool:
    compact: list[Optional[str]] = []
    for state in states:
        if not compact or compact[-1] != state:
            compact.append(state)
    return any(compact[index] == compact[index + 2] for index in range(len(compact) - 2))


def summarize_resource_feedback_history(
    entries: Iterable[ResourceFeedbackHistoryEntry],
    *,
    parameter_churn_threshold: int = 3,
) -> ResourceFeedbackHistorySnapshot:
    if parameter_churn_threshold < 2:
        raise ValueError("parameter_churn_threshold_must_be_at_least_2")
    rows = tuple(entries)
    valid, verify_reasons = verify_resource_feedback_history(rows)
    if not valid:
        anomalies = tuple(f"verified_history_failure:{reason}" for reason in verify_reasons)
        return _finalize(
            state="hold_invalid_history", reasons=verify_reasons, history_length=len(rows),
            history_tip_hash="GENESIS" if not rows else rows[-1].entry_hash,
            task_id=None, platform=None, external_id=None, current_selected_backend_id=None,
            latest_routing_hash=None, backend_states=(), routing_transitions=(),
            selected_backend_switch_count=0, selected_backend_oscillation_detected=False,
            parameter_churn_indicators=(), anomaly_indicators=anomalies,
            limitations=("derived_state_withheld_until_history_verifies",),
        )
    if not rows:
        return _finalize(
            state="empty_verified_history", reasons=(), history_length=0, history_tip_hash="GENESIS",
            task_id=None, platform=None, external_id=None, current_selected_backend_id=None,
            latest_routing_hash=None, backend_states=(), routing_transitions=(),
            selected_backend_switch_count=0, selected_backend_oscillation_detected=False,
            parameter_churn_indicators=(), anomaly_indicators=(),
            limitations=("no_feedback_history_available", "parameter_values_not_stored_in_i064_history"),
        )

    latest_refs: dict[tuple[str, str], LatestParameterEvidenceRef] = {}
    parameter_counts: dict[tuple[str, str], int] = {}
    backend_update_counts: dict[str, int] = {}
    backend_last_sequence: dict[str, int] = {}
    transitions: list[RoutingTransition] = []
    selected_states: list[Optional[str]] = [rows[0].before_selected_backend_id]
    switch_count = 0

    for row in rows:
        backend_update_counts[row.target_backend_id] = backend_update_counts.get(row.target_backend_id, 0) + 1
        backend_last_sequence[row.target_backend_id] = row.sequence
        single_exact_binding = len(row.feedback_parameter_times) == 1 and len(row.feedback_evidence_hashes) == 1
        for parameter, observed_at in row.feedback_parameter_times:
            key = (row.target_backend_id, parameter)
            parameter_counts[key] = parameter_counts.get(key, 0) + 1
            # I064 binds the evidence-hash tuple and parameter-time tuple to the entry,
            # but does not store an explicit parameter -> evidence-hash map for multi-parameter
            # updates. Preserve the whole evidence set rather than guessing by tuple order.
            evidence_hashes = row.feedback_evidence_hashes
            binding_precision = "exact_single_parameter" if single_exact_binding else "entry_set_only"
            latest_refs[key] = LatestParameterEvidenceRef(
                backend_id=row.target_backend_id, parameter=parameter, observed_at=observed_at,
                evidence_hashes=evidence_hashes, evidence_binding_precision=binding_precision,
                sequence=row.sequence, entry_hash=row.entry_hash,
                feedback_receipt_hash=row.feedback_receipt_hash,
                evidence_bundle_hash=row.after_target_evidence_bundle_hash,
            )
        changed = row.before_selected_backend_id != row.after_selected_backend_id
        if changed:
            switch_count += 1
        transitions.append(RoutingTransition(
            sequence=row.sequence, from_backend_id=row.before_selected_backend_id,
            to_backend_id=row.after_selected_backend_id, changed=changed,
            before_routing_hash=row.before_routing_hash, after_routing_hash=row.after_routing_hash,
            entry_hash=row.entry_hash,
        ))
        selected_states.append(row.after_selected_backend_id)

    states: list[BackendEvidenceState] = []
    for backend_id in sorted(backend_update_counts):
        refs = tuple(sorted((ref for (bid, _), ref in latest_refs.items() if bid == backend_id), key=lambda r: r.parameter))
        latest_observed = max((ref.observed_at for ref in refs), default=None)
        states.append(BackendEvidenceState(
            backend_id=backend_id, latest_parameters=refs,
            update_count=backend_update_counts[backend_id],
            last_update_sequence=backend_last_sequence[backend_id],
            latest_observed_at=latest_observed,
        ))

    churn = tuple(sorted(
        f"frequent_parameter_updates:{backend}:{parameter}:{count}"
        for (backend, parameter), count in parameter_counts.items()
        if count >= parameter_churn_threshold
    ))
    oscillation = _oscillation(selected_states)
    anomalies: list[str] = list(churn)
    if oscillation:
        anomalies.append("selected_backend_oscillation")

    return _finalize(
        state="verified_history_snapshot", reasons=(), history_length=len(rows),
        history_tip_hash=rows[-1].entry_hash, task_id=rows[-1].task_id,
        platform=rows[-1].platform, external_id=rows[-1].external_id,
        current_selected_backend_id=rows[-1].after_selected_backend_id,
        latest_routing_hash=rows[-1].after_routing_hash,
        backend_states=tuple(states), routing_transitions=tuple(transitions),
        selected_backend_switch_count=switch_count,
        selected_backend_oscillation_detected=oscillation,
        parameter_churn_indicators=churn, anomaly_indicators=tuple(anomalies),
        limitations=(
            "parameter_values_not_stored_in_i064_history",
            "snapshot_does_not_infer_reliability_quality_demand_or_authorization",
            "quantitative_repricing_requires_replay_of_bound_evidence_bundles",
            "multi_parameter_i064_entries_preserve_evidence_set_binding_only",
        ),
    )


def verify_resource_feedback_history_snapshot(snapshot: ResourceFeedbackHistorySnapshot) -> bool:
    return snapshot.snapshot_hash == _hash(snapshot.hash_body())
