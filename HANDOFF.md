# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I124 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I124_RUNTIME_RESOURCE_BOOTSTRAP.md`
- `implementation/i124_runtime_resource_bootstrap.py`
- `implementation/test_i124_runtime_resource_bootstrap.py`
- `implementation/RUN_I123_EXECUTION_BACKEND_PORTFOLIO.md`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/RUN_I122_RUNTIME_CONNECTOR_CAPABILITY_AUDIT.md`
- `.github/workflows/implementation-tests.yml`
- `implementation/i113_local_runtime_chain_runner.py`

## I124 result
I124 replaces a sequence of narrow operational checkpoints with one portable no-spend runtime+resource bootstrap command. It runs I113 once, performs the existing fixed deterministic local Python calibration probe/session, projects measured facts into I123 `BackendEvidence`, and writes one backend review packet.

The packet explicitly distinguishes partial measured evidence from complete `measured_reproducible` evidence. Missing electricity/economics or CI quota/capacity cannot be silently filled from reference defaults. I113 runtime success alone does not materialize `free_tier_ci`. A complete resource projection still does not create market evidence or authorization.

The I124 source and tests compile, but the bundle has not run in an exact current checkout. Current state therefore remains `BLOCKED`: fresh-real evidence absent; eligible non-synthetic current route absent; exact authorization absent; exact-current runtime receipt absent.

## Target flow
`cheap watcher -> deterministic local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I123 portfolio router -> I124 runtime/resource bootstrap -> I058-I067 complete attestation/materialization when evidence exists -> market readiness -> exact authorization lineage -> one-shot read-only observation -> measured demand/economics feedback`.

## Immediate next broad run
At the first executable exact-current checkout run `python implementation/i124_runtime_resource_bootstrap.py --root .`, then close all concrete no-spend local resource evidence gaps in the same stage where possible, pass complete evidence through I058-I067, and rerun I123.

If current-main manual Actions dispatch becomes available first, execute exactly one manual runtime run and use its current source-bound artifact chain as the runtime component. Materialize CI quota/capacity separately; do not infer it from a green job.

Do not create another micro safety layer unless a concrete defect is found. Do not rerun stale PR CI, re-enable automatic triggers, or perform the production GET from this checkpoint.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- Production resource selection needs current reproducible non-synthetic evidence.
- Free/conditional CI needs current quota/capacity/policy evidence and is not unlimited.
- External paid APIs and future VPS require separate credentials/spend/infrastructure authorization.
- Observation economics and paid-task fulfillment economics are independent.
- Resource routing never widens market/policy/authorization eligibility.

## Git/CI
Prefer one coherent commit per broad stage. Keep push/PR runtime triggers disabled. The implementation runtime workflow is manual-only. Expected fail-closed states belong in artifacts rather than notification-generating job failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
