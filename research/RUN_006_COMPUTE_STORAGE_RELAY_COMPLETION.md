# Run 006 — Compute / Storage / Relay Completion Pass

Date: 2026-08-15
Status: **completed**
Phase: Universe construction

## Goal
Finish the unresolved compute/storage/relay queue before the dedicated decentralized-AI/Bittensor sweep. This run prioritizes whether a **current paid supply-side role exists**, whether it can be operated autonomously, and whether normal server/bare-metal operation is actually supported.

## Strong additions / confirmations

### 1. TensorDock Host — VERIFIED, SERVER-NATIVE, automation 5
Official TensorDock material still describes the platform as a marketplace aggregating a global network of hosts, explicitly says hosts monetize their servers, and the live deployment UI says users can become a host. Current marketplace copy says hosts are vetted for hardware, technical knowledge and communication and must meet a 99.99% uptime standard; the service spans 100+ locations and includes both GPU and CPU cloud capacity.

Economic model: customer-paid VM/GPU/CPU rental. Host revenue is therefore utilization-dependent rather than a guaranteed token emission. Admission is **not permissionless**: TensorDock vets hosts and the operational bar is datacenter-like.

Classification: strong server-native marketplace, but likely most relevant to existing reliable server operators rather than a cheap generic VPS bot.

### 2. Runpod Community Cloud Host — VERIFIED, SERVER-NATIVE/HARDWARE, automation 5
Current Runpod Terms explicitly define Community Cloud as peer-to-peer GPU computing connecting individual compute providers (Hosts) with consumers. Current pricing still exposes a Community Cloud tier. This confirms the host role remains part of the current product, although detailed new-host onboarding and host payout percentages were not located in this pass.

Separate new earning mechanism discovered: **Runpod Hub revenue sharing**. Since September 2025, repositories published to Runpod Hub can earn up to 7% of compute revenue generated when users deploy them, paid as Runpod credit. This is a BUILD-ONCE digital/infrastructure asset rather than raw compute supply and should be revisited in that later pass.

### 3. Render Node Operator — VERIFIED but RESTRICTED onboarding, hardware-native, automation 4-5
Current official docs still pay node operators for rendering work in RENDER. New operators must submit an interest form and enter an onboarding queue. Current Render Compute Network waitlist requires an application plus benchmark/speed test and calls for existing hardware; stated requirements include an approved GPU at least around RTX 3050 class, 64 GB+ RAM, 2 TB+ SSD, Linux, Docker/NVIDIA tooling and 100/75 Mbps network. Render explicitly advises against buying new hardware solely for entry.

Conclusion: legitimate autonomous GPU work, but not an open arbitrary-cloud-server marketplace. Keep as RESTRICTED rather than permissionless server-native.

### 4. Arweave Miner — VERIFIED, SERVER/BARE-METAL, automation 5
Current Arweave docs still provide a mining guide and identify solo miner, coordinated miner, pool miner, VDF server and validator node types. Mining combines proof-of-work-like competition with proof of historical data access; the storage dataset is divided into 3.6 TB partitions and uniquely packed per miner. Current docs state block rewards are reserved and released after roughly 30 days, with slashing/revocation risk for prohibited fork/double-sign behavior.

This is not a cheap VPS daemon: meaningful participation is storage-capacity and system-performance intensive, and miners must consider the legal implications of storing arbitrary network data.

### 5. ScPrime Storage Provider — VERIFIED, storage market, automation 5
Current official docs still support DIY Storage Providers using a PC, NAS or server. Providers set storage/bandwidth/collateral parameters and earn rent from storage contracts. Current recommended storage target is about $4/TB/month in SCP and provider collateral is required. A current incentive page states the earlier broad provider incentive program formally ended in August 2025, so **base contract rent must be modeled separately from any temporary or selective incentive layer**.

Important constraint discovered: the post-announce guide says a provider does not receive ScPrime-source data without a license. This means the protocol may be permissionless at the host layer but material demand flow can be license-dependent. Classify VERIFIED + RESTRICTED economics.

### 6. Autonomi Node — VERIFIED, low-spec/headless/virtual compatible, automation 5
Current official docs state node operators receive Autonomi tokens based on storage/retrieval contribution and performance. FAQ says nodes cost nothing to start, each uses roughly 35 GB storage plus CPU/RAM/bandwidth, and advanced operators can use headless computers, home servers or virtual environments. Network economics state uploaders make payments that fund node operators.

