# Run 061 — Final residual pair validation + tiny exact-role control

Date: 2026-08-17
Status: **completed**
Project state after run: **IN PROGRESS**

## Scope
Validate only the two residual projects from Run 060:
1. RELOAD / reloadai.io
2. Conduit Protocol / conduitprotocol.net

Then perform one tiny exact-role control using vocabulary from those two projects only. Do not reopen broad categories.

## Executive result
Both residual projects normalize cleanly into already-known mechanism families. **No new top-level economic mechanism** was discovered.

However, the required tiny exact-role control surfaced one additional independent current project not yet present in the repository: **API Mart / tryapimart.app**. It is materially aligned with the original autonomous-server objective because it explicitly lets sellers list upstream inference keys, receives USDG directly on Robinhood Chain, and also exposes x402 agent skills/capabilities. Therefore the project remains IN PROGRESS for one smallest-possible follow-up validation pass.

---

# 1. RELOAD / reloadai.io
Status: **WATCHLIST / VERIFIED MECHANISM, CURRENT SELLER LIQUIDITY UNPROVEN**
Category: inference/API resale + automatic routing marketplace
Server-native: **yes**
Automation: **5/5 in principle**

### What is live
Current primary pages describe an OpenAI-compatible routing layer in which buyers approve USDG on Robinhood Chain and requests are routed automatically to the cheapest healthy seller. Sellers connect a wallet, list an upstream provider key/model, choose pricing, and receive USDG per completed routed request. Seller credentials are verified and encrypted at rest.

### Current activity signal
The current seller page snapshot is the decisive weak point: it showed **$0.00 earned by sellers, $0.00 pool balance, 0 active offers and 0 live models** at crawl time. This contradicts more promotional homepage examples that display marketplace-scale numbers. For research purposes the live seller surface is treated as the stronger signal: mechanism is production-shaped, but current seller liquidity/utilization is not demonstrated.

### Admission / KYC / geography
- wallet-based authentication via Privy is documented;
- no mandatory identity/KYC step was found in the reviewed seller Terms/privacy/acceptable-use pages;
- no Azerbaijan-specific eligibility statement was found;
- absence of a geographic exclusion is not proof of eligibility or practical off-ramp access.

### Settlement / fees
- settlement asset: USDG on Robinhood Chain;
- sellers receive USDG per completed routed request;
- Terms say platform fees may apply, but a current numeric seller fee was not established from the reviewed primary pages;
- on-chain transfers are irreversible.

### ToS / upstream-resale restriction
This is explicit and important. Sellers represent that they have the right to resell upstream inference capacity, and RELOAD's acceptable-use policy forbids resale that violates upstream provider terms. Only keys/capacity the seller is authorized to resell may be listed.

### Recurring costs
`upstream provider cost + optional VPS/proxy/monitoring cost + Robinhood-chain gas/settlement/off-ramp cost + operational exceptions`

### Net-profit model
`Net = routed token revenue in USDG - upstream model/API cost - RELOAD/platform fees - server/proxy cost - network/off-ramp costs - failed-request/health-check overhead - human maintenance`

The key variable is fill rate. A positive unit spread is useless if no requests route to the seller.

### Conclusion
Technically excellent fit for a fully autonomous server/API supplier, but **do not call it currently profitable**. It adds no new mechanism beyond inference-resale/routing markets already represented by Surplus Intelligence and related suppliers. Keep WATCHLIST until live seller demand/liquidity is observable.

---

# 2. Conduit Protocol / conduitprotocol.net
Status: **VERIFIED MECHANISM / EARLY-EXPERIMENTAL, ECONOMICS NOT YET PROVEN**
Category: machine-callable capability marketplace + compute endpoints + relay participation + stake-backed provider routing
Server-native: **yes**
Automation: **5/5 for provider/compute/API roles; relay also automatable**

### What is live
Current first-party pages describe Conduit as experimental Solana-mainnet coordination infrastructure connecting buyers/agents to providers of APIs, compute endpoints, workflows, relays and other capabilities, with x402-style USDC settlement. Current roadmap pages label compute endpoints, capability providers, relay participation and the core Anchor programs as live/mainnet.

The public marketplace surface exposes machine-callable categories including GPU/CPU compute, object storage, LLM inference, embeddings, image generation, OCR, transcription, translation, vector retrieval, web scraping and agent-style services.

### Provider paths
Conduit exposes several supply-side roles:
- **Capability Provider** — wrap an API/model/service and earn per routed call;
- **Compute Endpoint** — register GPU/CPU capacity with region/concurrency/rate metadata;
- **Workflow** — compose multiple calls into a paid execution graph;
- **Relay Node** — contribute routing/benchmark/uptime intelligence;
- stake-backed provider/relay participation.

This is highly compatible with a daemon/API server and does not require pretending to be a human worker.

