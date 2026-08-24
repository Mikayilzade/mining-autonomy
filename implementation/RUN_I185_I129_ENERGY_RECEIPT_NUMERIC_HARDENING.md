# I185 — I129 local-energy receipt numeric hardening

Date: 2026-08-24
Status: **completed repository-side safety checkpoint; focused regressions authored**

## Purpose
Close a distinct fail-closed numeric gap found by auditing the older I129 `python_local` energy-receipt path after I182/I183/I184 hardened the external-meter path.

I129 previously documented zero/invalid energy as blocked, but its implementation still allowed `energy_after == energy_before`, accepted non-finite floats (`NaN`/infinity) through ordinary comparisons, accepted non-finite tariffs, and could underflow/crash on extreme task counts. That could permit an artificial zero/non-finite electricity cost to reach the Resource / Execution Router through `EnergyMeasurement`.

## Changes
- `implementation/i129_energy_measurement_receipt.py`
  - requires integer, non-boolean positive `task_count` and `max_age_seconds`;
  - validates text/provenance fields without unsafe `.strip()` calls on non-strings;
  - requires finite non-negative before/after readings;
  - requires a finite **strictly positive** measured energy delta;
  - requires finite non-negative tariff;
  - computes per-task energy fail-closed and requires finite strictly positive kWh/task;
  - normalizes malformed observation timestamps to the existing UTC validation error.
- `implementation/test_i129_energy_measurement_receipt.py`
  - expands regression coverage for zero delta, NaN/infinity readings, NaN/infinity tariff, extreme task-count underflow, bool/non-integer counts, malformed timestamps/max-age values and valid finite-positive preservation.

## Source bindings
- hardened I129 module blob: `9d4b9d9c089e17d333746f0fbd9a025b3c63b1bc`
- expanded I129 test blob: `7f6ebf970d221bef9fcd12a0c1cb19d7d43397a4`

The current automation environment does not contain a complete byte-identical local checkout of I129's dependency closure (`resource_evidence_adapter`, calibration/profile modules). CI was not dispatched merely to obtain a green status. Therefore this checkpoint records the regression suite as **authored, not falsely claimed executed**.

## Outcome
The direct I129 receipt builder can no longer create a zero/non-finite per-task energy measurement from a zero delta, non-finite raw values/tariff or arithmetic underflow. This removes a real alternate-path integrity defect rather than adding another handoff/package layer.

The real forward path is unchanged: run I181 on the actual owned PC; obtain genuine before/after readings from a validated local cumulative counter or already-available whole-system external meter; supply genuine tariff/availability/opportunity-cost/accounting provenance; then run exact I178/I179.

## Residual risk / next action
`resource_evidence_adapter.build_resource_evidence()` still deserves a separate fail-closed audit because it accepts `EnergyMeasurement` objects from sources other than I129. Do not assume I129 hardening alone proves every possible adapter caller finite. A future repository-side stage is justified only if that audit identifies a concrete independent gap; otherwise await real owned-PC evidence.

## Safety
No production market/API request, credentials, subprocess device access, software install, privilege escalation, hardware purchase, paid infrastructure, CI dispatch, task acceptance/submission, settlement, spend or value movement occurred.
