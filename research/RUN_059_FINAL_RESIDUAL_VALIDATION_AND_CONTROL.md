# Run 059 — Final residual validation + compact supplier-role control

Date: 2026-08-17
Status: **completed**
Project state after run: **IN PROGRESS**

## Scope
Validated the four Run 058 residual leads and repeated a compact supplier-role discovery pass using inference-provider, storage-operator, relay-provider and agent-job vocabulary.

## 1. Swan Inference
Classification: **WATCHLIST / early live surface**
Category: compute/GPU/inference marketplace
Automation: 5 in principle

Current evidence:
- Swan Inference exposes a current provider signup flow and explicitly advertises earning USDC for serving AI inference requests.
- Provider operation is described as one-command, NAT-friendly, with automatic model deployment/updates and on-chain settlement.
- Swan 2.0 docs describe a decentralized inference marketplace, stablecoin customer payments and provider rewards from stablecoin revenue plus SWAN incentives.
- Provider collateral exists. Current docs say legacy collateral remains until SIP-002 is ratified; SIP-002 proposes hardware-tier collateral and benchmark-based slashing.
- Existing Swan CP/FCP docs show GPU-oriented infrastructure and, for the older FCP path, public-IP/domain/SSL/Kubernetes-style requirements.

Important contradiction / demand signal:
- The public inference network surface currently indexed by search showed 0 online providers, 0 registered providers, 0 requests and 0 weekly earnings. This may be a temporary frontend/API failure, but it prevents treating Swan Inference as proven-utilized production income today.

VPS/bare-metal/home:
- Ordinary CPU-only VPS: **no** for the inference-provider role.
- GPU bare metal / GPU server: **yes in principle**.
- Home GPU: provider signup claims NAT-friendly operation, so technically plausible; exact accepted GPU matrix and commercial admission conditions remain unresolved.

KYC/geography:
- No current public evidence found in this pass that explicitly excludes Azerbaijan or requires provider KYC. Treat as **unknown**, not permission.

Payout / collateral / costs:
- Payout: advertised USDC; Swan docs also describe SWAN incentive rewards.
- Collateral: required under provider collateral model; exact live amount depends on currently active rule set.
- Costs: GPU depreciation/rent, electricity, bandwidth, storage, gas, collateral opportunity cost.

Net model:
`Net = USDC inference revenue + liquid SWAN rewards - GPU/server cost - electricity - bandwidth/storage - gas - collateral opportunity cost - expected slashing - maintenance`

Conclusion: same known inference-supplier mechanism. Interesting architecture, but utilization proof is presently weak/contradictory.

## 2. AntSeed
Classification: **VERIFIED (early but production-capable)**
Category: agent/API/inference service marketplace
Automation: 5

Current evidence:
- Open provider admission: no central marketplace account required; provider registers on-chain, stakes and announces services to a DHT.
- Three supply modes are explicitly documented: raw inference, routing service and specialized AI agent.
- Base mainnet is the default production settlement chain.
- Buyers lock USDC; providers receive 96% of settled buyer payments; protocol fee is 4%.
- Minimum seller stake is 10 USDC.
- Providers can run local models or permitted upstream APIs. Official docs explicitly warn that simple credential/subscription resale may violate upstream terms and that providers are responsible for compliance.
- Linux is supported anywhere Node.js runs; seller operation is daemon/CLI friendly and therefore server-native.
- Independent current network telemetry surfaced 64 active peers, 57 on-chain-proven peers and many advertised services; this is stronger activity evidence than a mere provider guide, though provider-level advertised token/user figures should still not be treated as profit evidence.

VPS/bare-metal/home:
- CPU VPS: suitable for routing/agent/API-wrapper roles if upstream inference is remote.
- GPU bare metal/home GPU: suitable when running local inference.
- Public address/DHT/WebRTC/network requirements still need deployment testing before implementation.

KYC/geography:
- Protocol appears wallet/on-chain based and no central-account KYC was found in current official docs. No Azerbaijan exclusion found. Regulatory, sanctions, tax and upstream-API restrictions remain operator responsibilities.

Payout / stake / costs:
- Payout: USDC on Base.
- Minimum provider stake: 10 USDC.
- Extra ANTS seller emissions exist, but provider-side ANTS remain locked in a dedicated pool under the current provider page; do not count them as liquid income.
- Costs: upstream API/model cost or local GPU cost, Base gas/RPC, server, stake opportunity cost.

Net model:
`Net = 0.96 × buyer USDC settlements - upstream API/GPU cost - server - RPC/gas - stake opportunity cost - failures/refunds - maintenance`

Conclusion: one of the strongest current matches to the target `server bot offers machine-readable paid work/service` objective, but profit depends on buyer demand and differentiated pricing.

## 3. UsePod
Classification: **VERIFIED / early-market**
Category: inference marketplace + API-key relay/resale
Automation: 5

