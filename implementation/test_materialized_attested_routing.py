from dataclasses import asdict, replace
from datetime import datetime, timezone
from hashlib import sha256
import json

from evaluator import CapabilityProfile
from resource_router import ExecutionBackend
from resource_profile_evidence import (
    CRITICAL_PARAMETERS,
    attest_resource_profile,
    make_evidence,
    reference_backend_hash,
)
from resource_feedback_summary import (
    BackendEvidenceState,
    LatestParameterEvidenceRef,
    ResourceFeedbackHistorySnapshot,
)
from materialized_attested_routing import (
    materialized_routing_record,
    observe_and_route_with_materialized_resources,
    verify_materialized_routing_replay,
)

NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
POLICY = dict(
    rights_status="confirmed",
    tos_status="confirmed",
    automation_allowed="allowed",
    source_data_permission="confirmed",
)


def h(value):
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def backend():
    return ExecutionBackend(
        backend_id="python_local",
        family="deterministic_python",
        capabilities=frozenset({"extract"}),
        automation_role="autonomous",
        programmatic_access=True,
        policy_allowed=True,
        currently_available=True,
        requires_credentials=False,
        requires_paid_account=False,
        requires_new_spend=False,
        fixed_monthly_cost_usd=0.0,
        sunk_or_already_committed=True,
        allocation_basis_tasks_per_month=None,
        quota_units_monthly=None,
        quota_units_remaining=None,
        unit_name="task",
        marginal_cost_per_unit_usd=0.0,
        units_per_task=1.0,
        electricity_per_task_usd=0.01,
        external_api_per_task_usd=0.0,
        retry_failure_expected_cost_usd=0.01,
        maintenance_minutes_per_task=0.0,
        human_time_value_per_hour_usd=10.0,
        opportunity_cost_per_task_usd=0.0,
        latency_seconds=1.0,
        reliability_probability=0.995,
        quality_probability=0.995,
        max_parallelism=4,
        rate_limit_per_minute=120.0,
        notes="reference",
    )


def evidence_set(
    *,
    observed="2026-08-21T11:30:00Z",
    source_kind="measured_local",
    overrides=None,
):
    b = backend()
    ref = asdict(b)
    values = {parameter: ref[parameter] for parameter in CRITICAL_PARAMETERS}
    values.update(
        {
            "electricity_per_task_usd": 0.20,
            "latency_seconds": 2.5,
            "reliability_probability": 0.98,
            "quality_probability": 0.97,
        }
    )
    values.update(overrides or {})
    rh = reference_backend_hash(ref)
    return [
        make_evidence(
            evidence_id=f"e-{parameter}-{observed}",
            backend_id=b.backend_id,
            parameter=parameter,
            value=values[parameter],
            source_kind=source_kind,
            source_ref=f"fixture://{parameter}/{observed}",
            observed_at=observed,
            max_age_seconds=7200,
            reference_hash=rh,
            source_content_digest=None
            if source_kind == "user_declared"
            else "a" * 64,
        )
        for parameter in CRITICAL_PARAMETERS
    ]


def bundle(records, *, now=NOW):
    attestation = attest_resource_profile(asdict(backend()), records, now=now)
    assert attestation.state in {"calibrated_reproducible", "calibrated_declared"}
    return attestation.evidence_bundle_hash


def ref(parameter, evidence_hashes, bundle_hash):
    return LatestParameterEvidenceRef(
        "python_local",
        parameter,
        "2026-08-21T11:30:00Z",
        tuple(evidence_hashes),
        "exact_single_parameter",
        1,
        "1" * 64,
        "q1" * 32,
        bundle_hash,
    )


