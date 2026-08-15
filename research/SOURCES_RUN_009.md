# Sources — Run 009 Physical DePIN Sweep

Evidence date: 2026-08-15. Primary/official sources unless explicitly noted.

## Helium
- https://docs.helium.com/ — current overview: IoT LoRaWAN + Mobile carrier-offload networks; Hotspots provide coverage and earn HNT.
- https://docs.helium.com/iot/onboard-a-hotspot/ — any LoRaWAN gateway can join IoT as a Hotspot and earn HNT for device data; permissionless onboarding; `multi-gateway` supports one server fronting many physical gateways.
- https://docs.helium.com/iot/packet-forwarders/balena/ — Raspberry Pi + LoRa concentrator data-only Hotspot example; earns HNT for carried traffic.
- https://docs.helium.com/mobile/5g-on-helium/ — Mobile Hotspots/converted Wi-Fi networks provide carrier offload and earn HNT from eligible traffic.
- https://docs.helium.com/mobile/wifi-conversion-onboarding/ — existing Passpoint networks can be onboarded and earn HNT for carrier traffic; self-serve currently rewardable for Helium Mobile traffic, commercial fleets can use Helium Plus.
- https://docs.helium.com/tokens/data-credit/ — network usage paid in DC; Mobile data rate documented as $0.10/GB to network users; IoT billed per payload increments.
- https://docs.helium.com/tokens/hnt-token/ — HNT rewards operators; token emission schedule current through 2026+.
- https://docs.helium.com/network-data/oracle-data/ — important 2026 change: Proof-of-Coverage removed from Helium networks on 2026-07-06; do not use old PoC-mining assumptions.

## Hivemapper
- https://docs.hivemapper.com/contribute/driving/ — approved/certified mapping device required; Bee is current third-generation device; contributors collect street imagery and receive HONEY.
- https://docs.hivemapper.com/honey-token/what-is-honey/ — contributors earn HONEY for mapping data and Map AI labeling/editing; enterprise/developer map consumption burns HONEY.
- https://docs.hivemapper.com/honey-token/honey-burn-and-mint/ — customer map consumption feeds contributor incentives through burn-and-mint / consumption rewards.
- https://docs.hivemapper.com/honey-token/earning-honey/individual-reward-factors/map-tile-saturation/ — rewards vary with freshness/saturation and favor useful under-covered routes.
- https://docs.hivemapper.com/honey-token/earning-honey/individual-reward-factors/usable-imagery/ — unusable/fraudulent imagery does not earn.

## DIMO
- https://docs.dimo.org/governance/dip2 — deployed Baseline Issuance: authorized client + valid connected vehicle/integration + weekly transmitted data are required; emission declines 15% each year; rewards intentionally do not incentivize unnecessary driving.
- https://docs.dimo.org/governance/dip-3-marketplace-issuance-and-token-burn — deployed vehicle-data access fees; developers pay per vehicle/month; storage nodes receive 40% of DIMO-purchase pool proportional to DCX usage attributed to them.
- https://docs.dimo.org/developer-platform/ — developer roles include data provider; storage provider and validator are still marked `Coming Soon` in current docs.
- https://docs.dimo.org/docs/data/validation — vehicle data cross-validated against cellular/GPS/accelerometer/etc.; fabricated movement is not a legitimate strategy.

## GEODNET
- https://docs.geodnet.com/geod-token/geod-token-introduction — GEOD rewards operators of quality Base Stations and is also used to pay for RTK data service.
- https://docs.geodnet.com/geod-mining/hex-reward-rules — reward dilution/hex rules, NFT vs non-NFT station mechanics, anti-density economics.
- https://docs.geodnet.com/geodnet-console-platform-basics/track-your-stations-performance-and-rewards — rewards depend on uptime/RRR, multipath and device type; underperforming hours can earn zero; backbone bonus requires very high reliability.

## WeatherXM
- https://docs.weatherxm.com/introduction — community-owned weather stations provide data and receive WXM.
- https://docs.weatherxm.com/tokenomics — station owners receive WXM; 55% supply allocated to station rewards; commercial weather-data licensing creates token demand.
- https://docs.weatherxm.com/rewards/reward-mechanism — current v2.0 reward mechanism; data quality, PoL, hardware class/cell capacity and business boosts; rewards can be claimed programmatically from RewardPool.
- https://docs.weatherxm.com/rewards/proof-of-location — real location/continuity required; relocation temporarily reduces eligibility.
- https://docs.weatherxm.com/rewards/cell-capacity — finite rewardable station capacity per geographic cell.
- https://docs.weatherxm.com/wxm-devices/d1/connect-and-claim — physical weather station + always-powered gateway + Wi-Fi required; no data means no rewards.
- https://docs.weatherxm.com/rewards/reward-boosts — current bounty/boost framework can fund high-value cells from consumers/partners.

