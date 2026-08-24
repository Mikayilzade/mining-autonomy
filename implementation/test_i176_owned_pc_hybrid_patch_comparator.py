import i176_owned_pc_hybrid_patch_comparator as i176


def _sources(accounting_kind="user_declared"):
    result = {name: "system_probe" for name in i176.CRITICAL_PARAMETERS}
    for name in i176.ACCOUNTING_PARAMETERS:
        result[name] = accounting_kind
    return result


def _candidate(**overrides):
    base = dict(
        backend_id="owned_pc",
        backend_family="owned_pc",
        i050_attestation_state="calibrated_declared",
        source_kinds=_sources(),
        i172_state="NARROW_HYBRID_REVIEW_READY",
        i172_review_contract_digest="a" * 64,
        non_synthetic=True,
        capacity_verified=True,
        policy_evidence_current=True,
    )
    base.update(overrides)
    return i176.Candidate(**base)


def test_exact_two_accounting_declarations_are_only_hypothetical_difference():
    result = i176.compare(_candidate())
    assert result.state == "NARROW_HYBRID_WOULD_BE_ELIGIBLE_IF_PATCH_APPROVED"
    assert result.strict_current_path_ready is False
    assert result.narrow_hybrid_shape_valid is True
    assert result.would_be_eligible_under_proposal is True
    assert set(result.declaration_parameters) == set(i176.ACCOUNTING_PARAMETERS)
    assert result.widens_non_owned_pc is False
    assert result.widens_declaration_scope is False
    assert result.bypasses_authorization is False
    assert result.policy_patch_applied is False
    assert result.i123_promotion_performed is False


def test_strict_reproducible_path_remains_unchanged():
    result = i176.compare(_candidate(
        i050_attestation_state="calibrated_reproducible",
        source_kinds=_sources("system_probe"),
        i172_state=None,
        i172_review_contract_digest=None,
    ))
    assert result.state == "STRICT_PATH_UNCHANGED"
    assert result.strict_current_path_ready is True
    assert result.would_be_eligible_under_proposal is False


def test_other_backend_cannot_use_owned_pc_exception():
    result = i176.compare(_candidate(backend_id="python_local", backend_family="deterministic_python"))
    assert result.state == "PASS_BLOCKED"
    assert result.narrow_hybrid_shape_valid is False
    assert result.would_be_eligible_under_proposal is False


def test_declaration_outside_two_accounting_fields_is_rejected():
    sources = _sources()
    sources["requires_credentials"] = "user_declared"
    result = i176.compare(_candidate(source_kinds=sources))
    assert result.state == "PASS_BLOCKED"
    assert "declaration_outside_accounting_scope:requires_credentials" in result.errors
    assert result.would_be_eligible_under_proposal is False


def test_current_non_synthetic_capacity_policy_gates_are_preserved():
    for field, blocker in (
        ("non_synthetic", "backend_evidence_synthetic"),
        ("capacity_verified", "backend_capacity_not_verified"),
        ("policy_evidence_current", "backend_policy_evidence_not_current"),
    ):
        result = i176.compare(_candidate(**{field: False}))
        assert result.state == "HYBRID_SHAPE_VALID_BUT_EXISTING_GATE_BLOCKS"
        assert blocker in result.preserved_blockers
        assert result.would_be_eligible_under_proposal is False


def test_credentials_spend_and_paid_account_authorization_are_not_bypassed():
    result = i176.compare(_candidate(
        backend_requires_credentials=True,
        backend_requires_paid_account=True,
        backend_requires_new_spend=True,
        credentials_authorized=False,
        spend_authorized=False,
    ))
    assert result.state == "HYBRID_SHAPE_VALID_BUT_EXISTING_GATE_BLOCKS"
    assert "credentials_not_authorized" in result.preserved_blockers
    assert "paid_account_not_authorized" in result.preserved_blockers
    assert "new_spend_not_authorized" in result.preserved_blockers
    assert result.would_be_eligible_under_proposal is False
    assert result.bypasses_authorization is False


def test_missing_i172_binding_blocks_hybrid_shape():
    result = i176.compare(_candidate(i172_review_contract_digest=None))
    assert result.state == "PASS_BLOCKED"
    assert result.narrow_hybrid_shape_valid is False
