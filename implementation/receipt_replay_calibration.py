"""I061 deterministic replay/verification and calibration feedback for I060 receipts."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json, math
from typing import Any, Optional

from local_execution_receipt import LocalExecutionPlan, LocalExecutionReceipt
from resource_profile_evidence import ResourceEvidence, make_evidence, reference_backend_hash

def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class ReceiptReplayVerification:
    state: str
    reasons: tuple[str, ...]
    receipt_hash: str
    plan_hash: str
    task_id: str
    backend_id: str
    provenance_binding_hash: str
    fixture_hash: str
    output_hash: str
    expected_output_hash: str
    runtime_seconds: Optional[float]
    observed_energy_cost_usd: Optional[float]
    observed_total_incremental_cost_usd: Optional[float]
    router_marginal_cost_usd: float
    runtime_fact_verified: bool
    energy_fact_verified: bool
    total_cost_fact_verified: bool
    market_demand_evidence: bool = False
    execution_authorized: bool = False
    dry_run_only: bool = True
    network_enabled: bool = False
    credentials_enabled: bool = False
    submission_enabled: bool = False
    value_movement_enabled: bool = False

@dataclass(frozen=True)
class CalibrationFeedback:
    state: str
    reasons: tuple[str, ...]
    backend_id: str
    receipt_hash: str
    evidence_records: tuple[ResourceEvidence, ...]
    runtime_evidence_emitted: bool
    electricity_evidence_emitted: bool
    total_incremental_cost_observed_usd: Optional[float]
    reliability_inferred: bool = False
    quality_probability_inferred: bool = False
    market_demand_evidence: bool = False
    execution_authorized: bool = False
    dry_run_only: bool = True
    network_enabled: bool = False
    value_movement_enabled: bool = False

def _finite_nonnegative(value: Any) -> bool:
    return (not isinstance(value, bool) and isinstance(value, (int, float))
            and math.isfinite(float(value)) and float(value) >= 0.0)

def verify_i060_receipt(plan: LocalExecutionPlan, receipt: LocalExecutionReceipt) -> ReceiptReplayVerification:
    reasons: list[str] = []
    expected_plan_hash = _hash(asdict(plan))
    receipt_hash = _hash(asdict(receipt))
    if any((plan.network_enabled, plan.credentials_enabled, plan.submission_enabled, plan.value_movement_enabled)):
        reasons.append("plan_not_inert")
    if any((not receipt.dry_run_only, receipt.network_enabled, receipt.credentials_enabled,
            receipt.submission_enabled, receipt.value_movement_enabled)):
        reasons.append("receipt_not_inert")
    if receipt.plan_hash != expected_plan_hash: reasons.append("plan_hash_mismatch")
    if receipt.task_id != plan.task_id: reasons.append("task_identity_mismatch")
    if receipt.backend_id != plan.backend_id or plan.backend_id != "python_local": reasons.append("backend_identity_mismatch")
    if receipt.provenance_binding_hash != plan.provenance_binding_hash: reasons.append("provenance_identity_mismatch")
    if receipt.fixture_hash != plan.fixture_hash: reasons.append("fixture_identity_mismatch")
    if receipt.output_hash != plan.expected_output_hash or not receipt.output_matches_expected:
        reasons.append("expected_output_identity_mismatch")
    if receipt.router_marginal_cost_usd != plan.router_marginal_cost_usd:
        reasons.append("router_quote_identity_mismatch")
    if receipt.state != "receipt_verified_inert" or receipt.reasons:
        reasons.append("source_receipt_not_verified")

    runtime_ok = _finite_nonnegative(receipt.runtime_seconds)
    if not runtime_ok: reasons.append("invalid_runtime_fact")
    energy = receipt.observed_energy_cost_usd
    total = receipt.observed_total_incremental_cost_usd
    energy_ok = energy is not None and _finite_nonnegative(energy)
    total_ok = total is not None and _finite_nonnegative(total)

    if energy is None:
        if total is not None:
            reasons.append("total_cost_present_with_unknown_energy")
            total_ok = False
    else:
        if not energy_ok: reasons.append("invalid_energy_cost_fact")
        if total is None:
            reasons.append("total_cost_missing_with_known_energy")
            total_ok = False
        elif total_ok and float(total) + 1e-12 < float(energy):
            reasons.append("total_cost_below_energy_cost")
            total_ok = False
    if total_ok and float(total) > plan.router_marginal_cost_usd + plan.max_cost_drift_usd + 1e-12:
        reasons.append("observed_incremental_cost_exceeds_router_quote")
        total_ok = False

    state = "verified_i060_replay" if not reasons else "hold"
    clean = not reasons
    return ReceiptReplayVerification(
        state=state, reasons=tuple(dict.fromkeys(reasons)), receipt_hash=receipt_hash,
        plan_hash=expected_plan_hash, task_id=plan.task_id, backend_id=plan.backend_id,
        provenance_binding_hash=plan.provenance_binding_hash, fixture_hash=plan.fixture_hash,
        output_hash=receipt.output_hash, expected_output_hash=plan.expected_output_hash,
        runtime_seconds=float(receipt.runtime_seconds) if runtime_ok else None,
        observed_energy_cost_usd=float(energy) if energy_ok else None,
        observed_total_incremental_cost_usd=float(total) if total_ok else None,
        router_marginal_cost_usd=float(plan.router_marginal_cost_usd),
        runtime_fact_verified=runtime_ok and clean,
        energy_fact_verified=energy_ok and clean,
        total_cost_fact_verified=total_ok and clean,
    )

def calibration_feedback_from_verified_receipt(
    verification: ReceiptReplayVerification,
    reference_backend: dict[str, Any],
    *, observed_at: str, max_age_seconds: int = 86400
) -> CalibrationFeedback:
    reasons: list[str] = []
    records: list[ResourceEvidence] = []
    if verification.state != "verified_i060_replay": reasons.append("receipt_replay_not_verified")
    if verification.backend_id != "python_local": reasons.append("python_local_only")
    if str(reference_backend.get("backend_id") or "") != verification.backend_id: reasons.append("reference_backend_mismatch")
    if max_age_seconds <= 0: reasons.append("invalid_max_age_seconds")
    try:
        dt = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt): raise ValueError
    except Exception:
        reasons.append("observed_at_must_be_utc")
    if reasons:
        return CalibrationFeedback("planning_only", tuple(dict.fromkeys(reasons)), verification.backend_id,
            verification.receipt_hash, (), False, False, verification.observed_total_incremental_cost_usd)

    ref_hash = reference_backend_hash(reference_backend)
    source_ref = f"i060-receipt:{verification.receipt_hash}"
    digest = verification.receipt_hash
    if verification.runtime_fact_verified and verification.runtime_seconds is not None:
        records.append(make_evidence(
            evidence_id=f"i061-runtime-{verification.receipt_hash[:16]}",
            backend_id=verification.backend_id, parameter="latency_seconds",
            value=verification.runtime_seconds, source_kind="measured_local",
            source_ref=source_ref, observed_at=observed_at, max_age_seconds=max_age_seconds,
            reference_hash=ref_hash, source_content_digest=digest,
            notes="Exact fixed-fixture I060 wall-clock runtime; not market latency/throughput."
        ))
    if verification.energy_fact_verified and verification.observed_energy_cost_usd is not None:
        records.append(make_evidence(
            evidence_id=f"i061-energy-{verification.receipt_hash[:16]}",
            backend_id=verification.backend_id, parameter="electricity_per_task_usd",
            value=verification.observed_energy_cost_usd, source_kind="measured_local",
            source_ref=source_ref, observed_at=observed_at, max_age_seconds=max_age_seconds,
            reference_hash=ref_hash, source_content_digest=digest,
            notes="Explicit I060 fixed-fixture energy-cost observation; unknown energy emits no evidence."
        ))
    state = "measured_feedback_ready" if records else "verified_but_no_calibratable_facts"
    return CalibrationFeedback(
        state, (), verification.backend_id, verification.receipt_hash, tuple(records),
        any(x.parameter=="latency_seconds" for x in records),
        any(x.parameter=="electricity_per_task_usd" for x in records),
        verification.observed_total_incremental_cost_usd
    )

def replay_record(verification: ReceiptReplayVerification) -> dict[str, Any]:
    record = asdict(verification)
    record.update(market_demand_evidence=False, execution_authorized=False, dry_run_only=True,
                  network_enabled=False, credentials_enabled=False, submission_enabled=False,
                  value_movement_enabled=False)
    return record
