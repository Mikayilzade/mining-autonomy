"""I145 reproducible PayanAgent source-evidence checkpoint.

This module encodes only current first-party public documentation facts collected on
2026-08-23. It deliberately omits geography/access eligibility because no explicit
current PayanAgent rule for Azerbaijan/global worker geography was found. Therefore
I142 must remain HOLD rather than treating silence as permission.

No network request is performed here.
"""
from __future__ import annotations

from dataclasses import asdict

from i142_market_source_evidence_gate import SourceFact, assess_source

OBSERVED_DATE = "2026-08-23"
API_DOC = "https://payanagent.com/docs/api"
ROOT_DOC = "https://payanagent.com/"
SELLER_DOC = "https://payanagent.com/docs/seller"
CONCEPTS_DOC = "https://payanagent.com/docs/concepts"


def current_facts() -> tuple[SourceFact, ...]:
    return (
        SourceFact(
            "task_list_read_auth_requirement",
            "none_public_GET_/api/v1/requests",
            API_DOC,
            OBSERVED_DATE,
        ),
        SourceFact(
            "task_detail_read_auth_requirement",
            "none_public_GET_/api/v1/requests/:id",
            API_DOC,
            OBSERVED_DATE,
        ),
        SourceFact(
            "platform_fee_rate",
            "0_currently_marketplace_fee_not_imposed_yet",
            SELLER_DOC,
            OBSERVED_DATE,
        ),
        SourceFact(
            "payout_to_worker_rate",
            "1.0_of_agreed_provider_payment_before_external_chain_or_tax_costs",
            CONCEPTS_DOC,
            OBSERVED_DATE,
        ),
        SourceFact(
            "rate_limit_or_minimum_interval",
            "public_endpoints_30_requests_per_minute_per_ip",
            API_DOC,
            OBSERVED_DATE,
        ),
        SourceFact(
            "automation_permission",
            "explicit_api_first_programmatic_agent_market_no_human_in_loop_required",
            ROOT_DOC,
            OBSERVED_DATE,
        ),
        # geography_access_rule intentionally absent: current first-party docs reviewed
        # do not provide an explicit supported-country/global-access statement.
    )


def checkpoint() -> dict:
    decision = assess_source("PayanAgent", current_facts())
    body = asdict(decision)
    body.update({
        "schema": "mining-autonomy/i145-payanagent-source-checkpoint/v1",
        "run": "I145",
        "observed_date": OBSERVED_DATE,
        "authoritative_sources": [API_DOC, ROOT_DOC, SELLER_DOC, CONCEPTS_DOC],
        "expected_state": "HOLD",
        "expected_remaining_blocker": "missing_required_fact:geography_access_rule",
        "zentience_status": "DEFERRED_SOURCE_EVIDENCE_CONFLICT_OR_GAPS",
        "production_market_endpoint_called": False,
        "credentials_used": False,
        "registration_performed": False,
        "spend_or_value_movement": False,
    })
    return body
