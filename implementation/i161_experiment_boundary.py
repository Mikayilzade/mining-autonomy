#!/usr/bin/env python3
"""I161 fail-closed experiment boundary after I156-I160.

This module does not perform network access, credentials use, CI dispatch, account
creation, infrastructure rental, task acceptance, spend, settlement, or value movement.
It turns the already-established runtime/backend control outcomes into one explicit
readiness boundary and a deterministic next inert evidence packet.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable

from i160_remaining_backend_control_pass import run as i160_run

SCHEMA = "mining-autonomy/i161-experiment-boundary/v1"


@dataclass(frozen=True)
class Boundary:
    boundary_id: str
    state: str
    autonomous_preparation_allowed: tuple[str, ...]
    required_external_fact_or_authorization: str
    production_promotion_allowed: bool = False


def build_boundaries() -> tuple[Boundary, ...]:
    return (
        Boundary(
            "user_pc_measurement",
            "EXTERNAL_FACT_REQUIRED",
            (
                "prepare portable I159 measurement packet",
                "validate packet locally after user-PC measurements exist",
            ),
            "machine-bound hardware/interface/benchmark/availability/energy/tariff/opportunity-cost measurements",
        ),
        Boundary(
            "external_api_materialization",
            "AUTHORIZATION_REQUIRED",
            (
                "collect first-party pricing/policy/rate-limit documentation",
                "prepare benchmark and retry-cost design",
            ),
            "explicit authorization for real credentials and bounded live API measurement",
        ),
        Boundary(
            "future_vps_materialization",
            "SPEND_AUTHORIZATION_REQUIRED",
            (
                "prepare provider/spec/price comparison",
                "prepare fixed-cost allocation and capacity benchmark design",
            ),
            "explicit spend/infrastructure authorization before rental or paid materialization",
        ),
        Boundary(
            "payanagent_provider_geography",
            "NEW_FIRST_PARTY_EVIDENCE_REQUIRED",
            (
                "retain current source packet",
                "accept only genuinely new first-party policy/contact evidence",
            ),
            "first-party Azerbaijan/provider-country eligibility evidence or separately authorized local-access evidence",
        ),
        Boundary(
            "bounded_readonly_observation",
            "EXACT_AUTHORIZATION_REQUIRED",
            (
                "prepare exact one-shot read-only request manifest",
                "keep observation runner disabled",
            ),
            "exact explicit authorization for the bounded production read-only observation",
        ),
    )


def _backend_control_consistent() -> bool:
    rows = {row["backend_id"]: row for row in i160_run()["rows"]}
    return (
        rows.get("subscription_assistant", {}).get("classification") == "SUPPORT_ONLY"
        and rows.get("cheap_external_api", {}).get("classification") == "AUTHORIZATION_GATED_EVIDENCE_PREPARABLE"
        and rows.get("strong_external_api", {}).get("classification") == "AUTHORIZATION_GATED_EVIDENCE_PREPARABLE"
        and rows.get("future_paid_vps", {}).get("classification") == "SPEND_AND_INFRASTRUCTURE_AUTHORIZATION_GATED"
    )


def assess(
    *,
    exact_runtime_pass_blocked: bool = True,
    current_measured_positive_route: bool = False,
    user_pc_measurement_ready: bool = False,
    api_live_measurement_authorized: bool = False,
    vps_spend_authorized: bool = False,
    payanagent_geography_ready: bool = False,
    bounded_observation_authorized: bool = False,
) -> dict:
    boundaries = build_boundaries()
    backend_control_consistent = _backend_control_consistent()

    blockers: list[str] = []
    if not exact_runtime_pass_blocked:
        blockers.append("exact_current_runtime_regression_receipt_absent")
    if not backend_control_consistent:
        blockers.append("i160_backend_control_drift")
    if not current_measured_positive_route:
        blockers.append("current_measured_positive_conservative_execution_route_absent")
    if not user_pc_measurement_ready:
        blockers.append("user_pc_measurement_absent")
    if not api_live_measurement_authorized:
        blockers.append("external_api_live_measurement_authorization_absent")
    if not vps_spend_authorized:
        blockers.append("vps_spend_infrastructure_authorization_absent")
    if not payanagent_geography_ready:
        blockers.append("payanagent_provider_geography_evidence_absent")
    if not bounded_observation_authorized:
        blockers.append("exact_bounded_observation_authorization_absent")

    # A real economic observation is intentionally impossible at this layer.
    ready_for_real_economic_observation = all((
        exact_runtime_pass_blocked,
        backend_control_consistent,
        current_measured_positive_route,
        payanagent_geography_ready,
        bounded_observation_authorized,
    ))

    if current_measured_positive_route:
        next_inert_packet = "source_geography_or_observation_authorization_packet"
    else:
        # The broad control pass shows no external backend can self-materialize now.
        # User-PC measurement is the only zero-new-spend production-resource fact
        # that can materially advance routing without credentials or rental.
        next_inert_packet = "I159_user_pc_measurement_packet"

    return {
        "schema": SCHEMA,
        "run": "I161",
        "state": "FAIL_CLOSED_EXTERNAL_BOUNDARIES" if blockers else "BOUNDARIES_SATISFIED_REVIEW_REQUIRED",
        "exact_runtime_pass_blocked": exact_runtime_pass_blocked,
        "backend_control_consistent": backend_control_consistent,
        "current_measured_positive_route": current_measured_positive_route,
        "boundaries": [asdict(x) for x in boundaries],
        "blockers": blockers,
        "autonomous_preparation_may_continue": True,
        "next_inert_packet": next_inert_packet,
        "ready_for_real_economic_observation": ready_for_real_economic_observation,
        "production_observation_enabled": False,
        "execution_enabled": False,
        "network_enabled": False,
        "credentials_enabled": False,
        "ci_dispatch_enabled": False,
        "paid_infrastructure_enabled": False,
        "task_acceptance_enabled": False,
        "spend_enabled": False,
        "value_movement_enabled": False,
        "control_note": (
            "I156 runtime is materially demonstrated, but runtime evidence cannot substitute for a current measured "
            "positive execution route, provider-geography evidence, or exact observation authorization. I157-I160 "
            "show that remaining external backends require local facts, credentials/live-call authorization, or spend."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(assess(), indent=2, sort_keys=True))
