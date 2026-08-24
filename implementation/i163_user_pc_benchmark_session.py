#!/usr/bin/env python3
"""I163 portable deterministic benchmark/session wrapper for I162.

Runs only the existing fixed local Python benchmark. No network, credentials,
downloads, CI dispatch, paid infrastructure, task acceptance, spend or value
movement. The wrapper measures benchmark quality, latency, reliability and a
safe parallelism level actually exercised during this session. It never treats
CPU count as measured parallelism and never invents availability, energy,
electricity tariff or opportunity cost.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from hashlib import sha256
import argparse
import json
import os
import statistics
from time import perf_counter
from typing import Any

import i162_user_pc_measurement_procedure as i162
from i164_fixed_benchmark_core import (
    BENCHMARK_ID,
    EXPECTED_OUTPUT,
    EXPECTED_OUTPUT_DIGEST,
    benchmark_transform,
)

SCHEMA = "mining-autonomy/i163-user-pc-benchmark-session/v1"
RUNNER_ID = "i163-fixed-json-transform-session-v1"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _run_work_unit(inner_iterations: int) -> dict[str, Any]:
    started = perf_counter()
    success = True
    digest_match = True
    try:
        for _ in range(inner_iterations):
            output = benchmark_transform()
            if output != EXPECTED_OUTPUT or _digest(output) != EXPECTED_OUTPUT_DIGEST:
                digest_match = False
                success = False
                break
    except Exception:
        success = False
        digest_match = False
    return {
        "success": success,
        "quality_passed": digest_match,
        "latency_seconds": max(0.0, perf_counter() - started),
    }


def _candidate_parallelism(logical_cpu_count: int | None, cap: int) -> tuple[int, ...]:
    upper = max(1, min(int(logical_cpu_count or 1), cap))
    values = [1]
    value = 2
    while value <= upper:
        values.append(value)
        value *= 2
    if values[-1] != upper:
        values.append(upper)
    return tuple(dict.fromkeys(values))


def run_session(
    *, repetitions: int = 20,
    inner_iterations: int = 500,
    parallelism_cap: int = 8,
    confirm_user_owned_pc: bool = False,
) -> dict[str, Any]:
    if repetitions < 10:
        raise ValueError("repetitions_must_be_at_least_10")
    if inner_iterations < 1:
        raise ValueError("inner_iterations_must_be_positive")
    if parallelism_cap < 1:
        raise ValueError("parallelism_cap_must_be_positive")

    identity = i162.collect_local_identity()
    candidates = _candidate_parallelism(identity.get("logical_cpu_count"), parallelism_cap)
    levels: list[dict[str, Any]] = []
    all_observations: list[dict[str, Any]] = []
    safe_parallelism = 0

    for parallelism in candidates:
        observations: list[dict[str, Any]] = []
        started = perf_counter()
        with ThreadPoolExecutor(max_workers=parallelism) as executor:
            futures = [executor.submit(_run_work_unit, inner_iterations) for _ in range(repetitions)]
            for future in as_completed(futures):
                observations.append(future.result())
        wall_seconds = max(0.0, perf_counter() - started)
        successful = sum(1 for row in observations if row["success"])
        quality_passes = sum(1 for row in observations if row["quality_passed"])
        reliability = successful / len(observations)
        quality_probability = quality_passes / len(observations)
        latencies = [float(row["latency_seconds"]) for row in observations]
        level = {
            "parallelism": parallelism,
            "attempts": len(observations),
            "successful": successful,
            "quality_passes": quality_passes,
            "reliability_probability": reliability,
            "quality_acceptance_probability": quality_probability,
            "median_latency_seconds": statistics.median(latencies),
            "p95_latency_seconds": sorted(latencies)[max(0, min(len(latencies) - 1, int(len(latencies) * 0.95) - 1))],
            "wall_seconds": wall_seconds,
            "tasks_per_second": (len(observations) / wall_seconds) if wall_seconds > 0 else None,
        }
        levels.append(level)
        all_observations.extend({"parallelism": parallelism, **row} for row in observations)
        if reliability == 1.0 and quality_probability == 1.0:
            safe_parallelism = parallelism
        else:
            break

    if safe_parallelism < 1:
        state = "BENCHMARK_FAILED"
    else:
        state = "BENCHMARK_SESSION_COMPLETE"

    serial = next((row for row in levels if row["parallelism"] == 1), levels[0])
    safe = next((row for row in levels if row["parallelism"] == safe_parallelism), serial)
    benchmark_source_ref = f"repo:{RUNNER_ID}:{_digest({'benchmark_id': BENCHMARK_ID, 'expected': EXPECTED_OUTPUT_DIGEST})}"
    environment_body = {
        "runner_id": RUNNER_ID,
        "benchmark_id": BENCHMARK_ID,
        "identity": identity,
        "repetitions": repetitions,
        "inner_iterations": inner_iterations,
        "parallelism_cap": parallelism_cap,
        "levels": levels,
    }
    measurement_environment_ref = f"i163-session:{_digest(environment_body)}"

    measurements = i162.ExplicitMeasurements(
        benchmark_id=BENCHMARK_ID,
        benchmark_source_ref=benchmark_source_ref,
        quality_acceptance_probability=float(safe["quality_acceptance_probability"]),
        latency_seconds=float(serial["median_latency_seconds"]),
        reliability_probability=float(safe["reliability_probability"]),
        max_parallelism=safe_parallelism,
    )
    i162_projection = i162.build_packet(
        measurements,
        confirm_user_owned_pc=confirm_user_owned_pc,
        measurement_environment_ref=measurement_environment_ref,
        identity=identity,
    )

    return {
        "schema": SCHEMA,
        "run": "I163",
        "state": state,
        "runner_id": RUNNER_ID,
        "benchmark_id": BENCHMARK_ID,
        "expected_output_digest": EXPECTED_OUTPUT_DIGEST,
        "identity": identity,
        "measurement_environment_ref": measurement_environment_ref,
        "benchmark_source_ref": benchmark_source_ref,
        "candidate_parallelism": list(candidates),
        "measured_safe_parallelism": safe_parallelism,
        "levels": levels,
        "observation_count": len(all_observations),
        "i162_explicit_measurements": asdict(measurements),
        "i162_projection": i162_projection,
        "ownership_confirmation_supplied": confirm_user_owned_pc,
        "external_facts_intentionally_not_measured": [
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
        ],
        "network_enabled": False,
        "credentials_used": False,
        "downloads_or_installs_performed": False,
        "ci_dispatched": False,
        "paid_infrastructure_created": False,
        "task_acceptance_or_submission": False,
        "spend_or_value_movement": False,
        "production_route_created": False,
        "next_gate": (
            "Run I163 on the user-owned PC with explicit ownership confirmation. Feed its benchmark/session "
            "reference into I162, then separately add genuinely observed availability, trustworthy joule-counter "
            "readings, explicit electricity tariff and explicit opportunity-cost provenance. Missing external "
            "facts remain blockers and must not be estimated by this runner."
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--inner-iterations", type=int, default=500)
    parser.add_argument("--parallelism-cap", type=int, default=8)
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = run_session(
        repetitions=args.repetitions,
        inner_iterations=args.inner_iterations,
        parallelism_cap=args.parallelism_cap,
        confirm_user_owned_pc=args.confirm_user_owned_pc,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text, end="")
    return 0 if result["state"] == "BENCHMARK_SESSION_COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
