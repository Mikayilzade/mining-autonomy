# Run 045 — fourth paid-MCP / agent-market convergence pass

Evidence date: 2026-08-17

## Objective
Continue the provider-side machine-paid service tail after Run 044. Search alternative vocabulary around paid MCP marketplaces, hosted MCP seller programs, agent-native skill/data markets, per-call API monetization and non-custodial machine-payment rails. Re-check whether this cluster is converging enough to move to the final all-category saturation pass.

## Result
**Not converged yet.** No new top-level economic mechanism appeared, but the pass found multiple independent provider/seller implementations not present in the Run-044 checkpoint. Taxonomy saturation remains very high; project-level saturation in paid MCP / agent-service / agent-native digital-product markets is still incomplete.

## New independent provider implementations

### MCP Marketplace (mcp-marketplace.io) — VERIFIED / COMMERCIAL
- Dedicated MCP marketplace with free and paid tools, one-time purchase and subscription monetization.
- Creator Terms state **85% creator / 15% marketplace commission**.
- Creator payouts use **Stripe Connect Express** and require a valid Stripe Connect account in good standing.
- Remote hosted MCP servers can be monetized while the creator hosts the endpoint; local package/license-key distribution is also supported.
- Automation: **4–5** depending on whether the seller runs a remote endpoint or distributes a build-once package.
- Azerbaijan: seller onboarding remains **RESTRICTED / VERIFY** because the payout path is Stripe Connect Express and Azerbaijan production eligibility cannot be assumed from Stripe preview availability.
- Demand evidence: official creator pages expose installs/revenue analytics but this run found no independently audited paid-utilization figure.

### Zion (zionmcp.com) — VERIFIED / EARLY
- Marketplace/distribution layer for MCP-era tools, agents and packaged capabilities.
- Official site advertises **80/20 creator revenue split**, with usage-based, subscription, one-time and bounty pricing surfaces.
- Marketplace handles discovery and hosted instances; seller can import from GitHub.
- Automation: **4–5** for reusable hosted agent/tool assets.
- Risk: headline marketplace metrics are operator-reported; no independent transaction/revenue proof captured in this pass.
- Seller-country/KYC/payout-rail details remain unverified.

### SkillExchange — VERIFIED / EARLY
- MCP + A2A skill marketplace oriented to autonomous agent consumption.
- Official creator pages describe per-use, subscription and tiered monetization and Stripe Connect payouts.
- Public pages are internally inconsistent on creator share: some sections state **80/20**, while FAQ/marketing sections state **85% creator**; paid Pro tier advertises 85/15 and Enterprise 90/10. Treat exact default share as **VERIFY AT ONBOARDING**.
- Stripe Connect is the payout rail, with KYC implied/explicit in platform copy.
- Automation: **5 potential** for stable HTTPS/MCP skills receiving autonomous calls.
- Geography: Azerbaijan seller support remains unconfirmed because platform-specific Stripe Connect onboarding must succeed.
- Demand evidence: execution/developer/income figures are platform-reported marketing metrics, not independently audited.

### Sigrix — VERIFIED / LIVE EARLY MARKETPLACE
- Curated AI marketplace covering prompts, personas, skills, agents, crews, products and MCP servers.
- Official seller pages state **80% standard seller share / 20% fee**, while founding sellers keep **85% / 15%** for life.
- Product Hub confirms paid MCP-server listings and Stripe-connected seller onboarding.
- No monthly/listing fee is stated for ordinary seller listings; commission is per sale.
- Automation: **3–5** depending on asset type; MCP servers/agents can be near-autonomous, static prompts/personas are build-once digital assets.
- Current marketplace page showed **0 live MCP-server listings** despite MCP support, so present paid demand for MCP specifically is unproven.
- Geography: Stripe onboarding gate; Azerbaijan requires direct validation.

### Persona Markets — VERIFIED / PRE-LAUNCH-SEEDING
- Curated marketplace turning substantial Obsidian knowledge vaults into hosted MCP endpoints.
- Official site states **85% creator revenue share**, flat/no tiers, and says platform handles ingestion, hosting, billing, payouts and usage reporting.
- Creator input requirement: substantial rights-clean vault (site states 200+ interconnected notes minimum) and clear domain/identity.
- Current state is seeding / creator submissions after launch cohort; classify as **WATCHLIST / EARLY**, not immediate deployment target.
- Automation: **4–5** once a vault is accepted and hosted.
- Main constraint is asset creation/rights quality, not compute.

