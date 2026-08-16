# Run 024 — Non-GPU Provider-Tail Convergence Pass

Evidence date: 2026-08-16

## Objective
Search the current non-GPU provider tail using storage-provider, host-node, capacity-marketplace, edge/CDN, bandwidth/relay, RPC supplier and generic provider vocabulary. Prefer current official docs/current repositories and distinguish production earning paths from whitelist/testnet/watchlist states.

## Result summary
- **New top-level economic mechanisms:** 0
- **Genuinely new provider projects/leads:** 9
- **Existing catalog leads materially upgraded/validated:** 3
- **Conclusion:** taxonomy remains saturated, but project-level tail is **still productive**. Do not mark COMPLETE.

The important pattern is unchanged: these projects monetize one of the already-known primitives — compute, storage, bandwidth/relay, RPC/API service, or staked infrastructure — but current provider software/onboarding makes several of them material implementation candidates.

---

## 1. NodeOps Cloud — VERIFIED / SERVER-NATIVE, capital-bonded

**Mechanism:** supply generic cloud capacity; workloads consume Compute Units and providers receive provider rewards / a share of paid CU consumption.

**Current evidence:** official docs expose an active `Provide Compute` path. Provider bond is **2,000 NODE + 200 NODE per CU**. One CU maps to 1 vCPU, 2 GB RAM, 30 GB NVMe in the Cloud documentation. Provider machines require at least 2 vCPU, 4 GB RAM, 80 GB NVMe, 1 Gbps unlimited networking, >=99% uptime, Debian 12+ or Ubuntu 22.04+, static public IPv4 and root-level integration. Current docs state each 2 CU can earn up to 10 NODE/day (8 base + up to 2 performance), while gNODE rewards convert to NODE with time-dependent redemption ratios.

**Server fit:** strong. Official GCP provider guide explicitly shows registering cloud VMs, so public-cloud re-rental is contemplated by the project itself. However cloud cost vs reward must be modeled before deployment.

**Automation:** 5/5 after provisioning; machine must remain dedicated and cannot run extra workloads.

**Capital / lock:** material NODE bond. Opportunity cost and token-price risk must be included.

**Payout/economics caveat:** published token reward rate is not proof of positive fiat net profit. Need live NODE price, redemption delay, utilization, bond cost and actual CU demand.

**Geography/KYC:** no Azerbaijan exclusion found in the reviewed provider docs, but this is not positive onboarding confirmation.

**Verdict:** material new server-native candidate; prioritize later pilot economics.

---

## 2. DeNet Datakeeper — VERIFIED / SERVER-NATIVE STORAGE

**Mechanism:** rent disk space to storage users and submit storage proofs; users pay for stored data and Datakeepers receive rewards.

**Current evidence:** official/current DeNetPRO node repository explicitly describes Datakeepers earning by providing storage. It provides CLI and Web Manager builds for Linux x86_64/ARM64 and explicitly calls the Web Manager/CLI suitable for **server environments, headless systems, Ubuntu Server and CentOS**. Latest indexed production release is Datakeeper Node **v4.1.0 dated 2026-07-21**, with active Proof-of-Storage fixes and server binaries.

**Server fit:** strong, including headless Linux server.

**Automation:** 5/5 daemon-style after setup; monitoring still required.

**Capital:** node license is part of onboarding; exact current license price/payment economics need a dedicated validation pass.

**Revenue driver:** actual user storage + successful proofs, not mere disk uptime.

**Risks:** storage commitment, protocol/license economics, token liquidity and potentially uneven utilization.

**Verdict:** material new storage-provider candidate, strong enough to keep project discovery open.

---

## 3. Iagon Storage Node — VERIFIED / SERVER-NATIVE STORAGE

**Mechanism:** commit storage and stake IAG; node operators receive **90% of storage-user subscription payments** based on performance plus additional IAG staking rewards.

**Current evidence:** official docs say anyone with a computer **or server** with excess storage and continuous availability may join. Minimum eligibility currently includes ~900 GB storage, 4 GB RAM, 20 Mbps upload/download, 20 Mbps read/write and 90% uptime. CLI supports remote/SSH-style operation. Registration requires Cardano wallet connection and staking IAG. Node retirement/unstake period is 3 months. The 2026 tier system ranks providers by throughput, I/O and uptime, and low-performing/flagged nodes receive no rewards.

**Server fit:** yes, explicit server language and CLI remote operation.

**Automation:** 4–5/5 after registration.

**Capital:** IAG stake required; exact stake per committed TB should be normalized in a deeper economics run.

**Revenue quality:** unusually useful because docs link 90% of customer subscription payments to node operators rather than describing only emissions.

**Risks:** token stake, 3-month retirement, performance-tier dilution, storage utilization and token liquidity.

**Verdict:** material new provider project.

---

## 4. Edge Network Host — VERIFIED / EDGE COMPUTE+STORAGE+CDN

