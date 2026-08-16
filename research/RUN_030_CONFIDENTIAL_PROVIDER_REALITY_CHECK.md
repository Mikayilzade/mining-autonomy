# Run 030 — Confidential-compute supplier / open-provider reality check

Date: 2026-08-16
Status: **completed**

## Objective
Revalidate the provider-side reality behind the TEE/confidential-compute cluster from Run 029, test whether Targon/Tenzro/SecretVM/Aleph/Akash are actually provider-income paths, and search alternate vocabulary for previously missed provider networks.

## Executive result
Run 030 produced **no new top-level economic mechanism**, but it did produce a **material new current provider cluster: Telegram COCOON**. Because this is a genuine current confidential-AI GPU supplier network with downloadable worker software and TON-denominated payments, project-level saturation is **not yet complete**.

A second small discovery lead, **DICOMPUTE**, appears to expose a public-alpha cross-platform inference-provider program, but its reward realization/economics are not yet strong enough for VERIFIED status.

## 1. Tenzro reality check
Current first-party material is much stronger than Run 029's architecture-only view, but the critical limitation is explicit: the network-role and compute/storage references are still marked **Testnet**.

Confirmed current provider mechanics:
- ModelProvider earns TNZO per settled inference request.
- ComputeProvider rents spare capacity by epoch; the consumer prepays TNZO and the provider earns one epoch slice after a valid availability proof.
- StorageProvider is billed per byte-epoch and earns after retrievability proofs.
- TeeProvider hosts confidential compute/sealed-key workloads; tenants pay for enclave time in TNZO.
- One stake can cover multiple roles.
- Operator material says cloud VM, home server, desktop, SBC or multi-GPU rack can participate depending on role, with self-selected offerings/prices.
- Public GitHub material exposes `tenzro-node`, a `join --provider` path and references a 100 TNZO compute bond for provider registration.

Important downgrade/constraint:
- The role/reference pages explicitly label the system **Testnet**. Therefore TNZO payment mechanics are technically specified but not yet sufficient evidence of dependable production cash flow or liquid realized earnings.

Classification: **WATCHLIST / architecture + testnet implementation verified**.
Automation: 5/5 technically.
Main blockers: production launch, liquid TNZO/off-ramp, actual paid demand, stake value, Azerbaijan onboarding.

## 2. Targon / Manifold Labs reality check
Targon remains a strong confidential-compute supply candidate. Current public materials still expose a **Targon Supply Portal** and explicitly invite users to “access or provide confidential compute.” Documentation covers provider/miner/validator references and confidential GPU/CPU rentals.

What is still not normalized in publicly retrievable first-party material:
- exact open self-serve supplier admission by hardware tier;
- complete provider fee split/payout formula;
- realized utilization by hardware class;
- payout/withdrawal history;
- exact KYC/contract boundary for each supply tier.

Classification remains **VERIFIED provider role / RESTRICTED economics** rather than deployment-ready.

## 3. SecretVM BYOH
Current SecretVM is real and production-facing on the demand side: developers can launch Intel TDX / AMD SEV confidential VMs through the SecretAI portal/CLI.

However the **supplier** path is still future roadmap. Secret Network's 2026 roadmap says Bring Your Own Hardware will be introduced in **Q4 2026**, initially with specific partners, and that revenue sharing for hardware owners will arrive with the BYOH/compute marketplace rollout.

Therefore:
- current SecretVM user/developer service: real;
- current independent hardware-owner income path: **not yet open**;
- expected future mechanism: confidential-compute marketplace revenue share.

Classification: **WATCHLIST (future provider role)**.

## 4. Aleph Cloud CRN/GPU economics
Aleph Cloud remains an established compute-provider mechanism rather than a new category.

Current first-party confirmations:
- Compute Resource Nodes execute VMs/containers and can support confidential computing.
- CRN reward docs still describe token rewards of roughly **250–1500 ALEPH/month** for performant CRNs, depending on location/network decentralization and score.
- GPU CRNs must enable the billing path and compatible GPU configuration.
- GPU pricing is published in Compute Units; standard/premium GPU groups have different per-CU hourly rates.
- Aleph is migrating customer workloads toward **Credits**; instances are credits-only. PAYG is marked deprecated for new workloads, though existing streamed PAYG workloads remain supported and operators should keep reward addresses configured for them.

Economic caution:
Token rewards + customer resource billing must be separated. The legacy incentive range is not proof of net profitability, and current credit settlement to operators needs empirical measurement before deployment.

Classification: **VERIFIED existing compute-provider family; economics require pilot normalization**.

## 5. Akash confidential compute
Akash confidential compute is now a concrete provider capability, not merely roadmap language.