### Qatom — VERIFIED / PREVIEW, MACHINE-NATIVE PAYMENT LAYER
- Hosted multi-tenant MCP commerce layer where providers register any HTTP API as a payable tool.
- Official site states **0% platform fee during preview**, per-call settlement in **USD-TDN**, instant settlement to provider Twin and fiat withdrawal through traditional bank rails.
- Supports multi-payee splits and headless marketplace discovery.
- Provider setup can be performed via REST/chat and earnings land per call; structurally near-autonomous.
- Automation: **5**.
- This is not a new top-level mechanism; it is another direct machine-payment/marketplace implementation for owned APIs/services.
- Important unknowns: legal operator, exact withdrawal/KYC/bank-country coverage, permanence of 0% fee after preview, Azerbaijan eligibility and observed paid utilization.

### Sigrix adjacent seller surface — build-once AI assets
- Sigrix additionally confirms a broader build-once digital-product path: prompts, personas, assistants, agents, crews and bundles can share the same marketplace/payment rail.
- This is not a new mechanism and is catalogued only to prevent rediscovery as a separate income class.

## Additional discovery leads requiring caution

### MachinePal / x402proxy
- Open-source gateway/proxy that can protect APIs/files/services behind x402 payments and is explicitly framed as a way to sell API access or paid resources without ordinary Stripe/user-account plumbing.
- Valuable as implementation infrastructure, but **not itself proof of a demand marketplace**. Classify as an enabling tool rather than an income source until a paying customer channel is attached.

### Logion
- Agent-native marketplace for reviewed operational-knowledge bundles with **85/15** creator/platform split, Stripe Connect payouts, referral rewards and bounties.
- Economically it belongs to the existing build-once digital asset + bounty mechanism.
- Worth deeper validation in Run 046 because it is another independent seller implementation, but this pass did not complete legal/geography validation.

## Convergence observations
1. The cluster is increasingly splitting into repeated implementations of only a few durable strategies:
   - paid hosted MCP/API endpoint;
   - marketplace-distributed paid tool/skill;
   - build-once digital/knowledge/data asset;
   - bounty/request-driven production;
   - payment proxy/gateway around an owned endpoint.
2. **No new economic mechanism** appeared.
3. New project names are still appearing with materially distinct seller onboarding/payment/distribution implementations.
4. Therefore the project-level tail is shrinking but not yet negligible.

## Demand-authenticity result
The major unresolved issue is still real paid utilization. Across this pass:
- creator revenue shares and payout mechanics are much easier to verify than buyer demand;
- many visible execution/developer/creator counts are platform-reported;
- several platforms are beta, preview, seeding or early launch;
- marketplace catalog size does not imply seller revenue;
- a provider-side strategy should prefer platforms exposing public paid-call, bounty, settlement, subscriber or purchase signals.

## Economics
For paid MCP/API marketplaces:

`Net = paid_calls_or_sales × price × creator_share - variable_compute/API/model_cost - hosting - payment/network fees - refunds/disputes - compliance/tax - maintenance`

For build-once agent/knowledge assets:

`Net = sales × price × creator_share - creation/update/hosting/compliance cost`

For Qatom/x402-like direct payment rails:

`Net = paid_calls × (price - variable service cost - settlement/network/platform fee) - fixed hosting - monitoring - compliance/tax`

A nominal 0–20% platform fee remains secondary to paid utilization and upstream service cost.

## Azerbaijan gate
Stripe-Connect-dependent marketplaces remain **VERIFY ONBOARDING / RESTRICTED** for an Azerbaijan-based seller until the exact platform successfully accepts seller onboarding. Wallet/native settlement alternatives reduce ordinary card-payout friction but do not remove KYC, bank withdrawal, sanctions, tax, legal-entity or country restrictions.

## Saturation conclusion
- New top-level mechanisms: **0**
- New material independent provider/seller implementations: **6+**
- New enabling infrastructure leads: **1+**
- Taxonomy saturation: **very high**
- Paid MCP/agent-service project saturation: **high, still incomplete**
- Overall project: **IN PROGRESS**

## Next run
Run 046 should be a **fifth paid-MCP / agent-service tail pass plus explicit candidate-dedup check**, not yet the final all-category pass.

Priority targets:
1. Validate Logion legal operator, Terms and seller-country/payout restrictions.
2. Search and validate: MCPChannel, MarketNow, RuleSell, xpay and other independent paid-MCP directories/marketplaces surfaced by secondary ecosystem maps.
3. Search terms around `agent skill marketplace creator payout`, `MCP paid tool seller agreement`, `AI API bounty marketplace seller`, `agent marketplace pay per call creator`, `MCP marketplace bank payout`, `x402 marketplace provider directory`, `machine customer API marketplace`.
4. Check whether new hits are true independent monetization implementations or only directories/gateways/docs.
5. Continue public-demand evidence search: paid call counts, settlement explorers, active bounties, actual paid listings and transparent seller-revenue evidence.
6. If Run 046 yields only duplicates or negligible new viable independent projects, move to Run 047 final all-category saturation/control pass.
