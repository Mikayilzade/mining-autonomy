# Run 033 — Inference-worker normalization + fresh tail discovery

Date: 2026-08-16
Status: **completed**

## Goal
Normalize the six fresh inference-worker leads from Run 032, distinguish production cash-like earning from pre-launch/testnet/credits, and test whether provider-tail discovery has converged.

## Executive result
Provider-tail discovery has **not** fully converged.

The six Run-032 leads mostly remain early-stage/watchlist rather than proven net-profitable production income. However, the same alternate-vocabulary pass surfaced **Dispatch**, a distinct current project that implements agent-submitted machine jobs routed to idle devices, with desktop/mobile workers, signed receipts, x402 payment design and testnet/devnet token settlement. This is not a new top-level economic mechanism, but it is a new material project/operator implementation and prevents project-level saturation from being declared.

No new top-level economic mechanism was found.

---

## 1. Basis
Classification: **WATCHLIST / technically runnable worker, production rewards not yet live enough for income classification**
Automation: 5
Resource: GPU inference
Server-native: yes in principle (self-hosted worker + Ollama); cloud-host permissibility still provider-specific.

### What is current
- Worker is a standalone package and can be run locally/self-hosted.
- Valid EVM reward address is required to accrue rewards.
- Worker registers, heartbeats and serves jobs through a hosted or self-hosted orchestrator.
- Current worker package supports Ollama and echo; registration also accepts vLLM/external declarations.
- Worker can publish signed model/price/capacity offers.
- Reward accounting is deterministic from job charge minus protocol fee, with future quality/uptime/latency multipliers.
- Current public market showed only one published offer, already expired.

### Critical income limitation
First-party status is unusually explicit: public worker routing is not yet actually routing contributor traffic in the normal public path, most current traffic is served by a hosted upstream, and reward settlement is/was gated by configuration/dry-run state. The live site also describes the public API as a free metered demo and says contributor routing activates when a verified worker is online/eligible.

### Economics
Published market example: credits are USDC-pegged at $0.001/credit; sample ask showed roughly $0.088/M prompt tokens and $0.3523/M output tokens. Receipts describe worker 90% / protocol burn 10% for the referenced market flow. This is **price evidence, not realized utilization evidence**.

Net formula:
`Net = routed paid jobs × worker share − GPU/CPU/electricity/cloud cost − model storage/bandwidth − downtime/maintenance − token/liquidity/off-ramp costs`

Dominant unknown: paid contributor-worker utilization.

Azerbaijan/KYC: unresolved; live wallet/provider onboarding required before CAPEX.

Verdict: serious watchlist, not yet deploy-for-profit.

---

## 2. Open Communication (0_C)
Classification: **WATCHLIST / very early**
Automation: 4–5 conceptually
Resource: browser/native GPU inference

### What is current
- First-party site advertises contributor GPU inference through browser or native worker.
- Economic unit is credits; whitepaper states 1 credit = $0.01.
- Advertised split: worker 70%, stakers 10%, protocol 20%.
- Credits are bought with SOL; $0C is described as the ownership/settlement token layer.
- Site reported **0 active nodes** in the retrieved current page.
- Whitepaper is explicitly early/draft-stage material rather than mature audited production economics.

### Income quality
The economic design is coherent, but no durable evidence was found in this run of sustained active-node supply, realized worker payouts, stable job utilization, or mature public worker telemetry.

Verdict: keep as watchlist; do not treat advertised 70% share as realizable income yet.

---

## 3. Kunagi Systems
Classification: **WATCHLIST / marketplace being built**
Automation: 5 if native worker becomes production-ready
Resource: GPU inference

### What is current
- First-party docs define a native worker lifecycle: install/authenticate, benchmark GPU/runtime, list models, receive routed jobs, stream responses, receive credit.
- Browser, native and bootstrap workers are distinguished.
- Reward accounting design: `worker_reward = job_price × worker_share`; staking can later boost share.
- Worker bonding/slashing is a planned verification/collateral mechanism.
- Official disclosures explicitly state that not all described staking, bonding, trustless-verification and pay-per-call settlement mechanisms are live.
- Docs state launch supply can include rented/owned GPUs while the worker marketplace is being built.

### Income quality
Current documentation proves a real provider architecture and intended paid marketplace, but not mature public realized earnings, withdrawal liquidity or utilization distribution.

Azerbaijan: official terms only say access may be restricted where law requires; no country-specific admission proof.

Verdict: watchlist; technically credible design, economics still pre-maturity.

---

## 4. Jatevo decentralized inference
Classification: **WATCHLIST / early access**
Automation: 5 when contributor worker opens
Resource: CUDA GPU inference

### What is current
- First-party site documents decentralized contributor GPUs, open-model routing and request-linked $JTVO earning.
- GPU-owner flow: install Jatevo worker on CUDA GPU, stake $JTVO, earn per served inference request, monitor dashboard.
- Decentralized contributor access remains behind a waitlist/early-access gate.
- Jatevo simultaneously advertises live dedicated GPU rental inventory on the centralized/managed side, so live customer inference does **not** prove the contributor pool itself is generally open.

