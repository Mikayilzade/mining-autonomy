# Implementation Run I002 — PayanAgent read-only market / receipt sampler checkpoint

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E1**

## Objective
Validate the read-only surface needed for a PayanAgent worker and attempt to measure buyer-side demand without registration, bidding, wallet signing, purchases, or other value-moving actions.

## Current first-party surface confirmed
Fresh first-party material confirms PayanAgent remains API-first and exposes public read paths without authentication:
- `GET /api/v1/discover` — unified agents/offers/open-request discovery;
- `GET /api/v1/offers` — public catalog;
- `GET /api/v1/requests` and request detail — public request observation according to current machine-facing documentation;
- `GET /api/v1/receipts` — live public settled-transaction feed;
- agent receipt history/statistics are public;
- seller/request actions require an API key;
- direct buys use x402/USDC on Base.

The current public site still advertises 24,000+ offers, but this is explicitly treated as **supply**, not demand.

## Attempted live sampling
The run attempted direct read-only retrieval of the public request and receipt endpoints. The available web execution path could confirm the endpoint contract and current first-party documentation, but did not expose the raw JSON response bodies for the direct API endpoints in this environment. A secondary container attempt was blocked by environment DNS/network resolution. Therefore **no request count, receipt count, bounty distribution, buyer count, or transaction velocity is invented in this run**.

This is an environment-observability limitation, not evidence that the feeds are empty.

## Demand evidence status after I002
- Open-request mechanism: **CONFIRMED**.
- Public receipt mechanism: **CONFIRMED**.
- Current quantitative open-request density: **UNMEASURED in this execution environment**.
- Current quantitative settled demand: **UNMEASURED in this execution environment**.
- 24k+ catalog: **not usable as demand evidence**.

PayanAgent remains Rank #1 for architecture/dry-run work, but a real-money test is not justified until actual demand can be sampled or independently observed.

## Common opportunity schema v0.1
The following platform-neutral shape should be used by E3 adapters:

```json
{
  "platform": "payanagent",
  "external_id": "string",
  "observed_at": "ISO-8601",
  "kind": "request|offer|job|call",
  "status": "open|closed|unknown",
  "title": "string|null",
  "description": "string|null",
  "tags": [],
  "budget_min_usd": null,
  "budget_max_usd": null,
  "fixed_payout_usd": null,
  "currency": "USDC|USD|other|null",
  "deadline": null,
  "bid_count": null,
  "buyer_id": null,
  "buyer_reputation": null,
  "escrowed": null,
  "input_schema": null,
  "output_schema": null,
  "requires_auth_to_accept": true,
  "requires_value_moving_action": true,
  "source_url": "string",
  "raw_observation_hash": "string|null"
}
```

## Receipt schema v0.1

```json
{
  "platform": "payanagent",
  "receipt_id": "string",
  "observed_at": "ISO-8601",
  "settled_at": null,
  "seller_id": null,
  "buyer_id": null,
  "amount_usd": null,
  "currency": "USDC",
  "transaction_hash": null,
  "request_id": null,
  "offer_id": null,
  "success": null,
  "source_url": "string"
}
```

## Demand metrics to compute once raw feed access is available
For each rolling window (1h / 24h / 7d where history permits):
1. unique open requests;
2. newly opened requests;
3. requests with explicit non-zero budget;
4. median / p25 / p75 budget;
5. bids per request;
6. unique buyers;
7. settled receipts;
8. unique paying buyers and sellers;
9. total settled USD/USDC;
10. median receipt value;
11. repeat-buyer rate;
12. request-to-settlement ratio where linkage exists;
13. concentration: top buyer/seller share;
14. task categories compatible with deterministic/cheap execution.

## Conservative implementation gate
Do not promote PayanAgent to a money test merely because the API exists. Promotion requires at least one of:
- repeated public snapshots showing non-trivial bespoke request arrival plus credible budgets; or
- attributable settled receipts showing repeat organic buyers for capabilities we can execute cheaply.

Before any future bid, the evaluator must also pass policy, rights, geography, worst-case cost and margin gates.

## No-action boundary respected
No account was created. No API key was requested. No wallet was created/funded. No bid/request/fulfillment was submitted. No USDC was moved. No paid infrastructure was used.

## Result
E1 contract validation is complete; quantitative demand sampling remains pending because raw public API bodies were not reachable through the present execution environment.

### Next run
**I003 / E2 — OKX.AI A2A ASP task-intake observability**, while retaining PayanAgent for later repeated public snapshots. In parallel, begin the platform-neutral E3 adapter/evaluator design using the schema above so implementation can advance even when a market feed is temporarily inaccessible.

Project state: **IMPLEMENTATION IN PROGRESS**.
