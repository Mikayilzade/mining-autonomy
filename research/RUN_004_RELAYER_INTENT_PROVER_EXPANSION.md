# Run 004 — Relayer / intent / prover / data-worker expansion

Date: 2026-08-15
Status: completed

## Scope
This run finished several unresolved candidates from Run 003 and broadened the server-native universe into intent fillers/relayers, decentralized search, and data-serving workers.

## High-confidence validated additions

### 1. Succinct Prover Network / SP1 prover — VERIFIED
Category: ZK proof marketplace / server-native compute.

What earns:
- Requesters pay PROVE for proof generation.
- Provers compete in reverse auctions; the lowest eligible bidder wins the proof request.
- The winning prover receives the requester payment less protocol and staker shares.

Admission:
- Official docs explicitly describe proving as open and permissionless and state that anyone can participate by running a prover.
- Provers need sufficient PROVE stake for a request, but can source stake through delegation.
- Missing deadlines can slash stake.

Automation: 5/5 in principle once prover/bidding/monitoring infrastructure is configured.
Server fit: yes; official market structure explicitly discusses both datacenters and home provers.
Capital: GPU/prover hardware + stake/delegated stake; amount is request-dependent rather than one universal minimum.
Risk: competitive pricing, hardware cost, utilization, missed-deadline slashing.

Conclusion: strong fit for the project thesis: useful computational work continuously auctioned to autonomous provers.

### 2. SQD Network worker — VERIFIED
Category: decentralized historical blockchain-data service / storage + compute.

What earns:
- Workers store and serve historical blockchain data and earn SQD rewards.
- Rewards depend on liveness, delegated/bonded tokens, and served query traffic.

Official current requirements:
- 4 vCPU
- 16 GB RAM
- 1 TB SSD
- stable 24/7 connection, minimum 1 Gbit
- public IP

Reward mechanics:
- epoch rewards combine liveness and traffic components and depend on bonded/delegated stake.
- worker reward pool is explicitly allocated in tokenomics.

Automation: 5/5 node daemon with monitoring.
Server fit: yes; docs are written as a server-worker deployment and even advise against one hosting provider for reliability reasons.
Capital: server + SQD bond/delegation economics; exact optimal bond requires later modeling.
Risk: utilization, jailing/reliability, token-price risk.

Conclusion: strong server-native candidate; corrects Run 003 uncertainty.

### 3. Across Protocol relayer — VERIFIED
Category: cross-chain intent relayer / capital + autonomous execution.

What earns:
- Users pay relayer fees.
- Relayers monitor deposits, evaluate profitability, front destination-chain capital, execute fills, then receive reimbursement through settlement.

Admission:
- Official docs explicitly state participation is permissionless and anyone can operate a relayer.
- Open-source relayer-v3 software is provided.

Minimum documented server requirements:
- 64-bit dual-core CPU @ 2+ GHz
- 4 GB RAM
- UNIX-like OS

Capital:
- Requires inventory/liquidity across chains plus gas.
- Capital is locked until bundle settlement, roughly 1.5 hours under normal documented flow.

Automation: 5/5; software supports automatic inventory management/rebalancing configuration.
Risk: gas, capital lock-up, chain reorg/finality, software bugs, liquidity inventory and competition.

Conclusion: one of the clearest examples of the user's original target: a continuously running server bot performing simple protocol-defined jobs for fees, but with material working capital.

### 4. UniswapX filler — VERIFIED
Category: intent filler / DEX execution bot.

What earns:
- Fillers monitor signed UniswapX orders and settle them when economically viable.
- They source liquidity from private inventory and/or external on-chain liquidity.
- Economic profit is execution spread/opportunity after gas and routing costs rather than a fixed protocol emission.

Admission:
- Official docs state anyone can fill orders.
- Mainnet orders may have temporary exclusivity; permissionless fillers can participate after expiration or via documented override conditions.
- Open orders can be polled via the UniswapX API.

Automation: 5/5 technically, but requires strategy/pricing/risk code.
Server fit: yes.
Capital: gas + inventory/flash/on-chain liquidity strategy.
Risk: competition, latency, revert/gas loss, bad pricing, MEV and inventory risk.

Conclusion: valid autonomous earning mechanism, but closer to competitive market-making infrastructure than passive mining.

### 5. Presearch node — VERIFIED
Category: decentralized search compute node.

What earns:
- Node operators provide processing/server capacity to the search network and receive PRE rewards.
- Current official node pages require at least 4,000 PRE staked for node reward eligibility.
- Rewards depend on utilization, reliability/quality and staked capacity.

Server fit:
- Explicitly supports outside servers; official run page discusses local versus outside-server operation.
- Docker-based deployment.