## Wingbits
- https://docs.wingbits.com/ — ADS-B aircraft-tracking network; specialized cryptographically secured hardware contributes data for rewards.
- https://docs.wingbits.com/get-started/hardware-needed — current approved HYFIX WB200 and MGW310 hardware options.
- https://docs.wingbits.com/project/wingbits-approved-hardware-program — ADS-B radio + cryptographic chip + GNSS + Ethernet required; client may run in Docker only with access to real radio/GPS/security hardware.
- https://docs.wingbits.com/wingbits-byod-english/grandfathered-byod-diy-info/hardware-needed — new BYOD onboarding ended 2024-10-14; old Raspberry-Pi DIY path is grandfathered.
- https://docs.wingbits.com/rewards/how-rewards-work — WINGS rewards are tied to useful positional messages, early-participation and data value/competition.
- https://docs.wingbits.com/tge-mainnet/devnet-wallet-and-rewards — current transition docs describe beta/devnet rewards and planned mainnet reissuance; beta tokens are not equivalent to already-liquid mainnet income.
- https://docs.wingbits.com/project/wingbits-faq — docs still describe project as beta and target mainnet timeline; treat monetization as WATCHLIST until mainnet/liquidity is current and verified.

## NATIX
- https://docs.natix.network/whitepaper/market-entry-products/natix-drive-and — smartphone camera + driving; on-device AI collects road-event metadata; users receive in-app rewards convertible within NATIX ecosystem.
- https://docs.natix.network/whitepaper/natix-economy/natix-economy-summary — in-app NATIX can convert to on-chain NATIX; separate `xNodes` are described as validator nodes that stake NATIX and earn from uptime/validation tasks.
- https://docs.natix.network/policies/campaign_terms — campaign terms explicitly say road metadata may be used to build maps and/or sold to third parties; campaign earning is app/mission dependent.

## Nodle
- https://docs.nodle.com/nodle-app — smartphone becomes BLE edge node; requires Internet, Bluetooth and location; NODL rewards depend on availability, Bluetooth availability and geographic coverage.
- https://docs.nodle.com/nodle-sdk — app publishers can embed the SDK; their users' phones become IoT hotspots and publisher can generate revenue without ads; distinct BUILD-ONCE SDK model.
- https://docs.nodle.com/nodl-token — rewards quantify network utility; rewards discourage dense device farms and favor coverage/movement.
- https://docs.nodle.com/introduction — architecture explicitly uses smartphone infrastructure, not generic VPS nodes.

## Roam Network
- https://docs.roam.network/introduction — Android smartphone connectivity-intelligence network; current Feb-2026 docs describe 127k installs/187 countries and pre-TGE state.
- https://docs.roam.network/faq — smartphone collects signal/latency/handover/geospatial measurements; contributors earn points; $XRO is planned utility/reward token.
- https://docs.roam.network/token-economy/airdrop — pre-TGE points allocate a community airdrop; points are not themselves cash.
- https://docs.roam.network/token-economy/contributor-rewards — post-TGE design: validated contributions earn points converted pro-rata into XRO by epoch.
- https://docs.roam.network/token-economy/supply-allocation — fixed-supply token plan; contributor pool emitted over 48 months.

## Silencio
- https://whitepaper.silencio.network/tokenomics — in-app contribution units feed SLC token allocation; transferable SLC token described.
- https://www.silencio.network/privacy-policy — consensual smartphone noise/geolocation/network measurements may be shared with business partners; users receive in-app noise coins.
- https://www.silencio.network/termsandconditions — important distinction: in-app Noise-Coins cannot themselves be redeemed for cash; fraudulent/unverified measurements can be destroyed and accounts suspended.
- https://whitepaper.silencio.network/tokenomics/data-monetization-and-value-accrual — data products sold in SLC; protocol revenue model tied to data commercialization.

## MapMetrics
- https://mapmetrics.org/faqs/ — current official FAQ says global navigation app can earn MMAP; rewards depend on activity/engagement; SPT device is vehicle/phone bound and advertised around 110 MMAP/hour under described conditions. Treat self-reported headline economics as unvalidated until liquid-market/net-cost checks.

## Notes on evidence quality
- All economics above are mechanism validation, not profitability proof.
- Token emissions, points and advertised token/hour figures are not converted to net income in Run 009.
- Azerbaijan-specific regulatory/radio-frequency/import/KYC availability still requires a dedicated geography pass.
