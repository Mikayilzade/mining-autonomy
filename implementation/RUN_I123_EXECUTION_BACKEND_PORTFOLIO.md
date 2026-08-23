# I123 — Execution Backend Portfolio / Deterministic-First Routing

Status: **completed broad network-inert implementation stage — portfolio + tests authored**
Date: 2026-08-23

## Goal
Use the blocked runtime checkpoint productively without inventing another safety gate. Consolidate the Resource / Execution Router into a portfolio-level decision layer that answers both **whether a task is worth doing** and **which execution backend should do it**, while preserving the existing no-spend/no-credentials/no-network boundaries.

## Work performed
Added:
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/test_i123_execution_backend_portfolio.py`

I123 intentionally extends the existing I048 `resource_router.py` instead of creating a second economics model.

The portfolio covers all required backend families already represented by I048:
1. pure Python / local deterministic execution;
2. local CPU/GPU/local model;
3. already-paid ChatGPT/Codex-style subscription support as fixed/sunk and capacity-limited, with **no assumed autonomous programmatic API**;
4. cheap external LLM/API;
5. stronger/more expensive external LLM/API;
6. free/conditional CI/cloud;
7. owned PC;
8. future VPS/server requiring separate authorization.

I123 adds an explicit current-evidence layer on top of each backend: provenance class, current reproducibility, synthetic/non-synthetic status, capacity verification, current policy evidence, credential authorization, spend authorization and infrastructure authorization.

## Economics retained from I048/I101
The underlying router still accounts separately for:
- fixed/sunk monthly cost vs true per-task marginal cost;
- quota/capacity and remaining quota;
- latency, reliability, quality, parallelism and rate limit;
- incremental unit/compute cost, electricity, external API/model cost, retry/failure cost;
- human maintenance and opportunity cost;
- marketplace/platform fee, transaction fee, gas, withdrawal/conversion cost;
- acceptance probability, dispute probability and non-payment probability.

A sunk subscription is not charged in full to every task, but it is also not treated as a zero-cost unlimited API. The subscription reference remains `support_only` / non-programmatic.

## Routing behavior
The new portfolio rule is:

`deterministic/local -> existing capability/policy/quota/reliability/quality/margin gate -> current reproducible non-synthetic materialization gate -> AI only if needed -> cheapest qualifying backend`

Production-ready selection now additionally requires:
- `measured_reproducible` provenance;
- current reproducibility;
- non-synthetic evidence;
- verified capacity;
- current backend policy evidence;
- credentials/spend/infrastructure authorization when the backend actually requires them.

The portfolio does not enable execution. Every decision retains `production_execution_enabled=false` and `value_movement_enabled=false`.

Observation and paid-task execution remain separate `task_kind` values so a cheap read-only observation can never be used as evidence that paid fulfillment is profitable.

## Current checkpoint snapshot
`current_backend_evidence()` encodes only repository-known facts and deliberately marks all eight backends as planning/non-production evidence.

Consequences:
- `python_local` remains the preferred no-spend deterministic family, but exact executable current-checkout measurement/materialization is absent;
- local model / owned PC remain unmeasured;
- ChatGPT/Codex remains fixed/limited support only, not autonomous API capacity;
- external APIs remain unmaterialized and separately credential/spend gated;
- free/conditional CI exists as a manual backend, but current connector still exposes no `workflow_dispatch`;
- future VPS remains separately spend/infrastructure-authorized only.

Therefore `current_snapshot()` reports `eligible_non_synthetic_route_exists=false` and creates no production route.

## Verification
Both new Python files passed source compilation in the available authoring environment.

`test_i123_execution_backend_portfolio.py` adds 16 deterministic cases covering:
- all eight backend families;
- default planning-only state;
- deterministic-first routing;
- AI escalation only after deterministic insufficiency;
- AI-disabled tasks;
- subscription not becoming programmatic merely because it is already paid;
- synthetic/planning evidence quarantine;
- paid API credential/spend authorization;
- future VPS infrastructure authorization;
- non-sunk fixed-cost allocation basis;
- finite CI quota;
- quality threshold;
- negative conservative margin;
- acceptance/dispute/non-payment economics;
- observation vs paid-task separation;
- execution/value movement remaining disabled.

The full repository runtime suite is still pending because this environment has no executable current checkout and no authenticated manual workflow-dispatch capability. No runtime PASS was fabricated.

## Safety / external actions
No DNS/HTTP/socket/TLS market observation occurred. No real credentials, account creation, KYC, paid API/server, task acceptance/submission, wallet, deposit, stake, payment or value movement occurred. No GitHub Actions workflow was dispatched or rerun. Automatic CI remains disabled.

## Conclusion
The Resource / Execution Router is now explicit at portfolio level rather than only individual quotes/materialization. The remaining gap is empirical: obtain one current measured reproducible no-spend backend and later real permitted market evidence, not more abstract safety layers.

## Next action
Take one broader **no-spend runtime + resource bootstrap** stage.

Prepare a single portable repository-local command/bundle that, when a valid executable checkout or manual Actions dispatch is available:
1. executes the exact I113 current-main runtime chain once;
2. executes the existing no-spend resource calibration/materialization path;
3. converts measured backend evidence into I123 `BackendEvidence`;
4. emits one compact review packet showing whether `python_local` or free/conditional CI is now `measured_reproducible` and economically eligible.

The bundle must remain market-network-inert and must not infer authorization or perform the production GET.
