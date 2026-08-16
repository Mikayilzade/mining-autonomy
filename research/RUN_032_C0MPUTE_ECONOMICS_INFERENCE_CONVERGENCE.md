# Run 032 — c0mpute worker economics + inference-provider convergence

Date: 2026-08-16
Status: **completed**

## Objective
Normalize c0mpute's native-worker reality/economics and run another deliberately different inference-provider tail sweep using contributor/native/browser-worker vocabulary.

## Executive result
Run 032 produced **0 new top-level economic mechanisms** but **multiple material project-level provider leads** that were not yet durably catalogued. Therefore the project is **not complete**.

The strongest normalized result is c0mpute: its native worker is genuinely headless-capable, supports unattended Linux operation through explicit CLI flags, runs one worker per NVIDIA GPU automatically, has a 10-workers-per-IP/account cap, uses 20GB+ VRAM for text and ~24GB recommended for image work, and exposes a real USDC withdrawal path on Solana from an internal worker balance. The exact public payout rate per token/image and realized per-GPU utilization remain unresolved.

The fresh convergence sweep also surfaced several 2026 inference-worker networks that require dedicated normalization before saturation can be claimed: **Basis, Open Communication, Kunagi Systems, Jatevo decentralized inference, Kvasir, and Senda**. Several appear early-stage, market-opening, waitlist, zero-node, preview or draft, so they are leads rather than assumed profitable deployments.

## 1. c0mpute native worker — technical normalization
Current first-party worker README/repository establishes:
- CLI: `npx @c0mpute/worker --token <token>`.
- Explicit non-interactive flags exist: `--mode max|image`, `--model qwen|supergemma`, `--gpu`.
- Text worker uses Ollama and currently offers Qwen3.5 27B or SuperGemma4 26B.
- Text requirements: Node 18+, Ollama, **20GB+ VRAM**, ~17GB model disk. README names RTX 3090/4090 and Apple Silicon 32GB+ as examples.
- Image worker uses ComfyUI + Chroma1-HD; **24GB GPU recommended**, ~14GB model storage.
- On Linux the worker can install/start Ollama itself unless the operator disables management.
- Multi-GPU rigs are supervised automatically: one worker process per NVIDIA GPU with per-card `CUDA_VISIBLE_DEVICES` and per-card Ollama port.
- Child workers are automatically restarted on a fixed 30-second backoff.
- The network currently caps accepted workers at **10 per IP and 10 per account**.
- Earnings are job-linked: text by tier/tokens generated; image jobs per render.

### Server autonomy
Classification: **SERVER-NATIVE capable on qualifying GPU bare metal / GPU VM, subject to upstream host policy**.

Automation: **5/5 after setup**. The non-interactive flags plus supervisor/restart behavior are sufficient for systemd/container-style unattended operation. A browser tab is not required for the native path.

Ordinary CPU VPS: **no** for practical earning because current worker modes require substantial GPU/Apple Silicon capacity.

Cloud GPU: technically plausible if the VM exposes the GPU and permits Ollama/ComfyUI, but c0mpute documentation does not itself prove that a given cloud host permits re-rental/third-party earning workloads. Upstream cloud ToS remains a mandatory gate.

## 2. c0mpute settlement / withdrawal
Current first-party source code in `lib/payout.ts` establishes a concrete USDC withdrawal mechanism:
- worker identity is tied to authenticated account identity;
- destination is a worker-supplied Solana address;
- withdrawal debits the worker's internal ledger balance before transfer;
- treasury sends SPL USDC to the destination address;
- destination ATA can be created by the treasury;
- failed payout logic is designed so the caller can restore worker balance.

This is stronger evidence than generic points or roadmap rewards: a real cash-like settlement path exists in code and the prior run found public aggregate USDC-paid-to-workers telemetry.

### Still unknown
Public material retrieved in this run did **not** establish a stable universal:
- USD/USDC per output token;
- USD/USDC per image render;
- minimum withdrawal;
- worker revenue share percentage;
- realized jobs/GPU-hour by model;
- realized earnings distribution by worker/GPU;
- Azerbaijan-specific account/KYC eligibility.

Do not infer profitability without those values.

## 3. c0mpute economics model
For a text worker:

`net_gpu_hour = (completed_output_tokens × realized_USD_per_token) - GPU_rental_or_depreciation - electricity - host/network - Solana/off-ramp fees - maintenance`

For image:

`net_gpu_hour = (completed_renders × realized_USD_per_render) - GPU_rental_or_depreciation - electricity - host/network - Solana/off-ramp fees - maintenance`

Critical empirical variables:
1. routed jobs per online hour;
2. output tokens or renders per job;
3. worker ledger credit actually earned;
4. rejected/canary/anti-cheat jobs;
5. payout-to-wallet realization;
6. idle-vs-busy ratio by model;
7. competition effect from live worker count;
8. IP/account cap effect on multi-GPU rigs.

Best future pilot: existing/cheaply rented single qualifying GPU for 24–72 measured hours before CAPEX.

## 4. Geography / KYC / account dependencies
The current worker path requires a worker token obtained through c0mpute's earn flow. The payout implementation references authenticated account identity and a user-supplied Solana destination wallet.

