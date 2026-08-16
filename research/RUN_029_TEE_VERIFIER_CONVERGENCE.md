# Run 029 — TEE / Confidential-Compute + Verifier-Node Convergence

Date: 2026-08-16
State: COMPLETE FOR THIS RUN; project remains IN PROGRESS

## Objective
Re-run the remaining TEE/confidential-compute/verifier/prover tail using current primary sources, with special attention to independently joinable paid operator roles that can run autonomously.

## Result summary

### Taxonomy result
- **0 new top-level economic mechanisms.**
- TEE/CVM operator income remains economically a form of compute rental / machine-service provision.
- Verifier/prover roles remain compute + stake/license/service-reward variants.

### Project-level result
Project-level saturation is **not complete**. This pass found two current provider clusters that were not present in the durable checkpoint from Runs 001–028:

1. **Targon / Manifold Labs confidential-compute supply network** — material, current, supply-side marketplace with provider onboarding and confidential-compute hardware roles.
2. **Tenzro open multi-role operator network** — material current operator model spanning compute, storage, TEE, AI inference and validator roles, with explicit machine-readable payments/staking model.

Because new material providers still appear under alternate vocabulary, completion gate is not met.

---

## 1. Targon / Manifold Labs — VERIFIED / HIGH-PRIORITY

### What it is
Targon describes itself as a decentralized confidential-compute network and exposes a **Supply Portal** for compute providers. Current first-party materials describe a permissionless compute network where hardware providers register machines, contribute TDX/NVIDIA-confidential-compute capacity, and receive economic incentives.

### Economic mechanism
- Resource supplied: CPU/GPU compute, especially TDX-capable CPU + NVIDIA confidential-compute GPU clusters.
- Demand: customer GPU rentals, confidential VMs, serverless execution and managed inference.
- Revenue source: marketplace/customer compute usage plus protocol incentive layer.
- Provider operation: node/CVM continuously attested and admitted into a Kubernetes scheduling pool.
- Automation: very high; workload placement, attestation, scheduling and failover are orchestrated automatically.

### Current supply evidence
Targon main site exposes an **Access or Provide Confidential Compute** path and a dedicated Targon Supply Portal.

The Intel/Manifold whitepaper published in 2026 states that:
- Manifold operates a decentralized permissionless compute network;
- hardware providers can register/contribute machines for economic incentives;
- validated CVMs join the scheduling pool automatically;
- workloads include GPU rentals, serverless execution and managed inference;
- validators calculate contribution weights and payouts are distributed automatically;
- the architecture is explicitly designed around third-party, potentially anonymous/untrusted hardware providers.

### Hardware / server fit
Strong fit for owned bare-metal/datacenter hardware. Current architecture requires confidential-compute capability:
- Intel TDX CPU platform;
- compatible NVIDIA confidential-compute GPUs for GPU workloads;
- appropriate kernel/virtualization stack;
- continuously attested CVM.

This is not a normal cheap VPS opportunity. It is closer to an owned/server-rack or specialty-cloud supply strategy.

### Capital
Potentially high. Targon's Tower page publishes example hardware builds including multi-GPU systems and shows very large purchase costs for H100/H200-class configurations. This makes a retail CAPEX purchase unsuitable without measured utilization and contract/reward validation.

### Important nuance
The Tower page distinguishes hardware that can be monetized permissionlessly from some consumer hardware that requires a KYC/contracted tier. Therefore:
- do not assume every GPU is permissionlessly monetizable;
- provider path and KYC status are hardware/tier dependent;
- Azerbaijan eligibility must be checked during real onboarding before CAPEX.

### Profitability model
`Net = customer rentals + protocol incentives - hardware depreciation - electricity - cooling - networking - downtime - maintenance - capital opportunity cost - token/stake exposure - taxes/withdrawal costs`

Dominant unknowns:
- realized utilization;
- supply-side fee split;
- incentive-pool durability;
- actual accepted hardware list;
- power cost and cooling;
- whether supplier onboarding from Azerbaijan is allowed;
- withdrawal/off-ramp path.

