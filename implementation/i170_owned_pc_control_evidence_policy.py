#!/usr/bin/env python3
"""I170 source-policy contract for the seven unresolved owned-PC I050 controls.

I168/I169 expose a structural distinction that the earlier route hid: some remaining
I050 fields describe the exact local execution interface and can in principle be
reproduced from source/system evidence; two fields are owner/accounting classifications
and cannot honestly be turned into machine measurements.

I170 codifies that boundary without changing I050 or I123. It therefore cannot promote
an owned-PC backend. Its purpose is to prevent either of two bad shortcuts:
1) copying synthetic Router defaults into I050; or
2) relabelling owner/accounting declarations as measured/system-probe evidence.

No network, credentials, CI dispatch, account creation, paid infrastructure, task
action, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

SCHEMA = "mining-autonomy/i170-owned-pc-control-evidence-policy/v1"

CONTROL_PARAMETERS = (
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
    "quota_units_remaining",
    "rate_limit_per_minute",
)

INTERFACE_REPRODUCIBLE_PARAMETERS = (
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "quota_units_remaining",
    "rate_limit_per_minute",
)

OWNER_ACCOUNTING_PARAMETERS = (
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
)

REPRODUCIBLE_SOURCE_KINDS = {"provider_first_party", "measured_local", "system_probe"}


@dataclass(frozen=True)
class Requirement:
    parameter: str
    evidence_class: str
    accepted_source_kinds: tuple[str, ...]
    acquisition_contract: str
    forbidden_shortcut: str


@dataclass(frozen=True)
class PolicyResult:
    state: str
    errors: tuple[str, ...]
    reproducible_interface_parameters: tuple[str, ...]
    owner_accounting_parameters: tuple[str, ...]
    strict_i123_measured_reproducible_possible_without_policy_change: bool
    narrow_hybrid_policy_review_required: bool
    i050_change_performed: bool = False
    i123_change_performed: bool = False
    i123_promotion_allowed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False


def requirements() -> tuple[Requirement, ...]:
    return (
        Requirement(
            "requires_credentials",
            "exact_interface_reproducible",
            ("system_probe", "provider_first_party", "measured_local"),
            "Bind the exact owned-PC execution interface/source closure and demonstrate that the production executor has no credential dependency or credential-consuming path.",
            "A benchmark that merely happened not to use credentials is insufficient if the production executor differs.",
        ),
        Requirement(
            "requires_paid_account",
            "exact_interface_reproducible",
            ("system_probe", "provider_first_party", "measured_local"),
            "Bind the exact local executor and demonstrate that execution does not depend on a remote provider account or paid service entitlement.",
            "Do not infer false only from the absence of a login prompt during one test.",
        ),
        Requirement(
            "requires_new_spend",
            "exact_interface_reproducible",
            ("system_probe", "measured_local", "provider_first_party"),
            "Prove the bound executor requires no purchase, paid API, rental, paid install or new infrastructure action; measured electricity remains a separate marginal-cost field.",
            "Do not use ownership alone to hide a paid dependency or future purchase requirement.",
        ),
        Requirement(
            "fixed_monthly_cost_usd",
            "owner_accounting_declaration",
            ("user_declared", "provider_first_party"),
            "Record the actual recurring fixed cost attributable to this already-owned execution resource with an owner/accounting source reference; zero must be explicit, not inferred.",
            "Do not relabel an owner accounting statement as system_probe/measured_local just to satisfy I123.",
        ),
        Requirement(
            "sunk_or_already_committed",
            "owner_accounting_declaration",
            ("user_declared", "provider_first_party"),
            "Record whether the relevant fixed cost is already committed/sunk for the decision horizon, with explicit owner/accounting provenance.",
            "Machine ownership/availability does not by itself prove the accounting classification used for economics.",
        ),
        Requirement(
            "quota_units_remaining",
            "exact_interface_semantics",
            ("system_probe", "provider_first_party", "measured_local"),
            "For a purely local executor, bind a source/system proof that no external provider quota primitive applies; None means not applicable, never unlimited host capacity.",
            "Do not copy synthetic Router quota values or interpret None as infinite compute.",
        ),
        Requirement(
            "rate_limit_per_minute",
            "exact_interface_semantics",
            ("system_probe", "provider_first_party", "measured_local"),
            "For a purely local executor, bind a source/system proof that no external provider rate-limit primitive applies; host throughput remains measured separately.",
            "Do not convert measured parallelism/throughput into a provider rate-limit claim.",
        ),
    )


def evaluate_source_plan(source_kinds: Mapping[str, str]) -> PolicyResult:
    errors: list[str] = []
    expected = {item.parameter: item for item in requirements()}
    unknown = sorted(set(source_kinds) - set(expected))
    if unknown:
        errors.append("unknown_control_parameters:" + ",".join(unknown))

    for parameter in CONTROL_PARAMETERS:
        kind = source_kinds.get(parameter)
        if kind is None:
            errors.append(f"missing_source_plan:{parameter}")
            continue
        req = expected[parameter]
        if kind not in req.accepted_source_kinds:
            errors.append(f"source_kind_not_allowed:{parameter}:{kind}")

    interface_reproducible = all(
        source_kinds.get(parameter) in REPRODUCIBLE_SOURCE_KINDS
        for parameter in INTERFACE_REPRODUCIBLE_PARAMETERS
    )
    accounting_declared = all(
        source_kinds.get(parameter) in {"user_declared", "provider_first_party"}
        for parameter in OWNER_ACCOUNTING_PARAMETERS
    )
    contains_user_accounting = any(
        source_kinds.get(parameter) == "user_declared"
        for parameter in OWNER_ACCOUNTING_PARAMETERS
    )

    errors = sorted(set(errors))
    if errors:
        state = "PASS_BLOCKED"
    elif interface_reproducible and accounting_declared and contains_user_accounting:
        state = "HYBRID_ACCOUNTING_POLICY_REVIEW_REQUIRED"
    elif interface_reproducible and accounting_declared:
        state = "SOURCE_PLAN_COMPLETE"
    else:
        state = "PASS_BLOCKED"

    # Under current I050/I123 semantics, any user_declared record makes the I050
    # attestation declared rather than calibrated_reproducible. I170 records that
    # fact; it does not change the downstream acceptance rule.
    strict_possible = bool(
        not errors
        and interface_reproducible
        and all(source_kinds.get(p) in REPRODUCIBLE_SOURCE_KINDS for p in OWNER_ACCOUNTING_PARAMETERS)
    )
    hybrid_review = bool(not errors and contains_user_accounting)

    return PolicyResult(
        state=state,
        errors=tuple(errors),
        reproducible_interface_parameters=INTERFACE_REPRODUCIBLE_PARAMETERS,
        owner_accounting_parameters=OWNER_ACCOUNTING_PARAMETERS,
        strict_i123_measured_reproducible_possible_without_policy_change=strict_possible,
        narrow_hybrid_policy_review_required=hybrid_review,
    )


def payload(result: PolicyResult) -> dict[str, Any]:
    return {
        **asdict(result),
        "schema": SCHEMA,
        "run": "I170",
        "requirements": [asdict(item) for item in requirements()],
        "next_gate": (
            "Acquire exact-interface reproducible evidence for the five interface parameters and explicit "
            "owner/accounting provenance for fixed_monthly_cost_usd and sunk_or_already_committed. If either "
            "accounting fact must remain user_declared, review a narrowly scoped owned-PC hybrid evidence "
            "policy instead of falsifying the I050 source class. I170 itself changes no production gate."
        ),
    }
