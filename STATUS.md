# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I165 — user-PC one-shot materializer**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I164_I165_USER_PC_TEST_CLOSURE.md`
- `implementation/i165_user_pc_one_shot_materializer.py`
- `implementation/test_i165_user_pc_one_shot_materializer.py`
- `implementation/i164_fixed_benchmark_core.py`
- `implementation/test_i164_fixed_benchmark_core.py`
- `implementation/i163_user_pc_benchmark_session.py`
- `implementation/test_i163_user_pc_benchmark_session.py`
- `implementation/RUN_I163_USER_PC_BENCHMARK_SESSION.md`
- `implementation/i162_user_pc_measurement_procedure.py`
- `implementation/i159_owned_pc_evidence_packet.py`
- `implementation/RUN_I161_EXPERIMENT_BOUNDARY.md`
- `implementation/i160_remaining_backend_control_pass.py`
- `implementation/RUN_I156_EXACT_I113_LOCAL_RUNTIME.md`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/i123_execution_backend_portfolio.py`

## I164-I165 outcome
I164 removed the unnecessary heavy calibration/router import graph from I163 focused tests by extracting the unchanged fixed deterministic JSON-transform benchmark primitives into a lightweight network-inert core. The deterministic expected output digest remains `30b102b8e451d052387927e05e57ee4e5e7e046b0c3e15869a1684a9d52fa419`.

The exact connector-materialized I159/I162/I163/I164 focused closure was verified by Git blob SHA and executed locally with network/proxy disabled: **6 passed**. This closes the previous I163 focused-test blocker without dispatching CI.

I165 then adds a one-shot local user-PC materializer. It runs I163, takes benchmark fields only from that measured session, rejects external benchmark overrides, merges only explicit availability/energy-counter/tariff/opportunity-cost fields, and feeds the result into I162 using the same identity/environment binding. Combined exact-current I163/I164/I165 focused tests: **9 passed**.

The positive-completion I165 unit test uses labelled `test-fixture:*` values only to test control/merge logic. Those values are not real resource evidence and were not persisted as production evidence.

No production market/API request, credentials, downloads/paid installs, CI dispatch, account creation, paid infrastructure, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Previous outcomes
I156 exact-source I113: **PASS_BLOCKED**, 7/7 clean. I157: GitHub-hosted `free_tier_ci` **SUPPORT_TESTING_ONLY**. I158: no usable local model/GPU interface in this environment. I159: owned-PC evidence contract. I160: remaining backend control pass. I161: **FAIL_CLOSED_EXTERNAL_BOUNDARIES** with user-PC measurement as the next zero-new-spend inert branch. I162: portable user-PC measurement procedure, 4 focused tests passed. I163: deterministic user-PC benchmark/session wrapper, now exact-locally verified through I164.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder/control pass -> I161/I162/I163/I164/I165 user-PC materialization boundary -> I050/I066/I123 -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. runtime regression: materially demonstrated by I156;
2. `python_local`: measured energy + explicit applicable tariff provenance absent;
3. `free_tier_ci`: support/testing-only for generic external paid work;
4. `local_model`: no usable local model/GPU interface observed here;
5. `owned_pc`: repository-side benchmark/materialization path is implemented and exact-locally tested, but the real run must occur on the user-owned PC with explicit ownership confirmation;
6. `owned_pc`: genuinely observed availability, trustworthy energy readings if available, explicit applicable tariff, and explicit opportunity-cost provenance are not yet materialized;
7. `subscription_assistant`: support-only, no autonomous API assumed;
8. external LLM APIs: credentials/live measurement authorization absent;
9. future VPS: spend/infrastructure authorization absent;
10. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
11. PayanAgent geography/provider-access evidence: absent; public-doc search converged;
12. exact authorization for later bounded read-only production observation: **false**.

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
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
Run I165 on the actual user-owned PC with `--confirm-user-owned-pc`. Supply external JSON only for genuinely observed fields: availability with provenance; before/after joule-counter readings and task count if a trustworthy meter/counter exists; explicit applicable electricity tariff provenance; and explicit opportunity-cost provenance.

If the resulting I162 packet reaches `USER_PC_PACKET_COMPLETE`, feed it into the existing I050/I066/I123 -> I130/I131/I133 -> I136/I138 chain and evaluate conservative economics. If trustworthy energy measurement is unavailable, keep that blocker explicit rather than estimating it. Do not perform production market/API calls, credential use, paid installs, account creation, infrastructure rental, spend or task/value-moving actions. Do not reopen discovery.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
