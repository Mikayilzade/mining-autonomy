#!/usr/bin/env python3
"""I112 offline verifier for a future I111 manifest result.

Network-inert by construction. This verifier checks that an existing generated
I111 JSON result exactly matches a deterministic recomputation from the current
repository-local I111 source/artifact closure. It cannot create evidence,
a Resource / Execution Router route, authorization, runtime PASS, credentials,
network capability, paid work, spend, or value movement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import i111_preobservation_artifact_manifest as i111

ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "I111_PREOBSERVATION_ARTIFACT_MANIFEST.json"
I111_SOURCE = ROOT / "i111_preobservation_artifact_manifest.py"

FORBIDDEN_CREATOR_TRUE_FIELDS = (
    "network_capable",
    "execution_token",
    "authorization_creator",
    "resource_route_creator",
    "fresh_real_evidence_creator",
    "task_acceptance_or_submission",
    "credentials_used",
    "paid_infrastructure_created",
    "spend_or_value_movement",
    "github_actions_dispatched",
    "production_observation_performed",
    "production_observation_allowed",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_object(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def verify_manifest(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    errors: list[str] = []
    candidate: Mapping[str, Any] = {}

    if not I111_SOURCE.is_file():
        errors.append("missing current I111 source")
    if not manifest_path.is_file():
        errors.append(f"missing I111 generated manifest: {manifest_path.name}")
    else:
        try:
            candidate = _load_object(manifest_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"invalid I111 generated manifest: {exc}")

    try:
        expected = i111.build_manifest(ROOT)
    except Exception as exc:  # fail closed: upstream recomputation must succeed
        expected = {}
        errors.append(f"I111 deterministic recomputation failed: {type(exc).__name__}: {exc}")

    if candidate and expected and dict(candidate) != expected:
        errors.append("I111 generated manifest does not exactly match current deterministic recomputation")

    if candidate:
        if candidate.get("schema") != "mining-autonomy/i111-preobservation-artifact-manifest/v1":
            errors.append("unexpected I111 manifest schema")
        if candidate.get("run") != "I111":
            errors.append("unexpected I111 manifest run identity")
        if candidate.get("result") not in {"PASS_BLOCKED", "FAIL_CLOSED"}:
            errors.append("unexpected I111 manifest result value")
        for field in FORBIDDEN_CREATOR_TRUE_FIELDS:
            if candidate.get(field) is True:
                errors.append(f"I111 manifest illegally widens capability/permission: {field}=true")
        if candidate.get("four_gate_and") is True:
            errors.append("I112 cannot accept a four-gate authorization state from this offline layer")

        blockers = candidate.get("blocker_projection_from_i104")
        if not isinstance(blockers, Mapping):
            errors.append("I111 blocker projection missing or invalid")
        else:
            # I112 is intentionally unable to mint runtime or non-runtime blockers.
            # If any blocker is true, a separate upstream evidence/authorization review
            # is required rather than accepting it through this offline verifier.
            for name, satisfied in blockers.items():
                if satisfied is True:
                    errors.append(f"offline verifier refuses to mint/accept satisfied blocker: {name}")

    exact_current_match = bool(candidate and expected and dict(candidate) == expected)
    candidate_sha = _sha256(manifest_path) if manifest_path.is_file() else None
    source_sha = _sha256(I111_SOURCE) if I111_SOURCE.is_file() else None

    return {
        "schema": "mining-autonomy/i112-i111-manifest-offline-verifier/v1",
        "run": "I112",
        "result": "PASS_BLOCKED" if not errors else "FAIL_CLOSED",
        "network_capable": False,
        "execution_token": False,
        "authorization_creator": False,
        "resource_route_creator": False,
        "fresh_real_evidence_creator": False,
        "runtime_regression_verification_creator": False,
        "runtime_regression_verification": False,
        "task_acceptance_or_submission": False,
        "credentials_used": False,
        "paid_infrastructure_created": False,
        "spend_or_value_movement": False,
        "github_actions_dispatched": False,
        "production_observation_performed": False,
        "production_observation_allowed": False,
        "i111_source_sha256": source_sha,
        "i111_generated_manifest_path": manifest_path.name,
        "i111_generated_manifest_sha256": candidate_sha,
        "exact_current_deterministic_match": exact_current_match,
        "errors": errors,
        "next_gate": (
            "Run I106 -> I107 -> I108 -> I109 -> I110 -> I111 in an exact repository-local "
            "Python checkout. I112 may verify a resulting I111 manifest against current bytes, "
            "but cannot itself satisfy runtime verification or any non-runtime blocker. The later "
            "one-shot production observation still separately requires fresh-real execution evidence, "
            "a current materialized eligible non-synthetic Resource / Execution Router route with "
            "positive conservative expected margin, and exact explicit user authorization."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output", default=str(ROOT / "I112_I111_MANIFEST_OFFLINE_VERIFIER_RESULT.json"))
    args = parser.parse_args()

    result = verify_manifest(Path(args.manifest))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS_BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
