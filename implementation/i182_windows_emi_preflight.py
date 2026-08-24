#!/usr/bin/env python3
"""I182 Windows Energy Metering Interface (EMI) preflight.

Discovers whether the local Windows machine exposes the standard EMI device-interface
GUID. It does NOT read energy measurements, install software, request elevation, use
credentials/network, or create I166 evidence. A discovered device is only a candidate
for a later explicit before/after measurement adapter.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import ctypes
from ctypes import wintypes
import json
import platform
from typing import Any, Callable

SCHEMA = "mining-autonomy/i182-windows-emi-preflight/v1"
EMI_GUID_TEXT = "45BD8344-7ED6-49CF-A440-C276C933B053"
DIGCF_PRESENT = 0x00000002
DIGCF_DEVICEINTERFACE = 0x00000010
ERROR_NO_MORE_ITEMS = 259
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


@dataclass(frozen=True)
class EmiPreflightResult:
    state: str
    system: str
    interface_guid: str
    candidate_count: int
    blockers: tuple[str, ...]
    energy_value_read: bool = False
    evidence_created: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    subprocess_used: bool = False
    software_installed: bool = False
    elevated_privileges_requested: bool = False
    spend_or_value_movement: bool = False


def _guid_from_text(text: str):
    import uuid
    raw = uuid.UUID(text).bytes_le
    class GUID(ctypes.Structure):
        _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8)]
    return GUID.from_buffer_copy(raw)


def _native_candidate_count() -> int:
    """Enumerate present EMI device interfaces through SetupAPI; read no meter values."""
    if platform.system().lower() != "windows":
        raise OSError("windows_required")
    setupapi = ctypes.WinDLL("setupapi", use_last_error=True)
    guid = _guid_from_text(EMI_GUID_TEXT)

    class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("InterfaceClassGuid", type(guid)),
                    ("Flags", wintypes.DWORD), ("Reserved", ctypes.c_void_p)]

    get_class = setupapi.SetupDiGetClassDevsW
    get_class.restype = ctypes.c_void_p
    get_class.argtypes = [ctypes.POINTER(type(guid)), wintypes.LPCWSTR,
                          wintypes.HWND, wintypes.DWORD]
    enum_if = setupapi.SetupDiEnumDeviceInterfaces
    enum_if.restype = wintypes.BOOL
    enum_if.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                        ctypes.POINTER(type(guid)), wintypes.DWORD,
                        ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)]
    destroy = setupapi.SetupDiDestroyDeviceInfoList
    destroy.restype = wintypes.BOOL
    destroy.argtypes = [ctypes.c_void_p]

    handle = get_class(ctypes.byref(guid), None, None, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE)
    if handle == INVALID_HANDLE_VALUE:
        raise OSError(ctypes.get_last_error(), "SetupDiGetClassDevsW_failed")
    count = 0
    try:
        while True:
            row = SP_DEVICE_INTERFACE_DATA()
            row.cbSize = ctypes.sizeof(row)
            ok = enum_if(handle, None, ctypes.byref(guid), count, ctypes.byref(row))
            if ok:
                count += 1
                continue
            error = ctypes.get_last_error()
            if error == ERROR_NO_MORE_ITEMS:
                break
            raise OSError(error, "SetupDiEnumDeviceInterfaces_failed")
    finally:
        destroy(handle)
    return count


def preflight_windows_emi(*, system: str | None = None,
                          counter: Callable[[], int] | None = None) -> EmiPreflightResult:
    system_name = (system or platform.system() or "Unknown").strip()
    if system_name.lower() != "windows":
        return EmiPreflightResult(
            state="NOT_WINDOWS", system=system_name, interface_guid=EMI_GUID_TEXT,
            candidate_count=0, blockers=("windows_emi_preflight_requires_windows",))
    try:
        count = int((counter or _native_candidate_count)())
        if count < 0:
            raise ValueError("negative_candidate_count")
    except Exception as exc:
        return EmiPreflightResult(
            state="EMI_DISCOVERY_FAILED", system=system_name, interface_guid=EMI_GUID_TEXT,
            candidate_count=0, blockers=(f"emi_discovery_error:{type(exc).__name__}",))
    if count:
        return EmiPreflightResult(
            state="EMI_DEVICE_CANDIDATES_FOUND", system=system_name,
            interface_guid=EMI_GUID_TEXT, candidate_count=count,
            blockers=("emi_candidate_requires_metadata_scope_and_measurement_semantics_validation",))
    return EmiPreflightResult(
        state="NO_EMI_DEVICE_INTERFACE_FOUND", system=system_name,
        interface_guid=EMI_GUID_TEXT, candidate_count=0,
        blockers=("no_present_windows_emi_device_interface",))


def payload(result: EmiPreflightResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA, "run": "I182",
        "source_basis": "Microsoft Windows Energy Metering Interface GUID_DEVICE_ENERGY_METER",
        "safety_boundary": (
            "Discovery only. No IOCTL_EMI_GET_MEASUREMENT call occurs, so no energy value or I166 evidence is created."
        ),
        "next_gate": (
            "If candidates are found on the actual owned PC, a later adapter may validate EMI version/metadata, "
            "confirm measurement scope/unit, and record explicit before/after AbsoluteEnergy values. Otherwise "
            "keep the energy blocker explicit or use a separately provenance-bound physical meter."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = preflight_windows_emi()
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        open(args.output, "w", encoding="utf-8").write(text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
