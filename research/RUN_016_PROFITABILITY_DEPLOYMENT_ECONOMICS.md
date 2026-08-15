# Run 016 — Profitability / deployment-economics normalization

Evidence date: 2026-08-15

## Goal
Normalize the economics of the highest-priority autonomous/server-native resource markets before spending more discovery effort. The key question is not merely whether a daemon can earn, but under what utilization, pricing, capital, uptime and cost conditions it can produce positive net income.

This run does **not** claim exact future profit for any platform. Marketplace prices, utilization, token prices, electricity and bandwidth costs change continuously. The durable output is a comparable economic model and current primary-source constraints.

## 1. Cross-market economic model

For machine/resource markets use:

`Net monthly = paid utilization revenue + protocol incentives - electricity - server/rack rent - bandwidth/egress - storage/media replacement - platform/payment fees - chain/gas fees - depreciation - expected downtime/slashing loss - maintenance labor - tax`

For owned hardware:

`Economic profit = cash net - opportunity cost of using the same hardware on the best alternative market`

For rented hardware/cloud:

`Arbitrage margin = worker/provider revenue - rental bill - data-transfer/storage/API fees - failed-job/idle-time cost`

A rented-cloud deployment is only attractive when the platform's expected paid utilization and rate exceed the all-in cloud bill. A technically runnable VPS is not evidence of positive EV.

### Utilization threshold
If a resource earns `R` per paid hour, variable operating cost is `V` per active hour, and fixed monthly cost is `F`:

`break-even paid hours = F / (R - V)`

`break-even utilization = break-even paid hours / available hours`

For a 30-day month, available hours are approximately 720 per continuously available unit.

### Storage threshold
If storage earns `S` per TB-month, egress earns `E` per TB, expected stored utilization is `u_s`, expected monthly egress is `q_e`, and fixed cost per TB-month is `C`:

`Net/TB-month = S*u_s + E*q_e - C - expected collateral/slashing/drive-loss cost`

### Bandwidth supplier threshold
If payout is `P` per GB and all-in cost of the IP/server is `F` per month plus incremental traffic cost `B` per GB:

`break-even GB/month = F / (P - B)`

This is crucial for datacenter bandwidth: an explicit $/GB rate is useful only if demand generates enough paid GB per IP/server.

## 2. Vast.ai host — VERIFIED marketplace economics; owned hardware strongly preferred

### Revenue unit / payer
Hosts set GPU, storage, upload and download prices. Customers rent machines and the host receives rental earnings. Pricing is market-driven rather than fixed.

### Current primary-source constraints
- Host can set per-GPU hourly price, storage price and bandwidth prices.
- On-demand and interruptible prices coexist; reserved discounts may be offered.
- Host documentation says clients may drive GPUs close to maximum capacity during rentals and expects strong uptime, networking and cooling.
- Earnings are directly observable per machine and day through Vast's host earnings API.
- First payout takes roughly two weeks; payout rails include external payment processors depending on host setup.

### Economics
For one GPU:

`Net = occupied_hours * host_GPU_rate + storage_income + bandwidth_income - electricity - depreciation - connectivity - maintenance - payout/platform deductions`

The dominant variable is **occupied hours**. An idle listed GPU earns no compute rent.

### Owned vs rented
- **Owned spare GPU:** strong candidate because sunk hardware can be monetized when otherwise idle.
- **New financed hardware:** must beat depreciation/interest and electricity at realistic utilization, not 100% occupancy.
- **Rent a cloud GPU and relist it:** generally fragile; cloud rental price already embeds provider margin, and Vast hosts compete aggressively. Only pursue if there is a verifiable structural cost advantage and upstream provider terms permit resale.

### Minimum efficient scale
Can begin with a single eligible machine, but uptime, cooling, remote recovery and networking overhead improve with a dedicated host setup/fleet.

### Classification
`VERIFIED`, automation 4–5, server/bare-metal native. Profitability: `UTILIZATION-DEPENDENT`.

## 3. Akash provider — VERIFIED infrastructure business, not a tiny passive VPS trick

### Revenue unit / payer
Providers bid to host deployments and earn lease revenue from tenants. Current docs identify CPU, GPU, RAM, storage, IP leases and premium features as revenue components.

