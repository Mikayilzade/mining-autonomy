# Run 003 — RPC / Oracle / ZK Prover / Keeper-Solver Expansion

Date: 2026-08-15
Status: COMPLETED (research stage, not project completion)

## Scope
This pass deepens server-native earning mechanisms around paid RPC/data relay, decentralized indexing, ZK proving, oracle/node operation, keeper/executor infrastructure and intent/solver markets. Priority remains opportunities that can operate continuously on a VPS/bare-metal/GPU server with minimal human intervention.

## Validated / materially clarified candidates

### 1. Lava Network — RPC Node Provider
Status: VERIFIED
Category: server-native paid RPC relay / hybrid work+stake infrastructure
Automation: 5/5 after deployment and monitoring

Economic mechanism:
- Provider runs RPC infrastructure for supported chains, stakes LAVA for each service, receives relay requests and produces cryptographic proofs of relay service.
- Official docs state providers receive 95% of subscription/public-RPC-pool rewards shared according to service, plus possible provider drops and commission on delegated stake.
- Rewards depend on valid relay proofs, QoS, reputation and avoiding jail.

Server fit:
- Strong. Setup is ordinary persistent Linux/network infrastructure: synced backend chain node(s), `lavap rpcprovider`, public endpoints and optional TLS/cache.
- Required geolocation is explicit; Asia is a supported geolocation class.

Capital / constraints:
- Must fund a wallet and stake LAVA separately for services/chains; minimum stake is spec-specific, so a cheap VPS does NOT imply low total capital.
- Backend RPC nodes can be much heavier than the Lava provider process itself.
- 21-day unbonding is documented in provider FAQ.

Why it matters:
- This is one of the clearest examples of the target model: a daemon performing measurable paid machine-to-machine work continuously.

Next economics work:
- Query current per-spec min stake, provider counts, real relay utilization and estimated provider rewards; compare own backend-node cost versus purchased upstream RPC.

### 2. Boundless / RISC Zero — decentralized ZK proving + ZK mining
Status: VERIFIED
Category: GPU compute marketplace / zero-knowledge proving
Automation: 5/5 technically, operational monitoring required

Economic mechanism:
- Requestors post proof requests; provers bid/lock requests, generate proofs, submit aggregated proof onchain and receive the request reward on successful verification.
- Separate Proof of Verifiable Work (PoVW) / “ZK Mining” mechanism rewards provers in ZKC for verified proving work, including proving work associated with Boundless market activity.
- CLI explicitly exposes prover, collateral and mining/staking-reward operations.

Server fit:
- Strong for GPU servers. Official quick-start explicitly describes deploying a prover to a GPU server.
- Recommended minimum documented configuration includes 16 CPU threads, 32 GB RAM, 200 GB SSD and NVIDIA GPU support; stack scales from single-GPU systems to clusters.

Capital / constraints:
- Market orders involve collateral; ZK mining also involves ZKC staking configuration.
- Profitability is utilization-sensitive and GPU-specific. Gross token rewards alone are insufficient.

Why it matters:
- This is a direct “machine does jobs -> receives money/token” market rather than passive token inflation only.

Next economics work:
- Pull live order/reward statistics, ZKC stake requirements, collateral/slashing rules, accepted GPU models, proof throughput and revenue per GPU-hour.

### 3. Succinct / SP1 decentralized prover network
Status: WATCHLIST / PARTIALLY VERIFIED
Category: ZK proving infrastructure
Automation potential: 5/5

Current evidence:
- Official current Succinct documentation advertises a decentralized prover network and mainnet explorer, confirming the network/service is live enough to remain a serious candidate.
- This pass did not obtain sufficiently detailed current primary documentation on open prover admission, reward formula, collateral or hardware requirements.

Classification:
- Do NOT yet assume that any user can attach a GPU server and earn.
- Retain as high-priority validation target; distinguish public proof-service usage from permissionless supply-side prover participation.

### 4. SQD / Subsquid worker/indexer roles
Status: WATCHLIST / UNVERIFIED FOR CURRENT PERMISSIONLESS EARNINGS
Category: decentralized data/indexing infrastructure
Automation potential: 5/5 if supply role is open

Current evidence:
- Current official docs clearly document indexing/network APIs and running indexers, but searches surfaced older testnet quest/reward material rather than a clear current mainnet “run worker -> receive SQD” supply-side guide.

Classification:
- Do not count generic SQD Cloud deployments as mining/earning; running an indexer for your own app is a cost unless a separate network role pays it.
- Requires direct validation of current worker role, bonding/delegation, reward source and admission.

### 5. Chainlink node operator / data-provider opportunity
Status: RESTRICTED
Category: oracle infrastructure / data monetization
Automation: 4–5/5 operationally

Economic mechanism:
- Official Chainlink material says node operators provide oracle computation and can earn revenue; data/API providers can monetize existing APIs through Chainlink.
- The framework itself is described as permissionless and anyone can technically run a Chainlink node.

Critical accessibility distinction:
- Running the software is not equivalent to being selected into high-value production oracle networks.
- Current Chainlink material emphasizes professional/institutional operators and Sybil-resistant known reliable operators for major services; historical Oracle Olympics onboarding also selected participants for production feeds.
- Therefore this is not yet a “spin up anonymous VPS tonight and automatically receive jobs” opportunity.

Capital / risk:
- Production participation may require reputation, contracts/admission and substantial operational standards.
- Node-operator staking economics are distinct from ordinary community LINK staking; current staking pages show separate operator stake parameters but this should not be mistaken for open admission to paid DON work.

