# Run 052 — eleventh paid-agent / MCP / x402 / A2A provider-tail pass

Date: 2026-08-17
Status: completed

## Objective
Continue the provider-level saturation search for legal, ToS-compliant seller channels where a server/API/MCP tool/agent skill can be listed or discovered and paid automatically. Deduplicate against Runs 041–051 and reject mere standards, SDKs, directories, demos, or buyer-only products without an explicit provider path.

## Result
The tail is **not converged**. This pass found multiple independent seller-capable channels, so the project must remain IN PROGRESS.

No new top-level economic mechanism emerged. All findings map to existing durable strategies: paid endpoint, marketplace/proxy monetization, paid skill/digital asset, or agent marketplace listing.

## New independent candidates

### MCP Marketplace (mcp-marketplace.io) — VERIFIED
- Explicit creator path for publishing paid MCP servers/tools.
- Supports one-time and subscription pricing, creator analytics, license keys and Stripe checkout.
- Terms state creators receive **85%** of paid Tool revenue and the marketplace retains **15%**.
- Creator payouts use **Stripe Connect Express**.
- Remote MCP servers can be hosted by the seller; local packaged servers can also be monetized.
- Admission is curated/reviewed; security scan and approval are part of listing flow.
- Fit: server-native yes for remote MCP; automation 5/5 after deployment; main risk is buyer utilization.
- Geography/KYC gate: Stripe Connect availability and onboarding eligibility must be validated for Azerbaijan before implementation.

### FiatDock — WATCHLIST / strong seller-channel lead
- First-party site describes an MCP/x402 marketplace where sellers can list hosted or package-based MCP services.
- Non-custodial USDC settlement over Base; seller-first economics advertised as 0% fee for first 30 days then 1% per call.
- Agent-native discovery via MCP, JSON/OpenAPI and marketplace tools.
- First-party claims 25k+ MCP calls in the prior month from 2k+ unique clients; treat as platform-reported demand, not independently audited seller receipts.
- KYC/security-scan path exists for verified sellers.
- Fit: server-native yes; automation 5/5.
- Keep WATCHLIST until seller onboarding/terms and attributable paid demand are independently validated.

### Qatom / TODAQ — WATCHLIST
- First-party surface explicitly supports registering an API as a payable tool and earning per call.
- Hosted multi-tenant MCP marketplace; machine buyers discover priced tools and settle in-flight.
- Seller flow accepts normal HTTP methods and full parameter passthrough; earnings route to a seller Twin.
- Advertised zero-fee settlement and USD-TDN denomination.
- Fit: server-native yes; automation 5/5.
- Keep WATCHLIST because current production demand, settlement asset liquidity/off-ramp, seller eligibility, and Azerbaijan usability remain unresolved.

### SkillExchange — WATCHLIST
- Explicit marketplace for publishing and selling MCP skills / AI automations.
- Seller can package automation, set pricing and receive payouts via Stripe.
- A2A-ready discovery is advertised.
- Fit: build-once + server-native depending on skill type; automation 4–5/5.
- Keep WATCHLIST until fee schedule, seller terms, payout eligibility and real paid demand are validated.

### Agent402 Marketplace — WATCHLIST
- Explicit seller path: register an API, index it for semantic discovery and receive per-request x402 payments.
- Non-custodial design; USDC settlement; claims multi-chain support and trust scoring.
- First-party surface claims 17k+ indexed services, 13 networks and 3 facilitators.
- Fit: server-native yes; automation 5/5.
- Keep WATCHLIST pending current terms, exact fee path, production paid-call evidence and seller eligibility.

### ArisPay Agent Marketplace — VERIFIED architecture / WATCHLIST economics
- Explicit publisher onboarding: merchant signup, publish paid MCP/x402/HTTP listings, PayGate acceptance and settlement through ArisPay.
- Marketplace currently exposes paid live listings, including x402 endpoints.
- Supports Base-mainnet x402 and publisher earnings.
- Fit: server-native yes; automation 5/5.
- Seller channel itself is real; keep economics WATCHLIST until fee/payout/KYC terms and attributable seller receipts are measured.

### endpoint.farm — WATCHLIST
- Alpha marketplace wrapping any existing API/MCP tool into a paid agent-callable x402 endpoint.
- Free listing; non-custodial USDC settlement via on-chain splitter on Base/Stellar/Solana.
- Seller chooses price and wallet; marketplace discovery can be enabled.
- First-party site explicitly says alpha and actively seeks first providers, implying demand depth is not yet mature.
- Fit: excellent server-native architecture, automation 5/5; economics WATCHLIST due likely thin utilization.

