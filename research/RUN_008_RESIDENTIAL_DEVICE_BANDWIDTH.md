# Run 008 — Residential / Device Passive Income + Bandwidth/IP Sweep

Date: 2026-08-15
Status: completed

## Scope
Dedicated sweep of residential-IP monetization, bandwidth-sharing apps, browser/device DePIN and adjacent supplier/SDK programs, with explicit separation between true server-native opportunities and consumer/residential-only programs.

## Executive findings

### 1. EarnFM Supplier / Fleetshare is a genuinely important server-native addition
EarnFM is not only a consumer bandwidth-sharing app. Current official Supplier/Fleetshare documentation explicitly supports supplier applications bringing 20+ IPs from application users, servers or devices, with integration types including SDK, Fleetshare server and Docker. Current docs also distinguish datacenter IPs from residential IPs and state no fixed upper limit for authorized datacenter connections. Fleetshare pays a lower documented datacenter rate than residential traffic.

Current official rate table in Fleetshare docs:
- Residential traffic: $0.10/GB.
- Datacenter traffic: $0.04/GB.
- Standard withdrawal threshold: $15.
- Supplier onboarding requires application/approval, KYC/KYB and signed supplier agreement.
- SDK/device integrations require recorded user consent; this is important for compliance and rules out covert bandwidth monetization.

Classification: `VERIFIED / SERVER-NATIVE BUT CURATED`.
Automation: 5 after acceptance; suitable for daemon/server deployment.
Economic caveat: traffic demand is not guaranteed, so revenue is `eligible GB routed × rate - server/network cost` rather than a fixed server yield.

### 2. EarnApp remains clearly residential-only and is unsuitable for server farming
Official support explicitly prohibits VMs, Docker, cloud hosting, personal/home servers and devices used for business/monetization purposes. Datacenter IPs are blocked. Current published earnings guide states up to $5/IP/month for rest-of-world and up to $10/IP/month for US, conditional on actual demand/usage.

Classification: `VERIFIED / HOME-RESIDENTIAL-ONLY`.
Automation: 5 on a compliant personal device, 0 for the intended VPS/server farm strategy.

### 3. Honeygain is residential/non-datacenter despite technical Docker support
Current support docs say Honeygain supports Linux through Docker, but Data Center (DCH), Organization, Reserved, Military and Government IP types are unsupported. A current anti-cheat article explicitly says users should not use data centers. VPS/VM/emulator use is technically possible but not recommended and can trigger fraud controls; typical VPS IPs are DCH and unusable.

Other current rules:
- maximum 10 gathering devices/account;
- 1 device per IP/network;
- PayPal default payout threshold $20;
- JumpTask mode can lower practical withdrawal threshold to 0.5 JMPT and pays in token form;
- Azerbaijan appears in Honeygain's current Tipalti payout-country list.

Classification: `VERIFIED / RESIDENTIAL-ONLY FOR PRACTICAL PURPOSES`.
Do not treat Docker support as server eligibility.

### 4. PacketStream is a real residential proxy supplier program with transparent economics
Current Terms (updated 2026-07-20) state Packeters earn $0.10 per GB of eligible customer traffic, $5 minimum cashout, USD via PayPal, weekly processing and 3% PacketStream cashout fee. The product is explicitly a residential proxy network and customer demand is not guaranteed.

Terms require the device/connection to be owned or authorized; current public materials describe desktop Windows/macOS/Linux Packeter usage. No current primary evidence in this run establishes ordinary datacenter/VPS Packeter eligibility, so it remains Tier B residential rather than Tier A server-native.

Classification: `VERIFIED / RESIDENTIAL-PROXY SUPPLIER`.

### 5. Pawns.app supports Docker/Linux technically, but datacenter-class IPs are rejected
Current Pawns help says Android, iOS, macOS, Windows and Linux are supported, including a Docker version. However, current support states datacenter-classified IPs can trigger the VPN error and are not accepted as normal earning connections. Azerbaijan appears in Pawns survey availability, but this does not itself prove bandwidth payout availability or payout-method support; those require a later country-specific check.

