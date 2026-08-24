#!/usr/bin/env python3
"""I177 fail-closed assembly of future real owned-PC evidence for I169.

I177 joins three already-existing evidence lanes without inventing any fact:
1. I168: seven measured/resource parameters from a future real I166/I167 packet;
2. I175: five exact production-executor interface controls bound through I171;
3. caller-supplied accounting evidence for fixed_monthly_cost_usd and
   sunk_or_already_committed.

It converts only the seven controls into the current I169 ControlEvidence shape and
immediately evaluates current I169 readiness. It never executes I050/I066/I123 and
cannot turn placeholder, fixture, synthetic, or missing accounting provenance into
real evidence. `user_declared` accounting evidence remains declared and therefore
cannot reach current strict I123 measured_reproducible semantics.

No network, credentials, CI dispatch, account creation, paid infrastructure, task
acceptance/submission, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

import i169_owned_pc_i050_i066_readiness as i169

SCHEMA = "mining-autonomy/i177-owned-pc-evidence-assembly/v1"
INTERFACE_PARAMETERS = (
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "quota_units_remaining",
    "rate_limit_per_minute",
)
ACCOUNTING_PARAMETERS = (
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
)
FORBIDDEN_PROVENANCE_MARKERS = (
    "test-fixture", "fixture", "example", "synthetic", "placeholder", "dummy", "mock",
)


@dataclass(frozen=True)
class AccountingEvidenceInput:
    parameter: str
    value: Any
    source_kind: str
    source_ref: str
    observed_at: str
    max_age_seconds: int
    source_content_digest: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class AssemblyResult:
    state: str
    errors: tuple[str, ...]
    backend_id: str
    control_records: tuple[i169.ControlEvidence, ...]
    i169_result: dict[str, Any] | None
    strict_i050_execution_ready: bool
    declared_accounting_boundary_reached: bool
    i050_executed: bool = False
    i066_executed: bool = False
    i123_promotion_performed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _real_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    low = value.strip().lower()
    return not any(marker in low for marker in FORBIDDEN_PROVENANCE_MARKERS)


def _mapping_rows(raw: Any) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(raw, (list, tuple)):
        return ()
    return tuple(row for row in raw if isinstance(row, Mapping))


def assemble_for_i169(
    i168_result: Mapping[str, Any],
    i175_result: Mapping[str, Any],
    accounting_inputs: tuple[AccountingEvidenceInput, ...],
    *,
    observed_at: str,
    interface_max_age_seconds: int = 86400,
) -> AssemblyResult:
    errors: list[str] = []

    if i168_result.get("state") != "PARTIAL_I050_EVIDENCE_READY":
        errors.append("i168_partial_i050_evidence_required")
    if i168_result.get("backend_id") != "owned_pc":
        errors.append("i168_owned_pc_required")
    if i168_result.get("i166_i167_source_binding_valid") is not True:
        errors.append("i168_real_source_binding_required")
    if tuple(i168_result.get("emitted_parameters") or ()) != i169.MEASURED_PARAMETERS:
        errors.append("i168_measured_parameter_set_drift")
    if i168_result.get("i050_source_blob_sha") != i169.I050_RESOURCE_PROFILE_BLOB_SHA:
        errors.append("i168_i050_source_binding_drift")
    if i168_result.get("i066_source_blob_sha") != i169.I066_MATERIALIZATION_BLOB_SHA:
        errors.append("i168_i066_source_binding_drift")

    reference_hash = i168_result.get("reference_backend_hash")
    if not isinstance(reference_hash, str) or len(reference_hash) < 16:
        errors.append("i168_reference_backend_hash_required")

    if i175_result.get("state") != "PRODUCTION_INTERFACE_CONTROLS_READY":
        errors.append("i175_production_interface_controls_required")
    if i175_result.get("production_executor_scope_bound") is not True:
        errors.append("i175_production_executor_scope_not_bound")
    if i175_result.get("i050_records_created") is not False:
        errors.append("i175_unexpected_i050_side_effect")
    if i175_result.get("i123_promotion_allowed") is not False:
        errors.append("i175_unexpected_i123_promotion")

    interface_rows = _mapping_rows(i175_result.get("interface_facts"))
    interface_by_parameter: dict[str, Mapping[str, Any]] = {}
    for row in interface_rows:
        parameter = row.get("parameter")
        if parameter not in INTERFACE_PARAMETERS:
            errors.append(f"unexpected_i175_interface_parameter:{parameter}")
            continue
        if parameter in interface_by_parameter:
            errors.append(f"duplicate_i175_interface_parameter:{parameter}")
            continue
        interface_by_parameter[str(parameter)] = row
        if row.get("source_kind") != "system_probe":
            errors.append(f"i175_interface_not_system_probe:{parameter}")
        if not _real_ref(row.get("source_ref")):
            errors.append(f"i175_interface_source_ref_invalid:{parameter}")
        digest = row.get("source_content_digest")
        if not isinstance(digest, str) or len(digest) < 16:
            errors.append(f"i175_interface_source_digest_invalid:{parameter}")

    for parameter in INTERFACE_PARAMETERS:
        if parameter not in interface_by_parameter:
            errors.append(f"missing_i175_interface_parameter:{parameter}")

    accounting_by_parameter: dict[str, AccountingEvidenceInput] = {}
    for row in accounting_inputs:
        if row.parameter not in ACCOUNTING_PARAMETERS:
            errors.append(f"unexpected_accounting_parameter:{row.parameter}")
            continue
        if row.parameter in accounting_by_parameter:
            errors.append(f"duplicate_accounting_parameter:{row.parameter}")
            continue
        accounting_by_parameter[row.parameter] = row
        if row.source_kind not in i169.ALLOWED_CONTROL_SOURCE_KINDS:
            errors.append(f"unsupported_accounting_source_kind:{row.parameter}")
        if not _real_ref(row.source_ref):
            errors.append(f"accounting_source_ref_invalid:{row.parameter}")
        if row.source_kind in i169.REPRODUCIBLE_SOURCE_KINDS:
            if not isinstance(row.source_content_digest, str) or len(row.source_content_digest) < 16:
                errors.append(f"accounting_reproducible_digest_required:{row.parameter}")
        if row.max_age_seconds <= 0:
            errors.append(f"accounting_positive_max_age_required:{row.parameter}")

    for parameter in ACCOUNTING_PARAMETERS:
        if parameter not in accounting_by_parameter:
            errors.append(f"missing_accounting_parameter:{parameter}")

    try:
        i169._parse_utc(observed_at)
    except Exception:
        errors.append("interface_observed_at_must_be_utc")
    if interface_max_age_seconds <= 0:
        errors.append("interface_positive_max_age_required")

    errors = sorted(set(errors))
    if errors or not isinstance(reference_hash, str):
        return AssemblyResult(
            state="PASS_BLOCKED",
            errors=tuple(errors),
            backend_id="owned_pc",
            control_records=(),
            i169_result=None,
            strict_i050_execution_ready=False,
            declared_accounting_boundary_reached=False,
        )

    controls: list[i169.ControlEvidence] = []
    for parameter in INTERFACE_PARAMETERS:
        row = interface_by_parameter[parameter]
        controls.append(i169.build_control_evidence(
            parameter=parameter,
            value=row.get("value"),
            source_kind="system_probe",
            source_ref=str(row["source_ref"]),
            observed_at=observed_at,
            max_age_seconds=interface_max_age_seconds,
            reference_backend_hash=reference_hash,
            source_content_digest=str(row["source_content_digest"]),
            notes="I177 projection of exact I175/I171 production-executor interface proof.",
        ))

    for parameter in ACCOUNTING_PARAMETERS:
        row = accounting_by_parameter[parameter]
        controls.append(i169.build_control_evidence(
            parameter=parameter,
            value=row.value,
            source_kind=row.source_kind,
            source_ref=row.source_ref,
            observed_at=row.observed_at,
            max_age_seconds=row.max_age_seconds,
            reference_backend_hash=reference_hash,
            source_content_digest=row.source_content_digest,
            notes=row.notes or "I177 explicit owned-PC accounting evidence; never inferred from machine state.",
        ))

    readiness = i169.evaluate_readiness(i168_result, tuple(controls))
    readiness_dict = asdict(readiness)
    strict_ready = readiness.state == "READY_FOR_EXACT_I050_EXECUTION" and readiness.exact_i050_execution_allowed
    declared_boundary = readiness.state == "COMPLETE_DECLARED_BUNDLE_BLOCKED_FOR_I123"

    if strict_ready:
        state = "ASSEMBLED_READY_FOR_EXACT_I050"
    elif declared_boundary:
        state = "ASSEMBLED_DECLARED_ACCOUNTING_BOUNDARY"
    else:
        state = "PASS_BLOCKED"

    return AssemblyResult(
        state=state,
        errors=tuple(readiness.errors),
        backend_id="owned_pc",
        control_records=tuple(controls),
        i169_result=readiness_dict,
        strict_i050_execution_ready=strict_ready,
        declared_accounting_boundary_reached=declared_boundary,
    )


def payload(result: AssemblyResult) -> dict[str, Any]:
    body = asdict(result)
    body["control_records"] = [asdict(row) for row in result.control_records]
    body.update({
        "schema": SCHEMA,
        "run": "I177",
        "next_gate": (
            "Do not run I050 from synthetic fixtures. With a future genuine I168 result, exact executed I175 proof, "
            "and truthful accounting provenance, I177 may reach either strict I050 readiness or the exact two-field "
            "declared-accounting boundary. I050/I066/I123 remain separate subsequent gates."
        ),
    })
    return body
