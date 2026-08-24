# I182 — Windows EMI preflight

Date: 2026-08-24
Status: **completed repository-side preflight checkpoint**

## Goal
Remove a distinct gap left by I181: Windows was previously fail-closed because the stdlib-only inventory had no supported cumulative-energy detector.

## Result
Added `i182_windows_emi_preflight.py`, which uses Windows SetupAPI only to enumerate present devices implementing the standard Energy Metering Interface (EMI) GUID `{45BD8344-7ED6-49CF-A440-C276C933B053}`. It deliberately does **not** open the device or call `IOCTL_EMI_GET_MEASUREMENT`.

Microsoft documents EMI as available starting with Windows 10, with accumulated `AbsoluteEnergy` measurements and before/after subtraction as the intended energy-consumption method. Discovery is through the EMI device-interface GUID. This makes EMI a legitimate candidate path when the actual PC exposes compatible hardware/driver support, but presence alone is not energy evidence.

## Safety boundary
- no energy value read;
- no I166 evidence created;
- no subprocess/PowerShell/vendor utility;
- no install/elevation;
- no network/credentials/CI/spend/value movement.

## Verification
Six focused tests are authored for non-Windows, candidate-found, no-candidate, discovery-error, invalid-count and safety-boundary behavior. They use injected counters and therefore do not pretend to test Windows SetupAPI on this Linux execution host. Native Windows execution remains required to validate actual device enumeration.

Current source blobs:
- module: `a1b031108413c02a364a01dea6bfa4d9492e2885`
- tests: `09827dab6369f1a74f49707cee847464fad77218`

## Risk / interpretation
An EMI device can meter a rail/domain rather than necessarily the whole PC. A future reader must inspect EMI metadata/version/unit and bind the exact channel/domain to the workload before using before/after values. If no EMI device exists, keep energy blocked or use a separately provenance-bound physical meter; do not estimate.

## Next action
Run I181 plus I182 on the actual owned PC. If Windows EMI candidates exist, implement a narrowly scoped read-only EMI metadata/measurement adapter with explicit unit conversion and before/after session binding. If none exist, do not add speculative software layers merely to manufacture an energy estimate.

Primary documentation used: Microsoft Learn, Energy Meter Interface / EMI IOCTL reference, checked 2026-08-24.
