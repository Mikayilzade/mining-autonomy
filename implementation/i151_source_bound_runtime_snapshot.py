"""I151 source-bound runtime snapshot transport contract.

Purpose: remove a transport-specific dependency on `git clone` for exact-current
local runtime verification. A caller may materialize repository files by any trusted
transport (for example, an authenticated repository connector), but every file must
match its expected Git blob SHA and the snapshot must be bound to an explicit commit
and tree identity before it can be considered eligible for local I113 execution.

This module performs no network access, credentials use, CI dispatch, task action,
spend, payment, or value movement. It does not itself execute I113.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
from pathlib import Path
from typing import Iterable, Mapping

SCHEMA = "mining-autonomy/i151-source-bound-runtime-snapshot/v1"

REQUIRED_RUNTIME_TOP_LEVEL = (
    "implementation/i106_local_runtime_receipt.py",
    "implementation/i107_runtime_receipt_binding_validator.py",
    "implementation/i108_runtime_receipt_lineage_validator.py",
    "implementation/i109_lineage_preauthorization_consistency.py",
    "implementation/i110_i109_result_chain_contract.py",
    "implementation/i111_preobservation_artifact_manifest.py",
    "implementation/i112_i111_manifest_offline_verifier.py",
    "implementation/i113_local_runtime_chain_runner.py",
)


@dataclass(frozen=True)
class SnapshotFile:
    path: str
    git_blob_sha: str


@dataclass(frozen=True)
class RuntimeSnapshotReceipt:
    schema: str
    repository: str
    commit_sha: str
    tree_sha: str
    state: str
    verified_files: tuple[str, ...]
    missing_required_files: tuple[str, ...]
    mismatched_files: tuple[str, ...]
    duplicate_paths: tuple[str, ...]
    source_bound: bool
    i113_execution_authorized_by_receipt: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def _valid_sha(value: str, length: int = 40) -> bool:
    if len(value) != length:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def verify_snapshot(
    *,
    repository: str,
    commit_sha: str,
    tree_sha: str,
    expected_files: Iterable[SnapshotFile],
    root: Path,
    required_paths: Iterable[str] = REQUIRED_RUNTIME_TOP_LEVEL,
) -> RuntimeSnapshotReceipt:
    expected = tuple(expected_files)
    seen: set[str] = set()
    duplicates: list[str] = []
    expected_map: dict[str, str] = {}
    for item in expected:
        if item.path in seen:
            duplicates.append(item.path)
        seen.add(item.path)
        expected_map[item.path] = item.git_blob_sha.lower()

    mismatched: list[str] = []
    verified: list[str] = []
    for path, digest in expected_map.items():
        if not _valid_sha(digest):
            mismatched.append(path)
            continue
        local = root / path
        if not local.is_file() or git_blob_sha(local.read_bytes()) != digest:
            mismatched.append(path)
        else:
            verified.append(path)

    required = tuple(dict.fromkeys(required_paths))
    missing_required = [p for p in required if p not in expected_map or p not in verified]
    identity_valid = (
        bool(repository.strip())
        and _valid_sha(commit_sha.lower())
        and _valid_sha(tree_sha.lower())
    )
    source_bound = bool(
        identity_valid
        and expected_map
        and not duplicates
        and not mismatched
        and not missing_required
    )
    return RuntimeSnapshotReceipt(
        schema=SCHEMA,
        repository=repository,
        commit_sha=commit_sha.lower(),
        tree_sha=tree_sha.lower(),
        state="SOURCE_BOUND_SNAPSHOT_READY_FOR_LOCAL_I113" if source_bound else "HOLD",
        verified_files=tuple(sorted(verified)),
        missing_required_files=tuple(sorted(set(missing_required))),
        mismatched_files=tuple(sorted(set(mismatched))),
        duplicate_paths=tuple(sorted(set(duplicates))),
        source_bound=source_bound,
    )


def payload(receipt: RuntimeSnapshotReceipt) -> dict:
    return asdict(receipt)
