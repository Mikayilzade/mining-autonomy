# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I167 — owned-PC Router bridge**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I167_OWNED_PC_ROUTER_BRIDGE.md`
- `implementation/i167_owned_pc_router_bridge.py`
- `implementation/test_i167_owned_pc_router_bridge.py`
- `implementation/RUN_I166_USER_PC_REAL_EVIDENCE_GATE.md`
- `implementation/i166_user_pc_real_evidence_gate.py`
- `implementation/test_i166_user_pc_real_evidence_gate.py`
- `implementation/RUN_I164_I165_USER_PC_TEST_CLOSURE.md`
- `implementation/i165_user_pc_one_shot_materializer.py`
- `implementation/i164_fixed_benchmark_core.py`
- `implementation/i163_user_pc_benchmark_session.py`
- `implementation/i162_user_pc_measurement_procedure.py`
- `implementation/i159_owned_pc_evidence_packet.py`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/resource_router.py`

## I167 outcome
Added a fail-closed bridge from a future completed real I166 -> I165 -> I162 -> I159 owned-PC evidence chain into Router-shaped resource facts. I167 maps only facts that can be derived from accepted measurements: current availability, benchmark latency/reliability/quality/parallelism, energy-derived electricity cost per task, and latency-bound opportunity cost per task.

I167 deliberately does **not** promote its I123-shaped evidence candidate to production evidence. `current_reproducible=false` and `policy_evidence_current=false` remain until the existing I050/I066 attestation/evidence chain binds the source and policy state. It also leaves real task payout/acceptance criteria, platform/payment fees, dispute/nonpayment/acceptance probabilities, retry/failure cost, maintenance time/value, market policy/ToS/geography and observation/value-moving authorizations explicit downstream requirements.

The authored I167 module and focused tests were executed locally from the exact authored bytes: **3 passed**. Repository Git blob SHAs matched the local authored module and test bytes. This does not close the older I166 exact-source test blocker; the current execution runtime still cannot resolve/clone `github.com`, and no CI workflow was dispatched solely to obtain that result.

## I166 outcome
I166 remains the real-evidence gate in front of I165. It requires explicit user-PC ownership confirmation, complete availability/energy-counter/tariff/opportunity-cost groups, valid ranges/counter order, and non-placeholder provenance labels. It does not measure or infer those facts and cannot prove a provenance string is truthful. If no trustworthy joule counter/meter exists, energy remains blocked rather than estimated.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder/control pass -> I161/I162/I163/I164/I165/I166 real user-PC materialization -> I167 Router resource bridge -> I050/I066 attestation -> I123 Router -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. runtime regression: materially demonstrated by I156;
2. `python_local`: measured energy + explicit applicable tariff provenance absent;
3. `free_tier_ci`: support/testing-only for generic external paid work;
4. `local_model`: no usable local model/GPU interface observed in this environment;
5. `owned_pc`: real I166 run must occur on the user-owned PC with explicit ownership confirmation;
6. `owned_pc`: genuinely observed availability, trustworthy energy readings if available, explicit applicable tariff, and explicit opportunity-cost provenance are not yet materialized;
7. I166 focused tests are authored but not yet exact-source locally executed;
8. I167 bridge is ready, but no real I166 packet exists to feed it;
9. I050/I066 attestation binding for a future real I167 candidate is not yet materialized;
10. task-specific retry/failure and human-maintenance economics for a real candidate remain unknown;
11. `subscription_assistant`: support-only, no autonomous API assumed;
12. external LLM APIs: credentials/live measurement authorization absent;
13. future VPS: spend/infrastructure authorization absent;
14. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
15. PayanAgent geography/provider-access evidence: absent; public-doc search converged;
16. exact authorization for later bounded read-only production observation: **false**.

## Durable rules
- Do not reopen broad discovery without a genuinely missing mechanism.
- Do not repeat PayanAgent geography searches unless new first-party material appears.
- Deterministic/local filtering precedes selective AI; sub-hour watchers only within API/ToS limits.
- ChatGPT/Codex subscription is fixed/sunk limited support, not autonomous API access.
- Separate sunk/fixed and marginal cost; include quota/opportunity cost, energy/API cost, retries, maintenance, watcher overhead, platform/payment fees and payment/acceptance risk.
- Automatic runtime CI remains disabled; GitHub-hosted CI is support/testing-only here.
- Do not substitute synthetic values for user-PC energy, tariff, availability, reliability, parallelism or opportunity cost.
- CPU/logical-core count may bound a benchmark search but cannot itself be used as measured safe parallelism.
- I165 external JSON may not override I163 benchmark fields.
- I166 rejects fixture/example/synthetic/placeholder/dummy/mock provenance from the real-evidence path.
- I167 may derive resource cost fields from accepted I166 measurements, but may not invent task/market economics or promote itself directly to I123 production evidence.
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
If exact source-bound local materialization becomes available, execute the pending I166 focused tests without dispatching CI solely for the result.

The real forward path remains user-PC materialization: run I166/I165 on the actual user-owned PC with genuine provenance-bound facts. When I162 reaches `USER_PC_PACKET_COMPLETE`, feed the resulting I166 packet into I167, then bind the I167 candidate through I050/I066 before I123 promotion. Only then apply I130/I131/I133 conservative economics and I136/I138 readiness.

Until real resource evidence exists, the next repository-side safe work is to prepare and test the I167 -> I050/I066 attestation adapter contract without supplying fake resource or market values. Do not perform production market/API calls, credential use, paid installs, account creation, infrastructure rental, spend or task/value-moving actions. Do not reopen discovery.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
