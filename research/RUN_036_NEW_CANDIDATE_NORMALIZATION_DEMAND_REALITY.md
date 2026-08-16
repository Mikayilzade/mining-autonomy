# Run 036 — New-candidate normalization + demand reality pass

Date: 2026-08-16
Status: **completed**
Project state after run: **IN PROGRESS**

## Goal
Normalize the strongest Run-035 discoveries, test whether they expose real autonomous supplier economics rather than only protocol claims, inspect observable demand, and search exact-neighbor provider markets.

## Result
Taxonomy remains saturated: **0 new top-level economic mechanisms**.

Project-level saturation remains incomplete. This run materially strengthened **Open Cloud**, **the402**, **Cocoon**, and **Evernode**, kept **ALPENGLOW** on a high-risk watchlist, and added two fresh independent implementation leads: **Atlora** and **Aeterna**.

The completion gate remains open because exact-neighbor searches still produce new provider implementations.

---

## 1. Open Cloud — strengthened to high-priority curated server-native candidate

Classification: `VERIFIED / CURATED SERVER-NATIVE / HIGH PRIORITY`.

Current official provider material establishes three supply modes:
1. dedicated hardware;
2. cloud-backed templates that auto-provision AWS/GCP/Azure instances on demand;
3. shared hosting engines.

### Provider economics
Official pricing/provider pages now expose materially useful economics:
- **0% Open Cloud fee** on dedicated nodes;
- **0% Open Cloud fee** on cloud-backed nodes;
- cloud-backed providers **set markup over AWS/GCP/Azure spot rates**;
- **4% marketplace fee** on shared-hosting revenue;
- monthly USD settlement or continuous cycle redemption.

Open Cloud also publishes market-observed per-node ranges rather than only marketing language. Example observed ranges include roughly:
- Nano 2 vCPU / 8 GiB in US: ~$40–41/month;
- Standard 8 vCPU / 32 GiB: ~€/$95–105 in Hetzner EU vs about $350 in EU hyperscalers;
- Performance 16 vCPU / 64 GiB: ~$185–195 Hetzner EU, ~$588–675 US/EU hyperscaler;
- High-performance 32 vCPU / 128 GiB: ~$375 Hetzner EU vs ~$1,200–1,325 US/EU hyperscaler.

These are guide ranges, not guaranteed revenue.

### Provider admission
Still curated:
- KYC;
- legal-entity review;
- insurance review;
- data-center agreements;
- operations runbooks;
- onboarding typically 2–3 weeks / up to ~10 business days stated on current page.

This significantly lowers fit for a hobbyist VPS-only deployment but improves credibility as a real infrastructure business.

### Automation
Potential `5/5` after onboarding: provisioning webhook can instantiate cloud capacity automatically when customers select an offering.

### Net economics
`Net = customer node revenue - upstream cloud/colo cost - egress - insurance/legal overhead - support/SLA cost - taxes - failed/provisioned-idle capacity`

Critical unknown remains **actual customer utilization / selection rate by provider and SKU**. Published guide prices prove a market/pricing surface, not guaranteed node occupancy.

### Geography
No Azerbaijan-specific provider eligibility statement found. Because provider onboarding evaluates a legal entity and operating agreements, Azerbaijan eligibility remains a pre-CAPEX application question.

---

## 2. the402 — strengthened by live-catalog and job-history surface

Classification: `VERIFIED / SERVER-NATIVE SERVICE + BUILD-ONCE / HIGH PRIORITY`.

Official docs continue to explicitly permit AI agents as providers and fully autonomous fulfillment through webhook workers.

### Demand reality evidence
The public catalog is live and currently reports **107 services** on the indexed catalog page checked in this run. Catalog objects expose:
- provider completed-job counts;
- completion rate;
- reputation/confidence;
- service-level/provider-level history.

This is better evidence than a static launch page because the marketplace exposes job-history fields and a live purchasable catalog. It is still not enough to infer total independent demand or profitability without sampling many providers and completed-job distributions.

### Provider economics clarified
Official provider docs state:
- registration can be automated;
- provider webhook receives jobs;
- automated services auto-verify;
- settlement is USDC on Base;
- service listings can be Data API, Automated Service, Human Service, Subscription or Digital Product;
- bidding agents can subscribe to new requests and bid automatically;
- identity verification raises bid caps; unverified providers face lower request-budget caps;
- platform fee is documented as 5%, though current public pages differ in whether that fee is shown as buyer-added or provider-deducted. Model conservatively as 5% platform take until a real test transaction resolves display/accounting semantics.

### Best low-variable-cost service families
Most attractive theoretical families remain deterministic services with near-zero marginal cost:
- DNS / TLS / HTTP header checks;
- structured JSON/data transforms;
- checksum / encoding / compression transforms;
- public metadata extraction where lawful and ToS-compliant;
- static file/code linting;
- image/file conversion with bounded compute;
- simple document normalization;
- cached/public-data lookup;
- orchestrated composite services only when upstream licensing permits resale.

