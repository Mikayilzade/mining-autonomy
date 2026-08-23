"""I125 audit of whether the current Resource Router evidence model can ever
promote python_local to strict measured/reproducible production evidence.

This is a model-consistency audit only. It performs no probe, network access,
credentials, spend, execution authorization, task action, or value movement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

from python_local_calibration_fixture import BENCHMARK_ID, EXPECTED_OUTPUT_DIGEST
from resource_calibration_acquisition import AcquisitionRequirement, build_local_no_spend_plan
from resource_profile_evidence import CRITICAL_PARAMETERS
from resource_router import default_backend_families

REPRODUCIBLE_SOURCE_KINDS = frozenset({"provider_first_party", "measured_local", "system_probe"})
DECLARATIVE_SOURCE_KIND = "user_declared"


@dataclass(frozen=True)
class ParameterPromotability:
    parameter: str
    accepted_source_kinds: tuple[str, ...]
    reproducible_source_kinds: tuple[str, ...]
    declaration_only: bool
    strict_reproducible_possible: bool
    acquisition_method: str


@dataclass(frozen=True)
class PromotabilityAudit:
    backend_id: str
    strict_target: str
    state: str
    parameter_results: tuple[ParameterPromotability, ...]
    declaration_only_parameters: tuple[str, ...]
    strict_reproducible_impossible_parameters: tuple[str, ...]
    model_defect_detected: bool
    recommended_fix: str
    production_selection_widened: bool = False
    execution_enabled: bool = False
    network_enabled: bool = False
    value_movement_enabled: bool = False


def _python_local_reference():
    return next(x for x in default_backend_families() if x.backend_id == "python_local")


def _classify(requirement: AcquisitionRequirement) -> ParameterPromotability:
    reproducible = tuple(sorted(set(requirement.accepted_source_kinds) & REPRODUCIBLE_SOURCE_KINDS))
    accepted = tuple(requirement.accepted_source_kinds)
    declaration_only = set(accepted) == {DECLARATIVE_SOURCE_KIND}
    return ParameterPromotability(
        parameter=requirement.parameter,
        accepted_source_kinds=accepted,
        reproducible_source_kinds=reproducible,
        declaration_only=declaration_only,
        strict_reproducible_possible=bool(reproducible),
        acquisition_method=requirement.acquisition_method,
    )


def audit_python_local_promotability() -> PromotabilityAudit:
    reference = _python_local_reference()
    plan = build_local_no_spend_plan(
        asdict(reference), benchmark_id=BENCHMARK_ID,
        expected_output_digest=EXPECTED_OUTPUT_DIGEST,
    )
    rows = tuple(_classify(req) for req in plan.requirements)
    if {row.parameter for row in rows} != set(CRITICAL_PARAMETERS):
        raise AssertionError("audit_must_cover_all_critical_parameters")
    declaration_only = tuple(row.parameter for row in rows if row.declaration_only)
    impossible = tuple(row.parameter for row in rows if not row.strict_reproducible_possible)
    defect = bool(impossible)
    recommendation = (
        "Do not weaken I123 to accept arbitrary declarations. Add a narrowly scoped, hash-bound "
        "reproducible backend-configuration invariant for python_local accounting facts that are "
        "model-defined (especially zero fixed software cost / zero-cost sunk normalization), while "
        "keeping host electricity and any nonzero external cost measured or first-party evidenced."
        if defect else
        "No source-class contradiction detected; proceed with measured evidence acquisition."
    )
    return PromotabilityAudit(
        backend_id=plan.backend_id,
        strict_target="all_current_evidence_reproducible -> I123 measured_reproducible",
        state="MODEL_DEFECT_BLOCKS_STRICT_PROMOTION" if defect else "STRICT_PROMOTION_SOURCE_CLASSES_FEASIBLE",
        parameter_results=rows,
        declaration_only_parameters=declaration_only,
        strict_reproducible_impossible_parameters=impossible,
        model_defect_detected=defect,
        recommended_fix=recommendation,
    )


def to_payload(audit: PromotabilityAudit) -> dict:
    payload = asdict(audit)
    payload.update({
        "schema": "mining-autonomy/i125-resource-promotability-audit/v1",
        "run": "I125",
        "fresh_real_market_evidence_created": False,
        "authorization_created": False,
        "production_route_created": False,
        "spend_or_value_movement": False,
    })
    return payload


def main() -> int:
    audit = audit_python_local_promotability()
    output = Path(__file__).with_name("I125_RESOURCE_PROMOTABILITY_AUDIT.json")
    output.write_text(json.dumps(to_payload(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(to_payload(audit), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
