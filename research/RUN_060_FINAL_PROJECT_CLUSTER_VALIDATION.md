# Run 060 — Final project-cluster validation + exact-vocabulary control

Date: 2026-08-17
Status: **completed**
Project state after run: **IN PROGRESS**

## Scope
Validate only the five residual projects from Run 059, then run one minimal alternate-vocabulary control using the exact terms `provider agent`, `agent jobs`, `seller offers`, `compute provider`, and `market maker`.

## Executive result
All five residual projects normalize into already-known mechanism families. **No new top-level economic mechanism** was discovered.

However, the required exact-vocabulary control surfaced two apparently independent current projects that are material enough to require a final narrow validation pass before completion:
- **RELOAD / reloadai.io** — decentralized AI inference market claiming live seller listings and idle-capacity monetization.
- **Conduit Protocol / conduitprotocol.net** — USDC marketplace for compute endpoints and machine-callable capabilities, with provider profiles and claimed mainnet earnings surface.

Because these are not merely keyword variants but concrete supply-side projects closely aligned with the original `server bot earns automatically` objective, the project must remain IN PROGRESS until they are normalized or rejected.

---

# 1. AgentLancer
Status: **WATCHLIST / VERIFIED MECHANISM, UNPROVEN PAID DEMAND**
Category: autonomous agent-job / service marketplace
Server-native: **yes**
Automation: **5/5**

### What is live
Primary site exposes agent-first signup, service publishing, job requests, proposals/negotiation, contract/escrow lifecycle and event polling. The platform explicitly provides a polling runner and machine-readable marketplace manifest. Seller payout is designed for USDT/USDC; buyer rails include card, USDT and USDC.

### Fees / settlement
- staged escrow default: 40% kickoff + 60% final balance;
- target card-assisted platform fee: up to ~5%;
- target crypto-direct fee: ~2%;
- seller payout: USDT/USDC after acceptance / settlement state.

### Admission / KYC / geography
Nickname-first API signup is documented. Public material reviewed in this run did not establish a mandatory KYC flow or documented Azerbaijan exclusion. Absence of an exclusion is **not** proof of Azerbaijan eligibility.

### Demand evidence
This is the weakness. AgentLancer itself distinguishes real activity from verified payment evidence and states that verified earnings remain zero until real buyer transaction proof exists. The homepage describes first-payment conversion as the current bottleneck. Therefore registrations, negotiations, views and service listings must not be treated as revenue proof.

### Net-profit model
`Net = accepted-job gross × (1 - platform_fee) - model/API cost - VPS/runtime cost - payment/network/off-ramp costs - failed-proposal/search cost - human exception handling`

### Conclusion
Excellent protocol fit for an autonomous server worker; poor current evidence of repeat paid demand. Keep on implementation shortlist only as a cheap experiment after research, not as a proven income source.

---

# 2. AgentGigs
Status: **VERIFIED, EARLY / DEMAND UNPROVEN**
Category: autonomous agent job marketplace + paid proofing
Server-native: **yes**
Automation: **5/5 after one-time onboarding**

### What is live
Official API docs explicitly support automated job browsing, applying, messaging, file delivery, proof submission, wallet-funded escrow operations and webhooks. Account registration/profile/API-key creation are programmatic; email verification can be automated if the agent has inbox API access.

### Human/KYC touchpoint
Stripe Connect onboarding is a one-time human KYC step required before receiving payouts. After this, the docs state the agent can operate autonomously.

### Fees
Agent-side commission currently documented as:
- Free: keep 90%;
- Pro $29/month: keep 93%;
- Enterprise $99/month: keep 95%.

The docs also describe paid proofer work, with eligibility gates for proofers and a 10% commission in the normal proof flow.

### Economics
For a free-tier worker:
`Net = accepted job value × 0.90 - model/API/tool cost - VPS cost - payment/off-ramp costs - proposal/revision/dispute overhead`

Break-even for Pro vs Free before other costs is roughly when monthly gross job value exceeds `29 / 0.03 ≈ $967`; Enterprise vs Free requires roughly `99 / 0.05 ≈ $1,980` gross/month, though the real comparison should include all tier benefits and demand limits.

### Demand evidence
The API documentation contains lifecycle examples and earnings-shaped response objects, but this run found no strong independent aggregate proof of recurring paid buyer demand. Treat the technical pathway as verified, utilization as unresolved.

### Geography
Stripe availability and payout country support are decisive. Azerbaijan eligibility was not established from the reviewed platform materials and must be checked at implementation time against current Stripe Connect coverage and platform policy.

### Conclusion
One of the best technical matches for the original goal because job discovery → application → delivery → payout are designed for agents. Viability depends almost entirely on actual job supply, win rate and ability to perform tasks cheaper than the bid.

---

# 3. Jobs in AI agent marketplace (jobsindrones.com)
Status: **WATCHLIST / PARTIALLY LIVE**
Category: autonomous agent job marketplace
Server-native: **yes in principle**
Automation: **3–4/5 today; target 5/5**

### What is live
Official pages state that agent registration, API-key creation, deployment and applying to a job by ID are live. Agents can expose HTTPS/JSON endpoints and apply programmatically. Completed agent work is intended to settle through Stripe escrow after milestone approval.

### Important limitation
Programmatic job discovery, contract history and outbound webhooks are explicitly still roadmap items on the agent-onboarding page reviewed in this run. The public homepage currently reported **0 agent-compatible roles** despite thousands of general AI jobs. This is a direct negative utilization signal for the autonomous-worker use case at this point in time.

### Fees
Listing is free; the marketplace says it takes a percentage fee on completed work, but the exact percentage was not published in the reviewed public agent pages.

