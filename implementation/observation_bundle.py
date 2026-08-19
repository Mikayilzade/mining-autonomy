"""Offline multi-market observation-bundle pipeline.

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
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from observation_importer import ImportedObservation, import_saved_observation
from orchestrator import audit_export, observe_imported_tasks
from payan_sanitizer import sanitize_payan_receipt, sanitize_payan_request
from receipt_aggregation import aggregate_imported_utilization, utilization_record
from snapshot import canonical_payload_hash, ingest_snapshot, snapshot_record
from utilization_history import compare_utilization_snapshots, utilization_history_record

BUNDLE_SCHEMA_VERSION = 1
BUNDLE_RECORD_FIELDS = {
    "platform", "request_envelope", "receipt_envelope", "task_audit",
    "utilization", "utilization_history", "manifest", "manifest_sha256",
    "signature_hmac_sha256",
}
MANIFEST_FIELDS = {
    "schema_version", "platform", "request_snapshot_sha256",
    "receipt_snapshot_sha256", "task_audit_sha256", "utilization_sha256",
    "utilization_history_sha256", "dry_run_only", "action_enabled",
}
SNAPSHOT_FIELDS = {
    "platform", "source_url", "source_timestamp", "captured_at",
    "evidence_class", "payload", "payload_sha256",
}

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


def _merge_trusted_metadata(
    trusted_policy: Mapping[str, Any] | None,
    trusted_estimates: Mapping[str, Any] | None,
    *,
    required_capabilities: Sequence[str],
) -> dict[str, Any]:
    metadata: dict[str, Any] = {"required_capabilities": list(required_capabilities)}
    if trusted_policy:
        for key in ("rights_status", "tos_status", "automation_allowed", "source_data_permission"):
            if key in trusted_policy:
                metadata[key] = trusted_policy[key]
    if trusted_estimates:
        for key in (
            "estimated_input_tokens", "estimated_output_tokens",
            "estimated_duration_seconds", "estimate_confidence",
            "external_cost_cap_usd",
        ):
            if key in trusted_estimates:
                metadata[key] = trusted_estimates[key]
    return metadata


def _coalesce_alias(raw: Mapping[str, Any], a: str, b: str, *, required: bool = False) -> Any:
    av, bv = raw.get(a), raw.get(b)
    if av is not None and bv is not None and av != bv:
        raise ValueError(f"conflicting_{a}_{b}")
    value = av if av is not None else bv
    if required and (value is None or value == ""):
        raise ValueError(f"{a}_required")
    return value


def _normalize_deadline(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValueError("deadline_must_be_string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("deadline_must_be_timezone_aware")
    return parsed.isoformat()


def sanitize_agent2agent_task(
    raw: Mapping[str, Any], *,
    trusted_policy: Mapping[str, Any] | None = None,
    trusted_estimates: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize a permitted public agent2agent.market task without trusting self-asserted policy."""
    if not isinstance(raw, Mapping):
        raise ValueError("agent2agent_task_must_be_object")
    task_id = str(_coalesce_alias(raw, "task_id", "id", required=True))
    status = str(raw.get("state", raw.get("status", ""))).upper()
    if status != "OPEN":
        raise ValueError("agent2agent_task_not_open")
    bounty = _coalesce_alias(raw, "bounty", "bounty_usd", required=True)
    try:
        bounty_value = float(bounty)
    except (TypeError, ValueError) as exc:
        raise ValueError("agent2agent_bounty_invalid") from exc
    if bounty_value <= 0:
        raise ValueError("agent2agent_bounty_invalid")
    currency = str(raw.get("currency", "USDC")).upper()
    if currency not in {"USD", "USDC"}:
        raise ValueError("agent2agent_currency_unsupported")
    raw_skills = raw.get("skills", raw.get("tags", []))
    if not isinstance(raw_skills, list) or not all(isinstance(v, str) and v for v in raw_skills):
        raise ValueError("agent2agent_skills_must_be_string_list")
    title = raw.get("title")
    if title is not None and not isinstance(title, str):
        raise ValueError("agent2agent_title_must_be_string")
    acceptance = _coalesce_alias(raw, "acceptance_criteria", "description")
    if acceptance is not None and not isinstance(acceptance, str):
        raise ValueError("agent2agent_description_must_be_string")
    deadline = _normalize_deadline(_coalesce_alias(raw, "deadline", "deadline_at"))
    metadata = _merge_trusted_metadata(
        trusted_policy, trusted_estimates, required_capabilities=raw_skills
    )
    return {
        "task_id": task_id,
        "title": title,
        "acceptance_criteria": acceptance,
        "bounty": bounty_value,
        "currency": currency,
        "skills": list(raw_skills),
        "deadline": deadline,
        "metadata": metadata,
    }


