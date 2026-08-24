#!/usr/bin/env python3
"""I182 fail-closed owned-PC cumulative energy session for the exact I173 executor.

I182 closes the gap between I181 counter discovery and the existing I162/I166 energy
fields. On the actual user-owned Linux PC, and only with explicit ownership
confirmation, it can read one I181-approved cumulative microjoule counter immediately
before and after a bounded batch of exact I173 dry-run executions. It emits only an
energy measurement fragment; tariff, availability, opportunity cost, accounting and
market facts remain separate inputs.

A non-root filesystem is treated as TEST_ONLY even when ownership confirmation is set,
so fixture tests cannot be promoted as real evidence. Counter wrap/reset, zero delta,
I173 source drift, rejected executor outputs, unreadable/non-I181 candidates and
missing ownership confirmation all fail closed.

No network, subprocess, credential, package install, elevation, CI, market action,
paid infrastructure, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1, sha256
import argparse
import json
from pathlib import Path
from typing import Any

import i173_structured_json_transform_executor as i173
import i181_local_energy_interface_inventory as i181

SCHEMA = "mining-autonomy/i182-owned-pc-energy-session/v1"
I173_PATH = "implementation/i173_structured_json_transform_executor.py"
I173_BLOB_SHA = "29485940ac92c26616a9b60ee9e309110a4fbe62"
MICROJOULES_PER_JOULE = 1_000_000.0
DEFAULT_TASK_COUNT = 2000
WORKLOAD_PAYLOAD = {
    "schema_version": 1,
    "records": [
        {"id": "gamma", "value": 5},
        {"id": "alpha", "value": 2},
        {"id": "beta", "value": 3},
    ],
}


@dataclass(frozen=True)
class EnergySessionResult:
    state: str
    blockers: tuple[str, ...]
    counter_path: str
    counter_kind: str | None
    executor_blob_sha: str | None
    task_count: int
    successful_tasks: int
    energy_before_joules: float | None
    energy_after_joules: float | None
    energy_delta_joules: float | None
    energy_kwh_per_task: float | None
    energy_source_ref: str | None
    evidence_eligible: bool
    test_only_root: bool
    ownership_confirmation_supplied: bool
    network_enabled: bool = False
    credentials_used: bool = False
    subprocess_used: bool = False
    software_installed: bool = False
    elevated_privileges_requested: bool = False
    ci_dispatched: bool = False
    market_action_performed: bool = False
    spend_or_value_movement: bool = False


def git_blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _read_microjoule_counter(path: Path) -> int:
    text = path.read_text(encoding="utf-8").strip()
    if not text or not text.isdigit():
        raise ValueError("counter_value_must_be_nonnegative_integer_microjoules")
    value = int(text)
    if value < 0:
        raise ValueError("counter_value_negative")
    return value


def _blocked(
    *, counter_path: str, task_count: int, confirm_user_owned_pc: bool,
    test_only_root: bool, blockers: list[str], counter_kind: str | None = None,
    executor_blob_sha: str | None = None, successful_tasks: int = 0,
    before_j: float | None = None, after_j: float | None = None,
) -> EnergySessionResult:
    return EnergySessionResult(
        state="PASS_BLOCKED",
        blockers=tuple(sorted(set(blockers))),
        counter_path=counter_path,
        counter_kind=counter_kind,
        executor_blob_sha=executor_blob_sha,
        task_count=task_count,
        successful_tasks=successful_tasks,
        energy_before_joules=before_j,
        energy_after_joules=after_j,
        energy_delta_joules=None,
        energy_kwh_per_task=None,
        energy_source_ref=None,
        evidence_eligible=False,
        test_only_root=test_only_root,
        ownership_confirmation_supplied=confirm_user_owned_pc,
    )


def run_energy_session(
    *,
    repo_root: Path,
    fs_root: Path = Path("/"),
    counter_path: str,
    task_count: int = DEFAULT_TASK_COUNT,
    confirm_user_owned_pc: bool = False,
) -> EnergySessionResult:
    test_only_root = fs_root.resolve() != Path("/").resolve()
    blockers: list[str] = []
    if task_count < 100:
        blockers.append("task_count_must_be_at_least_100_for_counter_resolution")
    if not confirm_user_owned_pc:
        blockers.append("explicit_user_owned_pc_confirmation_required")

    executor_file = repo_root / I173_PATH
    executor_blob: str | None = None
    if not executor_file.is_file():
        blockers.append("i173_source_missing")
    else:
        executor_blob = git_blob_sha(executor_file.read_bytes())
        if executor_blob != I173_BLOB_SHA:
            blockers.append("i173_source_blob_mismatch")

    inventory = i181.inventory_local_energy_interfaces(root=fs_root, system="Linux")
    candidate = next(
        (row for row in inventory.candidates if row.path == counter_path and row.i166_before_after_candidate),
        None,
    )
    if candidate is None:
        blockers.append("counter_not_approved_by_i181_inventory")

    if blockers:
        return _blocked(
            counter_path=counter_path, task_count=task_count,
            confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
            blockers=blockers, counter_kind=candidate.interface_kind if candidate else None,
            executor_blob_sha=executor_blob,
        )

    counter_file = fs_root / counter_path.lstrip("/")
    try:
        before_uj = _read_microjoule_counter(counter_file)
    except Exception as exc:
        return _blocked(
            counter_path=counter_path, task_count=task_count,
            confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
            blockers=[f"counter_before_read_failed:{type(exc).__name__}"],
            counter_kind=candidate.interface_kind, executor_blob_sha=executor_blob,
        )

    successful = 0
    for _ in range(task_count):
        result = i173.execute(WORKLOAD_PAYLOAD)
        if result.state != "DRY_RUN_ARTIFACT_ACCEPTED" or not result.accepted:
            return _blocked(
                counter_path=counter_path, task_count=task_count,
                confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
                blockers=["i173_workload_acceptance_failed"],
                counter_kind=candidate.interface_kind, executor_blob_sha=executor_blob,
                successful_tasks=successful,
                before_j=before_uj / MICROJOULES_PER_JOULE,
            )
        successful += 1

    try:
        after_uj = _read_microjoule_counter(counter_file)
    except Exception as exc:
        return _blocked(
            counter_path=counter_path, task_count=task_count,
            confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
            blockers=[f"counter_after_read_failed:{type(exc).__name__}"],
            counter_kind=candidate.interface_kind, executor_blob_sha=executor_blob,
            successful_tasks=successful,
            before_j=before_uj / MICROJOULES_PER_JOULE,
        )

    before_j = before_uj / MICROJOULES_PER_JOULE
    after_j = after_uj / MICROJOULES_PER_JOULE
    if after_uj < before_uj:
        return _blocked(
            counter_path=counter_path, task_count=task_count,
            confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
            blockers=["counter_wrap_or_reset_detected_rerun_shorter_session"],
            counter_kind=candidate.interface_kind, executor_blob_sha=executor_blob,
            successful_tasks=successful, before_j=before_j, after_j=after_j,
        )
    delta_j = after_j - before_j
    if delta_j <= 0:
        return _blocked(
            counter_path=counter_path, task_count=task_count,
            confirm_user_owned_pc=confirm_user_owned_pc, test_only_root=test_only_root,
            blockers=["zero_energy_delta_counter_resolution_insufficient"],
            counter_kind=candidate.interface_kind, executor_blob_sha=executor_blob,
            successful_tasks=successful, before_j=before_j, after_j=after_j,
        )

    kwh_per_task = delta_j / 3_600_000.0 / task_count
    source_body = {
        "counter_path": counter_path,
        "counter_kind": candidate.interface_kind,
        "counter_metadata": candidate.metadata,
        "executor_blob_sha": executor_blob,
        "executor_id": i173.EXECUTOR_ID,
        "task_family": i173.TASK_FAMILY,
        "acceptance_contract_digest": i173.acceptance_contract_digest(),
        "task_count": task_count,
        "before_microjoules": before_uj,
        "after_microjoules": after_uj,
    }
    source_ref = f"i182-local-counter-session:{_digest(source_body)}"

    if test_only_root:
        state = "TEST_ONLY_COUNTER_SESSION_COMPLETE"
        evidence_eligible = False
        blockers = ["non_root_filesystem_test_only_not_real_owned_pc_evidence"]
    else:
        state = "REAL_OWNED_PC_ENERGY_SESSION_COMPLETE"
        evidence_eligible = True
        blockers = []

    return EnergySessionResult(
        state=state,
        blockers=tuple(blockers),
        counter_path=counter_path,
        counter_kind=candidate.interface_kind,
        executor_blob_sha=executor_blob,
        task_count=task_count,
        successful_tasks=successful,
        energy_before_joules=before_j,
        energy_after_joules=after_j,
        energy_delta_joules=delta_j,
        energy_kwh_per_task=kwh_per_task,
        energy_source_ref=source_ref,
        evidence_eligible=evidence_eligible,
        test_only_root=test_only_root,
        ownership_confirmation_supplied=confirm_user_owned_pc,
    )


def payload(result: EnergySessionResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I182",
        "measurement_fragment": {
            "energy_before_joules": result.energy_before_joules if result.evidence_eligible else None,
            "energy_after_joules": result.energy_after_joules if result.evidence_eligible else None,
            "energy_task_count": result.task_count if result.evidence_eligible else None,
            "energy_source_ref": result.energy_source_ref if result.evidence_eligible else None,
        },
        "next_gate": (
            "Only REAL_OWNED_PC_ENERGY_SESSION_COMPLETE may supply the four energy fields to a separate working "
            "I180 measurement JSON. Tariff, availability and opportunity cost still require truthful independent "
            "provenance. Then run exact I178/I179. TEST_ONLY output and PASS_BLOCKED output are never evidence."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--fs-root", default="/")
    parser.add_argument("--counter-path", required=True)
    parser.add_argument("--task-count", type=int, default=DEFAULT_TASK_COUNT)
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = run_energy_session(
        repo_root=Path(args.repo_root), fs_root=Path(args.fs_root),
        counter_path=args.counter_path, task_count=args.task_count,
        confirm_user_owned_pc=args.confirm_user_owned_pc,
    )
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.state in {"REAL_OWNED_PC_ENERGY_SESSION_COMPLETE", "TEST_ONLY_COUNTER_SESSION_COMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
