# Implementation Run I049 — observation-to-resource routing integration

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Integrate the I048 Resource / Execution Router with the existing task observation/orchestrator path without allowing cheap execution to override upstream policy, capability, quality, or demand-evidence gates.

## Changes
Added `implementation/execution_routing_integration.py`.

The bridge now:
- consumes the same task tuple/payload contract used by the observation orchestrator;
- calls `observe_task()` first, preserving evaluator policy/capability/quality/cost gates and demand-evidence classification;
- refuses to construct or invoke a resource route when the upstream observation is `hold` or `reject`;
- converts only an upstream `accept_dry_run` task into router-compatible `TaskEconomics`;
- isolates optional payment-risk/fee overrides under an explicit `routing_economics` namespace so ordinary task metadata cannot silently alter the economic model;
- preserves gross payout and required capabilities from the normalized market adapter;
- then invokes I048 `route_task()` and records the selected backend only when the router itself returns `route_dry_run`;
- emits one combined `RoutedTaskObservation` with upstream state/economics, demand evidence, router economics/quotes and selected backend;
- keeps `dry_run_only=true`, `execution_enabled=false`, `network_enabled=false`, and `value_movement_enabled=false`.

Added `build_routed_task_queue()` so multiple task observations can be passed through the combined upstream-gate → resource-route pipeline. Routable dry-run candidates rank ahead of held/rejected items, but no queue state enables action.

## Important invariant
Resource price is downstream of safety/evidence. A $0 execution backend cannot rescue:
- prohibited work;
- unsupported capability;
- insufficient policy/source-rights evidence;
- missing quality contract;
- unproven open paid demand.

Likewise, a task that passes upstream observation can still be held by the Resource Router when explicit payment/acceptance/dispute/non-payment economics make the conservative route unattractive.

## Verification
Added `implementation/test_execution_routing_integration.py` with seven deterministic tests covering:
1. permitted open paid task routes to the cheapest eligible backend;
2. high-bounty prohibited work never reaches routing;
3. unsupported capability never becomes routable because execution is cheap;
4. listing-only evidence remains held before routing;
5. explicit acceptance/dispute/non-payment risk can turn an upstream accept into a routing hold;
6. subscription-backed ChatGPT/Codex-style support remains visible but cannot become a free autonomous API;
7. combined routed records remain execution/network/value-movement disabled.

Isolated bridge-harness verification: **7 passed**. The harness used interface-compatible local stubs because the execution container had no GitHub network access; repository code was not executed through GitHub Actions. The integration is deliberately dependency-light and matches the current `observe_task`, market-adapter and `route_task` contracts.

## Safety / external actions
No DNS/HTTP, credential, login/KYC, paid API, ChatGPT/Codex programmatic call, wallet, payment, task acceptance, service publication, server rental, settlement or value movement occurred. No GitHub Actions workflow was dispatched and push-triggered CI remains disabled.

## Outcome
The project now has a single inert path:

`market payload -> normalized observation/policy/demand gate -> TaskEconomics -> Resource Router -> selected backend dry-run record`

The upstream evidence gate is authoritative and resource routing can only narrow, never widen, eligibility.

The economic gap remains: default backend costs/capacities are still synthetic reference values and no real permitted production demand/utilization sample has yet been taken.

## Next run — I050
Build a deterministic resource-profile evidence/calibration layer. Separate synthetic reference backends from measured/declared real available resources; bind availability, fixed/sunk cost, quota, electricity, latency, reliability/quality and interface constraints to explicit evidence/provenance. Unknown or stale resource parameters must remain planning-only. Keep execution/network/value movement disabled.

Project state: **IMPLEMENTATION IN PROGRESS**.
