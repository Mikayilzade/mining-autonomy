"""Inert deterministic sampling manifest for permitted read-only evidence captures.

This module turns the production watchlist into an execution contract only. It performs
no network calls and never authenticates, accepts tasks, publishes services, or moves
value. A separate explicitly-authorized read-only capture client may later consume the
manifest and route already-captured bundles through observation_capture ->
evidence_archive -> archive_replay.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable
from urllib.parse import urlparse

from evidence_archive import EvidenceArchive
from observation_capture import CapturePolicy
from sampling_planner import DEFAULT_WATCH_TARGETS, WatchTarget, build_sampling_plan


@dataclass(frozen=True)
class SourceRateLimit:
    min_interval_seconds: float
    max_requests_per_window: int
    window_seconds: float
    budget_basis: str = "project_conservative_self_limit"


@dataclass(frozen=True)
class SourcePolicy:
    platform: str
    source_url: str
    expected_evidence_classes: tuple[str, ...]
    capture_within_hours: float
    max_source_age_hours: float
    rate_limit: SourceRateLimit
    method: str = "GET"
    credentials_allowed: bool = False
    environment: str = "production"
    notes: str = ""


@dataclass(frozen=True)
class SamplingManifestItem:
    platform: str
    source_url: str
    method: str
    scheduled: bool
    plan_score: int
    planner_reasons: tuple[str, ...]
    expected_evidence_classes: tuple[str, ...]
    environment: str
    capture_deadline: str | None
    max_source_age_hours: float
    rate_limit: SourceRateLimit
    provenance_requirements: tuple[str, ...]
    credentials_allowed: bool = False
    network_calls_performed: bool = False
    action_enabled: bool = False


DEFAULT_SOURCE_POLICIES: tuple[SourcePolicy, ...] = (
    SourcePolicy(
        platform="payanagent",
        source_url="https://payanagent.com/api/v1/discover",
        expected_evidence_classes=("open_demand_snapshot",),
        capture_within_hours=2.0,
        max_source_age_hours=6.0,
        rate_limit=SourceRateLimit(900.0, 1, 900.0),
        notes="Anonymous discovery endpoint documented by first-party API reference.",
    ),
    SourcePolicy(
        platform="payanagent",
        source_url="https://payanagent.com/api/v1/receipts",
        expected_evidence_classes=("paid_utilization_snapshot",),
        capture_within_hours=2.0,
        max_source_age_hours=6.0,
        rate_limit=SourceRateLimit(900.0, 1, 900.0),
        notes="Anonymous public receipts endpoint documented by first-party API reference.",
    ),
    SourcePolicy(
        platform="okx_ai_a2a",
        source_url="https://web3.okx.com/build/dev-docs/waas/a2a-network",
        expected_evidence_classes=("public_observability_gate",),
        capture_within_hours=6.0,
        max_source_age_hours=12.0,
        rate_limit=SourceRateLimit(1800.0, 1, 1800.0),
        notes="Documentation check only; provider demand must remain unproven if onboarding is required.",
    ),
    SourcePolicy(
        platform="agent2agent.market",
        source_url="https://agent2agent.market/",
        expected_evidence_classes=("open_demand_snapshot", "environment_marker"),
        capture_within_hours=6.0,
        max_source_age_hours=12.0,
        rate_limit=SourceRateLimit(1800.0, 1, 1800.0),
        environment="unknown",
        notes="Environment must be proven from the capture; testnet evidence cannot be promoted to production.",
    ),
    SourcePolicy(
        platform="mcpize",
        source_url="https://mcpize.com/developers",
        expected_evidence_classes=("public_observability_gate",),
        capture_within_hours=12.0,
        max_source_age_hours=24.0,
        rate_limit=SourceRateLimit(3600.0, 1, 3600.0),
        notes="Supply counts do not count as paid utilization.",
    ),
    SourcePolicy(
        platform="mcpize",
        source_url="https://mcpize.com/docs/monetization",
        expected_evidence_classes=("monetization_mechanics",),
        capture_within_hours=12.0,
        max_source_age_hours=24.0,
        rate_limit=SourceRateLimit(3600.0, 1, 3600.0),
        notes="Mechanics evidence cannot close a paid-utilization gap by itself.",
    ),
    SourcePolicy(
        platform="agentgigs.io",
        source_url="https://agentgigs.io/",
        expected_evidence_classes=("open_demand_snapshot", "public_observability_gate"),
        capture_within_hours=12.0,
        max_source_age_hours=24.0,
        rate_limit=SourceRateLimit(3600.0, 1, 3600.0),
        notes="No authentication or Stripe/KYC step is permitted by this manifest.",
    ),
)


PROVENANCE_REQUIREMENTS: tuple[str, ...] = (
    "record_exact_source_url",
    "record_source_timestamp_or_mark_unavailable",
    "record_capture_timestamp_utc",
    "record_environment_explicitly",
    "hash_normalized_request_snapshot",
    "hash_bundle_before_archive",
    "persist_no_raw_buyer_identity",
    "preserve_evidence_class_without_upgrading",
    "do_not_infer_demand_from_supply_counts",
)


def _validate_rate_limit(value: SourceRateLimit) -> None:
    if value.min_interval_seconds < 0:
        raise ValueError("manifest_rate_limit_min_interval_invalid")
    if not isinstance(value.max_requests_per_window, int) or isinstance(value.max_requests_per_window, bool) or value.max_requests_per_window <= 0:
        raise ValueError("manifest_rate_limit_request_budget_invalid")
    if value.window_seconds <= 0:
        raise ValueError("manifest_rate_limit_window_invalid")
    if value.budget_basis != "project_conservative_self_limit":
        raise ValueError("manifest_rate_limit_basis_invalid")


def _validate_source_policy(policy: SourcePolicy, target: WatchTarget) -> None:
    if policy.platform != target.platform:
        raise ValueError("manifest_policy_platform_mismatch")
    parsed = urlparse(policy.source_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("manifest_source_must_use_https")
    allowed_hosts = {urlparse(url).netloc for url in target.public_urls}
    if parsed.netloc not in allowed_hosts:
        raise ValueError("manifest_source_host_not_in_watch_target")
    if policy.method != "GET":
        raise ValueError("manifest_only_get_allowed")
    if policy.credentials_allowed is not False:
        raise ValueError("manifest_credentials_must_be_disabled")
    if policy.environment not in {"production", "unknown"}:
        raise ValueError("manifest_environment_invalid")
    if policy.capture_within_hours <= 0 or policy.max_source_age_hours <= 0:
        raise ValueError("manifest_capture_window_invalid")
    if not policy.expected_evidence_classes:
        raise ValueError("manifest_expected_evidence_required")
    _validate_rate_limit(policy.rate_limit)


def build_sampling_manifest(
    archive: EvidenceArchive,
    *,
    now: datetime | None = None,
    targets: Iterable[WatchTarget] = DEFAULT_WATCH_TARGETS,
    source_policies: Iterable[SourcePolicy] = DEFAULT_SOURCE_POLICIES,
) -> dict[str, Any]:
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    target_values = tuple(targets)
    target_by_platform = {target.platform: target for target in target_values}
    if len(target_by_platform) != len(target_values):
        raise ValueError("manifest_duplicate_watch_platform")

    plan = build_sampling_plan(archive, now=current, targets=target_values)
    plan_by_platform = {item.platform: item for item in plan}
    items: list[SamplingManifestItem] = []

    for policy in source_policies:
        target = target_by_platform.get(policy.platform)
        planned = plan_by_platform.get(policy.platform)
        if target is None or planned is None:
            raise ValueError("manifest_policy_platform_not_watched")
        _validate_source_policy(policy, target)
        deadline = current + timedelta(hours=policy.capture_within_hours) if planned.due else None
        items.append(SamplingManifestItem(
            platform=policy.platform,
            source_url=policy.source_url,
            method=policy.method,
            scheduled=planned.due,
            plan_score=planned.score,
            planner_reasons=planned.reasons,
            expected_evidence_classes=policy.expected_evidence_classes,
            environment=policy.environment,
            capture_deadline=deadline.isoformat() if deadline else None,
            max_source_age_hours=policy.max_source_age_hours,
            rate_limit=policy.rate_limit,
            provenance_requirements=PROVENANCE_REQUIREMENTS,
        ))

    items.sort(key=lambda item: (
        not item.scheduled,
        -item.plan_score,
        item.capture_deadline or "9999",
        item.platform,
        item.source_url,
    ))
    return {
        "schema_version": 1,
        "generated_at": current.isoformat(),
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "scheduled_source_count": sum(item.scheduled for item in items),
        "source_count": len(items),
        "items": [asdict(item) for item in items],
        "capture_bridge": {
            "input": "already_captured_sanitized_observation_bundle",
            "route": ("observation_capture", "evidence_archive", "archive_replay"),
            "environment_must_be_explicit": True,
            "raw_payload_archive_allowed": False,
            "buyer_identity_archive_allowed": False,
            "execution_authorization_from_evidence": False,
        },
    }


def capture_bridge_spec(item: SamplingManifestItem, *, bundle_sha256: str) -> dict[str, Any]:
    """Return exact offline capture/archive parameters for a future permitted capture."""
    if not isinstance(bundle_sha256, str) or len(bundle_sha256) != 64:
        raise ValueError("manifest_bundle_sha256_invalid")
    try:
        int(bundle_sha256, 16)
    except ValueError as exc:
        raise ValueError("manifest_bundle_sha256_invalid") from exc
    archive_environment = None if item.environment == "unknown" else item.environment
    return {
        "capture_policy": asdict(CapturePolicy(
            max_age_hours=item.max_source_age_hours,
            min_interval_seconds=item.rate_limit.min_interval_seconds,
            max_future_skew_seconds=120.0,
        )),
        "environment_by_bundle_sha256": (
            {bundle_sha256.lower(): archive_environment}
            if archive_environment is not None else {}
        ),
        "default_environment": "unknown",
        "route": ("observation_capture", "evidence_archive", "archive_replay"),
        "network_calls_performed": False,
        "action_enabled": False,
    }
