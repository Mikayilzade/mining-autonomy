# Sources — Run 054

Evidence date: 2026-08-17

Primary/current sources used for seller/provider validation.

## PayanAgent
- https://payanagent.com/
  - Provider registration, offers, request/bid/fulfill/approve flow, x402 direct-buy, USDC/Base settlement, public receipts, API-first operation.

## Agent402
- https://agent402.app/
  - Marketplace role, open seller registration, Demand Intel, x402/MCP/A2A/ERC-8004 positioning.
- https://marketplace.agent402.app/
  - Seller listing flow, multi-chain non-custodial settlement, open registration.
- https://marketplace.agent402.app/marketplace
  - Current marketplace snapshot used as a cautionary demand signal.
- https://tape.agent402.app/
  - Public directly-attributed x402 activity and named service call counts; used as demand-validation infrastructure, not as proof of profitability for any new seller.

## AiPayGen
- https://aipaygen.com/sell
  - Seller registration API/form, per-route pricing, 10% platform fee, Base USDC payout, no minimum withdrawal, seller dashboard.
- https://aipaygen.com/
  - Current marketplace/product context.

## Endpoints.market
- https://www.endpoints.market/
  - Provider pay-per-call model, USDC settlement, provider-set pricing.
- https://www.endpoints.market/docs
  - Current closed-beta status and provider documentation; this stricter source controls classification.

## Circle Agent Stack / Marketplace
- https://www.circle.com/blog/turn-your-api-into-an-agent-ready-revenue-stream
  - Published 2026-07-31. Paid API/x402 seller path and application for Agent Marketplace inclusion.
- https://www.circle.com/blog/turn-your-api-into-a-storefront-for-agents
  - Published 2026-05-18. Seller wallet / Gateway revenue path demonstrated on Arc testnet.

## x402 baseline / duplicate validation
- https://docs.x402.org/getting-started/quickstart-for-sellers
  - Direct self-hosted paid API/service seller flow; counted as a protocol strategy, not a distinct marketplace.
- https://docs.cdp.coinbase.com/x402/welcome
  - x402 seller/buyer protocol overview.
- https://www.x402apis.io/
  - Duplicate from Run 053; provider-node path remains valid.
- https://www.x402bazaar.org/
  - Duplicate/distribution layer from prior run.
- https://a2acloud.io/get-paid-for-ai-agents
  - Duplicate from Run 053; price-per-call and Stripe Connect seller settlement.

## Independent research used for risk/demand interpretation
- Shengchen Ling et al., `How Agentic Is Agentic Commerce? A Population-Scale Measurement of x402 Adoption and Authenticity`, arXiv:2607.12575, 2026-07-14.
  - Shows settlement counts cannot be treated as adoption/profitability evidence without attribution and independence checks.
- Qinying Wang et al., `When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments`, arXiv:2607.19545, 2026-07-21.
  - Documents authorization and facilitator/security failure classes relevant to merchant implementation risk.

## Evidence policy reminder
First-party provider counts, catalog size, marketing revenue calculators and aggregate settlement counts are discovery leads only. Promote demand confidence only when there is attributable paid activity, independent buyers/sellers, seller receipts, repeat utilization or similarly strong evidence.
