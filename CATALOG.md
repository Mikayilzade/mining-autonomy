# Opportunity Catalog

Status legend: `VERIFIED` = current primary source confirms earning/provider role; `UNVERIFIED` = discovery lead only; `RESTRICTED` = legitimate but key limitation already known; `REJECTED` = unsuitable/prohibited/non-paying; `WATCHLIST` = speculative or changing.

This is a living catalog. A name appearing here is **not** a profitability recommendation.

---

# A. Priority: server-native / online autonomous earning

## A1. General CPU / compute marketplaces
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Golem Network | VERIFIED | Yes | CPU/compute provider paid in GLM | Official docs explicitly allow laptop, desktop, or server machine; Linux provider daemon. Deep economics pending. |
| Akash Network Provider | VERIFIED | Yes | Lease compute through decentralized cloud marketplace | Provider runs Kubernetes infrastructure; operationally heavier than simple VPS bot. |
| Flux compute / FluxNode ecosystem | UNVERIFIED | TBD | Compute/node infrastructure | Validate current node economics and collateral requirements. |
| Clore.ai marketplace | UNVERIFIED | TBD | Compute/GPU rental | Validate current host rules and payouts. |
| Bacalhau / related compute markets | UNVERIFIED | TBD | Compute jobs | Determine whether providers currently earn market rewards. |

## A2. GPU / AI compute marketplaces
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Vast.ai Host | VERIFIED | Yes, especially owned/bare-metal | Rent GPU/CPU/storage/bandwidth | Host sets pricing; near-autonomous once configured but maintenance/reliability matters. |
| Nosana GPU Provider | VERIFIED | Likely dedicated machine/server | GPU job execution | Paid while GPU is used; hardware requirements apply. |
| Golem GPU Provider | VERIFIED | Dedicated compatible machine | GPU AI workloads paid in GLM | Current official GPU provider path exists; hardware-specific. |
| Render Network node/operator | UNVERIFIED | TBD | GPU rendering / compute | Validate current onboarding availability and rewards. |
| io.net supplier | UNVERIFIED | TBD | GPU compute | Validate supplier status, supported hardware, geography and collateral. |
| Aethir checker/container/provider roles | UNVERIFIED | TBD | GPU/cloud infrastructure | Validate which roles remain open and economics. |
| Hyperbolic provider | UNVERIFIED | TBD | GPU/AI compute | Discovery lead. |
| TensorDock host/provider | UNVERIFIED | TBD | GPU rental | Validate whether third-party hosting intake is open. |
| RunPod community cloud provider | UNVERIFIED | TBD | GPU rental | Validate current provider program. |
| Salad | VERIFIED | No ordinary server assumption yet | GPU/CPU/container jobs + bandwidth | Consumer-device oriented; research server eligibility separately. |

## A3. AI / algorithmic incentive networks
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Bittensor miners | VERIFIED | Often yes | Perform subnet-specific work; earn subnet emissions/stake | Not one generic bot: each subnet defines its commodity and scoring. Registration can cost capital. High-priority deep sweep of subnets required. |
| Bittensor validators | UNVERIFIED | Yes/TBD | Validate/rank subnet work | More capital/stake-heavy. Separate from miner opportunity. |
| Prime Intellect / decentralized training contributor roles | UNVERIFIED | TBD | AI training/compute/data | Determine whether permissionless providers currently earn. |
| Gensyn contributor/provider roles | UNVERIFIED | TBD | Distributed ML | Determine mainnet/reward reality vs testnet/speculation. |
| Ritual / inference node roles | UNVERIFIED | TBD | AI inference/network service | Validate current earning path. |
| Allora worker/reputer roles | UNVERIFIED | TBD | Predictions/inference | Validate current emissions and stake needs. |
| Morpheus compute/capital roles | UNVERIFIED | TBD | AI compute/services | Separate actual paid work from token incentives. |

## A4. Video / media transcoding infrastructure
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Livepeer Orchestrator | VERIFIED | Yes | ETH transcoding fees + LPT rewards | Requires stake/active-set economics; software alone does not guarantee work. |
| Theta Edge Node | UNVERIFIED | TBD | Edge compute/video/cache jobs | Validate server compatibility and actual payout modes. |
| AIOZ node | UNVERIFIED | TBD | Storage/bandwidth/transcoding/edge services | Validate current role and token rewards. |
| Media Network / similar CDN protocols | UNVERIFIED | TBD | CDN/media delivery | Ecosystem sweep needed. |

