# Implementation Run I011 — snapshot replay + CI diagnosis + demand observability refresh

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Close the next offline safety gap by replaying only integrity-checked/fresh evidence into market adapters, diagnose the historical pytest failure without restoring push-triggered email noise, and refresh public read-only evidence for PayanAgent/MCPize without inventing utilization.

## Changes
### 1. Verified snapshot-to-adapter replay
Extended `implementation/snapshot.py` with:
- `validate_snapshot()` — re-checks evidence class, HTTPS provenance, payload hash, timestamps and freshness at replay time;
- `records_from_snapshot()` — fail-closed extraction of a declared list contract;
- `replay_task_snapshot()` — feeds only verified records to a known adapter;
- evidence `source_timestamp` overrides any timestamp embedded in the raw record, preventing stale/untrusted payload timestamps from silently becoming the evaluator observation time;
- unknown platforms, tampered payloads, stale evidence and malformed record collections are rejected.

Extended `implementation/test_snapshot.py` for replay-time tamper/staleness checks, malformed record contracts, timestamp override and unknown-platform rejection.

Added `implementation/fixtures_i011_synthetic_snapshots.json`. It is explicitly marked `synthetic: true` and exists only for schema/replay tests; it is not buyer-demand evidence.

### 2. Historical CI failure diagnosis
The exact old Actions job log is not available through the current connector, so no false certainty is claimed. However, commit `f50e42324d4dd2cfb2f43e3932fe602d1a59268c` shows that the workflow previously invoked `python -m pytest -q` without a pytest installation step, and that commit explicitly added `python -m pip install ... pytest` before running the suite. This is strong evidence that the historical failure cluster was at least consistent with a missing test-runner dependency.

Automatic `push` execution remains disabled. The workflow is still available through `workflow_dispatch` and pull requests. No manual CI dispatch was performed in this run because a failed manual run could recreate unwanted notification mail and the user explicitly requested notification hygiene. Therefore **green CI is still not claimed**.

### 3. Fresh public demand/market refresh
Evidence date: 2026-08-19.

**PayanAgent** official public homepage still documents:
- 24,000+ catalog offers;
- anonymous `GET /api/v1/discover`, `GET /api/v1/offers`, and `GET /api/v1/receipts` surfaces;
- provider registration/listing plus request/bid/fulfill/approve lifecycle;
- USDC/x402 settlement and signed receipts.
Source: https://payanagent.com/

This strengthens the observability design because a public receipt feed is explicitly documented. It still does **not** establish the current rate of bespoke paid requests or the revenue available to our candidate worker. Search/web tooling in this environment did not yield a sanitized raw JSON response suitable for a real evidence snapshot, so quantitative demand remains unmeasured rather than inferred from the 24k offer count.

**MCPize** current official pages document:
- developer 80% revenue share / 20% platform fee for newly monetized servers;
- monthly Stripe Connect payouts for subscription revenue;
- x402 per-tool USDC payments on Base and free testing on Base Sepolia;
- a Free hosting tier listed at $0 with 250K requests/month, making a future capped-cost experiment potentially possible without paid hosting;
- account/identity/payout requirements still apply when moving from simulation to monetization.
Sources: https://mcpize.com/developers ; https://mcpize.com/faq ; https://mcpize.com/terms

Again, marketplace/server counts and example revenue calculators are supply/marketing signals, not attributable paid utilization. No demand value was assigned.

## Safety / external actions
No login, account creation, KYC, wallet, task acceptance, bid, publication, paid API/server, transaction, settlement, CI dispatch or money movement occurred.

## Outcome
The offline stack now has an evidence boundary before normalization: raw observations cannot reach adapters unless provenance, hash integrity, freshness and record shape pass. This makes future public snapshots reproducible and prevents an untrusted embedded timestamp from weakening staleness controls.

The next practical bottleneck is no longer adapter architecture; it is acquiring attributable, permitted, fresh demand observations and then mapping those observations into the existing evaluator/orchestrator.

## Next run — I012
1. Add a read-only observation importer contract that can ingest saved JSON/API exports without performing network calls itself.
2. Add demand-evidence scoring (`settled_receipt`, `open_paid_request`, `listing_only`, `marketing_claim`) so orchestrator ranking cannot confuse supply with utilization.
3. Extend audit export with evidence-strength counts and hold reasons.
4. Continue public PayanAgent receipt/request evidence checks and MCPize attributable-demand checks. Save a real sanitized snapshot only if a permitted raw payload becomes observable.
5. Keep CI push trigger disabled; do not manually dispatch merely to prove green status unless notification behavior is safe.

Project state: **IMPLEMENTATION IN PROGRESS**.
