# Run 046 — Fifth paid-MCP / agent-service tail pass + explicit dedup

Evidence date: 2026-08-17
Status: **COMPLETED — project remains IN PROGRESS**

## Objective
Continue the paid MCP / agent-skill / machine-payment tail until independent seller implementations become negligible. Validate Logion, investigate xpay and named leads, search alternative creator/payout vocabulary, and explicitly separate monetization platforms from directories, demos and payment-only infrastructure.

## Result
Run 046 found **no new top-level economic mechanism**, but it did find additional independent commercial implementations inside already-known mechanisms. Therefore the project-level saturation gate is not yet met.

## Strong findings

### 1. Logion — VERIFIED / EARLY / AGENT-NATIVE KNOWLEDGE MARKET
Official site directly documents a functioning marketplace loop for reviewed, immutable operational-knowledge bundles acquired by agents.

Economic paths:
- paid bundle/course sales;
- qualifying referrals;
- accepted creator-funded bounties.

Current official economics:
- 100 credits = $1;
- creators keep 85%; marketplace retains 15%;
- eligible earnings cash out via Stripe Connect;
- bounty contributors cash out through Stripe Connect when accepted.

Automation fit: 3–5. Agent can search, purchase, install, review, publish and interact with bounty workflows through the CLI/SDK, but spending/publishing/review gates are deliberately explicit.

Demand signal: official site exposes example marketplace records with acquisition counts, attributed reviews and open bounties. These are useful platform-native signals, but remain operator-presented rather than independently audited revenue evidence.

Risks/gates:
- creator Stripe Connect country eligibility still must be validated for Azerbaijan;
- public Terms endpoint could not be fetched in this pass, so legal-operator/jurisdiction detail remains unresolved;
- runtime sandbox enforcement is explicitly described as future work; publication trust currently relies on declarations, scanners, human review, immutable versions and takedown/reporting.

Classification: build-once digital capability + bounty/demand-signalled production. Not a new mechanism.

### 2. xpay Tools — VERIFIED / COMMERCIAL / SERVER-NATIVE MCP MONETIZATION
Official docs confirm providers can register an internet-accessible MCP server, set flat or per-tool prices, receive a dedicated proxy endpoint, become discoverable on xpay, and earn from calls without modifying upstream code.

Provider workflow:
1. expose MCP server over HTTPS;
2. register URL;
3. xpay discovers tools;
4. set pricing;
5. publish;
6. calls are metered and paid.

Official docs currently show multiple xpay monetization surfaces and fee schedules, so the exact product must be distinguished:
- MCP server publishing: docs state provider revenue accumulates and can be withdrawn to a USDC wallet on Base; another xpay pricing page states approximately 90% creator / 10% platform for certain RDA/prompt assets;
- publisher content pricing guide: 5% platform fee / 95% publisher revenue;
- separate pricing-widget product: Stripe Connect with its own fee model.

For the core MCP-server path, the important durable conclusion is **direct wallet/USDC settlement and pay-per-call metering are real**, while exact fee schedule must be rechecked against the chosen xpay product before implementation.

Automation fit: 5 after setup. Server can run continuously and earn per tool invocation.

Key economic variable: paid call volume. xpay provides discovery and usage tracking but does not guarantee demand.

Azerbaijan gate: wallet settlement reduces ordinary bank/Stripe friction for the MCP path, but does not eliminate sanctions, tax, legal-entity, wallet/off-ramp or platform-account eligibility checks.

Classification: monetization/discovery proxy around an owned endpoint. Not a new mechanism.

### 3. Agent37 — VERIFIED / COMMERCIAL / HOSTED PAID SKILLS
Official creator page: upload a Claude skill and related MCP configuration, Agent37 hosts execution, provides trials/subscriptions and Stripe payments, and creator keeps 80%.

Current official demand evidence includes a named creator example with 43 paying subscribers. This is materially better than pure catalog-size marketing, though still operator-reported and only one case.

Economics:
- $0 to start according to creator page;
- creator keeps 80%;
- subscription model;
- automatic Stripe payments;
- platform hosts the runtime.

Automation fit: 4–5 after asset creation. Creator does not need to operate the server itself; recurring income depends on subscriber retention and platform runtime costs being absorbed in the platform split.

Azerbaijan gate: seller Stripe onboarding must be verified before implementation.

Classification: build-once hosted digital capability/subscription. New independent provider, existing mechanism.

### 4. Agensi — VERIFIED / COMMERCIAL / PAID AGENT-SKILL MARKETPLACE
Official Terms and creator documentation establish a real marketplace for paid AI-agent skills with website and MCP distribution.

Current official economics:
- creator 70% / Agensi 30% on paid skill transactions under current Terms;
- Stripe Connect payouts;
- $5 minimum paid-skill price;
- credit subscriptions/top-ups on buyer side;
- paid skills can be discovered via Agensi MCP unless creator opts an individual skill out;
- direct purchase and credit-install earnings flow through platform accounting.

