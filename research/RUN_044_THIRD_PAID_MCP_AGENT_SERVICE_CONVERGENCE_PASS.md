# Run 044 — third paid-MCP / agent-service seller convergence pass

Evidence date: 2026-08-17

## Objective
Continue the productive machine-native paid-endpoint tail after Run 043. Search alternative seller vocabulary around MCP monetization, agent marketplaces, agent-native data sales, paid API gateways and provider-side x402 infrastructure. Validate Tollara and newly surfaced independent provider implementations with current primary sources.

## Result
**Not converged.** No new top-level economic mechanism appeared, but this pass again produced multiple independent provider/seller implementations that were not present in the durable checkpoint. Therefore Run 045 must remain inside this cluster rather than becoming the final all-category saturation pass.

## New independent provider implementations

### Tollara — VERIFIED / EARLY
- Commercial platform for selling APIs, AI agents, LLM services and MCP servers.
- Seller can create a marketplace listing, offer subscriptions, usage-based plans, volume tiers or prepaid credits, and meter requests, tokens, bytes or time.
- Can route traffic through Tollara's gateway or keep calls on the seller's own infrastructure and report usage back from the backend.
- Supports synchronous calls, streaming and background/async jobs, which makes it suitable for near-autonomous server-side services.
- Seller analytics include usage, subscribers and revenue.
- Automation: **5 potential** for an API/MCP/agent service once deployed.
- Important unknowns: exact seller fee/take rate, payout schedule/rail, KYC, legal operator, seller-country support and Azerbaijan eligibility were not exposed clearly in the primary pages captured in this run.

### AgenticMarket — VERIFIED / EARLY
- MCP marketplace where creators publish hosted/remote MCP servers and set a per-call price.
- Primary monetization docs state standard creators receive **80%**, platform **20%**; Founding Creators receive **90% / 10%** for the stated program period.
- Earnings accrue per successful call.
- Minimum withdrawal in the detailed docs: **$20**, payout within up to **7 business days**; supported payout methods listed as Wise globally and Razorpay for India.
- Marketplace supports free-trial calls per user; such calls do not generate creator revenue.
- Automation: **5 potential** for a stable remote MCP server.
- Geography/KYC: public docs do not yet establish Azerbaijan-specific seller onboarding. “Wise available globally” is not equivalent to confirmed platform eligibility and requires direct onboarding validation.
- Demand remains unproven from primary revenue/call telemetry in this pass.

### MCPize — VERIFIED / COMMERCIAL
- Hosted deployment + marketplace + billing for MCP servers.
- Current docs support both subscription billing and x402 pay-per-call in USDC on Base.
- For new monetized servers after 2026-06-10, current developer revenue share is **80% creator / 20% platform**; earlier founding servers remain on the grandfathered 85/15 rate.
- Subscription payments use Stripe Connect; x402 path settles USDC to a configured Base wallet.
- Platform handles hosting, usage tracking, payment plumbing and marketplace discovery.
- Terms identify **Procoders OÜ** as service owner and state identity verification/tax documentation requirements for Stripe Connect payouts.
- Automation: **5 potential**; especially relevant because hosting and monetization are bundled.
- Geography: ordinary Stripe/Connect seller onboarding remains a gate. Stripe currently lists Azerbaijan connected-account support only as **preview**, so platform-specific production eligibility cannot be assumed.
- Demand/authenticity caution: MCPize publishes vendor-payment and top-earner marketing claims, but these were not independently audited in this run; treat as platform-reported, not profitability proof.

### Loomal — VERIFIED / EARLY
- Agentic-commerce payment layer that paywalls any HTTP endpoint or MCP tool with x402 and settles USDC on Base.
- Two earning surfaces:
  1. self-hosted/proxied API or MCP endpoint;
  2. **hosted endpoint** where seller uploads JSON/files and Loomal hosts the paid resource, removing the need for a server.
- Hosted files can be sold per download; current guide states **5% fee on settled transactions, currently waived**, with no listing fee.
- Funds are described as non-custodial and settle directly to the seller wallet.
- Supports per-call pricing, signed receipts and seller payment history.
- Automation: **5 potential** for APIs/MCP; **4–5** for static hosted data/content.
- Core risk: own-rights only. Data, files or model outputs must be legally resellable and free of prohibited personal/confidential material.
- Unknowns: formal legal operator/KYC/geography terms, paid demand volume and Azerbaijan-specific access.