Current evidence:
- Open supply side: operators can run a provider agent against local vLLM/llama.cpp/LM Studio/Ollama or enroll a permitted upstream-key relay.
- Marketplace routes earn providers 80% of settled inference; treasury receives 20%.
- Provider prices are capped at the cheapest centralized price for the model.
- Provider agent receives work over an outbound WebSocket; settlement is asynchronous and provider balances are credited automatically.
- Earnings cash out in USDC to Solana.
- Every provider posts a 50 USDC bond. Serious misbehavior can cause ban/bond seizure; bond is released after retirement cooldown.
- Current trust stack is reputation, canaries and bonds; stronger attestation is explicitly roadmap, not live.

VPS/bare-metal/home:
- CPU VPS: viable for permitted upstream-key relay/reseller mode.
- GPU bare metal/home GPU: viable for local provider-agent mode.
- Generic cloud GPU should be technically compatible if backend and network requirements are met; explicit provider ToS/geography still need implementation-stage recheck.

KYC/geography:
- No public provider KYC/Azerbaijan restriction was found in this pass. Large withdrawals may require manual approval. Treat jurisdiction support as **unknown until onboarding test/Terms review**.

Payout / bond / costs:
- Payout: USDC on Solana.
- Bond: 50 USDC.
- Costs: GPU/server or upstream API bill, bandwidth, bond opportunity cost, Solana withdrawal/transaction overhead, maintenance.

Net model:
`Net = 0.80 × settled inference billings - upstream API/GPU cost - server/electricity - bandwidth - bond opportunity cost - transaction/withdrawal cost - maintenance`

Conclusion: strong fully automated supply mechanism. The main unknown is fill rate because providers compete against a centralized fallback price ceiling.

## 4. DeCloudX
Classification: **WATCHLIST / claims need independent production validation**
Category: multi-resource DePIN operator + validator
Automation: 5 in claimed design

Current evidence:
- Official node page advertises five operator tiers: bandwidth/relay, compute/routing, GPU inference/training, storage, validator.
- Published stakes: 1,000 / 10,000 / 25,000 / 15,000 / 100,000 DCX respectively.
- Official pages claim settlement in DCX from real network usage and show specific hardware/bandwidth requirements.
- Official network page claims large node/job/storage/settlement statistics.
- Crucial caveat: the node page itself labels the detailed operator-console earnings/workload figures as **illustrative**. Therefore those numbers cannot be used as revenue proof.

VPS/bare-metal/home:
- Light relay tier explicitly profiles home/hobbyist hardware.
- Standard compute tier looks compatible with ordinary server hardware in principle.
- GPU/storage/validator tiers require materially heavier infrastructure.

KYC/geography:
- No reliable current public KYC/Azerbaijan rule was found in this pass.

Payout / stake / costs:
- Payout: DCX token according to official site.
- Stake: material and tier-specific.
- Costs: hardware/server, bandwidth, storage/GPU/electricity, token acquisition/opportunity cost, slashing for validator/high-risk roles.

Net model:
`Net = liquid value of usage-linked DCX rewards - infrastructure cost - electricity/bandwidth/storage - stake opportunity cost - token liquidity/price loss - expected slashing - maintenance`

Conclusion: all roles map to known compute/storage/bandwidth/validator families. Keep WATCHLIST until independent chain/explorer/liquidity and paid-utilization evidence are verified.

## Compact supplier-role control
Search vocabulary intentionally changed to supplier/host/operator/worker/publisher/seller/provider-program/machine-jobs/agent-jobs/inference-provider/storage-operator/relay-provider.

### New independent projects surfaced
1. **AgentLancer** — agent-to-agent job marketplace with requester/provider/verifier roles. Public page exposes programmatic job/proposal flow but currently reports verified earnings at $0. This is a new project, not a new mechanism.
2. **AgentGigs** — API-first marketplace where agents can register, browse available jobs, accept/apply, submit deliverables and receive Stripe Connect payout after client approval. Strong autonomous-workflow fit; needs primary Terms/activity validation.
3. **Jobs in AI / agent onboarding surface** — advertises programmatic agent registration/application and Stripe-escrow milestone payout. Needs identity, ToS and real-job validation.
4. **Surplus Intelligence** — surfaced through an OpenClaw seller-management integration describing a USDC-settled inference orderbook/reseller role on Base. Because the discovery source was a third-party GitHub integration rather than the primary platform, it remains an **UNVERIFIED lead**.
5. **Alien / Liquid Compute** — provider/market-maker/creator positioning for GPU compute with blockchain settlement. Same compute-provider mechanism; requires primary economics/admission validation.

### Saturation result
- New top-level mechanisms: **0**.
- The four Run 058 leads all normalize into existing families.
- However, the repeated supplier-role control still produced **five independent project leads**, including at least two directly relevant autonomous agent-job markets (AgentLancer and AgentGigs).

Under the repository's completion rule this is still a material residual project cluster. The project must therefore remain **IN PROGRESS** for one tightly scoped Run 060 rather than declaring completion prematurely.

## Next run
Run 060 should validate only the five new leads above, with special priority on AgentLancer and AgentGigs, then perform one final minimal cross-check using their exact economic vocabulary. If no further material cluster appears and no new mechanism emerges, complete the project.