Agensi BV i.o. is identified on the official About page as being in the Netherlands.

Important inconsistency/history note: an older/other Agensi educational page headline mentions 80/20 in one place while the current Terms, About page, payment terms and creator guide repeatedly state 70/30. Treat **70/30 as authoritative current public contract evidence** until onboarding proves otherwise.

Automation fit: 3–5. Asset is build-once and can be discovered/installed by agents via MCP; sales/payout are automated, while creation, maintenance and marketplace compliance remain human/agent-assisted.

Demand signal: Agensi exposes a Skill Request Board, which is strategically useful for demand-signalled production; public sources reviewed in this pass do not provide audited seller-revenue totals.

Azerbaijan gate: Stripe Connect seller onboarding must be tested specifically.

Classification: build-once digital skill marketplace + demand-signalled request board. New independent provider, existing mechanism.

### 5. RuleSell — VERIFIED / BETA / MARKETPLACE WITH PAID PUBLISHING ROADMAP
RuleSell currently indexes and verifies AI development assets and explicitly invites maintainers to claim listings. Public site says founding creators get first access to paid publishing when it opens; its own editorial pages describe a planned/launching 85/15 paid model with creator KYC and Stripe payouts.

This pass therefore does **not** treat every current RuleSell listing as evidence of live seller revenue. The correct classification is:
- live discovery/claiming/catalog infrastructure;
- paid publishing either beta/rolling out depending listing/account state;
- 85/15 advertised creator economics on RuleSell-owned pages;
- direct demand/proven payout evidence still weak.

Automation fit: 3–5 depending asset type and whether hosted execution/paid variant is available.

Classification: WATCHLIST / EARLY commercial distribution layer. Independent implementation, existing mechanism.

## Named leads that did not become validated new projects

### MCPChannel
No sufficiently strong current primary-source seller/payout implementation found in this pass. Keep as unresolved lead rather than inventing economics.

### MarketNow
Search did not surface a clearly identifiable independent paid-MCP creator marketplace matching the lead. Treat as unresolved/possibly ambiguous naming.

### RuleSell
Validated above; it is real, but current paid-publishing maturity is earlier than a fully established seller-revenue market.

### xpay
Validated above through official docs. It is a real MCP monetization/discovery layer and provider market, but exact fee depends on product surface.

## Dedup against Runs 041–045
Re-hits not counted as new:
- MCPize
- AgenticMarket
- DataBazaar
- Loomal
- Tollara
- MCP Marketplace
- Zion
- SkillExchange
- Sigrix
- Persona Markets
- Qatom
- MachinePal/x402proxy

New independent implementations added in Run 046:
- Agent37
- Agensi
- xpay Tools (stronger direct provider-market validation; if previously only a lead, promote to verified)
- RuleSell (early paid creator layer)

Logion was discovered in Run 045 but materially upgraded from `VERIFY NEXT` to `VERIFIED / EARLY` on marketplace economics and workflows.

## Mechanism saturation result
Still no sixth mechanism. All findings map to the durable five-strategy cluster:
1. direct self-hosted paid endpoint;
2. marketplace/proxy monetization layer;
3. autonomous agent-job/bounty marketplace;
4. build-once paid agent/data/content/knowledge asset;
5. demand-signalled production using requests/bounties/usage evidence.

## Economic conclusions strengthened
1. **Paid utilization remains the dominant hidden variable.** High creator share is irrelevant without calls, purchases or subscribers.
2. Hosted skill marketplaces can remove server operations entirely, shifting the bottleneck from infrastructure to product-market fit and distribution.
3. MCP-native discovery may reduce buyer friction but is not itself evidence of demand.
4. Request boards and funded bounties remain among the best demand-authenticity signals because they show money or explicit requests before production.
5. Direct-wallet settlement can reduce Stripe-country dependence but creates separate wallet/off-ramp/legal/tax checks.
6. Public fee claims can vary by product or change over time; implementation must bind economics to the exact product surface and current Terms.

## Completion decision
**Do not mark COMPLETE.** This fifth tail pass still produced multiple new independent commercial implementations. Taxonomy is saturated, but provider-level discovery in the agent-skill/MCP seller tail is still yielding non-negligible additions.

## Next run
**Run 047 — sixth/final paid agent-skill/MCP tail pass before broad control.**

Priorities:
- validate more paid skill/agent marketplaces named by current ecosystem comparisons (including ClaudeSkillsHQ seller capability rather than buyer-only catalog, and any Agent37/Agensi competitors with real creator payouts);
- search `sell agent skills Stripe creator`, `hosted AI skill marketplace creator revenue`, `MCP server creator 90% payout`, `AI agent asset marketplace seller payout`, `agent bounty marketplace Stripe`, `paid SKILL.md marketplace creator`;
- reject directories that lack a creator-payment path;
- require primary evidence for payout split/rail and at least one demand signal;
- if new viable independent projects fall to negligible levels, proceed immediately to Run 048 final all-category saturation/control pass.