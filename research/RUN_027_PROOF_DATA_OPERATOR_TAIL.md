# Run 027 — Proof-market + decentralized-data operator tail sweep

Date: 2026-08-16
Status: **completed**

## Objective
Continue project-level tail discovery after taxonomy convergence. This pass focused on current 2025–2026 primary sources for prover markets, verifier/compute-contributor variants, decentralized database/query operators, data-availability roles and unresolved Succinct/Gevulot admission questions.

## Saturation result
- New top-level economic mechanisms: **0**.
- Material genuinely new current project/operator cluster: **1** — Space and Time (SXT Chain) validator + prover/query economy.
- Material upgrades to existing watchlist: **1** — Succinct Prover Network is confirmed live on mainnet, but fully permissionless independent prover admission remains insufficiently documented in the public material reviewed.
- Gevulot ZkCloud remains **WATCHLIST** because current official docs still describe it as in development despite a permissionless paid-prover design.
- Avail and Celestia non-validator DA nodes remain infrastructure roles, not independently proven paid provider roles; validators are already covered by the capital/stake + node family.

Run 027 therefore does **not** satisfy the project-level convergence threshold because a material current data/query operator family was still found.

---

## 1. Space and Time (SXT Chain) — VERIFIED, high-priority adjacent data/query cluster

### Operator roles
Current official documentation describes SXT Chain as permissionless and exposes three primary node families:
- **Validator Nodes** — BFT consensus, table-commitment signing, insertion verification and query-verification support.
- **Indexer Nodes** — transform blockchain/external data into relational inserts; docs say permissionless community indexers were planned for summer 2025, but current self-service mainnet setup remains less clearly documented than validators/provers.
- **Prover Nodes** — generate ZK-proven SQL query results. Official node-type documentation states that anyone can run the Proof of SQL repository on a local GPU and race other provers to service query requests through the ZKpay query relayer.

### What creates economic value / who pays
This is a genuine machine-readable data/query economy rather than generic uptime rewards.
- customers pay gas for data insertions;
- query jobs carry compute-credit payments;
- validators receive block rewards from insertion fees and a share of query-job fees;
- prover nodes execute SQL query work and generate zero-knowledge proofs for query requests.

### Validator economics
Official docs currently state:
- 100% of insert-data gas is routed into validator block rewards;
- 50% of query-job fees go to validators and 50% to table owners;
- bootstrap foundation subsidies also exist;
- validators may attract delegated stake and earn from delegation economics;
- poor performance or invalid behavior can be slashed.

A separate official staking page currently describes an expected staking rate of about 8% annualized as the validator set grows, but this is not a guaranteed return and mixes usage-backed fees with network incentives.

### Hardware / server fit
Official validator minimums:
- 16 CPU cores
- 64 GiB RAM
- 512 GiB SSD
- 500 Mbps up/down
- static IP
- Linux
- Docker + Docker Compose
- SXT stake required

This is strongly **SERVER-NATIVE**, but heavier than a cheap VPS.

### Automation level
**5/5** once deployed: validator and prover roles are persistent machine services consuming insertion/query workloads without human microtask interaction.

### Capital / recurring cost
- validator: SXT stake + substantial server cost + uptime/security burden;
- prover: GPU cost/electricity/cloud cost + transaction/payment plumbing; exact minimum economic stake/collateral for independent proving was not normalized in this pass.

### Main risks
- token-price and staking opportunity cost;
- validator slashing;
- query-demand/utilization uncertainty;
- GPU prover competition / race economics;
- cloud/provider ToS still needs host-specific validation;
- Azerbaijan token acquisition/off-ramp/geofencing remains unverified.

### Classification
- SXT Validator: **VERIFIED**, server-native, capital-heavy, automation 5.
- SXT Prover / Proof-of-SQL race: **VERIFIED**, server-native GPU role, automation 5, exact independent profitability still unmeasured.
- SXT Indexer: **WATCHLIST/RESTRICTED** until current public mainnet operator onboarding is proven from a fresh setup guide.

### Why it matters
SXT adds a strong adjacent machine-market implementation to the existing RPC/indexing/prover cluster: the supplied commodity is **verifiable relational data + ZK query execution**, with explicit usage fees from insertions and queries. It is not a new top-level mechanism, but it is materially relevant to the user’s target.

---

## 2. Succinct / SP1 Prover Network — mainnet status upgraded, operator admission still unresolved

Primary sources now clearly establish that:
- the Succinct Prover Network launched on mainnet on 2025-08-05;
- the network is a two-sided prover/requester marketplace;
- the public monorepo includes contracts, staking mechanisms, a reference prover and an `spn-node` binary;
- the reference prover demonstrates bidding and proof generation.

This materially improves confidence versus old platform docs that still describe the network as under development.

However, the reviewed public materials still do **not** cleanly prove that an arbitrary independent operator can currently join the production prover set, stake, bid and receive paid mainnet jobs without invitation/allowlisting or other admission constraints.

Classification remains **WATCHLIST**, but with stronger status:
- network itself: unquestionably live/mainnet;
- independent production prover admission: still not proven sufficiently for `VERIFIED` provider status.

Next validation should target the exact current prover onboarding/staking/admission page or contract-level admission process.

---

## 3. Gevulot ZkCloud — WATCHLIST, design strong but launch evidence stale/inconsistent

Official design docs remain unusually strong for the target model:
- permissionless validator/prover participation by design;
- Linux VM/container workloads;
- both CPU and GPU resource requirements can be declared per prover program;
- workloads are allocated to prover nodes;
- proving workload fee = transaction fee + compute fee × compute time × resource multiplier;
- provers earn workload fee + network reward + verification rewards;
- custom prover sets can set proof pricing.

