# I186 — generic ResourceEvidence energy adapter audit

Date: 2026-08-24
Status: **completed source audit; concrete independent defect confirmed**

## Scope
Audit `implementation/resource_evidence_adapter.py` independently of the hardened I129 receipt route. This is the exact repository-side audit requested by I185/STATUS; no discovery was reopened.

## Finding
`build_resource_evidence(..., energy_measurement=...)` currently checks only:

`energy_kwh_per_task < 0 or tariff_usd_per_kwh < 0`

and then emits:

`round(float(energy_kwh_per_task) * float(tariff_usd_per_kwh), 12)`.

This is not fail-closed for arbitrary `EnergyMeasurement` callers:

1. IEEE `NaN` compares false to `< 0`, so NaN energy or tariff can pass the nonnegative check and produce NaN electricity evidence.
2. Positive infinity can pass and produce infinite electricity evidence.
3. A zero `energy_kwh_per_task` is accepted directly even though the real measurement routes now require a strictly positive measured delta/per-task energy; this can reintroduce artificial zero electricity cost through a caller that bypasses I129.
4. Tiny positive energy × tariff can round/underflow to `0.0`, again creating an artificial zero electricity cost.
5. Boolean/nonnumeric values are not normalized through an explicit finite-number contract and may either be treated numerically or fail inconsistently.

The existing adapter regression only covers a negative energy input and a short digest. It does not cover NaN, infinity, zero, underflow/round-to-zero, booleans or malformed numeric types.

## Required patch contract
Before emitting `electricity_per_task_usd`, the generic adapter must independently require:
- numeric non-boolean finite `energy_kwh_per_task`;
- **strictly positive** `energy_kwh_per_task` for measured-local evidence;
- numeric non-boolean finite non-negative tariff;
- finite multiplication result;
- finite **strictly positive** emitted electricity cost after the adapter's chosen precision policy, unless a separately justified explicit zero-tariff provenance contract is designed (none exists today).

The patch must add focused regressions for NaN/+inf/-inf, zero energy, multiplication overflow, precision/round-to-zero, bool/nonnumeric inputs and a valid finite-positive case. It must preserve provenance/digest/source-kind behavior and must not weaken I169/I050/I123 gates.

## Conclusion
A concrete independent defect **was found**, so one further repository-side hardening stage is justified before waiting exclusively for owned-PC evidence. I129 hardening alone does not protect every adapter caller.

## Safety
No market/API call, credentials, CI dispatch, device access, install, privilege escalation, paid infrastructure, task acceptance, spend, settlement or value movement occurred.

## Next action
Patch `resource_evidence_adapter.py` itself to enforce the contract above and expand `test_resource_evidence_adapter.py`. After that, if no further concrete repository-side defect is identified, stop adding layers and await genuine I181/I182/I179 owned-PC evidence.