### Current primary-source constraints
- Providers publish capacity and pricing and automatically bid on matching orders.
- Providers lock AKT for active bids/leases rather than permanent collateral.
- Default provider configuration includes a bid deposit; official architecture docs show an example `0.5 AKT` bid deposit.
- Provider docs explicitly frame costs as hardware/infrastructure, electricity, maintenance, staff/operations and token stake.
- Current getting-started docs describe physical servers **or VMs**, but also require Linux/Kubernetes/networking/domain skills and estimate ongoing operations at roughly 2–4 hours/week.

### Economics
`Net = sum(active lease revenue) - cluster/server cost - electricity - IP/transit/storage - chain fees - operational labor - downtime/failed-lease cost`

Provider pricing can be automated through the bid engine, including dynamic pricing scripts. This makes Akash attractive as an autonomous **capacity allocator**, but not zero-maintenance.

### Owned vs rented
- **Owned datacenter/homelab capacity:** potentially attractive if capacity is already underused and reliable.
- **Wholesale/bare-metal arbitrage:** viable in principle if upstream monthly cost is lower than realized Akash lease revenue at realistic utilization.
- **Ordinary retail VPS arbitrage:** usually weak because margin must cover the upstream cloud provider plus Akash competition and operational overhead.

### Minimum efficient scale
Higher than Golem/Vast single-node experimentation. Kubernetes/provider operation, networking, domain and monitoring overhead favor multiple resources or a small cluster.

### Classification
`VERIFIED`, automation 4–5 after setup, server-native. Profitability: `UTILIZATION + OPERATIONS DEPENDENT`.

## 4. Golem provider — VERIFIED low-barrier CPU/GPU resource seller, but demand is the bottleneck

### Revenue unit / payer
Requestors pay providers in GLM for resource usage. Current docs define CPU pricing per utilized thread-hour, with optional environment/start fees.

### Current primary-source constraints
- Default provider installer currently suggests 0.1 GLM/hour/thread but explicitly warns this may be high relative to market conditions.
- Provider selection is controlled by requestor criteria/preferences including cores and reputation/performance.
- Current docs allow multiple providers from one IP.
- Official FAQ discusses running providers on cloud platforms such as OVH/AWS; server execution is therefore a legitimate environment, not a residential-only interpretation.
- Mainnet payment uses real GLM, commonly over Polygon; testnet tGLM has no value.

### Economics
For CPU:

`Gross = paid_thread_hours * GLM_per_thread_hour * GLM_price`

`Net = Gross - server/electricity/depreciation - chain/withdrawal friction - maintenance`

A 16-thread server listed at 0.025 GLM/thread-hour does **not** earn `16*0.025*720` automatically. Only actually utilized thread-hours count.

### Owned vs rented
- Very suitable for testing on an already-running server because incremental setup cost is small.
- Renting a VPS solely for Golem requires historical paid-thread utilization high enough to cover the entire VPS bill; idle supply can easily destroy the arbitrage.
- Multi-provider-from-one-IP support helps fleet management but does not create demand.

### Classification
`VERIFIED`, automation 5 after setup, server-native. Profitability: `DEMAND-LIMITED`.

## 5. EarnFM Fleetshare — VERIFIED explicit datacenter bandwidth unit economics

### Revenue unit / payer
Supplier revenue is based on traffic routed through supplied IPs.

### Current primary-source constraints
- Fleetshare is explicitly intended for Linux servers running 24/7.
- Supplier program requires at least 20 active IPs, application approval, KYC/KYB and supplier agreement.
- Current official rate table: **$0.10/GB residential** and **$0.04/GB datacenter**.
- Standard minimum withdrawal is $15; bank-transfer invoicing is available above $300 monthly traffic value according to current docs.
- Traffic volume depends on IP geography and reputation; more IPs can receive more traffic, but no fixed utilization is guaranteed.

### Economics
For datacenter supply:

`Gross = accepted_paid_GB * $0.04`

`Net = Gross - IP/server rental - bandwidth/egress cost - KYC/business/admin cost - maintenance`

If the server/IP pool costs `F` per month and upstream traffic cost is effectively zero/unmetered, break-even traffic is:

`GB_break_even = F / 0.04`

Examples purely as formulas:
- $4/IP-month cost -> 100 paid GB/month required per equivalent cost unit.
- $10/IP-month cost -> 250 paid GB/month required.

