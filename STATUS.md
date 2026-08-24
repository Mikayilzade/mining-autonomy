# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I190 — conservative economics numeric-domain audit**
Last updated: **2026-08-25**

## Latest durable files
- `implementation/RUN_I190_CONSERVATIVE_ECONOMICS_DOMAIN_AUDIT.md`
- `implementation/RUN_I189_I123_BOOLEAN_CONTROL_HARDENING.md`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/test_i189_i123_boolean_control_hardening.py`
- `implementation/RUN_I188_RESOURCE_ROUTER_NUMERIC_HARDENING.md`
- `implementation/resource_router.py`
- `implementation/test_i188_resource_router_numeric_hardening.py`
- `implementation/RUN_I187_GENERIC_ENERGY_ADAPTER_HARDENING.md`
- `implementation/resource_evidence_adapter.py`
- `implementation/test_resource_evidence_adapter.py`
- `implementation/RUN_I185_I129_ENERGY_RECEIPT_NUMERIC_HARDENING.md`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/RUN_I184_EXTERNAL_METER_POSITIVE_ENERGY_HARDENING.md`
- `implementation/i182_external_meter_energy_bridge.py`
- `implementation/RUN_I181_LOCAL_ENERGY_INTERFACE_INVENTORY.md`
- `implementation/i181_local_energy_interface_inventory.py`
- `implementation/RUN_I180_USER_PC_HANDOFF_PACKAGE.md`
- `implementation/i180_user_pc_handoff_package.py`
- `implementation/i179_user_pc_real_chain_runner.py`
- `implementation/i178_user_pc_handoff_manifest.py`

## I190 outcome
The first conservative economics path downstream of I123 was audited for semantic numeric-domain handling. A distinct fail-open defect remains in `resource_router.py`: finite but impossible/out-of-domain probabilities are silently clamped into `[0,1]`, and several negative costs/fees are silently promoted to zero. Examples include `acceptance_probability=2`, `dispute_probability=-1`, or negative fee/cost inputs. This can create optimistic conservative economics rather than rejecting malformed evidence.

I190 documents a narrow patch contract in `implementation/RUN_I190_CONSERVATIVE_ECONOMICS_DOMAIN_AUDIT.md`. The defect is **identified, not yet patched**. Until patched, out-of-domain finite economics/probability inputs are not production-trustworthy.

## I189 retained outcome
I123 requires exact booleans for backend control fields and all evidence/authorization flags, validates non-empty identities, rejects duplicate backend ids, and requires `ai_allowed` to be a real boolean. Truthy strings/integers can no longer act as production facts or authorization.

## I188 retained outcome
I188 hardened the base I048 Router against non-finite/nonnumeric arithmetic, boolean numeric values, overflow, malformed quota/capacity/probability/latency/rate-limit inputs and invalid parallelism before I123 routing. I190 narrows the remaining gap to finite values outside valid semantic domains.

## Retained Resource / Execution Router chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129/generic I054 energy adapter -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> hardened I048/I188 -> hardened I123/I189 -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

Router rules remain mandatory: deterministic/local filtering first; AI only when needed; compare marginal cost separately from fixed/sunk cost and include quota/capacity, latency, reliability, quality, parallelism, rate limits, energy, API/model cost, retry/failure, maintenance, marketplace/payment fees, acceptance/dispute/nonpayment risk and opportunity cost. Subscription capabilities are fixed/sunk limited support, not a free unlimited API. Sub-hour watchers may only use permitted API/ToS paths: cheap polling -> local dedupe/filter -> selective AI.

## Current blockers
1. **I190 numeric-domain defect is not yet patched**; out-of-range finite probabilities and negative costs/fees can be silently repaired into optimistic economics.
2. I181 has not run on the actual owned PC; built-in cumulative-counter availability is unknown.
3. No genuine I166 packet exists; genuine availability, energy, applicable tariff and opportunity-cost provenance are not materialized.
4. If no local counter exists, I182 requires a genuine already-available whole-system cumulative external meter; no hardware purchase is authorized.
5. Two accounting controls require truthful provenance; declarations are not relabelled reproducible.
6. Exact I050/I066 for `owned_pc` is not yet evidence-permitted/materialized.
7. Real task payout, retries/failures, maintenance, platform/payment fees and acceptance/dispute/nonpayment economics remain unknown.
8. Current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**.
9. Authorization for bounded read-only production observation: **false**.

## Immediate next broad run
Patch the concrete I190 defect before any further economics/readiness promotion:
1. enforce `[0,1]` domains for all probability fields instead of clamping invalid finite values;
2. reject negative costs/fees/resource quantities where negative semantics are unsupported instead of converting them to zero;
3. add focused regressions for finite out-of-domain values while preserving valid routes;
4. do not alter I123 authorization/evidence boundaries or enable execution/value movement.

After that repository-side correctness checkpoint, the next genuine forward step remains on the actual owned PC: run I181; use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter; supply genuine applicable tariff, availability, opportunity-cost and accounting provenance; run exact I178 then exact I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
