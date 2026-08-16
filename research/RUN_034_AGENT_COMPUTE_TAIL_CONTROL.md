# Run 034 — Agent-compute / machine-job tail control

Date: 2026-08-16
Status: **completed**
Project state after run: **IN PROGRESS**

## Objective
Run a dedicated tail-control pass over the exact vocabulary that still produced Dispatch in Run 033: x402 compute workers, agent-compute marketplaces, idle-device inference workers, OpenAI-compatible contributor nodes, phone compute, verified inference receipts, ERC-8004 job markets, and Solana/Base/Monad machine-job networks. Also test machine-readable task markets where autonomous execution is explicitly part of the product rather than a violation of a human-microtask ToS.

## Result
The pass **did produce additional material current projects**, so the completion gate is not met. No new top-level economic mechanism appeared, but the provider/project tail is still non-empty.

Most important discovery: **Singularity Compute / SGL Grid** appears to be a live mainnet confidential-inference provider network with an explicit server/Mac node-operator path, 50,000 SGL collateral, and per-settled-job rewards in USDC + SGL. This is materially stronger current-income evidence than the testnet/devnet projects found in Runs 032–033 and is a direct match for the original “server bot earns from simple machine work” target.

The same pass also found several earlier-stage implementations that should remain in the watchlist: **Fusio, CloudAGI, Tenzro, MyAi, A2Agora** and **CLAWORK**. These do not justify completion because they show that the 2026 agent-compute/x402/ERC-8004 ecosystem is still generating fresh supplier/job-market implementations.

## Material findings

### 1. Singularity Compute / SGL Grid — VERIFIED candidate, production-economics validation still required
Category: confidential AI inference / TEE compute provider
Classification: SERVER-NATIVE with hardware-attestation constraint
Automation: 5/5 once configured

Official current site states:
- Grid is operational on mainnet and settles on Solana/Base.
- A Mac or server can be turned into a compute node.
- Node operators serve models and earn **USDC + SGL per settled job**.
- Minimum operator/validator stake shown: **50,000 SGL**, recoverable after cooldown.
- Workloads are TEE-attested; tampering is slashable, downtime is stated as non-slashable.
- Client side pays per token in USDC; settlement is on-chain.
- Site advertises a single-command node path and OpenAI-compatible inference surface.

Why it matters:
This is the strongest new Run-034 match for fully autonomous online earning. It is not merely uptime points or a future roadmap token: current public material claims mainnet job settlement and an explicit operator earning path.

Unknowns before any deployment:
- exact supported TEE hardware matrix for a self-supplied node;
- whether ordinary VPS instances can satisfy attestation or only specific TEE-capable bare metal/cloud SKUs;
- current SGL market depth/value and effective fiat collateral cost;
- observable paid utilization per node;
- node reward split in production and withdrawal friction;
- operator Terms/AUP, KYC and Azerbaijan eligibility;
- whether the current public node installer is permissionless in practice or has hidden admission gates.

Economics formula:
`Net = settled USDC + realizable SGL rewards - SGL capital/opportunity cost - compatible TEE server/GPU cost - power/bandwidth - transaction/withdrawal fees - depreciation - maintenance - expected slashing/security loss`

Do not estimate profitability until utilization and collateral liquidity are measured.

### 2. Fusio — WATCHLIST / testnet core loop
Category: autonomous-agent machine-job marketplace
Automation: 5/5 conceptually

Official site describes requester → worker jobs with signed manifests, routing, escrow settlement and signed receipts. Workers earn FSO and providers stake FSO to list capabilities. Node software is described for Windows/macOS/Linux.

However the project explicitly labels the current phase as **Phase 1 / core loop**, with FSO on testnet; mainnet token and the first third-party jobs belong to Phase 2. Therefore this is not present production income.

Useful durable signal: the paid unit is a completed agent job, not raw GPU uptime. This remains the same known mechanism as Dispatch but a separate current implementation.

### 3. CloudAGI — WATCHLIST / marketplace waitlist + Solana devnet
Category: sell local-model / agent capacity per API call
Automation: 5/5 after provider endpoint setup

Current official page says sellers can connect a local Ollama endpoint or specialized agent, set a USDC-per-million-token price, and receive per-call x402 settlement. The live build status references Solana devnet and the public marketplace is still waitlist/early access.

Important caution: the site also discusses listing unused subscription/credit pools. Provider use of third-party subscription capacity must be checked against the upstream provider's resale/automation Terms before considering such a strategy. Self-hosted local-model capacity is the cleanest compliant branch.

### 4. Tenzro — WATCHLIST / substantial live testnet implementation
Category: multi-role AI inference + compute rental + storage + validator
Automation: 5/5 node daemon

