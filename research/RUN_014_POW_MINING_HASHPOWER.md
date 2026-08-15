# Run 014 — Proof-of-Work / mining / hashpower normalization

Date: 2026-08-15
Status: **completed**

## Goal
Normalize cryptocurrency mining as an earning family without confusing it with customer-paid compute marketplaces, storage-provider markets or stake-based validator income. Focus on legal/ToS-compliant autonomous operation, current pool mechanics, hashpower resale, merged mining, cloud restrictions and practical deployment constraints.

## Executive result
PoW mining is a genuine highly autonomous income family, but it is usually **hardware-and-energy arbitrage**, not a generic “rent a cheap VPS and earn” opportunity. The strongest subfamilies are:

1. owned ASIC/GPU/CPU hardware mining directly to a pool;
2. owned/authorized hashrate sold to a hashpower marketplace;
3. owned/authorized hashrate rented through a rig-rental marketplace;
4. merged/AuxPoW mining where one workstream earns multiple chain rewards;
5. algorithm/profit-switching that routes hardware to the best permitted destination;
6. approved dedicated/bare-metal/cloud mining where the provider explicitly permits it and economics survive rental cost;
7. mining-pool infrastructure / brokerage as a build-once service rather than mining return itself.

Ordinary shared VPS mining is generally a weak or rejected economic strategy even where technically possible. Several major providers require prior written approval or prohibit mining outright.

---

## 1. Core economic taxonomy

### A. Emission-funded PoW mining
**Who pays:** protocol issuance + transaction fees.

**Commodity supplied:** verifiable hash work securing a PoW chain.

**Automation:** 5/5 after setup; mining daemon/firmware can run continuously with monitoring.

**Main costs:** hardware purchase/depreciation, electricity, cooling, hosting/rack fees, pool fee, payout/withdrawal fees, maintenance, downtime.

**Base net formula:**

`Net = block/fee share + merged rewards - electricity - hardware depreciation - pool fees - hosting/cooling - payout fees - maintenance - downtime loss`

This differs fundamentally from customer-paid compute networks: demand for coin issuance is protocol-defined, while profitability is driven by coin price, network difficulty/hashrate, block subsidy/fees and energy/hardware efficiency.

### B. Hashpower marketplace seller
**Who pays:** buyers purchasing temporary hashrate.

**Commodity:** algorithm-specific hashrate routed to buyer-selected pools.

**Automation:** 5/5 technically; can be continuously priced/routed.

**Revenue driver:** market rental price × accepted hashrate × uptime.

This is not the same as mining the destination coin yourself. The seller earns marketplace consideration; the buyer takes destination-pool mining exposure.

### C. Hashrate rig rental
A marketplace rents an identifiable rig or hashrate allocation for a period. MiningRigRentals currently charges rig owners **3% of rental receipts** and documents automated/API-based resale/brokerage as an allowed business model when disclosures and platform rules are followed.

### D. Merged / Auxiliary Proof-of-Work
One PoW stream can secure additional compatible chains without adding equivalent new physical hashrate. f2pool explicitly documents BTC merged rewards and LTC merged rewards, making this a real additive-revenue mechanism rather than a marketing label.

### E. Profit-switching / route optimization
Software compares current pool/algorithm/hashpower-market revenue and directs compatible hardware to the highest expected net route. This is a **strategy layer**, not a new source of return. It can reduce idle/poor allocation but cannot create positive economics if all destinations are below energy + depreciation cost.

---

## 2. Mining pool economics

### Current f2pool evidence
Current f2pool documentation (July 2026) shows a useful live cross-section of payout schemes and fees:

- BTC: FPPS or PPLNS; FPPS fee 4%, PPLNS fee 2%; default payout threshold 0.005 BTC.
- LTC: PPS; 4% fee; default threshold 0.02 LTC.
- BCH: PPS; 3% fee.
- ETC: PPS; 1% fee.
- DASH: PPS; 2% fee.
- ETHW: PPS; 1% fee.

f2pool currently uses PPS, PPLNS, PPS+ and FPPS depending on asset.

