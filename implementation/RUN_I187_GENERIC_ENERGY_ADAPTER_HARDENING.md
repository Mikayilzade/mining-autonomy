# I187 — generic ResourceEvidence energy adapter hardening

Date: 2026-08-24
Status: **completed repository-side safety checkpoint**

## Scope
Close the concrete independent defect documented by I186 in `resource_evidence_adapter.build_resource_evidence()` without reopening discovery or changing downstream authorization gates.

## Changes
`implementation/resource_evidence_adapter.py` now independently validates generic `EnergyMeasurement` arithmetic even when the caller did not come through hardened I129:

- energy and tariff must be numeric `int`/`float`, non-boolean and finite;
- measured `energy_kwh_per_task` must be strictly positive;
- tariff must be non-negative;
- the raw energy × tariff product must remain finite;
- the emitted value after the adapter's 12-decimal precision policy must be finite and strictly positive;
- a zero tariff/product is blocked because no separate provenance contract currently proves a genuine zero electricity tariff;
- provenance, digest, source-kind, age and duplicate-parameter behavior is unchanged.

`implementation/test_resource_evidence_adapter.py` adds focused regressions for:

- NaN / +Infinity / -Infinity energy;
- NaN / +Infinity / -Infinity tariff;
- bool and nonnumeric energy/tariff;
- zero measured energy;
- zero tariff without a dedicated provenance contract;
- multiplication overflow;
- positive cost that rounds to zero;
- a small representable finite-positive cost;
- the existing valid finite-positive measured-local case remains covered.

## Source bindings
- hardened adapter blob: `19b2c482e4b2edcf1fe8129b183d1b0a0ebe992d`
- expanded adapter test blob: `e2f4b2415b006c5e342a2d86665a41acde761b9e`

## Verification
A network-free isolated arithmetic sanity check covering valid finite-positive values plus zero, NaN/infinity, bool, overflow, round-to-zero and zero-tariff cases passed in the current execution environment.

A complete byte-identical pytest dependency closure was not materialized in this run, so this checkpoint does **not** falsely claim the full `test_resource_evidence_adapter.py` suite was executed. CI was not dispatched merely to obtain a green status.

## Outcome
The I186 generic-adapter defect is patched. Hardened I129 is no longer the only protection against non-finite/artificial-zero electricity evidence reaching the Resource / Execution Router through `EnergyMeasurement`.

The remaining blockers are real-world evidence blockers rather than this repository arithmetic defect: actual owned-PC energy interface/meter availability, genuine availability/tariff/opportunity-cost/accounting provenance, and later separately authorized market observation/economic testing.

## Safety
No production market/API request, credentials, device access, install, privilege escalation, paid infrastructure, hardware purchase, CI dispatch, task acceptance/submission, settlement, spend or value movement occurred.

## Next action
Do not add another packaging layer unless a new concrete correctness/safety defect is found. The genuine forward step is to run I181 on the actual owned PC. Use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative meter; then supply genuine tariff/availability/opportunity-cost/accounting provenance and run exact I178/I179.
