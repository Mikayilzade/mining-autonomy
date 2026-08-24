# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I161 — experiment readiness boundary**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I161_EXPERIMENT_BOUNDARY.md`
- `implementation/i161_experiment_boundary.py`
- `implementation/RUN_I160_REMAINING_BACKEND_CONTROL_PASS.md`
- `implementation/i160_remaining_backend_control_pass.py`
- `implementation/RUN_I159_OWNED_PC_EVIDENCE_PACKET.md`
- `implementation/i159_owned_pc_evidence_packet.py`
- `implementation/RUN_I158_LOCAL_MODEL_EVIDENCE_GATE.md`
- `implementation/i158_local_model_evidence_gate.py`
- `implementation/RUN_I157_FREE_TIER_CI_POLICY_GATE.md`
- `implementation/i157_free_tier_ci_policy_gate.py`
- `implementation/RUN_I156_EXACT_I113_LOCAL_RUNTIME.md`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/i123_execution_backend_portfolio.py`

## I161 outcome
Advanced the existing I138 readiness/control chain using I156–I160 without reopening discovery.

I161 defines five non-substitutable external boundaries: **user-PC measurement**, **external API credentials/live measurement authorization**, **future VPS spend/infrastructure authorization**, **PayanAgent provider-geography evidence**, and **exact bounded read-only observation authorization**.

I156 runtime remains materially demonstrated as `PASS_BLOCKED` and is preserved as a separate regression fact. I161 verifies the I160 backend classifications and does not let runtime evidence substitute for a current measured positive execution route, geography eligibility, or exact observation authorization.

Current default state: **FAIL_CLOSED_EXTERNAL_BOUNDARIES**. No current measured positive conservative production execution route exists. The next inert packet is the existing I159 user-PC measurement branch because it is the only zero-new-spend production-resource fact that can materially advance routing without credentials or infrastructure rental.

No network access, credentials, API calls, CI dispatch, account creation, infrastructure rental, task acceptance, spend, settlement or value movement occurred.

## Previous outcomes
I156 exact-source I113: **PASS_BLOCKED**, 7/7 clean. I157: GitHub-hosted `free_tier_ci` **SUPPORT_TESTING_ONLY**. I158: no usable local model/GPU interface in this environment. I159: `owned_pc` portable evidence contract exists but requires user-PC-bound measurements. I160: subscription assistant support-only; external APIs authorization-gated; future VPS spend/infrastructure-gated.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder/control pass -> I161 readiness boundary -> I050/I066/I123 -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. runtime regression: materially demonstrated by I156;
2. `python_local`: measured energy + explicit applicable tariff provenance absent;
3. `free_tier_ci`: support/testing-only for generic external paid work;
4. `local_model`: no usable local model/GPU interface observed here;
5. `owned_pc`: local hardware/availability/energy/tariff/opportunity-cost packet not materialized;
6. `subscription_assistant`: support-only, no autonomous API assumed;
7. external LLM APIs: credentials/live measurement authorization absent;
8. future VPS: spend/infrastructure authorization absent;
9. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
10. PayanAgent geography/provider-access evidence: absent; public-doc search converged;
11. exact authorization for later bounded read-only production observation: **false**.

## Durable rules
- Do not reopen broad discovery without a genuinely missing mechanism.
- Do not repeat PayanAgent geography searches unless new first-party material appears.
- Deterministic/local filtering precedes selective AI; sub-hour watchers only within API/ToS limits.
- ChatGPT/Codex subscription is fixed/sunk limited support, not autonomous API access.
- Separate sunk/fixed and marginal cost; include quota/opportunity cost, energy/API cost, retries, maintenance, watcher overhead, platform/payment fees and payment/acceptance risk.
- Automatic runtime CI remains disabled; GitHub-hosted CI is support/testing-only here.
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
Prepare a portable, fail-closed **user-PC measurement procedure** around I159/I129. It may define how to collect hardware/interface identity, deterministic benchmark quality, latency/reliability/parallelism, actual availability, measured energy per task, explicit electricity tariff provenance and opportunity cost, but must not fabricate or infer measurements that were not actually produced on the user's machine.

Do not install paid software, use credentials, spend money, dispatch CI, or make production market/API calls. If a trustworthy local energy counter cannot be accessed without additional user-side execution, preserve the boundary and emit the exact local measurement packet/instructions rather than substituting synthetic values.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
