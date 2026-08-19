# Implementation Run I020 — production-only archive replay + freshness bridge

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Allow the unified offline orchestrator to consume sanitized archive evidence without ever admitting testnet/unknown observations into production conclusions, and make evidence age/freshness explicit so old production observations cannot silently remain current.

## Changes
Added `implementation/archive_replay.py`.

The bridge:
- reads only sanitized `EvidenceArchive` entries;
- admits only explicit `environment == production` observations;
- excludes testnet and unknown observations before orchestrator replay;
- selects the latest production observation per platform;
- computes source age and classifies evidence as `fresh`, `stale`, or `future_invalid` with a bounded future-clock-skew policy;
- converts archive evidence into `ObservationItem` records that are **always HOLD-only** and `action_enabled=False`;
- maps positive open demand to `open_paid_request`, positive paid utilization to `settled_receipt`, exact zero-open to a separate evidence class;
- refuses to infer executable economics from sanitized evidence because raw task/service payloads, trusted policy evidence, and cost estimates are intentionally absent;
- preserves non-aggregation of paid value across snapshots.

Added `implementation/test_archive_replay.py` with seven isolated deterministic tests covering environment quarantine, fresh production replay, paid-utilization reporting without action enablement, stale evidence, future skew, latest-observation selection, and the hard no-authorization invariant.

## Fresh public read-only checkpoint — 2026-08-19
### PayanAgent
Current first-party material still documents anonymous `GET /api/v1/discover` and `GET /api/v1/receipts`, request/bid/fulfill lifecycle, x402/USDC settlement on Base, and 24,000+ catalog offers. The catalog count remains supply rather than attributable paid demand. No timestamped raw production request/receipt payload was captured in this run, so production fill rate remains unmeasured.

### MCPize
Current first-party developer material still states an 80% standard developer revenue share, pay-per-call x402 USDC settlement on Base, and free Base Sepolia testing. The developer portal advertises 900+ MCP servers and 450+ publishing developers, but those are supply-side counts; attributable buyer utilization still requires publisher/dashboard evidence or another attributable public source.

## Safety / external actions
No account/login/KYC, API key, wallet creation/funding, bid, task acceptance, task submission, monetized publication, paid API/server, transaction, or settlement occurred. Archive replay remains read-only and cannot enable execution.

## Git / CI
Push-triggered CI remains disabled and the workflow was not changed. This stage is prepared as one atomic commit containing code, tests, docs, sources and checkpoint updates.

## Outcome
The offline control plane can now replay portable evidence history while maintaining a strict production/testnet boundary and explicit freshness state. Archived evidence can influence what to inspect next, but it cannot itself authorize work or claim current profitability.

The principal unresolved blocker remains attributable production demand/utilization for the highest-ranked markets.

## Next — I021
1. Add a production evidence watchlist/sampling planner that schedules read-only rechecks by freshness and evidence gap without generating network traffic by itself.
2. Add explicit per-platform observation targets: PayanAgent open requests + public receipts; MCPize attributable public utilization if any; production-only agent2agent surface if one becomes clearly identifiable.
3. Add a deterministic evidence-gap priority score so stale/unproven high-priority platforms outrank already-fresh low-value checks.
4. Continue without accounts, wallets, paid infrastructure, task acceptance or settlement.
