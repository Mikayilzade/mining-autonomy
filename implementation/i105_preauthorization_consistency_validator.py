#!/usr/bin/env python3
"""I105 network-inert consistency validator for I104 blockers vs I100 readiness.

No network, credentials, authorization creation, task actions, spend, or value movement.
It only reads local JSON artifacts and fails closed on disagreement.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parent
I104_PATH = ROOT / "I104_PREAUTHORIZATION_BLOCKERS.json"
I100_PATH = ROOT / "I100_EXECUTION_READINESS_RESULT.json"


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate(i104: Mapping[str, Any], i100: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    blockers = i104.get("non_substitutable_blockers") if isinstance(i104.get("non_substitutable_blockers"), Mapping) else {}
    readiness = i100.get("readiness_inputs") if isinstance(i100.get("readiness_inputs"), Mapping) else {}

    expected = {
        "fresh_real_execution_evidence": bool(
            readiness.get("fresh_real_execution_evidence_not_synthetic") is True
            and readiness.get("fresh_real_execution_evidence_valid") is True
        ),
        "current_materialized_non_synthetic_resource_route": bool(
            readiness.get("current_materialized_route_supplied") is True
            and readiness.get("resource_route_not_synthetic") is True
            and readiness.get("resource_route_eligible") is True
        ),
        "exact_explicit_user_authorization": readiness.get("explicit_exact_authorization_present") is True,
    }

    for name, expected_value in expected.items():
        item = blockers.get(name) if isinstance(blockers.get(name), Mapping) else {}
        actual = item.get("satisfied") is True
        if actual != expected_value:
            errors.append(f"{name} mismatch: I104={actual}, I100-derived={expected_value}")

    runtime = blockers.get("runtime_regression_verification") if isinstance(blockers.get("runtime_regression_verification"), Mapping) else {}
    if runtime.get("satisfied") is True:
        errors.append("runtime_regression_verification cannot be true without a separate exact-hash runtime receipt")

    all_four = all(
        isinstance(blockers.get(name), Mapping) and blockers[name].get("satisfied") is True
        for name in (
            "fresh_real_execution_evidence",
            "current_materialized_non_synthetic_resource_route",
            "exact_explicit_user_authorization",
            "runtime_regression_verification",
        )
    )
    allowed = i104.get("production_observation_allowed") is True
    if allowed != all_four:
        errors.append(f"production_observation_allowed mismatch: I104={allowed}, four-gate-AND={all_four}")

    if i100.get("ready_for_network_invocation") is True:
        errors.append("I100 result artifact must remain network-inert: ready_for_network_invocation must be false")
    if i100.get("execution_token") is True or i100.get("network_capable") is True:
        errors.append("I100 result artifact unexpectedly claims execution/network capability")
    if i104.get("external_effects", {}).get("production_dns_http_socket_tls") is True:
        errors.append("I104 unexpectedly records production network effects")

    return {
        "schema": "mining-autonomy/i105-preauthorization-consistency/v1",
        "run": "I105",
        "result": "PASS" if not errors else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_allowed": False,
        "checked": {
            "fresh_real_execution_evidence": expected["fresh_real_execution_evidence"],
            "current_materialized_non_synthetic_resource_route": expected["current_materialized_non_synthetic_resource_route"],
            "exact_explicit_user_authorization": expected["exact_explicit_user_authorization"],
            "runtime_regression_receipt_present": False,
            "four_gate_and": all_four,
        },
        "errors": errors,
        "next_gate": "notification-safe exact-hash runtime receipt remains required; production GET remains separately authorization-gated",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--i104", default=str(I104_PATH))
    parser.add_argument("--i100", default=str(I100_PATH))
    parser.add_argument("--output")
    args = parser.parse_args()
    result = validate(_load(Path(args.i104)), _load(Path(args.i100)))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
