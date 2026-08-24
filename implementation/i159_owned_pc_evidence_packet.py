"""I159 portable fail-closed evidence gate for the existing owned_pc router branch.

This module validates caller-supplied measurements from a user-owned computer. It
never probes or claims the user's hardware by itself. A production-capable owned_pc
route requires bound hardware/interface identity, measured benchmark quality,
latency/reliability/capacity/parallelism, availability, measured per-task energy,
explicit tariff provenance, and explicit opportunity-cost provenance.

No network, credentials, downloads, paid infrastructure, spend, task acceptance,
or value movement is performed here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

SCHEMA = "mining-autonomy/i159-owned-pc-evidence-packet/v1"


@dataclass(frozen=True)
class OwnedPcObservation:
    hardware_identity: Optional[str] = None
    os_identity: Optional[str] = None
    execution_interface: Optional[str] = None
    deterministic_programmatic_access_verified: bool = False
    benchmark_id: Optional[str] = None
    benchmark_source_ref: Optional[str] = None
    quality_acceptance_probability: Optional[float] = None
    latency_seconds: Optional[float] = None
    reliability_probability: Optional[float] = None
    max_parallelism: Optional[int] = None
    measured_available_hours_per_day: Optional[float] = None
    availability_source_ref: Optional[str] = None
    energy_kwh_per_task: Optional[float] = None
    energy_source_ref: Optional[str] = None
    tariff_usd_per_kwh: Optional[float] = None
    tariff_source_ref: Optional[str] = None
    opportunity_cost_usd_per_hour: Optional[float] = None
    opportunity_cost_source_ref: Optional[str] = None
    measurement_environment_ref: Optional[str] = None
    measurements_from_user_owned_pc: bool = False
    network_used: bool = False
    credentials_used: bool = False
    downloads_or_installs_for_probe: bool = False
    spend_performed: bool = False


def _probability_errors(name: str, value: Optional[float], errors: list[str]) -> None:
    if value is not None and not 0 <= value <= 1:
        errors.append(f"{name}_probability_out_of_range")


def evaluate(obs: OwnedPcObservation) -> dict:
    errors: list[str] = []
    if any((obs.network_used, obs.credentials_used, obs.downloads_or_installs_for_probe, obs.spend_performed)):
        errors.append("measurement_packet_not_local_no_spend")

    _probability_errors("quality", obs.quality_acceptance_probability, errors)
    _probability_errors("reliability", obs.reliability_probability, errors)

    if obs.latency_seconds is not None and obs.latency_seconds < 0:
        errors.append("negative_latency")
    if obs.max_parallelism is not None and obs.max_parallelism < 1:
        errors.append("invalid_parallelism")
    if obs.measured_available_hours_per_day is not None and not 0 <= obs.measured_available_hours_per_day <= 24:
        errors.append("availability_hours_out_of_range")
    if obs.energy_kwh_per_task is not None and obs.energy_kwh_per_task < 0:
        errors.append("negative_energy")
    if obs.tariff_usd_per_kwh is not None and obs.tariff_usd_per_kwh < 0:
        errors.append("negative_tariff")
    if obs.opportunity_cost_usd_per_hour is not None and obs.opportunity_cost_usd_per_hour < 0:
        errors.append("negative_opportunity_cost")

    identity_ready = bool(
        obs.hardware_identity
        and obs.os_identity
        and obs.execution_interface
        and obs.deterministic_programmatic_access_verified
        and obs.measurements_from_user_owned_pc
        and obs.measurement_environment_ref
    )
    benchmark_ready = bool(
        obs.benchmark_id
        and obs.benchmark_source_ref
        and obs.quality_acceptance_probability is not None
        and obs.latency_seconds is not None
        and obs.reliability_probability is not None
        and obs.max_parallelism is not None
    )
    availability_ready = bool(
        obs.measured_available_hours_per_day is not None
        and obs.availability_source_ref
    )
    energy_tariff_ready = bool(
        obs.energy_kwh_per_task is not None
        and obs.energy_source_ref
        and obs.tariff_usd_per_kwh is not None
        and obs.tariff_source_ref
    )
    opportunity_cost_ready = bool(
        obs.opportunity_cost_usd_per_hour is not None
        and obs.opportunity_cost_source_ref
    )

    supplied_measurement_fields = any(
        x is not None for x in (
            obs.quality_acceptance_probability,
            obs.latency_seconds,
            obs.reliability_probability,
            obs.max_parallelism,
            obs.measured_available_hours_per_day,
            obs.energy_kwh_per_task,
            obs.tariff_usd_per_kwh,
            obs.opportunity_cost_usd_per_hour,
        )
    )
    if supplied_measurement_fields and not obs.measurements_from_user_owned_pc:
        errors.append("measurements_not_bound_to_user_owned_pc")

    production_evidence_ready = all((
        identity_ready,
        benchmark_ready,
        availability_ready,
        energy_tariff_ready,
        opportunity_cost_ready,
    )) and not errors

    if production_evidence_ready:
        state = "OWNED_PC_EVIDENCE_COMPLETE"
    elif not supplied_measurement_fields and not obs.measurements_from_user_owned_pc and not errors:
        state = "LOCAL_MATERIALIZATION_REQUIRED"
    else:
        state = "PASS_BLOCKED"

    return {
        "schema": SCHEMA,
        "run": "I159",
        "state": state,
        "observation": asdict(obs),
        "identity_ready": identity_ready,
        "benchmark_ready": benchmark_ready,
        "availability_ready": availability_ready,
        "energy_tariff_ready": energy_tariff_ready,
        "opportunity_cost_ready": opportunity_cost_ready,
        "production_evidence_ready": production_evidence_ready,
        "measurement_boundary": (
            "Repository automation cannot claim user-owned-PC hardware, availability, energy, tariff, "
            "or opportunity cost without measurements produced on that machine and bound to explicit provenance."
        ),
        "execution_enabled": False,
        "network_enabled": False,
        "credentials_used": False,
        "spend_or_value_movement": False,
        "errors": errors,
    }
