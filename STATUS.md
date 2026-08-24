# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I191 — Resource Router semantic-domain hardening**
Last updated: **2026-08-25**

## Latest durable files
- `implementation/RUN_I191_RESOURCE_ROUTER_SEMANTIC_DOMAIN_HARDENING.md`
- `implementation/test_i191_resource_router_semantic_domains.py`
- `implementation/resource_router.py`
- `implementation/RUN_I190_CONSERVATIVE_ECONOMICS_DOMAIN_AUDIT.md`
- `implementation/RUN_I189_I123_BOOLEAN_CONTROL_HARDENING.md`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/test_i189_i123_boolean_control_hardening.py`
- `implementation/RUN_I188_RESOURCE_ROUTER_NUMERIC_HARDENING.md`
- `implementation/test_i188_resource_router_numeric_hardening.py`
- `implementation/RUN_I187_GENERIC_ENERGY_ADAPTER_HARDENING.md`
- `implementation/resource_evidence_adapter.py`
- `implementation/RUN_I185_I129_ENERGY_RECEIPT_NUMERIC_HARDENING.md`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/RUN_I181_LOCAL_ENERGY_INTERFACE_INVENTORY.md`
- `implementation/i181_local_energy_interface_inventory.py`
- `implementation/i180_user_pc_handoff_package.py`
- `implementation/i179_user_pc_real_chain_runner.py`
- `implementation/i178_user_pc_handoff_manifest.py`

## I191 outcome
I190's concrete conservative-economics fail-open defect is patched in the base Resource / Execution Router. Finite but semantically invalid values are no longer silently repaired into optimistic economics.

The Router now:
- requires backend reliability/quality and task acceptance/dispute/nonpayment/minimum-success probabilities in `[0,1]`;
- treats `platform_fee_rate` explicitly as a fraction in `[0,1]`;
- rejects negative payout, fees, marginal resource costs, energy/API/retry/maintenance/opportunity costs, units, fixed cost, quota/capacity, latency and rate-limit values where negative semantics are unsupported;
- requires a positive allocation basis when a non-sunk positive fixed cost must be allocated;
- preserves signed minimum expected-margin thresholds for now (intentional policy thresholds, not measured economic inputs);
- preserves dry-run-only routing and all existing authorization/value-movement blockers.

Focused staged verification for I191: **29 passed in 0.18s**. No CI workflow was dispatched.

## Retained safety/correctness chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129/generic I054 energy evidence -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> hardened I048/I188/I191 -> hardened I123/I189 -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

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
Do a narrow post-I191 downstream re-audit of the direct I123 -> conservative economics/readiness boundary for remaining concrete fail-open behavior, especially source/evidence promotion and signed-threshold semantics. Do not add packaging layers around absent real evidence.

The next genuine forward step remains on the actual owned PC: run I181; use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter; supply genuine applicable tariff, availability, opportunity-cost and accounting provenance; run exact I178 then exact I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