Best fit for project:
- Restricted professional infrastructure opportunity.
- Separate BUILD-ONCE variant: create a valuable external data/API business and sell data through oracle infrastructure.

### 6. Gelato executor / node supply side
Status: RESTRICTED / ACCESS NOT PROVEN OPEN
Category: transaction automation / relayer / verifier infrastructure
Automation: 5/5

Current evidence:
- Gelato docs confirm users pay fees that incentivize Gelato Nodes to run off-chain computation and execute transactions.
- Current docs expose Gelato-hosted executor/relay products and generic rollup/full-node deployment guides.
- Verifier-node packages exist where projects can sell/require node licenses and reward community verifier operators.

Critical distinction:
- Documentation found in this pass does NOT establish that an arbitrary external operator can join Gelato’s core executor network permissionlessly and earn transaction fees.
- Running an OP/Orbit full node from a Gelato guide by itself is non-paying.

Classification:
- Core Gelato executor: RESTRICTED pending explicit operator-admission evidence.
- Gelato-powered verifier-node projects: a separate candidate family; earnings depend on each project’s node-license/reward design.

### 7. CoW Protocol solver / intent competition
Status: WATCHLIST
Category: solver / intent execution / algorithmic market-making service
Automation: 5/5 conceptually

Current evidence:
- Official docs confirm CoW Protocol uses combinatorial batch auctions and a solver-based architecture is central to price finding, but this pass did not obtain enough current official detail on permissionless solver onboarding, bonding, reward/fee schedule and eligibility.

Classification:
- Keep as high-priority machine-to-machine service-market candidate.
- Do not model as passive income: solver profitability may require sophisticated routing, liquidity access, capital, gas management and competitive optimization.

### 8. Streamr Operator
Status: VERIFIED
Category: server-native bandwidth/data relay + stake
Automation: 5/5

Economic mechanism:
- Operators run Streamr nodes, stake DATA into funded Sponsorship contracts, relay sponsored streams and earn the DATA released by Sponsorships.
- Node software automatically performs operator-value maintenance, inspections and flag review/voting when selected.
- Delegators can provide additional DATA stake; operator takes a configurable owner cut from earnings.

Server fit:
- Strong. Official docs recommend roughly 4–8 GB RAM, 3–4 virtual cores, ~1 Gbps bandwidth, a public IP and open TCP/WebSocket port.
- Docker or npm deployment is supported. Many nodes may share an IP, though one node per machine is recommended.

Capital / constraints:
- Earning requires staking DATA; operator must self-own at least 5% of Operator stake.
- Node wallet needs POL for transactions.
- Stake is slashable for failing promised relay work or incorrect flagging/voting behavior.

Why it matters:
- Excellent match to the project: low/moderate server requirements, continuous daemon operation, protocol-defined paid relay work, near-autonomous maintenance/validation.

Next economics work:
- Collect live Sponsorship funding, total competing stake, effective yield, operator-cut market and revenue per unit stake/server.

## New/strengthened economic mechanism families from this run
1. Proof-of-relay RPC provider with service-specific stake and QoS/reputation weighting (Lava).
2. Open proof-order auction + GPU proving + collateral (Boundless market).
3. Protocol-level proof-of-work incentive layered on top of useful ZK computation (Boundless PoVW/ZK mining).
4. Sponsored data-relay pools where operators stake into customer-funded streams (Streamr Sponsorships).
5. Professional oracle/data-provider business where node execution may be technically open but paid production selection is reputation/admission constrained (Chainlink).
6. Project-specific licensed verifier nodes sold through node-launch infrastructure (Gelato verifier-node package family).
7. Competitive solver/intent markets as a distinct autonomous service class requiring algorithmic edge rather than raw hardware alone (CoW and peers).

## Important negative findings / anti-hype rules
- “Can run a node” does not imply “node earns.” Generic Chainlink, Gelato rollup-node and SQD indexer software must not be counted as income without a current reward path.
- “Network is decentralized” does not imply supply admission is permissionless.
- Stake-dependent service networks must be modeled as hybrid infrastructure + capital opportunities, not zero-capital VPS mining.
- Solver systems are closer to automated businesses/trading infrastructure than passive mining if they require proprietary optimization and inventory/capital.
- Testnet quests/points are not recurring income unless a current mainnet conversion/reward mechanism is documented.

## Priority candidates still unresolved from Run 003 scope
- Succinct/SP1 open prover admission and economics.
- SQD current mainnet worker/indexer supply rewards.
- CoW solver onboarding/rewards/bonding.
- Chainlink production node admission path versus merely running node software.
- Gelato core executor admission.
- Gevulot, Cysic, Lagrange current paid mainnet proving roles versus testnet/points.
- Meson bandwidth marketplace/node economics.
- Presearch node rewards and current server eligibility.
- Other intent/solver systems: 1inch Fusion resolvers, UniswapX fillers, Across relayers, LI.FI solver/intent supply roles, Bebop/Jam/Ruban style solvers where applicable.

## Run conclusion
Run 003 materially expanded and refined the server-native universe. Lava, Boundless and Streamr are validated high-value research targets matching the autonomous-server thesis. Chainlink/Gelato remain economically real but operator accessibility is constrained or unproven. SQD, Succinct and CoW remain watchlist items pending primary-source admission/economics validation.

The project is FAR FROM COMPLETE. Saturation passes completed: 0.