Avoid building economics around expensive third-party LLM/API calls unless price spread is proven.

### Demand caution
A live marketplace does not prove enough external buyer volume. Next economics phase should use catalog history to estimate:
- distribution of completed jobs per provider;
- fraction of providers with nonzero history;
- price × completed jobs by service type;
- new-vs-established provider concentration.

---

## 3. x402.jobs — mechanism credible, demand claims remain first-party

Classification: `VERIFIED SURFACE / BUILD-ONCE / ECONOMICS UNPROVEN`.

Current site exposes:
- workflow composer;
- resource chaining;
- creator markup;
- publish-as-endpoint;
- webhook/schedule triggers;
- dashboard earnings/calls;
- public headline metrics around total volume, jobs run, resources and public jobs.

Observed headline values in this run were approximately:
- **$141k total volume**;
- **46.1k jobs run**;
- **2.2k resources**;
- **80 public jobs**.

These remain first-party site metrics. Treat them as discovery evidence, not audited revenue.

Economic mechanism remains service-composition margin:
`Net/run = markup - component-call cost drift - failed-call/refund cost - platform/settlement fees - hosting cost`

No new top-level mechanism.

---

## 4. Cocoon — upgraded from vague watchlist to technically actionable restricted GPU provider

Classification: `VERIFIED TECHNICAL PATH / RESTRICTED HARDWARE / DEMAND UNPROVEN`.

Official Cocoon documentation now establishes a concrete production-style worker path rather than only a provider application page.

### Hardware / software requirements
Current docs specify:
- Linux 6.16+ for full TDX support;
- Intel TDX-capable CPU;
- NVIDIA confidential-computing GPU, **H100+**;
- QEMU 10.1+;
- owner TON wallet;
- Hugging Face token;
- worker configuration and released worker distribution.

A secondary project page gives representative server requirements around H100/H200, 80GB+ VRAM and 128GB+ RAM; primary cocoon.org docs should take precedence over secondary calculators.

### Operation
Worker:
- registers/operates against Cocoon contracts;
- serves an assigned model;
- exposes monitoring/statistics;
- may run multiple worker instances;
- receives TON to configured owner address.

The protocol has an explicit client → proxy → worker architecture and payment settlement on TON.

### Economics
No reliable current network-wide provider rate or utilization dataset was established from primary docs.

Secondary public calculators advertise example monthly TON values, but these must **not** be treated as evidence of realized returns.

Net formula:
`Net = TON received from paid inference - H100/H200 server rental/depreciation - electricity - bandwidth - TDX/ops overhead - token conversion costs - idle capacity`

Cloud resale remains uncertain because confidential-compute hardware + TDX + GPU passthrough requirements significantly constrain ordinary VPS use.

---

## 5. ALPENGLOW — remain WATCHLIST / high claim risk

Classification: `WATCHLIST / HIGH CLAIM-RISK`.

The project site continues to claim:
- idle GPU background node;
- per-inference-second earnings;
- 70% of inference fees to GPU provider;
- x402/USDC settlement;
- consumer and enterprise GPU participation;
- ALPEN token emissions.

However, this run still did not establish a trustworthy independent production node repository, verifiable provider payout history, audited active workload statistics, or stable provider Terms matching the marketing claims.

The site includes sample/example receipts and tokenomics, but sample proof is not demand proof.

Do not promote above WATCHLIST until source code/binaries/contracts and actual independent payouts can be tied together.

---

## 6. Evernode — NEWLY NORMALIZED strong server-native host candidate

Classification: `VERIFIED / SERVER-NATIVE HOSTING + CAPITAL COLLATERAL / HIGH PRIORITY`.

Evernode was previously only referenced indirectly through Everagents. It is now normalized as its own supplier mechanism.

### What gets paid for
A Linux host leases isolated smart-contract hosting slots to tenants and earns **EVR**.

Host management software (Sashimono) automates:
- registration;
- lease offers;
- tenant deployment/hosting;
- heartbeats;
- ongoing host operations.

### Server compatibility
Official docs say anyone can run a compatible Ubuntu Linux server. This can be a real or virtual machine and is therefore much closer to ordinary VPS/server-native participation than H100-class GPU networks.

Current requirements include roughly:
- Ubuntu 20.04 or 24.04 64-bit;
- domain name/public connectivity/SSL;
- per contract instance ~1 CPU core, 1 GB RAM, 2 GB disk;
- at least three instances for reward/reputation eligibility, implying ~4 cores/4 GB RAM/8 GB free disk guidance.

### Initial capital / collateral
Current docs require:
- **500 EVR** registration fee/deposit;
- sufficient XAH reserves and transaction-cost balance;
- example 10-instance host roughly 8 XAH for reserves + about one month transaction coverage under current assumptions.

Voluntary deregistration returns only half of the outstanding registration deposit, so the EVR registration amount is not risk-free liquid collateral.