This is one of the closest matches yet to the original "cheap autonomous daemon" concept: low resource requirement, virtual/headless support and reward path are all explicitly documented. Actual expected revenue and token liquidity still require later profitability normalization.

## Restricted / unresolved

### Lagrange ZK Prover Network — RESTRICTED / institutional operator path
Lagrange's current site still describes the ZK Prover Network as live on EigenLayer with 85+ operators. Official architecture material confirms provers receive rewards for valid proofs delivered on time, while missed obligations can cause non-payment/slashing and work capacity is tied to restaked collateral. However, current public material highlights institutional operators and a sign-up/onboarding path rather than a clearly open self-serve production prover flow.

Conclusion: real paid server-native proving mechanism, but keep RESTRICTED until current operator admission, collateral thresholds and hardware sizes are normalized.

### Hyperbolic provider supply — WATCHLIST / verified supply aggregation, open admission unproven
Hyperbolic's June 2026 Forge article explicitly states it aggregates heterogeneous GPU supply from providers around the world and normalizes machine lifecycle/provisioning. The current marketplace sells VMs/bare metal and GPU clusters. That proves an external supply side exists, but this pass did not locate a public self-service "become a provider" onboarding/payout document. Keep WATCHLIST, not yet a user-deployable earning option.

### Meson Network bandwidth/CDN mining — WATCHLIST
Current Meson.Network public site still presents an infrastructure marketplace and a 2025 mainnet roadmap, and legacy official/community material describes MSN rewards to miners providing server resources. However, this pass could not find sufficiently current primary documentation proving production node onboarding, current reward rates, stake, payout and server eligibility. Do not promote beyond WATCHLIST yet.

### Crust Network merchant/storage roles — WATCHLIST / protocol evidence exists, current operator path unclear
Current Crust chain documentation exposes storage-market merchant ledgers, collateral, storage orders and merchant reward calls/events, proving the economic mechanism exists at protocol level. This pass did not find a clear current operator deployment/onboarding guide for a new storage provider. Keep WATCHLIST pending stronger operational evidence.

### Salad supplier environment — VERIFIED home/distributed compute, not generic server supply
Current SaladCloud docs say its distributed compute supply is primarily privately owned gaming PCs and describes owners contributing idle GPUs for rewards. Salad is therefore a strong Tier B home/device compute option but should **not** be treated as a generic VPS/datacenter-host marketplace unless a separate supplier program explicitly permits that environment. An interesting second-order strategy was found: SaladCloud itself documents deploying an inference.net/Kuzco worker on rented SaladCloud GPU capacity, meaning one can run a reward network worker on cloud compute; this must later be modeled strictly as `worker rewards - SaladCloud rental cost` and not assumed profitable.

## New mechanism discovered this run

### Compute-template/repository revenue share
Runpod Hub introduced an economically distinct BUILD-ONCE model: publish a reusable deployment repository/template, then earn a percentage of downstream compute spend. This is not hardware mining and belongs in the later automated digital-asset pass. It is especially relevant because operation after publication can be nearly passive and serverless from the creator's perspective.

## Taxonomy refinements
1. GPU marketplaces split into **open marketplace host**, **vetted provider**, **application/waitlist node operator**, and **aggregated private supplier** models.
2. Storage networks must separate base customer rent from temporary emissions/incentive subsidies.
3. "Virtual environment supported" is strong evidence for server compatibility (Autonomi); "Linux client exists" alone is not.
4. A network can be technically permissionless while economically important demand is gated by a license or curated buyer channel (ScPrime).
5. Renting compute to run another reward worker is a distinct arbitrage strategy and must be tested with net economics, not catalogued as free mining.
6. Build-once compute templates/repositories create a new passive digital-income family separate from supplying compute itself.

## What remains before moving on
The compute/storage/relay universe is now broad enough for the next phase, but several watchlist items still need later targeted rechecks: Meson, Hyperbolic open supplier onboarding, Crust current provider workflow, and Lagrange production operator admission. These do not block moving to the dedicated AI-incentive discovery pass because their economic families are already represented.

## Completion assessment
Project remains **IN PROGRESS**.

Saturation/control passes completed: 0.
Discovery is still productive because this run added/strengthened multiple current earning roles and revealed a distinct Runpod repository revenue-share family.

## Next run
Run 007 — dedicated decentralized AI / Bittensor / inference / training / model-contribution reward sweep. Include Bittensor subnet miner families, inference.net/Kuzco, AI worker networks, distributed training/inference, model/data contribution markets, and explicit dead/restricted cross-checks.