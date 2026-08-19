"""Deterministic read-only production evidence watchlist planner.

The planner emits observation plans only. It never performs network calls, authenticates,
accepts work, publishes services, or enables money-moving actions.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable

from archive_replay import evidence_freshness
from evidence_archive import ArchiveEntry, EvidenceArchive


@dataclass(frozen=True)
class WatchTarget:
    platform: str
    priority: int
    max_age_hours: float
    observation_targets: tuple[str, ...]
    public_urls: tuple[str, ...]
    notes: str = ""


@dataclass(frozen=True)
class SamplingPlanItem:
    platform: str
    priority: int
    score: int
    due: bool
    freshness_state: str
    production_observation_present: bool
    demand_gap: bool
    paid_utilization_gap: bool
    reasons: tuple[str, ...]
    observation_targets: tuple[str, ...]
    public_urls: tuple[str, ...]
    network_calls_performed: bool = False
    action_enabled: bool = False


DEFAULT_WATCH_TARGETS: tuple[WatchTarget, ...] = (
    WatchTarget(
        platform="payanagent",
        priority=5,
        max_age_hours=6.0,
        observation_targets=("production_open_requests", "public_settled_receipts"),
        public_urls=("https://payanagent.com/",),
        notes="Primary task-market target; catalog supply is not demand.",
    ),
    WatchTarget(
        platform="okx_ai_a2a",
        priority=4,
        max_age_hours=12.0,
        observation_targets=("production_open_tasks_if_public", "provider_paid_utilization_if_public"),
        public_urls=("https://web3.okx.com/build/dev-docs/waas/a2a-network",),
        notes="Provider-side demand may remain onboarding-gated; never bypass account/KYC gates.",
    ),
    WatchTarget(
        platform="agent2agent.market",
        priority=4,
        max_age_hours=12.0,
        observation_targets=("production_open_tasks", "production_settled_receipts"),
        public_urls=("https://agent2agent.market/",),
        notes="Testnet/base-sepolia evidence never satisfies production evidence gaps.",
    ),
    WatchTarget(
        platform="mcpize",
        priority=4,
        max_age_hours=24.0,
        observation_targets=("attributable_public_paid_utilization",),
        public_urls=("https://mcpize.com/developers", "https://mcpize.com/docs/monetization"),
        notes="Server/publisher counts are supply-side only.",
    ),
    WatchTarget(
        platform="agentgigs.io",
        priority=3,
        max_age_hours=24.0,
        observation_targets=("public_production_jobs", "public_paid_utilization"),
        public_urls=("https://agentgigs.io/",),
        notes="Stripe/KYC geography remains an implementation gate, not a reason to evade controls.",
    ),
)


def _latest_production(archive: EvidenceArchive, platform: str) -> ArchiveEntry | None:
    matching = [
        entry for entry in archive.entries
        if entry.environment == "production" and entry.platform == platform
    ]
    if not matching:
        return None
    return max(matching, key=lambda item: (item.source_timestamp, item.entry_sha256))


def _score(*, target: WatchTarget, latest: ArchiveEntry | None,
           freshness_state: str, demand_gap: bool, paid_gap: bool) -> int:
    # Platform priority is intentionally dominant so high-value stale/unproven targets
    # outrank low-priority fresh checks. Evidence gaps then order work within a tier.
    score = target.priority * 100
    if latest is None:
        score += 80
    if paid_gap:
        score += 50
    if demand_gap:
        score += 40
    if freshness_state == "stale":
        score += 30
    elif freshness_state == "future_invalid":
        score += 70
    return score


def build_sampling_plan(
    archive: EvidenceArchive,
    *,
    now: datetime | None = None,
    targets: Iterable[WatchTarget] = DEFAULT_WATCH_TARGETS,
) -> list[SamplingPlanItem]:
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    plan: list[SamplingPlanItem] = []

    for target in targets:
        if target.priority < 1 or target.priority > 5:
            raise ValueError("watch_target_priority_out_of_range")
        if target.max_age_hours <= 0:
            raise ValueError("watch_target_max_age_must_be_positive")
        latest = _latest_production(archive, target.platform)

        if latest is None:
            freshness_state = "never_observed"
            demand_gap = True
            paid_gap = True
            reasons = [
                "no_production_observation",
                "production_demand_unproven",
                "production_paid_utilization_unproven",
            ]
        else:
            fresh = evidence_freshness(
                latest.source_timestamp,
                now=current,
                max_age_hours=target.max_age_hours,
            )
            freshness_state = fresh.state
            demand_gap = latest.demand_state != "positive_open_demand"
            paid_gap = latest.paid_utilization_state != "positive_paid_utilization"
            reasons = []
            if freshness_state != "fresh":
                reasons.append(f"evidence_{freshness_state}")
            if demand_gap:
                reasons.append("production_demand_unproven")
            if paid_gap:
                reasons.append("production_paid_utilization_unproven")

        due = bool(
            latest is None
            or freshness_state != "fresh"
            or demand_gap
            or paid_gap
        )
        if not due:
            reasons.append("fresh_required_evidence_present")

        plan.append(SamplingPlanItem(
            platform=target.platform,
            priority=target.priority,
            score=_score(
                target=target,
                latest=latest,
                freshness_state=freshness_state,
                demand_gap=demand_gap,
                paid_gap=paid_gap,
            ),
            due=due,
            freshness_state=freshness_state,
            production_observation_present=latest is not None,
            demand_gap=demand_gap,
            paid_utilization_gap=paid_gap,
            reasons=tuple(reasons),
            observation_targets=target.observation_targets,
            public_urls=target.public_urls,
        ))

    return sorted(
        plan,
        key=lambda item: (
            not item.due,
            -item.score,
            item.platform,
        ),
    )


def sampling_plan_report(
    archive: EvidenceArchive,
    *,
    now: datetime | None = None,
    targets: Iterable[WatchTarget] = DEFAULT_WATCH_TARGETS,
) -> dict[str, Any]:
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    items = build_sampling_plan(archive, now=current, targets=targets)
    return {
        "generated_at": current.isoformat(),
        "planner_mode": "read_only_plan_only",
        "network_calls_performed": False,
        "action_enabled": False,
        "platform_count": len(items),
        "due_count": sum(item.due for item in items),
        "items": [asdict(item) for item in items],
    }
