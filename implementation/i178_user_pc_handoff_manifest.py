#!/usr/bin/env python3
"""I178 exact-source user-PC handoff manifest and blocker reporter.

This module makes the real owned-PC handoff operational without inventing evidence.
It verifies the exact Git-blob identities of the local source chain needed to reach
I177, checks only structural completeness of caller-provided measurement/accounting
JSON, and reports the next safe gate. It never fills missing values or interprets a
placeholder as evidence.

No network, credentials, CI dispatch, account creation, paid infrastructure, market
observation, task acceptance/submission, spend, settlement, payment or value movement
is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
import argparse
import json
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "mining-autonomy/i178-user-pc-handoff-manifest/v1"

FORBIDDEN_PROVENANCE_MARKERS = (
    "test-fixture", "fixture", "example", "synthetic", "placeholder", "dummy", "mock",
)

MEASUREMENT_FIELDS = (
    "measured_available_hours_per_day",
    "availability_source_ref",
    "energy_before_joules",
    "energy_after_joules",
    "energy_task_count",
    "energy_source_ref",
    "tariff_usd_per_kwh",
    "tariff_source_ref",
    "opportunity_cost_usd_per_hour",
    "opportunity_cost_source_ref",
)

ACCOUNTING_PARAMETERS = (
    "fixed_monthly_cost_usd",
    "sunk_or_already_committed",
)


@dataclass(frozen=True)
class SourceSpec:
    path: str
    git_blob_sha: str
    role: str
    required_on_user_pc: bool = True


SOURCE_SPECS = (
    SourceSpec("implementation/i159_owned_pc_evidence_packet.py", "b2b9e1a5a7808f75b935751cca64d00326d273e3", "owned_pc_evidence_gate"),
    SourceSpec("implementation/i162_user_pc_measurement_procedure.py", "67319cf4d39b928c04531d4091a373a35d660136", "measurement_packet"),
    SourceSpec("implementation/i163_user_pc_benchmark_session.py", "9e6d0e95004506b6e384c813ddedb9e416e40db4", "benchmark_session"),
    SourceSpec("implementation/i164_fixed_benchmark_core.py", "2a39371bd38b377340c18b1ce77c8bcdbd71c03f", "benchmark_core"),
    SourceSpec("implementation/i165_user_pc_one_shot_materializer.py", "c336efd57f61acf9d7fd7571e729a753ddbf3b91", "measurement_materializer"),
    SourceSpec("implementation/i166_user_pc_real_evidence_gate.py", "a58a60c04d394a985f640b795ddb8b9ff2468464", "real_external_evidence_gate"),
    SourceSpec("implementation/i167_owned_pc_router_bridge.py", "4be411d0fdb7fdc03e4a490d502ef2b9dcb4b804", "router_resource_bridge"),
    SourceSpec("implementation/i168_owned_pc_i050_evidence_adapter.py", "024b2e29d3eddee2ba94b789ce3c5ef2d2997ff6", "measured_i050_adapter"),
    SourceSpec("implementation/i169_owned_pc_i050_i066_readiness.py", "26fa086c0c3130a88f2f8dd36a802062c56cdd7f", "strict_readiness_gate"),
    SourceSpec("implementation/i171_owned_pc_execution_scope_gate.py", "1d2e0cb92ba5883ee7e4deeb06f0b970b878f56a", "production_scope_gate"),
    SourceSpec("implementation/i173_structured_json_transform_executor.py", "29485940ac92c26616a9b60ee9e309110a4fbe62", "deterministic_executor"),
    SourceSpec("implementation/i174_exact_executor_interface_probe.py", "569ec58988abdfa055cd172358a39ed88e36e5f3", "exact_interface_probe"),
    SourceSpec("implementation/i175_i171_production_scope_binding.py", "f8b70be5a16479feb1ebeed8489d68bcdcd5ff33", "production_scope_binding"),
    SourceSpec("implementation/i177_owned_pc_evidence_assembly.py", "9ecea6cbf9ae9bf023171b734f3750f44ec7a926", "i169_evidence_assembly"),
    SourceSpec("implementation/resource_router.py", "3dc7a7f7bbe1437ca4cd396767e20a857aa658cd", "owned_pc_reference_backend"),
    SourceSpec("implementation/resource_profile_evidence.py", "9b76a2194d15f8277d15b2e46c85df71cca08874", "downstream_i050_binding"),
    SourceSpec("implementation/resource_feedback_materialization.py", "d995821e27ec27d72531dc71b433de702fb8fe7b", "downstream_i066_binding"),
    SourceSpec("implementation/i123_execution_backend_portfolio.py", "a3b7878b9114d3059784a4d3a0d6d6f55fa9fe3c", "downstream_i123_binding"),
)


@dataclass(frozen=True)
class SourceCheck:
    path: str
    expected_git_blob_sha: str
    actual_git_blob_sha: str | None
    present: bool
    exact: bool
    role: str


@dataclass(frozen=True)
class InputCheck:
    name: str
    supplied: bool
    structurally_complete: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class HandoffReport:
    state: str
    blockers: tuple[str, ...]
    source_checks: tuple[SourceCheck, ...]
    measurement_input: InputCheck
    accounting_input: InputCheck
    ownership_confirmation_supplied: bool
    exact_source_tree_ready: bool
    ready_to_run_real_chain: bool
    i050_execution_allowed: bool = False
    i066_execution_allowed: bool = False
    i123_promotion_allowed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def git_blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _real_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    low = value.strip().lower()
    return not any(marker in low for marker in FORBIDDEN_PROVENANCE_MARKERS)


def verify_source_tree(root: Path) -> tuple[SourceCheck, ...]:
    checks: list[SourceCheck] = []
    for spec in SOURCE_SPECS:
        target = root / spec.path
        if not target.is_file():
            checks.append(SourceCheck(spec.path, spec.git_blob_sha, None, False, False, spec.role))
            continue
        actual = git_blob_sha(target.read_bytes())
        checks.append(SourceCheck(spec.path, spec.git_blob_sha, actual, True, actual == spec.git_blob_sha, spec.role))
    return tuple(checks)


def _load_json(path: Path | None, name: str) -> tuple[Mapping[str, Any] | None, InputCheck]:
    if path is None:
        return None, InputCheck(name, False, False, (f"{name}_not_supplied",))
    if not path.is_file():
        return None, InputCheck(name, True, False, (f"{name}_file_missing",))
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None, InputCheck(name, True, False, (f"{name}_invalid_json",))
    if not isinstance(raw, dict):
        return None, InputCheck(name, True, False, (f"{name}_must_be_object",))
    return raw, InputCheck(name, True, True, ())


def check_measurement_input(path: Path | None) -> InputCheck:
    raw, base = _load_json(path, "measurement_json")
    if raw is None:
        return base
    errors: list[str] = []
    unknown = sorted(set(raw) - set(MEASUREMENT_FIELDS))
    if unknown:
        errors.append("measurement_unknown_fields:" + ",".join(unknown))
    for field in MEASUREMENT_FIELDS:
        if field not in raw or raw.get(field) is None:
            errors.append(f"measurement_missing:{field}")
    for field in ("availability_source_ref", "energy_source_ref", "tariff_source_ref", "opportunity_cost_source_ref"):
        if field in raw and raw.get(field) is not None and not _real_ref(raw.get(field)):
            errors.append(f"measurement_nonproduction_provenance:{field}")
    return InputCheck("measurement_json", True, not errors, tuple(sorted(set(errors))))


def check_accounting_input(path: Path | None) -> InputCheck:
    raw, base = _load_json(path, "accounting_json")
    if raw is None:
        return base
    errors: list[str] = []
    rows = raw.get("records")
    if not isinstance(rows, list):
        return InputCheck("accounting_json", True, False, ("accounting_records_list_required",))
    by_parameter: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            errors.append("accounting_record_must_be_object")
            continue
        parameter = row.get("parameter")
        if parameter not in ACCOUNTING_PARAMETERS:
            errors.append(f"accounting_unexpected_parameter:{parameter}")
            continue
        if parameter in by_parameter:
            errors.append(f"accounting_duplicate_parameter:{parameter}")
            continue
        by_parameter[str(parameter)] = row
        if row.get("value") is None:
            errors.append(f"accounting_missing_value:{parameter}")
        if row.get("source_kind") not in {"user_declared", "provider_first_party", "measured_local", "system_probe"}:
            errors.append(f"accounting_invalid_source_kind:{parameter}")
        if not _real_ref(row.get("source_ref")):
            errors.append(f"accounting_nonproduction_provenance:{parameter}")
        if not isinstance(row.get("observed_at"), str) or not row.get("observed_at", "").strip():
            errors.append(f"accounting_observed_at_required:{parameter}")
        age = row.get("max_age_seconds")
        if isinstance(age, bool) or not isinstance(age, int) or age <= 0:
            errors.append(f"accounting_positive_max_age_required:{parameter}")
        if row.get("source_kind") in {"provider_first_party", "measured_local", "system_probe"}:
            digest = row.get("source_content_digest")
            if not isinstance(digest, str) or len(digest) < 16:
                errors.append(f"accounting_reproducible_digest_required:{parameter}")
    for parameter in ACCOUNTING_PARAMETERS:
        if parameter not in by_parameter:
            errors.append(f"accounting_missing_parameter:{parameter}")
    return InputCheck("accounting_json", True, not errors, tuple(sorted(set(errors))))


def inspect_handoff(
    root: Path,
    *,
    measurement_json: Path | None = None,
    accounting_json: Path | None = None,
    confirm_user_owned_pc: bool = False,
) -> HandoffReport:
    source_checks = verify_source_tree(root)
    measurement = check_measurement_input(measurement_json)
    accounting = check_accounting_input(accounting_json)
    blockers: list[str] = []

    for check in source_checks:
        if not check.present:
            blockers.append(f"source_missing:{check.path}")
        elif not check.exact:
            blockers.append(f"source_blob_mismatch:{check.path}")
    if not confirm_user_owned_pc:
        blockers.append("explicit_user_owned_pc_confirmation_required")
    blockers.extend(measurement.errors)
    blockers.extend(accounting.errors)

    exact_sources = all(check.exact for check in source_checks)
    ready = bool(exact_sources and confirm_user_owned_pc and measurement.structurally_complete and accounting.structurally_complete)
    if ready:
        state = "READY_TO_RUN_REAL_LOCAL_CHAIN"
    elif not exact_sources:
        state = "SOURCE_TREE_BLOCKED"
    else:
        state = "HANDOFF_INPUTS_BLOCKED"

    return HandoffReport(
        state=state,
        blockers=tuple(sorted(set(blockers))),
        source_checks=source_checks,
        measurement_input=measurement,
        accounting_input=accounting,
        ownership_confirmation_supplied=confirm_user_owned_pc,
        exact_source_tree_ready=exact_sources,
        ready_to_run_real_chain=ready,
    )


def payload(result: HandoffReport) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I178",
        "measurement_fields_required": list(MEASUREMENT_FIELDS),
        "accounting_parameters_required": list(ACCOUNTING_PARAMETERS),
        "next_gate": (
            "READY_TO_RUN_REAL_LOCAL_CHAIN means only that source files and caller inputs are structurally ready. "
            "Run I166/I165 on the actual owned PC and let the existing gates validate the facts. I178 never "
            "authorizes I050/I066/I123 or treats file presence as truth."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--measurement-json")
    parser.add_argument("--accounting-json")
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = inspect_handoff(
        Path(args.root),
        measurement_json=Path(args.measurement_json) if args.measurement_json else None,
        accounting_json=Path(args.accounting_json) if args.accounting_json else None,
        confirm_user_owned_pc=args.confirm_user_owned_pc,
    )
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.state == "READY_TO_RUN_REAL_LOCAL_CHAIN" else 2


if __name__ == "__main__":
    raise SystemExit(main())
