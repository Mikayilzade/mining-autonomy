from dataclasses import replace
from local_execution_receipt import LocalExecutionPlan, LocalExecutionReceipt
from receipt_replay_calibration import (
    calibration_feedback_from_verified_receipt, verify_i060_receipt,
)

def _hash_plan(plan):
    from dataclasses import asdict
    from hashlib import sha256
    import json
    return sha256(json.dumps(asdict(plan), sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()

def plan():
    return LocalExecutionPlan(
        task_id="task-1", backend_id="python_local", provenance_binding_hash="p"*64,
        fixture_hash="f"*64, expected_output_hash="o"*64, router_marginal_cost_usd=0.05,
        max_cost_drift_usd=0.02,
    )

def receipt(p=None, energy=0.01, total=0.015):
    p = p or plan()
    return LocalExecutionReceipt(
        state="receipt_verified_inert", reasons=(), plan_hash=_hash_plan(p),
        task_id=p.task_id, backend_id=p.backend_id,
        provenance_binding_hash=p.provenance_binding_hash, fixture_hash=p.fixture_hash,
        output_hash=p.expected_output_hash, output_matches_expected=True,
        runtime_seconds=0.25, observed_energy_cost_usd=energy,
        observed_total_incremental_cost_usd=total,
        router_marginal_cost_usd=p.router_marginal_cost_usd,
    )

def reference():
    return {"backend_id": "python_local", "family": "deterministic_python", "notes": "exact-reference-fixture"}

def test_valid_receipt_replays_and_emits_runtime_and_energy_evidence():
    p=plan(); v=verify_i060_receipt(p, receipt(p))
    assert v.state == "verified_i060_replay"
    f=calibration_feedback_from_verified_receipt(v, reference(), observed_at="2026-08-21T07:45:00Z")
    assert f.state == "measured_feedback_ready"
    assert {x.parameter for x in f.evidence_records} == {"latency_seconds","electricity_per_task_usd"}
    assert all(x.source_kind == "measured_local" for x in f.evidence_records)
    assert all(x.source_content_digest == v.receipt_hash for x in f.evidence_records)

def test_unknown_energy_stays_unknown_and_only_runtime_is_reused():
    p=plan(); v=verify_i060_receipt(p, receipt(p, energy=None, total=None))
    assert v.state == "verified_i060_replay"
    assert v.energy_fact_verified is False
    f=calibration_feedback_from_verified_receipt(v, reference(), observed_at="2026-08-21T07:45:00Z")
    assert [x.parameter for x in f.evidence_records] == ["latency_seconds"]
    assert f.electricity_evidence_emitted is False

def test_plan_hash_tamper_fails_closed():
    p=plan(); v=verify_i060_receipt(p, replace(receipt(p), plan_hash="x"*64))
    assert v.state == "hold"
    assert "plan_hash_mismatch" in v.reasons

def test_provenance_or_fixture_drift_fails_closed():
    p=plan()
    v=verify_i060_receipt(p, replace(receipt(p), provenance_binding_hash="q"*64))
    assert "provenance_identity_mismatch" in v.reasons
    v2=verify_i060_receipt(p, replace(receipt(p), fixture_hash="z"*64))
    assert "fixture_identity_mismatch" in v2.reasons

def test_output_identity_mismatch_fails_closed():
    p=plan(); v=verify_i060_receipt(p, replace(receipt(p), output_hash="bad", output_matches_expected=False))
    assert v.state == "hold"
    assert "expected_output_identity_mismatch" in v.reasons

def test_cost_inconsistency_or_quote_excess_fails_closed():
    p=plan()
    v=verify_i060_receipt(p, replace(receipt(p), observed_energy_cost_usd=0.03, observed_total_incremental_cost_usd=0.02))
    assert "total_cost_below_energy_cost" in v.reasons
    v2=verify_i060_receipt(p, replace(receipt(p), observed_energy_cost_usd=0.04, observed_total_incremental_cost_usd=0.08))
    assert "observed_incremental_cost_exceeds_router_quote" in v2.reasons

def test_non_inert_receipt_fails_closed():
    p=plan(); v=verify_i060_receipt(p, replace(receipt(p), network_enabled=True))
    assert v.state == "hold"
    assert "receipt_not_inert" in v.reasons

def test_feedback_never_infers_reliability_quality_market_or_authorization():
    p=plan(); v=verify_i060_receipt(p, receipt(p))
    f=calibration_feedback_from_verified_receipt(v, reference(), observed_at="2026-08-21T07:45:00Z")
    assert f.reliability_inferred is False
    assert f.quality_probability_inferred is False
    assert f.market_demand_evidence is False
    assert f.execution_authorized is False

def test_unverified_replay_cannot_emit_calibration_evidence():
    p=plan(); v=verify_i060_receipt(p, replace(receipt(p), plan_hash="bad"))
    f=calibration_feedback_from_verified_receipt(v, reference(), observed_at="2026-08-21T07:45:00Z")
    assert f.state == "planning_only"
    assert f.evidence_records == ()

def test_reference_backend_mismatch_is_rejected():
    p=plan(); v=verify_i060_receipt(p, receipt(p))
    f=calibration_feedback_from_verified_receipt(v, {"backend_id":"owned_pc"}, observed_at="2026-08-21T07:45:00Z")
    assert f.state == "planning_only"
    assert "reference_backend_mismatch" in f.reasons
