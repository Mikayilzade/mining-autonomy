# Run 047 — Sixth paid agent-skill / MCP tail pass

Date: 2026-08-17
State: COMPLETE
Project state after run: IN PROGRESS

## Goal
Run a sixth deliberately narrow discovery/validation pass over paid agent skills, MCP monetization, machine-paid endpoints and agent job markets. Require an explicit creator/provider payment path and reject mere directories.

## Result
The tail is **not yet saturated**. This pass found multiple independent commercial implementations that were not present in Runs 041–046. No new top-level economic mechanism appeared: all hits still map to the existing five-strategy machine-paid architecture.

## Newly validated / promoted candidates

### 1. Techne Skills — VERIFIED / EARLY
- Model: build-once paid SKILL.md packages.
- Seller economics: founding creators keep 90% of each sale; standard creators 85%. Official pricing guide states Stripe processing is borne from Techne's portion; main creator page states payouts every two weeks.
- Pricing guidance: official tiers from roughly £15 to £149 depending on complexity/value.
- Automation: 3–4. Creation/maintenance remains human/product work; distribution and payment are automated.
- Demand signal: early/founding market, not enough durable seller-volume evidence yet. Official site explicitly says it is not yet using vanity metrics.
- Risk: early marketplace; utilization/product-market fit dominates.
- Azerbaijan gate: seller payout eligibility must be validated before implementation.

### 2. MCPlug — VERIFIED / EARLY
- Model: one-time paid MCP servers, AI tools, skills, workflows, prompts, templates, CLI tools and API integrations.
- Seller economics: creator sets price, keeps 85%; platform says payout via Stripe; 15% commission.
- Automation: 3–5 depending on whether product is downloadable or hosted service.
- Demand signal: official surface reports 3,255 skills, 8,381,227 downloads and 1,847 active agents, but the visible top-creator examples show that much download activity is free; paid conversion is not established.
- Important distinction: catalog/download scale is not proof of seller revenue.

### 3. AgenticMarket — VERIFIED / EARLY
- Model: paid MCP servers billed per successful call.
- Seller economics: standard creator 80%, founding creator 90%; creator sets per-call price. Official docs state $20 minimum withdrawal and payouts via Wise globally / Razorpay in India, within 7 business days; pricing page advertises average server prices around $0.03–$0.50/call.
- Automation: 5 for a stable hosted endpoint.
- Strength: server-native and directly aligned to project priority.
- Hidden variable: paid call volume / fill rate.
- Azerbaijan gate: Wise payout path and platform onboarding need direct validation before deployment.

### 4. SkillExchange — VERIFIED / EARLY
- Model: MCP/A2A agent-callable skills.
- Seller economics: 80/20 split; official creator page says payouts directly to bank via Stripe Connect.
- Demand signal: official marketplace claims 4,847 developers, 512 skills, 52.3K total executions, 100+ active creators and 25+ connected agents. These are platform self-reported and should be treated as early-market indicators, not audited revenue.
- Automation: 4–5 for hosted skill endpoints.
- Risk: beta-stage platform and Stripe-country eligibility.

### 5. Atrium Hermes — VERIFIED / EARLY, ON-CHAIN
- Model: portable agent skills priced per invocation in USDC on Base; creator can publish from CLI/web and agents can discover/quote/invoke/publish through MCP.
- Seller economics: protocol fee 2.5% (hard cap 5%); remainder after parent royalties accrues to creator and is withdrawable. Parent royalty shares can compose up to 50%.
- Automation: 5.
- Demand signal: official live page currently reports 68 skills, 60 active, 50 invocations and 16.098 USDC settled. Individual skill pages expose invocations and total earned; one paid demo shows 0.01 USDC volume and 0.00975 USDC earned after protocol fee.
- Interpretation: technically real settlement, but economic scale is presently tiny.
- Risks: wallet/private-key security, Base/USDC off-ramp, smart-contract risk, IPFS/key-service trust caveats, legal/tax treatment.

### 6. SkillHQ — VERIFIED / EARLY
- Model: paid Claude Code SKILL.md packages and Custom GPT configurations.
- Seller economics: 85% seller revenue advertised; Stripe Connect payouts. Seller page shows payout examples and says Stripe KYC is needed for direct bank payouts on Pro.
- Demand signal: official marketplace reports 272+ curated skills; visible listings include explicit sales counts, with many examples still at zero sales.
- Automation: 3–4.
- Important geography issue: official seller page says 45+ Stripe Express countries and does not establish Azerbaijan support. Treat Azerbaijan onboarding as unresolved.

### 7. .ctx (dotctx) — VERIFIED / EARLY
- Model: curated paid prompts, skills, templates, MCP assets, agents, harnesses, bundles and guides.
- Seller economics: creator keeps 80%; built-in Stripe Connect payouts.
- Demand signal: live official catalog exposes concrete product-level sold counts and reviews (examples visible during this run include 26 sold, 6 sold, etc.). This is stronger than a raw catalog count, though still platform self-reported.
- Automation: 3–4 for build-once assets; potentially 5 for MCP/agent products.

### 8. mcpmeter — VERIFIED / EARLY
- Model: metering proxy/marketplace for MCP servers; prepaid callers, per-call billing, publisher payouts.
- Seller economics: Terms state platform takes 10% for founders or 20% for standard publishers; publisher payouts once monthly. Site advertises Stripe Connect and per-call metering.
- Demand signal: official page shows 51 live listings and a live/simulated operational dashboard; actual paid-call volume needs stronger independent/on-ledger evidence.
- Automation: 5.
- Strategy fit: direct server-native monetization proxy.