Classification: `VERIFIED DEVICE APP; RESTRICTED FOR VPS/DATACENTER`.

### 6. TraffMonetizer explicitly prohibits server/VPN/proxy use for the consumer app
Current Terms say users may access/use the Application only with a valid residential IP address and may not use servers, VPNs or proxy services. Minimum withdrawal is $10. Current downloads include Windows, Android, macOS and Docker, demonstrating again that Docker availability does not imply datacenter permission.

A separate current developer SDK program exists: app developers can integrate the SDK after review and earn $0.10/GB from consenting app users' bandwidth. This is a build-once distribution/SDK revenue mechanism rather than a VPS bandwidth-mining opportunity.

Classification:
- Consumer app: `VERIFIED / RESIDENTIAL-ONLY`.
- Developer SDK: `VERIFIED / BUILD-ONCE BANDWIDTH SDK`, approval required.

### 7. Repocket is explicitly anti-VM/VPN/proxy for ordinary earning
Current site/terms continue to advertise passive leftover-data sharing. Public rules state users must not use VPNs, proxies, emulators or virtual machines to access Repocket and must not create/use multiple accounts.

Classification: `VERIFIED / RESIDENTIAL-DEVICE ONLY`; unsuitable for VPS farming.

### 8. Grass has moved beyond vague points: current Stage 2 material documents USDC distribution
Current official Grass documentation says users are rewarded for unused internet and a July 2026 Stage 2 allocation article states USDC rewards combine Uptime Points and Network Points. It recommends residential networks, explicitly says not to use a VPN, and says payout distribution is made available through a non-custodial wallet after claim. It also reports traffic concentration: roughly 150k users received about 90% of network traffic in Stage 2, demonstrating strong utilization/geography skew.

Classification: `VERIFIED / RESIDENTIAL-DEVICE BANDWIDTH`.
Server-native status: `NO CURRENT EVIDENCE`; keep Tier B unless official datacenter permission appears.
Economic caveat: rewards are allocation/utilization based, not a simple fixed $/GB rate.

### 9. DAWN validator extension rewards are points, not proven cash income
Current DAWN site still advertises Validator Extension rewards and Proof of Bandwidth. However, the current Terms explicitly state Rewards/points have no monetary value, are not transferable/redeemable and may never convert into cash or crypto. DAWN's broader network and Black Box hardware may later have real network economics, but extension points alone cannot be counted as production passive income.

Classification: `WATCHLIST / NON-CASH POINTS` for extension rewards.
Do not count current extension points as earned money.

### 10. Nodepay has materially changed; passive-bandwidth mining is no longer the core current earning proposition
Current Nodepay privacy material still references Node Points for sharing unused bandwidth, but current 2026 product/docs center rewards on active human-like signal participation: answering prompts, creating signals, campaigns, sharing and genuine engagement. Docs explicitly emphasize genuine contribution and distinguish it from passive activity. Current stats page says the system evolved from bandwidth rewards into a predictive-intelligence engine.

For our intended autonomous passive bot, current Nodepay should not be treated as a clean bandwidth daemon opportunity. Automating engagement would also conflict with its authenticity/quality design.

Classification: `WATCHLIST / RESTRICTED`; passive bandwidth path requires fresh proof before counting as viable.

## Important mechanism split discovered in Run 008
Bandwidth monetization is not one category. It must be split into at least:

