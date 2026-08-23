"""I148-I150 PayanAgent geography/access resolution and source-branch state.

Offline only. This checkpoint records the authoritative-first-party result after the
2026-08-24 Terms review. PayanAgent Terms explicitly require legality in the user's
jurisdiction but do not publish a supported-country list, global eligibility promise,
or Azerbaijan-specific rule. Documentation silence is not promoted to permission.

No market endpoint, registration, credential, wallet, payment, bid, acceptance,
fulfillment, or value-moving action is performed here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from i142_market_source_evidence_gate import SourceFact, assess_source
from i145_payanagent_source_checkpoint import current_facts

OBSERVED_DATE = "2026-08-24"
TERMS_URL = "https://payanagent.com/terms"
CONTACT_URL = "https://payanagent.com/contact"


@dataclass(frozen=True)
class GeographyResolution:
    platform: str
    state: str
    explicit_supported_country_rule_found: bool
    explicit_global_access_rule_found: bool
    explicit_azerbaijan_rule_found: bool
    jurisdiction_legality_clause_found: bool
    source_gate_state: str
    source_gate_blockers: tuple[str, ...]
    next_evidence_paths: tuple[str, ...]
    prohibited_inference: str
    production_market_endpoint_called: bool = False
    credentials_used: bool = False
    registration_performed: bool = False
    wallet_used: bool = False
    spend_or_value_movement: bool = False


def terms_facts() -> tuple[SourceFact, ...]:
    """Facts that the current Terms actually establish; no geography permission fact."""
    return (
        SourceFact(
            field="jurisdiction_legality_clause",
            value="user_responsible_for_activity_not_illegal_in_own_or_platform_jurisdiction",
            source_ref=TERMS_URL,
            observed_date=OBSERVED_DATE,
        ),
    )


def resolve() -> GeographyResolution:
    # Deliberately do not add geography_access_rule: the Terms clause allocates legal
    # responsibility but does not say which countries may access/observe/work.
    decision = assess_source("PayanAgent", (*current_facts(), *terms_facts()))
    expected = ("missing_required_fact:geography_access_rule",)
    if decision.blockers != expected:
        raise ValueError(f"unexpected_source_gate_state:{decision.blockers}")
    return GeographyResolution(
        platform="PayanAgent",
        state="POLICY_CONTACT_OR_USER_LOCAL_ACCESS_REQUIRED",
        explicit_supported_country_rule_found=False,
        explicit_global_access_rule_found=False,
        explicit_azerbaijan_rule_found=False,
        jurisdiction_legality_clause_found=True,
        source_gate_state=decision.state,
        source_gate_blockers=decision.blockers,
        next_evidence_paths=(
            "authoritative_provider_contact_reply_explicitly_covering_observation_and_provider_access_from_Azerbaijan",
            "user_local_access_evidence_only_after_separate_bounded_read_only_authorization",
        ),
        prohibited_inference="absence_of_country_block_or_public_endpoint_reachability_does_not_prove_marketplace_or_provider_eligibility",
    )


@dataclass(frozen=True)
class LocalAccessEvidenceContract:
    state: str
    purpose: str
    allowed_when_authorized: tuple[str, ...]
    forbidden: tuple[str, ...]
    promotion_rule: str
    observation_enabled: bool = False
    network_enabled: bool = False
    credentials_enabled: bool = False
    task_acceptance_enabled: bool = False
    spend_enabled: bool = False
    value_movement_enabled: bool = False


def local_access_contract() -> LocalAccessEvidenceContract:
    """I149: define, but do not execute, the minimal local-access evidence path."""
    return LocalAccessEvidenceContract(
        state="DESIGN_ONLY_SEPARATE_AUTHORIZATION_REQUIRED",
        purpose="resolve whether the intended public read-only PayanAgent observation path is accessible and permitted from the user's actual location without inferring provider eligibility",
        allowed_when_authorized=(
            "fetch_current_terms_and_api_docs",
            "perform_only_the_exact_public_read_only_endpoint_calls_named_in_the_authorized_manifest",
            "record_status_headers_retry_after_and_explicit_geography_or_access_messages",
            "stop_at_manifest_request_cap",
        ),
        forbidden=(
            "registration",
            "api_key_creation_or_use",
            "wallet_or_payment_use",
            "bid_accept_fulfill_approve_buy_or_sell",
            "captcha_or_geofence_bypass",
            "rate_limit_or_product_limit_bypass",
            "treating_plain_http_200_as_proof_of_provider_country_eligibility",
        ),
        promotion_rule="source geography gate may pass only from explicit provider policy/contact evidence that covers the intended access role; reachability alone is insufficient",
    )


@dataclass(frozen=True)
class SourceBranchDecision:
    active_source: str
    state: str
    blockers: tuple[str, ...]
    next_action: str
    discovery_reopened: bool = False
    observation_authorized: bool = False


def branch_decision(*, contact_evidence_available: bool = False, authorized_local_access_evidence_available: bool = False) -> SourceBranchDecision:
    """I150: prevent endless source re-search while preserving the existing shortlist."""
    resolution = resolve()
    if contact_evidence_available:
        return SourceBranchDecision(
            active_source="PayanAgent",
            state="REASSESS_WITH_EXPLICIT_PROVIDER_CONTACT_EVIDENCE",
            blockers=resolution.source_gate_blockers,
            next_action="encode_contact_evidence_as_source_fact_then_rerun_I142; do_not_infer beyond the reply",
        )
    if authorized_local_access_evidence_available:
        return SourceBranchDecision(
            active_source="PayanAgent",
            state="REASSESS_AUTHORIZED_LOCAL_ACCESS_EVIDENCE",
            blockers=resolution.source_gate_blockers,
            next_action="record authorized local-access result; provider eligibility still requires explicit policy evidence",
        )
    return SourceBranchDecision(
        active_source="PayanAgent",
        state="WAIT_FOR_POLICY_CONTACT_OR_SEPARATELY_AUTHORIZED_LOCAL_ACCESS",
        blockers=resolution.source_gate_blockers,
        next_action="stop repeated documentation searches; continue independent resource/runtime branch and retain PayanAgent as active source",
    )


def payload() -> dict:
    return {
        "schema": "mining-autonomy/i148-i150-payanagent-geography-resolution/v1",
        "runs": ["I148", "I149", "I150"],
        "geography_resolution": asdict(resolve()),
        "local_access_contract": asdict(local_access_contract()),
        "source_branch": asdict(branch_decision()),
        "production_observation_performed": False,
        "network_access_performed_by_module": False,
        "credentials_used": False,
        "spend_or_value_movement": False,
    }
