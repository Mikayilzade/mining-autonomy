"""Reproducible read-only evidence snapshots for implementation observations.

No network access, authentication, task acceptance, publication, or settlement is
performed here. Snapshots are sanitized evidence envelopes that can be replayed.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any
from urllib.parse import urlparse

EVIDENCE_CLASSES = {"official_api", "official_page", "official_docs", "onchain", "third_party"}


@dataclass(frozen=True)
class EvidenceSnapshot:
    platform: str
    source_url: str
    source_timestamp: str
    captured_at: str
    evidence_class: str
    payload: dict[str, Any]
    payload_sha256: str


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp_must_be_timezone_aware")
    return dt.astimezone(timezone.utc)


def canonical_payload_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def ingest_snapshot(*, platform: str, source_url: str, source_timestamp: str,
                    evidence_class: str, payload: dict[str, Any], captured_at: str | None = None,
                    max_age_hours: float = 24.0) -> EvidenceSnapshot:
    if evidence_class not in EVIDENCE_CLASSES:
        raise ValueError("unsupported_evidence_class")
    parsed = urlparse(source_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("https_source_required")
    source_dt = _parse_utc(source_timestamp)
    capture_dt = _parse_utc(captured_at) if captured_at else datetime.now(timezone.utc)
    age_hours = (capture_dt - source_dt).total_seconds() / 3600
    if age_hours < -0.1:
        raise ValueError("source_timestamp_in_future")
    if age_hours > max_age_hours:
        raise ValueError("stale_snapshot")
    if not isinstance(payload, dict):
        raise ValueError("payload_must_be_object")
    return EvidenceSnapshot(platform=platform, source_url=source_url,
        source_timestamp=source_dt.isoformat(), captured_at=capture_dt.isoformat(),
        evidence_class=evidence_class, payload=payload,
        payload_sha256=canonical_payload_hash(payload))


def verify_snapshot(snapshot: EvidenceSnapshot) -> bool:
    return snapshot.payload_sha256 == canonical_payload_hash(snapshot.payload)


def snapshot_record(snapshot: EvidenceSnapshot) -> dict[str, Any]:
    return asdict(snapshot)
