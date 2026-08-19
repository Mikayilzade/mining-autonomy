"""Offline importer for saved observation/evidence envelopes.

The importer performs no HTTP requests, authentication, task acceptance, service
publication or settlement. It only parses already-saved JSON and reuses snapshot
provenance/integrity/freshness checks before allowing replay.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping

from demand_evidence import DemandEvidence, classify_demand_evidence
from snapshot import EvidenceSnapshot, replay_task_snapshot, validate_snapshot


@dataclass(frozen=True)
class ImportedObservation:
    snapshot: EvidenceSnapshot
    demand_evidence: DemandEvidence
    records_key: str
    imported_at: str


def _load_saved(value: str | bytes | Path | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, Path):
        raw = value.read_text(encoding="utf-8")
    elif isinstance(value, bytes):
        raw = value.decode("utf-8")
    elif isinstance(value, str):
        stripped = value.lstrip()
        if stripped.startswith("{"):
            raw = value
        else:
            raw = Path(value).read_text(encoding="utf-8")
    else:
        raise ValueError("unsupported_saved_observation_input")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("saved_observation_must_be_object")
    return parsed


def import_saved_observation(value: str | bytes | Path | Mapping[str, Any], *,
                             now: datetime | None = None,
                             max_age_hours: float = 24.0) -> ImportedObservation:
    envelope = _load_saved(value)
    snapshot_raw = envelope.get("snapshot")
    if not isinstance(snapshot_raw, dict):
        raise ValueError("saved_observation_snapshot_required")
    required = {
        "platform", "source_url", "source_timestamp", "captured_at",
        "evidence_class", "payload", "payload_sha256",
    }
    if set(snapshot_raw) != required:
        raise ValueError("saved_observation_snapshot_schema_mismatch")
    snapshot = EvidenceSnapshot(**snapshot_raw)
    validate_snapshot(snapshot, now=now, max_age_hours=max_age_hours)
    evidence = classify_demand_evidence(envelope.get("demand_evidence_class"))
    records_key = envelope.get("records_key", "items")
    if not isinstance(records_key, str) or not records_key:
        raise ValueError("records_key_required")
    imported_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    return ImportedObservation(snapshot, evidence, records_key, imported_at)


def replay_imported_open_tasks(imported: ImportedObservation, *,
                               now: datetime | None = None,
                               max_age_hours: float = 24.0,
                               adapters: Mapping[str, Any] | None = None) -> list[Any]:
    """Replay only evidence explicitly classified as a current paid request."""
    if not imported.demand_evidence.proves_open_paid_demand:
        raise ValueError("open_paid_request_evidence_required")
    return replay_task_snapshot(
        imported.snapshot,
        records_key=imported.records_key,
        now=now,
        max_age_hours=max_age_hours,
        adapters=adapters,
    )
