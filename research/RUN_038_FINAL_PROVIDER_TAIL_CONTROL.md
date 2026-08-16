# Run 038 — Final exact-neighbor/provider-tail control

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Objective
Perform the planned final provider-tail control around autonomous inference suppliers, compute lenders, machine-service sellers, webhook/API providers, decentralized app hosting and low-friction server-native earning paths; re-check Atlara, Evernode, the402 and Aeterna; determine whether project-level discovery has converged enough to proceed to the final all-category saturation pass.

## Result
The completion gate was **not** met. This pass found at least two material independent supplier implementations that were not present in the repository search corpus: **Lilac** and **ResonTech**. They do not create a new top-level economic mechanism, but they are distinct live/provider-oriented implementations of paid compute supply and therefore show that provider-level saturation is not yet complete.

Taxonomy remains effectively saturated: this run again added **0 new top-level mechanisms**.

---

## 1. Lilac — NEW, material supplier candidate

### What it is
Lilac operates an idle-GPU network for AI inference and batch workloads. Capacity providers install a Kubernetes operator; Lilac detects reclaimable GPU capacity, schedules paid workloads, meters usage and preempts them when the supplier's primary jobs need the GPUs.

### Evidence current to 2026-08-16
Official supplier documentation explicitly states:
- supplier share: **70%** of revenue;
- Lilac share: 30%;
- supplier payout formula is token-based: `tokens_processed × model token price × 0.70`;
- payouts are **monthly**;
- payout rails documented: **wire transfer or ACH**;
- supplier reports include tokens processed, per-cluster earnings, gross revenue and payout;
- revenue depends on GPU availability, routed inference demand and model pricing.

The public provider page says supplier onboarding is still through demo/waitlist and targets existing GPU/Kubernetes clusters rather than a casual single-VPS user. Lilac's public product pages in 2026 show live inference products and current model pricing, which is stronger production evidence than points-only/devnet networks.

### Classification
- Category: paid GPU compute / inference marketplace
- Type: SERVER/BUSINESS-NATIVE, professional GPU cluster
- Status: **VERIFIED / RESTRICTED**
- Automation: 5/5 after onboarding
- Resource: GPU cluster + Kubernetes + bandwidth/uptime
- Ordinary cheap VPS: no practical fit
- Bare metal / existing GPU cluster: yes
- Payout: fiat bank rails documented
- KYC/business onboarding: likely part of supplier onboarding but exact public requirements not fully documented
- Azerbaijan availability: **unknown — mandatory pre-CAPEX check**
- Revenue evidence: commercially structured and usage-based; actual supplier utilization distribution not public

### Economics
Supplier gross payout per model can be approximated as:

`Supplier revenue = billable tokens × Lilac model price × 70%`

Net:

`Net = supplier payout - incremental electricity - cooling - bandwidth - operator overhead - hardware depreciation attributable to Lilac workloads - tax/bank fees`

For hardware already sunk into another workload, marginal economics can be attractive because Lilac targets otherwise-idle capacity. Buying GPUs solely to supply Lilac is a different risk profile and should not be modeled from the 70% share alone; utilization is the dominant unknown.

### Why material
This is a direct implementation of the user's target: software on already-owned/server GPU infrastructure automatically accepts useful paid jobs and earns with little human action. Unlike many token networks, official documentation defines fiat payout mechanics and a revenue split.

### Next validation
- supplier geography / entity requirements;
- Azerbaijan onboarding feasibility;
- minimum cluster scale and accepted GPU list;
- sample supplier utilization / payout data;
- whether a rented third-party GPU cluster may be re-supplied without violating upstream provider terms.

---

## 2. ResonTech supplier network — NEW, material but less economically verified

### What it is
ResonTech describes a multi-cluster fabric for HPC/cloud/on-prem compute with a supplier program. Operators with idle professional clusters register specs/location/scheduler/availability, install a node agent, and matched jobs/inference replicas are routed to their hardware automatically.

Official site says it is explicitly **not a consumer-GPU marketplace** and targets professional clusters, describing 8+ GPUs / fast intra-cluster networking as the intended supplier profile. It supports Slurm, Kubernetes and bare-metal-style environments and exposes job history/utilization to operators.

### Classification
- Category: professional cluster compute marketplace / training + inference
- Type: SERVER/BUSINESS-NATIVE
- Status: **WATCHLIST / RESTRICTED**
- Automation: 5/5 technically after onboarding
- Resource: professional GPU/HPC cluster
- Cheap VPS: no
- Payout currency/settlement: not established in currently accessible public material
- KYC/contracts/geography: not established publicly
- Azerbaijan availability: unknown
- Real demand: site claims real jobs route automatically, but independently measurable utilization/payout evidence is insufficient in this run

### Why material
Independent supplier implementation not found in prior repository searches. It is highly aligned with autonomous compute monetization, but financial proof is weaker than Lilac.

### Next validation
Find supplier commercial terms, payout mechanism, fee/revenue share, current customer workload evidence, supported countries and onboarding requirements. Downgrade if those remain non-public/marketing-only after the next proof pass.

---

## 3. Atlara — useful technical confirmation, cash ambiguity remains

Current official material continues to establish a real technical provider path:
- Linux installation is public;
- node automatically detects hardware, downloads a model and serves inference;
- network mode links the node to an Atlara account;
- public/private node routing is documented;
- provider marketing says devices can earn from contributed compute.

However, the strongest concrete reward page says contributed compute earns **Atlara credits redeemable for AI API calls**. It does not establish ordinary provider cash/crypto withdrawal. Marketing language uses terms such as income/earnings, but until withdrawal or a transferable asset is documented, ordinary provider earnings must not be counted as cash income.

