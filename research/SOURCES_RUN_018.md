# Sources — Run 018

Evidence date: 2026-08-15

Primary sources used for validation:

## IDLE Protocol
- https://earnidle.com/docs
  - Resource types: GPU, agent, API, PC, wallet, data.
  - Provider share: 85% of usage fees.
  - Settlement: USDC on Solana; $0.10 minimum payout.
  - Agent/API resources can be hosted externally and exposed through the gateway.
- https://earnidle.com/developers
  - Pay-per-request resource API; x402/USDC settlement; custom resource registration.

## NodeOps Network
- https://docs.nodeops.network/Get-Started/Cloud-Compute/Provide-Compute
  - Provider bond, current CU rewards, hardware/network requirements.
- https://docs.nodeops.network/Guides/Marketplace/Provide-Compute
  - Explicit VM support / VM reseller statement.
- https://docs.nodeops.network/Guides/Marketplace/Provide-Compute/provide-gcp-compute
  - Official GCP VM provider example.
- https://docs.nodeops.network/Get-Started/Cloud-Compute/Provide-Compute/register-to-provide
  - Live-on-mainnet provider registration and NODE bond.
- https://docs.nodeops.network/Reference/compute-requirements
  - CU definition and machine restrictions.
- https://docs.nodeops.network/Learn/Products/Cloud
  - Provider compensation from CU charges and marketplace participant roles.
- https://docs.nodeops.network/Guides/Marketplace/Configure-Compute/
  - Template marketplace; 20% workload-fee share during bootstrap phase.

## SubQuery
- https://subquery.network/doc/subquery_network/node_operators/rewards.html
  - Productive-work and network-inflation reward sources; 200,000 SQT minimum stake; slashing/reallocation risk.
- https://subquery.network/doc/subquery_network/introduction/reward-distribution.html
  - Productive work, stake rewards and consumer boosting.
- https://subquery.network/doc/subquery_network/node_operators/rpc_providers/connect-node.html
  - Existing RPC endpoint can be connected; endpoint need not be dedicated solely to SubQuery.
- https://subquery.network/doc/subquery_network/node_operators/rpc_providers/introduction.html
  - RPC provider role.
- https://subquery.network/doc/subquery_network/introduction/introduction.html
  - Consumer payments and Indexer/RPC provider roles.

## Diode
- https://diode.foundation/docs/diode_network.html
  - Relay nodes trade bandwidth for DIODE; Fleet Contract reward mechanism.
- https://network.docs.diode.io/docs/
  - Linux/VM node support, suggested system requirements, actual traffic/location affects rewards.
- https://network.docs.diode.io/docs/features/what-is-a-fleet-contract/
  - Fleet Contract staking and monthly reward basis.

## CESS
- https://doc.cess.network/cess-miners
  - Consensus, storage, CD2N and TEE node roles; retriever/cacher monetization.
- https://doc.cess.network/tokenomics/rewards
  - Storage challenge rewards; CD2N retrieval/caching reward formulas and release.
- https://doc.cess.network/cess-miners/storage-miner/running
  - Storage server requirements and operating path.
- https://doc.cess.network/tokenomics/staking
  - 2,000 CESS per TiB storage stake; 3,000,000 CESS validator threshold.

## Acurast
- https://docs.acurast.com/processors/become-compute-provider/
  - Smartphone compute-provider requirements and reward modes.
- https://docs.acurast.com/processors/rewards/
  - Base benchmark, staked-compute and execution bonus reward mechanics.
- https://docs.acurast.com/
  - Phone-powered TEE compute model; provider role and supported workload types.

## Existing lead / discovery
- https://runonflux.com/fluxnodes/
  - Current official FluxNodes provider/reward framing; already present in catalog.

Secondary discovery-only sources — not sufficient alone for VERIFIED status:
- https://depinhub.io/projects
- https://depinscan.io/

Discovery-only names from these directories are retained in Run 018 as UNVERIFIED until primary-source validation.
