# Implementation Run I128 — python_local resource completion

Date: 2026-08-23
Status: **COMPLETED AS SOURCE CHECKPOINT — EXECUTION / REAL ENERGY EVIDENCE PENDING**
Phase: Implementation / Experiment

## Objective
Take the exact I127 local evidence packet one broad step further and close the two ambiguous local-interface fields without turning `None` into an unlimited-capacity assumption.

## What changed
Added `i128_python_local_resource_completion.py` plus focused tests.

I128 assembles one python_local resource packet from four evidence classes:
1. I056/I053 fixed local probe: current availability, programmatic access, latency, reliability, quality and measured `max_parallelism`;
2. I126 exact repository-config invariants: no credentials, no paid account, no new spend, zero fixed software cost and zero-cost sunk normalization;
3. I128 local-interface semantics: `quota_units_remaining=None` and `rate_limit_per_minute=None` mean **no external provider quota/rate-limit primitive exists for this repository-local executor**;
4. optional measured energy + explicit tariff through the existing I054 `EnergyMeasurement` path.

The I128 `None` values are deliberately not interpreted as infinite compute, zero opportunity cost or unlimited parallelism. Host capacity is still represented by measured `max_parallelism`, latency/reliability/quality, energy and the existing economics model.

## Resulting gap
With a valid local probe and I126, I128 reduces the strict I050 evidence gap to exactly one genuine host/economic fact:

- `electricity_per_task_usd`.

If and only if measured energy and an explicit tariff are supplied, the source path can become complete and flow through:

`I050 calibrated_reproducible -> I066 materialized_reproducible -> I123 measured_reproducible BackendEvidence`.

This remains resource evidence only. It does not create a market route, fresh market demand evidence, authorization, credentials, task acceptance/submission, paid infrastructure or value movement.

## Isolation
The quota/rate semantic builder rejects every backend other than exact `python_local` / `deterministic_python` and rejects reference drift where quota/rate cease to be `None`. Therefore the interpretation cannot be reused for CI, owned PC, subscription assistants, external APIs or VPS providers.

## Runtime integration
`run_no_spend_bundle()` executes I113 once plus the fixed local probe in an executable checkout. Without explicit energy inputs it remains `PASS_BLOCKED`. With valid energy inputs it can become `RESOURCE_AND_RUNTIME_READY` only when the I113 receipt is also `PASS_BLOCKED`.

The current connector still does not provide an executable exact-current checkout or authenticated manual `workflow_dispatch`, so no runtime/resource PASS is claimed in this source checkpoint.

## Numbering cleanup
A concurrent stale status path had already created the real I127 (`i127_exact_local_evidence_packet.py`) while STATUS still displayed I126. A temporary duplicate I127 draft created during this run was removed and the new work was renumbered I128. Repository continuation should treat I127 exact-local-evidence and I128 resource-completion as the authoritative sequence.

## Safety
No production DNS/HTTP, credentials, CI dispatch, paid account, server/GPU rental, deposit/stake, task acceptance, submission, KYC, wallet, settlement, spend or value movement occurred.

## Next broad stage
At the first exact-current executable checkout:

`python implementation/i128_python_local_resource_completion.py --root .`

Run once without guessing energy. If trustworthy no-spend energy telemetry and an explicit electricity tariff are available, supply those measured values and materialize the resulting I050/I066/I123 resource evidence. In the same broad stage consume the exact I113 receipt and emit one final current resource-readiness packet.

Only after a current non-synthetic positive-margin resource route exists should the project move to separately authorized fresh read-only market observation. Exact explicit authorization remains an independent later gate.