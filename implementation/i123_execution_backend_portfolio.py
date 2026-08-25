#!/usr/bin/env python3
"""I123 portfolio-level Resource / Execution Router.

Production selection is fail-closed: measured evidence must be source-bound and
sensitive authorizations must carry independent explicit authorization origins.
No DNS/HTTP, credentials, CI dispatch, spend, task action, or value movement occurs here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Iterable, Optional

from resource_router import BackendQuote, ExecutionBackend, TaskEconomics, default_backend_families, quote_backend

MEASURED = "measured_reproducible"
PROMOTABLE_SOURCE_CLASSES = frozenset({"system_probe", "measurement_receipt", "external_meter_receipt", "runtime_receipt", "current_primary_source"})
NONPROMOTABLE_SOURCE_CLASSES = frozenset({"planning_reference", "declaration", "synthetic_fixture"})
KNOWN_SOURCE_CLASSES = PROMOTABLE_SOURCE_CLASSES | NONPROMOTABLE_SOURCE_CLASSES
AUTHORIZATION_ORIGINS = frozenset({"explicit_user_authorization"})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
AI_FAMILIES = frozenset({"local_cpu_gpu_model", "chatgpt_codex_subscription", "cheap_external_llm_api", "strong_external_llm_api"})

@dataclass(frozen=True)
class BackendEvidence:
    backend_id: str
    provenance_class: str
    current_reproducible: bool
    non_synthetic: bool
    capacity_verified: bool
    policy_evidence_current: bool
    credentials_authorized: bool = False
    spend_authorized: bool = False
    infrastructure_authorized: bool = False
    evidence_note: str = ""
    source_class: str = "planning_reference"
    source_artifact_id: str = ""
    source_artifact_sha256: str = ""
    observed_at_utc: str = ""
    credentials_authorization_origin: str = ""
    credentials_authorization_ref: str = ""
    spend_authorization_origin: str = ""
    spend_authorization_ref: str = ""
    infrastructure_authorization_origin: str = ""
    infrastructure_authorization_ref: str = ""

@dataclass(frozen=True)
class PortfolioQuote:
    backend_id: str
    family: str
    ai_backend: bool
    base_quote: BackendQuote
    production_blockers: tuple[str, ...]

@dataclass(frozen=True)
class PortfolioDecision:
    task_id: str
    task_kind: str
    state: str
    selected_backend_id: Optional[str]
    escalation_stage: str
    quotes: tuple[PortfolioQuote, ...]
    production_execution_enabled: bool = False
    value_movement_enabled: bool = False

def _require_bool(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{field}_must_be_boolean")
    return value

def _validate_backend_controls(backend: ExecutionBackend) -> None:
    for field in ("programmatic_access","policy_allowed","currently_available","requires_credentials","requires_paid_account","requires_new_spend","sunk_or_already_committed"):
        _require_bool(getattr(backend, field), field=f"backend_{field}")

def _valid_utc_timestamp(value: str) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        dt = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return dt.tzinfo is not None and dt.utcoffset() == timezone.utc.utcoffset(dt)

def _validate_authorization_binding(enabled: bool, origin: str, ref: str, *, field: str) -> None:
    if not enabled:
        return
    if origin not in AUTHORIZATION_ORIGINS:
        raise ValueError(f"{field}_authorization_origin_invalid")
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError(f"{field}_authorization_ref_required")

def _validate_evidence(item: BackendEvidence) -> None:
    if not isinstance(item.backend_id, str) or not item.backend_id.strip():
        raise ValueError("backend_evidence_id_required")
    if not isinstance(item.provenance_class, str) or not item.provenance_class.strip():
        raise ValueError("backend_evidence_provenance_class_required")
    for field in ("current_reproducible","non_synthetic","capacity_verified","policy_evidence_current","credentials_authorized","spend_authorized","infrastructure_authorized"):
        _require_bool(getattr(item, field), field=f"evidence_{field}")
    if item.source_class not in KNOWN_SOURCE_CLASSES:
        raise ValueError("backend_evidence_source_class_invalid")
    if item.provenance_class == MEASURED:
        if not isinstance(item.source_artifact_id, str) or not item.source_artifact_id.strip():
            raise ValueError("backend_evidence_source_artifact_id_required")
        if not isinstance(item.source_artifact_sha256, str) or not SHA256_RE.fullmatch(item.source_artifact_sha256):
            raise ValueError("backend_evidence_source_artifact_sha256_invalid")
        if not _valid_utc_timestamp(item.observed_at_utc):
            raise ValueError("backend_evidence_observed_at_utc_invalid")
    _validate_authorization_binding(item.credentials_authorized, item.credentials_authorization_origin, item.credentials_authorization_ref, field="credentials")
    _validate_authorization_binding(item.spend_authorized, item.spend_authorization_origin, item.spend_authorization_ref, field="spend")
    _validate_authorization_binding(item.infrastructure_authorized, item.infrastructure_authorization_origin, item.infrastructure_authorization_ref, field="infrastructure")

def _evidence_map(items: Iterable[BackendEvidence]) -> dict[str, BackendEvidence]:
    result = {}
    for item in items:
        _validate_evidence(item)
        if item.backend_id in result:
            raise ValueError(f"duplicate backend evidence: {item.backend_id}")
        result[item.backend_id] = item
    return result

def production_blockers(backend: ExecutionBackend, evidence: Optional[BackendEvidence]) -> tuple[str, ...]:
    _validate_backend_controls(backend)
    if evidence is not None:
        _validate_evidence(evidence)
    blockers = []
    if backend.automation_role != "autonomous" or not backend.programmatic_access: blockers.append("no_autonomous_programmatic_path")
    if not backend.policy_allowed: blockers.append("backend_policy_not_allowed")
    if not backend.currently_available: blockers.append("backend_not_currently_available")
    if backend.max_parallelism < 1: blockers.append("no_parallel_capacity")
    if backend.quota_units_remaining is not None and backend.quota_units_remaining < backend.units_per_task: blockers.append("quota_insufficient")
    if backend.allocated_fixed_cost_per_task_usd() is None: blockers.append("fixed_cost_allocation_basis_unknown")
    if evidence is None:
        blockers.append("backend_evidence_missing")
    else:
        if evidence.backend_id != backend.backend_id: blockers.append("backend_evidence_identity_mismatch")
        if evidence.provenance_class != MEASURED: blockers.append("backend_not_measured_reproducible")
        if evidence.provenance_class == MEASURED and evidence.source_class not in PROMOTABLE_SOURCE_CLASSES: blockers.append("backend_evidence_origin_not_promotable")
        if not evidence.current_reproducible: blockers.append("backend_evidence_not_current_reproducible")
        if not evidence.non_synthetic: blockers.append("backend_evidence_synthetic")
        if not evidence.capacity_verified: blockers.append("backend_capacity_not_verified")
        if not evidence.policy_evidence_current: blockers.append("backend_policy_evidence_not_current")
        if backend.requires_credentials and not evidence.credentials_authorized: blockers.append("credentials_not_authorized")
        if backend.requires_new_spend and not evidence.spend_authorized: blockers.append("new_spend_not_authorized")
        if backend.family == "paid_vps_server" and not evidence.infrastructure_authorized: blockers.append("infrastructure_not_authorized")
    return tuple(dict.fromkeys(blockers))

def portfolio_quotes(task, backends, evidence):
    evidence_by_id = _evidence_map(evidence); seen=set(); result=[]
    for backend in tuple(backends):
        _validate_backend_controls(backend)
        if not isinstance(backend.backend_id, str) or not backend.backend_id.strip(): raise ValueError("backend_id_required")
        if backend.backend_id in seen: raise ValueError(f"duplicate backend: {backend.backend_id}")
        seen.add(backend.backend_id)
        result.append(PortfolioQuote(backend.backend_id, backend.family, backend.family in AI_FAMILIES, quote_backend(task, backend), production_blockers(backend, evidence_by_id.get(backend.backend_id))))
    return tuple(result)

def _eligible(quotes, *, ai):
    _require_bool(ai, field="eligible_ai")
    return [q for q in quotes if q.ai_backend is ai and not q.base_quote.planning_reasons and not q.production_blockers]

def _cheapest(quotes):
    return sorted(quotes, key=lambda q:(q.base_quote.marginal_cost_usd,-q.base_quote.expected_margin_before_fixed_allocation_usd,-q.base_quote.success_probability,q.base_quote.latency_seconds,q.backend_id))[0]

def route_portfolio(task, backends, evidence, *, task_kind="paid_task", ai_allowed=True):
    if task_kind not in {"paid_task","observation"}: raise ValueError("task_kind must be paid_task or observation")
    _require_bool(ai_allowed, field="ai_allowed")
    quotes=portfolio_quotes(task, backends, evidence)
    deterministic=_eligible(quotes, ai=False)
    if deterministic:
        s=_cheapest(deterministic); return PortfolioDecision(task.task_id,task_kind,"production_route_ready",s.backend_id,"deterministic_first",quotes)
    if ai_allowed:
        aq=_eligible(quotes, ai=True)
        if aq:
            s=_cheapest(aq); return PortfolioDecision(task.task_id,task_kind,"production_route_ready",s.backend_id,"ai_only_after_deterministic_paths_fail_acceptance_or_materialization",quotes)
    planning=[q for q in quotes if not q.base_quote.planning_reasons]
    return PortfolioDecision(task.task_id,task_kind,"hold",None,"planning_candidates_exist_but_no_current_production_materialization" if planning else "no_backend_meets_task_acceptance_and_economics",quotes)

def current_backend_evidence():
    notes={"python_local":"Preferred deterministic no-spend family; exact executable current-checkout measurement is absent.","local_model":"Local CPU/GPU/model hardware, energy, quality and availability are unmeasured.","subscription_assistant":"Fixed/sunk limited support only; no autonomous programmatic API is assumed.","cheap_external_api":"No current vendor/credential/pricing/spend authorization materialization.","strong_external_api":"No current vendor/credential/pricing/spend authorization materialization.","free_tier_ci":"Manual GitHub-hosted runtime path exists, but current connector exposes no workflow_dispatch.","owned_pc":"Owned-PC power/capacity/reliability/quality evidence is not materialized.","future_paid_vps":"Future paid infrastructure requires separate authorization and spend."}
    return tuple(BackendEvidence(backend_id=b.backend_id,provenance_class="planning_reference",current_reproducible=False,non_synthetic=False,capacity_verified=False,policy_evidence_current=False,evidence_note=notes[b.backend_id],source_class="planning_reference") for b in default_backend_families())

def current_snapshot():
    backends=default_backend_families(); evidence=current_backend_evidence()
    paid=TaskEconomics(task_id="synthetic_paid_probe",required_capabilities=frozenset({"extract","validate"}),gross_payout_usd=1.0,platform_fee_rate=0.05,dispute_probability=0.05,nonpayment_probability=0.05,acceptance_probability=0.80,minimum_success_probability=0.90,minimum_expected_margin_usd=0.10,minimum_expected_margin_ratio=0.10)
    obs=TaskEconomics(task_id="synthetic_observation_value_probe",required_capabilities=frozenset({"extract","validate"}),gross_payout_usd=0.10,minimum_success_probability=0.90,minimum_expected_margin_usd=0.01,minimum_expected_margin_ratio=0.05)
    decisions=(route_portfolio(paid,backends,evidence,task_kind="paid_task"),route_portfolio(obs,backends,evidence,task_kind="observation",ai_allowed=False))
    return {"schema":"mining-autonomy/i123-execution-backend-portfolio/v2","run":"I123","artifact_class":"planning_reference","synthetic_fixture":True,"production_route_created":False,"authorization_created":False,"network_observation_performed":False,"credentials_used":False,"paid_infrastructure_created":False,"spend_or_value_movement":False,"routing_rule":"deterministic_first_then_ai_only_if_needed_then_cheapest_qualifying_positive_margin","fixed_vs_marginal_rule":"fixed/sunk cost remains separate; full monthly subscription cost is not charged to each task and finite capacity/opportunity cost is not treated as free","task_kind_separation":"observation economics never prove paid-task fulfillment economics","origin_binding_rule":"measured_reproducible requires promotable source class + artifact id + sha256 + explicit UTC observation time; sensitive authorization requires separate explicit_user_authorization reference","backend_evidence":[asdict(x) for x in evidence],"decisions":[asdict(x) for x in decisions],"current_route_summary":{"eligible_non_synthetic_route_exists":False,"reason":"No backend has current source-bound measured_reproducible non-synthetic evidence in the current checkpoint."}}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",default=str(Path(__file__).with_name("I123_EXECUTION_BACKEND_PORTFOLIO.json"))); a=p.parse_args(); payload=current_snapshot(); text=json.dumps(payload,indent=2,sort_keys=True)+"\n"; Path(a.output).write_text(text,encoding="utf-8"); print(text,end=""); return 0

if __name__ == "__main__": raise SystemExit(main())
