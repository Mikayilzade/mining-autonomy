#!/usr/bin/env python3
"""I107 network-inert binder for an I106 exact-hash runtime receipt.

This module does not execute the production request, create authorization, use
credentials, dispatch CI, or move value. It only validates a local I106 receipt
and projects *only* the independent runtime-regression blocker into a derived
four-gate preauthorization view.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parent
I104_PATH = ROOT / "I104_PREAUTHORIZATION_BLOCKERS.json"
I100_PATH = ROOT / "I100_EXECUTION_READINESS_RESULT.json"
I106_RECEIPT_PATH = ROOT / "I106_LOCAL_RUNTIME_RECEIPT.json"
EXPECTED_RUNS = ("I099", "I100", "I101", "I102")


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _derive_non_runtime(i100: Mapping[str, Any]) -> dict[str, bool]:
    readiness = i100.get("readiness_inputs") if isinstance(i100.get("readiness_inputs"), Mapping) else {}
    return {
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


def validate_receipt(receipt: Mapping[str, Any]) -> tuple[bool, list[str], dict[str, str]]:
    errors: list[str] = []
    if receipt.get("schema") != "mining-autonomy/i106-local-runtime-receipt/v1":
        errors.append("unexpected I106 receipt schema")
    if receipt.get("run") != "I106" or receipt.get("result") != "PASS":
        errors.append("I106 receipt is not PASS")
    if receipt.get("network_capable") is not False:
        errors.append("receipt must assert network_capable=false")
    if receipt.get("execution_token") is not False or receipt.get("authorization_creator") is not False:
        errors.append("receipt unexpectedly claims execution/authorization capability")
    if receipt.get("production_observation_performed") is not False:
        errors.append("receipt unexpectedly records a production observation")
    if receipt.get("github_actions_dispatched") is not False:
        errors.append("receipt unexpectedly records GitHub Actions dispatch")
    if receipt.get("dependency_hashes_stable_after_execution") is not True:
        errors.append("dependency hashes were not stable after execution")
    banned = receipt.get("banned_network_imports")
    if banned not in ({}, None):
        errors.append("receipt contains banned network imports")

    hashes = receipt.get("dependency_closure_sha256")
    clean_hashes: dict[str, str] = {}
    if not isinstance(hashes, Mapping) or not hashes:
        errors.append("exact dependency hash map missing")
    else:
        for name, digest in hashes.items():
            if not isinstance(name, str) or not isinstance(digest, str) or len(digest) != 64:
                errors.append("invalid dependency hash entry")
                break
            try:
                int(digest, 16)
            except ValueError:
                errors.append("non-hex dependency hash")
                break
            clean_hashes[name] = digest.lower()

    tests = receipt.get("tests")
    observed: dict[str, Mapping[str, Any]] = {}
    if not isinstance(tests, list):
        errors.append("receipt tests array missing")
    else:
        for item in tests:
            if isinstance(item, Mapping) and isinstance(item.get("run"), str):
                observed[item["run"]] = item
        if tuple(run for run in EXPECTED_RUNS if run in observed) != EXPECTED_RUNS or len(observed) != 4:
            errors.append("receipt must contain exactly I099-I102 test results")
        for run in EXPECTED_RUNS:
            item = observed.get(run)
            if not isinstance(item, Mapping) or item.get("pass") is not True or item.get("returncode") != 0:
                errors.append(f"{run} self-test is not a clean PASS")

    if receipt.get("errors") not in ([], None):
        errors.append("receipt contains execution errors")

    return not errors, errors, clean_hashes


def bind(i104: Mapping[str, Any], i100: Mapping[str, Any], receipt: Mapping[str, Any] | None) -> dict[str, Any]:
    errors: list[str] = []
    blockers = i104.get("non_substitutable_blockers") if isinstance(i104.get("non_substitutable_blockers"), Mapping) else {}
    non_runtime = _derive_non_runtime(i100)

    for name, expected in non_runtime.items():
        item = blockers.get(name) if isinstance(blockers.get(name), Mapping) else {}
        if (item.get("satisfied") is True) != expected:
            errors.append(f"historical I104 blocker mismatch for {name}")

    receipt_valid = False
    receipt_errors: list[str] = ["I106 receipt absent"]
    hashes: dict[str, str] = {}
    if receipt is not None:
        receipt_valid, receipt_errors, hashes = validate_receipt(receipt)

    derived = {
        **non_runtime,
        "runtime_regression_verification": receipt_valid,
    }
    four_gate_and = all(derived.values())

    # This binder is evidence projection only. Even if all four eventually become
    # true, downstream exact invocation/authorization consumption remains separate.
    if i100.get("ready_for_network_invocation") is True:
        errors.append("I100 must remain network-inert at this binding checkpoint")
    if i100.get("execution_token") is True or i100.get("network_capable") is True:
        errors.append("I100 unexpectedly claims execution/network capability")
    if i104.get("external_effects", {}).get("production_dns_http_socket_tls") is True:
        errors.append("I104 unexpectedly records production network effects")

    result = "PASS" if not errors else "FAIL_CLOSED"
    return {
        "schema": "mining-autonomy/i107-runtime-receipt-binding/v1",
        "run": "I107",
        "result": result,
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "receipt_present": receipt is not None,
        "receipt_valid": receipt_valid,
        "receipt_validation_errors": receipt_errors,
        "bound_dependency_closure_sha256": hashes if receipt_valid else {},
        "derived_blockers": derived,
        "four_gate_and": four_gate_and,
        "production_observation_allowed": False,
        "binding_note": (
            "A valid I106 PASS may satisfy only runtime_regression_verification. "
            "Fresh-real evidence, a current eligible non-synthetic Resource Router route, "
            "and exact explicit authorization remain independently derived and non-substitutable. "
            "This binder itself never authorizes or performs the production GET."
        ),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--i104", default=str(I104_PATH))
    parser.add_argument("--i100", default=str(I100_PATH))
    parser.add_argument("--receipt", default=str(I106_RECEIPT_PATH))
    parser.add_argument("--output", default=str(ROOT / "I107_RUNTIME_RECEIPT_BINDING_RESULT.json"))
    args = parser.parse_args()

    receipt_path = Path(args.receipt)
    receipt = _load(receipt_path) if receipt_path.is_file() else None
    result = bind(_load(Path(args.i104)), _load(Path(args.i100)), receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
