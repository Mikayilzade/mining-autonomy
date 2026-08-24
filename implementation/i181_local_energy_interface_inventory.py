#!/usr/bin/env python3
"""I181 inert local energy-interface inventory for the owned-PC measurement path.

This module does not measure task energy and never creates I166 evidence. It only
inspects already-present local operating-system interfaces and reports whether a
cumulative energy-counter candidate exists that could later be validated and used for
before/after readings on the actual owned PC.

No network access, package installation, subprocess execution, credentials, elevated
privileges, CI dispatch, market action, spend or value movement is performed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import os
from pathlib import Path
import platform
from typing import Any, Iterable

SCHEMA = "mining-autonomy/i181-local-energy-interface-inventory/v1"


@dataclass(frozen=True)
class EnergyInterfaceCandidate:
    interface_kind: str
    path: str
    unit: str
    cumulative_counter: bool
    system_scope: str
    readable: bool
    i166_before_after_candidate: bool
    requires_counter_semantics_validation: bool
    notes: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class InventoryResult:
    state: str
    system: str
    candidates: tuple[EnergyInterfaceCandidate, ...]
    blockers: tuple[str, ...]
    cumulative_candidate_count: int
    direct_i166_candidate_count: int
    evidence_created: bool = False
    energy_value_read: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    subprocess_used: bool = False
    software_installed: bool = False
    elevated_privileges_requested: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False


def _safe_text(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return text or None


def _relative(root: Path, path: Path) -> str:
    try:
        rel = path.relative_to(root)
        return "/" + rel.as_posix()
    except Exception:
        return path.as_posix()


def _readable(path: Path) -> bool:
    try:
        return path.is_file() and os.access(path, os.R_OK)
    except Exception:
        return False


def _linux_candidates(root: Path) -> tuple[EnergyInterfaceCandidate, ...]:
    rows: list[EnergyInterfaceCandidate] = []

    powercap = root / "sys" / "class" / "powercap"
    if powercap.exists():
        for counter in sorted(powercap.rglob("energy_uj")):
            parent = counter.parent
            metadata: dict[str, Any] = {}
            name = _safe_text(parent / "name")
            max_range = _safe_text(parent / "max_energy_range_uj")
            if name is not None:
                metadata["name"] = name
            if max_range is not None:
                metadata["max_energy_range_uj"] = max_range
            readable = _readable(counter)
            rows.append(EnergyInterfaceCandidate(
                interface_kind="linux_powercap_energy_uj",
                path=_relative(root, counter),
                unit="microjoule",
                cumulative_counter=True,
                system_scope="package_or_power_domain",
                readable=readable,
                i166_before_after_candidate=readable,
                requires_counter_semantics_validation=True,
                notes=(
                    "Kernel powercap cumulative energy counter candidate. Before use, validate that the domain "
                    "covers the intended workload, account for wraparound using max_energy_range_uj when present, "
                    "and bind exact before/after readings to the same task session."
                ),
                metadata=metadata,
            ))

    hwmon = root / "sys" / "class" / "hwmon"
    if hwmon.exists():
        for device in sorted(path for path in hwmon.iterdir() if path.is_dir()):
            device_name = _safe_text(device / "name")
            for counter in sorted(device.glob("energy*_input")):
                readable = _readable(counter)
                metadata = {"hwmon_name": device_name} if device_name else {}
                rows.append(EnergyInterfaceCandidate(
                    interface_kind="linux_hwmon_energy_input",
                    path=_relative(root, counter),
                    unit="microjoule",
                    cumulative_counter=True,
                    system_scope="device_or_sensor_domain",
                    readable=readable,
                    i166_before_after_candidate=readable,
                    requires_counter_semantics_validation=True,
                    notes=(
                        "hwmon cumulative energy candidate. Validate the specific driver's documented semantics, "
                        "counter scope and wrap behavior before treating readings as task energy."
                    ),
                    metadata=metadata,
                ))
            for power in sorted(device.glob("power*_input")):
                readable = _readable(power)
                metadata = {"hwmon_name": device_name} if device_name else {}
                rows.append(EnergyInterfaceCandidate(
                    interface_kind="linux_hwmon_power_input",
                    path=_relative(root, power),
                    unit="microwatt",
                    cumulative_counter=False,
                    system_scope="device_or_sensor_domain",
                    readable=readable,
                    i166_before_after_candidate=False,
                    requires_counter_semantics_validation=True,
                    notes=(
                        "Instantaneous power is not a before/after cumulative energy counter. I181 does not "
                        "integrate samples or convert this interface into I166 energy evidence."
                    ),
                    metadata=metadata,
                ))

    power_supply = root / "sys" / "class" / "power_supply"
    if power_supply.exists():
        for supply in sorted(path for path in power_supply.iterdir() if path.is_dir()):
            energy_now = supply / "energy_now"
            if energy_now.is_file():
                readable = _readable(energy_now)
                supply_type = _safe_text(supply / "type")
                metadata = {"supply_type": supply_type} if supply_type else {}
                rows.append(EnergyInterfaceCandidate(
                    interface_kind="linux_power_supply_energy_now",
                    path=_relative(root, energy_now),
                    unit="microwatt_hour",
                    cumulative_counter=False,
                    system_scope="battery_stored_energy",
                    readable=readable,
                    i166_before_after_candidate=False,
                    requires_counter_semantics_validation=True,
                    notes=(
                        "Battery stored-energy state is not a monotonic workload energy counter; charging, other "
                        "system load and battery behavior confound task attribution. It is not accepted directly."
                    ),
                    metadata=metadata,
                ))

    return tuple(rows)


def inventory_local_energy_interfaces(
    *,
    root: Path = Path("/"),
    system: str | None = None,
) -> InventoryResult:
    system_name = (system or platform.system() or "Unknown").strip()
    normalized = system_name.lower()
    blockers: list[str] = []

    if normalized == "linux":
        candidates = _linux_candidates(root)
    else:
        candidates = ()
        if normalized == "windows":
            blockers.append("no_supported_stdlib_cumulative_energy_counter_detector_for_windows")
        elif normalized == "darwin":
            blockers.append("no_supported_inert_cumulative_energy_counter_detector_for_macos")
        else:
            blockers.append("unsupported_operating_system_for_energy_interface_inventory")

    cumulative = tuple(row for row in candidates if row.cumulative_counter and row.readable)
    direct = tuple(row for row in candidates if row.i166_before_after_candidate)

    if direct:
        state = "CUMULATIVE_COUNTER_CANDIDATES_FOUND"
        blockers.append("candidate_requires_real_before_after_session_and_semantics_validation")
    elif candidates:
        state = "ONLY_NON_DIRECT_OR_UNREADABLE_INTERFACES_FOUND"
        blockers.append("no_readable_cumulative_counter_candidate_for_i166")
    else:
        state = "NO_SUPPORTED_LOCAL_ENERGY_INTERFACE_FOUND"
        if normalized == "linux":
            blockers.append("no_known_powercap_hwmon_or_power_supply_energy_interface_found")

    return InventoryResult(
        state=state,
        system=system_name,
        candidates=candidates,
        blockers=tuple(sorted(set(blockers))),
        cumulative_candidate_count=len(cumulative),
        direct_i166_candidate_count=len(direct),
    )


def payload(result: InventoryResult) -> dict[str, Any]:
    body = asdict(result)
    body["candidates"] = [asdict(row) for row in result.candidates]
    body.update({
        "schema": SCHEMA,
        "run": "I181",
        "safety_boundary": (
            "A detected interface is only a candidate. I181 never reads an energy value and never creates I166 "
            "evidence. A later real user-PC session must validate counter semantics and record genuine before/after "
            "readings plus task count and provenance."
        ),
        "next_gate": (
            "If CUMULATIVE_COUNTER_CANDIDATES_FOUND on the actual owned PC, validate one counter's scope/wrap "
            "semantics and use explicit before/after readings around the I163/I173 workload. Otherwise keep the "
            "energy blocker explicit rather than estimating it."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/")
    parser.add_argument("--system")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = inventory_local_energy_interfaces(root=Path(args.root), system=args.system)
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
