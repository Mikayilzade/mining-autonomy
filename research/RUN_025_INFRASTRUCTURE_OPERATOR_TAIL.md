# Run 025 — Remaining infrastructure/operator tail

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Goal
Sweep the remaining server-native infrastructure/operator vocabulary after Run 024, with emphasis on live 2025–2026 provider onboarding and real reward/fee paths: RPC suppliers, indexers, proof generators, validator-service operators, CDN/edge hosts and adjacent infrastructure roles.

## Result summary
- New top-level economic mechanisms: **0**.
- Material newly validated project implementations: **3**.
- Additional restricted/licensed project implementation: **1**.
- Previously partial lead resolved as restricted: **Supra validator/operator remains permissioned**.
- Fleek Network remains a **WATCHLIST** lead rather than promotion to VERIFIED because the discoverable operator/reward documentation is materially older and this pass did not establish a comparably current 2026 live-income/onboarding state.

This is another mechanism-level convergence pass, but **not project-level convergence**. The discovery of Lava, SubQuery, Aztec and Datagram means the completion gate is not yet satisfied.

---

## 1. Lava Network — RPC Node Provider
Status: **VERIFIED**
Category: blockchain RPC / API infrastructure provider
Server-native: **YES**
Automation: **5/5 once deployed, with monitoring/maintenance**

### Economic role
A Lava RPC Node Provider runs RPC nodes for one or more supported chains plus the Lava provider process, stakes LAVA for each service, serves consumer relay requests and submits cryptographic relay proofs. Provider rewards include subscription revenue, public RPC pool rewards, delegation commission and variable provider incentives.

Official documentation states that providers/restakers receive **95% of subscription rewards** and **95% of Lava Public RPC Pool rewards**; rewards depend on valid relay proofs, QoS, reputation and service availability. Providers can query estimated and claimable rewards on-chain.

### Entry / infrastructure
- Must operate the underlying chain RPC endpoint(s).
- Must stake LAVA separately for each supported chain/spec according to that spec's `min_stake_provider`.
- Provider process is machine/server native.
- Geolocation is declared on-chain; official enum includes Asia among regions.
- Current provider unbonding period documented as 21 days.
- Provider jailing exists for poor/unresponsive service. Older FAQ says provider slashing was not yet implemented, so current contract/protocol state must be checked before capital deployment.

### Revenue model
`Net = provider subscription share + RPC-pool rewards + provider drops + delegation commission - RPC-node infrastructure - provider infrastructure - LAVA opportunity cost - gas - monitoring/maintenance - token/liquidity/withdrawal costs`

Dominant hidden variable: actual consumer relay demand and provider selection/reputation.

### Azerbaijan / KYC
No Azerbaijan-specific exclusion was established in this pass. Protocol participation does not by itself prove exchange/off-ramp or ancillary-service availability. Live onboarding and payout liquidity must be tested before CAPEX.

### Next economics action
Pull live provider counts, chain-specific minimum stakes, estimated payouts and actual relay demand per spec; compare with cloud/bare-metal RPC node costs.

---

## 2. SubQuery Network — Node Operator / RPC Provider / Indexer
Status: **VERIFIED**
Category: blockchain indexing + RPC/API provider marketplace
Server-native: **YES**
Automation: **4–5/5**

### Economic role
SubQuery Node Operators can run data-indexing deployments, RPC endpoints, or both. Current official docs explicitly support deploying the operator stack locally or on an external VM and document Docker plus automated Compose upgrades.

Rewards come from two sources:
1. productive work — paid queries through Closed Agreements or Flex/PAYG plans;
2. network inflation / stake rewards — for running eligible boosted projects while online and synced.

RPC endpoints can receive query rewards generated when users pay for queries. Official docs warn that an operator can receive zero query rewards when price/performance, availability, sync state or demand are poor.

### Current capital parameters (official docs, 2026-04-23)
- Minimum Node Operator self-stake: **200,000 SQT**.
- Delegation capacity: **12x** own stake.
- SQT unlock period: **14 days**.
- Unlock fee: **0.1%**.
- Network inflation rate: **1.2%**, of which 1% is documented as network inflation rewards.
- Incorrect/incomplete service can cause stake reallocation/slashing to the treasury.

### Infrastructure
Official setup supports an **external VM**. Node Operators may run RPC endpoints or indexers and expose the public service endpoint. Current docs explicitly mention AWS, Google Cloud, DigitalOcean, Azure and other rented infrastructure for indexers.

