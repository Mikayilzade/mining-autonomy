# Run 062 — Final API Mart validation + exact-name saturation control

Date: 2026-08-17
Status: **completed**
Scope: deliberately narrow final residual validation only. No broad category reopening.

## Objective
Validate the only remaining independent residual project from Run 061 — **API Mart / tryapimart.app** — against the repository's server-native autonomous-income criteria, then run one tiny exact-name control to test whether the residual vocabulary reveals another independent project or mechanism.

## Result
**0 new top-level economic mechanisms. 0 material independent projects from the control.**

API Mart normalizes cleanly into two already-known families:
1. **inference/API resale + automatic routing marketplace**;
2. **machine-callable paid capability/agent-skill endpoints (x402-style).**

The project is technically an excellent fit for autonomous/server-native operation, but current paid utilization is not established strongly enough to call it a proven profitable deployment target. It is therefore retained as **WATCHLIST / VERIFIED MECHANISM, DEMAND UNPROVEN** rather than promoted to a top implementation pick.

## API Mart — current mechanism validation

### What is paid for
API Mart lets sellers list upstream model/API capacity, set a price per million tokens, and route buyer inference through the seller's upstream API key. Buyer credit purchases settle in USDG on Robinhood Chain.

First-party docs state:
- buyer calls use an OpenAI-compatible inference endpoint;
- routing prefers the cheapest healthy marketplace offer where the buyer holds credits;
- sellers select a supported upstream provider, paste a key and set a per-million-token price;
- buyer top-ups go directly to the seller wallet and platform treasury;
- seller margin is the seller price minus upstream-provider cost.

This is not a new mechanism: it is an inference-resale / metered API-capacity market already represented by prior candidates such as RELOAD and Surplus-like routing/supply markets.

### Seller economics
Current first-party seller/docs pages state:
- seller receives **99% of each buyer top-up upfront**;
- platform takes **1%** in the same settlement flow;
- settlement token is **USDG** on Robinhood Chain;
- ETH is used for chain gas;
- seller payment is wallet-to-wallet and there is no platform withdrawal step for the seller.

Net-profit model:

`Net = 0.99 × buyer top-ups attributable to seller - upstream API/model cost - server/proxy/monitoring cost - gas/off-ramp/FX cost - failure/refund/operational losses - taxes - maintenance`

A more useful unit model is:

`Net per 1M tokens = seller quoted revenue per 1M - actual upstream provider cost per 1M - effective platform/settlement overhead - ops cost`

The dominant hidden variable remains **fill rate / paid buyer demand**. An attractive spread is irrelevant if no buyers pre-purchase credits or route requests through the offer.

### Automation suitability
**Automation: 5/5 in principle.**

The service is explicitly API-native. Current docs describe wallet-signature authentication, API-key creation and autonomous agent purchasing without email/card/CAPTCHA. Seller-side offers are persistent and buyer requests are routed automatically to healthy offers. A seller can therefore operate with minimal intervention once upstream capacity and pricing are configured.

For the original project objective, the role is server-native only in the economic/control sense: the marketplace itself does not require a home device. The actual compute may be an upstream cloud/model provider rather than the seller's own VPS/GPU.

### Identity / KYC / geography
Public first-party material reviewed in this run shows wallet-signature identity and does **not** document universal seller KYC in the visible onboarding/docs flow.

However:
- absence of a public KYC step is not proof that none can be required later;
- no Azerbaijan-specific eligibility statement was found;
- wallet access and Robinhood Chain/USDG access do not by themselves establish local legal/off-ramp availability.

Classification: **geography/KYC still implementation-gated.**

### Upstream-resale authorization
This is the most important compliance gate.

API Mart technically allows sellers to paste upstream API keys and resell usage, but **marketplace support does not grant resale rights over an upstream provider's service, credits, subscription or promotional quota**. Before listing any provider, implementation research must inspect that provider's current Terms/plan terms for resale, sublicensing, credential sharing, pass-through use and commercial redistribution.

Do not assume unused subscription credits can legally be resold merely because API Mart's UI accepts the key.

