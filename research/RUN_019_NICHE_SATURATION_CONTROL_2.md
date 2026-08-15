# Run 019 — Niche Saturation / Control Pass #2

Date: 2026-08-15
Status: **completed**
Project state after run: **IN PROGRESS**

## Goal
Validate the strongest directory-only server-native leads from Run 018 using primary sources and alternate supply-side vocabulary (`provider`, `node operator`, `worker`, `miner`, `host`, `processor`, `edge node`, `executor`, `resource seller`). The completion question for this run was not whether the taxonomy changed, but whether fresh niche searches still produce materially new viable projects or important downgrades.

## Summary
This pass produced **0 new top-level economic mechanisms**, but it did produce one materially strong server-native candidate (**Fleek Network node operator**), one important device-only clarification (**OORT Edge / Deimos**), one currently unresolved but technically real decentralized-media node family (**dTelecom SFU nodes**), plus several downgrades/insufficient-evidence outcomes. Therefore the research is **not saturated**.

The main pattern is now clear: late-stage discovery increasingly yields projects inside already-known mechanisms rather than new mechanisms. That is progress toward saturation, but the viable-project tail is not yet negligible.

## Candidate results

### 1. Fleek Network node operator — VERIFIED mechanism, SERVER-NATIVE, current production-state verification still needed
**Classification:** decentralized edge compute / bandwidth / service execution.

Official Fleek docs describe a distributed edge network in which node operators make user-managed resources available and receive rewards. Services consume measurable commodities such as CPU and bandwidth; Delivery Acknowledgements record work and are used to determine rewards. The official node docs show a Linux/Docker `Lightning` node that can run as a service, with participation opt-in and health status reporting `running and staked`.

**Why it matters:** this is close to the target model: a daemonized server contributes compute/bandwidth to discrete service requests and the protocol measures actual work.

**Automation:** 5/5 once provisioned.

**Server fit:** strong technically; Docker/Linux instructions support normal server operation.

**Economic source:** protocol rewards tied to measured commodities and service fulfillment, not merely keeping software open.

**Important uncertainty:** current public docs surfaced by search still contain alpha/testnet-era language and preliminary tokenomics references. Before CAPEX, a later pass must establish current 2026 mainnet supplier admission, liquid payout path, staking amount, actual demand/utilization, and whether a fresh operator can join production today.

**Status:** `VERIFIED` as a real rewarded node mechanism; `RESTRICTED` for deployment until current production economics are revalidated.

**Net formula:** rewards for delivered compute/bandwidth/services − server cost − stake opportunity cost − bandwidth/egress − maintenance − token/withdrawal costs.

---

### 2. OORT Edge / Deimos provider — VERIFIED, HOME/DEVICE-ONLY rather than generic VPS
**Classification:** physical/device DePIN; storage + compute + bandwidth.

Current official OORT docs say node providers earn by running OORT Edge nodes and supplying storage/compute/bandwidth. However the current retail node path is explicitly tied to **Deimos** hardware (and some Helium hotspot integrations). The docs state that OORT node providers can only mine OORT utility tokens with Deimos.

Rewards have two components:
- mining rewards, with 25% released immediately and 75% linearly over 270 days;
- additional utility/service rewards when applications consume storage, compute or data transfer.

Current tokenomics also impose strong operational/economic constraints: online score affects rewards; Deimos has a 360-day serving period; early collateral withdrawal can trigger a penalty formula; new device admission is supply-controlled by a utilization gate.

**Why it matters:** legitimate autonomous earning, but **not** a normal VPS/server-native opportunity despite OORT’s cloud/storage architecture.

**Automation:** 5/5 after physical device provisioning.

**Status:** `VERIFIED`, Tier B / device-only.

**Risk:** hardware cost, token price, reward vesting, collateral, uptime penalty, vendor/device dependence, utilization.

---

### 3. OORT witness node — WATCHLIST / separate server-native network role
Official OORT infrastructure docs describe a daemonized witness node suitable for cloud or local-datacenter machines, with suggested hardware around 8 CPU cores, 32 GB RAM and 2 TB SSD. The docs explicitly mention that reduced performance can lower the reward for serving as a witness.

This is a genuine server-native lead distinct from Deimos, but this pass did not establish the current admission/stake requirements or a complete current reward/payout formula from primary docs.

**Status:** `WATCHLIST` pending current witness economics and permissionless admission confirmation.

---

### 4. dTelecom decentralized SFU node — WATCHLIST, technically server-native
Current dTelecom docs describe a decentralized WebRTC network based on independent SFU nodes registered on Solana. Client connections discover the geographically optimal SFU node from an on-chain registry. The network is therefore technically a real server-native bandwidth/real-time-media service architecture.

However the currently indexed operator docs did **not** expose a public permissionless node-onboarding or provider-reward page. Customer/developer usage is well documented; supply-side earnings are not yet sufficiently proven.

**Status:** `WATCHLIST`.

**Next check:** registry contract, operator CLI/repository, tokenomics and current node admission/reward docs.

---

### 5. Spheron community GPU supply — RESTRICTED / supplier admission unresolved
Current official Spheron docs clearly show a GPU marketplace containing both `Secure GPUs` and lower-cost `Community GPUs`, which proves third-party/community capacity exists on the supply side.

What this pass did **not** find in current primary docs is a self-service public provider onboarding/reward specification comparable to Vast.ai, io.net or Clore.ai.

**Status:** `RESTRICTED` / supplier path unresolved.

Do not treat the existence of `Community GPUs` as proof that a new arbitrary host can list capacity today.