### Revenue model
`Net = query/PAYG revenue + closed-agreement revenue + stake/inflation rewards + operator commission on delegated capital - VM/RPC/indexer/database cost - 200k SQT opportunity cost - gas - monitoring/support - expected slashing/loss - token/withdrawal costs`

Important: this is not a pure idle-server yield. Operators must choose deployments, maintain services and periodically optimize stake/project allocation. It is still highly automatable infrastructure work.

### Azerbaijan / KYC
No country-specific confirmation in the sources reviewed. Treat geographic eligibility and token liquidity/off-ramp as unresolved until live onboarding.

### Next economics action
Convert 200k SQT to current fiat opportunity cost; inspect live operator/project APYs and query revenue rather than using headline APY; model an RPC-only VM vs indexing stack.

---

## 3. Aztec — Mainnet Prover
Status: **VERIFIED**
Category: ZK proof generation / rollup infrastructure
Server-native: **YES, but high-spec/datacenter class**
Automation: **5/5 after deployment, with experienced operations required**

### Economic role
Aztec's current mainnet has a prover role that generates epoch proofs. Official docs state that proof rewards accrue per epoch to the `PROVER_ID`; a prover's share is `yourShares × epochRewards / totalShares`, and rewards are claimable after the proof submission deadline. Current docs publish canonical **mainnet** rollup addresses and explicitly say reward claiming is enabled on mainnet and testnet.

### Capital / stake
- Prover stake: official operator overview currently lists **none**.
- ETH is needed in the publisher account for L1 proof-submission gas.
- No slashing is listed for the prover role in the current role overview.

### Hardware
Current minimum architecture is much heavier than an ordinary VPS:
- prover node: 16 cores / 32 vCPU, 16 GB RAM, 1 TB NVMe, 25 Mbps;
- broker: 8 cores / 16 vCPU, 16 GB RAM;
- each prover agent: **32 cores / 64 vCPU, 128 GB RAM**, scaling linearly for multiple agents.

Aztec explicitly describes prover agents as high-performance, typically datacenter-grade infrastructure. CPU and RAM, rather than a consumer GPU, are the central resource in the current published requirements.

### Revenue model
`Net = epoch proof rewards - high-core/high-RAM server cost - 1 TB NVMe/node cost - L1 gas - networking - monitoring/engineering maintenance - failed/late proof opportunity loss - token/withdrawal costs`

The critical unknown is reward per successful epoch relative to infrastructure cost and competition. This is a particularly relevant discovery because it is a genuine machine-to-machine server job market without a staking barrier, but its compute requirements are substantial.

### Azerbaijan / KYC
Protocol docs reviewed do not establish country-specific eligibility. Ethereum wallet operation does not imply fiat off-ramp availability. Live network participation and withdrawal route need separate validation.

### Next economics action
Measure recent prover reward pools, number of competing provers/shares, epoch frequency and L1 gas; derive break-even cost per 64-vCPU/128-GB agent-hour.

---

## 4. Datagram — Full Core Node
Status: **RESTRICTED**
Category: licensed compute/storage/bandwidth/edge infrastructure
Server-native: **YES**
Automation: **5/5 after setup**

### Current state
Official docs now state that **mainnet is live** and Full Core nodes may run on laptops, desktops or **cloud instances**. A low-end UDP configuration is listed at roughly 2 CPU cores, 2 GB RAM (16 GB recommended), 2 GB SSD and 10 Mbps up/down; higher-value AI or other services require more resources.

### Why restricted
Unlike permissionless software-only provider paths, a Full Core operator must own a **paid Full Core Node License NFT**. The license grants lifetime node-operation rights, is locked for one year after purchase, and only the license-holding wallet can operate/earn unless delegated. Claiming a purchased node license requires **KYC**.

Official KYC geographic exclusion list reviewed in this pass does **not** list Azerbaijan, but this is not a guarantee that all payment, wallet and off-ramp steps work from Azerbaijan.

### Rewards
Official docs describe mainnet DGRAM token rewards tied to uptime/availability, latency/performance and actual compute/storage/bandwidth usage. Full Core holders are documented as receiving a share of daily DGRAM emissions, with uptime and resource-sharing components. Because the economics depend heavily on license purchase price, token liquidity and emissions, this is not comparable to a zero-capital VPS daemon.

### Revenue model
`Net = DGRAM uptime/resource rewards - license purchase opportunity cost/amortization - cloud/server cost - bandwidth - maintenance - token/liquidity/withdrawal costs`

