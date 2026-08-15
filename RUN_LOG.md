# Research Run Log

## Run 001 — 2026-08-15
Status: **completed**
Stage: Foundation + broad seed discovery

### Work performed
- Confirmed repository was empty and initialized persistent research structure.
- Defined mission, prioritization, safety constraints, evidence hierarchy, economics framework and saturation/completion rules.
- Built initial taxonomy spanning:
  - server-native compute/GPU/AI;
  - storage;
  - bandwidth/relay/CDN/VPN;
  - validators/RPC/indexing;
  - ZK/prover markets;
  - keepers/solvers;
  - proof-of-work;
  - machine-to-machine task markets;
  - residential/device resource sharing;
  - physical DePIN;
  - capital yield;
  - automated trading families;
  - build-once digital businesses;
  - royalties/referrals/asset rental;
  - rejected/adjacent categories.
- Seeded dozens of named candidate projects plus many mechanism families.
- Performed first current-web validation batch using primary sources.

### Current verified examples from primary sources
- Golem provider
- Akash provider
- Vast.ai host
- Nosana GPU provider
- Golem GPU provider
- Bittensor miner mechanism
- Livepeer orchestrator
- Filecoin storage provider
- Sia storage provider
- Storj storage provider
- EarnApp residential bandwidth model + explicit prohibition on VM/Docker/hosting/cloud/server monetization
- Honeygain passive bandwidth model (server policy still unresolved)
- Salad resource-sharing model

### Important findings
1. “Runs on Linux” is not enough to classify something as server-native; ToS must explicitly allow the environment.
2. There are at least four fundamentally different economic families already visible: selling machine resources, performing protocol-defined jobs/services, risking capital/stake, and building an asset/service that later runs autonomously.
3. AI/DePIN marketing frequently hides the actual paid commodity; catalog must classify by what buyers/protocols actually reward.
4. Some promising server-native opportunities require infrastructure rather than a cheap single VPS (e.g. Kubernetes providers, GPU hosts, active-set/stake systems).
5. Bittensor should be treated as an ecosystem of many subnet-specific markets, not one opportunity.

### Sources added
See `SOURCES.md` for primary-source register.

### Output files created
- START_HERE.md
- METHODOLOGY.md
- CATALOG.md
- SOURCES.md
- STATUS.md
- HANDOFF.md
- RUN_LOG.md

### Next stage
Run 002: broad expansion of server-native opportunity universe, with special attention to missing GPU/AI providers, relay/CDN/VPN nodes, RPC/indexing/oracles, ZK/provers, keepers/solvers and DePIN directories.

### Saturation metrics
- Control/saturation passes completed: 0
- New mechanisms in this run: many
- New named candidates in this run: many
- Conclusion: nowhere near saturation; continue.

---

## Run 002 — 2026-08-15
Status: **completed**
Stage: Server-native opportunity expansion

### Work performed
- Expanded the primary server-native universe using current official documentation.
- Validated/clarified Mysterium, Pocket Network Supplier, Pocket commercial Gateway, The Graph Indexer, Aztec Prover, Aethir Checker, Render Node Operator/Compute Client and NKN Proof-of-Relay roles.
- Separated pure server work from hidden capital/license requirements.
- Added new economic subfamilies: paid RPC supplier, commercial decentralized API gateway, licensed checker/verifier, mainnet ZK prover, and hybrid work+stake infrastructure.
- Recorded high-priority unresolved leads for Lava, Subsquid, Boundless/RISC Zero, Succinct/SP1, Gevulot/Cysic/Lagrange, Chainlink, Gelato, CoW/intent solvers, Meson, Streamr and Presearch.

