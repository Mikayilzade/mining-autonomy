# Run 054 — Thirteenth paid-agent / MCP / x402 / A2A seller-tail pass

Date: 2026-08-17
Status: **COMPLETED**
Project state after run: **IN PROGRESS**

## Objective
Execute another ultra-narrow provider-side search across paid AI-agent, MCP, A2A and x402 marketplaces, deduplicate against Runs 041–053, and promote only channels with an explicit seller/provider path plus a real payment flow.

## Search families used
- autonomous service marketplace provider API paid webhook
- agent job marketplace seller USDC
- MCP server creator marketplace payout
- A2A agent marketplace price-per-call creator payout
- x402 provider marketplace register capability earn USDC
- machine service marketplace provider routing settlement
- AI API marketplace seller earn per request
- agent plugin/API creator payout
- provider-role and seller-role variants around x402/A2A/MCP

## Result summary
This pass found **four material independent seller-capable channels not present in the repository search index** plus one closed-beta channel and one important demand-intelligence layer.

No new top-level economic mechanism emerged. All additions fit the already-converged machine-paid model: self-hosted paid endpoints, marketplace distribution, request/bid work, or demand-signalled production.

Because new viable projects are still appearing at a material rate, the project **must not be marked COMPLETE yet**.

---

## 1. PayanAgent — VERIFIED

### Why it matters
PayanAgent is one of the strongest matches to the original target: a server-side autonomous agent can register as a provider, publish offers, respond to bespoke requests, bid, fulfill work and receive USDC through an API-first marketplace.

### Explicit seller path
Official site documents:
- provider/agent registration through `POST /api/v1/agents`;
- seller offer creation through `POST /api/v1/offers`;
- bespoke work requests through `POST /api/v1/requests`;
- provider bidding through `POST /api/v1/requests/:id/bid`;
- fulfillment through `POST /api/v1/requests/:id/fulfill`;
- approval releasing escrow to provider;
- x402 direct-buy flow with USDC settlement to seller;
- public receipt feed for settled transactions.

### Classification
- Category: autonomous agent/API marketplace + request/bid job market
- Status: **VERIFIED**
- Server-native: **Yes**
- Automation: **5/5**
- Resource supplied: software service / API / agent work
- Payment: USDC on Base
- Seller admission: open API registration
- Capital: low, excluding hosting/model/API costs and any task-specific working capital
- KYC/geography: no KYC requirement found in the public seller flow; wallet-based settlement reduces bank-rail geography friction, but local legal/tax treatment remains separate
- Main risk: demand/fill rate, task-specific cost overruns, buyer-approval dependency for bespoke escrow jobs, smart-contract/payment-layer risk

### Economics
Direct offer:
`Net = paid calls × price - model/API costs - compute - bandwidth - transaction/withdrawal costs - maintenance - expected failures`

Request/bid work:
`Expected net/job = P(accepted bid) × P(approved fulfillment) × payout - expected execution cost - failed-bid cost - maintenance`

### Evidence quality
Strong first-party evidence of provider, offer, bid, fulfillment, escrow and receipt flows. First-party claim of 24k+ catalog entries is not treated as buyer demand proof.

### Strategic note
PayanAgent combines two already-known strategies in one platform:
1. passive pay-per-call endpoint;
2. autonomous request-feed worker that bids and fulfills jobs.

This makes it particularly relevant for later implementation testing.

---

## 2. Agent402 Marketplace — VERIFIED, demand currently weak/uneven

### Why it matters
Agent402 provides explicit seller registration for any HTTP endpoint/API/tool, adds x402 payment wiring and marketplace discovery, and settles USDC directly to the seller wallet across multiple networks.

### Explicit seller path
Official marketplace states:
- free/open service registration;
- seller points the platform at an endpoint;
- Agent402 handles x402 payment wiring and indexing;
- buyers discover and invoke services by natural-language search;
- settlement is non-custodial, per-call USDC to seller-controlled wallet;
- marketplace supports x402, MCP, A2A and ERC-8004 discovery/identity layers.

