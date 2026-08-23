#!/usr/bin/env python3
"""I113 notification-safe repository-local runtime chain runner.

Executes the already-authored exact local verification chain I106 -> I112 in order.
This orchestration layer is intentionally network-inert: it invokes only repository-local
Python modules, never GitHub Actions, DNS, sockets, TLS, HTTP, credentials, task actions,
paid infrastructure, spend, payment or value movement.

The runner stops on the first failure and records a compact receipt. It deletes each
expected step output immediately before that step so stale artifacts cannot be mistaken
for fresh evidence. Launch errors and timeouts are captured as FAIL_CLOSED receipts
instead of escaping before I113 can write its result.
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
STEP_TIMEOUT_SECONDS = 180


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tail(value: str | bytes | None, limit: int = 2000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return value[-limit:]


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
            output_path = ROOT / output_name
            try:
                output_path.unlink(missing_ok=True)
            except OSError as exc:
                errors.append(f"{run_id} could not clear stale output {output_name}: {exc}")
                executions.append(
                    {
                        "run": run_id,
                        "module": filename,
                        "output": output_name,
                        "returncode": None,
                        "pass": False,
                        "timed_out": False,
                        "launch_error": None,
                        "output_present": output_path.is_file(),
                        "output_sha256": sha256(output_path) if output_path.is_file() else None,
                        "stdout_tail": "",
                        "stderr_tail": "",
                    }
                )
                break

            command = [sys.executable, str(ROOT / filename)]
            try:
                proc = subprocess.run(
                    command,
                    cwd=str(ROOT),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=STEP_TIMEOUT_SECONDS,
                    check=False,
                )
                returncode: int | None = proc.returncode
                stdout_tail = tail(proc.stdout)
                stderr_tail = tail(proc.stderr)
                timed_out = False
                launch_error: str | None = None
            except subprocess.TimeoutExpired as exc:
                returncode = None
                stdout_tail = tail(exc.stdout)
                stderr_tail = tail(exc.stderr)
                timed_out = True
                launch_error = None
            except OSError as exc:
                returncode = None
                stdout_tail = ""
                stderr_tail = ""
                timed_out = False
                launch_error = f"{type(exc).__name__}: {exc}"

            output_present = output_path.is_file()
            item = {
                "run": run_id,
                "module": filename,
                "output": output_name,
                "returncode": returncode,
                "pass": returncode == 0 and output_present and not timed_out and launch_error is None,
                "timed_out": timed_out,
                "launch_error": launch_error,
                "output_present": output_present,
                "output_sha256": sha256(output_path) if output_present else None,
                "stdout_tail": stdout_tail,
                "stderr_tail": stderr_tail,
            }
            executions.append(item)

            if timed_out:
                errors.append(f"{run_id} timed out after {STEP_TIMEOUT_SECONDS}s")
                break
            if launch_error is not None:
                errors.append(f"{run_id} launch failed: {launch_error}")
                break
            if returncode != 0:
                errors.append(f"{run_id} returned {returncode}")
                break
            if not output_present:
                errors.append(f"{run_id} did not create fresh expected output {output_name}")
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
        "schema": "mining-autonomy/i113-local-runtime-chain-runner/v2",
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
        "step_timeout_seconds": STEP_TIMEOUT_SECONDS,
        "fresh_output_required_per_step": True,
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