Automation: 5/5 once deployed.
Capital: server + minimum 4,000 PRE stake per rewarding node under current published rules.
Risk: token price, changing tokenomics/reward weights, utilization and reliability.

Important exclusion:
- Presearch search-usage rewards are NOT a bot opportunity. Official docs explicitly treat automated/fake searching as abuse and use reward verification against token farming. Only the node-operator role belongs in this project.

### 6. Cysic prover node — VERIFIED
Category: ZK proving / GPU compute.

What earns:
- Prover nodes receive assigned ZK proof tasks and earn Cysic network credits/rewards.
- Operators choose a bid price: lower bid increases likelihood of receiving tasks; higher bid increases reward per completed task.

Admission / capital:
- Current official mainnet setup exists.
- 1,000 CYS must be reserved for each prover worker node.
- High-performance GPU hardware is required; current docs include RTX 5090 support.

Automation: 5/5 after setup.
Server fit: yes, Linux high-performance machine/bare metal or suitable GPU server.
Risk: hardware cost, competitive bid pricing, utilization, token economics.

Conclusion: strong current prover-market candidate and no longer merely testnet/points.

## Validated but capital/admission-heavy or still incomplete

### 7. CoW Protocol solver — VERIFIED economic role, RESTRICTED admission/economics
Category: solver / intent competition.

Evidence:
- Solvers compete to settle batched intents and receive COW rewards plus reimbursements under the solver-reward pipeline.
- Official docs describe solvers as bonded third parties and document weekly solver rewards.
- Anyone with DeFi knowledge and an optimization algorithm can create solver software.

Restriction:
- Bonding and production onboarding must be treated separately from software creation. Current docs confirm bonded solver operation and rewards, but this run did not fully normalize exact onboarding/bond thresholds for a new production solver.

Automation: 5/5 technically; sophisticated algorithmic and capital requirements.

### 8. 1inch Fusion resolver — RESTRICTED
Category: intent resolver.

What earns:
- Resolvers compete to fill Fusion orders and can earn fees.

Restriction:
- Current official help docs describe resolver access as limited to approved resolvers, with the top 10 Unicorn Power balances eligible, and a minimum requirement tied to 5% of total Unicorn Power supply.
- Therefore this is not an open low-capital server bot despite technically autonomous execution.

Status: legitimate earning role, but highly capital/admission constrained.

### 9. Gevulot / zkCloud prover — VERIFIED mechanism, deployment economics need current operational check
Category: ZK proving marketplace.

What earns:
- Provers are rewarded for proof generation and proof verification.
- Workloads are allocated to prover nodes, completed and verified, then rewards are distributed.
- Global prover-set failure/fallback rules and validator staking are documented.

Open question:
- Need a separate current deployment/operator guide pass to establish exact current mainnet hardware, prover admission and token/stake thresholds before ranking profitability.

## Important taxonomy refinements from this run
1. Intent infrastructure should be split into three economic types:
   - protocol-subsidized/rewarded solver (CoW);
   - spread/execution-profit filler (UniswapX);
   - explicit relayer-fee + working-capital model (Across).
2. A node can be both server-native and capital-native. Across, Presearch, Succinct and Cysic all need separate infrastructure-cost and capital-at-risk accounting.
3. Permissionless software does not imply permissionless profitable order flow. Production admission/exclusivity must be documented independently.
4. Human-usage rewards and node rewards on the same platform must be separated. Presearch explicitly forbids automated token-farming search behavior while rewarding autonomous node infrastructure.
5. Reward competition may be price-auction based (Succinct/Cysic), performance/reliability based (SQD/Presearch), or latency/liquidity based (Across/UniswapX).

## Next run priority — Run 005
Broaden away from this branch so universe construction does not over-focus on blockchain solvers.

Priority:
1. Lagrange proving / ZK coprocessor operator opportunities.
2. Meson bandwidth/CDN provider economics.
3. Deep decentralized compute/GPU expansion: io.net, Clore.ai, TensorDock, Hyperbolic, RunPod community/provider programs, Salad server limits, Render onboarding.
4. Decentralized storage expansion: Swarm Bee, Arweave roles, Crust, ScPrime, Autonomi.
5. Relay/CDN/VPN expansion beyond Mysterium/Streamr/NKN: Meson plus other server-permitted networks.
6. Bittensor subnet-miner universe sweep should begin soon as a dedicated run because each subnet can represent a distinct automated paid task market.

## Saturation state
Control passes completed: 0.
New strong validated roles this run: Succinct prover, SQD worker, Across relayer, UniswapX filler, Presearch node, Cysic prover.
New restricted/partially normalized roles: CoW solver, 1inch resolver, Gevulot prover.
Conclusion: still far from saturation; discovery remains productive.