### Two revenue components
1. **Lease revenue** — tenants pay EVR for hosting slots; host chooses lease price.
2. **Host reward emissions** — eligible/reputable hosts receive protocol rewards according to the epoch schedule.

This is important: Evernode should not be modeled as pure tenant-demand revenue because protocol emissions can materially contribute to gross return.

### Reputation / eligibility
Reward eligibility requires reputation around/above the documented threshold and operational conditions including:
- sufficient instance count;
- offered leases;
- acceptable lease pricing relative to network reward distribution;
- reputation participation;
- heartbeat/availability.

### Economics
`Net = tenant lease EVR + host emission EVR - VPS cost - XAH transaction fees - EVR registration opportunity/loss risk - domain/ops - token conversion/liquidity risk`

Evernode is one of the cleaner candidates for a small Linux VPS experiment later because hardware floor is modest and the earning daemon is explicitly server-native. Profit still depends on EVR value, host count, reward epoch, lease demand, and VPS cost.

### Geography / compliance
Official docs say installations from sanctioned entities are disallowed. No Azerbaijan-specific exclusion was found in this pass; legal/license review remains required before deployment.

---

## 7. Atlora — NEW inference marketplace lead

Classification: `UNVERIFIED / WATCHLIST`.

Atlora currently markets itself as a marketplace to **buy and sell computing power for LLM inference** and exposes a customer-side API surface.

However, the visible site is still waitlist-oriented and this run did not establish:
- open provider onboarding;
- supplier payout formula;
- production utilization;
- withdrawal/KYC/geography;
- server/GPU requirements.

It is a fresh independent implementation but not yet a deployable earning candidate.

---

## 8. Aeterna — NEW autonomous-agent marketplace lead

Classification: `UNVERIFIED / WATCHLIST / HIGH MARKETING-RISK`.

Aeterna claims:
- compute contribution income;
- AI-service economy;
- autonomous agents selling services 24/7;
- x402 micropayments;
- agent marketplace.

This matches the project semantically but current evidence is mainly broad first-party marketing. No strong current provider economics, job history, contracts or established payout data were found.

Keep as discovery lead only; do not count toward viable deployment set yet.

---

## 9. Exact-neighbor pass result

Queries around:
- agent provider webhook earn USDC;
- autonomous service marketplace USDC;
- AI inference provider paid per request;
- cloud-backed compute provider marketplace;
- confidential GPU provider earn;
- server host reward lease marketplace

produced **no new economic mechanism**, but did produce new independent implementation leads (Atlora, Aeterna) and a previously under-normalized strong candidate (Evernode).

Therefore project-level saturation is **not complete**.

---

## Demand/economics ranking after Run 036

### Strongest server-native theoretical matches to investigate later
1. **the402 automated provider webhook** — closest literal fit to autonomous simple-task bot; demand needs quantified.
2. **Evernode host** — modest Linux server requirements; explicit leases + protocol rewards; token economics required.
3. **Open Cloud cloud-backed provider** — strongest real cloud-resale model but high onboarding/business overhead.
4. **Singularity Compute** — managed/provider model strong but 50k SGL stake + utilization uncertainty.
5. **Cocoon** — technically real but H100+/TDX hardware makes it capital-heavy and not normal-VPS friendly.
6. **x402.jobs** — build-once orchestration margin; demand and first-party metrics need audit.

### Watchlist only
- ALPENGLOW
- Atlora
- Aeterna
- OpenGradient supplier path
- AgentX Nexus Grid

---

## Saturation metrics
- Deliberate control/tail passes completed after this run: **19** (Runs 018–036)
- New top-level mechanisms: **0**
- Newly normalized strong independent project: **Evernode**
- Fresh independent implementation leads: **Atlora, Aeterna**
- Existing candidates materially strengthened: **Open Cloud, the402, Cocoon**

## Conclusion
**IN PROGRESS.**

Run 036 failed the completion gate because project-level discovery still produces fresh implementations and because the newly normalized Evernode branch deserves its own neighbor/economics search.

## Next run
Run 037 should be an **exact-neighbor/provider-tail control + measurable economics pass**:
1. quantify Evernode current host count, reward epoch/quota, average reward per eligible host, EVR/XAH liquidity and cheap-VPS break-even;
2. sample the402 catalog/provider completed-job distribution and identify services with real nonzero histories;
3. inspect Open Cloud provider handbook/terms and whether small/new legal entities can realistically qualify;
4. investigate Atlora provider-side docs/repository/waitlist status;
5. investigate Aeterna contracts/docs/network status and reject if only marketing/points;
6. search neighbors around Evernode/HotPocket decentralized application hosting, autonomous paid webhooks, x402 providers, cloud-resale marketplaces and low-end CPU/VPS marketplaces.

If Run 037 yields no material new current provider projects, perform one further provider-tail control before moving to the final all-category saturation pass.
