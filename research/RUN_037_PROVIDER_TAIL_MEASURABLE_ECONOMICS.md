# Run 037 — exact-neighbor/provider-tail control + measurable economics

Date: 2026-08-16
Status: COMPLETE (research run), PROJECT STILL IN PROGRESS

## Goal
Continue exact-neighbor discovery after Run 036, test economics where possible, and determine whether project-level saturation has been reached.

## Executive result
Taxonomy remains saturated: **0 new top-level economic mechanisms**.

Project/provider saturation is **not complete** because this pass found and normalized a new independent implementation: **Atlara** (distinct from Atlora). Atlara explicitly advertises a Linux provider-node path for distributed AI inference and says providers receive roughly 85% of network economics, but the public earning flow is still early-access and some pages describe earnings as platform credits redeemable for AI API usage rather than clearly cash-withdrawable income. It therefore enters as a serious WATCHLIST/RESTRICTED provider candidate, not as proven profitable income.

Run 037 also materially tightened Evernode, the402, Open Cloud, Atlora and Aeterna.

---

## 1. Evernode — measurable economics tightened

### Current network scale
Community dashboard `everdash.geveo.com` reported **6,024 active hosts / 6,024 total hosts** when crawled in the current period. This is not the canonical hook state, but it is a useful live-network scale indicator.

### Reward mechanics
Official Evernode material still states:
- 10 host-reward epochs;
- first-epoch network reward quota 5,120 EVR per moment/hour, halving each epoch;
- 5,160,960 EVR allocated per epoch;
- rewards shared among eligible hosts;
- reputation threshold >=200 required by current reputationd documentation;
- reputation can be zeroed when fewer than 3 instances are offered, leases are not offered, lease fee exceeds the reward-linked ceiling, or other reputation conditions fail.

Official host docs require current Ubuntu host setup and warn that sanctioned entities are excluded by license.

### Registration economics
Current host onboarding requires **500 EVR** registration plus XAH reserves/fees. Official operations docs state that normal deregistration/membership redemption mechanics do not make the full registration amount risk-free; pruning can return only half of registration EVR stake, and the membership NFT/redemption system should therefore be treated as capital-at-risk/opportunity-cost rather than a simple refundable deposit.

### Token/liquidity reality
Xahau Explorer recently showed EVR around **$0.09–$0.094**, with only roughly **$1k/day** trading volume in the observed snapshot. This is a material liquidity/exit-risk warning even if accounting rewards look attractive in EVR terms.

### Rough reward sanity check
Do not treat this as a current-epoch assertion because the exact current hook epoch/eligible-host count was not retrieved.

If total network reward were 320 EVR/hour (the fifth scheduled quota) and all 6,024 observed hosts were eligible, gross host reward would be only about:

`320 / 6024 * 24 = 1.275 EVR/day`

At $0.091/EVR this is about **$0.12/day or $3.5/month** before tenant lease revenue, server cost, XAH fees, downtime and conversion spread.

If only a subset is eligible, per-eligible-host rewards rise. If the current epoch differs, results differ. Therefore the exact canonical epoch and eligible-host count remain mandatory before CAPEX.

### Decision
**VERIFIED / HIGH-PRIORITY MECHANISM, profitability unproven.**

The key insight is that host-reward-only economics may be too weak for a rented VPS at current token value unless eligible-host dilution is much lower than total-host count or tenant lease revenue is material.

---

## 2. the402 — autonomous provider path strengthened, demand caveat strengthened

Official provider docs now give a very clear machine-provider workflow:
- provider may be human or AI agent;
- services can be listed via API;
- automated services can receive jobs by webhook;
- a bidding agent can subscribe to requests and bid using the same public API as first-party agents;
- provider receives listed price minus a **5% platform fee**;
- payout is USDC;
- provider starter template exists as a Cloudflare Worker;
- public catalog exposes `provider_completed_jobs`, `provider_completion_rate`, reputation and confidence.

This remains one of the closest compliant forms of the user's target: a bot/service deployed once and allowed to discover or receive machine jobs and fulfill them automatically.

### Demand evidence caveat
A July 2026 population-scale academic measurement of the wider x402 ecosystem found that raw settlement counts are a poor demand proxy: activity was extremely concentrated and a large portion could be internal/manufactured rather than independent commercial demand. This paper does **not** prove the402 itself has fake demand, but it materially strengthens our rule that x402 transaction counts/catalog size must not be interpreted as independent buyer demand.

### Decision
**VERIFIED / HIGH PRIORITY.**

Next economic test should sample the402 provider job-history distribution directly and identify deterministic low-cost services with nonzero independent-looking histories. Catalog inventory alone is not enough.

---

## 3. Open Cloud — admission barrier clarified

Official provider page states provider onboarding includes:
- **KYC**;
- review of **legal entity**;
- **insurance**;
- data-center agreements;
- operations runbooks;
- typical onboarding around 2–3 weeks / KYC around 10 business days;
- dedicated and cloud-backed AWS/GCP/Azure provider models;
- provisioning webhook for cloud-backed templates;
- customer selection by provider identity/geography/compliance/reputation;
- 0% Open Cloud fee on dedicated/cloud-backed nodes;
- provider sets markup over hyperscaler spot rates;
- 4% marketplace fee on shared hosting.

