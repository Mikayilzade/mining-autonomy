# Sources — Run 026

Evidence date: 2026-08-16.

Primary/official sources were prioritized. Older or state-ambiguous pages are explicitly treated as weaker evidence.

## The Graph
- Indexing overview: https://thegraph.com/docs/en/indexing/overview/
- Graph Horizon changes: https://thegraph.com/docs/en/graph-horizon/what-changes/
- GraphTally/TAP payment guide: https://thegraph.com/docs/en/indexing/tap/
- Explorer / network participant metrics: https://thegraph.com/docs/en/subgraphs/explorer/

Key evidence used:
- Indexers run nodes, index and serve queries.
- Current minimum self-stake stated as 100,000 GRT.
- Revenue = query fee rebates + indexing rewards.
- GRT stake can be slashed.
- Horizon/TAPv2 is current for gateway queries.

## SQD / Subsquid
- Current worker guide: https://docs.sqd.dev/en/network/worker
- Current network dashboard: https://tethys.subsquid.io/
- Network/reward design reference: https://github-wiki-see.page/m/subsquid/subsquid-network-contracts/wiki/Whitepaper

Key evidence used:
- Docker/source worker installation and continuous operation.
- 100,000 SQD registration bond.
- Withdrawal delay around 14 days plus epoch.
- Workers process queries/data and earn rewards linked to liveness, stake/delegation and traffic.
- Live dashboard exposes active workers, rewards, APR, query and data metrics.

## Boundless / RISC Zero
- What is Boundless: https://docs.boundless.network/developers/what
- Proof lifecycle: https://docs.boundless.network/developers/proof-lifecycle
- Prover quick start: https://docs.boundless.network/provers/quick-start
- Proving stack / Bento + Broker: https://docs.boundless.network/provers/proving-stack
- Broker config/operation: https://docs.boundless.network/provers/broker
- Proving collateral: https://docs.boundless.network/zkc/collateral
- ZK Mining overview: https://docs.boundless.network/zkc/mining/overview
- CLI/rewards tooling: https://docs.boundless.network/developers/tooling/cli
- Current contract deployments: https://docs.boundless.network/developers/smart-contracts/deployments

Key evidence used:
- Permissionless proving market between requesters and provers.
- Request locking/bidding, proof generation and fulfillment reward.
- Bento/Broker automated stack, multi-GPU/multi-machine support.
- Recommended baseline hardware around 16 CPU threads, 32 GB RAM, 200 GB SSD plus NVIDIA GPU configuration.
- ZKC collateral required for market locks; failed fulfillment can slash collateral.
- ZK Mining pays ZKC incentives for proving work but requires staked ZKC.

## Cysic
- Network overview: https://docs.cysic.xyz/
- Prover node tutorial: https://docs.cysic.xyz/tutorial-docs/how-to-run-a-prover-node
- Auction mechanism: https://docs.cysic.xyz/tec-docs/cysic-auction-mechanism
- Compute contributor overview: https://docs.cysic.xyz/cysic-network-overview/key-components-of-cysic-network

Key evidence used:
- Current mainnet prover setup script/path exists.
- Provers bid for tasks and can tune bid price.
- 1,000 CYS reserve required per prover worker in current tutorial.
- Prover/verifier task reward split and slashing formulas are documented.

## Succinct / SP1
- Official network repository: https://github.com/succinctlabs/network
- Official docs root: https://docs.succinct.xyz/
- Older platform docs: https://platform-docs.succinct.xyz/
- Network explorer FAQ: https://network.succinct.xyz/faq
- SP1 project template: https://github.com/succinctlabs/sp1-project-template

Interpretation:
- Strong evidence that the prover-network architecture and software exist.
- Public materials conflict in freshness/state; some pages still describe development or whitelisted access.
- No clean current 2026 public independent-prover admission proof established in this pass, so status remains WATCHLIST rather than VERIFIED.

## Gevulot
- Introduction/current network descriptions: https://docs.gevulot.com/gevulot-docs
- Network actors: https://docs.gevulot.com/gevulot-docs/zkcloud-design/provers
- Economics: https://docs.gevulot.com/gevulot-docs/zkcloud-design/fees
- Proving workload lifecycle: https://docs.gevulot.com/gevulot-docs/zkcloud-design/transactions
- Execution guarantees: https://docs.gevulot.com/gevulot-docs/zkcloud-design/execution-guarantees

Interpretation:
- Design docs clearly specify permissionless prover roles, stake, workload fees/rewards and verification rewards.
- But the introduction still characterizes permissionless ZkCloud as in development and Firestarter as production-ready but permissioned; roadmap language is stale.
- Therefore current public live paid admission is not proven and the project stays WATCHLIST.
