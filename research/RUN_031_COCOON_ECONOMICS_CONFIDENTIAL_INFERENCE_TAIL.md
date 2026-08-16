# Run 031 — COCOON provider economics + confidential-inference tail sweep

Date: 2026-08-16
Status: **completed**

## Objective
Normalize Telegram COCOON's provider reality and economics, validate DICOMPUTE, re-check 0G/io.net confidential-inference supplier paths, and sweep worker/supplier/contributor terminology for current inference networks.

## Executive result
Run 031 produced **0 new top-level economic mechanisms**. COCOON is now much better normalized and clearly exposes a production-oriented, self-configured GPU-worker path with request-linked TON payments. DICOMPUTE is technically real but still public alpha and does not disclose enough reward economics to treat as dependable income.

However, the tail sweep found one **material current project-level provider cluster that had not been captured in the durable checkpoint: c0mpute**. It exposes contributor GPU workers, an OpenAI-compatible demand API, on-chain settlement on Solana, and a live public network-data page showing credits, USDC deposits and USDC paid to workers. This is economically the same customer-paid inference mechanism, not a new category, but it is material enough that project-level saturation is **not yet complete**.

## 1. Telegram COCOON — provider reality normalized
Current first-party COCOON documentation confirms:
- GPU owners run `worker` instances and earn TON for processed AI inference requests.
- Production workers require a Linux server with Intel TDX-capable CPU, NVIDIA confidential-computing GPU, and QEMU with TDX support.
- Official GPU docs say **NVIDIA H100 or newer** with confidential-computing support; consumer RTX GPUs are not supported for production.
- Tested hardware includes H200 NVL.
- GPU attestation may require an updated CC-enabled VBIOS obtained through NVIDIA support.
- Production uses a `seal-server` plus TDX guest worker; one seal server can serve multiple workers.
- Current multi-GPU scaling is one independent worker/TDX guest per GPU; each worker has its own wallet/keys/instance.
- Provider config includes a TON owner wallet and a `worker_coefficient` price coefficient; therefore providers expose a pricing parameter, while the proxy selects workers based on model/load/reputation and network configuration.
- Architecture docs describe payment as client -> proxy -> worker; proxies receive client payment, pay workers for completed work and take commission.
- Current proxies are operated by the COCOON team; future proxy operation is intended to open more broadly.
- Production instructions are publicly available and do not describe an application/curation step for ordinary worker setup. Treat worker participation as technically self-serve **subject to hardware, root-contract/network admission and live network acceptance** rather than claiming guaranteed open admission.

### Automation and infrastructure fit
- Server-native: **yes**, but specialty bare-metal/TEE hardware rather than ordinary VPS.
- Automation: **5/5** after setup; worker is a persistent service and exposes HTTP stats/health endpoints.
- Ordinary cloud VM: generally unsuitable because TDX BIOS configuration, VFIO GPU passthrough and CC-mode/VBIOS control may be unavailable or forbidden.
- Multiple GPUs: scale by multiple worker instances today.

### Economics
Revenue is request-driven TON settlement. The docs establish the payment mechanism but do **not** provide enough public evidence for a stable net TON/GPU-hour figure, realized utilization distribution, break-even utilization, or a universal provider fee split.

Required pilot metrics before CAPEX:
`net per GPU-hour = worker TON receipts converted at executable off-ramp price - hardware depreciation - electricity - networking - hosting - TON tx/withdrawal costs - maintenance`

Measure separately:
- idle hours vs billed requests;
- tokens/sec and requests/hour by supported model;
- effective TON/request and TON/GPU-hour;
- proxy/network commission actually deducted;
- outage/reputation effect on routing;
- hardware purchase or rental cost;
- TON liquidity/off-ramp and tax/withdrawal friction in Azerbaijan.

### Geography/KYC
First-party technical docs do not establish Azerbaijan eligibility or a formal KYC rule. Therefore status is **unknown, must validate live**. Wallet-level permissionlessness is not enough to prove legal/regulated off-ramp availability.

Classification: **VERIFIED current provider role / RESTRICTED economics & geography**.

## 2. DICOMPUTE — technical provider path verified, income still alpha
Current provider dashboard confirms:
- public alpha / pilot program;
- macOS, Windows and Linux support;
- desktop app plus pure-Go CLI connector;
- CPU-only operation is possible for smaller models; GPU accelerates/larger models;
- 8 GB+ RAM baseline;
- automatic hardware detection, model selection/download, background serving and coordinator routing;
- Linux/server CLI path via `dico-provider serve`;
- Apple Silicon hardware attestation offers a higher trust tier.

The developer side exposes an OpenAI-compatible paid-service surface, proving a coherent demand-side product exists.

Still missing from public first-party material retrieved this run:
- reward currency/unit;
- exact provider pricing or split;
- withdrawal procedure/minimum;
- payout history/liquidity;
- realized demand/utilization;
- region/KYC constraints.

Classification: **WATCHLIST / public-alpha provider implementation verified, monetary realization unverified**.
Automation: technically 5/5 after login/setup.