### DataBazaar — VERIFIED / AGENT-NATIVE DATA MARKET
- Marketplace where humans **and autonomous agents can sell datasets programmatically** through MCP or REST.
- Seller agent can register, create drafts, upload data, publish listings and receive proceeds through the operator's Stripe account.
- Current primary site states **3% platform fee / 97% seller**, no listing fee, with funds released from escrow 24 hours after successful buyer download.
- Includes fixed-price listings, auctions and **open data bounties**, creating a direct demand-discovery mechanism rather than requiring sellers to guess what buyers need.
- Agents can also post data gaps/bounties when search fails, so supply can react programmatically to visible demand.
- Automation: **4–5 potential** for data a seller already has legitimate rights to produce/resell; human/operator verification is still part of onboarding.
- Compliance is important: platform guidance explicitly warns sellers not to list personal data, data scraped contrary to terms, or material they lack rights to sell; automated PII scanning is mentioned.
- Geography: Stripe payout dependency creates the same country-support gate. Azerbaijan seller onboarding must be tested rather than inferred.

## New strategic refinement
Run 044 adds a fifth useful operational subtype inside the same owned-software/data/content/service mechanism:

1. Direct self-hosted paid endpoint.
2. Marketplace/proxy monetization layer.
3. Autonomous agent-job marketplace.
4. Build-once paid agent/data/content asset.
5. **Demand-signalled data/API production** — marketplace exposes bounties/data gaps or subscriber/usage signals, enabling an autonomous operator to build or refresh only products with visible demand.

This is still **not** a new top-level mechanism; it is a superior operating strategy for reducing demand risk.

## Azerbaijan / payout gate update
Primary Stripe documentation captured in this run materially changes the country picture:
- Stripe Connect lists Azerbaijan under **“Available in preview”** for connected accounts, not standard production availability.
- Stripe stablecoin payouts documentation lists Azerbaijan among supported countries for qualifying US-platform payouts to **individuals or sole proprietors**, but this does not mean every marketplace using Stripe Connect has enabled that payout route.

Therefore:
- Stripe-Connect-based marketplaces must remain **RESTRICTED / VERIFY ONBOARDING** for an Azerbaijan-based seller unless the platform confirms its configuration accepts Azerbaijan.
- Wallet-native x402 platforms remain operationally attractive because they bypass ordinary bank payout rails, but legal/KYC/sanctions/tax/platform-country rules still must be checked separately.

## Economics implications
The principal hidden variable remains **paid utilization**.

For a server-native paid endpoint:

`Net = paid_calls × (price_per_call × seller_share - variable_compute/API_cost_per_call) - fixed_hosting - monitoring - compliance/tax - expected refund/dispute/loss cost`

For hosted digital/data assets:

`Net = paid_downloads × price × seller_share - creation/update/storage/compliance cost`

A high creator share does not fix zero demand. Marketplaces with bounties, public requests, real call telemetry or subscriber analytics should be weighted above large static directories with no proof of purchase activity.

## Saturation conclusion
- New top-level mechanisms: **0**
- New independent provider/seller implementations: **5 material**
- Taxonomy saturation: **very high**
- Paid MCP / agent-service project saturation: **still not reached**
- Overall project: **IN PROGRESS**

## Next run
Run 045 should be a **fourth provider-side convergence pass**, not the final all-category pass.

Priority vocabulary:
- `paid MCP hosting marketplace creator revenue`
- `MCP server marketplace payouts`
- `sell API to agents x402`
- `agent native data marketplace seller API`
- `AI agent bounty marketplace provider API`
- `machine customer marketplace seller`
- `MCP marketplace Wise payout`
- `MCP creator marketplace Stripe Connect`
- `pay per tool MCP hosting`
- `AI agent buys datasets API seller`

Specific targets:
1. Validate AgenticMarket legal operator / Terms / country policy.
2. Validate Loomal legal operator / Terms / seller eligibility.
3. Validate Tollara exact fees and payout rail.
4. Search for provider-side implementations omitted by directory articles: commercial hosted MCP vendors, agent-native data/product markets, API-bounty markets and non-custodial payment proxies.
5. Search GitHub repositories only as discovery leads, then validate monetization on official docs/sites.
6. Capture any public utilization/revenue telemetry and separate platform-reported marketing metrics from independently observable demand.

Only after this cluster produces negligible new viable independent projects should the project advance to a final all-category saturation/control pass.
