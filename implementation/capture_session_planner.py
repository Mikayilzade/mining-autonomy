"""Deterministic no-network capture-session planner over I028 readiness packets.

The planner batches only sources explicitly classified as ready, applies a global
request/time budget plus per-host conservative rate contracts, and emits an exact
chronological plan. It never performs HTTP, uses credentials, accepts work,
publishes services, moves value, or grants authorization.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from urllib.parse import urlsplit


READY_STATE = "ready_for_future_explicit_read_only_capture"
BLOCKED_STATE = "blocked_by_observability_or_environment_requirement"


@dataclass(frozen=True)
class SessionStep:
    sequence: int
    priority_index: int
    platform: str
    item_index: int
    source_url: str
    host: str
    method: str
    scheduled_at_utc: str
    offset_seconds: float
    expected_evidence_classes: tuple[str, ...]
    required_environment: str
    provenance_checklist: tuple[str, ...]
    manifest_item_sha256: str
    authorization_state: str = "explicit_read_only_network_authorization_required"
    credentials_allowed: bool = False
    network_calls_performed: bool = False
    dry_run_only: bool = True
    action_enabled: bool = False


def _parse_start(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("capture_session_start_invalid")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("capture_session_start_invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("capture_session_start_timezone_required")
    return parsed.astimezone(timezone.utc)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _validate_packet(packet: Mapping[str, Any]) -> None:
    if packet.get("schema_version") != 1:
        raise ValueError("capture_session_packet_schema_invalid")
    if packet.get("mode") != "deterministic_no_network_capture_readiness_packet":
        raise ValueError("capture_session_packet_mode_invalid")
    if packet.get("authorization_granted") is not False:
        raise ValueError("capture_session_packet_authorization_invalid")
    if packet.get("network_calls_performed") is not False:
        raise ValueError("capture_session_packet_network_flag_invalid")
    if packet.get("credentials_allowed") is not False:
        raise ValueError("capture_session_packet_credentials_flag_invalid")
    if packet.get("dry_run_only") is not True:
        raise ValueError("capture_session_packet_dry_run_flag_invalid")
    if packet.get("action_enabled") is not False:
        raise ValueError("capture_session_packet_action_flag_invalid")
    if packet.get("missing_evidence_is_negative_demand") is not False:
        raise ValueError("capture_session_missing_evidence_semantics_invalid")
    if not isinstance(packet.get("ready_for_future_explicit_read_only_capture"), list):
        raise ValueError("capture_session_ready_list_invalid")
    if not isinstance(packet.get("blocked_by_observability_or_environment_requirement"), list):
        raise ValueError("capture_session_blocked_list_invalid")


def _host(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("capture_session_source_url_invalid")
    if parsed.fragment:
        raise ValueError("capture_session_source_url_fragment_forbidden")
    return parsed.hostname.lower()


def _rate_contract(row: Mapping[str, Any]) -> tuple[float, int, float]:
    rate = row.get("rate_limit")
    if not isinstance(rate, Mapping):
        raise ValueError("capture_session_rate_limit_missing")
    if rate.get("budget_basis") != "project_conservative_self_limit":
        raise ValueError("capture_session_rate_limit_basis_invalid")
    try:
        min_interval = float(rate["min_interval_seconds"])
        max_requests = int(rate["max_requests_per_window"])
        window_seconds = float(rate["window_seconds"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("capture_session_rate_limit_invalid") from exc
    if min_interval < 0 or max_requests <= 0 or window_seconds <= 0:
        raise ValueError("capture_session_rate_limit_invalid")
    return min_interval, max_requests, window_seconds


def _validate_ready_row(row: Mapping[str, Any]) -> None:
    if not isinstance(row, Mapping):
        raise ValueError("capture_session_ready_row_invalid")
    if row.get("readiness_state") != READY_STATE:
        raise ValueError("capture_session_ready_state_invalid")
    if row.get("authorization_state") != "explicit_read_only_network_authorization_required":
        raise ValueError("capture_session_item_authorization_invalid")
    if row.get("method") != "GET":
        raise ValueError("capture_session_non_get_forbidden")
    if row.get("required_environment") != "production":
        raise ValueError("capture_session_nonproduction_ready_forbidden")
    if row.get("credentials_allowed") is not False:
        raise ValueError("capture_session_credentials_forbidden")
    if row.get("network_calls_performed") is not False or row.get("action_enabled") is not False:
        raise ValueError("capture_session_action_boundary_invalid")
    if row.get("dry_run_only") is not True:
        raise ValueError("capture_session_dry_run_required")
    if not row.get("manifest_item_sha256"):
        raise ValueError("capture_session_manifest_item_hash_missing")
    if not row.get("expected_evidence_classes"):
        raise ValueError("capture_session_evidence_class_missing")
    if not row.get("provenance_checklist"):
        raise ValueError("capture_session_provenance_missing")
    _host(str(row.get("source_url", "")))
    _rate_contract(row)


def _validate_blocked_row(row: Mapping[str, Any]) -> None:
    if not isinstance(row, Mapping):
        raise ValueError("capture_session_blocked_row_invalid")
    if row.get("readiness_state") != BLOCKED_STATE:
        raise ValueError("capture_session_blocked_state_invalid")
    if row.get("network_calls_performed") is not False or row.get("action_enabled") is not False:
        raise ValueError("capture_session_blocked_action_boundary_invalid")
    if row.get("credentials_allowed") is not False:
        raise ValueError("capture_session_blocked_credentials_invalid")


def _next_host_slot(
    *,
    start: datetime,
    history: list[datetime],
    min_interval: float,
    max_requests: int,
    window_seconds: float,
) -> datetime:
    candidate = start
    if history and min_interval:
        candidate = max(candidate, history[-1] + timedelta(seconds=min_interval))
    if len(history) >= max_requests:
        candidate = max(candidate, history[-max_requests] + timedelta(seconds=window_seconds))
    return candidate


def build_capture_session_plan(
    readiness_packet: Mapping[str, Any],
    *,
    start_time_utc: str,
    total_request_budget: int,
    total_time_budget_seconds: float,
) -> dict[str, Any]:
    """Build a deterministic chronological no-network capture session."""
    _validate_packet(readiness_packet)
    start = _parse_start(start_time_utc)
    if not isinstance(total_request_budget, int) or isinstance(total_request_budget, bool) or total_request_budget <= 0:
        raise ValueError("capture_session_request_budget_invalid")
    try:
        time_budget = float(total_time_budget_seconds)
    except (TypeError, ValueError) as exc:
        raise ValueError("capture_session_time_budget_invalid") from exc
    if time_budget < 0:
        raise ValueError("capture_session_time_budget_invalid")

    ready_rows = readiness_packet["ready_for_future_explicit_read_only_capture"]
    blocked_rows = readiness_packet["blocked_by_observability_or_environment_requirement"]
    for row in ready_rows:
        _validate_ready_row(row)
    for row in blocked_rows:
        _validate_blocked_row(row)

    host_history: dict[str, list[datetime]] = {}
    planned: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []

    # I028 preserves the I027 priority order. Keep that order for admission,
    # then sort admitted steps by exact scheduled timestamp for execution view.
    for priority_index, row in enumerate(ready_rows):
        if len(planned) >= total_request_budget:
            deferred.append({
                "priority_index": priority_index,
                "platform": str(row.get("platform")),
                "item_index": int(row.get("item_index")),
                "source_url": str(row.get("source_url")),
                "reason": "global_request_budget_exhausted",
            })
            continue

        host = _host(str(row["source_url"]))
        min_interval, max_requests, window_seconds = _rate_contract(row)
        history = host_history.setdefault(host, [])
        slot = _next_host_slot(
            start=start,
            history=history,
            min_interval=min_interval,
            max_requests=max_requests,
            window_seconds=window_seconds,
        )
        offset = (slot - start).total_seconds()
        if offset > time_budget:
            deferred.append({
                "priority_index": priority_index,
                "platform": str(row.get("platform")),
                "item_index": int(row.get("item_index")),
                "source_url": str(row.get("source_url")),
                "reason": "global_time_budget_exceeded_by_host_rate_contract",
                "earliest_offset_seconds": offset,
            })
            continue

        history.append(slot)
        planned.append({
            "priority_index": priority_index,
            "platform": str(row["platform"]),
            "item_index": int(row["item_index"]),
            "source_url": str(row["source_url"]),
            "host": host,
            "method": "GET",
            "scheduled_at_utc": _iso_utc(slot),
            "offset_seconds": offset,
            "expected_evidence_classes": tuple(str(v) for v in row["expected_evidence_classes"]),
            "required_environment": str(row["required_environment"]),
            "provenance_checklist": tuple(str(v) for v in row["provenance_checklist"]),
            "manifest_item_sha256": str(row["manifest_item_sha256"]),
        })

    planned.sort(key=lambda row: (row["offset_seconds"], row["priority_index"]))
    steps = [
        asdict(SessionStep(sequence=sequence, **row))
        for sequence, row in enumerate(planned, start=1)
    ]

    host_groups: dict[str, dict[str, Any]] = {}
    for step in steps:
        group = host_groups.setdefault(
            step["host"],
            {"host": step["host"], "request_count": 0, "sequence_numbers": []},
        )
        group["request_count"] += 1
        group["sequence_numbers"].append(step["sequence"])

    remediation = [
        {
            "platform": str(row.get("platform")),
            "item_index": int(row.get("item_index")),
            "source_url": str(row.get("source_url")),
            "readiness_reasons": tuple(str(v) for v in row.get("readiness_reasons", ())),
            "required_environment": str(row.get("required_environment", "unknown")),
            "remediation_state": "resolve_observability_or_environment_before_capture",
        }
        for row in blocked_rows
    ]

    return {
        "schema_version": 1,
        "mode": "deterministic_no_network_capture_session_plan",
        "manifest_sha256": readiness_packet.get("manifest_sha256"),
        "start_time_utc": _iso_utc(start),
        "total_request_budget": total_request_budget,
        "total_time_budget_seconds": time_budget,
        "planned_request_count": len(steps),
        "deferred_ready_count": len(deferred),
        "blocked_remediation_count": len(remediation),
        "chronological_session_plan": steps,
        "host_groups": [host_groups[key] for key in sorted(host_groups)],
        "deferred_ready_items": deferred,
        "blocked_remediation_queue": remediation,
        "authorization_state": "explicit_read_only_network_authorization_required",
        "authorization_granted": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "dry_run_only": True,
        "action_enabled": False,
        "missing_evidence_is_negative_demand": False,
    }
