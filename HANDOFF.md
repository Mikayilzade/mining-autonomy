# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read, in order:
   - `START_HERE.md`
   - `STATUS.md`
   - `METHODOLOGY.md`
   - `HANDOFF.md`
   - `RUN_LOG.md`
   - `CATALOG.md`
   - `SOURCES.md`
   - latest run-specific files named in STATUS.
3. Trust repository state over remembered chat state.
4. Continue from `STATUS.md -> Next run priority`.
5. Search the live web because platform rules, rewards, availability and economics are time-sensitive.
6. Prefer current primary sources.
7. Update run-specific research/source files plus STATUS and this HANDOFF before ending the run. Update RUN_LOG when full current contents can be safely preserved; never truncate historical state merely to append a new run. Central CATALOG may lag run-specific findings until a safe normalization pass.

## User intent
The user wants an exhaustive theoretical inventory first, implementation later.

Primary target: autonomous online/server bots/nodes/services that can continuously earn from legitimate simple work with minimal input.

Secondary target: all other passive/semi-passive income mechanisms, including home compute/storage/bandwidth, physical DePIN, capital-based yield, and systems that become passive after initial creation/investment.

Weak, restricted, rejected and dead options must stay documented so later runs do not rediscover and re-hype them.

## User interaction preference
Unless the user asks a substantive question, report only `в процессе` while unfinished and `завершено` only when the completion gate is genuinely met.

## Current durable checkpoint
Runs **001–009** are complete.

Latest files:
- `research/RUN_009_PHYSICAL_DEPIN.md`
- `research/SOURCES_RUN_009.md`

`STATUS.md` is the authoritative current checkpoint and next-run pointer.

## Run 009 durable findings
Physical DePIN was decomposed into distinct paid commodities rather than one generic category:
- wireless traffic carriage — Helium;
- road imagery — Hivemapper;
- vehicle telemetry — DIMO;
- GNSS/RTK correction data — GEODNET;
- weather telemetry — WeatherXM;
- ADS-B aircraft positional data — Wingbits;
- smartphone road-scene metadata — NATIX;
- smartphone BLE relay — Nodle;
- mobile connectivity measurements — Roam;
- environmental/noise measurements — Silencio;
- navigation/driver data — MapMetrics;
- embedded publisher SDK device monetization — Nodle SDK and analogous SDK families.

### Strong physical/device confirmations
- **Helium IoT**: any compatible LoRaWAN gateway can be onboarded permissionlessly and earn HNT for carried device data. Current docs also support a `multi-gateway` architecture where one server fronts many physical gateways.
- **Helium Mobile/converted Wi-Fi**: eligible carrier-offload traffic can earn HNT. Commercial/high-traffic deployments have Helium Plus pathways.
- **Important Helium correction**: current official docs say Proof-of-Coverage was removed on **2026-07-06**. Never use old beacon/witness farming assumptions as current economics.
- **Hivemapper**: certified physical camera + authentic road imagery required; reward value depends on freshness/saturation/data utility. Synthetic/replayed imagery is excluded.
- **DIMO**: real connected vehicle/integration required for driver rewards; baseline issuance and marketplace data demand are separate revenue components.
- **GEODNET**: physical GNSS station earning is real; uptime/quality/density matter.
- **WeatherXM**: approved real weather station/gateway required; rewards depend on data quality, proof of location and cell capacity.
- **Nodle**: real smartphone BLE/location/Internet contribution; background operation can be highly autonomous, but a generic VPS cannot replace the phone/radio/geographic contribution.

### Server-native leads discovered inside physical ecosystems
These are important for later Tier-A control passes:
1. **NATIX xNodes** — docs describe staked validator nodes earning from uptime/validation tasks, but current public production onboarding/hardware/stake/payout remain unproven. WATCHLIST.
2. **DIMO Storage Nodes** — deployed economics allocate a portion of paid data-access demand to storage entities, but current developer docs still say `Coming Soon`. WATCHLIST.
3. **DIMO data validators** — current developer docs still `Coming Soon`. WATCHLIST.
4. **Helium multi-gateway server** — legitimate server control-plane role for fleets, but not standalone VPS income because physical radios create the paid commodity.
5. **Nodle publisher SDK** — BUILD-ONCE app monetization: integrate an opt-in SDK so user phones provide IoT connectivity and publisher earns revenue/rewards.
6. **Physical-DePIN fleet orchestration SaaS** — newly identified BUILD-ONCE family: paid monitoring/accounting/uptime/firmware/location optimization service for device fleets.

