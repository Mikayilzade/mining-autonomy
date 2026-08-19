# Sources — I016

Evidence date: 2026-08-19

## PayanAgent
1. PayanAgent first-party homepage/API reference — https://payanagent.com/
   - Confirms agent/service registration, public `GET /api/v1/discover`, public `GET /api/v1/receipts`, API-key-gated request bid/fulfill/approve workflow, x402/USDC mechanics and signed receipts.
   - Marketing/catalog counts are not treated as demand/utilization evidence.

## agent2agent.market
2. agent2agent.market first-party homepage — https://agent2agent.market/
   - Confirms anonymous machine-readable task browsing, worker registration, signed accept/submit lifecycle and USDC settlement after approval.
3. agent2agent.market current app surface — https://api.agent2agent.market/app
   - Observed current rendered state: `Open tasks 0`, no open rows, `no activity yet`.
   - Classified only as a zero-open public observation; not proof of historical inactivity.

## MCPize
4. MCPize monetization docs — https://mcpize.com/docs/monetization
   - Confirms subscription and x402 pay-per-call monetization, Stripe subscription path and Base/USDC x402 path.
5. MCPize Terms of Service (last updated 2026-04-12) — https://mcpize.com/terms
   - Confirms developer marketplace role, standard 20% fee for servers monetized on/after 2026-06-10, Stripe Connect payouts, identity verification and tax documentation requirements.
6. MCPize developer page — https://mcpize.com/developers
   - Confirms marketplace publishing and 80% developer revenue share for subscription/sale economics.
7. MCPize x402 pay-per-call article — https://mcpize.com/blog/x402-pay-per-call-live
   - Describes publisher Payments view with settlement ledger, BaseScan links, lifetime/7-day revenue analytics and direct USDC settlement.
   - Used to classify attributable utilization as publisher/account-view evidence rather than anonymous public demand.

## Evidence discipline
- No raw PayanAgent API response with attributable source timestamp was captured.
- No MCPize account/publisher analytics were opened.
- Public provider/server/catalog counts and hypothetical revenue examples were not treated as paid utilization.
