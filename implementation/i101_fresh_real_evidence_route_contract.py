#!/usr/bin/env python3
"""I101 network-inert fresh-real-evidence acquisition + route-materialization contract.

Defines and validates externally acquired evidence inputs required before the exact I096
one-shot observation can advance. This module performs no DNS, sockets, TLS, HTTP,
credential use, authorization creation, task acceptance, submission, spend or value movement.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

PACKET_SHA256 = "0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56"
SCOPE_SHA256 = "df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e"
HOST = "payanagent.com"
PATH_QUERY = "/api/v1/requests?status=open&limit=1"
METHOD = "GET"
REQUEST_COUNT = 1
ALLOWED_BACKENDS = {
    "pure_python_local",
    "local_cpu_gpu_model",
    "chatgpt_codex_subscription_assisted",
    "cheap_external_llm_api",
    "strong_external_llm_api",
    "free_ci_cloud_tier",
    "owned_pc",
    "future_vps_server",
}
REQUIRED_ROUTE_COST_FIELDS = {
    "incremental_compute_usd",
    "energy_usd",
    "external_api_model_usd",
    "retry_failure_usd",
    "human_maintenance_usd",
    "platform_marketplace_fees_usd",
    "gas_withdrawal_conversion_usd",
    "opportunity_cost_usd",
}


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _bound(obj: Mapping[str, Any]) -> bool:
    return obj.get("bound_packet_sha256") == PACKET_SHA256 and obj.get("bound_scope_sha256") == SCOPE_SHA256


def _fresh(obj: Mapping[str, Any], now: datetime) -> bool:
    observed = _parse_ts(obj.get("observed_at"))
    valid_until = _parse_ts(obj.get("valid_until"))
    return observed is not None and valid_until is not None and observed <= now <= valid_until


def _public_ip(value: Any) -> bool:
    try:
        ip = ipaddress.ip_address(str(value))
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified or ip.is_reserved)


def validate_evidence_plan_input(bundle: Mapping[str, Any], now: datetime | None = None) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    errors: list[str] = []
    if bundle.get("synthetic_fixture") is True:
        errors.append("fresh-real evidence must not be synthetic")
    if not _bound(bundle):
        errors.append("bundle packet/scope binding mismatch")
    exact = bundle.get("exact_request") if isinstance(bundle.get("exact_request"), Mapping) else {}
    if (exact.get("hostname"), exact.get("path_query"), exact.get("method"), exact.get("request_count")) != (HOST, PATH_QUERY, METHOD, REQUEST_COUNT):
        errors.append("exact request drift")

    components = bundle.get("components") if isinstance(bundle.get("components"), Mapping) else {}
    for name in ("policy_tos", "dns_resolution", "tls_transport", "anti_rebinding"):
        comp = components.get(name)
        if not isinstance(comp, Mapping):
            errors.append(f"missing component: {name}")
            continue
        if not _bound(comp):
            errors.append(f"{name} binding mismatch")
        if not _fresh(comp, current):
            errors.append(f"{name} not fresh")
        if not isinstance(comp.get("provenance_url"), str) or not comp.get("provenance_url"):
            errors.append(f"{name} provenance_url absent")
        if not isinstance(comp.get("content_sha256"), str) or len(comp.get("content_sha256", "")) != 64:
            errors.append(f"{name} content_sha256 invalid")

    policy = components.get("policy_tos") if isinstance(components.get("policy_tos"), Mapping) else {}
    if policy.get("official_source") is not True or policy.get("anonymous_read_only_get_permitted") is not True:
        errors.append("official policy evidence does not affirm anonymous read-only GET eligibility")

    dns = components.get("dns_resolution") if isinstance(components.get("dns_resolution"), Mapping) else {}
    pins = dns.get("public_ip_pins") if isinstance(dns.get("public_ip_pins"), list) else []
    if not pins or not all(_public_ip(x) for x in pins):
        errors.append("DNS pins missing or non-public")

    tls = components.get("tls_transport") if isinstance(components.get("tls_transport"), Mapping) else {}
    if tls.get("connected_ip") not in pins or tls.get("hostname_verified") is not True or tls.get("certificate_valid") is not True:
        errors.append("TLS-to-pin proof invalid")

    rebinding = components.get("anti_rebinding") if isinstance(components.get("anti_rebinding"), Mapping) else {}
    rebound = rebinding.get("public_ip_pins") if isinstance(rebinding.get("public_ip_pins"), list) else []
    if sorted(map(str, rebound)) != sorted(map(str, pins)):
        errors.append("anti-rebinding pin set changed")

    return {"valid": not errors, "errors": errors}


def validate_route(route: Mapping[str, Any], now: datetime | None = None) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    errors: list[str] = []
    if not _bound(route):
        errors.append("route packet/scope binding mismatch")
    if route.get("synthetic_fixture") is True:
        errors.append("production route must be current/materialized, not synthetic")
    backend = route.get("backend_id")
    if backend not in ALLOWED_BACKENDS:
        errors.append("backend_id outside modeled router backends")
    if route.get("current_materialized_resource") is not True:
        errors.append("resource is not currently materialized")
    if route.get("policy_eligible") is not True:
        errors.append("route policy eligibility absent")
    if route.get("capacity_available") is not True:
        errors.append("route capacity unavailable")
    if not _fresh(route, current):
        errors.append("route evidence not fresh")
    if backend == "future_vps_server" and route.get("separate_user_authorization_for_paid_infrastructure") is not True:
        errors.append("future VPS route lacks separate paid-infrastructure authorization")
    if backend == "chatgpt_codex_subscription_assisted" and route.get("programmatic_api_assumed") is not False:
        errors.append("subscription backend must not assume programmatic API access")

    capacity = route.get("capacity") if isinstance(route.get("capacity"), Mapping) else {}
    for field in ("quota_remaining", "parallelism", "rate_limit_per_minute", "latency_ms_p95", "reliability_probability", "quality_probability"):
        if field not in capacity:
            errors.append(f"capacity.{field} absent")
    for field in ("reliability_probability", "quality_probability"):
        value = capacity.get(field)
        if not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            errors.append(f"capacity.{field} invalid")

    economics = route.get("economics") if isinstance(route.get("economics"), Mapping) else {}
    if not isinstance(economics.get("fixed_sunk_cost_usd_period"), (int, float)):
        errors.append("fixed/sunk cost treatment absent")
    costs = economics.get("marginal_observation_costs_usd") if isinstance(economics.get("marginal_observation_costs_usd"), Mapping) else {}
    missing = REQUIRED_ROUTE_COST_FIELDS - set(costs)
    if missing:
        errors.append("missing marginal cost fields: " + ",".join(sorted(missing)))
    if any(not isinstance(costs.get(k), (int, float)) or costs.get(k, 0) < 0 for k in REQUIRED_ROUTE_COST_FIELDS):
        errors.append("marginal cost values invalid")
    marginal_total = sum(float(costs.get(k, 0.0)) for k in REQUIRED_ROUTE_COST_FIELDS)
    declared_total = economics.get("marginal_observation_cost_usd_total")
    if not isinstance(declared_total, (int, float)) or abs(float(declared_total) - marginal_total) > 1e-9:
        errors.append("marginal observation cost total mismatch")

    expected = economics.get("conservative_expected_value_usd")
    acceptance = economics.get("acceptance_probability")
    dispute = economics.get("dispute_or_nonpayment_probability")
    if not isinstance(expected, (int, float)):
        errors.append("conservative expected value absent")
    if not isinstance(acceptance, (int, float)) or not 0 <= float(acceptance) <= 1:
        errors.append("acceptance probability invalid")
    if not isinstance(dispute, (int, float)) or not 0 <= float(dispute) <= 1:
        errors.append("dispute/non-payment probability invalid")
    margin = float(expected or 0.0) - marginal_total
    declared_margin = economics.get("conservative_margin_usd")
    if not isinstance(declared_margin, (int, float)) or abs(float(declared_margin) - margin) > 1e-9:
        errors.append("conservative margin mismatch")
    if margin <= 0 or route.get("conservative_margin_positive") is not True:
        errors.append("conservative margin is not positive")
    if economics.get("paid_task_execution_cost_reused_for_observation") is not False:
        errors.append("observation cost must remain separate from later paid-task execution cost")

    return {"valid": not errors, "errors": errors, "computed_marginal_observation_cost_usd": marginal_total, "computed_conservative_margin_usd": margin}


def build_readiness_input(evidence: Mapping[str, Any] | None, route: Mapping[str, Any] | None, now: datetime | None = None) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    evidence_result = validate_evidence_plan_input(evidence, current) if evidence is not None else {"valid": False, "errors": ["fresh real evidence absent"]}
    route_result = validate_route(route, current) if route is not None else {"valid": False, "errors": ["current materialized route absent"]}
    return {
        "schema_version": 1,
        "mode": "i101_network_inert_external_input_contract",
        "bound_packet_sha256": PACKET_SHA256,
        "bound_scope_sha256": SCOPE_SHA256,
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "fresh_real_evidence_valid": evidence_result["valid"],
        "current_resource_route_valid": route_result["valid"],
        "exact_authorization_still_required_separately": True,
        "production_get_performed": False,
        "ready_inputs_for_i100": evidence_result["valid"] and route_result["valid"],
        "result": "INPUTS_READY_BUT_AUTHORIZATION_STILL_REQUIRED" if evidence_result["valid"] and route_result["valid"] else "BLOCKED",
        "diagnostics": {"evidence": evidence_result, "route": route_result},
    }


def _self_test() -> None:
    now = datetime(2026, 8, 22, 19, 0, tzinfo=timezone.utc)
    result = build_readiness_input(None, None, now)
    assert result["result"] == "BLOCKED"
    assert result["network_capable"] is False
    assert result["exact_authorization_still_required_separately"] is True
    print("I101 self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence")
    parser.add_argument("--route")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test(); return 0
    evidence = json.loads(Path(args.evidence).read_text()) if args.evidence else None
    route = json.loads(Path(args.route).read_text()) if args.route else None
    result = build_readiness_input(evidence, route)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
