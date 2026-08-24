#!/usr/bin/env python3
"""I160 fail-closed control pass for remaining Resource/Execution Router backends.

Classifies existing backend families without credentials, API calls, account creation,
CI dispatch, infrastructure rental, spend, task action, or value movement.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from typing import Optional
from resource_router import default_backend_families

SCHEMA = "mining-autonomy/i160-remaining-backend-control-pass/v1"
TARGETS = ("subscription_assistant", "cheap_external_api", "strong_external_api", "future_paid_vps")

@dataclass(frozen=True)
class ControlRow:
    backend_id: str
    classification: str
    autonomous_programmatic_execution: bool
    evidence_preparable_without_credentials_or_spend: bool
    credentials_required_for_live_execution: bool
    new_spend_required_for_live_execution: bool
    infrastructure_authorization_required: bool
    fixed_cost_semantics: str
    marginal_cost_semantics: str
    evidence_required_before_economic_routing: tuple[str, ...]
    current_blockers: tuple[str, ...]


def classify(backend_id: str) -> ControlRow:
    b = next(x for x in default_backend_families() if x.backend_id == backend_id)
    if backend_id == "subscription_assistant":
        return ControlRow(
            backend_id, "SUPPORT_ONLY", False, True, False, False, False,
            "existing subscription is fixed/sunk support capacity; never charge the full monthly price to every task",
            "marginal task cost is not assumed zero: finite quota/session capacity, latency and human-maintenance opportunity cost remain unmeasured",
            ("actual product quota/capacity if exposed", "latency/reliability/quality for support workflow", "human maintenance/opportunity cost"),
            ("no proven autonomous programmatic execution interface", "must not reinterpret ChatGPT/Codex subscription as a free API"),
        )
    if backend_id in {"cheap_external_api", "strong_external_api"}:
        return ControlRow(
            backend_id, "AUTHORIZATION_GATED_EVIDENCE_PREPARABLE", True, True, True, False, False,
            "no monthly fixed cost may be assumed; any committed tier/subscription must be separately evidenced",
            "real token/request/model pricing plus retries, latency, quality failures and quota opportunity cost must replace synthetic reference values",
            ("current first-party pricing", "current API policy/ToS", "rate limits/quota semantics", "quality acceptance benchmark design", "retry/failure cost model"),
            ("real credentials absent and not authorized", "no current measured reproducible vendor-specific capacity/quality evidence", "no live API call authorized"),
        )
    if backend_id == "future_paid_vps":
        return ControlRow(
            backend_id, "SPEND_AND_INFRASTRUCTURE_AUTHORIZATION_GATED", True, True, False, True, True,
            "monthly rental is fixed committed cost and needs an explicit task-volume allocation basis; it is not marginally free after rental for economic comparison",
            "per-task marginal cost still includes workload energy semantics if separately billed, bandwidth/storage/API costs, retries, maintenance and opportunity cost",
            ("current provider price/spec plan", "capacity/latency/reliability benchmark design", "allocation basis", "bandwidth/storage limits", "maintenance/opportunity cost"),
            ("rental/spend not authorized", "no paid infrastructure exists", "current measured capacity/quality evidence absent"),
        )
    raise ValueError(backend_id)


def run() -> dict:
    rows = tuple(classify(x) for x in TARGETS)
    return {
        "schema": SCHEMA, "run": "I160", "state": "AUTONOMOUS_EXTERNAL_BACKEND_BOUNDARY_REACHED",
        "rows": [asdict(x) for x in rows],
        "production_route_created": False, "network_enabled": False, "credentials_used": False,
        "accounts_created": False, "api_calls_performed": False, "ci_dispatched": False,
        "paid_infrastructure_created": False, "spend_performed": False, "task_action_performed": False,
        "value_movement_enabled": False,
        "control_conclusion": (
            "subscription_assistant remains support-only; external APIs require credentials before measured live materialization; "
            "future VPS requires separate spend/infrastructure authorization. Planning/evidence contracts may advance, but no remaining external backend can become a measured production route autonomously from the current boundary."
        ),
        "next_gate": (
            "Advance I138/readiness control using these fail-closed backend classifications. Do not weaken PayanAgent geography/access or exact bounded-observation authorization gates; do not reopen discovery."
        ),
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