### Status
**VERIFIED, HIGH-PRIORITY, HARDWARE/CAPEX-HEAVY.**

It is one of the clearest current examples of legitimate autonomous 'mining' via continuously attested hardware that receives machine-generated jobs rather than human microtasks.

---

## 2. Tenzro — VERIFIED ARCHITECTURE / DEPLOYMENT MATURITY NEEDS LIVE CHECK

### What it is
Tenzro presents an open network where node operators can provide several resources from one node:
- AI model serving;
- spare CPU/GPU compute;
- storage;
- TEE/confidential compute;
- validator/security work;
- light-node participation.

Current first-party operator material says a node can run on a cloud VM, home server, desktop or small device depending on role. Operators choose offered services and prices; work is routed by price/performance/reputation; payments settle in TNZO.

### Economic mechanisms
No new top-level mechanism, but a useful **multi-resource bundling strategy**:
- ComputeProvider: spare capacity rented by epoch;
- StorageProvider: paid per byte-epoch with retrievability proof;
- TeeProvider: confidential enclave time paid by tenants;
- Model provider: paid per inference/request;
- Validator: stake + fees/rewards.

### Strong fit with project target
The operator description is almost exactly the desired theoretical target:
- install node;
- expose hardware/resource roles;
- receive routed machine work;
- earn programmatically;
- no human-task impersonation;
- high automation potential.

### Capital / stake
First-party operator page claims $0 sign-up and says some roles require TNZO stake; qualifying operators may be sponsored for initial stake. This is attractive in theory but requires direct onboarding verification before treating as a deployable zero-capital option.

### TEE role
Tenzro explicitly supports independent TEE providers using Intel TDX, AMD SEV-SNP, AWS Nitro Enclaves and NVIDIA confidential compute. Current material says an operator can register, stake TNZO, advertise capability and earn for serving without permission.

### Profitability unknowns
Current public pages establish the economic design, but they do **not yet provide enough evidence of realized demand, provider revenue or token liquidity** for a profitability claim.

Need to validate next:
- production network status and downloadable node software;
- live provider count;
- real paid jobs rather than demo/test traffic;
- TNZO liquidity/redemption/off-ramp;
- minimum stake and sponsorship rules;
- Azerbaijan access;
- actual per-role utilization.

### Status
**WATCHLIST → VERIFIED ARCHITECTURE; production-income realization still needs validation.**

Do not rank it above mature marketplaces until live node + payment evidence is confirmed.

---

## 3. Marlin Oyster — strengthened, no new mechanism

Current official documentation continues to support Run 028 conclusions:
- CVM providers set instance/rate offerings and register on-chain;
- provider control plane is long-running and automates provisioning/shutdown;
- jobs are funded in USDC;
- providers stake POND per job and can be slashed;
- CVM providers are paid while instances are rented;
- Serverless Gateways/Executors stay active and are compensated by protocol/user fees;
- serverless pricing explicitly targets commercial viability where user fees exceed operator operating cost.

### Important economics refinement
Oyster is stronger than generic emission-only DePIN because its CVM model has a direct customer escrow/payment path. However, it remains impossible to call profitable without measuring marketplace utilization and provider price competition.

Status remains **VERIFIED / HIGH PRIORITY FOR PILOT ECONOMICS**.

---

## 4. Lumoz — verified reward mechanics, capital intensity remains

First-party Lumoz docs continue to establish:
- 25% token allocation for Verifier Node rewards;
- 25% allocation for Compute Node rewards;
- verifier rewards depend on licenses, delegated licenses, staked esMOZ and reward splits;
- compute-node/prover rewards use ZK-PoW and stake-weighted reward allocation;
- provers can be slashed for failed proof obligations;
- protocol usage fees are denominated in MOZ while node rewards are largely esMOZ/token-incentive based.

