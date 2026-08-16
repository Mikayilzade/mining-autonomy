# Run 028 — Final data/query/prover cross-category tail + saturation test

Date: 2026-08-16
Status: **COMPLETED — project remains IN PROGRESS**

## Goal
Run the planned cross-category tail sweep around proof markets, query/data workers, coprocessors, alternate provider-role names and current independent operator admission. This pass was explicitly intended as a near-final saturation test after Runs 018–027.

## Result summary
- New top-level economic mechanisms: **0**.
- New material provider clusters: **2**.
- New weak/restricted proof-market candidate: **1**.
- Prior watchlist status rechecked: Succinct and Lagrange remain constrained by public admission clarity rather than by lack of a real network.

Because two material current provider clusters were discovered, project-level saturation is **not yet achieved**.

---

## 1. Marlin Oyster — VERIFIED material cluster

### Classification
- Category: TEE / confidential compute marketplace + serverless executor/gateway network
- Status: **VERIFIED**
- Server-native: **YES**, with TEE/secure-enclave requirements and/or supported cloud provider account
- Automation: **5/5** once control plane / executor / gateway is configured
- Resource sold: compute, enclave instance time, bandwidth, gateway relay, serverless execution capacity
- Payout/revenue: customer payments; current protocol docs identify USDC as payment token for Oyster instance jobs, with POND used for stake/bootstrap incentives in parts of the protocol
- Capital: gas + POND stake/collateral where required; cloud/TEE infrastructure cost
- Main hidden variable: paid utilization / job volume
- Risks: slashable stake, cloud/TEE cost, uptime obligations, gas, demand concentration, protocol upgrade risk

### Why it is material
Current official Marlin docs expose a permissionless infrastructure-provider workflow for Oyster. Operators run a long-lived Control Plane, publish rates and regions, register in the marketplace, and can be selected by users to run confidential VM jobs. The marketplace UI/docs explicitly say becoming an Oyster infrastructure provider is permissionless and that operators can monitor usage and claim accrued amounts from active jobs.

The Confidential VM protocol is customer-paid infrastructure rather than generic emissions: users escrow/payment-fund jobs and providers quote per-second resource prices. Providers are required to stake at least the protocol StakePerJob amount of POND, and can be slashed for non-performance.

### Oyster Confidential VM provider
Official workflow establishes:
1. Provider defines instance types and prices.
2. Provider runs a control plane.
3. Provider registers the control-plane URL on-chain/in the marketplace.
4. Users choose resource offerings and fund jobs.
5. Control plane automates provisioning, enclave deployment and shutdown.
6. Provider receives job payments while satisfying monitoring/uptime guarantees.

Current docs also state that an operator can participate with SGX-capable hardware or an AWS/GCP/Azure account. The documented control-plane example uses AWS and dynamically provisions enclave instances.

### Oyster Serverless Executor
Current protocol docs define Executors as TEE nodes that perform assigned computation. Registration includes enclave attestation, stake, compute capacity, owner address and execution environment. Executors can be slashed for failed duties. User payments are released after successful responses. The incentive design explicitly aims for user fees to exceed operator costs and includes a bootstrap Payment Pool when demand is below target latent capacity.

### Oyster Serverless Gateway
Gateways are TEE nodes that relay requests/responses. They register with stake, supported chains and enclave attestation, need gas inventory on supported chains, and can be slashed for missed duties. Successful requests pay both gateway and executor; gateway compensation is primarily intended to cover relay/gas cost.

### Fit to the target
This is one of the cleanest examples yet of a legitimate autonomous server earning model: a daemon/control plane advertises machine-readable resources, receives machine-generated jobs and gets paid without human microtask impersonation.

### Economics model
For Confidential VM provider:
`Net = job revenue in USDC - cloud/owned TEE cost - bandwidth - control-plane server - gas - stake opportunity cost - expected slashing loss - maintenance`

For Serverless Executor/Gateway:
`Net = user fees + bootstrap/payment-pool incentives - enclave infrastructure - gas - stake opportunity cost - expected slashing - maintenance`

Critical next measurement: live marketplace utilization, current rates by region/instance, required POND stake per job, and whether cloud resale margins remain positive after provider cloud cost.

### Azerbaijan / KYC / ToS
Official protocol onboarding is wallet/on-chain based and no Azerbaijan exclusion was found in the operator docs used in this pass. This is **not** proof of full Azerbaijan eligibility because cloud provider accounts, token acquisition/off-ramp and any Marlin front-end terms still require live validation before capital deployment.

---

## 2. Lumoz — VERIFIED material ZK/AI node cluster

### Classification
- Category: ZK/AI compute + verification node rewards
- Status: **VERIFIED**, with capital/licensing caveats
- Server-native: **YES** for verifier node; compute node is GPU-oriented
- Automation: **5/5** node daemon / Docker
- Resource sold: proof/AI compute, proof verification, network service
- Payout: MOZ/esMOZ token incentives; application/resource-use fees are denominated in MOZ according to official token utility docs
- Capital: verifier license and/or stake; gas; hardware; compute node stake requirements need current empirical confirmation
- Risks: token price, lock/redemption schedule, stake/slashing, license opportunity cost, utilization, hardware economics

