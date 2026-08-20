# Implementation Run I048 — Resource / Execution Router foundation

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add the mandatory offline Resource / Execution Router foundation before any real monetization test. The router must distinguish fixed/sunk cost from true per-task marginal cost, model multiple execution backends, and choose the cheapest sufficiently reliable currently usable autonomous backend while keeping all execution inert.

## Changes
Added `implementation/resource_router.py`.

The model now represents execution backends with:
- capability set and autonomous vs support-only role;
- programmatic-access status and policy allowance;
- current availability;
- credential / paid-account / new-spend requirements;
- fixed monthly cost, sunk/already-committed status and optional per-task allocation basis;
- quota/capacity and remaining quota;
- marginal unit cost and units per task;
- electricity, external API/model cost, retry/failure expected cost;
- human maintenance minutes and human-time value;
- opportunity cost;
- latency, reliability and quality probability;
- parallelism and rate limits.

Synthetic reference backend families are included for:
1. deterministic local Python;
2. local CPU/GPU/model execution;
3. subscription-backed ChatGPT/Codex-style assistance as a fixed/limited **non-API support resource**;
4. cheap external LLM/API;
5. stronger external LLM/API;
6. free-tier CI/cloud;
7. owned-PC execution;
8. future paid VPS/server.

The subscription-backed profile is deliberately not treated as a free autonomous API: it is visible as an already-paid/sunk resource for support/accounting, but `programmatic_access=false` and `automation_role=support_only`, so it cannot silently become an autonomous execution backend.

## Economics and routing
Added `TaskEconomics`, `BackendQuote` and `RoutingDecision`.

For each backend the router computes:
- marginal execution cost separately from fixed/sunk cost;
- optional amortized fixed cost only when a non-sunk recurring resource has an explicit monthly task-allocation basis;
- effective success probability = reliability × quality probability;
- expected collectible revenue after acceptance, dispute and non-payment probabilities;
- platform/transaction/gas/withdrawal/conversion fees;
- conservative expected margin and margin ratio.

Routing behavior:
- capability, quota, policy and quality/reliability gates fail closed;
- currently unavailable, credentialed, paid-account and new-spend resources can remain visible as `planning_only`, but cannot beat a currently available backend in the dry-run route;
- available eligible resources are ordered by lowest marginal cost, then higher expected margin/reliability and lower latency;
- every decision remains `dry_run_only=true`, `execution_enabled=false`, and every quote has `action_enabled=false`.

This prevents two opposite accounting errors: charging a full already-paid monthly subscription to every task, and pretending a fixed/limited subscription is a free unlimited programmatic API.

## Watcher foundation
Added an inert `WatcherPolicy` validator for future polling/webhook/WebSocket workers.

The architecture permits a future watcher to operate more frequently than chat-level automation **only** when the source API/ToS/rate limits allow it. The default policy requires local deterministic filtering before AI, disallows LLM invocation on every poll, rejects rate-limit/product-limit bypass, and keeps network access disabled in I048.

Target future flow:
`cheap poll/webhook/ws -> local parsing/dedupe/filter -> only promising opportunities -> Resource Router -> AI/backend only when justified`.

## Verification
Added `implementation/test_resource_router.py` with ten deterministic tests covering:
1. cheapest available marginal-cost route selection;
2. subscription resource visibility without free-API assumption;
3. credentialed/unavailable API remains planning-only;
4. future paid VPS requires authorization and explicit fixed-cost allocation basis;
5. non-sunk monthly cost is amortized rather than charged in full per task;
6. acceptance/dispute/non-payment risk reduces expected revenue;
7. weak-quality cheap backend loses to sufficiently reliable backend;
8. insufficient quota fails closed;
9. fast polling is valid only inside platform limits and remains network-off;
10. rate-limit bypass and LLM-on-every-poll policies are rejected.

Isolated local verification: **10 passed**.

## Safety / external actions
All backend prices/capacities are synthetic reference values, not claims about current vendors. No external API, model credential, ChatGPT/Codex programmatic access, DNS/HTTP, login/KYC, wallet, payment, paid server, task acceptance, publication, settlement or value-moving action occurred. GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Outcome
The implementation now has an explicit resource-accounting and backend-selection layer. It can distinguish existing/sunk resources from marginal task cost and can prevent unavailable/credentialed/new-spend resources from being chosen as if they were already usable.

The economic gap remains unchanged: no real demand/utilization capture or paid task has yet occurred.

## Next run — I049
Integrate the Resource / Execution Router into the existing observation/orchestrator path. Convert accepted normalized task observations into router-compatible `TaskEconomics`, preserve demand-evidence and policy gates, and emit one combined dry-run record containing opportunity economics plus selected execution backend. Add deterministic tests proving that a high-bounty unsafe/unsupported task cannot become routable and that a low-cost backend cannot override upstream policy/demand holds. Keep all execution/network/value movement disabled.

Project state: **IMPLEMENTATION IN PROGRESS**.
