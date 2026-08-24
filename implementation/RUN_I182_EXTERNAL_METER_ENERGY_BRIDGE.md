# I182 — External physical-meter energy bridge

## Status
Completed repository-side fail-closed checkpoint. Real meter readings are still required on the actual owned PC.

## Purpose
Remove a distinct owned-PC energy-measurement blocker when I181 finds no trustworthy built-in cumulative energy counter. I182 provides a safe path for an already-available external physical watt/energy meter without purchasing hardware, reading devices automatically, or estimating energy.

## Added
- `implementation/i182_external_meter_energy_bridge.py`
- `implementation/test_i182_external_meter_energy_bridge.py`

## Contract
I182 accepts only caller-supplied cumulative before/after readings in `joule`, `Wh`, or `kWh` and converts them to the joule fields already required by I166/I162.

Promotion to `EXTERNAL_METER_ENERGY_FIELDS_READY` requires:
- `meter_scope == whole_system_ac_input`;
- explicit confirmation that the PC was the exclusive measured load during the session;
- explicit confirmation that before/after came from the same cumulative counter;
- a strictly positive measurable delta (zero delta is blocked to avoid treating meter resolution as zero electricity cost);
- positive task count;
- real non-placeholder/non-estimated meter and session references;
- a source-content digest.

Component-only meters, instantaneous-power readings, shared-load sessions, counter reset/wrap, unsupported units, placeholders, estimates/inferences and zero-resolution sessions fail closed.

## Output boundary
When valid, I182 emits only the four fields I166 already expects:
- `energy_before_joules`
- `energy_after_joules`
- `energy_task_count`
- `energy_source_ref`

It also emits a deterministic session/source digest for audit binding. It does not fill availability, tariff, opportunity cost, accounting facts, benchmark facts or any market economics.

## Relationship to existing code
- I181 answers whether a local cumulative counter candidate exists.
- I182 supplies an alternative conversion/provenance bridge when the real machine has no suitable local counter but the user already has a trustworthy external whole-system cumulative meter.
- I129 already accepts independently observed joule readings for the older `python_local` receipt path; I182 does not replace I129 and does not relax I166/I162.
- I166/I162 remain the authority for complete real owned-PC materialization.

## Verification
Seven focused test functions were authored covering kWh/Wh/joule conversion, I166 field shape, scope/exclusivity, provenance, counter reset, task count, zero-delta blocking and inert safety flags.

Exact raw Git materialization from this execution host could not be performed because DNS access to `raw.githubusercontent.com` is unavailable. Therefore this run **does not claim an exact-local pytest PASS** for I182. No CI workflow was dispatched merely to obtain a green result.

Current Git blobs after hardening:
- I182 module: `eab56be15068a67fa893e047b3d329ea83900148`
- I182 tests: `5690c6b754b64fc7d511a15ec691a38a9aafee20`

## Safety
No network/API market call, credentials, subprocess-based device access, software install, elevation, account creation, hardware purchase, CI dispatch, paid infrastructure, task acceptance/submission, spend, settlement, payment or value movement was performed.

## Result
A missing built-in energy counter no longer implies that the repository has no safe measurement route. If an already-available trustworthy whole-system cumulative external meter exists, genuine readings can be converted into the exact I166/I162 joule shape without estimation. If neither a local counter nor an external meter exists, the energy blocker remains explicit.

## Next action
The genuine forward path remains on the actual owned PC: run I181; use a validated local counter if available, otherwise use I182 only with a real already-available whole-system cumulative meter; then supply real tariff, availability, opportunity-cost and accounting provenance and run exact I178/I179. Do not buy measurement hardware or infer energy without separate authorization.
