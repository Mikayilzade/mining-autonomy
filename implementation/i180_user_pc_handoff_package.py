#!/usr/bin/env python3
"""I180 inert user-PC handoff package for the I178/I179 real-evidence path.

I180 makes the operational handoff copy/paste-safe without creating evidence. It owns
blank NON_EVIDENCE measurement/accounting templates, concise local instructions, and a
source-drift check for the exact current I178/I179 entry points. Blank templates are
required to FAIL I178 until every real fact is replaced by the user on the owned PC.

No measurement is performed. No value is estimated. No network, credentials, CI,
account creation, paid infrastructure, market observation, task action, spend,
settlement, payment, I050/I066/I123 execution or hybrid-policy application occurs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

import i178_user_pc_handoff_manifest as i178

SCHEMA = "mining-autonomy/i180-user-pc-handoff-package/v1"
I178_PATH = "implementation/i178_user_pc_handoff_manifest.py"
I178_GIT_BLOB_SHA = "9f227af6402e973b4a3b898b0bd9929cb61393cd"
I179_PATH = "implementation/i179_user_pc_real_chain_runner.py"
I179_GIT_BLOB_SHA = "e0dac00cba1acbd9d5dbda6362867af298f50a0a"

MEASUREMENT_TEMPLATE_NAME = "measurement.NON_EVIDENCE.json"
ACCOUNTING_TEMPLATE_NAME = "accounting.NON_EVIDENCE.json"
INSTRUCTIONS_NAME = "README.md"

NON_EVIDENCE_NOTE = "NON_EVIDENCE_TEMPLATE_REPLACE_WITH_GENUINE_FACTS"


@dataclass(frozen=True)
class RuntimeBindingCheck:
    path: str
    expected_git_blob_sha: str
    actual_git_blob_sha: str | None
    present: bool
    exact: bool


@dataclass(frozen=True)
class PackageReport:
    state: str
    blockers: tuple[str, ...]
    runtime_bindings: tuple[RuntimeBindingCheck, ...]
    measurement_template_blank: bool
    accounting_template_blank: bool
    measurement_template_rejected_by_i178: bool
    accounting_template_rejected_by_i178: bool
    package_files_written: tuple[str, ...]
    real_evidence_created: bool = False
    real_chain_ready: bool = False
    i050_execution_allowed: bool = False
    i066_execution_allowed: bool = False
    i123_promotion_allowed: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def measurement_template() -> dict[str, Any]:
    """Return exactly I178's accepted measurement keys, all deliberately null."""
    return {field: None for field in i178.MEASUREMENT_FIELDS}


def accounting_template() -> dict[str, Any]:
    """Return exactly two accounting rows; every promotable fact remains null."""
    return {
        "records": [
            {
                "parameter": parameter,
                "value": None,
                "source_kind": None,
                "source_ref": None,
                "observed_at": None,
                "max_age_seconds": None,
                "source_content_digest": None,
                "notes": NON_EVIDENCE_NOTE,
            }
            for parameter in i178.ACCOUNTING_PARAMETERS
        ]
    }


def instructions_text() -> str:
    return """# User-PC handoff (NON_EVIDENCE templates)\n\nThese two JSON files are intentionally invalid as evidence. Do not invent values just to make the gate pass.\n\n1. Keep the repository source files unchanged. I178 verifies exact Git blob identities.\n2. Copy `measurement.NON_EVIDENCE.json` to a working JSON file and replace every null only with a genuine observed value/provenance from the owned PC.\n3. Energy requires trustworthy before/after joule-counter or meter readings. If no trustworthy meter/counter exists, leave the real chain blocked; do not estimate energy.\n4. Copy `accounting.NON_EVIDENCE.json` to a working JSON file and replace both accounting rows with truthful values and provenance. `user_declared` is allowed as a truthful source class but remains blocked by current strict I050/I123 semantics.\n5. Run the structural/source check first:\n\n```bash\npython implementation/i178_user_pc_handoff_manifest.py --root . --measurement-json <real-measurement.json> --accounting-json <real-accounting.json> --confirm-user-owned-pc\n```\n\n6. Only after I178 returns `READY_TO_RUN_REAL_LOCAL_CHAIN`, run the local evidence chain with an explicit UTC timestamp:\n\n```bash\npython implementation/i179_user_pc_real_chain_runner.py --root . --measurement-json <real-measurement.json> --accounting-json <real-accounting.json> --observed-at <YYYY-MM-DDTHH:MM:SSZ> --confirm-user-owned-pc --output user_pc_chain_result.json\n```\n\nI179 still does not execute I050/I066/I123, contact a market, accept a task, use credentials, spend money or move value.\n"""


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package(output_dir: Path) -> tuple[str, ...]:
    output_dir.mkdir(parents=True, exist_ok=True)
    measurement_path = output_dir / MEASUREMENT_TEMPLATE_NAME
    accounting_path = output_dir / ACCOUNTING_TEMPLATE_NAME
    instructions_path = output_dir / INSTRUCTIONS_NAME
    _write_json(measurement_path, measurement_template())
    _write_json(accounting_path, accounting_template())
    instructions_path.write_text(instructions_text(), encoding="utf-8")
    return tuple(str(path) for path in (measurement_path, accounting_path, instructions_path))


