# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I172 — owned-PC narrow hybrid evidence contract**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I172_OWNED_PC_HYBRID_EVIDENCE_CONTRACT.md`
- `implementation/i172_owned_pc_hybrid_evidence_contract.py`
- `implementation/test_i172_owned_pc_hybrid_evidence_contract.py`
- `implementation/RUN_I171_OWNED_PC_EXECUTION_SCOPE_GATE.md`
- `implementation/i171_owned_pc_execution_scope_gate.py`
- `implementation/test_i171_owned_pc_execution_scope_gate.py`
- `implementation/RUN_I170_OWNED_PC_CONTROL_EVIDENCE_POLICY.md`
- `implementation/i170_owned_pc_control_evidence_policy.py`
- `implementation/test_i170_owned_pc_control_evidence_policy.py`
- `implementation/RUN_I168_I169_OWNED_PC_I050_I066_ADAPTER.md`
- `implementation/i169_owned_pc_i050_i066_readiness.py`
- `implementation/test_i169_owned_pc_i050_i066_readiness.py`
- `implementation/i168_owned_pc_i050_evidence_adapter.py`
- `implementation/test_i168_owned_pc_i050_evidence_adapter.py`
- `implementation/RUN_I167_OWNED_PC_ROUTER_BRIDGE.md`
- `implementation/i167_owned_pc_router_bridge.py`
- `implementation/i166_user_pc_real_evidence_gate.py`
- `implementation/i165_user_pc_one_shot_materializer.py`
- `implementation/i163_user_pc_benchmark_session.py`
- `implementation/i162_user_pc_measurement_procedure.py`
- `implementation/i159_owned_pc_evidence_packet.py`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/resource_profile_evidence.py`
- `implementation/resource_feedback_materialization.py`

## I168-I172 outcome
I168 provides a source-bound adapter from a future accepted real I166 packet plus its exact I167 bridge into I050-shaped resource evidence. It emits only seven facts supported by real measurement/session evidence: `currently_available`, `programmatic_access`, `electricity_per_task_usd`, `latency_seconds`, `reliability_probability`, `quality_probability`, and `max_parallelism`. The other seven I050 control/accounting/interface parameters remain missing rather than being copied from synthetic Router defaults.

I168 is bound to current I050 blob `9b76a2194d15f8277d15b2e46c85df71cca08874` and I066 blob `d995821e27ec27d72531dc71b433de702fb8fe7b`. Exact local verification from matching Git blobs: **5 passed**.

I169 validates the seven missing control records and preserves current I050 source-class semantics. A complete bundle using only current reproducible source classes may reach `READY_FOR_EXACT_I050_EXECUTION`, but I066 and I123 remain disabled until actual I050/I066 execution. A complete bundle containing `user_declared` control facts is classified `COMPLETE_DECLARED_BUNDLE_BLOCKED_FOR_I123`; declarations are never relabelled `measured_reproducible`. Exact local verification: **6 passed**.

I170 formalizes the source policy for the seven controls. Five are exact-interface facts that must be reproducibly proven: `requires_credentials`, `requires_paid_account`, `requires_new_spend`, `quota_units_remaining`, `rate_limit_per_minute`. Two are owner/accounting facts that must not be disguised as machine measurements: `fixed_monthly_cost_usd`, `sunk_or_already_committed`. If either accounting fact genuinely remains `user_declared`, current strict I050/I123 semantics create a deliberate hybrid-policy review boundary rather than automatic promotion. Exact local verification: **6 passed**.

I171 closes an execution-scope substitution gap. I163 benchmark evidence is `benchmark_only` and may not be reused as evidence about an unknown future paid-task executor. The five I170 interface facts may become production-scoped only when bound to a named deterministic task executor, its complete Git source closure, a concrete task family and acceptance-contract identity. Focused logic verification: **6 passed**. I171 creates no I050 records and no I123 promotion.

I172 completes the exact repository-side next action from I170: a **review-only narrow owned-PC hybrid contract**. `user_declared` provenance is permitted only for the two accounting facts; every other I050 critical parameter must remain in current reproducible source classes with source-content binding. The contract is `owned_pc`-only, cannot widen another backend family, cannot consume/create credentials/spend/infrastructure authorization, does not modify I050/I123, and cannot enable I123 promotion. Focused logic verification: **7 passed**.

No CI dispatch was used for I171/I172 testing. Their current local test materializations exercised authored logic but are not claimed as new byte-for-byte exact-Git-blob execution closures. No production market/API request, credentials, downloads/paid installs, account creation, paid infrastructure, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Previous outcomes
I156 exact-source I113: **PASS_BLOCKED**, 7/7 clean. I157: GitHub-hosted `free_tier_ci` **SUPPORT_TESTING_ONLY**. I158: no usable local model/GPU interface observed here. I159-I166: portable owned-PC evidence/materialization path. I167: Router resource bridge from future real I166 evidence; exact-local focused tests **3 passed**.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder -> I161/I162/I163/I164/I165/I166 real user-PC materialization -> I167 Router resource bridge -> I168 partial I050 evidence -> I170 control-source policy -> I171 production-executor scope binding -> I172 narrow hybrid review contract -> I169 readiness -> exact I050 -> I066 -> I123 Router -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. runtime regression: materially demonstrated by I156;
2. `python_local`: measured energy + explicit applicable tariff provenance absent;
3. `free_tier_ci`: support/testing-only for generic external paid work;
4. `local_model`: no usable local model/GPU interface observed in this environment;
5. `owned_pc`: real I166 run must occur on the actual user-owned PC with explicit ownership confirmation;
6. `owned_pc`: genuine availability, trustworthy energy readings if available, explicit applicable tariff, and explicit opportunity-cost provenance are not materialized;
7. I166 focused tests remain authored but not exact-source locally executed as their full dependency closure is not currently materialized here;
8. no real I166 packet exists to feed I167/I168;
9. I168 can populate only 7/14 I050 parameters from measured evidence;
10. five interface controls need reproducible evidence bound to the exact production task executor, not I163 benchmark scope;
11. two owner/accounting controls need explicit real accounting provenance; if they remain `user_declared`, I172 is review-only and current I050/I123 still do not promote them;
12. no concrete permitted deterministic production task executor + acceptance contract has yet been selected/built and source-bound through I171;
13. no hybrid policy patch has been applied; I050/I123 remain unchanged;
14. exact I050 and I066 execution for owned_pc is not yet permitted/materialized;
15. task-specific retry/failure, maintenance, payout, platform/payment fees, acceptance/dispute/nonpayment economics remain unknown for a real candidate;
16. `subscription_assistant`: support-only, no autonomous API assumed;
17. external LLM APIs: credentials/live measurement authorization absent;
18. future VPS: spend/infrastructure authorization absent;
19. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
20. PayanAgent geography/provider-access evidence: absent; public-doc search converged;
21. exact authorization for later bounded read-only production observation: **false**.

## Durable rules
- Do not reopen broad discovery without a genuinely missing mechanism.
- Do not repeat PayanAgent geography searches unless new first-party material appears.
- Deterministic/local filtering precedes selective AI; sub-hour watchers only within API/ToS limits.
- ChatGPT/Codex subscription is fixed/sunk limited support, not autonomous API access.
- Separate sunk/fixed and marginal cost; include quota/opportunity cost, energy/API cost, retries, maintenance, watcher overhead, platform/payment fees and payment/acceptance risk.
- Automatic runtime CI remains disabled; GitHub-hosted CI is support/testing-only here.
- Do not substitute synthetic values for user-PC energy, tariff, availability, reliability, parallelism, opportunity cost, quota/rate semantics or accounting facts.
- CPU/logical-core count may bound a benchmark search but cannot itself be used as measured safe parallelism.
- I165 external JSON may not override I163 benchmark fields.
- I166 rejects fixture/example/synthetic/placeholder/dummy/mock provenance from the real-evidence path.
- I167/I168 may derive only facts actually supported by accepted I166 measurements; synthetic Router defaults are not evidence.
- I169 may not relabel `user_declared` records as reproducible or enable I066/I123 before exact I050 execution.
- I170 permits no policy widening by itself.
- I171 forbids benchmark-only evidence from satisfying production-executor interface controls.
- I172 is review-only, owned_pc-only, and may recognize declarations solely for the two accounting parameters; it cannot create authorization or production eligibility.
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
Repository-side: build/select one concrete deterministic **offline/dry-run executor** for a permitted task family already represented in the implementation architecture, with explicit machine-checkable acceptance criteria. Bind its complete Git source closure and acceptance contract through I171. Do not call a production market merely to obtain a task.

Then prepare reproducible evidence for the five I170 interface controls against that exact production-scoped executor. Keep the two accounting facts truthful. If they remain `user_declared`, compare a minimal proposed owned_pc-only I050/I123 policy patch against the strict path and prove by tests that it cannot widen any other backend/source/authorization gate; do not apply the patch until the real evidence path actually needs it.

Real forward path remains user-PC materialization: run I166/I165 on the actual user-owned PC with genuine provenance-bound facts, then I167 -> I168 -> I169. If no trustworthy energy counter exists, keep that blocker explicit rather than estimating it.

If exact source-bound full I166 dependency materialization becomes available, execute its pending focused tests without dispatching CI solely for that result. Do not perform production market/API calls, credential use, paid installs, account creation, infrastructure rental, spend or task/value-moving actions. Do not reopen discovery.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