1. **Residential proxy exit-node supplier** — customer traffic exits through a household IP; value comes from residential IP reputation/geolocation. Examples: EarnApp, Honeygain, PacketStream, Pawns, TraffMonetizer consumer app, Repocket, Grass.
2. **Authorized datacenter bandwidth supplier** — server IPs may be accepted at lower value. Current strong example: EarnFM Fleetshare supplier.
3. **Embedded SDK monetization** — developer puts bandwidth-sharing SDK into a real app with informed user consent and receives revenue from user devices. Examples: EarnFM Fleetshare SDK, TraffMonetizer developer SDK, Honeygain Web Intelligence SDK.
4. **Proof-of-bandwidth / DePIN points** — participant proves uptime/bandwidth but reward may be non-cash/speculative. Example: DAWN Validator Extension.
5. **Activity/data contribution disguised by older bandwidth branding** — current reward requires genuine active responses/engagement rather than passive network sharing. Example: current Nodepay direction.

These mechanisms have materially different legality, server suitability and economics.

## Azerbaijan notes established this run
- Honeygain current Tipalti payout-country list includes Azerbaijan.
- Pawns.app current survey-country list includes Azerbaijan, but that is not sufficient to prove bandwidth payout-method support.
- EarnApp blocked-country list and payout support require later explicit Azerbaijan normalization; do not infer availability merely from absence in snippets.
- EarnFM supplier path is contract/KYC based; Azerbaijan supplier acceptance not yet proven.

## Safety / privacy / abuse considerations
Residential proxy products expose the participant's public IP as an exit node. Even if the provider says traffic is screened, practical risks include:
- IP reputation degradation;
- CAPTCHA/challenge increase on household browsing;
- ISP terms or fair-use conflicts;
- third-party abuse complaints;
- account/payment-provider KYC exposure;
- household privacy/security concerns.

These are legitimate products when operated according to provider rules, but they should be treated as IP-risk businesses rather than "free money."

## Economics formulas
For per-GB residential programs:
`Net = routed_GB × supplier_rate - incremental_bandwidth_cost - device_power - payout_fees - expected_IP_reputation_cost - maintenance`

For EarnFM datacenter supplier:
`Net = eligible_datacenter_GB × $0.04 - server/network cost - KYC/admin cost - payout/tax costs`

For Stage/allocation systems such as Grass:
`Net = allocation_value × probability_of_traffic/reward - device/network cost - claim/gas/tax costs`

Do not assume 24/7 connection implies 24/7 payable usage.

## Rejected / restricted conclusions from seed list
- EarnApp VPS farm: rejected by policy.
- Honeygain ordinary datacenter/VPS farm: rejected/restricted by IP policy.
- Pawns ordinary datacenter VPS: restricted; DCH detection prevents normal participation.
- TraffMonetizer consumer app on VPS/server: explicitly prohibited.
- Repocket VM farm: explicitly prohibited.
- DAWN extension points as cash income: rejected as current cash claim; keep watchlist for future token/network changes.
- Nodepay autonomous engagement bot: do not operationalize; current system emphasizes genuine active contribution and anti-spam quality.

## Candidates still needing dedicated continuation
- Repocket payout threshold/rates/country support normalization.
- Pawns bandwidth rate, payout methods/threshold and explicit Azerbaijan payout path.
- Grass Terms/device limits, country/KYC rules and current exact Stage 2 reward mechanics.
- EarnFM supplier Azerbaijan eligibility, exact payout methods, demand by datacenter geography and minimum viable economics.
- Honeygain Web Intelligence SDK as a separate build-once monetization family.
- Additional competitors/successors not yet validated: ProxyRack-style suppliers, ByteLixir, PacketShare, Bitping, mysterium-like consumer nodes, telecom/measurement panels and device telemetry programs.
- Dead/renamed historical programs: Peer2Profit and similar legacy bandwidth apps.

## Run conclusion
Run 008 materially expanded the taxonomy and found a high-priority server-native candidate that had been hidden inside a consumer bandwidth brand: **EarnFM Fleetshare authorized datacenter supplier**. It also eliminated multiple false server candidates where Docker/Linux support could have been misleading. Discovery is still productive. Project remains **IN PROGRESS**.
