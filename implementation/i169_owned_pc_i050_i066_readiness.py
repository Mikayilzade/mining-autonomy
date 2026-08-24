#!/usr/bin/env python3
"""I169 fail-closed readiness gate before exact I050/I066 execution for owned_pc.

I168 intentionally emits only seven facts supported by real I166/I167 measurement.
I169 validates provenance-bound evidence for the seven remaining I050 control/accounting
parameters and determines whether the full 14-parameter bundle is eligible to be handed
to the *actual* I050 implementation. It does not execute or emulate I050/I066 and never
upgrades declarations into reproducible evidence.

A complete bundle containing any `user_declared` control fact is explicitly classified
as declared-only and therefore insufficient for I123's `measured_reproducible` gate.
Only source classes already considered reproducible by current I050 can reach
READY_FOR_EXACT_I050_EXECUTION here. Actual I050 and I066 still must run afterwards.

No network, credentials, CI dispatch, account creation, paid infrastructure, task
acceptance, spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

SCHEMA = "mining-autonomy/i169-owned-pc-i050-i066-readiness/v1"
I050_RESOURCE_PROFILE_BLOB_SHA = "9b76a2194d15f8277d15b2e46c85df71cca08874"
I066_MATERIALIZATION_BLOB_SHA = "d995821e27ec27d72531dc71b433de702fb8fe7b"

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
MEASURED_PARAMETERS = (
    "currently_available",
    "programmatic_access",
    "electricity_per_task_usd",
    "latency_seconds",
    "reliability_probability",
    "quality_probability",
    "max_parallelism",
)
CONTROL_PARAMETERS = tuple(x for x in CRITICAL_PARAMETERS if x not in MEASURED_PARAMETERS)
REPRODUCIBLE_SOURCE_KINDS = {"provider_first_party", "measured_local", "system_probe"}
ALLOWED_CONTROL_SOURCE_KINDS = REPRODUCIBLE_SOURCE_KINDS | {"user_declared"}


@dataclass(frozen=True)
class ControlEvidence:
    evidence_id: str
    backend_id: str
    parameter: str
    value: Any
    source_kind: str
    source_ref: str
    observed_at: str
    max_age_seconds: int
    reference_backend_hash: str
    source_content_digest: str | None
    notes: str = ""
    evidence_hash: str | None = None

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("evidence_hash", None)
        return body


@dataclass(frozen=True)
class ReadinessResult:
    state: str
    errors: tuple[str, ...]
    backend_id: str
    measured_parameters: tuple[str, ...]
    control_parameters: tuple[str, ...]
    complete_parameter_set: bool
    all_control_sources_reproducible: bool
    contains_user_declaration: bool
    exact_i050_execution_allowed: bool
    exact_i066_execution_allowed: bool
    i123_promotion_allowed: bool
    authorization_implications: tuple[str, ...]
    i050_source_blob_sha: str = I050_RESOURCE_PROFILE_BLOB_SHA
    i066_source_blob_sha: str = I066_MATERIALIZATION_BLOB_SHA
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _digest(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def _validate_control_value(parameter: str, value: Any) -> str | None:
    if parameter in {"requires_credentials", "requires_paid_account", "requires_new_spend", "sunk_or_already_committed"}:
        return None if type(value) is bool else "invalid_boolean_value"
    if parameter == "fixed_monthly_cost_usd":
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) < 0:
            return "invalid_nonnegative_numeric_value"
        return None
    if parameter == "quota_units_remaining":
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) < 0:
            return "invalid_optional_nonnegative_numeric_value"
        return None
    if parameter == "rate_limit_per_minute":
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) <= 0:
            return "rate_limit_must_be_positive_or_none"
        return None
    return "unsupported_control_parameter"


def build_control_evidence(
    *, parameter: str, value: Any, source_kind: str, source_ref: str,
    observed_at: str, max_age_seconds: int, reference_backend_hash: str,
    source_content_digest: str | None, notes: str = "",
) -> ControlEvidence:
    if parameter not in CONTROL_PARAMETERS:
        raise ValueError("control_parameter_required")
    value_error = _validate_control_value(parameter, value)
    if value_error:
        raise ValueError(value_error)
    if source_kind not in ALLOWED_CONTROL_SOURCE_KINDS:
        raise ValueError("unsupported_control_source_kind")
    if not source_ref.strip():
        raise ValueError("source_ref_required")
    _parse_utc(observed_at)
    if max_age_seconds <= 0:
        raise ValueError("positive_max_age_required")
    if source_kind in REPRODUCIBLE_SOURCE_KINDS and (not source_content_digest or len(source_content_digest) < 16):
        raise ValueError("reproducible_source_digest_required")
    draft = ControlEvidence(
        evidence_id=f"i169-owned-pc-{parameter}",
        backend_id="owned_pc",
        parameter=parameter,
        value=value,
        source_kind=source_kind,
        source_ref=source_ref,
        observed_at=observed_at,
        max_age_seconds=max_age_seconds,
        reference_backend_hash=reference_backend_hash,
        source_content_digest=source_content_digest,
        notes=notes,
    )
    return ControlEvidence(**{**asdict(draft), "evidence_hash": _digest(draft.hash_body())})


def evaluate_readiness(
    i168_result: Mapping[str, Any],
    control_records: Iterable[ControlEvidence],
) -> ReadinessResult:
    errors: list[str] = []
    if i168_result.get("state") != "PARTIAL_I050_EVIDENCE_READY":
        errors.append("i168_partial_i050_evidence_not_ready")
    if i168_result.get("backend_id") != "owned_pc":
        errors.append("i168_backend_identity_mismatch")
    if i168_result.get("i166_i167_source_binding_valid") is not True:
        errors.append("i168_source_binding_not_valid")
    if i168_result.get("i050_source_blob_sha") != I050_RESOURCE_PROFILE_BLOB_SHA:
        errors.append("i050_source_binding_drift")
    if i168_result.get("i066_source_blob_sha") != I066_MATERIALIZATION_BLOB_SHA:
        errors.append("i066_source_binding_drift")

    measured = tuple(i168_result.get("emitted_parameters") or ())
    if measured != MEASURED_PARAMETERS:
        errors.append("i168_measured_parameter_set_drift")
    expected_reference_hash = i168_result.get("reference_backend_hash")
    if not isinstance(expected_reference_hash, str) or len(expected_reference_hash) < 16:
        errors.append("i168_reference_backend_hash_missing")

    rows = tuple(control_records)
    by_parameter: dict[str, ControlEvidence] = {}
    for record in rows:
        if record.backend_id != "owned_pc":
            errors.append(f"control_backend_mismatch:{record.parameter}")
        if record.parameter not in CONTROL_PARAMETERS:
            errors.append(f"unexpected_control_parameter:{record.parameter}")
            continue
        if record.parameter in by_parameter:
            errors.append(f"duplicate_control_parameter:{record.parameter}")
            continue
        by_parameter[record.parameter] = record
        if record.reference_backend_hash != expected_reference_hash:
            errors.append(f"reference_hash_mismatch:{record.parameter}")
        value_error = _validate_control_value(record.parameter, record.value)
        if value_error:
            errors.append(f"{record.parameter}:{value_error}")
        if record.source_kind not in ALLOWED_CONTROL_SOURCE_KINDS:
            errors.append(f"unsupported_source_kind:{record.parameter}")
        if not record.source_ref.strip():
            errors.append(f"missing_source_ref:{record.parameter}")
        try:
            _parse_utc(record.observed_at)
        except Exception:
            errors.append(f"invalid_observed_at:{record.parameter}")
        if record.max_age_seconds <= 0:
            errors.append(f"invalid_max_age:{record.parameter}")
        if record.source_kind in REPRODUCIBLE_SOURCE_KINDS and (
            not record.source_content_digest or len(record.source_content_digest) < 16
        ):
            errors.append(f"missing_reproducible_digest:{record.parameter}")
        if record.evidence_hash != _digest(record.hash_body()):
            errors.append(f"evidence_hash_mismatch:{record.parameter}")

    missing = [name for name in CONTROL_PARAMETERS if name not in by_parameter]
    errors.extend(f"missing_control_parameter:{name}" for name in missing)

    controls = tuple(name for name in CONTROL_PARAMETERS if name in by_parameter)
    full_set = set(measured) | set(controls)
    complete = full_set == set(CRITICAL_PARAMETERS) and len(full_set) == len(CRITICAL_PARAMETERS)
    if not complete:
        errors.append("complete_i050_parameter_set_absent")

    contains_declared = any(record.source_kind == "user_declared" for record in by_parameter.values())
    all_reproducible = bool(by_parameter) and len(by_parameter) == len(CONTROL_PARAMETERS) and all(
        record.source_kind in REPRODUCIBLE_SOURCE_KINDS for record in by_parameter.values()
    )

    implications: list[str] = []
    for parameter, marker in (
        ("requires_credentials", "credentials_authorization_required"),
        ("requires_paid_account", "paid_account_evidence_or_authorization_required"),
        ("requires_new_spend", "new_spend_authorization_required"),
    ):
        record = by_parameter.get(parameter)
        if record is not None and record.value is True:
            implications.append(marker)
    fixed = by_parameter.get("fixed_monthly_cost_usd")
    sunk = by_parameter.get("sunk_or_already_committed")
    if fixed is not None and float(fixed.value) > 0 and sunk is not None and sunk.value is False:
        implications.append("fixed_cost_allocation_basis_required_downstream")

    errors = sorted(set(errors))
    exact_i050_allowed = not errors and complete and all_reproducible and not contains_declared
    if exact_i050_allowed:
        state = "READY_FOR_EXACT_I050_EXECUTION"
    elif not errors and complete and contains_declared:
        state = "COMPLETE_DECLARED_BUNDLE_BLOCKED_FOR_I123"
    else:
        state = "PASS_BLOCKED"

    return ReadinessResult(
        state=state,
        errors=tuple(errors),
        backend_id="owned_pc",
        measured_parameters=measured,
        control_parameters=controls,
        complete_parameter_set=complete,
        all_control_sources_reproducible=all_reproducible,
        contains_user_declaration=contains_declared,
        exact_i050_execution_allowed=exact_i050_allowed,
        exact_i066_execution_allowed=False,
        i123_promotion_allowed=False,
        authorization_implications=tuple(dict.fromkeys(implications)),
    )


def payload(result: ReadinessResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I169",
        "next_gate": (
            "If READY_FOR_EXACT_I050_EXECUTION, run the bound current I050 implementation on the complete "
            "14-record bundle. I066 remains forbidden until I050 returns a complete current attestation. "
            "A declared-only bundle must not be relabelled measured_reproducible to satisfy I123."
        ),
    })
    return body
