"""I134 evidence-acquisition planner for execution backends.

Ranks what to measure/verify next when a backend is not production-materialized.
It prefers no-new-spend, autonomous, programmatic paths and never treats support-only
subscriptions, paid APIs, CI free tiers, owned hardware or VPS as free/unlimited.
No external action is performed.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Iterable

from i123_execution_backend_portfolio import BackendEvidence, current_backend_evidence
from resource_router import ExecutionBackend, default_backend_families


@dataclass(frozen=True)
class AcquisitionStep:
    backend_id: str
    family: str
    priority_score: int
    state: str
    evidence_needed: tuple[str, ...]
    authorization_needed_before_execution: tuple[str, ...]
    disqualifiers: tuple[str, ...]
    no_new_spend_evidence_work_possible: bool


def _step(backend: ExecutionBackend, evidence: BackendEvidence) -> AcquisitionStep:
    needed=[]
    auth=[]
    disq=[]
    if backend.automation_role != "autonomous" or not backend.programmatic_access:
        disq.append("support_only_or_no_programmatic_execution")
    if not evidence.current_reproducible:
        needed.append("current_reproducible_backend_evidence")
    if not evidence.capacity_verified:
        needed.append("quota_capacity_parallelism_rate_limit_evidence")
    if not evidence.policy_evidence_current:
        needed.append("current_policy_tos_execution_permission_evidence")
    if not evidence.non_synthetic:
        needed.append("non_synthetic_cost_quality_reliability_evidence")
    if backend.backend_id == "python_local":
        needed.extend(("exact_current_runtime_receipt", "measured_energy_plus_explicit_tariff"))
    elif backend.backend_id == "local_model":
        needed.extend(("local_model_presence_and_interface", "model_quality_acceptance_benchmark", "host_energy_and_opportunity_cost"))
    elif backend.backend_id == "free_tier_ci":
        needed.extend(("provider_free_tier_policy", "remaining_quota_and_rate_limits", "source_bound_runtime_receipt"))
    elif backend.backend_id == "owned_pc":
        needed.extend(("owned_pc_availability", "energy_and_capacity_measurement", "quality_reliability_benchmark"))
    elif backend.backend_id == "subscription_assistant":
        disq.append("not_an_autonomous_api_backend")
    elif backend.backend_id in {"cheap_external_api", "strong_external_api"}:
        needed.extend(("current_vendor_pricing", "rate_limit_quota", "quality_reliability_benchmark"))
    elif backend.backend_id == "future_paid_vps":
        needed.extend(("current_vps_price_and_specs", "runtime_quality_capacity", "energy_included_or_external_cost_semantics"))

    if backend.requires_credentials:
        auth.append("credentials_authorization")
    if backend.requires_new_spend or backend.requires_paid_account:
        auth.append("spend_or_paid_account_authorization")
    if backend.family == "paid_vps_server":
        auth.append("infrastructure_rental_authorization")

    no_spend = not backend.requires_new_spend and not backend.requires_paid_account
    score=100
    if backend.automation_role != "autonomous" or not backend.programmatic_access: score += 100
    if backend.requires_new_spend: score += 50
    if backend.requires_paid_account: score += 30
    if backend.requires_credentials: score += 20
    if backend.backend_id == "python_local": score -= 60
    if backend.backend_id == "free_tier_ci": score -= 25
    if backend.backend_id == "local_model": score -= 15
    if backend.backend_id == "owned_pc": score -= 10
    state = "EVIDENCE_ACQUISITION_CANDIDATE" if not disq else "DEFER_OR_SUPPORT_ONLY"
    return AcquisitionStep(
        backend_id=backend.backend_id,
        family=backend.family,
        priority_score=score,
        state=state,
        evidence_needed=tuple(dict.fromkeys(needed)),
        authorization_needed_before_execution=tuple(dict.fromkeys(auth)),
        disqualifiers=tuple(dict.fromkeys(disq)),
        no_new_spend_evidence_work_possible=no_spend,
    )


def plan(
    backends: Iterable[ExecutionBackend] = (),
    evidence: Iterable[BackendEvidence] = (),
) -> tuple[AcquisitionStep, ...]:
    bs=tuple(backends) or default_backend_families()
    es=tuple(evidence) or current_backend_evidence()
    em={e.backend_id:e for e in es}
    rows=[]
    for b in bs:
        e=em.get(b.backend_id)
        if e is None:
            e=BackendEvidence(b.backend_id,"missing",False,False,False,False)
        rows.append(_step(b,e))
    return tuple(sorted(rows,key=lambda x:(x.priority_score,x.backend_id)))


def payload(rows: Iterable[AcquisitionStep]) -> dict:
    rows=tuple(rows)
    return {
        "schema":"mining-autonomy/i134-backend-evidence-acquisition-plan/v1",
        "run":"I134",
        "rows":[asdict(x) for x in rows],
        "next_backend_id":next((x.backend_id for x in rows if x.state=="EVIDENCE_ACQUISITION_CANDIDATE"),None),
        "execution_enabled":False,
        "network_enabled":False,
        "credentials_used":False,
        "spend_or_value_movement":False,
    }
