# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I189 — I123 boolean/control-plane hardening**
Last updated: **2026-08-25**

## Latest durable files
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

## I189 outcome
I189 closes a distinct fail-open control-plane defect in the direct I123 Resource / Execution Router consumer. Runtime type annotations did not enforce booleans, so truthy strings/integers could be interpreted as backend policy/availability/sunk-cost or evidence/authorization facts.

I123 now requires exact `bool` values for backend control fields and all evidence/authorization flags, validates non-empty identities, rejects duplicate backend ids, and requires `ai_allowed` to be a real boolean. In particular, values such as `policy_allowed="false"`, `programmatic_access="false"`, `sunk_or_already_committed="false"`, or `ai_allowed="false"` now fail closed instead of being interpreted by Python truthiness.

Current blobs:
- hardened `i123_execution_backend_portfolio.py`: `fa7de3bdc814adec81496d938ebd8814bff504ad`
- I189 regressions: `f91bfb1ca6004c3a987d06e2719d482f5453ba65`

Focused regressions are authored. This run does **not** claim a byte-identical full pytest PASS because raw GitHub/DNS materialization remains unavailable in the execution host and CI was not dispatched merely for status.

## I188 retained outcome
I188 hardened the base I048 Router against non-finite/nonnumeric arithmetic, boolean numeric values, overflow, malformed quota/capacity/probability/latency/rate-limit inputs and invalid parallelism before I123 routing.

Current blobs:
- `resource_router.py`: `366a7d5071db02276ecd10d4c66eb3012a4ea7e2`
- I188 regressions: `5447f4c80c845e84d023ede3f48bbb9aa3e779aa`

## Retained Resource / Execution Router chain
`I113 PASS_BLOCKED -> resource evidence ladder -> I159–I166 owned-PC materialization -> I167/I168 Router facts -> I173/I174/I175 production interface proof -> I181 local-counter preflight OR hardened I182 external-meter route -> hardened I129/generic I054 energy adapter -> I180/I178/I179 handoff -> I177/I169 readiness -> exact I050 -> I066 -> hardened I048/I188 -> hardened I123/I189 -> conservative economics/readiness -> separately authorized bounded observation -> economic-test packet`.

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
The I123 boolean/control-plane fail-open path is closed. Do **not** add another packaging/abstraction layer unless a new distinct correctness/safety defect is identified.

The next genuine forward step is on the actual owned PC:
1. run I181;
2. use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter;
3. supply genuine applicable tariff, availability, opportunity-cost and accounting provenance;
4. run exact I178 then exact I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization.

Until a real I179 result exists, repository-side work should proceed only on concrete fail-open/correctness defects in direct downstream Router/economics/readiness consumers. A useful next audit is the first conservative economics/readiness consumer after I123, checking runtime type/finite handling and source-class promotion without changing authorization boundaries.

After a genuine I179/I177 result, proceed only through the existing exact I050 -> I066 -> hardened Router/I123 -> conservative economics/readiness gates. Do not apply any I050/I123 hybrid patch unless exactly the two accounting declarations remain as the only source-class blocker and I176 has first been rebound to then-current sources.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass. Do not estimate missing real-world evidence.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
