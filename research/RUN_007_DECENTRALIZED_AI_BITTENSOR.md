# Run 007 — Decentralized AI / Bittensor / inference / distributed training

Date: 2026-08-15
Status: **completed**
Phase: Universe construction

## Goal
Expand the AI-incentive universe beyond a generic `Bittensor miner` entry. Separate economically different autonomous worker families, validate current reward paths, and distinguish production earning from testnet/points/speculation.

## Core conclusion
Bittensor is not one opportunity. It is a meta-market containing many economically distinct miner jobs. For this project, the useful unit is the **subnet mechanism**, not Bittensor itself. Several currently documented subnets are unusually close to the desired autonomous-server model because the worker is software, jobs/scoring are machine-readable, and TAO emissions are programmatic.

## Validated / materially strengthened candidates

### 1. Bittensor generic miner framework — VERIFIED umbrella, not a standalone strategy
- Official OpenTensor material states subnet miners produce digital commodities and top performers receive TAO via Yuma Consensus.
- Subnets can pay for intelligence, storage, compute, protein folding, predictions and other commodities.
- Registration to a subnet is required and can involve a dynamic TAO registration/recycle cost.
- Automation: 5 at protocol level, but actual economics depend entirely on the subnet.
- Classification rule: never model `Bittensor mining` as one profitability line.

### 2. Chutes / Bittensor SN64 — VERIFIED GPU inference/compute miner
- Current miner repository explicitly says miners provide compute and incentives are based on total compute time, including first-provider inference bounties.
- Miner stack is designed for automation with Kubernetes, Ansible, API services and the Gepetto workload manager.
- One UID should aggregate capacity rather than multi-account/self-compete.
- Hardware can range from inexpensive GPUs to large H100 clusters.
- Economic type: TAO subnet emissions tied to useful inference compute/time, not ordinary cloud rental.
- Server-native: yes, strongly.
- Automation: 5 after deployment.
- Cost drivers: GPU rental/ownership, cluster operations, registration, network, idle capacity.
- Net test required later: emission share per GPU-hour vs cloud/owned-GPU cost.

### 3. Omron / Inference Labs Bittensor SN2 — VERIFIED verifiable-inference miner
- Miners receive AI inference jobs, generate outputs and zk proofs, and validators score proof integrity/performance.
- Current minimum published hardware is CPU-oriented: 8 cores, 32 GB RAM, 400 Mbps, 1 TB NVMe; recommended 64 GB+, 1 Gbps, 2 TB NVMe.
- Faster storage/network/CPU can increase rewards because scoring is performance-sensitive.
- This is important because it creates an AI-related reward path that is not necessarily GPU-only.
- Server-native: yes.
- Automation: 5.
- Key economics: TAO emission share vs CPU/NVMe/network cost and registration.

### 4. Nous Finetuning Subnet — VERIFIED model-finetuning competition miner
- Miners continuously fine-tune LLMs on changing synthetic data, publish models to Hugging Face, and commit metadata on-chain.
- Validators evaluate model quality; Yuma Consensus distributes TAO according to performance.
- Economic mechanism is competitive model improvement, not raw GPU-time rental.
- Server-native: yes, but likely GPU-heavy.
- Automation: 4–5; training/publishing can be automated, but winning requires continual strategy/model optimization.
- Risk: competition means compute spend does not guarantee emissions.

### 5. Macrocosmos Pretraining / Bittensor SN9 — VERIFIED pretrained-model competition
- Miners train and publish foundation models; validators compare losses on the Falcon Refined Web dataset.
- Highest-performing models receive TAO emissions through subnet weights/Yuma Consensus.
- Distinct mechanism from finetuning: pretraining/model-quality race.
- Server-native: yes.
- Automation: 4–5.
- Economics: extremely competition/compute sensitive; not a low-cost VPS candidate.

### 6. Macrocosmos IOTA — VERIFIED distributed-training worker family
- IOTA describes permissionless heterogeneous miners processing activations for orchestrated training.
- Miners compete to process as many activations as possible; validators spot-check work.
- Current public run recommends CUDA GPU with >=16 GB VRAM and Ubuntu 22.04; project had a March 2026 release.
- Important distinct family: paid/incentivized **pipeline/distributed training contribution**, rather than submitting a complete model.
- Server-native: yes.
- Automation: 5.
- Economics still need exact subnet/reward normalization in a later profitability phase.

### 7. Macrocosmos Data Universe / Bittensor SN13 — VERIFIED data miner, LEGAL/ToS SENSITIVE
- Miners collect/store fresh desired web/social data and are scored on data value, freshness, rarity and credibility.
- Rewards favor useful, non-duplicated, current data.
- The project has an explicit miner data-compliance policy requiring lawful processing, platform-ToS compliance and GDPR awareness.
- Server-native technically: yes.
- Automation: 5 technically.
- Project classification: **RESTRICTED for our implementation shortlist** until each data source can be operated lawfully and within source-platform rules. We will not use unauthorized scraping or ToS evasion.

### 8. Macrocosmos Apex / Bittensor SN1 — VERIFIED autonomous solver/agent competition
- Current Apex docs describe a general problem market where human or autonomous-agent solvers submit solutions to measurable competitions.
- Rewards are winner-takes-all to the top-ranked submission for a competition.
- The project explicitly describes agentic mining and autonomous agents as valid solvers.
- This is one of the closest conceptual matches to `software bot does machine-scored jobs for money`, but it is competitive rather than guaranteed piecework.
- Server-native: yes.
- Automation: potentially 5.
- Economics: expected reward = probability of holding #1 score × emissions − inference/compute/API/experiment costs.

