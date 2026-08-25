# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I193 — I123 evidence-origin / authorization-promotion audit**
Last updated: **2026-08-25**

## Latest durable files
- `implementation/RUN_I193_I123_EVIDENCE_ORIGIN_AUDIT.md`
- `implementation/RUN_I192_RESOURCE_ROUTER_POSITIVE_MARGIN_HARDENING.md`
- `implementation/test_i192_resource_router_positive_margin.py`
- `implementation/resource_router.py`
- `implementation/RUN_I191_RESOURCE_ROUTER_SEMANTIC_DOMAIN_HARDENING.md`
- `implementation/test_i191_resource_router_semantic_domains.py`
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

## I193 outcome
A concrete direct-I123 source/evidence promotion gap is isolated.

I123 currently validates evidence/control booleans and conservative economics, but a caller can still self-label an in-memory `BackendEvidence` as `measured_reproducible` without a machine-checkable source artifact binding. Likewise `credentials_authorized`, `spend_authorized`, and `infrastructure_authorized` have strict boolean typing but no separate authorization-origin/reference contract.

This is not proof of an exposed remote exploit: the project remains dry-run and has no materialized real route. It is a fail-open correctness boundary because repository policy says declarations must not be relabelled reproducible and external authorization must be separately explicit.

I193 performed an audit only; it intentionally did not invent real provenance or authorization. No CI workflow was dispatched and no market/value-moving action occurred.

## Retained safety/correctness chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129/generic I054 energy evidence -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> hardened I048/I188/I191/I192 -> hardened I123/I189 -> I193 origin-boundary audit -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

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
9. I123 measured evidence and authorization flags are not yet bound to explicit machine-checkable origin/reference fields; I193 requires this to be hardened before relying on `production_route_ready` for a real test.

## Immediate next broad run
Implement the narrow I193 hardening contract in `implementation/i123_execution_backend_portfolio.py`: measured reproducible evidence must be source-bound; planning/declaration/synthetic origins must not promote; authorization booleans must require a separate explicit authorization-origin/reference; malformed origin metadata must fail closed. Add focused adversarial regressions and preserve all I191/I192 conservative economics invariants.

Do not add packaging layers around absent real evidence.

The next genuine forward step remains on the actual owned PC: run I181; use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter; supply genuine applicable tariff, availability, opportunity-cost and accounting provenance; run exact I178 then exact I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
