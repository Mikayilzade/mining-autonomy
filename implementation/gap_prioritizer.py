"""Deterministic production-gap prioritizer over the I026 evidence audit.

This module is plan-only. It performs no network calls, authentication, task
acceptance, publication, wallet activity, or settlement. Missing evidence is
prioritized as an unknown that deserves observation; it is never interpreted
as zero or negative demand.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from sampling_receipt import manifest_item_sha256, verify_sampling_manifest_envelope


DEFAULT_PLATFORM_PRIORITIES: dict[str, int] = {
    "payanagent": 5,
    "okx_ai_a2a": 4,
    "agent2agent.market": 4,
    "mcpize": 4,
    "agentgigs.io": 3,
}

GAP_EVIDENCE_VALUE: dict[str, int] = {
    "production_capture_missing": 220,
    "valid_capture_receipt_missing": 210,
    "production_receipt_missing": 200,
    "replay_evidence_future_invalid": 190,
    "replay_evidence_stale": 180,
    "production_capture_not_in_durable_archive": 150,
    "replay_receipt_provenance_missing": 140,
    "archived_capture_not_latest_production_replay": 120,
}

OFFLINE_GAPS = frozenset({
    "production_capture_not_in_durable_archive",
    "replay_receipt_provenance_missing",
    "archived_capture_not_latest_production_replay",
})

OBSERVATION_GAPS = frozenset({
    "production_capture_missing",
    "valid_capture_receipt_missing",
    "production_receipt_missing",
    "replay_evidence_stale",
    "replay_evidence_future_invalid",
})


@dataclass(frozen=True)
class PrioritizedObservation:
    rank_score: int
    platform: str
    platform_priority: int
    item_index: int
    source_url: str
    manifest_item_sha256: str
    unresolved_gaps: tuple[str, ...]
    evidence_value: int
    freshness_urgency: int
    rate_budget_score: int
    rate_limit: Mapping[str, Any]
    expected_evidence_classes: tuple[str, ...]
    declared_environment: str
    method: str
    next_step: str
    missing_evidence_interpretation: str = "unknown_not_negative_demand"
    credentials_allowed: bool = False
    network_calls_performed: bool = False
    action_enabled: bool = False


def _validate_audit(audit: Mapping[str, Any]) -> None:
    if audit.get("schema_version") != 1:
        raise ValueError("gap_priority_audit_schema_invalid")
    if audit.get("network_calls_performed") is not False:
        raise ValueError("gap_priority_audit_network_flag_invalid")
    if audit.get("action_enabled") is not False:
        raise ValueError("gap_priority_audit_action_flag_invalid")
    if audit.get("missing_capture_is_not_zero_demand") is not True:
        raise ValueError("gap_priority_missing_capture_semantics_invalid")
    if not isinstance(audit.get("sources"), list):
        raise ValueError("gap_priority_audit_sources_invalid")


def _manifest_item_index(manifest_envelope: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    verify_sampling_manifest_envelope(manifest_envelope)
    manifest = manifest_envelope["manifest"]
    items = manifest["items"]
    return {index: item for index, item in enumerate(items) if item.get("scheduled") is True}


def _validate_rate_limit(rate_limit: Mapping[str, Any]) -> tuple[float, int, float]:
    if not isinstance(rate_limit, Mapping):
        raise ValueError("gap_priority_rate_limit_missing")
    try:
        min_interval = float(rate_limit["min_interval_seconds"])
        max_requests = int(rate_limit["max_requests_per_window"])
        window = float(rate_limit["window_seconds"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("gap_priority_rate_limit_invalid") from exc
    if min_interval < 0 or max_requests <= 0 or window <= 0:
        raise ValueError("gap_priority_rate_limit_invalid")
    return min_interval, max_requests, window


def _rate_budget_score(rate_limit: Mapping[str, Any]) -> int:
    min_interval, max_requests, window = _validate_rate_limit(rate_limit)
    per_hour_window = max_requests * 3600.0 / window
    per_hour_interval = 3600.0 / max(min_interval, 1.0)
    conservative_hourly_ceiling = min(per_hour_window, per_hour_interval)
    return max(1, min(100, int(round(conservative_hourly_ceiling * 10.0))))


def _freshness_urgency(row: Mapping[str, Any], gaps: tuple[str, ...]) -> int:
    if "replay_evidence_future_invalid" in gaps:
        return 90
    if "replay_evidence_stale" in gaps:
        return 80
    if row.get("replay_freshness_state") is None:
        return 60
    if row.get("replay_freshness_state") == "fresh":
        return 0
    return 50


def _classify_next_step(gaps: tuple[str, ...]) -> str:
    gap_set = set(gaps)
    has_observation = bool(gap_set & OBSERVATION_GAPS)
    has_offline = bool(gap_set & OFFLINE_GAPS)
    if has_observation:
        return "read_only_observation"
    if has_offline:
        return "offline_integrity_repair"
    return "manual_review_unknown_gap"


def _evidence_value(gaps: tuple[str, ...]) -> int:
    if not gaps:
        return 0
    values = sorted((GAP_EVIDENCE_VALUE.get(gap, 100) for gap in gaps), reverse=True)
    # The largest gap dominates; secondary gaps add bounded value without making
    # a many-error source automatically outrank a materially higher-priority market.
    return values[0] + min(100, sum(values[1:]) // 4)


def prioritize_production_gaps(
    audit: Mapping[str, Any],
    manifest_envelope: Mapping[str, Any],
    *,
    platform_priorities: Mapping[str, int] = DEFAULT_PLATFORM_PRIORITIES,
    max_observations: int = 3,
) -> dict[str, Any]:
    """Rank unresolved production evidence without performing any capture.

    The observation queue contains only GET/no-credential manifest items whose
    unresolved state benefits from a fresh permitted read-only observation.
    Offline integrity/provenance repairs are emitted separately and consume no
    request budget.
    """
    _validate_audit(audit)
    if not isinstance(max_observations, int) or isinstance(max_observations, bool) or max_observations < 0:
        raise ValueError("gap_priority_max_observations_invalid")

    manifest_items = _manifest_item_index(manifest_envelope)
    audit_manifest_sha = audit.get("manifest_sha256")
    if audit_manifest_sha != manifest_envelope.get("manifest_sha256"):
        raise ValueError("gap_priority_manifest_hash_mismatch")

    candidates: list[PrioritizedObservation] = []
    for row in audit["sources"]:
        if not isinstance(row, Mapping):
            raise ValueError("gap_priority_source_row_invalid")
        gaps_value = row.get("unresolved_production_gaps")
        if not isinstance(gaps_value, list):
            raise ValueError("gap_priority_source_gaps_invalid")
        gaps = tuple(sorted({str(gap) for gap in gaps_value if gap}))
        if not gaps:
            continue

        item_index = row.get("item_index")
        if not isinstance(item_index, int) or isinstance(item_index, bool):
            raise ValueError("gap_priority_item_index_invalid")
        item = manifest_items.get(item_index)
        if item is None:
            raise ValueError("gap_priority_item_not_scheduled")

        if row.get("platform") != item.get("platform") or row.get("source_url") != item.get("source_url"):
            raise ValueError("gap_priority_manifest_source_mismatch")
        expected_item_sha = manifest_item_sha256(manifest_envelope, item_index)
        if row.get("manifest_item_sha256") != expected_item_sha:
            raise ValueError("gap_priority_manifest_item_hash_mismatch")
        if item.get("method") != "GET" or item.get("credentials_allowed") is not False:
            raise ValueError("gap_priority_read_only_contract_invalid")
        if item.get("action_enabled") is not False or item.get("network_calls_performed") is not False:
            raise ValueError("gap_priority_manifest_action_boundary_invalid")

        platform = str(item.get("platform"))
        priority = int(platform_priorities.get(platform, 1))
        if priority < 1 or priority > 5:
            raise ValueError("gap_priority_platform_priority_invalid")

        evidence_value = _evidence_value(gaps)
        freshness_urgency = _freshness_urgency(row, gaps)
        rate_score = _rate_budget_score(item.get("rate_limit", {}))
        next_step = _classify_next_step(gaps)
        rank_score = priority * 1000 + evidence_value * 3 + freshness_urgency * 2 + rate_score

        candidates.append(PrioritizedObservation(
            rank_score=rank_score,
            platform=platform,
            platform_priority=priority,
            item_index=item_index,
            source_url=str(item.get("source_url")),
            manifest_item_sha256=expected_item_sha,
            unresolved_gaps=gaps,
            evidence_value=evidence_value,
            freshness_urgency=freshness_urgency,
            rate_budget_score=rate_score,
            rate_limit=dict(item.get("rate_limit", {})),
            expected_evidence_classes=tuple(item.get("expected_evidence_classes", ())),
            declared_environment=str(item.get("environment", "unknown")),
            method="GET",
            next_step=next_step,
        ))

    ordered = sorted(
        candidates,
        key=lambda item: (-item.rank_score, item.platform, item.source_url, item.item_index),
    )
    observation_all = [item for item in ordered if item.next_step == "read_only_observation"]
    offline = [item for item in ordered if item.next_step == "offline_integrity_repair"]
    manual = [item for item in ordered if item.next_step == "manual_review_unknown_gap"]
    selected = observation_all[:max_observations]

    return {
        "schema_version": 1,
        "mode": "deterministic_plan_only_production_gap_priority",
        "manifest_sha256": manifest_envelope["manifest_sha256"],
        "unresolved_source_count": len(ordered),
        "read_only_observation_candidate_count": len(observation_all),
        "selected_read_only_observation_count": len(selected),
        "offline_repair_count": len(offline),
        "manual_review_count": len(manual),
        "max_observations": max_observations,
        "selected_read_only_observations": [asdict(item) for item in selected],
        "deferred_read_only_observations": [asdict(item) for item in observation_all[max_observations:]],
        "offline_repairs": [asdict(item) for item in offline],
        "manual_review": [asdict(item) for item in manual],
        "missing_evidence_is_negative_demand": False,
        "missing_evidence_interpretation": "unknown_not_negative_demand",
        "rate_budget_is_self_imposed_ceiling": True,
        "credentials_allowed": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }
