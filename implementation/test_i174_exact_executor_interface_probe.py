from pathlib import Path

import i174_exact_executor_interface_probe as i174


def _target_source():
    return Path(__file__).with_name("i173_structured_json_transform_executor.py").read_text(encoding="utf-8")


def test_exact_i173_blob_proves_five_interface_controls():
    result = i174.inspect_source(_target_source())
    assert result.state == "EXACT_EXECUTOR_INTERFACE_PROVED"
    assert result.errors == ()
    assert result.git_blob_sha == i174.TARGET_GIT_BLOB_SHA
    assert result.executor_id == i174.EXPECTED_EXECUTOR_ID
    assert result.task_family == i174.EXPECTED_TASK_FAMILY
    assert result.acceptance_contract_id == i174.EXPECTED_ACCEPTANCE_CONTRACT_ID
    assert result.source_closure_complete is True
    assert result.requires_credentials is False
    assert result.requires_paid_account is False
    assert result.requires_new_spend is False
    assert result.quota_units_remaining is None
    assert result.rate_limit_per_minute is None
    assert result.provider_quota_not_applicable is True
    assert result.provider_rate_limit_not_applicable is True


def test_any_source_change_breaks_exact_blob_binding():
    result = i174.inspect_source(_target_source() + "\n# changed\n")
    assert result.state == "PASS_BLOCKED"
    assert "target_git_blob_sha_mismatch" in result.errors
    assert result.source_closure_complete is False


def test_forbidden_import_cannot_be_hidden_by_expected_sha_override():
    source = _target_source() + "\nimport socket\n"
    fake_sha = i174.git_blob_sha(source.encode("utf-8"))
    result = i174.inspect_source(source, expected_git_blob_sha=fake_sha)
    assert result.state == "PASS_BLOCKED"
    assert "target_git_blob_sha_mismatch" in result.errors or "nonwhitelisted_import:socket" in result.errors


def test_identity_constant_tamper_is_rejected():
    source = _target_source().replace(
        'EXECUTOR_ID = "owned-pc-structured-json-normalizer-v1"',
        'EXECUTOR_ID = "different-executor"',
    )
    result = i174.inspect_source(source)
    assert result.state == "PASS_BLOCKED"
    assert "target_git_blob_sha_mismatch" in result.errors
    assert "identity_constant_mismatch:EXECUTOR_ID" in result.errors
