# Run 049 — Eighth paid-agent / x402 / A2A seller tail

Date: 2026-08-17
Status: **COMPLETE — project remains IN PROGRESS**

## Purpose
Narrow saturation pass focused on seller-capable x402 directories, Bazaar-style merchant discovery, paid MCP publishers, A2A service exchanges and explicit direct-wallet/USDC seller settlement. Deduplicated against the durable catalog and Runs 041–048.

## Result
**0 new top-level economic mechanisms.** The five-strategy machine-paid architecture remains unchanged.

However, this pass still found several independent seller channels not present in the durable catalog. Provider-level saturation therefore has **not** converged enough to trigger the final all-category pass yet.

## New independent candidates

### 1. Agent402 Marketplace — VERIFIED seller channel
- Type: marketplace/proxy monetization layer for machine-payable APIs.
- Supply: seller registers an existing API/service endpoint.
- Payment: x402 per-request USDC; seller chooses among supported networks; settlement described as non-custodial/direct to seller wallet.
- Entry: official marketplace says registration is free and seller pays only when buyers pay.
- Scale evidence: first-party surface currently advertises 17k+ indexed services, 13 networks and 3 facilitators. These are supply/infrastructure counts, **not proof of independent paid demand**.
- Server-native: **yes**; ordinary HTTPS API endpoint is the supplied asset.
- Automation: **5/5** after deployment, subject to uptime/support.
- KYC/geography: no Azerbaijan-specific restriction established in this pass because direct-wallet crypto settlement is emphasized; legal/tax/off-ramp remains separate.
- Economics: `net = paid_calls × seller_net_per_call - compute/API/model cost - hosting - chain/facilitator/marketplace charges - maintenance - tax/off-ramp`.
- Key unknown: fee schedule beyond “free to register / pay when buyers pay”, plus attributable paid volume by independent buyers.
- Classification: **VERIFIED, economics unproven**.

### 2. Atelier — VERIFIED seller + bounty + x402 channel
- Type: two-sided AI-agent marketplace plus bounties/subscriptions/x402 machine orders.
- Supply: an independent autonomous agent is an HTTP service; builders can register it and list services.
- Payment: USDC on Solana/Base. Standard completed marketplace order: official docs say agent receives 90%, platform 10%. For x402 machine orders the 10% is added on top, so the agent receives its full list price.
- Demand modes: direct orders, subscription workspaces, bounties and x402 machine hires.
- Server-native: **yes**; official builder docs describe the agent as an HTTP service.
- Automation: **5/5** is feasible for machine-fulfillable services.
- Entry: builder guide describes API registration; no conventional approval process is claimed in the referenced current guide, though identity/owner verification mechanisms exist.
- Economics: unusually transparent relative to tail peers, but utilization remains unknown.
- Geography/KYC: Azerbaijan eligibility and any linked wallet/provider restrictions remain unresolved.
- Classification: **VERIFIED, high-priority later pilot candidate**.

### 3. The Grid — WATCHLIST / technically seller-capable
- Type: Base-mainnet A2A services marketplace.
- Seller flow: create/host Agent Card, register on-chain via ERC-8004, list services, accept negotiation, buyer settles USDC via x402/EIP-3009, seller delivers.
- Settlement: direct on-chain USDC; facilitator is described as paying Base gas.
- Server-native: **yes in architecture**.
- Automation: **5/5** in architecture.
- Demand evidence: public surface showed blank system metrics and a network feed waiting for activity during this pass. No credible paid-volume evidence established.
- Security: direct signing/facilitator/payment-verification architecture requires careful implementation review.
- Classification: **WATCHLIST** — valid seller mechanics, liquidity unproven.

### 4. CONMARK — WATCHLIST / technically seller-capable
- Type: Solana-mainnet A2A service marketplace.
- Seller flow: host Agent Card with service/pricing, register agent, auto-index, negotiate, receive x402 USDC payment and deliver.
- Settlement: docs describe autonomous SPL-USDC settlement through a facilitator, which submits the partially signed transaction and pays Solana fees.
- Server-native: **yes in architecture**.
- Automation: **5/5**.
- Demand evidence: no trustworthy independent volume/activity established; public metrics were not populated in discovery output.
- Classification: **WATCHLIST** — independently implemented seller channel but liquidity/economics not yet demonstrated.

### 5. AgentHire — WATCHLIST pending stronger verification
- Type: per-task marketplace where agents hire agents and humans can post jobs; x402 USDC on Solana.
- Seller proposition: public site explicitly invites owners to register an AI agent and earn USDC for capabilities.
- Server-native/API-first: **yes in stated architecture**.
- Automation: **5/5** possible.
- First-party demand claims: 500+ active agents, 10k+ jobs, $50k+ processed volume. These are **not independently audited** and should not be treated as proof of achievable seller utilization.
- Pricing examples are very low ($0.01–$0.10+), so inference/API cost discipline matters.
- Fee/KYC/geography and reproducible transaction evidence were not established in this pass.
- Classification: **WATCHLIST** until stronger operational/settlement evidence is collected.

## Adjacent but not an open seller marketplace

### 402.coffee / Agent Café — direct paid service example
A live operator selling machine-payable trust/risk/escrow/arbitration functions on Base. Current public prices include paid certification/risk lookup/arbiter services and a 1% escrow release fee. It is useful evidence that tiny autonomous x402 trust services can themselves be sold, but this pass did **not** establish an open third-party seller program. Keep as an implementation/business-model reference rather than a marketplace channel.

### x402 official Bazaar discovery
Official x402 seller quickstart confirms that a seller can add discovery metadata and use a facilitator supporting the Bazaar extension so paid endpoints become discoverable. This strengthens the already-known **direct self-hosted paid endpoint + discovery layer** strategy; it does not create a sixth mechanism.

## Duplicates / non-promotions
- Hunazo reappeared; already covered in Run 048 and still showed 0 escrow-protected transactions in current discovery.
- Generic x402/A2A explainers and payment stacks were not promoted unless an actual seller earning path existed.
- Directories/registries without creator-payment or direct-wallet settlement remain RESTRICTED/rejected as earning channels.

## Security control learned in this pass
Recent 2026 research on deployed x402 facilitators reports material authorization/execution weaknesses across evaluated implementations. For later pilots, treat the facilitator and merchant integration as a payment-security boundary, not a convenience library. Mandatory implementation checks should include payment-to-resource binding, replay protection/nonces, asset/network/recipient/amount validation, idempotency, bounded facilitator gas sponsorship, delivery/payment state consistency, wallet spend limits and withdrawal isolation.

## Saturation judgment
- New top-level mechanisms: **0**.
- New independent seller-capable platforms: **5 material candidates**, plus one useful direct paid-service reference.
- This is still a non-negligible provider yield, so project-level saturation is **not complete**.
- The next run should be a **ninth ultra-narrow tail pass** using names/terms adjacent to agent API stores, x402 Bazaar mirrors, paid MCP hosting and skill/service exchanges.
- If that pass yields only duplicates/negligible new channels, advance to the final all-category saturation/control pass.

## Next search vocabulary
`x402 API store publisher`, `x402 Bazaar merchant`, `AI agent API seller USDC`, `MCP server monetize per call`, `paid tool registry x402`, `agent skill store USDC`, `machine payable API directory`, `A2A service exchange seller`, `ERC-8004 marketplace seller`, `agent bounty API autonomous`.
