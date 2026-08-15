# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read, in order:
   - `START_HERE.md`
   - `STATUS.md`
   - `METHODOLOGY.md`
   - `HANDOFF.md`
   - `RUN_LOG.md`
   - `CATALOG.md`
   - `SOURCES.md`
   - latest files in `research/` named in STATUS/RUN_LOG
3. Trust repository state over remembered chat state.
4. Continue from `STATUS.md -> Next run priority`.
5. Search the live web because platform rules, rewards, availability and economics are time-sensitive.
6. Prefer primary sources for validation.
7. Update the catalog/evidence/status/log before ending the run. If the central catalog is too large for a safe whole-file replacement, create a durable run-specific catalog/source file under `research/`, then point STATUS and RUN_LOG to it rather than risking data loss.

## User intent
The user wants an exhaustive theoretical inventory first, implementation later.

Primary target: autonomous online/server bots/nodes/services that can continuously earn from legitimate simple work with minimal input.

Secondary target: all other passive/semi-passive income mechanisms, including home compute/storage/bandwidth, physical DePIN, capital-based yield, and systems that become passive after initial creation/investment.

The aim is not to force a favorite idea. Keep weak, restricted and rejected options documented so future runs do not rediscover and re-hype them.

## User interaction preference for this research loop
When the user sends `го`, continue the next research stage. Unless the user asks a substantive question, keep chat output minimal: `в процессе` while unfinished, `завершено` only when the completion gate is genuinely met.

## Run sizing
Work in medium coherent passes and save durable checkpoints. The user's ideal is roughly half-hour-sized research stages rather than tiny minute-by-minute fragments or fragile marathon runs. If a prior stage was clearly too small, broaden the next one.

## Current durable checkpoint
Runs 001–003 are complete.

Latest detailed files:
- `research/RUN_003_RPC_ZK_KEEPERS_SOLVERS.md`
- `research/SOURCES_RUN_003.md`

Run 003 strong validated additions:
- Lava RPC Node Provider: continuous paid relay service with proof-of-relay, QoS/reputation and per-service LAVA stake.
- Boundless/RISC Zero: live proof-order market plus PoVW/ZK mining on GPU servers; collateral/stake and utilization matter.
- Streamr Operator: server-native sponsored data relay with DATA stake, modest hardware requirements and automated recurring maintenance/inspection.

Run 003 restricted/watchlist clarifications:
- Chainlink: node/data-provider revenue is real, but production oracle revenue is not automatically available merely by running software.
- Gelato: nodes receive execution fees but arbitrary operator admission to the core executor network was not proven; project-specific verifier-node licensing is a separate family.
- Succinct/SP1: decentralized prover network exists; open prover admission and economics unverified.
- SQD/Subsquid: indexing infrastructure exists; current permissionless paid worker role not yet proven.
- CoW: solver/intent architecture is relevant; exact current solver onboarding/bond/reward rules still need validation.

Run 004 priority:
1. Succinct/SP1 admission and economics.
2. SQD/Subsquid paid mainnet worker/indexer roles.
3. CoW solver onboarding/bonding/rewards.
4. Gevulot, Cysic, Lagrange paid proving versus testnet/points.
5. Meson node/bandwidth economics.
6. Presearch node rewards/server eligibility.
7. Other intent/relayer markets: 1inch Fusion resolvers, UniswapX fillers, Across relayers and similar.
8. Revisit Chainlink/Gelato only if stronger primary operator-admission evidence is found.

## Hourly automation
An hourly continuation task is active. Each scheduled run should read repository state first and continue from there. If repository status becomes `COMPLETE`, no further research should be performed and the recurring task should be disabled.

## Non-negotiable exclusions
Do not operationalize CAPTCHA bypass, fake engagement, ad fraud, spam, prohibited multi-accounting, KYC/geofence evasion, unauthorized access/scraping, cryptojacking or other deceptive/illegal activity.

## Research discipline
A technically possible server installation is not enough. Confirm that platform policy permits the intended environment. Example already learned: EarnApp technically has software clients but explicitly prohibits VM/Docker/hosting/cloud/server monetization, so it belongs in residential/device research rather than server-native research.

Also separate server cost from required stake/license/collateral. A cheap VPS does not make an opportunity low-capital if participation rights require an expensive NFT/token stake.

Do not infer earning from generic node/indexer tutorials. Prove a current reward path and supply-side admission separately.

## Completion
Only mark `COMPLETE` after repeated broad + niche saturation passes stop producing new independent mechanisms and produce negligible new viable projects. Document those final control passes in `RUN_LOG.md`.
