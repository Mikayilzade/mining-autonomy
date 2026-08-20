"""Deterministic longitudinal evidence-quality/regression gate over I036 history.

Offline-only. This module evaluates capture/infrastructure evidence integrity,
never economic demand. A recommendation to repeat a future read-only capture
is inert and still requires separate explicit authorization.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

EXPECTED_HISTORY_MODE = "capture_session_attestation_history"
QUALITY_MODE = "longitudinal_capture_integrity_gate"


def _canonical_hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _parse_canonical_utc(value: Any, code: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(code)
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(code) from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError(f"{code}_not_utc")
    dt = dt.astimezone(timezone.utc)
    canonical = dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    if value != canonical:
        raise ValueError(f"{code}_not_canonical")
    return dt


def _nonnegative_int(value: Any, code: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(code)
    return value


def _validate_history(history: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(history, Mapping):
        raise ValueError("quality_history_invalid")
    if history.get("schema_version") != 1 or history.get("mode") != EXPECTED_HISTORY_MODE:
        raise ValueError("quality_history_schema_or_mode_invalid")
    supplied_hash = history.get("history_sha256")
    if not isinstance(supplied_hash, str) or len(supplied_hash) != 64:
        raise ValueError("quality_history_hash_invalid")
    core = dict(history)
    core.pop("history_sha256", None)
    if _canonical_hash(core) != supplied_hash:
        raise ValueError("quality_history_hash_mismatch")

    count = _nonnegative_int(history.get("observation_count"), "quality_observation_count_invalid")
    timeline = history.get("coverage_timeline")
    if not isinstance(timeline, list) or len(timeline) != count or count < 2:
        raise ValueError("quality_coverage_timeline_invalid")

    times: list[datetime] = []
    normalized: list[dict[str, Any]] = []
    for index, row in enumerate(timeline):
        if not isinstance(row, Mapping):
            raise ValueError(f"quality_timeline_{index}_invalid")
        dt = _parse_canonical_utc(row.get("observed_at"), f"quality_timeline_{index}_observed_at_invalid")
        if times and dt <= times[-1]:
            raise ValueError("quality_timeline_non_monotonic")
        times.append(dt)
        normalized.append({
            "observed_at": row["observed_at"],
            "coverage_complete": row.get("coverage_complete") is True,
            "captured_count": _nonnegative_int(row.get("captured_count"), f"quality_timeline_{index}_captured_invalid"),
            "missing_count": _nonnegative_int(row.get("missing_count"), f"quality_timeline_{index}_missing_invalid"),
            "rejected_planned_count": _nonnegative_int(row.get("rejected_planned_count"), f"quality_timeline_{index}_rejected_invalid"),
            "production_gap_count": _nonnegative_int(row.get("production_gap_count"), f"quality_timeline_{index}_gap_invalid"),
        })

    if history.get("first_observed_at") != normalized[0]["observed_at"]:
        raise ValueError("quality_first_observed_at_mismatch")
    if history.get("last_observed_at") != normalized[-1]["observed_at"]:
        raise ValueError("quality_last_observed_at_mismatch")

    evolution = history.get("coverage_evolution")
    if not isinstance(evolution, Mapping):
        raise ValueError("quality_coverage_evolution_invalid")
    expected_evolution = {
        "captured_count_change": normalized[-1]["captured_count"] - normalized[0]["captured_count"],
        "missing_count_change": normalized[-1]["missing_count"] - normalized[0]["missing_count"],
        "rejected_planned_count_change": normalized[-1]["rejected_planned_count"] - normalized[0]["rejected_planned_count"],
        "production_gap_count_change": normalized[-1]["production_gap_count"] - normalized[0]["production_gap_count"],
        "coverage_complete_observation_count": sum(1 for row in normalized if row["coverage_complete"]),
    }
    if dict(evolution) != expected_evolution:
        raise ValueError("quality_coverage_evolution_mismatch")

    transitions = history.get("transition_frequencies")
    if not isinstance(transitions, Mapping):
        raise ValueError("quality_transition_frequencies_invalid")
    normalized_transitions: dict[str, int] = {}
    for key, value in transitions.items():
        if not isinstance(key, str) or "->" not in key:
            raise ValueError("quality_transition_key_invalid")
        normalized_transitions[key] = _nonnegative_int(value, "quality_transition_count_invalid")

    return {
        "timeline": normalized,
        "times": times,
        "evolution": expected_evolution,
        "transitions": normalized_transitions,
        "history_sha256": supplied_hash,
    }


def evaluate_longitudinal_capture_integrity(
    history: Mapping[str, Any],
    *,
    minimum_observations: int = 3,
    minimum_span_seconds: int = 3600,
) -> dict[str, Any]:
    """Evaluate capture-integrity trend without making economic-demand claims."""
    if not isinstance(minimum_observations, int) or isinstance(minimum_observations, bool) or minimum_observations < 2:
        raise ValueError("quality_minimum_observations_invalid")
    if not isinstance(minimum_span_seconds, int) or isinstance(minimum_span_seconds, bool) or minimum_span_seconds < 1:
        raise ValueError("quality_minimum_span_invalid")

    replay = _validate_history(history)
    timeline = replay["timeline"]
    span_seconds = int((replay["times"][-1] - replay["times"][0]).total_seconds())
    sample_sufficient = len(timeline) >= minimum_observations
    span_sufficient = span_seconds >= minimum_span_seconds
    trend_eligible = sample_sufficient and span_sufficient

    evolution = replay["evolution"]
    transitions = replay["transitions"]
    harmful_transitions = sum(
        value for key, value in transitions.items()
        if key.startswith("captured->") and not key.endswith("->captured")
    )
    beneficial_transitions = sum(
        value for key, value in transitions.items()
        if key.endswith("->captured") and not key.startswith("captured->")
    )

    regression_points = (
        max(0, evolution["missing_count_change"])
        + max(0, evolution["rejected_planned_count_change"])
        + max(0, evolution["production_gap_count_change"])
        + harmful_transitions
    )
    improvement_points = (
        max(0, -evolution["missing_count_change"])
        + max(0, -evolution["rejected_planned_count_change"])
        + max(0, -evolution["production_gap_count_change"])
        + beneficial_transitions
    )

    if not trend_eligible:
        label = "insufficient_history"
    elif regression_points > improvement_points:
        label = "regressing"
    elif improvement_points > regression_points:
        label = "improving"
    else:
        label = "stable"

    last = timeline[-1]
    unresolved_capture_gap = (
        last["missing_count"] > 0
        or last["rejected_planned_count"] > 0
        or last["production_gap_count"] > 0
        or not last["coverage_complete"]
    )

    if not trend_eligible:
        repeat_recommendation = "repeat_may_add_integrity_evidence_after_explicit_authorization"
        repeat_reason = "minimum_history_not_met"
        worth_repeating = True
    elif label == "regressing":
        repeat_recommendation = "repeat_may_diagnose_capture_regression_after_explicit_authorization"
        repeat_reason = "capture_integrity_regressing"
        worth_repeating = True
    elif unresolved_capture_gap:
        repeat_recommendation = "repeat_may_close_unresolved_capture_gap_after_explicit_authorization"
        repeat_reason = "latest_capture_incomplete"
        worth_repeating = True
    else:
        repeat_recommendation = "no_repeat_needed_for_capture_integrity_only"
        repeat_reason = "history_sufficient_and_latest_capture_complete"
        worth_repeating = False

    core = {
        "schema_version": 1,
        "mode": QUALITY_MODE,
        "history_sha256": replay["history_sha256"],
        "observation_count": len(timeline),
        "observation_span_seconds": span_seconds,
        "minimum_observations": minimum_observations,
        "minimum_span_seconds": minimum_span_seconds,
        "sample_sufficient": sample_sufficient,
        "span_sufficient": span_sufficient,
        "trend_eligible": trend_eligible,
        "capture_integrity_label": label,
        "capture_regression_points": regression_points,
        "capture_improvement_points": improvement_points,
        "harmful_transition_count": harmful_transitions,
        "beneficial_transition_count": beneficial_transitions,
        "latest_coverage_complete": last["coverage_complete"],
        "latest_missing_count": last["missing_count"],
        "latest_rejected_planned_count": last["rejected_planned_count"],
        "latest_production_gap_count": last["production_gap_count"],
        "unresolved_capture_gap": unresolved_capture_gap,
        "economic_evidence_classification": "not_evaluated_capture_integrity_is_not_demand",
        "missing_capture_interpretation": "unknown_not_negative_demand",
        "future_read_only_capture_worth_repeating_for_integrity": worth_repeating,
        "future_read_only_capture_recommendation": repeat_recommendation,
        "recommendation_reason": repeat_reason,
        "authorization_required": True,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "quality_gate_sha256": _canonical_hash(core)}
