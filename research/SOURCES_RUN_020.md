# Sources — Run 020 provider/repository & tokenomics control pass

Evidence date: **2026-08-16**.

Primary/current sources used in this run. Search-result snippets are treated only as discovery; classification below relies on the linked official/project sources or official repositories.

## dTelecom
- Official site: https://www.dtelecom.org/
  - Current page explicitly says Node Operators can run nodes and earn **75% of customer payments**.
- Official docs — Getting Started: https://docs.dtelecom.org/guides/getting-started
  - Current SDK uses Solana mainnet registry for discovery of decentralized SFU nodes.
- Official docs — Architecture: https://docs.dtelecom.org/guides/architecture
  - Confirms independent SFU node network registered/discovered on Solana.
- Official x402 gateway: https://x402.dtelecom.org/
  - Current customer-side prices include WebRTC/STT/TTS and crypto-native payments.

## Edge Network / XE
- Official site: https://edge.network/
- Current official About page: https://edge.network/about
  - Run a node, contribute bandwidth/compute/storage, earn $EDGE; rewards scale with demand/usage.
- Current Edge Community Wiki — host setup: https://wiki.edge.network/contributing-to-the-network/edge-cli/set-up-a-host/
  - Mainnet CLI, Linux/Docker host setup, wallet/stake/start-node workflow.
- Current Edge Community Wiki — staking: https://wiki.edge.network/contributing-to-the-network/an-introduction-to-staking
  - Community Host onboarding currently available; Host stake listed at 100 XE; penalties for availability failures.
- Current Edge Community Wiki — expected yields: https://wiki.edge.network/contributing-to-the-network/expected-yields/
  - Explains relative yield model; not treated as guaranteed profit.
- Current Edge Community Wiki — token distribution/node rewards: https://wiki.edge.network/getting-started/edge-tokenomics/xe-distribution/
  - Node-reward pool/emissions documented through 2026/27.

## StorX
- Official host-node page: https://storx.tech/host-node.html
  - Farm/storage node hardware, bandwidth and staking requirements; SRX rewards tied to reputation.
- Official storage-node onboarding page: https://storx.tech/storx-website-host-storage-node.html
  - Explicit VPS/server setup path, SRX staking, reputation and continuous reward framing.

## Impossible Cloud Network (ICN)
- Official docs — Hardware Providers: https://docs.icn.global/icn-economics/hardware-providers-hps
  - HPs provide storage/compute, earn ICNT; utilization + capacity rewards; collateral/slashing.
- Official docs — Become a Hardware Provider: https://docs.icn.global/icn-participation/contribute-hardware
  - Current onboarding is **contact/verification based**, not fully permissionless self-service.
- Official docs — HP rewards: https://docs.icn.global/icn-economics/hardware-providers-hps/hp-rewards
  - Utilization rewards + temporary capacity subsidy; payout delay and slashing.
- Official docs — collateral: https://docs.icn.global/icn-economics/hardware-providers-hps/collateral
  - Node and network collateral; HP commitment initially 36 months; undercollateralization/diversion rules.
- Official docs — services/apps: https://docs.icn.global/network-architecture/services-and-apps
  - Current protocol capacity booking; currently one storage hardware class is available.

## YOM
- Official operator page: https://yom.net/operators/
  - Current NANO self-host route; gaming-PC GPU sessions; license model; earnings depend on regional demand/utilization. NaaS advertised for Q3 2026.
- Official FAQ: https://yom.net/docs/about/faq
  - Current hardware/license cost framing and utilization-dependent earnings.
- Official payout docs: https://yom.net/docs/solution/payout/
  - Session-based fee tiers; 40/55/5 operator/foundation/burn split; Avalanche settlement.
- Official NaaS delegation docs: https://yom.net/docs/earn/naas-delegation/
  - Delegation not yet active; targeted Q2–Q3 2026.
- Official how-it-works docs: https://yom.net/docs/solution/how-it-works
  - Node runs through NANO secure-boot device; settlement is per served session.

## iExec
- Official PoCo repository: https://github.com/iExecBlockchainComputing/PoCo
  - Current protocol repository; latest surfaced release v6.2.0 dated 2026-01-21; worker contribution/reward/stake primitives remain live at protocol level.
- Current public docs/repository search did **not** establish a simple self-service 2026 worker/workerpool supplier onboarding path suitable for an ordinary VPS. Keep restricted rather than inferring deployability from contracts alone.

## Fleek Network
- Official docs — services: https://docs.fleek.network/docs/learn/services
  - Rewards based on measured bandwidth/compute commodities and Delivery Acknowledgements.
- Official docs — node health: https://docs.fleek.network/docs/node/health-check/
  - Node is expected to be staked; operator health affects rewards.
- Official docs landing/current surfaced copy still labels participation as alpha/testnet: https://docs.fleek.network/docs
- Official tokenomics/testnet article: https://blog.fleek.network/post/fleek-network-testnet-plans/
  - Explicitly preliminary/pre-mainnet. Therefore 2026 production/liquid payout status remains unresolved in this run.

## Fluence
- Official Fluence tokenomics article: https://cloudways-wp-blog.fluence.dev/blog/fluence-tokenomics-explained-flt-token-supply-use-governance/
  - Compute providers contribute CPU and receive FLT rewards; stake required per CPU; slashing concept documented.
- Current searches failed to surface a sufficiently current 2026 self-service provider onboarding/economics document. Keep WATCHLIST/RESTRICTED pending direct provider-console/repository evidence.

## Spheron
- Official docs — Marketplace consumer deployment: https://docs.spheron.network/rent-gpu/deploy-container/with-console
  - Confirms Community GPUs exist as supply, but this run still did not find current public self-service supplier onboarding/reward docs. Keep RESTRICTED.

## Evidence discipline
- Marketing earnings figures from YOM/Edge/StorX are not treated as guaranteed profitability.
- Token rewards are valued only after liquidity/withdrawal and geography checks.
- A protocol contract/repository proves mechanism existence, not public supplier admission.
- Contact-based supplier onboarding is classified as RESTRICTED even when economically real.
