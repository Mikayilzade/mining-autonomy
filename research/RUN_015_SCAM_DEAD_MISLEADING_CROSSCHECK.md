# Run 015 — Scam / dead / discontinued / misleading-opportunity cross-check

Evidence date: 2026-08-15

## Goal
Re-scan commonly rediscovered passive-income / mining / bandwidth / task-market claims and separate:
- current production payout;
- points-only or discretionary future rewards;
- residential-only opportunities that are not server-native;
- legitimate-but-restricted opportunities;
- scam patterns and fake income mechanics.

This run does not claim full saturation. It is a defensive normalization pass before profitability and geography filtering.

## 1. Strong anti-pattern taxonomy

### A. Deposit-to-work / recharge-to-complete-task schemes — REJECT
If a supposedly paid task/job requires the worker to deposit their own money to unlock tasks, increase commissions, clear a negative balance, or finish a task bundle, treat it as a fraud pattern rather than autonomous income. FBI guidance explicitly identifies this as a cryptocurrency job-scam pattern.

### B. Withdrawal-fee / tax-unlock traps — REJECT
If a platform freezes withdrawals and then demands new taxes, verification deposits, clearance fees, liquidity fees, or additional capital to unlock existing funds, stop treating displayed balances as earnings. FBI and SEC enforcement material identify this as a recurring crypto-investment fraud pattern.

### C. Guaranteed high mining / staking / yield returns — REJECT unless independently proven
CFTC/SEC and SEC enforcement examples explicitly warn about websites claiming mining/trading returns that are very high, guaranteed, and low/no-risk. A real mining business exposes hash rate, hardware, electricity, network difficulty, fees, counterparty risk and fluctuating returns; fixed guaranteed daily return is a major red flag.

### D. Fake cloud-mining / fake node-license economics — REJECT until verifiable
A dashboard showing "hashrate", "node rewards" or "daily mining" is not evidence of production. Require a verifiable supplier role, actual hardware/network work, transparent payout mechanics, withdrawal path, operator identity, and ideally on-chain/network evidence. If the only economic source is new deposits or referrals, classify as scam/ponzi risk rather than resource income.

### E. Points are not income — RESTRICT / WATCHLIST / REJECT depending on terms
Points must not be converted to cash in project economics unless current official terms establish a conversion/redemption path. Explicitly separate:
1. points with no monetary value;
2. points that may influence discretionary future rewards;
3. points with a defined current conversion to token/cash.

### F. Referral-heavy is not automatically fraud, but referral-only is not independent resource income
Referral bonuses may coexist with a genuine service. Count the underlying service as the earning mechanism and referral revenue as a distribution layer. Do not treat a referral tree as proof that customer demand exists.

### G. "Runs on Linux/Docker" does not mean server-native
Current residential-bandwidth services often provide Linux or Docker clients while still forbidding datacenter/server/VM use. Server eligibility must come from terms or supplier documentation, not software compatibility.

## 2. Current project cross-checks

### DAWN — REJECT as current cash income / keep as points-only adjacent
Official DAWN terms state that Rewards are points, may never convert into cash, cash equivalent, cryptocurrency or other assets, have no monetary value, and can be revoked or terminated. Therefore current browser-extension participation must not be counted as realized passive income.

Classification: `REJECTED` for current income; `WATCHLIST` only for future network economics.

### Nodepay — UPGRADE from old points-only ambiguity to RESTRICTED / current token reward path
Current Nodepay docs describe monthly cycles where eligible participation points can be converted into Nodecoin ($NC), claimed to a connected wallet, and withdrawn on-chain. This is materially stronger than a pure points-only system.

However, many rewarded actions involve active contribution/signals and fraud checks rather than a simple unattended bandwidth daemon. The passive-bandwidth component still needs a clean current earnings-rate and device/server-policy normalization before promotion to a high-priority autonomous opportunity.

Classification: `RESTRICTED` pending bandwidth-specific economics and environment rules.

### Grass — VERIFIED reward path, but not fixed cash income
Grass official materials now state that contribution can lead to Grass Tokens or USDC rewards. A July 10, 2026 official update says Stage 2 participant rewards for eligible users are being made available in USDC. Current terms still state that points themselves have no monetary value and rewards are discretionary/non-guaranteed.

This means the old "points only" shorthand is no longer accurate. Grass is a real rewarded bandwidth mechanism, but expected revenue cannot be inferred directly from points and must be modeled from distributions, geography, uptime, network usage and eligibility.

Classification: `VERIFIED` for rewarded bandwidth; `RESTRICTED` for deterministic profitability.

### EarnApp — current and legitimate, but explicitly residential-only
Official support states VMs, Docker, cloud hosting, personal/home servers, and devices used for business/monetization purposes are prohibited; personal residential devices only. Current support also confirms multi-device use is allowed within ToS, but unique residential IPs drive independent earning capacity.

Classification: `VERIFIED` Tier B residential; `REJECTED` for server-native deployment.

### Pawns.app bandwidth sharing — current and legitimate, residential-only
Current Terms require a valid residential IP and explicitly disallow servers, VPNs and proxy services for traffic sharing.

