#!/usr/bin/env python3
"""I111 compact pre-observation artifact manifest.

Network-inert only. This artifact binds the exact current safety/resource/runtime
contract sources into one deterministic manifest. It does not perform DNS/HTTP,
create authorization, materialize a Resource Router route, accept work, spend
money, or move value.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parent

REQUIRED_ARTIFACTS = (
    "I100_EXECUTION_READINESS_RESULT.json",
    "I104_PREAUTHORIZATION_BLOCKERS.json",
    "i105_preauthorization_consistency_validator.py",
    "i106_local_runtime_receipt.py",
    "i107_runtime_receipt_binding_validator.py",
    "i108_runtime_receipt_lineage_validator.py",
    "i109_lineage_preauthorization_consistency.py",
    "i110_i109_result_chain_contract.py",
)

OPTIONAL_RUNTIME_RESULTS = (
    "I106_LOCAL_RUNTIME_RECEIPT.json",
    "I109_LINEAGE_PREAUTHORIZATION_CONSISTENCY_RESULT.json",
    "I110_I109_RESULT_CHAIN_CONTRACT_RESULT.json",
)

BLOCKER_NAMES = (
    "fresh_real_execution_evidence",
    "current_materialized_non_synthetic_resource_route",
    "exact_explicit_user_authorization",
    "runtime_regression_verification",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def build_manifest(root: Path = ROOT) -> dict[str, Any]:
    errors: list[str] = []
    required_hashes: dict[str, str] = {}
    optional_results: dict[str, dict[str, Any]] = {}

    for filename in REQUIRED_ARTIFACTS:
        path = root / filename
        if not path.is_file():
            errors.append(f"missing required artifact: {filename}")
            continue
        required_hashes[filename] = _sha256(path)

    for filename in OPTIONAL_RUNTIME_RESULTS:
        path = root / filename
        optional_results[filename] = {
            "present": path.is_file(),
            "sha256": _sha256(path) if path.is_file() else None,
        }

    i100_path = root / "I100_EXECUTION_READINESS_RESULT.json"
    i104_path = root / "I104_PREAUTHORIZATION_BLOCKERS.json"
    i100 = _load_json(i100_path) if i100_path.is_file() else {}
    i104 = _load_json(i104_path) if i104_path.is_file() else {}

    i104_blockers = i104.get("non_substitutable_blockers")
    if not isinstance(i104_blockers, Mapping):
        i104_blockers = {}

    blocker_projection = {
        name: bool(
            isinstance(i104_blockers.get(name), Mapping)
            and i104_blockers[name].get("satisfied") is True
        )
        for name in BLOCKER_NAMES
    }

    # This checkpoint is intentionally fail-closed. A future legitimate change
    # to any non-runtime blocker must be reviewed through its upstream evidence
    # chain rather than being silently accepted by this manifest.
    for name in BLOCKER_NAMES[:3]:
        if blocker_projection[name]:
            errors.append(f"non-runtime blocker unexpectedly satisfied at I111: {name}")

    if i100.get("ready_for_network_invocation") is True:
        errors.append("I100 unexpectedly reports ready_for_network_invocation=true")
    if i100.get("network_capable") is not False:
        errors.append("I100 must remain network_capable=false")
    if i100.get("execution_token") is not False:
        errors.append("I100 must remain execution_token=false")
    if i104.get("production_observation_allowed") is True:
        errors.append("I104 unexpectedly allows production observation")

    external = i104.get("external_effects")
    if not isinstance(external, Mapping):
        external = {}
    if any(external.get(key) is True for key in (
        "production_dns_http_socket_tls",
        "credentials",
        "task_acceptance_or_submission",
        "spend_or_value_movement",
        "github_actions_dispatched",
    )):
        errors.append("I104 records an external effect incompatible with I111")

    return {
        "schema": "mining-autonomy/i111-preobservation-artifact-manifest/v1",
        "run": "I111",
        "result": "PASS_BLOCKED" if not errors else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "resource_route_creator": False,
        "fresh_real_evidence_creator": False,
        "task_acceptance_or_submission": False,
        "credentials_used": False,
        "paid_infrastructure_created": False,
        "spend_or_value_movement": False,
        "github_actions_dispatched": False,
        "production_observation_performed": False,
        "required_artifact_sha256": required_hashes,
        "optional_runtime_results": optional_results,
        "blocker_projection_from_i104": blocker_projection,
        "four_gate_and": all(blocker_projection.values()),
        "production_observation_allowed": False,
        "exact_observation_scope": i100.get("exact_request_target"),
        "resource_router_route_currently_eligible": bool(
            isinstance(i100.get("readiness_inputs"), Mapping)
            and i100["readiness_inputs"].get("resource_route_eligible") is True
        ),
        "errors": errors,
        "next_gate": (
            "Execute I106 -> I107 -> I108 -> I109 -> I110 -> I111 in a repository-local "
            "Python runtime. A valid current-lineage runtime chain may satisfy only the runtime "
            "verification blocker. Fresh-real policy/DNS/TLS/rebinding evidence, a current "
            "materialized eligible non-synthetic Resource Router route with positive conservative "
            "margin, and exact explicit user authorization remain independently required before "
            "the separately gated one-shot read-only production observation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(ROOT / "I111_PREOBSERVATION_ARTIFACT_MANIFEST.json"),
    )
    args = parser.parse_args()

    result = build_manifest()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS_BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
