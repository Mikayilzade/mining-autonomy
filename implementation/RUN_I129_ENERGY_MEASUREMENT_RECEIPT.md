# Implementation Run I129 — verifiable local energy measurement receipt

Date: 2026-08-23
Status: **COMPLETED AS SOURCE CHECKPOINT — REAL MEASUREMENT PENDING**
Phase: Implementation / Experiment

## Objective
Remove the last loose/manual shape around `electricity_per_task_usd` without inventing an energy value or tariff, so the next executable checkout can turn trustworthy no-spend host telemetry into the exact I054/I128 evidence type.

## Work performed
Added `i129_energy_measurement_receipt.py` and focused negative/conversion tests.

I129 accepts only independently observed before/after energy-counter readings in joules, a positive task count, exact workload identity, counter provenance/digest, an explicit electricity tariff plus tariff provenance/digest, UTC observation time and freshness window. It computes the energy delta and kWh/task, binds the full packet to a canonical SHA-256 receipt, re-verifies the receipt, then converts it to the existing `EnergyMeasurement` consumed by I054/I128.

## Fail-closed properties
- no zero-task division or inferred workload count;
- no negative counter values;
- counter reset/wrap (`after < before`) is rejected rather than guessed;
- meter/source identity and content digest are mandatory;
- tariff is never guessed and requires independent explicit provenance;
- stale, future, tampered or scope-mismatched receipts fail;
- receipt is exact `python_local` only;
- receipt does not claim that a hardware counter measures whole-machine energy unless its source actually establishes that;
- no meter reading is fabricated when the host exposes no trustworthy telemetry.

## Economics meaning
I129 preserves the Resource Router distinction between fixed/sunk and marginal cost. It contributes only the marginal electricity component for the measured benchmark. It does not erase opportunity cost, hardware depreciation, subscription allocation, API cost, platform fees or other backend-specific costs.

## Runtime situation
A fresh public GitHub clone was attempted again from the available execution container during I129 and failed at DNS resolution (`Could not resolve host: github.com`). Therefore the exact-current repository still cannot be executed here and no measured energy/runtime PASS is claimed.

## Safety
No production market request, credentials, workflow dispatch, paid infrastructure, account creation, task acceptance/submission, KYC, wallet, deposit, spend or value movement occurred.

## Next broad stage
At the first exact-current executable checkout, run I128's fixed benchmark and I113 receipt. If trustworthy local energy telemetry is available, capture counter before/after around the fixed workload, build/verify an I129 receipt using an explicit real electricity tariff source, convert it to `EnergyMeasurement`, and feed it through I128 -> I050 -> I066 -> I123. If telemetry or tariff provenance is unavailable, keep electricity unknown.

Only after the resulting current non-synthetic Resource Router decision is positive should the separate market-observation authorization chain advance.