Current first-party provider setup supports:
- AMD SEV-SNP or Intel TDX CPU confidential VMs;
- optional NVIDIA GPU Confidential Computing;
- provider attributes `tee/type=cpu` or `tee/type=cpu-gpu`;
- Kata-based confidential runtimes and attestation sidecars;
- tenant SDL placement on TEE-capable providers.

Important limitation: Akash labels the TEE feature **experimental and under active development**.

This is not a new income mechanism: an Akash provider is still selling compute leases, now with a higher-security capability that may improve differentiated demand/pricing.

Classification: **VERIFIED capability extension of Akash Provider; experimental TEE feature**.

## 6. Material new discovery — Telegram COCOON
This is the main reason the project cannot yet close.

Current first-party COCOON material states:
- COCOON is a decentralized AI inference platform on TON.
- GPU owners earn TON by serving AI models.
- “Anyone with a GPU server can rent it out and earn money” is an explicit design goal.
- Worker and proxy execute inside TEE environments.
- Payments are settled on TON.
- The official TelegramMessenger GitHub repository contains worker tooling, a current worker release path, setup material, and reproducible TEE-image build instructions.
- Official/current architecture describes worker selection, attestation, GPU verification and payment contracts.

Provider fit:
- SERVER-NATIVE: yes, but requires specialized confidential-compute GPU server hardware.
- Automation: 5/5 once the worker is configured.
- Revenue: request-driven TON payments.
- Capital: high; production documentation prominently targets confidential-compute-capable datacenter GPUs rather than cheap VPSs.
- Demand evidence is unusually interesting because Telegram itself is positioned as an anchor customer, but this does **not** establish provider utilization or profitability.
- KYC/geography/Azerbaijan: unresolved; must be tested before CAPEX.
- ToS/cloud re-rental: cloud-host permission must be checked provider by provider.

Classification: **VERIFIED current provider role, high-priority economics follow-up**.

Why this is materially new:
It is not a new mechanism beyond customer-paid confidential GPU inference, but it is a current supplier network missed in prior passes and has enough implementation/payment evidence to count as a material project-level discovery.

## 7. Minor new lead — DICOMPUTE
Discovery search surfaced a public-alpha provider dashboard for DICOMPUTE describing:
- macOS/Windows/Linux provider app;
- optional GPU acceleration;
- automatic model selection and background inference participation;
- public-alpha/pilot status.

Insufficiently established this run:
- concrete reward unit/currency;
- payment history/liquidity;
- pricing/utilization;
- operator admission/geography.

Classification: **WATCHLIST / discovery lead**.

## 8. Alternate-vocabulary search outcome
Queries around attested compute provider, secure GPU supplier, confidential inference provider, TEE marketplace operator, encrypted VM provider, supply portal and BYOH confidential cloud mainly converged back to:
- Targon;
- Tenzro;
- SecretVM;
- Akash;
- io.net confidential inference as an existing supplier-market capability extension;
- COCOON as the material new cluster;
- small early-stage leads such as DICOMPUTE.

No new economic family appeared.

## Durable conclusions after Run 030
1. **Confidential GPU inference is now a distinct provider-discovery vocabulary cluster but not a new economic mechanism**: economically it is still customer-paid compute/inference.
2. COCOON is a material omission from prior provider-level mapping and requires its own economics/admission normalization.
3. Tenzro is technically much more concrete than a whitepaper, but the explicit Testnet status prevents production-income classification.
4. SecretVM BYOH remains future Q4 2026 roadmap, so do not count projected revenue share as present income.
5. Akash TEE is real current provider functionality but experimental.
6. Aleph current billing migration means legacy PAYG/token-reward assumptions must not be treated as stable provider revenue without measuring actual operator receipts.
7. Specialized TEE hardware materially raises CAPEX and makes cloud re-rental/financing assumptions important.

## Saturation consequence
Taxonomy saturation remains **very high**: Run 030 again found **0 new top-level economic mechanisms**.
Project/provider saturation remains **high but not complete** due to COCOON and the DICOMPUTE lead.

## Next run
**Run 031 — COCOON provider economics + confidential-inference tail sweep.**

Priority checks:
1. COCOON official worker requirements, admission, payout formula, TON settlement details, live demand/utilization signals and provider onboarding.
2. COCOON supported GPUs / TEE CPU requirements / networking / expected uptime.
3. Determine whether provider participation is open self-serve or application-curated.
4. Test Azerbaijan/KYC/off-ramp dependencies where evidence exists.
5. Validate DICOMPUTE rewards/payment reality or reject/watchlist it.
6. Sweep 0G Compute confidential inference, io.net confidential inference and similar networks specifically for independent supply-side admission.
7. Search current GitHub releases and provider docs for `worker`, `miner`, `supplier`, `GPU owner`, `TEE provider`, `confidential inference`, `attested inference`.
8. If Run 031 adds no material provider cluster after these checks, perform the final all-category control pass before considering COMPLETE.
