#!/usr/bin/env python3
"""I109 network-inert lineage-aware preauthorization consistency validator.

Purpose: bind the I108 exact-source runtime lineage result into the I104/I105
four-blocker view without allowing runtime evidence to substitute for fresh-real
market evidence, a current non-synthetic Resource Router route, or exact user
authorization.

No DNS/HTTP/socket/TLS, credentials, authorization creation, task acceptance,
submission, paid infrastructure, CI dispatch, spend, payment or value movement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import i105_preauthorization_consistency_validator as i105
import i108_runtime_receipt_lineage_validator as i108

ROOT = Path(__file__).resolve().parent
I104_PATH = ROOT / "I104_PREAUTHORIZATION_BLOCKERS.json"
I100_PATH = ROOT / "I100_EXECUTION_READINESS_RESULT.json"
I106_RECEIPT_PATH = ROOT / "I106_LOCAL_RUNTIME_RECEIPT.json"

BLOCKER_NAMES = (
    "fresh_real_execution_evidence",
    "current_materialized_non_synthetic_resource_route",
    "exact_explicit_user_authorization",
    "runtime_regression_verification",
)


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(
    i104_doc: Mapping[str, Any],
    i100_doc: Mapping[str, Any],
    receipt: Mapping[str, Any] | None,
) -> dict[str, Any]:
    errors: list[str] = []

    base = i105.validate(i104_doc, i100_doc)
    if base.get("result") != "PASS":
        errors.extend(f"i105:{message}" for message in base.get("errors", []))

    lineage_view = i108.run(i104_doc, i100_doc, receipt)
    derived = lineage_view.get("derived_blockers") if isinstance(lineage_view.get("derived_blockers"), Mapping) else {}

    # Non-runtime blockers must remain exactly the I100-derived values that I105
    # independently validates. Runtime is the only field I108 may project.
    expected_non_runtime = i108.i107._derive_non_runtime(i100_doc)
    for name, expected in expected_non_runtime.items():
        actual = derived.get(name) is True
        if actual != expected:
            errors.append(f"I108 widened/non-matched blocker {name}: derived={actual}, expected={expected}")

    runtime_expected = bool(
        receipt is not None
        and lineage_view.get("exact_source_lineage_valid") is True
        and lineage_view.get("result") == "PASS"
    )
    runtime_actual = derived.get("runtime_regression_verification") is True
    if runtime_actual != runtime_expected:
        errors.append(
            "runtime_regression_verification mismatch: "
            f"I108-derived={runtime_actual}, exact-current-lineage={runtime_expected}"
        )

    if receipt is None and runtime_actual:
        errors.append("runtime blocker cannot be satisfied while I106 receipt is absent")

    four_gate_and = all(derived.get(name) is True for name in BLOCKER_NAMES)
    if four_gate_and:
        # I109 is consistency evidence only; even all-four true would still flow to
        # downstream exact authorization consumption/executor gates.
        errors.append("I109 must never itself authorize production observation")

    if lineage_view.get("production_observation_allowed") is True:
        errors.append("I108 lineage view unexpectedly authorizes production observation")
    if lineage_view.get("network_capable") is not False:
        errors.append("I108 lineage view unexpectedly claims network capability")
    if lineage_view.get("execution_token") is not False:
        errors.append("I108 lineage view unexpectedly claims execution token")
    if i104_doc.get("external_effects", {}).get("production_dns_http_socket_tls") is True:
        errors.append("I104 unexpectedly records production network effects")

    return {
        "schema": "mining-autonomy/i109-lineage-preauthorization-consistency/v1",
        "run": "I109",
        "result": "PASS_BLOCKED" if not errors and not four_gate_and else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "receipt_present": receipt is not None,
        "exact_source_lineage_valid": lineage_view.get("exact_source_lineage_valid") is True,
        "derived_blockers": {name: derived.get(name) is True for name in BLOCKER_NAMES},
        "four_gate_and": four_gate_and,
        "production_observation_allowed": False,
        "source_binding": {
            "i105_sha256": _sha256(ROOT / "i105_preauthorization_consistency_validator.py"),
            "i106_sha256": _sha256(ROOT / "i106_local_runtime_receipt.py"),
            "i107_sha256": _sha256(ROOT / "i107_runtime_receipt_binding_validator.py"),
            "i108_sha256": _sha256(ROOT / "i108_runtime_receipt_lineage_validator.py"),
        },
        "lineage_errors": list(lineage_view.get("lineage_validation_errors", [])),
        "errors": errors,
        "next_gate": (
            "Execute I106 -> I107 -> I108 -> I109 only in an isolated repository-local Python runtime. "
            "A current-lineage PASS may satisfy only runtime_regression_verification; the other three blockers "
            "remain independently required before any separately authorized production observation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--i104", default=str(I104_PATH))
    parser.add_argument("--i100", default=str(I100_PATH))
    parser.add_argument("--receipt", default=str(I106_RECEIPT_PATH))
    parser.add_argument("--output", default=str(ROOT / "I109_LINEAGE_PREAUTHORIZATION_CONSISTENCY_RESULT.json"))
    args = parser.parse_args()

    receipt_path = Path(args.receipt)
    receipt = _load(receipt_path) if receipt_path.is_file() else None
    result = validate(_load(Path(args.i104)), _load(Path(args.i100)), receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS_BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