## 3. io.net confidential compute re-check
Current io.net material confirms the existing supplier mechanism remains live:
- IO Worker onboarding exists for GPU/CPU suppliers;
- Linux worker binaries and unattended/silent-auth style operation exist;
- supplier earnings are paid in IO Coin while customers pay in USDC;
- earnings dashboard tracks compute hours/jobs and claimable earnings;
- separate block rewards accrue hourly subject to eligibility/slashing;
- io.net also maintains current confidential-compute/attestation tooling for Intel TDX and NVIDIA confidential GPUs.

This is **not** a new provider mechanism: confidential inference is a capability/market segment layered on the already-known io.net compute-supplier role.

Catalog consequence: io.net should no longer remain merely UNVERIFIED in the durable catalog. Treat as **VERIFIED supplier role; economics/geography require normalization**.

## 4. 0G Compute re-check
Current 0G first-party docs clearly expose a Compute product and a `Provider Setup` documentation family, while the broader node stack includes validators/storage/DA roles. The search did not produce evidence of a distinct new confidential-inference supplier mechanism beyond the existing compute-provider/provider-setup family.

Classification consequence: no new economic category. Keep 0G Compute as an existing compute-provider lead and separately validate provider payment/mainnet economics if not already normalized elsewhere.

## 5. Material new provider discovery — c0mpute
Current project repository describes c0mpute as a decentralized inference network on Solana where **anyone can plug in a machine and earn for the tokens it serves**.

Provider architecture:
- contributor GPUs can run via browser/WebGPU or native worker/Ollama;
- orchestrator dispatches jobs, bills credits and verifies workers using anti-cheat checks;
- an OpenAI-compatible API creates a real machine-readable demand surface;
- payouts settle on Solana;
- worker code is in the public `c0mpute-worker` tree.

Most important economic evidence: the project's public data page exposes live aggregate metrics including:
- jobs/day;
- tokens generated/day;
- sampled workers online;
- credits spent/day with 1 credit = $0.01;
- cumulative USDC deposits;
- **USDC paid out to workers**;
- buyback/staker-reward aggregates.

This is substantially stronger than points/testnet-only evidence because it exposes demand-side credits and worker cash-like settlement metrics. It still does not prove a specific worker is profitable.

### Fit
- Server-native: **native worker potentially yes**, subject to the worker/runtime/hardware path and any provider-side policy not yet normalized.
- Home/device fit: yes for browser/WebGPU and native consumer GPUs.
- Automation: likely 4–5/5 for native worker; browser mode is less server-native.
- Revenue driver: paid inference jobs / served tokens, with network-level USDC worker payouts visible.
- Initial capital: depends on existing GPU vs purchased/rented GPU.
- Key unknowns: exact worker payout formula, minimum hardware, queue/routing preference, withdrawal/KYC/geography, anti-cheat false-positive risk, current per-GPU utilization and whether VPS/cloud GPU participation is supported/allowed.

Classification: **VERIFIED current contributor/provider mechanism; economics and geography require dedicated normalization**.

Why material: it is not a new mechanism, but the combination of current contributor worker code, demand API and live worker payout telemetry is strong enough to count as a new viable project-level cluster and blocks completion.

## 6. Safety/ToS boundary
No human-task botting, CAPTCHA bypass, fake demand, multi-accounting or utilization spoofing is needed for any candidate above. Provider integrity/anti-cheat controls must be respected. Cloud GPU re-rental must be checked against the upstream host's ToS before deployment.

## Durable conclusions after Run 031
1. COCOON is a real high-CAPEX confidential-inference worker network, not a generic VPS bot.
2. Its production hardware floor is currently H100+ confidential GPU plus Intel TDX-class server requirements; consumer RTX is not production-supported.
3. COCOON exposes worker pricing configuration but public docs still do not give enough utilization/realized-revenue data to claim profitability.
4. DICOMPUTE is technically real and unusually accessible, but public-alpha reward realization remains too opaque.
5. io.net confidential compute is an extension of a verified supplier marketplace, not a new mechanism.
6. c0mpute is a material missed current provider project and therefore provider-level saturation has not yet converged.
7. Across all four projects, **paid utilization remains the dominant unknown**.

## Saturation consequence
Top-level mechanism novelty this run: **0**.
Material new provider projects: **1 (c0mpute)**.
Taxonomy saturation: **very high**.
Project/provider saturation: **high, not complete**.

## Next run
**Run 032 — c0mpute worker economics + final inference-provider convergence pass.**

Priorities:
1. Normalize c0mpute native worker requirements, payout formula, worker admission, USDC settlement/withdrawal, current worker count/utilization and anti-cheat constraints.
2. Determine whether c0mpute native worker can run unattended on Linux server/bare metal and whether cloud GPUs are acceptable.
3. Check c0mpute geography/KYC/account requirements and Azerbaijan/off-ramp dependencies.
4. Re-sweep current inference-provider projects under `contributor GPU`, `native worker`, `browser worker`, `serve tokens earn`, `OpenAI-compatible decentralized inference`, `permissionless inference worker`, and similar terminology.
5. Dedupe against COCOON, io.net, DICOMPUTE, Nosana, Golem GPU, Bittensor, Akash, Targon/Tenzro and existing catalog.
6. If Run 032 yields no material new provider cluster, immediately perform the final all-category saturation pass before marking COMPLETE.
