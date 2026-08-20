"""Deterministic hash-bound attestation for I033 capture-session audits.

No network access lives here. The attestation binds an I033 synthetic session audit to the
exact I029 session plan and I030 transport-envelope set, then replays coverage/accounting
invariants and capture-report membership before producing a canonical SHA-256 identity.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

SESSION_PLAN_MODE = "deterministic_no_network_capture_session_plan"
PREFLIGHT_MODE = "deterministic_read_only_transport_preflight"
SESSION_AUDIT_MODE = "synthetic_capture_session_audit"
ATTESTATION_MODE = "capture_session_replay_coverage_attestation"


def _canonical_hash(value: Any) -> str:
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("capture_attestation_noncanonical_input") from exc
    return sha256(encoded).hexdigest()


def _sha256_text(value: Any, error: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(error)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(error) from exc
    return value.lower()


def _validate_plan_and_preflight(session_plan: Mapping[str, Any], preflight: Mapping[str, Any]) -> tuple[list[Mapping[str, Any]], str, str]:
    if not isinstance(session_plan, Mapping) or session_plan.get("schema_version") != 1 or session_plan.get("mode") != SESSION_PLAN_MODE:
        raise ValueError("capture_attestation_session_plan_invalid")
    if not isinstance(preflight, Mapping) or preflight.get("schema_version") != 1 or preflight.get("mode") != PREFLIGHT_MODE:
        raise ValueError("capture_attestation_preflight_invalid")

    plan_hash = _canonical_hash(session_plan)
    if preflight.get("session_plan_sha256") != plan_hash:
        raise ValueError("capture_attestation_session_plan_hash_mismatch")

    envelopes = preflight.get("transport_envelopes")
    if not isinstance(envelopes, list):
        raise ValueError("capture_attestation_transport_envelopes_invalid")
    if preflight.get("planned_request_count") != len(envelopes):
        raise ValueError("capture_attestation_preflight_count_mismatch")

    envelope_set_hash = _canonical_hash(envelopes)
    if preflight.get("transport_envelope_set_sha256") != envelope_set_hash:
        raise ValueError("capture_attestation_envelope_set_hash_mismatch")

    steps = session_plan.get("chronological_session_plan")
    if not isinstance(steps, list) or session_plan.get("planned_request_count") != len(steps):
        raise ValueError("capture_attestation_plan_count_mismatch")
    if len(steps) != len(envelopes):
        raise ValueError("capture_attestation_plan_preflight_count_mismatch")

    for index, (step, envelope) in enumerate(zip(steps, envelopes), start=1):
        if not isinstance(step, Mapping) or not isinstance(envelope, Mapping):
            raise ValueError("capture_attestation_request_row_invalid")
        if step.get("sequence") != index or envelope.get("sequence") != index:
            raise ValueError("capture_attestation_sequence_invalid")
        for key in ("platform", "source_url", "manifest_item_sha256", "expected_evidence_classes"):
            left = list(step.get(key, [])) if key == "expected_evidence_classes" else step.get(key)
            right = list(envelope.get(key, [])) if key == "expected_evidence_classes" else envelope.get(key)
            if left != right:
                raise ValueError(f"capture_attestation_{key}_binding_mismatch")
        _sha256_text(envelope.get("request_binding_sha256"), "capture_attestation_request_binding_invalid")

    return envelopes, plan_hash, envelope_set_hash


def _capture_receipt_hashes(captures: Sequence[Mapping[str, Any]]) -> list[str]:
    hashes: list[str] = []
    seen: set[str] = set()
    for capture in captures:
        if not isinstance(capture, Mapping):
            raise ValueError("capture_attestation_verified_capture_invalid")
        receipt = capture.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("capture_attestation_verified_capture_receipt_missing")
        receipt_hash = _sha256_text(receipt.get("receipt_sha256"), "capture_attestation_capture_receipt_hash_invalid")
        if receipt_hash in seen:
            raise ValueError("capture_attestation_duplicate_capture_receipt")
        seen.add(receipt_hash)
        hashes.append(receipt_hash)
    return sorted(hashes)


def _report_receipt_hashes(report: Mapping[str, Any] | None) -> list[str]:
    if report is None:
        return []
    if not isinstance(report, Mapping):
        raise ValueError("capture_attestation_verified_capture_report_invalid")
    attestations = report.get("capture_attestations")
    if not isinstance(attestations, list):
        raise ValueError("capture_attestation_report_attestations_invalid")
    hashes: list[str] = []
    seen: set[str] = set()
    for attestation in attestations:
        if not isinstance(attestation, Mapping) or not isinstance(attestation.get("receipt"), Mapping):
            raise ValueError("capture_attestation_report_attestation_invalid")
        receipt_hash = _sha256_text(attestation["receipt"].get("receipt_sha256"), "capture_attestation_report_receipt_hash_invalid")
        if receipt_hash in seen:
            raise ValueError("capture_attestation_duplicate_report_receipt")
        seen.add(receipt_hash)
        hashes.append(receipt_hash)
    return sorted(hashes)


def _validate_session_audit(envelopes: Sequence[Mapping[str, Any]], session_result: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(session_result, Mapping) or session_result.get("schema_version") != 1 or session_result.get("mode") != SESSION_AUDIT_MODE:
        raise ValueError("capture_attestation_session_audit_invalid")
    if session_result.get("dry_run_only") is not True or session_result.get("action_enabled") is not False:
        raise ValueError("capture_attestation_session_boundary_invalid")
    if session_result.get("network_calls_performed") is not False or session_result.get("credentials_used") is not False:
        raise ValueError("capture_attestation_session_external_action_invalid")

    rows = session_result.get("planned_request_audit")
    if not isinstance(rows, list) or len(rows) != len(envelopes):
        raise ValueError("capture_attestation_audit_row_count_mismatch")

    envelope_by_binding: dict[str, Mapping[str, Any]] = {}
    for envelope in envelopes:
        binding = _sha256_text(envelope.get("request_binding_sha256"), "capture_attestation_request_binding_invalid")
        if binding in envelope_by_binding:
            raise ValueError("capture_attestation_duplicate_preflight_binding")
        envelope_by_binding[binding] = envelope

    seen_bindings: set[str] = set()
    captured_hashes: list[str] = []
    state_counts = {"captured": 0, "missing": 0, "rejected": 0}
    canonical_rows: list[dict[str, Any]] = []

    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("capture_attestation_audit_row_invalid")
        binding = _sha256_text(row.get("request_binding_sha256"), "capture_attestation_audit_binding_invalid")
        if binding in seen_bindings:
            raise ValueError("capture_attestation_duplicate_audit_binding")
        seen_bindings.add(binding)
        envelope = envelope_by_binding.get(binding)
        if envelope is None:
            raise ValueError("capture_attestation_audit_binding_outside_plan")
        for key in ("sequence", "platform", "source_url"):
            if row.get(key) != envelope.get(key):
                raise ValueError(f"capture_attestation_audit_{key}_mismatch")
        if list(row.get("expected_evidence_classes", [])) != list(envelope.get("expected_evidence_classes", [])):
            raise ValueError("capture_attestation_audit_evidence_class_mismatch")

        state = row.get("state")
        if state not in state_counts:
            raise ValueError("capture_attestation_audit_state_invalid")
        state_counts[state] += 1
        response_hash = row.get("response_receipt_sha256")
        capture_hash = row.get("capture_receipt_sha256")
        error_code = row.get("error_code")

        if state == "captured":
            if error_code is not None:
                raise ValueError("capture_attestation_captured_error_code_invalid")
            response_hash = _sha256_text(response_hash, "capture_attestation_response_receipt_hash_invalid")
            capture_hash = _sha256_text(capture_hash, "capture_attestation_capture_receipt_hash_invalid")
            captured_hashes.append(capture_hash)
        elif state == "missing":
            if response_hash is not None or capture_hash is not None:
                raise ValueError("capture_attestation_missing_receipt_invalid")
            if error_code != "session_missing_scheduled_response":
                raise ValueError("capture_attestation_missing_error_code_invalid")
        else:
            if capture_hash is not None:
                raise ValueError("capture_attestation_rejected_capture_receipt_invalid")
            if not isinstance(error_code, str) or not error_code:
                raise ValueError("capture_attestation_rejected_error_code_invalid")
            if response_hash is not None:
                response_hash = _sha256_text(response_hash, "capture_attestation_response_receipt_hash_invalid")

        canonical_rows.append({
            "sequence": row.get("sequence"),
            "platform": row.get("platform"),
            "source_url": row.get("source_url"),
            "request_binding_sha256": binding,
            "expected_evidence_classes": list(row.get("expected_evidence_classes", [])),
            "state": state,
            "error_code": error_code,
            "response_receipt_sha256": response_hash,
            "capture_receipt_sha256": capture_hash,
        })

    if seen_bindings != set(envelope_by_binding):
        raise ValueError("capture_attestation_audit_plan_coverage_mismatch")
    if session_result.get("planned_request_count") != len(envelopes):
        raise ValueError("capture_attestation_planned_count_mismatch")
    if session_result.get("captured_count") != state_counts["captured"]:
        raise ValueError("capture_attestation_captured_count_mismatch")
    if session_result.get("missing_count") != state_counts["missing"]:
        raise ValueError("capture_attestation_missing_count_mismatch")
    if session_result.get("rejected_planned_count") != state_counts["rejected"]:
        raise ValueError("capture_attestation_rejected_count_mismatch")

    gap_count = state_counts["missing"] + state_counts["rejected"]
    if session_result.get("production_gap_count") != gap_count:
        raise ValueError("capture_attestation_production_gap_count_mismatch")
    expected_coverage = state_counts["captured"] == len(envelopes)
    if session_result.get("coverage_complete") is not expected_coverage:
        raise ValueError("capture_attestation_coverage_flag_mismatch")
    if session_result.get("missing_means_zero_demand") is not False:
        raise ValueError("capture_attestation_missing_demand_semantics_invalid")

    rejected_inputs = session_result.get("rejected_response_inputs")
    if not isinstance(rejected_inputs, list):
        raise ValueError("capture_attestation_rejected_inputs_invalid")
    if session_result.get("rejected_extra_input_count") != len(rejected_inputs):
        raise ValueError("capture_attestation_rejected_extra_count_mismatch")

    verified_captures = session_result.get("verified_captures")
    if not isinstance(verified_captures, list):
        raise ValueError("capture_attestation_verified_captures_invalid")
    verified_hashes = _capture_receipt_hashes(verified_captures)
    if sorted(captured_hashes) != verified_hashes:
        raise ValueError("capture_attestation_audit_capture_set_mismatch")

    report_hashes = _report_receipt_hashes(session_result.get("verified_capture_report"))
    if state_counts["captured"] == 0:
        if session_result.get("verified_capture_report") is not None:
            raise ValueError("capture_attestation_empty_capture_report_mismatch")
    elif report_hashes != verified_hashes:
        raise ValueError("capture_attestation_capture_report_mismatch")

    return {
        "planned_request_count": len(envelopes),
        "captured_count": state_counts["captured"],
        "missing_count": state_counts["missing"],
        "rejected_planned_count": state_counts["rejected"],
        "rejected_extra_input_count": len(rejected_inputs),
        "production_gap_count": gap_count,
        "coverage_complete": expected_coverage,
        "planned_request_audit": canonical_rows,
        "rejected_response_inputs_sha256": _canonical_hash(rejected_inputs),
        "verified_capture_receipt_sha256s": verified_hashes,
        "capture_report_receipt_sha256s": report_hashes,
        "missing_means_zero_demand": False,
    }


def build_capture_session_attestation(session_plan: Mapping[str, Any], preflight: Mapping[str, Any], session_result: Mapping[str, Any]) -> dict[str, Any]:
    """Replay I033 accounting and return a canonical hash-addressed attestation."""
    envelopes, plan_hash, envelope_set_hash = _validate_plan_and_preflight(session_plan, preflight)
    coverage = _validate_session_audit(envelopes, session_result)
    core = {
        "schema_version": 1,
        "mode": ATTESTATION_MODE,
        "session_plan_sha256": plan_hash,
        "transport_envelope_set_sha256": envelope_set_hash,
        "preflight_sha256": _canonical_hash(preflight),
        "planned_request_binding_sha256s": [envelope["request_binding_sha256"] for envelope in envelopes],
        "coverage": coverage,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "coverage_sha256": _canonical_hash(coverage), "attestation_sha256": _canonical_hash(core)}


def verify_capture_session_attestation(session_plan: Mapping[str, Any], preflight: Mapping[str, Any], session_result: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    """Rebuild and exactly compare a stored attestation."""
    if not isinstance(attestation, Mapping):
        raise ValueError("capture_attestation_record_invalid")
    rebuilt = build_capture_session_attestation(session_plan, preflight, session_result)
    if dict(attestation) != rebuilt:
        raise ValueError("capture_attestation_record_mismatch")
    return rebuilt
