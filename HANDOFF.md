# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I128 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I128_PYTHON_LOCAL_RESOURCE_COMPLETION.md`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/test_i128_python_local_resource_completion.py`
- `implementation/RUN_I127_EXACT_LOCAL_EVIDENCE_PACKET.md`
- `implementation/i127_exact_local_evidence_packet.py`
- `implementation/test_i127_exact_local_evidence_packet.py`
- `implementation/RUN_I126_PYTHON_LOCAL_CONFIG_INVARIANT.md`
- `implementation/i126_python_local_config_invariant.py`
- `implementation/i124_runtime_resource_bootstrap.py`
- `implementation/i123_execution_backend_portfolio.py`
- `.github/workflows/implementation-tests.yml`
- `implementation/i113_local_runtime_chain_runner.py`

## I128 result
I127 created the exact I124 -> I050/I066/I123 local evidence packet and left three unresolved dynamic fields. I128 safely resolves two of them at the local-interface semantic layer.

For exact `python_local` / `deterministic_python` only, `quota_units_remaining=None` and `rate_limit_per_minute=None` now mean there is no external provider quota/rate-limit primitive for the repository-local executor. This is not an infinite-capacity claim. Actual host capacity remains represented by measured max parallelism, latency/reliability/quality, electricity and opportunity cost.

The current local evidence path is:

`fixed local probe + I126 config invariants + I128 quota/rate interface semantics + optional measured energy/tariff -> I050 -> I066 -> I123`.

Without genuine energy evidence, the exact strict resource gap is now only `electricity_per_task_usd`. With a real measured energy-per-task value and an explicit tariff, the source path can become fully reproducible and materialized, but it still does not create a market route, demand evidence or authorization.

I128 also integrates I113: `RESOURCE_AND_RUNTIME_READY` is possible only if resource evidence is complete and the exact I113 receipt is `PASS_BLOCKED`.

The current connector still does not expose an executable exact-current checkout or authenticated manual workflow dispatch, so no runtime/resource PASS is claimed.

A temporary duplicate I127 draft caused by STATUS lagging behind `implementation/RUN_LOG.md` was removed. Authoritative order is I127 exact local evidence packet -> I128 python_local resource completion.

## Target flow
`cheap watcher -> deterministic local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I123 portfolio router -> I128 complete local resource packet -> current positive-margin resource decision -> market readiness -> exact authorization lineage -> one-shot read-only observation -> measured demand/economics feedback`.

## Immediate next broad run
At the first executable exact-current checkout run once:

`python implementation/i128_python_local_resource_completion.py --root .`

In the same stage consume the fresh I113 receipt, run the local probe, and keep electricity unknown unless reliable no-spend energy telemetry exists. If energy is measured, combine it only with an explicit real tariff, materialize through I050/I066, then rerun I123 and emit one current resource-readiness/economics packet.

Free/conditional CI quota/capacity remains a separate evidence branch. If current-main manual Actions becomes executable first, use one source-bound run only and do not infer CI quota/capacity from a green job.

Do not rerun stale PR CI, re-enable automatic triggers or perform the production GET.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization.

## Resource boundary
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- I126 invariants are python_local-only and exclude host/runtime/electricity evidence.
- I128 quota/rate `None` is a local-interface semantic, not unlimited host capacity.
- Electricity and opportunity cost are never inferred from synthetic defaults.
- Free/conditional CI needs current quota/capacity/policy evidence and is not unlimited.
- Observation economics and paid-task fulfillment economics are independent.
- Resource routing never widens market/policy/authorization eligibility.

## Git/CI
Prefer one coherent commit per broad stage. Keep automatic runtime triggers disabled; the runtime workflow remains manual-only. Expected fail-closed outcomes belong in artifacts rather than notification-generating failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.