# Run 018 — Broad Saturation / Control Pass #1

Date: 2026-08-15
Status: COMPLETE
Purpose: first deliberate control pass using alternate vocabulary and directories after Runs 001–017.

## Method
Search families deliberately differed from earlier project-name-led discovery:
- machine economy / machine-to-machine earning;
- idle-resource monetization;
- capacity marketplace / compute supplier / VM reseller;
- node operator income;
- provider / supplier / partner programs;
- daemon/service earnings;
- distributed infrastructure rewards;
- DePIN directories as recall amplifiers.

Primary-source validation was then applied to the most promising net-new leads. Directory results were treated only as discovery leads.

## Saturation result
This pass did **not** reach saturation. It found no wholly new top-level economic class, but it produced multiple viable concrete projects/roles that were absent or insufficiently normalized in the durable catalog. Therefore the project remains IN PROGRESS.

### Net-new independent mechanisms
- New top-level mechanism count: **0**.
- New sub-mechanism worth separating: **1** — generalized pay-per-call resource gateway where arbitrary machine resources (GPU, API, agent, data, PC compute) become metered endpoints and provider payout is programmatic. This is economically adjacent to API/job markets, but sufficiently general to track as a separate machine-service marketplace pattern.

### Net-new / materially upgraded viable projects
1. **IDLE Protocol — VERIFIED / high-interest discovery**
   - Category: generalized machine-service / resource marketplace.
   - Value: provider exposes GPU, agent, API, PC compute or data behind a metered gateway.
   - Payout: official docs state provider receives 85% of usage fees; settlement in USDC on Solana; $0.10 minimum.
   - Automation: 5/5 for an already-hosted API/agent/resource; daemon/gateway model.
   - Server-native: **Yes for agent/API resources; likely yes for GPU depending hardware; PC mode is device-oriented.** Official docs explicitly say agent can be hosted anywhere and provide a sample deploy-anywhere flow.
   - Capital: can be near-zero if an API/agent/server already exists; GPU mode requires hardware/hosting.
   - Revenue driver: paid calls, not uptime. No demand means no revenue.
   - Risk/unknowns: platform is new; real external demand and durable payout volume must be empirically verified; ToS/KYC/geography details need a dedicated pass. Do not treat listed active-node counts or suggested prices as profitability proof.
   - Why important: closest current match found to the original concept of an autonomous server exposing small machine jobs and receiving automatic micro-payments.

2. **NodeOps Cloud Marketplace Compute Provider — VERIFIED / high-interest**
   - Category: CPU/VM compute marketplace.
   - Server-native: **Yes.** Official docs explicitly support both owned machines and VMs and provide a GCP VM provider guide. VM resale is explicitly supported.
   - Minimum machine: >=2 vCPU, >=4 GB RAM, >=80 GB NVMe, >=1 Gbps unlimited, >=99% uptime, public static IPv4, Debian 12+ or Ubuntu 22.04+, Linux kernel 6.7+.
   - Bond: official current docs require 2,000 NODE plus 200 NODE per CU, with Arbitrum ETH for gas.
   - Rewards: docs describe up to 10 NODE/day per 2 CU (8 base + up to 2 performance) in the bootstrapping reward model; separate docs state providers also earn a share of CU consumption fees.
   - Automation: 4–5/5 after provisioning, with reliability monitoring.
   - Important constraint: protocol runs at root; provider machine cannot run other workloads, third-party applications/monitoring agents or swap.
   - Economics: unusually relevant because cloud VM resale is explicitly acknowledged; nevertheless retail-cloud cost vs reward/token value and future subsidy decay must be modeled before any deployment.

3. **NodeOps Template Marketplace — VERIFIED / build-once machine income**
   - Category: build-once template/software marketplace.
   - What earns: builder publishes an approved public infrastructure/app template and receives a workload-fee share when users deploy it.
   - Current bootstrap share: official docs state 20% of workload fee for templates during the bootstrapping phase.
   - Automation: 4/5 after template is accepted and maintained.
   - Not raw mining: requires useful template creation and marketplace acceptance/discoverability.
   - Why retain: it bridges Tier A machine infrastructure and Tier D build-once income, and can stack with provider economics without fake activity.

4. **SubQuery Node Operator (Indexer / RPC Provider) — VERIFIED**
   - Category: blockchain data indexing / RPC service market.
   - Value: serve data-index queries and/or RPC requests to consumers.
   - Revenue: current docs state two reward sources: productive work (closed agreements / flex PAYG) and network inflation/stake rewards.
   - Stake: current docs state minimum 200,000 SQT to register as Node Operator; invalid/incomplete service can cause stake reallocation/slashing.
   - RPC reuse: official guide says an existing RPC endpoint used for other purposes can be connected to SubQuery and need not be dedicated.
   - Automation: 5/5 once infrastructure is operational, but monitoring and stake management remain.
   - Server-native: yes.
   - Economics: capital-heavy relative to trivial VPS experiments; profitability must separate customer-paid query revenue from inflation subsidies.

