#!/usr/bin/env python3
"""I171 exact execution-scope gate for owned-PC control evidence.

I170 showed that five unresolved I050 controls can in principle be evidenced from an
exact local execution interface. I171 prevents a subtle substitution: the I163 fixed
benchmark proves properties of the benchmark closure, not of an unknown future paid-task
executor. Interface/control evidence is therefore promotable only when it is bound to a
named exact source closure and the same acceptance/execution scope used downstream.

No network, credentials, CI dispatch, account creation, paid infrastructure, task
action, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

SCHEMA = "mining-autonomy/i171-owned-pc-execution-scope-gate/v1"
INTERFACE_PARAMETERS = (
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "quota_units_remaining",
    "rate_limit_per_minute",
)
BENCHMARK_SCOPE = "benchmark_only"
PRODUCTION_SCOPE = "production_task_executor"


@dataclass(frozen=True)
class SourceBlob:
    path: str
    git_blob_sha: str


@dataclass(frozen=True)
class ExecutionScope:
    executor_id: str
    scope_kind: str
    source_blobs: tuple[SourceBlob, ...]
    source_closure_complete: bool
    acceptance_contract_id: str | None
    task_family: str | None
    interface_probe_id: str
    network_dependency_absent: bool
    credential_dependency_absent: bool
    paid_service_dependency_absent: bool
    provider_quota_not_applicable: bool
    provider_rate_limit_not_applicable: bool


@dataclass(frozen=True)
class ScopeResult:
    state: str
    errors: tuple[str, ...]
    executor_id: str | None
    scope_kind: str | None
    source_closure_digest: str | None
    interface_parameters_bound: tuple[str, ...]
    production_interface_evidence_ready: bool
    benchmark_evidence_reuse_for_production_allowed: bool
    exact_task_executor_required: bool
    i050_records_created: bool = False
    i123_promotion_allowed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _valid_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(ch in "0123456789abcdef" for ch in value.lower())


def evaluate_scope(scope: ExecutionScope) -> ScopeResult:
    errors: list[str] = []
    if not scope.executor_id.strip():
        errors.append("executor_id_required")
    if scope.scope_kind not in {BENCHMARK_SCOPE, PRODUCTION_SCOPE}:
        errors.append("unsupported_scope_kind")
    if not scope.interface_probe_id.strip():
        errors.append("interface_probe_id_required")
    if not scope.source_blobs:
        errors.append("source_blobs_required")
    if len({blob.path for blob in scope.source_blobs}) != len(scope.source_blobs):
        errors.append("duplicate_source_path")
    for blob in scope.source_blobs:
        if not blob.path.strip() or not _valid_sha(blob.git_blob_sha):
            errors.append("invalid_source_blob_binding")
    if not scope.source_closure_complete:
        errors.append("source_closure_not_complete")

    source_digest = None
    if not errors:
        source_digest = _digest({
            "executor_id": scope.executor_id,
            "scope_kind": scope.scope_kind,
            "source_blobs": [asdict(blob) for blob in sorted(scope.source_blobs, key=lambda x: x.path)],
            "interface_probe_id": scope.interface_probe_id,
            "acceptance_contract_id": scope.acceptance_contract_id,
            "task_family": scope.task_family,
        })

    interface_assertions = {
        "requires_credentials": scope.credential_dependency_absent,
        "requires_paid_account": scope.paid_service_dependency_absent,
        "requires_new_spend": scope.paid_service_dependency_absent,
        "quota_units_remaining": scope.provider_quota_not_applicable,
        "rate_limit_per_minute": scope.provider_rate_limit_not_applicable,
    }
    if not scope.network_dependency_absent:
        errors.append("network_dependency_not_absent")
    for parameter, proved in interface_assertions.items():
        if proved is not True:
            errors.append(f"interface_fact_not_proved:{parameter}")

    if scope.scope_kind == PRODUCTION_SCOPE:
        if not scope.acceptance_contract_id or not scope.acceptance_contract_id.strip():
            errors.append("production_acceptance_contract_required")
        if not scope.task_family or not scope.task_family.strip():
            errors.append("production_task_family_required")

    errors = sorted(set(errors))
    all_interface = not any(error.startswith("interface_fact_not_proved:") for error in errors) and "network_dependency_not_absent" not in errors
    production_ready = (
        not errors
        and scope.scope_kind == PRODUCTION_SCOPE
        and all_interface
        and source_digest is not None
    )

    if production_ready:
        state = "PRODUCTION_EXECUTOR_SCOPE_BOUND"
    elif not errors and scope.scope_kind == BENCHMARK_SCOPE:
        state = "BENCHMARK_SCOPE_BOUND_NOT_PRODUCTION"
    else:
        state = "PASS_BLOCKED"

    return ScopeResult(
        state=state,
        errors=tuple(errors),
        executor_id=scope.executor_id or None,
        scope_kind=scope.scope_kind or None,
        source_closure_digest=source_digest,
        interface_parameters_bound=INTERFACE_PARAMETERS if all_interface and not errors else (),
        production_interface_evidence_ready=production_ready,
        benchmark_evidence_reuse_for_production_allowed=False,
        exact_task_executor_required=not production_ready,
    )


def scope_from_mapping(raw: Mapping[str, Any]) -> ExecutionScope:
    blobs_raw = raw.get("source_blobs")
    if not isinstance(blobs_raw, Iterable) or isinstance(blobs_raw, (str, bytes, Mapping)):
        raise ValueError("source_blobs_must_be_list")
    blobs = tuple(SourceBlob(path=str(row["path"]), git_blob_sha=str(row["git_blob_sha"])) for row in blobs_raw)
    return ExecutionScope(
        executor_id=str(raw.get("executor_id") or ""),
        scope_kind=str(raw.get("scope_kind") or ""),
        source_blobs=blobs,
        source_closure_complete=raw.get("source_closure_complete") is True,
        acceptance_contract_id=raw.get("acceptance_contract_id"),
        task_family=raw.get("task_family"),
        interface_probe_id=str(raw.get("interface_probe_id") or ""),
        network_dependency_absent=raw.get("network_dependency_absent") is True,
        credential_dependency_absent=raw.get("credential_dependency_absent") is True,
        paid_service_dependency_absent=raw.get("paid_service_dependency_absent") is True,
        provider_quota_not_applicable=raw.get("provider_quota_not_applicable") is True,
        provider_rate_limit_not_applicable=raw.get("provider_rate_limit_not_applicable") is True,
    )


def payload(result: ScopeResult) -> dict[str, Any]:
    return {
        **asdict(result),
        "schema": SCHEMA,
        "run": "I171",
        "next_gate": (
            "Select or build the exact deterministic executor for a concrete permitted task family and bind "
            "its complete Git source closure plus acceptance contract. Only that production-scoped closure may "
            "supply the five I170 interface controls to I169/I050. I163 benchmark-only evidence must not be reused."
        ),
    }
