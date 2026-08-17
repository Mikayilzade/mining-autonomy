# Run 058 — Residual validation + alternative-vocabulary spot-check

Date: 2026-08-17
Status: **COMPLETED — project remains IN PROGRESS**

## Result
- New top-level economic mechanisms: **0**.
- All Run 057 residual candidates normalize into existing families.
- However, the compact supplier-role spot-check surfaced **4 additional independent provider projects** not found in the durable repository search: Swan Inference, AntSeed, UsePod, and DeCloudX.
- Because this is more than negligible project-level residual discovery, the completion gate is **not yet passed**.

## Residual candidate normalization

### 1. NodeOps Network Compute Provider — VERIFIED / server-native
Official docs state Live on Mainnet. Providers can supply owned hardware or VMs; NodeOps explicitly documents VM resale and a GCP deployment path. Minimum machine profile includes >=2 vCPU, >=4 GB RAM, >=80 GB NVMe, public static IPv4, >=1 Gbps unlimited network, >=99% uptime, Debian 12+/Ubuntu 22.04+, root integration, and no other workloads. Provider bond: 2000 NODE + 200 NODE per CU. Published reward headline: each 2CU up to 10 NODE/day (8 base + up to 2 performance). Docs also state providers receive a share of CU consumption fees. gNODE redemption to NODE is time-constrained. No general KYC/geography requirement was found in the checked provider docs; Azerbaijan is not explicitly discussed.

Key economics: value of NODE/gNODE, bond opportunity cost, VM cost, utilization/performance component, bandwidth requirements, and eventual slashing rules. Slashing details remain incomplete in docs.

### 2. OpenGPU Provider — VERIFIED product path / demand still uncertain
Official provider pages describe Linux/Windows/macOS provider software, automatic job routing, and rewards per completed real AI workload. A provider connects GPU + wallet, with no OGPU lockup required for hardware provision. Management UI supports automatic routing and fleet scaling. The public site labels the network as an early network phase, so production demand depth and token liquidity remain the dominant unknowns. No explicit Azerbaijan/KYC rule was found in the checked pages.

Mechanism: GPU/inference compute marketplace. Net model: completed-task rewards minus GPU/server cost, power, depreciation and withdrawal/token conversion costs.

### 3. Lium / Bittensor SN51 — VERIFIED / GPU-node marketplace + subnet emission
Current docs describe a live provider path on Bittensor Subnet 51. Operator runs a lightweight CPU coordinator (self-hosted Linux or Lium-hosted) plus one or more GPU nodes. GPU nodes need supported NVIDIA hardware, >=8 GB RAM, >=100 GB free disk, >=50 Mbps, public IP, required ports and Sysbox. Providers must register a hotkey on SN51 and pay the dynamic subnet registration burn fee in TAO. Earnings have two streams: renter-paid GPU fees and subnet emission. Rental payments go to coldkey daily; subnet emission accrues as alpha stake on the hotkey. No blanket KYC/geography rule was found in checked provider docs; Azerbaijan not explicitly documented.

Mechanism: GPU rental + Bittensor incentive emission. Critical economics: GPU-hour rental utilization, operator-set pricing, model/GPU scoring, subnet emission dynamics, registration cost and hardware cost.

### 4. NodeAI Host — VERIFIED / curated datacenter supply
Official host page accepts individuals/businesses only after approval and specifically asks for GPUs in a qualified datacenter. Approved hosts install NodeAI hypervisor software, list servers in the marketplace, set their own prices, and earn when GPU/CPU/RAM/disk resources are rented. Published platform fee: 25%. Current public pricing confirms active GPU instance inventory across several models. This is not an ordinary low-cost VPS bot path; it is curated GPU/datacenter hosting. No Azerbaijan-specific eligibility or public KYC detail found.

Mechanism: GPU/VM host marketplace. Net model: 75% of collected host-side price (before any other deductions) minus datacenter/hardware/network/electricity/depreciation.

### 5. Kunagi Systems Worker — WATCHLIST / early but more concrete than Run 057
Current official site describes a permissionless GPU worker path: router chooses eligible workers by model, availability and measured speed; usage is metered per token and workers earn for compute. Site states any GPU can join, worker benchmarking is used, and a bond is used for higher tiers with slashing on failed verification. Docs still say launch supply can include rented or owned GPUs while the worker marketplace is being built, so maturity and real third-party paid utilization remain uncertain.

Mechanism: decentralized inference marketplace. Unknowns: exact worker payout rate, withdrawal asset/path, production buyer volume, bond size by tier, KYC/geography.

### 6. Scalattice Provider — VERIFIED onboarding / demand-dependent economics
Official provider page describes one-command Windows/Linux GPU agent, automatic inference-job routing, no setup fee, per-job earnings, dashboard payout tracking, minimum payout balance $10, schedule controls, and an open-source MIT agent. Scalattice explicitly models a demand percentage and warns earnings are not guaranteed. Provider keeps the majority of developer spend. Consumer and datacenter GPUs are supported; NVIDIA is recommended. No Azerbaijan-specific restriction found.

