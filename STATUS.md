# Status

Project state: **IN PROGRESS**

Last completed run: **Run 018 — broad saturation/control pass #1**
Last updated: **2026-08-15**

## Completed research runs
- Run 001 — initial universe / structure.
- Run 002 — server-native expansion.
- Run 003 — RPC / ZK / keepers / solvers.
- Run 004 — relayer / intent / prover expansion.
- Run 005 — compute / storage expansion.
- Run 006 — compute / storage / relay completion.
- Run 007 — decentralized AI / Bittensor.
- Run 008 — residential / device bandwidth.
- Run 009 — physical DePIN.
- Run 010 — capital-yield universe.
- Run 011 — build-once digital income.
- Run 012 — automated task / API / job markets.
- Run 013 — marketplace / royalty / distribution gaps.
- Run 014 — proof-of-work / mining / hashpower normalization.
- Run 015 — scam/dead/misleading-opportunity cross-check.
- Run 016 — profitability/deployment economics normalization.
- Run 017 — Azerbaijan/KYC/payout/geography filtering.
- Run 018 — broad saturation/control pass #1.

Run-specific files under `research/` are the durable detailed record. Latest:
- `research/RUN_018_BROAD_SATURATION_CONTROL_1.md`
- `research/SOURCES_RUN_018.md`

## Current validated server-native / highly autonomous highlights
- Compute/GPU: Golem provider; Akash provider; Vast.ai host; Nosana/Golem GPU providers; io.net Supplier; Clore.ai Host; TensorDock Host; Runpod Community Cloud Host; NodeOps Cloud Compute Provider.
- Media/storage: Livepeer Orchestrator; Filecoin, Sia, Storj, ScPrime; Swarm Bee; Autonomi Node; Arweave Miner; CESS Storage Node.
- Relay/network: Mysterium datacenter/VPS relay; EarnFM Fleetshare supplier; Pocket Network Supplier; Lava RPC Provider; Streamr Operator; SQD worker; Diode Relay Node; CESS CD2N Retriever/Cacher.
- Index/proof/solver: The Graph Indexer; Aztec Prover; Boundless/RISC Zero proving; Succinct/SP1 prover; Cysic prover; Across relayer; UniswapX filler; Presearch node; SubQuery Indexer/RPC Provider.
- AI incentive networks: selected Bittensor subnets/roles, Omron, Chutes, Nous/Macrocosmos variants, Allora workers/reputers and related competitive compute/agent roles documented in prior run files.
- Machine-service monetization: Apify paid Actors; RapidAPI providers; GitHub Marketplace paid Apps; AWS/Microsoft/Google cloud marketplace SaaS; Databricks commercial listings; IDLE Protocol pay-per-call GPU/agent/API/data/resource endpoints; NodeOps paid template marketplace.
- Mining/hashpower: owned-hardware PoW pool mining; merged mining; NiceHash-style selling; MiningRigRentals rig seller; explicitly permitted MRR API broker/reseller strategy.
- Supplier bandwidth: EarnFM Fleetshare remains notable because official docs explicitly price residential traffic at $0.10/GB and datacenter traffic at $0.04/GB for accepted suppliers.

## Run 016 — durable economics findings
- **Paid utilization, not uptime, is the dominant hidden variable.** A listed but idle GPU/CPU/disk/IP is not revenue-producing.
- **Owned spare resources have a structural advantage.** Retail cloud arbitrage usually stacks an upstream provider margin underneath a competitive earning market.
- **Opportunity cost must be explicit.** Compare expected net $/GPU-hour, $/CPU-thread-hour, $/TB-month and $/GB across competing markets before deployment.
- **Collateral has financing cost and loss risk even when normally returned.**
- **Small empirical pilots should precede CAPEX.** Measure actual paid utilization first.

Representative normalized economics:
- Vast.ai: host sets GPU/storage/bandwidth prices; earnings depend on occupied rental hours.
- Akash: real provider business with Kubernetes/networking/operations overhead; better suited to infrastructure than trivial VPS arbitrage.
- Golem: low-barrier CPU/GPU provider with GLM pay-per-use; utilization is the bottleneck.
- EarnFM Fleetshare: 20+ IP supplier program; $0.04/GB datacenter / $0.10/GB residential.
- Storj: thin storage rent favors otherwise-idle disk.
- Sia: thin storage rent + collateral favors cheap/sunk storage and reliable uptime.
- Filecoin: infrastructure/mining business with collateral, proving, operational reliability and ≥10 TiB power for WinningPoSt eligibility.

