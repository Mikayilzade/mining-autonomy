# Catalog Additions — Run 056

Date: 2026-08-17

| Project | Status | Server-native | Automation | What earns | Payment / economics | Key limitation |
|---|---|---:|---:|---|---|---|
| MCPize | VERIFIED | Yes | 5/5 | Paid MCP subscriptions, usage tiers, one-off licenses and x402 per-tool calls | Creator keeps standard 80%; Stripe Connect monthly payouts; x402 USDC per-call supported | Demand/fill rate; Stripe/KYC/geography; upstream API/model cost; first-party aggregate payout metrics need independent corroboration |
| a2a cloud | VERIFIED | Yes | 5/5 | Paid deployed-agent invocations | Seller keeps 80% of markup; Stripe Connect Express bank payout; buyer compute charged separately | Passive invocation demand; Stripe geography/KYC; paid economics only on authenticated Agent API path |
| agent2agent.market | VERIFIED | Yes | 4–5/5 | Agent accepts posted tasks/bounties, submits result, gets approval-triggered payout | USDC on Base via escrow/approval release | Task availability, task-fit/quality, failed delivery, client approval/dispute and wallet security |
| SkillExchange | WATCHLIST | Yes | 5/5 | Paid MCP/A2A skill invocations/subscriptions | Stripe Connect; public site variously advertises 80/20, 85/15 and higher tiers | Current fee/revenue/activity figures conflict across first-party pages; demand claims need corroboration |
| EndPoints / endpoints.market | DUPLICATE / CLOSED BETA | Yes in architecture | 5/5 | x402 per-call API monetization | USDC; docs advertise zero platform fees | Still closed beta; already normalized in prior run |

## Strategic ranking impact
Top later implementation-research candidates for the original `autonomous server bot finds simple paid work` objective now include:
1. PayanAgent request/bid worker;
2. OKX.AI A2A ASP automatic matching + task intake;
3. agent2agent.market machine-readable bounty/task feed;
4. MCPize for paid MCP/API deployment where demand can be validated;
5. a2a cloud for paid deployed-agent invocations.

The machine-paid seller tail is now sufficiently converged at the mechanism level to move to the final all-category saturation pass.