#!/usr/bin/env python3
"""I162 portable, fail-closed user-PC measurement procedure.

This module prepares and validates a local-only measurement packet for the existing
I159 owned_pc Resource / Execution Router branch. It does not claim that the current
runtime is the user's computer and does not perform network access, downloads,
credential use, CI dispatch, paid infrastructure, task acceptance, spend, or value
movement.

Automatic collection is intentionally limited to identity/runtime facts available to
Python. Availability, energy, electricity tariff, and opportunity cost remain explicit
caller-supplied measurements with provenance. Energy can be derived only from explicit
before/after joule counter readings; no counter or tariff is inferred.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import argparse
import json
import os
import platform
import sys
from typing import Any, Mapping, Optional

import i159_owned_pc_evidence_packet as i159

SCHEMA = "mining-autonomy/i162-user-pc-measurement-procedure/v1"
JOULES_PER_KWH = 3_600_000.0


@dataclass(frozen=True)
class ExplicitMeasurements:
    benchmark_id: Optional[str] = None
    benchmark_source_ref: Optional[str] = None
    quality_acceptance_probability: Optional[float] = None
    latency_seconds: Optional[float] = None
    reliability_probability: Optional[float] = None
    max_parallelism: Optional[int] = None
    measured_available_hours_per_day: Optional[float] = None
    availability_source_ref: Optional[str] = None
    energy_before_joules: Optional[float] = None
    energy_after_joules: Optional[float] = None
    energy_task_count: Optional[int] = None
    energy_source_ref: Optional[str] = None
    tariff_usd_per_kwh: Optional[float] = None
    tariff_source_ref: Optional[str] = None
    opportunity_cost_usd_per_hour: Optional[float] = None
    opportunity_cost_source_ref: Optional[str] = None


def _digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return sha256(text.encode("utf-8")).hexdigest()


def collect_local_identity() -> dict[str, Any]:
    """Collect non-network Python-visible identity only; this is not an ownership claim."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "logical_cpu_count": os.cpu_count(),
        "executable": sys.executable,
    }


def _energy_per_task(measurements: ExplicitMeasurements, errors: list[str]) -> Optional[float]:
    supplied = (
        measurements.energy_before_joules,
        measurements.energy_after_joules,
        measurements.energy_task_count,
    )
    if all(value is None for value in supplied):
        return None
    if any(value is None for value in supplied):
        errors.append("energy_counter_inputs_must_be_supplied_together")
        return None
    before = float(measurements.energy_before_joules)
    after = float(measurements.energy_after_joules)
    count = int(measurements.energy_task_count)
    if before < 0 or after < before:
        errors.append("energy_counter_wrap_reset_or_negative_delta")
        return None
    if count <= 0:
        errors.append("positive_energy_task_count_required")
        return None
    if not measurements.energy_source_ref:
        errors.append("energy_source_ref_required")
        return None
    return (after - before) / JOULES_PER_KWH / count