## Run 017 — durable geography/KYC/payout findings
- **Crypto-native provider rails survive the Azerbaijan filter best.** Golem, Storj, Sia, Filecoin and Akash provider roles use wallet/protocol settlement rather than depending on PayPal-style receiving capability.
- **Golem** is currently the cleanest low-capital geography fit: Linux server provider, GLM wallet payout, no ordinary provider KYC or Azerbaijan-specific exclusion found in reviewed provider/payment docs. Fiat off-ramp/tax remains separate.
- **Storj** pays STORJ via Ethereum L1 or optional zkSync L2; current Node Operator Terms use sanctions/export restrictions rather than naming Azerbaijan as excluded. Terms also constrain scaling: one node per IP and common payout-address rules.
- **Sia** uses a host-owned Siacoin wallet and protocol contracts; geography is less of an onboarding bottleneck than hardware/collateral/storage economics.
- **Filecoin** likewise has protocol/FIL economics, but is too infrastructure/collateral/proving-heavy for an early low-capital pilot; Filecoin Plus programs can introduce separate KYC/due-diligence requirements.
- **Akash** remains technically open/wallet-based and exposes provider location as a market attribute; current provider/audit overhead makes it a later experiment.
- **Vast.ai** remains viable but Azerbaijan payout needs a live onboarding check. Vast references PayPal/Wise/Stripe and other payment integrations, while PayPal's own official country table says Azerbaijan accounts cannot receive payments. Wise can deliver to Azerbaijani local bank accounts, but Vast-specific use of that route is not proven.
- **EarnFM Fleetshare** requires supplier approval, 20+ IPs, Didit KYC/KYB and agreement. Standard payout has a $15 minimum; >$300/month invoice bank transfer is documented as SEPA/ACH, so Azerbaijan-specific standard payout availability still needs portal confirmation.
- Geography is also an economics variable: EarnFM explicitly says traffic depends on IP geography/reputation; compute-provider location can affect matching/latency even when account creation is allowed.

### Later low-capital experiment priority after research saturation
1. Golem on an already-paid server.
2. Storj on already-owned unused disk/bandwidth.
3. Sia where spare multi-TB storage already exists.
4. EarnFM Fleetshare only after Azerbaijan KYC/payout confirmation and economically sourced eligible controlled IPs.
5. Vast.ai only with existing GPU hardware and a confirmed Azerbaijan host-payout route.
6. Akash as a later infrastructure/provider pilot.
7. Filecoin only as a dedicated infrastructure-business case.

This is **not** yet an implementation decision; research remains theoretical.

## Run 018 — saturation/control findings
- Broad alternate-term searches produced **0 new top-level economic classes**, but multiple genuinely new or materially upgraded projects, so saturation is not reached.
- **IDLE Protocol** is a particularly close match to the original “server does tiny jobs forever” concept: arbitrary GPU/agent/API/data resources can become metered endpoints; official docs state 85% provider share, USDC/Solana settlement and pay-per-call economics. Demand still needs empirical validation.
- **NodeOps Cloud Marketplace** explicitly supports VM providers/resellers, including an official GCP path. Current provider entry requires 2,000 NODE + 200 NODE/CU bond and strict machine requirements. This is a rare explicit retail-cloud-resale lead worth later economics testing.
- **NodeOps Templates** add a separate build-once revenue stream; official docs currently state 20% of workload fees during bootstrap for accepted public templates.
- **SubQuery** concretely validates server-native paid RPC/indexing supply with productive-work + inflation rewards, but current registration needs 200,000 SQT stake and carries service/slashing risk.
- **Diode** validates a lightweight Linux/VM relay node whose rewards depend on routed bandwidth and Fleet Contract economics.
- **CESS** adds both storage mining and a distinct CD2N retrieval/cache role; storage entry currently requires at least 1 TiB and 2,000 CESS/TiB stake.
- **Acurast** validates autonomous smartphone compute but remains Tier B/device-only, not a normal VPS path.
- Directory sweep produced a substantial primary-source validation queue: Impossible Cloud Network, Fleek, Spheron, StorX, OORTech, Fluence, iExec, Edge/XE, dTelecom, YOM and related leads.

## Important restricted/watchlist findings carried forward
- Lagrange: paid/slashable prover economics but public production admission not clearly self-service.
- Hyperbolic: external GPU providers exist; public supplier onboarding/payout unresolved.
- Meson/Crust/selected oracle, executor and solver roles: mechanism exists but current admission/economics need normalization.
- CoW solver, 1inch Fusion resolver, Gevulot/zkCloud: legitimate but constrained/onboarding-dependent.
- Macrocosmos Data Universe: data-source legality/ToS can constrain implementation.
- Gensyn RL Swarm and inference.net/Kuzco: production reward path not yet established.
- AWS Data Exchange and Snowflake paid-provider eligibility have Azerbaijan-specific limitations recorded in prior runs.
- Hugging Face Inference Provider: real economics but curated/integration-heavy.
- OpenAI GPT direct monetization: not a general builder-income rail in the prior validation pass.

## Current phase
**Phase 1 universe construction is broad and high-priority economics/geography are normalized, but research is NOT saturated.**

Saturation/control passes completed: **1 broad pass**.
Completion confidence: **medium**. Taxonomy stability is improving, but the first control pass still produced several strong new projects inside existing mechanisms.

## Next run priority
**Run 019 — niche saturation/control pass #2.**

Validate strongest directory-only server-native leads with primary sources:
- Impossible Cloud Network;
- Fleek;
- Spheron;
- StorX;
- OORTech;
- Fluence;
- iExec;
- Edge/XE;
- dTelecom;
- YOM.

Use alternate role vocabulary:
- worker / miner / provider / edge node / executor / processor / host / resource seller;
- infrastructure supplier / compute seller / bandwidth seller / cache operator;
- “earn”, “provider”, “host”, “supply”, “operator”, “rewards”, “mainnet” inside ecosystem docs.

Track:
1. new independent economic mechanisms;
2. new viable projects inside existing mechanisms;
3. duplicates / renamed projects;
4. restricted/dead/rejected rediscoveries;
5. net-new viable count by query family.

If Run 019 still produces material net-new server-native projects, schedule another differently-worded control pass before considering completion.

## Completion gate
Do **not** mark complete until multiple differently-worded broad + niche control passes add no new independent earning mechanisms and almost no new viable projects. Remaining unknowns must be explicitly documented rather than guessed.