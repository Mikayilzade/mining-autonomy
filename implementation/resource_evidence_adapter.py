"""Deterministic I053 -> I050 ResourceEvidence adapter (I054).

Converts already-collected offline probe summaries and explicit accounting/
energy inputs into hash-bound I050 evidence. Missing values stay missing.
No probe execution, hardware inspection, network, credentials, spend or value
movement occurs here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional

from resource_calibration_acquisition import CalibrationAcquisitionPlan, ProbeSummary
from resource_profile_evidence import CRITICAL_PARAMETERS, ResourceEvidence, make_evidence

_OBSERVED_AT_KEY = "_observed_at_utc"


@dataclass(frozen=True)
class ExplicitDeclaration:
    parameter: str
    value: Any
    observed_at: str
    max_age_seconds: int
    source_ref: str
    notes: str = ""


@dataclass(frozen=True)
class EnergyMeasurement:
    energy_kwh_per_task: float
    tariff_usd_per_kwh: float
    observed_at: str
    max_age_seconds: int
    source_ref: str
    source_content_digest: str
    notes: str = ""


@dataclass(frozen=True)
class EvidenceBuildResult:
    backend_id: str
    reference_backend_hash: str
    records: tuple[ResourceEvidence, ...]
    emitted_parameters: tuple[str, ...]
    missing_parameters: tuple[str, ...]
    source_kinds: tuple[str, ...]
    complete_for_attestation: bool
    planning_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _requirements_by_parameter(plan: CalibrationAcquisitionPlan) -> dict[str, Any]:
    requirements = {req.parameter: req for req in plan.requirements}
    if set(requirements) != set(CRITICAL_PARAMETERS):
        raise ValueError("plan_does_not_cover_i050_critical_parameters")
    return requirements


def _same_numeric(a: Any, b: Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return False
    return abs(float(a) - float(b)) <= 1e-9


def _validate_probe_summary(plan: CalibrationAcquisitionPlan, summary: ProbeSummary) -> str:
    if summary.backend_id != plan.backend_id:
        raise ValueError("probe_backend_mismatch")
    if summary.benchmark_id != plan.probe_contract.benchmark_id:
        raise ValueError("probe_benchmark_mismatch")
    if not summary.transcript_digest or len(summary.transcript_digest) < 16:
        raise ValueError("probe_transcript_digest_required")
    if summary.network_enabled or summary.credentials_used or summary.spend_performed or summary.value_movement_enabled:
        raise ValueError("probe_summary_not_inert")
    if not isinstance(summary.measured_parameters, Mapping):
        raise ValueError("probe_measured_parameters_must_be_mapping")
    observed_at = summary.measured_parameters.get(_OBSERVED_AT_KEY)
    if not isinstance(observed_at, str) or not observed_at.strip():
        raise ValueError("probe_observed_at_utc_required")

    expected = {
        "currently_available": summary.successful_runs > 0,
        "programmatic_access": summary.successful_runs > 0,
        "latency_seconds": summary.latency_p95_seconds,
        "reliability_probability": summary.reliability_probability,
        "quality_probability": summary.quality_probability,
        "max_parallelism": summary.max_parallelism_observed,
    }
    if summary.rate_limit_per_minute_observed is not None:
        expected["rate_limit_per_minute"] = summary.rate_limit_per_minute_observed
    for parameter, value in expected.items():
        if parameter not in summary.measured_parameters:
            raise ValueError(f"probe_summary_missing_derived_parameter:{parameter}")
        observed = summary.measured_parameters[parameter]
        if isinstance(value, bool):
            consistent = observed is value
        elif parameter == "max_parallelism":
            consistent = observed == value
        else:
            consistent = _same_numeric(observed, value)
        if not consistent:
            raise ValueError(f"probe_summary_internal_mismatch:{parameter}")
    if summary.rate_limit_per_minute_observed is None and "rate_limit_per_minute" in summary.measured_parameters:
        raise ValueError("probe_summary_internal_mismatch:rate_limit_per_minute")
    return observed_at


def _evidence_id(prefix: str, parameter: str, ordinal: int = 0) -> str:
    return f"i054-{prefix}-{parameter}" + (f"-{ordinal}" if ordinal else "")


def build_resource_evidence(
    plan: CalibrationAcquisitionPlan,
    *,
    probe_summary: Optional[ProbeSummary] = None,
    declarations: Iterable[ExplicitDeclaration] = (),
    energy_measurement: Optional[EnergyMeasurement] = None,
) -> EvidenceBuildResult:
    """Emit evidence only for facts explicitly present in the inputs."""
    requirements = _requirements_by_parameter(plan)
    emitted: dict[str, ResourceEvidence] = {}

    if probe_summary is not None:
        observed_at = _validate_probe_summary(plan, probe_summary)
        for parameter, value in probe_summary.measured_parameters.items():
            if parameter == _OBSERVED_AT_KEY:
                continue
            if parameter not in requirements:
                raise ValueError(f"probe_emits_unknown_parameter:{parameter}")
            requirement = requirements[parameter]
            if "system_probe" not in requirement.accepted_source_kinds:
                raise ValueError(f"system_probe_not_allowed_for:{parameter}")
            emitted[parameter] = make_evidence(
                evidence_id=_evidence_id("probe", parameter),
                backend_id=plan.backend_id,
                parameter=parameter,
                value=value,
                source_kind="system_probe",
                source_ref=f"probe:{probe_summary.benchmark_id}:{probe_summary.transcript_digest}",
                observed_at=observed_at,
                max_age_seconds=requirement.max_age_seconds,
                reference_hash=plan.reference_backend_hash,
                source_content_digest=probe_summary.transcript_digest,
                notes="Derived only from the I053 inert probe transcript summary.",
            )

    for index, declaration in enumerate(declarations, start=1):
        parameter = declaration.parameter
        if parameter not in requirements:
            raise ValueError(f"declaration_unknown_parameter:{parameter}")
        requirement = requirements[parameter]
        if "user_declared" not in requirement.accepted_source_kinds:
            raise ValueError(f"user_declared_not_allowed_for:{parameter}")
        if parameter in emitted:
            raise ValueError(f"duplicate_parameter_input:{parameter}")
        if not declaration.source_ref.strip():
            raise ValueError("declaration_source_ref_required")
        if declaration.max_age_seconds <= 0:
            raise ValueError("declaration_max_age_must_be_positive")
        emitted[parameter] = make_evidence(
            evidence_id=_evidence_id("declared", parameter, index),
            backend_id=plan.backend_id,
            parameter=parameter,
            value=declaration.value,
            source_kind="user_declared",
            source_ref=declaration.source_ref,
            observed_at=declaration.observed_at,
            max_age_seconds=min(declaration.max_age_seconds, requirement.max_age_seconds),
            reference_hash=plan.reference_backend_hash,
            notes=declaration.notes,
        )

    if energy_measurement is not None:
        parameter = "electricity_per_task_usd"
        requirement = requirements[parameter]
        if parameter in emitted:
            raise ValueError(f"duplicate_parameter_input:{parameter}")
        if energy_measurement.energy_kwh_per_task < 0 or energy_measurement.tariff_usd_per_kwh < 0:
            raise ValueError("energy_inputs_must_be_nonnegative")
        if not energy_measurement.source_ref.strip():
            raise ValueError("energy_source_ref_required")
        if not energy_measurement.source_content_digest or len(energy_measurement.source_content_digest) < 16:
            raise ValueError("energy_source_digest_required")
        if energy_measurement.max_age_seconds <= 0:
            raise ValueError("energy_max_age_must_be_positive")
        value = round(float(energy_measurement.energy_kwh_per_task) * float(energy_measurement.tariff_usd_per_kwh), 12)
        emitted[parameter] = make_evidence(
            evidence_id=_evidence_id("energy", parameter),
            backend_id=plan.backend_id,
            parameter=parameter,
            value=value,
            source_kind="measured_local",
            source_ref=energy_measurement.source_ref,
            observed_at=energy_measurement.observed_at,
            max_age_seconds=min(energy_measurement.max_age_seconds, requirement.max_age_seconds),
            reference_hash=plan.reference_backend_hash,
            source_content_digest=energy_measurement.source_content_digest,
            notes=(
                f"energy_kwh_per_task={energy_measurement.energy_kwh_per_task}; "
                f"tariff_usd_per_kwh={energy_measurement.tariff_usd_per_kwh}. " + energy_measurement.notes
            ).strip(),
        )

    records = tuple(emitted[p] for p in CRITICAL_PARAMETERS if p in emitted)
    emitted_parameters = tuple(record.parameter for record in records)
    missing_parameters = tuple(p for p in CRITICAL_PARAMETERS if p not in emitted)
    return EvidenceBuildResult(
        backend_id=plan.backend_id,
        reference_backend_hash=plan.reference_backend_hash,
        records=records,
        emitted_parameters=emitted_parameters,
        missing_parameters=missing_parameters,
        source_kinds=tuple(sorted({record.source_kind for record in records})),
        complete_for_attestation=not missing_parameters,
    )


def normalize_probe_summary_for_evidence(summary: ProbeSummary, *, observed_at_utc: str) -> ProbeSummary:
    """Attach collector-supplied measurement time without inventing it."""
    measured = dict(summary.measured_parameters)
    if _OBSERVED_AT_KEY in measured:
        raise ValueError("probe_observed_at_already_present")
    measured[_OBSERVED_AT_KEY] = observed_at_utc
    return ProbeSummary(
        backend_id=summary.backend_id,
        benchmark_id=summary.benchmark_id,
        observation_count=summary.observation_count,
        successful_runs=summary.successful_runs,
        quality_passed_runs=summary.quality_passed_runs,
        latency_p95_seconds=summary.latency_p95_seconds,
        reliability_probability=summary.reliability_probability,
        quality_probability=summary.quality_probability,
        max_parallelism_observed=summary.max_parallelism_observed,
        rate_limit_per_minute_observed=summary.rate_limit_per_minute_observed,
        transcript_digest=summary.transcript_digest,
        measured_parameters=measured,
        network_enabled=summary.network_enabled,
        credentials_used=summary.credentials_used,
        spend_performed=summary.spend_performed,
        value_movement_enabled=summary.value_movement_enabled,
    )
