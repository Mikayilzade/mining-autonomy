#!/usr/bin/env python3
"""I167 fail-closed bridge from real I166 owned-PC evidence to Router-shaped facts.

This module performs no measurements and no external actions. It only accepts an
already-complete I166/I165/I162/I159 chain and derives the owned-PC resource fields
that can be computed without inventing task/market economics. Unknown task-specific
maintenance, platform fees, acceptance/dispute/nonpayment risk and payout remain
outside this bridge and therefore block any claim of a real economic route.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA = "mining-autonomy/i167-owned-pc-router-bridge/v1"
FORBIDDEN_MARKERS = ("test-fixture", "fixture", "synthetic", "placeholder", "dummy", "mock", "example")


@dataclass(frozen=True)
class BridgeResult:
    state: str
    errors: tuple[str, ...]
    backend_id: str
    router_backend_patch: dict[str, Any]
    backend_evidence_candidate: dict[str, Any]
    still_required_for_economic_test: tuple[str, ...]
    source_digest: str | None
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _digest(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def _nonproduction_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return True
    low = value.lower()
    return any(marker in low for marker in FORBIDDEN_MARKERS)


def build_bridge(i166_result: Mapping[str, Any]) -> BridgeResult:
    errors: list[str] = []
    gate = i166_result.get("gate")
    if not isinstance(gate, Mapping) or gate.get("state") != "REAL_EXTERNAL_EVIDENCE_ACCEPTED":
        errors.append("i166_real_external_evidence_not_accepted")
    if isinstance(gate, Mapping) and gate.get("ownership_confirmation_supplied") is not True:
        errors.append("user_owned_pc_not_confirmed")

    i165 = i166_result.get("i165_result")
    if not isinstance(i165, Mapping) or i165.get("state") != "USER_PC_MATERIALIZED":
        errors.append("i165_user_pc_not_materialized")
        i165 = {}
    packet = i165.get("i162_packet") if isinstance(i165, Mapping) else None
    if not isinstance(packet, Mapping) or packet.get("state") != "USER_PC_PACKET_COMPLETE":
        errors.append("i162_packet_not_complete")
        packet = {}
    evaluation = packet.get("i159_evaluation") if isinstance(packet, Mapping) else None
    if not isinstance(evaluation, Mapping) or evaluation.get("production_evidence_ready") is not True:
        errors.append("i159_production_evidence_not_ready")

    explicit = packet.get("explicit_measurements") if isinstance(packet, Mapping) else None
    if not isinstance(explicit, Mapping):
        errors.append("explicit_measurements_missing")
        explicit = {}

    for name in ("availability_source_ref", "energy_source_ref", "tariff_source_ref", "opportunity_cost_source_ref"):
        if _nonproduction_ref(explicit.get(name)):
            errors.append(f"nonproduction_or_missing_provenance:{name}")

    required_numeric = (
        "latency_seconds", "reliability_probability", "quality_acceptance_probability", "max_parallelism",
        "measured_available_hours_per_day", "tariff_usd_per_kwh", "opportunity_cost_usd_per_hour",
    )
    for name in required_numeric:
        if explicit.get(name) is None:
            errors.append(f"missing_measurement:{name}")
    energy_kwh = packet.get("derived_energy_kwh_per_task") if isinstance(packet, Mapping) else None
    if energy_kwh is None:
        errors.append("derived_energy_kwh_per_task_missing")

    patch: dict[str, Any] = {}
    evidence: dict[str, Any] = {}
    if not errors:
        latency = float(explicit["latency_seconds"])
        reliability = float(explicit["reliability_probability"])
        quality = float(explicit["quality_acceptance_probability"])
        parallelism = int(explicit["max_parallelism"])
        available_hours = float(explicit["measured_available_hours_per_day"])
        tariff = float(explicit["tariff_usd_per_kwh"])
        opportunity_hour = float(explicit["opportunity_cost_usd_per_hour"])
        energy = float(energy_kwh)
        if latency < 0 or not 0 <= reliability <= 1 or not 0 <= quality <= 1 or parallelism < 1 or not 0 <= available_hours <= 24 or tariff < 0 or opportunity_hour < 0 or energy < 0:
            errors.append("invalid_measurement_range")
        else:
            electricity = energy * tariff
            opportunity_task = opportunity_hour * latency / 3600.0
            patch = {
                "backend_id": "owned_pc",
                "currently_available": available_hours > 0,
                "electricity_per_task_usd": round(electricity, 12),
                "opportunity_cost_per_task_usd": round(opportunity_task, 12),
                "latency_seconds": latency,
                "reliability_probability": reliability,
                "quality_probability": quality,
                "max_parallelism": parallelism,
                "notes": "I167 patch derived only from accepted I166 real owned-PC evidence; task/market economics are not inferred.",
            }
            evidence = {
                "backend_id": "owned_pc",
                "provenance_class": "i166_real_owned_pc_measurement_candidate",
                "current_reproducible": False,
                "non_synthetic": True,
                "capacity_verified": True,
                "policy_evidence_current": False,
                "credentials_authorized": False,
                "spend_authorized": False,
                "infrastructure_authorized": False,
                "evidence_note": "I166-accepted local owned-PC measurement candidate; must pass I050/I066 attestation before promotion to I123 production evidence.",
            }

    errors = sorted(set(errors))
    source_digest = _digest(i166_result) if not errors else None
    remaining = (
        "i050_i066_resource_attestation_binding",
        "real_task_payout_and_acceptance_criteria",
        "platform_marketplace_and_payment_fees",
        "dispute_and_nonpayment_probability",
        "acceptance_probability",
        "task_specific_retry_failure_cost_or_conservative_bound",
        "task_specific_human_maintenance_time_and_value_or_zero_with_evidence",
        "market_policy_tos_and_geography_evidence",
        "separate_authorization_before_read_only_production_observation",
        "separate_authorization_before_any_value_moving_action",
    )
    return BridgeResult(
        state="ROUTER_RESOURCE_FACTS_READY" if not errors else "PASS_BLOCKED",
        errors=tuple(errors),
        backend_id="owned_pc",
        router_backend_patch=patch if not errors else {},
        backend_evidence_candidate=evidence if not errors else {},
        still_required_for_economic_test=remaining,
        source_digest=source_digest,
    )


def payload(result: BridgeResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({"schema": SCHEMA, "run": "I167"})
    return body
