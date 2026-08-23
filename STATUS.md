# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I138 — integrated experiment readiness orchestrator**
Last updated: **2026-08-23**

## Latest durable files
- `implementation/RUN_I136_I138_BROAD_EXPERIMENT_READINESS.md`
- `implementation/i136_conservative_portfolio_evaluator.py`
- `implementation/i137_resource_fallback_ladder.py`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/test_i136_i138_broad_experiment_readiness.py`
- `implementation/RUN_I133_I135_CONSERVATIVE_ROUTING_READINESS.md`
- `implementation/i133_conservative_route_gate.py`
- `implementation/i134_backend_evidence_acquisition_planner.py`
- `implementation/i135_pre_observation_readiness_packet.py`
- `implementation/RUN_I130_I132_BROAD_RESOURCE_ECONOMICS.md`
- `implementation/i130_resource_economics_sensitivity.py`
- `implementation/i131_watcher_cost_budget.py`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/i113_local_runtime_chain_runner.py`

## I136–I138 outcome
Three linked steps were completed as one broad stage.

I136 combines I123 evidence/materialization blockers with I133 conservative economics across the full existing backend portfolio. A backend becomes a candidate only when current reproducible non-synthetic evidence, capacity/policy gates and conservative economics including stress + watcher overhead all pass. Deterministic routes remain preferred before AI families.

I137 provides the runtime-independent fallback loop over I134's existing backend acquisition plan. If no current conservative route exists, it chooses the next already-defined no-new-spend evidence branch rather than reopening discovery. The current ordering keeps `python_local` first; after that branch is attempted, free/conditional CI is the next existing no-spend branch under the current model.

I138 turns the pre-observation flow into one fail-closed next-action state machine: resource measurement -> exact-current runtime -> fresh market/policy evidence -> exact single read-only observation authorization -> readiness. Even final readiness does not itself enable network, execution, spend, task acceptance or value movement.

Focused tests were added for evidence/economics conjunction, deterministic-first selection, fallback progression and gate ordering. A fresh exact-current clone/test attempt again failed before checkout because `github.com` DNS cannot resolve in the available execution container, so no executed pytest/runtime PASS is claimed and no CI was dispatched.

## Current resource/economics chain
`I113 runtime + I128/I129 local resource measurement -> I050/I066/I123 -> I130 stress + I131 watcher overhead -> I133 conservative route -> I136 portfolio selection -> I137 fallback when needed -> I138 experiment readiness`.

## Current blockers
1. exact-current I113 runtime receipt: **absent**;
2. genuine measured energy + explicit tariff provenance for `python_local`: **absent**;
3. current measured non-synthetic backend route surviving conservative economics + watcher overhead: **false**;
4. fresh-real market/policy evidence: **false**;
5. exact authorization for later one-shot read-only observation: **false**.

## Durable rules
- Do not reopen broad discovery unless implementation proves a genuinely missing mechanism.
- Real demand/fill must be measured, never inferred from listings/provider counts.
- Deterministic/local filtering precedes AI; AI is used only when required by acceptance criteria.
- Fixed/sunk cost, marginal cost, quota/opportunity cost, watcher overhead, energy, API/model fees, retries, maintenance and platform/payment risk remain separate.
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free unlimited autonomous API and not assumed programmatically accessible.
- Free/conditional CI is a separate capacity/policy evidence branch and is not unlimited/free by assumption.
- Paid APIs and future VPS require separate credentials/spend/infrastructure authorization before execution.
- No production market DNS/HTTP GET has yet been performed by this chain.
- Automatic push/PR runtime CI remains disabled to avoid notification spam.

## Immediate next broad run
Keep the next stage broad rather than creating micro-checkpoints.

At the first executable exact-current checkout, run the whole local path in one cycle: I113 + I128/I129 -> I050/I066/I123 -> I133/I136 -> I138. Use genuine no-spend energy telemetry only if available and pair it with an explicit real tariff; never guess either component.

If `python_local` cannot be materialized or fails conservative economics, use I137/I134 immediately to advance to the next existing no-new-spend backend branch (currently free/conditional CI under the model) and evaluate it under the same evidence/economics framework. Do not perform the production GET. Only after runtime, current conservative resource route and fresh market/policy evidence are all ready should exact one-shot observation authorization be requested/used.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.