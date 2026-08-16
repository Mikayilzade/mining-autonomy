# Run 040 — Second supplier-tail convergence pass

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Objective
Re-check Keld/hosted.ai/Fluxenta supplier economics, then search exact inference-exchange/GPU-mesh/wholesale-resale neighbors plus non-GPU capacity-market analogs. Deduplicate against the durable repository checkpoint and decide whether supplier-level discovery has converged enough to move to the final all-category control pass.

## Result
The completion gate is **not met**.

Taxonomy remains saturated: **0 new top-level economic mechanisms**. However this pass found multiple independent provider implementations absent from the durable Run-039 checkpoint, including several that are already live or have explicit current supplier economics. Supplier-tail discovery is therefore still productive.

### New material current provider implementations
1. **Inpherio** — live beta peer-to-peer inference marketplace; providers keep 85%, monthly bank payout via Stripe, £10 minimum.
2. **UsePod** — open inference-provider + API-key resale market; providers earn 80% of settled inference in USDC; $50 USDC provider bond.
3. **HZ AI** — live distributed GPU exchange; GPU owners set price/GPU-hour and receive fiat payouts through Stripe.
4. **SpotNode.ai** — current inference-execution exchange for qualified GPU owners/operators; commercial terms are negotiated/opaque.
5. **KeyMart** — curated enterprise inference-provider marketplace with explicit volume-tier provider fees and automated payouts.
6. **Compute Exchange / TCEX** — institutional compute marketplace where legal-entity providers list idle compute and respond to buyer RFQs/asks.

Additional watch/restricted implementations discovered: **ClusterBid** and **Exascale/Hyperlink**. These require stronger commercial/external validation before economic modeling.

---

## 1. Keld — live supplier concept remains strong; payout/KYC still not public
Keld's current site and July 8, 2026 launch article continue to confirm:
- live inference marketplace;
- 100+ providers claimed by Keld;
- provider-side `Keld Trade`;
- spare inference capacity can be listed;
- micro-batching fills idle headroom;
- matching is based on price/deadline/performance/policy constraints.

No public primary-source fee schedule, provider payout rail, minimum payout, provider-country list or Azerbaijan eligibility was located in this pass.

Classification: `VERIFIED / RESTRICTED`.

---

## 2. hosted.ai GPU Mesh — supplier and zero-CAPEX resale paths confirmed
Current hosted.ai material explicitly says:
- service providers can publish physical GPU pools to Mesh;
- suppliers get paid for Mesh consumption;
- direct selling can continue in parallel;
- buyers can subscribe to wholesale GPU pools and resell under their own brand;
- wholesale is paid when downstream customers consume GPU;
- supplier/buyer payments use a built-in wallet;
- access is for service providers using the hosted.ai platform, not arbitrary consumer hosts;
- Mesh access is included for existing hosted.ai platform customers; pure-Mesh neocloud usage has a small minimum monthly platform fee.

Exact fee percentages, supplier payout rails, provider geography and Azerbaijan eligibility remain non-public.

Classification: `VERIFIED / RESTRICTED`.

---

## 3. Fluxenta — retain pre-production
No stronger evidence was found in this pass sufficient to upgrade the prior status. Keep `WATCHLIST / PRE-PRODUCTION` until provider onboarding and real settlement are publicly live.

---

## 4. Inpherio — NEW, unusually transparent live-beta provider economics
Inpherio states that its marketplace is fully functional in beta and provider self-service is live.

Provider economics and operations:
- £0 listing fee;
- providers keep **85%** of settled usage;
- 15% platform fee, waived for the first 3 months after first node;
- earnings credited when successful requests complete;
- payouts monthly on the 1st;
- payout to verified bank account via Stripe Connect;
- **£10 minimum payout**;
- **£0.50 flat payout processing fee**;
- provider sets model/token price;
- dedicated node rental also supported;
- outbound-only provider connector; no public inbound port required;
- current calculator explicitly warns that utilization, demand, price and model mix determine earnings.

Classification:
- Category: inference marketplace / node rental
- Type: SERVER/HOME GPU-NATIVE
- Status: `VERIFIED / BETA`
- Automation: 5/5 after setup
- Resource: GPU/model endpoint
- KYC: identity/bank verification via Stripe is implied by payout flow
- Geography/Azerbaijan: not confirmed in public material checked

