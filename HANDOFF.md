# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I129 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I129_ENERGY_MEASUREMENT_RECEIPT.md`
- `implementation/i129_energy_measurement_receipt.py`
- `implementation/test_i129_energy_measurement_receipt.py`
- `implementation/RUN_I128_PYTHON_LOCAL_RESOURCE_COMPLETION.md`
- `implementation/i128_python_local_resource_completion.py`
- `implementation/RUN_I127_EXACT_LOCAL_EVIDENCE_PACKET.md`
- `implementation/i126_python_local_config_invariant.py`
- `implementation/i123_execution_backend_portfolio.py`
- `.github/workflows/implementation-tests.yml`
- `implementation/i113_local_runtime_chain_runner.py`

## I129 result
The strict python_local resource path now has an explicit acquisition contract for its last genuine marginal-cost fact. I129 converts independently observed joule-counter before/after readings around a known workload plus an explicit sourced electricity tariff into a canonical hash-bound receipt and then into the existing I054/I128 `EnergyMeasurement`.

It rejects counter reset/wrap, missing source identity/digests, invalid task count, negative values, stale/future/tampered receipts and scope drift. It never guesses energy or tariff and does not imply that a hardware counter covers whole-machine energy unless the source establishes that.

Current chain:
`fixed local probe + I126 config invariants + I128 quota/rate semantics + I129 verified energy receipt -> I054/I050 -> I066 -> I123`.

A fresh checkout attempt from the available execution container again failed because GitHub DNS resolution is unavailable, so no exact-current runtime/resource PASS exists yet.

## Immediate next broad run
At the first exact-current executable checkout, run I113 and the fixed I128 benchmark once. If trustworthy no-spend local energy telemetry exists, capture before/after readings around the workload and combine them with an explicit real tariff source via I129. Feed the verified measurement through I128/I050/I066, rerun I123, and emit one current resource-readiness/economics packet.

If telemetry or tariff provenance is absent, leave electricity unknown. Free/conditional CI quota/capacity remains separate. Do not restore automatic CI or perform the production GET.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization.

## Resource boundary
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- I126 invariants are python_local-only and exclude host/runtime/electricity evidence.
- I128 quota/rate `None` is a local-interface semantic, not unlimited host capacity.
- I129 requires independently sourced meter readings and explicit tariff provenance.
- Free/conditional CI needs current quota/capacity/policy evidence and is not unlimited.
- Observation economics and paid-task fulfillment economics are independent.
- Resource routing never widens market/policy/authorization eligibility.

## Git/CI
Prefer one coherent commit per broad stage where tooling permits. Keep automatic runtime triggers disabled; runtime workflow remains manual-only. Expected fail-closed outcomes belong in artifacts rather than notification-generating failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.