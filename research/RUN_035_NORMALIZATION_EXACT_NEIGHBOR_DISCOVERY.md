# Run 035 — Normalize Run-034 projects + exact-neighbor discovery

Date: 2026-08-16
Status: **completed**
Project state after run: **IN PROGRESS**

## Goal
Deep-validate Singularity Compute and search exact neighbors around confidential inference, TEE providers, x402/agent-service markets, OpenAI-compatible paid providers, and the Run-034 discovery-only queue.

## Result
The taxonomy remains saturated: **0 new top-level economic mechanisms**.

However, project/provider saturation is **not yet complete**. This run found multiple fresh independent implementations. Two are especially material for the project goal:

1. **Open Cloud provider marketplace** — a current centralized marketplace explicitly allowing both dedicated hardware and cloud-backed templates, with KYC/operational onboarding and monthly USD settlement.
2. **the402 provider marketplace** — a current machine-permitted job/API market where an autonomous server webhook can list Data APIs or Automated Services and receive USDC after automated delivery.

Additional current/early candidates include **x402.jobs**, **Cocoon**, and **ALPENGLOW**. Because new viable-looking projects still appeared, the completion gate remains open.

---

## 1. Singularity Compute / SGL Grid — strengthened, but economics still unproven

Classification: `VERIFIED / RESTRICTED` for technical earning path; **not yet deployment-approved**.

### What is now strongly supported
- Main site describes an operational mainnet confidential-compute grid with Solana/Base settlement.
- A node can be a Mac or server and is explicitly described as earning from routed jobs.
- Operator/validator collateral: **50,000 SGL**.
- Rewards: **USDC + SGL per settled job**.
- Operator stake is described as recoverable after cooldown.
- Grid workloads use attestation / allow-listed binaries; tampering is slashable.
- AI Machines documentation exposes a managed mode: deploy a GPU machine, select **Join the grid & earn**, stake 50,000 SGL, then the machine serves grid traffic automatically.
- The managed compute layer currently provisions through Vultr and DigitalOcean in documented releases.
- Staking interface says stakers receive **10% of compute revenue** and that rewards depend on network compute activity.

### Important contradiction / caution
The compute marketing page says stake tied to operators is slashable for tampering and says not for going offline, while the staking risk disclosure says compute/validator stake can be slashed for misbehavior **or downtime** according to program rules. Treat downtime slashing as unresolved until contract/program rules are inspected directly.

### Geography / KYC
- Public legal pages do not provide an Azerbaijan-specific allow/deny statement.
- Staking eligibility excludes sanctioned persons/jurisdictions and any jurisdiction where the activity would be illegal or require unavailable licensing.
- No universal mandatory identity-KYC flow was established from the public operator pages; wallet information is collected by the platform. This is **not** proof that all operator paths are KYC-free.

### Economics
Still insufficient to call profitable.

Net formula:
`operator USDC + realized SGL - machine rent - stake opportunity cost - token price/liquidity risk - chain/withdrawal fees - expected slashing/security loss - maintenance`

Critical unknowns:
- real paid grid utilization;
- operator share of each job vs staker/treasury/other shares;
- current SGL market depth and effective cost of 50k SGL;
- cooldown duration and exact slashing program rules;
- whether a managed rented AI Machine can earn more than its prepaid rental cost under observed demand;
- whether arbitrary external VPS/bare-metal operators can currently onboard without hidden approval.

Current classification: **high-priority RESTRICTED candidate**.

---

## 2. Open Cloud — NEW strong server-native provider candidate

Classification: `VERIFIED / CURATED SERVER-NATIVE`.

Official provider page explicitly says operators can:
- list dedicated hardware; or
- offer **cloud instances as-a-service** using on-demand provisioning against AWS, GCP or Azure accounts.

Provider onboarding:
- KYC and operational checks;
- legal entity, insurance, data-center agreements and operations runbooks reviewed;
- stated typical onboarding: 2–3 weeks.

Settlement:
- customers select/bond provider nodes;
- providers are paid in cycles;
- settlement is **USD monthly**;
- provider page says no Open Cloud markup.

### Why this matters
This is a cleaner version of the user’s desired model than many DePIN token networks: an approved operator can automate provisioning of ordinary cloud capacity and receive fiat-denominated settlement. It is not permissionless and may require a real business/legal entity, but cloud-backed supply is explicitly supported rather than inferred from Linux compatibility.

### Automation
Potential **4–5/5** after onboarding because inventory/templates can provision cloud instances on demand.

### Economics
`Net = monthly USD settlement - upstream AWS/GCP/Azure/dedicated-host cost - insurance/business overhead - bandwidth/egress - support/ops - taxes`