### Next economics action
Recover current license market/purchase price and liquid DGRAM value/volume, then calculate realized fiat yield per license and per cloud instance. Do not infer profitability from token emission percentages.

---

## 5. Supra node/operator — partial lead resolved
Status: **RESTRICTED / permissioned**

Current official Supra docs (updated 2026-05-12) explicitly state that **node operation is currently permissioned to select node operators and is not available to the public**. Mainnet validator documentation and reward/claiming material exists, but this is not presently an open autonomous earning path for a new generic operator.

Hardware is also substantial: current mainnet upgrade checklist specifies Xeon/EPYC 3.2 GHz+, 64 GB RAM, SSD, 500 GB disk and 2 Gbps networking.

Do not promote Supra to the deployable shortlist until public operator admission opens.

---

## 6. Fleek Network — keep WATCHLIST
The operator/reward documentation found describes a permissionless node model, resource health checks and rewards for operators contributing hosting/edge resources. However, the indexed pages surfaced in this pass are materially older than the 2026 evidence standard used for high-priority promotion, and this pass did not establish a current 2026 live onboarding + liquid realized-income path comparable to Lava/SubQuery/Aztec.

Action: revisit through current repository releases/network explorer/token/reward state before promotion.

---

## 7. ClayStack — keep WATCHLIST / validator-service implementation
Official operator docs describe registration by individuals or professional operators, dynamic bonds, validator reward sharing and support for SSV/Obol/direct-staking operator types. But current evidence surfaced here is older and delegation is demand/selection dependent. It is an implementation of the already-known validator-as-a-service/operator family, not a new mechanism.

Action: verify current protocol/app activity and whether fresh operator registration/delegation is actually occurring before promotion.

---

## 8. Livepeer 2026 recheck — existing entry strengthened, not new
Current 2026 Livepeer docs materially strengthen the already VERIFIED catalog entry:
- Orchestrators have two revenue streams: ETH service fees from Gateway work and inflationary LPT rewards.
- Running software alone creates neither revenue stream.
- The main transcoding active set is top 100 by LPT stake, a significant barrier for new solo orchestrators.
- Current docs identify two alternatives when stake is limited: join a pool as a worker, or run AI inference only; AI routing emphasizes capability/price, although the official AI Orchestrator guide currently describes a Top-100 Mainnet Orchestrator prerequisite for that guide/path.
- ETH gas budget and workload demand must be modeled explicitly.

No new mechanism counted.

---

## Run-level economics conclusions
1. **RPC/data infrastructure is a real paid machine market.** Lava and SubQuery both provide direct current evidence of operators earning for serving programmatic requests.
2. **CPU/RAM proof generation is now a concrete server earning role, not merely a future category.** Aztec mainnet prover rewards make high-core, high-RAM machines a directly monetizable resource, subject to competition and gas.
3. **Capital barriers vary sharply:** Lava requires per-service LAVA stake, SubQuery requires 200k SQT self-stake, Datagram requires a paid license/KYC, while Aztec prover currently lists no stake but has very high infrastructure requirements.
4. **Customer usage remains the strongest economic evidence.** Lava relay service and SubQuery query payments are preferable evidence to emissions alone, but neither proves positive net profit.
5. **Uptime/emissions models require skepticism.** Datagram is technically easy to cloud-host but license/token economics can dominate server cost.
6. **Permissioned programs must not be treated as available opportunities.** Supra is explicitly closed to the public today.

## Saturation decision
Run 025 produced **0 new top-level mechanisms** but **4 genuinely new current project implementations**, three of them strong server-native provider roles. Therefore the project-level convergence gate failed again.

Project state remains **IN PROGRESS**.

## Next run — Run 026
Perform a focused **proof/RPC/indexing convergence pass** rather than another generic provider search. Search current official 2025–2026 sources for:
- RPC provider / gateway supplier / decentralized API node
- indexer operator / query provider / subgraph provider
- ZK prover / proof marketplace / prover auction / proof pool
- CPU prover / high-RAM prover / proof broker
- data-availability provider / archival node reward
- worker pool / transcoding worker without stake

Prioritize candidates absent from all previous runs. Explicitly test whether likely families such as The Graph Indexer, Subsquid workers, Boundless/RISC Zero, Succinct/SP1, Gevulot, Lagrange, Cysic and other proof markets currently admit independent paid operators, and whether the earning role is mainnet/live versus testnet/invite-only.

If Run 026 yields another material cluster, continue. If it yields only 0–2 weak/restricted new implementations, move to the final cross-category saturation check.