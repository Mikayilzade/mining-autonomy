#!/usr/bin/env python3
"""I110 exact I109 result/source-chain receipt contract.

Network-inert hardening only. This validator accepts an I109 result only when it
is reproduced from the current I104/I100 inputs, the current optional I106
receipt, and the exact current I105-I109 source chain. It cannot create
fresh-real evidence, a Resource Router route, authorization, or execution power.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import i109_lineage_preauthorization_consistency as i109

ROOT = Path(__file__).resolve().parent
I104_PATH = ROOT / "I104_PREAUTHORIZATION_BLOCKERS.json"
I100_PATH = ROOT / "I100_EXECUTION_READINESS_RESULT.json"
I106_RECEIPT_PATH = ROOT / "I106_LOCAL_RUNTIME_RECEIPT.json"
I109_RESULT_PATH = ROOT / "I109_LINEAGE_PREAUTHORIZATION_CONSISTENCY_RESULT.json"

SOURCE_CHAIN = (
    "i105_preauthorization_consistency_validator.py",
    "i106_local_runtime_receipt.py",
    "i107_runtime_receipt_binding_validator.py",
    "i108_runtime_receipt_lineage_validator.py",
    "i109_lineage_preauthorization_consistency.py",
)
BLOCKER_NAMES = i109.BLOCKER_NAMES


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current_source_chain() -> dict[str, str]:
    result: dict[str, str] = {}
    for filename in SOURCE_CHAIN:
        path = ROOT / filename
        if not path.is_file():
            raise FileNotFoundError(filename)
        result[filename] = _sha256(path)
    return result


def _canonical_projection(value: Mapping[str, Any]) -> dict[str, Any]:
    blockers = value.get("derived_blockers")
    if not isinstance(blockers, Mapping):
        blockers = {}
    return {
        "schema": value.get("schema"),
        "run": value.get("run"),
        "result": value.get("result"),
        "network_capable": value.get("network_capable"),
        "execution_token": value.get("execution_token"),
        "authorization_creator": value.get("authorization_creator"),
        "production_observation_performed": value.get("production_observation_performed"),
        "github_actions_dispatched": value.get("github_actions_dispatched"),
        "receipt_present": value.get("receipt_present"),
        "exact_source_lineage_valid": value.get("exact_source_lineage_valid"),
        "derived_blockers": {name: blockers.get(name) is True for name in BLOCKER_NAMES},
        "four_gate_and": value.get("four_gate_and") is True,
        "production_observation_allowed": value.get("production_observation_allowed") is True,
        "source_binding": value.get("source_binding"),
        "lineage_errors": value.get("lineage_errors"),
        "errors": value.get("errors"),
    }


def validate(
    i104_doc: Mapping[str, Any],
    i100_doc: Mapping[str, Any],
    receipt: Mapping[str, Any] | None,
    observed_i109: Mapping[str, Any] | None,
) -> dict[str, Any]:
    errors: list[str] = []
    source_chain = _current_source_chain()
    expected = i109.validate(i104_doc, i100_doc, receipt)

    if observed_i109 is None:
        errors.append("I109 result receipt absent")
    else:
        if _canonical_projection(observed_i109) != _canonical_projection(expected):
            errors.append("I109 result does not exactly match current deterministic recomputation")

        binding = observed_i109.get("source_binding")
        expected_binding = {
            "i105_sha256": source_chain["i105_preauthorization_consistency_validator.py"],
            "i106_sha256": source_chain["i106_local_runtime_receipt.py"],
            "i107_sha256": source_chain["i107_runtime_receipt_binding_validator.py"],
            "i108_sha256": source_chain["i108_runtime_receipt_lineage_validator.py"],
        }
        if binding != expected_binding:
            errors.append("I109 embedded I105-I108 source binding is stale or mismatched")

    expected_blockers = expected.get("derived_blockers") if isinstance(expected.get("derived_blockers"), Mapping) else {}
    non_runtime = (
        "fresh_real_execution_evidence",
        "current_materialized_non_synthetic_resource_route",
        "exact_explicit_user_authorization",
    )
    if any(expected_blockers.get(name) is True for name in non_runtime):
        # This contract is not the place to mint or infer those permissions. If a
        # future repository state legitimately changes them, the upstream exact
        # evidence/authorization chain must be reviewed before this checkpoint.
        errors.append("non-runtime blocker became true; requires separate upstream review, not I110 inference")

    four_gate_and = all(expected_blockers.get(name) is True for name in BLOCKER_NAMES)
    if four_gate_and:
        errors.append("I110 cannot itself authorize production observation")
    if expected.get("production_observation_allowed") is True:
        errors.append("I109 recomputation unexpectedly authorizes production observation")
    if expected.get("network_capable") is not False or expected.get("execution_token") is not False:
        errors.append("I109 recomputation unexpectedly exposes network/execution capability")

    return {
        "schema": "mining-autonomy/i110-i109-result-chain-contract/v1",
        "run": "I110",
        "result": "PASS_BLOCKED" if not errors else "BLOCKED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "i109_result_present": observed_i109 is not None,
        "i106_receipt_present": receipt is not None,
        "current_source_chain_sha256": source_chain,
        "current_i104_sha256": _sha256(I104_PATH),
        "current_i100_sha256": _sha256(I100_PATH),
        "expected_i109_projection": _canonical_projection(expected),
        "four_gate_and": four_gate_and,
        "production_observation_allowed": False,
        "errors": errors,
        "next_gate": (
            "In a repository-local Python runtime execute I106 -> I107 -> I108 -> I109 -> I110. "
            "A valid current-chain receipt may satisfy only runtime regression verification. "
            "Fresh-real evidence, a current eligible non-synthetic Resource Router route, and exact explicit "
            "authorization remain separately required before any one-shot production observation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--i104", default=str(I104_PATH))
    parser.add_argument("--i100", default=str(I100_PATH))
    parser.add_argument("--receipt", default=str(I106_RECEIPT_PATH))
    parser.add_argument("--i109-result", default=str(I109_RESULT_PATH))
    parser.add_argument("--output", default=str(ROOT / "I110_I109_RESULT_CHAIN_CONTRACT_RESULT.json"))
    args = parser.parse_args()

    receipt_path = Path(args.receipt)
    i109_path = Path(args.i109_result)
    receipt = _load(receipt_path) if receipt_path.is_file() else None
    observed_i109 = _load(i109_path) if i109_path.is_file() else None
    result = validate(_load(Path(args.i104)), _load(Path(args.i100)), receipt, observed_i109)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS_BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
