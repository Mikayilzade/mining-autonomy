import i169_owned_pc_i050_i066_readiness as i169


def _i168_result():
    return {
        "state": "PARTIAL_I050_EVIDENCE_READY",
        "backend_id": "owned_pc",
        "emitted_parameters": list(i169.MEASURED_PARAMETERS),
        "i166_i167_source_binding_valid": True,
        "reference_backend_hash": "a" * 64,
        "i050_source_blob_sha": i169.I050_RESOURCE_PROFILE_BLOB_SHA,
        "i066_source_blob_sha": i169.I066_MATERIALIZATION_BLOB_SHA,
    }


def _controls(source_kind="system_probe"):
    values = {
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "fixed_monthly_cost_usd": 0.0,
        "sunk_or_already_committed": True,
        "quota_units_remaining": None,
        "rate_limit_per_minute": None,
    }
    rows = []
    for name in i169.CONTROL_PARAMETERS:
        kind = source_kind
        digest = "b" * 64 if kind in i169.REPRODUCIBLE_SOURCE_KINDS else None
        rows.append(i169.build_control_evidence(
            parameter=name,
            value=values[name],
            source_kind=kind,
            source_ref=f"local-proof:{name}",
            observed_at="2026-08-24T07:45:00Z",
            max_age_seconds=86400,
            reference_backend_hash="a" * 64,
            source_content_digest=digest,
        ))
    return rows


def test_complete_reproducible_controls_ready_only_for_actual_i050():
    result = i169.evaluate_readiness(_i168_result(), _controls())
    assert result.state == "READY_FOR_EXACT_I050_EXECUTION"
    assert result.errors == ()
    assert result.complete_parameter_set is True
    assert result.all_control_sources_reproducible is True
    assert result.contains_user_declaration is False
    assert result.exact_i050_execution_allowed is True
    assert result.exact_i066_execution_allowed is False
    assert result.i123_promotion_allowed is False


def test_user_declarations_are_not_relabelled_reproducible():
    result = i169.evaluate_readiness(_i168_result(), _controls("user_declared"))
    assert result.state == "COMPLETE_DECLARED_BUNDLE_BLOCKED_FOR_I123"
    assert result.errors == ()
    assert result.complete_parameter_set is True
    assert result.contains_user_declaration is True
    assert result.all_control_sources_reproducible is False
    assert result.exact_i050_execution_allowed is False
    assert result.i123_promotion_allowed is False


def test_missing_control_fact_blocks_i050():
    rows = _controls()[:-1]
    result = i169.evaluate_readiness(_i168_result(), rows)
    assert result.state == "PASS_BLOCKED"
    assert "missing_control_parameter:rate_limit_per_minute" in result.errors
    assert "complete_i050_parameter_set_absent" in result.errors
    assert result.exact_i050_execution_allowed is False


def test_tampered_control_hash_fails_closed():
    rows = _controls()
    broken = rows[0]
    rows[0] = i169.ControlEvidence(**{**broken.__dict__, "evidence_hash": "0" * 64})
    result = i169.evaluate_readiness(_i168_result(), rows)
    assert result.state == "PASS_BLOCKED"
    assert f"evidence_hash_mismatch:{broken.parameter}" in result.errors


def test_i050_or_i066_source_drift_blocks_handoff():
    source = _i168_result()
    source["i050_source_blob_sha"] = "0" * 40
    source["i066_source_blob_sha"] = "1" * 40
    result = i169.evaluate_readiness(source, _controls())
    assert result.state == "PASS_BLOCKED"
    assert "i050_source_binding_drift" in result.errors
    assert "i066_source_binding_drift" in result.errors


def test_authorization_implications_are_preserved_not_consumed():
    rows = _controls()
    replacements = {
        "requires_credentials": True,
        "requires_paid_account": True,
        "requires_new_spend": True,
        "fixed_monthly_cost_usd": 10.0,
        "sunk_or_already_committed": False,
    }
    rebuilt = []
    for row in rows:
        value = replacements.get(row.parameter, row.value)
        rebuilt.append(i169.build_control_evidence(
            parameter=row.parameter,
            value=value,
            source_kind=row.source_kind,
            source_ref=row.source_ref,
            observed_at=row.observed_at,
            max_age_seconds=row.max_age_seconds,
            reference_backend_hash=row.reference_backend_hash,
            source_content_digest=row.source_content_digest,
        ))
    result = i169.evaluate_readiness(_i168_result(), rebuilt)
    assert result.state == "READY_FOR_EXACT_I050_EXECUTION"
    assert "credentials_authorization_required" in result.authorization_implications
    assert "paid_account_evidence_or_authorization_required" in result.authorization_implications
    assert "new_spend_authorization_required" in result.authorization_implications
    assert "fixed_cost_allocation_basis_required_downstream" in result.authorization_implications
    assert result.exact_i066_execution_allowed is False
    assert result.i123_promotion_allowed is False
