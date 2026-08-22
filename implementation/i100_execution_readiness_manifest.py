#!/usr/bin/env python3
"""I100 network-inert execution-readiness manifest for the exact I096 one-shot target.

This module is deliberately incapable of DNS, sockets, TLS, HTTP, credential use,
authorization creation, task acceptance, submission, payment, or value movement.
It only inspects local JSON/contract artifacts and produces fail-closed booleans.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import i097_offline_packet_verifier as i097
import i098_fresh_execution_evidence_contract as i098
import i099_synthetic_evidence_sequencer as i099

ROOT = Path(__file__).resolve().parent
PACKET_PATH = ROOT / "I096_FRESH_ONE_SHOT_REVIEW_PACKET.json"
I098_CONTRACT_PATH = ROOT / "I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json"


def _load(path: Path | None) -> Mapping[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _bool(value: Any) -> bool:
    return value is True


def _resource_route_checks(resource_route: Mapping[str, Any] | None) -> dict[str, bool]:
    """Fail closed unless a later current materialized route explicitly satisfies all gates.

    I100 does not create or infer a live route. The dry-run/local deterministic verifier
    itself is permitted, but that is not the same as proving a production observation
    backend is currently materialized and eligible.
    """
    if resource_route is None:
        return {
            "router_chain_declared_present": True,
            "current_materialized_route_supplied": False,
            "route_policy_eligible": False,
            "route_capacity_available": False,
            "route_conservative_margin_positive": False,
            "resource_route_eligible": False,
        }
    policy = _bool(resource_route.get("policy_eligible"))
    capacity = _bool(resource_route.get("capacity_available"))
    margin = _bool(resource_route.get("conservative_margin_positive"))
    materialized = _bool(resource_route.get("current_materialized_resource"))
    return {
        "router_chain_declared_present": True,
        "current_materialized_route_supplied": materialized,
        "route_policy_eligible": policy,
        "route_capacity_available": capacity,
        "route_conservative_margin_positive": margin,
        "resource_route_eligible": materialized and policy and capacity and margin,
    }


def build_manifest(
    *,
    packet: Mapping[str, Any],
    authorization: Mapping[str, Any] | None = None,
    fresh_real_evidence: Mapping[str, Any] | None = None,
    resource_route: Mapping[str, Any] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)

    packet_errors = i097.verify_packet(packet)
    packet_integrity = not packet_errors
    scope = packet.get("exact_scope") if isinstance(packet.get("exact_scope"), Mapping) else {}
    scope_integrity = (
        packet_integrity
        and packet.get("hostname") == i097.EXPECTED_HOST
        and packet.get("path_query") == i097.EXPECTED_PATH_QUERY
        and scope.get("method") == "GET"
        and scope.get("request_count") == 1
        and scope.get("https_path_query") == i097.EXPECTED_PATH_QUERY
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
    )

    # Presence of the code-level sequencing contract is a local implementation fact.
    sequencing_contract_present = tuple(i099.ORDER) == (
        "policy_tos", "dns_resolution", "tls_transport", "anti_rebinding"
    )

    authorization_errors = i097.verify_authorization(authorization, now=current)
    explicit_exact_authorization_present = not authorization_errors

    fresh_real_evidence_present = fresh_real_evidence is not None
    fresh_real_evidence_is_synthetic = bool(
        fresh_real_evidence and fresh_real_evidence.get("synthetic_fixture") is True
    )
    evidence_validation = (
        i098.validate_bundle(fresh_real_evidence, now=current)
        if fresh_real_evidence is not None
        else {"contract_valid": False, "errors": ["fresh real execution evidence absent"]}
    )
    fresh_real_evidence_valid = (
        fresh_real_evidence_present
        and not fresh_real_evidence_is_synthetic
        and evidence_validation.get("contract_valid") is True
    )

    request_count_boundary = scope.get("request_count") == 1 and packet.get("exact_scope_sha256") == i097.EXPECTED_SCOPE_SHA256
    credentials_prohibited = scope.get("credentials_allowed") is False and packet.get("safety", {}).get("credentials_allowed") is False
    value_movement_prohibited = packet.get("safety", {}).get("value_movement_enabled") is False
    task_acceptance_prohibited = packet.get("safety", {}).get("task_acceptance_enabled") is False
    submission_prohibited = packet.get("safety", {}).get("submission_enabled") is False

    route = _resource_route_checks(resource_route)

    readiness_inputs = {
        "exact_packet_integrity": packet_integrity,
        "exact_scope_integrity": scope_integrity,
        "synthetic_sequencing_contract_present": sequencing_contract_present,
        "fresh_real_execution_evidence_present": fresh_real_evidence_present,
        "fresh_real_execution_evidence_not_synthetic": fresh_real_evidence_present and not fresh_real_evidence_is_synthetic,
        "fresh_real_execution_evidence_valid": fresh_real_evidence_valid,
        "explicit_exact_authorization_present": explicit_exact_authorization_present,
        "request_count_boundary_exactly_one": request_count_boundary,
        "credentials_prohibited": credentials_prohibited,
        "value_movement_prohibited": value_movement_prohibited,
        "task_acceptance_prohibited": task_acceptance_prohibited,
        "submission_prohibited": submission_prohibited,
        **route,
    }

    required_for_later_network_invocation = (
        "exact_packet_integrity",
        "exact_scope_integrity",
        "synthetic_sequencing_contract_present",
        "fresh_real_execution_evidence_not_synthetic",
        "fresh_real_execution_evidence_valid",
        "explicit_exact_authorization_present",
        "request_count_boundary_exactly_one",
        "credentials_prohibited",
        "value_movement_prohibited",
        "task_acceptance_prohibited",
        "submission_prohibited",
        "resource_route_eligible",
    )
    all_prerequisites_satisfied = all(readiness_inputs[name] for name in required_for_later_network_invocation)

    blockers = [name for name in required_for_later_network_invocation if not readiness_inputs[name]]
    return {
        "schema_version": 1,
        "mode": "i100_network_inert_execution_readiness_manifest",
        "candidate": packet.get("candidate"),
        "bound_packet_sha256": i097.EXPECTED_PACKET_SHA256,
        "bound_scope_sha256": i097.EXPECTED_SCOPE_SHA256,
        "exact_request_target": i097.EXPECTED_TARGET,
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "transport_implemented_here": False,
        "readiness_inputs": readiness_inputs,
        "required_for_later_network_invocation": list(required_for_later_network_invocation),
        "remaining_blockers": blockers,
        "all_prerequisites_satisfied": all_prerequisites_satisfied,
        "ready_for_network_invocation": False,
        "result": "READY_INPUTS_ONLY_BUT_NO_EXECUTION_TOKEN" if all_prerequisites_satisfied else "BLOCKED",
        "notes": [
            "I100 can report readiness only; it cannot perform DNS/TLS/HTTP or create authorization.",
            "Synthetic I099 evidence never satisfies the fresh-real-evidence gate.",
            "Resource routing never widens upstream policy or authorization eligibility.",
            "Even all-green inputs require the existing later single-use invocation/executor lineage; this manifest is never an execution token.",
        ],
        "diagnostics": {
            "packet_errors": packet_errors,
            "authorization_errors": authorization_errors,
            "execution_evidence_errors": list(evidence_validation.get("errors", [])),
        },
    }


def _self_test() -> None:
    packet = _load(PACKET_PATH)
    assert packet is not None
    now = datetime(2026, 8, 22, 18, 30, tzinfo=timezone.utc)
    blocked = build_manifest(packet=packet, now=now)
    assert blocked["result"] == "BLOCKED"
    assert blocked["readiness_inputs"]["exact_packet_integrity"] is True
    assert blocked["readiness_inputs"]["exact_scope_integrity"] is True
    assert blocked["readiness_inputs"]["synthetic_sequencing_contract_present"] is True
    assert blocked["readiness_inputs"]["fresh_real_execution_evidence_present"] is False
    assert blocked["readiness_inputs"]["explicit_exact_authorization_present"] is False
    assert blocked["readiness_inputs"]["resource_route_eligible"] is False
    assert blocked["ready_for_network_invocation"] is False

    _, synthetic_bundle, _ = i099.build_valid_synthetic_chain(now)
    synthetic = build_manifest(packet=packet, fresh_real_evidence=synthetic_bundle, now=now)
    assert synthetic["readiness_inputs"]["fresh_real_execution_evidence_present"] is True
    assert synthetic["readiness_inputs"]["fresh_real_execution_evidence_not_synthetic"] is False
    assert synthetic["readiness_inputs"]["fresh_real_execution_evidence_valid"] is False
    assert synthetic["result"] == "BLOCKED"

    drifted = json.loads(json.dumps(packet))
    drifted["path_query"] = "/api/v1/requests?status=open&limit=2"
    assert build_manifest(packet=drifted, now=now)["readiness_inputs"]["exact_packet_integrity"] is False
    print("I100 self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization")
    parser.add_argument("--fresh-real-evidence")
    parser.add_argument("--resource-route")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    packet = _load(PACKET_PATH)
    assert packet is not None
    result = build_manifest(
        packet=packet,
        authorization=_load(Path(args.authorization)) if args.authorization else None,
        fresh_real_evidence=_load(Path(args.fresh_real_evidence)) if args.fresh_real_evidence else None,
        resource_route=_load(Path(args.resource_route)) if args.resource_route else None,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result["result"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
