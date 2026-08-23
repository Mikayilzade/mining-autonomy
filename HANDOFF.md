# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I127 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I127_EXACT_LOCAL_EVIDENCE_PACKET.md`
- `implementation/i127_exact_local_evidence_packet.py`
- `implementation/test_i127_exact_local_evidence_packet.py`
- `implementation/RUN_I126_PYTHON_LOCAL_CONFIG_INVARIANT.md`
- `implementation/i126_python_local_config_invariant.py`
- `implementation/resource_profile_evidence.py`
- `implementation/i124_runtime_resource_bootstrap.py`
- `implementation/i123_execution_backend_portfolio.py`
- `.github/workflows/implementation-tests.yml`
- `implementation/i113_local_runtime_chain_runner.py`

## I127 result
I127 is now the exact local-resource evidence packet layer. It can run I124, convert only the verified inert local probe facts into I050 records, merge I126's narrow python_local config invariants, attest through I050, and project the result to I123. If all critical facts are complete and reproducible, it also verifies the bundle through I066 materialization.

The default I124 + I126 combination leaves exactly three dynamic facts unresolved: `quota_units_remaining`, `electricity_per_task_usd`, and `rate_limit_per_minute`. I127 accepts optional additional evidence only for those three parameters through a local JSON file; the records must be hash-valid and still pass I050.

No current route, market evidence or authorization is created. Runtime execution remains pending because the available execution container cannot obtain a fresh GitHub checkout.

## Target flow
`cheap watcher -> deterministic local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I123 portfolio router -> I127 exact local evidence packet (I124 + I126 + I050/I066) -> market readiness -> exact authorization lineage -> one-shot read-only observation -> measured demand/economics feedback`.

## Immediate next broad run
At the first executable exact-current checkout run `python implementation/i127_exact_local_evidence_packet.py --root .`. Measure/source only the three remaining local facts where trustworthy no-spend telemetry or exact source evidence exists; otherwise leave them unknown. If complete, use the I066 materialization to rerun I123 and produce the final local resource-readiness decision.

Free/conditional CI quota/capacity remains a separate evidence branch. If current-main manual Actions becomes executable first, use one source-bound run only and do not infer CI quota/capacity from a green job.

Do not rerun stale PR CI, re-enable automatic triggers or perform the production GET.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization.

## Resource boundary
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- I126 invariants are python_local-only and exclude runtime/electricity/quota/rate evidence.
- I127 additional evidence is restricted to the three remaining dynamic parameters and is revalidated by I050.
- Electricity, external costs and finite capacity are never inferred from synthetic defaults.
- Free/conditional CI needs current quota/capacity/policy evidence and is not unlimited.
- Observation economics and paid-task fulfillment economics are independent.

## Git/CI
Prefer one coherent commit per broad stage. Keep automatic runtime triggers disabled; the runtime workflow remains manual-only.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
