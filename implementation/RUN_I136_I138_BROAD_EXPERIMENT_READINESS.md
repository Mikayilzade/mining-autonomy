# Implementation Runs I136–I138 — broad experiment-readiness stage

Date: 2026-08-23
Status: **COMPLETED AS BROAD SOURCE CHECKPOINT — EXACT-CURRENT EXECUTION / REAL EVIDENCE PENDING**
Phase: Implementation / Experiment

## Scope
This stage intentionally combines three linked implementation steps instead of another micro-checkpoint. It advances the Resource / Execution Router from single-backend readiness into portfolio-level conservative selection, deterministic resource fallback, and one integrated next-action state machine.

## I136 — conservative portfolio evaluator
Added `i136_conservative_portfolio_evaluator.py`.

I136 evaluates every already-defined execution backend against both:
- I123 production evidence/materialization blockers; and
- I133 conservative economics, which already includes I130 stress and I131 watcher/acquisition overhead.

A backend is a production candidate only when its evidence is current/reproducible/non-synthetic, capacity/policy gates pass, and conservative economics survive. Selection remains deterministic-first and cheapest-qualifying; AI families are considered only when no qualifying deterministic candidate exists.

This closes an earlier architectural gap where economics and evidence existed as separate layers but there was no portfolio-wide conservative decision object.

## I137 — existing-resource fallback ladder
Added `i137_resource_fallback_ladder.py`.

When I136 has no current route, I137 consumes I134's acquisition plan and deterministically chooses the next already-known no-new-spend evidence branch. It does not reopen discovery. The expected order remains led by `python_local`; after an attempted local branch, free/conditional CI is the next existing no-spend branch under the current score model, followed by other already-defined resources as applicable.

Support-only subscription capability remains non-autonomous; external API/VPS execution authorization boundaries remain intact. The ladder records attempted/exhausted branches separately from authorization-blocked/deferred ones.

## I138 — experiment readiness orchestrator
Added `i138_experiment_readiness_orchestrator.py`.

I138 collapses the current control flow into one fail-closed state machine:
1. if no conservative route exists, measure the next existing no-spend resource branch;
2. if a route exists but exact-current runtime is absent, obtain one runtime receipt without restoring automatic CI;
3. if runtime+route exist but fresh market/policy evidence is absent, prepare that evidence acquisition under existing gates;
4. if all prior gates pass but exact authorization is absent, request only the exact single read-only observation authorization;
5. only when every independent gate is true does the packet report `READY_FOR_SINGLE_READ_ONLY_OBSERVATION`.

Even that state does not enable or perform the observation. Execution/network/spend/task-acceptance/value-movement flags remain false.

## Verification
Added `test_i136_i138_broad_experiment_readiness.py` covering:
- economics alone cannot bypass missing evidence;
- measured deterministic `python_local` wins when conservative economics survive;
- fallback stays inside existing no-spend branches and advances to free-tier CI after local is attempted;
- readiness advances runtime -> fresh market/policy evidence -> exact authorization in order;
- route absence takes precedence and sends control back to resource measurement;
- final readiness still does not enable action.

A fresh exact-current clone/test attempt was made from the available execution container and failed before checkout because `github.com` DNS still cannot resolve. Therefore this run does **not** claim executed pytest or exact-current runtime PASS. Automatic CI was not enabled or dispatched.

## Safety / boundaries
No production DNS/HTTP market observation, credentials, paid API, server/GPU rental, deposit/stake, paid-task acceptance, publication, KYC, wallet, settlement, spend or value movement occurred. No rate-limit/CAPTCHA/geofence/product-limit bypass was attempted.

## Conclusions
The control plane now has a materially broader closed loop before real market testing:

`measured resource evidence -> conservative portfolio economics -> fallback to next existing resource -> integrated experiment readiness -> exact observation authorization boundary`.

The remaining blockers are empirical/authorization blockers rather than another missing routing abstraction.

## Risks
- Exact-current runtime remains unavailable in this environment.
- `python_local` still needs genuine I129 energy + explicit tariff evidence before strict materialization.
- Free-tier CI remains unmaterialized and cannot be treated as unlimited/free simply because GitHub Actions exists.
- Fresh market/policy evidence and real demand/fill remain absent.
- No observation authorization exists.

## Files
- `implementation/i136_conservative_portfolio_evaluator.py`
- `implementation/i137_resource_fallback_ladder.py`
- `implementation/i138_experiment_readiness_orchestrator.py`
- `implementation/test_i136_i138_broad_experiment_readiness.py`
- `implementation/RUN_I136_I138_BROAD_EXPERIMENT_READINESS.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/RUN_LOG.md`

## Next action
Keep stages broad. At the first executable exact-current checkout, run the full local chain (I113 + I128/I129 -> I050/I066/I123 -> I136/I138) in one stage and include I130/I131 economics through I133. If local resource materialization cannot be completed or fails conservative economics, immediately advance via I137/I134 to the next existing no-new-spend backend branch in the same broad cycle where practical. Do not reopen discovery and do not perform the production GET until all independent gates and exact user authorization are satisfied.
