"""I140 bounded read-only market observation design.

Builds a no-spend, no-credential observation plan for a public endpoint only after
current policy evidence says that the observation method is permitted. The module
never performs network access. It enforces a caller-supplied provider/API minimum
interval and explicit request cap; it never bypasses rate limits, CAPTCHA, KYC,
geofencing, authentication, robots/Terms restrictions, or product limits.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil
from typing import Optional


@dataclass(frozen=True)
class ObservationDesignInput:
    platform: str
    source_ref: str
    policy_evidence_ref: str
    public_read_only_allowed: bool
    credentials_required: bool
    paid_account_required: bool
    captcha_or_human_challenge_required: bool
    geography_allowed: bool
    requested_poll_interval_seconds: float
    minimum_allowed_interval_seconds: float
    planned_duration_seconds: float
    max_requests: int
    hard_request_cap: int = 100
    expected_candidates_per_request: float = 0.0
    external_request_cost_usd: float = 0.0
    local_processing_cost_per_request_usd: float = 0.0
    ai_escalation_probability: float = 0.0
    ai_cost_per_call_usd: float = 0.0


@dataclass(frozen=True)
class ReadOnlyObservationPlan:
    state: str
    platform: str
    source_ref: str
    policy_evidence_ref: str
    effective_poll_interval_seconds: float
    planned_duration_seconds: float
    planned_requests: int
    request_cap: int
    expected_candidates: float
    expected_ai_calls: float
    estimated_incremental_cost_usd: float
    blockers: tuple[str, ...]
    stop_rules: tuple[str, ...]
    metrics_to_collect: tuple[str, ...]
    network_enabled: bool = False
    credentials_enabled: bool = False
    spend_enabled: bool = False
    task_acceptance_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False


def design_observation(inp: ObservationDesignInput) -> ReadOnlyObservationPlan:
    blockers=[]
    if not inp.platform.strip() or not inp.source_ref.strip():
        blockers.append("platform_and_source_ref_required")
    if not inp.policy_evidence_ref.strip():
        blockers.append("current_policy_evidence_ref_required")
    if not inp.public_read_only_allowed:
        blockers.append("public_read_only_observation_not_confirmed_allowed")
    if inp.credentials_required:
        blockers.append("credentials_required")
    if inp.paid_account_required:
        blockers.append("paid_account_required")
    if inp.captcha_or_human_challenge_required:
        blockers.append("captcha_or_human_challenge_present")
    if not inp.geography_allowed:
        blockers.append("geography_not_confirmed_allowed")
    if inp.requested_poll_interval_seconds <= 0 or inp.minimum_allowed_interval_seconds <= 0:
        blockers.append("positive_poll_intervals_required")
    if inp.requested_poll_interval_seconds < inp.minimum_allowed_interval_seconds:
        blockers.append("requested_polling_faster_than_allowed_limit")
    if inp.planned_duration_seconds <= 0:
        blockers.append("positive_duration_required")
    if inp.max_requests <= 0 or inp.hard_request_cap <= 0:
        blockers.append("positive_request_caps_required")
    if inp.max_requests > inp.hard_request_cap:
        blockers.append("requested_cap_exceeds_hard_cap")
    if inp.external_request_cost_usd != 0:
        blockers.append("external_paid_request_cost_not_allowed_in_no_spend_observation")
    for value in (
        inp.expected_candidates_per_request,
        inp.local_processing_cost_per_request_usd,
        inp.ai_escalation_probability,
        inp.ai_cost_per_call_usd,
    ):
        if value < 0:
            blockers.append("negative_economic_input")
            break
    if inp.ai_escalation_probability > 1:
        blockers.append("ai_escalation_probability_above_one")

    interval=max(inp.requested_poll_interval_seconds, inp.minimum_allowed_interval_seconds, 1e-9)
    duration_requests=max(1, ceil(inp.planned_duration_seconds / interval)) if inp.planned_duration_seconds > 0 else 0
    planned=min(duration_requests, max(0, inp.max_requests), max(0, inp.hard_request_cap))
    expected_candidates=planned*max(0.0, inp.expected_candidates_per_request)
    expected_ai_calls=expected_candidates*max(0.0, min(1.0, inp.ai_escalation_probability))
    estimated=(
        planned*max(0.0, inp.local_processing_cost_per_request_usd)
        + expected_ai_calls*max(0.0, inp.ai_cost_per_call_usd)
    )

    return ReadOnlyObservationPlan(
        state="PLAN_READY_FOR_SEPARATE_AUTHORIZED_RUNNER" if not blockers else "HOLD",
        platform=inp.platform,
        source_ref=inp.source_ref,
        policy_evidence_ref=inp.policy_evidence_ref,
        effective_poll_interval_seconds=interval,
        planned_duration_seconds=max(0.0, inp.planned_duration_seconds),
        planned_requests=planned,
        request_cap=min(max(0, inp.max_requests), max(0, inp.hard_request_cap)),
        expected_candidates=round(expected_candidates, 6),
        expected_ai_calls=round(expected_ai_calls, 6),
        estimated_incremental_cost_usd=round(estimated, 8),
        blockers=tuple(dict.fromkeys(blockers)),
        stop_rules=(
            "stop_on_policy_or_terms_change",
            "stop_on_rate_limit_or_retry_after_signal",
            "stop_on_authentication_captcha_or_human_challenge",
            "stop_on_geography_or_access_restriction",
            "stop_at_request_cap",
            "stop_if_endpoint_behavior_differs_from_read_only_contract",
            "never_accept_or_submit_paid_work",
        ),
        metrics_to_collect=(
            "observation_timestamp_utc",
            "opportunity_external_id_or_stable_dedupe_key",
            "new_vs_duplicate",
            "advertised_payout_or_price_when_public",
            "platform_fee_when_public",
            "task_category_and_machine_executable_requirements",
            "public_acceptance_or_availability_signal_without_claiming_work",
            "expiry_or_deadline_when_public",
            "required_capabilities",
            "policy_or_access_anomalies",
            "request_latency_and_parse_success",
        ),
    )


def payload(plan: ReadOnlyObservationPlan) -> dict:
    body=asdict(plan)
    body.update({
        "schema":"mining-autonomy/i140-readonly-observation-design/v1",
        "run":"I140",
        "production_observation_performed":False,
        "network_access_performed":False,
        "credentials_used":False,
        "spend_or_value_movement":False,
    })
    return body