def _runtime_binding(root: Path, path: str, expected: str) -> RuntimeBindingCheck:
    target = root / path
    if not target.is_file():
        return RuntimeBindingCheck(path, expected, None, False, False)
    actual = i178.git_blob_sha(target.read_bytes())
    return RuntimeBindingCheck(path, expected, actual, True, actual == expected)


def verify_runtime_bindings(root: Path) -> tuple[RuntimeBindingCheck, ...]:
    return (
        _runtime_binding(root, I178_PATH, I178_GIT_BLOB_SHA),
        _runtime_binding(root, I179_PATH, I179_GIT_BLOB_SHA),
    )


def _templates_are_blank(measurement: dict[str, Any], accounting: dict[str, Any]) -> tuple[bool, bool]:
    measurement_blank = (
        set(measurement) == set(i178.MEASUREMENT_FIELDS)
        and all(measurement[field] is None for field in i178.MEASUREMENT_FIELDS)
    )
    rows = accounting.get("records")
    accounting_blank = bool(
        isinstance(rows, list)
        and len(rows) == len(i178.ACCOUNTING_PARAMETERS)
        and {row.get("parameter") for row in rows if isinstance(row, dict)} == set(i178.ACCOUNTING_PARAMETERS)
        and all(
            isinstance(row, dict)
            and row.get("value") is None
            and row.get("source_kind") is None
            and row.get("source_ref") is None
            and row.get("observed_at") is None
            and row.get("max_age_seconds") is None
            and row.get("source_content_digest") is None
            for row in rows
        )
    )
    return measurement_blank, accounting_blank


def inspect_package(root: Path, *, package_dir: Path | None = None) -> PackageReport:
    package_dir = package_dir or (root / "implementation" / "user_pc_handoff")
    bindings = verify_runtime_bindings(root)
    blockers: list[str] = []
    for binding in bindings:
        if not binding.present:
            blockers.append(f"runtime_source_missing:{binding.path}")
        elif not binding.exact:
            blockers.append(f"runtime_source_blob_mismatch:{binding.path}")

    measurement_path = package_dir / MEASUREMENT_TEMPLATE_NAME
    accounting_path = package_dir / ACCOUNTING_TEMPLATE_NAME
    written = tuple(
        str(path) for path in (
            measurement_path,
            accounting_path,
            package_dir / INSTRUCTIONS_NAME,
        ) if path.is_file()
    )

    try:
        measurement = json.loads(measurement_path.read_text(encoding="utf-8"))
    except Exception:
        measurement = {}
        blockers.append("measurement_template_missing_or_invalid")
    try:
        accounting = json.loads(accounting_path.read_text(encoding="utf-8"))
    except Exception:
        accounting = {}
        blockers.append("accounting_template_missing_or_invalid")

    measurement_blank, accounting_blank = _templates_are_blank(measurement, accounting)
    if not measurement_blank:
        blockers.append("measurement_template_not_blank_non_evidence")
    if not accounting_blank:
        blockers.append("accounting_template_not_blank_non_evidence")

    measurement_rejected = False
    accounting_rejected = False
    if measurement_path.is_file():
        measurement_rejected = not i178.check_measurement_input(measurement_path).structurally_complete
    if accounting_path.is_file():
        accounting_rejected = not i178.check_accounting_input(accounting_path).structurally_complete
    if not measurement_rejected:
        blockers.append("measurement_template_must_fail_i178")
    if not accounting_rejected:
        blockers.append("accounting_template_must_fail_i178")

    exact_runtime = all(binding.exact for binding in bindings)
    package_ready = bool(
        exact_runtime
        and measurement_blank
        and accounting_blank
        and measurement_rejected
        and accounting_rejected
        and (package_dir / INSTRUCTIONS_NAME).is_file()
    )
    return PackageReport(
        state="PACKAGE_READY_NON_EVIDENCE" if package_ready and not blockers else "PASS_BLOCKED",
        blockers=tuple(sorted(set(blockers))),
        runtime_bindings=bindings,
        measurement_template_blank=measurement_blank,
        accounting_template_blank=accounting_blank,
        measurement_template_rejected_by_i178=measurement_rejected,
        accounting_template_rejected_by_i178=accounting_rejected,
        package_files_written=written,
    )


def payload(result: PackageReport) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I180",
        "template_warning": "Blank templates are NON_EVIDENCE and are required to fail I178 until replaced with genuine facts.",
        "next_gate": (
            "Copy/fill working JSON files on the actual user-owned PC, run I178, then I179. "
            "Do not modify the checked-in NON_EVIDENCE templates into fake passing examples."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--package-dir")
    parser.add_argument("--write-package", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    root = Path(args.root)
    package_dir = Path(args.package_dir) if args.package_dir else root / "implementation" / "user_pc_handoff"
    if args.write_package:
        write_package(package_dir)
    result = inspect_package(root, package_dir=package_dir)
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.state == "PACKAGE_READY_NON_EVIDENCE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
