import i172_owned_pc_hybrid_evidence_contract as i172


def _refs(accounting_kind="user_declared"):
    rows = []
    for parameter in i172.CRITICAL_PARAMETERS:
        if parameter in i172.ACCOUNTING_DECLARATION_PARAMETERS:
            kind = accounting_kind
            digest = None if kind == "user_declared" else "a" * 64
        else:
            kind = "system_probe"
            digest = "b" * 64
        rows.append(i172.EvidenceRef(
            backend_id="owned_pc",
            parameter=parameter,
            source_kind=kind,
            source_ref=f"proof:{parameter}",
            source_content_digest=digest,
        ))
    return rows


def test_narrow_hybrid_allows_only_two_accounting_declarations():
    result = i172.evaluate_hybrid_contract("owned_pc", _refs())
    assert result.state == "NARROW_HYBRID_REVIEW_READY"
    assert result.errors == ()
    assert result.declaration_parameters == i172.ACCOUNTING_DECLARATION_PARAMETERS
    assert result.complete_parameter_set is True
    assert result.declaration_scope_narrow is True
    assert result.all_non_accounting_reproducible is True
    assert result.review_contract_digest
    assert result.i050_change_performed is False
    assert result.i123_change_performed is False
    assert result.i123_promotion_allowed is False
    assert result.production_execution_enabled is False


def test_strict_reproducible_accounting_needs_no_hybrid_exception():
    result = i172.evaluate_hybrid_contract("owned_pc", _refs("provider_first_party"))
    assert result.state == "STRICT_REPRODUCIBLE_PATH_AVAILABLE_NO_HYBRID_NEEDED"
    assert result.errors == ()
    assert result.declaration_parameters == ()
    assert result.i123_promotion_allowed is False


def test_user_declaration_on_dynamic_or_interface_fact_is_rejected():
    rows = _refs()
    target = next(i for i, row in enumerate(rows) if row.parameter == "requires_credentials")
    row = rows[target]
    rows[target] = i172.EvidenceRef(
        backend_id=row.backend_id,
        parameter=row.parameter,
        source_kind="user_declared",
        source_ref=row.source_ref,
        source_content_digest=None,
    )
    result = i172.evaluate_hybrid_contract("owned_pc", rows)
    assert result.state == "PASS_BLOCKED"
    assert "non_accounting_must_be_reproducible:requires_credentials:user_declared" in result.errors
    assert "declaration_outside_accounting_scope:requires_credentials" in result.errors
    assert result.i123_promotion_allowed is False


def test_contract_cannot_apply_to_other_backend_family():
    rows = _refs()
    rows[0] = i172.EvidenceRef(
        backend_id="python_local",
        parameter=rows[0].parameter,
        source_kind=rows[0].source_kind,
        source_ref=rows[0].source_ref,
        source_content_digest=rows[0].source_content_digest,
    )
    result = i172.evaluate_hybrid_contract("python_local", rows)
    assert result.state == "PASS_BLOCKED"
    assert "hybrid_contract_owned_pc_only" in result.errors
    assert any(error.startswith("evidence_backend_not_owned_pc:") for error in result.errors)


def test_missing_or_duplicate_parameter_fails_closed():
    rows = _refs()
    rows = rows[:-1] + [rows[0]]
    result = i172.evaluate_hybrid_contract("owned_pc", rows)
    assert result.state == "PASS_BLOCKED"
    assert any(error.startswith("duplicate_parameter:") for error in result.errors)
    assert "missing_parameter:rate_limit_per_minute" in result.errors
    assert result.review_contract_digest is None


def test_review_contract_cannot_consume_any_authorization():
    result = i172.evaluate_hybrid_contract(
        "owned_pc",
        _refs(),
        credentials_authorized=True,
        spend_authorized=True,
        infrastructure_authorized=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "hybrid_contract_cannot_consume_credentials_authorization" in result.errors
    assert "hybrid_contract_cannot_consume_spend_authorization" in result.errors
    assert "hybrid_contract_cannot_consume_infrastructure_authorization" in result.errors
    assert result.credentials_authorized is False
    assert result.spend_authorized is False
    assert result.infrastructure_authorized is False
    assert result.i123_promotion_allowed is False


def test_reproducible_source_requires_digest():
    rows = _refs()
    row = rows[0]
    rows[0] = i172.EvidenceRef(
        backend_id=row.backend_id,
        parameter=row.parameter,
        source_kind=row.source_kind,
        source_ref=row.source_ref,
        source_content_digest=None,
    )
    result = i172.evaluate_hybrid_contract("owned_pc", rows)
    assert result.state == "PASS_BLOCKED"
    assert f"reproducible_digest_required:{row.parameter}" in result.errors