This proves that **CPU-only proving is architecturally supported**, answering one Run-027 research question. It does not prove that CPU-only work is economically abundant.

But current official introduction still says:
- Firestarter is production-ready but permissioned;
- ZkCloud is “in development” and references a launch target that has already passed.

Therefore do not classify ZkCloud as currently deployable paid income until launch/admission is confirmed from newer official evidence.

Classification: **WATCHLIST**.

---

## 4. Cysic adjacent roles — VERIFIED expansion, no new mechanism

Current Cysic documentation broadens the already-verified Prover Worker into an explicitly open **Compute Contributor** family:
- Provers and Verifiers can contribute compute for ZK and AI;
- devices range from mobile/light verifier and PC to GPU/CPU and future dedicated ASIC hardware;
- requesters publish tasks and providers bid;
- winners execute tasks and selected verifiers validate results;
- rewards are distributed to participating providers/verifiers;
- current Prover Worker setup still requires 1,000 CYS reserved per worker.

The current docs also describe usage-based AI inference/training ambitions and serverless inference endpoints. These strengthen Cysic as a general machine-job market but do not add a new economic mechanism beyond compute/proof task execution.

Important caution: some dedicated hardware products are described as shipping in 2026, so they should not be treated as already generally available.

---

## 5. Data-availability / archival / blob operator check

### Avail
Current docs expose light client, full node, RPC node and validator roles. Only validators are explicitly described as earning staking rewards. The former Light Client Lift-off challenge is explicitly ended/deprecated.

Conclusion:
- validator = already-covered stake + node economics;
- light/full/RPC nodes = **not counted as autonomous income** absent current direct reward evidence.

### Celestia
Current 2026 docs clearly support bridge, light, consensus and validator nodes. Bridge nodes perform substantial erasure-coding/data-serving work, with current recommended hardware around 32 cores, 64 GB RAM, 25 TiB NVMe and 1 Gbps for a non-archival bridge configuration. However, no primary source reviewed in this pass established a direct independent reward stream for bridge/light nodes separate from validator economics.

Conclusion:
- bridge/light = infrastructure, **not counted as paid provider roles**;
- validator = already-covered stake + node family.

This prevents a common false positive: useful infrastructure work is not itself evidence of income.

---

## 6. CPU/RAM-only proving question

Result: **architecturally yes, economically unproven**.

Evidence:
- Gevulot explicitly supports prover programs whose declared requirements may be CPU/RAM only or GPU-backed.
- Cysic describes compute contributors spanning PCs, GPUs and CPUs, while its production prover path remains heavily associated with GPU-class proving.
- Boundless current recommended stack is GPU-oriented.
- SXT Proof of SQL explicitly describes a single-GPU prover model.

Practical conclusion: the currently strongest live paid proving markets remain overwhelmingly **GPU/datacenter-oriented**. Cheap CPU/RAM-only proof work remains a niche to watch rather than a proven low-cost VPS income path.

---

## 7. Economics normalization

### Strong usage-linked machine markets now in the project
- Boundless — requester proof payments + optional network incentives.
- Cysic — task bidding / proof rewards + reserve/slashing model.
- SXT — insertion/query fees + validator/prover execution.
- Lava/SubQuery/The Graph/SQD — RPC/query/indexing/data-service economics.

### Dominant economic variable
**Paid utilization remains more important than theoretical reward rate.** A daemon can be perfectly autonomous and still lose money if there are too few paid jobs.

### Required pilot formula
For any next-stage implementation candidate:

`Net/month = paid-job revenue + protocol incentives - compute - GPU amortization - electricity - storage - bandwidth - RPC/API - chain gas - collateral/stake opportunity cost - expected slashing/losses - maintenance`

For competitive proof/query races add:

`Expected revenue = eligible jobs × win probability × payout/job`

Win probability must be measured empirically; advertised task volume alone is insufficient.

---

## 8. ToS / legality / geography

No candidate in this run requires CAPTCHA bypass, fake traffic, spam, human-task impersonation or prohibited account automation.

Still unresolved before CAPEX:
- GPU/cloud host policy for proof/mining workloads;
- SXT/CYS/PROVE/ZKC token acquisition and payout liquidity in Azerbaijan;
- exchange/off-ramp KYC/geofencing;
- tax treatment;
- sanctions/geo restrictions of dependent RPC/cloud/wallet services.

Silence in protocol docs is not proof of Azerbaijan eligibility.

---

## 9. Run 027 verdict

Taxonomy saturation remains **very high**: this was the tenth deliberate control/tail pass with **0 new top-level mechanisms**.

Project-level saturation is **still not complete** because Space and Time materially adds a current, documented permissionless data/query operator economy with validator and prover roles.

### Next run
**Run 028 — final data/query/prover cross-category tail + saturation test.**

Priority searches:
- verifiable SQL / database prover / query prover / data coprocessor node rewards
- decentralized database operator / data warehouse validator / query worker
- proof marketplace / prover race / proof auction / proof broker
- current Succinct prover admission/staking/onboarding
- Lagrange public prover admission
- decentralized data-availability paid non-validator roles
- RPC/indexing networks using alternate terms: gateway supplier, data worker, query executor, archive provider, coprocessor node

If Run 028 yields 0 new mechanisms and only 0–2 weak/restricted genuinely new projects, perform the final all-category saturation pass immediately after it. If that final pass also yields no material novelty, prepare `COMPLETE`.