### Restricted/watchlist findings
- **Wingbits**: reward mechanics and approved ADS-B/GNSS/security hardware are real; current docs still describe beta/devnet-to-mainnet transition, so do not yet count as proven liquid cash yield.
- **Roam Network**: Android connectivity-measurement contribution is real, but current docs still describe pre-TGE points and future XRO conversion. Points are not current cash.
- **Silencio**: Terms say in-app Noise-Coins cannot be redeemed for cash from Silencio; newer SLC tokenomics describes a transferable token economy. Exact current contribution-to-liquid-token path needs validation.
- **MapMetrics**: current official FAQ advertises MMAP earning and global usage, including headline SPT token/hour figures. Treat as unnormalized marketing economics until token liquidity, hardware cost, caps and realized withdrawals are verified.

### New strategy lesson
**Physical DePIN stacking** is a separate strategy family. Wingbits documents HYFIX MGW310 as a combined Wingbits/GEODNET device. Later economics should search other legal multi-network combinations where hardware/site/power/backhaul are shared.

### Hard boundary reinforced by Run 009
Real-world verification is the product, not an obstacle to bypass. GPS/GNSS, radio reception, cryptographic hardware, authentic imagery, vehicle telemetry and environmental measurements cannot be faked/emulated merely to collect rewards. Such strategies are out of scope.

## Earlier durable lessons still active
- Docker/Linux support never proves VPS/datacenter eligibility.
- A runnable daemon is not enough: separately prove reward path, supply-side admission, permitted environment, hidden stake/license/collateral, payout mechanism and demand/utilization.
- Consumer brands can hide separate supplier/partner/developer programs; search those portals explicitly.
- Customer-paid utilization must be separated from temporary token/provider subsidies.
- Points/testnet/devnet units are not money without a current redeemable/liquid path.
- Bittensor must be decomposed by subnet/commodity, not treated as one generic miner.
- Competitive AI/solver networks require expected-share modeling, not simple hourly-rate assumptions.
- Permissionless software can still require significant stake, liquidity or hardware.
- Residential IP monetization and generic datacenter bandwidth monetization are separate commodities.
- Embedded SDK monetization requires explicit disclosure/consent and platform compliance; no deceptive bundling.

## Current next run
**Run 010 — capital-based passive/semi-passive income universe.**

Research broadly before profitability ranking:
- bank deposits/savings/term deposits;
- money-market funds/instruments;
- sovereign bills/bonds and inflation-linked instruments;
- investment-grade/high-yield bond structures;
- index/dividend/REIT/infrastructure/preferred/BDC/royalty securities;
- P2P/private credit/invoice financing/real-estate debt/revenue-share financing;
- PoS staking, liquid staking, restaking;
- crypto lending/stablecoin yield;
- AMM/LP yield and concentrated liquidity;
- fixed-rate DeFi;
- basis/funding/cash-and-carry and other market-neutral-looking strategies, explicitly without claiming guarantees;
- tokenized RWAs/revenue-share assets;
- automated treasury/vault/API strategies where current platform rules permit automation.

For each family record what actually pays the return, capital-loss modes, counterparty/custody/smart-contract risk, liquidity/lockup, KYC/geography, automation level, fees and a net-return formula.

After Run 010 continue build-once digital systems, automated task/API markets, dead/scam cross-check, profitability normalization, Azerbaijan/KYC filtering, and saturation/control passes.

## Completion
Only mark `COMPLETE` after repeated broad + niche saturation passes stop producing new independent mechanisms and produce negligible new viable projects. Document the final control passes, then disable the recurring research task.
