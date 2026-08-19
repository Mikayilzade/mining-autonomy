"""Deterministic receipt-aware audit helpers for inert sampling manifests.

No network, credentials, task acceptance, publication, wallet, or settlement action is
performed here. The module only verifies already-produced sealed manifests, capture
receipts and receipt-gated capture reports.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from evidence_archive import validate_capture_report
from sampling_receipt import (
    ALLOWED_ENVIRONMENTS,
    manifest_item_sha256,
    verify_capture_receipt,
    verify_sampling_manifest_envelope,
)


def _receipt_by_item_index(
    receipts: Iterable[Mapping[str, Any]],
) -> tuple[dict[int, list[Mapping[str, Any]]], int]:
    grouped: dict[int, list[Mapping[str, Any]]] = {}
    unmatched = 0
    for receipt in receipts:
        if not isinstance(receipt, Mapping):
            unmatched += 1
            continue
        index = receipt.get("item_index")
        if not isinstance(index, int) or isinstance(index, bool) or index < 0:
            unmatched += 1
            continue
        grouped.setdefault(index, []).append(receipt)
    return grouped, unmatched


def sampling_audit_summary(
    manifest_envelope: Mapping[str, Any],
    receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Classify every scheduled manifest item by capture/receipt state.

    States are deliberately coarse and deterministic:
    - scheduled_but_uncaptured
    - receipt_invalid
    - receipt_valid_non_production
    - receipt_valid_production

    Valid testnet and unknown receipts are both non-production. Unscheduled or
    structurally unmatchable receipts are counted separately and cannot close a gap.
    """
    verify_sampling_manifest_envelope(manifest_envelope)
    manifest = manifest_envelope["manifest"]
    items = manifest["items"]
    grouped, structurally_unmatched = _receipt_by_item_index(receipts)
    rows: list[dict[str, Any]] = []
    unexpected_receipts = structurally_unmatched

    for index, item in enumerate(items):
        candidates = grouped.get(index, [])
        if item.get("scheduled") is not True:
            unexpected_receipts += len(candidates)
            continue

        base = {
            "item_index": index,
            "platform": item.get("platform"),
            "source_url": item.get("source_url"),
            "manifest_sha256": manifest_envelope["manifest_sha256"],
            "manifest_item_sha256": manifest_item_sha256(manifest_envelope, index),
            "declared_environment": item.get("environment", "unknown"),
        }

        if not candidates:
            rows.append({
                **base,
                "state": "scheduled_but_uncaptured",
                "receipt_sha256": None,
                "captured_environment": None,
                "reason": "no_receipt_for_scheduled_item",
            })
            continue

        if len(candidates) != 1:
            rows.append({
                **base,
                "state": "receipt_invalid",
                "receipt_sha256": None,
                "captured_environment": None,
                "reason": "multiple_receipts_for_manifest_item",
            })
            continue

        receipt = candidates[0]
        try:
            verify_capture_receipt(manifest_envelope, receipt)
            captured_environment = receipt.get("captured_environment")
            if captured_environment not in ALLOWED_ENVIRONMENTS:
                raise ValueError("capture_receipt_environment_invalid")
            if item.get("scheduled") is not True:
                raise ValueError("capture_receipt_item_not_scheduled")
        except (TypeError, ValueError) as exc:
            rows.append({
                **base,
                "state": "receipt_invalid",
                "receipt_sha256": receipt.get("receipt_sha256"),
                "captured_environment": receipt.get("captured_environment"),
                "reason": str(exc) or exc.__class__.__name__,
            })
            continue

        state = (
            "receipt_valid_production"
            if captured_environment == "production"
            else "receipt_valid_non_production"
        )
        rows.append({
            **base,
            "state": state,
            "receipt_sha256": receipt["receipt_sha256"],
            "captured_environment": captured_environment,
            "environment_evidence_sha256": receipt.get("environment_evidence_sha256"),
            "sanitized_bundle_sha256": receipt.get("sanitized_bundle_sha256"),
            "capture_finished_at": receipt.get("capture_finished_at"),
            "reason": None,
        })

    rows.sort(key=lambda row: (row["platform"] or "", row["source_url"] or "", row["item_index"]))
    counts = {
        state: sum(row["state"] == state for row in rows)
        for state in (
            "scheduled_but_uncaptured",
            "receipt_invalid",
            "receipt_valid_non_production",
            "receipt_valid_production",
        )
    }
    return {
        "schema_version": 1,
        "manifest_sha256": manifest_envelope["manifest_sha256"],
        "scheduled_item_count": len(rows),
        **{f"{state}_count": count for state, count in counts.items()},
        "unexpected_or_unmatched_receipt_count": unexpected_receipts,
        "items": rows,
        "production_evidence_requires_valid_receipt": True,
        "non_production_can_close_production_gap": False,
        "receipt_can_authorize_action": False,
        "network_calls_performed": False,
        "dry_run_only": True,
        "action_enabled": False,
    }


def receipt_provenance_index(
    capture_report: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Return verified receipt/manifest references keyed by sanitized bundle hash.

    The full capture report is revalidated through the durable-ingestion validator
    before any provenance reference is returned.
    """
    value, deltas, verified_environments = validate_capture_report(capture_report)
    attestations = value["capture_attestations"]
    by_bundle = {attestation["bundle_sha256"]: attestation for attestation in attestations}
    result: dict[str, dict[str, Any]] = {}
    for delta in deltas:
        bundle_sha = delta["bundle_sha256"]
        attestation = by_bundle[bundle_sha]
        envelope = attestation["manifest_envelope"]
        receipt = attestation["receipt"]
        verify_capture_receipt(envelope, receipt)
        result[bundle_sha] = {
            "manifest_sha256": receipt["manifest_sha256"],
            "manifest_item_sha256": receipt["manifest_item_sha256"],
            "receipt_sha256": receipt["receipt_sha256"],
            "captured_environment": verified_environments[bundle_sha],
            "environment_evidence_sha256": receipt.get("environment_evidence_sha256"),
            "source_url": receipt["source_url"],
            "capture_finished_at": receipt["capture_finished_at"],
        }
    return result
