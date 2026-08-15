# Run 021 — Broad cross-directory / alternative-vocabulary control pass #4

Date: 2026-08-16
Status: **COMPLETED — project remains IN PROGRESS**

## Purpose
Test project-level saturation using differently-worded searches for server/resource providers, storage nodes, GPU hosts, machine-service markets and provider/supplier vocabulary. Directories/search results were used only as discovery leads; material candidates were checked against current official docs or official repositories.

## Saturation result
- New top-level economic mechanisms: **0**.
- Material genuinely new provider projects: **3** — DeNet Datakeeper, Iagon storage/compute provider, OpenGPU Provider.
- Material upgrade of an unresolved existing project: **Fluence Compute Provider**.
- Spheron supplier path remains curated/aggregated rather than public self-service.
- iExec still lacks a clearly surfaced 2026 ordinary self-service worker/workerpool onboarding path in this pass.

Taxonomy saturation remains **high**, but project-level saturation is **not yet complete** because this fourth control pass still found several real providers.

---

## Net-new provider findings

### 1. DeNet Datakeeper — VERIFIED / RESTRICTED
**Category:** decentralized storage provider

Current official GitHub repository describes DeNet Storage as a market where Datakeepers rent disk space and receive rewards from storage users. The current node stack has:
- Linux x86_64 and ARM64 CLI binaries;
- a web manager explicitly described as suitable for server/headless environments;
- node instructions for Ubuntu Server/CentOS-style server environments;
- direct statement that users pay for storage and Datakeepers are rewarded.

The official releases page shows a current Datakeeper Node v4.1.0 release dated 2026-07-21, materially strengthening live-project confidence.

**Server-native:** yes technically; current docs explicitly support server/headless installation.

**Automation:** 5 once configured, subject to storage maintenance and uptime.

**Capital/costs:** disk, bandwidth, server/host costs, Datakeeper license requirement, plus possible token/network costs. Exact license price and current realized utilization/revenue still need normalization.

**Economics:** customer-paid storage is the core value source; profitability depends on occupied TB, retrieval/traffic, license amortization and server/disk cost.

**Risks / unknowns:** license economics; exact payout asset/liquidity; demand/utilization; Azerbaijan onboarding; hosting-provider ToS; public-IP/network requirements.

**Next action:** deep economics + license/payout/KYC/geography validation.

### 2. Iagon Storage / Compute Node Provider — VERIFIED / RESTRICTED
**Category:** decentralized storage + compute provider

Current official documentation confirms active node-provider roles. Storage operators commit capacity and earn rewards; compute providers are scored by capacity/performance and have a current reward/fee design.

Important current economics from official docs:
- storage subscriber fees: **90% distributed to storage nodes and delegators**, 7% treasury, 3% IAG buyback;
- compute subscriber fees: **90% distributed to compute node providers**, 7% treasury, 3% IAG buyback;
- compute staking requirement is tied to committed capacity and IAG token price; current docs show a base USD-stake variable initially set to 80 per commitment unit, while warning reward parameters can change;
- storage tiering considers performance dimensions and committed capacity rather than pure pledged size.

**Server-native:** likely yes for compute; storage has node software/provider model. Exact bare-metal/VPS acceptance still needs explicit environment validation.

**Automation:** 4–5 after node deployment.

**Capital/costs:** hardware/server + required IAG staking/commitment + Cardano transaction fees.

**Economics:** unusually useful evidence because subscriber fees are directly allocated to providers, not only emissions.

**Risks / unknowns:** stake volatility/opportunity cost; exact current node minimums; demand/utilization; Azerbaijan access; payout liquidity; cloud/VPS acceptance.

**Next action:** hardware requirements, onboarding flow, geography/KYC and realized-fee/utilization check.

### 3. OpenGPU Provider — VERIFIED mechanism / RESTRICTED economics
**Category:** GPU compute marketplace / decentralized AI inference

Current official site provides a Provider Suite for Linux, Windows and macOS and explicitly markets earning from contributed GPUs. The management dApp can register GPU sources, track rewards, choose jobs manually or enable **automatic routing**.

**Server-native:** technically plausible on Linux GPU systems; ordinary public-cloud/VPS acceptance not yet proven.

**Automation:** 5 with automatic job routing.

**Payout:** OGPU token rewards are advertised for completed GPU tasks.

**Economics:** still incomplete — no trustworthy current public evidence in this pass for provider realized $/GPU-hour, utilization, minimum payout, staking/collateral, or Azerbaijan/KYC.

