# Sources — Implementation Run I019

Evidence date: 2026-08-19

## PayanAgent
- https://payanagent.com/
  - First-party homepage/API reference.
  - Documents `GET /api/v1/discover` and `GET /api/v1/receipts` as unauthenticated/public; provider/request/bid/fulfill actions use API keys.
  - Documents x402/USDC Base settlement architecture and 24,000+ catalog/offers claim.
  - Catalog size treated as supply, not attributable demand.

## agent2agent.market
- https://api.agent2agent.market/app
  - First-party public app currently renders `Open tasks 0`, `all 0`, `no open tasks`.
  - Same interface explicitly labels network `base-sepolia`; observation classified testnet only.
- https://agent2agent.market/
  - First-party homepage documents worker browse/accept/submit flow and USDC settlement mechanics.

## MCPize
- https://mcpize.com/developers
  - First-party developer page: standard 80% developer revenue share; x402 pay-per-call; Base Sepolia testing.
- https://mcpize.com/docs/monetization
  - First-party monetization documentation: subscriptions and x402 per-call USDC; Base mainnet vs Base Sepolia test flow; dashboard/payment setup boundary.
- https://mcpize.com/blog/x402-pay-per-call-live
  - First-party dated production announcement and fee/revenue-share context.

## Evidence handling note
No source above was used to infer paid utilization from listing/provider counts. No authenticated dashboard, wallet or transaction action was used.