### Payout-scheme interpretation
- **PPS**: pool absorbs more block-luck variance; miner receives expected share-based payment less fee.
- **FPPS/PPS+**: extends deterministic-style share payment to some transaction-fee components.
- **PPLNS**: miner retains more short-term variance because payout depends on shares in a rolling window around blocks found.

For autonomy research, payout scheme changes **variance/cash-flow timing**, not the underlying expected physical efficiency of hardware.

### Pool risk fields to preserve
Every future profitability model should include:
- fee rate;
- payout threshold and cadence;
- payout coin/custody duration;
- orphan/stale share treatment;
- merged-mining reward policy;
- pool centralization/counterparty risk;
- regional stratum latency;
- withdrawal/network fee;
- whether rewards can be forfeited if auxiliary payout addresses are not configured.

---

## 3. Merged mining: validated additive mechanism

f2pool currently documents:
- BTC merged mining with FB, HTR, NMC, ELA and NAT;
- LTC merged mining with DOGE, BELLS, PEP, LKY and DINGO, with additional current update pages expanding the list further.

The key economic principle is that merged mining can add auxiliary rewards **without requiring proportional additional hashrate**. It should therefore be modeled as:

`Primary mining net + expected auxiliary rewards - auxiliary payout/handling costs`

It is not free money in an absolute sense: auxiliary-token liquidity, payout thresholds, wallet support and pool policy matter. Some current f2pool guides state that auxiliary rewards do not accrue until the corresponding payout address is configured, so operational automation must include wallet-configuration checks.

Poolin also currently documents BTC/Fractal Bitcoin merge mining and LTC/DOGE/Bellscoin-style merge mining examples, confirming that the mechanism exists beyond a single pool.

---

## 4. Hashpower marketplaces

### NiceHash — VERIFIED mechanism, fee normalization pending
Current official NiceHash pages continue to describe the product as a live **hashrate marketplace**, with mining, ASIC/CPU/GPU supply, live marketplace pricing, compatible pools and profitability tooling. The seller-side mechanism is therefore current and distinct from ordinary pool mining.

Classification:
- status: **VERIFIED mechanism / pricing details to revalidate**;
- automation: 5/5;
- resource: CPU/GPU/ASIC hashrate;
- server-native: only where the underlying host/hardware provider permits mining and economics work;
- revenue: buyer-paid hashpower demand, generally settled through NiceHash's platform;
- key risk: marketplace demand/price volatility + platform/custody/KYC rules + hardware cost.

Do **not** treat a current marketplace price as stable expected monthly revenue. It changes continuously by algorithm and order-book demand.

### MiningRigRentals — VERIFIED seller + broker/reseller model
Current official help center states:
- rig-owner service fee: **3%** of received rental value;
- rental proceeds are held for dispute resolution after a rental finishes before becoming available;
- owners may set payout/autopayout settings;
- a current explicit **Hashrate Resale / Broker Policy** permits third-party hashrate sourcing, dynamic API pricing/listing, routing to rentals/fallback destinations and retaining a margin, subject to disclosure, performance and withdrawal rules.

This creates two distinct earning models:
1. own-rig rental seller;
2. authorized hashrate broker/reseller with dynamic API allocation.

The broker model is especially relevant to the original autonomous-bot idea because pricing and routing may be automated. However, it is not risk-free arbitrage: upstream cost, downstream utilization, refunds, uptime, hashrate consistency and withdrawal restrictions must all be modeled.

---

## 5. Cloud / VPS / server policy normalization

### Hetzner — REJECTED for mining
Current Hetzner Terms and dedicated-server service agreement explicitly prohibit cryptocurrency mining applications. The wording includes mining, farming and plotting. Therefore Hetzner must not be used as a mining host in this project.

### DigitalOcean — RESTRICTED / prior written permission required
DigitalOcean's current Acceptable Use Policy (updated March 20, 2026) prohibits mining cryptocurrency **without explicit written permission**. Therefore ordinary deployment is not assumed permitted.

### Google Cloud — RESTRICTED / prior written approval required
Current Google Cloud terms state that cryptocurrency mining requires Google's prior written approval; Free Trial Services cannot be used for mining. Treat mining as unavailable unless approval is obtained.

