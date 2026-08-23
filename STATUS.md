# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I157 — free-tier CI policy gate**
Last updated: **2026-08-24**

## Latest durable files
- `implementation/RUN_I157_FREE_TIER_CI_POLICY_GATE.md`
- `implementation/i157_free_tier_ci_policy_gate.py`
- `implementation/test_i157_free_tier_ci_policy_gate.py`
- `implementation/RUN_I156_EXACT_I113_LOCAL_RUNTIME.md`
- `implementation/RUN_I155_CONNECTOR_BLOB_INGEST.md`
- `implementation/i155_connector_blob_ingest.py`
- `implementation/test_i155_connector_blob_ingest.py`
- `implementation/RUN_I154_EXACT_I113_RUNTIME_CLOSURE.md`
- `implementation/i154_exact_i113_runtime_closure.py`
- `implementation/test_i154_exact_i113_runtime_closure.py`
- `implementation/RUN_I151_I153_SOURCE_BOUND_RUNTIME_TRANSPORT.md`
- `implementation/i151_source_bound_runtime_snapshot.py`
- `implementation/test_i151_source_bound_runtime_snapshot.py`
- `implementation/RUN_I148_I150_PAYANAGENT_GEOGRAPHY_CLOSURE.md`
- `implementation/i148_payanagent_geography_resolution.py`
- `implementation/i142_market_source_evidence_gate.py`
- `implementation/i143_observation_source_selector.py`
- `implementation/i140_readonly_observation_design.py`
- `implementation/i141_economic_test_packet.py`
- `implementation/i136_conservative_portfolio_evaluator.py`
- `implementation/i137_resource_fallback_ladder.py`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/i113_local_runtime_chain_runner.py`

## I157 outcome
The existing `free_tier_ci` Resource / Execution Router branch was revalidated against current first-party GitHub policy without dispatching CI.

Repository `Mikayilzade/mining-autonomy` is currently public. GitHub's current billing documentation states that standard GitHub-hosted runners are free for public repositories, but GitHub Actions remains subject to service limits and Additional Product Terms. Those terms prohibit cryptomining, disproportionate server burden/commercial resale patterns, and — for GitHub-hosted runners — activity unrelated to production, testing, deployment or publication of the software project associated with the repository.

Therefore GitHub-hosted Actions is classified **SUPPORT_TESTING_ONLY** for this project. The public-repository `$0` incremental runner-price fact is not promoted into generic external paid-task permission or infinite capacity. It is not an eligible production earning backend for arbitrary marketplace work.

Added `i157_free_tier_ci_policy_gate.py` and focused tests. Local verification before write: **3 tests passed**. The gate fails closed if policy evidence is widened to generic external paid-task permission or if this public-repository checkpoint is substituted with a private repository state.

No workflow was dispatched; no credentials, production market request, task action, paid infrastructure, spend or value movement occurred.

## Previous runtime outcome
I156 materially demonstrated the exact I154-bound I113 local runtime chain: **PASS_BLOCKED**, 7/7 subprocesses clean, source hashes stable, errors empty. Runtime-regression evidence is no longer the active blocker for that snapshot.

## Current control chain
`I113 exact runtime PASS_BLOCKED -> Resource/Execution Router evidence ladder (python_local -> free_tier_ci -> local_model -> owned_pc -> separately authorized paid/API/VPS branches) -> I050/I066/I123 -> I130/I131/I133 economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142/I145/I148 source evidence -> I143 selection -> I140 bounded observation -> I141 economic-test packet`.

## Current blockers
1. exact-source local runtime regression verification: **materially demonstrated by I156**;
2. `python_local`: genuine measured energy + explicit applicable tariff provenance **absent in current execution environment**;
3. `free_tier_ci` / GitHub-hosted Actions: **support/testing-only; not policy-eligible for generic external paid-task execution**;
4. current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**;
5. PayanAgent explicit geography/provider-access evidence: **absent; public-doc search converged**;
6. exact authorization for any later bounded read-only production observation: **false**.

## Durable rules
- Do not reopen broad discovery unless implementation proves a genuinely missing mechanism.
- Do not repeat PayanAgent geography documentation searches unless new first-party material appears.
- Exact-current source identity may use a verified connector/snapshot transport; source integrity may not be relaxed because direct git/DNS is unavailable.
- Connector-delivered source must pass exact Git blob SHA verification before local execution; do not manually reconstruct/reformat rejected blobs.
- I113 PASS_BLOCKED satisfies only the runtime-regression evidence branch; it cannot substitute for fresh-real evidence, resource-route economics, or authorization.
- Real demand/fill must be measured, never inferred from listings/provider counts.
- Deterministic/local polling/filtering precedes selective AI; sub-hour watchers only within API/ToS limits.
- ChatGPT/Codex subscription is fixed/sunk limited support, not autonomous API access.
- GitHub Actions public-runner pricing does not imply permission for arbitrary paid external compute or unlimited capacity; keep GitHub-hosted CI support/testing-only under current terms.
- Automatic push/PR runtime CI remains disabled.
- No spend, credentials, registration, wallet, task acceptance, fulfillment, purchase or value movement before separate authorization.

## Immediate next broad run
Advance I134/I137 to the existing `local_model` no-new-spend evidence branch. Detect only genuinely available local CPU/GPU/model interfaces and measure/verify what the current execution environment can actually support: interface presence, model identity, deterministic/programmatic access, quality acceptance benchmark, capacity/parallelism/latency/reliability, and energy/opportunity-cost evidence. Do not assume a GPU or local model exists and do not download large models or create new spend.

If `local_model` cannot be materially evidenced without downloads, credentials, unavailable hardware, or invented energy values, mark that no-spend branch exhausted and continue I137 to `owned_pc`. Do not reopen discovery.

If new explicit PayanAgent policy/contact evidence or separately authorized local-access evidence appears, encode it and rerun I142/I145/I148 before I140/I141.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
