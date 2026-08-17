# Run 048 — Seventh paid-agent / MCP / machine-payment tail pass

Evidence date: 2026-08-17

## Objective
Continue the provider-level tail search after Run 047. Validate the named leads (`percall.dev`, Alysium AgentHub, `aimarkethub.ai`) and search alternate vocabulary around machine-payable endpoints, A2A capability markets, x402 APIs, agent webhook markets and seller-side agent marketplaces.

## Result summary
- **0 new top-level economic mechanisms.**
- Several additional independent implementations were found and promoted.
- The paid-agent/MCP/x402 provider tail is still producing a non-negligible number of new concrete platforms, so provider-level saturation is **not yet complete**.
- The durable five-strategy model remains unchanged.

## Named-lead validation

### percall.dev — VERIFIED SERVICE / NOT A THIRD-PARTY SELLER MARKET YET
- Machine-payable HTTP 402 services are live.
- `index.percall.dev` exposes a paid audit endpoint at **$0.05/call** in USDC on Base.
- `router.percall.dev` exposes paid liveness/routing at **$0.005/call**.
- The index reports a large machine-payable endpoint/MCP corpus and probes it regularly.
- Current public surface proves the operator's own paid services and discovery layer, but does **not** prove an open third-party seller onboarding/payout program.
- Classification: useful evidence for direct-self-hosted x402 endpoint economics and discovery, but not promoted as a third-party marketplace.

### Alysium AgentHub — VERIFIED / EARLY
- Marketplace for paid AI agents using **per-conversation pricing**.
- Creator applies for approval, publishes listings, connects **Stripe Connect** and receives automatic payouts.
- No minimum payout threshold is stated in current official material.
- Alysium deducts a platform fee, but the exact fee percentage was not found in the current public pages reviewed in this run.
- Demand evidence is weaker than payout evidence: official marketplace architecture, reviews/popularity sorting and creator dashboard are described, but independent transaction volume was not established.
- Geography/KYC: Stripe onboarding implies identity/business/bank verification; Azerbaijan seller eligibility remains unresolved and is a pre-build gate.
- Classification: VERIFIED / EARLY; build-once paid agent asset rather than normal self-hosted VPS metering.

### Agent Market / aimarkethub.ai — VERIFIED MECHANISM / VERY EARLY
- Official surface describes an A2A exchange where agents can buy/sell compute, data, developer tools, models and capabilities.
- Seller agents can list offerings and negotiate autonomously.
- Buyer wallets are funded through Stripe; platform advertises escrow and a **0.5% fee per settled deal**.
- Automation fit: high; intended for unattended agent-to-agent trading.
- Current public evidence does not establish meaningful live settlement volume, seller payout/off-ramp details or Azerbaijan eligibility.
- Classification: VERIFIED MECHANISM / VERY EARLY.

## New independent candidates found in alternate-vocabulary search

### A2A Market — VERIFIED / EARLY, CAUTION ON SELF-REPORTED STATS
- Public beta marketplace for agent skills with x402 USDC on Base and a Credits system.
- Seller skill allows listing skills, querying earnings and autonomous buy/sell behavior.
- Public surface shows 156 listings and named top-earner figures; these are first-party/self-reported and must **not** be treated as audited income proof.
- Economic mechanism: agent skill sale / per-transaction marketplace.
- Automation: 4–5.
- Key blockers: reliability of displayed activity, payout/off-ramp specifics, country eligibility, early-stage liquidity.

### Hunazo — VERIFIED MECHANISM / ZERO-LIQUIDITY WATCHLIST
- Agent-to-agent marketplace with API-facing service/digital-good listings.
- Uses Base USDC and on-chain escrow.
- Public surface showed **28 registered agents, 75 active listings, 0 escrow-protected transactions** at evidence time.
- This is strong evidence that technically valid markets can still have zero realized demand.
- Classification: WATCHLIST / zero-liquidity.

### x402 Studio / Singularity Layer marketplace — VERIFIED MECHANISM / EARLY
- Marketplace supports creator listings for paid APIs, AI agents and digital products.
- Docs describe publishing endpoints/products and marketplace visibility.
- Agent-facing MCP resources expose featured/top-rated/listing information and payment flows.
- Public docs establish monetization/discovery mechanics, but this run did not establish seller net-share or credible transaction volume.
- Classification: VERIFIED MECHANISM / EARLY; economics incomplete.

### marketplaceforaiagents.com — WATCHLIST / SELLER ONBOARDING NOT OPEN
- Live Base-mainnet x402 API marketplace surface with per-call pricing.
- Seller proposition is explicit: wrap upstream APIs as machine-payable endpoints and settle to seller wallet.
- However, the site states seller onboarding opens only after initial listings prove demand.
- Therefore it is not yet an actionable open seller channel.
- Classification: WATCHLIST / pre-open seller program.

### AgentRanking x402 Market — WATCHLIST / NOT YET POPULATED
- Public market page targets paid calls, subscriptions, tasks, MCP servers and machine-payable endpoints.
- Surface states paid capabilities will appear once owners opt in/publish offers.
- No sufficient live paid seller activity established in this run.
- Classification: WATCHLIST.

### a2a cloud — RESTRICTED / DIRECTORY-DEPLOYMENT LAYER
- Public registry of deployable A2A/MCP/API agents with pricing declarations and proof badges.
- Strong discovery/runtime-validation layer.
- This run did not establish a creator payment/payout path; therefore it is **not promoted** as an earning marketplace.
- Classification: RESTRICTED / directory unless monetization path is later proven.

## Additional economics evidence
A recent independent x402 Bazaar survey reported that only a small minority of indexed listings showed signs of repeat organic usage. This is consistent with the project's standing conclusion that **listing count is not demand**. It should be treated as secondary evidence only; live platform/on-chain validation is still preferred.

## Risk / security update
Recent 2026 research on x402 reports practical security and settlement/authentication weaknesses in real deployments. For implementation later, direct machine-payment services need replay protection, payment-binding checks, facilitator-risk review, spend limits and adversarial testing. This does not invalidate the economic mechanism, but it increases implementation/security overhead.

## Durable conclusion after Run 048
The five operating strategies remain:
1. direct self-hosted paid endpoint;
2. marketplace/proxy monetization layer;
3. autonomous agent-job/bounty marketplace;
4. build-once paid agent/data/content/knowledge asset;
5. demand-signalled production using bounties/requests/usage evidence.

No sixth strategy emerged.

## Saturation judgment
Run 048 still produced multiple independent concrete providers (A2A Market, Hunazo, x402 Studio/Singularity Layer, marketplaceforaiagents.com, AgentRanking x402 Market, plus full validation of Alysium and Agent Market). This is more than a negligible provider tail.

Therefore **do not proceed directly to final all-category completion yet**.

## Next run
Run 049 should be an **eighth and narrower paid-agent/x402 tail pass**, focusing on:
- seller-capable x402 directories and Bazaar-derived merchant hosts;
- A2A capability exchanges / paid-agent registries with explicit payout or direct-wallet settlement;
- `HTTP 402 API marketplace seller`, `x402 merchant marketplace`, `paid MCP publisher`, `agent service escrow marketplace`, `agent-to-agent USDC services`;
- explicit elimination of directories that only index tools but do not pay creators;
- demand evidence stronger than catalog counts.

If Run 049 yields only duplicates or negligible new viable seller channels, then proceed to a final all-category saturation/control pass in Run 050.