**Mechanism:** Host nodes supply processing/storage capacity and participate in CDN/edge workloads; nodes earn network yield/rewards tied to contribution and demand.

**Current evidence:** current Edge site says node operators contribute bandwidth, compute or storage and earn EDGE rewards. Community onboarding docs say **Host onboarding is open** and Host software runs in background and self-updates. Host minimums are low (quad-core class CPU, 1 GB RAM, 50 GB disk, 15 Mbps+ bandwidth, >=20% availability); higher Gateway/Stargate tiers are more data-center-like but community onboarding for those roles is not currently open. Host setup requires a stake; current wiki lists 100 XE for Host and warns stake/yield parameters can change.

**Server fit:** likely yes for Host; Linux/server-style deployment is technically compatible, though the project also targets spare devices. Do not assume every VPS provider permits nested/container workloads.

**Automation:** 5/5 once node is running; official docs explicitly state background operation and auto-updates.

**Capital:** stake required; penalties may apply when availability targets are missed.

**Revenue caveat:** advertised expected-yield figures are protocol targets/estimates, not guaranteed customer-paid cashflow.

**Verdict:** material new non-GPU edge-provider candidate.

---

## 5. Anyone Network Relay — VERIFIED / BANDWIDTH+PRIVACY RELAY, stake-locked

**Mechanism:** run privacy-network relay; rewards depend on relay contribution, uptime/type/geolocation and reward multipliers, with future/ongoing premium-circuit revenue intended to connect high-demand relays to paid users.

**Current evidence:** official docs provide Relay setup specifically to earn rewards for bandwidth/encrypted traffic contribution. Non-hardware relays currently require a **100 ANYONE token lock**, minimum 180-day lock plus 14-day unstaking period. Reward docs also incorporate uptime/quality and relay-family/geolocation adjustments.

**Server fit:** technically strong for Linux relay deployment, but exact datacenter/VPS desirability and geolocation scoring should be tested before assuming favorable economics.

**Automation:** 5/5 daemon/relay.

**Capital:** token lock, with liquidity/opportunity cost.

**Risks:** abuse/exit-traffic exposure must be understood operationally; relay family/geolocation multipliers can materially change economics.

**Verdict:** material new relay candidate.

---

## 6. Marlin Relay Cluster Operator — VERIFIED / SERVER-NATIVE RELAY, staked

**Mechanism:** relay blockchain blocks/transactions; fees are sourced from receiver subscription fees and distributed according to work/tickets, with network rewards supplementing fees during bootstrapping.

**Current evidence:** official docs actively describe running Relay clusters. Cluster operators run beacon, monitoring and relay components. Current staking docs require **minimum delegation of 0.5 MPond** for a cluster to operate, with staking contracts on Arbitrum.

**Server fit:** yes, infrastructure/operator role rather than residential-sharing model.

**Automation:** 4–5/5, but multi-component cluster operations and availability monitoring raise maintenance burden.

**Capital:** 0.5 MPond minimum delegation plus server costs.

**Revenue quality:** better than pure emission-only leads because docs explicitly describe receiver subscription fees paying relayers, though actual traffic/utilization remains the hidden variable.

**Verdict:** material new server relay project.

---

## 7. EthStorage Storage Provider — RESTRICTED / MAINNET WHITELIST

**Mechanism:** store blob data, submit proof-of-replication over time and receive storage rewards/fees from storage contracts.

**Current evidence:** official Storage Provider Guide describes mainnet storage-provider mining and rewards. **Initial mainnet earning is currently whitelist-limited**; non-whitelisted operators can run a mainnet storage node but must disable mining until whitelisted or the restriction is lifted.

**Server fit:** yes in architecture, but permission to earn is currently gated.

**Automation:** 5/5 after setup if/when mining enabled.

**Capital/requirements:** hardware/storage and likely chain gas; exact current provider economics need further validation.

**Verdict:** new restricted watchlist candidate, not deployable permissionlessly today.

---

## 8. DCDN Cloud Node Operator — WATCHLIST / NEEDS TRUST VALIDATION

**Mechanism:** CDN/WAF/bandwidth plus VPS hosting. Current operator dashboard claims node operators receive **70% of revenue**, with published activity rates and monthly token payouts.

**Current evidence:** current public node dashboard exposes registration, per-node earnings, rates for bandwidth/requests/WAF, a 70/25/5 VPS/CDN revenue split and Linux node troubleshooting details.

**Why not VERIFIED:** evidence is concentrated in one project-controlled dashboard and there is insufficient independent/current protocol/repository history in this pass. Treat economics and token liquidity as unverified until contracts, operator software, network usage and real withdrawals are confirmed.

**Server fit:** apparently yes; operator troubleshooting references Linux binaries and >99.9% uptime.

**Verdict:** genuinely new but weak/watchlist.

---

## 9. ARO Network ARO Server — WATCHLIST / TESTNET-SENSITIVE

