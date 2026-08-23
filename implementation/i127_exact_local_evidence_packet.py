"""I127 exact python_local evidence packet over I124 + I126 + I050/I066/I123.

Runs I124 when invoked in a real checkout, converts its verified fixed local probe
into exact I050 ResourceEvidence, merges only the narrow I126 config invariants,
optionally accepts additional explicit evidence records for the still-missing
dynamic facts, and emits a fail-closed resource-readiness packet.

No market network access, credentials, paid service, task acceptance, submission,
authorization creation, or value movement is performed here.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

import i124_runtime_resource_bootstrap as i124
from i126_python_local_config_invariant import (
    attest_with_python_local_invariants,
    project_i050_attestation_to_i123,
    verify_i066_compatibility,
)
from resource_profile_evidence import (
    ResourceEvidence,
    make_evidence,
    reference_backend_hash,
)
from resource_router import default_backend_families

SCHEMA_VERSION = 1
DEFAULT_OUTPUT = "I127_EXACT_LOCAL_EVIDENCE_PACKET.json"

PROBE_PARAMETERS = (
    "currently_available",
    "programmatic_access",
    "latency_seconds",
    "reliability_probability",
    "quality_probability",
    "max_parallelism",
)
ALLOWED_ADDITIONAL_PARAMETERS = frozenset({
    "quota_units_remaining",
    "electricity_per_task_usd",
    "rate_limit_per_minute",
})


def _python_local_reference() -> dict[str, Any]:
    backend = next(x for x in default_backend_families() if x.backend_id == "python_local")
    return asdict(backend)


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def _probe_value_map(probe: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "currently_available": probe.get("state") == "MEASURED_LOCAL_PROBE_COMPLETE",
        "programmatic_access": probe.get("state") == "MEASURED_LOCAL_PROBE_COMPLETE",
        "latency_seconds": float(probe["latency_p95_seconds"]),
        "reliability_probability": float(probe["reliability_probability_observed"]),
        "quality_probability": float(probe["quality_probability_observed"]),
        "max_parallelism": int(probe["max_parallelism_observed"]),
    }


def _validate_i124_probe(probe: Mapping[str, Any]) -> None:
    if probe.get("state") != "MEASURED_LOCAL_PROBE_COMPLETE":
        raise ValueError("i124_probe_not_verified")
    if probe.get("backend_id") != "python_local":
        raise ValueError("i124_probe_backend_mismatch")
    if int(probe.get("repetitions", 0)) < 10:
        raise ValueError("i124_probe_repetitions_insufficient")
    if any(bool(probe.get(k)) for k in (
        "network_enabled", "credentials_used", "spend_performed", "value_movement_enabled"
    )):
        raise ValueError("i124_probe_not_inert")
    digest = str(probe.get("portable_transcript_digest") or "")
    if len(digest) < 16:
        raise ValueError("i124_probe_digest_missing")
    _parse_utc(str(probe.get("observed_at") or ""))


def build_probe_evidence(
    reference_backend: Mapping[str, Any],
    probe: Mapping[str, Any],
) -> tuple[ResourceEvidence, ...]:
    _validate_i124_probe(probe)
    observed_at = str(probe["observed_at"])
    digest = str(probe["portable_transcript_digest"])
    ref_hash = reference_backend_hash(reference_backend)
    values = _probe_value_map(probe)
    records = []
    for parameter in PROBE_PARAMETERS:
        records.append(make_evidence(
            evidence_id=f"i127-i124-probe-{parameter}",
            backend_id="python_local",
            parameter=parameter,
            value=values[parameter],
            source_kind="system_probe",
            source_ref=f"i124-portable-transcript:{digest}",
            observed_at=observed_at,
            max_age_seconds=86400,
            reference_hash=ref_hash,
            source_content_digest=digest,
            notes="Exact value derived from the verified inert I124 fixed local probe result.",
        ))
    return tuple(records)


def _resource_evidence_from_dict(raw: Mapping[str, Any]) -> ResourceEvidence:
    required = {
        "evidence_id", "backend_id", "parameter", "value", "source_kind",
        "source_ref", "observed_at", "max_age_seconds", "reference_backend_hash",
    }
    missing = required - set(raw)
    if missing:
        raise ValueError("additional_evidence_missing_fields:" + ",".join(sorted(missing)))
    record = ResourceEvidence(**dict(raw))
    if record.backend_id != "python_local":
        raise ValueError("additional_evidence_python_local_only")
    if record.parameter not in ALLOWED_ADDITIONAL_PARAMETERS:
        raise ValueError("additional_evidence_parameter_not_allowed:" + record.parameter)
    if record.evidence_hash != record.computed_hash():
        raise ValueError("additional_evidence_hash_invalid")
    return record


def load_additional_evidence(path: Path | None) -> tuple[ResourceEvidence, ...]:
    if path is None:
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("additional_evidence_records_list_required")
    records = tuple(_resource_evidence_from_dict(row) for row in rows)
    parameters = [r.parameter for r in records]
    if len(parameters) != len(set(parameters)):
        raise ValueError("duplicate_additional_evidence_parameter")
    return records


def build_exact_packet(
    i124_payload: Mapping[str, Any],
    *,
    additional_records: Iterable[ResourceEvidence] = (),
) -> dict[str, Any]:
    reference = _python_local_reference()
    probe = i124_payload.get("python_local_probe")
    if not isinstance(probe, Mapping):
        raise ValueError("i124_python_local_probe_required")
    probe_records = build_probe_evidence(reference, probe)
    extras = tuple(additional_records)
    observed_at = str(probe["observed_at"])
    now = _parse_utc(observed_at)
    attestation, all_records = attest_with_python_local_invariants(
        reference, probe_records + extras, observed_at=observed_at, now=now
    )
    i123_evidence = project_i050_attestation_to_i123(attestation)
    missing = tuple(
        row.parameter for row in attestation.parameter_calibrations if row.state != "current"
    )
    i066 = None
    if attestation.state == "calibrated_reproducible":
        materialization = verify_i066_compatibility(reference, all_records, now=now)
        i066 = asdict(materialization)
    return {
        "schema_version": SCHEMA_VERSION,
        "state": "RESOURCE_EVIDENCE_COMPLETE" if not missing else "PASS_BLOCKED",
        "i124_result_hash": i124_payload.get("result_hash"),
        "observed_at": observed_at,
        "resource_evidence_records": [asdict(x) for x in all_records],
        "i050_attestation": asdict(attestation),
        "missing_parameters": missing,
        "i066_materialization": i066,
        "i123_backend_evidence": asdict(i123_evidence),
        "current_resource_route_created": False,
        "fresh_real_market_evidence_created": False,
        "authorization_created": False,
        "production_observation_performed": False,
        "safety": {
            "market_network_access": False,
            "credentials_used": False,
            "new_spend": False,
            "task_acceptance": False,
            "submission": False,
            "value_movement": False,
        },
        "notes": (
            "I127 converts only I124 measured probe facts plus I126 exact config invariants.",
            "quota_units_remaining, electricity_per_task_usd and rate_limit_per_minute stay missing unless supplied as independent hash-valid evidence.",
            "A complete I050/I066 resource packet still does not prove market demand, positive task economics or authorization.",
        ),
    }


def build_result(
    root: Path,
    *,
    repetitions: int = 20,
    i113_timeout_seconds: int = 1200,
    additional_evidence_path: Path | None = None,
) -> dict[str, Any]:
    i124_payload = i124.build_result(
        root, repetitions=repetitions, i113_timeout_seconds=i113_timeout_seconds
    )
    extras = load_additional_evidence(additional_evidence_path)
    packet = build_exact_packet(i124_payload, additional_records=extras)
    packet["i124_state"] = i124_payload.get("state")
    packet["i113_runtime"] = i124_payload.get("i113_runtime")
    return packet


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--i113-timeout-seconds", type=int, default=1200)
    parser.add_argument("--additional-evidence-json")
    args = parser.parse_args(argv)
    if args.repetitions < 10:
        raise SystemExit("repetitions_must_be_at_least_10")
    root = Path(args.root).resolve()
    extra = Path(args.additional_evidence_json).resolve() if args.additional_evidence_json else None
    result = build_result(
        root,
        repetitions=args.repetitions,
        i113_timeout_seconds=args.i113_timeout_seconds,
        additional_evidence_path=extra,
    )
    output = Path(args.output)
    if not output.is_absolute():
        output = root / "implementation" / output
    output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "state": result["state"],
        "missing_parameters": result["missing_parameters"],
        "output": str(output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
