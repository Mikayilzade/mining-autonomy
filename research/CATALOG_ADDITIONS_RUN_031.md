# Catalog additions / corrections — Run 031

Date: 2026-08-16

These entries are durable deltas. They should be folded into `CATALOG.md` when a safe full-file update is available.

## A2 — GPU / AI compute marketplaces

| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Telegram COCOON GPU Worker | VERIFIED / RESTRICTED economics | Yes, specialty bare metal | Confidential AI inference; TON per processed requests | Production requires Intel TDX-capable server + NVIDIA H100+ CC GPU; RTX unsupported for production. Public worker tooling; request-linked TON payments. Utilization, exact provider net rate, Azerbaijan/KYC and cloud-host rules unresolved. |
| io.net Supplier | VERIFIED | Yes for supported Linux hardware; also device-based | GPU/CPU compute jobs + supplier/block rewards in IO | Upgrade existing catalog entry from UNVERIFIED. Current IO Worker onboarding/binaries and supplier earnings docs are live. Confidential compute is a capability extension, not a new mechanism. Economics/geography still need normalization. |
| DICOMPUTE Provider | WATCHLIST | Yes technically via Linux CLI; also desktop | Background private inference | Public alpha/pilot. CPU-only possible; GPU optional; 8GB+ RAM; auto model selection/background serving. Reward currency/split/withdrawal/utilization not sufficiently disclosed. |
| c0mpute Contributor GPU Worker | VERIFIED / economics pending | Potentially yes via native worker; also browser/home | Paid inference jobs / served tokens; Solana settlement | Public worker code, OpenAI-compatible demand API, browser/WebGPU and native/Ollama workers. Live public data reports credits spent, USDC deposits and USDC paid to workers. Dedicated economics/geography normalization required. |

## Provider-discovery vocabulary additions
Future saturation passes must include:
- contributor GPU
- native inference worker
- browser inference worker
- serve tokens earn
- permissionless inference worker
- decentralized OpenAI-compatible inference provider
- GPU contributor payouts
- USDC worker payouts
- confidential inference worker
- attested GPU worker

## Anti-duplication rule
COCOON, io.net confidential compute, DICOMPUTE and c0mpute all collapse economically into **customer-paid AI inference/compute supply** despite different privacy/token/attestation architectures. They are distinct projects, not distinct top-level mechanisms.
