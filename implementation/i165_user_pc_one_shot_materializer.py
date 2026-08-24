#!/usr/bin/env python3
"""I165 one-shot local materializer for the existing owned_pc evidence branch.

Runs I163 locally, then merges its measured benchmark/session fields with optional
caller-supplied external facts required by I162. Benchmark fields cannot be overridden
by the external JSON. Availability, energy-counter readings, electricity tariff and
opportunity cost remain explicit provenance-bound inputs and are never inferred.

No network, credentials, downloads, CI dispatch, paid infrastructure, task acceptance,
spend, settlement, payment or value movement is performed by this module.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Mapping

import i162_user_pc_measurement_procedure as i162
import i163_user_pc_benchmark_session as i163

SCHEMA = "mining-autonomy/i165-user-pc-one-shot-materializer/v1"

EXTERNAL_FIELDS = (
    "measured_available_hours_per_day",
    "availability_source_ref",
    "energy_before_joules",
    "energy_after_joules",
    "energy_task_count",
    "energy_source_ref",
    "tariff_usd_per_kwh",
    "tariff_source_ref",
    "opportunity_cost_usd_per_hour",
    "opportunity_cost_source_ref",
)

BENCHMARK_FIELDS = (
    "benchmark_id",
    "benchmark_source_ref",
    "quality_acceptance_probability",
    "latency_seconds",
    "reliability_probability",
    "max_parallelism",
)


@dataclass(frozen=True)
class MaterializationResult:
    state: str
    benchmark_session_state: str
    ownership_confirmation_supplied: bool
    external_fields_supplied: tuple[str, ...]
    i162_packet: dict[str, Any]
    network_enabled: bool = False
    credentials_used: bool = False
    downloads_or_installs_performed: bool = False
    ci_dispatched: bool = False
    paid_infrastructure_created: bool = False
    task_acceptance_or_submission: bool = False
    spend_or_value_movement: bool = False
    production_route_created: bool = False


def _validate_external(raw: Mapping[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(raw) - set(EXTERNAL_FIELDS))
    if unknown:
        raise ValueError("unsupported_or_benchmark_override_fields:" + ",".join(unknown))
    return {name: raw[name] for name in EXTERNAL_FIELDS if name in raw}


def materialize(
    *,
    external_facts: Mapping[str, Any] | None = None,
    confirm_user_owned_pc: bool = False,
    repetitions: int = 20,
    inner_iterations: int = 500,
    parallelism_cap: int = 8,
) -> MaterializationResult:
    external = _validate_external(external_facts or {})
    session = i163.run_session(
        repetitions=repetitions,
        inner_iterations=inner_iterations,
        parallelism_cap=parallelism_cap,
        confirm_user_owned_pc=confirm_user_owned_pc,
    )
    if session.get("state") != "BENCHMARK_SESSION_COMPLETE":
        raise RuntimeError("i163_benchmark_session_not_complete")

    benchmark = session.get("i162_explicit_measurements")
    if not isinstance(benchmark, Mapping):
        raise RuntimeError("i163_measurement_projection_missing")
    merged = {name: benchmark.get(name) for name in BENCHMARK_FIELDS}
    merged.update(external)

    packet = i162.build_packet(
        i162.ExplicitMeasurements(**merged),
        confirm_user_owned_pc=confirm_user_owned_pc,
        measurement_environment_ref=str(session.get("measurement_environment_ref") or ""),
        identity=session.get("identity") if isinstance(session.get("identity"), Mapping) else None,
    )
    state = "USER_PC_MATERIALIZED" if packet.get("state") == "USER_PC_PACKET_COMPLETE" else "PASS_BLOCKED"
    return MaterializationResult(
        state=state,
        benchmark_session_state=str(session.get("state")),
        ownership_confirmation_supplied=confirm_user_owned_pc,
        external_fields_supplied=tuple(sorted(external)),
        i162_packet=packet,
    )


def payload(result: MaterializationResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I165",
        "external_fields_allowed": list(EXTERNAL_FIELDS),
        "benchmark_fields_source": "I163 only; external override rejected",
        "next_gate": (
            "Run I165 on the user-owned PC with --confirm-user-owned-pc. Supply only genuinely observed "
            "availability, trustworthy before/after joule-counter readings, explicit applicable electricity "
            "tariff and explicit opportunity-cost provenance. USER_PC_MATERIALIZED is evidence assembly only; "
            "conservative economics/routing remains separate and no market/task action is authorized here."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-json", help="JSON object containing only I165 EXTERNAL_FIELDS")
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--inner-iterations", type=int, default=500)
    parser.add_argument("--parallelism-cap", type=int, default=8)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    raw: Mapping[str, Any] = {}
    if args.external_json:
        value = json.loads(Path(args.external_json).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("external_json_must_be_object")
        raw = value

    result = materialize(
        external_facts=raw,
        confirm_user_owned_pc=args.confirm_user_owned_pc,
        repetitions=args.repetitions,
        inner_iterations=args.inner_iterations,
        parallelism_cap=args.parallelism_cap,
    )
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
