# Implementation Runs I133–I135 — conservative routing/readiness integration

Date: 2026-08-23
Status: **COMPLETED AS BROAD SOURCE CHECKPOINT — CURRENT RUNTIME/MEASUREMENTS STILL PENDING**

## Objective
Turn the separate I123/I130/I131 components into a useful pre-test decision chain, and define what to do next when the preferred backend cannot yet be materially evidenced.

## I133 — integrated conservative route gate
Added `i133_conservative_route_gate.py`. I133 takes a real `TaskEconomics`, one execution backend and an I131 watcher budget, runs the I130 stress envelope, allocates watcher acquisition overhead per surviving candidate, and requires every configured stress case to remain above the task's conservative absolute and ratio margin thresholds.

This closes an important economic gap: a backend can no longer look positive merely because its direct execution cost is low while polling/dedupe/AI/maintenance acquisition overhead consumes the margin.

## I134 — backend evidence-acquisition planner
Added `i134_backend_evidence_acquisition_planner.py`. It ranks evidence work rather than pretending unavailable backends are executable. The preference is no-new-spend autonomous/programmatic evidence acquisition first. `python_local` remains first; free/conditional CI, local model and owned-PC branches remain possible evidence branches but require their own capacity/policy/energy facts. Subscription ChatGPT/Codex remains support-only, not an autonomous API. External APIs and VPS retain credential/spend/infrastructure authorization boundaries.

This gives the implementation a deterministic fallback when local execution cannot be proven economical: move to the next already-defined backend evidence branch instead of reopening broad market discovery.

## I135 — integrated pre-observation readiness packet
Added `i135_pre_observation_readiness_packet.py`. A single packet now combines six independent requirements: exact-current runtime receipt, measured non-synthetic backend evidence, conservative I133 economics, watcher overhead accounting, fresh market/policy evidence and exact observation authorization.

Even a `READY_FOR_SINGLE_READ_ONLY_OBSERVATION` packet does not execute anything; `observation_enabled` remains false in this layer. It is a handoff boundary, not permission widening.

## Verification coverage
Added `test_i133_i135_broad_readiness.py` covering:
- watcher overhead being included in route economics;
- high acquisition overhead destroying a nominal margin;
- python_local acquisition priority;
- subscription assistant remaining support-only;
- VPS retaining infrastructure authorization;
- current false gates producing HOLD;
- all supplied gates producing readiness without executing the observation.

No exact-current executable checkout is available through the current connector, so no runtime test PASS is claimed here.

## Safety / CI
No production DNS/HTTP, workflow dispatch, credentials, paid account, task acceptance, KYC, wallet, settlement, spend or value movement occurred. Automatic CI remains disabled.

## Outcome
The Resource / Execution Router now has an end-to-end conservative planning chain:

`backend evidence -> I123 base route economics -> I130 uncertainty stress -> I131 watcher/acquisition overhead -> I133 conservative route gate -> I135 pre-observation readiness`.

If the preferred backend is blocked, I134 chooses the next evidence-acquisition branch without broad rediscovery.

## Next broad stage
At the first executable current checkout, run the full local chain once (I113 + I128/I129 -> I050/I066/I123), then immediately apply I133 using a realistic watcher budget. If that current route survives, build I135 with fresh market/policy evidence and ask for the exact one-shot observation authorization only then. If local economics fail, use I134 to move to the next no-new-spend evidence branch and evaluate it in the same conservative framework.
