# Implementation Run I017 — deterministic bundle registry + cross-market evidence scorecard

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a deterministic history/index layer above the portable I016 bundles so repeated observations can be compared without double-counting bundle hashes, collapsing zero-open observations into positive demand, or extrapolating paid utilization across mismatched snapshots.

## Changes
### 1. Bundle registry/history
Added `implementation/bundle_registry.py`.

The registry rejects duplicate `manifest_sha256` values globally, stores exact request snapshot/provenance data, distinguishes `positive_open_demand`, `zero_open_observation`, and `unproven`, preserves paid utilization as a stronger evidence state, rejects action-enabled/non-dry-run bundles, and preserves deterministic ordering independent of input order. An empty list is only a zero observation for that exact snapshot; it is not proof of platform-wide absence of demand.

### 2. Cross-market scorecard
The scorecard reports observation count, distinct request-snapshot count, latest source timestamp/state/open count, positive versus zero-open counts, paid-utilization count, strongest evidence seen, and the latest exact paid observation when present. Paid values are never summed or annualized across snapshots: `cross_snapshot_paid_value_sum_usd = null` and `cross_snapshot_extrapolation = false`.

### 3. Tests
Added `implementation/test_bundle_registry.py` with eight deterministic tests covering global hash deduplication, zero/positive separation, paid-utilization precedence without summing windows, deterministic ordering, repeated snapshot visibility, action-enabled rejection, empty open-paid evidence rejection and immutable dry-run state.

Local isolated result: **8 passed**.

## Public read-only checkpoint — 2026-08-19
### PayanAgent
Current first-party pages still document anonymous discovery/receipts, API-key-gated bid/fulfill/approve operations, x402/USDC settlement and public receipts. The rendered Requests page exposes `0 open` while also showing a loading state. This is retained only as a rendered zero-open observation; no raw timestamped API payload was captured, and the 24,000+ catalog claim is not treated as demand.

### agent2agent.market
Current first-party pages still document anonymous task browsing and machine-native accept/submit/USDC settlement. The public app shell exposes dashes for Open tasks / Total bounty / Median pay rather than attributable live counts. Homepage examples are documentation examples, not demand observations. Current anonymous quantitative demand remains **unmeasured**.

### MCPize
Current first-party material still documents 80% standard developer revenue share and x402 pay-per-call. Publisher-side payment analytics remain the strongest attributable utilization surface and require publisher/account context. No account was created and no utilization was inferred from marketplace counts or examples.

## Safety / external actions
No login, account creation, API key, KYC, wallet creation/funding, task acceptance, bid, submission, service publication, paid API/server, transaction or settlement occurred. The registry has no network or value-moving functions.

## Git / CI
Push-triggered CI remains disabled. No workflow change was made. This stage is persisted as one atomic commit.

## Outcome
The implementation now has both a portable evidence layer and a deterministic cross-market history layer. Exact zero observations cannot erase historical positive evidence, duplicate bundles cannot inflate evidence, and overlapping windows cannot manufacture revenue.

The bottleneck remains external: attributable current paid demand/utilization is still sparse or gated.

## Next — I018
Add a reproducible observation-capture plan/runner that can ingest public read-only snapshots from multiple markets when raw payloads are available, persist registry deltas, and produce a time-series scorecard while preserving source freshness and rate limits. Continue PayanAgent request/receipt observation and agent2agent public task observation; do not create accounts or wallets merely to unlock metrics.
