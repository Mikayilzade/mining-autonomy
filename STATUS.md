# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I166 — user-PC real-evidence gate**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I166_USER_PC_REAL_EVIDENCE_GATE.md`
- `implementation/i166_user_pc_real_evidence_gate.py`
- `implementation/test_i166_user_pc_real_evidence_gate.py`
- `implementation/RUN_I164_I165_USER_PC_TEST_CLOSURE.md`
- `implementation/i165_user_pc_one_shot_materializer.py`
- `implementation/test_i165_user_pc_one_shot_materializer.py`
- `implementation/i164_fixed_benchmark_core.py`
- `implementation/test_i164_fixed_benchmark_core.py`
- `implementation/i163_user_pc_benchmark_session.py`
- `implementation/test_i163_user_pc_benchmark_session.py`
- `implementation/i162_user_pc_measurement_procedure.py`
- `implementation/i159_owned_pc_evidence_packet.py`
- `implementation/RUN_I161_EXPERIMENT_BOUNDARY.md`
- `implementation/i160_remaining_backend_control_pass.py`
- `implementation/RUN_I156_EXACT_I113_LOCAL_RUNTIME.md`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/i123_execution_backend_portfolio.py`

## I166 outcome
Added a fail-closed real-evidence gate in front of I165. It prevents unit-test/synthetic provenance from being promoted into owned-PC evidence by requiring explicit user-PC ownership confirmation, complete external evidence groups, valid ranges/counter order, and non-placeholder provenance labels. The emitted template contains only nulls and is explicitly non-evidence.

I166 does not measure or infer availability, energy, tariff or opportunity cost and cannot prove a provenance string is truthful. Real facts must still come from the actual user-owned PC or an applicable real source. If no trustworthy joule counter/meter exists, energy remains blocked rather than estimated.

Focused tests were authored for template semantics, fixture provenance rejection, ownership confirmation, partial groups, clean gate acceptance and invalid ranges. No CI workflow was dispatched solely to obtain a pass, so I166 tests are not claimed as executed in this checkpoint.

## I164-I165 outcome
I164 extracted the fixed deterministic benchmark primitives into a lightweight network-inert core while preserving benchmark identity/digest. Exact connector-materialized I159/I162/I163/I164 closure was verified by Git blob SHA and executed locally: **6 passed**.

I165 adds a one-shot local user-PC materializer. It runs I163, takes benchmark fields only from that measured session, rejects external benchmark overrides, merges only explicit availability/energy-counter/tariff/opportunity-cost fields, and feeds I162 using the same identity/environment binding. Combined exact-current I163/I164/I165 focused tests: **9 passed**.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder/control pass -> I161/I162/I163/I164/I165/I166 user-PC materialization boundary -> I050/I066/I123 -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. runtime regression: materially demonstrated by I156;
2. `python_local`: measured energy + explicit applicable tariff provenance absent;
3. `free_tier_ci`: support/testing-only for generic external paid work;
4. `local_model`: no usable local model/GPU interface observed in this environment;
5. `owned_pc`: repository-side benchmark/materialization/evidence-gate path exists, but the real run must occur on the user-owned PC with explicit ownership confirmation;
6. `owned_pc`: genuinely observed availability, trustworthy energy readings if available, explicit applicable tariff, and explicit opportunity-cost provenance are not yet materialized;
7. I166 focused tests are authored but not yet exact-source locally executed;
8. `subscription_assistant`: support-only, no autonomous API assumed;
9. external LLM APIs: credentials/live measurement authorization absent;
10. future VPS: spend/infrastructure authorization absent;
11. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
12. PayanAgent geography/provider-access evidence: absent; public-doc search converged;
13. exact authorization for later bounded read-only production observation: **false**.

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
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
First, exact-source execute the I166 focused tests locally if a source-bound materialization path is available without dispatching CI solely for this result.

Then run I166/I165 on the actual user-owned PC with `--confirm-user-owned-pc`. Supply only genuinely observed fields: availability with provenance; before/after joule-counter readings and task count if a trustworthy meter/counter exists; explicit applicable electricity tariff provenance; and explicit opportunity-cost provenance.

If the resulting I162 packet reaches `USER_PC_PACKET_COMPLETE`, feed it into the existing I050/I066/I123 -> I130/I131/I133 -> I136/I138 chain and evaluate conservative economics. If trustworthy energy measurement is unavailable, keep that blocker explicit rather than estimating it. Do not perform production market/API calls, credential use, paid installs, account creation, infrastructure rental, spend or task/value-moving actions. Do not reopen discovery.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
