"""Offline Resource / Execution Router foundation (I048).

Models execution resources and conservative per-task economics without enabling
execution, network access, credentials, paid infrastructure, or value movement.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import FrozenSet, Iterable, Optional, Any

@dataclass(frozen=True)
class ExecutionBackend:
    backend_id: str
    family: str
    capabilities: FrozenSet[str]
    automation_role: str  # autonomous | support_only
    programmatic_access: bool
    policy_allowed: bool
    currently_available: bool
    requires_credentials: bool
    requires_paid_account: bool
    requires_new_spend: bool
    fixed_monthly_cost_usd: float
    sunk_or_already_committed: bool
    allocation_basis_tasks_per_month: Optional[float]
    quota_units_monthly: Optional[float]
    quota_units_remaining: Optional[float]
    unit_name: str
    marginal_cost_per_unit_usd: float
    units_per_task: float
    electricity_per_task_usd: float
    external_api_per_task_usd: float
    retry_failure_expected_cost_usd: float
    maintenance_minutes_per_task: float
    human_time_value_per_hour_usd: float
    opportunity_cost_per_task_usd: float
    latency_seconds: float
    reliability_probability: float
    quality_probability: float
    max_parallelism: int
    rate_limit_per_minute: Optional[float]
    notes: str = ""

    def marginal_cost_usd(self) -> float:
        maintenance = (max(0.0, self.maintenance_minutes_per_task) / 60.0) * max(0.0, self.human_time_value_per_hour_usd)
        return round(
            max(0.0, self.units_per_task) * max(0.0, self.marginal_cost_per_unit_usd)
            + max(0.0, self.electricity_per_task_usd)
            + max(0.0, self.external_api_per_task_usd)
            + max(0.0, self.retry_failure_expected_cost_usd)
            + maintenance
            + max(0.0, self.opportunity_cost_per_task_usd),
            6,
        )

    def allocated_fixed_cost_per_task_usd(self) -> Optional[float]:
        if self.sunk_or_already_committed:
            return 0.0
        if self.fixed_monthly_cost_usd <= 0:
            return 0.0
        basis = self.allocation_basis_tasks_per_month
        if basis is None or basis <= 0:
            return None
        return round(self.fixed_monthly_cost_usd / basis, 6)

    def effective_success_probability(self) -> float:
        return round(
            max(0.0, min(1.0, self.reliability_probability))
            * max(0.0, min(1.0, self.quality_probability)),
            6,
        )

@dataclass(frozen=True)
class TaskEconomics:
    task_id: str
    required_capabilities: FrozenSet[str]
    gross_payout_usd: float
    platform_fee_usd: float = 0.0
    platform_fee_rate: float = 0.0
    transaction_fee_usd: float = 0.0
    gas_fee_usd: float = 0.0
    withdrawal_conversion_fee_usd: float = 0.0
    dispute_probability: float = 0.0
    nonpayment_probability: float = 0.0
    acceptance_probability: float = 1.0
    minimum_success_probability: float = 0.90
    minimum_expected_margin_usd: float = 0.25
    minimum_expected_margin_ratio: float = 0.30

    def fixed_fees_usd(self) -> float:
        return round(
            max(0.0, self.platform_fee_usd)
            + max(0.0, self.gross_payout_usd) * max(0.0, self.platform_fee_rate)
            + max(0.0, self.transaction_fee_usd)
            + max(0.0, self.gas_fee_usd)
            + max(0.0, self.withdrawal_conversion_fee_usd),
            6,
        )

    def expected_collect_probability(self) -> float:
        acceptance = max(0.0, min(1.0, self.acceptance_probability))
        dispute_survival = 1.0 - max(0.0, min(1.0, self.dispute_probability))
        nonpayment_survival = 1.0 - max(0.0, min(1.0, self.nonpayment_probability))
        return round(acceptance * dispute_survival * nonpayment_survival, 6)

@dataclass(frozen=True)
class BackendQuote:
    backend_id: str
    planning_state: str
    planning_reasons: tuple[str, ...]
    live_blockers: tuple[str, ...]
    marginal_cost_usd: float
    allocated_fixed_cost_per_task_usd: Optional[float]
    fixed_monthly_cost_reference_usd: float
    success_probability: float
    expected_revenue_usd: float
    expected_margin_before_fixed_allocation_usd: float
    expected_margin_after_fixed_allocation_usd: Optional[float]
    expected_margin_ratio: float
    latency_seconds: float
    max_parallelism: int
    rate_limit_per_minute: Optional[float]
    action_enabled: bool = False

def quote_backend(task: TaskEconomics, backend: ExecutionBackend) -> BackendQuote:
    planning_reasons: list[str] = []
    live_blockers: list[str] = []

    if not backend.policy_allowed:
        planning_reasons.append("backend_not_policy_allowed")
    if backend.automation_role != "autonomous" or not backend.programmatic_access:
        planning_reasons.append("no_autonomous_programmatic_execution_path")
    if not task.required_capabilities.issubset(backend.capabilities):
        planning_reasons.append("capability_mismatch")
    if backend.max_parallelism < 1:
        planning_reasons.append("no_parallel_capacity")
    if backend.quota_units_remaining is not None and backend.quota_units_remaining < backend.units_per_task:
        planning_reasons.append("quota_insufficient")

    success = backend.effective_success_probability()
    if success < task.minimum_success_probability:
        planning_reasons.append("success_probability_below_threshold")

    marginal = backend.marginal_cost_usd()
    allocated_fixed = backend.allocated_fixed_cost_per_task_usd()
    collect_probability = task.expected_collect_probability()
    expected_revenue = max(0.0, task.gross_payout_usd) * success * collect_probability
    expected_margin = expected_revenue - task.fixed_fees_usd() - marginal
    expected_margin_after_fixed = None if allocated_fixed is None else expected_margin - allocated_fixed
    ratio = expected_margin / task.gross_payout_usd if task.gross_payout_usd > 0 else -1.0

    if expected_margin < task.minimum_expected_margin_usd or ratio < task.minimum_expected_margin_ratio:
        planning_reasons.append("insufficient_conservative_expected_margin")

    if not backend.currently_available:
        live_blockers.append("backend_not_currently_available")
    if backend.requires_credentials:
        live_blockers.append("credentials_required_before_live_execution")
    if backend.requires_paid_account:
        live_blockers.append("paid_account_required_before_live_execution")
    if backend.requires_new_spend:
        live_blockers.append("new_spend_requires_explicit_authorization")
    if allocated_fixed is None:
        live_blockers.append("fixed_cost_allocation_basis_unknown")
    live_blockers.append("execution_globally_disabled")

    hard_live_blockers = {
        "backend_not_currently_available",
        "credentials_required_before_live_execution",
        "paid_account_required_before_live_execution",
        "new_spend_requires_explicit_authorization",
        "fixed_cost_allocation_basis_unknown",
    }
    if planning_reasons:
        state = "hold"
    elif any(blocker in hard_live_blockers for blocker in live_blockers):
        state = "planning_only"
    else:
        state = "eligible_dry_run"
    return BackendQuote(
        backend_id=backend.backend_id,
        planning_state=state,
        planning_reasons=tuple(dict.fromkeys(planning_reasons)),
        live_blockers=tuple(dict.fromkeys(live_blockers)),
        marginal_cost_usd=round(marginal, 6),
        allocated_fixed_cost_per_task_usd=allocated_fixed,
        fixed_monthly_cost_reference_usd=round(max(0.0, backend.fixed_monthly_cost_usd), 6),
        success_probability=success,
        expected_revenue_usd=round(expected_revenue, 6),
        expected_margin_before_fixed_allocation_usd=round(expected_margin, 6),
        expected_margin_after_fixed_allocation_usd=None if expected_margin_after_fixed is None else round(expected_margin_after_fixed, 6),
        expected_margin_ratio=round(ratio, 6),
        latency_seconds=max(0.0, backend.latency_seconds),
        max_parallelism=backend.max_parallelism,
        rate_limit_per_minute=backend.rate_limit_per_minute,
    )

@dataclass(frozen=True)
class RoutingDecision:
    task_id: str
    state: str
    selected_backend_id: Optional[str]
    selected_quote: Optional[BackendQuote]
    quotes: tuple[BackendQuote, ...]
    selection_rule: str = "lowest_marginal_cost_then_highest_expected_margin_then_reliability"
    dry_run_only: bool = True
    execution_enabled: bool = False

def route_task(task: TaskEconomics, backends: Iterable[ExecutionBackend]) -> RoutingDecision:
    quotes = tuple(quote_backend(task, backend) for backend in backends)
    eligible = [q for q in quotes if q.planning_state == "eligible_dry_run"]
    if not eligible:
        return RoutingDecision(task.task_id, "hold", None, None, quotes)
    eligible.sort(
        key=lambda q: (
            q.marginal_cost_usd,
            -q.expected_margin_before_fixed_allocation_usd,
            -q.success_probability,
            q.latency_seconds,
            q.backend_id,
        )
    )
    selected = eligible[0]
    return RoutingDecision(
        task_id=task.task_id,
        state="route_dry_run",
        selected_backend_id=selected.backend_id,
        selected_quote=selected,
        quotes=quotes,
    )

def default_backend_families() -> tuple[ExecutionBackend, ...]:
    """Synthetic reference profiles; values are illustrative, never live price claims."""
    return (
        ExecutionBackend(
            "python_local", "deterministic_python", frozenset({"extract", "transform", "validate"}),
            "autonomous", True, True, True, False, False, False,
            0.0, True, None, None, None, "task", 0.0, 1.0,
            0.01, 0.0, 0.01, 0.2, 10.0, 0.0, 1.0, 0.995, 0.995, 4, 120.0,
            "Owned/local deterministic execution reference."
        ),
        ExecutionBackend(
            "local_model", "local_cpu_gpu_model", frozenset({"extract", "summarize", "classify"}),
            "autonomous", True, True, False, False, False, False,
            0.0, True, None, None, None, "task", 0.0, 1.0,
            0.03, 0.0, 0.03, 0.5, 10.0, 0.01, 8.0, 0.98, 0.92, 1, 30.0,
            "Availability/hardware intentionally not assumed."
        ),
        ExecutionBackend(
            "subscription_assistant", "chatgpt_codex_subscription", frozenset({"extract", "summarize", "research", "code"}),
            "support_only", False, True, True, False, False, False,
            20.0, True, None, 100.0, 100.0, "session", 0.0, 1.0,
            0.0, 0.0, 0.0, 1.0, 10.0, 0.0, 15.0, 0.99, 0.98, 1, None,
            "Fixed/limited non-API resource; no free autonomous programmatic access is assumed."
        ),
        ExecutionBackend(
            "cheap_external_api", "cheap_external_llm_api", frozenset({"extract", "summarize", "classify", "research"}),
            "autonomous", True, True, False, True, False, False,
            0.0, False, None, None, None, "request", 0.0, 1.0,
            0.0, 0.03, 0.01, 0.1, 10.0, 0.0, 2.0, 0.99, 0.94, 10, 60.0,
            "Synthetic cost only; real vendor/pricing/credentials not assumed."
        ),
        ExecutionBackend(
            "strong_external_api", "strong_external_llm_api", frozenset({"extract", "summarize", "classify", "research", "code"}),
            "autonomous", True, True, False, True, False, False,
            0.0, False, None, None, None, "request", 0.0, 1.0,
            0.0, 0.40, 0.03, 0.1, 10.0, 0.0, 5.0, 0.995, 0.985, 5, 30.0,
            "Synthetic cost only; expensive path should be used only when economics justify it."
        ),
        ExecutionBackend(
            "free_tier_ci", "free_tier_ci_cloud", frozenset({"extract", "transform", "validate", "code"}),
            "autonomous", True, True, False, False, False, False,
            0.0, True, None, 100.0, 100.0, "minute", 0.0, 2.0,
            0.0, 0.0, 0.01, 0.1, 10.0, 0.0, 20.0, 0.98, 0.99, 2, 6.0,
            "Synthetic free-tier capacity; provider quota/ToS must be verified before use."
        ),
        ExecutionBackend(
            "owned_pc", "owned_pc", frozenset({"extract", "transform", "validate", "summarize", "classify"}),
            "autonomous", True, True, True, False, False, False,
            0.0, True, None, None, None, "task", 0.0, 1.0,
            0.04, 0.0, 0.02, 0.5, 10.0, 0.02, 5.0, 0.97, 0.94, 2, 60.0,
            "Owned hardware reference; actual energy/hardware availability must be measured."
        ),
        ExecutionBackend(
            "future_paid_vps", "paid_vps_server", frozenset({"extract", "transform", "validate", "summarize", "classify"}),
            "autonomous", True, True, False, False, True, True,
            10.0, False, None, None, None, "task", 0.0, 1.0,
            0.0, 0.0, 0.01, 0.1, 10.0, 0.0, 3.0, 0.995, 0.96, 4, 120.0,
            "Future paid infrastructure; no rental/spend is authorized."
        ),
    )

@dataclass(frozen=True)
class WatcherPolicy:
    polling_interval_seconds: int
    mode: str  # poll | webhook | websocket
    local_filtering_required: bool = True
    llm_on_every_poll: bool = False
    obey_platform_rate_limits: bool = True
    bypass_product_limits: bool = False
    network_enabled: bool = False

def validate_watcher_policy(policy: WatcherPolicy, *, platform_min_interval_seconds: int) -> dict[str, Any]:
    reasons: list[str] = []
    if policy.mode not in {"poll", "webhook", "websocket"}:
        reasons.append("unsupported_watcher_mode")
    if policy.polling_interval_seconds <= 0:
        reasons.append("invalid_poll_interval")
    if policy.mode == "poll" and policy.polling_interval_seconds < platform_min_interval_seconds:
        reasons.append("polling_faster_than_platform_limit")
    if policy.llm_on_every_poll:
        reasons.append("llm_on_every_poll_disallowed_by_default")
    if not policy.local_filtering_required:
        reasons.append("local_filtering_required")
    if not policy.obey_platform_rate_limits or policy.bypass_product_limits:
        reasons.append("rate_limit_or_product_limit_bypass")
    if policy.network_enabled:
        reasons.append("network_must_remain_disabled_in_i048")
    return {
        "state": "valid_inert_watcher_plan" if not reasons else "hold",
        "reasons": tuple(dict.fromkeys(reasons)),
        "network_enabled": False,
        "local_filtering_before_ai": True,
    }

def decision_record(decision: RoutingDecision) -> dict[str, Any]:
    return asdict(decision)
