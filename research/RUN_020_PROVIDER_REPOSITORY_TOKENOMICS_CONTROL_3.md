# Run 020 — Provider/repository & tokenomics control pass #3

Date: **2026-08-16**
Status: **COMPLETED — project still IN PROGRESS**

## Goal
Revisit the unresolved supplier/provider tail using current primary documentation, official repositories and alternative role vocabulary: capacity provider, supply node, workerpool, resource provider, edge supplier, operator rewards, node rewards, host marketplace, permissionless provider and capacity seller.

Completion test for this run: determine whether the third saturation/control pass finds any new independent earning mechanism or still uncovers meaningful new viable provider projects.

## Executive result
- **New top-level economic mechanisms: 0.**
- **Materially new / upgraded viable provider projects: 4 strong, plus several important reclassifications.**
- Therefore taxonomy convergence is strong, but project-level saturation is **not yet sufficient** to declare the whole research complete.

This pass strengthened the evidence that the universe is converging by mechanism: customer-paid compute/storage/bandwidth/session work + token subsidies/stake/collateral keeps recurring. However, alternate supplier vocabulary still surfaced real projects that were previously unresolved, so one more broad cross-directory/control pass is justified.

## Strong discoveries / upgrades

### 1. dTelecom SFU Node Operator — upgraded from WATCHLIST to VERIFIED/RESTRICTED
**Category:** server-native real-time communications / SFU bandwidth+compute service

Current official material now explicitly states that node operators can run nodes and earn **75% of customer payments**. The current SDK discovers decentralized SFU nodes through a Solana mainnet registry, and the current x402 gateway exposes customer-paid WebRTC/STT/TTS services.

Why this matters: this is very close to the original target — an online machine that serves real requests and receives a share of customer payments. It is not merely inflation-for-uptime.

Classification:
- Server-native potential: **high**
- Automation: **5** once admitted/configured
- Revenue source: customer real-time communication usage
- Payout: crypto-native; exact operator settlement details still need deployment-level confirmation
- Admission: current public site says “Become a Node Operator”, but exact permissionless onboarding/stake/hardware gates require a dedicated implementation check
- Risk: service quality/latency demand concentration; real utilization is critical
- Status: **VERIFIED mechanism, RESTRICTED for deployment until onboarding details are normalized**

Net formula:
`Net = 0.75 × attributable customer payments - server/bandwidth/egress - stake/license if any - maintenance - token/withdrawal costs`

### 2. Edge Network Host — upgraded to VERIFIED
**Category:** compute/storage/bandwidth edge host

Current official site/wiki confirms community operators contribute capacity and earn XE/EDGE rewards. Current host instructions use the mainnet CLI, Linux and Docker. The staking page says only **Host** onboarding is currently available to the community and lists a 100 XE Host stake, while uptime/performance affects rewards and penalties.

Why this matters: this is a genuine autonomous resource-provider role, not merely a speculative node license.

Classification:
- Server-native: **plausible/yes for Linux host**, but exact VPS/datacenter policy should be checked before renting cloud instances
- Automation: **5**
- Resources: compute + storage + bandwidth
- Stake: current wiki lists 100 XE for Host, subject to change
- Revenue: network jobs + node reward pool; demand/performance weighted
- Status: **VERIFIED**, economics still require measured pilot

Important caution: “expected yield” pages are protocol targets/estimates, not guaranteed fiat returns.

### 3. StorX Storage/Farm Node — upgraded from unresolved tail to VERIFIED/RESTRICTED
**Category:** storage provider

Current official StorX pages explicitly describe farm/storage node rewards, SRX staking, hardware/network requirements and a VPS/server setup path. The page currently lists roughly 6 CPU cores, 8 GB RAM, 1 TB storage, high bandwidth/speed and 24/7 availability; staking and reputation affect rewards.

Classification:
- Server/VPS compatible by official onboarding language: **yes**, subject to economics
- Automation: **5**
- Capital: SRX stake + storage/server
- Revenue: SRX hosting/staking rewards tied to node reputation
- Risk: token/stake/reputation and likely weak economics if renting retail storage
- Status: **VERIFIED/RESTRICTED** pending actual reward-rate, liquidity and Azerbaijan payout modeling

Likely structural conclusion: strongest where disk/server is already owned; retail VPS storage arbitrage needs skepticism.

### 4. Impossible Cloud Network Hardware Provider / ScalerNode — upgraded to real but curated provider path
**Category:** professional storage/compute capacity provider

Current ICN docs explicitly define Hardware Providers who contribute storage/compute and receive ICNT. Rewards combine customer-utilization rewards with temporary capacity subsidies. Hardware providers must collateralize nodes; current docs describe a long initial commitment (36 months) and slashing/performance requirements.

Crucially, current onboarding is **contact/verification based** rather than open anonymous VPS mining. Current protocol docs also say only one storage hardware class is presently available.

Classification:
- Economic mechanism: **VERIFIED**
- Ordinary user/VPS accessibility: **RESTRICTED / professional-provider onboarding**
- Automation: **5** after onboarding
- Capital: hardware + substantial ICNT collateral; long lock
- Revenue: booked utilization + temporary capacity subsidy
- Risk: slashing, collateral lock, token price, professional hardware thresholds
- Status: **RESTRICTED**, not a first low-capital pilot

This corrects the earlier ambiguity between Impossible Cloud commercial storage/reseller offerings and the separate ICN protocol provider path.

## Important reclassifications / unresolved tails

