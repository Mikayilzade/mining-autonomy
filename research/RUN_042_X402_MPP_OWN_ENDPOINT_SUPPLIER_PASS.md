# Run 042 — x402 / MPP / own-endpoint supplier saturation pass

Evidence date: 2026-08-16

## Objective
Continue from Run 041's newly productive API-capacity cluster and test whether x402/MPP search vocabulary reveals independent seller/provider markets beyond Proxygate, JellyNet, cn2.ai, CreditSwap and UsePod/KeyMart-like implementations.

## Result
**Not converged.** This pass produced a large independent implementation cluster. No new top-level economic mechanism appeared, but project-level saturation is not reached.

The key structural split is now durable:

1. **Own-endpoint monetization/discovery** — seller owns/controls the API/service and adds x402/MPP-style per-call payment. This is the cleanest legal profile because no third-party API quota is being resold.
2. **Authorized upstream resale** — seller has an enterprise/reseller/sub-licensing right and resells capacity legitimately.
3. **Ordinary retail API-key/quota resale** — high upstream-ToS risk; restricted by default unless explicit contractual permission exists.

## New independent projects / implementations

### Agent402 Marketplace — VERIFIED / EARLY
- Provider points marketplace at an endpoint, receives x402 per-call USDC, and funds settle non-custodially to provider wallet.
- Public site states registration is free and sellers pay only when buyers pay.
- Claims 17k+ indexed services and support across 13 networks / 3 facilitators.
- Classification: own-endpoint discovery/monetization, automation 5 potential.
- Unknowns: legal entity, exact fee schedule, real independent paid utilization, geography/KYC.

### the402 — VERIFIED / EARLY
- Provider marketplace with API/webhook onboarding, autonomous bidding on requests, service listings, subscriptions and digital products.
- Public provider docs state 95% provider / 5% platform split for subscriptions and service payments.
- Supports programmatic provider registration and webhook fulfillment; suitable for autonomous server agents.
- Self-custody/embedded USDC wallet workflow is documented.
- Classification: own-service marketplace + autonomous job/request market; automation 5 potential.
- Important: this is more than an API directory because providers can bid on requests and fulfill jobs through webhooks.

### x402 Bazaar — VERIFIED / VERY EARLY
- Providers can wrap any owned HTTP endpoint and advertise it through the marketplace.
- Public site advertises 95% provider revenue and multi-chain x402 settlement.
- However, current public traction panel simultaneously displayed **0 external providers / $0 USDC on-chain volume** while marketing 100+ APIs.
- Classification: technically live but demand proof weak; treat profitability as unproven.

### PayanAgent — VERIFIED / EARLY
- Agent/SaaS providers can register capabilities, list API offers and receive USDC on x402 calls.
- Also exposes request posting/escrow workflows, suggesting a broader machine-native services market rather than only endpoint listing.
- Public site claims a 24k+ catalog; this must not be interpreted as paid utilization without transaction evidence.
- Classification: own-endpoint + agent-service marketplace; automation 5 potential.

### RelAI Marketplace — VERIFIED / BETA
- Providers list owned HTTP routes, set per-call USDC price and receive wallet settlement through x402.
- Multi-chain support advertised; self-custodial wallet required.
- Listing is free during beta; public page says a protocol fee applies on settled payments but exact pricing was not captured in this pass.
- Classification: own-endpoint marketplace, automation 5 potential.

### to402 — VERIFIED / RESTRICTED
- Proxy layer that can make an existing API x402-compatible without changing upstream application code.
- Public site also explicitly advertises third-party API reselling.
- Own-endpoint use is clean; third-party reselling is **RESTRICTED** unless upstream terms grant resale/sub-licensing rights.
- Current product says free, but provider economics/demand need validation.

### PayAPI Market — VERIFIED / EARLY
- UK-positioned x402 marketplace for paid data/APIs.
- Public site states providers can list endpoints, set per-request prices from $0.001 and keep 100%.
- Claims hosted/no-code path and USDC/Base settlement.
- Geography and provider eligibility outside the UK positioning are unresolved.
- Classification: own-data/endpoint monetization; automation 5 potential.

### endpoint.farm — VERIFIED / ALPHA
- Marketplace for paid agent-callable endpoints/MCP tools with non-custodial settlement on Base/Stellar/Solana.
- Alpha page states providers can publish for free and keep 100% of listed price.
- Explicitly seeking first providers, so demand/fill-rate evidence is currently weak.
- Classification: own-endpoint monetization; automation 5 potential.

