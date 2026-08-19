# Implementation Run I021 — deterministic production evidence watchlist planner

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Turn the production-only archive/freshness state into a deterministic read-only sampling plan. The planner must decide **what should be checked next and why** without performing network traffic, authenticating, accepting work, publishing services, or enabling value-moving actions.

## Changes
Added `implementation/sampling_planner.py`.

The planner:
- defines an explicit watch target for each shortlisted platform;
- assigns platform priority and per-platform freshness horizon;
- uses **production-only** archive evidence; testnet/unknown observations never satisfy a production gap;
- distinguishes missing production observation, missing positive open-demand evidence, missing paid-utilization evidence, stale evidence, future-invalid evidence, and fresh complete evidence;
- emits deterministic scores where platform priority is deliberately dominant and evidence gaps/freshness refine ordering;
- keeps every output plan-only with `network_calls_performed=False` and `action_enabled=False`;
- carries explicit public observation URLs/targets but does not fetch them;
- never treats supply/listing/provider counts as demand.

Current default watch order favors PayanAgent first, then OKX.AI A2A / agent2agent.market / MCPize, with AgentGigs behind them. Ties are deterministic by platform name.

Added `implementation/test_sampling_planner.py` covering:
1. empty archive / never-observed prioritization;
2. testnet evidence not satisfying production gaps;
3. stale high-priority evidence outranking a fresh lower-priority check;
4. positive open demand still leaving a paid-utilization gap;
5. fresh complete evidence becoming not-due;
6. future-invalid timestamps failing closed;
7. report-level no-network/no-action invariants.

## Fresh public read-only checkpoint — 2026-08-19
### PayanAgent
The current first-party homepage/API reference still documents anonymous `GET /api/v1/discover` and `GET /api/v1/receipts`, the machine-native request/bid/fulfill lifecycle, x402/USDC on Base, and 24,000+ offers. Search-visible first-party material did not expose a raw attributable timestamped production request/receipt payload in this run. Catalog supply remains explicitly excluded from demand evidence.

### MCPize
Current first-party developer/monetization pages still document the standard 80% creator share, Stripe Connect subscriptions, x402 pay-per-call USDC on Base, and Base Sepolia testing. The developer portal still advertises 900+ servers and 450+ publishing developers. Those are supply-side counts; no attributable public buyer-utilization series was established in this run.

## Safety / external actions
No account/login/KYC, API key, wallet creation/funding, bid, task acceptance, task submission, monetized publication, paid API/server, transaction, settlement, or prohibited automation occurred.

## Git / CI
Push-triggered CI remains disabled and the workflow is unchanged. This stage is committed atomically with code, tests, sources, status, handoff and run log.

## Outcome
The stack can now turn sanitized production evidence history into a reproducible observation queue. This prevents ad-hoc repeated browsing and makes stale/unproven high-priority markets surface automatically while already-fresh complete evidence can fall out of the due queue.

The principal blocker remains the same: attributable production demand/utilization for the strongest candidates is not yet captured without crossing account/onboarding boundaries.

## Next — I022
1. Add a deterministic sampling manifest/execution contract derived from the planner with per-source rate limits, expected evidence class, provenance and capture deadlines.
2. Keep the manifest inert: it may describe permitted GET/read-only checks but must not execute network traffic itself.
3. Bridge successful future read-only captures into the existing `observation_capture` → archive → replay path with explicit environment tagging.
4. Continue anonymous public production-demand checks and document any observability gate rather than bypassing it.
