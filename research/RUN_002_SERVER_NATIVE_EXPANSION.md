# Run 002 — Server-native opportunity expansion

Date: 2026-08-15
Status: completed
Scope: broaden the server-native universe before detailed profitability modeling.

## Executive result
This pass confirms that the primary target is larger than raw CPU/GPU renting. There are at least six distinct server-native earning mechanisms worth separate treatment:

1. sell compute/GPU time;
2. sell bandwidth/IP/relay service;
3. serve paid blockchain RPC/data requests;
4. index/query blockchain data;
5. generate cryptographic proofs;
6. operate protocol verification/checker infrastructure tied to a license/stake.

A seventh adjacent model also appeared clearly: run a commercial gateway/API business on top of decentralized infrastructure and retain the margin. This is closer to BUILD-ONCE than pure mining, but can become highly autonomous.

---

## Newly validated / upgraded candidates

### 1. Mysterium Network node
Status: VERIFIED
Classification: SERVER-NATIVE bandwidth / VPN / proxy relay
Automation: 5
Normal VPS: YES — official Linux guide explicitly says a node may run in a datacenter and gives a 1-core/1GB VPS as sufficient example.
Value supplied: bandwidth + routable IP + uptime.
Revenue: users pay node runners for VPN/proxy service; official docs describe MYST earnings and a 20% network/service fee.
Capital: low if using a cheap VPS; no staking requirement stated in current token docs.
Recurring costs: VPS + bandwidth/egress + withdrawal gas.
Important risk: exit-node/legal/abuse exposure. Official FAQ advises node operators to consider local law and offers B2B traffic modes; public traffic can raise risk and earnings.
Scaling: supply/demand is regional; datacenter IP quality/type is an input to pricing, so merely spawning identical VPS nodes is not guaranteed to scale profitably.
Next action: model expected revenue by datacenter IP/location and compare against VPS bandwidth pricing; verify Azerbaijan/legal and provider ToS.
Evidence: official Mysterium docs, checked 2026-08-15.

### 2. Pocket Network Supplier / RelayMiner
Status: VERIFIED
Classification: SERVER-NATIVE paid RPC relay provider
Automation: 5 after setup/monitoring
Normal VPS: technically possible, but practical capacity depends on backend chain nodes and traffic.
Value supplied: blockchain API/RPC relays.
Revenue: usage-based POKT. Current Shannon docs state applications burn POKT to pay for data and suppliers receive POKT for valid proven relay work; no relay/proof means no reward.
Capital: material. Current provider quickstart states a supplier stake of 59,500 POKT plus liquid funds for claims/proof transaction fees.
Recurring costs: RelayMiner infrastructure, chain RPC/full-node backends, bandwidth, POKT transaction fees.
Economics: demand/utilization-driven, not a fixed APR. Competition, relay volume, service mix and token price affect revenue.
Risk: missed claims/proofs lose revenue; operational complexity and stake exposure.
Next action: calculate current stake USD value, real service-level revenue from POKTscan, backend-node costs, and low-cost service niches.
Evidence: official Pocket Network docs, checked 2026-08-15.

### 3. Pocket Network commercial Gateway
Status: VERIFIED mechanism
Classification: SERVER-NATIVE / BUILD-ONCE API gateway business
Automation: 4–5 after customer acquisition
Value supplied: sell RPC access to customers and route through Pocket suppliers.
Revenue: customer RPC fees minus protocol burn and infrastructure; official docs explicitly describe commercial gateway operators setting their own pricing and keeping the margin.
Capital: infrastructure + working POKT/burn cost; customer acquisition is the main non-passive component.
Why important: this is not resource mining, but it is a legitimate machine-to-machine business that can later run mostly autonomously and should be tracked separately.
Next action: later include under automated paid API businesses.

