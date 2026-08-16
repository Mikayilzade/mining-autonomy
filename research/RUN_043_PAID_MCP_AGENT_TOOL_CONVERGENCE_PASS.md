# Run 043 — paid MCP / agent-tool marketplace convergence pass

Evidence date: 2026-08-16

## Objective
Continue from Run 042 and test whether alternative seller vocabulary around paid MCP tools, agent skills, x402 relays, endpoint monetization and agent-service marketplaces still reveals independent provider implementations.

## Result
**Not converged.** No new top-level economic mechanism appeared, but this pass found several independent provider/seller surfaces not captured in Run 042. The machine-native paid-endpoint cluster remains project-productive.

## New independent implementations

### xpay Tools — VERIFIED / EARLY
- Lets a provider register an existing remote MCP server, set flat or per-tool pricing, receive a proxy endpoint, appear in discovery, and earn on every paid tool call.
- Public docs say no monthly fee or minimum volume for MCP-server publishing; provider revenue can be withdrawn in USDC on Base.
- The broader publisher/content product explicitly documents a 5% platform fee / 95% publisher revenue. MCP-server-specific fee wording is less explicit in the pages captured in this run and needs a direct rate-card confirmation.
- Also offers a distinct **RSS/sitemap → monetized MCP content server** path, automatically refreshed every six hours. This is a build-once content/data monetization implementation with high automation potential.
- Automation: 5 potential for a stable remote MCP server or feed-backed content endpoint.
- Unknowns: seller geography/KYC, Azerbaijan eligibility, independent paid utilization, exact MCP-server take rate.

### MCP Marketplace (mcp-marketplace.io) — VERIFIED / RESTRICTED-BY-GEOGRAPHY
- Supports two monetization models: paid local packages via license-key gating and remote hosted MCP servers.
- Creator Terms state 15% marketplace commission / 85% creator payout.
- Creator payouts use Stripe Connect Express.
- This creates an important geography gate: seller eligibility depends on Stripe Connect availability and marketplace onboarding, so Azerbaijan must be validated before considering deployment.
- Automation: remote hosted server can reach 5; local package/license sales are build-once/semi-passive rather than daemon-native.

### datapoint.market — VERIFIED / ALPHA
- Hosted paid relay for owned APIs, MCP wrappers and downloadable datasets.
- Provider points the relay at an origin, sets a price and receives non-custodial USDC settlement.
- Public docs state listing is free, provider keeps 100% of stated price, and a 10% protocol fee (minimum $0.005/call) is added on top and paid by the buyer.
- Live on Base, Stellar and Solana according to current docs; provider automation keys and management MCP allow programmatic operation.
- Explicit public requested-data board creates a useful demand-discovery feature distinct from simple directory listing.
- Automation: 5 potential.
- Important restriction: wrapping third-party upstream data/API still requires explicit resale/license rights; own data/endpoint is preferred.
- Unknowns: real independent paid call volume, geography/KYC, Azerbaijan eligibility.

### AgentsMarketplace.app — VERIFIED / EARLY
- X Layer marketplace where providers register an AI agent, expose paid service endpoints, set USD-denominated prices and receive x402 settlement in USDC/USDT/USDG.
- Provides downloadable server files and a deployment path; registration is on-chain and endpoint-driven.
- Automation: 5 potential.
- Unknowns: legal entity, seller terms/fees, KYC/geography, demand authenticity, Azerbaijan eligibility.

### ArcAgent — VERIFIED / EARLY
- Agent service marketplace on Arc with USDC escrow, on-chain agent registration, task creation, deliverable submission and reputation.
- Seller/agent can be hired for tasks rather than merely exposing a static API call, making it closer to an autonomous job market.
- Automation: potentially 4–5 where job intake, execution and deliverable submission can be automated legitimately.
- Unknowns: provider terms, fee schedule, live paid utilization, legal entity/geography/KYC.

### MCP Market (mcpmarket.com) — VERIFIED / BUILD-ONCE
- Sitka Labs marketplace for paid AI-agent skills/digital products rather than a pay-per-call server market.
- Seller can import from GitHub or upload a SKILL.md, set a price, publish and earn per sale.
- This is not server-native compute income, but belongs in Tier D as a build-once digital asset channel.
- Public Terms identify Sitka Labs as a Canadian company.
- Exact seller commission/payout rate was not confirmed in the captured primary pages and remains an unknown.

## Important adjacent implementations / infrastructure

### Cloudflare Agents paidTool/x402 — VERIFIED / INFRASTRUCTURE
- Cloudflare officially documents charging per MCP tool call via `paidTool` + x402.
- This is enabling infrastructure, not a marketplace or independent demand source.
- Strategy value: a provider can operate its own paid MCP endpoint without marketplace lock-in, then distribute across multiple indexes/marketplaces.

### agentx402.ai — VERIFIED / SELLER EXAMPLE, NOT MARKETPLACE
- Demonstrates a live machine-paid service model: agent memory and web extraction sold per request in USDC over x402.
- It is useful as proof that the `owned utility endpoint + machine payment` pattern is operational, but it is a seller/operator example rather than an open provider marketplace.

### x402agentic.ai — WATCHLIST / PLANNED
- Public roadmap advertises pay-per-request middleware, service registry, MCP bridge and future agent-to-agent marketplace.
- The marketplace/commerce layer is still roadmap/planned, so do not count it as a current earning counterparty.