Classification: `VERIFIED` Tier B residential; `REJECTED` for server-native deployment.

### PacketStream Packeter — current cash bandwidth mechanism
Current Terms (updated July 20, 2026) state Packeter currently credits $0.10/GB of eligible customer traffic, with $5 minimum cashout via PayPal and 3% cashout fee. Device/connection must be owned or authorized.

Current public material describes broadband/residential sharing and Linux via Docker. This run does not infer datacenter permission from Docker support. Treat ordinary server-native use as unresolved until explicit datacenter policy is validated.

Classification: `VERIFIED` passive bandwidth; server-native status `RESTRICTED/TBD`.

### TraffMonetizer — current cash bandwidth mechanism; datacenter eligibility not yet proven from Terms
Current Terms describe paid shared-traffic monetization with $10 withdrawal threshold and current country restrictions. Official downloads include Docker. Terms require lawful control of device/connection and prohibit fraudulent traffic manipulation, but do not by themselves prove that arbitrary VPS/datacenter IP supply is accepted.

Classification: `VERIFIED` bandwidth monetization; server-native `RESTRICTED/TBD` pending explicit IP-type policy.

### Repocket — current cash bandwidth mechanism, but VM/proxy access restriction
Current Terms describe cash compensation for valid offers and leftover-data/bandwidth sharing and explicitly prohibit VPN/location masking. Current site policy text states users must not use VPNs, proxies, emulators or virtual machines to access Repocket. Therefore it should not be generalized into a VPS-farm opportunity.

Classification: `VERIFIED` passive bandwidth / consumer model; `REJECTED` for ordinary VM bot-farm deployment.

### EarnFM Fleetshare — strong supplier-side finding retained
Current official Fleetshare docs explicitly describe supplier onboarding for 20+ active IPs, KYC, supplier agreement, API key, user consent, and rates of $0.10/GB residential and $0.04/GB datacenter traffic. This is one of the clearest legitimate supplier/fleet models because datacenter traffic is explicitly priced in developer documentation.

Important nuance: ordinary EarnFM app onboarding may block datacenter IPs, while Fleetshare supplier documentation separately supports application users, servers or devices and publishes a datacenter rate. Treat the supplier program as a distinct role rather than assuming consumer-app rules apply.

Classification: `VERIFIED` supplier/fleet bandwidth role; high relevance to autonomous infrastructure.

## 3. Common rediscovery traps to preserve

1. "AI mining" often means bandwidth/data contribution, GPU inference, competitive model scoring, or token points — classify by what is actually paid for.
2. Browser uptime points are not cash until redemption is established.
3. Airdrop history proves past reward distribution, not future deterministic APY.
4. Docker availability can coexist with a server ban.
5. A consumer bandwidth app and a supplier/SDK/fleet program from the same company can have different datacenter rules.
6. "Passive income" landing-page claims such as "up to $X/month" are marketing ceilings, not expected value.
7. A withdrawal minimum is not proof of payout reliability; verify terms, payment rail and current operation.
8. Referral depth/bonuses are separate from underlying unit economics.
9. Cloud-mining contracts should be treated as counterparty/investment products, not direct mining infrastructure.
10. Any fixed/guaranteed daily mining return should trigger enhanced fraud review.

## 4. New durable decision rules

- `CURRENT PAYOUT > POINTS`: only current redeemable value enters revenue models.
- `ROLE-SPECIFIC TOS`: consumer, supplier, SDK, reseller and fleet roles must be evaluated separately.
- `ENVIRONMENT EXPLICITNESS`: datacenter/VPS eligibility requires explicit evidence, not inference from Docker/Linux.
- `NO DEPOSIT TO WORK`: paid-task systems requiring worker-funded deposits are rejected.
- `NO PAY-TO-WITHDRAW`: unexpected taxes/fees/deposits required to release existing earnings are a fraud red flag.
- `NO GUARANTEED MINING APY`: mining economics must float with real inputs; guaranteed high yield is presumptively deceptive until independently established.

## 5. Status impact

This pass found meaningful state changes and therefore the project is not saturated:
- Nodepay moved beyond pure points-only ambiguity into a current token conversion path.
- Grass now has a clearly documented current reward path including USDC distribution for Stage 2 eligible participants.
- PacketStream and TraffMonetizer are confirmed current rather than dead rediscovery leads.
- EarnFM Fleetshare remains a particularly strong supplier-side bandwidth mechanism with explicit datacenter pricing.
- DAWN remains a clear example of points that current Terms say have no monetary value.

## 6. Next run
Run 016 should normalize profitability and deployment economics across the highest-priority autonomous/server-native opportunities, including:
- revenue unit;
- utilization dependency;
- minimum efficient scale;
- server/GPU/storage/bandwidth cost;
- capital/stake/collateral;
- payout/withdrawal friction;
- expected maintenance;
- breakeven formula;
- whether positive EV depends on owning hardware versus rented cloud resources.

After that, perform Azerbaijan/KYC/geography filtering and then repeated saturation/control passes.
