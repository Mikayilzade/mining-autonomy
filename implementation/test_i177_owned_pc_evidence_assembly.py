import copy

import i177_owned_pc_evidence_assembly as i177


def _i168():
    return {
        "state": "PARTIAL_I050_EVIDENCE_READY",
        "backend_id": "owned_pc",
        "emitted_parameters": list(i177.i169.MEASURED_PARAMETERS),
        "i166_i167_source_binding_valid": True,
        "reference_backend_hash": "a" * 64,
        "i050_source_blob_sha": i177.i169.I050_RESOURCE_PROFILE_BLOB_SHA,
        "i066_source_blob_sha": i177.i169.I066_MATERIALIZATION_BLOB_SHA,
    }


def _i175():
    values = {
        "requires_credentials": False,
        "requires_paid_account": False,
        "requires_new_spend": False,
        "quota_units_remaining": None,
        "rate_limit_per_minute": None,
    }
    return {
        "state": "PRODUCTION_INTERFACE_CONTROLS_READY",
        "production_executor_scope_bound": True,
        "i050_records_created": False,
        "i123_promotion_allowed": False,
        "interface_facts": [
            {
                "parameter": name,
                "value": values[name],
                "source_kind": "system_probe",
                "source_ref": "i171-scope:" + "b" * 64,
                "source_content_digest": "c" * 64,
            }
            for name in i177.INTERFACE_PARAMETERS
        ],
    }


def _accounting(kind="user_declared"):
    digest = None if kind == "user_declared" else "d" * 64
    return (
        i177.AccountingEvidenceInput(
            parameter="fixed_monthly_cost_usd",
            value=0.0,
            source_kind=kind,
            source_ref="owner-accounting:fixed-cost-2026-08-24",
            observed_at="2026-08-24T08:30:00Z",
            max_age_seconds=2592000,
            source_content_digest=digest,
        ),
        i177.AccountingEvidenceInput(
            parameter="sunk_or_already_committed",
            value=True,
            source_kind=kind,
            source_ref="owner-accounting:sunk-classification-2026-08-24",
            observed_at="2026-08-24T08:30:00Z",
            max_age_seconds=2592000,
            source_content_digest=digest,
        ),
    )


def test_declared_accounting_reaches_only_declared_boundary():
    result = i177.assemble_for_i169(
        _i168(), _i175(), _accounting(), observed_at="2026-08-24T08:30:00Z"
    )
    assert result.state == "ASSEMBLED_DECLARED_ACCOUNTING_BOUNDARY"
    assert result.errors == ()
    assert result.declared_accounting_boundary_reached is True
    assert result.strict_i050_execution_ready is False
    assert result.i169_result["state"] == "COMPLETE_DECLARED_BUNDLE_BLOCKED_FOR_I123"
    assert result.i169_result["i123_promotion_allowed"] is False
    assert result.i050_executed is False
    assert result.i066_executed is False
    assert result.i123_promotion_performed is False
    assert len(result.control_records) == 7


def test_reproducible_accounting_can_reach_strict_i050_readiness_only():
    result = i177.assemble_for_i169(
        _i168(), _i175(), _accounting("provider_first_party"),
        observed_at="2026-08-24T08:30:00Z",
    )
    assert result.state == "ASSEMBLED_READY_FOR_EXACT_I050"
    assert result.errors == ()
    assert result.strict_i050_execution_ready is True
    assert result.declared_accounting_boundary_reached is False
    assert result.i169_result["state"] == "READY_FOR_EXACT_I050_EXECUTION"
    assert result.i169_result["exact_i050_execution_allowed"] is True
    assert result.i169_result["exact_i066_execution_allowed"] is False
    assert result.i169_result["i123_promotion_allowed"] is False


def test_missing_or_placeholder_accounting_fails_closed():
    rows = list(_accounting())
    rows[0] = i177.AccountingEvidenceInput(
        parameter="fixed_monthly_cost_usd",
        value=0.0,
        source_kind="user_declared",
        source_ref="test-fixture:zero-cost",
        observed_at="2026-08-24T08:30:00Z",
        max_age_seconds=2592000,
    )
    result = i177.assemble_for_i169(
        _i168(), _i175(), tuple(rows[:-1]), observed_at="2026-08-24T08:30:00Z"
    )
    assert result.state == "PASS_BLOCKED"
    assert "accounting_source_ref_invalid:fixed_monthly_cost_usd" in result.errors
    assert "missing_accounting_parameter:sunk_or_already_committed" in result.errors
    assert result.control_records == ()
    assert result.i169_result is None


def test_i175_must_be_exact_production_scope_and_complete():
    source = _i175()
    source["production_executor_scope_bound"] = False
    source["interface_facts"] = source["interface_facts"][:-1]
    result = i177.assemble_for_i169(
        _i168(), source, _accounting(), observed_at="2026-08-24T08:30:00Z"
    )
    assert result.state == "PASS_BLOCKED"
    assert "i175_production_executor_scope_not_bound" in result.errors
    assert "missing_i175_interface_parameter:rate_limit_per_minute" in result.errors


def test_i168_source_or_measured_set_drift_blocks_assembly():
    source = _i168()
    source["i166_i167_source_binding_valid"] = False
    source["emitted_parameters"] = source["emitted_parameters"][:-1]
    source["i050_source_blob_sha"] = "0" * 40
    result = i177.assemble_for_i169(
        source, _i175(), _accounting(), observed_at="2026-08-24T08:30:00Z"
    )
    assert result.state == "PASS_BLOCKED"
    assert "i168_real_source_binding_required" in result.errors
    assert "i168_measured_parameter_set_drift" in result.errors
    assert "i168_i050_source_binding_drift" in result.errors


def test_tampered_interface_source_class_or_digest_blocks_assembly():
    source = copy.deepcopy(_i175())
    source["interface_facts"][0]["source_kind"] = "user_declared"
    source["interface_facts"][1]["source_content_digest"] = "short"
    result = i177.assemble_for_i169(
        _i168(), source, _accounting(), observed_at="2026-08-24T08:30:00Z"
    )
    assert result.state == "PASS_BLOCKED"
    assert "i175_interface_not_system_probe:requires_credentials" in result.errors
    assert "i175_interface_source_digest_invalid:requires_paid_account" in result.errors


def test_invalid_time_or_age_never_reaches_i169():
    rows = list(_accounting())
    rows[0] = i177.AccountingEvidenceInput(
        **{**rows[0].__dict__, "max_age_seconds": 0}
    )
    result = i177.assemble_for_i169(
        _i168(), _i175(), tuple(rows), observed_at="2026-08-24T08:30:00"
    )
    assert result.state == "PASS_BLOCKED"
    assert "accounting_positive_max_age_required:fixed_monthly_cost_usd" in result.errors
    assert "interface_observed_at_must_be_utc" in result.errors