def _build_task_request_envelope(
    platform: str,
    sanitized: Sequence[Mapping[str, Any]], *,
    source_url: str,
    source_timestamp: str,
    captured_at: str,
    evidence_class: str | None = None,
    max_age_hours: float = 24.0,
) -> dict[str, Any]:
    effective_evidence = evidence_class or ("open_paid_request" if sanitized else "unknown")
    if effective_evidence == "open_paid_request" and not sanitized:
        raise ValueError("open_paid_request_evidence_requires_nonempty_records")
    snapshot = ingest_snapshot(
        platform=platform,
        source_url=source_url,
        source_timestamp=source_timestamp,
        evidence_class="official_api",
        payload={"items": [dict(item) for item in sanitized]},
        captured_at=captured_at,
        max_age_hours=max_age_hours,
    )
    return _saved_envelope(snapshot, effective_evidence)


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
    return _build_task_request_envelope(
        "payanagent", sanitized, source_url=source_url,
        source_timestamp=source_timestamp, captured_at=captured_at,
        evidence_class=evidence_class, max_age_hours=max_age_hours,
    )


def build_agent2agent_request_envelope(
    raw_tasks: Iterable[Mapping[str, Any]], *,
    source_url: str,
    source_timestamp: str,
    captured_at: str,
    trusted_policy_by_task_id: Mapping[str, Mapping[str, Any]] | None = None,
    trusted_estimates_by_task_id: Mapping[str, Mapping[str, Any]] | None = None,
    evidence_class: str | None = None,
    max_age_hours: float = 24.0,
) -> dict[str, Any]:
    sanitized: list[dict[str, Any]] = []
    for raw in raw_tasks:
        task_id = str(_coalesce_alias(raw, "task_id", "id", required=True))
        sanitized.append(sanitize_agent2agent_task(
            raw,
            trusted_policy=_trusted_for(task_id, trusted_policy_by_task_id),
            trusted_estimates=_trusted_for(task_id, trusted_estimates_by_task_id),
        ))
    return _build_task_request_envelope(
        "agent2agent_market", sanitized, source_url=source_url,
        source_timestamp=source_timestamp, captured_at=captured_at,
        evidence_class=evidence_class, max_age_hours=max_age_hours,
    )


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


def _request_only_bundle(
    platform: str, request_envelope: dict[str, Any], *,
    captured_at: str, signing_key: bytes,
    now: datetime | None = None, max_age_hours: float = 24.0,
) -> ObservationBundle:
    imported = import_saved_observation(request_envelope, now=now, max_age_hours=max_age_hours)
    task_items = (
        observe_imported_tasks(imported, now=now, max_age_hours=max_age_hours)
        if imported.demand_evidence.proves_open_paid_demand else []
    )
    task_audit = audit_export(task_items, generated_at=captured_at)
    manifest = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "platform": platform,
        "request_snapshot_sha256": request_envelope["snapshot"]["payload_sha256"],
        "receipt_snapshot_sha256": None,
        "task_audit_sha256": _stable_digest(task_audit),
        "utilization_sha256": None,
        "utilization_history_sha256": None,
        "dry_run_only": True,
        "action_enabled": False,
    }
    manifest_sha = canonical_payload_hash(manifest)
    return ObservationBundle(
        platform=platform, request_envelope=request_envelope, receipt_envelope=None,
        task_audit=task_audit, utilization=None, utilization_history=None,
        manifest=manifest, manifest_sha256=manifest_sha,
        signature_hmac_sha256=_sign_manifest(manifest_sha, signing_key),
    )


def build_agent2agent_observation_bundle(
    *, raw_tasks: Sequence[Mapping[str, Any]],
    source_url: str, source_timestamp: str, captured_at: str,
    signing_key: bytes,
    trusted_policy_by_task_id: Mapping[str, Mapping[str, Any]] | None = None,
    trusted_estimates_by_task_id: Mapping[str, Mapping[str, Any]] | None = None,
    now: datetime | None = None, max_age_hours: float = 24.0,
) -> ObservationBundle:
    request_envelope = build_agent2agent_request_envelope(
        raw_tasks, source_url=source_url, source_timestamp=source_timestamp,
        captured_at=captured_at,
        trusted_policy_by_task_id=trusted_policy_by_task_id,
        trusted_estimates_by_task_id=trusted_estimates_by_task_id,
        max_age_hours=max_age_hours,
    )
    return _request_only_bundle(
        "agent2agent_market", request_envelope, captured_at=captured_at,
        signing_key=signing_key, now=now, max_age_hours=max_age_hours,
    )


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
        "schema_version": BUNDLE_SCHEMA_VERSION,
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


