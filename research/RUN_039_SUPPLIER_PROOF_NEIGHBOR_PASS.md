# Run 039 — Supplier-proof + newly discovered neighbor pass

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Objective
Validate unresolved supplier economics and onboarding around Lilac and ResonTech; search exact neighbors revealed by Run 038 (idle-GPU/Kubernetes operators, HPC/Slurm capacity sellers, inference revenue-share markets, reserved-capacity resale); re-check the402 demand evidence; decide whether provider-level discovery has converged enough for a final all-category saturation pass.

## Result
The completion gate is **not met**. Taxonomy remains saturated — **0 new top-level economic mechanisms** — but this run found at least **three independent supplier/provider implementations** that were not present in the durable Run-038 checkpoint:

1. **Keld** — live enterprise inference marketplace with an explicit provider side for monetizing idle inference capacity.
2. **hosted.ai GPU Mesh** — wholesale GPU-capacity sharing network where infrastructure owners publish GPU pools and are paid for consumption; also supports buy-and-resell.
3. **Fluxenta** — coming-soon agent-first inference marketplace that explicitly intends to let providers sell idle GPU/CPU capacity via secure tunnel and token settlement; not deployable yet.

Provider-tail discovery is therefore still producing fresh projects and completion remains premature.

---

## 1. Lilac — strong supplier economics confirmed; geography still unresolved

Current official supplier documentation continues to establish a unusually concrete supplier model:
- supplier receives **70%** of workload revenue;
- Lilac keeps 30%;
- payout formula is usage/token based;
- monthly supplier reporting;
- monthly payout by **wire transfer or ACH**;
- revenue depends on GPU availability, routed demand and model pricing.

The public provider page confirms supplier onboarding is via demo/waitlist and the intended supply is existing Kubernetes GPU infrastructure rather than a normal cheap VPS. Public product pages show active inference and batch products and current customer-side pricing.

### Unresolved after this pass
No public primary source located in this run specified:
- supported supplier countries;
- Azerbaijan eligibility;
- legal-entity requirement;
- exact KYC/compliance package;
- a public minimum cluster size;
- public distribution of supplier utilization or payouts.

### Classification
`VERIFIED / RESTRICTED`

### Economics
`Supplier gross = billable workload revenue × 70%`

`Net = supplier gross - incremental electricity - cooling - bandwidth - hardware depreciation attributable to Lilac jobs - operations - tax/bank fees`

Utilization remains the dominant unknown. The strongest use case is already-owned idle capacity, not new GPU CAPEX justified by the 70% share alone.

---

## 2. ResonTech — supplier path technically stronger; commercial proof still insufficient

Current official infrastructure material explicitly describes a supplier program:
- HPC operators, datacenter owners and teams with reserved cloud capacity can register clusters;
- supplier provides cluster specs, location, scheduler and availability windows;
- supported scheduler styles include **Slurm / Kubernetes / bare metal**;
- one-line node agent joins the routing layer;
- jobs/inference replicas route automatically when matched;
- dashboard shows utilization and job history;
- supplier language says operators **earn from utilization** without negotiating contracts.

The public page says the intended supplier profile is professional clusters, specifically **8+ GPUs** with fast intra-cluster networking. Hardware table separately shows lower technical minimums, but those should not be interpreted as proof that a single consumer GPU is commercially accepted.

### Still missing
This run still found no public primary-source statement of:
- provider payout rail;
- marketplace fee / revenue share;
- settlement currency;
- minimum payout;
- supported supplier countries;
- Azerbaijan eligibility;
- KYC/entity requirements;
- independent supplier utilization/payout distribution.

### Classification
`WATCHLIST / RESTRICTED`

Do not model profitability until settlement terms are known.

---

## 3. Keld — NEW material provider implementation

Keld is a live enterprise marketplace for AI inference. Its current official site and July-2026 launch material describe a two-sided market in which enterprise jobs are matched to independent model providers according to price, deadline, quality and policy constraints.

Provider-side evidence is explicit:
- model providers can bring models/capacity to market;
- Keld Trade is the provider interface for listing spare capacity and managing orders;
- micro-batching feeds matched jobs into provider fleets at a pace intended to fill otherwise-idle headroom;
- Keld says providers can monetize capacity they already own and that jobs clear into billable revenue;
- provider supply is at the **inference-output/token level**, not raw GPU-hour rental;
- the company says the marketplace is live and matches across 100+ providers, although its public subprocessor page still does not name individual inference providers.

### Classification
- Category: paid AI inference / model-service marketplace
- Type: SERVER/BUSINESS-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation potential: 5/5 once provider integration is established
- Resource: inference fleet/model endpoint/GPU capacity
- Cheap normal VPS: generally no, unless the sold model/service is CPU-capable and accepted
- Payout/settlement details: not established in accessible public material during this run
- Supplier geography/KYC/entity: unresolved
- Azerbaijan feasibility: unresolved

### Materiality
Keld is a genuinely independent implementation of the same broad mechanism as Lilac, but the economic unit differs: Keld markets inference outcomes/tokens through a market rather than renting raw hardware. This is strongly aligned with the target of autonomous machine work.

### Economics
`Net = cleared inference revenue - model-serving compute - power/cloud cost - bandwidth - provider integration/operations - marketplace/settlement fees - taxes`

Do not rely on Keld's marketing uplift figures as a forecast for a new supplier. Actual fill rate and provider settlement terms are required.

---

## 4. hosted.ai GPU Mesh — NEW material professional supplier + resale path

hosted.ai's current official GPU Mesh material describes a wholesale capacity-sharing network integrated with its neocloud platform.