### 4. The Graph Indexer
Status: VERIFIED
Classification: SERVER-NATIVE indexing/query service + CAPITAL-NATIVE stake
Automation: 4–5 operationally, but economically/strategically active.
Value supplied: index blockchain/subgraph data and serve queries.
Revenue: query fees + indexing rewards.
Capital: high. Current official docs state minimum self-stake = 100,000 GRT.
Risk: stake can be slashed for malicious/incorrect service; operational indexing costs; competitive allocation strategy.
Scaling: requires both reliable infrastructure and capital/delegation, so not a cheap VPS penny-miner.
Next action: move to high-capital server matrix; calculate minimum stake value and server footprint during economics phase.
Evidence: official The Graph docs, checked 2026-08-15.

### 5. Aztec Prover
Status: VERIFIED
Classification: SERVER-NATIVE ZK proof generation
Automation: 5 once provisioned
Value supplied: cryptographic proof generation for rollup epochs.
Revenue: official mainnet documentation states prover rewards accrue per epoch and can be claimed from the Rollup contract.
Hardware: very heavy. Current docs list separate prover node/broker/agent roles; one prover agent is 32 core/64 vCPU, 128 GB RAM, with scaling roughly linear for multiple agents; node also needs 1 TB NVMe.
Capital: no conclusion yet on bond/stake from this pass; compute capital/hosting cost is high.
Economics: reward share depends on prover shares/epoch reward pool, so profitability requires measured competition and actual reward data.
Importance: strong proof that ZK proving is not merely a speculative future category — a current mainnet paid prover role exists.
Next action: benchmark cloud/bare-metal cost versus actual mainnet reward history; investigate whether commodity rented hardware can compete.
Evidence: official Aztec docs, checked 2026-08-15.

### 6. Aethir Checker Node
Status: VERIFIED
Classification: SERVER-NATIVE checker/verification infrastructure + LICENSE/CAPITAL-NATIVE
Automation: 5 after setup
Normal VPS: YES. Official docs explicitly provide VPS/NaaS options and state location does not affect node operation; current minimum for one checker license is 1 x86 core, 64 MB RAM, 10 GB disk, 10 Mbps.
Value supplied: validates performance/specifications of Aethir cloud containers.
Revenue: checker node license rewards in ATH/vATH ecosystem; official owner/operator docs describe reward claiming and ongoing checker rewards.
Capital: requires a Checker Node License NFT or delegation from an owner; therefore this is not a zero-capital daemon despite tiny server requirements.
Scaling: up to 100 licenses per checker client according to docs, with resources scaling linearly; potential delegation/operator business requires separate research.
Risk: license economics/token exposure; incorrect/offline nodes can lose rewards or be banned.
Next action: current license acquisition/delegation economics, exact reward schedule, KYC/Azerbaijan restrictions, and whether operating delegated licenses can be entered without buying NFTs.
Evidence: official Aethir docs, checked 2026-08-15.

### 7. Render Network Node Operator / Compute Client
Status: VERIFIED role, RESTRICTED onboarding/fit pending
Classification: GPU compute/rendering
Automation: 4–5
Value supplied: idle GPU compute for rendering and AI/general compute.
Revenue: official foundation FAQ says node operators receive rewards for work plus availability; BME emissions/rewards are tied to supplied compute and network usage.
Server-native classification: compatible with Linux and dedicated GPU machines, but official positioning is primarily high-end consumer GPU capacity and node onboarding is controlled as capacity demand changes. Do not assume arbitrary cloud-GPU instances are accepted/economic.
Capital: GPU hardware/hosting.
Important finding: current Render Compute Network extends beyond rendering into AI/general compute, so it belongs in both rendering and GPU-compute sweeps.
Next action: verify current onboarding path, supported GPU list, datacenter/cloud restrictions, and whether new independent operators are being accepted at present.
Evidence: official Render Foundation FAQ/support pages, checked 2026-08-15.