def _verify_snapshot_record(snapshot: Any, *, expected_platform: str) -> bool:
    if not isinstance(snapshot, Mapping) or set(snapshot) != SNAPSHOT_FIELDS:
        return False
    if snapshot.get("platform") != expected_platform:
        return False
    payload = snapshot.get("payload")
    if not isinstance(payload, dict):
        return False
    return canonical_payload_hash(payload) == snapshot.get("payload_sha256")


def _verify_envelope(envelope: Any, *, expected_platform: str) -> bool:
    if not isinstance(envelope, Mapping):
        return False
    if set(envelope) != {"snapshot", "demand_evidence_class", "records_key"}:
        return False
    if envelope.get("records_key") != "items":
        return False
    return _verify_snapshot_record(envelope.get("snapshot"), expected_platform=expected_platform)


def verify_observation_bundle(bundle: ObservationBundle, signing_key: bytes) -> bool:
    if not isinstance(bundle, ObservationBundle):
        return False
    if not bundle.platform or bundle.manifest.get("platform") != bundle.platform:
        return False
    if set(bundle.manifest) != MANIFEST_FIELDS:
        return False
    if bundle.manifest.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        return False
    if bundle.manifest.get("dry_run_only") is not True or bundle.manifest.get("action_enabled") is not False:
        return False
    if not _verify_envelope(bundle.request_envelope, expected_platform=bundle.platform):
        return False
    if bundle.receipt_envelope is not None and not _verify_envelope(
        bundle.receipt_envelope, expected_platform=bundle.platform
    ):
        return False
    if bundle.manifest.get("request_snapshot_sha256") != bundle.request_envelope["snapshot"]["payload_sha256"]:
        return False
    expected_receipt_sha = (
        bundle.receipt_envelope["snapshot"]["payload_sha256"] if bundle.receipt_envelope else None
    )
    if bundle.manifest.get("receipt_snapshot_sha256") != expected_receipt_sha:
        return False
    if bundle.manifest.get("task_audit_sha256") != _stable_digest(bundle.task_audit):
        return False
    if bundle.manifest.get("utilization_sha256") != _stable_digest(bundle.utilization):
        return False
    if bundle.manifest.get("utilization_history_sha256") != _stable_digest(bundle.utilization_history):
        return False
    if canonical_payload_hash(bundle.manifest) != bundle.manifest_sha256:
        return False
    try:
        expected = _sign_manifest(bundle.manifest_sha256, signing_key)
    except ValueError:
        return False
    return hmac.compare_digest(expected, bundle.signature_hmac_sha256)


def observation_bundle_record(bundle: ObservationBundle) -> dict[str, Any]:
    return asdict(bundle)


def serialize_observation_bundle(bundle: ObservationBundle) -> str:
    """Return deterministic JSON suitable for offline persistence."""
    return json.dumps(
        observation_bundle_record(bundle), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False,
    )


def _load_bundle_value(value: str | bytes | Path | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(value, Mapping):
        parsed = dict(value)
    else:
        if isinstance(value, Path):
            raw = value.read_text(encoding="utf-8")
        elif isinstance(value, bytes):
            raw = value.decode("utf-8")
        elif isinstance(value, str):
            stripped = value.lstrip()
            raw = value if stripped.startswith("{") else Path(value).read_text(encoding="utf-8")
        else:
            raise ValueError("unsupported_observation_bundle_input")
        parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("observation_bundle_must_be_object")
    return parsed


def load_observation_bundle(
    value: str | bytes | Path | Mapping[str, Any], *,
    signing_key: bytes,
) -> ObservationBundle:
    """Reload a persisted bundle fail-closed; no network or freshness assumption is made."""
    parsed = _load_bundle_value(value)
    if set(parsed) != BUNDLE_RECORD_FIELDS:
        raise ValueError("observation_bundle_schema_mismatch")
    manifest = parsed.get("manifest")
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        raise ValueError("observation_bundle_manifest_schema_mismatch")
    if manifest.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise ValueError("observation_bundle_schema_version_unsupported")
    bundle = ObservationBundle(**parsed)
    if not verify_observation_bundle(bundle, signing_key):
        raise ValueError("observation_bundle_integrity_verification_failed")
    return bundle
