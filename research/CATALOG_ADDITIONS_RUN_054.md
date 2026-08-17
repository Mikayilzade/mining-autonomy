# Catalog additions — Run 054

Date: 2026-08-17

These entries supplement the living catalog and should be treated as current-evidence snapshots, not profitability guarantees.

| Project | Status | Server-native? | Automation | What earns | Payout / fee | Key limitation |
|---|---|---:|---:|---|---|---|
| PayanAgent | VERIFIED | Yes | 5/5 | Paid API/service offers plus request→bid→fulfill jobs | USDC on Base; direct seller settlement / escrow approval flow | Real demand/fill rate still uncertain; bespoke jobs depend on bid acceptance and buyer approval |
| Agent402 Marketplace | VERIFIED | Yes | 5/5 | Pay-per-call APIs, tools, agents and models | Non-custodial USDC, multi-chain | Public marketplace snapshot showed very weak recent call activity despite large indexed inventory; utilization is key risk |
| AiPayGen Seller Marketplace | VERIFIED | Yes | 5/5 | Third-party API calls listed in marketplace | Base USDC; 10% platform fee; no min withdrawal stated | First-party agent/call claims are not profitability proof; marginal upstream API/model cost can dominate |
| Endpoints.market | RESTRICTED / WATCHLIST | Architecturally yes | 5/5 if admitted | Pay-per-call API marketplace | USDC; docs advertise zero platform fee | Current docs say closed beta / early access; not yet an open deploy-now channel |
| Agent402 Demand Intel / Tape | VERIFIED strategic layer | Yes | 5/5 | No direct payout; identifies demand gaps and attributable paid x402 activity | N/A | Research/distribution signal only, not independent income mechanism |
| Circle Agent Marketplace | WATCHLIST / RESTRICTED | Yes | 5/5 | Paid API/service discovery through agent marketplace | x402 / USDC seller flow; marketplace inclusion appears curated | Apply/partner-style marketplace admission; public demand not established |

## High-priority implementation relevance

### PayanAgent
Closest new match to the original autonomous-small-jobs concept because the provider can programmatically discover requests, bid, fulfill and receive escrow release, while also exposing passive pay-per-call offers.

### Agent402
Useful not just as a seller marketplace but as a demand-selection system. The Tape/Demand Intel layer can help choose what to build based on observable demand rather than guesswork.

### AiPayGen
Clean fee model makes break-even testing easy:
`net/call = price × 0.90 - marginal cost - infra allocation`.

## Not new mechanisms
All Run 054 additions collapse into existing strategy families:
1. self-hosted paid endpoint;
2. marketplace/proxy distribution;
3. autonomous request/bid/service work;
4. build-once paid service asset;
5. demand-signalled production.

No sixth top-level machine-paid mechanism was discovered.
