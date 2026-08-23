#!/usr/bin/env python3
"""I108 network-inert exact-source lineage validator for an I106 runtime receipt.

This checkpoint closes a stale-receipt gap left intentionally open by I107: a
structurally valid I106 PASS receipt must also describe the exact dependency
bytes that are present in the current repository checkout at validation time.

No DNS/HTTP/socket/TLS, credentials, authorization creation, task acceptance,
submission, paid infrastructure, CI dispatch, spend, payment or value movement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import i106_local_runtime_receipt as i106
import i107_runtime_receipt_binding_validator as i107

ROOT = Path(__file__).resolve().parent
I104_PATH = ROOT / "I104_PREAUTHORIZATION_BLOCKERS.json"
I100_PATH = ROOT / "I100_EXECUTION_READINESS_RESULT.json"
I106_RECEIPT_PATH = ROOT / "I106_LOCAL_RUNTIME_RECEIPT.json"


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current_dependency_hashes() -> dict[str, str]:
    target_paths: list[Path] = []
    for run_id, filename, _ in i106.TARGETS:
        path = ROOT / filename
        if not path.is_file():
            raise FileNotFoundError(f"{run_id} target missing: {filename}")
        target_paths.append(path)
    closure = i106.dependency_closure(target_paths)
    return {path.name: _sha256(path) for path in closure}


def _expected_test_spec() -> list[dict[str, Any]]:
    return [
        {"run": run_id, "module": filename, "args": list(args)}
        for run_id, filename, args in i106.TARGETS
    ]


def validate_lineage(receipt: Mapping[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    base_valid, base_errors, receipt_hashes = i107.validate_receipt(receipt)
    if not base_valid:
        errors.extend(f"i107:{message}" for message in base_errors)

    try:
        current_hashes = _current_dependency_hashes()
    except Exception as exc:
        current_hashes = {}
        errors.append(f"current dependency closure unavailable: {type(exc).__name__}: {exc}")

    if current_hashes and receipt_hashes != current_hashes:
        missing = sorted(set(current_hashes) - set(receipt_hashes))
        extra = sorted(set(receipt_hashes) - set(current_hashes))
        changed = sorted(
            name for name in set(current_hashes) & set(receipt_hashes)
            if current_hashes[name] != receipt_hashes[name]
        )
        errors.append(
            "stale/external receipt dependency closure mismatch "
            f"(missing={missing}, extra={extra}, changed={changed})"
        )

    tests = receipt.get("tests")
    expected = _expected_test_spec()
    observed_spec: list[dict[str, Any]] = []
    if isinstance(tests, list):
        for item in tests:
            if not isinstance(item, Mapping):
                errors.append("receipt tests must contain objects only")
                continue
            observed_spec.append({
                "run": item.get("run"),
                "module": item.get("module"),
                "args": item.get("args"),
            })
    if observed_spec != expected:
        errors.append("receipt test order/module/args do not exactly match current I106 TARGETS")

    if receipt.get("targets") != [item["run"] for item in expected]:
        errors.append("receipt targets do not exactly match current I106 target order")

    harness_hash = _sha256(ROOT / "i106_local_runtime_receipt.py")
    binder_hash = _sha256(ROOT / "i107_runtime_receipt_binding_validator.py")
    lineage = {
        "current_dependency_closure_sha256": current_hashes,
        "current_i106_harness_sha256": harness_hash,
        "current_i107_binder_sha256": binder_hash,
        "expected_test_spec": expected,
    }
    return not errors, errors, lineage


def run(
    i104: Mapping[str, Any],
    i100: Mapping[str, Any],
    receipt: Mapping[str, Any] | None,
) -> dict[str, Any]:
    lineage_valid = False
    lineage_errors = ["I106 receipt absent"]
    lineage: dict[str, Any] = {}
    if receipt is not None:
        lineage_valid, lineage_errors, lineage = validate_lineage(receipt)

    # Preserve I107 semantics and then fail closed if exact-source lineage fails.
    i107_view = i107.bind(i104, i100, receipt if lineage_valid else None)
    derived = dict(i107_view.get("derived_blockers", {}))
    derived["runtime_regression_verification"] = bool(
        lineage_valid and i107_view.get("receipt_valid") is True
    )

    return {
        "schema": "mining-autonomy/i108-runtime-receipt-lineage/v1",
        "run": "I108",
        "result": "PASS" if not i107_view.get("errors") and receipt is not None and lineage_valid else "BLOCKED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "receipt_present": receipt is not None,
        "exact_source_lineage_valid": lineage_valid,
        "lineage_validation_errors": lineage_errors,
        "lineage": lineage,
        "derived_blockers": derived,
        "four_gate_and": all(derived.values()) if derived else False,
        "production_observation_allowed": False,
        "anti_replay_note": (
            "A runtime receipt is accepted only when its exact dependency closure and "
            "test specification match the current repository checkout. A PASS still "
            "satisfies only runtime_regression_verification; fresh-real evidence, a "
            "current eligible non-synthetic Resource Router route, and exact explicit "
            "authorization remain independent gates."
        ),
        "errors": list(i107_view.get("errors", [])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--i104", default=str(I104_PATH))
    parser.add_argument("--i100", default=str(I100_PATH))
    parser.add_argument("--receipt", default=str(I106_RECEIPT_PATH))
    parser.add_argument("--output", default=str(ROOT / "I108_RUNTIME_RECEIPT_LINEAGE_RESULT.json"))
    args = parser.parse_args()

    receipt_path = Path(args.receipt)
    receipt = _load(receipt_path) if receipt_path.is_file() else None
    result = run(_load(Path(args.i104)), _load(Path(args.i100)), receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
