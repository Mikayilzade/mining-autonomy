"""Deterministic resource-profile evidence/calibration layer (I050).

This module is deliberately transport- and execution-free. It turns synthetic
resource-router references into planning-only objects unless current evidence
binds every critical live-routing parameter to an explicit fresh provenance record.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Optional

BACKEND_CONFIG_INVARIANT_SOURCE_KIND = "backend_config_invariant"
SOURCE_KINDS = {
    "synthetic_reference",
    "user_declared",
    "measured_local",
    "provider_first_party",
    "system_probe",
    BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
}
REPRODUCIBLE_SOURCE_KINDS = {
    "provider_first_party",
    "measured_local",
    "system_probe",
    BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
}

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

BOOL_PARAMETERS = {
    "currently_available",
    "programmatic_access",
    "requires_credentials",
    "requires_paid_account",
    "requires_new_spend",
    "sunk_or_already_committed",
}
NONNEGATIVE_FLOAT_PARAMETERS = {
    "fixed_monthly_cost_usd",
    "electricity_per_task_usd",
    "latency_seconds",
}
PROBABILITY_PARAMETERS = {
    "reliability_probability",
    "quality_probability",
}
OPTIONAL_NONNEGATIVE_FLOAT_PARAMETERS = {
    "quota_units_remaining",
    "rate_limit_per_minute",
}

# I126: only these intrinsic software/interface facts may use the reproducible
# repository-config invariant source. Runtime capacity, quota/rate limits,
# electricity, latency, reliability and quality are intentionally excluded.
PYTHON_LOCAL_CONFIG_INVARIANTS = {
    "requires_credentials": False,
    "requires_paid_account": False,
    "requires_new_spend": False,
    "fixed_monthly_cost_usd": 0.0,
    "sunk_or_already_committed": True,
}
PYTHON_LOCAL_CONFIG_INVARIANT_SCOPE = "intrinsic_python_local_software_interface_only"


def _canonical_hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def backend_config_invariant_source_ref(backend_id: str, parameter: str) -> str:
    return f"repo-invariant:{backend_id}:{parameter}:v1"


def backend_config_invariant_digest(backend_id: str, parameter: str, value: Any) -> str:
    return _canonical_hash({
        "schema": "mining-autonomy/backend-config-invariant/v1",
        "scope": PYTHON_LOCAL_CONFIG_INVARIANT_SCOPE,
        "backend_id": backend_id,
        "parameter": parameter,
        "value": value,
    })


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def reference_backend_hash(reference_backend: Mapping[str, Any]) -> str:
    """Bind calibration to the exact router reference profile being calibrated."""
    return _canonical_hash(dict(reference_backend))


@dataclass(frozen=True)
class ResourceEvidence:
    evidence_id: str
    backend_id: str
    parameter: str
    value: Any
    source_kind: str
    source_ref: str
    observed_at: str
    max_age_seconds: int
    reference_backend_hash: str
    source_content_digest: Optional[str] = None
    notes: str = ""
    evidence_hash: Optional[str] = None

    def hash_body(self) -> dict[str, Any]:
        body = asdict(self)
        body.pop("evidence_hash", None)
        return body

    def computed_hash(self) -> str:
        return _canonical_hash(self.hash_body())


@dataclass(frozen=True)
class ParameterCalibration:
    parameter: str
    state: str
    value: Any
    evidence_id: Optional[str]
    source_kind: Optional[str]
    observed_at: Optional[str]
    reason: Optional[str]


@dataclass(frozen=True)
class ResourceProfileAttestation:
    backend_id: str
    reference_backend_hash: str
    state: str
    reasons: tuple[str, ...]
    parameter_calibrations: tuple[ParameterCalibration, ...]
    calibrated_values: Mapping[str, Any]
    evidence_bundle_hash: Optional[str]
    contains_user_declaration: bool
    all_current_evidence_reproducible: bool
    planning_only: bool = True
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def make_evidence(
    *,
    evidence_id: str,
    backend_id: str,
    parameter: str,
    value: Any,
    source_kind: str,
    source_ref: str,
    observed_at: str,
    max_age_seconds: int,
    reference_hash: str,
    source_content_digest: Optional[str] = None,
    notes: str = "",
) -> ResourceEvidence:
    draft = ResourceEvidence(
        evidence_id=evidence_id,
        backend_id=backend_id,
        parameter=parameter,
        value=value,
        source_kind=source_kind,
        source_ref=source_ref,
        observed_at=observed_at,
        max_age_seconds=max_age_seconds,
        reference_backend_hash=reference_hash,
        source_content_digest=source_content_digest,
        notes=notes,
    )
    return ResourceEvidence(**{**asdict(draft), "evidence_hash": draft.computed_hash()})


def _validate_value(parameter: str, value: Any) -> Optional[str]:
    if parameter in BOOL_PARAMETERS:
        if type(value) is not bool:
            return "invalid_boolean_value"
        return None
    if parameter in NONNEGATIVE_FLOAT_PARAMETERS:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) < 0:
            return "invalid_nonnegative_numeric_value"
        return None
    if parameter in PROBABILITY_PARAMETERS:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            return "invalid_probability_value"
        return None
    if parameter in OPTIONAL_NONNEGATIVE_FLOAT_PARAMETERS:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) < 0:
            return "invalid_optional_nonnegative_numeric_value"
        if parameter == "rate_limit_per_minute" and float(value) == 0:
            return "rate_limit_must_be_positive_or_none"
        return None
    if parameter == "max_parallelism":
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            return "invalid_parallelism_value"
        return None
    return "unsupported_parameter"


def _validate_backend_config_invariant(evidence: ResourceEvidence) -> Optional[str]:
    if evidence.backend_id != "python_local":
        return "backend_config_invariant_python_local_only"
    if evidence.parameter not in PYTHON_LOCAL_CONFIG_INVARIANTS:
        return "backend_config_invariant_parameter_not_allowed"
    expected_value = PYTHON_LOCAL_CONFIG_INVARIANTS[evidence.parameter]
    if json.dumps(evidence.value, sort_keys=True) != json.dumps(expected_value, sort_keys=True):
        return "backend_config_invariant_value_mismatch"
    expected_ref = backend_config_invariant_source_ref(evidence.backend_id, evidence.parameter)
    if evidence.source_ref != expected_ref:
        return "backend_config_invariant_source_ref_mismatch"
    expected_digest = backend_config_invariant_digest(
        evidence.backend_id, evidence.parameter, expected_value
    )
    if evidence.source_content_digest != expected_digest:
        return "backend_config_invariant_digest_mismatch"
    return None


def _evidence_status(
    evidence: ResourceEvidence,
    *,
    backend_id: str,
    expected_reference_hash: str,
    now: datetime,
) -> Optional[str]:
    if evidence.backend_id != backend_id:
        return "backend_binding_mismatch"
    if evidence.parameter not in CRITICAL_PARAMETERS:
        return "unsupported_parameter"
    if evidence.source_kind not in SOURCE_KINDS:
        return "unsupported_source_kind"
    if not evidence.source_ref.strip():
        return "missing_source_ref"
    if evidence.max_age_seconds <= 0:
        return "invalid_max_age"
    if evidence.reference_backend_hash != expected_reference_hash:
        return "reference_backend_hash_mismatch"
    if evidence.evidence_hash != evidence.computed_hash():
        return "evidence_hash_mismatch"
    value_error = _validate_value(evidence.parameter, evidence.value)
    if value_error:
        return value_error
    try:
        observed = _parse_utc(evidence.observed_at)
    except Exception:
        return "invalid_observed_at"
    if observed > now:
        return "future_dated_evidence"
    if (now - observed).total_seconds() > evidence.max_age_seconds:
        return "stale_evidence"
    if evidence.source_kind == "synthetic_reference":
        return "synthetic_reference_not_live_evidence"
    if evidence.source_kind == BACKEND_CONFIG_INVARIANT_SOURCE_KIND:
        invariant_error = _validate_backend_config_invariant(evidence)
        if invariant_error:
            return invariant_error
    if evidence.source_kind in REPRODUCIBLE_SOURCE_KINDS:
        digest = evidence.source_content_digest
        if not digest or len(digest) < 16:
            return "reproducible_source_digest_required"
    return None


def attest_resource_profile(
    reference_backend: Mapping[str, Any],
    evidence_records: Iterable[ResourceEvidence],
    *,
    now: datetime,
) -> ResourceProfileAttestation:
    """Fail closed unless every critical parameter has fresh, bound evidence."""
    if now.tzinfo is None or now.utcoffset() != timezone.utc.utcoffset(now):
        raise ValueError("now_must_be_utc")
    backend = dict(reference_backend)
    backend_id = str(backend.get("backend_id") or "")
    if not backend_id:
        raise ValueError("reference_backend_id_required")
    ref_hash = reference_backend_hash(backend)

    grouped: dict[str, list[ResourceEvidence]] = {p: [] for p in CRITICAL_PARAMETERS}
    global_reasons: list[str] = []
    for record in evidence_records:
        if record.parameter in grouped:
            grouped[record.parameter].append(record)
        else:
            global_reasons.append(f"{record.evidence_id}:unsupported_parameter")

    calibrations: list[ParameterCalibration] = []
    selected: list[ResourceEvidence] = []
    calibrated_values: dict[str, Any] = {}

    for parameter in CRITICAL_PARAMETERS:
        candidates = grouped[parameter]
        if not candidates:
            calibrations.append(ParameterCalibration(
                parameter, "missing", None, None, None, None, "missing_evidence"
            ))
            continue

        valid: list[ResourceEvidence] = []
        failures: list[str] = []
        for record in candidates:
            reason = _evidence_status(
                record, backend_id=backend_id, expected_reference_hash=ref_hash, now=now
            )
            if reason is None:
                valid.append(record)
            else:
                failures.append(f"{record.evidence_id}:{reason}")

        if not valid:
            calibrations.append(ParameterCalibration(
                parameter, "invalid_or_stale", None, None, None, None,
                ";".join(sorted(failures)) or "no_valid_evidence",
            ))
            continue

        distinct_values = {
            json.dumps(r.value, sort_keys=True, separators=(",", ":"), default=str)
            for r in valid
        }
        if len(distinct_values) > 1:
            calibrations.append(ParameterCalibration(
                parameter, "conflict", None, None, None, None, "conflicting_current_evidence"
            ))
            continue

        valid.sort(key=lambda r: (_parse_utc(r.observed_at), r.evidence_id), reverse=True)
        chosen = valid[0]
        selected.append(chosen)
        calibrated_values[parameter] = chosen.value
        calibrations.append(ParameterCalibration(
            parameter=parameter,
            state="current",
            value=chosen.value,
            evidence_id=chosen.evidence_id,
            source_kind=chosen.source_kind,
            observed_at=chosen.observed_at,
            reason=None,
        ))

    incomplete = [c for c in calibrations if c.state != "current"]
    if incomplete:
        state = "planning_only"
        global_reasons.extend(f"{c.parameter}:{c.reason}" for c in incomplete)
    else:
        contains_declared = any(x.source_kind == "user_declared" for x in selected)
        state = "calibrated_declared" if contains_declared else "calibrated_reproducible"

    contains_declared = any(x.source_kind == "user_declared" for x in selected)
    reproducible = bool(selected) and all(
        x.source_kind in REPRODUCIBLE_SOURCE_KINDS for x in selected
    )
    bundle_hash = None
    if selected:
        bundle_hash = _canonical_hash({
            "backend_id": backend_id,
            "reference_backend_hash": ref_hash,
            "evidence_hashes": sorted(x.evidence_hash for x in selected if x.evidence_hash),
        })

    return ResourceProfileAttestation(
        backend_id=backend_id,
        reference_backend_hash=ref_hash,
        state=state,
        reasons=tuple(dict.fromkeys(global_reasons)),
        parameter_calibrations=tuple(calibrations),
        calibrated_values=calibrated_values,
        evidence_bundle_hash=bundle_hash,
        contains_user_declaration=contains_declared,
        all_current_evidence_reproducible=reproducible and not incomplete,
    )


def materialize_calibrated_backend_fields(
    reference_backend: Mapping[str, Any],
    attestation: ResourceProfileAttestation,
) -> dict[str, Any]:
    """Return router fields only for a complete current attestation.

    This function does not instantiate an executor and never enables transport.
    """
    backend = dict(reference_backend)
    expected_hash = reference_backend_hash(backend)
    if attestation.backend_id != backend.get("backend_id"):
        raise ValueError("attestation_backend_mismatch")
    if attestation.reference_backend_hash != expected_hash:
        raise ValueError("attestation_reference_hash_mismatch")
    if attestation.state not in {"calibrated_declared", "calibrated_reproducible"}:
        raise ValueError("resource_profile_not_live_calibrated")
    missing = [p for p in CRITICAL_PARAMETERS if p not in attestation.calibrated_values]
    if missing:
        raise ValueError("attestation_missing_critical_parameters")
    out = dict(backend)
    out.update(attestation.calibrated_values)
    out["_resource_attestation"] = {
        "state": attestation.state,
        "evidence_bundle_hash": attestation.evidence_bundle_hash,
        "execution_enabled": False,
        "network_enabled": False,
        "value_movement_enabled": False,
    }
    return out