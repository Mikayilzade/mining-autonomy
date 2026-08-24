#!/usr/bin/env python3
"""I168 fail-closed adapter from I166/I167 owned-PC facts to I050-shaped evidence.

The adapter is intentionally narrow. It converts only resource facts that are already
bound to an accepted I166 real-user-PC packet and a matching I167 Router bridge. It
never invents ownership/accounting/interface-control facts just to make I050 complete.

This file is self-contained so its mapping logic can be exact-source tested without
loading the broader Router graph. The emitted record schema/hash algorithm mirrors the
current I050 ResourceEvidence contract and is source-bound to the current I050/I066
Git blobs recorded below. A source drift requires review before promotion.

No network, credentials, CI dispatch, account creation, paid infrastructure, task
acceptance, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA = "mining-autonomy/i168-owned-pc-i050-evidence-adapter/v1"
I050_RESOURCE_PROFILE_BLOB_SHA = "9b76a2194d15f8277d15b2e46c85df71cca08874"
I066_MATERIALIZATION_BLOB_SHA = "d995821e27ec27d72531dc71b433de702fb8fe7b"

I050_CRITICAL_PARAMETERS = (
    "currently_available",
    "programmatic_access",
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
    "quota_units_remaining",
    "electricity_per_task_usd",
    "latency_seconds",
    "reliability_probability",
    "quality_probability",
    "max_parallelism",
    "rate_limit_per_minute",
)

MEASURED_PARAMETERS = (
    "currently_available",
    "programmatic_access",
    "electricity_per_task_usd",
    "latency_seconds",
    "reliability_probability",
    "quality_probability",
    "max_parallelism",
)

CONTROL_PARAMETERS = tuple(x for x in I050_CRITICAL_PARAMETERS if x not in MEASURED_PARAMETERS)


@dataclass(frozen=True)
class I050Record:
    evidence_id: str
    backend_id: str
    parameter: str
    value: Any
    source_kind: str
    source_ref: str
    observed_at: str
    max_age_seconds: int
    reference_backend_hash: str
    source_content_digest: str
    notes: str = ""
    evidence_hash: str | None = None

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("evidence_hash", None)
        return body


@dataclass(frozen=True)
class AdapterResult:
    state: str
    errors: tuple[str, ...]
    backend_id: str
    emitted_records: tuple[I050Record, ...]
    emitted_parameters: tuple[str, ...]
    missing_control_parameters: tuple[str, ...]
    i166_i167_source_binding_valid: bool
    reference_backend_hash: str | None
    i050_source_blob_sha: str = I050_RESOURCE_PROFILE_BLOB_SHA
    i066_source_blob_sha: str = I066_MATERIALIZATION_BLOB_SHA
    i050_attestation_executed: bool = False
    i066_materialization_executed: bool = False
    i123_promotion_performed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _git_source_digest(value: Mapping[str, Any]) -> str:
    # Matches I167's source digest over the complete I166 result.
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("observed_at_must_be_utc")
    return dt


def _make_record(
    *, parameter: str, value: Any, source_kind: str, source_ref: str,
    source_content_digest: str, observed_at: str, reference_hash: str,
    max_age_seconds: int, notes: str,
) -> I050Record:
    draft = I050Record(
        evidence_id=f"i168-owned-pc-{parameter}",
        backend_id="owned_pc",
        parameter=parameter,
        value=value,
        source_kind=source_kind,
        source_ref=source_ref,
        observed_at=observed_at,
        max_age_seconds=max_age_seconds,
        reference_backend_hash=reference_hash,
        source_content_digest=source_content_digest,
        notes=notes,
    )
    return I050Record(**{**asdict(draft), "evidence_hash": _digest(draft.hash_body())})


def build_adapter(
    i166_result: Mapping[str, Any],
    i167_result: Mapping[str, Any],
    reference_backend: Mapping[str, Any],
    *,
    observed_at: str,
) -> AdapterResult:
    errors: list[str] = []
    try:
        _parse_utc(observed_at)
    except Exception:
        errors.append("observed_at_must_be_utc")

    if str(reference_backend.get("backend_id") or "") != "owned_pc":
        errors.append("owned_pc_reference_required")
    if str(reference_backend.get("family") or "") != "owned_pc":
        errors.append("owned_pc_reference_family_required")
    reference_hash = _digest(dict(reference_backend)) if not errors or reference_backend else None

    if i167_result.get("state") != "ROUTER_RESOURCE_FACTS_READY":
        errors.append("i167_router_resource_facts_not_ready")
    if i167_result.get("backend_id") != "owned_pc":
        errors.append("i167_backend_identity_mismatch")

    expected_i166_digest = _git_source_digest(i166_result)
    binding_valid = i167_result.get("source_digest") == expected_i166_digest
    if not binding_valid:
        errors.append("i166_i167_source_digest_mismatch")

    gate = i166_result.get("gate")
    if not isinstance(gate, Mapping) or gate.get("state") != "REAL_EXTERNAL_EVIDENCE_ACCEPTED":
        errors.append("i166_real_external_evidence_not_accepted")
    if isinstance(gate, Mapping) and gate.get("ownership_confirmation_supplied") is not True:
        errors.append("i166_ownership_confirmation_missing")

    i165 = i166_result.get("i165_result")
    if not isinstance(i165, Mapping) or i165.get("state") != "USER_PC_MATERIALIZED":
        errors.append("i165_user_pc_not_materialized")
        i165 = {}
    packet = i165.get("i162_packet") if isinstance(i165, Mapping) else None
    if not isinstance(packet, Mapping) or packet.get("state") != "USER_PC_PACKET_COMPLETE":
        errors.append("i162_packet_not_complete")
        packet = {}
    evaluation = packet.get("i159_evaluation") if isinstance(packet, Mapping) else None
    if not isinstance(evaluation, Mapping) or evaluation.get("production_evidence_ready") is not True:
        errors.append("i159_production_evidence_not_ready")
        evaluation = {}
    observation = evaluation.get("observation") if isinstance(evaluation, Mapping) else None
    if not isinstance(observation, Mapping) or observation.get("deterministic_programmatic_access_verified") is not True:
        errors.append("programmatic_access_not_verified")
        observation = {}

    explicit = packet.get("explicit_measurements") if isinstance(packet, Mapping) else None
    if not isinstance(explicit, Mapping):
        errors.append("explicit_measurements_missing")
        explicit = {}

    patch = i167_result.get("router_backend_patch")
    if not isinstance(patch, Mapping):
        errors.append("i167_router_backend_patch_missing")
        patch = {}

    required_patch = {
        "currently_available",
        "electricity_per_task_usd",
        "latency_seconds",
        "reliability_probability",
        "quality_probability",
        "max_parallelism",
    }
    for name in sorted(required_patch):
        if name not in patch:
            errors.append(f"i167_patch_missing:{name}")

    benchmark_ref = explicit.get("benchmark_source_ref")
    environment_ref = observation.get("measurement_environment_ref") or explicit.get("measurement_environment_ref")
    availability_ref = explicit.get("availability_source_ref")
    energy_ref = explicit.get("energy_source_ref")
    tariff_ref = explicit.get("tariff_source_ref")
    for name, value in (
        ("benchmark_source_ref", benchmark_ref),
        ("measurement_environment_ref", environment_ref),
        ("availability_source_ref", availability_ref),
        ("energy_source_ref", energy_ref),
        ("tariff_source_ref", tariff_ref),
    ):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing_source_ref:{name}")

    errors = sorted(set(errors))
    if errors or reference_hash is None:
        return AdapterResult(
            state="PASS_BLOCKED",
            errors=tuple(errors),
            backend_id="owned_pc",
            emitted_records=(),
            emitted_parameters=(),
            missing_control_parameters=CONTROL_PARAMETERS,
            i166_i167_source_binding_valid=binding_valid,
            reference_backend_hash=reference_hash,
        )

    measured_source_digest = str(i167_result["source_digest"])
    benchmark_digest = _digest({
        "i166_source_digest": measured_source_digest,
        "benchmark_source_ref": benchmark_ref,
        "measurement_environment_ref": environment_ref,
        "latency_seconds": patch["latency_seconds"],
        "reliability_probability": patch["reliability_probability"],
        "quality_probability": patch["quality_probability"],
        "max_parallelism": patch["max_parallelism"],
    })
    availability_digest = _digest({
        "i166_source_digest": measured_source_digest,
        "availability_source_ref": availability_ref,
        "currently_available": patch["currently_available"],
        "measured_available_hours_per_day": explicit.get("measured_available_hours_per_day"),
    })
    energy_digest = _digest({
        "i166_source_digest": measured_source_digest,
        "energy_source_ref": energy_ref,
        "tariff_source_ref": tariff_ref,
        "derived_energy_kwh_per_task": packet.get("derived_energy_kwh_per_task"),
        "electricity_per_task_usd": patch["electricity_per_task_usd"],
    })

    records = (
        _make_record(
            parameter="currently_available", value=bool(patch["currently_available"]),
            source_kind="measured_local", source_ref=f"i166-availability:{availability_ref}",
            source_content_digest=availability_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="I168 projection of I166/I167 availability evidence; no 24/7 assumption.",
        ),
        _make_record(
            parameter="programmatic_access", value=True,
            source_kind="system_probe", source_ref=f"i163-session:{environment_ref}",
            source_content_digest=benchmark_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="Exact local deterministic benchmark session verified programmatic execution only.",
        ),
        _make_record(
            parameter="electricity_per_task_usd", value=float(patch["electricity_per_task_usd"]),
            source_kind="measured_local", source_ref=f"i166-energy:{energy_ref};tariff:{tariff_ref}",
            source_content_digest=energy_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=604800,
            notes="Derived only from accepted before/after energy readings plus explicit tariff.",
        ),
        _make_record(
            parameter="latency_seconds", value=float(patch["latency_seconds"]),
            source_kind="system_probe", source_ref=str(benchmark_ref),
            source_content_digest=benchmark_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="Measured fixed local benchmark latency.",
        ),
        _make_record(
            parameter="reliability_probability", value=float(patch["reliability_probability"]),
            source_kind="system_probe", source_ref=str(benchmark_ref),
            source_content_digest=benchmark_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="Measured fixed local benchmark reliability.",
        ),
        _make_record(
            parameter="quality_probability", value=float(patch["quality_probability"]),
            source_kind="system_probe", source_ref=str(benchmark_ref),
            source_content_digest=benchmark_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="Measured exact-output acceptance probability for the fixed local benchmark.",
        ),
        _make_record(
            parameter="max_parallelism", value=int(patch["max_parallelism"]),
            source_kind="system_probe", source_ref=str(benchmark_ref),
            source_content_digest=benchmark_digest, observed_at=observed_at,
            reference_hash=reference_hash, max_age_seconds=86400,
            notes="Measured safe parallelism exercised by I163; never inferred from CPU count.",
        ),
    )
    emitted = tuple(record.parameter for record in records)
    if emitted != MEASURED_PARAMETERS:
        raise AssertionError("i168_measured_parameter_order_drift")

    return AdapterResult(
        state="PARTIAL_I050_EVIDENCE_READY",
        errors=(),
        backend_id="owned_pc",
        emitted_records=records,
        emitted_parameters=emitted,
        missing_control_parameters=CONTROL_PARAMETERS,
        i166_i167_source_binding_valid=True,
        reference_backend_hash=reference_hash,
    )


def payload(result: AdapterResult) -> dict[str, Any]:
    body = asdict(result)
    body["emitted_records"] = [asdict(record) for record in result.emitted_records]
    body.update({
        "schema": SCHEMA,
        "run": "I168",
        "critical_parameter_count": len(I050_CRITICAL_PARAMETERS),
        "emitted_parameter_count": len(result.emitted_parameters),
        "missing_control_parameter_count": len(result.missing_control_parameters),
        "next_gate": (
            "Acquire provenance-bound evidence for the seven remaining I050 control/accounting/interface "
            "parameters without copying synthetic Router defaults. Only after a complete current I050 "
            "attestation may I066 materialization be attempted. I168 itself cannot promote I123 evidence."
        ),
    })
    return body