Main unknowns:
- customer demand/utilization by region and SKU;
- payout cycle/unit definition;
- minimum inventory/insurance requirements;
- Azerbaijan legal-entity eligibility;
- SLA/support burden and chargebacks/penalties.

This candidate deserves a dedicated economics/admission pass before CAPEX.

---

## 3. the402 — NEW strong autonomous machine-job/API market

Classification: `VERIFIED / BUILD-ONCE + SERVER-NATIVE SERVICE`.

Official docs are unusually explicit that **AI agents may be providers** and that automated services can run with no humans in the loop.

Provider flow:
1. register provider;
2. list a Data API or Automated Service;
3. point platform to a webhook URL;
4. server receives job payload;
5. webhook performs the work and posts deliverable;
6. automated service auto-verifies on completion;
7. provider receives USDC.

Economics and settlement:
- Base L2 / USDC;
- platform fee model documented as 5%; public provider page says provider sets desired amount and buyer pays fee on top, while some docs phrase release as minus fee. Treat exact quote/display convention as a billing-detail check, not a mechanism uncertainty.
- automated service range in docs: roughly $0.50–$10; Data API tier roughly $0.001–$1.
- self-registration via x402 is available for a tiny one-time payment.
- provider can also register a bidding agent to monitor open requests and bid autonomously.
- subscriptions and digital products add recurring/build-once income paths.

Compliance:
- Terms explicitly allow automated agent execution.
- illegal/fraudulent/harmful services, sanctions evasion, fee circumvention, reputation manipulation and identity misrepresentation are prohibited.
- optional identity verification exists for a badge; US bank cash-out through Coinbase requires Coinbase KYC, but direct self-custody USDC receipt is a separate path.

### Why this matters
This is one of the closest current matches to “a server bot doing simple online tasks for money” without pretending to be human. The right implementation is a narrow deterministic/AI-assisted service with bounded input/output and low variable API cost.

Candidate service families for later implementation research (not building now):
- DNS/SSL/domain checks;
- structured website metadata extraction where permitted;
- document transforms;
- image/file conversion;
- code/static checks;
- public-data enrichment with lawful sources;
- model/API inference wrappers where upstream resale terms permit it;
- scheduled monitoring reports;
- agent-to-agent transformation workflows.

Net formula:
`Net/job = provider receipt - model/API cost - server cost allocation - paid third-party data cost - chain/off-ramp fees - expected dispute/failure cost`

Main unknown: **real independent paid demand**. Platform existence and permission do not prove enough jobs to cover costs.

---

## 4. x402.jobs — NEW build-once autonomous workflow endpoint candidate

Classification: `VERIFIED SURFACE / ECONOMICS NEED VALIDATION`.

Current site describes:
- visual composition of existing x402 resources into workflows/jobs;
- creator-set markup;
- one-click publication as an endpoint;
- earnings on each run;
- scheduled or webhook triggers;
- public claims of current network volume/jobs/resources.

Economic mechanism: **service orchestration markup**, not raw compute mining. A builder composes paid resources and charges a higher bundled price; margin is earned per invocation.

Automation potential: **5/5** after publishing.

Main risks/unknowns:
- platform claims need independent/on-chain validation;
- upstream resource reliability and price changes;
- actual external buyer concentration;
- security of x402 payment/facilitator stack;
- margin can be erased by component calls or failed workflows.

Keep as a high-priority BUILD-ONCE candidate for later demand/economics validation.

---

## 5. Cocoon — NEW confidential-inference GPU-provider watchlist

Classification: `WATCHLIST / CONFIDENTIAL GPU PROVIDER`.

Current official site describes a decentralized confidential inference network where:
- developers submit inference requests;
- dispatcher assigns jobs to secure nodes;
- attested GPU nodes execute inside confidential environments;
- GPU owners/providers earn **TON** for processed requests;
- prospective GPU providers can apply.

This is economically distinct as an implementation but not a new mechanism: paid confidential inference on attested GPUs.

Unknowns preventing stronger status:
- precise eligible hardware;
- provider admission and KYC/geography;
- current mainnet utilization and actual payout history;
- price/rate formula and minimum payout;
- ordinary rented-server/cloud permission;
- operator software and SLA.

---

## 6. ALPENGLOW — NEW early GPU passive-inference watchlist

Classification: `WATCHLIST / HIGH CLAIM-RISK`.

Current project site claims:
- Windows/Mac/Linux background node;
- idle GPU paid per inference-second;
- USDC x402 fee settlement at protocol level;
- 70% of inference fee routed to GPU provider;
- TEE on enterprise hardware, optimistic/ZK checks for retail GPUs.

This would be an excellent match if production demand and settlement are real, but the current evidence is mainly the project’s own marketing page. No independent current utilization/payment proof was established in this run.