### Classification
- Category: paid API/agent discovery + x402 marketplace
- Status: **VERIFIED**
- Server-native: **Yes**
- Automation: **5/5**
- Resource supplied: API / model / oracle / tool / agent endpoint
- Payment: USDC / multi-chain
- Seller admission: open registration
- Capital: low beyond service delivery cost
- KYC/geography: wallet-native public flow; no bank payout dependency found
- Main risk: utilization is the dominant uncertainty

### Critical live-demand observation
The public marketplace snapshot surfaced during this pass showed roughly 77k discoverable services, 18 verified sellers, and **0 calls in the displayed 24-hour snapshot**. This is useful negative evidence: large discovery counts do not imply buyer demand.

Agent402's separate public Tape is more useful than marketplace listing counts. It reports directly attributed x402 activity over a 30-day window, including named services with thousands of calls. This demonstrates that real x402 paid traffic exists somewhere in the ecosystem, but it does **not** prove that a new Agent402-listed seller will receive traffic.

### Strategic note
Agent402 also operates Demand Intel, aggregating demand signals and identifying supply gaps. That is not an independent payout mechanism, but it is potentially valuable for choosing what paid API/agent to build instead of creating supply blindly.

---

## 3. AiPayGen seller marketplace — VERIFIED

### Why it matters
AiPayGen exposes an unusually explicit seller registration and fee model for third-party APIs.

### Explicit seller path
Official seller page documents:
- API registration through a seller endpoint or web form;
- per-route price setting;
- automatic marketplace listing;
- x402-paid calls;
- Base USDC settlement;
- seller dashboard;
- instant withdrawal to EVM wallet;
- no minimum withdrawal;
- flat **10% platform fee** on paid calls.

### Classification
- Category: paid API marketplace
- Status: **VERIFIED**
- Server-native: **Yes**
- Automation: **5/5**
- Resource supplied: API/data/model/tool execution
- Payment: USDC on Base
- Seller admission: open registration path
- Capital: low; operating costs depend on endpoint
- Geography/KYC: EVM-wallet payout path; no bank rail required in the documented seller flow
- Main risks: utilization, upstream API/model cost, platform concentration, payment/security implementation

### Economics
Published fee permits a clean first-pass model:

`Net per call = price × 0.90 - marginal endpoint cost - infra allocation - tx/withdrawal cost`

Break-even paid calls/month:

`fixed monthly cost / (price × 0.90 - marginal cost per call)`

The site's revenue calculator is not evidence of actual demand and is not used as profitability proof.

---

## 4. Endpoints.market — RESTRICTED / WATCHLIST (closed beta)

### Why it matters
The platform describes a direct x402 pay-per-call API marketplace with provider-set pricing and real-time USDC settlement.

### Current limitation
Its own documentation says the service is currently in **closed beta / early access**. Therefore it cannot yet be treated as an immediately deployable open provider channel.

### Classification
- Category: paid API marketplace
- Status: **RESTRICTED / WATCHLIST**
- Server-native: architecturally yes
- Automation: 5/5 if admitted
- Payment: USDC
- Platform fee: docs currently advertise zero platform fees
- Seller admission: closed beta / waitlist
- Main uncertainty: public launch, real paid buyer demand, final provider rules

### Important caution
The marketing page says providers can start earning and implies broad access, while the documentation explicitly states closed beta. The stricter documentation is used as the authoritative current classification.

---

## 5. Agent402 Demand Intel / Tape — STRATEGIC INFRASTRUCTURE, not a standalone earning channel

### Demand Intel
Agent402 aggregates demand signals, clusters them and highlights supply gaps. This is useful for **demand-signalled production**: selecting an API/agent to build only after evidence of unmet requests appears.

### Tape
The public Tape provides attributable x402 transaction/call data and is valuable for estimating whether specific service categories show real paid activity.

During this pass, the Tape showed a 30-day direct-attributed set totaling tens of thousands of calls, with named services spanning token/address data, touch/signal endpoints, options data, distributed inference and legal search.

### Classification
- Status: **VERIFIED strategic research/distribution signal**
- Independent earning mechanism: **No**
- Use: demand validation, service selection, traffic benchmarking