Mechanism: GPU inference marketplace. Dominant unknowns: actual live demand/fill rate and exact provider share by model/job.

### 7. SILO Storage Node — VERIFIED docs / economics weak unless utilization is high
Official docs allow either personal computer or dedicated server. Minimum free storage: 500 GB; connectivity >=5 Mbps upload / 25 Mbps download; uptime target >=99.3%. Node operators are paid for actual storage and egress used by SILO-operated Orbitals. Published rates as of 2025-01-01: $2.03/TB-month storage, $2.70/TB egress, $2.70/TB audit/repair, paid in SILO tokens based on USD-equivalent value at payout time. No Azerbaijan rule found.

Mechanism: storage + egress marketplace. Net model must include disk depreciation, server/storage rent, bandwidth/egress, token liquidity and actual stored TB/utilization. Dedicated-server economics may be unattractive at low fill.

### 8. Sentinel dVPN Node — VERIFIED / Linux bandwidth supply
Current official site explicitly advertises Linux dVPN nodes that provide bandwidth and earn rewards and reports 3,200+ node operators. Current docs provide containerized node configuration with multiple VPN service types. This remains the existing bandwidth/VPN-relay mechanism. Precise earnings depend on sold traffic, node pricing, geography and token economics. No Azerbaijan-specific prohibition found in checked official material.

### 9. UPGO.IO Relay Leaf — WATCHLIST / production claims need external corroboration
Current 2026 first-party whitepaper describes a Solana-based bandwidth-sharing relay network, Linux x64/ARM64 support, daemon/CLI operation and BNC token rewards based on contribution. It claims thousands of active nodes and multi-TB daily traffic, but these are first-party metrics and were not independently attributed to buyer-paid demand in this pass. Linux server deployment is technically possible. No explicit Azerbaijan/KYC restriction found.

Mechanism: bandwidth/IP relay. Treat as WATCHLIST until token liquidity, attributable demand and payout behavior are independently verified.

### 10. SOMA — VERIFIED testnet path / strategically important autonomous-worker lead
Current official docs describe data submitters, model developers and validators as reward roles. The quickstart explicitly supports AI agents and demonstrates an automated submitter that streams source files, scores them against open targets and submits valid matches. Every 24 hours the network creates targets; first valid submission wins and reward splits with the winning model. The checked quickstart requires a funded **testnet** account and GPU scoring via Modal, so this is not yet evidence of liquid mainnet income. No Azerbaijan/KYC restriction found.

Mechanism: AI/data competition worker. Strong fit to the original autonomous-machine-work goal, but current cash-equivalent economics remain unproven until mainnet/token liquidity and reward value are established.

## Compact alternative-vocabulary spot-check
Queries used supplier/host/operator/worker/inference-provider/storage-operator/machine-jobs/relay-provider terminology.

### New independent projects surfaced
1. **Swan Inference** — decentralized inference API with GPU-provider role; official page says providers earn by serving inference and settlement is in USDC. This is an existing compute/inference mechanism, but an independent provider project requiring validation.
2. **AntSeed** — open provider market where a provider can serve raw inference, routing, or a specialized AI agent, set its own price, and receive USDC for settled deliveries. Particularly relevant because it combines GPU/API resale and agent-service supply under one machine-readable market.
3. **UsePod** — open inference marketplace where operators can run local GPU backends or relay upstream API keys, set prices and earn USDC. Existing inference/API-resale mechanism, but a distinct platform.
4. **DeCloudX** — node economy advertising compute, GPU, storage, relay and validator tiers with DCX staking and usage-linked earning. Multiple known mechanisms bundled under one platform; production/liquidity and demand need validation.

### Duplicate/adjacent result
- **Hugging Face Inference Providers registration** is a supplier integration/channel for established inference-provider organizations, not a simple idle-resource marketplace. It maps to the build-once/inference-service business channel already covered.

## Completion decision
Taxonomy saturation remains extremely high: Run 058 again found **0 new economic mechanisms**. But project-level saturation is not yet sufficient because the compact spot-check found four independent provider platforms that were not already normalized in the repository search.

Therefore define only one narrow follow-up:

**Run 059 — validate Swan Inference, AntSeed, UsePod and DeCloudX, then repeat the same compact supplier-role spot-check once.**

If Run 059 yields 0 new mechanisms and only duplicates/negligible new viable projects, mark the project COMPLETE. If it surfaces another material cluster, continue with only that cluster.

## Safety/integrity
No CAPTCHA bypass, fake engagement, prohibited multi-accounting, spam, ad fraud, unauthorized access/scraping, stolen resources, cryptojacking, KYC/geofence evasion, or automation of human-only tasks was treated as viable.