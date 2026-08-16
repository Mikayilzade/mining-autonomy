# Run 026 — Proof / RPC / Indexing Convergence Pass

Date: 2026-08-16
State: COMPLETE FOR THIS RUN; overall project remains IN PROGRESS.

## Objective
Test the remaining proof-generation, RPC/data-provider and indexing tail using current primary/official sources, with special focus on whether a third party can join now and earn autonomously from server/compute work.

## Result summary
- New top-level economic mechanisms: **0**.
- Genuinely material current implementations strengthened or newly verified in this pass: **4+**.
- Therefore project-level saturation is **not yet reached**.

The same economic families seen in earlier runs remain dominant: customer-paid machine work, token/emission subsidies, stake/collateral-secured operator work, and hybrid fee+inflation models. However, this pass found several current implementations strong enough to keep the project open.

## 1. Boundless / RISC Zero prover market — VERIFIED, HIGH PRIORITY

### What is paid
Boundless is a permissionless market connecting proof requesters with provers. A prover evaluates requests, bids/locks an order, generates a ZK proof and receives the request reward after valid fulfillment. This is direct machine-to-machine paid computational work.

Boundless also has Proof-of-Verifiable-Work / ZK Mining: proving work can earn additional ZKC incentives, but mining eligibility requires staking ZKC.

### Automation
Automation level: **5/5** in principle.
Official prover stack uses Dockerized Bento plus Broker. Broker handles market request evaluation, pricing/bidding, lock-in, sending work to proving cluster and on-chain fulfillment. Monitoring/restart policy is still required.

### Hardware / server fit
Official quick-start recommends approximately:
- 16 CPU threads;
- 32 GB RAM;
- 200 GB SSD/NVMe;
- NVIDIA GPU proving configuration.
Bento supports multi-GPU and multi-machine clusters.

This is datacenter/server-native, but generally GPU rather than cheap VPS economics.

### Capital / risk
- Prover must deposit ZKC collateral to lock market orders.
- Official docs describe typical collateral around 10x request maximum fee; failure to fulfill on time can slash collateral, burning 50% and making the other 50% available as a bounty to secondary provers.
- ETH/gas balance is also required for smooth broker operation.
- ZK mining rewards additionally require staked ZKC; official docs currently link each epoch reward ceiling to stake.

### Revenue source
Two layers:
1. **Customer/market request reward** — economically strongest because it corresponds to demanded proving work.
2. **Protocol ZKC mining incentives** — subsidy/emission layer and must not be mistaken for organic demand.

### Net economics formula
`Net = request rewards + mining incentives - GPU depreciation - electricity - server/network - gas - opportunity cost of collateral/stake - expected slashing losses - maintenance`

Key unknown: real order flow and winning price per GPU-hour / cycle under competition.

### Classification
**VERIFIED / SERVER-NATIVE / HIGH PRIORITY / CAPITAL-AT-RISK.**
One of the closest matches yet to the user's original idea of autonomous servers continuously earning from machine-readable jobs.

## 2. Cysic Mainnet Prover Worker — VERIFIED, HIGH PRIORITY

### What is paid
Current Cysic official docs provide a mainnet prover setup path. Compute providers bid for proving tasks; lower bids improve chance of task selection while higher bids increase potential reward. Official auction docs define prover rewards from selected bid price and task difficulty, with verifier rewards paid separately.

### Current entry requirements
- Linux prover deployment path is documented.
- Current mainnet setup scripts are published by Cysic.
- Each prover worker must reserve **1,000 CYS** to participate in proof generation tasks.
- Reward-address keys are created locally and must be protected.

### Reward model
Official auction docs define task reward and split:
- prover pool: 80% of selected bid × task difficulty;
- verifier pool: 20%;
- reserve-weighted incentives further adjust prover rewards.
Failure to meet the deadline can lead to penalty/slashing and task reassignment.

### Automation
Automation level: **4–5/5**. A running Linux worker receives/bids on proving tasks and can operate continuously; monitoring, bid-price tuning, software updates and key/security operations remain human responsibilities.

### Server fit
GPU/compute-provider role; strong fit for dedicated GPU server or cloud GPU if hosting ToS and economics allow. Current official docs also position datacenter-grade hardware as part of the proving ecosystem.

### Classification
**VERIFIED / SERVER-NATIVE / HIGH PRIORITY / STAKE-RESERVE RISK.**
Must later measure actual tasks/day, reward/CYS liquidity, GPU efficiency and cloud-vs-owned-hardware break-even.

## 3. The Graph Indexer — VERIFIED, SERVER-NATIVE BUT CAPITAL-HEAVY

### What is paid
Current official docs confirm Indexers run indexing nodes, index blockchain data and serve queries.
Revenue streams:
1. query fee rebates paid for serving queries;
2. indexing rewards generated through protocol issuance.

Graph Horizon is live and current gateway/query payment uses GraphTally/TAPv2.

### Entry requirements
- Current minimum Indexer self-stake: **100,000 GRT**.
- Stake is subject to thawing/lock mechanics and can be slashed for malicious/incorrect service.
- Current stack must support Horizon/TAPv2; old stacks do not receive gateway queries.

