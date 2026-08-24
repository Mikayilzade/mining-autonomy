# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I186 — generic ResourceEvidence energy adapter audit**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I186_GENERIC_ENERGY_ADAPTER_AUDIT.md`
- `implementation/RUN_I185_I129_ENERGY_RECEIPT_NUMERIC_HARDENING.md`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/test_i129_energy_measurement_receipt.py`
- `implementation/RUN_I184_EXTERNAL_METER_POSITIVE_ENERGY_HARDENING.md`
- `implementation/i182_external_meter_energy_bridge.py`
- `implementation/test_i182_external_meter_energy_bridge.py`
- `implementation/RUN_I181_LOCAL_ENERGY_INTERFACE_INVENTORY.md`
- `implementation/i181_local_energy_interface_inventory.py`
- `implementation/RUN_I180_USER_PC_HANDOFF_PACKAGE.md`
- `implementation/i180_user_pc_handoff_package.py`
- `implementation/i179_user_pc_real_chain_runner.py`
- `implementation/i178_user_pc_handoff_manifest.py`
- `implementation/resource_evidence_adapter.py`
- `implementation/test_resource_evidence_adapter.py`
- `implementation/i123_execution_backend_portfolio.py`

## I186 outcome
The requested independent audit of `resource_evidence_adapter.build_resource_evidence()` found a concrete fail-closed defect. The generic `EnergyMeasurement` path accepts values without an independent finite-number contract: NaN/infinity can evade `< 0`, zero energy is accepted, and multiplication/rounding can yield non-finite or artificial zero electricity cost. This matters because callers other than hardened I129 can construct `EnergyMeasurement` directly.

I186 documents the exact patch contract and missing regressions. No production observation or value-moving action occurred. The defect is **confirmed but not yet patched**; therefore one further repository-side hardening stage is justified.

## Retained Resource / Execution Router chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129 where applicable -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> I123 Router -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

Router rules remain mandatory: deterministic/local filtering first; AI only when needed; compare marginal cost separately from fixed/sunk cost and include quota/capacity, latency, reliability, quality, parallelism, rate limits, energy, API/model cost, retry/failure, maintenance, marketplace/payment fees, acceptance/dispute/nonpayment risk and opportunity cost. Subscription capabilities are fixed/sunk limited support, not a free unlimited API. Sub-hour watchers may only use permitted API/ToS paths: cheap polling -> local dedupe/filter -> selective AI.

## Current blockers
1. **I186 defect:** generic `resource_evidence_adapter` energy arithmetic is not yet independently finite/positive fail-closed.
2. I181 has not run on the actual owned PC; built-in cumulative-counter availability is unknown.
3. No genuine I166 packet exists; genuine availability, energy, applicable tariff and opportunity-cost provenance are not materialized.
4. If no local counter exists, I182 requires a genuine already-available whole-system cumulative external meter; no hardware purchase is authorized.
5. Two accounting controls require truthful provenance; declarations are not relabelled reproducible.
6. Exact I050/I066 for `owned_pc` is not yet evidence-permitted/materialized.
7. Real task payout, retries/failures, maintenance, platform/payment fees and acceptance/dispute/nonpayment economics remain unknown.
8. Current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**.
9. Authorization for bounded read-only production observation: **false**.

## Immediate next broad run
Patch `resource_evidence_adapter.py` itself per I186: reject bool/nonnumeric/non-finite energy/tariff, require strictly positive measured per-task energy, reject non-finite multiplication and precision/round-to-zero output, and add focused regressions while preserving provenance/source-kind semantics. Decide explicitly how a genuine zero electricity tariff would be represented; absent a separate provenance contract, do not let a zero product silently become measured-local zero cost.

After that hardening, if no new concrete repository-side defect is identified, stop adding packaging layers and await the genuine owned-PC step: run I181; use a validated local cumulative counter if present or I182 only with an already-available trustworthy whole-system meter; supply genuine tariff/availability/opportunity-cost/accounting provenance; then run exact I178/I179.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
