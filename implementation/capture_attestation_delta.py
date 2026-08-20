"""Deterministic same-plan delta verifier for capture-session attestations.

No network access lives here. Two stored I034 attestations are accepted only when
both are internally self-consistent and bind to the exact same I029 session-plan
and I030 transport-envelope-set identities.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

ATTESTATION_MODE = "capture_session_replay_coverage_attestation"
DELTA_MODE = "capture_session_attestation_delta"


def _canonical_hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _sha256_text(value: Any, error: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(error)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(error) from exc
    return value.lower()


def _validate_attestation(attestation: Mapping[str, Any], label: str) -> dict[str, Any]:
    p = f"capture_delta_{label}"
    if not isinstance(attestation, Mapping):
        raise ValueError(f"{p}_record_invalid")
    if attestation.get("schema_version") != 1 or attestation.get("mode") != ATTESTATION_MODE:
        raise ValueError(f"{p}_mode_invalid")
    if attestation.get("dry_run_only") is not True or attestation.get("action_enabled") is not False:
        raise ValueError(f"{p}_boundary_invalid")
    if attestation.get("network_calls_performed") is not False or attestation.get("credentials_used") is not False:
        raise ValueError(f"{p}_external_action_invalid")
    plan = _sha256_text(attestation.get("session_plan_sha256"), f"{p}_plan_hash_invalid")
    env = _sha256_text(attestation.get("transport_envelope_set_sha256"), f"{p}_envelope_hash_invalid")
    _sha256_text(attestation.get("preflight_sha256"), f"{p}_preflight_hash_invalid")
    bindings = attestation.get("planned_request_binding_sha256s")
    if not isinstance(bindings, list):
        raise ValueError(f"{p}_bindings_invalid")
    bindings = [_sha256_text(x, f"{p}_binding_invalid") for x in bindings]
    if len(bindings) != len(set(bindings)):
        raise ValueError(f"{p}_duplicate_binding")
    coverage = attestation.get("coverage")
    if not isinstance(coverage, Mapping):
        raise ValueError(f"{p}_coverage_invalid")
    if _sha256_text(attestation.get("coverage_sha256"), f"{p}_coverage_hash_invalid") != _canonical_hash(coverage):
        raise ValueError(f"{p}_coverage_hash_mismatch")
    rows = coverage.get("planned_request_audit")
    if not isinstance(rows, list) or len(rows) != len(bindings):
        raise ValueError(f"{p}_audit_count_mismatch")
    by = {}
    counts = {"captured": 0, "missing": 0, "rejected": 0}
    captured = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError(f"{p}_audit_row_invalid")
        binding = _sha256_text(row.get("request_binding_sha256"), f"{p}_audit_binding_invalid")
        if binding in by:
            raise ValueError(f"{p}_duplicate_audit_binding")
        state = row.get("state")
        if state not in counts:
            raise ValueError(f"{p}_state_invalid")
        counts[state] += 1
        response_hash = row.get("response_receipt_sha256")
        capture_hash = row.get("capture_receipt_sha256")
        error_code = row.get("error_code")
        if state == "captured":
            if error_code is not None:
                raise ValueError(f"{p}_captured_error_invalid")
            response_hash = _sha256_text(response_hash, f"{p}_response_receipt_invalid")
            capture_hash = _sha256_text(capture_hash, f"{p}_capture_receipt_invalid")
            captured.append(capture_hash)
        elif state == "missing":
            if response_hash is not None or capture_hash is not None:
                raise ValueError(f"{p}_missing_receipt_invalid")
            if error_code != "session_missing_scheduled_response":
                raise ValueError(f"{p}_missing_error_invalid")
        else:
            if capture_hash is not None:
                raise ValueError(f"{p}_rejected_capture_receipt_invalid")
            if not isinstance(error_code, str) or not error_code:
                raise ValueError(f"{p}_rejected_error_invalid")
            if response_hash is not None:
                response_hash = _sha256_text(response_hash, f"{p}_response_receipt_invalid")
        by[binding] = {
            "sequence": row.get("sequence"),
            "platform": row.get("platform"),
            "source_url": row.get("source_url"),
            "request_binding_sha256": binding,
            "expected_evidence_classes": list(row.get("expected_evidence_classes", [])),
            "state": state,
            "error_code": error_code,
            "response_receipt_sha256": response_hash,
            "capture_receipt_sha256": capture_hash,
        }
    if set(by) != set(bindings):
        raise ValueError(f"{p}_audit_binding_set_mismatch")
    checks = {
        "planned_request_count": len(bindings),
        "captured_count": counts["captured"],
        "missing_count": counts["missing"],
        "rejected_planned_count": counts["rejected"],
        "production_gap_count": counts["missing"] + counts["rejected"],
    }
    for key, expected in checks.items():
        if coverage.get(key) != expected:
            raise ValueError(f"{p}_{key}_mismatch")
    if coverage.get("coverage_complete") is not (counts["captured"] == len(bindings)):
        raise ValueError(f"{p}_coverage_flag_mismatch")
    if coverage.get("missing_means_zero_demand") is not False:
        raise ValueError(f"{p}_missing_demand_semantics_invalid")
    verified = coverage.get("verified_capture_receipt_sha256s")
    report = coverage.get("capture_report_receipt_sha256s")
    if not isinstance(verified, list) or not isinstance(report, list):
        raise ValueError(f"{p}_receipt_sets_invalid")
    verified = sorted(_sha256_text(x, f"{p}_verified_receipt_invalid") for x in verified)
    report = sorted(_sha256_text(x, f"{p}_report_receipt_invalid") for x in report)
    if len(verified) != len(set(verified)) or len(report) != len(set(report)):
        raise ValueError(f"{p}_duplicate_receipt")
    if sorted(captured) != verified or report != verified:
        raise ValueError(f"{p}_receipt_membership_mismatch")
    keys = ("schema_version", "mode", "session_plan_sha256", "transport_envelope_set_sha256", "preflight_sha256", "planned_request_binding_sha256s", "coverage", "dry_run_only", "action_enabled", "network_calls_performed", "credentials_used")
    core = {key: attestation[key] for key in keys}
    attestation_hash = _sha256_text(attestation.get("attestation_sha256"), f"{p}_attestation_hash_invalid")
    if attestation_hash != _canonical_hash(core):
        raise ValueError(f"{p}_attestation_hash_mismatch")
    return {"plan_hash": plan, "envelope_hash": env, "attestation_hash": attestation_hash, "bindings": bindings, "rows": by, "coverage": dict(coverage), "verified_receipts": verified}


def compare_capture_session_attestations(baseline: Mapping[str, Any], target: Mapping[str, Any]) -> dict[str, Any]:
    """Return deterministic deltas for two valid attestations sharing one exact plan."""
    left = _validate_attestation(baseline, "baseline")
    right = _validate_attestation(target, "target")
    if left["plan_hash"] != right["plan_hash"]:
        raise ValueError("capture_delta_cross_plan_comparison")
    if left["envelope_hash"] != right["envelope_hash"]:
        raise ValueError("capture_delta_cross_envelope_set_comparison")
    if left["bindings"] != right["bindings"]:
        raise ValueError("capture_delta_binding_order_mismatch")
    changes = []
    for binding in left["bindings"]:
        before = left["rows"][binding]
        after = right["rows"][binding]
        for field in ("sequence", "platform", "source_url", "expected_evidence_classes"):
            if before[field] != after[field]:
                raise ValueError(f"capture_delta_request_identity_{field}_mismatch")
        if before != after:
            changes.append({
                "sequence": before["sequence"],
                "platform": before["platform"],
                "source_url": before["source_url"],
                "request_binding_sha256": binding,
                "from_state": before["state"],
                "to_state": after["state"],
                "from_error_code": before["error_code"],
                "to_error_code": after["error_code"],
                "response_receipt_changed": before["response_receipt_sha256"] != after["response_receipt_sha256"],
                "capture_receipt_changed": before["capture_receipt_sha256"] != after["capture_receipt_sha256"],
                "from_capture_receipt_sha256": before["capture_receipt_sha256"],
                "to_capture_receipt_sha256": after["capture_receipt_sha256"],
            })
    left_receipts = set(left["verified_receipts"])
    right_receipts = set(right["verified_receipts"])
    fields = ("captured_count", "missing_count", "rejected_planned_count", "production_gap_count")
    core = {
        "schema_version": 1,
        "mode": DELTA_MODE,
        "session_plan_sha256": left["plan_hash"],
        "transport_envelope_set_sha256": left["envelope_hash"],
        "baseline_attestation_sha256": left["attestation_hash"],
        "target_attestation_sha256": right["attestation_hash"],
        "planned_request_count": len(left["bindings"]),
        "coverage_complete_transition": {"from": left["coverage"]["coverage_complete"], "to": right["coverage"]["coverage_complete"]},
        "coverage_delta": {field: right["coverage"][field] - left["coverage"][field] for field in fields},
        "request_state_changes": changes,
        "verified_capture_receipts_added": sorted(right_receipts - left_receipts),
        "verified_capture_receipts_removed": sorted(left_receipts - right_receipts),
        "missing_evidence_semantics": "unknown_not_negative_demand",
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
    return {**core, "delta_sha256": _canonical_hash(core)}