### Decision
The mechanism remains unusually attractive for autonomous cloud resale, but it is **not a frictionless hobby/VPS marketplace**. The legal-entity, KYC, insurance and operational-review gate makes it a curated business-provider route.

Azerbaijan legal-entity eligibility remains unresolved and must be checked before any setup cost.

---

## 4. Atlora — remains unverified supplier side

Atlora's current public site describes itself as a marketplace for buying and selling LLM inference compute and shows API documentation, but the visible flow remains **waitlist-oriented** and the public documentation found in this pass is buyer/API focused rather than a concrete provider daemon, provider payout schedule or live supplier onboarding procedure.

Decision: **WATCHLIST / UNVERIFIED PROVIDER PATH**. Do not spend capital until provider onboarding, payout mechanics and live supply-side status are documented.

---

## 5. Aeterna — marketing claims still ahead of verifiable provider network

Current Aeterna public site claims:
- AI service economy;
- autonomous agents selling services using x402;
- compute contribution for passive income;
- data/attention/network-effect rewards;
- AETHER staking/resource credits.

However, this pass did not establish a sufficiently concrete production provider daemon, payout history, live job marketplace or independently inspectable network state corresponding to those claims.

Decision: keep **WATCHLIST / HIGH MARKETING-RISK**. If the next exact-neighbor pass still cannot find provider contracts/docs/explorer/prod payout evidence, downgrade/reject as non-actionable for this research phase.

---

## 6. NEW independent candidate — Atlara

Important: **Atlara (`atlara.ai`) is distinct from Atlora (`atlora.com`)**.

### What it claims
Current Atlara pages describe:
- distributed AI inference network;
- provider software for Linux, Windows and macOS;
- Linux installer and provider-node flow;
- automatic hardware detection/model selection and serving;
- network mode that links a device to an account and earns credits when idle;
- provider network spanning consumer hardware through servers;
- private-node routing via provider node codes;
- approximately **85% to providers** according to the mission page;
- marketing estimates for monthly earnings by device class;
- early-access provider enrollment.

### Why it matters
This is a genuinely separate provider implementation in the same economic family as distributed inference markets and therefore proves that project/provider discovery is still yielding new independent candidates.

### Important contradiction / uncertainty
Some Atlara pages frame provider rewards as 'earnings' and 'payouts', while another official program explicitly says idle compute earns **Atlara credits redeemable for Claude/Codex/GPT/Gemini API calls**. The public pages found do not yet establish that ordinary public-pool providers can withdraw those credits as fiat/crypto cash.

The site also remains early-access oriented. Marketing earning estimates are not utilization evidence.

### Classification
- Category: distributed AI inference compute provider
- Status: **WATCHLIST / RESTRICTED / EARLY ACCESS**
- Resource: CPU/GPU/RAM + uptime
- Linux: yes (official installer page)
- Normal VPS: technically possible for CPU/basic inference, but economic/provider eligibility unknown; GPU hosts much more relevant
- Bare metal/home device: yes by claim
- Automation: potentially 5/5 after setup
- Initial capital: existing hardware or rented compute
- Payout: **unclear — credits definitely documented; cash withdrawal not yet verified**
- KYC/geography: unresolved
- Economics: provider-share claim ~85%, but no verified paid utilization/rate distribution
- Main risks: early access, credit-vs-cash ambiguity, demand, hardware depreciation/electricity, marketing-only earning estimates
- Next action: verify terms, provider dashboard docs, withdrawal policy, supported countries, actual public-network availability and independent paid utilization.

---

## 7. Exact-neighbor saturation result

New top-level mechanisms: **0**.
New independent provider implementation: **1 material candidate (Atlara)**.
Existing candidates materially tightened: Evernode, the402, Open Cloud, Atlora, Aeterna.

Therefore the completion gate is **not met**.

## Next run — Run 038
One more exact-neighbor/provider-tail control is mandatory before any final all-category saturation pass.

Priority:
1. Atlara: terms, provider payout/withdrawal, geography/KYC, public-vs-early-access network status, provider cash vs credits.
2. Evernode: canonical hook/current epoch + eligible hosts if accessible; tenant/lease utilization evidence.
3. the402: direct catalog/job-history distribution; find automated/data providers with nonzero histories and estimate gross price minus platform/API cost.
4. Aeterna: one final production-proof check; downgrade if still marketing only.
5. Search neighbors using alternate role names: inference supplier, compute lender, AI worker node, API merchant, machine-service seller, webhook provider, server host marketplace, app-host node, cloud arbitrage/reseller marketplace.
6. If Run 038 produces no new material provider project (or only dead/test/duplicate projects), proceed to final all-category saturation control in Run 039.

## Run verdict
**IN PROGRESS.** Project-level saturation remains high but not complete.