## A5. Decentralized storage
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Filecoin Storage Provider | VERIFIED | Yes | Storage service / proofs / deals | Current PDP warm-storage path marketed as lower hardware/collateral entry than historical sealing path. |
| Sia hostd | VERIFIED | Yes | Disk + bandwidth; paid in SC | Hosts set pricing and lock collateral; server/data-center participation explicitly supported. |
| Storj Storage Node | VERIFIED | Yes, incl. commercial data centers | Used disk capacity + bandwidth | Public nodes can monetize spare capacity; commercial provider option also exists. |
| Swarm Bee node | UNVERIFIED | TBD | Storage/bandwidth incentives | Validate stake, postage/reward model and realistic earnings. |
| Arweave mining/storage roles | UNVERIFIED | TBD | Storage/mining | Validate modern hardware and profitability. |
| Crust Network storage provider | UNVERIFIED | TBD | Storage | Validate current activity and rewards. |
| ScPrime storage provider | UNVERIFIED | TBD | Storage | Validate current health/economics. |
| Autonomi / MaidSafe-style storage nodes | UNVERIFIED | TBD | Storage/network contribution | Validate production rewards. |

## A6. Bandwidth / proxy / VPN / relay / CDN nodes
| Project | Status | Server-native? | What earns | Notes |
|---|---|---:|---|---|
| Mysterium Network node | UNVERIFIED | TBD | VPN/proxy traffic relay | Strong candidate for server-native relay; validate current node rules, abuse exposure and payouts. |
| NKN node | UNVERIFIED | TBD | Network relay / mining | Validate current reward economics and node requirements. |
| Meson Network node | UNVERIFIED | TBD | Bandwidth/CDN | Validate current provider onboarding. |
| Streamr node/operator | UNVERIFIED | TBD | Data relay/infrastructure | Validate current incentives. |
| PacketStream provider | UNVERIFIED | Probably residential-focused | Proxy bandwidth | Validate VPS/datacenter prohibition. |
| IPRoyal Pawns / Pawns.app bandwidth | UNVERIFIED | Probably residential-focused | Bandwidth sharing | Validate hosting/VPS policy. |
| EarnApp | RESTRICTED | **No** | Residential bandwidth/IP sharing | Official support explicitly prohibits VMs, Docker, hosting services, cloud hosting and servers used for monetization. Keep only Tier B. |
| Honeygain | VERIFIED for passive bandwidth; server status TBD | TBD | Unused internet traffic | Official site confirms passive sharing; need explicit VPS/datacenter policy before server classification. |
| Grass | UNVERIFIED | Probably residential/browser/device | Bandwidth/data contribution | Validate server/VM policy and current monetization path. |
| Nodepay | UNVERIFIED | TBD | Bandwidth/data contribution | Validate production rewards and device rules. |
| Dawn | UNVERIFIED | TBD | Bandwidth / decentralized broadband contribution | Validate rewards and automation restrictions. |
| Gradient Network | UNVERIFIED | TBD | Edge/bandwidth/compute | Validate current incentives. |

## A7. Blockchain service nodes: validators, RPC, indexing, relays
These are a **large family**, not automatically passive or low-capital. Each project will be split by required stake and whether revenue is customer fees, inflation, MEV, or subsidies.

Discovery leads:
- Ethereum validator / solo staking
- Solana validator
- Cosmos-SDK validators across chains
- Polkadot validators/nominators
- Avalanche validators
- Celestia validators
- Sui validators
- Aptos validators
- Near validators
- Cardano stake pools
- Tezos bakers
- Mina block producers
- Algorand consensus participation
- Pocket Network gateway/service nodes
- The Graph indexers
- Subsquid workers/indexers
- Chainlink node operators
- Pyth publisher roles
- API3 Airnode/provider roles
- EigenLayer operator/AVS ecosystem
- Symbiotic operator ecosystems
- Babylon staking/finality-provider ecosystems
- rollup sequencer/prover/operator opportunities
- Bitcoin Lightning routing nodes
- Bitcoin/crypto masternodes where still economically relevant

All currently `UNVERIFIED` for this project until individual economics and permissionless access are checked.

## A8. Search / crawling / indexing / data infrastructure
| Project/type | Status | What may earn | Notes |
|---|---|---|---|
| Presearch node | UNVERIFIED | Search node rewards | Validate current stake/reward requirements. |
| decentralized web-crawl/index networks | UNVERIFIED | Crawl/index/data service | Ecosystem sweep required. |
| decentralized oracle/data-feed node roles | UNVERIFIED | Data delivery fees/rewards | Often permissioned; filter permissionless opportunities. |
| public API data marketplace provider | UNVERIFIED | Sell data/API calls | May become build-once rather than pure mining. |

## A9. Proof generation / ZK / prover markets
Potentially ideal for autonomous servers because value is computational and programmatic.

Discovery leads (`UNVERIFIED` until checked):
- ZK proof marketplaces
- zkVM prover networks
- Succinct / SP1 prover-related networks
- RISC Zero / Boundless-style proving markets
- Gevulot
- Cysic
- Lagrange prover roles
- Scroll/Polygon/zkSync ecosystem prover markets
- rollup proof aggregation markets

