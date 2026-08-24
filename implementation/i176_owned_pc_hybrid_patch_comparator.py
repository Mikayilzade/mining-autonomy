#!/usr/bin/env python3
"""I176 review-only comparator for a minimal owned_pc hybrid I050/I123 policy patch.

Nothing is patched here. The module compares current strict semantics with the narrow
I172 proposal and answers only: would a hypothetical owned_pc-only accounting exception
accept a bundle that current strict I050/I123 rejects solely because the two intrinsic
owner/accounting facts are user_declared?

The hypothetical exception is deliberately incapable of widening backend identity,
declaration scope, non-synthetic/current/capacity/policy requirements, or any credential,
spend/infrastructure authorization gate. Actual I050/I123 source remains unchanged.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

SCHEMA = "mining-autonomy/i176-owned-pc-hybrid-patch-comparator/v1"
I050_BLOB_SHA = "9b76a2194d15f8277d15b2e46c85df71cca08874"
I123_BLOB_SHA = "a3b7878b9114d3059784a4d3a0d6d6f55fa9fe3c"
I172_BLOB_SHA = "a61828d1d680d9f6ba25fa772573e68673eabfeb"
OWNED_PC = "owned_pc"
ACCOUNTING_PARAMETERS = frozenset({"fixed_monthly_cost_usd", "sunk_or_already_committed"})
CRITICAL_PARAMETERS = (
    "currently_available",
    "programmatic_access",
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
    "quota_units_remaining",
    "electricity_per_task_usd",
    "latency_seconds",
    "reliability_probability",
    "quality_probability",
    "max_parallelism",
    "rate_limit_per_minute",
)
REPRODUCIBLE_SOURCE_KINDS = frozenset({"provider_first_party", "measured_local", "system_probe"})
PROPOSED_CLASS = "owned_pc_hybrid_accounting_declared_v1"


@dataclass(frozen=True)
class Candidate:
    backend_id: str
    backend_family: str
    i050_attestation_state: str
    source_kinds: Mapping[str, str]
    i172_state: str | None
    i172_review_contract_digest: str | None
    non_synthetic: bool
    capacity_verified: bool
    policy_evidence_current: bool
    backend_requires_credentials: bool = False
    backend_requires_new_spend: bool = False
    backend_requires_paid_account: bool = False
    credentials_authorized: bool = False
    spend_authorized: bool = False
    infrastructure_authorized: bool = False


@dataclass(frozen=True)
class ComparisonResult:
    state: str
    errors: tuple[str, ...]
    strict_current_path_ready: bool
    narrow_hybrid_shape_valid: bool
    would_be_eligible_under_proposal: bool
    proposed_provenance_class: str | None
    declaration_parameters: tuple[str, ...]
    preserved_blockers: tuple[str, ...]
    widens_non_owned_pc: bool
    widens_declaration_scope: bool
    bypasses_authorization: bool
    i050_change_performed: bool = False
    i123_change_performed: bool = False
    policy_patch_applied: bool = False
    i123_promotion_performed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False


def compare(candidate: Candidate) -> ComparisonResult:
    errors: list[str] = []
    sources = dict(candidate.source_kinds)
    if set(sources) != set(CRITICAL_PARAMETERS) or len(sources) != len(CRITICAL_PARAMETERS):
        errors.append("complete_critical_source_map_required")

    declarations = tuple(sorted(name for name, kind in sources.items() if kind == "user_declared"))
    illegal_declarations = tuple(name for name in declarations if name not in ACCOUNTING_PARAMETERS)
    unknown_sources = tuple(sorted(
        name for name, kind in sources.items()
        if kind not in REPRODUCIBLE_SOURCE_KINDS and kind != "user_declared"
    ))
    if illegal_declarations:
        errors.extend(f"declaration_outside_accounting_scope:{name}" for name in illegal_declarations)
    if unknown_sources:
        errors.extend(f"unsupported_source_kind:{name}" for name in unknown_sources)

    strict_reproducible = bool(
        not errors
        and candidate.i050_attestation_state == "calibrated_reproducible"
        and all(kind in REPRODUCIBLE_SOURCE_KINDS for kind in sources.values())
    )

    non_accounting_reproducible = all(
        sources.get(name) in REPRODUCIBLE_SOURCE_KINDS
        for name in CRITICAL_PARAMETERS
        if name not in ACCOUNTING_PARAMETERS
    )
    accounting_valid = all(
        sources.get(name) in (REPRODUCIBLE_SOURCE_KINDS | {"user_declared"})
        for name in ACCOUNTING_PARAMETERS
    )
    declaration_scope_narrow = not illegal_declarations and set(declarations).issubset(ACCOUNTING_PARAMETERS)
    hybrid_review_bound = bool(
        candidate.i172_state == "NARROW_HYBRID_REVIEW_READY"
        and isinstance(candidate.i172_review_contract_digest, str)
        and len(candidate.i172_review_contract_digest) == 64
    )
    owned_pc_only = candidate.backend_id == OWNED_PC and candidate.backend_family == OWNED_PC
    hybrid_shape = bool(
        not errors
        and owned_pc_only
        and candidate.i050_attestation_state == "calibrated_declared"
        and declarations
        and declaration_scope_narrow
        and non_accounting_reproducible
        and accounting_valid
        and hybrid_review_bound
    )

    preserved: list[str] = []
    if not candidate.non_synthetic:
        preserved.append("backend_evidence_synthetic")
    if not candidate.capacity_verified:
        preserved.append("backend_capacity_not_verified")
    if not candidate.policy_evidence_current:
        preserved.append("backend_policy_evidence_not_current")
    if candidate.backend_requires_credentials and not candidate.credentials_authorized:
        preserved.append("credentials_not_authorized")
    if candidate.backend_requires_paid_account and not candidate.credentials_authorized:
        preserved.append("paid_account_not_authorized")
    if candidate.backend_requires_new_spend and not candidate.spend_authorized:
        preserved.append("new_spend_not_authorized")
    if candidate.backend_family == "paid_vps_server" and not candidate.infrastructure_authorized:
        preserved.append("infrastructure_not_authorized")

    proposal_ready = bool(
        hybrid_shape
        and candidate.non_synthetic
        and candidate.capacity_verified
        and candidate.policy_evidence_current
        and not preserved
    )

    if strict_reproducible:
        state = "STRICT_PATH_UNCHANGED"
    elif proposal_ready:
        state = "NARROW_HYBRID_WOULD_BE_ELIGIBLE_IF_PATCH_APPROVED"
    elif errors or not hybrid_shape:
        state = "PASS_BLOCKED"
    else:
        state = "HYBRID_SHAPE_VALID_BUT_EXISTING_GATE_BLOCKS"

    return ComparisonResult(
        state=state,
        errors=tuple(sorted(set(errors))),
        strict_current_path_ready=strict_reproducible,
        narrow_hybrid_shape_valid=hybrid_shape,
        would_be_eligible_under_proposal=proposal_ready,
        proposed_provenance_class=PROPOSED_CLASS if hybrid_shape else None,
        declaration_parameters=declarations,
        preserved_blockers=tuple(dict.fromkeys(preserved)),
        widens_non_owned_pc=False,
        widens_declaration_scope=False,
        bypasses_authorization=False,
    )


def payload(result: ComparisonResult) -> dict[str, Any]:
    return {
        **asdict(result),
        "schema": SCHEMA,
        "run": "I176",
        "bound_current_sources": {
            "i050_blob_sha": I050_BLOB_SHA,
            "i123_blob_sha": I123_BLOB_SHA,
            "i172_blob_sha": I172_BLOB_SHA,
        },
        "proposal_boundary": {
            "backend_id": OWNED_PC,
            "declarations_allowed_only_for": sorted(ACCOUNTING_PARAMETERS),
            "all_other_parameters_reproducible": True,
            "non_synthetic_required": True,
            "capacity_verified_required": True,
            "policy_evidence_current_required": True,
            "authorization_gates_unchanged": True,
            "review_only": True,
        },
        "next_gate": (
            "Do not apply the proposed class now. First materialize real I166/I168 evidence and truthful accounting "
            "facts. Apply no I050/I123 source change unless the real path reaches exactly this two-accounting-field "
            "boundary; then rebind to current source blobs and rerun non-widening regression tests."
        ),
    }
