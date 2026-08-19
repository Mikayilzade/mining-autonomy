"""Strict offline aggregation for saved paid-utilization observations.

Consumes only already-saved, verified snapshots classified as settled receipts or
paid invocations. It never fetches, authenticates, pays, publishes, or settles.
Buyer identifiers must already be sanitized to SHA-256 hashes if retained.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import re
from statistics import mean, median
from typing import Any

from observation_importer import ImportedObservation
from snapshot import records_from_snapshot

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RAW_IDENTITY_FIELDS = {
    "buyer", "buyer_id", "buyer_address", "wallet", "wallet_address",
    "customer", "customer_id", "payer", "payer_address",
}

@dataclass(frozen=True)
class UtilizationSummary:
    platform: str
    evidence_class: str
    transaction_count: int
    total_value_usd: float
    average_value_usd: float
    median_value_usd: float
    unique_hashed_buyers: int
    repeat_hashed_buyers: int
    top_hashed_buyer_value_share: float | None
    active_days: int
    first_observed_at: str
    last_observed_at: str

def _parse_utc(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("utilization_timestamp_required")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("utilization_timestamp_must_be_timezone_aware")
    return dt.astimezone(timezone.utc)

def _amount(record: dict[str, Any]) -> float:
    values = [record.get(k) for k in ("amount_usd", "value_usd", "payment_usd") if record.get(k) is not None]
    if len(values) != 1:
        raise ValueError("exactly_one_utilization_value_required")
    try:
        value = float(values[0])
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid_utilization_value") from exc
    if value <= 0:
        raise ValueError("positive_utilization_value_required")
    return value

def _timestamp(record: dict[str, Any]) -> datetime:
    values = [record.get(k) for k in ("occurred_at", "settled_at", "timestamp") if record.get(k) is not None]
    if len(values) != 1:
        raise ValueError("exactly_one_utilization_timestamp_required")
    return _parse_utc(values[0])

def _buyer_hash(record: dict[str, Any]) -> str | None:
    if any(field in record for field in _RAW_IDENTITY_FIELDS):
        raise ValueError("raw_buyer_identity_not_allowed")
    value = record.get("buyer_hash")
    if value is None:
        return None
    if not isinstance(value, str) or not _SHA256.fullmatch(value.lower()):
        raise ValueError("buyer_hash_must_be_sha256")
    return value.lower()

def aggregate_imported_utilization(imported: ImportedObservation, *, now: datetime | None = None, max_age_hours: float = 24.0) -> UtilizationSummary:
    if not isinstance(imported, ImportedObservation):
        raise ValueError("imported_observation_required")
    if not imported.demand_evidence.proves_paid_utilization:
        raise ValueError("paid_utilization_evidence_required")
    records = records_from_snapshot(imported.snapshot, records_key=imported.records_key, now=now, max_age_hours=max_age_hours)
    if not records:
        raise ValueError("utilization_records_required")
    amounts=[]; timestamps=[]; buyer_counts=Counter(); buyer_values=defaultdict(float)
    for record in records:
        amount=_amount(record); timestamp=_timestamp(record); buyer=_buyer_hash(record)
        amounts.append(amount); timestamps.append(timestamp)
        if buyer is not None:
            buyer_counts[buyer]+=1; buyer_values[buyer]+=amount
    total=sum(amounts)
    top_share=max(buyer_values.values())/total if buyer_values else None
    first=min(timestamps); last=max(timestamps)
    return UtilizationSummary(imported.snapshot.platform, imported.demand_evidence.evidence_class, len(records), round(total,6), round(mean(amounts),6), round(median(amounts),6), len(buyer_counts), sum(1 for c in buyer_counts.values() if c>1), round(top_share,6) if top_share is not None else None, len({ts.date() for ts in timestamps}), first.isoformat(), last.isoformat())

def utilization_record(summary: UtilizationSummary) -> dict[str, Any]:
    return asdict(summary)
