# Run 023 — Tight Provider-Tail Convergence Pass

Date: 2026-08-16
Status: COMPLETE (project remains IN PROGRESS)

## Objective
Search current provider-role vocabulary rather than generic DePIN terms, with emphasis on live/current 2025–2026 provider software, payout paths, automation and evidence of customer-funded demand.

## Result summary
- New top-level economic mechanisms: **0**.
- Material genuinely new provider projects: **3** (DCP, WorldLand Cloud, StorX).
- Additional restricted/watchlist provider projects: **4** (Abakos, IonDEX, CryptoGPU, ComputeMarket).
- Taxonomy saturation therefore remains high, but project-level tail discovery is still materially productive.
- Completion gate is **not met**.

## Material new providers

### 1. DCP (Saudi sovereign AI GPU provider network)
Classification: **VERIFIED / RESTRICTED**
Category: GPU inference / GPU rental marketplace
Server-native: technically yes for compatible Linux GPU rigs, but economically/geographically focused on Saudi Arabia
Automation: **5/5** after setup — detached daemon, automatic demand routing, successful-work billing

Current official provider page says:
- provider network is open;
- providers can attach NVIDIA or Apple Silicon rigs;
- demand routes automatically from agents/renters;
- provider keeps **75% of every billed token / published rate**, DCP fee 25%;
- payout is denominated in Saudi Riyal;
- Linux/Windows/macOS supported;
- rig joins an **in-Kingdom WireGuard mesh**;
- only successful work is billed;
- earnings calculator is explicitly illustrative, not guaranteed.

Economic formula:
`Net SAR/month = billed provider usage × 0.75 - electricity - depreciation - connectivity - maintenance - taxes/withdrawal costs`

Critical constraint: the product is explicitly KSA-resident / sovereign in-Kingdom AI infrastructure. Treat Azerbaijan participation as **not eligible unless official onboarding later confirms otherwise**. This is nevertheless a strong proof that autonomous agent-routed inference markets exist as a real commercial provider model.

### 2. WorldLand Cloud GPU Provider
Classification: **VERIFIED / RESTRICTED (early/testnet economics)**
Category: GPU cloud provider + PoW/mining fallback
Server-native: yes on Ubuntu/Docker/Kubernetes with public IP; dedicated/bare-metal-like infrastructure preferred
Automation: **5/5** for job scheduling after setup

Current official 2026 docs state:
- NVIDIA GTX 1080+ minimum, Ubuntu 20.04/22.04, Docker + NVIDIA Container Toolkit + Kubernetes;
- provider agent registers node and joins cluster;
- customers pay per-hour GPU usage in WL;
- **90% of service fee goes to provider, 10% to protocol**;
- providers set prices;
- when GPU is rented it serves customer jobs; when idle it can also be allocated to network mining;
- no provider capital requirement is listed for ordinary provider role, while high-tier/validator roles may involve staking;
- provider docs still mark exact reward rates / some network statistics as post-testnet or after mainnet, so realized demand and token liquidity are unresolved.

Economic formula:
`Net = paid GPU-hours × provider price × 0.90 + eligible mining rewards - electricity - depreciation - bandwidth - maintenance - token conversion costs`

Important: this is economically close to the Abakos “rent first / mine idle” idea, but is a separate current project and therefore material project-level novelty, not a new mechanism.

### 3. StorX Farm/Storage Node
Classification: **VERIFIED / RESTRICTED**
Category: decentralized storage provider
Server-native: **yes** — official material explicitly describes deploying a Server/VPS
Automation: **4–5/5** after installation, with uptime/reputation monitoring

Current official pages state:
- farmer/storage-node operators contribute storage capacity and receive SRX rewards;
- server/VPS deployment is supported;
- current indicative node requirements include 6-core CPU, 8 GB RAM (16 recommended), 1 TB HDD/SSD/NVMe, 10 TB bandwidth, 100 Mbps-class connectivity, 24/7/365 availability;
- farmers must stake SRX and maintain sufficient reputation;
- low reputation can reduce hosting rewards;
- current GitHub node setup uses Docker and warns of possible slashing.

Economic formula:
`Net = hosting rewards + staking rewards - VPS/bare-metal cost - storage cost/depreciation - bandwidth - SRX opportunity cost - expected slashing/reputation loss - conversion fees`

This project was missing from the durable catalog (Storj was present; StorX is a separate network).