Explicit supplier behavior:
- infrastructure owners can **publish GPU pools** to GPU Mesh;
- they are **paid for GPU Mesh consumption**;
- direct sales may continue in parallel, so Mesh is an additional channel rather than exclusive capacity;
- supplier capacity can be monetized without separate sales/marketing work;
- the same platform also allows operators to **buy wholesale GPU pools and resell them** under their own brand;
- buyers pay wholesale only when downstream customers consume capacity;
- hosted.ai provides metering, billing, orchestration and multi-tenant GPU controls.

### Classification
- Category: professional GPU capacity marketplace / wholesale resale
- Type: SERVER/BUSINESS-NATIVE
- Status: `VERIFIED / RESTRICTED`
- Automation: 4–5/5 after business/platform setup
- Resource: owned GPU infrastructure, or business operation reselling supplier pools
- Cheap VPS: no
- Payout amount/fee schedule: not public in material found this run
- Geography/KYC/entity: unresolved and likely business-contract oriented
- Azerbaijan feasibility: unresolved

### Why it matters
This adds a second autonomous strategy beyond simply hosting owned hardware: **zero-hardware-CAPEX neocloud resale** is explicitly offered by the platform. It is not a new top-level mechanism — the economics are still capacity resale/margin — but it is a distinct implementation worth preserving for later modeling.

### Risk
The resale path is not passive money by itself. Customer acquisition, pricing, support, credit risk, tax/compliance and contractual obligations remain business costs unless the platform or another channel supplies demand.

---

## 5. Fluxenta — NEW but pre-production

Fluxenta currently presents a public coming-soon preview of an agent-first inference marketplace.

Intended provider path:
- any provider can advertise locally hosted models;
- secure tunneling connects a provider's inference server without requiring a public IP;
- proxy routes buyer requests across providers by policy/price/latency;
- provider can sell idle GPU/CPU inference;
- headless APIs are intended to allow agents to self-register, advertise capacity and transact;
- settlement is intended through crypto tokens.

The site explicitly labels the product **coming soon** and says provider onboarding starts later. Therefore there is no current deployable income path to count.

### Classification
`WATCHLIST / PRE-PRODUCTION`

### Significance
Not a new mechanism, but a fresh independent provider implementation and strong evidence that the agent-native inference-seller niche is still expanding in 2026.

---

## 6. the402 — stronger public demand/proof surface, but do not infer provider profitability

Current public documentation/catalog now gives more concrete evidence than the prior checkpoint:
- public catalog endpoint is exposed without auth;
- catalog entries include provider completed-job counts, completion rate, reputation and confidence;
- automated services can auto-verify on completion;
- providers can receive jobs through webhooks and autonomous bidding;
- provider earnings endpoint distinguishes settled/held/pending amounts;
- current provider docs say escrow releases funds minus a 5% platform fee, while the public provider marketing page says listed provider price is received and 5% is added to the buyer. This wording conflict remains and live settlement should be treated as authoritative before modeling.
- the public catalog currently exposes over one hundred listings, including automated/data offerings, so the platform is not merely an empty specification.

This is useful **market activity evidence**, but a service listing count is not equivalent to independent paid demand, and the public search surface inspected in this run did not provide a trustworthy marketplace-wide completed-job/revenue total.

### Classification
Remain `VERIFIED / RESTRICTED`, and keep demand validation as a deployment preflight.

---

## 7. Neighbor/control findings that are NOT separate passive-income projects

### Lightning GPU marketplace
Current Lightning documentation aggregates GPU supply across clouds/neoclouds for buyers. Public material inspected here did not establish an open small-provider intake path, so do not add it as a new earning project yet.

### Waldur marketplace + Slurm partitions
Waldur exposes provider-side marketplace APIs and Slurm/GPU partition management. This is infrastructure that an organization can use to operate its own service marketplace; it is not, by itself, a buyer-demand network that pays an arbitrary operator. Classify as enabling software / BUILD-ONCE infrastructure, not a stand-alone passive-income source.

### Cedana
Cedana optimizes/checkpoints/migrates GPU workloads and can improve utilization, but current AWS Marketplace material is customer-side optimization software, not a marketplace that pays the operator. Enabler only.

### Internal quota marketplaces
Recent research on internal ML quota markets shows market mechanisms can improve utilization inside organizations, but internal accounting credits are not external income. Do not count as earning platforms.

---

## 8. Saturation assessment after Run 039

### New top-level mechanisms
**0**

### New material independent provider implementations
**3**
- Keld — live inference marketplace/provider fleet path
- hosted.ai GPU Mesh — GPU capacity supplier + wholesale-resale path
- Fluxenta — explicit agent-first supplier market, but coming soon

### Interpretation
The economic taxonomy has clearly converged, but the exact-provider tail has **not** fully converged. A narrow search still produced multiple independent names, including two current commercial supplier paths. Therefore it would be incorrect to mark the project COMPLETE now.

## Next run
**Run 040 — second supplier-tail convergence pass.**

Priority:
1. Keld: provider onboarding, settlement/payout, fees, geography/entity/KYC, actual public supplier names and demand/fill evidence.
2. hosted.ai GPU Mesh: supplier commercial terms, fees, payout rails, minimum infrastructure/business requirements, geography and Azerbaijan feasibility.
3. Fluxenta: production launch check only; retain pre-production unless provider onboarding and real settlement are live.
4. Search exact neighbors using new vocabulary: inference exchange, model-provider exchange, GPU mesh, wholesale GPU resale, capacity clearing, token-level inference market, micro-batched provider fleet, sovereign GPU supplier, idle-capacity sales channel.
5. Re-run non-GPU analogs of the same pattern: CPU/HPC/storage/bandwidth/API capacity exchanges and reseller networks.
6. If this pass produces no new material independent provider project (only enablers/duplicates/pre-production names), proceed to Run 041 final all-category saturation/control pass.

Do not mark COMPLETE before that convergence + final broad control sequence.