**Status rationale:** live provider path is current, but economics and admission constraints remain too incomplete for low-capital priority ranking.

**Next action:** provider hardware matrix, reward formula/token liquidity, onboarding admission, datacenter/VPS rules and demand evidence.

---

## Existing unresolved projects revisited

### Fluence Compute Provider — upgraded to VERIFIED / RESTRICTED
Current official Fluence material materially resolves the prior staleness problem.

Evidence:
- Dec 23, 2025 Provider App update describes a current web app for infrastructure providers that configures **bare-metal servers**, installs Fluence Provider Software and automates network/smart-contract interactions.
- Feb 3, 2026 year-end recap says the CPU/GPU marketplace has onboarded customers and a first GPU deal signed in Q4 2025.
- Current provider page invites operators to monetize idle servers and explicitly targets data-center, enterprise and regional operators.

**Conclusion:** provider mechanism and current onboarding activity are now sufficiently fresh to classify the provider path as real. It remains **RESTRICTED** for our low-capital target because the material strongly emphasizes bare-metal/data-center/provider infrastructure, not one cheap generic VPS.

### Spheron
Current 2026 product pages show a live multi-provider GPU marketplace, but supplier messaging emphasizes sourcing from a **certified data-center network** and supplier matchmaking. This supports a curated/professional supply model rather than proving open self-service third-party GPU hosting.

**Conclusion:** retain restricted/aggregated-supplier classification; do not count as a simple permissionless host bot.

### iExec
Current protocol explorer remains live, but this pass did not surface sufficiently current official 2026 documentation proving a simple ordinary user flow for joining as a public worker/workerpool supplier.

**Conclusion:** protocol/provider mechanism remains real; easy public supplier admission remains unresolved.

### Fleek
No sufficiently current production/liquid node-reward evidence surfaced in this pass to upgrade the prior restricted/watchlist state.

### dTelecom / Edge
No stronger admission/VPS-policy evidence than Run 020 was obtained in this pass. Retain prior classifications.

---

## Control-query observations

Alternative terms that were productive:
- `datakeeper`
- `provider suite`
- `idle servers`
- `compute provider app`
- `subscriber fee allocation to node providers`

This is important: provider opportunities are often hidden behind project-specific role names, not obvious phrases like "mine" or "host".

### New mechanism count by family
- decentralized cloud / idle server: 0 new mechanisms, 1 major provider upgrade (Fluence)
- GPU host/provider: 0 new mechanisms, 1 new provider (OpenGPU)
- storage node/server: 0 new mechanisms, 2 new providers (DeNet, Iagon storage)
- compute node: 0 new mechanisms, 1 new provider role within Iagon
- machine API/pay-per-call: 0 new mechanisms; IDLE rediscovered as already known
- bandwidth/CDN/relay: 0 material new provider projects in this pass
- workerpool/prover/relayer: 0 material new provider projects

## Economics lessons reinforced
1. **Customer-fee allocation** is stronger evidence than generic token emissions. Iagon's documented 90% subscriber-fee distribution is therefore higher-quality mechanism evidence than marketing-only rewards.
2. **Current software releases matter.** DeNet's July 2026 node release materially raises confidence that the provider path is live.
3. **Linux support does not prove public-cloud permission.** OpenGPU and Iagon still require explicit hosting-environment policy checks.
4. **Professional provider networks are a separate segment.** Fluence and Spheron show that provider supply can be real while still unsuitable for a cheap single-VPS experiment.

## Completion decision
Do **not** mark COMPLETE.

Run 021 found 0 new economic mechanisms but **3 material new provider projects** plus a significant Fluence upgrade. This fails the completion condition requiring almost no net-new viable projects.

## Next run
**Run 022 — role-name / repository-release tail sweep + economics normalization.**

Priorities:
1. search project-specific role vocabulary: datakeeper, farmer, executor, hoster, supplier, contributor, resource provider, capacity provider, edge worker, workerpool, render worker, inference provider;
2. sweep current GitHub releases/docs for live provider software that directory searches miss;
3. deep-check DeNet, Iagon and OpenGPU economics/admission;
4. revisit iExec/Fleek/Spheron/dTelecom/Edge only where fresh evidence appears;
5. track net-new material providers per query family.

If Run 022 produces 0 new mechanisms and only 0–2 weak/restricted projects, proceed to a final saturation check. Otherwise continue until the tail converges.
