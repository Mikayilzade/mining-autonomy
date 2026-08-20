"""Deterministic longitudinal verifier for same-plan capture attestations.

This module is offline-only. It validates a chronological series of I034
attestations through the I035 replay/delta verifier, requires exact plan and
envelope identity, and summarizes evidence-state evolution without inferring
buyer demand from missing observations.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

from capture_attestation_delta import _validate_attestation, compare_capture_session_attestations

SERIES_MODE = "capture_session_attestation_history"


def _canonical_hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _parse_observed_at(value: Any) -> tuple[datetime, str]:
    if not isinstance(value, str) or not value:
        raise ValueError("capture_history_observed_at_invalid")
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError("capture_history_observed_at_invalid") from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("capture_history_observed_at_not_utc")
    dt = dt.astimezone(timezone.utc)
    canonical = dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    if value != canonical:
        raise ValueError("capture_history_observed_at_not_canonical")
    return dt, canonical


def _validate_supplied_delta(supplied: Mapping[str, Any], expected: Mapping[str, Any], index: int) -> None:
    if not isinstance(supplied, Mapping):
        raise ValueError(f"capture_history_delta_{index}_invalid")
    if supplied != expected:
        raise ValueError(f"capture_history_delta_{index}_mismatch")


def build_attestation_history(
    observations: Sequence[Mapping[str, Any]],
    supplied_deltas: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate and summarize a strictly chronological same-plan attestation series.

    ``observations`` entries must contain ``observed_at`` (canonical UTC seconds,
    e.g. ``2026-08-20T06:00:00Z``) and an I034 ``attestation``. If I035 deltas are
    supplied, every adjacent delta must exactly equal a freshly replayed delta.
    """
    if not isinstance(observations, Sequence) or isinstance(observations, (str, bytes)):
        raise ValueError("capture_history_observations_invalid")
    if len(observations) < 2:
        raise ValueError("capture_history_requires_multiple_observations")
    if supplied_deltas is not None:
        if not isinstance(supplied_deltas, Sequence) or isinstance(supplied_deltas, (str, bytes)):
            raise ValueError("capture_history_deltas_invalid")
        if len(supplied_deltas) != len(observations) - 1:
            raise ValueError("capture_history_delta_count_mismatch")

    validated: list[dict[str, Any]] = []
    times: list[datetime] = []
    canonical_times: list[str] = []
    seen_attestations: set[str] = set()

    for index, item in enumerate(observations):
        if not isinstance(item, Mapping):
            raise ValueError(f"capture_history_observation_{index}_invalid")
        dt, canonical = _parse_observed_at(item.get("observed_at"))
        if times and dt <= times[-1]:
            raise ValueError("capture_history_non_monotonic_observation_time")
        attestation = item.get("attestation")
        replay = _validate_attestation(attestation, f"history_{index}")
        if replay["attestation_hash"] in seen_attestations:
            raise ValueError("capture_history_duplicate_attestation_identity")
        seen_attestations.add(replay["attestation_hash"])
        if validated:
            first = validated[0]
            if replay["plan_hash"] != first["plan_hash"]:
                raise ValueError("capture_history_cross_plan_series")
            if replay["envelope_hash"] != first["envelope_hash"]:
                raise ValueError("capture_history_cross_envelope_series")
            if replay["bindings"] != first["bindings"]:
                raise ValueError("capture_history_binding_order_mismatch")
            for binding in first["bindings"]:
                before = first["rows"][binding]
                after = replay["rows"][binding]
                for field in ("sequence", "platform", "source_url", "expected_evidence_classes"):
                    if before[field] != after[field]:
                        raise ValueError(f"capture_history_request_identity_{field}_mismatch")
        validated.append(replay)
        times.append(dt)
        canonical_times.append(canonical)

    transitions: Counter[str] = Counter()
    adjacent_deltas: list[dict[str, Any]] = []
    delta_refs: list[dict[str, Any]] = []
    coverage_timeline: list[dict[str, Any]] = []

    for index, replay in enumerate(validated):
        coverage = replay["coverage"]
        coverage_timeline.append({
            "observed_at": canonical_times[index],
            "attestation_sha256": replay["attestation_hash"],
            "coverage_complete": coverage["coverage_complete"],
            "captured_count": coverage["captured_count"],
            "missing_count": coverage["missing_count"],
            "rejected_planned_count": coverage["rejected_planned_count"],
            "production_gap_count": coverage["production_gap_count"],
        })
        if index == 0:
            continue
        expected_delta = compare_capture_session_attestations(
            observations[index - 1]["attestation"], observations[index]["attestation"]
        )
        if supplied_deltas is not None:
            _validate_supplied_delta(supplied_deltas[index - 1], expected_delta, index - 1)
        adjacent_deltas.append(expected_delta)
        delta_refs.append({
            "from_observed_at": canonical_times[index - 1],
            "to_observed_at": canonical_times[index],
            "delta_sha256": expected_delta["delta_sha256"],
            "baseline_attestation_sha256": expected_delta["baseline_attestation_sha256"],
            "target_attestation_sha256": expected_delta["target_attestation_sha256"],
        })
        for change in expected_delta["request_state_changes"]:
            transitions[f"{change['from_state']}->{change['to_state']}"] += 1

    first_coverage = validated[0]["coverage"]
    last_coverage = validated[-1]["coverage"]
    core = {
        "schema_version": 1,
        "mode": SERIES_MODE,
        "session_plan_sha256": validated[0]["plan_hash"],
        "transport_envelope_set_sha256": validated[0]["envelope_hash"],
        "planned_request_binding_sha256s": list(validated[0]["bindings"]),
        "observation_count": len(validated),
        "first_observed_at": canonical_times[0],
        "last_observed_at": canonical_times[-1],
        "attestation_sha256s": [item["attestation_hash"] for item in validated],
        "adjacent_delta_refs": delta_refs,
        "coverage_timeline": coverage_timeline,
        "transition_frequencies": dict(sorted(transitions.items())),
        "coverage_evolution": {
            "captured_count_change": last_coverage["captured_count"] - first_coverage["captured_count"],
            "missing_count_change": last_coverage["missing_count"] - first_coverage["missing_count"],
            "rejected_planned_count_change": last_coverage["rejected_planned_count"] - first_coverage["rejected_planned_count"],
            "production_gap_count_change": last_coverage["production_gap_count"] - first_coverage["production_gap_count"],
            "coverage_complete_observation_count": sum(1 for item in validated if item["coverage"]["coverage_complete"]),
        },
        "demand_interpretation": "none_missing_or_failed_capture_is_not_negative_demand_evidence",
        "aggregation_scope": "evidence_integrity_and_coverage_only_no_demand_extrapolation",
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "history_sha256": _canonical_hash(core)}
