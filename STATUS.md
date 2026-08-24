# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I187 — generic ResourceEvidence energy adapter hardening**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I187_GENERIC_ENERGY_ADAPTER_HARDENING.md`
- `implementation/resource_evidence_adapter.py`
- `implementation/test_resource_evidence_adapter.py`
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
- `implementation/i123_execution_backend_portfolio.py`

## I187 outcome
I187 patches the concrete generic-adapter defect confirmed by I186. `resource_evidence_adapter.build_resource_evidence()` no longer relies on hardened I129 callers to keep electricity evidence finite and non-artificial.

The generic `EnergyMeasurement` path now independently requires numeric non-boolean finite energy/tariff inputs, strictly positive measured per-task energy, non-negative tariff, finite multiplication, and a finite strictly positive emitted electricity cost after the adapter's 12-decimal precision policy. NaN/infinity, bool/nonnumeric values, zero measured energy, multiplication overflow, and positive values that round to zero fail closed.

A zero tariff/product is also blocked because no separate provenance contract currently establishes when a genuine zero electricity tariff may be promoted as reproducible measured-local cost. This avoids silently converting "unknown/free" semantics into zero marginal cost.

Regression coverage was expanded for all I186 cases plus valid small finite-positive preservation. Hardened current blobs:
- `resource_evidence_adapter.py`: `19b2c482e4b2edcf1fe8129b183d1b0a0ebe992d`
- `test_resource_evidence_adapter.py`: `e2f4b2415b006c5e342a2d86665a41acde761b9e`

A network-free isolated arithmetic sanity check passed. A complete byte-identical pytest dependency closure was not materialized, so no false full-suite PASS is claimed. No CI workflow was dispatched merely for status.

## Retained Resource / Execution Router chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129/generic I054 energy adapter -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> I123 Router -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

Router rules remain mandatory: deterministic/local filtering first; AI only when needed; compare marginal cost separately from fixed/sunk cost and include quota/capacity, latency, reliability, quality, parallelism, rate limits, energy, API/model cost, retry/failure, maintenance, marketplace/payment fees, acceptance/dispute/nonpayment risk and opportunity cost. Subscription capabilities are fixed/sunk limited support, not a free unlimited API. Sub-hour watchers may only use permitted API/ToS paths: cheap polling -> local dedupe/filter -> selective AI.

## Current blockers
1. I181 has not run on the actual owned PC; built-in cumulative-counter availability is unknown.
2. No genuine I166 packet exists; genuine availability, energy, applicable tariff and opportunity-cost provenance are not materialized.
3. If no local counter exists, I182 requires a genuine already-available whole-system cumulative external meter; no hardware purchase is authorized.
4. Two accounting controls require truthful provenance; declarations are not relabelled reproducible.
5. Exact I050/I066 for `owned_pc` is not yet evidence-permitted/materialized.
6. Real task payout, retries/failures, maintenance, platform/payment fees and acceptance/dispute/nonpayment economics remain unknown.
7. Current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**.
8. Authorization for bounded read-only production observation: **false**.

## Immediate next broad run
The I186 repository arithmetic blocker is closed. Do **not** add another packaging layer unless a new distinct correctness/safety defect is identified.

The next genuine forward step is on the actual owned PC:
1. run I181;
2. use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter;
3. supply genuine applicable tariff, availability, opportunity-cost and accounting provenance;
4. run exact I178 then exact I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization.

After a genuine I179/I177 result, proceed only through the existing exact I050 -> I066 -> I123 Router and conservative economics/readiness gates. Do not apply any I050/I123 hybrid patch unless exactly the two accounting declarations remain as the only source-class blocker and I176 has first been rebound to then-current sources.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