### AWS — RESTRICTED / written approval required
AWS current security guidance states that AWS requires written approval for crypto mining under Service Terms and that Free Tier/credits cannot be used for mining. Mining on AWS without that approval is outside the accepted strategy set.

### Akamai/Linode — RESTRICTED; dedicated resources only with prior support context
Current Linode support guidance says shared-CPU cryptomining can violate resource-use policy; dedicated CPU plans may be permissible but support recommends opening a ticket and notes approval is not guaranteed. Treat shared VPS mining as rejected and dedicated mining as restricted until explicit current account-level approval is received.

### General cloud rule
A cloud VM being technically capable of running a miner never proves permission. Provider policy must be checked individually. Even with permission, public-cloud hourly CPU/GPU prices are usually designed for general compute workloads and often exceed mining revenue; rented-cloud mining therefore needs a strict break-even test before any implementation.

---

## 6. Proof-of-capacity / plotting normalization

“Storage mining” must be separated into two families:

1. **protocol PoW/PoSpace/plotting** — rewards come from blockchain issuance/fees for maintaining plotted capacity or proofs;
2. **customer-paid storage provider** — rewards come from storing/retrieving user data under contracts.

They may use the same disks but have different economics. Hetzner's current prohibition explicitly includes cryptocurrency plotting, so even non-CPU-heavy plotting cannot be assumed allowed there.

No new high-confidence server-native plotting opportunity was promoted in this run because the goal was mechanism normalization; concrete live plotting chains remain for later candidate-level profitability screening.

---

## 7. Hardware classes

### ASIC mining
Best suited to stable algorithm-specific workloads where specialized hardware dominates efficiency. Capital intensive but generally the economically serious class for ASIC-dominated chains.

Key variables:
- J/TH or analogous efficiency metric;
- purchase price and residual value;
- firmware/pool compatibility;
- electricity tariff;
- thermal/noise/hosting constraints;
- network difficulty and block economics.

### GPU mining
More flexible across algorithms and may switch between mining, inference/rendering/compute rental and other GPU markets. This flexibility gives an **option value** absent from many ASICs.

Important cross-market strategy:
`route GPU to max(expected mining net, compute-market net, rendering net, AI-worker net)`.

### CPU mining
Technically autonomous and accessible, but ordinary rented VPS economics are generally weak. CPU mining remains relevant mainly where:
- the chain is intentionally CPU-oriented;
- hardware is already owned/sunk-cost;
- electricity is unusually cheap;
- mining is one fallback use among other CPU-paid workloads.

### Disk / plotting
High write volume, drive wear and storage opportunity cost must be included. “Low electricity” does not automatically mean low total cost.

---

## 8. Autonomous strategies worth later modeling

### Strategy 1 — owned-hardware profit router
Continuously compare:
- direct pool mining;
- merged-mining-enabled pools;
- hashpower marketplace sell price;
- rig-rental price;
- alternative GPU compute markets.

Switch only when expected net improvement exceeds switching cost, pool ramp/variance effects and operational risk.

### Strategy 2 — merged-mining maximizer
Prefer pools that expose valid auxiliary rewards where wallet/liquidity support exists and effective net is positive.

### Strategy 3 — hashrate broker
Acquire authorized upstream hashrate under clear contracts and resell through a marketplace/API where rules expressly permit brokerage. MRR currently documents this as a permitted model. Profit formula:

`Net broker margin = downstream rental revenue - upstream hashrate cost - marketplace fees - refunds - payout/transaction fees - support/operations - expected downtime loss`

### Strategy 4 — hybrid GPU allocator
A scheduler chooses among mining, AI inference, rendering and generic GPU compute based on current expected contribution margin. This can be more robust than “mine 24/7” because GPU economics vary across markets.

### Strategy 5 — owner-operator ASIC hosting
Purchase ASICs and place them with an explicitly mining-friendly hosting provider priced by kW/kWh/rack. This is not “serverless” and requires capex, but can be highly autonomous after deployment.

---

## 9. Rejected / weak patterns

