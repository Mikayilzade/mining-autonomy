"""I127 complete no-spend python_local resource-evidence assembly path.

Combines four already-distinct evidence sources without widening production gates:
1) I056/I053 fixed local probe -> availability/programmatic access/latency/reliability/
   quality/max_parallelism;
2) I126 exact python_local intrinsic configuration invariants;
3) a narrow python_local-only local-interface semantic probe establishing that the
   local deterministic executor has no external provider quota or provider rate-limit
   layer (None means not applicable at that interface, NOT infinite host capacity);
4) optional explicit measured energy+tariff input through the existing I054 adapter.

No market/network request, credentials, paid infrastructure, task acceptance,
submission, authorization creation, spend, or value movement occurs here. Missing
energy remains missing and prevents strict I050/I123 promotion.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
from pathlib import Path
from typing import Any, Optional

from i123_execution_backend_portfolio import BackendEvidence
from i124_runtime_resource_bootstrap import _run_i113
from i126_python_local_config_invariant import (
    build_python_local_config_invariants,
    project_i050_attestation_to_i123,
    verify_i066_compatibility,
)
from python_local_calibration_fixture import (
    BENCHMARK_ID,
    EXPECTED_OUTPUT_DIGEST,
    replay_python_local_transcript,
    run_python_local_fixture,
    transcript_to_json,
)
from resource_calibration_acquisition import ProbeSummary, build_local_no_spend_plan
from resource_evidence_adapter import (
    EnergyMeasurement,
    build_resource_evidence,
    normalize_probe_summary_for_evidence,
)
from resource_profile_evidence import (
    CRITICAL_PARAMETERS,
    ResourceEvidence,
    attest_resource_profile,
    make_evidence,
    reference_backend_hash,
)
from resource_router import default_backend_families

SCHEMA = "mining-autonomy/i127-python-local-resource-completion/v1"
INTERFACE_SEMANTIC_SCHEMA = "mining-autonomy/python-local-interface-semantics/v1"
INTERFACE_PARAMETERS = {
    "quota_units_remaining": None,
    "rate_limit_per_minute": None,
}


@dataclass(frozen=True)
class ResourceCompletionPacket:
    state: str
    observed_at: str
    probe_summary: dict[str, Any]
    evidence_records: tuple[ResourceEvidence, ...]
    emitted_parameters: tuple[str, ...]
    missing_parameters: tuple[str, ...]
    i050_state: str
    i050_reproducible: bool
    i066_state: Optional[str]
    i123_evidence: BackendEvidence
    runtime_receipt_state: str
    energy_measurement_supplied: bool
    strict_resource_promotion_ready: bool
    production_route_created: bool = False
    fresh_real_market_evidence_created: bool = False
    authorization_created: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    spend_performed: bool = False
    value_movement_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def python_local_reference():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")


def build_local_interface_semantic_evidence(
    reference_backend: Any, *, observed_at: str,
) -> tuple[ResourceEvidence, ...]:
    """Emit only python_local provider-quota/rate semantic facts.

    `None` here means there is no *external provider/interface* quota or rate-limit
    primitive for the repository-local deterministic executor. It does not mean
    unbounded CPU capacity, zero opportunity cost, or unlimited parallelism; those
    remain independently measured/modelled.
    """
    reference = asdict(reference_backend) if hasattr(reference_backend, "backend_id") else dict(reference_backend)
    if reference.get("backend_id") != "python_local" or reference.get("family") != "deterministic_python":
        raise ValueError("python_local_deterministic_backend_required")
    if reference.get("quota_units_remaining") is not None:
        raise ValueError("python_local_reference_quota_semantic_drift")
    if reference.get("rate_limit_per_minute") is not None:
        raise ValueError("python_local_reference_rate_semantic_drift")
    ref_hash = reference_backend_hash(reference)
    manifest = {
        "schema": INTERFACE_SEMANTIC_SCHEMA,
        "backend_id": "python_local",
        "family": "deterministic_python",
        "reference_backend_hash": ref_hash,
        "meaning": "no_external_provider_quota_or_rate_limit; host_capacity_remains_separate",
        "values": INTERFACE_PARAMETERS,
    }
    digest = _digest(manifest)
    return tuple(
        make_evidence(
            evidence_id=f"i127-python-local-interface-{parameter}",
            backend_id="python_local",
            parameter=parameter,
            value=value,
            source_kind="system_probe",
            source_ref=f"i127-interface-semantics:{digest}:{parameter}",
            observed_at=observed_at,
            max_age_seconds=86400,
            reference_hash=ref_hash,
            source_content_digest=digest,
            notes=(
                "No external provider quota/rate primitive for this repository-local executor. "
                "None is not an infinite-capacity claim; max_parallelism, latency, reliability, "
                "quality, electricity and opportunity cost remain separate facts."
            ),
        )
        for parameter, value in INTERFACE_PARAMETERS.items()
    )


def assemble_python_local_evidence(
    reference_backend: Any,
    probe_summary: ProbeSummary,
    *,
    observed_at: str,
    now: datetime,
    energy_measurement: Optional[EnergyMeasurement] = None,
) -> tuple[ResourceCompletionPacket, Any]:
    reference = asdict(reference_backend) if hasattr(reference_backend, "backend_id") else dict(reference_backend)
    plan = build_local_no_spend_plan(
        reference,
        benchmark_id=BENCHMARK_ID,
        expected_output_digest=EXPECTED_OUTPUT_DIGEST,
    )
    normalized = normalize_probe_summary_for_evidence(probe_summary, observed_at_utc=observed_at)
    dynamic = build_resource_evidence(
        plan,
        probe_summary=normalized,
        energy_measurement=energy_measurement,
    )
    config = build_python_local_config_invariants(reference, observed_at=observed_at)
    interface = build_local_interface_semantic_evidence(reference, observed_at=observed_at)

    by_parameter: dict[str, ResourceEvidence] = {}
    for record in (*dynamic.records, *config.evidence_records, *interface):
        if record.parameter in by_parameter:
            raise ValueError(f"duplicate_resource_parameter:{record.parameter}")
        by_parameter[record.parameter] = record
    records = tuple(by_parameter[p] for p in CRITICAL_PARAMETERS if p in by_parameter)
    missing = tuple(p for p in CRITICAL_PARAMETERS if p not in by_parameter)
    attestation = attest_resource_profile(reference, records, now=now)
    i123 = project_i050_attestation_to_i123(attestation)

    i066_state: Optional[str] = None
    if not missing and attestation.state == "calibrated_reproducible":
        materialized = verify_i066_compatibility(reference, records, now=now)
        i066_state = materialized.state

    strict_ready = (
        not missing
        and attestation.state == "calibrated_reproducible"
        and attestation.all_current_evidence_reproducible
        and i066_state == "materialized_reproducible"
        and i123.provenance_class == "measured_reproducible"
    )
    packet = ResourceCompletionPacket(
        state="RESOURCE_EVIDENCE_COMPLETE" if strict_ready else "PASS_BLOCKED",
        observed_at=observed_at,
        probe_summary=asdict(probe_summary),
        evidence_records=records,
        emitted_parameters=tuple(r.parameter for r in records),
        missing_parameters=missing,
        i050_state=attestation.state,
        i050_reproducible=attestation.all_current_evidence_reproducible,
        i066_state=i066_state,
        i123_evidence=i123,
        runtime_receipt_state="not_checked_by_assemble_function",
        energy_measurement_supplied=energy_measurement is not None,
        strict_resource_promotion_ready=strict_ready,
    )
    return packet, attestation


def run_no_spend_bundle(
    root: Path,
    *,
    repetitions: int = 20,
    i113_timeout_seconds: int = 1200,
    energy_kwh_per_task: Optional[float] = None,
    tariff_usd_per_kwh: Optional[float] = None,
) -> ResourceCompletionPacket:
    if repetitions < 10:
        raise ValueError("repetitions_must_be_at_least_10")
    if (energy_kwh_per_task is None) != (tariff_usd_per_kwh is None):
        raise ValueError("energy_and_tariff_must_be_supplied_together")
    if energy_kwh_per_task is not None and (energy_kwh_per_task < 0 or tariff_usd_per_kwh < 0):
        raise ValueError("energy_and_tariff_must_be_nonnegative")

    runtime = _run_i113(root, i113_timeout_seconds)
    reference = python_local_reference()
    transcript = run_python_local_fixture(reference, enabled=True, repetitions=repetitions)
    replay = replay_python_local_transcript(reference, transcript_to_json(transcript))
    observed_at = _utc_now()
    now = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))

    energy: Optional[EnergyMeasurement] = None
    if energy_kwh_per_task is not None and tariff_usd_per_kwh is not None:
        energy = EnergyMeasurement(
            energy_kwh_per_task=float(energy_kwh_per_task),
            tariff_usd_per_kwh=float(tariff_usd_per_kwh),
            observed_at=observed_at,
            max_age_seconds=604800,
            source_ref="i127:explicit-local-energy-measurement",
            source_content_digest=_digest({
                "schema": "mining-autonomy/i127-explicit-energy-input/v1",
                "energy_kwh_per_task": float(energy_kwh_per_task),
                "tariff_usd_per_kwh": float(tariff_usd_per_kwh),
                "observed_at": observed_at,
            }),
            notes="Caller-supplied measured energy and explicit tariff; I127 does not infer either value.",
        )

    packet, _ = assemble_python_local_evidence(
        reference,
        replay.probe_summary,
        observed_at=observed_at,
        now=now,
        energy_measurement=energy,
    )
    runtime_state = str(runtime.get("state") or "FAIL_CLOSED")
    return ResourceCompletionPacket(
        **{
            **asdict(packet),
            "evidence_records": packet.evidence_records,
            "i123_evidence": packet.i123_evidence,
            "runtime_receipt_state": runtime_state,
            "state": (
                "RESOURCE_AND_RUNTIME_READY"
                if packet.strict_resource_promotion_ready and runtime_state == "PASS_BLOCKED"
                else "PASS_BLOCKED"
            ),
        }
    )


def payload(packet: ResourceCompletionPacket) -> dict[str, Any]:
    body = asdict(packet)
    body.update({
        "schema": SCHEMA,
        "run": "I127",
        "interface_none_semantics": "not_applicable_external_provider_limit_not_infinite_host_capacity",
        "remaining_independent_gates": {
            "fresh_real_market_evidence": False,
            "exact_explicit_authorization": False,
            "production_route": False,
        },
    })
    body["result_hash"] = _digest(body)
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", default="I127_PYTHON_LOCAL_RESOURCE_COMPLETION_RESULT.json")
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--i113-timeout-seconds", type=int, default=1200)
    parser.add_argument("--energy-kwh-per-task", type=float)
    parser.add_argument("--tariff-usd-per-kwh", type=float)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    packet = run_no_spend_bundle(
        root,
        repetitions=args.repetitions,
        i113_timeout_seconds=args.i113_timeout_seconds,
        energy_kwh_per_task=args.energy_kwh_per_task,
        tariff_usd_per_kwh=args.tariff_usd_per_kwh,
    )
    out = Path(args.output)
    if not out.is_absolute():
        out = root / "implementation" / out
    out.write_text(json.dumps(payload(packet), indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"state": packet.state, "missing": packet.missing_parameters, "output": str(out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