### 9. SquidBay — VERIFIED / EARLY
- Model: agent skill marketplace with one-time ownership plus per-job remote-skill rental through A2A.
- Seller economics: seller keeps 90%; Stripe Connect v2 destination charges route 90% to seller, 10% platform fee; standard Stripe payout schedule.
- Automation: 4–5; remote skill mode can be fully server-native.
- Novel implementation detail, not new mechanism: one listing supports both downloadable full-skill sale and per-job remote execution.
- Risk: very early marketplace; buyer side is currently tied to Squid agents, limiting demand surface.

### 10. AI Agent Marketplace — VERIFIED MECHANISM / VERY EARLY, LOW-DEMAND
- Model: providers list webhook-connected AI agents; customers pay per approved task.
- Seller economics: provider keeps 88%, platform takes 12%; automatic Stripe Connect payout after approval; $45/month provider subscription.
- Automation: 5 after agent endpoint exists.
- Demand signal: official live platform currently states **no agents listed yet**. This makes it a valid implementation but a poor near-term deployment target because provider fixed cost begins before demonstrated demand.
- Net formula must include $45/month before API/model/server costs.

### 11. Callboard — VERIFIED MECHANISM / EARLY
- Model: autonomous agents compete for paid jobs; requester posts job, worker agents enter and best entry is paid.
- Demand signal: official site shows example job cards with concrete dollar values across editing, fact-checking, transcription, localization and device testing.
- Automation: potentially 5 for tasks that can be completed entirely digitally and compliantly.
- Remaining validation: exact worker payout rail/fee/withdrawal conditions must be captured before promotion to deployment shortlist.

### 12. Skarnfall — WATCHLIST / ZERO LIQUIDITY
- Model: agents register, bid on tasks and accept direct peer-to-peer payments.
- Automation: 5 conceptually.
- Critical demand signal: official site currently shows zero open tasks, zero registered agents and zero active humans.
- Classification: valid implementation lead but not viable deployment target today; keep on watchlist to prevent rediscovery.

## ClaudeSkillsHQ / similarly named services
### ClaudeSkillsHQ.com — RESTRICTED / BUYER-MARKET CONFIRMED, SELLER PROGRAM UNPROVEN
- Official Terms describe marketplace buying/downloading and tools for creating skills, and the live marketplace sells many paid skills.
- This pass still did **not** establish a clear third-party seller onboarding, revenue split or creator payout program for ClaudeSkillsHQ.com itself.
- Do not infer that because it sells skills it necessarily operates an open third-party seller marketplace.

### Claudeskills.ai — WATCHLIST / PRE-LAUNCH SELLER MARKET
- Separate domain/project. Official Terms specify buying/selling, Stripe Connect and 10% platform fee / 90% seller share.
- Homepage says “Coming Soon — Join the Waitlist.” Therefore economics are defined but marketplace liquidity is not live enough for deployment.
- Keep separate from ClaudeSkillsHQ.com to avoid name collision.

## Explicit rejects / non-promotions
- Directories and discovery-only registries with no creator payment path were not promoted.
- Claudeskillshop.com appears to aggregate public/community skill sources into a paid buyer store; no third-party creator payout path was established in this run, so it is not a seller opportunity.
- AI-agent/MCP directories whose only economic action is listing/free distribution remain discovery channels, not earning mechanisms.

## Dedup against earlier strategy model
All new candidates reduce to existing strategies:
1. direct self-hosted paid endpoint — AgenticMarket, mcpmeter, remote SquidBay, SkillExchange endpoint mode;
2. marketplace/proxy monetization — MCPlug, AgenticMarket, SkillExchange, SkillHQ, Techne, .ctx;
3. agent-job/bounty market — Callboard, Skarnfall, AI Agent Marketplace;
4. build-once paid asset — Techne, MCPlug, SkillHQ, .ctx, Atrium;
5. demand-signalled production — marketplace sales/executions, job boards and invocation ledgers.

No sixth top-level mechanism emerged.

## Strategic findings
- The paid-agent/MCP tail is larger and younger than expected; vocabulary changes rapidly and new seller surfaces keep appearing.
- Platform self-reported catalog/download counts must not be equated with paid demand. Prefer paid invocation, sold-count, funded-job or on-chain settlement evidence.
- A platform with explicit seller economics but zero supply/demand can be technically valid and economically useless today.
- For normal VPS/server autonomy, the strongest architecture remains metered per-call API/MCP or webhook job execution, because revenue can scale without repeatedly selling static files.
- Static skill marketplaces have lower operating burden but generally lower defensibility and uncertain repeat revenue.

## Outcome and next step
Run 047 produced a **non-negligible** number of independent viable/early implementations, so the completion condition is not met and Run 048 must **not** yet be the final broad saturation pass.

Next: Run 048 should perform a seventh paid-agent/MCP tail pass focused on recently surfaced alternate vocabulary: `machine-payable endpoint`, `agent tool marketplace payout`, `A2A skill seller`, `agent capability marketplace`, `HTTP 402 paid API`, `x402 creator marketplace`, `agent webhook marketplace`, and should deduplicate against the candidates above. If that pass collapses to negligible novelty, then move to a final all-category control pass.
