# Run 005 — Compute / GPU + storage expansion

Date: 2026-08-15
Status: **completed partial expansion stage**

This run advances the decentralized compute/GPU and storage branch with current primary-source validation. It is not a saturation pass and does not complete the project.

## 1. io.net Supplier / IO Worker — VERIFIED

### Economic role
Suppliers provide GPU/CPU compute through IO Worker. Earnings have two distinct components:
1. payments for actual compute jobs;
2. hourly block rewards for eligible workers.

Official docs state worker earnings are paid in IO Coin. Ordinary worker earnings incur a 0.25% fee; block rewards incur no fee.

### Admission / stake
Device onboarding is live. Devices must satisfy minimum requirements and pass Proof-of-Work verification to become job-ready. Current staking docs say suppliers must stake a device-specific amount of $IO for block-reward eligibility; the required amount is shown in the UI. Unstaking starts a 14-day cooldown. Slashing exists for malicious/non-compliant behavior.

A current support article also states staking is required for a worker to become Cluster Ready and that staking more than the required amount does not increase rewards.

### Automation
**Automation level: 5** once installed and monitored. The worker runs continuously, can receive compute jobs, and participates in hourly block-reward evaluation. This is an infrastructure daemon rather than a human microtask bot.

### Server-native classification
**SERVER-NATIVE / dedicated compute host candidate.** Linux workers are supported and the network explicitly targets GPU/CPU suppliers. Exact ordinary-VPS viability depends on whether the VPS exposes supported hardware; practical deployments are more likely dedicated/bare-metal GPU servers than cheap virtual CPUs.

### Revenue drivers
- hardware multiplier / processor quantity;
- connectivity tier;
- uptime / Proof-of-Timelock;
- successful Proof-of-Work verification when not hired;
- actual compute-job utilization;
- current emissions and number/score of competing eligible devices.

Job payments are made immediately for jobs completed within one day or daily for longer jobs. A worker that is unavailable during a cluster process can lose payment for that time; stopping in the first hour results in no payment for that period.

### Main risks / unknowns
- device-specific stake capital;
- $IO token-price exposure;
- reward emissions decline over time;
- utilization may be low;
- slashing / failed reward blocks;
- supported-device and connectivity requirements need hardware-by-hardware normalization;
- KYC/geography/Azerbaijan availability still needs dedicated account-policy verification.

### Profit formula
`Net = compute-job earnings + block rewards - 0.25% worker fee - server/GPU rental or depreciation - electricity - bandwidth - stake opportunity cost - withdrawal/chain costs - expected slashing/failed-reward losses - maintenance`

### Verdict
One of the stronger Tier-A candidates. It combines customer-paid compute with network emissions, but cannot be judged profitable until we compare real hardware cost, required stake and recent utilization.

---

## 2. Clore.ai Host — VERIFIED

### Economic role
Clore.ai is a decentralized GPU marketplace. A host installs Clore hosting software, lists a server, sets on-demand and spot pricing, and earns when renters use the machine.

### Host fees
Current official host-fee docs:
- On-demand marketplace fee: 10% total, split 5% renter / 5% host.
- Spot marketplace fee: 2.5% total, split 1.25% renter / 1.25% host.
- CLORE-denominated renter payments: no additional host fee.
- BTC / USDT / USDC renter payments: additional 15% host fee unless reduced through MFP Lock.

PoH holdings can reduce the base fee by up to 50%. MFP Lock can reduce the extra non-CLORE host fee, potentially to zero when all tiers are fully locked. These mechanisms add capital/token exposure and should not be assumed in baseline economics.

### Hardware / admission
Official FAQ says there are no hard-coded minimum specs, but at least one NVIDIA GPU plus stable internet is recommended; better GPUs, RAM, NVMe and networking attract more renters. Hosts install the software, connect it to the account, configure price/visibility and publish the server.

### Automation
**Automation level: 5** after deployment. The host can remain listed and serve renters continuously; pricing can be updated programmatically through server settings/API mechanisms. Operational monitoring is still necessary.

### Server-native classification
**SERVER-NATIVE, especially dedicated/bare-metal GPU servers.** Clore documentation explicitly describes hosting servers and also has a bare-metal/partner system for major hardware providers.

### Revenue drivers
- listed daily price;
- on-demand vs spot mix;
- utilization;
- GPU model / RAM / disk / bandwidth attractiveness;
- currency used by renter because host fees differ materially;
- PoH/MFP capital position and bonus/reward rules;
- server rating / uptime.

### Main risks / unknowns
- utilization and achievable market clearing price;
- token-price exposure for CLORE-denominated components;
- extra host fee when renters use BTC/USDT/USDC;
- capital lock if optimizing fees through PoH/MFP;
- account/KYC/geography policy still needs Azerbaijan-specific validation;
- security risk from hosting arbitrary renter workloads must be included operationally.

