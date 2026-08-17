# Sources — Run 060

Evidence date: 2026-08-17

Primary sources were preferred. Search/discovery results are used only to identify leads unless promoted below by current first-party documentation.

## AgentLancer
- https://agentlancer.io/
  - autonomous provider/requester/verifier roles;
  - machine-readable onboarding + event polling;
  - card/USDT/USDC buyer rails and USDT/USDC seller payout;
  - staged escrow and target fee disclosures;
  - platform explicitly separates activity from verified earnings and identifies first-payment conversion as a bottleneck.
- https://agentlancer.io/transparency.html
  - production/market indicators and separation of synthetic, platform-recorded, real-agent and verified-payment evidence.

## AgentGigs
- https://www.agentgigs.io/docs/api
  - full agent API lifecycle;
  - one-time Stripe Connect KYC before payouts;
  - autonomous job browse/apply/deliver/message/proof operations after onboarding;
  - current agent commission tiers: Free 10%, Pro 7% ($29/mo), Enterprise 5% ($99/mo);
  - paid proofer workflow and API/webhook operations.

## Jobs in AI / jobsindrones.com
- https://www.jobsindrones.com/for-agents
  - registration, API-key creation, deploy and apply-by-job-ID live;
  - programmatic discovery/contracts/webhooks still roadmap on this page;
  - Stripe escrow payout after milestone approval;
  - listing free, percentage fee on completed work, exact percentage not shown.
- https://www.jobsindrones.com/agents/faq
  - HTTPS/JSON agent endpoint requirements;
  - expected autonomous operation;
  - escrow/dispute model and API limits.
- https://www.jobsindrones.com/
  - current public marketplace snapshot observed with thousands of general AI roles but 0 agent-compatible roles at crawl time; used as a negative current-utilization signal, not a guarantee of future inventory.

## Surplus Intelligence
- https://www.surplusintelligence.ai/docs
  - two-sided inference marketplace;
  - sellers list OpenAI-compatible endpoints and earn USDC per request;
  - Base settlement;
  - current model/provider/orderbook snapshot information and fee multiplier.
- https://www.surplusintelligence.ai/sell
  - current seller-offer surface.
- https://www.surplusintelligence.ai/markets
  - seller/buyer market framing and current marketplace price surface.
- https://www.surplusintelligence.ai/analytics
  - current aggregate production request/token and realized-pricing statistics; used as production-use evidence but not as seller-specific profit proof.

Secondary implementation corroboration (not relied upon for platform legitimacy/profitability):
- https://github.com/ProlowN/openclaw-plugin-surplus-intelligence
  - seller-key/offer/earnings integration details; useful as a discovery and implementation cross-check only.

## Alien / Liquid Compute
- https://alien.international/
  - GPU provider marketplace and launcher claims;
  - training/inference/rendering/quantization/federated adapters;
  - ACU settlement + AVL availability/staking design;
  - provider staking and slashing mechanics.

The page did not provide sufficient attributable paid-utilization proof in this run, so Alien remains WATCHLIST.

## Exact-vocabulary control leads
- https://reloadai.io/
  - surfaced by exact-vocabulary seller/inference control;
  - public surface claims decentralized inference routing and monetization of idle capacity;
  - requires Run 061 primary-source supplier/economics validation.
- https://www.conduitprotocol.net/roadmap
  - surfaced by exact-vocabulary compute-provider/capability-provider control;
  - public roadmap states compute endpoints and capability providers are live on mainnet and denominated in USDC;
  - requires Run 061 primary-source production/admission/economics validation.

## Evidence discipline
- No platform was called profitable from headline rewards or architecture claims.
- Marketplace registrations/listings/views were not treated as paid demand.
- Aggregate marketplace usage was distinguished from attributable seller earnings.
- Upstream API resale remains conditional on the upstream provider's own Terms.
- No Azerbaijan exclusion found was not interpreted as proof of Azerbaijan eligibility.