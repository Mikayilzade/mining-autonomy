#!/usr/bin/env python3
"""I173 deterministic offline structured-JSON transform executor.

Concrete task family: structured_json_normalization_v1 (Router capability: transform).
The executor is deliberately local and pure: it parses caller-supplied in-memory/JSON
payloads, validates a fixed acceptance contract, produces a deterministic normalized
artifact, and validates that artifact. It has no network/provider/account/credential,
paid-service, quota, rate-limit, subprocess, filesystem-discovery, task-acceptance,
submission, settlement, payment or value-moving path.

This is production-shaped source for later exact-scope evidence, but I173 itself is
DRY-RUN ONLY. It does not fetch a real marketplace task and does not authorize use.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA = "mining-autonomy/i173-structured-json-transform-executor/v1"
EXECUTOR_ID = "owned-pc-structured-json-normalizer-v1"
TASK_FAMILY = "structured_json_normalization_v1"
ROUTER_CAPABILITY = "transform"
ACCEPTANCE_CONTRACT_ID = "structured-json-normalization-acceptance-v1"

ACCEPTANCE_CONTRACT = {
    "input": {
        "schema_version": 1,
        "records": "non-empty list of objects with unique non-empty string id and nonnegative integer value",
    },
    "output": {
        "schema_version": 1,
        "records": "input records normalized to {id,value} and sorted by id ascending",
        "count": "exact record count",
        "sum": "exact arithmetic sum of value",
        "records_checksum": "sha256 of id:value pairs joined with | in normalized order",
    },
    "acceptance": "output must exactly equal an independently recomputed expected artifact",
}


@dataclass(frozen=True)
class ExecutionResult:
    state: str
    executor_id: str
    task_family: str
    acceptance_contract_id: str
    artifact: dict[str, Any] | None
    artifact_digest: str | None
    accepted: bool
    errors: tuple[str, ...]
    dry_run_only: bool = True
    network_enabled: bool = False
    credentials_used: bool = False
    provider_account_used: bool = False
    paid_service_used: bool = False
    external_quota_used: bool = False
    external_rate_limit_used: bool = False
    task_acceptance_or_submission: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def acceptance_contract_digest() -> str:
    return _digest({
        "acceptance_contract_id": ACCEPTANCE_CONTRACT_ID,
        "task_family": TASK_FAMILY,
        "contract": ACCEPTANCE_CONTRACT,
    })


def _normalize(payload: Mapping[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported_schema_version")
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("nonempty_records_required")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in records:
        if not isinstance(row, Mapping):
            raise ValueError("record_must_be_mapping")
        key = row.get("id")
        value = row.get("value")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("invalid_or_duplicate_id")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("value_must_be_nonnegative_integer")
        seen.add(key)
        normalized.append({"id": key, "value": value})

    normalized.sort(key=lambda item: item["id"])
    checksum_input = "|".join(f'{row["id"]}:{row["value"]}' for row in normalized)
    return {
        "schema_version": 1,
        "records": normalized,
        "count": len(normalized),
        "sum": sum(row["value"] for row in normalized),
        "records_checksum": sha256(checksum_input.encode("utf-8")).hexdigest(),
    }


def validate_artifact(payload: Mapping[str, Any], artifact: Mapping[str, Any]) -> bool:
    try:
        expected = _normalize(payload)
    except Exception:
        return False
    return dict(artifact) == expected


def execute(payload: Mapping[str, Any]) -> ExecutionResult:
    errors: list[str] = []
    artifact: dict[str, Any] | None = None
    try:
        artifact = _normalize(payload)
    except Exception as exc:
        errors.append(str(exc))

    accepted = bool(artifact is not None and validate_artifact(payload, artifact))
    if artifact is not None and not accepted:
        errors.append("acceptance_contract_failed")

    errors = sorted(set(errors))
    state = "DRY_RUN_ARTIFACT_ACCEPTED" if accepted and not errors else "REJECTED"
    return ExecutionResult(
        state=state,
        executor_id=EXECUTOR_ID,
        task_family=TASK_FAMILY,
        acceptance_contract_id=ACCEPTANCE_CONTRACT_ID,
        artifact=artifact if accepted else None,
        artifact_digest=_digest(artifact) if accepted and artifact is not None else None,
        accepted=accepted and not errors,
        errors=tuple(errors),
    )


def payload(result: ExecutionResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "router_capability": ROUTER_CAPABILITY,
        "acceptance_contract_digest": acceptance_contract_digest(),
        "next_gate": (
            "Bind the exact Git blob containing this executor through I171, then prove the five I170 interface "
            "controls against that exact source closure. A later real task may use this executor only when its "
            "actual acceptance criteria are compatible with this contract; I173 does not infer that compatibility."
        ),
    })
    return body
