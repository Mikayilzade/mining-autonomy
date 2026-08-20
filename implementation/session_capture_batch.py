"""Deterministic session-level bridge for synthetic I031 responses into verified captures.

No network access lives here. The batch runner reconciles the exact I029/I030 planned
request set against supplied synthetic responses, isolates failures per request, and sends
only successful I032-verified captures into the existing receipt-gated capture report.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from observation_capture import run_verified_capture_batch
from response_capture_bridge import PayloadBuilder, bridge_response_to_verified_capture

SESSION_MODE = "synthetic_capture_session_audit"


@dataclass(frozen=True)
class SyntheticResponseInput:
    response_receipt_sha256: str
    response_body: bytes
    source_timestamp_utc: str
    capture_started_at_utc: str
    capture_finished_at_utc: str
    payload_builder: PayloadBuilder
    captured_environment: str = "production"
    environment_evidence_sha256: str | None = None


def _stable_error_code(exc: Exception) -> str:
    text = str(exc).strip()
    if isinstance(exc, ValueError) and text and " " not in text and "\n" not in text:
        return text
    return "session_unexpected_capture_error"


def _planned_requests(preflight: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    envelopes = preflight.get("transport_envelopes") if isinstance(preflight, Mapping) else None
    if not isinstance(envelopes, list):
        raise ValueError("session_preflight_envelopes_invalid")
    declared = preflight.get("planned_request_count")
    if declared is not None and declared != len(envelopes):
        raise ValueError("session_planned_request_count_mismatch")
    seen: set[str] = set()
    result: list[Mapping[str, Any]] = []
    for envelope in envelopes:
        if not isinstance(envelope, Mapping):
            raise ValueError("session_request_envelope_invalid")
        binding = envelope.get("request_binding_sha256")
        if not isinstance(binding, str) or not binding:
            raise ValueError("session_request_binding_invalid")
        if binding in seen:
            raise ValueError("session_duplicate_planned_request_binding")
        seen.add(binding)
        result.append(envelope)
    return result


def _execution_response_index(execution_receipt: Mapping[str, Any]) -> tuple[dict[str, Mapping[str, Any]], set[str]]:
    responses = execution_receipt.get("response_receipts") if isinstance(execution_receipt, Mapping) else None
    if not isinstance(responses, list):
        raise ValueError("session_execution_response_receipts_invalid")
    by_hash: dict[str, Mapping[str, Any]] = {}
    duplicates: set[str] = set()
    for response in responses:
        if not isinstance(response, Mapping):
            continue
        receipt_hash = response.get("response_receipt_sha256")
        if not isinstance(receipt_hash, str) or not receipt_hash:
            continue
        if receipt_hash in by_hash:
            duplicates.add(receipt_hash)
        else:
            by_hash[receipt_hash] = response
    return by_hash, duplicates


def run_synthetic_capture_session(
    preflight: Mapping[str, Any],
    execution_receipt: Mapping[str, Any],
    manifest_envelope: Mapping[str, Any],
    responses: Sequence[SyntheticResponseInput],
) -> dict[str, Any]:
    """Reconcile and bridge a complete synthetic response session.

    Every planned request ends in exactly one audit state. Missing, duplicate, extra and
    bridge-rejected responses remain explicit production evidence gaps. Only successful
    I032 verified captures are passed to `run_verified_capture_batch`.
    """
    planned = _planned_requests(preflight)
    planned_by_binding = {item["request_binding_sha256"]: item for item in planned}
    execution_by_hash, execution_duplicate_hashes = _execution_response_index(execution_receipt)

    supplied_counts: dict[str, int] = {}
    for item in responses:
        supplied_counts[item.response_receipt_sha256] = supplied_counts.get(item.response_receipt_sha256, 0) + 1
    supplied_duplicate_hashes = {key for key, count in supplied_counts.items() if count > 1}

    candidate_by_binding: dict[str, list[SyntheticResponseInput]] = {}
    rejected_inputs: list[dict[str, Any]] = []

    for item in responses:
        receipt_hash = item.response_receipt_sha256
        if receipt_hash in supplied_duplicate_hashes:
            rejected_inputs.append({
                "response_receipt_sha256": receipt_hash,
                "request_binding_sha256": None,
                "state": "rejected",
                "error_code": "session_duplicate_response_receipt_input",
            })
            continue
        if receipt_hash in execution_duplicate_hashes:
            rejected_inputs.append({
                "response_receipt_sha256": receipt_hash,
                "request_binding_sha256": None,
                "state": "rejected",
                "error_code": "session_duplicate_response_receipt_execution",
            })
            continue
        receipt = execution_by_hash.get(receipt_hash)
        if receipt is None:
            rejected_inputs.append({
                "response_receipt_sha256": receipt_hash,
                "request_binding_sha256": None,
                "state": "rejected",
                "error_code": "session_response_receipt_not_in_execution",
            })
            continue
        binding = receipt.get("request_binding_sha256")
        if binding not in planned_by_binding:
            rejected_inputs.append({
                "response_receipt_sha256": receipt_hash,
                "request_binding_sha256": binding,
                "state": "rejected",
                "error_code": "session_response_not_in_planned_session",
            })
            continue
        candidate_by_binding.setdefault(binding, []).append(item)

    successful: list[dict[str, Any]] = []
    planned_audit: list[dict[str, Any]] = []
    duplicate_request_bindings = {binding for binding, items in candidate_by_binding.items() if len(items) > 1}

    for request in planned:
        binding = request["request_binding_sha256"]
        candidates = candidate_by_binding.get(binding, [])
        base = {
            "sequence": request.get("sequence"),
            "platform": request.get("platform"),
            "source_url": request.get("source_url"),
            "request_binding_sha256": binding,
            "expected_evidence_classes": list(request.get("expected_evidence_classes", [])),
        }
        if not candidates:
            planned_audit.append({
                **base,
                "state": "missing",
                "error_code": "session_missing_scheduled_response",
                "response_receipt_sha256": None,
                "capture_receipt_sha256": None,
            })
            continue
        if binding in duplicate_request_bindings:
            planned_audit.append({
                **base,
                "state": "rejected",
                "error_code": "session_duplicate_response_for_request",
                "response_receipt_sha256": None,
                "capture_receipt_sha256": None,
            })
            continue

        supplied = candidates[0]
        try:
            bridged = bridge_response_to_verified_capture(
                preflight,
                execution_receipt,
                manifest_envelope,
                response_receipt_sha256=supplied.response_receipt_sha256,
                response_body=supplied.response_body,
                source_timestamp_utc=supplied.source_timestamp_utc,
                capture_started_at_utc=supplied.capture_started_at_utc,
                capture_finished_at_utc=supplied.capture_finished_at_utc,
                payload_builder=supplied.payload_builder,
                captured_environment=supplied.captured_environment,
                environment_evidence_sha256=supplied.environment_evidence_sha256,
            )
        except Exception as exc:  # per-request isolation is intentional
            planned_audit.append({
                **base,
                "state": "rejected",
                "error_code": _stable_error_code(exc),
                "response_receipt_sha256": supplied.response_receipt_sha256,
                "capture_receipt_sha256": None,
            })
            continue

        successful.append(bridged)
        planned_audit.append({
            **base,
            "state": "captured",
            "error_code": None,
            "response_receipt_sha256": supplied.response_receipt_sha256,
            "capture_receipt_sha256": bridged["receipt"]["receipt_sha256"],
        })

    capture_report = run_verified_capture_batch(successful) if successful else None
    captured_count = sum(1 for item in planned_audit if item["state"] == "captured")
    missing_count = sum(1 for item in planned_audit if item["state"] == "missing")
    rejected_planned_count = sum(1 for item in planned_audit if item["state"] == "rejected")

    return {
        "schema_version": 1,
        "mode": SESSION_MODE,
        "planned_request_count": len(planned),
        "supplied_response_count": len(responses),
        "captured_count": captured_count,
        "missing_count": missing_count,
        "rejected_planned_count": rejected_planned_count,
        "rejected_extra_input_count": len(rejected_inputs),
        "coverage_complete": captured_count == len(planned),
        "production_gap_count": len(planned) - captured_count,
        "planned_request_audit": planned_audit,
        "rejected_response_inputs": rejected_inputs,
        "verified_captures": successful,
        "verified_capture_report": capture_report,
        "missing_means_zero_demand": False,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