Classification remains: **WATCHLIST / RESTRICTED / EARLY ACCESS**.

New durable rule reinforced: a displayed USD-equivalent credit balance is not cash revenue unless redemption/withdrawal into money is explicitly available.

---

## 4. Evernode — no decisive economics breakthrough

Official docs still establish the important host-reward constraints:
- reputation >= 200 for reward eligibility;
- unoffered leases can reset reputation;
- host capacity below 3 instances can reset reputation;
- lease fee above 110% of the reward-per-host reference can reset reputation;
- sanctioned-entity restrictions apply to new-host installation.

The canonical current eligible-host denominator and paid tenant utilization were not established strongly enough in this run to improve the reward-only break-even estimate. Keep the earlier caution: token reward value without tenant utilization is not sufficient evidence of VPS profitability.

Classification remains unchanged.

---

## 5. the402 — strongest low-capital machine-service pattern remains valid

Current official documentation confirms:
- an AI agent may itself be a provider;
- providers can expose automated services through a webhook;
- request-created webhooks allow real-time autonomous bidding;
- automated services can auto-verify on completion;
- USDC escrow/settlement and provider earnings endpoints are documented;
- bid caps depend on verification tier;
- service listings can include data APIs, automated services, products and subscriptions.

This remains one of the closest matches to the target when starting without expensive hardware: deploy a deterministic useful service/API, allow agents to discover/buy it, fulfill by webhook, and receive machine-native payment.

### Important fee wording correction
Official current pages use two descriptions: provider docs mention a 5% platform fee in the flow, while the public provider page says the listed provider price is received by the provider and 5% is added to the buyer. Treat economics conservatively until the exact current fee implementation is verified from settlement/account data; do not assume either wording blindly.

### Demand caveat
The broader x402 ecosystem remains subject to the July-2026 measurement warning: transaction count does not equal independent commercial demand. Evaluate the402 with completed independent jobs/provider earnings, not ecosystem transaction headlines.

---

## 6. Aeterna — downgrade from candidate production path

Current official/public pages describe Aeterna inference, subnets, miners/validators, x402 and an autonomous service economy, but the project's own roadmap places key AI-inference mainnet/subnet marketplace/x402 features in upcoming phases rather than proving a mature currently open supplier market. Accessible material did not produce a public provider daemon with completed paid-job history or withdrawal proof.

Classification after this pass: **WATCHLIST / PRE-PRODUCTION; do not count as currently deployable income**.

If another future proof pass still finds no production supplier onboarding or payout history, move to REJECTED-FOR-CURRENT-DEPLOYMENT while retaining it as a future watchlist project.

---

## 7. Additional exact-neighbor discoveries / classifications

### x402 direct API monetization
The x402 standard itself supports selling paid HTTP endpoints without requiring a centralized marketplace. This is not a new top-level mechanism; it reinforces the BUILD-ONCE / autonomous API-service pattern already in the taxonomy. Seller success still requires actual discovery/distribution and useful output.

### GOAT x402 merchant infrastructure
Current GOAT documentation provides production merchant configuration and machine-payment infrastructure. It is a payment-enablement implementation, not evidence that the platform supplies buyer demand. Catalog as enabling infrastructure, not a stand-alone passive-income source.

### AgentPay / PayAI and similar facilitators
These enable paid API/agent endpoints and merchant settlement. They are relevant deployment rails but should not be double-counted as separate economic mechanisms. The value source is still customers purchasing the provider's service/API.

### Masa AI Worker Nodes
Discovery returned Masa worker-node material describing data/LLM work plus rewards. This mechanism and project family are already represented in decentralized AI/data worker-node research; no new top-level mechanism was found in this pass.

### NodeOps Inference Devnet
Current documentation explicitly describes devnet/test rewards/points and rented GPU deployment. Do not treat points/devnet incentives as proven cash profitability. Adjacent/watching only unless mainnet paid utilization is established.

---

## 8. Saturation assessment after Run 038

### New top-level mechanisms
**0**

### New material independent provider projects
**2+**
- Lilac — strong, commercially specified supplier route
- ResonTech supplier network — technically aligned, economics need proof

### Interpretation
Taxonomy saturation is effectively achieved, but project-level/provider-level saturation is **not yet achieved** because an intentionally narrow neighbor search still produced new live supplier implementations.

Therefore the planned Run 039 final all-category completion pass must be postponed. First perform another provider proof/tail pass focused on the newly found projects and their close neighbors. If that pass produces no further material providers, then run the final broad all-category saturation control.

## Next run
**Run 039 — supplier-proof + newly discovered neighbor pass**

Priorities:
1. Lilac supplier geography/KYC/entity requirements, minimum cluster size, supported hardware, utilization evidence and Azerbaijan feasibility.
2. ResonTech supplier commercial terms, payout/fee structure, onboarding, geography and real demand.
3. Search close neighbors of the concepts revealed here: Kubernetes idle-GPU operator, enterprise GPU reclaim marketplace, HPC spare-capacity supplier, Slurm capacity seller, reserved-cloud-capacity resale, inference revenue-share operator.
4. the402 public catalog/provider statistics or completed-job evidence if exposed without private credentials.
5. Atlara terms and cash-withdrawal proof; if still credit-only, classify explicitly as non-cash for current objective.
6. Aeterna final production proof only if new evidence appears; otherwise retain pre-production classification.

Only after a no-new-material-provider result should the next run become the final all-category saturation/control pass.
