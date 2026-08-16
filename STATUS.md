# Status

Project state: **IN PROGRESS**

Last completed run: **Run 039 — supplier-proof + newly discovered neighbor pass**
Last updated: **2026-08-16**

## Completed research runs
Runs **001–039** are complete.

Latest durable files:
- `research/RUN_039_SUPPLIER_PROOF_NEIGHBOR_PASS.md`
- `research/SOURCES_RUN_039.md`
- `research/CATALOG_ADDITIONS_RUN_039.md`

## Saturation state
Twenty-two deliberate control/tail passes (Runs 018–039) have produced **0 new top-level economic mechanisms**. Taxonomy saturation confidence is **very high**.

Project-level saturation is still **not complete**. Run 039 found at least three fresh independent provider implementations absent from the durable Run-038 checkpoint: **Keld**, **hosted.ai GPU Mesh**, and **Fluxenta**. Two are current commercial supplier paths; Fluxenta is explicitly pre-production. Provider-tail discovery therefore remains productive enough that the final all-category completion pass must again be postponed.

## Material Run 039 findings

### Keld — NEW, material candidate
- Live enterprise AI-inference marketplace with independent model providers.
- Provider-side product `Keld Trade` lists spare capacity/manages orders; micro-batching is designed to fill idle fleet headroom with matched jobs.
- Market sells inference/model output rather than raw GPU-hours.
- Current launch material says the exchange is live and matches across 100+ providers, but public provider names, settlement mechanics, fees, KYC/geography and Azerbaijan eligibility remain unresolved.
- Classification: `VERIFIED / RESTRICTED`.

### hosted.ai GPU Mesh — NEW, material professional supplier/resale path
- GPU owners can publish GPU pools and get paid for Mesh consumption while retaining direct sales.
- Operators can also buy wholesale GPU pools and resell them under their own neocloud brand, including a zero-hardware-CAPEX path.
- Platform provides metering/billing/orchestration and multi-tenant GPU controls.
- Commercial fee/payout terms, supplier minimums, geography/entity requirements and Azerbaijan feasibility remain unresolved.
- Classification: `VERIFIED / RESTRICTED`.

### Fluxenta — NEW, pre-production
- Agent-first inference marketplace intends to let providers sell idle GPU/CPU capacity through secure tunnel, headless APIs and token settlement.
- Official site explicitly says coming soon / provider onboarding starts later.
- Classification: `WATCHLIST / PRE-PRODUCTION`.

### Lilac
- 70% supplier share and monthly wire/ACH payout remain strongly verified.
- No public proof found for supported supplier countries, Azerbaijan eligibility, entity/KYC package, public minimum commercial cluster scale or utilization distribution.
- Keep `VERIFIED / RESTRICTED`.

### ResonTech
- Supplier path now has clearer professional-cluster requirements: intended operators are 8+ GPU clusters; Slurm/K8s/bare-metal and automatic job routing are explicit.
- Public commercial settlement terms remain missing.
- Keep `WATCHLIST / RESTRICTED`.

### the402
- Public catalog/reputation surface strengthens production evidence: provider completed-job counts and completion-rate fields exist; public catalog shows 100+ listings.
- Listing count is not equivalent to paid demand/revenue.
- Current official fee wording remains inconsistent between provider docs and marketing page; verify live settlement before economic modeling.

## Durable economics findings
- **Paid utilization/fill rate remains the dominant hidden variable.**
- Existing idle-capacity economics and new hardware CAPEX economics must be modeled separately.
- A professional provider market can be operationally autonomous but inaccessible without business onboarding, cluster scale or geographic eligibility.
- Wholesale capacity resale is a distinct implementation strategy but not passive profit by itself; customer acquisition/support/compliance still matter.
- A marketplace listing count proves supply surface, not independent demand.
- Enabling software (Waldur, Cedana-style optimizers, payment rails) must not be double-counted as stand-alone earning networks.
- Azerbaijan remains a hard pre-CAPEX validation gate.

## Current phase
Taxonomy is effectively converged, but provider-tail discovery is still producing independent implementations. Completion remains premature.

Completion confidence:
- taxonomy: **very high**
- high-priority economics: **medium-high**
- project-level saturation: **high, not complete**
- overall completion: **not yet**

## Next run priority
**Run 040 — second supplier-tail convergence pass.**

Priority:
1. Keld: provider onboarding, settlement/payout, fees, KYC/entity/geography, Azerbaijan feasibility, public supplier names and fill/demand evidence.
2. hosted.ai GPU Mesh: supplier commercial terms, fees, payout rails, minimum infrastructure/business requirements, geography and Azerbaijan feasibility.
3. Fluxenta: production-launch check only; retain pre-production unless live provider onboarding and settlement appear.
4. Search exact neighbors using new vocabulary: inference exchange, model-provider exchange, GPU mesh, wholesale GPU resale, capacity clearing, token-level inference market, micro-batched provider fleet, sovereign GPU supplier, idle-capacity sales channel.
5. Re-run non-GPU analogs of the same pattern: CPU/HPC/storage/bandwidth/API capacity exchanges and reseller networks.
6. Re-check Keld/hosted.ai neighbors against master catalog/addition files to avoid duplicate names.

### Completion logic
If Run 040 finds **no new material independent provider project** (or only dead/test-only/specification/duplicate/enabler/pre-production projects), proceed to **Run 041 — final all-category saturation/control pass**. Only if that broad pass also converges should the project be marked COMPLETE.

## Completion gate
Do **not** mark complete until repeated broad + niche + alternative-vocabulary + role-name/repository + non-GPU/provider-operator + proof/RPC/indexing + proof-market/data-operator + TEE/verifier-node + confidential-supplier/open-provider + confidential-inference-worker + contributor/native/browser-worker + x402/agent-compute + cloud-backed-provider + autonomous-webhook-service + decentralized-hosting + professional-idle-GPU/HPC-supplier + inference-exchange/GPU-mesh/wholesale-resale + final all-category control passes add no new independent mechanism and almost no new viable projects, with remaining unknowns explicitly recorded rather than guessed.