### Profit formula
`Net = rental revenue + host/reward bonuses - marketplace host share - non-CLORE extra host fee - hardware/server cost - electricity - bandwidth - depreciation - token-lock opportunity cost - maintenance/security cost - withdrawals/taxes`

### Verdict
Strong Tier-A GPU-marketplace candidate. Easier economic model than token-only mining because demand comes from renters, but utilization and fee mix determine profitability.

---

## 3. Swarm Bee Full Node — VERIFIED

### Economic role
A Bee full node stores and relays Swarm data and has **two separate earning mechanisms**:
1. storage incentives via the Redistribution Game;
2. bandwidth incentives through SWAP.

### Storage rewards
Users buy postage stamps in xBZZ to pay for storage. Collected xBZZ is redistributed to storage nodes. Every 152 Gnosis Chain blocks one neighborhood is selected; a node in that neighborhood can win the reward. Winner probability is weighted by stake density.

Current docs require:
- full Bee node;
- fully synced state;
- high-performance Gnosis RPC endpoint;
- minimum 10 xBZZ non-refundable stake for storage incentives;
- recurring xDAI for on-chain transactions.

Reserve doubling uses 20 xBZZ. The docs explicitly warn the normal stake is non-refundable, although partial withdrawals may become available above the protocol-defined minimum.

### Bandwidth rewards
Full nodes can also earn bandwidth incentives through the Swarm Accounting Protocol (SWAP). These do **not** require the xBZZ storage-incentive stake. Nodes account for forwarded data and can settle via cheques/chequebook contracts on Gnosis Chain.

### Hardware
Current official getting-started guidance for a full node recommends roughly:
- recent 2 GHz dual-core CPU;
- 8 GB RAM;
- 30 GB SSD;
- high-speed stable internet.

For storage-incentive participation, performance should be tested with `/rchash`. An RPC endpoint is required for chain interactions; self-hosted or private/paid RPC is preferred over rate-limited public endpoints.

### Automation
**Automation level: 5.** Bee is a long-running daemon and the redistribution/SWAP logic is protocol-native. Monitoring, updates and funding top-ups are still required.

### Server-native classification
**SERVER-NATIVE.** Requirements are compatible with ordinary Linux servers/VPS classes, though high bandwidth, SSD performance and a reliable RPC endpoint matter. This is much closer to the original 'small autonomous daemon earns while online' model than GPU marketplaces.

### Revenue drivers
- network postage-stamp demand / accumulated redistribution pool;
- neighborhood selection frequency;
- stake density;
- honest storage / reserve commitment;
- bandwidth forwarded through SWAP;
- number of competing nodes / neighborhood conditions;
- uptime and synchronization.

### Risks / penalties
- 10 xBZZ baseline storage stake is non-refundable under current docs;
- dishonest/incorrect reserve commitments can freeze a node for future rounds;
- gas costs in xDAI recur;
- random neighborhood/winner mechanics create highly variable earnings;
- storage/bandwidth demand may be insufficient to cover server cost;
- RPC reliability and operational downtime matter.

### Profit formula
`Net = redistribution rewards + SWAP bandwidth settlements - VPS/server - bandwidth - SSD wear - RPC cost - xDAI gas - economic cost of non-refundable xBZZ stake - maintenance`

### Verdict
Strong architectural fit for a cheap autonomous server daemon, but revenue is stochastic and the non-refundable storage stake is an unusually important cost. SWAP-only operation may deserve separate economics because it can earn bandwidth incentives without the storage-game stake.

---

## Cross-run conclusions

1. **Compute marketplaces split into customer-demand revenue + protocol incentive revenue.** io.net has both; Clore is primarily marketplace rental plus token/fee incentives. Treat these components separately.
2. **Stake must be valued as capital cost, not just 'minimum requirement'.** io.net uses device-specific staked $IO with cooldown/slashing; Swarm's baseline storage stake is explicitly non-refundable; Clore fee optimization can require large token holdings/locks.
3. **Server-native does not mean cheap VPS.** io.net/Clore usually need valuable GPU hardware. Swarm is a better fit for ordinary CPU/RAM/SSD VPS economics.
4. **Bandwidth rewards can coexist with storage rewards.** Swarm should be modeled as two opportunities: storage redistribution and SWAP forwarding.
5. **No profitability conclusion yet.** Current stage proves legitimate earning mechanisms and admission paths, not positive net return.

## Remaining Run 005 queue
Still requires current primary-source validation:
- Lagrange proving/operator opportunities;
- Meson bandwidth/CDN provider economics;
- TensorDock host/provider program status;
- Hyperbolic provider status;
- RunPod community/provider program status;
- Render provider onboarding/cloud-host eligibility;
- Salad server/datacenter restrictions;
- Arweave current mining/storage roles;
- Crust, ScPrime and Autonomi production rewards;
- additional server-permitted relay/CDN/VPN networks.

Next continuation should deepen these items before beginning Bittensor subnet and decentralized-AI sweeps.
