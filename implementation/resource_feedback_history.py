"""I064 append-only audit/history chain for feedback-refreshed attested observations.

Successful I063 updates can enter the history only when their exact feedback
receipt/evidence records are supplied again and remain current at append time.
The chain binds before/after routing hashes, target evidence-bundle hashes and
parameter-level evidence timestamps. It never enables execution, network access,
credentials, submission or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Optional

from feedback_attested_observation import FeedbackAttestedTaskUpdate
from receipt_replay_calibration import CalibrationFeedback


def _hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


@dataclass(frozen=True)
class ResourceFeedbackHistoryEntry:
    sequence: int
    task_id: str
    platform: str
    external_id: str
    target_backend_id: str
    previous_entry_hash: str
    original_observation_hash: str
    before_routing_hash: str
    after_routing_hash: str
    before_target_evidence_bundle_hash: str
    after_target_evidence_bundle_hash: str
    feedback_receipt_hash: str
    feedback_evidence_hashes: tuple[str, ...]
    feedback_parameter_times: tuple[tuple[str, str], ...]
    replaced_parameters: tuple[str, ...]
    before_selected_backend_id: Optional[str]
    after_selected_backend_id: Optional[str]
    update_provenance_binding_hash: str
    appended_at: str
    entry_hash: str
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("entry_hash", None)
        return body


@dataclass(frozen=True)
class ResourceFeedbackHistoryResult:
    state: str
    reasons: tuple[str, ...]
    entry: Optional[ResourceFeedbackHistoryEntry]
    history_length: int
    history_tip_hash: str
    dry_run_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False


def _feedback_facts(feedback: CalibrationFeedback, *, now: datetime):
    reasons: list[str] = []
    if now.tzinfo is None or now.utcoffset() != timezone.utc.utcoffset(now):
        reasons.append("append_time_must_be_utc")
    if feedback.execution_authorized or not feedback.dry_run_only or feedback.network_enabled or feedback.value_movement_enabled:
        reasons.append("feedback_not_inert")
    hashes: list[str] = []
    parameter_times: list[tuple[str, str]] = []
    seen_parameters: set[str] = set()
    for evidence in feedback.evidence_records:
        computed = evidence.computed_hash()
        if evidence.evidence_hash is not None and evidence.evidence_hash != computed:
            reasons.append("feedback_evidence_hash_mismatch")
        hashes.append(evidence.evidence_hash or computed)
        if evidence.backend_id != feedback.backend_id:
            reasons.append("feedback_evidence_backend_mismatch")
        if evidence.parameter in seen_parameters:
            reasons.append(f"duplicate_feedback_parameter:{evidence.parameter}")
        seen_parameters.add(evidence.parameter)
        try:
            observed = _parse_utc(evidence.observed_at)
            if observed > now:
                reasons.append("feedback_evidence_future_dated")
            elif (now - observed).total_seconds() > evidence.max_age_seconds:
                reasons.append("feedback_evidence_stale")
        except Exception:
            reasons.append("feedback_evidence_timestamp_invalid")
        parameter_times.append((evidence.parameter, evidence.observed_at))
    return tuple(hashes), tuple(sorted(parameter_times)), tuple(dict.fromkeys(reasons))


def _expected_entry_hash(entry: ResourceFeedbackHistoryEntry) -> str:
    return _hash(entry.hash_body())


def verify_resource_feedback_history(entries: Iterable[ResourceFeedbackHistoryEntry]) -> tuple[bool, tuple[str, ...]]:
    rows = tuple(entries)
    reasons: list[str] = []
    previous_hash = "GENESIS"
    previous_after_routing = None
    task_key = None
    seen_receipts: set[str] = set()
    seen_evidence_hashes: set[str] = set()
    latest_parameter_time: dict[tuple[str, str], datetime] = {}

    for index, row in enumerate(rows, start=1):
        if row.sequence != index:
            reasons.append("history_sequence_gap")
        if row.previous_entry_hash != previous_hash:
            reasons.append("history_previous_hash_mismatch")
        if row.entry_hash != _expected_entry_hash(row):
            reasons.append("history_entry_hash_mismatch")
        if any((not row.dry_run_only, row.execution_enabled, row.network_enabled,
                row.credentials_enabled, row.submission_enabled, row.value_movement_enabled)):
            reasons.append("history_entry_not_inert")
        current_key = (row.platform, row.external_id, row.task_id)
        if task_key is None:
            task_key = current_key
        elif current_key != task_key:
            reasons.append("history_task_identity_changed")
        if previous_after_routing is not None and row.before_routing_hash != previous_after_routing:
            reasons.append("history_routing_chain_mismatch")
        if row.feedback_receipt_hash in seen_receipts:
            reasons.append("history_replayed_receipt")
        seen_receipts.add(row.feedback_receipt_hash)
        for evidence_hash in row.feedback_evidence_hashes:
            if evidence_hash in seen_evidence_hashes:
                reasons.append("history_replayed_evidence")
            seen_evidence_hashes.add(evidence_hash)
        for parameter, observed_at in row.feedback_parameter_times:
            try:
                observed = _parse_utc(observed_at)
            except Exception:
                reasons.append("history_parameter_timestamp_invalid")
                continue
            key = (row.target_backend_id, parameter)
            prior = latest_parameter_time.get(key)
            if prior is not None and observed <= prior:
                reasons.append(f"history_stale_parameter_regression:{row.target_backend_id}:{parameter}")
            if prior is None or observed > prior:
                latest_parameter_time[key] = observed
        previous_hash = row.entry_hash
        previous_after_routing = row.after_routing_hash
    return (not reasons, tuple(dict.fromkeys(reasons)))


def append_resource_feedback_history(
    history: Iterable[ResourceFeedbackHistoryEntry],
    update: FeedbackAttestedTaskUpdate,
    feedback: CalibrationFeedback,
    *,
    now: datetime,
) -> ResourceFeedbackHistoryResult:
    rows = tuple(history)
    reasons: list[str] = []
    history_ok, history_reasons = verify_resource_feedback_history(rows)
    if not history_ok:
        reasons.extend(history_reasons)

    if update.state not in {"feedback_refreshed_route_dry_run", "feedback_refreshed_hold"}:
        reasons.append("update_not_history_eligible")
    if update.task_id is None or update.original_routing_hash is None or update.refreshed_routing is None:
        reasons.append("update_missing_routing_state")
    if update.before_target_evidence_bundle_hash is None or update.after_target_evidence_bundle_hash is None:
        reasons.append("update_missing_evidence_bundle_binding")
    if update.provenance_binding_hash is None:
        reasons.append("update_missing_provenance_binding")
    if any((not update.dry_run_only, update.execution_enabled, update.network_enabled,
            update.credentials_enabled, update.submission_enabled, update.value_movement_enabled)):
        reasons.append("update_not_inert")
    if feedback.backend_id != update.target_backend_id:
        reasons.append("feedback_backend_update_mismatch")
    if feedback.receipt_hash != update.feedback_receipt_hash:
        reasons.append("feedback_receipt_update_mismatch")

    feedback_hashes, parameter_times, feedback_reasons = _feedback_facts(feedback, now=now)
    reasons.extend(feedback_reasons)
    if feedback_hashes != update.feedback_evidence_hashes:
        reasons.append("feedback_evidence_update_mismatch")
    feedback_parameters = tuple(sorted(parameter for parameter, _ in parameter_times))
    if tuple(sorted(update.replaced_parameters)) != feedback_parameters:
        reasons.append("feedback_parameter_update_mismatch")

    after_routing_hash = None if update.refreshed_routing is None else _hash(asdict(update.refreshed_routing))
    previous_hash = "GENESIS" if not rows else rows[-1].entry_hash
    if rows:
        tip = rows[-1]
        if (tip.platform, tip.external_id, tip.task_id) != (update.platform, update.external_id, update.task_id):
            reasons.append("history_append_task_identity_mismatch")
        if tip.after_routing_hash != update.original_routing_hash:
            reasons.append("history_append_out_of_order_routing")
        if feedback.receipt_hash in {row.feedback_receipt_hash for row in rows}:
            reasons.append("history_replayed_receipt")
        historical_evidence = {h for row in rows for h in row.feedback_evidence_hashes}
        if any(h in historical_evidence for h in feedback_hashes):
            reasons.append("history_replayed_evidence")
        latest: dict[tuple[str, str], datetime] = {}
        for row in rows:
            for parameter, observed_at in row.feedback_parameter_times:
                key = (row.target_backend_id, parameter)
                observed = _parse_utc(observed_at)
                if key not in latest or observed > latest[key]:
                    latest[key] = observed
        for parameter, observed_at in parameter_times:
            prior = latest.get((update.target_backend_id, parameter))
            if prior is not None and _parse_utc(observed_at) <= prior:
                reasons.append(f"history_stale_parameter_regression:{update.target_backend_id}:{parameter}")

    if reasons or after_routing_hash is None:
        return ResourceFeedbackHistoryResult(
            "hold", tuple(dict.fromkeys(reasons)), None, len(rows),
            "GENESIS" if not rows else rows[-1].entry_hash
        )

    entry_kwargs = dict(
        sequence=len(rows) + 1,
        task_id=update.task_id,
        platform=update.platform,
        external_id=update.external_id,
        target_backend_id=update.target_backend_id,
        previous_entry_hash=previous_hash,
        original_observation_hash=update.original_observation_hash,
        before_routing_hash=update.original_routing_hash,
        after_routing_hash=after_routing_hash,
        before_target_evidence_bundle_hash=update.before_target_evidence_bundle_hash,
        after_target_evidence_bundle_hash=update.after_target_evidence_bundle_hash,
        feedback_receipt_hash=feedback.receipt_hash,
        feedback_evidence_hashes=feedback_hashes,
        feedback_parameter_times=parameter_times,
        replaced_parameters=tuple(sorted(update.replaced_parameters)),
        before_selected_backend_id=update.before_selected_backend_id,
        after_selected_backend_id=update.after_selected_backend_id,
        update_provenance_binding_hash=update.provenance_binding_hash,
        appended_at=now.isoformat().replace("+00:00", "Z"),
        entry_hash="",
    )
    provisional = ResourceFeedbackHistoryEntry(**entry_kwargs)
    entry = ResourceFeedbackHistoryEntry(**{**entry_kwargs, "entry_hash": _expected_entry_hash(provisional)})
    return ResourceFeedbackHistoryResult("history_appended", (), entry, len(rows) + 1, entry.entry_hash)