No first-party evidence retrieved here proves or rejects Azerbaijan eligibility. Therefore:
- provider eligibility: **UNKNOWN — live onboarding required**;
- formal KYC: **UNKNOWN**;
- wallet settlement: technically Solana USDC;
- practical local cash-out: must separately validate legal exchange/off-ramp availability, fees and tax treatment.

## 5. Fresh inference-provider leads from alternative vocabulary
The dedicated search used terms such as contributor GPU, native worker, browser worker, decentralized OpenAI-compatible inference and worker payout. It surfaced material project-level leads that were not in the durable checkpoint.

### Basis
Current first-party site describes:
- Base-native decentralized inference market;
- OpenAI-compatible inference API;
- workers publish models/prices/capacity;
- completed verified jobs earn `$BASIS`;
- worker lifecycle: connect EVM reward wallet, register, heartbeat, serve, earn;
- failed jobs earn nothing;
- customer credits are described as USDC-pegged;
- importantly, the site also says **market opening** and currently reports **no verified offers yet** / contributor network being activated.

Classification: **WATCHLIST / early live-market activation**.
Reason material: explicit native supply-side worker market and machine-payable inference economics, but not yet proven mature utilization/payout history.

### Open Communication
Current first-party site/whitepaper describes:
- browser or native contributed GPU workers;
- OpenAI-compatible inference;
- credits debited on completed work;
- workers advertised as earning **70% of credits served**;
- current public site displayed **0 active nodes** at retrieval;
- whitepaper is labeled **DRAFT v0.1**.

Classification: **WATCHLIST / very early network**.
Do not count advertised share as realized income until live jobs/payouts are proven.

### Kunagi Systems
Current worker guide describes:
- native worker target using CUDA/Metal/Vulkan via local model runtime;
- worker authenticates provider account, benchmarks capability, lists models, receives routed jobs and receives credit for completed work;
- browser/native/bootstrap worker distinctions;
- reward-pool concept for smoothing provider payouts.

Classification: **WATCHLIST — provider workflow technically documented; payout realization/liquidity still needs validation**.

### Jatevo decentralized inference
Current first-party site describes:
- contributor-run decentralized inference;
- worker agent on CUDA GPU;
- stake `$JTVO` to join contributor pool;
- earn `$JTVO` for served requests;
- routing by model availability, latency and stake;
- but decentralized participation is currently presented behind a **waitlist / early access**.

Classification: **WATCHLIST / not yet open production provider income**.

### Kvasir
Current first-party site describes:
- distributed model-layer serving across GPU/CPU/NPU/phone hardware;
- OpenAI + Anthropic compatible gateway;
- nodes advertised as earning `KVR` for layers served;
- a 443/WebSocket relay path for NAT-bound devices is documented.

Classification: **UNVERIFIED/WATCHLIST pending reward token, withdrawal, network status and actual provider-payout proof**.
Potential distinction: layer/shard contribution rather than whole-model worker, but economically still customer-paid inference compute.

### Senda
Current first-party site describes:
- mesh peers serving open-weight inference;
- paid `/v1` preview, OpenAI-compatible;
- contributor credits for tokens served;
- paid mesh serves may accrue peer USD;
- wallet binding can be used to request payout.

Classification: **WATCHLIST pending exact payout process, provider admission, live utilization and geography**.

## 6. Dedupe / mechanism result
None of the above creates a new top-level economic mechanism. All collapse into one or more already-known families:
- customer-paid inference compute;
- competitive/routed worker marketplace;
- sharded/layer inference contribution;
- token/credit settlement layered on compute;
- stake/collateral-gated provider access.

Therefore taxonomy saturation remains extremely high, but **project-level saturation failed again** because alternate provider terminology still surfaced multiple current 2026 projects.

## 7. Safety / ToS
No candidate requires CAPTCHA bypass, fake traffic, fake demand, human-task impersonation, unauthorized access or multi-accounting. Provider anti-cheat and IP/account caps must be respected. Cloud GPU re-rental must be checked against the upstream provider's ToS rather than assumed permissible.

## Run 032 saturation consequence
- New top-level mechanisms: **0**.
- Material project/provider leads added: **6** (Basis, Open Communication, Kunagi, Jatevo decentralized inference, Kvasir, Senda).
- c0mpute normalized materially: **yes**.
- Final all-category saturation pass: **not yet justified**, because inference provider-tail discovery is still producing fresh projects.
- Project state: **IN PROGRESS**.

## Next run
**Run 033 — normalize the six fresh inference-worker leads and test whether they are independent/live enough to remain in the serious catalog.**

Priority order:
1. Basis worker install/runtime, reward contract, payout/liquidity, worker admission and current offer/job counts.
2. Open Communication source/repository, worker installation, actual active jobs/payout path and whether 70% worker share is implemented vs roadmap.
3. Kunagi provider executable/source, reward unit and withdrawal.
4. Jatevo production status beyond waitlist, stake size, provider payout and worker availability.
5. Kvasir node software, KVR definition/liquidity, live jobs and payout proof.
6. Senda node runtime, peer-USD payout request mechanics, paid-mesh utilization and wallet/geography constraints.
7. Search exact project names plus `worker install`, `earn`, `withdraw`, `provider`, `node rewards`, repository/package registries and on-chain evidence.
8. If most collapse to pre-launch/watchlist and no further material provider project appears, perform another inference-tail control. Only then proceed to final all-category saturation.
