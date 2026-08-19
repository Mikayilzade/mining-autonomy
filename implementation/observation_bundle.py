"""Offline PayanAgent observation-bundle pipeline.

Joins raw-public-payload sanitization, hash-bounded evidence snapshots, saved
observation import, dry-run task replay, paid-utilization aggregation/history,
and a deterministic HMAC-signed audit manifest. No network, authentication,
task acceptance, publication, wallet, payment, or settlement action is present.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import hmac
from typing import Any, Iterable, Mapping, Sequence

from observation_importer import ImportedObservation, import_saved_observation
from orchestrator import audit_export, observe_imported_tasks
from payan_sanitizer import sanitize_payan_receipt, sanitize_payan_request
from receipt_aggregation import aggregate_imported_utilization, utilization_record
from snapshot import canonical_payload_hash, ingest_snapshot, snapshot_record
from utilization_history import compare_utilization_snapshots, utilization_history_record


@dataclass(frozen=True)
class ObservationBundle:
    platform: str
    request_envelope: dict[str, Any]
    receipt_envelope: dict[str, Any] | None
    task_audit: dict[str, Any]
    utilization: dict[str, Any] | None
    utilization_history: dict[str, Any] | None
    manifest: dict[str, Any]
    manifest_sha256: str
    signature_hmac_sha256: str


def _saved_envelope(snapshot: Any, evidence_class: str, records_key: str = "items") -> dict[str, Any]:
    return {
        "snapshot": snapshot_record(snapshot),
        "demand_evidence_class": evidence_class,
        "records_key": records_key,
    }


def _trusted_for(request_id: str, mapping: Mapping[str, Mapping[str, Any]] | None) -> Mapping[str, Any] | None:
    if mapping is None:
        return None
    value = mapping.get(request_id)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("trusted_request_mapping_value_must_be_object")
    return value


def build_payan_request_envelope(
    raw_requests: Iterable[Mapping[str, Any]], *,
    source_url: str,
    source_timestamp: str,
    captured_at: str,
    trusted_policy_by_request_id: Mapping[str, Mapping[str, Any]] | None = None,
    trusted_estimates_by_request_id: Mapping[str, Mapping[str, Any]] | None = None,
    evidence_class: str | None = None,
    max_age_hours: float = 24.0,
) -> dict[str, Any]:
    sanitized: list[dict[str, Any]] = []
    for raw in raw_requests:
        provisional = sanitize_payan_request(raw)
        request_id = provisional["id"]
        sanitized.append(sanitize_payan_request(
            raw,
            trusted_policy=_trusted_for(request_id, trusted_policy_by_request_id),
            trusted_estimates=_trusted_for(request_id, trusted_estimates_by_request_id),
        ))
    effective_evidence = evidence_class or ("open_paid_request" if sanitized else "unknown")
    if effective_evidence == "open_paid_request" and not sanitized:
        raise ValueError("open_paid_request_evidence_requires_nonempty_records")
    snapshot = ingest_snapshot(
        platform="payanagent",
        source_url=source_url,
        source_timestamp=source_timestamp,
        evidence_class="official_api",
        payload={"items": sanitized},
        captured_at=captured_at,
        max_age_hours=max_age_hours,
    )
    return _saved_envelope(snapshot, effective_evidence)


def build_payan_receipt_envelope(
    raw_receipts: Iterable[Mapping[str, Any]], *,
    source_url: str,
    source_timestamp: str,
    captured_at: str,
    evidence_class: str = "settled_receipt",
    max_age_hours: float = 24.0,
) -> dict[str, Any]:
    sanitized = [sanitize_payan_receipt(raw) for raw in raw_receipts]
    if evidence_class in {"settled_receipt", "paid_invocation"} and not sanitized:
        raise ValueError("paid_utilization_evidence_requires_nonempty_records")
    snapshot = ingest_snapshot(
        platform="payanagent",
        source_url=source_url,
        source_timestamp=source_timestamp,
        evidence_class="official_api",
        payload={"items": sanitized},
        captured_at=captured_at,
        max_age_hours=max_age_hours,
    )
    return _saved_envelope(snapshot, evidence_class)


def _stable_digest(value: Mapping[str, Any] | None) -> str | None:
    if value is None:
        return None
    return canonical_payload_hash(dict(value))


def _sign_manifest(manifest_sha256: str, signing_key: bytes) -> str:
    if not isinstance(signing_key, bytes) or len(signing_key) < 16:
        raise ValueError("bundle_signing_key_must_be_at_least_16_bytes")
    return hmac.new(signing_key, manifest_sha256.encode("ascii"), sha256).hexdigest()


def build_payan_observation_bundle(
    *,
    raw_requests: Sequence[Mapping[str, Any]],
    raw_receipts: Sequence[Mapping[str, Any]] = (),
    request_source_url: str,
    request_source_timestamp: str,
    receipt_source_url: str | None = None,
    receipt_source_timestamp: str | None = None,
    captured_at: str,
    signing_key: bytes,
    trusted_policy_by_request_id: Mapping[str, Mapping[str, Any]] | None = None,
    trusted_estimates_by_request_id: Mapping[str, Mapping[str, Any]] | None = None,
    prior_receipt_envelopes: Sequence[Mapping[str, Any]] = (),
    now: datetime | None = None,
    max_age_hours: float = 24.0,
) -> ObservationBundle:
    request_envelope = build_payan_request_envelope(
        raw_requests,
        source_url=request_source_url,
        source_timestamp=request_source_timestamp,
        captured_at=captured_at,
        trusted_policy_by_request_id=trusted_policy_by_request_id,
        trusted_estimates_by_request_id=trusted_estimates_by_request_id,
        max_age_hours=max_age_hours,
    )
    imported_requests = import_saved_observation(
        request_envelope, now=now, max_age_hours=max_age_hours
    )
    if imported_requests.demand_evidence.proves_open_paid_demand:
        task_items = observe_imported_tasks(
            imported_requests, now=now, max_age_hours=max_age_hours
        )
    else:
        task_items = []
    task_audit = audit_export(task_items, generated_at=captured_at)

    receipt_envelope: dict[str, Any] | None = None
    utilization: dict[str, Any] | None = None
    history_record: dict[str, Any] | None = None
    if raw_receipts:
        if not receipt_source_url or not receipt_source_timestamp:
            raise ValueError("receipt_source_provenance_required")
        receipt_envelope = build_payan_receipt_envelope(
            raw_receipts,
            source_url=receipt_source_url,
            source_timestamp=receipt_source_timestamp,
            captured_at=captured_at,
            max_age_hours=max_age_hours,
        )
        current = import_saved_observation(
            receipt_envelope, now=now, max_age_hours=max_age_hours
        )
        utilization = utilization_record(
            aggregate_imported_utilization(current, now=now, max_age_hours=max_age_hours)
        )
        if prior_receipt_envelopes:
            prior: list[ImportedObservation] = [
                import_saved_observation(value, now=now, max_age_hours=max_age_hours)
                for value in prior_receipt_envelopes
            ]
            history_record = utilization_history_record(compare_utilization_snapshots(
                [*prior, current], now=now, max_age_hours=max_age_hours
            ))

    manifest = {
        "schema_version": 1,
        "platform": "payanagent",
        "request_snapshot_sha256": request_envelope["snapshot"]["payload_sha256"],
        "receipt_snapshot_sha256": (
            receipt_envelope["snapshot"]["payload_sha256"] if receipt_envelope else None
        ),
        "task_audit_sha256": _stable_digest(task_audit),
        "utilization_sha256": _stable_digest(utilization),
        "utilization_history_sha256": _stable_digest(history_record),
        "dry_run_only": True,
        "action_enabled": False,
    }
    manifest_sha = canonical_payload_hash(manifest)
    signature = _sign_manifest(manifest_sha, signing_key)
    return ObservationBundle(
        platform="payanagent",
        request_envelope=request_envelope,
        receipt_envelope=receipt_envelope,
        task_audit=task_audit,
        utilization=utilization,
        utilization_history=history_record,
        manifest=manifest,
        manifest_sha256=manifest_sha,
        signature_hmac_sha256=signature,
    )


def verify_observation_bundle(bundle: ObservationBundle, signing_key: bytes) -> bool:
    if not isinstance(bundle, ObservationBundle):
        return False
    if canonical_payload_hash(bundle.manifest) != bundle.manifest_sha256:
        return False
    expected = _sign_manifest(bundle.manifest_sha256, signing_key)
    return hmac.compare_digest(expected, bundle.signature_hmac_sha256)


def observation_bundle_record(bundle: ObservationBundle) -> dict[str, Any]:
    return asdict(bundle)