def build_packet(
    measurements: ExplicitMeasurements,
    *,
    confirm_user_owned_pc: bool = False,
    measurement_environment_ref: Optional[str] = None,
    identity: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    errors: list[str] = []
    identity_map = dict(identity) if identity is not None else collect_local_identity()
    energy_kwh_per_task = _energy_per_task(measurements, errors)

    hardware_identity = _digest({
        "machine": identity_map.get("machine"),
        "processor": identity_map.get("processor"),
        "logical_cpu_count": identity_map.get("logical_cpu_count"),
    })
    os_identity = _digest({
        "system": identity_map.get("system"),
        "release": identity_map.get("release"),
    })
    execution_interface = (
        f"{identity_map.get('python_implementation') or 'Python'} "
        f"{identity_map.get('python_version') or ''}".strip()
    )

    obs = i159.OwnedPcObservation(
        hardware_identity=hardware_identity,
        os_identity=os_identity,
        execution_interface=execution_interface,
        deterministic_programmatic_access_verified=True,
        benchmark_id=measurements.benchmark_id,
        benchmark_source_ref=measurements.benchmark_source_ref,
        quality_acceptance_probability=measurements.quality_acceptance_probability,
        latency_seconds=measurements.latency_seconds,
        reliability_probability=measurements.reliability_probability,
        max_parallelism=measurements.max_parallelism,
        measured_available_hours_per_day=measurements.measured_available_hours_per_day,
        availability_source_ref=measurements.availability_source_ref,
        energy_kwh_per_task=energy_kwh_per_task,
        energy_source_ref=measurements.energy_source_ref if energy_kwh_per_task is not None else None,
        tariff_usd_per_kwh=measurements.tariff_usd_per_kwh,
        tariff_source_ref=measurements.tariff_source_ref,
        opportunity_cost_usd_per_hour=measurements.opportunity_cost_usd_per_hour,
        opportunity_cost_source_ref=measurements.opportunity_cost_source_ref,
        measurement_environment_ref=measurement_environment_ref,
        measurements_from_user_owned_pc=confirm_user_owned_pc,
        network_used=False,
        credentials_used=False,
        downloads_or_installs_for_probe=False,
        spend_performed=False,
    )
    evaluation = i159.evaluate(obs)
    errors.extend(evaluation.get("errors", []))

    required_missing = []
    for ready_key, label in (
        ("identity_ready", "ownership_bound_identity"),
        ("benchmark_ready", "benchmark_quality_latency_reliability_parallelism"),
        ("availability_ready", "measured_availability"),
        ("energy_tariff_ready", "measured_energy_plus_explicit_tariff"),
        ("opportunity_cost_ready", "explicit_opportunity_cost"),
    ):
        if evaluation.get(ready_key) is not True:
            required_missing.append(label)

    state = "USER_PC_PACKET_COMPLETE" if evaluation.get("production_evidence_ready") is True and not errors else "PASS_BLOCKED"
    return {
        "schema": SCHEMA,
        "run": "I162",
        "state": state,
        "local_identity": identity_map,
        "identity_digest": _digest(identity_map),
        "ownership_confirmation_required": True,
        "explicit_measurements": asdict(measurements),
        "derived_energy_kwh_per_task": energy_kwh_per_task,
        "i159_evaluation": evaluation,
        "missing_evidence": required_missing,
        "errors": sorted(set(errors)),
        "network_enabled": False,
        "credentials_used": False,
        "downloads_or_installs_performed": False,
        "ci_dispatched": False,
        "paid_infrastructure_created": False,
        "spend_or_value_movement": False,
        "production_route_created": False,
        "next_gate": (
            "Run this file on the user-owned PC and supply only genuinely measured benchmark, availability, "
            "energy-counter, tariff and opportunity-cost values with provenance. A complete I159 packet still "
            "requires conservative economics/routing and does not authorize market observation or task execution."
        ),
    }


def procedure_manifest() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "run": "I162",
        "state": "LOCAL_USER_PC_EXECUTION_REQUIRED",
        "steps": [
            "copy the repository or these measurement files to the user-owned PC without adding paid software",
            "run Python locally with network disabled/not required and record the emitted identity digest",
            "run the existing deterministic benchmark enough times to measure quality, latency, reliability and safe parallelism",
            "record realistic available hours/day from an explicit observation window; do not infer 24/7 availability",
            "obtain before/after joule readings from a trustworthy local meter/counter around the benchmark workload; if unavailable leave energy blocked",
            "supply an explicit electricity tariff and source reference; do not infer or scrape it inside this harness",
            "supply an explicit opportunity-cost estimate and provenance for PC occupation/maintenance",
            "rerun I162 with ownership confirmation and the measured values; accept completion only when I159 returns production_evidence_ready=true",
        ],
        "forbidden_substitutions": [
            "synthetic energy or tariff",
            "os.cpu_count as measured max_parallelism",
            "single successful run as reliability=1",
            "machine reachability as 24h/day availability",
            "subscription or owned-hardware sunk cost as zero opportunity cost",
        ],
        "external_actions_performed": False,
        "network_enabled": False,
        "credentials_used": False,
        "downloads_or_installs_performed": False,
        "spend_or_value_movement": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", action="store_true", help="emit the portable procedure manifest only")
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--measurement-environment-ref")
    parser.add_argument("--input-json", help="JSON object matching ExplicitMeasurements")
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    if args.template or not args.input_json:
        result = procedure_manifest()
    else:
        raw = json.loads(open(args.input_json, "r", encoding="utf-8").read())
        result = build_packet(
            ExplicitMeasurements(**raw),
            confirm_user_owned_pc=args.confirm_user_owned_pc,
            measurement_environment_ref=args.measurement_environment_ref,
        )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text, end="")
    return 0 if result.get("state") in {"USER_PC_PACKET_COMPLETE", "LOCAL_USER_PC_EXECUTION_REQUIRED", "PASS_BLOCKED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