Current official docs label the public network **Testnet**. Network roles include ModelProvider, ComputeProvider, StorageProvider and TeeProvider under one stake. Docs say ModelProviders earn TNZO per inference, while the repository documents direct provider setup, a 100-TNZO compute bond, automatic hardware profiling/model serving and per-call TNZO settlement.

This is technically a strong fit but not current cash income while the network and token economics remain testnet/faucet based. Keep as a future pilot candidate rather than treating faucet/testnet TNZO as income.

### 5. MyAi — WATCHLIST / pre-TGE network; do not treat token estimates as realized profit
Category: GPU/CPU inference contributor network
Automation: 5/5 provider daemon

Official site/docs claim:
- Linux/macOS/Windows provider agent polling jobs continuously;
- explicit **datacenter / Linux cloud instance** provider tier;
- Base-based MYAI settlement design;
- provider rewards calculated per completed inference job and model size;
- a 10,000 MYAI stake requirement is advertised on the main page;
- current state is **Pre-TGE / genesis window**, with 1:1 testnet→mainnet language;
- marketplace snapshot showed 0 online providers in the indexed public view, while the main page separately advertised a very small live network.

The project publishes estimated MYAI/day bands, but those are emission-based estimates, not proof of liquid realized profit. Public community material still says liquidity lock/TGE pending. Therefore keep as WATCHLIST until token liquidity, mainnet payout transferability, stake acquisition cost, actual jobs and independent on-chain settlement can be verified.

### 6. A2Agora / ACMP — ADJACENT WATCHLIST, protocol not current earning marketplace
Category: open agent-compute market protocol

A2Agora defines negotiation, pricing, proof, escrow/settlement abstractions and provider invocation, but official material labels it a **pre-v0 open specification**. The reference SDK is explicitly a proof of implementability and uses an in-memory transport and escrow stub; full production settlement is not implemented there.

Record it as an important protocol/discovery surface for future providers, not as a current revenue source.

### 7. CLAWORK — WATCHLIST / autonomous agent-service job market
Category: machine-readable freelance/task market for AI agents and humans
Automation: potentially 4–5/5 depending on job type

Current site describes a Base marketplace where AI agents and humans take work and settle in USDC via x402, with ERC-8004 identity/reputation. The jobs page is wallet-gated and the public front page shows very low visible completion counts for example agents.

This is economically distinct from raw compute rental: revenue comes from delivering a task outcome (research, engineering, writing, analysis, etc.). It fits the project's “machine-readable task/API job market” branch only where the job itself permits autonomous agent execution. Do not automate work advertised as human-only or misrepresent agent identity.

## Adjacent / non-income findings

### A2Agora
Useful market standard and future supplier discovery layer, but not a production marketplace today.

### x402 itself
x402 is a payment rail, not an earning mechanism. A provider only earns when a real customer purchases a resource or outcome. Transaction count alone should never be treated as demand evidence.

A July 2026 population-scale study of x402 activity found extreme concentration and substantial internally linked/fictitious settlement patterns. Treat this as a warning that raw x402 settlement count can badly overstate independent customer demand. For any x402-based candidate, measure unique external buyers, paid value and repeat independent demand rather than transaction count.

## Dispatch follow-up
Run 034 re-confirmed Dispatch remains testnet/devnet in its current public docs: Monad testnet + Solana devnet, with BOLT/wBOLT rewards and 5% protocol fee. The public worker path is desktop/mobile oriented. This run still did not establish generic rented-VPS/datacenter permission or production mainnet cash payout. Keep WATCHLIST.

## Taxonomy conclusion
New top-level economic mechanisms in Run 034: **0**.

New material implementations/leads: **7**, of which one (Singularity Compute) is currently much stronger on live-mainnet earning evidence than the rest.

The tail remains productive. The project must therefore remain **IN PROGRESS**.

## Next run
**Run 035 — normalize new Run-034 projects + exact-neighbor discovery.**

Priority:
1. Singularity Compute operator docs/Terms/AUP, exact TEE hardware eligibility, permissionless admission, stake liquidity/value, reward split, utilization telemetry, KYC and geography.
2. Search exact neighbors of Singularity Grid, MyAi, Fusio, CloudAGI, Tenzro and CLAWORK.
3. Search `confidential inference node earn`, `TEE inference provider marketplace`, `x402 TEE compute provider`, `ERC-8004 paid agent jobs`, `agent job board USDC`, `AI agent task marketplace x402`, `OpenAI compatible provider earn USDC`, and `compute provider USDC per call`.
4. Separate production-mainnet, pre-TGE, testnet/devnet, waitlist and specification-only projects.
5. If this normalization/tail pass yields no further material implementation, proceed to the final all-category saturation pass described in STATUS.

## Run-log note
`RUN_LOG.md` was intentionally not replaced in this run because the connector returned only a truncated view of the large file; replacing it without the full current text risks deleting prior history. This run file is the durable journal entry and STATUS/HANDOFF are advanced safely.
