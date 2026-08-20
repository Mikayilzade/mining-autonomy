"""Deterministic resource-calibration acquisition plan and offline probe contract (I053).

This module does not inspect hardware, read credentials, access the network, spend
money, or enable execution. It defines exactly which local/no-new-spend resource
facts may be measured and which must remain explicit declarations/provider facts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
from typing import Any, Iterable, Mapping, Optional

from resource_profile_evidence import CRITICAL_PARAMETERS, reference_backend_hash

LOCAL_NO_SPEND_FAMILIES = {"deterministic_python", "owned_pc"}


@dataclass(frozen=True)
class AcquisitionRequirement:
    parameter: str
    preferred_source_kind: str
    accepted_source_kinds: tuple[str, ...]
    acquisition_method: str
    must_not_infer: bool
    requires_source_digest: bool
    max_age_seconds: int


@dataclass(frozen=True)
class OfflineProbeContract:
    backend_id: str
    reference_backend_hash: str
    benchmark_id: str
    expected_output_digest: str
    minimum_repetitions: int = 10
    network_allowed: bool = False
    credentials_allowed: bool = False
    paid_service_allowed: bool = False
    value_movement_allowed: bool = False


@dataclass(frozen=True)
class ProbeObservation:
    run_id: str
    latency_seconds: float
    execution_succeeded: bool
    output_digest: Optional[str]
    quality_passed: bool


@dataclass(frozen=True)
class ProbeSummary:
    backend_id: str
    benchmark_id: str
    observation_count: int
    successful_runs: int
    quality_passed_runs: int
    latency_p95_seconds: float
    reliability_probability: float
    quality_probability: float
    max_parallelism_observed: int
    rate_limit_per_minute_observed: Optional[float]
    transcript_digest: str
    measured_parameters: Mapping[str, Any]
    network_enabled: bool = False
    credentials_used: bool = False
    spend_performed: bool = False
    value_movement_enabled: bool = False


@dataclass(frozen=True)
class CalibrationAcquisitionPlan:
    backend_id: str
    backend_family: str
    reference_backend_hash: str
    target_state: str
    requirements: tuple[AcquisitionRequirement, ...]
    probe_contract: OfflineProbeContract
    planning_only_until_attested: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _canonical_hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def build_local_no_spend_plan(
    reference_backend: Mapping[str, Any],
    *,
    benchmark_id: str,
    expected_output_digest: str,
) -> CalibrationAcquisitionPlan:
    """Define exact acquisition requirements without asserting that the backend exists."""
    backend = dict(reference_backend)
    backend_id = str(backend.get("backend_id") or "")
    family = str(backend.get("family") or "")
    if not backend_id:
        raise ValueError("backend_id_required")
    if family not in LOCAL_NO_SPEND_FAMILIES:
        raise ValueError("backend_not_local_no_spend_priority")
    if not benchmark_id.strip() or len(expected_output_digest) < 16:
        raise ValueError("benchmark_identity_required")

    requirements = (
        AcquisitionRequirement("currently_available", "system_probe", ("system_probe", "user_declared"), "offline local runner availability probe", False, True, 86400),
        AcquisitionRequirement("programmatic_access", "system_probe", ("system_probe", "user_declared"), "invoke the exact local interface with a fixed offline fixture", False, True, 86400),
        AcquisitionRequirement("requires_credentials", "user_declared", ("user_declared", "system_probe"), "explicit interface constraint; a probe only proves credentials were not used in that probe", True, False, 604800),
        AcquisitionRequirement("requires_paid_account", "user_declared", ("user_declared", "provider_first_party", "system_probe"), "explicit ownership/interface constraint", True, False, 604800),
        AcquisitionRequirement("requires_new_spend", "user_declared", ("user_declared", "system_probe"), "explicit no-new-spend statement bound to this backend", True, False, 604800),
        AcquisitionRequirement("fixed_monthly_cost_usd", "user_declared", ("user_declared", "provider_first_party"), "explicit recurring/already-paid cost statement", True, False, 2592000),
        AcquisitionRequirement("sunk_or_already_committed", "user_declared", ("user_declared",), "explicit accounting classification", True, False, 2592000),
        AcquisitionRequirement("quota_units_remaining", "user_declared", ("user_declared", "provider_first_party", "system_probe"), "explicit quota/capacity fact; None must be intentional and never inferred", True, False, 86400),
        AcquisitionRequirement("electricity_per_task_usd", "measured_local", ("measured_local", "user_declared"), "derive only from measured energy plus explicit electricity tariff, or declare directly", True, True, 604800),
        AcquisitionRequirement("latency_seconds", "system_probe", ("system_probe", "measured_local"), "p95 latency from a fixed offline benchmark transcript", False, True, 86400),
        AcquisitionRequirement("reliability_probability", "system_probe", ("system_probe", "measured_local"), "successful runs divided by total fixed benchmark runs", False, True, 86400),
        AcquisitionRequirement("quality_probability", "system_probe", ("system_probe", "measured_local"), "quality-passing successful runs divided by successful runs", False, True, 86400),
        AcquisitionRequirement("max_parallelism", "system_probe", ("system_probe", "measured_local", "user_declared"), "bounded concurrency probe; never infer from CPU/GPU count", True, True, 86400),
        AcquisitionRequirement("rate_limit_per_minute", "user_declared", ("user_declared", "system_probe", "provider_first_party"), "explicit interface limit; None must be intentional and never inferred", True, False, 86400),
    )
    if {r.parameter for r in requirements} != set(CRITICAL_PARAMETERS):
        raise AssertionError("acquisition_plan_must_cover_all_critical_parameters")

    return CalibrationAcquisitionPlan(
        backend_id=backend_id,
        backend_family=family,
        reference_backend_hash=reference_backend_hash(backend),
        target_state="calibrated_declared_or_reproducible",
        requirements=requirements,
        probe_contract=OfflineProbeContract(
            backend_id=backend_id,
            reference_backend_hash=reference_backend_hash(backend),
            benchmark_id=benchmark_id,
            expected_output_digest=expected_output_digest,
        ),
    )


def _p95(values: list[float]) -> float:
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[index]


def evaluate_probe_transcript(
    contract: OfflineProbeContract,
    observations: Iterable[ProbeObservation],
    *,
    max_parallelism_observed: int,
    rate_limit_per_minute_observed: Optional[float] = None,
) -> ProbeSummary:
    """Reduce an already-collected offline transcript into reproducible measured facts.

    The function itself performs no benchmark execution. The transcript must come
    from an external local harness that obeys this inert contract.
    """
    if contract.network_allowed or contract.credentials_allowed or contract.paid_service_allowed or contract.value_movement_allowed:
        raise ValueError("probe_contract_not_inert")
    rows = list(observations)
    if len(rows) < contract.minimum_repetitions:
        raise ValueError("insufficient_probe_repetitions")
    if max_parallelism_observed < 1:
        raise ValueError("invalid_parallelism_observation")
    if rate_limit_per_minute_observed is not None and rate_limit_per_minute_observed <= 0:
        raise ValueError("invalid_rate_limit_observation")

    run_ids: set[str] = set()
    for row in rows:
        if not row.run_id or row.run_id in run_ids:
            raise ValueError("duplicate_or_missing_run_id")
        run_ids.add(row.run_id)
        if row.latency_seconds < 0:
            raise ValueError("invalid_latency")
        if row.quality_passed and (
            not row.execution_succeeded or row.output_digest != contract.expected_output_digest
        ):
            raise ValueError("invalid_quality_pass_claim")

    successful = [row for row in rows if row.execution_succeeded]
    passed = [
        row for row in successful
        if row.quality_passed and row.output_digest == contract.expected_output_digest
    ]
    reliability = len(successful) / len(rows)
    quality = len(passed) / len(successful) if successful else 0.0
    latency_source = [row.latency_seconds for row in successful] or [row.latency_seconds for row in rows]
    latency_p95 = _p95(latency_source)
    transcript = {
        "contract": asdict(contract),
        "observations": [asdict(row) for row in sorted(rows, key=lambda x: x.run_id)],
        "max_parallelism_observed": max_parallelism_observed,
        "rate_limit_per_minute_observed": rate_limit_per_minute_observed,
    }
    measured: dict[str, Any] = {
        "currently_available": bool(successful),
        "programmatic_access": bool(successful),
        "latency_seconds": round(latency_p95, 6),
        "reliability_probability": round(reliability, 6),
        "quality_probability": round(quality, 6),
        "max_parallelism": max_parallelism_observed,
    }
    if rate_limit_per_minute_observed is not None:
        measured["rate_limit_per_minute"] = float(rate_limit_per_minute_observed)

    return ProbeSummary(
        backend_id=contract.backend_id,
        benchmark_id=contract.benchmark_id,
        observation_count=len(rows),
        successful_runs=len(successful),
        quality_passed_runs=len(passed),
        latency_p95_seconds=round(latency_p95, 6),
        reliability_probability=round(reliability, 6),
        quality_probability=round(quality, 6),
        max_parallelism_observed=max_parallelism_observed,
        rate_limit_per_minute_observed=rate_limit_per_minute_observed,
        transcript_digest=_canonical_hash(transcript),
        measured_parameters=measured,
    )