Research questions: permissionless entry, hardware, bond/stake, task demand, current mainnet payouts, cloud-host restrictions.

## A10. Keeper / automation / solver / intent infrastructure
Potentially paid for continuous online service rather than raw resources.

Discovery leads:
- Gelato executors/automation infrastructure
- Chainlink Automation keeper roles
- CoW Protocol solvers
- intent/solver networks
- liquidation keeper bots where protocols explicitly permit it
- auction keepers
- oracle update keepers
- DeFi rebalancing executors

These require protocol-by-protocol review. Separate legitimate protocol service from harmful market manipulation or prohibited exploitation.

## A11. Crypto mining / proof-of-work
Server feasibility depends heavily on provider ToS and electricity/hardware economics.

Families:
- CPU-minable coins
- GPU-minable coins
- ASIC mining
- merge mining
- storage/proof-of-capacity mining
- mining pools
- auto-switching profitability miners
- bare-metal rented hardware mining where host explicitly permits it

Ordinary cloud VPS crypto mining is often economically bad and/or prohibited; never assume permission.

## A12. Legitimate automated jobs / machine-to-machine markets
Potentially closest to the user's original “bot does tiny jobs forever” idea, but requires very careful ToS validation.

Research families:
- APIs that pay providers per completed computational task
- data transformation jobs
- model inference job markets
- batch rendering markets
- transcoding markets
- web monitoring/data freshness jobs
- translation/transcription job APIs that explicitly allow automated suppliers
- synthetic-data generation markets
- benchmark/evaluation markets
- ML model competitions with repeatable machine scoring
- decentralized agent/task markets
- automated research/bounty markets with machine submissions explicitly allowed

Do **not** automate websites that contract for human-only microtasks unless their rules explicitly permit bots.

---

# B. Autonomous but home/residential/device based

## B1. Bandwidth/IP sharing
- EarnApp — `RESTRICTED`, confirmed residential/personal-device only for our purposes.
- Honeygain — `VERIFIED` as passive bandwidth sharing; server policy pending.
- Pawns.app — `UNVERIFIED` detailed rules pending.
- PacketStream — `UNVERIFIED`.
- Grass — `UNVERIFIED`.
- Nodepay — `UNVERIFIED`.
- Dawn — `UNVERIFIED`.
- Repocket — `UNVERIFIED`.
- Peer2Profit / successors — `UNVERIFIED`, current existence/safety check required.
- TraffMonetizer — `UNVERIFIED`.
- EarnFM — `UNVERIFIED`.
- ProxyRack/provider-style programs — `UNVERIFIED`.

## B2. Home GPU/CPU sharing
- Salad — `VERIFIED` for GPU/CPU/internet resource rewards, consumer-app model.
- Golem provider — may fit both server and home.
- GPU marketplaces above where consumer hardware accepted.
- traditional crypto mining if electricity economics work.

## B3. Spare storage
- Storj
- Sia
- Filecoin variants
- Swarm
- other decentralized-storage networks after validation.

## B4. Physical DePIN / sensor / wireless / mapping
Discovery universe:
- Helium hotspots / Mobile / IoT
- Hivemapper
- DIMO
- GEODNET
- WeatherXM
- Wingbits
- Silencio
- NATIX
- MapMetrics
- Nodle
- Roam
- WiFi/telecom DePIN networks
- environmental sensor networks
- energy/grid DePIN
- vehicle telemetry networks
- camera/mapping contribution

These require hardware/location/mobility and are secondary, but must be catalogued for completeness.

## B5. Phone/browser/device contribution
Families:
- background data contribution
- opt-in research panels
- telemetry/data marketplaces
- browser-extension DePIN
- passive measurement panels
- device uptime/reliability networks
- decentralized identity/reputation contribution

Must screen privacy implications and whether rewards are real cash/tokens vs points with no liquid value.

---

# C. Capital-based passive / semi-passive income
Not “free money”; capital is the supplied resource and can be lost.

## C1. Low-volatility traditional
- insured bank deposits / savings
- term deposits
- money-market funds
- Treasury bills / government bonds
- investment-grade bonds
- bond ETFs
- inflation-linked bonds
- certificates/deposit-like products where available

## C2. Market securities
- dividend equities
- broad index funds
- REITs
- infrastructure funds
- preferred shares
- covered-call funds
- royalty trusts
- business development companies

## C3. P2P/private credit
- P2P lending
- invoice financing
- marketplace lending
- real-estate debt crowdfunding
- revenue-based financing
- private-credit platforms

## C4. Crypto capital yield
- native PoS staking
- liquid staking
- restaking
- lending markets
- liquidity provision / AMMs
- stablecoin lending
- basis/funding-rate strategies
- delta-neutral yield strategies
- fixed-rate DeFi
- validator delegation
- protocol revenue sharing

