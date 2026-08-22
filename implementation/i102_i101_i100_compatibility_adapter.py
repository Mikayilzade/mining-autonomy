#!/usr/bin/env python3
"""I102 network-inert I101 -> I100 compatibility adapter and synthetic regressions.

This module performs no DNS, socket, TLS, HTTP, credential, authorization, task acceptance,
submission, payment, spend, or value-moving operation. It creates synthetic fixtures only.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import i098_fresh_execution_evidence_contract as i098
import i100_execution_readiness_manifest as i100
import i101_fresh_real_evidence_route_contract as i101

ROOT = Path(__file__).resolve().parent
PACKET_PATH = ROOT / "I096_FRESH_ONE_SHOT_REVIEW_PACKET.json"


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_packet() -> Mapping[str, Any]:
    value = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("I096 packet must be an object")
    return value


def build_synthetic_evidence(now: datetime) -> dict[str, Any]:
    observed = now - timedelta(seconds=10)
    policy_until = now + timedelta(hours=1)
    transport_until = now + timedelta(seconds=120)
    rebind_until = now + timedelta(seconds=30)
    base = {
        "schema_version": 1,
        "bound_packet_sha256": i101.PACKET_SHA256,
        "bound_scope_sha256": i101.SCOPE_SHA256,
        "hostname": i101.HOST,
    }
    policy = {
        **base,
        "evidence_type": "policy_tos",
        "observed_at": _iso(observed),
        "valid_until": _iso(policy_until),
        "provenance_url": "https://example.invalid/synthetic-policy",
        "source_url": "https://example.invalid/synthetic-policy",
        "source_kind": "official_public_primary_source",
        "content_sha256": "1" * 64,
        "official_source": True,
        "anonymous_read_only_get_permitted": True,
        "automation_prohibited_for_exact_observation": False,
        "credentials_required": False,
        "value_movement_required": False,
    }
    dns = {
        **base,
        "evidence_type": "dns_resolution",
        "observed_at": _iso(observed),
        "valid_until": _iso(transport_until),
        "provenance_url": "https://example.invalid/synthetic-dns",
        "content_sha256": "2" * 64,
        "resolver_mode": "fresh_system_or_authorized_resolver",
        "raw_answer_sha256": "3" * 64,
        "effective_ttl_seconds": 120,
        "public_ip_pins": ["93.184.216.34"],
        "public_addresses": ["93.184.216.34"],
    }
    tls = {
        **base,
        "evidence_type": "tls_transport",
        "observed_at": _iso(now - timedelta(seconds=5)),
        "valid_until": _iso(transport_until),
        "provenance_url": "https://example.invalid/synthetic-tls",
        "content_sha256": "4" * 64,
        "connected_ip": "93.184.216.34",
        "hostname_verified": True,
        "certificate_valid": True,
        "certificate_hostname_valid": True,
        "certificate_time_valid": True,
        "tls_version": "TLSv1.3",
        "peer_certificate_sha256": "5" * 64,
        "certificate_chain_sha256": "6" * 64,
        "handshake_transcript_sha256": "7" * 64,
    }
    rebinding = {
        **base,
        "evidence_type": "anti_rebinding",
        "observed_at": _iso(now - timedelta(seconds=1)),
        "valid_until": _iso(rebind_until),
        "provenance_url": "https://example.invalid/synthetic-rebinding",
        "content_sha256": "8" * 64,
        "public_ip_pins": ["93.184.216.34"],
        "revalidated_public_addresses": ["93.184.216.34"],
        "performed_immediately_before_request": True,
        "revalidation_sha256": "9" * 64,
    }
    components = {
        "policy_tos": policy,
        "dns_resolution": dns,
        "tls_transport": tls,
        "anti_rebinding": rebinding,
    }
    return {
        "schema_version": 1,
        "artifact_type": "i098_fresh_execution_evidence_bundle",
        "synthetic_fixture": True,
        "fixture_origin": "I102 network-inert compatibility fixture",
        "bound_packet_sha256": i101.PACKET_SHA256,
        "bound_scope_sha256": i101.SCOPE_SHA256,
        "method": i101.METHOD,
        "hostname": i101.HOST,
        "path_query": i101.PATH_QUERY,
        "request_count": i101.REQUEST_COUNT,
        "credentials_allowed": False,
        "value_movement_allowed": False,
        "exact_request": {
            "hostname": i101.HOST,
            "path_query": i101.PATH_QUERY,
            "method": i101.METHOD,
            "request_count": i101.REQUEST_COUNT,
        },
        "components": components,
        **components,
        "component_sha256": {name: i098.canonical_sha256(value) for name, value in components.items()},
        "valid_until": _iso(rebind_until),
        "pinned_public_addresses": ["93.184.216.34"],
        "anti_rebinding_revalidation_required": True,
        "network_capable": False,
        "execution_token": False,
    }


def build_synthetic_route(now: datetime) -> dict[str, Any]:
    costs = {
        "incremental_compute_usd": 0.0004,
        "energy_usd": 0.0002,
        "external_api_model_usd": 0.0,
        "retry_failure_usd": 0.0002,
        "human_maintenance_usd": 0.0005,
        "platform_marketplace_fees_usd": 0.0,
        "gas_withdrawal_conversion_usd": 0.0,
        "opportunity_cost_usd": 0.0003,
    }
    total = sum(costs.values())
    expected = 0.01
    return {
        "schema_version": 1,
        "artifact_type": "i101_resource_route_materialization",
        "synthetic_fixture": True,
        "bound_packet_sha256": i101.PACKET_SHA256,
        "bound_scope_sha256": i101.SCOPE_SHA256,
        "backend_id": "pure_python_local",
        "current_materialized_resource": True,
        "policy_eligible": True,
        "capacity_available": True,
        "conservative_margin_positive": True,
        "observed_at": _iso(now - timedelta(seconds=10)),
        "valid_until": _iso(now + timedelta(minutes=5)),
        "capacity": {
            "quota_remaining": 1000,
            "parallelism": 1,
            "rate_limit_per_minute": 30,
            "latency_ms_p95": 25,
            "reliability_probability": 0.99,
            "quality_probability": 0.999,
        },
        "economics": {
            "fixed_sunk_cost_usd_period": 20.0,
            "marginal_observation_costs_usd": costs,
            "marginal_observation_cost_usd_total": total,
            "acceptance_probability": 1.0,
            "dispute_or_nonpayment_probability": 0.0,
            "conservative_expected_value_usd": expected,
            "conservative_margin_usd": expected - total,
            "paid_task_execution_cost_reused_for_observation": False,
        },
        "programmatic_api_assumed": False,
        "separate_user_authorization_for_paid_infrastructure": False,
        "observation_economics_only": True,
        "paid_task_execution_economics_proven": False,
    }


def _shape_only_i101_evidence_result(fixture: Mapping[str, Any], now: datetime) -> dict[str, Any]:
    candidate = copy.deepcopy(dict(fixture))
    candidate["synthetic_fixture"] = False
    return i101.validate_evidence_plan_input(candidate, now)


def _shape_only_i101_route_result(fixture: Mapping[str, Any], now: datetime) -> dict[str, Any]:
    candidate = copy.deepcopy(dict(fixture))
    candidate["synthetic_fixture"] = False
    return i101.validate_route(candidate, now)


def project_to_i100(evidence: Mapping[str, Any], route: Mapping[str, Any], now: datetime) -> dict[str, Any]:
    """Identity-project the fixtures into I100 without stripping synthetic provenance."""
    return i100.build_manifest(
        packet=_load_packet(),
        fresh_real_evidence=copy.deepcopy(dict(evidence)),
        resource_route=copy.deepcopy(dict(route)),
        now=now,
    )


def _rehash_bundle(bundle: dict[str, Any]) -> None:
    names = ("policy_tos", "dns_resolution", "tls_transport", "anti_rebinding")
    bundle["component_sha256"] = {name: i098.canonical_sha256(bundle[name]) for name in names}
    bundle["components"] = {name: bundle[name] for name in names}


def run_regressions(now: datetime) -> dict[str, Any]:
    evidence = build_synthetic_evidence(now)
    route = build_synthetic_route(now)

    evidence_shape = _shape_only_i101_evidence_result(evidence, now)
    route_shape = _shape_only_i101_route_result(route, now)
    i098_shape = i098.validate_bundle(evidence, now=now)
    manifest = project_to_i100(evidence, route, now)

    private_pin = copy.deepcopy(evidence)
    private_pin["dns_resolution"]["public_ip_pins"] = ["127.0.0.1"]
    private_pin["dns_resolution"]["public_addresses"] = ["127.0.0.1"]
    private_pin["tls_transport"]["connected_ip"] = "127.0.0.1"
    private_pin["anti_rebinding"]["public_ip_pins"] = ["127.0.0.1"]
    private_pin["anti_rebinding"]["revalidated_public_addresses"] = ["127.0.0.1"]
    private_pin["pinned_public_addresses"] = ["127.0.0.1"]
    _rehash_bundle(private_pin)

    stale_route = copy.deepcopy(route)
    stale_route["observed_at"] = _iso(now - timedelta(hours=2))
    stale_route["valid_until"] = _iso(now - timedelta(hours=1))

    subscription_free_api = copy.deepcopy(route)
    subscription_free_api["backend_id"] = "chatgpt_codex_subscription_assisted"
    subscription_free_api["programmatic_api_assumed"] = True

    missing_cost_results: dict[str, bool] = {}
    for field in ("energy_usd", "retry_failure_usd", "opportunity_cost_usd"):
        candidate = copy.deepcopy(route)
        del candidate["economics"]["marginal_observation_costs_usd"][field]
        missing_cost_results[field] = not _shape_only_i101_route_result(candidate, now)["valid"]

    nonpositive_margin = copy.deepcopy(route)
    total = nonpositive_margin["economics"]["marginal_observation_cost_usd_total"]
    nonpositive_margin["economics"]["conservative_expected_value_usd"] = total
    nonpositive_margin["economics"]["conservative_margin_usd"] = 0.0
    nonpositive_margin["conservative_margin_positive"] = False

    conflated_cost = copy.deepcopy(route)
    conflated_cost["economics"]["paid_task_execution_cost_reused_for_observation"] = True

    result = {
        "schema_version": 1,
        "artifact_type": "i102_i101_i100_compatibility_result",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "synthetic_fixture": True,
        "positive_checks": {
            "i101_evidence_shape_valid_when_synthetic_marker_is_ignored_for_shape_test_only": evidence_shape["valid"],
            "i101_route_shape_valid_when_synthetic_marker_is_ignored_for_shape_test_only": route_shape["valid"],
            "i098_bundle_contract_valid": i098_shape["contract_valid"],
            "i100_receives_identity_projection": manifest["readiness_inputs"]["fresh_real_execution_evidence_present"],
            "i100_detects_synthetic_evidence": not manifest["readiness_inputs"]["fresh_real_execution_evidence_not_synthetic"],
            "i100_remains_blocked_without_real_evidence_and_authorization": manifest["result"] == "BLOCKED",
            "i100_ready_for_network_invocation_is_false": manifest["ready_for_network_invocation"] is False,
        },
        "negative_checks": {
            "non_public_dns_pin_rejected": not _shape_only_i101_evidence_result(private_pin, now)["valid"],
            "stale_route_capacity_rejected": not _shape_only_i101_route_result(stale_route, now)["valid"],
            "subscription_free_programmatic_api_assumption_rejected": not _shape_only_i101_route_result(subscription_free_api, now)["valid"],
            "missing_required_cost_fields_rejected": all(missing_cost_results.values()),
            "missing_cost_field_details": missing_cost_results,
            "nonpositive_conservative_margin_rejected": not _shape_only_i101_route_result(nonpositive_margin, now)["valid"],
            "observation_paid_task_cost_conflation_rejected": not _shape_only_i101_route_result(conflated_cost, now)["valid"],
        },
        "projection": {
            "fresh_real_evidence_synthetic_marker_preserved": evidence.get("synthetic_fixture") is True,
            "resource_route_synthetic_marker_preserved": route.get("synthetic_fixture") is True,
            "route_may_be_structurally_complete_but_cannot_overcome_synthetic_evidence_or_missing_authorization": True,
            "authorization_supplied": False,
            "production_get_performed": False,
        },
        "result": "PASS",
    }
    all_positive = all(result["positive_checks"].values())
    all_negative = all(v for k, v in result["negative_checks"].items() if k != "missing_cost_field_details")
    if not (all_positive and all_negative):
        result["result"] = "FAIL"
    return result


def _self_test() -> None:
    now = datetime(2026, 8, 22, 20, 30, tzinfo=timezone.utc)
    result = run_regressions(now)
    assert result["result"] == "PASS", result
    assert result["network_capable"] is False
    assert result["projection"]["production_get_performed"] is False
    print("I102 self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    now = datetime.now(timezone.utc)
    result = run_regressions(now)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