### KYC / geography
Stripe escrow implies payment-rail identity/country constraints, but exact agent payout onboarding and Azerbaijan support were not established in the reviewed public material.

### Conclusion
Technically relevant but weaker than AgentGigs today because autonomous discovery is not yet fully live and current agent-compatible inventory is effectively absent in the observed snapshot. Keep WATCHLIST.

---

# 4. Surplus Intelligence
Status: **VERIFIED / STRONG TECHNICAL FIT**
Category: inference orderbook / API-capacity resale marketplace
Server-native: **yes**
Automation: **5/5**

### What is live
Official docs describe a two-sided marketplace where sellers list OpenAI-compatible endpoints, set prices and earn USDC per request. Settlement is on Base. The current docs expose seller APIs, model/price surfaces, routing/health mechanisms and an agent quickstart.

Current official snapshot reviewed in this run reported:
- 145 catalog models in a recent API snapshot;
- 76 active marketplace models in the public price surface;
- active production offers concentrated on a smaller provider subset;
- fee multiplier `10000` (1.0x / no percentage markup in that snapshot).

The public analytics page also exposed very large request/token counts over a recent 28-day window and realized-pricing statistics. These are stronger production-use signals than mere registrations, though they still need seller-attributable revenue analysis before calling any particular strategy profitable.

### Supplier model
A seller lists a supported upstream endpoint/key or other OpenAI-compatible capacity. Buyer traffic routes to the cheapest healthy offer and seller receives USDC settlement.

### Critical ToS caveat
Marketplace permission to relay an upstream key does **not** override the upstream API provider's Terms. Any resale strategy must independently verify that the specific upstream provider permits this use.

### Net-profit model
`Net = routed tokens × seller price - upstream provider cost - marketplace/settlement/network costs - server/proxy cost - failed/health-check traffic - withdrawal/off-ramp cost`

The core edge is a positive spread while staying cheap enough to win routing. Price competition can compress this toward zero.

### Geography / KYC
USDC/Base reduces dependence on a bank payout rail, but platform identity rules, wallet/off-ramp availability and upstream-provider geography still matter. Azerbaijan support was not explicitly established.

### Conclusion
Promote from lead to VERIFIED. One of the strongest current server-native opportunities in the catalog, especially when paired with legitimately discounted/committed upstream inference or owned inference hardware. Profit is not guaranteed; the crucial variables are fill rate and lawful upstream cost basis.

---

# 5. Alien / Liquid Compute
Status: **WATCHLIST / MECHANISM VERIFIED, PRODUCTION ECONOMICS UNPROVEN**
Category: decentralized GPU compute marketplace + availability staking
Server-native: **GPU server yes**
Automation: **5/5 target**

### What is documented
Official documentation presents provider onboarding through a launcher/CLI, workload adapters for training/inference/rendering/quantization/federated work, automated health/autoscaling, compute settlement and a dual-token system:
- ACU for compute settlement;
- AVL for availability incentives / staking.

The docs explicitly describe provider staking, availability rewards and slashing, and claim providers can monetize gaming or enterprise GPUs.

### Important risk
The reviewed page contains strong architectural and economic claims, including network-stat placeholders and claims of broad participation, but did not supply enough independently attributable real paid utilization or liquid payout evidence in this pass. Token settlement design and production customer demand must be separated from marketing/architecture documentation.

### Economics
`Net = customer-paid compute settlement + realizable availability rewards - electricity - GPU depreciation - bandwidth - server/ops - stake opportunity cost - expected slashing - token liquidity/price losses - withdrawal costs`

### Conclusion
Keep WATCHLIST. It maps entirely to known GPU compute + stake-backed availability mechanisms and adds no new family.

---

# Exact-vocabulary control
Queries intentionally restricted to the residual vocabulary rather than reopening broad categories:
- `provider agent marketplace earn API autonomous`
- `agent jobs marketplace API autonomous earn`
- `seller offers inference marketplace USDC AI`
- `compute provider market maker GPU marketplace`

## Result
Mostly duplicates / already-known concepts appeared: AgentLancer, Surplus Intelligence, UsePod and generic marketplace material.

Two concrete independent leads were material enough to prevent completion:

### RELOAD / reloadai.io
Current public surface describes a decentralized AI inference market with a seller-listing concept, live marketplace metrics placeholders and monetization of idle capacity. It appears to normalize into the existing inference-marketplace family, but supplier admission, payout economics, real seller utilization, KYC/geography and production state must be validated from primary docs.

### Conduit Protocol / conduitprotocol.net
Current roadmap/public material describes live mainnet compute endpoints and capability providers paid in USDC, machine-readable provider profiles and a marketplace ranked by on-chain earnings. This appears to normalize into existing compute-endpoint / paid-API / machine-to-machine service families, but primary production activity, provider onboarding, fees, payout and identity rules require validation.

No third independent cluster emerged from the control.

---

# Run 060 mechanism conclusion
New top-level mechanisms: **0**.

The five residual projects normalize to:
1. autonomous agent-job/service marketplaces;
2. inference/API resale markets;
3. GPU compute/resource marketplaces;
4. stake-backed availability incentives.

Taxonomy saturation remains effectively converged. Project-level saturation is **not yet complete** solely because the final control surfaced RELOAD and Conduit Protocol as two concrete residual projects.

# Next run
**Run 061 — validate only RELOAD and Conduit Protocol, then repeat one tiny exact-name/role control.**

If both normalize into existing families and that tiny control produces only duplicates/negligible results, mark the project COMPLETE and record remaining implementation unknowns rather than opening another broad search.