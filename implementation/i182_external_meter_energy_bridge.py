#!/usr/bin/env python3
"""I182 fail-closed bridge from real external meter readings to I166 energy fields.

This module exists for owned PCs that expose no trustworthy local cumulative joule
counter. It NEVER reads a meter and NEVER estimates energy. It only validates caller-
supplied before/after cumulative readings from an already-available external physical
meter, converts supported units to joules, and emits the four energy fields expected
by I166/I162.

A promotable bridge requires whole-system AC-input scope, an exclusive PC load during
the measurement window, the same cumulative counter for before/after readings, a
positive measurable energy delta, a positive task count, explicit real provenance and
a source-content digest. Component-only meters, instantaneous power, inferred/estimated
readings, missing provenance, counter reset/wrap and zero-resolution sessions remain
blocked.

No network, credentials, subprocess, package install, privilege escalation, CI,
account creation, hardware purchase, spend, market action or value movement occurs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "mining-autonomy/i182-external-meter-energy-bridge/v1"
JOULES_PER_WH = 3600.0
JOULES_PER_KWH = 3_600_000.0
SUPPORTED_UNITS = {"joule", "wh", "kwh"}
FORBIDDEN_PROVENANCE_MARKERS = (
    "test-fixture", "fixture", "example", "synthetic", "placeholder", "dummy", "mock",
    "estimate", "estimated", "assumed", "inferred",
)


@dataclass(frozen=True)
class ExternalMeterSession:
    meter_source_ref: str
    meter_source_digest: str
    meter_scope: str
    exclusive_pc_load_confirmed: bool
    same_cumulative_counter_confirmed: bool
    reading_unit: str
    reading_before: float
    reading_after: float
    task_count: int
    session_ref: str
    notes: str = ""


@dataclass(frozen=True)
class BridgeResult:
    state: str
    errors: tuple[str, ...]
    energy_before_joules: float | None
    energy_after_joules: float | None
    energy_delta_joules: float | None
    energy_kwh_per_task: float | None
    energy_task_count: int | None
    energy_source_ref: str | None
    source_content_digest: str | None
    i166_energy_fields_ready: bool
    meter_read_performed: bool = False
    evidence_invented: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    subprocess_used: bool = False
    software_installed: bool = False
    elevated_privileges_requested: bool = False
    hardware_purchased: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False


def _real_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    low = value.strip().lower()
    return not any(marker in low for marker in FORBIDDEN_PROVENANCE_MARKERS)


def _convert_to_joules(value: float, unit: str) -> float:
    normalized = unit.strip().lower()
    if normalized == "joule":
        return float(value)
    if normalized == "wh":
        return float(value) * JOULES_PER_WH
    if normalized == "kwh":
        return float(value) * JOULES_PER_KWH
    raise ValueError("unsupported_reading_unit")


def _digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return sha256(text.encode("utf-8")).hexdigest()


def bridge_external_meter(session: ExternalMeterSession) -> BridgeResult:
    errors: list[str] = []

    if not _real_ref(session.meter_source_ref):
        errors.append("real_meter_source_ref_required")
    if not isinstance(session.meter_source_digest, str) or len(session.meter_source_digest) < 16:
        errors.append("meter_source_digest_required")
    if not _real_ref(session.session_ref):
        errors.append("real_session_ref_required")
    if session.meter_scope != "whole_system_ac_input":
        errors.append("whole_system_ac_input_scope_required")
    if session.exclusive_pc_load_confirmed is not True:
        errors.append("exclusive_pc_load_confirmation_required")
    if session.same_cumulative_counter_confirmed is not True:
        errors.append("same_cumulative_counter_confirmation_required")

    unit = session.reading_unit.strip().lower() if isinstance(session.reading_unit, str) else ""
    if unit not in SUPPORTED_UNITS:
        errors.append("unsupported_reading_unit")

    before = session.reading_before
    after = session.reading_after
    numeric_before = isinstance(before, (int, float)) and not isinstance(before, bool)
    numeric_after = isinstance(after, (int, float)) and not isinstance(after, bool)
    if not numeric_before or float(before) < 0:
        errors.append("invalid_reading_before")
    if not numeric_after or float(after) < 0:
        errors.append("invalid_reading_after")
    if numeric_before and numeric_after:
        if float(after) < float(before):
            errors.append("meter_counter_wrap_reset_or_negative_delta")
        elif float(after) == float(before):
            errors.append("positive_measurable_energy_delta_required")
    if isinstance(session.task_count, bool) or not isinstance(session.task_count, int) or session.task_count <= 0:
        errors.append("positive_task_count_required")

    if errors:
        return BridgeResult(
            state="PASS_BLOCKED",
            errors=tuple(sorted(set(errors))),
            energy_before_joules=None,
            energy_after_joules=None,
            energy_delta_joules=None,
            energy_kwh_per_task=None,
            energy_task_count=None,
            energy_source_ref=None,
            source_content_digest=None,
            i166_energy_fields_ready=False,
        )

    before_j = _convert_to_joules(float(before), unit)
    after_j = _convert_to_joules(float(after), unit)
    delta_j = after_j - before_j
    per_task = delta_j / JOULES_PER_KWH / session.task_count
    binding = {
        "schema": SCHEMA,
        "meter_source_ref": session.meter_source_ref,
        "meter_source_digest": session.meter_source_digest,
        "meter_scope": session.meter_scope,
        "exclusive_pc_load_confirmed": True,
        "same_cumulative_counter_confirmed": True,
        "reading_unit": unit,
        "reading_before": float(before),
        "reading_after": float(after),
        "task_count": session.task_count,
        "session_ref": session.session_ref,
    }
    digest = _digest(binding)
    source_ref = f"external-meter:{session.session_ref}:sha256:{digest}"

    return BridgeResult(
        state="EXTERNAL_METER_ENERGY_FIELDS_READY",
        errors=(),
        energy_before_joules=before_j,
        energy_after_joules=after_j,
        energy_delta_joules=delta_j,
        energy_kwh_per_task=per_task,
        energy_task_count=session.task_count,
        energy_source_ref=source_ref,
        source_content_digest=digest,
        i166_energy_fields_ready=True,
    )


def i166_energy_fields(result: BridgeResult) -> dict[str, Any]:
    if result.state != "EXTERNAL_METER_ENERGY_FIELDS_READY" or not result.i166_energy_fields_ready:
        raise ValueError("external_meter_bridge_not_ready")
    return {
        "energy_before_joules": result.energy_before_joules,
        "energy_after_joules": result.energy_after_joules,
        "energy_task_count": result.energy_task_count,
        "energy_source_ref": result.energy_source_ref,
    }


def payload(result: BridgeResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I182",
        "i166_energy_fields": i166_energy_fields(result) if result.i166_energy_fields_ready else None,
        "safety_boundary": (
            "I182 does not read a meter or prove that supplied readings are truthful. It only validates scope, "
            "provenance structure and arithmetic. The real user must bind genuine meter readings to the actual "
            "owned-PC workload session."
        ),
        "next_gate": (
            "Merge i166_energy_fields into a separate working measurement JSON together with independently real "
            "availability, tariff and opportunity-cost provenance, then let I166/I162 validate the complete packet."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    raw = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("input_json_must_be_object")
    result = bridge_external_meter(ExternalMeterSession(**raw))
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.i166_energy_fields_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