Economics:
`Net = settled usage × 0.85 - electricity/cloud - hardware depreciation - bandwidth - ops - payout/tax costs`

This is one of the strongest later-stage candidates because settlement terms are public and provider operation is explicitly daemon-like.

---

## 5. UsePod — NEW open provider + API-key resale path
UsePod's current docs describe a two-sided inference marketplace with an open supply side.

Provider paths:
1. run a provider agent against local inference backends such as vLLM/llama.cpp/LM Studio/Ollama;
2. enroll an authorized upstream API key/key relay and resell inference capacity.

Economics:
- provider receives **80%** of each settled marketplace inference;
- treasury receives 20%;
- price is set by provider but capped at cheapest centralized price for the same model;
- earnings settle per request;
- withdrawal is on-demand in **USDC on Solana**;
- provider posts a **$50 USDC bond**;
- serious misbehavior can lead to ban/bond seizure;
- key-relay operator remains responsible for upstream API cost.

Classification:
- Category: paid inference marketplace / authorized API-capacity resale
- Type: SERVER-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation: 5/5
- Capital: $50 USDC bond + serving resources/upstream credits
- Geography/KYC/Azerbaijan: unresolved in material checked

Important compliance rule: the API-key resale branch is viable only where upstream provider contracts/ToS authorize resale. Do not treat possession of an API key as resale permission.

---

## 6. HZ AI — NEW live distributed GPU exchange
HZ AI currently advertises a live GPU exchange and an explicit provider onboarding path.

Provider evidence:
- one-command agent install on Ubuntu/Debian;
- GPU specs auto-detected;
- provider sets own price per GPU-hour;
- jobs are metered per second;
- marketplace supports SSH, batch/training jobs and inference endpoints;
- provider receives **fiat payouts**;
- payout rail stated as **Stripe**;
- consumer and datacenter GPU models are supported according to current marketplace description.

Classification:
- Category: raw GPU compute marketplace
- Type: SERVER/HOME GPU-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation: 5/5 after enrollment
- Geography/KYC/Azerbaijan: unresolved
- Platform fee: referenced but exact percentage not found in the inspected public page

Economics:
`Net = billed GPU-seconds × provider price - platform fee - power - depreciation/cloud lease - bandwidth - ops - tax/withdrawal costs`

---

## 7. SpotNode.ai — NEW qualified inference-execution supplier path
SpotNode.ai Pte. Ltd. describes a current exchange for production inference rather than a raw GPU listing market.

Supplier path:
- GPU owners, endpoint owners, enterprise infra teams and hosting operators can bring real spare capacity;
- zero-inbound onboarding agent;
- supply is benchmarked/scored/qualified before publication;
- live inference traffic is routed according to economics, health, latency and policy;
- payouts depend on qualified execution, live usage and commercial terms.

The public material does **not** expose a provider fee schedule, payout currency/rail, minimum payout or geography list. Onboarding appears commercial/qualified rather than permissionless.

Classification: `VERIFIED / RESTRICTED`.
Automation after qualification: 5/5.

---

## 8. KeyMart — NEW curated enterprise inference provider market
KeyMart exposes unusually explicit provider-side economics but is curated.

Provider requirements include:
- valid API keys with documented provenance / authorized reseller status;
- 99.5% trailing uptime baseline;
- streaming support;
- latency and minimum 50 RPM requirements;
- signed Provider Agreement;
- identity verification;
- upstream ToS compliance;
- automated SLA monitoring.

Fee schedule published by KeyMart:
- first 7 days: 0% platform fee;
- standard < $5k/month: 2.8%;
- pro $5k–$25k/month: 1.6%;
- enterprise > $25k/month: 0.5%;
- self-service withdrawal or scheduled automatic settlement.

Classification:
- Category: enterprise inference/API-capacity marketplace
- Type: SERVER/BUSINESS-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation: 4–5/5 after compliance onboarding
- KYC: yes
- Geography/Azerbaijan: unresolved

This is not a cheap anonymous VPS bot. It is a potentially autonomous business/provider channel after enterprise qualification.

---

## 9. Compute Exchange / TCEX — NEW institutional compute seller channel
Current official documentation and marketplace terms describe a buyer/seller compute market in which cloud providers/data centers can monetize unused compute capacity.