If upstream bandwidth itself costs $0.01/GB, contribution margin becomes $0.03/GB and required traffic rises by one third.

### Key conclusion
Fleetshare is unusually valuable for this project because the platform publishes an explicit **datacenter** $/GB rate and allows authorized server/fleet participation. The unresolved variable is demand/utilization by geography/IP reputation. Therefore the first implementation experiment later should measure paid GB/IP/day before acquiring a large IP fleet.

### Classification
`VERIFIED`, automation 5, server-native supplier program. Profitability: `TRAFFIC-DEMAND DEPENDENT`.

## 6. Storj storage node — VERIFIED, but low storage rent makes rented disk unattractive

### Revenue unit / payer
Storj Labs-operated satellites pay storage node operators for actual stored data and actual egress/audit/repair bandwidth.

### Current official rates
Current docs still publish:
- storage: **$1.50/TB-month**;
- egress: **$2.00/TB**;
- audit/repair: **$2.00/TB**.

Payout is monthly and subject to a wallet minimum tied to transaction fees; sub-threshold balances roll forward.

### Economics
`Net/TB = 1.50 * occupied_TB + 2.00 * egress_TB + 2.00 * audit_repair_TB - drive/power/network/depreciation`

At 100% occupancy, storage-only gross is just $1.50/TB-month before egress. Therefore:
- existing underused disks can be rational;
- buying retail cloud block storage to resell is normally impossible to justify;
- egress can matter, but is customer-demand driven and must not be assumed.

### Operational economics
A new node also needs time to receive data; capacity offered is not instantly filled. Drive failure and replacement matter because payout per TB is low.

### Classification
`VERIFIED`, automation 5, server/home hardware. Profitability: `BEST FOR SUNK/LOW-COST DISK`.

## 7. Sia host — VERIFIED market-priced storage with explicit collateral

### Revenue unit / payer
Renters pay hosts for storage and bandwidth; host sets prices and locks collateral that can be lost for failed contracts.

### Current official recommended starting economics
Current Sia host docs recommend approximately:
- storage: **$1/TB-month**;
- egress: **>$5/TB**;
- ingress: **$0–$0.05/TB**;
- collateral multiplier: **2x storage price**;
- max collateral starting guidance: around 10x the collateral price for a contract.

The docs explicitly warn that excessively high prices reduce renter selection and excessively low prices may not cover operating expense.

### Economics
`Net = storage_contract_revenue + egress + ingress/contract/RPC fees - disk/power/network/depreciation - chain costs - expected collateral loss`

Because suggested storage rent is only around $1/TB-month, the same conclusion as Storj applies: **cheap owned excess storage** is structurally better than rented cloud disk. Egress pricing offers more upside but requires real retrieval traffic.

### Classification
`VERIFIED`, automation 5 after host setup, server/home storage. Profitability: `LOW-COST-DISK + UPTIME DEPENDENT`.

## 8. Filecoin storage provider — VERIFIED but capital/operations heavy

### Revenue unit / payer
Storage providers can earn client deal payments and protocol block rewards. Current docs explicitly say business planning must include hardware, CAPEX/OPEX, collateral and network variables.

### Current primary-source constraints
- Initial FIL collateral is required and is proportional to committed storage.
- Missing storage proofs can lead to penalties/slashing.
- WindowPoSt must prove sectors continuously; proving periods and 30-minute deadlines create hard operational requirements.
- At least 10 TiB storage power is required for eligibility for WinningPoSt/block rewards.
- Official docs warn not to rely solely on block rewards and note committed-capacity economics can be unprofitable depending on FIL price.
- Current provider docs note new/extended/updated sectors incur daily fees after FIP-0100 activation.

### Economics
`Net = deal revenue + expected block rewards - hardware - sealing/proving compute - power - storage - network - chain/daily fees - financing cost of FIL collateral - expected slashing/fault loss - operations`

Expected block rewards must be modeled probabilistically from quality-adjusted storage power, not treated as deterministic APY.

### Owned vs rented
Ordinary VPS/cloud resale is not the right mental model. Filecoin is closer to a storage-infrastructure/mining business with capital, collateral, proving hardware and operational discipline.

