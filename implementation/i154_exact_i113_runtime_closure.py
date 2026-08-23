"""I154 exact-current I113 runtime closure manifest and fail-closed verifier.

This module is network-inert. It binds the complete pre-stage runtime source/artifact
closure needed by I113 to an explicit repository commit/tree and Git blob identities.
It does not execute I113 and does not authorize any network, spend, credentials,
registration, task acceptance, fulfillment, payment, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
from pathlib import Path
from typing import Iterable

SCHEMA = "mining-autonomy/i154-exact-i113-runtime-closure/v1"
REPOSITORY = "Mikayilzade/mining-autonomy"
COMMIT_SHA = "3699c39aa3e61f217afd37cb44b7cfa0c33a1082"
TREE_SHA = "efb9a4d06e18a5d2ec9421aaaa1c7d379c6e8db9"

@dataclass(frozen=True)
class ClosureEntry:
    path: str
    git_blob_sha: str
    role: str

ENTRIES = (
    ClosureEntry("implementation/I096_FRESH_ONE_SHOT_REVIEW_PACKET.json", "3250f3bb180d3bc0040e97af96529b8044c72b50", "seed_artifact"),
    ClosureEntry("implementation/I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json", "b69374d60dc9ab2b0552816f0049a2aae2e02c4b", "seed_artifact"),
    ClosureEntry("implementation/I100_EXECUTION_READINESS_RESULT.json", "9a71e26c1be94b382d395138bd340d511d39389a", "seed_artifact"),
    ClosureEntry("implementation/I104_PREAUTHORIZATION_BLOCKERS.json", "9f9f2f7d52ad37aaef2067acaad6b942ed533f77", "seed_artifact"),
    ClosureEntry("implementation/i097_offline_packet_verifier.py", "61eeda458a8bfb47fe7d020dc5aa167ba0e88702", "transitive_module"),
    ClosureEntry("implementation/i098_fresh_execution_evidence_contract.py", "d6abaff46530063bf905c7b939e4a69f8eca1ccb", "transitive_module"),
    ClosureEntry("implementation/i099_synthetic_evidence_sequencer.py", "0b097fd223c7a46c5068e0d4d6eef949921abcb7", "i106_target"),
    ClosureEntry("implementation/i100_execution_readiness_manifest.py", "9c6c3ae5843c1664646e0f754a47560fe868161a", "i106_target"),
    ClosureEntry("implementation/i101_fresh_real_evidence_route_contract.py", "651c53b306ce7eac47419168fa3e1990ef047d42", "i106_target"),
    ClosureEntry("implementation/i102_i101_i100_compatibility_adapter.py", "269e9f745c4804c9566153aa3849d228169b5351", "i106_target"),
    ClosureEntry("implementation/i105_preauthorization_consistency_validator.py", "0b3735932f9982419c05c18fbae0909b98609abc", "transitive_module"),
    ClosureEntry("implementation/i106_local_runtime_receipt.py", "3c44e9a250a95570ecbc4ad43cefd330a89854c2", "i113_step"),
    ClosureEntry("implementation/i107_runtime_receipt_binding_validator.py", "3c23db049f03de5682244d1b4fd2d59a610f80b7", "i113_step"),
    ClosureEntry("implementation/i108_runtime_receipt_lineage_validator.py", "d492ae96972e46481a2528a6a289255a8e5d67a1", "i113_step"),
    ClosureEntry("implementation/i109_lineage_preauthorization_consistency.py", "b2bd5adfdaaa915cacbe2330caee7fe2daa83c5e", "i113_step"),
    ClosureEntry("implementation/i110_i109_result_chain_contract.py", "991c992324fb407a73d3fb141515d41c3807448a", "i113_step"),
    ClosureEntry("implementation/i111_preobservation_artifact_manifest.py", "3346ae0385e7882673e95c9ca075edeac4f12d65", "i113_step"),
    ClosureEntry("implementation/i112_i111_manifest_offline_verifier.py", "b543b8211fd7d50cd207c09c7e2f6e1e6af0d56c", "i113_step"),
    ClosureEntry("implementation/i113_local_runtime_chain_runner.py", "d65aa8f46a361e68b11f0c456e2673a2bf1f42ca", "runner"),
)

def git_blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

def _valid_sha(value: str) -> bool:
    if len(value) != 40:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True

def validate_manifest(entries: Iterable[ClosureEntry] = ENTRIES) -> dict:
    items=tuple(entries)
    paths=[e.path for e in items]
    required_steps={f"implementation/i{n}_" for n in range(106,114)}
    step_presence={prefix: any(p.startswith(prefix) for p in paths) for prefix in required_steps}
    errors=[]
    if not _valid_sha(COMMIT_SHA) or not _valid_sha(TREE_SHA): errors.append("invalid source identity")
    if len(paths) != len(set(paths)): errors.append("duplicate path")
    for e in items:
        if not _valid_sha(e.git_blob_sha): errors.append(f"invalid blob sha: {e.path}")
    for prefix,present in step_presence.items():
        if not present: errors.append(f"missing required runtime step: {prefix}")
    seed={e.path for e in items if e.role=="seed_artifact"}
    expected_seed={
        "implementation/I096_FRESH_ONE_SHOT_REVIEW_PACKET.json",
        "implementation/I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json",
        "implementation/I100_EXECUTION_READINESS_RESULT.json",
        "implementation/I104_PREAUTHORIZATION_BLOCKERS.json",
    }
    if seed != expected_seed: errors.append("seed artifact set mismatch")
    return {"schema":SCHEMA,"repository":REPOSITORY,"commit_sha":COMMIT_SHA,"tree_sha":TREE_SHA,"entry_count":len(items),"manifest_valid":not errors,"errors":errors,"i113_executed":False,"execution_authorized_by_manifest":False,"network_enabled":False,"spend_or_value_movement":False}

def verify_materialized(root: Path, entries: Iterable[ClosureEntry] = ENTRIES) -> dict:
    base=validate_manifest(entries)
    missing=[]; mismatched=[]; verified=[]
    for e in tuple(entries):
        local=root/e.path
        if not local.is_file(): missing.append(e.path)
        elif git_blob_sha(local.read_bytes()) != e.git_blob_sha: mismatched.append(e.path)
        else: verified.append(e.path)
    ready=bool(base["manifest_valid"] and not missing and not mismatched)
    return {**base,"verified_files":sorted(verified),"missing_files":sorted(missing),"mismatched_files":sorted(mismatched),"source_bound_bundle_ready":ready,"state":"SOURCE_BOUND_I113_CLOSURE_READY" if ready else "HOLD"}

def manifest_payload() -> dict:
    return {**validate_manifest(),"entries":[asdict(e) for e in ENTRIES]}
