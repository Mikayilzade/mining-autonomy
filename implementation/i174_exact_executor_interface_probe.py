#!/usr/bin/env python3
"""I174 exact-source interface probe for the I173 deterministic executor.

The probe consumes source text; it does not import or execute the target. It verifies
the exact Git blob identity and a deliberately strict AST/source contract sufficient
for the five I170 interface facts of this single-file executor. The proof applies only
to the exact I173 blob and cannot be generalized to another executor or later source.

No network, credentials, provider account, CI, installs, subprocesses, filesystem
probing, spend, task acceptance, settlement, payment or value movement occurs here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1, sha256
import ast
from typing import Any

SCHEMA = "mining-autonomy/i174-exact-executor-interface-probe/v1"
TARGET_PATH = "implementation/i173_structured_json_transform_executor.py"
TARGET_GIT_BLOB_SHA = "29485940ac92c26616a9b60ee9e309110a4fbe62"
EXPECTED_EXECUTOR_ID = "owned-pc-structured-json-normalizer-v1"
EXPECTED_TASK_FAMILY = "structured_json_normalization_v1"
EXPECTED_ACCEPTANCE_CONTRACT_ID = "structured-json-normalization-acceptance-v1"
EXPECTED_ROUTER_CAPABILITY = "transform"

ALLOWED_IMPORT_ROOTS = frozenset({"__future__", "dataclasses", "hashlib", "json", "typing"})
FORBIDDEN_CALL_NAMES = frozenset({
    "open", "exec", "eval", "compile", "__import__", "input", "breakpoint",
})
FORBIDDEN_NAME_ROOTS = frozenset({
    "socket", "requests", "urllib", "http", "subprocess", "os", "pathlib", "shutil",
    "ctypes", "importlib", "ftplib", "smtplib", "ssl", "asyncio", "multiprocessing",
})
REQUIRED_FALSE_DEFAULTS = (
    "network_enabled",
    "credentials_used",
    "provider_account_used",
    "paid_service_used",
    "external_quota_used",
    "external_rate_limit_used",
    "task_acceptance_or_submission",
    "spend_or_value_movement",
    "production_execution_enabled",
)


@dataclass(frozen=True)
class InterfaceProof:
    state: str
    errors: tuple[str, ...]
    target_path: str
    git_blob_sha: str | None
    source_sha256: str | None
    executor_id: str | None
    task_family: str | None
    acceptance_contract_id: str | None
    router_capability: str | None
    source_closure_complete: bool
    requires_credentials: bool | None
    requires_paid_account: bool | None
    requires_new_spend: bool | None
    quota_units_remaining: float | None
    rate_limit_per_minute: float | None
    provider_quota_not_applicable: bool
    provider_rate_limit_not_applicable: bool
    network_dependency_absent: bool
    credential_dependency_absent: bool
    paid_service_dependency_absent: bool
    source_kind: str = "system_probe"
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def git_blob_sha(source_bytes: bytes) -> str:
    header = f"blob {len(source_bytes)}\0".encode("ascii")
    return sha1(header + source_bytes).hexdigest()


def _literal_assignments(tree: ast.AST) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except Exception:
                pass
    return result


def _execution_result_false_defaults(tree: ast.AST) -> set[str]:
    found: set[str] = set()
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.ClassDef) or node.name != "ExecutionResult":
            continue
        for child in node.body:
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                try:
                    value = ast.literal_eval(child.value) if child.value is not None else None
                except Exception:
                    continue
                if value is False:
                    found.add(child.target.id)
    return found


def inspect_source(source_text: str, *, expected_git_blob_sha: str = TARGET_GIT_BLOB_SHA) -> InterfaceProof:
    errors: list[str] = []
    source_bytes = source_text.encode("utf-8")
    actual_blob = git_blob_sha(source_bytes)
    source_digest = sha256(source_bytes).hexdigest()
    if actual_blob != expected_git_blob_sha or expected_git_blob_sha != TARGET_GIT_BLOB_SHA:
        errors.append("target_git_blob_sha_mismatch")

    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return InterfaceProof(
            state="PASS_BLOCKED", errors=("target_source_syntax_error",), target_path=TARGET_PATH,
            git_blob_sha=actual_blob, source_sha256=source_digest, executor_id=None, task_family=None,
            acceptance_contract_id=None, router_capability=None, source_closure_complete=False,
            requires_credentials=None, requires_paid_account=None, requires_new_spend=None,
            quota_units_remaining=None, rate_limit_per_minute=None,
            provider_quota_not_applicable=False, provider_rate_limit_not_applicable=False,
            network_dependency_absent=False, credential_dependency_absent=False,
            paid_service_dependency_absent=False,
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in ALLOWED_IMPORT_ROOTS:
                    errors.append(f"nonwhitelisted_import:{root}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root not in ALLOWED_IMPORT_ROOTS:
                errors.append(f"nonwhitelisted_import:{root}")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALL_NAMES:
                errors.append(f"forbidden_call:{node.func.id}")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAME_ROOTS:
            errors.append(f"forbidden_name_root:{node.id}")

    assignments = _literal_assignments(tree)
    expected_constants = {
        "EXECUTOR_ID": EXPECTED_EXECUTOR_ID,
        "TASK_FAMILY": EXPECTED_TASK_FAMILY,
        "ACCEPTANCE_CONTRACT_ID": EXPECTED_ACCEPTANCE_CONTRACT_ID,
        "ROUTER_CAPABILITY": EXPECTED_ROUTER_CAPABILITY,
    }
    for name, expected in expected_constants.items():
        if assignments.get(name) != expected:
            errors.append(f"identity_constant_mismatch:{name}")

    false_defaults = _execution_result_false_defaults(tree)
    for name in REQUIRED_FALSE_DEFAULTS:
        if name not in false_defaults:
            errors.append(f"inert_default_not_false:{name}")

    # I173 is intentionally one self-contained production-shaped source file.
    # Because all imports are whitelisted pure-library dependencies and there are no
    # local-module imports, the repository source closure for executor logic is one blob.
    source_closure_complete = not any(error.startswith("nonwhitelisted_import:") for error in errors)
    errors = tuple(sorted(set(errors)))
    proved = not errors and source_closure_complete

    return InterfaceProof(
        state="EXACT_EXECUTOR_INTERFACE_PROVED" if proved else "PASS_BLOCKED",
        errors=errors,
        target_path=TARGET_PATH,
        git_blob_sha=actual_blob,
        source_sha256=source_digest,
        executor_id=assignments.get("EXECUTOR_ID"),
        task_family=assignments.get("TASK_FAMILY"),
        acceptance_contract_id=assignments.get("ACCEPTANCE_CONTRACT_ID"),
        router_capability=assignments.get("ROUTER_CAPABILITY"),
        source_closure_complete=proved,
        requires_credentials=False if proved else None,
        requires_paid_account=False if proved else None,
        requires_new_spend=False if proved else None,
        quota_units_remaining=None,
        rate_limit_per_minute=None,
        provider_quota_not_applicable=proved,
        provider_rate_limit_not_applicable=proved,
        network_dependency_absent=proved,
        credential_dependency_absent=proved,
        paid_service_dependency_absent=proved,
    )


def payload(result: InterfaceProof) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I174",
        "interface_parameters_proved": (
            [
                "requires_credentials", "requires_paid_account", "requires_new_spend",
                "quota_units_remaining", "rate_limit_per_minute",
            ] if result.state == "EXACT_EXECUTOR_INTERFACE_PROVED" else []
        ),
        "scope_limit": "exact I173 Git blob only",
        "next_gate": (
            "Feed this exact-source proof into I171 with I173 as a production_task_executor scope. "
            "Do not reuse the proof after any I173 source change; recompute the Git/source binding instead."
        ),
    })
    return body
