#!/usr/bin/env python3
"""I175 bind the exact I173 interface proof into I171 production scope.

Consumes an I174 exact-source proof and projects the five I170 interface controls only
when the proof is tied to the exact I173 Git blob, task family and acceptance contract.
It then calls current I171 to obtain the production_task_executor scope result.

No I050 records are created here. No I123 promotion, market observation, credentials,
CI dispatch, account creation, paid infrastructure, spend, task action or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

import i171_owned_pc_execution_scope_gate as i171

SCHEMA = "mining-autonomy/i175-i171-production-scope-binding/v1"
TARGET_PATH = "implementation/i173_structured_json_transform_executor.py"
TARGET_GIT_BLOB_SHA = "29485940ac92c26616a9b60ee9e309110a4fbe62"
EXECUTOR_ID = "owned-pc-structured-json-normalizer-v1"
TASK_FAMILY = "structured_json_normalization_v1"
ACCEPTANCE_CONTRACT_ID = "structured-json-normalization-acceptance-v1"
INTERFACE_PARAMETERS = i171.INTERFACE_PARAMETERS


@dataclass(frozen=True)
class InterfaceFact:
    parameter: str
    value: Any
    source_kind: str
    source_ref: str
    source_content_digest: str


@dataclass(frozen=True)
class BindingResult:
    state: str
    errors: tuple[str, ...]
    i171_result: dict[str, Any] | None
    interface_facts: tuple[InterfaceFact, ...]
    production_executor_scope_bound: bool
    i050_records_created: bool = False
    i066_materialization_executed: bool = False
    i123_promotion_allowed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def bind_interface_proof(proof: Mapping[str, Any]) -> BindingResult:
    errors: list[str] = []
    if proof.get("state") != "EXACT_EXECUTOR_INTERFACE_PROVED":
        errors.append("i174_exact_interface_proof_required")
    if proof.get("target_path") != TARGET_PATH:
        errors.append("target_path_mismatch")
    if proof.get("git_blob_sha") != TARGET_GIT_BLOB_SHA:
        errors.append("target_git_blob_sha_mismatch")
    if proof.get("executor_id") != EXECUTOR_ID:
        errors.append("executor_id_mismatch")
    if proof.get("task_family") != TASK_FAMILY:
        errors.append("task_family_mismatch")
    if proof.get("acceptance_contract_id") != ACCEPTANCE_CONTRACT_ID:
        errors.append("acceptance_contract_mismatch")
    if proof.get("source_closure_complete") is not True:
        errors.append("source_closure_not_complete")
    source_sha256 = proof.get("source_sha256")
    if not isinstance(source_sha256, str) or len(source_sha256) != 64:
        errors.append("source_sha256_required")

    expected_flags = (
        "network_dependency_absent",
        "credential_dependency_absent",
        "paid_service_dependency_absent",
        "provider_quota_not_applicable",
        "provider_rate_limit_not_applicable",
    )
    for name in expected_flags:
        if proof.get(name) is not True:
            errors.append(f"interface_proof_missing:{name}")

    expected_values = {
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "quota_units_remaining": None,
        "rate_limit_per_minute": None,
    }
    for name, expected in expected_values.items():
        if proof.get(name) != expected:
            errors.append(f"interface_value_mismatch:{name}")

    errors = sorted(set(errors))
    if errors:
        return BindingResult(
            state="PASS_BLOCKED", errors=tuple(errors), i171_result=None,
            interface_facts=(), production_executor_scope_bound=False,
        )

    scope = i171.ExecutionScope(
        executor_id=EXECUTOR_ID,
        scope_kind=i171.PRODUCTION_SCOPE,
        source_blobs=(i171.SourceBlob(path=TARGET_PATH, git_blob_sha=TARGET_GIT_BLOB_SHA),),
        source_closure_complete=True,
        acceptance_contract_id=ACCEPTANCE_CONTRACT_ID,
        task_family=TASK_FAMILY,
        interface_probe_id=f"i174:{source_sha256}",
        network_dependency_absent=True,
        credential_dependency_absent=True,
        paid_service_dependency_absent=True,
        provider_quota_not_applicable=True,
        provider_rate_limit_not_applicable=True,
    )
    scope_result = i171.evaluate_scope(scope)
    if scope_result.state != "PRODUCTION_EXECUTOR_SCOPE_BOUND" or not scope_result.production_interface_evidence_ready:
        return BindingResult(
            state="PASS_BLOCKED",
            errors=("i171_production_scope_not_bound", *scope_result.errors),
            i171_result=asdict(scope_result), interface_facts=(),
            production_executor_scope_bound=False,
        )

    source_ref = f"i171-scope:{scope_result.source_closure_digest}"
    facts = tuple(
        InterfaceFact(
            parameter=name,
            value=expected_values[name],
            source_kind="system_probe",
            source_ref=source_ref,
            source_content_digest=source_sha256,
        )
        for name in INTERFACE_PARAMETERS
    )
    return BindingResult(
        state="PRODUCTION_INTERFACE_CONTROLS_READY",
        errors=(),
        i171_result=asdict(scope_result),
        interface_facts=facts,
        production_executor_scope_bound=True,
    )


def payload(result: BindingResult) -> dict[str, Any]:
    body = asdict(result)
    body["interface_facts"] = [asdict(row) for row in result.interface_facts]
    body.update({
        "schema": SCHEMA,
        "run": "I175",
        "next_gate": (
            "Use these five system-probe facts only with the exact I173 production scope. The two owner/accounting "
            "I050 controls remain separate truthful evidence. I175 does not create I050 records or alter I123."
        ),
    })
    return body
