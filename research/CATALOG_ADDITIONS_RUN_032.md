# Catalog additions — Run 032

Evidence date: 2026-08-16

## c0mpute Contributor GPU Worker
- Category: customer-paid decentralized AI inference compute
- Status: **VERIFIED provider mechanism / economics pending**
- Resource: GPU / Apple Silicon memory-compute
- Server-native: yes on qualifying GPU host; upstream host ToS still required
- Bare metal: yes
- Residential/home hardware: yes
- Automation: **5/5** native CLI after setup
- Text requirements: Node 18+, Ollama, 20GB+ VRAM, ~17GB model disk
- Image requirements: ComfyUI, 24GB GPU recommended, ~14GB model disk
- Multi-GPU: one worker per NVIDIA GPU; supervisor auto-restarts failed child after 30s
- Scale cap: max 10 workers/IP and 10/account
- Revenue: completed text jobs by tier/tokens; image jobs per render
- Payout: internal ledger -> treasury-sent SPL USDC to worker-provided Solana address
- KYC/geography: unknown; Azerbaijan must be tested live
- Main unknown: realized USD/token or USD/render and utilization
- Confidence: high on technical/provider path; medium on economics

## Basis Worker
- Category: decentralized inference marketplace
- Status: **WATCHLIST / market opening**
- Resource: GPU inference
- Server-native: likely, pending worker-runtime validation
- Automation: likely 5/5
- Revenue: completed verified jobs earn `$BASIS`; failed jobs earn nothing
- Demand/payment surface: OpenAI-compatible API, USDC-pegged credits, Base settlement
- Critical caveat: first-party site reported no verified worker offers yet / contributor network being activated
- Next validation: worker software, contract/payout, real jobs/offers, liquidity

## Open Communication GPU Contributor
- Category: decentralized inference worker
- Status: **WATCHLIST / very early**
- Resource: GPU via browser or native worker
- Automation: native path potentially 5/5; not yet normalized
- Advertised economics: worker receives 70% of credits served
- Critical caveat: site showed 0 active nodes at retrieval; whitepaper marked draft v0.1
- Next validation: source/runtime, actual jobs, implemented payout, token/credit liquidity

## Kunagi Native Worker
- Category: decentralized inference marketplace
- Status: **WATCHLIST**
- Resource: GPU / local model runtime using CUDA/Metal/Vulkan
- Server-native: likely
- Automation: likely 5/5
- Provider flow: authenticate, benchmark, list models, receive routed jobs, earn contribution credit
- Unknown: exact reward unit, withdrawal/liquidity, mature production demand
- Next validation: executable/source, provider terms, payout mechanics

## Jatevo Decentralized Inference Contributor
- Category: decentralized inference worker + stake-gated provider access
- Status: **WATCHLIST / early access**
- Resource: CUDA GPU
- Provider requirement: stake `$JTVO`
- Revenue: `$JTVO` per served inference request
- Critical caveat: contributor network presented behind waitlist
- Risks: token liquidity + stake opportunity cost + utilization
- Next validation: production launch, stake size, worker binary, actual payouts

## Kvasir Node
- Category: sharded/layer decentralized inference
- Status: **UNVERIFIED/WATCHLIST**
- Resource: GPU / CPU / NPU / phone; serves model layers/slices
- Gateway: OpenAI + Anthropic compatible
- Claimed reward: KVR for layers served
- Server-native: potentially yes; runtime documentation mentions native workers and 443 relay
- Unknown: KVR definition/liquidity, live network jobs, withdrawal, provider admission
- Next validation: node package/source, network explorer, reward contract

## Senda Contributor Node
- Category: mesh inference provider
- Status: **WATCHLIST**
- Resource: capable Mac/GPU box
- Demand: paid OpenAI-compatible `/v1` preview
- Revenue: contributor credits; paid mesh serves may accrue peer USD; wallet binding can request payout
- Unknown: exact USD rate, minimum/withdrawal, provider eligibility, live utilization
- Next validation: node runtime/source, payout mechanics, paid-mesh traffic
