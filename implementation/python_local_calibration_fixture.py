"""I056 opt-in no-network calibration fixture/runner for python_local.

Runs only a fixed deterministic local JSON transform. Disabled unless explicitly
opted in. Never opens network connections, uses credentials, spends money, or
infers accounting/electricity/quota facts. Portable transcripts replay through
I053 and can feed the existing I055 calibration packet.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from time import perf_counter
from typing import Any, Iterable, Mapping, Optional

from calibration_routing_packet import CalibrationRoutingPacket, build_calibration_routing_packet
from evaluator import CapabilityProfile, CostProfile
from resource_calibration_acquisition import (
    CalibrationAcquisitionPlan, ProbeObservation, ProbeSummary,
    build_local_no_spend_plan, evaluate_probe_transcript,
)
from resource_evidence_adapter import EnergyMeasurement, ExplicitDeclaration
from resource_router import ExecutionBackend

BENCHMARK_ID = "python-local-fixed-json-transform-v1"
FIXTURE_INPUT = {
    "records": [
        {"id": "gamma", "value": 5},
        {"id": "alpha", "value": 2},
        {"id": "beta", "value": 3},
    ],
    "schema_version": 1,
}

def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _hash(value: Any) -> str:
    payload = value if isinstance(value, str) else _canonical_json(value)
    return sha256(payload.encode("utf-8")).hexdigest()

def benchmark_transform(payload: Mapping[str, Any] = FIXTURE_INPUT) -> dict[str, Any]:
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported_fixture_schema")
    rows = payload.get("records")
    if not isinstance(rows, list) or not rows:
        raise ValueError("fixture_records_required")
    normalized = []
    seen = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("fixture_row_must_be_mapping")
        key = row.get("id")
        value = row.get("value")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("invalid_or_duplicate_fixture_id")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("fixture_value_must_be_nonnegative_int")
        seen.add(key)
        normalized.append({"id": key, "value": value})
    normalized.sort(key=lambda x: x["id"])
    checksum_input = "|".join(f'{row["id"]}:{row["value"]}' for row in normalized)
    return {
        "count": len(normalized),
        "sum": sum(row["value"] for row in normalized),
        "records": normalized,
        "records_checksum": _hash(checksum_input),
        "schema_version": 1,
    }

EXPECTED_OUTPUT = benchmark_transform()
EXPECTED_OUTPUT_DIGEST = _hash(EXPECTED_OUTPUT)

@dataclass(frozen=True)
class PortableProbeTranscript:
    format_version: int
    backend_id: str
    benchmark_id: str
    reference_backend_hash: str
    expected_output_digest: str
    observations: tuple[ProbeObservation, ...]
    max_parallelism_observed: int
    rate_limit_per_minute_observed: Optional[float]
    i053_transcript_digest: str
    runner_kind: str = "local_python_fixed_fixture"
    network_enabled: bool = False
    credentials_used: bool = False
    spend_performed: bool = False
    value_movement_enabled: bool = False

@dataclass(frozen=True)
class TranscriptReplay:
    plan: CalibrationAcquisitionPlan
    transcript: PortableProbeTranscript
    probe_summary: ProbeSummary
    portable_transcript_digest: str
    verified: bool
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False

def build_python_local_plan(reference_backend: ExecutionBackend) -> CalibrationAcquisitionPlan:
    if reference_backend.backend_id != "python_local":
        raise ValueError("python_local_backend_required")
    return build_local_no_spend_plan(
        asdict(reference_backend), benchmark_id=BENCHMARK_ID,
        expected_output_digest=EXPECTED_OUTPUT_DIGEST,
    )

def _portable_body(transcript: PortableProbeTranscript) -> dict[str, Any]:
    return asdict(transcript)

def portable_transcript_digest(transcript: PortableProbeTranscript) -> str:
    return _hash(_portable_body(transcript))

def transcript_to_json(transcript: PortableProbeTranscript) -> str:
    return _canonical_json(_portable_body(transcript))

def transcript_from_json(raw: str) -> PortableProbeTranscript:
    try:
        data = json.loads(raw)
    except Exception as exc:
        raise ValueError("invalid_transcript_json") from exc
    if not isinstance(data, dict) or data.get("format_version") != 1:
        raise ValueError("unsupported_transcript_format")
    rows = data.get("observations")
    if not isinstance(rows, list):
        raise ValueError("transcript_observations_required")
    observations = tuple(ProbeObservation(**row) for row in rows)
    return PortableProbeTranscript(
        format_version=1,
        backend_id=str(data.get("backend_id") or ""),
        benchmark_id=str(data.get("benchmark_id") or ""),
        reference_backend_hash=str(data.get("reference_backend_hash") or ""),
        expected_output_digest=str(data.get("expected_output_digest") or ""),
        observations=observations,
        max_parallelism_observed=int(data.get("max_parallelism_observed", 0)),
        rate_limit_per_minute_observed=data.get("rate_limit_per_minute_observed"),
        i053_transcript_digest=str(data.get("i053_transcript_digest") or ""),
        runner_kind=str(data.get("runner_kind") or ""),
        network_enabled=bool(data.get("network_enabled")),
        credentials_used=bool(data.get("credentials_used")),
        spend_performed=bool(data.get("spend_performed")),
        value_movement_enabled=bool(data.get("value_movement_enabled")),
    )

def run_python_local_fixture(reference_backend: ExecutionBackend, *, enabled: bool = False, repetitions: int = 10) -> PortableProbeTranscript:
    if not enabled:
        raise RuntimeError("benchmark_runner_opt_in_required")
    plan = build_python_local_plan(reference_backend)
    if repetitions < plan.probe_contract.minimum_repetitions:
        raise ValueError("insufficient_probe_repetitions")
    observations = []
    for index in range(repetitions):
        started = perf_counter()
        output_digest = None
        succeeded = False
        quality = False
        try:
            output = benchmark_transform()
            output_digest = _hash(output)
            succeeded = output_digest == plan.probe_contract.expected_output_digest
            quality = succeeded and output == EXPECTED_OUTPUT
        finally:
            latency = max(0.0, perf_counter() - started)
        observations.append(ProbeObservation(
            run_id=f"local-{index:04d}", latency_seconds=latency,
            execution_succeeded=succeeded, output_digest=output_digest,
            quality_passed=quality,
        ))
    summary = evaluate_probe_transcript(
        plan.probe_contract, observations, max_parallelism_observed=1,
        rate_limit_per_minute_observed=None,
    )
    return PortableProbeTranscript(
        format_version=1, backend_id=plan.backend_id, benchmark_id=BENCHMARK_ID,
        reference_backend_hash=plan.reference_backend_hash,
        expected_output_digest=EXPECTED_OUTPUT_DIGEST,
        observations=tuple(observations), max_parallelism_observed=1,
        rate_limit_per_minute_observed=None,
        i053_transcript_digest=summary.transcript_digest,
    )

def replay_python_local_transcript(reference_backend: ExecutionBackend, raw_transcript_json: str) -> TranscriptReplay:
    plan = build_python_local_plan(reference_backend)
    transcript = transcript_from_json(raw_transcript_json)
    if transcript.backend_id != plan.backend_id:
        raise ValueError("transcript_backend_mismatch")
    if transcript.benchmark_id != plan.probe_contract.benchmark_id:
        raise ValueError("transcript_benchmark_mismatch")
    if transcript.reference_backend_hash != plan.reference_backend_hash:
        raise ValueError("transcript_reference_hash_mismatch")
    if transcript.expected_output_digest != plan.probe_contract.expected_output_digest:
        raise ValueError("transcript_expected_output_mismatch")
    if transcript.runner_kind != "local_python_fixed_fixture":
        raise ValueError("unexpected_runner_kind")
    if transcript.network_enabled or transcript.credentials_used or transcript.spend_performed or transcript.value_movement_enabled:
        raise ValueError("transcript_not_inert")
    for row in transcript.observations:
        if row.execution_succeeded and row.output_digest != EXPECTED_OUTPUT_DIGEST:
            raise ValueError("transcript_output_digest_mismatch")
        if row.quality_passed and row.output_digest != EXPECTED_OUTPUT_DIGEST:
            raise ValueError("transcript_quality_digest_mismatch")
    summary = evaluate_probe_transcript(
        plan.probe_contract, transcript.observations,
        max_parallelism_observed=transcript.max_parallelism_observed,
        rate_limit_per_minute_observed=transcript.rate_limit_per_minute_observed,
    )
    if summary.transcript_digest != transcript.i053_transcript_digest:
        raise ValueError("i053_transcript_digest_mismatch")
    return TranscriptReplay(
        plan=plan, transcript=transcript, probe_summary=summary,
        portable_transcript_digest=portable_transcript_digest(transcript), verified=True,
    )

def replay_transcript_through_i055(
    reference_backend: ExecutionBackend, raw_transcript_json: str, *,
    probe_observed_at_utc: str, now, platform: str,
    task_payload: Mapping[str, Any], demand_evidence_class: str,
    declarations: Iterable[ExplicitDeclaration] = (),
    energy_measurement: Optional[EnergyMeasurement] = None,
    capabilities: CapabilityProfile | None = None,
    cost: CostProfile | None = None,
) -> CalibrationRoutingPacket:
    replay = replay_python_local_transcript(reference_backend, raw_transcript_json)
    return build_calibration_routing_packet(
        reference_backend, benchmark_id=BENCHMARK_ID,
        expected_output_digest=EXPECTED_OUTPUT_DIGEST, now=now,
        platform=platform, task_payload=task_payload,
        demand_evidence_class=demand_evidence_class,
        probe_summary=replay.probe_summary,
        probe_observed_at_utc=probe_observed_at_utc,
        declarations=tuple(declarations), energy_measurement=energy_measurement,
        capabilities=capabilities, cost=cost,
    )
