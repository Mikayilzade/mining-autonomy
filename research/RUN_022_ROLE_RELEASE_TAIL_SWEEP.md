# Run 022 — provider-role tail sweep

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Result
- New top-level economic mechanisms: 0.
- Material net-new provider projects: 2 — ThreeFold Farming and ParalonCloud GPU Provider.
- Material upgrades: OpenGPU, Iagon, DeNet.
- Conclusion: taxonomy remains strongly saturated, but provider-project tail is still producing material additions, so completion gate is not met.

## ThreeFold Farming
Status: VERIFIED/RESTRICTED.
Official manual describes farmers running 3Nodes that contribute compute, storage and network capacity to the ThreeFold Grid and receive rewards for available capacity and utilization. Nodes run Zero-OS on standard hardware and are described as mostly autonomous after setup. This is a dedicated-hardware provider model rather than an ordinary generic VPS bot. Remaining unknowns: exact current farmer reward formula, utilization, TFT liquidity, Azerbaijan onboarding, electricity/CAPEX economics.

## ParalonCloud GPU Provider
Status: VERIFIED/RESTRICTED.
Current 2026 official provider material describes a Docker-based NVIDIA GPU provider agent with automatic scheduling. Providers receive 80% of rental revenue; billing is per minute. Official material states payouts in USDC/USDT on Solana, no KYC and no minimum payout. Hardware ranges from consumer RTX cards to datacenter GPUs. Economics remain utilization-sensitive, so listed hourly rates are not expected profit.

Net model: provider share × paid utilization hours minus electricity, hardware depreciation, bandwidth, host/server cost, withdrawal/tax costs and maintenance.

## OpenGPU upgrade
Current official evidence strengthens the provider path: datacenters, cloud operators, GPU farms and home rigs are explicitly eligible; Linux provider software uses Docker Compose; workloads are automatically routed; providers earn OGPU for completed tasks; no token lockup is required simply to provide hardware. Current explorer evidence shows an active provider/task surface. Fiat-equivalent revenue per GPU-hour remains unresolved.

## Iagon deepening
Official current docs confirm 90% of monthly compute subscription fees go to compute node providers, weighted by performance/usage. Storage docs likewise allocate 90% of storage subscriber fees to storage nodes/delegators. Compute and storage roles require IAG staking, and current docs describe a three-month retirement/unbonding period. Therefore collateral opportunity cost must be included in ROI.

## DeNet deepening
Current official repository and July 2026 release confirm server/headless CLI and web-manager support, plus live Datakeeper software. Datakeepers provide storage to users and require a Datakeeper license. Current license price, payout/liquidity and realized utilization remain unresolved, so status stays VERIFIED/RESTRICTED.

## Saturation interpretation
Five differently-worded control passes have now produced zero new top-level mechanisms. Taxonomy confidence is high. However Run 022 still found two material live provider projects, so project-level saturation is not yet sufficient for COMPLETE.

## Next run
Run 023: tighter provider-tail convergence using current role vocabulary such as farmer, hoster, provider agent, provider docker, earn with GPU, capacity provider, cloud host rewards, storage node operator, render provider and inference provider. Focus on 2025–2026 provider guides/releases, fee splits, payout rails and deduplication against the existing catalog.

If Run 023 finds zero mechanisms and at most 0–2 weak/restricted new projects, perform one final short saturation check. If that final pass also yields no material novelty, mark COMPLETE.
