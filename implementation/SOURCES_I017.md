# Sources — Implementation Run I017

Checked: 2026-08-19. Primary/first-party sources only for time-sensitive platform mechanics.

## PayanAgent
- https://payanagent.com/ — official platform/API reference. Confirms anonymous discovery/receipts, API-key-gated seller/request actions, x402/USDC mechanics and public signed receipts.
- https://payanagent.com/marketplace/requests — rendered Requests surface observed with `0 open` plus loading state; treated conservatively as rendered zero-open only, not a raw API snapshot.
- https://payanagent.com/marketplace/receipts — rendered receipts surface describes live public settled feed but did not expose attributable rows in the available read-only rendering.

## agent2agent.market
- https://agent2agent.market/ — official task-exchange mechanics, anonymous task browsing, signed accept/submit lifecycle and USDC settlement.
- https://api.agent2agent.market/app — public read-only app shell; current available rendering exposes dashes rather than attributable live Open tasks / bounty / median values. No positive/zero count inferred.

## MCPize
- https://mcpize.com/developers — official developer monetization page; standard 80% developer revenue share, Stripe monthly payouts and x402 pay-per-call.
- https://mcpize.com/blog/x402-pay-per-call-live — official x402 production/payment-ledger description; publisher dashboard provides payment ledger and recent revenue analytics.
- https://mcpize.com/terms — official Terms; 20% platform fee for servers with monetization activated on/after 2026-06-10.

## Evidence handling
Marketing/catalog/provider counts and documentation examples are not classified as paid demand. No credentialed/account-only analytics were accessed. No raw public API payload with a trustworthy source timestamp was captured in this run.
