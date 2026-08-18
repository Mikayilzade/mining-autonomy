# Implementation Run I001 — Candidate ranking and first experiment gate

Date: 2026-08-18
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Convert the completed discovery map into an implementation shortlist for the original objective: a legal server-native agent that can find paid machine-readable work, estimate execution cost, accept only positive expected-margin work, deliver automatically, and receive payment.

No money, credentials, KYC, wallet funds, paid servers, deposits, or irreversible external actions were used in this run.

## Ranking model
Candidates were ranked on eight dimensions (5 = best):
- direct fit to autonomous paid-work objective;
- evidence of a real programmable seller/worker path;
- evidence of currently observable demand;
- low starting capital;
- low recurring cost before revenue;
- automation ceiling;
- compliance/ToS clarity;
- implementation simplicity.

Demand evidence is deliberately weighted heavily. A technically perfect API with no paid jobs is not a profitable market.

## Current shortlist

| Rank | Candidate | Fit | Automation | Demand evidence now | Capital/cost | Compliance gate | Implementation verdict |
|---|---|---:|---:|---|---|---|---|
| 1 | PayanAgent | 5/5 | 5/5 | Medium: public receipts + 24k+ aggregated offers claimed; request/bid path exists | Very low until paid execution | wallet/USDC + task-specific rights | **PRIMARY DRY-RUN TARGET** |
| 2 | OKX.AI A2A ASP | 5/5 | 4–5/5 | Medium: official active-intake/open-task workflow; paid demand volume still needs measurement | Low | Agentic Wallet, XLayer, marketplace review; geography/KYC to confirm | **PRIMARY VALIDATION TARGET** |
| 3 | agent2agent.market | 5/5 | 5/5 | **Low currently**: official UI observed 0 open tasks / no activity on Base Sepolia despite documented worker flow | Very low | Base wallet; testnet/live-state ambiguity | **WATCH + ADAPTER TARGET, NOT FIRST MONEY TEST** |
| 4 | AgentGigs.io | 5/5 | 5/5 after setup | **Low currently**: public jobs page observed 0 jobs; marketing shows paid example but live fill not demonstrated | Low | one-time email verification + Stripe Connect KYC; Azerbaijan Stripe availability must be confirmed | **WATCH / GEO-GATED** |
| 5 | MCPize | 3/5 | 5/5 | Medium but first-party: claims 900+ servers, 1K+ developers, $200K+ paid to vendors | Low; managed hosting/model/API costs | Stripe Connect + security review + service rights | **PASSIVE SELLER EXPERIMENT CANDIDATE** |
| 6 | OKX.AI A2MCP | 3/5 | 5/5 | Unknown-to-medium; marketplace listing exists, volume unmeasured | Low | x402 endpoint + wallet + review | **SECONDARY PASSIVE TARGET** |
| 7 | API Mart | 3/5 | 5/5 | Low/unproven from Run 062 | Low but upstream usage costs | upstream resale rights + wallet/geography | **WATCHLIST** |
| 8 | Compute/inference suppliers | 2/5 | 4–5/5 | platform-specific | often hardware/capital intensive | hardware/provider admission | **DEFER until task-market tests** |

## Fresh primary-source observations

### PayanAgent
Current first-party site states:
- API-first marketplace for agents and SaaS providers;
- `GET /api/v1/discover`, offers, requests, bids, fulfill and approve endpoints;
- requests support bespoke work with bids and optional escrow;
- settlement/receipts use USDC on Base;
- no platform fee is advertised;
- seller registration/listing is programmatic;
- site currently claims 24,000+ offers, largely aggregated x402 services.

Important distinction: 24k offers measure **supply**, not worker demand. Before a real worker deployment we need to sample the open-request feed and public settled receipts attributable to bespoke requests.

### OKX.AI A2A ASP
Current official tutorial states:
- A2A services can wait for direct offers or **browse open tasks and negotiate to take the order**;
- pricing can be negotiated or fixed per task;
- funds are escrowed on XLayer and released after user approval;
- provider listing is reviewed, normally within 24h according to the tutorial;
- rejected delivery can enter arbitration, requiring a 5% bounty deposit.

This is an unusually direct match, but live task density and Azerbaijan/onboarding availability remain implementation gates.

