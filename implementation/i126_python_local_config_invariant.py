"""I126 narrow reproducible backend-configuration evidence for python_local only.

This module resolves the I125 source-class contradiction without widening I123.
It can emit only five intrinsic software/interface facts whose values are fixed by
the repository model. It cannot evidence electricity, quota/rate capacity, latency,
reliability, quality, owned-PC cost, CI capacity, subscriptions, APIs or VPS cost.

No network access, credentials, spend, workflow dispatch, task action, production
observation, authorization creation or value movement occurs here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from i123_execution_backend_portfolio import BackendEvidence, MEASURED
from resource_feedback_materialization import (
    ResourceEvidenceMaterializationResult,
    materialize_resource_feedback_snapshot,
)
from resource_feedback_summary import (
    BackendEvidenceState,
    LatestParameterEvidenceRef,
    ResourceFeedbackHistorySnapshot,
)
from resource_profile_evidence import (
    BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
    CRITICAL_PARAMETERS,
    PYTHON_LOCAL_CONFIG_INVARIANTS,
    ResourceEvidence,
    attest_resource_profile,
    backend_config_invariant_digest,
    backend_config_invariant_source_ref,
    make_evidence,
    reference_backend_hash,
)

SCHEMA = "mining-autonomy/i126-python-local-config-invariant/v1"
MAX_AGE_SECONDS = 30 * 24 * 60 * 60


@dataclass(frozen=True)
class PythonLocalInvariantResult:
    backend_id: str
    state: str
    evidence_records: tuple[ResourceEvidence, ...]
    emitted_parameters: tuple[str, ...]
    forbidden_parameters: tuple[str, ...]
    strict_reproducible_source_class_available: bool
    production_route_created: bool = False
    execution_enabled: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    spend_performed: bool = False
    value_movement_enabled: bool = False


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def _validate_reference(reference_backend: Mapping[str, Any]) -> None:
    if str(reference_backend.get("backend_id") or "") != "python_local":
        raise ValueError("python_local_backend_required")
    if str(reference_backend.get("family") or "") != "deterministic_python":
        raise ValueError("python_local_deterministic_family_required")
    for parameter, expected in PYTHON_LOCAL_CONFIG_INVARIANTS.items():
        if parameter not in reference_backend:
            raise ValueError(f"python_local_reference_missing:{parameter}")
        actual = reference_backend[parameter]
        if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ValueError(f"python_local_reference_invariant_mismatch:{parameter}")


def build_python_local_config_invariants(
    reference_backend: Mapping[str, Any], *, observed_at: str,
) -> PythonLocalInvariantResult:
    """Build only exact repository-model invariants, hash-bound to the reference."""
    _validate_reference(reference_backend)
    reference_hash = reference_backend_hash(reference_backend)
    records = []
    for parameter, value in PYTHON_LOCAL_CONFIG_INVARIANTS.items():
        records.append(make_evidence(
            evidence_id=f"i126-python-local-config-{parameter}",
            backend_id="python_local",
            parameter=parameter,
            value=value,
            source_kind=BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
            source_ref=backend_config_invariant_source_ref("python_local", parameter),
            observed_at=observed_at,
            max_age_seconds=MAX_AGE_SECONDS,
            reference_hash=reference_hash,
            source_content_digest=backend_config_invariant_digest("python_local", parameter, value),
            notes=(
                "Repository-model intrinsic software/interface invariant only; does not evidence "
                "host energy, capacity, quota, runtime quality or any external service cost."
            ),
        ))
    forbidden = tuple(p for p in CRITICAL_PARAMETERS if p not in PYTHON_LOCAL_CONFIG_INVARIANTS)
    return PythonLocalInvariantResult(
        backend_id="python_local",
        state="REPRODUCIBLE_CONFIG_INVARIANTS_READY",
        evidence_records=tuple(records),
        emitted_parameters=tuple(PYTHON_LOCAL_CONFIG_INVARIANTS),
        forbidden_parameters=forbidden,
        strict_reproducible_source_class_available=True,
    )


def attest_with_python_local_invariants(
    reference_backend: Mapping[str, Any], dynamic_records: Iterable[ResourceEvidence], *,
    observed_at: str, now: datetime,
):
    """Merge genuine dynamic evidence with I126 invariants and call I050.

    Missing dynamic facts stay missing. This function never fills quota/rate limits,
    electricity, latency, reliability, quality or capacity from model defaults.
    """
    config = build_python_local_config_invariants(reference_backend, observed_at=observed_at)
    records = tuple(dynamic_records) + config.evidence_records
    return attest_resource_profile(reference_backend, records, now=now), records


def project_i050_attestation_to_i123(attestation) -> BackendEvidence:
    complete = (
        attestation.state == "calibrated_reproducible"
        and attestation.all_current_evidence_reproducible
        and len(attestation.calibrated_values) == len(CRITICAL_PARAMETERS)
    )
    return BackendEvidence(
        backend_id="python_local",
        provenance_class=MEASURED if complete else "measured_partial",
        current_reproducible=complete,
        non_synthetic=complete,
        capacity_verified=complete,
        policy_evidence_current=complete,
        credentials_authorized=False,
        spend_authorized=False,
        infrastructure_authorized=False,
        evidence_note=(
            "I126 projection from exact I050 attestation. Complete only when all non-config "
            "runtime/electricity/capacity facts are independently evidenced."
        ),
    )


def _snapshot_hash(snapshot: ResourceFeedbackHistorySnapshot) -> str:
    return _hash(snapshot.hash_body())


def build_i066_compatibility_snapshot(
    records: Iterable[ResourceEvidence], *, evidence_bundle_hash: str,
    observed_at: str,
) -> ResourceFeedbackHistorySnapshot:
    """Build an offline compatibility fixture for I066, never a production history claim."""
    rows = tuple(records)
    if not rows or {r.parameter for r in rows} != set(CRITICAL_PARAMETERS):
        raise ValueError("complete_critical_evidence_set_required")
    refs = tuple(
        LatestParameterEvidenceRef(
            backend_id="python_local",
            parameter=record.parameter,
            observed_at=record.observed_at,
            evidence_hashes=(record.evidence_hash or record.computed_hash(),),
            evidence_binding_precision="exact_single_parameter",
            sequence=1,
            entry_hash="i126-fixture-entry",
            feedback_receipt_hash="i126-fixture-feedback",
            evidence_bundle_hash=evidence_bundle_hash,
        )
        for record in sorted(rows, key=lambda r: r.parameter)
    )
    state = BackendEvidenceState(
        backend_id="python_local", latest_parameters=refs,
        update_count=1, last_update_sequence=1, latest_observed_at=observed_at,
    )
    draft = ResourceFeedbackHistorySnapshot(
        state="verified_history_snapshot", reasons=(), history_length=1,
        history_tip_hash="i126-compatibility-fixture", task_id="i126-resource-fixture",
        platform="offline_fixture", external_id="i126-resource-fixture",
        current_selected_backend_id=None, latest_routing_hash="i126-no-route",
        backend_states=(state,), routing_transitions=(), selected_backend_switch_count=0,
        selected_backend_oscillation_detected=False, parameter_churn_indicators=(),
        anomaly_indicators=(),
        limitations=(
            "i126_offline_i066_compatibility_fixture_not_i064_production_history",
            "does_not_create_route_or_authorization",
        ), snapshot_hash="",
    )
    return replace(draft, snapshot_hash=_snapshot_hash(draft))


def verify_i066_compatibility(
    reference_backend: Mapping[str, Any], records: Iterable[ResourceEvidence], *, now: datetime,
) -> ResourceEvidenceMaterializationResult:
    """Prove that a complete I050 bundle containing I126 invariants survives I066."""
    rows = tuple(records)
    attestation = attest_resource_profile(reference_backend, rows, now=now)
    if attestation.state != "calibrated_reproducible" or not attestation.evidence_bundle_hash:
        raise ValueError("complete_reproducible_i050_attestation_required")
    snapshot = build_i066_compatibility_snapshot(
        rows, evidence_bundle_hash=attestation.evidence_bundle_hash,
        observed_at=max(r.observed_at for r in rows),
    )
    return materialize_resource_feedback_snapshot(
        snapshot,
        reference_backends={"python_local": dict(reference_backend)},
        evidence_bundles={attestation.evidence_bundle_hash: rows},
        now=now,
    )


def result_payload(result: PythonLocalInvariantResult) -> dict[str, Any]:
    payload = asdict(result)
    payload["evidence_records"] = [asdict(x) for x in result.evidence_records]
    payload.update({
        "schema": SCHEMA,
        "run": "I126",
        "fresh_real_market_evidence_created": False,
        "authorization_created": False,
        "production_observation_performed": False,
        "free_ci_capacity_inferred": False,
        "owned_pc_cost_inferred": False,
    })
    return payload
