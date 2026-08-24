#!/usr/bin/env python3
"""I172 review-only narrow hybrid evidence contract for owned_pc.

Current I050 classifies any user-declared fact as calibrated_declared, while I123's
production gate requires measured_reproducible evidence. I170 showed that exactly two
remaining owned-PC facts are intrinsically owner/accounting classifications rather than
machine measurements: fixed_monthly_cost_usd and sunk_or_already_committed.

I172 defines the narrowest reviewable exception boundary without changing I050 or I123.
It permits user_declared provenance only for those two accounting facts, requires every
other resource/interface fact to remain reproducibly evidenced, applies only to owned_pc,
and explicitly cannot create credential/spend/infrastructure authorization or enable a
production route. This is a policy-design artifact, not an implemented gate widening.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

SCHEMA = "mining-autonomy/i172-owned-pc-hybrid-evidence-contract/v1"
OWNED_PC = "owned_pc"

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

ACCOUNTING_DECLARATION_PARAMETERS = (
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
)

REPRODUCIBLE_ONLY_PARAMETERS = tuple(
    parameter for parameter in CRITICAL_PARAMETERS
    if parameter not in ACCOUNTING_DECLARATION_PARAMETERS
)

REPRODUCIBLE_SOURCE_KINDS = frozenset({
    "provider_first_party",
    "measured_local",
    "system_probe",
})
ACCOUNTING_SOURCE_KINDS = REPRODUCIBLE_SOURCE_KINDS | {"user_declared"}


@dataclass(frozen=True)
class EvidenceRef:
    backend_id: str
    parameter: str
    source_kind: str
    source_ref: str
    source_content_digest: str | None


@dataclass(frozen=True)
class HybridReviewResult:
    state: str
    errors: tuple[str, ...]
    backend_id: str
    declaration_parameters: tuple[str, ...]
    reproducible_parameters: tuple[str, ...]
    complete_parameter_set: bool
    declaration_scope_narrow: bool
    all_non_accounting_reproducible: bool
    i050_change_performed: bool
    i123_change_performed: bool
    credentials_authorized: bool
    spend_authorized: bool
    infrastructure_authorized: bool
    i123_promotion_allowed: bool
    production_execution_enabled: bool
    review_contract_digest: str | None


def _digest_contract(rows: Iterable[EvidenceRef]) -> str:
    from hashlib import sha256
    import json
    body = [asdict(row) for row in sorted(rows, key=lambda row: row.parameter)]
    return sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def evaluate_hybrid_contract(
    backend_id: str,
    evidence_refs: Iterable[EvidenceRef],
    *,
    credentials_authorized: bool = False,
    spend_authorized: bool = False,
    infrastructure_authorized: bool = False,
) -> HybridReviewResult:
    errors: list[str] = []
    if backend_id != OWNED_PC:
        errors.append("hybrid_contract_owned_pc_only")

    rows = tuple(evidence_refs)
    by_parameter: dict[str, EvidenceRef] = {}
    for row in rows:
        if row.backend_id != OWNED_PC:
            errors.append(f"evidence_backend_not_owned_pc:{row.parameter}")
        if row.parameter not in CRITICAL_PARAMETERS:
            errors.append(f"unexpected_parameter:{row.parameter}")
            continue
        if row.parameter in by_parameter:
            errors.append(f"duplicate_parameter:{row.parameter}")
            continue
        by_parameter[row.parameter] = row
        if not isinstance(row.source_ref, str) or not row.source_ref.strip():
            errors.append(f"missing_source_ref:{row.parameter}")

        if row.parameter in ACCOUNTING_DECLARATION_PARAMETERS:
            if row.source_kind not in ACCOUNTING_SOURCE_KINDS:
                errors.append(f"unsupported_accounting_source:{row.parameter}:{row.source_kind}")
        else:
            if row.source_kind not in REPRODUCIBLE_SOURCE_KINDS:
                errors.append(f"non_accounting_must_be_reproducible:{row.parameter}:{row.source_kind}")

        if row.source_kind in REPRODUCIBLE_SOURCE_KINDS:
            if not row.source_content_digest or len(row.source_content_digest) < 16:
                errors.append(f"reproducible_digest_required:{row.parameter}")

    missing = [parameter for parameter in CRITICAL_PARAMETERS if parameter not in by_parameter]
    errors.extend(f"missing_parameter:{parameter}" for parameter in missing)

    declaration_parameters = tuple(
        parameter for parameter in ACCOUNTING_DECLARATION_PARAMETERS
        if parameter in by_parameter and by_parameter[parameter].source_kind == "user_declared"
    )
    illegal_declarations = tuple(
        parameter for parameter, row in by_parameter.items()
        if row.source_kind == "user_declared" and parameter not in ACCOUNTING_DECLARATION_PARAMETERS
    )
    if illegal_declarations:
        errors.extend(f"declaration_outside_accounting_scope:{parameter}" for parameter in illegal_declarations)

    complete = set(by_parameter) == set(CRITICAL_PARAMETERS) and len(by_parameter) == len(CRITICAL_PARAMETERS)
    all_non_accounting_reproducible = all(
        parameter in by_parameter and by_parameter[parameter].source_kind in REPRODUCIBLE_SOURCE_KINDS
        for parameter in REPRODUCIBLE_ONLY_PARAMETERS
    )
    narrow = not illegal_declarations and all(
        parameter in ACCOUNTING_DECLARATION_PARAMETERS for parameter in declaration_parameters
    )

    # Authorizations are intentionally not consumable by this review contract.
    if credentials_authorized:
        errors.append("hybrid_contract_cannot_consume_credentials_authorization")
    if spend_authorized:
        errors.append("hybrid_contract_cannot_consume_spend_authorization")
    if infrastructure_authorized:
        errors.append("hybrid_contract_cannot_consume_infrastructure_authorization")

    errors = sorted(set(errors))
    review_ready = not errors and complete and narrow and all_non_accounting_reproducible
    if review_ready and declaration_parameters:
        state = "NARROW_HYBRID_REVIEW_READY"
    elif review_ready:
        state = "STRICT_REPRODUCIBLE_PATH_AVAILABLE_NO_HYBRID_NEEDED"
    else:
        state = "PASS_BLOCKED"

    digest = _digest_contract(rows) if review_ready else None
    return HybridReviewResult(
        state=state,
        errors=tuple(errors),
        backend_id=backend_id,
        declaration_parameters=declaration_parameters,
        reproducible_parameters=REPRODUCIBLE_ONLY_PARAMETERS,
        complete_parameter_set=complete,
        declaration_scope_narrow=narrow,
        all_non_accounting_reproducible=all_non_accounting_reproducible,
        i050_change_performed=False,
        i123_change_performed=False,
        credentials_authorized=False,
        spend_authorized=False,
        infrastructure_authorized=False,
        i123_promotion_allowed=False,
        production_execution_enabled=False,
        review_contract_digest=digest,
    )


def payload(result: HybridReviewResult) -> dict[str, Any]:
    return {
        **asdict(result),
        "schema": SCHEMA,
        "run": "I172",
        "policy_boundary": {
            "backend_id": OWNED_PC,
            "user_declared_allowed_only_for": list(ACCOUNTING_DECLARATION_PARAMETERS),
            "reproducible_required_for": list(REPRODUCIBLE_ONLY_PARAMETERS),
            "cannot_create_authorization": True,
            "cannot_enable_i123": True,
            "review_only": True,
        },
        "next_gate": (
            "Keep I050/I123 unchanged. First build/bind the exact production-scoped deterministic executor "
            "through I171 and acquire real I166/I168 evidence. If the only remaining non-reproducible facts "
            "are the two accounting declarations, compare a minimal owned_pc-only policy patch against the "
            "strict path and prove by tests that no other backend/source/authorization gate can widen."
        ),
    }