## Discovery/index layers — relevant but not necessarily direct revenue counterparties

### x402gle
- Auditions x402-paid APIs by making real paid calls, then lists passing endpoints automatically.
- Useful as a distribution/discovery layer for an owned paid endpoint.
- Not independently an earning mechanism unless it routes meaningful demand.

### Agentic Market
- Marketplace/discovery surface where agents find and pay x402 APIs in USDC.
- Public site indicates Coinbase operates the marketplace while x402 itself is Linux Foundation ecosystem infrastructure.
- Seller listing exists, but fee/eligibility/traffic economics need dedicated validation.

### 402 Index
- Open directory aggregating paid APIs across x402/L402/MPP sources and continuously checking endpoint health.
- Provides provider listing/claiming but is better modeled as distribution infrastructure than a payer.
- Important insight: indexed endpoints can greatly exceed payment-verified healthy endpoints, so directory size is not demand proof.

### gate402
- Free x402 endpoint listing with web/MCP discovery; ownership challenge required for listing/import.
- Optional paid visibility boost exists.
- Distribution layer rather than confirmed demand source.

### Decixa
- Probe-tested x402 API discovery layer; provider listing currently invitation/waitlist based.
- Distribution/watchlist rather than proven payer.

## Protocol layer findings

### x402 itself
Official seller documentation confirms that any existing API/server can add payment middleware and accept mainnet payments. This is **infrastructure, not a marketplace**. Therefore the economic strategy must always be modeled as:

`owned useful endpoint + discovery/demand channel + payment protocol + low-cost hosting`

not simply “run x402 and earn.”

### MPP
MPP (Tempo + Stripe) is likewise a machine-payment protocol, not an income source by itself. Its public service catalog is a discovery surface. MPP is payment-method agnostic and supports stablecoins/cards/Lightning-style rails depending on implementation.

## New risk evidence
Recent 2026 research adds two important cautions for x402 economics:

1. A security study of facilitator deployments found authorization/execution-safety weaknesses across evaluated facilitators; merchant-side facilitator choice and payment-verification hardening are real operating risks.
2. A population-scale measurement study argues that raw x402 settlement counts are highly manufacturable/concentrated and cannot be treated as proof of independent customer demand.

Therefore **on-chain transaction count must not be used as a profitability proxy without counterparty/demand analysis**.

## Economics implications
For an owned endpoint:

`Net = paid_calls * (price_per_call - variable_compute/API/data_cost - protocol/platform_fee - gas/subsidy cost) - server_cost - monitoring/security - tax`

The critical unknown is still paid utilization. Free listing, 95–100% revenue share, or instant USDC settlement do not create demand.

For endpoints wrapping a third-party paid API:

`Net = paid_calls * (sale_price - upstream_call_cost - platform/protocol fee) - hosting - failures/refunds - compliance cost`

but only if upstream resale rights are explicit.

## Azerbaijan gate
No newly discovered platform in this pass provided sufficient first-party evidence to conclude Azerbaijan seller eligibility. Wallet-native non-custodial settlement may reduce dependence on Stripe, but it does not remove sanctions/KYC/tax/platform-country rules. Keep Azerbaijan eligibility unresolved until platform-specific validation.

## Saturation conclusion
- New top-level mechanisms: **0**
- New independent own-endpoint marketplaces/services: **materially many**
- New directories/discovery layers: **materially many**
- Taxonomy saturation: **very high**
- Project saturation in x402/MPP cluster: **not reached**
- Overall project: **IN PROGRESS**

## Next run
Run 043 should not yet be the final all-category pass. First perform a **second x402/MPP own-endpoint convergence + authenticity/economics pass**:
- validate legal entities/terms/fees for Agent402, the402, PayanAgent, RelAI, PayAPI, endpoint.farm;
- determine whether marketplace fees are charged to seller, buyer, or facilitator;
- find direct evidence of independent paid utilization rather than catalog size;
- validate Azerbaijan/provider geography and KYC where possible;
- separate true marketplaces from directories/indexes/protocol wrappers;
- search alternative vocabulary: paid MCP marketplace, agent tool marketplace, 402 service registry provider, monetize MCP tool, pay-per-tool-call API, AI agent service seller, autonomous webhook marketplace.

Only after this cluster produces negligible new viable implementations should the next run become the final broad all-category saturation/control pass.