### Current activity / demand evidence
There is a material conflict in API Mart's own public surfaces:
- the homepage advertises a live marketplace and **350+ models**;
- the currently indexed `/markets` surface showed **0 of 0 models**, 0 text/image/video/music/TTS/STT entries and no visible seller inventory.

Therefore the repository does **not** treat the 350+ model claim as proof of active third-party marketplace liquidity.

The homepage also presents example prices, a free demo and broad seller language, but these do not prove repeat customer-paid seller utilization. No robust public evidence of distinct paying buyers, seller receipts, recurring settled volume, or seller-attributable marketplace revenue was established in this run.

Conclusion: **mechanism live/implemented; organic seller demand unproven.**

### Agent Skills / x402 path
The homepage describes a separate pay-per-call Agent Skills surface where callable tools such as summarization/translation/JSON extraction can be listed and agents pay per request in USDG via x402.

This maps directly to the already-established **paid machine capability / paid endpoint / agent-service marketplace** family. It is strategically interesting because it better matches `server bot performs simple machine-paid work`, but this run did not find enough first-party public evidence for:
- live skill inventory;
- provider admission details;
- provider fee schedule distinct from inference resale;
- attributable paid request volume;
- repeat buyer demand;
- skill-provider receipts.

Classification: **WATCHLIST / mechanism advertised, provider economics not yet independently proven.**

### Token incentives
The homepage advertises $APIMart-related fee discounts/free inference and promotional credit mechanics. These are not treated as seller revenue or proof of marketplace demand. Token incentives are excluded from core economics unless they can be shown to represent durable, liquid, independently realizable value rather than a subsidy.

## Tiny exact-name control
Queries were deliberately restricted to:
- `API Mart`
- `tryapimart`
- `Agent Skills`
- `Robinhood Chain USDG inference marketplace`
- directly adjacent wording

Results:
- official API Mart docs/home/buy/sell/markets surfaces;
- unrelated name collision `apimarts.com`, which is a conventional API marketplace and not the residual project;
- token-market pages for $APIMart, useful only as weak activity context and not a new earning mechanism;
- no new independent server-bot earning project requiring another research run.

### Control conclusion
- New top-level mechanisms: **0**
- New material independent projects: **0**
- Duplicate/adjacent results only: **yes**
- Residual queue after validation: **empty**

## Final classification — API Mart
- Category: inference/API resale marketplace + paid machine-callable agent skills
- Status: **WATCHLIST / VERIFIED MECHANISM, PAID DEMAND UNPROVEN**
- Server-native: **yes**
- Automation: **5/5 in principle**
- Resource/service: authorized upstream inference/API capacity; separately self-hosted callable skills/endpoints
- Settlement: USDG on Robinhood Chain; ETH gas
- Seller fee: 1% stated on current first-party pages; 99% seller top-up receipt
- KYC: no universal public seller-KYC step found; unknown beyond reviewed flow
- Geography/Azerbaijan: no explicit eligibility confirmation found
- ToS gate: upstream provider must independently permit the intended resale/pass-through use
- Demand: **not proven**; public marketplace inventory conflicts with homepage model-count claims
- Main economic risk: near-zero fill rate despite technically favorable routing/margins
- Scaling constraint: upstream quotas/terms, price competition, buyer credit fragmentation, provider reliability and actual demand
- Maintenance: low-to-moderate after setup; upstream health and pricing need monitoring

## Completion decision
The repository's completion gate is met:
- all major mechanism families were explored across prior runs;
- Runs 018–062 produced repeated saturation/control passes without a new top-level mechanism;
- the sole remaining residual project was normalized into existing families;
- the final exact-name control returned only duplicates/adjacent results;
- remaining unknowns are implementation/economics unknowns, not missing taxonomy branches.

**Research phase verdict: COMPLETE.**

Completion does not mean every candidate is profitable. It means the opportunity universe has converged sufficiently that additional broad discovery is now lower-value than implementation-specific validation and small-scale experiments on the strongest candidates.