### Free-tier mining
Rejected. Major clouds prohibit or restrict this; it is also commonly uneconomic and high risk for account loss.

### Shared-VPS CPU mining
Rejected as a default strategy. Even where not explicitly banned, sustained CPU saturation can violate fair-use policies and rented cost usually dominates mining output.

### Hidden/consentless browser mining
Rejected. It violates the project's consent/integrity boundary and can constitute cryptojacking.

### Mining on infrastructure contrary to provider ToS
Rejected regardless of expected gross revenue.

### Treating “cloud mining contract” marketing as equivalent to owned hashrate
Rejected as an assumption. Such contracts require counterparty, custody, pricing and fraud-risk validation and should be treated as capital products, not as direct autonomous mining infrastructure.

---

## 10. KYC / geography

This run did not establish a universal Azerbaijan restriction for ordinary self-mining to a wallet; protocol mining itself is generally permissionless at the chain level. However, centralized pools, marketplaces, exchanges and fiat off-ramps may impose KYC, sanctions/geography rules or payout restrictions.

Therefore geography/KYC must be attached to the **intermediary** used, not to PoW mining as a universal mechanism.

High-priority later check:
- current NiceHash account/KYC/Azerbaijan eligibility;
- MiningRigRentals account/withdrawal/KYC geography;
- pool-specific account requirements;
- practical Azerbaijan electricity/hosting assumptions;
- exchange/off-ramp access.

---

## 11. Profitability framework for Run 014 candidates

### Direct miner
`Monthly net = H × R_hash - kWh × tariff - hosting - pool fee - payout fees - depreciation - maintenance`

Where `R_hash` is expected gross revenue per unit hashrate after difficulty/block economics but before listed costs.

### Marketplace seller
`Monthly net = accepted hash × avg marketplace payrate × uptime - marketplace fee - energy - depreciation - hosting - payout fees`

### Rented cloud miner
`Monthly net = mining gross - cloud hourly charge - storage/egress - pool fees - payout fees`

If cloud charge is fixed and materially exceeds conservative mining gross, reject immediately without optimizing further.

### Hardware break-even electricity price
`break-even tariff = (gross mining revenue - non-electric operating costs - depreciation target) / monthly kWh`

### Hardware payback
`payback months = hardware acquisition cost / conservative monthly cash contribution`

Do not use payback if the denominator depends on unrealistic constant coin price/difficulty assumptions; scenario ranges are required.

---

## 12. New durable rules from this run

1. **Mining is energy/hardware arbitrage; hashpower resale is customer-demand arbitrage.** Keep them separate.
2. **Pool payout scheme changes variance/cash-flow, not hardware efficiency.**
3. **Merged mining is a genuine additive mechanism** and should be captured separately in profitability models.
4. **Cloud permission must be proven provider-by-provider.** AWS/Google/DigitalOcean require approval; Hetzner prohibits; shared Linode-style VPS mining is not a default compliant path.
5. **Algorithm/profit switching is a strategy layer, not a source of return.**
6. **GPU hardware has cross-market option value** because the same asset may earn from mining, AI, rendering or compute rental.
7. **Hashrate brokerage is a distinct automation opportunity** when a marketplace explicitly allows API-based resale and disclosures are satisfied.
8. **Do not infer profitability from gross hashprice or a calculator screenshot.** Model energy, depreciation, marketplace/pool fees and downtime.
9. **Proof-of-capacity/plotting and customer-paid storage are different economic families.**
10. **Cloud-mining contracts are capital/counterparty products**, not equivalent to owning or operating a miner.

---

## 13. Run completion / next work

Run 014 completes the planned PoW/hashpower normalization stage.

Next priority:
1. broad scam/dead/discontinued-project cross-check across all prior runs;
2. normalize profitability formulas and minimum evidence required for ranking;
3. Azerbaijan/KYC/payout filter on strongest candidates;
4. begin repeated broad + niche saturation/control passes;
5. only then consider COMPLETE if passes stop producing independent mechanisms and almost no viable projects.

Saturation/control passes completed after this run: **0**.

Conclusion: project remains **IN PROGRESS**.