import i171_owned_pc_execution_scope_gate as i171


def _blob(path="implementation/i163_user_pc_benchmark_session.py"):
    return i171.SourceBlob(path=path, git_blob_sha="a" * 40)


def _scope(kind=i171.BENCHMARK_SCOPE):
    return i171.ExecutionScope(
        executor_id="fixed-local-json-transform",
        scope_kind=kind,
        source_blobs=(_blob(),),
        source_closure_complete=True,
        acceptance_contract_id="contract-v1" if kind == i171.PRODUCTION_SCOPE else None,
        task_family="deterministic-transform" if kind == i171.PRODUCTION_SCOPE else None,
        interface_probe_id="local-static-interface-proof-v1",
        network_dependency_absent=True,
        credential_dependency_absent=True,
        paid_service_dependency_absent=True,
        provider_quota_not_applicable=True,
        provider_rate_limit_not_applicable=True,
    )


def test_benchmark_scope_is_bound_but_never_promoted_to_production():
    result = i171.evaluate_scope(_scope())
    assert result.state == "BENCHMARK_SCOPE_BOUND_NOT_PRODUCTION"
    assert result.errors == ()
    assert result.source_closure_digest
    assert result.interface_parameters_bound == i171.INTERFACE_PARAMETERS
    assert result.production_interface_evidence_ready is False
    assert result.benchmark_evidence_reuse_for_production_allowed is False
    assert result.exact_task_executor_required is True
    assert result.i050_records_created is False
    assert result.i123_promotion_allowed is False


def test_production_scope_requires_acceptance_contract_and_task_family():
    scope = _scope(i171.PRODUCTION_SCOPE)
    broken = i171.ExecutionScope(**{**scope.__dict__, "acceptance_contract_id": None, "task_family": None})
    result = i171.evaluate_scope(broken)
    assert result.state == "PASS_BLOCKED"
    assert "production_acceptance_contract_required" in result.errors
    assert "production_task_family_required" in result.errors
    assert result.production_interface_evidence_ready is False


def test_complete_production_scope_can_only_reach_scope_bound_gate():
    result = i171.evaluate_scope(_scope(i171.PRODUCTION_SCOPE))
    assert result.state == "PRODUCTION_EXECUTOR_SCOPE_BOUND"
    assert result.errors == ()
    assert result.production_interface_evidence_ready is True
    assert result.benchmark_evidence_reuse_for_production_allowed is False
    assert result.exact_task_executor_required is False
    assert result.i050_records_created is False
    assert result.i123_promotion_allowed is False


def test_unproved_interface_dependency_fails_closed():
    scope = _scope(i171.PRODUCTION_SCOPE)
    broken = i171.ExecutionScope(**{
        **scope.__dict__,
        "credential_dependency_absent": False,
        "provider_quota_not_applicable": False,
        "network_dependency_absent": False,
    })
    result = i171.evaluate_scope(broken)
    assert result.state == "PASS_BLOCKED"
    assert "network_dependency_not_absent" in result.errors
    assert "interface_fact_not_proved:requires_credentials" in result.errors
    assert "interface_fact_not_proved:quota_units_remaining" in result.errors
    assert result.interface_parameters_bound == ()


def test_source_closure_must_be_complete_and_git_bound():
    scope = _scope(i171.PRODUCTION_SCOPE)
    broken = i171.ExecutionScope(**{
        **scope.__dict__,
        "source_closure_complete": False,
        "source_blobs": (i171.SourceBlob(path="x.py", git_blob_sha="not-a-sha"),),
    })
    result = i171.evaluate_scope(broken)
    assert result.state == "PASS_BLOCKED"
    assert "source_closure_not_complete" in result.errors
    assert "invalid_source_blob_binding" in result.errors
    assert result.source_closure_digest is None


def test_duplicate_paths_and_unknown_scope_fail_closed():
    scope = _scope()
    broken = i171.ExecutionScope(**{
        **scope.__dict__,
        "scope_kind": "mystery",
        "source_blobs": (_blob("same.py"), _blob("same.py")),
    })
    result = i171.evaluate_scope(broken)
    assert result.state == "PASS_BLOCKED"
    assert "unsupported_scope_kind" in result.errors
    assert "duplicate_source_path" in result.errors