### Practical conclusion
Lumoz is not a simple zero-capital VPS bot. Current verifier economics are license/stake dependent; compute-node economics require proof-capable hardware plus stake and slashing tolerance.

Status remains **VERIFIED / CAPITAL-AND-HARDWARE CONSTRAINED**.

---

## 5. Fermah — still WATCHLIST / TESTNET-RESTRICTED

Current first-party docs still describe:
- Prover Nodes in Testnet/Devnet;
- machine-secret authentication;
- whitelist application;
- Sepolia RPC;
- incentivized testnet points with future rewards;
- significant GPU/RAM requirements for current proof systems.

The daemon/tooling is real and highly autonomous, but the public path still does not establish a clean permissionless production-income opportunity.

Status remains **WATCHLIST / RESTRICTED**.

---

## 6. Succinct/SP1 and Lagrange

This run did not find stronger current first-party evidence that reverses the Run 028 admission conclusion.

### Succinct/SP1
The production prover network/mainnet is real, but this pass did not establish a frictionless public path for an arbitrary new independent prover to onboard and earn immediately.

### Lagrange
Production proving is real, but public evidence found in previous passes still supports operator/program-style admission rather than commodity self-service participation.

Both remain **WATCHLIST / admission not sufficiently proven**.

---

## 7. Other TEE/confidential-compute leads from this pass

### Aleph Cloud
Current first-party material shows Compute Resource Nodes and GPU-provider economics, including an 80% GPU-cost share in a 2025 campaign and confidential-VM support. Aleph was already within the broader decentralized-compute universe and does not create a new mechanism. Revalidate current generic CRN economics in a future provider-tail pass.

### SecretVM / Secret Network
SecretVM is current confidential-compute infrastructure. A 2026 roadmap describes future BYOH/compute-marketplace revenue sharing for hardware owners. This is **future/watchlist**, not current independent paid-provider proof.

### Verida Confidential Compute
Current docs say first nodes are Foundation-operated and outside operators will be opened later. **WATCHLIST / future provider role.**

### Akash confidential compute
Akash announced confidential compute in July 2026. Akash provider economics are already part of decentralized-compute taxonomy; TEE support is an important capability extension, not a new earning mechanism.

### ALPENGLOW / Ealna and other very new networks
They advertise GPU/inference provider rewards and TEE verification but need stronger maturity, software, payment and independent-source validation before promotion from discovery lead. Keep as low-confidence discovery leads, not deployable recommendations.

---

## Safety / ToS / legality
None of the serious candidates in this run depend on CAPTCHA bypass, fake engagement, spam, account farms or automation of human-only tasks. Their core activity is legitimate infrastructure/service supply.

Remaining legal/commercial gates:
- cloud-provider resale/hosting terms if using rented hardware;
- token/staking legal treatment;
- tax/reporting;
- KYC/sanctions/geofencing;
- data-center/ISP terms;
- Azerbaijan token acquisition and off-ramp availability.

---

## Run 029 conclusion

### New mechanisms
**0**

### Material new provider clusters
**2**
- Targon / Manifold Labs
- Tenzro

### Completion decision
**DO NOT MARK COMPLETE.**

Provider-level tail discovery remains productive under alternate terms such as confidential cloud, supply portal, TEE provider, secure-hardware provider, attested compute and distributed CVM.

## Next run recommendation — Run 030
Perform a focused convergence pass around:
- Targon supplier onboarding, current supply portal, payout formula and realized utilization;
- Tenzro production-node/software/payment reality;
- SecretVM BYOH status;
- Aleph current CRN/GPU economics;
- Akash confidential-compute provider capability;
- TEE provider / attested compute / secure GPU supplier / confidential inference provider vocabulary;
- Bittensor subnets whose economic role is effectively confidential-compute supply;
- current provider directories and GitHub releases for Targon/Tenzro.

If Run 030 again finds another material cluster, remain IN PROGRESS. If it yields no new material cluster, proceed immediately to a final all-category saturation pass before COMPLETE.