### GreenSmokeNetwork marketplace — WATCHLIST / NOT LIVE
- Public roadmap says marketplace is in active build/devnet and not yet live; target mainnet is future and conditional.
- Track to prevent rediscovery, but not a current earning option.

## Validation of Run-042 candidates

### the402 — stronger validation
- Terms identify operator as **Tolomato Capital, LLC**.
- Terms and provider docs confirm a 5% platform fee and USDC/Base settlement.
- Provider guide confirms webhook-based fulfillment, service requests, subscriptions and digital products, all compatible with highly automated provider operation.
- 95% provider / 5% platform economics are explicitly documented for service and subscription/product payments.
- Geography/Azerbaijan eligibility remains unresolved.

### PayanAgent — stronger validation
- Public site currently states **$0 platform fees** and non-custodial x402 settlement directly to seller.
- Supports API offers plus request/bid/fulfill/approve workflow and API-first provider registration.
- The public 24k+ catalog is aggregated supply and must not be treated as paid-demand proof.
- Legal entity/geography/KYC still unresolved.

### RelAI — stronger validation
- Marketplace is live and terms explicitly allow API monetization subject to applicable law.
- Current public marketplace UI shows a 5% platform fee in a payment example.
- Separate pricing page also shows Free / Pro / Enterprise account plans, so total provider economics can include both transaction fee and optional subscription costs.
- Terms state governing law of Poland.
- Azerbaijan/provider eligibility remains unresolved.

### PayAPI Market — stronger validation
- Public site states free listing, no per-request marketplace fee, providers keep 100%, and optional Featured placement costs $49/month.
- Current positioning is UK-focused; explicit international seller eligibility and Azerbaijan support remain unresolved.
- Public catalog count is small enough that demand depth remains an open question.

### endpoint.farm — stronger validation
- Public page now makes pricing explicit: free publishing; provider keeps 100% of set price; 10% protocol fee is added on top and paid by buyer, minimum $0.005/call.
- Alpha positioning is explicit and the site is actively seeking first providers; this is strong evidence that current demand/fill rate is immature.
- Live settlement is advertised on Base, Stellar and Solana; legal/geography/KYC questions remain open.

### Agent402 Marketplace — authenticity signal
- Marketplace currently displays many indexed/discoverable services but only a small verified-seller set and a public Calls/24h metric that was **0** at capture time.
- This strengthens the rule that indexed supply is not paid-demand proof.
- Seller economics beyond “free to register / pay when buyers pay” still need an exact fee schedule and legal-entity Terms.

## Demand/authenticity conclusion
The central economic unknown remains **independent paid utilization**. Several marketplaces expose impressive catalog sizes, but captured live panels often show weak or opaque realized call volume. Therefore:

- directory/catalog count ≠ paying customers;
- on-chain settlement count ≠ independent organic demand unless counterparties are analyzed;
- headline 95–100% provider share ≠ profitability;
- the correct test remains paid calls × contribution margin minus fixed hosting/monitoring/compliance cost.

## Durable architecture refinement
There are now at least four viable implementation styles inside the same economic mechanism:

1. **Direct self-hosted paid endpoint** — own API/MCP + x402/MPP payment middleware.
2. **Marketplace proxy** — existing endpoint behind a monetizing relay (xpay, datapoint.market, endpoint.farm, RelAI, etc.).
3. **Agent-job marketplace** — provider agent bids/accepts/fulfills structured jobs (the402, PayanAgent, ArcAgent).
4. **Build-once agent asset** — paid skills/packages/datasets/content feeds (MCP Market, MCP Marketplace local packages, xpay publisher feeds).

These should remain separate operational strategies even though they share the same underlying value source: owned software/data/content/service.

## Azerbaijan gate
No newly captured primary source was sufficient to confirm Azerbaijan seller eligibility for the new marketplaces. Stripe Connect-backed creator payouts are particularly sensitive to country support. Wallet-native platforms reduce payment-processor dependence but do not eliminate legal, sanctions, tax, KYC or platform-country restrictions.

## Saturation conclusion
- New top-level mechanisms: **0**
- New independent provider/seller implementations: **materially several**
- New infrastructure/examples/watchlist items: **several**
- Taxonomy saturation: **very high**
- x402/MCP/agent-tool project saturation: **not reached**
- Overall project: **IN PROGRESS**

## Next run
Run 044 should remain inside the productive machine-native cluster rather than becoming the final all-category pass.

Priority:
1. Search seller vocabulary around `MCP monetization platform`, `sell MCP server`, `MCP creator payout`, `paid agent skill marketplace`, `AI agent job marketplace API`, `agent service escrow`, `autonomous task marketplace agent`, `x402 provider dashboard`, `agent API monetization proxy`, `sell dataset to AI agents`.
2. Validate Tollara and any other API/AI/MCP commercial marketplaces surfaced but not yet primary-source validated.
3. Search ecosystem directories/GitHub repositories for provider-side products, not only buyer tools.
4. Capture exact seller fees, payout rails, KYC/geography and legal operator where available.
5. Continue demand-authenticity checks using public call/revenue/settlement dashboards rather than catalog size.
6. Deduplicate every hit against Runs 041–043.

Only after this cluster yields negligible new independent viable projects should a final broad all-category saturation pass begin.
