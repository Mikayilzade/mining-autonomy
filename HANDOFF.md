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
7. Update run-specific research/source files plus STATUS and this HANDOFF before ending a run. Update RUN_LOG only when full current contents can be safely preserved; never truncate history merely to append.

## User intent
Build an exhaustive theoretical inventory first; implementation comes later.

Primary target: autonomous online/server bots, nodes, services and machine markets that can continuously earn from legitimate simple work with minimal human input.

Secondary target: every other passive/semi-passive income mechanism, including home compute/storage/bandwidth, physical DePIN, capital yield, royalties and build-once automated businesses.

Weak, restricted, rejected, dead and points-only options must stay documented to prevent rediscovery and re-hype.

## User interaction preference
Unless the user asks a substantive question, report only `в процессе` while unfinished and `завершено` only when the completion gate is genuinely met.

## Current durable checkpoint
Runs **001–016** are complete.

Latest files:
- `research/RUN_016_PROFITABILITY_DEPLOYMENT_ECONOMICS.md`
- `research/SOURCES_RUN_016.md`

`STATUS.md` is the authoritative checkpoint and next-run pointer.

## Run 016 durable findings
A profitability/deployment-economics normalization pass was completed for representative high-priority autonomous resource markets.

### Cross-market economics
- Paid utilization is the critical hidden variable. Listed/online capacity is not automatically paid capacity.
- Owned spare hardware has a structural advantage over renting retail cloud resources and attempting to resell them.
- Always compare opportunity cost across competing uses of the same GPU, CPU, disk, bandwidth and IP resources.
- Collateral must be priced as capital with financing/opportunity cost plus expected slashing/loss.
- Later implementation should begin with small measured pilots rather than CAPEX based on headline rewards.

### Representative normalized candidates
- **Vast.ai:** host-set GPU/storage/bandwidth pricing; net return depends on occupied rental hours, electricity, depreciation and networking. Strongest with owned/low-cost GPU hardware.
- **Akash:** provider earns tenant lease revenue through automated bidding. Real server/cloud business with Kubernetes/networking/domain/operations overhead; better suited to a cluster or wholesale infrastructure than trivial VPS arbitrage.
- **Golem:** pay-per-use GLM resource market; CPU pricing is per utilized thread-hour. Very low barrier for an already-paid server, but utilization/demand is the bottleneck.
- **EarnFM Fleetshare:** official supplier docs explicitly target Linux servers running 24/7, require 20+ IPs plus KYC/KYB and agreement, and currently publish $0.04/GB datacenter / $0.10/GB residential rates. One of the best later empirical tests because unit revenue is explicit; actual GB/IP/day is still unknown.
- **Storj:** current official rates remain $1.50/TB-month storage and $2/TB egress/audit-repair. Thin storage economics favor sunk/cheap disks rather than rented cloud storage.
- **Sia:** current host guidance is roughly $1/TB-month storage and >$5/TB egress, with collateral. Again favors cheap owned storage and reliable uptime.
- **Filecoin:** capital/operations-heavy storage infrastructure business. Requires FIL collateral and continuous proofs; ≥10 TiB storage power for WinningPoSt eligibility. Profit depends on deal flow, token price, quality-adjusted power, fees and slashing risk.

### Economic formulas now mandatory
Resource marketplaces:
`Net = paid utilization revenue + incentives - infrastructure - electricity - bandwidth - depreciation - fees - capital/slashing loss - maintenance - tax`

Break-even utilization:
`paid_hours_break_even = fixed_cost / (revenue_per_paid_hour - variable_cost_per_active_hour)`

Bandwidth:
`GB_break_even = fixed_monthly_cost / (payout_per_GB - incremental_cost_per_GB)`

Storage:
`Net/TB-month = storage_rate*occupied_fraction + egress_rate*egress_TB - disk/power/network/depreciation - collateral/loss cost`

### Later low-capital experiment priority
Only after geography filtering and research saturation:
1. Golem on an already-paid server.
2. EarnFM Fleetshare with economically sourced eligible controlled IPs.
3. Storj/Sia on already-owned spare disk.
4. Vast.ai/other GPU markets where owned GPU hardware exists.

No candidate is assumed to provide guaranteed profit.

## Earlier durable lessons still active
- A runnable daemon is not enough: prove reward path, supplier admission, permitted environment, stake/license/collateral, payout mechanics and demand/utilization.
- Customer-paid utilization must be separated from token/provider subsidies.
- Testnet/devnet/points units are not money without liquid/redeemable path.
- Bittensor must be decomposed by subnet/commodity.
- Competitive AI/solver networks require expected-share modeling.
- Permissionless software can still require meaningful stake, liquidity or hardware.
- Residential IP monetization and datacenter bandwidth are separate commodities.
- Embedded SDK monetization requires explicit consent/disclosure and platform compliance.
- Data products require source-by-source legal/ToS/licensing validation.
- Market-neutral financial automation is still trading with execution/custody/liquidation risk.
- Marketplace discoverability without a payment rail is distribution, not income.
- Mining = hardware/energy economics; hashpower resale = customer-demand economics.
- Merged mining is a genuine additive mechanism; profit switching is only a routing strategy.
- No deposit-to-work or pay-to-withdraw schemes.
- Guaranteed/high fixed mining or yield claims require enhanced fraud review.
- Docker/Linux compatibility does not prove VPS/datacenter permission.
- Consumer, supplier, SDK, reseller and fleet roles must be checked separately.

## Current next run
**Run 017 — Azerbaijan / KYC / payout / geography filtering.**

For the highest-priority shortlist, verify:
- Azerbaijan individual/business onboarding;
- unsupported-country/sanctions/KYC lists;
- KYC/KYB requirements;
- payout rails available from Azerbaijan;
- crypto-only vs fiat settlement;
- SEPA/ACH/business-entity requirements where relevant;
- demand differences by IP geography;
- which platforms are practically testable from Azerbaijan.

After Run 017 begin repeated broad and niche saturation/control passes using alternate terminology and ecosystem directories.

## Completion
Only mark `COMPLETE` after repeated differently-worded broad + niche searches converge, producing no new independent earning mechanisms and negligible new viable projects, with all remaining uncertainty documented. Then record final saturation checks and disable the recurring research task.