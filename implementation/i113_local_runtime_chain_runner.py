#!/usr/bin/env python3
"""I113 notification-safe repository-local runtime chain runner.

Executes the already-authored exact local verification chain I106 -> I112 in order.
This orchestration layer is intentionally network-inert: it invokes only repository-local
Python modules, never GitHub Actions, DNS, sockets, TLS, HTTP, credentials, task actions,
paid infrastructure, spend, payment or value movement.

The runner stops on the first non-zero exit code and records a compact receipt. It does
not convert any non-runtime blocker to true and cannot authorize the production GET.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
STEPS = (
    ("I106", "i106_local_runtime_receipt.py", "I106_LOCAL_RUNTIME_RECEIPT.json"),
    ("I107", "i107_runtime_receipt_binding_validator.py", "I107_RUNTIME_RECEIPT_BINDING_RESULT.json"),
    ("I108", "i108_runtime_receipt_lineage_validator.py", "I108_RUNTIME_RECEIPT_LINEAGE_RESULT.json"),
    ("I109", "i109_lineage_preauthorization_consistency.py", "I109_LINEAGE_PREAUTHORIZATION_CONSISTENCY_RESULT.json"),
    ("I110", "i110_i109_result_chain_contract.py", "I110_I109_RESULT_CHAIN_CONTRACT_RESULT.json"),
    ("I111", "i111_preobservation_artifact_manifest.py", "I111_PREOBSERVATION_ARTIFACT_MANIFEST.json"),
    ("I112", "i112_i111_manifest_offline_verifier.py", "I112_I111_MANIFEST_OFFLINE_VERIFIER_RESULT.json"),
)

BANNED_ENV_PREFIXES = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_chain() -> dict[str, Any]:
    errors: list[str] = []
    executions: list[dict[str, Any]] = []

    missing = [filename for _, filename, _ in STEPS if not (ROOT / filename).is_file()]
    if missing:
        errors.append("missing chain modules: " + ", ".join(missing))

    env = os.environ.copy()
    env["PYTHONNOUSERSITE"] = "1"
    env["NO_PROXY"] = "*"
    env["no_proxy"] = "*"
    for key in BANNED_ENV_PREFIXES:
        env[key] = ""

    pre_source_hashes = {
        filename: sha256(ROOT / filename)
        for _, filename, _ in STEPS
        if (ROOT / filename).is_file()
    }

    if not errors:
        for run_id, filename, output_name in STEPS:
            command = [sys.executable, str(ROOT / filename)]
            proc = subprocess.run(
                command,
                cwd=str(ROOT),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=180,
                check=False,
            )
            output_path = ROOT / output_name
            item = {
                "run": run_id,
                "module": filename,
                "output": output_name,
                "returncode": proc.returncode,
                "pass": proc.returncode == 0,
                "output_present": output_path.is_file(),
                "output_sha256": sha256(output_path) if output_path.is_file() else None,
                "stdout_tail": proc.stdout[-2000:],
                "stderr_tail": proc.stderr[-2000:],
            }
            executions.append(item)
            if proc.returncode != 0:
                errors.append(f"{run_id} returned {proc.returncode}")
                break
            if not output_path.is_file():
                errors.append(f"{run_id} did not create expected output {output_name}")
                break

    post_source_hashes = {
        filename: sha256(ROOT / filename)
        for _, filename, _ in STEPS
        if (ROOT / filename).is_file()
    }
    source_hashes_stable = bool(pre_source_hashes) and pre_source_hashes == post_source_hashes
    if pre_source_hashes and not source_hashes_stable:
        errors.append("I106-I112 source bytes changed while running the chain")

    completed = [item["run"] for item in executions if item["pass"]]
    return {
        "schema": "mining-autonomy/i113-local-runtime-chain-runner/v1",
        "run": "I113",
        "result": "PASS_BLOCKED" if not errors and completed == [x[0] for x in STEPS] else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "resource_route_creator": False,
        "fresh_real_evidence_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "paid_infrastructure_created": False,
        "spend_or_value_movement": False,
        "chain_order": [x[0] for x in STEPS],
        "completed_steps": completed,
        "source_sha256_before": pre_source_hashes,
        "source_hashes_stable_after_execution": source_hashes_stable,
        "executions": executions,
        "errors": errors,
        "next_gate": (
            "If PASS_BLOCKED, runtime verification evidence exists only for the exact current local chain. "
            "Fresh-real execution evidence, a current eligible non-synthetic Resource / Execution Router route "
            "with positive conservative margin, and exact explicit user authorization remain independent blockers "
            "before any separately gated one-shot production observation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "I113_LOCAL_RUNTIME_CHAIN_RESULT.json"))
    args = parser.parse_args()
    result = run_chain()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS_BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
