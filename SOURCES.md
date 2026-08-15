# Evidence / Source Register

Use this file for source-level facts. Prefer official/primary sources and date every validation pass.

Validation date for entries below: **2026-08-15**.

## Compute / GPU / AI

### Golem Network — provider
- Official docs: https://docs.golem.network/docs/providers
- Official install guide: https://docs.golem.network/docs/providers/provider-installation
- GPU provider guide: https://docs.golem.network/docs/providers/gpu/gpu-golem-live
- Established: provider supplies compute and receives GLM; general provider docs explicitly say a provider can be laptop, desktop, or server machine; Linux provider daemon exists; GPU path exists with hardware requirements.

### Akash Network — provider
- Official provider page: https://akash.network/providers/
- Established: compute providers offer resources on Akash marketplace and earn when deployments lease them; provider deployment is Kubernetes/cluster-oriented rather than a trivial consumer app.

### Vast.ai — host
- Official hosting docs: https://docs.vast.ai/host/hosting-overview
- Official host payout docs: https://docs.vast.ai/host/payment
- Official hosting page: https://console.vast.ai/hosting/
- Established: hosts sell GPU resources, set pricing/contract terms, and can also expose storage/bandwidth; platform automates parts of workload/resource management. Hosting requires reliable Linux server administration.

### Nosana — GPU provider
- Official provider page: https://www.nosana.com/gpu-providers/
- Established: provider installs a node, verifies hardware and is paid for GPU utilization by Nosana clients; hardware/network requirements apply.

### Bittensor — miner
- Official mining docs: https://www.bittensor.com/docs/guides/mining
- Established: miner registers on a subnet and performs work defined by that subnet's incentive mechanism; rewards/emissions depend on validators/subnet scoring; registration can have burn/collateral costs; mining is competitive and not one generic passive workload.

### Livepeer — orchestrator
- Official operator rationale: https://docs.livepeer.org/v2/orchestrators/guides/operator-considerations/operator-rationale
- Getting started: https://docs.livepeer.org/v1/orchestrators/guides/get-started
- Established: orchestrators have ETH service-fee and LPT reward streams; simply running software does not guarantee service revenue; stake and active-set constraints matter.

### Salad — consumer compute/bandwidth
- Official support: https://support.salad.com/
- Earnings explanation: https://support.salad.com/faq/jobs/how-much-can-i-earn-with-salad/
- Established: current app can earn from GPU, CPU and internet bandwidth workloads; job demand and earnings fluctuate. Server/datacenter eligibility requires separate validation.

## Storage

### Filecoin — storage provider
- Official provider page: https://www.filecoin.io/provide-storage
- Established: active storage-provider role; current PDP warm-storage route is presented as lower-hardware-cost and without long-term collateral compared with older sealing-heavy onboarding. Detailed economics still pending.

### Sia — storage provider / hostd
- Official provider docs: https://devs.sia.storage/docs/core-concepts/storage-providers
- Official hosting page: https://sia.tech/provide-storage
- Established: provider runs `hostd`, supplies disk and bandwidth, sets prices, accepts contracts and earns SC; collateral/proof failure risk exists; individuals, home servers and data centers can participate.

### Storj — storage node/provider
- Official provider page: https://www.storj.io/partner/storage-providers
- Capacity article: https://www.storj.io/blog/put-your-spare-capacity-to-work
- Established: public nodes monetize spare disk and bandwidth; commercial data-center provider path also exists; uptime/bandwidth/storage requirements matter.

## Bandwidth / residential-resource programs

### EarnApp
- Official rate article: https://help.earnapp.com/hc/en-us/articles/38191916327441
- Official VM/hosting restriction: https://help.earnapp.com/hc/en-us/articles/10199416541969--Can-I-install-EarnApp-on-Hosting-Services-Virtual-Machines-or-Dockers
- Established: background bandwidth/IP monetization is active; official support explicitly prohibits VM, Docker, hosting services, cloud hosting and servers used for monetization. Therefore classify as residential/personal-device only for this project, not VPS mining.

### Honeygain
- Official passive bandwidth page: https://www.honeygain.com/sell-internet-data/
- Official app page: https://www.honeygain.com/sell-internet-data/app/
- Official support on traffic demand: https://support.honeygain.com/hc/en-us/articles/360013095720-Does-doing-other-network-activities-influence-my-earnings
- Established: passive unused-bandwidth sharing remains active; earnings depend on regional demand and network/device factors. Exact VPS/datacenter permission not yet established by this research pass.

## Discovery directories / secondary maps

### CIJSS DePIN catalog
- https://cijss.org/depin/catalog
- Use: discovery lead only, not final proof. Current catalog surfaces categories/projects such as Bittensor, Render, Filecoin, Grass, The Graph and Akash. Every candidate found there must be validated against official docs.

## Source discipline
- Do not infer server eligibility from Linux support alone.
- Do not infer profitability from “earn” marketing text alone.
- Do not infer liquid value from points/rewards unless payout/token liquidity is verified.
- ToS restrictions override technical ability.
- Community earnings screenshots are leads, not proof.