**Mechanism:** contribute IP, bandwidth and hardware resources through Desktop/Mobile/Pod/**Server** node forms.

**Current evidence:** official docs say the network is permissionless, offers an ARO Server node type and rewards contribution; however the same docs distinguish token incentives for mainnet from Jade points during testnet.

**Server fit:** explicit Server node exists.

**Why watchlist:** current reward state/mainnet settlement needs separate confirmation before treating this as realized income.

**Verdict:** new watchlist lead, not yet a high-confidence income candidate.

---

# Existing catalog entries materially upgraded

## Pocket Network Provider / Supplier — upgrade to VERIFIED
Official 2026 docs now provide a concrete permissionless supplier path: stake POKT, expose one or more JSON-RPC/REST/WebSocket service endpoints, run RelayMiner, serve relays and earn POKT according to proven Compute Units. Docs explicitly state anyone globally can become a Supplier without application/approval/geographic restriction, subject to stake and reliable infrastructure. Earnings are usage-based rather than fixed APR. This is a strong server-native RPC/API-service candidate.

## Swarm Bee — upgrade from UNVERIFIED to VERIFIED mechanism
Current official incentives docs explicitly state node operators are compensated for **storage** and **bandwidth relay** contributions through storage and bandwidth incentive mechanisms. A later economics pass should still normalize stake, neighborhood competition and actual win probability.

## SSV Network Operator — add/validate within validator-service family
Current operator docs (updated 2026-06-09) describe operators running SSV Node infrastructure and earning **fees from validators/Stakers**. This is not a new mechanism; it is a concrete fee-earning infrastructure implementation inside the already-known staked validator/operator family. It should be included in future ranked server-native candidates, with hardware, operator fee competition and ETH/SSV capital exposure normalized.

---

# Cross-project economics normalization

| Project | Paid resource | Server native | Capital lock/stake | Automation | Main gating variable |
|---|---|---:|---|---:|---|
| NodeOps | CPU/RAM/NVMe cloud CU | Yes | High NODE bond | 5 | reward value vs cloud cost + demand |
| DeNet | storage | Yes | license / protocol requirements | 5 | real stored-user data + license economics |
| Iagon | storage | Yes | IAG stake | 4–5 | tier score + utilization + stake cost |
| Edge Host | compute/storage/bandwidth | Likely | XE stake | 5 | workload demand + token yield |
| Anyone Relay | bandwidth/relay | Yes | 100 ANYONE lock | 5 | traffic/geography/quality multipliers |
| Marlin Relay | blockchain relay | Yes | >=0.5 MPond delegation | 4–5 | receiver traffic/subscription fees |
| EthStorage | storage | Yes | TBD + whitelist | 5 | whitelist + actual storage demand |
| DCDN | bandwidth/CDN/VPS | Yes claimed | TBD | 5 claimed | project credibility + real demand |
| ARO Server | bandwidth/IP/hardware | Yes claimed | TBD | 5 | mainnet cash/token reward state |
| Pocket Supplier | RPC/API relay | Yes | POKT stake | 5 | real relay volume / service competition |
| Swarm | storage+relay | Yes | protocol stake/economics | 5 | neighborhood competition + paid usage |
| SSV Operator | validator service | Yes | operator infra; customer stake external | 4–5 | validator customers + operator fee competition |

## Durable inference
The non-GPU tail strongly reinforces the project thesis: the closest legitimate version of “bots mining simple online tasks” is usually **a continuously running provider daemon that sells a machine-readable resource** (RPCs, storage, relay bandwidth, CPU/RAM capacity, validator duties) rather than a bot automating human microtasks.

The best candidates increasingly have all four features:
1. daemon/API-native provider software;
2. explicit customer-paid or usage-linked revenue;
3. permissionless or open onboarding;
4. no requirement to impersonate a human/residential user.

---

# Saturation decision
Run 024 again produced **0 new economic mechanisms**, so taxonomy convergence is extremely strong. But it found **multiple material current provider projects** (NodeOps, DeNet, Iagon, Edge, Anyone, Marlin) plus restricted/watchlist projects and upgraded Pocket/Swarm/SSV evidence.

Therefore the completion gate is **not met**. Project-level discovery is still too productive.

## Next run
Run 025 should target the remaining non-GPU infrastructure/provider tail with project-name and vocabulary families that this run only partially covered:
- RPC gateway/provider / decentralized API supplier
- validator-as-a-service operator marketplaces
- edge host / CDN cache operator
- decentralized web hosting node
- CPU-only marketplace/provider
- proof/prover markets that accept commodity CPU
- data availability / archival node earning roles
- “operator fee”, “supplier revenue”, “host reward”, “provider marketplace” vocabulary

Prioritize current 2025–2026 official docs/repos and explicitly search for live provider onboarding. Dedupe against all Run 024 projects before counting novelty.