### Automation
Automation level: **4–5/5** after deployment. Indexer agent/service automates allocation and serving work, but selection of subgraphs, cost models, infrastructure reliability and capital management require operational competence.

### Revenue quality
Hybrid:
- query fees = true customer/usage-linked revenue;
- indexing rewards = inflation subsidy.
Query volume is therefore a key utilization metric and should be separated from emission-supported yield.

### Classification
**VERIFIED / SERVER-NATIVE / CAPITAL-HEAVY.**
Not a cheap bot, but a real paid autonomous data-service operator market.

## 4. SQD / Subsquid Worker — VERIFIED, SERVER-NATIVE BUT CAPITAL-HEAVY

### What is paid
Current SQD docs provide a live worker installation/registration path. Workers store network data, process and serve queries and earn SQD rewards. Current network dashboard exposes active workers, worker APR, rewards, queries served and stored/served data.

### Entry requirements
- worker installation via Docker Compose or source;
- public P2P connectivity;
- on-chain registration;
- **100,000 SQD** locked for worker registration;
- withdrawal delay about 14 days plus the current epoch according to current docs.

### Reward drivers
Official network design/reward material ties worker rewards to combinations of:
- liveness;
- delegated/bonded stake;
- data/query traffic served;
- longevity/fairness parameters.
Thus current rewards are a hybrid of productive traffic and token incentive economics.

### Automation
Automation level: **5/5** once configured; docs explicitly suggest daemonizing/restarting automatically. Maintenance and monitoring remain necessary.

### Classification
**VERIFIED / SERVER-NATIVE / CAPITAL-HEAVY.**
This is a strong machine-readable data-service example, though stake requirement makes it less attractive for low-capital experiments.

## 5. Succinct Prover Network / SP1 — WATCHLIST / TRANSITIONING

Current public official materials are inconsistent in freshness/state:
- official network repository describes a two-sided prover/requester marketplace and contains a reference prover/node implementation;
- an older official platform page still says decentralized network is under active development/not yet live;
- network explorer material describes proof requests paid in USDC and whitelisted keys in some older templates.

Because the current independent public paid-prover admission path was not established cleanly enough in this pass, do **not** count Succinct as a newly VERIFIED deployable opportunity yet.

Classification: **WATCHLIST** pending a current explicit public mainnet prover onboarding page and admission/economics evidence.

## 6. Gevulot ZkCloud — WATCHLIST / NOT COUNTED AS CURRENT OPEN INCOME

Official design docs describe a compelling permissionless prover market:
- anyone can in principle join as prover;
- provers stake native tokens;
- workloads are randomly allocated;
- provers receive workload fees + network rewards + verification rewards;
- missed/non-responsive work can cause removal/slashing.

However, the official introduction page still describes ZkCloud as in development and refers to Firestarter as the production-ready but permissioned network. The roadmap text is stale relative to 2026, so current permissionless live paid admission cannot be asserted from these docs.

Classification: **WATCHLIST**, not VERIFIED for current deployability.

## 7. Dedupe / convergence interpretation
No new economic mechanism appeared. Boundless and Cysic are variants of the already-known proof-market / verifiable-compute family; The Graph and SQD are variants of paid indexing/query/data-provider markets.

But project discovery is still yielding material current implementations. Boundless and Cysic in particular are sufficiently close to the primary target that ending research now would be premature.

## 8. Economics ranking from this run
1. **Boundless prover** — strongest match to autonomous machine-job market; direct request revenue + optional protocol incentives; GPU and collateral risk.
2. **Cysic prover** — strong live bid/task model; GPU + reserve requirement + token/reward liquidity need measurement.
3. **The Graph Indexer** — real customer query fees plus issuance, but 100k GRT self-stake creates large capital hurdle.
4. **SQD worker** — real autonomous query/data worker, but 100k SQD bond creates large capital hurdle.
5. **Succinct** — potentially strong but current open admission unresolved.
6. **Gevulot** — attractive design, current permissionless live status not established.

## 9. Safety / ToS / geography
No automation in this pass requires human impersonation, CAPTCHA bypass, fake engagement, spam or prohibited microtask botting. These are protocol-native machine roles.

Azerbaijan availability remains unconfirmed for all CAPEX deployments unless live onboarding, wallet/token acquisition, exchange/off-ramp and any provider/KYC dependencies are tested. Protocol permissionlessness does not guarantee every ancillary service is available in Azerbaijan.

## 10. Decision
**Do not mark COMPLETE.**

Run 026 produced zero mechanism novelty but more than the allowed 0–2 weak/restricted new projects. The project tail remains productive.

## Next run
Run 027 should be a **proof-market + decentralized data operator tail sweep**, concentrating on:
- proof marketplaces adjacent to Boundless/Cysic;
- prover brokers/aggregators and independent worker pools;
- Lagrange current operator admission;
- Succinct public prover admission status;
- current Gevulot/ZkCloud launch state;
- The Graph Horizon adjacent data services/operators;
- SQD ecosystem operator variants;
- archival/data-availability/DA provider roles with explicit current rewards;
- RPC/query/indexing networks not yet in the catalog.

Completion remains gated on project-level convergence, not taxonomy alone.