### Important findings
1. Mysterium is a genuine positive example of datacenter/VPS-permitted paid relay infrastructure; this contrasts with EarnApp's explicit server prohibition.
2. Pocket's Shannon model is usage-backed: supplier earnings require actual proven relays, but the current documented supplier stake is substantial.
3. Pocket also exposes a distinct BUILD-ONCE opportunity: commercial gateways can sell RPC service and retain the margin after protocol/infrastructure cost.
4. The Graph is server-native but capital-heavy due to the current 100,000 GRT indexer self-stake requirement.
5. Aztec currently documents mainnet prover reward claiming, proving that ZK proving belongs in the live opportunity universe; however hardware requirements are data-center grade.
6. Aethir Checker can run on an ordinary VPS with very small compute requirements, but the earning right comes from a Checker license NFT/delegation, so ROI must be split into infrastructure versus license capital.
7. Render node/operator rewards for work and availability are current, but onboarding and arbitrary cloud-GPU eligibility remain unresolved.
8. Relay/proxy/VPN nodes need a legal/abuse-risk dimension separate from technical and financial ROI.

### Durable outputs
- `research/RUN_002_SERVER_NATIVE_EXPANSION.md`
- `research/SOURCES_RUN_002.md`
- `STATUS.md` advanced to Run 003 priority.

### Next stage
Run 003: RPC/indexer/oracle + ZK/prover + keeper/solver expansion, prioritizing Lava, Subsquid, Boundless/RISC Zero, Succinct/SP1, Gevulot/Cysic/Lagrange, Chainlink operator accessibility, Gelato executors and CoW/intent solvers.

### Saturation metrics
- Control/saturation passes completed: 0
- Newly validated roles/mechanisms: several
- New taxonomy refinements: at least 5
- Conclusion: still far from saturation; continue.

---

## Run 003 — 2026-08-15
Status: **completed**
Stage: RPC / oracle / ZK prover / keeper-solver expansion

### Work performed
- Validated Lava Network RPC Provider as a strong server-native paid relay opportunity using current official provider/reward docs.
- Validated Boundless/RISC Zero as a live GPU-server proof marketplace plus protocol-level ZK mining/PoVW mechanism.
- Validated Streamr Operator as a modest-hardware server-native sponsored data-relay role with stake/slashing and highly automated node maintenance.
- Clarified Chainlink node/data-provider economics versus production-network admission constraints.
- Clarified Gelato core-node fee economics versus lack of proof that arbitrary external operators can join the core executor set; separated project-specific verifier-node licenses as a distinct family.
- Kept Succinct/SP1, SQD/Subsquid and CoW solver roles on watchlist because current primary evidence was insufficient to prove open paid supply-side admission/economics.
- Added anti-hype rule: running node/indexer software is not an earning opportunity unless a current reward path is proven.

### Important findings
1. Lava closely matches the target thesis: continuous machine-to-machine RPC work, cryptographic relay proofs, service-specific stake and rewards affected by QoS/reputation.
2. Boundless is a particularly strong “bot/miner-like” candidate: GPU servers compete for useful proof jobs and can also participate in ZKC PoVW mining, but collateral/stake and utilization must be modeled.
3. Streamr is another strong fit: operators run persistent nodes, relay sponsored streams and earn DATA; software automatically performs recurring maintenance and network inspections.
4. Oracle/keeper ecosystems frequently separate technical permissionlessness from economic admission. A node can be runnable without being automatically eligible for production revenue.
5. Testnet quests/points and generic full-node tutorials must never be counted as passive income without current mainnet rewards.
6. Solver/intent markets deserve their own category because profit can depend on algorithms, liquidity/capital and competitive execution rather than raw CPU/GPU supply.

### Durable outputs
- `research/RUN_003_RPC_ZK_KEEPERS_SOLVERS.md`
- `research/SOURCES_RUN_003.md`
- `STATUS.md` advanced to Run 004 priority.

### Next stage
Run 004: finish unresolved prover/indexer/solver candidates (Succinct, SQD, CoW, Gevulot, Cysic, Lagrange), then broaden into Meson/Presearch and other intent/relayer markets such as 1inch Fusion resolvers, UniswapX fillers and Across relayers.

### Saturation metrics
- Control/saturation passes completed: 0
- Newly validated strong server-native roles: Lava RPC Provider, Boundless prover/ZK miner, Streamr Operator
- Newly refined restricted/watchlist roles: Chainlink, Gelato, Succinct, SQD, CoW
- New mechanism-family refinements: proof-order auctions, useful ZK PoW, sponsored data relay, professional oracle admission, licensed verifier nodes, competitive solver markets
- Conclusion: project remains far from saturation; continue.
