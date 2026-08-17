# Run 050 — ninth ultra-narrow paid-agent / x402 / A2A seller tail pass

Date: 2026-08-17
Status: **completed**

## Objective
Continue the provider-level saturation pass around paid agents, x402, MCP monetization, A2A service exchanges and ERC-8004 marketplaces. Deduplicate against Runs 041–049 and promote only candidates with an explicit seller/creator/payment path.

## Search families used
- `x402 API marketplace seller publisher USDC`
- `MCP monetize per call x402 seller`
- `ERC-8004 marketplace seller agent`
- `A2A agent marketplace seller USDC`
- `x402 API store publisher`
- `x402 Bazaar merchant`
- `AI agent API seller USDC`
- `MCP server monetize per call`
- `paid tool registry x402`
- `agent skill store USDC`
- `machine payable API directory`
- `A2A service exchange seller`
- `ERC-8004 marketplace seller`
- `agent bounty API autonomous`

## Results

### 1. t2000 — VERIFIED, high-priority
Official live surface: `https://t2000.ai/`

What it is:
- A2A commerce marketplace where agents can list services and humans/agents can hire them.
- Jobs are escrowed in USDC and settle to sellers with receipts.
- The live page exposes a seller path (`Sell -> list a service; payouts land in this wallet`).
- The page displayed actual settled entries and sold counts for listed services during this run, including examples priced per call/job.
- A visible settled example showed a 5% marketplace fee deducted from seller payout; x402 entries can also appear with no protocol fee depending on flow.

Fit to project:
- Server-native: **yes** for an HTTP/API-backed agent.
- Automation: **5/5** in principle.
- Resource sold: machine-executable service/task capability.
- Capital: low, aside from hosting/model/API costs and wallet funding/operational float if needed.
- Revenue driver: actual paid jobs/calls, not token emissions.
- Main hidden variable: buyer demand / fill rate.

Risk/unknowns:
- KYC and Azerbaijan eligibility were not established on the public surface.
- Real market depth is still small enough that utilization should be measured by a pilot rather than inferred from marketplace existence.
- Wallet/key security and x402/escrow correctness remain implementation-critical.

Conclusion: one of the clearest additional matches for the original goal: deploy a useful autonomous service, list it, and earn per completed machine/human purchase.

### 2. Basilisk — WATCHLIST, technically seller-capable but currently near-zero demand
Official live surface: `https://www.basilisk.exchange/`

What it is:
- Native marketplace for AI agents using ERC-8004, x402, MCP/REST and on-chain escrow.
- Explicit seller path: register agent, browse jobs, bid/accept work automatically, earn via on-chain escrow.
- Supports Solana and Base on the public surface.
- Public page states 70% released immediately on approval and 30% vested over 30 days.

Important current evidence:
- During this run, the public marketplace counters showed **0 registered agents, 0 total jobs, 0 active services and 0 payments processed**, and the jobs section stated there were no open jobs yet.

Fit:
- Server-native: **yes in architecture**.
- Automation: **5/5**.
- Economic mechanism: autonomous service/job marketplace, already known.

Conclusion: technically real seller architecture, but not currently actionable as an income source without proof of demand. Keep WATCHLIST; do not treat launch-readiness as revenue evidence.

### 3. x402 Bazaar — WATCHLIST / partial seller channel
Primary project repository surfaced as `Wintyx57/x402-backend`; live product advertises an x402 API marketplace.

Evidence found:
- Third-party services can be registered through a `/register` endpoint.
- Registration price shown in the project documentation: 1.00 USDC.
- The project advertises 43+ marketplace services in addition to native wrappers and positions itself as an API marketplace for agents paying in USDC.
- It provides a fast monetization template for turning Python functions into x402-paid endpoints.

Why not VERIFIED as a full seller opportunity yet:
- The retrieved documentation clearly proves registration and paid invocation architecture, but this run did not establish a sufficiently explicit current seller payout split/withdrawal path for third-party registrants.
- Utilization and independent paid-demand evidence remain unclear.

Conclusion: useful implementation/distribution lead, but retain WATCHLIST until payout mechanics and real demand are directly validated.

### 4. A2A Market — WATCHLIST, seller path strongly indicated but primary market surface not sufficiently validated
Discovered through the published OpenClaw/ClawHub skill ecosystem.

Evidence found:
- Skill documentation explicitly supports listing/selling AI-agent skills, x402 USDC payments on Base, seller rules, autonomous pricing/listing and earnings tracking.
- Multiple mirrors of the same skill describe a 2.5% platform fee and seller receipt of 97.5% on a sample sale.

Why not VERIFIED:
- Search results in this run were mostly skill mirrors/directories rather than a strongly validated current first-party marketplace surface.
- Treat example sales counts contained in skill documentation as examples unless independently tied to current production data.

Conclusion: real enough for WATCHLIST and later direct endpoint validation; not sufficient to promote to VERIFIED from this pass alone.

## Important negative/adjacent results

### Generic x402 seller quickstarts
Official x402 seller documentation proves that any API/server can charge buyers or AI agents per request, including mainnet operation on Base/Solana. This is infrastructure, not an independent marketplace/distribution channel, so it is **not a new provider candidate**.

### MCP payment guides/gateways
Current MCP monetization guides continue to confirm per-call, subscription and x402 patterns. They reinforce the direct-self-hosted paid-endpoint strategy but do not constitute an independent buyer marketplace unless they also provide discovery/demand.

### ERC-8004 directories/registries
Directories and identity registries without paid demand are not earning channels. Current empirical research also cautions against treating registration counts as economic activity.

## Security/economics update
Two recent empirical studies materially strengthen an existing caution:
- ERC-8004 registration/activity can be operationally shallow and reputation can be manipulated; registry counts are weak demand evidence.
- x402 settlement counts can substantially overstate independent commerce because linked/internal/fictitious activity is possible.

Therefore future ranking should weight, in descending order:
1. independently attributable paid buyers/jobs;
2. seller receipts / sold counts tied to distinct buyers;
3. repeat utilization;
4. gross settlement value after removing obvious internal/self flows;
5. only then listing counts / registered agents / protocol transaction counts.

## Saturation result
- New top-level economic mechanisms: **0**.
- New independent seller-capable platforms/candidates: **4** (1 VERIFIED, 3 WATCHLIST/partial).
- The provider tail is still producing several independent implementations, so project-level saturation is **not yet complete**.

Run 050 therefore does **not** trigger the final all-category closure pass yet. One more ultra-narrow tail pass is justified because the new-project yield is still non-negligible.

## Next run
**Run 051 — tenth ultra-narrow paid-agent / x402 / A2A tail pass**, but with stricter anti-duplication and demand evidence.

Focus vocabulary:
- `agent marketplace seller receipts x402`
- `x402 seller marketplace sold`
- `agent service escrow USDC marketplace`
- `MCP paid marketplace publisher revenue`
- `AI agent bounty marketplace API`
- `agent-to-agent marketplace per call USDC`
- `ERC-8004 jobs marketplace`
- `autonomous agent seller escrow`
- `paid agent skill marketplace`
- `machine API marketplace seller USDC`

If Run 051 yields only duplicates or negligible new viable seller channels, then proceed to a final all-category saturation/control pass.