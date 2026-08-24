import i175_i171_production_scope_binding as i175


def _proof():
    return {
        "state": "EXACT_EXECUTOR_INTERFACE_PROVED",
        "target_path": i175.TARGET_PATH,
        "git_blob_sha": i175.TARGET_GIT_BLOB_SHA,
        "source_sha256": "a" * 64,
        "executor_id": i175.EXECUTOR_ID,
        "task_family": i175.TASK_FAMILY,
        "acceptance_contract_id": i175.ACCEPTANCE_CONTRACT_ID,
        "source_closure_complete": True,
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "quota_units_remaining": None,
        "rate_limit_per_minute": None,
        "network_dependency_absent": True,
        "credential_dependency_absent": True,
        "paid_service_dependency_absent": True,
        "provider_quota_not_applicable": True,
        "provider_rate_limit_not_applicable": True,
    }


def test_exact_proof_binds_i171_production_scope_and_five_facts():
    result = i175.bind_interface_proof(_proof())
    assert result.state == "PRODUCTION_INTERFACE_CONTROLS_READY"
    assert result.errors == ()
    assert result.production_executor_scope_bound is True
    assert result.i171_result["state"] == "PRODUCTION_EXECUTOR_SCOPE_BOUND"
    assert result.i171_result["production_interface_evidence_ready"] is True
    assert tuple(row.parameter for row in result.interface_facts) == i175.INTERFACE_PARAMETERS
    assert {row.parameter: row.value for row in result.interface_facts} == {
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "quota_units_remaining": None,
        "rate_limit_per_minute": None,
    }
    assert all(row.source_kind == "system_probe" for row in result.interface_facts)
    assert result.i050_records_created is False
    assert result.i123_promotion_allowed is False


def test_source_sha_or_blob_tamper_blocks_scope_binding():
    proof = _proof()
    proof["git_blob_sha"] = "0" * 40
    proof["source_sha256"] = "bad"
    result = i175.bind_interface_proof(proof)
    assert result.state == "PASS_BLOCKED"
    assert "target_git_blob_sha_mismatch" in result.errors
    assert "source_sha256_required" in result.errors
    assert result.interface_facts == ()


def test_missing_interface_proof_flag_blocks_binding():
    proof = _proof()
    proof["provider_quota_not_applicable"] = False
    result = i175.bind_interface_proof(proof)
    assert result.state == "PASS_BLOCKED"
    assert "interface_proof_missing:provider_quota_not_applicable" in result.errors


def test_benchmark_or_other_executor_identity_cannot_substitute():
    proof = _proof()
    proof["executor_id"] = "i163-fixed-json-transform-session-v1"
    proof["task_family"] = "benchmark_only"
    result = i175.bind_interface_proof(proof)
    assert result.state == "PASS_BLOCKED"
    assert "executor_id_mismatch" in result.errors
    assert "task_family_mismatch" in result.errors