### Verifier Node
Current official docs provide a mainnet CLI release and Docker workflow. A node owner delegates at least one license to the operator and sets a reward split between commission, delegated-license rewards and staked esMOZ rewards. The node runner and reward claimer can run continuously in Docker.

The published license sale had multiple historical tiers; public sale is marked ended, so acquisition/liquidity of a valid license is now a deployment constraint rather than an assumption.

### Compute Node / zkProver
Official docs describe Compute Nodes as ZK/AI computational providers. As a zkProver, participants contribute compute and receive Lumoz protocol-token rewards. The ZK-PoW design allows multiple provers to submit valid work for a sequence, then distributes PoW reward among valid provers in proportion to stake. Invalid/missing proof conditions can cause stake slashing.

The tokenomics docs allocate 25% of supply to Compute Node rewards and 25% to Verifier Node rewards; MOZ is also the resource-use fee token, while esMOZ is used for participant rewards/staking and can be redeemed to MOZ according to a redemption schedule.

### Fit to the target
Strong fit for autonomous machine work, but weaker than customer-priced marketplaces until real demand/reward composition is normalized. It contains both protocol-emission and service-fee components, so profitability cannot be inferred from allocation percentages.

### Economics model
Verifier:
`Net = verifier rewards + commission - license opportunity/depreciation cost - server - gas - token conversion/lock costs - expected losses`

Compute node:
`Net = ZK/AI compute rewards - GPU depreciation/rental - electricity/cloud - stake opportunity cost - gas - expected slashing - maintenance`

### Azerbaijan / KYC / ToS
No operator-region exclusion was established from the technical docs reviewed. Token acquisition, wallet/front-end access and off-ramp still need a live Azerbaijan check before deployment.

---

## 3. Fermah — WATCHLIST / RESTRICTED

Fermah remains a real universal proof-market architecture, but current official operator material still points to testnet/devnet participation, machine-secret whitelisting and incentivized-testnet points rather than a clean permissionless production-income path.

Important evidence:
- Prover nodes run CPU/GPU proof workloads.
- Current onboarding page requires a machine secret to be whitelisted.
- Docs describe testnet participation and future planned rewards.
- Proof request lifecycle includes escrow and operator eligibility for payment, but present public operator flow is not yet sufficient for VERIFIED production classification.

Status: **WATCHLIST/RESTRICTED** until production mainnet operator admission and paid workload economics are current and self-service.

---

## 4. Succinct / SP1 — WATCHLIST maintained

Current official Succinct documentation confirms a decentralized prover network and a mainnet explorer, strengthening that the network itself is live. However, this pass still did not establish a clean current self-service path for an independent new prover to join the production network and receive assignments without an admission dependency.

Status unchanged: **WATCHLIST for independent provider onboarding**, not rejected.

---

## 5. Lagrange — WATCHLIST maintained, network strengthened

Current first-party Lagrange material confirms a live production prover network on EigenLayer and states that operators/provers receive rewards for successfully completed proof work, with penalties/non-payment for missed commitments. The public site reports 85+ operators and a large production proof count.

However, the practical admission path still appears operator/program-oriented rather than a frictionless self-service commodity worker: recent/current materials encourage interested operator teams to reach out/join, while the visible operator set is dominated by professional staking/infrastructure firms. This is enough to confirm a real paid network, but not enough to upgrade it to a low-friction permissionless target.

Status: **WATCHLIST/RESTRICTED for independent admission**.

---

## 6. No-paid-role controls

The pass again enforced the distinction between useful infrastructure and paid provider roles. A technical full/light/archive/query node is not counted merely because it contributes to a network. Payment evidence, independent admission and a supply-side earning path remain mandatory.

No new paid non-validator DA-node mechanism was established in this pass.

---

## 7. Saturation assessment after Run 028

This pass was supposed to be a near-final cross-category tail check. It failed the completion gate because Marlin Oyster and Lumoz were both material current operator clusters absent from the durable catalogue.

Metrics:
- Control/tail passes now completed: **11** (Runs 018–028)
- New top-level mechanisms in those passes: **0**
- New material clusters in Run 028: **2**
- Taxonomy saturation: **very high**
- Project/provider saturation: **high but not complete**

The project remains **IN PROGRESS**.

## Next run — Run 029

Perform a focused convergence pass around the two newly exposed vocabulary families and their adjacent ecosystems:

1. TEE/confidential-compute marketplaces
   - enclave marketplace operator
   - confidential VM provider
   - TEE executor / gateway
   - serverless enclave worker
   - secure coprocessor provider
   - SGX/SEV compute marketplace
   - verifiable cloud provider

2. License/stake-backed ZK/AI verification networks
   - verifier node license rewards
   - ZK verification operator
   - proof verifier node rewards
   - compute-node ZK-PoW
   - AI verifier node

3. Recheck adjacent named systems
   - Marlin Kalypso provider/prover roles
   - Lumoz live compute-node setup and real utilization
   - current Fermah production status
   - current independent Lagrange/Succinct prover admission

4. Economics normalization
   - live Oyster marketplace rates/utilization
   - POND stake per job and slashing exposure
   - Lumoz license acquisition path, verifier reward realization and esMOZ redemption
   - whether either model has a credible low-capital pilot from Azerbaijan

If Run 029 finds no new material cluster beyond direct variants of Oyster/Lumoz, immediately follow with an all-category control pass before considering COMPLETE.
