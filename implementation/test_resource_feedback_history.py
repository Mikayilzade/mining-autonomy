from dataclasses import dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json

from feedback_attested_observation import FeedbackAttestedTaskUpdate
from receipt_replay_calibration import CalibrationFeedback
from resource_feedback_history import append_resource_feedback_history, verify_resource_feedback_history
from resource_profile_evidence import ResourceEvidence

NOW = datetime(2026, 8, 21, 10, 45, tzinfo=timezone.utc)


def h(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


@dataclass(frozen=True)
class DummyRouting:
    state: str
    selected_backend_id: str
    marginal_cost_usd: float


def evidence(*, evidence_id="e1", parameter="electricity_per_task_usd", observed_at="2026-08-21T10:40:00Z"):
    e = ResourceEvidence(
        evidence_id=evidence_id, backend_id="python_local", parameter=parameter, value=0.01,
        source_kind="measured_local", source_ref=f"receipt:{evidence_id}", observed_at=observed_at,
        max_age_seconds=3600, reference_backend_hash="a"*64, source_content_digest="b"*64,
    )
    return replace(e, evidence_hash=e.computed_hash())


def feedback(e, *, receipt="r1"):
    return CalibrationFeedback(
        state="measured_feedback_ready", reasons=(), backend_id="python_local",
        receipt_hash=h(receipt), evidence_records=(e,), runtime_evidence_emitted=False,
        electricity_evidence_emitted=e.parameter == "electricity_per_task_usd",
        total_incremental_cost_observed_usd=0.01,
    )


def update(*, before_routing="c"*64, after_cost=0.01, receipt_hash=None, evidence_hashes=None,
           provenance="d"*64, before_bundle="e"*64, after_bundle="f"*64):
    routing = DummyRouting("route_dry_run", "python_local", after_cost)
    return FeedbackAttestedTaskUpdate(
        state="feedback_refreshed_route_dry_run", reasons=(), platform="payanagent",
        external_id="task-1", task_id="task-1", target_backend_id="python_local",
        original_observation_hash="1"*64, original_task_economics_hash="2"*64,
        original_routing_hash=before_routing,
        feedback_receipt_hash=receipt_hash or h("r1"),
        feedback_evidence_hashes=evidence_hashes or (),
        replaced_parameters=("electricity_per_task_usd",),
        before_target_evidence_bundle_hash=before_bundle,
        after_target_evidence_bundle_hash=after_bundle,
        before_selected_backend_id="alternate", after_selected_backend_id="python_local",
        route_delta={"before_marginal_cost_usd": .4, "after_marginal_cost_usd": after_cost},
        provenance_binding_hash=provenance, original_observation=None,
        refreshed_target_attestation=None, refreshed_routing=routing,
    )


def test_first_entry_binds_receipt_evidence_and_routing_and_is_inert():
    e = evidence()
    fb = feedback(e)
    u = update(receipt_hash=fb.receipt_hash, evidence_hashes=(e.evidence_hash,))
    result = append_resource_feedback_history([], u, fb, now=NOW)
    assert result.state == "history_appended"
    assert result.entry.sequence == 1 and result.entry.previous_entry_hash == "GENESIS"
    assert result.entry.feedback_receipt_hash == fb.receipt_hash
    assert result.entry.feedback_evidence_hashes == (e.evidence_hash,)
    assert result.entry.execution_enabled is False and result.entry.network_enabled is False


def test_second_entry_requires_exact_prior_after_routing_hash():
    e1 = evidence()
    fb1 = feedback(e1)
    u1 = update(receipt_hash=fb1.receipt_hash, evidence_hashes=(e1.evidence_hash,))
    first = append_resource_feedback_history([], u1, fb1, now=NOW).entry
    after_hash = h({"state":"route_dry_run","selected_backend_id":"python_local","marginal_cost_usd":0.01})
    e2 = evidence(evidence_id="e2", observed_at="2026-08-21T10:42:00Z")
    fb2 = feedback(e2, receipt="r2")
    u2 = update(before_routing=after_hash, after_cost=.005, receipt_hash=fb2.receipt_hash,
                evidence_hashes=(e2.evidence_hash,), before_bundle="f"*64, after_bundle="9"*64, provenance="8"*64)
    second = append_resource_feedback_history([first], u2, fb2, now=NOW)
    assert second.state == "history_appended" and second.entry.sequence == 2
    ok, reasons = verify_resource_feedback_history([first, second.entry])
    assert ok and not reasons


def test_out_of_order_routing_is_rejected():
    e1 = evidence(); fb1 = feedback(e1)
    u1 = update(receipt_hash=fb1.receipt_hash, evidence_hashes=(e1.evidence_hash,))
    first = append_resource_feedback_history([], u1, fb1, now=NOW).entry
    e2 = evidence(evidence_id="e2", observed_at="2026-08-21T10:42:00Z"); fb2 = feedback(e2, receipt="r2")
    u2 = update(before_routing="0"*64, receipt_hash=fb2.receipt_hash, evidence_hashes=(e2.evidence_hash,))
    result = append_resource_feedback_history([first], u2, fb2, now=NOW)
    assert result.state == "hold" and "history_append_out_of_order_routing" in result.reasons


def test_replayed_receipt_is_rejected_even_with_new_evidence():
    e1 = evidence(); fb1 = feedback(e1)
    u1 = update(receipt_hash=fb1.receipt_hash, evidence_hashes=(e1.evidence_hash,))
    first = append_resource_feedback_history([], u1, fb1, now=NOW).entry
    after_hash = h({"state":"route_dry_run","selected_backend_id":"python_local","marginal_cost_usd":0.01})
    e2 = evidence(evidence_id="e2", observed_at="2026-08-21T10:42:00Z")
    fb2 = feedback(e2, receipt="r1")
    u2 = update(before_routing=after_hash, receipt_hash=fb2.receipt_hash, evidence_hashes=(e2.evidence_hash,))
    result = append_resource_feedback_history([first], u2, fb2, now=NOW)
    assert result.state == "hold" and "history_replayed_receipt" in result.reasons


def test_stale_parameter_regression_is_rejected():
    e1 = evidence(observed_at="2026-08-21T10:40:00Z"); fb1 = feedback(e1)
    u1 = update(receipt_hash=fb1.receipt_hash, evidence_hashes=(e1.evidence_hash,))
    first = append_resource_feedback_history([], u1, fb1, now=NOW).entry
    after_hash = h({"state":"route_dry_run","selected_backend_id":"python_local","marginal_cost_usd":0.01})
    e2 = evidence(evidence_id="e2", observed_at="2026-08-21T10:39:00Z"); fb2 = feedback(e2, receipt="r2")
    u2 = update(before_routing=after_hash, receipt_hash=fb2.receipt_hash, evidence_hashes=(e2.evidence_hash,))
    result = append_resource_feedback_history([first], u2, fb2, now=NOW)
    assert result.state == "hold"
    assert "history_stale_parameter_regression:python_local:electricity_per_task_usd" in result.reasons


def test_stale_at_append_time_and_hash_tamper_fail_closed():
    old = evidence(observed_at="2026-08-21T09:00:00Z")
    fb = feedback(old)
    u = update(receipt_hash=fb.receipt_hash, evidence_hashes=(old.evidence_hash,))
    result = append_resource_feedback_history([], u, fb, now=NOW)
    assert result.state == "hold" and "feedback_evidence_stale" in result.reasons
    fresh = evidence(); fbf = feedback(fresh)
    uf = update(receipt_hash=fbf.receipt_hash, evidence_hashes=(fresh.evidence_hash,))
    entry = append_resource_feedback_history([], uf, fbf, now=NOW).entry
    bad = replace(entry, entry_hash="0"*64)
    ok, reasons = verify_resource_feedback_history([bad])
    assert not ok and "history_entry_hash_mismatch" in reasons


def test_update_feedback_binding_mismatch_is_rejected():
    e = evidence(); fb = feedback(e)
    u = update(receipt_hash="0"*64, evidence_hashes=(e.evidence_hash,))
    result = append_resource_feedback_history([], u, fb, now=NOW)
    assert result.state == "hold" and "feedback_receipt_update_mismatch" in result.reasons