Provider evidence:
- sellers list resources and asking prices;
- buyers place bids; matching can occur through auctions/RFQs;
- provider resources may include processing, memory, storage and networking associated with compute;
- current provider page targets H100/H200-class institutional GPU supply and verified enterprise buyers;
- current marketplace terms define a Provider as a **legal entity** offering Compute;
- onboarding includes Master T&Cs and provider-network participation;
- current workflow includes qualified RFQs and direct introductions.

Classification:
- Category: institutional compute capacity marketplace/brokerage
- Type: BUSINESS-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation: 2–4/5 depending product/workflow; current provider RFQ path still contains human negotiation
- Cheap VPS: no
- KYC/KYB: effectively yes / identity-verified counterparties
- Geography/Azerbaijan: unresolved

Important: this is a real monetization channel for professional idle capacity but less autonomous than daemon-style retail markets.

---

## 10. ClusterBid — NEW but early-stage broker/sourcing desk
ClusterBid says it canvasses 340+ verified data centers and exposes a `List capacity (I am a DC)` route. However its April 23, 2026 Terms explicitly describe the public site as a marketing page for an **early-stage GPU sourcing service**, and commercial engagements are governed by separate written agreements.

Classification: `WATCHLIST / RESTRICTED`.
Do not model as an autonomous exchange until provider commercial operation and settlement are independently/currently demonstrated.

---

## 11. Exascale / Hyperlink — NEW claim-heavy exchange; verification caution
The current site at hyperlink.org presents Exascale as a live compute exchange with spot/futures/credits, provider capacity listings, per-second metering/payout, T+0 settlement and multiple data-center partners.

These claims would make it highly relevant if independently substantiated. The inspected material is almost entirely first-party and contains unusually specific market/audit/liquidity statistics. Before treating it as deployable income, verify company identity, counterparties, legal terms, actual provider onboarding and external production evidence.

Classification: `UNVERIFIED / WATCHLIST`.

---

## 12. Non-GPU analog/control pass
The same vocabulary was re-run for CPU/HPC/storage/bandwidth/API capacity exchanges.

Findings:
- Compute Exchange's legal definition includes processing, memory, storage and networking attached to compute, but its current public commercial focus remains GPU/AI capacity.
- Open Capacity Marketplace is a permissionless content-delivery capacity concept connecting content providers to ISPs/CDNs/broadcasters/distributed infrastructure through smart-contract settlement. It is relevant as a **network-capacity market** but is not yet counted here as a proven small-provider cash-flow path without stronger current supplier economics.
- Bandwidth.com reseller APIs/partner program are a build-a-service resale channel, not a marketplace paying owners for spare home/server bandwidth.
- No new top-level CPU/storage/bandwidth earning mechanism emerged from this control pass.

---

## 13. Saturation assessment after Run 040

### New top-level economic mechanisms
**0**

### New material independent provider implementations
At least **6 current material implementations** plus **2 restricted/watchlist names**.

### Interpretation
Taxonomy convergence is extremely strong, but provider/project-level saturation is still not sufficient for a final completion claim. A second supplier-tail pass produced several significant current platforms with explicit supplier economics, including Inpherio, UsePod, HZ AI and KeyMart.

Therefore **do not proceed directly to final completion**. One more supplier-tail convergence pass is required before the broad final control pass.

## Next run
**Run 041 — third supplier-tail convergence + authenticity/dedup pass.**

Priority:
1. Verify Inpherio geography/KYC/Azerbaijan feasibility and any current live-grid activity evidence.
2. Verify UsePod provider enrollment requirements, geography/KYC, withdrawal limits and production activity.
3. Verify HZ AI platform fee, Stripe/provider geography and real marketplace activity.
4. Verify KeyMart legal/company identity, provider settlement rail/geography and live activity claims.
5. Verify SpotNode commercial terms or keep restricted.
6. Validate Exascale/Hyperlink and ClusterBid externally enough to distinguish live commercial exchanges from early marketing surfaces.
7. Search exact neighbors using the newly productive terms: `inference marketplace provider agent`, `sell model endpoint`, `API key resale authorized`, `GPU execution exchange`, `idle inference provider`, `compute liquidity layer`, `capacity seller API`, `provider earnings inference`.
8. Re-run non-GPU analogs once more.

### Gate after Run 041
Only if Run 041 yields **no or negligible new viable independent provider projects** should the next run become the final all-category saturation/control pass.
