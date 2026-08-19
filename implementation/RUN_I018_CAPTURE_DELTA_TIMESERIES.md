# Implementation Run I018 — reproducible capture/delta runner + exact time-series scorecard

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a reproducible, read-only runner above the I016/I017 signed bundle + registry stack so already-captured public observations can be admitted with explicit freshness and per-source rate-limit guards, converted into exact registry deltas, and exported as a non-extrapolating time series.

## Changes
Added `implementation/observation_capture.py`.

The runner:
- accepts only already-captured observation bundles; it contains no HTTP/network client;
- reuses `index_bundle()` / `add_bundle()` so bundle integrity/dry-run invariants remain upstream requirements;
- requires HTTPS public provenance;
- rejects stale source snapshots, excessive future clock skew, capture-time regression and too-frequent repeated capture of the same `(platform, source_url)`;
- records whether a request snapshot hash is genuinely new for that platform;
- records exact before/after latest demand state rather than inventing trend semantics;
- exports registry state, exact registry deltas, the existing cross-market scorecard and a new exact time-series scorecard;
- preserves each paid observation independently and explicitly sets paid-value aggregation/extrapolation to disabled.

Added `implementation/test_observation_capture.py` with eight isolated tests covering fresh zero-open capture, stale rejection, future-skew rejection, HTTPS-only provenance, per-source rate limiting, repeated-snapshot distinction, exact paid observation preservation and deterministic batch ordering/action-disable invariants.

Isolated local result: **8 passed**.

## Public read-only checkpoint — 2026-08-19
### PayanAgent
First-party public material still documents anonymous `GET /api/v1/discover`, public `GET /api/v1/receipts`, API-key-gated seller/request actions, x402 settlement and a 24,000+ offer/catalog claim. The catalog count is supply, not buyer demand. No raw attributable timestamped request or receipt API payload was captured in this environment, so the quantitative demand/utilization state remains unmeasured.

### agent2agent.market
The public first-party app currently renders `Open tasks 0`, `all 0`, and `no open tasks`, but the same interface is explicitly labeled `base-sepolia`. Therefore this is retained only as a **testnet/public-app observation**, not as evidence of zero production demand. The homepage/docs still document anonymous task browsing and machine-native accept/submit/USDC settlement mechanics.

### MCPize
Current first-party monetization docs still document subscription + x402 pay-per-call monetization, standard 80% developer revenue share, Base USDC settlement and free Base Sepolia testing. Real-time payment analytics are described in publisher/dashboard context. No publisher account or wallet was created, so attributable utilization remains gated rather than inferred from marketplace/listing counts.

## Safety / external actions
No account/login/KYC, API key, wallet creation/funding, task acceptance, bid, submission, service publication, paid API/server, transaction or settlement occurred. No network-fetch implementation was added; the runner consumes saved evidence only.

## Git / CI
Push-triggered CI remains disabled and the workflow is unchanged. This stage is persisted as one atomic commit containing code, tests, documentation, sources and checkpoint files.

## Outcome
The evidence stack can now replay a sequence of saved public observations reproducibly and distinguish: (a) duplicate bundles, (b) repeated identical market snapshots, (c) newly observed market states, (d) exact zero-open states, (e) positive open demand, and (f) paid utilization — without converting any of those into unsupported revenue forecasts.

The primary bottleneck remains external observability: raw attributable production demand/utilization is not yet available from the public surfaces observed so far.

## Next — I019
1. Add a deterministic sanitized fixture-import/export command for capture reports and registry state, with schema/version/hash validation and append-only audit semantics.
2. Add explicit environment/network classification (`production`, `testnet`, `unknown`) so testnet zero-open observations can never affect a production scorecard.
3. Continue permitted public observation for PayanAgent request/receipt feeds and agent2agent production surfaces; save a sanitized fixture only if a raw attributable payload is actually obtainable.
4. Keep MCPize on the public-only branch and document the onboarding boundary rather than creating a publisher account.