### datapoint.market — WATCHLIST
- Sister-style marketplace focused on data APIs/dataset files for AI-agent buyers.
- Seller can wrap an API/MCP tool or sell CSV/Parquet as a paid download.
- Non-custodial x402 settlement; seller keeps stated price while buyer pays an added platform fee (first-party example: 10% fee, minimum $0.005/call).
- Alpha status and unclear independent buyer depth keep it WATCHLIST.
- Fit: server-native for API/data endpoints; automation 5/5.

### AgentMart — WATCHLIST
- Marketplace for reusable agent resources: prompts, workflows, playbooks, research packs, templates and automation assets.
- x402/USDC on Base; first-party page states 3% platform fee and 97% seller payout.
- Current site displayed 49 shops, 62 agents and 296 products, but recent surfaced items included many $0 listings; buyer-depth evidence remains weak.
- Fit: build-once digital-asset strategy, not necessarily continuous server work; automation 4–5/5.

### AgentStore — WATCHLIST
- Marketplace concept for Claude Code plugins/agent resources with publisher monetization.
- Public marketplace description reports 80% publisher revenue share and gasless USDC/x402 payments.
- Current evidence came from an MCP-market listing rather than sufficiently strong first-party production documentation.
- Keep WATCHLIST until direct source, current deployment status and real seller flow are verified.

## Leads rejected / not promoted

### Atto Market
- Paid API execution and receipts are demonstrated, but provider onboarding / independent seller publication path was not explicit enough in this pass.
- Keep as lead, not catalog promotion.

### AgentMint / Orkai
- Clear self-hosted x402 marketplace software, but evidence points to software you deploy yourself rather than an independent demand/distribution marketplace.
- Useful implementation stack for the direct paid-endpoint strategy, not a new external earning channel.

### x402 Agentic
- Roadmap advertises future service registry/marketplace, but key marketplace monetization stages are planned rather than current independent seller distribution.
- Not promoted as live income channel.

### MCIP
- Machine Customer Interaction Protocol enables stores to become agent-readable, but it is a protocol/translation layer and not presently a third-party seller marketplace paying API providers.
- Relevant to build-once machine-commerce strategy, not a standalone earning platform.

### Pantheron
- Surface reports marketplace volume/provider/purchase metrics, but it explicitly describes itself as a demo marketplace. Do not treat demo metrics as production demand.

### agentlearn.fun
- Marketplace flow currently references Base Sepolia/test-style environment and inconsistent surface counters; useful proof-of-concept, not promoted to production income channel.

### MiniUp x402
- Buyer-side paid publishing/hosting workflow; seller revenue path for third-party providers is not the product. Not a supplier marketplace for our target.

### x402scan / Poncho discovery
- Strong discovery layer for already-monetized APIs, but the page is primarily discovery/merchant surfacing rather than a distinct third-party settlement marketplace. Treat as distribution tooling for direct x402 endpoints.

## Durable conclusions
1. **No sixth top-level mechanism emerged.** Taxonomy saturation remains extremely strong.
2. Provider-level saturation is **still incomplete**: this narrow pass found at least 8–10 independent seller-capable channels or strong watchlist candidates.
3. The paid-MCP/x402 ecosystem is fragmenting into several economically distinct admission modes:
   - curated marketplace + fiat payout (Stripe);
   - open crypto marketplace + direct/non-custodial settlement;
   - marketplace/proxy wrapping of existing endpoints;
   - digital-skill/resource stores;
   - self-hosted discovery layers.
4. Most new projects have a **demand-depth problem, not a technical-autonomy problem**. Publishing can be nearly hands-off; utilization remains the dominant hidden variable.
5. First-party activity claims must be separated from verified seller receipts. Platform-reported calls, indexed services, shops, products and protocol-wide transaction counts are not enough to model expected revenue.
6. Azerbaijan eligibility remains a pre-deployment gate where Stripe, KYC, wallet/exchange/off-ramp or sanctions screening is involved.

## Next run
**Run 053 — twelfth paid-agent / MCP / x402 seller-tail pass**, not the final all-category pass yet.

Priority should shift from generic `marketplace` vocabulary to monetization synonyms likely to expose remaining channels:
- `MCP creator monetize server payout`
- `paid MCP server marketplace creator Stripe`
- `x402 API directory add service seller`
- `AI tool marketplace developer revenue share`
- `agent tool marketplace publish paid tool`
- `agent API monetization directory provider`
- `pay per call MCP registry creator`
- `AI agent plugin marketplace creator payout`
- `agent service store publish paid skill`
- `machine buyer API seller marketplace`

Deduplicate all names from Runs 041–052. If the next ultra-narrow pass collapses to duplicates/negligible viable additions, then proceed to a final all-category saturation/control pass.