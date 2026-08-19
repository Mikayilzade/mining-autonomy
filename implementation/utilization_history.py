"""Non-extrapolating comparison of saved paid-utilization snapshots.

Each snapshot is aggregated independently. Cross-window deltas are emitted only when
coverage durations match within tolerance; mismatched windows are never annualized,
per-day-normalized, or otherwise extrapolated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Iterable

from observation_importer import ImportedObservation
from receipt_aggregation import UtilizationSummary, aggregate_imported_utilization


@dataclass(frozen=True)
class UtilizationWindow:
    snapshot_sha256: str
    source_timestamp: str
    summary: UtilizationSummary
    coverage_seconds: float


@dataclass(frozen=True)
class UtilizationComparison:
    previous_snapshot_sha256: str
    current_snapshot_sha256: str
    comparable_window: bool
    previous_coverage_seconds: float
    current_coverage_seconds: float
    transaction_delta: int | None
    value_delta_usd: float | None
    reason: str


@dataclass(frozen=True)
class UtilizationHistory:
    platform: str
    evidence_class: str
    windows: tuple[UtilizationWindow, ...]
    comparisons: tuple[UtilizationComparison, ...]


def _iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _coverage(summary: UtilizationSummary) -> float:
    return max(0.0, (_iso(summary.last_observed_at) - _iso(summary.first_observed_at)).total_seconds())


def compare_utilization_snapshots(imported: Iterable[ImportedObservation], *,
                                  now: datetime | None = None,
                                  max_age_hours: float = 24.0,
                                  duration_tolerance_seconds: float = 1.0) -> UtilizationHistory:
    observations = list(imported)
    if len(observations) < 2:
        raise ValueError("at_least_two_utilization_snapshots_required")
    if duration_tolerance_seconds < 0:
        raise ValueError("duration_tolerance_must_be_nonnegative")

    seen: set[str] = set()
    windows: list[UtilizationWindow] = []
    platform: str | None = None
    evidence_class: str | None = None
    for observation in observations:
        digest = observation.snapshot.payload_sha256
        if digest in seen:
            raise ValueError("duplicate_utilization_snapshot")
        seen.add(digest)
        summary = aggregate_imported_utilization(observation, now=now, max_age_hours=max_age_hours)
        if platform is None:
            platform = summary.platform
            evidence_class = summary.evidence_class
        elif summary.platform != platform:
            raise ValueError("utilization_platform_mismatch")
        elif summary.evidence_class != evidence_class:
            raise ValueError("utilization_evidence_class_mismatch")
        windows.append(UtilizationWindow(digest, observation.snapshot.source_timestamp, summary, _coverage(summary)))

    windows.sort(key=lambda item: item.source_timestamp)
    comparisons: list[UtilizationComparison] = []
    for previous, current in zip(windows, windows[1:]):
        duration_match = abs(previous.coverage_seconds - current.coverage_seconds) <= duration_tolerance_seconds
        if duration_match:
            comparisons.append(UtilizationComparison(
                previous.snapshot_sha256, current.snapshot_sha256, True,
                previous.coverage_seconds, current.coverage_seconds,
                current.summary.transaction_count - previous.summary.transaction_count,
                round(current.summary.total_value_usd - previous.summary.total_value_usd, 6),
                "matched_coverage_duration",
            ))
        else:
            comparisons.append(UtilizationComparison(
                previous.snapshot_sha256, current.snapshot_sha256, False,
                previous.coverage_seconds, current.coverage_seconds,
                None, None, "mismatched_coverage_no_extrapolation",
            ))
    assert platform is not None and evidence_class is not None
    return UtilizationHistory(platform, evidence_class, tuple(windows), tuple(comparisons))


def utilization_history_record(history: UtilizationHistory) -> dict[str, Any]:
    return asdict(history)
