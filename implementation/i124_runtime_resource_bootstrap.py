"""I124 portable no-spend runtime + resource bootstrap.

Runs the exact I113 offline runtime chain and a current python_local calibration
probe in one repository-local command, then projects only observed facts into the
I123 backend-evidence model. It never performs market/network access, credentials,
spend, task acceptance, submission, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from i126_python_local_config_invariant import build_python_local_config_invariants
from python_local_calibration_fixture import (
    run_python_local_fixture,
    transcript_to_json,
    replay_python_local_transcript,
)
from local_calibration_session import build_session_bundle, replay_session_bundle, session_to_json
from resource_router import default_backend_families

SCHEMA_VERSION = 2
DEFAULT_OUTPUT = "I124_RUNTIME_RESOURCE_BOOTSTRAP_RESULT.json"
I113_OUTPUT = "I113_LOCAL_RUNTIME_CHAIN_RESULT.json"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _hash(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _python_local_backend():
    return next(b for b in default_backend_families() if b.backend_id == "python_local")


def _run_i113(root: Path, timeout_seconds: int) -> dict[str, Any]:
    output = root / "implementation" / I113_OUTPUT
    if output.exists():
        output.unlink()
    command = [
        sys.executable,
        str(root / "implementation" / "i113_local_runtime_chain_runner.py"),
        "--output",
        str(output),
    ]
    try:
        proc = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired as exc:
        return {"state": "FAIL_CLOSED", "reason": "i113_timeout", "timeout_seconds": timeout_seconds, "stdout": exc.stdout or "", "stderr": exc.stderr or ""}
    except OSError as exc:
        return {"state": "FAIL_CLOSED", "reason": "i113_launch_error", "error_type": type(exc).__name__, "error": str(exc)}
    payload = None
    if output.exists():
        try:
            payload = json.loads(output.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"state": "FAIL_CLOSED", "reason": "i113_output_parse_error", "returncode": proc.returncode, "error_type": type(exc).__name__}
    return {
        "state": "PASS_BLOCKED" if proc.returncode == 0 and isinstance(payload, dict) and payload.get("result") == "PASS_BLOCKED" else "FAIL_CLOSED",
        "returncode": proc.returncode,
        "receipt_present": payload is not None,
        "receipt": payload,
        "stderr_tail": proc.stderr[-2000:],
    }


def _run_python_local_probe(observed_at: str, repetitions: int) -> dict[str, Any]:
    backend = _python_local_backend()
    transcript = run_python_local_fixture(backend, enabled=True, repetitions=repetitions)
    raw = transcript_to_json(transcript)
    replay = replay_python_local_transcript(backend, raw)
    session = build_session_bundle(backend, raw, collector_observed_at_utc=observed_at)
    report = replay_session_bundle(backend, session_to_json(session))
    config = build_python_local_config_invariants(asdict(backend), observed_at=observed_at)
    successes = replay.probe_summary.successful_runs
    count = replay.probe_summary.observation_count
    reliability = successes / count if count else 0.0
    quality_passes = sum(1 for row in transcript.observations if row.quality_passed)
    quality = quality_passes / count if count else 0.0
    raw_missing = set(report.missing_parameters)
    config_parameters = set(config.emitted_parameters)
    effective_missing = tuple(sorted(raw_missing - config_parameters))
    return {
        "state": "MEASURED_LOCAL_PROBE_COMPLETE" if replay.verified else "FAIL_CLOSED",
        "backend_id": backend.backend_id,
        "observed_at": observed_at,
        "repetitions": count,
        "successful_runs": successes,
        "quality_passes": quality_passes,
        "latency_p95_seconds": replay.probe_summary.latency_p95_seconds,
        "reliability_probability_observed": reliability,
        "quality_probability_observed": quality,
        "max_parallelism_observed": transcript.max_parallelism_observed,
        "rate_limit_per_minute_observed": transcript.rate_limit_per_minute_observed,
        "portable_transcript_digest": replay.portable_transcript_digest,
        "session_digest": session.immutable_session_digest,
        "session_replay": asdict(report),
        "i126_config_invariant_parameters": tuple(config.emitted_parameters),
        "i126_config_invariants_ready": True,
        "effective_missing_parameters_after_i126": effective_missing,
        "network_enabled": False,
        "credentials_used": False,
        "spend_performed": False,
        "value_movement_enabled": False,
    }


def _project_i123_evidence(probe: dict[str, Any]) -> tuple[BackendEvidence, tuple[str, ...]]:
    blockers: list[str] = []
    measured_ok = probe.get("state") == "MEASURED_LOCAL_PROBE_COMPLETE"
    if not measured_ok:
        blockers.append("python_local_probe_not_verified")
    if probe.get("repetitions", 0) < 10:
        blockers.append("insufficient_probe_repetitions")
    if probe.get("reliability_probability_observed", 0.0) < 0.90:
        blockers.append("observed_reliability_below_threshold")
    if probe.get("quality_probability_observed", 0.0) < 0.90:
        blockers.append("observed_quality_below_threshold")

    if "effective_missing_parameters_after_i126" in probe:
        missing = set(probe.get("effective_missing_parameters_after_i126") or ())
        if not probe.get("i126_config_invariants_ready"):
            blockers.append("python_local_config_invariants_not_ready")
    else:
        # Backward-compatible unit fixtures without I126 metadata remain conservative.
        report = probe.get("session_replay") or {}
        missing = set(report.get("missing_parameters") or ())

    if missing:
        blockers.append("i050_critical_resource_facts_incomplete")
    if "electricity_per_task_usd" in missing:
        blockers.append("electricity_cost_not_measured")
    if "quota_units_remaining" in missing:
        blockers.append("quota_capacity_not_evidenced")
    if "rate_limit_per_minute" in missing:
        blockers.append("rate_limit_not_evidenced")

    complete = measured_ok and not blockers
    evidence = BackendEvidence(
        backend_id="python_local",
        provenance_class=MEASURED if complete else "measured_partial",
        current_reproducible=measured_ok,
        non_synthetic=measured_ok,
        capacity_verified=complete,
        policy_evidence_current=measured_ok,
        credentials_authorized=False,
        spend_authorized=False,
        infrastructure_authorized=False,
        evidence_note=(
            "I124 v2 fixed local probe plus I126 exact python_local config invariants. "
            "Production-selectable only after all remaining dynamic I050 economics/capacity facts are current and reproducible."
        ),
    )
    return evidence, tuple(dict.fromkeys(blockers))


def _free_ci_evidence(runtime: dict[str, Any]) -> tuple[BackendEvidence, tuple[str, ...]]:
    blockers = ["free_tier_ci_capacity_quota_not_materialized", "free_tier_ci_policy_capacity_evidence_not_materialized"]
    receipt = runtime.get("receipt") or {}
    source_current = runtime.get("state") == "PASS_BLOCKED" and receipt.get("result") == "PASS_BLOCKED"
    evidence = BackendEvidence(
        backend_id="free_tier_ci",
        provenance_class="runtime_observed_partial" if source_current else "planning_reference",
        current_reproducible=source_current,
        non_synthetic=source_current,
        capacity_verified=False,
        policy_evidence_current=False,
        evidence_note="I113 runtime can prove execution of the offline chain, but does not by itself prove current Actions quota/capacity or autonomous dispatch availability.",
    )
    return evidence, tuple(blockers)


def build_result(root: Path, *, repetitions: int = 20, i113_timeout_seconds: int = 1200) -> dict[str, Any]:
    observed_at = _utc_now()
    runtime = _run_i113(root, i113_timeout_seconds)
    try:
        probe = _run_python_local_probe(observed_at, repetitions)
    except Exception as exc:
        probe = {"state": "FAIL_CLOSED", "reason": "python_local_probe_error", "error_type": type(exc).__name__, "error": str(exc)}
    python_ev, python_blockers = _project_i123_evidence(probe)
    ci_ev, ci_blockers = _free_ci_evidence(runtime)
    review = {
        "python_local": {"backend_evidence": asdict(python_ev), "production_blockers": python_blockers, "production_selectable": python_ev.provenance_class == MEASURED and not python_blockers},
        "free_tier_ci": {"backend_evidence": asdict(ci_ev), "production_blockers": ci_blockers, "production_selectable": False},
    }
    state = "READY_FOR_PORTFOLIO_MATERIALIZATION" if any(x["production_selectable"] for x in review.values()) else "PASS_BLOCKED"
    body = {
        "schema_version": SCHEMA_VERSION,
        "state": state,
        "observed_at": observed_at,
        "root": str(root),
        "i113_runtime": runtime,
        "python_local_probe": probe,
        "backend_review": review,
        "remaining_independent_blockers": {
            "fresh_real_market_evidence": True,
            "eligible_non_synthetic_positive_margin_route": not any(x["production_selectable"] for x in review.values()),
            "exact_explicit_authorization": True,
        },
        "safety": {
            "market_network_access": False,
            "credentials_used": False,
            "new_spend": False,
            "task_acceptance": False,
            "submission": False,
            "value_movement": False,
        },
    }
    body["result_hash"] = _hash(body)
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--i113-timeout-seconds", type=int, default=1200)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.repetitions < 10:
        raise SystemExit("repetitions_must_be_at_least_10")
    result = build_result(root, repetitions=args.repetitions, i113_timeout_seconds=args.i113_timeout_seconds)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / "implementation" / output
    output.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"state": result["state"], "output": str(output), "result_hash": result["result_hash"]}, sort_keys=True))
    return 0 if result["state"] in {"PASS_BLOCKED", "READY_FOR_PORTFOLIO_MATERIALIZATION"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
