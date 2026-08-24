from dataclasses import replace

import pytest

import i123_execution_backend_portfolio as i123
import resource_router as rr


def _task():
    return rr.TaskEconomics(
        task_id="i189",
        required_capabilities=frozenset({"extract", "validate"}),
        gross_payout_usd=1.0,
        minimum_success_probability=0.90,
        minimum_expected_margin_usd=0.01,
        minimum_expected_margin_ratio=0.01,
    )


def _backend():
    return rr.default_backend_families()[0]


def _evidence(backend_id="python_local"):
    return i123.BackendEvidence(
        backend_id=backend_id,
        provenance_class=i123.MEASURED,
        current_reproducible=True,
        non_synthetic=True,
        capacity_verified=True,
        policy_evidence_current=True,
    )


def test_valid_strict_boolean_evidence_can_reach_deterministic_route_ready():
    decision = i123.route_portfolio(_task(), (_backend(),), (_evidence(),))
    assert decision.state == "production_route_ready"
    assert decision.selected_backend_id == "python_local"
    assert decision.escalation_stage == "deterministic_first"
    assert decision.production_execution_enabled is False
    assert decision.value_movement_enabled is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("programmatic_access", "false"),
        ("policy_allowed", "false"),
        ("currently_available", 1),
        ("requires_credentials", 0),
        ("requires_paid_account", "no"),
        ("requires_new_spend", "false"),
        ("sunk_or_already_committed", "false"),
    ],
)
def test_backend_control_flags_require_exact_booleans(field, value):
    backend = replace(_backend(), **{field: value})
    with pytest.raises(ValueError, match=f"backend_{field}_must_be_boolean"):
        i123.route_portfolio(_task(), (backend,), (_evidence(),))


@pytest.mark.parametrize(
    "field,value",
    [
        ("current_reproducible", "false"),
        ("non_synthetic", 1),
        ("capacity_verified", "true"),
        ("policy_evidence_current", None),
        ("credentials_authorized", "false"),
        ("spend_authorized", 0),
        ("infrastructure_authorized", "yes"),
    ],
)
def test_evidence_and_authorization_flags_require_exact_booleans(field, value):
    evidence = replace(_evidence(), **{field: value})
    with pytest.raises(ValueError, match=f"evidence_{field}_must_be_boolean"):
        i123.route_portfolio(_task(), (_backend(),), (evidence,))


def test_ai_allowed_string_cannot_enable_ai_escalation():
    with pytest.raises(ValueError, match="ai_allowed_must_be_boolean"):
        i123.route_portfolio(_task(), (_backend(),), (_evidence(),), ai_allowed="false")


def test_duplicate_backend_ids_are_rejected_before_selection():
    backend = _backend()
    with pytest.raises(ValueError, match="duplicate backend: python_local"):
        i123.route_portfolio(_task(), (backend, backend), (_evidence(),))


def test_duplicate_evidence_ids_remain_rejected():
    evidence = _evidence()
    with pytest.raises(ValueError, match="duplicate backend evidence: python_local"):
        i123.route_portfolio(_task(), (_backend(),), (evidence, evidence))


def test_empty_evidence_identity_is_rejected():
    with pytest.raises(ValueError, match="backend_evidence_id_required"):
        i123.route_portfolio(_task(), (_backend(),), (_evidence(""),))
