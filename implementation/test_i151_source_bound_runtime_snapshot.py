from pathlib import Path

from i151_source_bound_runtime_snapshot import SnapshotFile, git_blob_sha, verify_snapshot


def _write(root: Path, rel: str, data: bytes) -> SnapshotFile:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return SnapshotFile(rel, git_blob_sha(data))


def test_source_bound_snapshot_accepts_exact_required_bytes(tmp_path):
    files = tuple(
        _write(tmp_path, path, (path + "\n").encode())
        for path in (
            "implementation/i106_local_runtime_receipt.py",
            "implementation/i107_runtime_receipt_binding_validator.py",
            "implementation/i108_runtime_receipt_lineage_validator.py",
            "implementation/i109_lineage_preauthorization_consistency.py",
            "implementation/i110_i109_result_chain_contract.py",
            "implementation/i111_preobservation_artifact_manifest.py",
            "implementation/i112_i111_manifest_offline_verifier.py",
            "implementation/i113_local_runtime_chain_runner.py",
        )
    )
    result = verify_snapshot(
        repository="Mikayilzade/mining-autonomy",
        commit_sha="a" * 40,
        tree_sha="b" * 40,
        expected_files=files,
        root=tmp_path,
    )
    assert result.source_bound is True
    assert result.state == "SOURCE_BOUND_SNAPSHOT_READY_FOR_LOCAL_I113"
    assert result.i113_execution_authorized_by_receipt is False
    assert result.network_enabled is False


def test_snapshot_fails_closed_on_tamper_missing_duplicate_or_bad_identity(tmp_path):
    first = _write(tmp_path, "implementation/i106_local_runtime_receipt.py", b"x")
    duplicate = SnapshotFile(first.path, first.git_blob_sha)
    (tmp_path / first.path).write_bytes(b"tampered")
    result = verify_snapshot(
        repository="Mikayilzade/mining-autonomy",
        commit_sha="not-a-sha",
        tree_sha="b" * 40,
        expected_files=(first, duplicate),
        root=tmp_path,
    )
    assert result.source_bound is False
    assert result.state == "HOLD"
    assert first.path in result.mismatched_files
    assert first.path in result.duplicate_paths
    assert "implementation/i113_local_runtime_chain_runner.py" in result.missing_required_files
