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
   - latest run-specific files named in STATUS.
3. Trust repository state over remembered chat state.
4. Continue from `STATUS.md -> Next run priority`.
5. Search the live web because platform rules, rewards, availability and economics are time-sensitive.
6. Prefer primary sources for validation.
7. Update run-specific research/source files plus STATUS, RUN_LOG and this HANDOFF before ending the run. Avoid unsafe whole-file replacement of the central catalog if its full current contents cannot be fetched reliably.

## User intent
The user wants an exhaustive theoretical inventory first, implementation later.

Primary target: autonomous online/server bots/nodes/services that can continuously earn from legitimate simple work with minimal input.

Secondary target: all other passive/semi-passive income mechanisms, including home compute/storage/bandwidth, physical DePIN, capital-based yield, and systems that become passive after initial creation/investment.

Weak, restricted, rejected and dead options must stay documented so later runs do not rediscover and re-hype them.

## User interaction preference
Unless the user asks a substantive question, report only `в процессе` while unfinished and `завершено` only when completion gate is genuinely met.

## Current durable checkpoint
Runs 001–007 are complete.

Latest files:
- `research/RUN_007_DECENTRALIZED_AI_BITTENSOR.md`
- `research/SOURCES_RUN_007.md`

### Run 007 strongest additions / confirmations
- **Bittensor must be modeled subnet-by-subnet**, not as one generic miner. Different subnets pay for different commodities and have different competition/cost structures.
- **Chutes SN64**: strong server-native GPU candidate. Current miner repo says incentives depend on compute time and inference bounties; Kubernetes/Gepetto stack automates workload operation.
- **Omron / Inference Labs SN2**: verifiable AI inference + ZK proof worker with published CPU/RAM/NVMe/network requirements, creating an important non-GPU-heavy AI family.
- **Nous Finetuning** and **Macrocosmos Pretraining**: competitive model-improvement families where miners publish models and TAO rewards follow validator-measured quality.
- **Macrocosmos IOTA**: distributed-training worker family; miners process activations in an orchestrated training pipeline, recommended current miner GPU >=16 GB VRAM.
- **Macrocosmos Apex SN1**: explicitly accepts humans and autonomous agents as solvers; winner-takes-all machine-scored competitions. Conceptually close to the desired autonomous software-worker model, but expected value is highly competitive.
- **Macrocosmos Mainframe**: scientific compute/optimization jobs, currently molecular dynamics, with top-K reward distribution.
- **TensorUSD SN113**: prediction-agent and liquidation-auction miner mechanisms; liquidation requires capital/token inventory and chain fees.
- **Allora workers**: current official docs confirm consumer-fee-funded inference/forecast worker rewards; **reputers** are a separate stake-dependent evaluation role.

### Run 007 restricted/watchlist outcomes
- **Macrocosmos Data Universe**: technically autonomous and rewarded, but implementation must remain RESTRICTED pending source-by-source lawful/ToS-compliant data acquisition. No unauthorized scraping.
- **Prime Intellect GPU provider**: supplier network exists, including individuals, but current onboarding is contact-based rather than clearly self-service.
- **Gensyn RL Swarm**: WATCHLIST, not current verified income. Current docs say official swarms/Gensyn-hosted nodes are paused; current published market material includes test-only rewards.
- **inference.net / Kuzco**: no sufficiently current official worker reward/onboarding source established in Run 007; keep UNVERIFIED/WATCHLIST.

### Important modeling lessons from Run 007
- Competitive AI networks require expected-emission modeling: `P(rank/reward) × reward - compute/API/data/registration costs`, not a simple hourly rate.
- Autonomous machine-scored competitions are a separate earning family from raw compute rental.
- Distributed training can monetize partial pipeline work rather than complete model delivery.
- A machine-readable autonomous worker can still be legally unsuitable if its upstream data collection violates source-platform rules or privacy law.
- Token emissions, customer fees, points/testnet units and capital-based spreads must never be merged into one “reward” number.

## Run 008 priority
Dedicated residential/device passive-income + bandwidth/IP/browser/device DePIN sweep:
1. Revalidate **EarnApp**, **Honeygain**, **Pawns.app**, **PacketStream**, **Grass**, **Nodepay**, **Dawn**, **Repocket**, **TraffMonetizer**, **EarnFM** and current successors/competitors.
2. For each, establish whether VPS/datacenter/cloud/VM/Docker operation is allowed, blocked or simply unsupported.
3. Record payout type (cash/token/points), minimum payout, KYC, country restrictions, Azerbaijan availability, device/IP limits, referral dependence and privacy/abuse risk.
4. Distinguish residential-IP monetization from generic bandwidth/CDN contribution.
5. Expand into browser extensions, phone/device background contribution, telemetry/measurement panels and low-resource DePIN clients with real rewards.
6. Identify dead, renamed, scammy or abandoned historical projects explicitly so they do not re-enter the queue.
7. Keep the run broad enough to discover new mechanism families, not only validate the seed list.

After Run 008 continue physical DePIN, capital yield, build-once systems, rejected/dead cross-checks, profitability normalization, Azerbaijan/KYC filtering and saturation/control passes.

## Research discipline
A runnable daemon is not enough. Prove all of the following separately:
- current reward path;
- supply-side admission;
- intended server/device environment allowed by docs/ToS;
- hidden stake/license/collateral;
- payout/reward mechanism;
- utilization or demand driver.

Examples already learned:
- EarnApp is not server-native because its policy prohibits VM/Docker/hosting/cloud/server monetization.
- 1inch resolver software may be technically automatable but profitable participation is restricted by resolver admission/stake.
- Across is permissionless but capital-heavy because relayers front liquidity.
- Succinct proving is permissionless, yet stake controls auction eligibility and missed deadlines can slash stake.
- io.net is server-compatible supply-side compute but required stake/hardware economics must be normalized per device.
- Swarm's low hardware requirement does not imply cheap participation because storage incentives carry non-refundable xBZZ stake and recurring gas/RPC costs.
- Autonomi is unusually close to the cheap-daemon target because virtual/headless operation and low per-node storage are explicitly supported, but real net revenue still requires measurement.
- ScPrime shows why protocol permissionlessness and customer-demand accessibility must be checked separately.
- Bittensor shows why a single ecosystem label can hide many fundamentally different earning mechanisms.
- Gensyn shows why a live/testnet technical contribution path must not be mistaken for current production income.

Do not infer profitability from token APY, headline rewards, points, or generic node tutorials.

## Non-negotiable exclusions
Do not operationalize CAPTCHA bypass, fake engagement, ad fraud, spam, prohibited multi-accounting, KYC/geofence evasion, unauthorized access/scraping, cryptojacking or deceptive/illegal activity.

## Completion
Only mark `COMPLETE` after repeated broad + niche saturation passes stop producing new independent mechanisms and produce negligible new viable projects. Document final control passes in RUN_LOG and disable the recurring research task only then.