### YOM — VERIFIED Tier B/device path, not generic VPS path today
Current 2026 operator/docs pages make the model much clearer:
- gaming PC GPU contributes streaming sessions;
- NANO secure-boot device/license is required for self-hosting;
- each license enables one concurrent session;
- rewards are session/utilization driven and settle in YOM;
- official payout docs currently show a 40/55/5 operator/foundation/burn split;
- NaaS/datacenter delegation is targeted for Q3 2026 and is not yet active according to docs.

Result: **real autonomous GPU income**, but current self-host path is hardware/device-gated and therefore Tier B, not a normal arbitrary VPS/GPU-host marketplace.

The site’s headline monthly earnings are marketing estimates dependent on utilization and must not be treated as guaranteed returns.

### iExec PoCo — protocol real; simple public worker admission still unresolved
The official PoCo repository is current and surfaced a 2026 release, confirming the worker/workerpool contribution/reward/staking protocol remains technically alive. However current search still did not establish a straightforward self-service 2026 ordinary-VPS worker onboarding flow.

Result: keep **RESTRICTED/WATCHLIST**. A live protocol contract is not enough to classify an easy public earning path.

### Fleek Network — mechanism still strong, production status evidence still stale/ambiguous
Current docs continue to show:
- measured CPU/bandwidth commodities;
- Delivery Acknowledgements used to determine node rewards;
- node health expected to be “running and staked”.

But surfaced official landing/docs still contain alpha/testnet/pre-mainnet language and the tokenomics page is explicitly preliminary. This run did not establish a clean 2026 liquid mainnet operator payout path.

Result: **WATCHLIST/RESTRICTED**, not deployment-ready.

### Fluence — economic mechanism credible, current provider onboarding still insufficiently current
Official Fluence material supports compute-provider FLT rewards and stake per CPU. Yet the surfaced direct evidence remains old relative to 2026 and no sufficiently current self-service provider onboarding/economics page was found in this pass.

Result: **WATCHLIST/RESTRICTED**, requiring direct provider-console/repository follow-up before implementation.

### Spheron Community GPU — supply exists; public supplier onboarding still not proven
Current docs clearly let customers rent “Community GPUs,” so third-party supply exists. But this pass again failed to locate a current self-service supplier admission/reward specification.

Result: **RESTRICTED** rather than inferring public host eligibility from consumer marketplace pages.

## Saturation metrics

### New independent mechanisms
**0**

Third consecutive control pass in which no genuinely new top-level economic mechanism was needed.

### Material project-level discoveries/upgrades
- dTelecom node operator — major upgrade
- Edge Host — major upgrade
- StorX node — major upgrade
- Impossible Cloud Network Hardware Provider — major clarification/upgrade
- YOM — resolved into Tier B/device model with explicit current payout economics

This is still too much project-level discovery to call the full universe saturated.

### Repeated patterns confirmed
1. Customer-paid machine service + provider revenue share.
2. Customer-paid capacity + token subsidy.
3. Stake/collateral + performance/slashing.
4. Usage/reputation/latency controls actual utilization.
5. Device/license gating can prevent generic VPS participation.
6. Curated supplier onboarding is common even in “decentralized” networks.

## Economics implications
- **dTelecom** deserves future empirical demand testing because it exposes a clear customer-payment share.
- **Edge** deserves a low-cost pilot only after confirming VPS/datacenter acceptance and current XE liquidity/reward rate.
- **StorX** is likely most attractive on sunk/owned storage; rented cloud storage must beat both server cost and stake opportunity cost.
- **ICN** is not a low-capital experiment: professional onboarding + long collateral commitment make it infrastructure-business territory.
- **YOM** should be compared against alternative uses of the same gaming GPU, electricity and license/NANO capital; demand is regional.

## Geography / KYC notes
This run did not find Azerbaijan-specific exclusions in the primary pages above. Do **not** interpret absence of an exclusion as confirmed availability. Before CAPEX, live onboarding must test:
- Azerbaijan residency/KYC acceptance;
- exchange/wallet route for reward token;
- sanctions/geofencing language;
- payout minimums and tax/withdrawal friction.

## Completion decision
**NOT COMPLETE.**

Reason: top-level mechanisms appear strongly saturated, but Run 020 still produced multiple material provider upgrades. The project-level tail has not yet converged enough to satisfy the completion rule.

## Next run — Run 021
Perform a **broad cross-directory / alternative-vocabulary control pass #4** designed to catch remaining projects rather than new mechanisms.

Required query families:
- decentralized cloud provider earn capacity
- idle server capacity marketplace provider
- edge node operator customer revenue share
- storage node VPS earn
- GPU host community provider onboarding
- machine API marketplace provider revenue share
- bandwidth/CDN node customer fees
- DePIN hardware provider storage compute
- workerpool / executor / prover / relayer supplier
- autonomous service marketplace x402 / pay-per-call / agent service provider

Sweep current DePIN/cloud directories only as discovery aids, then validate every net-new candidate against primary docs.

Explicitly revisit:
- Fluence
- Fleek
- iExec workerpool
- Spheron supplier
- dTelecom operator onboarding details
- Edge VPS/datacenter acceptance
- any renamed/relaunched compute/storage/bandwidth projects

If Run 021 finds **0 new mechanisms and only negligible (0–2 weak/restricted) net-new viable projects**, perform one final short saturation check and prepare COMPLETE. If it again finds several material provider projects, continue.

## Durable output
- `research/RUN_020_PROVIDER_REPOSITORY_TOKENOMICS_CONTROL_3.md`
- `research/SOURCES_RUN_020.md`