### agent2agent.market
Current official documentation still describes a machine-native worker flow: register, browse task feed, accept, submit signed deliverable, receive USDC after approval. However the currently observed public app showed **0 open tasks** and no live activity on `base-sepolia`. Therefore it falls below PayanAgent/OKX for a first real-money attempt despite excellent architecture.

### AgentGigs.io
Current first-party site documents the full autonomous lifecycle via REST API, webhooks/SSE, escrow and Stripe Connect payouts after one-time email verification and bank/KYC setup. However the public jobs page currently showed **0 total/open jobs**. It remains technically excellent but demand and payout geography are immediate blockers.

### MCPize
Current first-party developer page advertises one-command deployment, automatic marketplace listing, subscription or per-call monetization, and 80% creator revenue share. Current Terms state a 20% platform fee for monetized servers from 2026-06-10. It is a useful second model: rather than hunt jobs, publish a cheap deterministic capability and wait for paid calls.

## Economic decision rule for the future orchestrator
Never accept work from headline bounty alone.

For task `j`:

`EV_j = P(accepted/hired) × P(approved | hired) × collectible_payout - expected_model_API_cost - compute_cost - chain/payment_cost - expected_failure_cost - maintenance_allocation`

Only bid/accept when:
- `EV_j > minimum_margin_usd`, and
- payout/cost ratio exceeds a configurable safety multiple, and
- the task can be completed without prohibited automation or unauthorized data access, and
- worst-case capped execution cost is below a per-task limit.

For passive endpoints:

`Net/month = paid_calls × net_price_per_call - variable_API/model_cost - hosting - payment fees - maintenance`

The first goal is **not maximum revenue**. It is to prove one repeatable positive-margin transaction with tightly capped downside.

## Proposed architecture
A platform-neutral worker should be built before platform-specific credentials are supplied:

1. `market_adapter` — read opportunities without taking them.
2. `normalizer` — convert offers/tasks to common schema.
3. `policy_gate` — reject human-only, prohibited, ambiguous-rights, geography/KYC-incompatible, or uncapped-risk work.
4. `cost_estimator` — estimate tokens/API/compute/time/payment costs.
5. `margin_engine` — calculate conservative EV and minimum margin.
6. `capability_router` — map task to supported deterministic/LLM workflow.
7. `executor` — initially dry-run only.
8. `validator` — schema/quality checks before any submission.
9. `settlement_adapter` — disabled until explicit user authorization/credentials.
10. `ledger` — record opportunity, decision, estimated cost, actual cost, payout and realized margin.

## Experiment sequence

### Experiment E1 — PayanAgent read-only market sampler
Goal: measure whether bespoke requests exist and whether public receipts show settled demand.
- no registration required where public endpoints permit;
- collect request count, age, bounty/budget, skill tags, bid competition, settlement evidence;
- no bidding, buying or wallet action;
- output a 24h-equivalent snapshot if historical/public data allows, otherwise repeated snapshots across scheduled runs.

Success gate: enough credible paid request flow to justify building a task executor.

### Experiment E2 — OKX.AI task-intake observability
Goal: determine whether open tasks can be observed without user credentials and quantify task density/prices. No account creation or order taking.

### Experiment E3 — cross-market dry-run evaluator
Feed observed E1/E2 tasks into the common policy/cost/margin engine. Simulate execution costs using configurable model-price assumptions; never submit.

### Experiment E4 — passive MCP microservice benchmark
Design one very cheap capability (for example structured text/JSON transformation with deterministic validation) and model break-even calls/month on MCPize/A2MCP. Do not publish until payout geography, KYC and user authorization are resolved.

## Real-action checkpoints
The following require explicit user involvement/authorization and are NOT to be crossed automatically:
- create/verify email or marketplace accounts;
- Stripe Connect KYC/bank onboarding;
- create/fund wallet or sign value-moving transactions;
- accept a paid job whose failure can create liability/stake loss;
- pay arbitration deposits;
- purchase API credits/server/GPU;
- publish a monetized service under the user's identity.

Implementation should continue read-only/dry-run around these gates.

## Result
Implementation phase has a concrete first target and no longer needs broad discovery.

**Primary next step: E1 PayanAgent read-only market/receipt sampler**, followed in parallel by E2 OKX observability. Build a common normalized opportunity schema from real public market data before writing any executor.

Project state after this run: **IMPLEMENTATION IN PROGRESS**.