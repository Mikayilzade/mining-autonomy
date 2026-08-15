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
Runs 001–005 are complete.

Latest files:
- `research/RUN_005_COMPUTE_STORAGE_EXPANSION.md`
- `research/SOURCES_RUN_005.md`

### Run 005 strong validated additions
- **io.net Supplier / IO Worker**: live GPU/CPU supplier path with customer compute-job payments plus hourly block rewards. Current official docs state 0.25% fee on worker earnings, no fee on block rewards, device-specific $IO stake for reward/Cluster Ready eligibility, 14-day unstake cooldown and slashing framework.
- **Clore.ai Host**: live GPU-server rental marketplace. Host sets on-demand and spot pricing. Current base host fee share is 5% on-demand and 1.25% spot; renter payments in BTC/USDT/USDC add a 15% host-side fee unless reduced through MFP Lock. Server/bare-metal hosting is explicitly part of the product.
- **Swarm Bee Full Node**: full node can earn two distinct streams: storage Redistribution Game rewards and SWAP bandwidth incentives. Current docs require at least 10 xBZZ baseline stake for storage incentives and explicitly describe that stake as non-refundable; bandwidth incentives are available to full nodes without that storage-game stake. Current recommended full-node specs are roughly dual-core 2 GHz, 8 GB RAM, 30 GB SSD and stable high-speed internet.

### Important modeling lessons from Run 005
- Separate actual customer-paid utilization from token emissions/subsidies.
- Treat stake differently depending on reversibility: io.net has cooldown/slashing exposure; Swarm baseline storage stake is non-refundable; Clore fee optimization can require optional token holdings/locks.
- Distinguish expensive dedicated-GPU server opportunities from low-spec VPS daemons even when both are server-native.
- One node may expose multiple paid resources; model each revenue stream independently before combining them.

## Run 006 priority
Finish unresolved compute/storage/relay expansion before moving to the Bittensor/decentralized-AI sweep:
1. Lagrange proving/operator opportunities.
2. Meson bandwidth/CDN provider economics.
3. TensorDock host/provider program status.
4. Hyperbolic provider status.
5. RunPod community/provider program status.
6. Render provider onboarding/cloud-host eligibility.
7. Salad server/datacenter restrictions.
8. Arweave current mining/storage roles.
9. Crust, ScPrime and Autonomi production rewards.
10. Additional server-permitted relay/CDN/VPN networks.

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

Do not infer profitability from token APY, headline rewards, or generic node tutorials.

## Non-negotiable exclusions
Do not operationalize CAPTCHA bypass, fake engagement, ad fraud, spam, prohibited multi-accounting, KYC/geofence evasion, unauthorized access/scraping, cryptojacking or deceptive/illegal activity.

## Completion
Only mark `COMPLETE` after repeated broad + niche saturation passes stop producing new independent mechanisms and produce negligible new viable projects. Document final control passes in RUN_LOG and disable the recurring research task only then.
