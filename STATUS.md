# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I016 — portable multi-market observation bundles**
Last updated: **2026-08-19**

## Current objective
Build a legal server-native agent that can observe machine-readable paid work, estimate execution cost and expected margin, reject unsafe/non-compliant/unprofitable tasks, and eventually execute only positive-margin work after explicit authorization for credentials/money-moving actions.

## Latest durable files
- `implementation/RUN_I016_PORTABLE_MULTI_MARKET_BUNDLES.md`
- `implementation/SOURCES_I016.md`
- `implementation/observation_bundle.py`
- `implementation/test_observation_bundle.py`
- `implementation/RUN_I015_OBSERVATION_BUNDLE.md`
- `implementation/payan_sanitizer.py`
- `implementation/utilization_history.py`
- `implementation/receipt_aggregation.py`
- `implementation/observation_importer.py`
- `implementation/snapshot.py`

## I016 outcome
The signed offline evidence bundle is now portable and fail-closed on reload. `serialize_observation_bundle` emits deterministic JSON; `load_observation_bundle` requires the exact top-level/manifest schema, supported schema version, internally consistent component hashes, immutable dry-run/action-disabled flags and a valid caller-supplied HMAC key. Child-snapshot payload tampering is detected even if an attacker leaves the old manifest/signature in place.

The request-envelope pattern now supports a second task market, `agent2agent.market`. Its sanitizer accepts only open positive-bounty USD/USDC tasks, normalizes aliases/deadlines/skills, discards platform-supplied policy assertions, and injects rights/ToS/automation/source-data permission plus cost estimates only from caller-controlled trusted mappings. The resulting bundle reuses the same snapshot → importer → evidence-aware orchestrator → signed manifest path and stays `dry_run_only=True`, `action_enabled=False`.

Fresh public checks on 2026-08-19:
- PayanAgent still documents anonymous `GET /api/v1/discover` and `GET /api/v1/receipts`, with request bid/fulfill/approve operations API-key-gated and settlement/receipts designed around x402/USDC. No trustworthy raw attributable response + source timestamp was captured, so no demand/utilization figure was created.
- `agent2agent.market` documents an anonymous open-task feed and machine-native worker lifecycle, but its currently rendered app surface showed **0 open tasks** and no live activity. This is a real zero-open observation, not positive demand.
- MCPize still documents seller monetization through subscriptions and x402 pay-per-call. Public developer pages show 80/20 subscription economics; its public x402 material describes a settlement ledger/7-day revenue metrics in the publisher Payments view, meaning the strongest attributable utilization surface appears account/publisher gated rather than anonymously observable. No utilization estimate was inferred from marketplace/server counts or revenue examples.

Push-triggered CI remains disabled. I016 is persisted as one atomic commit. No account, KYC, API key, wallet, paid infrastructure, service publication, task acceptance, bid or settlement was created.

## Current ranking
1. **PayanAgent** — primary task-market target; end-to-end evidence pipeline ready, but quantitative open-request/settled-utilization data remains uncaptured.
2. **OKX.AI A2A ASP** — architecture confirmed; provider-side live demand observation appears onboarding-gated.
3. **agent2agent.market** — now bundle-ready; public task feed remains observable but current rendered state showed 0 open tasks.
4. **AgentGigs.io** — autonomous lifecycle but prior public jobs zero; Stripe Connect geography/KYC gate.
5. **MCPize** — strongest passive paid-endpoint candidate; monetization mechanics strong, attributable utilization appears publisher/account gated.

## Durable implementation rules
- Demand/fill rate is the dominant unknown; supply/listing/provider counts are not demand.
- Open paid demand and historical paid utilization are different evidence classes.
- Platform payloads cannot self-authorize compliance; trusted policy evidence stays separate.
- Raw buyer identities must not persist.
- Never extrapolate mismatched observation windows.
- Empty feeds must not be promoted to positive-demand evidence.
- Persisted evidence bundles must fail closed on schema/version/hash/signature mismatch.
- Bundle HMAC is an offline integrity seal only; it never authorizes value-moving action.
- Never spend money, fund a wallet, stake/deposit, rent paid infrastructure, create paid accounts, submit KYC, or take irreversible external action without explicit user authorization.
- No CAPTCHA bypass, spam, fake activity, ad fraud, prohibited multi-accounting, credential abuse, geofence/KYC evasion, unauthorized access/scraping, or automation of human-only work contrary to ToS.

## Immediate next run — I017
Add a deterministic observation-bundle registry/history index that deduplicates bundle hashes across platforms, records zero-demand versus positive-demand observations without extrapolation, and produces a cross-market evidence scorecard. Continue anonymous/public quantitative observation for PayanAgent and agent2agent.market; deepen MCPize only through public surfaces and document the onboarding gate rather than creating an account.

## Completion gate
Implementation is complete only if either a documented autonomous stack achieves confirmed positive economics on real permitted tests, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then: **IMPLEMENTATION IN PROGRESS**.