### 8. NKN node / Proof of Relay
Status: VERIFIED mechanism; economics still UNVERIFIED
Classification: SERVER-NATIVE relay/mining
Automation: 5
Value supplied: network data transmission / relay power.
Revenue mechanism: official NKN docs define Proof of Relay and state expected node rewards depend on network connectivity and data transmission contribution.
Server fit: protocol architecture is node/server friendly, but this pass did not yet validate current minimum stake/ID-generation costs, latest mining rewards, or datacenter economics.
Next action: current node setup docs + reward schedule + number-of-neighbor/IP constraints + VPS economics.

---

## High-priority unresolved leads from this pass

These remain discovery leads and should NOT be called profitable or fully verified yet:

- io.net worker/supplier: current official discovery was noisy; verify worker onboarding and reward status directly.
- Lava Network providers: RPC provider family; primary documentation/reward mechanics need a dedicated pass.
- Subsquid / SQD workers: likely data/query infrastructure; confirm current paid worker/indexer roles.
- Boundless / RISC Zero proving market: strong candidate for permissionless ZK jobs; dedicated primary-source pass required.
- Succinct/SP1 prover network: dedicated check for current paid/mainnet prover access.
- Gevulot / Cysic / Lagrange proving roles: separate current-mainnet versus testnet/points.
- Chainlink node operator / Automation roles: do not assume permissionless earning; operator sets may be curated/approved.
- Gelato executors: determine whether independent executors can currently join and earn or whether execution infrastructure is centrally/operator managed.
- CoW/intent solvers: technically autonomous paid service, but competition, bonding and solver admission need protocol-specific review.
- Meson Network: CDN/bandwidth node economics and onboarding need verification.
- Streamr operator: validate current DATA/operator reward mechanics and stake requirements.
- Presearch node: validate current node-reward program and server/VPS conditions.

---

## Taxonomy additions discovered

### Paid RPC supplier
A daemon serves measurable machine API requests; protocol verifies work and pays per usage. Example: Pocket Supplier.

### Commercial decentralized API gateway
Operator acquires customers and resells/routs decentralized infrastructure, keeping margin. Example: Pocket commercial Gateway. Not pure passive mining, but can be highly automated after setup.

### Licensed verifier/checker node
Server work is lightweight but earning right comes from a purchased/delegated license. Example: Aethir Checker. Economics must split `server ROI` from `license/capital ROI`.

### Mainnet ZK prover
Compute-intensive autonomous job market producing proofs, with protocol reward pool. Example: Aztec prover. This deserves a full category rather than being treated only as future technology.

### Hybrid work + stake infrastructure
Operator earns for useful service but must also lock substantial token capital. Examples: Pocket Supplier, The Graph Indexer. These should never be compared directly with zero-capital VPS daemons without charging an opportunity cost for stake.

---

## Research conclusions for later economics

1. Cheap VPS cost alone is not the right filter. Aethir demonstrates tiny compute can hide expensive license capital; Pocket/The Graph demonstrate useful server work can hide major token stake.
2. Revenue should be separated into CUSTOMER-DEMAND revenue versus PROTOCOL-EMISSION rewards. Demand-backed work is generally more informative for sustainability analysis.
3. VPS compatibility must be explicitly verified. Mysterium is a positive example; EarnApp from Run 001 is a negative example.
4. Exit/relay nodes require a legal-abuse-risk column independent of profitability.
5. ZK proving deserves a dedicated hardware-efficiency sweep because it is a genuine paid server workload, not merely token farming.
6. Some of the best autonomous online models may be machine-to-machine service businesses (gateway/API) rather than protocols that call themselves mining.

## Saturation metric
This run produced multiple newly verified server-native opportunities and at least four useful taxonomy refinements. Saturation is nowhere near reached.

## Next recommended stage
Run 003: dedicated **RPC/indexer/oracle + ZK/prover + keeper/solver** expansion, with primary-source checks for Lava, Subsquid, Boundless/RISC Zero, Succinct, Gevulot/Cysic/Lagrange, Chainlink operator accessibility, Gelato executor accessibility and CoW/intent solver economics. Then follow with an independent DePIN-directory sweep to discover missed server-native categories.