Every one needs smart-contract, custody, depeg, liquidation, counterparty, token-price and regulatory risk treatment.

## C5. Automated trading / market infrastructure
Research-only until risk modeling:
- market making
- cross-exchange arbitrage
- triangular arbitrage
- funding-rate arbitrage
- cash-and-carry
- statistical arbitrage
- prediction-market arbitrage
- DEX/CEX spread capture

Not guaranteed passive income. Fees, latency, slippage, inventory risk and competition can erase edge.

---

# D. Build-once / automate-later digital income

## D1. Micro-SaaS / bots / APIs
- tiny paid API
- monitoring service
- conversion/transformation API
- scraping-as-a-service only for authorized/public data and compliant use
- alerts/notification bot
- scheduling bot
- document processing bot
- AI utility bot
- niche calculator
- data-cleaning service
- report generator
- webhook relay
- status/uptime service
- browser extension with legitimate paid utility

## D2. Content assets
- niche websites with ads
- affiliate sites
- programmatic SEO where content is genuinely useful and platform-compliant
- newsletters
- paid research databases
- automated price/comparison sites
- directories
- job boards
- lead directories with consent/compliance

## D3. Digital products / licensing
- ebooks
- templates
- spreadsheets
- code libraries
- plugins
- themes
- prompts/workflows where marketplaces permit
- datasets
- fonts/icons/graphics created/licensed legitimately
- stock photos/video/audio
- music/sound-effect licensing
- 3D models
- game assets
- educational courses
- printables

## D4. Automated commerce / fulfillment
- print-on-demand
- marketplace digital downloads
- licensed merch
- dropshipping with compliant sourcing/customer support
- subscription boxes with third-party fulfillment
- self-service software licenses

## D5. Royalties / IP
- book royalties
- music royalties
- photography/video licensing
- patent/license royalties
- software licensing
- game/app royalties
- revenue-share marketplaces

## D6. Asset rental
- websites/domains
- domain parking
- server capacity
- storage
- GPUs
- equipment
- vehicles/property/parking where applicable
- unused licenses/seats only if transfer/rental is contractually allowed

---

# E. Referrals / distribution / revenue share
- affiliate programs
- referral programs
- reseller programs
- white-label SaaS
- hosting reseller
- API reseller
- commission marketplaces
- creator referral revenue

Automation can support distribution, but spam/fake traffic/fake accounts are out of scope.

---

# F. Adjacent ideas to explicitly test and often reject

## F1. Non-paying volunteer compute
- BOINC projects
- Folding@home
- Tor relay
These may be useful technology analogues but normally do not directly pay. Check any third-party reward wrappers separately.

## F2. Faucets / ad-watching / click-to-earn
Usually human-presence or anti-bot systems, very low value, and automation often violates rules. Catalog only to prove why rejected unless an explicit machine API exists.

## F3. Airdrop/testnet farming
May reward genuine early participation, but not reliable income. Multi-account/Sybil farming or evasion is out of scope. One-account legitimate automation only if rules permit.

## F4. Human microtask sites
Mechanical Turk-like tasks, surveys, CAPTCHA solving, ad clicking, app installs, play-to-earn chores: automation is generally not assumed allowed. Search only for platforms that explicitly expose machine/provider APIs.

## F5. “Cloud mining” investment sites
Treat as high scam/counterparty-risk category. Separate genuine hardware contracts from Ponzi-like fixed-return schemes.

---

# First-stage verified facts
Current primary sources already establish these points:
1. **Golem**: provider software can run on a server machine and earns GLM for supplied compute.
2. **Akash**: providers offer compute resources and earn when deployments lease them.
3. **Vast.ai**: hosts sell GPU resources; platform supports host-controlled prices and automated resource management.
4. **Nosana**: GPU providers are paid for GPU use by clients.
5. **Bittensor**: miners perform subnet-defined work; rewards/emissions depend on subnet scoring and registration has costs/competition.
6. **Livepeer**: orchestrators can earn ETH service fees plus LPT rewards, but software alone does not guarantee work.
7. **Filecoin**: storage-provider path is active; modern PDP warm-storage onboarding reduces some historical entry barriers.
8. **Sia**: storage providers run `hostd`, supply disk/bandwidth, set prices and earn SC subject to contract/collateral behavior.
9. **Storj**: both public spare-capacity nodes and commercial storage providers can earn from used capacity/bandwidth.
10. **EarnApp**: ordinary VPS/VM/Docker/cloud/server monetization is explicitly prohibited; therefore it is not a server-mining candidate.
11. **Honeygain**: passive background bandwidth sharing is current; exact server/VPS permission remains to be verified before classification.
12. **Salad**: current consumer application can reward GPU, CPU and bandwidth sharing; job availability varies.

Next passes must transform the large `UNVERIFIED` universe into evidence-backed records and add projects not yet discovered.