---

### 6. Impossible Cloud — RESTRICTED as an earning lead; reseller/channel model exists
Current official Impossible Cloud docs strongly validate it as a commercial S3-compatible cloud/storage service. The management-console documentation also exposes **Distributor** and **Channel Partner** roles, including reserved-capacity and pay-per-use allocation to downstream partners/accounts.

This establishes a legitimate reseller/channel business mechanism, but it is not evidence of a permissionless storage-node/provider market. The reviewed docs did not show a path where an arbitrary user contributes spare disk/server capacity and receives protocol rewards.

**Status:**
- raw storage-node mining: `REJECTED/UNVERIFIED` for now;
- channel/reseller business: `VERIFIED` as a commercial partnership mechanism, Tier D/business rather than autonomous resource mining.

---

### 7. iExec worker / workerpool — WATCHLIST pending refreshed current supplier docs
Search of current official docs confirms iExec’s PoCo layer remains an off-chain computation coordination system, but the easily indexed documentation is now strongly developer/privacy-product oriented. This pass did not obtain sufficiently current first-party workerpool/worker onboarding and payout documentation to upgrade the supplier path.

Historical knowledge is not enough for this project’s evidence standard.

**Status:** `WATCHLIST`.

**Next check:** current PoCo repositories, workerpool deployment docs and on-chain marketplace contracts.

---

### 8. Edge Network / XE — WATCHLIST for resource-provider admission; separate paid writing path VERIFIED
Current official Edge docs describe a decentralized compute network composed of contributed nodes and sell VM/server products to users. This proves third-party infrastructure is part of the architecture, but this pass did not locate a current self-service node-provider earning/onboarding page.

A separate official program pays technical writers in XE (typically stated as $250 equivalent per accepted tutorial, with some higher/lower ranges). That is legitimate income but manual content work, not passive mining.

**Status:** infrastructure supply `WATCHLIST`; writing bounty `VERIFIED` but out of primary autonomous scope.

---

### 9. StorX — UNVERIFIED in this pass
The targeted primary-source search did not return sufficiently strong current StorX operator/reward documentation. Do not infer viability from directory listings or older ecosystem material.

**Status:** `UNVERIFIED`; retain for another direct-doc/repository pass.

---

### 10. Fluence — WATCHLIST / likely valid compute-provider family, current docs retrieval incomplete
Primary-source search surfaced Fluence material describing compute providers contributing CPU supply in exchange for FLT rewards, with stake required per added CPU and stake at risk for incorrect job execution. This strongly suggests a real capital-backed compute-provider mechanism.

However the surfaced material was not sufficient to normalize current 2026 provider onboarding, hardware requirements, payout economics and production demand.

**Status:** `WATCHLIST` with high priority for direct current docs/repository validation.

---

### 11. YOM — UNVERIFIED in this pass
Targeted primary-source search did not return enough current operator/reward evidence to classify a public provider role.

**Status:** `UNVERIFIED`.

## Economic/taxonomy lessons from Run 019

1. **Late discovery is converging by mechanism.** No new economic class appeared; new hits map to edge compute, media relay, storage/reseller, or physical device DePIN already represented in the taxonomy.
2. **Customer marketplace ≠ open supplier marketplace.** Spheron, Edge and Impossible Cloud all demonstrate why consumer-side capacity listings or decentralized architecture cannot be assumed to imply public supplier admission.
3. **Protocol architecture ≠ current cash opportunity.** dTelecom and iExec show that a technically decentralized worker/node architecture can be real while the current permissionless reward path remains inadequately documented.
4. **Device lock-in is a major classification boundary.** OORT’s current rewarded edge path is tied to Deimos/approved device hardware and should not be marketed as VPS mining.
5. **Current-state validation matters more late in the search.** Several directory leads appear to be based on older testnet/provider documentation. A project only counts as high-priority if current production admission and payout are proven.

## Saturation metrics
- New top-level economic mechanisms: **0**
- Strong/materially strengthened server-native projects: **1** (Fleek)
- New server-native watchlist role: **2+** (OORT witness, dTelecom SFU; Fluence strengthened)
- Device-only project clarified: **1** (OORT Deimos)
- Reseller/business mechanism clarified: **1** (Impossible Cloud channel model)
- Supplier paths downgraded/unresolved: **5+**

## Saturation conclusion
**Not complete.** The taxonomy is stable, but this second control-style pass still yielded enough materially useful project-level information that another differently-worded direct-repository / operator-doc pass is justified.

## Next run — Run 020
Perform a **provider-repository / tokenomics control pass #3** focused on unresolved high-value tails:

1. Fluence current compute-provider docs/repository and marketplace economics.
2. Fleek 2026 production/mainnet status, staking and payout path.
3. iExec current worker/workerpool status from PoCo repositories/contracts.
4. dTelecom SFU operator onboarding/rewards/registry.
5. Spheron community GPU supplier onboarding.
6. StorX node/reward current docs/repository.
7. Edge/XE node contribution/provider admission.
8. YOM provider/node program.
9. Impossible Cloud Network specifically, separating ICN protocol from Impossible Cloud commercial storage/reseller docs.
10. Broad alternate terms: `capacity provider`, `supply node`, `workerpool`, `resource provider`, `edge supplier`, `operator rewards`, `node rewards`, `host marketplace`, `permissionless provider`.

If Run 020 again produces no new economic mechanism and only negligible net-new viable public provider projects, proceed to a final broad cross-directory pass; otherwise continue until the project-level tail converges.