### 9. Macrocosmos Mainframe — VERIFIED scientific-compute competition miner
- Current mechanism includes molecular-dynamics jobs in a global job pool.
- Miners compete on all challenges and upload results for validation.
- Top-K miners are paid; current docs describe 80% of a challenge reward to rank #1 and 20% split among the remaining top-K.
- Distinct family: scientific optimization / simulation mining.
- Server-native: yes, typically compute-heavy.
- Automation: 5 after a competitive solver is built.

### 10. TensorUSD Bittensor SN113 — VERIFIED prediction/liquidation miner, CAPITAL-ASSISTED
- Current repo says miners can earn TAO through liquidation auctions and prediction-agent mechanisms.
- Liquidation mechanism requires TUSDT inventory and incurs on-chain transaction costs.
- Prediction-agent path is more software-native; liquidation is capital-native + bot infrastructure.
- Server-native: yes.
- Automation: 4–5.
- Classification: split into (a) autonomous prediction agent and (b) capitalized liquidation/auction bot.

### 11. Allora workers — VERIFIED non-Bittensor inference/forecast worker
- Current official docs state consumers pay fees and workers are rewarded based on the quality/unique contribution of their inferences.
- Separate worker types include inference workers and forecast workers.
- This is a real machine-readable prediction/inference earning family.
- Server-native: yes in principle; deployment and topic-specific worker logic required.
- Automation: 5.
- Economics: topic reward pool × marginal forecast/inference contribution − compute/data/API cost.

### 12. Allora reputers — VERIFIED, stake-dependent
- Reputers calculate losses against ground truth and are rewarded for accurate reports relative to consensus.
- Reputers secure topics with stake; delegated stake can increase influence.
- Server-native: yes.
- Automation: 5.
- Classification: hybrid service + capital/stake, not a zero-capital bot.

### 13. Prime Intellect GPU provider — RESTRICTED / curated
- Current official FAQ confirms Prime Intellect is expanding a network of both individual GPU providers and cloud platforms.
- Supplier onboarding is currently contact-based rather than a clearly self-service public daemon path.
- Platform's consumer side has full API automation for provisioning compute, but that does not prove open supplier automation.
- Keep as RESTRICTED provider opportunity; not a cheap VPS bot.

### 14. Gensyn RL Swarm / compute contribution — WATCHLIST, currently not production income
- Current docs show the public testnet and permissionless compute contribution concept.
- However current Gensyn pages say previous RL Swarm/Gensyn-hosted nodes are paused and there are no official swarms running right now.
- Delphi currently uses test-only `$TEST` in the published docs.
- Therefore do **not** count current RL Swarm participation as verified cash/token income in this project.
- Classification: WATCHLIST until mainnet/current reward path is explicit.

## Important unresolved / negative result
### inference.net / Kuzco
The planned direct validation did not produce sufficiently strong current official worker-reward documentation in this pass. Do not promote it to VERIFIED from historical reputation. Keep WATCHLIST/UNVERIFIED until a current official provider/reward path is located.

## New economic families added by this run
1. GPU inference-emission miner (Chutes).
2. zk-verifiable inference miner (Omron).
3. continuous model-finetuning competition.
4. full-model pretraining competition.
5. pipeline/distributed-training activation worker (IOTA).
6. machine-scored autonomous agent/solver competitions (Apex).
7. scientific simulation/optimization competitions (Mainframe).
8. data freshness/rarity mining with compliance constraints (Data Universe).
9. prediction-agent subnet miner.
10. capitalized liquidation-auction miner.
11. inference/forecast workers paid by consumer-fee pools (Allora).
12. staked inference-reputation worker (Allora reputer).

## Architecture implications for the eventual autonomy system
The future orchestrator should not only ask `which platform pays most?`; for competitive AI networks it must evaluate:
- expected emission share;
- registration cost and UID survival risk;
- GPU/CPU-hours required to remain competitive;
- rank volatility;
- whether rewards are customer-paid, protocol emissions, or both;
- autonomous optimization loop feasibility;
- model/API costs external to the worker daemon;
- stake/collateral;
- legal/data-source constraints.

Potential future strategy: a portfolio orchestrator may move compute between deterministic rental markets and competitive subnet mining based on measured trailing net revenue per GPU-hour.

## Safety / ToS outcomes
- Bittensor subnets that explicitly accept autonomous miners/agents are compatible with project scope.
- Data-mining subnets are not automatically acceptable: source-platform ToS and privacy law still govern acquisition.
- No CAPTCHA bypass, fake activity, unauthorized scraping or identity/account evasion will be used.

## Saturation status
Saturation/control passes completed: **0**.
This run found many genuinely new independent earning mechanisms, so the research remains far from saturation.

## Next run
Run 008 should move to **residential/device passive income + bandwidth/IP/browser/device DePIN**, validating actual cash/token payouts, VPS prohibitions, multi-device limits, KYC/geography, payout thresholds and whether Azerbaijan is supported. It should include EarnApp, Honeygain, Pawns.app, PacketStream, Grass, Nodepay, Dawn, Repocket, TraffMonetizer, EarnFM and current successors/competitors, plus explicit dead/scam checks.
