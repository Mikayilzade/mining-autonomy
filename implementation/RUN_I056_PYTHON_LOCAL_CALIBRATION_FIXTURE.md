# Implementation Run I056 — opt-in local python calibration fixture/runner

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Turn the I053 local calibration contract into a concrete, portable and replayable `python_local` fixture without enabling any market/network execution or inferring facts that a local benchmark cannot prove.

## Changes
Added `implementation/python_local_calibration_fixture.py`.

The module defines one fixed benchmark, `python-local-fixed-json-transform-v1`, over a small canonical JSON fixture. The transform is pure deterministic Python: schema validation, stable sorting, aggregation and SHA-256 checksumming only.

The runner is **opt-in**. `run_python_local_fixture()` raises `benchmark_runner_opt_in_required` unless the caller explicitly passes `enabled=True`. When enabled, it performs only the fixed local transform for at least the I053 minimum repetitions, records latency/success/output-digest/quality observations and reduces them through the existing I053 `evaluate_probe_transcript()` contract.

The portable transcript binds:
- backend id;
- benchmark id;
- exact reference-backend hash;
- expected output digest;
- every observation;
- observed parallelism;
- optional explicitly observed rate limit;
- exact I053 transcript digest;
- inert safety flags.

Added deterministic JSON serialization/deserialization plus `replay_python_local_transcript()`. Replay fails closed on backend/benchmark/reference-hash/output-digest/runner-kind mismatches, non-inert flags, output tampering or I053 transcript-digest mismatch.

Added `replay_transcript_through_i055()` to feed a verified local transcript back through the established I053 -> I054 -> I050 -> I052/I055 chain. The replay supplies only probe-demonstrated facts. Accounting, electricity, quota and other non-probe critical fields remain missing unless separately evidenced through the existing declaration/measurement contracts.

## Verification coverage
Added `implementation/test_python_local_calibration_fixture.py` covering:
1. deterministic fixed benchmark identity/output;
2. runner disabled by default;
3. opted-in run remains local/inert and emits the expected digest;
4. portable JSON round-trip and exact I053 digest replay;
5. tampered observation rejection;
6. exact reference-backend binding;
7. I055 replay remains hold when accounting/electricity evidence is absent;
8. declarations cannot overwrite probe-derived fields.

The new tests are committed for the existing manual/PR test workflow. GitHub Actions was intentionally not dispatched, and push-triggered CI remains disabled.

## Safety / evidence boundary
No HTTP/DNS, sockets, marketplace calls, credentials, API keys, KYC, wallet, payment, paid server/API, task acceptance, publication, settlement or value movement is introduced.

A successful local fixture proves only the facts that I053 permits the probe to demonstrate: current local execution availability for that exact interface/fixture, programmatic invocation, latency, observed reliability/quality and observed bounded parallelism. It does **not** prove electricity cost, fixed/sunk cost, quota, subscription API availability, account requirements, real market compatibility or profitability.

## Outcome
The resource-calibration path now has a concrete reproducible first backend fixture instead of only an abstract acquisition contract. A future local collector can run this exact no-network benchmark, persist its portable transcript and replay it into I055 while preserving the existing fail-closed evidence distinctions.

## Next run — I057
Build a deterministic local calibration session bundle around I056: explicit collector timestamp, transcript file digest, separate declaration template for the non-probe critical fields, optional energy-measurement slot, and a one-command offline replay/report contract. Keep collection opt-in; do not infer missing resource facts and do not perform market/network calls.

Project state: **IMPLEMENTATION IN PROGRESS**.
