#!/usr/bin/env python3
"""I106 notification-safe local exact-hash runtime receipt harness.

Purpose: execute only the existing network-inert I099/I100/I101/I102 self-tests,
hash the exact executed module bytes, and emit one machine-readable PASS/FAIL receipt.

This harness performs no DNS/HTTP/socket/TLS transport, credentials, authorization
creation, task acceptance/submission, paid infrastructure, spend, payment or value
movement. It never invokes GitHub Actions.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
TARGETS = (
    ("I099", "i099_synthetic_evidence_sequencer.py", ()),
    ("I100", "i100_execution_readiness_manifest.py", ("--self-test",)),
    ("I101", "i101_fresh_real_evidence_route_contract.py", ("--self-test",)),
    ("I102", "i102_i101_i100_compatibility_adapter.py", ("--self-test",)),
)
BANNED_IMPORT_ROOTS = {
    "socket", "ssl", "http", "urllib", "requests", "httpx", "aiohttp",
    "ftplib", "smtplib", "imaplib", "poplib", "telnetlib", "websockets",
}


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_imports(path: Path) -> set[Path]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    local: set[Path] = set()
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
        for name in names:
            candidate = ROOT / (name.split(".")[0] + ".py")
            if candidate.exists():
                local.add(candidate.resolve())
    return local


def banned_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        else:
            continue
        for name in names:
            root = name.split(".")[0]
            if root in BANNED_IMPORT_ROOTS:
                found.add(name)
    return sorted(found)


def dependency_closure(targets: list[Path]) -> list[Path]:
    pending = [p.resolve() for p in targets]
    seen: set[Path] = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        pending.extend(local_imports(path) - seen)
    return sorted(seen, key=lambda p: p.name)


def run() -> dict[str, Any]:
    errors: list[str] = []
    target_paths: list[Path] = []
    for run_id, filename, _ in TARGETS:
        path = ROOT / filename
        if not path.is_file():
            errors.append(f"{run_id} target missing: {filename}")
        else:
            target_paths.append(path)

    closure: list[Path] = []
    if not errors:
        try:
            closure = dependency_closure(target_paths)
        except Exception as exc:  # fail closed on source/AST problems
            errors.append(f"dependency inspection failed: {type(exc).__name__}: {exc}")

    banned: dict[str, list[str]] = {}
    if not errors:
        for path in closure:
            hits = banned_imports(path)
            if hits:
                banned[path.name] = hits
        if banned:
            errors.append("network-capable import found in tested local dependency closure")

    pre_hashes = {p.name: sha256_bytes(p) for p in closure} if not errors else {}
    test_results: list[dict[str, Any]] = []

    if not errors:
        env = os.environ.copy()
        env.update({
            "PYTHONNOUSERSITE": "1",
            "NO_PROXY": "*",
            "no_proxy": "*",
            "HTTP_PROXY": "",
            "HTTPS_PROXY": "",
            "ALL_PROXY": "",
        })
        for run_id, filename, args in TARGETS:
            command = [sys.executable, str(ROOT / filename), *args]
            try:
                proc = subprocess.run(
                    command,
                    cwd=str(ROOT),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60,
                    check=False,
                )
                item = {
                    "run": run_id,
                    "module": filename,
                    "args": list(args),
                    "returncode": proc.returncode,
                    "stdout": proc.stdout[-4000:],
                    "stderr": proc.stderr[-4000:],
                    "pass": proc.returncode == 0,
                }
                test_results.append(item)
                if proc.returncode != 0:
                    errors.append(f"{run_id} self-test returned {proc.returncode}")
                    break
            except Exception as exc:
                errors.append(f"{run_id} execution failed: {type(exc).__name__}: {exc}")
                break

    post_hashes = {p.name: sha256_bytes(p) for p in closure} if closure else {}
    hash_stable = bool(pre_hashes) and pre_hashes == post_hashes
    if closure and not hash_stable:
        errors.append("tested module/dependency bytes changed during receipt run")

    return {
        "schema": "mining-autonomy/i106-local-runtime-receipt/v1",
        "run": "I106",
        "result": "PASS" if not errors else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "production_observation_performed": False,
        "github_actions_dispatched": False,
        "runtime": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "targets": [x[0] for x in TARGETS],
        "dependency_closure_sha256": pre_hashes,
        "dependency_hashes_stable_after_execution": hash_stable,
        "banned_network_imports": banned,
        "tests": test_results,
        "errors": errors,
        "four_blocker_note": (
            "A PASS receipt satisfies only the independent runtime-regression-verification checkpoint. "
            "It does not create fresh-real evidence, a current eligible non-synthetic Resource Router route, "
            "or exact explicit user authorization."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "I106_LOCAL_RUNTIME_RECEIPT.json"))
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
