#!/usr/bin/env python3
"""I166 fail-closed real-evidence gate for the I165 owned-PC materializer.

The gate does not measure or infer economics. It only validates that caller-supplied
external facts intended for a real user-PC run are complete, provenance-bound, and
not labelled as fixtures/examples/synthetic placeholders before I165 may consume them.

No network, credentials, downloads, CI dispatch, paid infrastructure, task acceptance,
spend, settlement, payment or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Mapping

import i165_user_pc_one_shot_materializer as i165

SCHEMA = "mining-autonomy/i166-user-pc-real-evidence-gate/v1"

PROVENANCE_FIELDS = (
    "availability_source_ref",
    "energy_source_ref",
    "tariff_source_ref",
    "opportunity_cost_source_ref",
)

FORBIDDEN_PROVENANCE_MARKERS = (
    "test-fixture",
    "fixture",
    "example",
    "synthetic",
    "placeholder",
    "dummy",
    "mock",
)

REQUIRED_GROUPS = (
    ("measured_available_hours_per_day", "availability_source_ref"),
    ("energy_before_joules", "energy_after_joules", "energy_task_count", "energy_source_ref"),
    ("tariff_usd_per_kwh", "tariff_source_ref"),
    ("opportunity_cost_usd_per_hour", "opportunity_cost_source_ref"),
)


@dataclass(frozen=True)
class GateResult:
    state: str
    errors: tuple[str, ...]
    accepted_external_facts: dict[str, Any]
    ownership_confirmation_supplied: bool
    i165_invocation_allowed: bool
    network_enabled: bool = False
    credentials_used: bool = False
    downloads_or_installs_performed: bool = False
    ci_dispatched: bool = False
    paid_infrastructure_created: bool = False
    task_acceptance_or_submission: bool = False
    spend_or_value_movement: bool = False
    production_route_created: bool = False


def blank_template() -> dict[str, Any]:
    """Emit only null placeholders; these are intentionally non-promotable until replaced."""
    return {name: None for name in i165.EXTERNAL_FIELDS}


def _is_real_provenance(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    lowered = value.strip().lower()
    return not any(marker in lowered for marker in FORBIDDEN_PROVENANCE_MARKERS)


def validate_external_facts(
    raw: Mapping[str, Any],
    *,
    confirm_user_owned_pc: bool,
) -> GateResult:
    errors: list[str] = []
    unknown = sorted(set(raw) - set(i165.EXTERNAL_FIELDS))
    if unknown:
        errors.append("unsupported_external_fields:" + ",".join(unknown))

    if not confirm_user_owned_pc:
        errors.append("explicit_user_owned_pc_confirmation_required")

    accepted = {name: raw.get(name) for name in i165.EXTERNAL_FIELDS if name in raw}

    for group in REQUIRED_GROUPS:
        present = [accepted.get(name) is not None for name in group]
        if any(present) and not all(present):
            errors.append("partial_external_group:" + ",".join(group))
        if not all(present):
            errors.append("missing_external_group:" + ",".join(group))

    for field in PROVENANCE_FIELDS:
        value = accepted.get(field)
        if value is not None and not _is_real_provenance(value):
            errors.append(f"nonproduction_provenance:{field}")

    if accepted.get("measured_available_hours_per_day") is not None:
        value = accepted["measured_available_hours_per_day"]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 24:
            errors.append("invalid_measured_available_hours_per_day")

    before = accepted.get("energy_before_joules")
    after = accepted.get("energy_after_joules")
    count = accepted.get("energy_task_count")
    if before is not None and (isinstance(before, bool) or not isinstance(before, (int, float)) or float(before) < 0):
        errors.append("invalid_energy_before_joules")
    if after is not None and (isinstance(after, bool) or not isinstance(after, (int, float)) or float(after) < 0):
        errors.append("invalid_energy_after_joules")
    if before is not None and after is not None and float(after) < float(before):
        errors.append("energy_counter_wrap_reset_or_negative_delta")
    if count is not None and (isinstance(count, bool) or not isinstance(count, int) or count <= 0):
        errors.append("invalid_energy_task_count")

    tariff = accepted.get("tariff_usd_per_kwh")
    if tariff is not None and (isinstance(tariff, bool) or not isinstance(tariff, (int, float)) or float(tariff) < 0):
        errors.append("invalid_tariff_usd_per_kwh")

    opportunity = accepted.get("opportunity_cost_usd_per_hour")
    if opportunity is not None and (isinstance(opportunity, bool) or not isinstance(opportunity, (int, float)) or float(opportunity) < 0):
        errors.append("invalid_opportunity_cost_usd_per_hour")

    errors = sorted(set(errors))
    allowed = not errors
    return GateResult(
        state="REAL_EXTERNAL_EVIDENCE_ACCEPTED" if allowed else "PASS_BLOCKED",
        errors=tuple(errors),
        accepted_external_facts=accepted if allowed else {},
        ownership_confirmation_supplied=confirm_user_owned_pc,
        i165_invocation_allowed=allowed,
    )


def gate_and_materialize(
    raw: Mapping[str, Any],
    *,
    confirm_user_owned_pc: bool,
    repetitions: int = 20,
    inner_iterations: int = 500,
    parallelism_cap: int = 8,
) -> dict[str, Any]:
    gate = validate_external_facts(raw, confirm_user_owned_pc=confirm_user_owned_pc)
    body = {
        "schema": SCHEMA,
        "run": "I166",
        "gate": asdict(gate),
        "i165_result": None,
        "next_gate": (
            "Replace every null/template field with genuinely observed user-PC evidence and real provenance. "
            "If no trustworthy joule counter exists, keep PASS_BLOCKED rather than estimate energy."
        ),
    }
    if not gate.i165_invocation_allowed:
        return body

    result = i165.materialize(
        external_facts=gate.accepted_external_facts,
        confirm_user_owned_pc=True,
        repetitions=repetitions,
        inner_iterations=inner_iterations,
        parallelism_cap=parallelism_cap,
    )
    body["i165_result"] = asdict(result)
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--external-json")
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--inner-iterations", type=int, default=500)
    parser.add_argument("--parallelism-cap", type=int, default=8)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    if args.template:
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "run": "I166",
            "state": "TEMPLATE_ONLY_NOT_EVIDENCE",
            "external_facts_template": blank_template(),
        }
    else:
        if not args.external_json:
            raise ValueError("external_json_required_unless_template")
        raw = json.loads(Path(args.external_json).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("external_json_must_be_object")
        result = gate_and_materialize(
            raw,
            confirm_user_owned_pc=args.confirm_user_owned_pc,
            repetitions=args.repetitions,
            inner_iterations=args.inner_iterations,
            parallelism_cap=args.parallelism_cap,
        )

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
