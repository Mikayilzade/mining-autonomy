"""I157 policy gate for the current free_tier_ci evidence branch.

Classifies GitHub Actions standard GitHub-hosted runners for this public repository
without dispatching workflows or using credentials. Current GitHub policy allows
free standard hosted-runner use for public repositories, but hosted runners may not
be used for arbitrary activity unrelated to production/testing/deployment/publication
of the software project associated with the repository. Therefore generic external
paid-task execution is support/testing-only, not a production earning backend.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CiPolicyEvidence:
    provider: str
    repository_visibility: str
    standard_public_runner_free: bool
    generic_external_paid_task_execution_allowed: bool
    project_development_testing_allowed: bool
    quota_semantics: str
    evidence_date: str
    billing_source: str
    terms_source: str
    limits_source: str


@dataclass(frozen=True)
class CiPolicyDecision:
    backend_id: str
    state: str
    production_paid_task_eligible: bool
    development_testing_eligible: bool
    incremental_runner_price_usd: float | None
    capacity_claim_verified: bool
    source_bound_runtime_feasible_for_testing: bool
    no_workflow_dispatched: bool
    credentials_used: bool
    spend_performed: bool
    blockers: tuple[str, ...]


def evaluate(evidence: CiPolicyEvidence) -> CiPolicyDecision:
    if evidence.provider != "github_actions":
        raise ValueError("unsupported_provider")
    if evidence.repository_visibility != "public":
        raise ValueError("public_repository_evidence_required_for_this_checkpoint")

    blockers: list[str] = []
    if not evidence.standard_public_runner_free:
        blockers.append("standard_public_runner_free_not_verified")
    if evidence.generic_external_paid_task_execution_allowed:
        blockers.append("policy_evidence_unexpectedly_allows_generic_external_paid_tasks")
    if not evidence.project_development_testing_allowed:
        blockers.append("project_development_testing_not_verified")

    # "Free and unlimited" in GitHub billing docs is a pricing statement for
    # standard public-repository runners, not a claim of infinite capacity. System
    # limits, concurrency and abuse controls still apply, so capacity remains unmeasured.
    return CiPolicyDecision(
        backend_id="free_tier_ci",
        state="SUPPORT_TESTING_ONLY" if not blockers else "FAIL_CLOSED",
        production_paid_task_eligible=False,
        development_testing_eligible=not blockers,
        incremental_runner_price_usd=0.0 if evidence.standard_public_runner_free else None,
        capacity_claim_verified=False,
        source_bound_runtime_feasible_for_testing=not blockers,
        no_workflow_dispatched=True,
        credentials_used=False,
        spend_performed=False,
        blockers=tuple(blockers) + (
            "generic_external_paid_task_execution_not_allowed_on_github_hosted_runner",
            "capacity_concurrency_rate_limits_not_measured",
        ),
    )


def current_github_public_repo_evidence() -> CiPolicyEvidence:
    return CiPolicyEvidence(
        provider="github_actions",
        repository_visibility="public",
        standard_public_runner_free=True,
        generic_external_paid_task_execution_allowed=False,
        project_development_testing_allowed=True,
        quota_semantics=(
            "standard GitHub-hosted runners are free for public repositories, but usage remains "
            "subject to Actions limits, concurrency, abuse controls and product terms; not infinite capacity"
        ),
        evidence_date="2026-08-24",
        billing_source="https://docs.github.com/en/actions/concepts/billing-and-usage",
        terms_source="https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features",
        limits_source="https://docs.github.com/en/actions/reference/limits",
    )


def payload() -> dict[str, Any]:
    evidence = current_github_public_repo_evidence()
    decision = evaluate(evidence)
    return {
        "schema": "mining-autonomy/i157-free-tier-ci-policy-gate/v1",
        "run": "I157",
        "evidence": asdict(evidence),
        "decision": asdict(decision),
        "production_route_created": False,
        "workflow_dispatched": False,
        "authorization_created": False,
        "network_execution_performed": False,
        "spend_or_value_movement": False,
        "next_backend": "local_model",
    }