### Classification
`VERIFIED`, automation 4 after mature setup, server-native but capital-heavy. Profitability: `SCALE + TOKEN + DEAL FLOW + COLLATERAL DEPENDENT`.

## 9. Comparative ranking by economic simplicity

### Best for a low-capital experiment later
1. **Golem CPU provider on an already-paid server** — very low incremental cost; measure actual paid utilization.
2. **EarnFM Fleetshare with already-controlled eligible datacenter IPs** — explicit unit price; measure GB/IP/day before scaling.
3. **Storj/Sia on already-owned spare disk** — low incremental cost but likely small absolute income.

### Best for owned GPU hardware
1. Vast.ai-style GPU marketplace.
2. Competing GPU provider markets from earlier runs (Akash GPU, Golem GPU, io.net, Clore, TensorDock, Runpod where eligible).
3. AI-incentive/prover networks only after comparing expected reward per GPU-hour against ordinary rental opportunity cost.

### Better treated as infrastructure businesses, not tiny passive bots
- Akash provider.
- Filecoin storage provider.
- Livepeer orchestrator/indexer/prover/validator roles with stake or specialized operations.

## 10. Resource opportunity-cost rule

Every physical resource should be compared against competing uses before deployment.

### GPU
`choose market with highest expected net $/GPU-hour after idle probability, fees, power and failure risk`

A token-reward worker paying $0.40 expected net/GPU-hour is inferior to a GPU rental marketplace paying $0.55 expected net/GPU-hour at comparable risk, even if the token worker advertises a higher nominal APY.

### CPU
Compare Golem/compute worker income with:
- ordinary VPS resale/service hosting;
- paid API/micro-SaaS use;
- proof/AI worker roles;
- leaving capacity idle if incremental electricity exceeds revenue.

### Storage
At current official Storj/Sia storage rates, storage markets strongly favor sunk/cheap disk. Compare with backup hosting, object-storage resale, content distribution and other storage networks before purchasing new drives.

### Bandwidth/IP
Compare Fleetshare/proxy supplier income with:
- IP lease cost;
- bandwidth/egress cost;
- abuse/reputation/security overhead;
- alternative legitimate proxy/CDN/relay markets.

## 11. Deployment decision matrix

Before any future implementation, require all of these:
1. Current payout rail verified.
2. Server/environment explicitly allowed.
3. Unit revenue known or measurable.
4. Paid utilization can be measured separately from uptime.
5. Full recurring cost known.
6. Stake/collateral/slashing included.
7. Withdrawal/KYC/geography verified.
8. Opportunity cost of same hardware calculated.
9. Small-scale experiment possible before large CAPEX.
10. Stop-loss rule defined if measured utilization is below break-even.

## 12. New durable conclusions

1. **Utilization is the hidden variable across nearly all machine markets.** Listed capacity is not paid capacity.
2. **Owned spare resources have a structural advantage.** Retail cloud arbitrage usually stacks one provider margin on top of another and therefore needs an unusual price/demand mismatch.
3. **Storage $/TB-month is currently thin.** Storj and Sia make strongest sense for otherwise-idle low-cost disks, not rented cloud storage.
4. **Explicit datacenter bandwidth pricing is rare and valuable.** EarnFM Fleetshare remains a high-priority empirical test candidate.
5. **Token emissions must be converted to expected $ per resource-hour**, then compared with customer-paid marketplaces.
6. **Collateral is a real cost even when returned later** because it has financing/opportunity cost and may be slashed.
7. **Minimum scale differs radically.** Golem can be a one-machine experiment; Akash/Filecoin are operational businesses.
8. **No platform in this run supports a claim of guaranteed passive profit.** The correct next phase is geography/KYC filtering and then saturation discovery, followed later by controlled experiments.

## 13. Next run
Run 017 — Azerbaijan / KYC / payout / geography filter across the highest-priority shortlist.

Check:
- whether Azerbaijan individuals/businesses can onboard;
- KYC/KYB providers and unsupported-country lists;
- payout rails available to Azerbaijan;
- crypto-only vs fiat settlement;
- tax/business-account friction to flag for later legal review;
- IP/geographic demand effects;
- whether supplier programs require US/EU entities or bank rails.

After Run 017 begin repeated broad + niche saturation/control passes using alternate terminology and ecosystem directories.