Do **not** model advertised token emissions as realized income. Require contract, node binary/repository, actual paid jobs, provider receipts, token liquidity, terms and geography validation before promotion above WATCHLIST.

---

## 7. OpenGradient supplier side — architecture real, public earning path still incomplete

Classification: `WATCHLIST / PROVIDER ADMISSION UNRESOLVED`.

Official docs now clearly document specialized **Inference Nodes**:
- Local Inference Nodes supply GPUs and run models;
- LLM Proxy Nodes run in TEEs and provide secure access to third-party LLM APIs;
- full nodes manage registration and payment settlement;
- x402 LLM inference settles on Base.

This proves a genuine supply-side architecture. However, this run did not find a current self-service operator onboarding path, reward schedule, payout unit, collateral requirement or public provider economics. The public network remains described as testnet in the main site.

Conclusion: stronger technical evidence than before, still not a deployable income candidate.

---

## 8. AgentX Nexus Grid — remain UNVERIFIED/WATCHLIST

Official site names **AgentX Nexus Grid — Decentralized Compute Network**, but current public material found in this run did not establish:
- how an external provider joins;
- what resource is paid for;
- liquid payout currency/rate;
- mainnet job utilization;
- VPS/cloud eligibility.

Do not upgrade from discovery-only branding.

---

## 9. Everagents — not a current provider-income path

Classification: `ADJACENT WATCHLIST`.

Everagents currently demonstrates autonomous agents deployed on Evernode testnet. The site says the commission loop is still being built and mainnet/real-value operations are next. It describes a future internal market where agents can sell cognition, but this is roadmap rather than current production provider revenue.

Important distinction: Everagents is currently primarily an autonomous-agent deployment/economy layer; **Evernode host economics** are the underlying compute-provider mechanism and should be evaluated separately if not already normalized.

---

## 10. Confidential.ai — useful comparator, not an open earning marketplace

Classification: `ADJACENT / CUSTOMER-SIDE INFRA`.

Current site sells confidential inference, confidential VMs and licensed confidential-compute software. It is useful for estimating customer-side TEE prices and understanding TEE hardware, but no public open marketplace was found where an arbitrary external operator joins and receives workload revenue.

Do not count as autonomous supplier income without a provider program.

---

## Cross-cutting evidence / risk update

### x402 transaction counts are weak demand evidence
Recent empirical research on the x402 ecosystem reports that raw settlement counts can be heavily concentrated and partly internally generated. Therefore all x402-derived candidates must be judged on:
- unique external buyers;
- repeat purchasers;
- actual merchant/provider USDC receipts;
- paid value excluding self/internal settlement;
- net revenue after upstream calls.

### x402 security must be modeled
Recent work has also identified authorization/settlement weaknesses across facilitator implementations. For our project this means any future autonomous seller should:
- use actively maintained libraries;
- bind payment proof to exact resource/price/network;
- enforce replay protection;
- verify settlement correctly;
- cap sponsored gas/exposure;
- keep hot-wallet balances limited.

This does not invalidate x402 income; it adds implementation and counterparty risk.

---

## Saturation metrics
- Deliberate control/tail passes completed after this run: **18** (Runs 018–035)
- New top-level economic mechanisms: **0**
- Fresh independent implementations with material relevance: **5+**
- Strong new current candidates: **Open Cloud, the402**
- New promising but insufficiently validated/watchlist: **x402.jobs, Cocoon, ALPENGLOW**
- Queue strengthened but still unresolved: **OpenGradient supplier side**

## Conclusion
**IN PROGRESS.**

The taxonomy has converged, but exact-neighbor discovery remains productive at the project level. Run 035 materially fails the completion condition because multiple previously uncatalogued, potentially viable provider/service implementations were found.

## Next run
Run 036 should focus on a **new-candidate normalization + demand reality pass**:
1. Open Cloud provider terms, minimum operational requirements, business/geography eligibility, payout unit/cycle and demand evidence.
2. the402 live catalog/job/request demand, provider counts, completed jobs where observable, fees, direct USDC withdrawal/geography and upstream-ToS-safe automated-service opportunities.
3. x402.jobs docs, revenue accounting, public server/resource statistics and buyer concentration.
4. Cocoon operator requirements/software/current mainnet status/reward rates and TON payout proof.
5. ALPENGLOW contracts/repository/node download/production jobs/token state/provider receipts/terms.
6. Search exact neighbors around `agent provider webhook earn USDC`, `autonomous service marketplace USDC`, `cloud-backed compute provider marketplace`, `confidential GPU provider earn`, `AI inference provider paid per request`.
7. Revisit Evernode host economics if not already separately normalized.

Only after these stop producing new material provider projects should the project move to the final all-category saturation pass.
