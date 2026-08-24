# I184 — external-meter positive-energy arithmetic hardening

Date: 2026-08-24
Status: **completed repository-side safety checkpoint**

## Purpose
Close a second concrete fail-closed numeric gap in the hardened I182 external-meter bridge without adding another evidence layer.

I183 rejected non-finite raw readings and conversion overflow, but two residual arithmetic cases could still undermine conservative energy accounting:
1. two distinct finite cumulative readings can collapse to the same floating-point joule value after Wh/kWh conversion, producing a zero converted delta even though the raw readings compare as increasing;
2. an extreme positive `task_count` can overflow/underflow Python float division and either raise or collapse per-task energy toward zero.

Either outcome must remain blocked rather than become an artificial zero electricity cost.

## Changes
- `implementation/i182_external_meter_energy_bridge.py`
  - validates converted joule delta after conversion, not only raw reading order;
  - requires converted delta to remain finite and strictly positive;
  - computes per-task energy inside fail-closed arithmetic handling;
  - requires per-task kWh to remain finite and strictly positive;
  - blocks arithmetic overflow/underflow rather than crashing or promoting zero energy.
- `implementation/test_i182_external_meter_energy_bridge.py`
  - adds a regression where `reading_after > reading_before` but kWh-to-joule conversion collapses both floats to the same value;
  - adds an extreme-task-count regression proving the bridge blocks instead of crashing/underflowing;
  - retains all previous scope, provenance, reset, zero-delta, non-finite, overflow and inert-safety tests.

## Exact-local verification
Exact byte-identical current Git content was materialized locally from the committed source payloads and Git blob SHA-checked before test execution.

- I182 module blob: `c0576d24e347e7880fd181be5f16caac30ba46ef`
- I182 tests blob: `bd32d9cb7b3c5507b1bb6a19a5aec8cfbf9990ae`
- focused result: **11 passed in 0.09s** with proxy/network environment variables removed.

A direct raw.githubusercontent.com fetch was unavailable because DNS resolution remained blocked in the execution environment; no CI workflow was dispatched merely to obtain a green result.

## Outcome
I182/I183/I184 now fail closed on raw non-finite readings, conversion overflow, conversion precision collapse, non-finite/non-positive converted delta, and per-task arithmetic overflow/underflow. The bridge still does not read or purchase a meter, prove caller truth, infer tariff/availability/opportunity cost, authorize I050/I066/I123, or perform a market/value-moving action.

The genuine forward step remains unchanged: run I181 on the actual owned PC; use a validated local cumulative counter if available, otherwise use I182 only with an already-available trustworthy whole-system cumulative external meter; then provide real tariff, availability, opportunity-cost and accounting provenance and run exact I178/I179.

## Risks / remaining blockers
- meter resolution/measurement uncertainty is still external provenance and is not inferred by I182;
- no genuine owned-PC energy session exists yet;
- no genuine I166 packet exists yet;
- downstream task-specific payout/fees/retry/acceptance/dispute economics remain blocked pending separately authorized real observation/testing.

## Next action
Do not add another packaging layer. Await/run the real owned-PC measurement path. Repository-side work should only continue if source audit reveals another distinct correctness/safety defect or if real I181/I182/I179 evidence exposes a new blocker.

## Safety
No production market/API request, credentials, subprocess device access, software install, privilege escalation, hardware purchase, paid infrastructure, CI dispatch, task acceptance/submission, settlement, spend or value movement occurred.
