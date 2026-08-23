"""I129 fail-closed local energy measurement receipt for python_local.

This module does not read privileged hardware counters by itself and never invents a
tariff. It turns independently observed before/after energy-counter readings plus an
explicit tariff into a hash-bound receipt that can feed the existing I054/I128
EnergyMeasurement path.

Supported counter unit is joules. The caller must obtain readings from a trustworthy
local meter/telemetry source. Counter wrap/reset, missing source identity, zero work,
negative deltas, stale/mismatched receipt content, and non-explicit tariffs fail closed.
No network, credentials, spend, market action or value movement occurs here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

from resource_evidence_adapter import EnergyMeasurement

SCHEMA = "mining-autonomy/i129-energy-measurement-receipt/v1"
JOULES_PER_KWH = 3_600_000.0


@dataclass(frozen=True)
class EnergyReceipt:
    schema: str
    backend_id: str
    workload_id: str
    task_count: int
    counter_source_ref: str
    counter_source_digest: str
    counter_unit: str
    energy_before: float
    energy_after: float
    energy_delta_joules: float
    energy_kwh_per_task: float
    tariff_usd_per_kwh: float
    tariff_source_ref: str
    tariff_source_digest: str
    observed_at: str
    max_age_seconds: int
    receipt_hash: str
    network_enabled: bool = False
    credentials_used: bool = False
    spend_performed: bool = False
    value_movement_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("observed_at_must_be_utc")
    return dt


def _hash_body(receipt: EnergyReceipt) -> dict[str, Any]:
    body = asdict(receipt)
    body["receipt_hash"] = ""
    return body


def build_energy_receipt(
    *, workload_id: str, task_count: int, counter_source_ref: str,
    counter_source_digest: str, energy_before_joules: float,
    energy_after_joules: float, tariff_usd_per_kwh: float,
    tariff_source_ref: str, tariff_source_digest: str, observed_at: str,
    max_age_seconds: int = 604800,
) -> EnergyReceipt:
    if not workload_id.strip():
        raise ValueError("workload_id_required")
    if task_count <= 0:
        raise ValueError("positive_task_count_required")
    if not counter_source_ref.strip() or len(counter_source_digest) < 16:
        raise ValueError("counter_source_identity_required")
    if not tariff_source_ref.strip() or len(tariff_source_digest) < 16:
        raise ValueError("explicit_tariff_source_required")
    _parse_utc(observed_at)
    if max_age_seconds <= 0:
        raise ValueError("positive_max_age_required")
    before = float(energy_before_joules)
    after = float(energy_after_joules)
    if before < 0 or after < 0 or after < before:
        raise ValueError("energy_counter_wrap_reset_or_negative_delta")
    tariff = float(tariff_usd_per_kwh)
    if tariff < 0:
        raise ValueError("tariff_must_be_nonnegative")
    delta = after - before
    per_task = delta / JOULES_PER_KWH / task_count
    draft = EnergyReceipt(
        schema=SCHEMA, backend_id="python_local", workload_id=workload_id,
        task_count=task_count, counter_source_ref=counter_source_ref,
        counter_source_digest=counter_source_digest, counter_unit="joules",
        energy_before=before, energy_after=after, energy_delta_joules=delta,
        energy_kwh_per_task=per_task, tariff_usd_per_kwh=tariff,
        tariff_source_ref=tariff_source_ref, tariff_source_digest=tariff_source_digest,
        observed_at=observed_at, max_age_seconds=max_age_seconds, receipt_hash="",
    )
    return replace(draft, receipt_hash=_digest(_hash_body(draft)))


def verify_energy_receipt(receipt: EnergyReceipt, *, now: datetime) -> None:
    if receipt.schema != SCHEMA or receipt.backend_id != "python_local":
        raise ValueError("energy_receipt_scope_mismatch")
    if receipt.receipt_hash != _digest(_hash_body(receipt)):
        raise ValueError("energy_receipt_hash_invalid")
    observed = _parse_utc(receipt.observed_at)
    if now.tzinfo is None:
        raise ValueError("now_must_be_timezone_aware")
    age = (now.astimezone(timezone.utc) - observed).total_seconds()
    if age < 0 or age > receipt.max_age_seconds:
        raise ValueError("energy_receipt_not_current")
    rebuilt = build_energy_receipt(
        workload_id=receipt.workload_id, task_count=receipt.task_count,
        counter_source_ref=receipt.counter_source_ref,
        counter_source_digest=receipt.counter_source_digest,
        energy_before_joules=receipt.energy_before, energy_after_joules=receipt.energy_after,
        tariff_usd_per_kwh=receipt.tariff_usd_per_kwh,
        tariff_source_ref=receipt.tariff_source_ref,
        tariff_source_digest=receipt.tariff_source_digest,
        observed_at=receipt.observed_at, max_age_seconds=receipt.max_age_seconds,
    )
    if rebuilt.receipt_hash != receipt.receipt_hash:
        raise ValueError("energy_receipt_rebuild_mismatch")
    if any((receipt.network_enabled, receipt.credentials_used, receipt.spend_performed, receipt.value_movement_enabled)):
        raise ValueError("energy_receipt_not_inert")


def to_energy_measurement(receipt: EnergyReceipt, *, now: datetime) -> EnergyMeasurement:
    verify_energy_receipt(receipt, now=now)
    source_digest = _digest({
        "receipt_hash": receipt.receipt_hash,
        "counter_source_digest": receipt.counter_source_digest,
        "tariff_source_digest": receipt.tariff_source_digest,
    })
    return EnergyMeasurement(
        energy_kwh_per_task=receipt.energy_kwh_per_task,
        tariff_usd_per_kwh=receipt.tariff_usd_per_kwh,
        observed_at=receipt.observed_at,
        max_age_seconds=receipt.max_age_seconds,
        source_ref=f"i129-energy-receipt:{receipt.receipt_hash}",
        source_content_digest=source_digest,
        notes=(
            f"I129 verified receipt; workload={receipt.workload_id}; tasks={receipt.task_count}; "
            f"counter_source={receipt.counter_source_ref}; tariff_source={receipt.tariff_source_ref}."
        ),
    )


def receipt_from_mapping(raw: Mapping[str, Any]) -> EnergyReceipt:
    return EnergyReceipt(**dict(raw))
