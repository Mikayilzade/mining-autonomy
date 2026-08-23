"""I158 fail-closed evidence gate for the existing local_model router branch.

This module classifies only caller-supplied local observations. It never downloads a
model, starts a service, uses credentials/network, or invents GPU/model/energy facts.
A production-capable local_model route requires an identified programmatic model plus
measured quality/capacity and measured energy with explicit tariff provenance.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Optional

@dataclass(frozen=True)
class LocalModelObservation:
    model_interface: Optional[str] = None
    model_identity: Optional[str] = None
    gpu_interface: Optional[str] = None
    programmatic_access_verified: bool = False
    quality_acceptance_probability: Optional[float] = None
    latency_seconds: Optional[float] = None
    reliability_probability: Optional[float] = None
    max_parallelism: Optional[int] = None
    energy_kwh_per_task: Optional[float] = None
    tariff_usd_per_kwh: Optional[float] = None
    tariff_source_ref: Optional[str] = None
    downloaded_or_installed_for_probe: bool = False
    credentials_used: bool = False
    network_used: bool = False
    spend_performed: bool = False


def evaluate(obs: LocalModelObservation) -> dict:
    forbidden = any((obs.downloaded_or_installed_for_probe, obs.credentials_used, obs.network_used, obs.spend_performed))
    errors=[]
    if forbidden:
        errors.append("probe_not_no_spend_local_only")
    if bool(obs.model_interface) != bool(obs.model_identity):
        errors.append("model_interface_identity_must_be_bound_together")
    for name, value in (("quality", obs.quality_acceptance_probability), ("reliability", obs.reliability_probability)):
        if value is not None and not 0 <= value <= 1:
            errors.append(f"{name}_probability_out_of_range")
    if obs.latency_seconds is not None and obs.latency_seconds < 0:
        errors.append("negative_latency")
    if obs.max_parallelism is not None and obs.max_parallelism < 1:
        errors.append("invalid_parallelism")
    energy_pair = obs.energy_kwh_per_task is not None and obs.tariff_usd_per_kwh is not None and bool(obs.tariff_source_ref)
    if any(x is not None for x in (obs.energy_kwh_per_task, obs.tariff_usd_per_kwh)) and not energy_pair:
        errors.append("energy_requires_explicit_tariff_provenance")

    interface_ready = bool(obs.model_interface and obs.model_identity and obs.programmatic_access_verified)
    quality_capacity_ready = all(x is not None for x in (
        obs.quality_acceptance_probability, obs.latency_seconds,
        obs.reliability_probability, obs.max_parallelism,
    ))
    production_evidence_ready = interface_ready and quality_capacity_ready and energy_pair and not errors
    if production_evidence_ready:
        state="LOCAL_MODEL_EVIDENCE_COMPLETE"
    elif not obs.model_interface and not obs.model_identity and not obs.gpu_interface and not errors:
        state="NO_LOCAL_MODEL_INTERFACE_OBSERVED"
    else:
        state="PASS_BLOCKED"
    return {
        "schema":"mining-autonomy/i158-local-model-evidence-gate/v1",
        "run":"I158",
        "state":state,
        "observation":asdict(obs),
        "interface_ready":interface_ready,
        "quality_capacity_ready":quality_capacity_ready,
        "energy_tariff_ready":energy_pair,
        "production_evidence_ready":production_evidence_ready,
        "execution_enabled":False,
        "network_enabled":False,
        "credentials_used":False,
        "spend_or_value_movement":False,
        "errors":errors,
    }