5. **Diode Relay Node — VERIFIED**
   - Category: bandwidth / secure relay network.
   - Server-native: **Yes.** Official docs explicitly accept Linux boxes/VMs and note datacenter VMs commonly have suitable public addresses.
   - Suggested resources: public IPv4/IPv6, roughly 2 GB RAM, ~20 GB disk.
   - Value: relay encrypted TCP/UDP traffic.
   - Reward mechanism: Relay Nodes trade provided bandwidth for DIODE; Fleet Contracts sponsor traffic, and official docs state 1% of fleet-contract stake is deducted monthly and distributed algorithmically to relay nodes based on bandwidth contribution.
   - Revenue driver: actual routed traffic and location/proximity, not mere uptime.
   - Automation: 5/5 daemon-style.
   - Risk/unknowns: token liquidity/value, current real traffic, node-license obligations and Azerbaijan-specific legal/tax/off-ramp remain to normalize.

6. **CESS Storage Node — VERIFIED**
   - Category: decentralized storage.
   - Server-native: yes. Official server guide specifies Linux x64, >=4 cores, >=8 GB RAM, >=20 Mbps, public IP; minimum storage unit is 1 TiB.
   - Stake: official current staking docs state 2,000 CESS per TiB declared storage.
   - Reward: on-chain storage challenges; used/in-service storage is weighted much more heavily than idle space (95% vs 5% in current reward formula).
   - Automation: 4–5/5 but storage proofs, uptime and claiming require operations.
   - Economics: collateral/token exposure plus disk, bandwidth and utilization; not a low-capital VPS experiment unless storage is already cheap/sunk.

7. **CESS CD2N Retriever / Cacher — VERIFIED / separate bandwidth-cache role**
   - Category: CDN/cache/retrieval service.
   - Value: retrieval nodes serve data; cacher nodes store and serve hot content.
   - Revenue: official docs say retrieval rewards derive mainly from retrieval/caching order revenue plus service-cycle incentives; cache work earns points redeemable for CESS rewards.
   - Automation: 5/5 node role.
   - Server/device fit: retriever is server-like; cacher can be lightweight/edge.
   - Why distinct from storage: paid commodity is retrieval/caching traffic rather than persistent storage capacity.

8. **Acurast Processor — VERIFIED but Tier B, not server-native**
   - Category: smartphone compute.
   - Hardware: Android 12+ non-rooted/locked bootloader or iPhone 6S+/iOS 15+; dedicated Android Core mode can run 24/7.
   - Rewards: ACU base benchmark inflation rewards; optional staked-compute rewards; deployment-execution bonus.
   - Automation: 4–5/5 after phone setup.
   - Classification: HOME/DEVICE. Official docs emphasize genuine smartphone TEEs and explicitly position the network as phone-powered rather than datacenter/server compute.
   - Importance: fills a device-compute gap, but not the primary VPS target.

## Existing lead upgraded, but not new
**Flux / FluxNodes** surfaced again in broad search. Official current site continues to present user-operated underutilized compute nodes earning network rewards. Because Flux already existed in the catalog and this pass did not fully normalize collateral tiers/reward math, it remains an existing lead rather than a net-new candidate. Dedicated validation can be deferred unless control passes keep surfacing it as economically distinctive.

## Discovery-only leads retained for future niche pass
Directory sweeps surfaced several candidates requiring primary-source proof before promotion:
- Impossible Cloud Network;
- Fleek;
- Spheron;
- StorX;
- OORTech;
- Hyra Network;
- Inferix;
- Cere Network;
- dTelecom;
- YOM;
- AR.IO;
- Edge Network/XE;
- Fluence;
- iExec;
- Mawari;
- BrinxAI;
- Multiple Network.

These are **UNVERIFIED discovery leads** only. Some will almost certainly collapse into already-covered compute/storage/CDN mechanisms or prove closed/testnet/points-only.

## Rejected / non-proof observations
- A directory listing, token price, device count, “mineable” label, or marketing APR is not evidence of an open profitable supplier role.
- Generic “machine economy” settlement/payment networks are not earning opportunities unless they expose a provider/service role with a real payer.
- Paxeer-like machine-payment rails are infrastructure/distribution until a self-service provider listing with demand/revenue can be proven.
- Token bootstrap emissions must not be mixed with customer-paid utilization when estimating sustainable economics.

## Query-family yield summary
- machine economy / M2M: low mechanism yield; mostly payment/settlement framing; IDLE was the strongest actionable provider-market result.
- idle-resource monetization: medium project yield; many duplicates plus IDLE.
- capacity marketplace / provider / reseller: high yield; NodeOps explicit VM resale/provider model was the strongest new result.
- node operator income: medium yield; SubQuery became a concrete validated RPC/indexer market.
- bandwidth/CDN relay: medium yield; Diode and CESS CD2N validated.
- DePIN directories: high recall but low precision; produced a sizable unverified queue for niche pass #2.

## Durable conclusion
Run 018 proves the universe is **not yet saturated**. The broad taxonomy is stable, but alternate terminology still surfaces new viable projects inside existing mechanisms. The most important new primary-target candidates from this pass are **IDLE, NodeOps Compute, SubQuery, Diode, and CESS CD2N/storage**.

## Next run
Run 019 — niche saturation/control pass #2.

Priorities:
1. validate the strongest directory-only server-native leads (Impossible Cloud Network, Fleek, Spheron, StorX, OORTech, Fluence, iExec, Edge/XE, dTelecom, YOM);
2. search alternate terms: worker/miner/provider/edge node/executor/processor/host/resource seller/market maker for compute rather than only “node operator”;
3. search ecosystem docs directly for “earn”, “provider”, “host”, “supply”, “operator”, “rewards”, “mainnet”;
4. record net-new count and duplicates;
5. only after this pass decide whether another control pass is needed.