## Additional restricted/watchlist discoveries

### Abakos
Classification: **WATCHLIST / RESTRICTED (public sandbox, not production mainnet)**
Category: compute rental + idle CPU/GPU mining fallback
Automation: target **5/5** Provider Agent

Current official status is unusually explicit: public sandbox is live, mainnet is still gated on audit/external validators. Provider economics claim customer-paid rental with a 3% settlement fee and idle mining proceeds split **88% host / 12% protocol destinations**. Current sandbox uses real USDC rails for mining buyback, but ABA is not yet a production-mainnet asset with established market value. Do not treat sandbox earnings as deployable production income yet.

### IonDEX
Classification: **WATCHLIST / RESTRICTED (alpha)**
Category: decentralized GPU session marketplace
Automation: **4/5** once Windows provider agent is online

Official site describes a provider agent, WSL2/Docker/GPU-runtime setup, provider-set pricing, payout wallet, automatic hosting of time-boxed sessions, and USDC payment flow on Base. Provider flow is currently described as alpha and Windows-based. Realized utilization/fees/payout history remain unresolved.

### CryptoGPU
Classification: **WATCHLIST / UNVERIFIED production readiness**
Category: GPU marketplace
Automation: claimed **5/5** daemon

Official docs describe provider agent installation, provider-set pricing and daemon mode. However the official marketplace explicitly labels displayed listings as **sample listings** and says live marketplace data will be available at launch. Therefore it is not yet evidence of a current deploy-and-earn production market.

### ComputeMarket
Classification: **WATCHLIST / UNVERIFIED**
Category: GPU marketplace
Automation: claimed provider agent / job matching

Official landing page claims provider agent installation, automatic matching, containerized workloads and pay-per-use provider earnings. Public evidence found in this pass is too shallow to establish fees, payout rail, production utilization, KYC/geography or durable provider economics.

## Dedupe / non-new outcomes
- ParalonCloud — already captured in Run 022; still a strong current Docker GPU provider path.
- OpenGPU — already captured; no independent mechanism change.
- ThreeFold — already captured; farmer vocabulary rediscovered it but produced no new mechanism.
- Render Network — already in catalog; node-operator monetization confirmed but not net-new.
- Autonomys farming — storage-farming mechanism already represented; project may deserve later catalog normalization but did not alter taxonomy.
- Hugging Face Inference Providers — provider integration is for established inference organizations, not a simple permissionless spare-server earning daemon; classify adjacent/build-business rather than “mining” bot.

## Economics normalization from this pass
1. Provider share is becoming a useful comparable metric across GPU markets: Paralon 80%, DCP 75%, WorldLand 90%, Abakos rental settlement effectively 97% before other product-specific cuts and idle-mining 88% host share.
2. These percentages are **not comparable profit guarantees** because utilization, buyer price, token liquidity and hardware eligibility differ.
3. “Rent first, mine idle” is now seen in at least two independent current projects (Abakos design/sandbox and WorldLand docs), suggesting a strategy family worth later implementation analysis: dynamically route owned compute to the highest compliant use rather than dedicating it to one marketplace.
4. Geography can dominate technical feasibility: DCP is technically easy but designed around KSA-resident infrastructure.
5. Early/testnet projects can publish precise splits while still lacking liquid realized economics; status must remain restricted/watchlist until customer demand and payout liquidity are measured.

## Run 023 saturation judgment
This pass found **three material live/current provider projects** plus multiple early-stage leads. Therefore the Run 022 convergence condition (“0–2 weak/restricted additions, then final short check”) failed.

The taxonomy is saturated, but the provider-project tail is **not yet saturated**.

## Next recommended run
Run 024 should target a different remaining tail rather than repeat generic GPU searches:
- current 2025–2026 `host node`, `storage provider`, `VPS node rewards`, `provider SDK`, `capacity marketplace`, `edge provider`, `CDN provider`, `bandwidth node operator` vocabulary;
- search official docs + current GitHub releases where possible;
- explicitly distinguish production mainnet, alpha/testnet, waitlist and dead projects;
- dedupe against StorX, WorldLand, DCP, Abakos, IonDEX, CryptoGPU, ComputeMarket and all earlier runs;
- normalize any explicit fee split / stake / minimum hardware / payout rail.

If this non-GPU provider-tail pass yields only 0–2 weak additions, then return to a final cross-category saturation check.