def snapshot(records, bundle_hash, *, selected="python_local"):
    target = next(x for x in records if x.parameter == "latency_seconds")
    state = BackendEvidenceState(
        "python_local",
        (ref("latency_seconds", [target.evidence_hash], bundle_hash),),
        1,
        1,
        "2026-08-21T11:30:00Z",
    )
    kwargs = dict(
        state="verified_history_snapshot",
        reasons=(),
        history_length=1,
        history_tip_hash="t" * 64,
        task_id="t1",
        platform="payanagent",
        external_id="t1",
        current_selected_backend_id=selected,
        latest_routing_hash="r" * 64,
        backend_states=(state,),
        routing_transitions=(),
        selected_backend_switch_count=0,
        selected_backend_oscillation_detected=False,
        parameter_churn_indicators=(),
        anomaly_indicators=(),
        limitations=("parameter_values_not_stored_in_i064_history",),
        snapshot_hash="",
    )
    draft = ResourceFeedbackHistorySnapshot(**kwargs)
    return replace(draft, snapshot_hash=h(draft.hash_body()))


def payload(title="extract data"):
    return {
        "id": "t1",
        "title": title,
        "bounty_usd": 5.0,
        "currency": "USD",
        "skills": ["extract"],
        "observed_at": "2026-08-21T12:00:00Z",
        "metadata": {
            **POLICY,
            "estimated_input_tokens": 1000,
            "estimated_output_tokens": 1000,
            "estimated_duration_seconds": 120,
            "estimate_confidence": 0.9,
            "external_cost_cap_usd": 0,
        },
    }


def run(records, *, evidence_bundle=None, snap=None, demand="open_paid_request"):
    bh = evidence_bundle or bundle(records)
    s = snap or snapshot(records, bh)
    return observe_and_route_with_materialized_resources(
        "payanagent",
        payload(),
        history_snapshot=s,
        reference_backends={"python_local": backend()},
        evidence_bundles={bh: records},
        now=NOW,
        demand_evidence_class=demand,
        capabilities=CapabilityProfile({"extract"}),
    )


def test_fresh_reproducible_materialization_routes_through_existing_attested_path():
    records = evidence_set()
    result = run(records)
    assert result.state == "route_dry_run"
    assert result.selected_backend_after == "python_local"
    assert result.selected_calibration_state == "calibrated_reproducible"
    assert result.materialization_state == "materialized_reproducible"
    assert result.history_tip_hash == "t" * 64
    assert result.materialization_hash
    assert verify_materialized_routing_replay(result)


def test_materialized_measurements_reprice_same_task_without_enabling_execution():
    records = evidence_set()
    result = run(records)
    drift = result.route_drifts[0]
    assert drift.backend_id == "python_local"
    assert drift.calibrated_marginal_cost_usd > drift.reference_marginal_cost_usd
    assert drift.calibrated_success_probability < drift.reference_success_probability
    assert drift.calibrated_latency_seconds > drift.reference_latency_seconds
    assert result.attested_observation.execution_enabled is False
    assert result.attested_observation.network_enabled is False


