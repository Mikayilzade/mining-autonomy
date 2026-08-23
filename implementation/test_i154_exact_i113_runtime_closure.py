from pathlib import Path
from i154_exact_i113_runtime_closure import ENTRIES, ClosureEntry, git_blob_sha, validate_manifest, verify_materialized

def test_exact_manifest_is_complete_and_fail_closed():
    result=validate_manifest()
    assert result["manifest_valid"] is True
    assert result["entry_count"] == 19
    assert result["i113_executed"] is False
    assert result["network_enabled"] is False
    assert result["spend_or_value_movement"] is False

def test_materialization_rejects_missing_and_tampered_bytes(tmp_path: Path):
    result=verify_materialized(tmp_path)
    assert result["source_bound_bundle_ready"] is False
    assert result["state"] == "HOLD"
    assert len(result["missing_files"]) == len(ENTRIES)
    one=ENTRIES[0]
    target=tmp_path/one.path
    target.parent.mkdir(parents=True)
    target.write_bytes(b"tampered")
    result=verify_materialized(tmp_path)
    assert one.path in result["mismatched_files"]

def test_git_blob_hash_and_invalid_manifest():
    assert git_blob_sha(b"test content\n") == "d670460b4b4aece5915caf5c68d12f560a9fe3e4"
    bad=(ClosureEntry("implementation/i106_x.py","bad","i113_step"),)
    assert validate_manifest(bad)["manifest_valid"] is False
