import i125_resource_promotability_audit as m


def test_audit_covers_all_critical_parameters():
    audit = m.audit_python_local_promotability()
    assert {x.parameter for x in audit.parameter_results} == set(m.CRITICAL_PARAMETERS)


def test_current_model_detects_declaration_only_strict_promotion_blocker():
    audit = m.audit_python_local_promotability()
    assert audit.model_defect_detected is True
    assert audit.state == "MODEL_DEFECT_BLOCKS_STRICT_PROMOTION"
    assert "sunk_or_already_committed" in audit.declaration_only_parameters
    assert "sunk_or_already_committed" in audit.strict_reproducible_impossible_parameters


def test_audit_does_not_widen_execution_or_production_selection():
    audit = m.audit_python_local_promotability()
    assert audit.production_selection_widened is False
    assert audit.execution_enabled is False
    assert audit.network_enabled is False
    assert audit.value_movement_enabled is False


def test_recommendation_prefers_narrow_reproducible_invariant_not_arbitrary_declaration_widening():
    audit = m.audit_python_local_promotability()
    assert "Do not weaken I123" in audit.recommended_fix
    assert "hash-bound" in audit.recommended_fix
    assert "electricity" in audit.recommended_fix