### Settlement / fees / stake
- primary settlement: USDC on Solana;
- paid calls settle per-call/per-token/per-second/GB-hour depending capability;
- first-party whitepaper states a **5% protocol cut** on paid calls feeds protocol rewards;
- provider/relay stake is slashable for objective failures such as downtime, failed execution, fake capability claims, payment fraud or fraudulent routing;
- provider tiers and routing weight may depend partly on stake/reputation/latency/price;
- some pages conflict on the exact asset used for provider stake (USDC vs CONDUIT), so the stake asset/amount must be rechecked immediately before any implementation.

### Bootstrap rewards caveat
The whitepaper describes a temporary bootstrap subsidy for active providers/relays in addition to organic demand. This must be separated from customer-paid revenue. Subsidies can disappear and should never be treated as durable profitability.

### Identity / geography
- current onboarding emphasizes wallets rather than account/invoice flow;
- Terms require lawful use, sanctions/AML compliance and prohibit bypassing regional restrictions;
- no explicit Azerbaijan approval was found;
- KYC is not documented as a universal onboarding requirement on the reviewed provider pages, but legal/off-ramp obligations remain jurisdiction-dependent.

### Real-demand evidence
The public site claims live analytics/on-chain settled volume and exposes many provider slots. These are stronger than a pure roadmap but still insufficient here to establish **provider-attributable recurring net profit**. Provider count/listing count is not demand. Organic paid calls must be separated from treasury/bootstrap payouts.

### Net-profit models
Capability/API:
`Net = paid calls/tokens × provider price - upstream API/model cost - 5% protocol cut if applicable - server cost - Solana/off-ramp cost - expected slashing - maintenance`

Compute:
`Net = paid GPU/CPU utilization - electricity - hardware depreciation/rent - bandwidth - protocol fees - stake opportunity cost - expected slashing - maintenance`

Relay:
`Net = relay fees + realizable bootstrap subsidy - server/device/network cost - stake opportunity cost - expected slashing - maintenance`

### Conclusion
Conduit is one of the closest conceptual matches to the original project: a server can expose compute or a machine-callable service and be discovered/paid autonomously. It still adds **no new economic mechanism**; it combines already-known paid API/capability, compute marketplace, relay and stake-backed operator families. Keep VERIFIED/EARLY rather than proven profitable.

---

# Tiny exact-role control
Queries intentionally limited to vocabulary directly surfaced by RELOAD and Conduit:
- `decentralized inference USDG seller marketplace`
- `Robinhood Chain inference seller marketplace USDG`
- `capability provider x402 USDC Solana marketplace`
- `compute endpoint x402 USDC provider marketplace`

## Result
Most results were duplicates, generic x402/capability material or already-known patterns.

One new independent project was material:

### API Mart / tryapimart.app
Current primary pages describe a Robinhood Chain inference marketplace where sellers:
- list provider/model offers using upstream API keys;
- set per-million-token prices;
- receive **99% of each buyer top-up upfront in USDG**, with a stated **1% platform fee**;
- are routed when they are the cheapest healthy offer;
- can operate via wallet-based, non-custodial settlement;
- must bear upstream provider cost, so seller margin is explicitly price minus provider cost.

The same project also advertises pay-per-call **Agent Skills** using x402, allowing endpoints to be listed and paid per call. Its docs state autonomous agents can complete buyer onboarding without email/card/CAPTCHA using wallet signatures and API calls.

Important activity caveat: the `/markets` snapshot observed during this run showed **0 of 0 models / no text models available yet**, despite the homepage advertising 350+ models and example prices. This discrepancy makes live third-party market activity uncertain and warrants direct validation rather than immediate promotion.

API Mart appears to normalize into the same existing inference-resale + paid-capability families, but it is a concrete independent project and must be validated once before project completion.

No second material independent project emerged from this control.

---

# Run 061 mechanism conclusion
New top-level mechanisms: **0**.

RELOAD normalizes to:
1. inference/API resale;
2. automatic cheapest-healthy routing;
3. wallet/stablecoin settlement.

Conduit normalizes to:
1. paid API/capability endpoints;
2. GPU/CPU compute marketplace;
3. relay/benchmark contribution;
4. stake-backed provider/operator incentives;
5. composable paid workflows.

Taxonomy saturation remains effectively converged. Project-level saturation remains open only because the mandatory tiny control surfaced **API Mart**.

# Next run
**Run 062 — validate only API Mart / tryapimart.app, then one tiny exact-name control.**

Required validation:
- seller ToS and upstream-resale authorization requirement;
- actual live offers/buyers/settled activity vs homepage examples;
- autonomous seller/API suitability;
- wallet/KYC/geography/Azerbaijan evidence;
- 1% fee and payout mechanics;
- Agent Skills provider economics;
- recurring costs and net-margin formula;
- whether any independent project emerges from exact-name control.

If API Mart normalizes into existing families and the exact-name control yields no further material independent project, mark the project COMPLETE and record remaining implementation unknowns instead of reopening broad discovery.