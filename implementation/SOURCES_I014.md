# Sources — Implementation Run I014

Evidence date: **2026-08-19**

## PayanAgent — first party
- `https://payanagent.com/`
  - API-first agent marketplace.
  - Documents public `GET /api/v1/discover`, public `GET /api/v1/receipts`, request/bid/fulfill/approve lifecycle, x402/USDC settlement and signed receipts.
  - Current homepage claims 24,000+ offers; this is supply/catalog evidence, not buyer demand.
- `https://payanagent.com/marketplace/requests`
  - Rendered retrieval exposed `0 open`.
  - Not saved as an API snapshot because the rendered shell did not provide a trustworthy raw-payload source timestamp.
- `https://payanagent.com/marketplace/receipts`
  - Rendered retrieval exposed the Receipts live-feed shell but no attributable rows.
  - Not saved as utilization evidence.

## MCPize — first party
- `https://mcpize.com/docs/monetization`
  - Subscription and x402 pay-per-call monetization; Base Sepolia testing; current standard 80% developer share.
- `https://mcpize.com/terms`
  - Current terms describe a 20% platform fee for servers with active monetization on/after 2026-06-10.
- `https://mcpize.com/developers`
  - Creator/deployment mechanics and first-party aggregate vendor-payout claims. Aggregate claims remain insufficient to infer our expected utilization.

## Evidence handling
No rendered counter, loading shell, provider count, listing count or first-party aggregate payout claim was promoted to transaction-level demand evidence. No source timestamp was fabricated.