### Income quality
Contributor-side realized payouts, stake amount, public utilization distribution and unrestricted worker binary/admission were not established.

Verdict: watchlist; real demand-side product exists, but community-worker earnings are not yet an open production opportunity.

---

## 5. Kvasir
Classification: **WATCHLIST / DEVNET, non-cash utility reward today**
Automation: 4–5
Resource: GPU / CPU / NPU / phone; layer-split inference; hub/gateway roles

### What is current
- First-party site now documents KVR mechanics in much more detail than Run 032.
- Compute nodes earn contribution units based on tokens served × layer share × performance tier.
- Gateway host and hub host roles also receive infrastructure/uptime-style rewards; roles can stack.
- Node rewards are associated with Solana wallets.
- Source-available `linkcpp`/distributed engine is claimed as the runtime.
- Public site says current KVR is on **Solana devnet**, explicitly describes KVR as a utility/contribution token and says it is **not a tradable asset/price/investment**.
- Mainnet/on-chain reward program is on the roadmap; present settlement is devnet/off-chain-oriented.
- Production/commercial use of the BSL engine may require a purchased license.

### Income quality
This is a technically distinct and interesting provider topology, especially because hub/gateway/compute roles can stack, but current KVR is not production cash income.

Verdict: keep as high-interest watchlist, not current income.

---

## 6. Senda
Classification: **WATCHLIST / early paid preview with stronger evidence than most peers**
Automation: 5
Resource: GPU / Apple Silicon / other supported local inference hardware

### What is current
- Public peer-to-peer inference mesh is live and described as early access.
- Linux/macOS/Windows node software is advertised; desktop can stay online automatically.
- Paid `/v1` API preview exists; mesh peers serve paid requests by default with fallback provider possible.
- Contributor credits are explicitly **not cash**.
- A second accounting unit, **Peer USD**, may accrue on paid `/v1` mesh serves.
- Earner dashboard requires a bound Solana wallet.
- Public docs say Peer USD can be withdrawn as USDC when enabled/eligible and subject to caps/minimums.
- Public settlement metrics page exposes aggregate USDC liabilities/payout concept, though values were dynamically loaded and not captured in this pass.

### Income quality
Senda is stronger than a points-only network because the project explicitly separates non-cash credits from paid-served Peer USD and USDC withdrawal. Still, it is early access, utilization is unknown, payout thresholds/caps require live account verification, and peer economics are not stable enough for a profitability claim.

Verdict: **serious watchlist / pilot candidate later**, especially for owned hardware; do not buy hardware until measured utilization exists.

---

## 7. New material lead: Dispatch
Classification: **WATCHLIST / testnet-devnet beta**
Automation: 5
Resource: phone/desktop CPU/GPU inference and simple machine tasks
New mechanism? **No** — still paid machine-readable compute/task execution.
New material implementation? **Yes**.

### Why it matters
Dispatch maps unusually closely to the original project target: autonomous machines processing simple online jobs rather than pretending to be human microtask workers.

First-party docs/repository describe:
- AI agents submit jobs over HTTP.
- Coordinator routes jobs to idle phone/desktop workers.
- Job types include LLM inference, summarization, classification and data extraction.
- Desktop worker uses Node.js + Ollama and picks jobs over WebSocket automatically.
- Workers sign ed25519 receipts.
- x402 is used/designed for machine-native payment gating.
- Protocol fee: 5% per job.
- No stake required for base participation; higher staking tiers are planned for priority.

### Current economic limitation
The current site/docs are explicit that the network is on **Monad testnet + Solana devnet**. BOLT/wBOLT settlement is therefore not yet production cash income, and Jupiter liquidity/auto-swap is described as contingent on a live BOLT/USDC pool.

### Server-native fit
The public marketing emphasizes phones/laptops/desktops, while the desktop worker is ordinary software and therefore technically could run headlessly. However, **generic rented-VPS eligibility is not yet proven** and should not be assumed. A future run should inspect worker requirements and Terms for datacenter/server restrictions.

Verdict: add to serious watchlist; strong conceptual fit, not current cash-producing opportunity.

---

## Dedupe and saturation conclusion
All seven normalized projects belong to already-known families:
- decentralized inference marketplace;
- paid machine-task/compute routing;
- token/credit settlement for verified machine work;
- uptime/infrastructure rewards layered around compute.

Therefore Run 033 adds **0 new top-level mechanisms**.

However, the discovery of Dispatch means the project-level provider tail is still producing material implementations. The correct next step is another dedicated inference/machine-job tail control pass using newer vocabulary such as:
- x402 compute worker
- agent compute marketplace
- idle-device inference worker
- OpenAI-compatible contributor node
- phone compute worker
- verified inference receipt worker
- ERC-8004 worker marketplace
- Solana/Monad/Base machine job worker

If that pass produces no additional material current providers, proceed to a final all-category control pass.

## Safety / compliance
No prohibited automation was pursued. These systems sell machine-readable compute or tasks. Future implementation must still check provider Terms, local law, KYC/geofencing, cloud-provider AUP, model/content policies, tax and off-ramp availability.

## Completion state
**IN PROGRESS.** Taxonomy saturation remains very high; project-level saturation is high but not yet complete.