This improves the project's methodology: instead of treating marketplace listings as demand, later implementation candidate selection should use attributable paid-call history where available.

---

## 6. Circle Agent Marketplace / Agent Stack — WATCHLIST / curated distribution

Current Circle material explicitly describes an Agent Marketplace for agent-discoverable paid services and encourages builders with monetized APIs to apply for inclusion. Seller-side x402/USDC endpoint monetization is real, but the current marketplace admission route appears curated/application-based rather than an open self-service seller market.

Classification:
- Status: **WATCHLIST / RESTRICTED**
- Mechanism: x402 paid endpoint + curated marketplace discovery
- Server-native: yes
- Automation: 5/5 once endpoint is deployed
- Admission risk: curated/partner application
- Demand evidence: not established from the material reviewed in this run

Circle's own July 31, 2026 material emphasizes that the agent-service market is still early; this is consistent with the project's caution against projecting demand from infrastructure growth alone.

---

## Deduplication / non-promotions

### x402 API Registry
Duplicate from Run 053. Explicit provider-node path earning USDC remains valid; no new economic mechanism.

### x402 Bazaar
Already treated as distribution/marketplace infrastructure in Run 053. Search results continue to confirm third-party marketplace services and paid endpoints, but no reason to count a new mechanism.

### a2a cloud
Duplicate from Run 053. Current seller docs still show `price_per_call_usd`, seller markup, configurable platform fee and Stripe Connect settlement.

### Generic x402 seller implementation
Not an independent marketplace. x402 itself allows a self-hosted paid endpoint; that strategy is already represented as direct self-hosted paid service.

---

## Cross-platform economic observations

### 1. Open seller admission is now common; demand is the scarce asset
The technical act of listing a paid API is rapidly commoditizing. The practical differentiator is paid traffic, not payment integration.

### 2. Marketplace inventory counts are poor revenue indicators
Agent402's marketplace snapshot and prior x402 measurement research reinforce the rule: thousands of listed or indexed services do not equal buyers.

### 3. Public payment tapes are high-value research inputs
Where a platform exposes attributable paid calls or seller receipts, those signals should rank above registration counts, demo transactions or protocol-wide settlement totals.

### 4. Request/bid markets are closer to the original "bot does simple jobs" concept than passive API listing alone
PayanAgent's request → bid → fulfill → approve flow is a particularly strong implementation candidate because the worker can actively search for demand instead of waiting for API traffic.

### 5. Security remains part of unit economics
Recent x402 research found serious authorization/settlement implementation risks across facilitators. Any later implementation should isolate merchant wallets, bind payment exactly to resource/price/request, enforce replay protection and idempotency, and cap spend/gas exposure.

---

## Run 054 saturation result
- New top-level economic mechanisms: **0**
- New material independent seller-capable channels: **4** (PayanAgent, Agent402 Marketplace, AiPayGen, Endpoints.market)
- New strategic demand-intelligence layer: **1 major** (Agent402 Demand Intel/Tape)
- New curated/watchlist seller distribution channel: **1** (Circle Agent Marketplace)
- Taxonomy saturation: **very high**
- Provider-level saturation in paid-agent/x402/A2A tail: **still incomplete**

## Decision
Do **not** advance to the final all-category completion pass yet. Run 054 still produced a material number of independent channels.

## Next run
**Run 055 — fourteenth paid-agent / x402 / A2A / machine-service seller-tail pass**, but narrow the vocabulary toward less SEO-obvious provider surfaces:

1. `agent service provider register offer bid fulfill paid API`
2. `AI agent marketplace provider request bid escrow USDC`
3. `agent skill marketplace developer revenue per execution`
4. `paid MCP tool marketplace creator withdraw earnings`
5. `agent API marketplace seller dashboard payout wallet`
6. `x402 seller marketplace provider waitlist API monetization`
7. `machine customer marketplace API provider revenue share`
8. `agent tool registry paid calls seller fee`
9. `autonomous task marketplace agent provider escrow bid`
10. `AI tool marketplace usage based creator payout`

If Run 055 yields only duplicates or negligible viable additions, then proceed to the final all-category saturation/control pass.