def test_upstream_demand_hold_precedes_resource_materialization():
    records = evidence_set()
    bh = bundle(records)
    s = snapshot(records, bh)
    result = observe_and_route_with_materialized_resources(
        "payanagent",
        payload(),
        history_snapshot=s,
        reference_backends={"python_local": backend()},
        evidence_bundles={bh: records},
        now=NOW,
        demand_evidence_class="listing_only",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "hold"
    assert result.upstream_state == "hold"
    assert result.materialization_hash is None
    assert result.attested_observation is None


def test_upstream_policy_reject_precedes_resource_materialization():
    records = evidence_set()
    bh = bundle(records)
    s = snapshot(records, bh)
    result = observe_and_route_with_materialized_resources(
        "payanagent",
        payload("spam automation"),
        history_snapshot=s,
        reference_backends={"python_local": backend()},
        evidence_bundles={bh: records},
        now=NOW,
        demand_evidence_class="open_paid_request",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "reject"
    assert result.materialization_hash is None


def test_user_declared_materialization_cannot_enter_reproducible_route_set():
    records = evidence_set(source_kind="user_declared")
    result = run(records)
    assert result.state == "hold"
    assert result.materialization_state == "materialized_with_declarations"
    assert "verified_current_resource_snapshot_unavailable" in result.reasons
    assert result.selected_backend_after is None


def test_stale_evidence_fails_closed_before_attested_routing():
    records = evidence_set(observed="2026-08-21T08:00:00Z")
    old_now = datetime(2026, 8, 21, 8, 30, tzinfo=timezone.utc)
    bh = bundle(records, now=old_now)
    target = next(x for x in records if x.parameter == "latency_seconds")
    state = BackendEvidenceState(
        "python_local",
        (
            LatestParameterEvidenceRef(
                "python_local",
                "latency_seconds",
                "2026-08-21T08:00:00Z",
                (target.evidence_hash,),
                "exact_single_parameter",
                1,
                "1" * 64,
                "q1" * 32,
                bh,
            ),
        ),
        1,
        1,
        "2026-08-21T08:00:00Z",
    )
    kwargs = dict(
        state="verified_history_snapshot",
        reasons=(),
        history_length=1,
        history_tip_hash="t" * 64,
        task_id="t1",
        platform="payanagent",
        external_id="t1",
        current_selected_backend_id="python_local",
        latest_routing_hash="r" * 64,
        backend_states=(state,),
        routing_transitions=(),
        selected_backend_switch_count=0,
        selected_backend_oscillation_detected=False,
        parameter_churn_indicators=(),
        anomaly_indicators=(),
        limitations=("parameter_values_not_stored_in_i064_history",),
        snapshot_hash="",
    )
    draft = ResourceFeedbackHistorySnapshot(**kwargs)
    s = replace(draft, snapshot_hash=h(draft.hash_body()))
    result = observe_and_route_with_materialized_resources(
        "payanagent",
        payload(),
        history_snapshot=s,
        reference_backends={"python_local": backend()},
        evidence_bundles={bh: records},
        now=NOW,
        demand_evidence_class="open_paid_request",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "hold"
    assert result.materialization_state == "hold_unresolved_evidence"
    assert result.attested_observation is None


def test_tampered_evidence_fails_exact_replay_binding():
    records = evidence_set()
    bh = bundle(records)
    target = next(x for x in records if x.parameter == "latency_seconds")
    tampered = list(records)
    tampered[tampered.index(target)] = replace(target, value=999.0)
    s = snapshot(records, bh)
    result = observe_and_route_with_materialized_resources(
        "payanagent",
        payload(),
        history_snapshot=s,
        reference_backends={"python_local": backend()},
        evidence_bundles={bh: tampered},
        now=NOW,
        demand_evidence_class="open_paid_request",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "hold"
    assert result.materialization_state == "hold_unresolved_evidence"
    assert result.selected_backend_after is None


def test_reference_backend_identity_mismatch_is_rejected():
    records = evidence_set()
    bh = bundle(records)
    s = snapshot(records, bh)
    wrong = replace(backend(), backend_id="other")
    try:
        observe_and_route_with_materialized_resources(
            "payanagent",
            payload(),
            history_snapshot=s,
            reference_backends={"python_local": wrong},
            evidence_bundles={bh: records},
            now=NOW,
            demand_evidence_class="open_paid_request",
            capabilities=CapabilityProfile({"extract"}),
        )
    except ValueError as exc:
        assert str(exc) == "reference_backend_mapping_identity_mismatch"
    else:
        raise AssertionError("expected identity mismatch")


def test_selected_backend_churn_is_surfaced_deterministically():
    records = evidence_set()
    bh = bundle(records)
    s = snapshot(records, bh, selected="legacy_backend")
    result = run(records, evidence_bundle=bh, snap=s)
    assert result.state == "route_dry_run"
    assert result.selected_backend_before == "legacy_backend"
    assert result.selected_backend_after == "python_local"
    assert result.selected_backend_changed is True


def test_exported_record_keeps_every_action_gate_off():
    records = evidence_set()
    result = run(records)
    record = materialized_routing_record(result)
    assert record["dry_run_only"] is True
    assert record["execution_enabled"] is False
    assert record["network_enabled"] is False
    assert record["credentials_enabled"] is False
    assert record["submission_enabled"] is False
    assert record["value_movement_enabled"] is False
