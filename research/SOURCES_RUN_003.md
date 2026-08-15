# Sources — Run 003

Evidence date: 2026-08-15

Primary sources only unless explicitly marked otherwise.

## Lava Network
- Provider overview: https://docs.lavanet.xyz/provider/
- Provider setup/staking: https://docs.lavanet.xyz/provider-setup/
- Provider rewards: https://docs.lavanet.xyz/provider-rewards-service/
- Provider FAQ / unbonding / participation: https://docs.lavanet.xyz/provider-faq/
- Mainnet API/reward query surface: https://docs.lavanet.xyz/api-methods/lava/

Validated facts used:
- RPC providers stake per supported service/chain and serve relays.
- Relay proofs, QoS/reputation and jail state affect rewards.
- Providers/restakers receive 95% of specified subscription/public-RPC-pool rewards according to documented allocation rules.
- Asia is an explicit provider geolocation class.
- Provider unbonding is documented as 21 days.

## Boundless / RISC Zero
- What is Boundless: https://docs.boundless.network/developers/what
- Proof lifecycle / market payout: https://docs.boundless.network/developers/proof-lifecycle
- Prover quick start / hardware: https://docs.boundless.network/provers/quick-start
- Proving stack: https://docs.boundless.network/provers/proving-stack
- ZK mining overview: https://docs.boundless.network/zkc/mining/overview
- Enable ZK mining: https://docs.boundless.network/zkc/mining/enable
- Boundless CLI/rewards commands: https://docs.boundless.network/developers/tooling/cli
- Mainnet deployments: https://docs.boundless.network/developers/smart-contracts/deployments

Validated facts used:
- Requestors submit proof requests, provers compete and successful proof settlement releases reward.
- PoVW/ZK Mining pays ZKC for proving work.
- Official docs explicitly describe deployment to a GPU server.
- Recommended minimum includes 16 CPU threads, 32 GB RAM and 200 GB SSD plus supported NVIDIA GPU setup.
- Bento supports single-GPU through cluster-scale proving.
- Collateral/staking mechanics exist and must be included in ROI.

## Succinct / SP1
- Current docs landing page: https://docs.succinct.xyz/

Validated only:
- Succinct currently advertises SP1 plus a decentralized prover network and a mainnet explorer.

Not yet validated:
- permissionless prover admission;
- current reward/collateral formula;
- hardware/economic requirements.

## SQD / Subsquid
- Current docs: https://docs.sqd.ai/
- Example indexer launch material: https://docs.sqd.ai/solana-indexing/how-to-start/cli-cheatsheet/
- Older testnet quest rules surfaced during discovery: https://docs.sqd.ai/network-launch-quests-rules/

Validated only:
- SQD provides decentralized/indexing infrastructure and indexer software.
- The surfaced explicit reward material was testnet-era and is insufficient to prove a current open mainnet paid worker role.

## Chainlink
- Official FAQ / node operators / economics: https://chain.link/faqs
- Ecosystem / monetize API / node operator: https://chain.link/ecosystem
- Current operator-context article: https://chain.link/article/operator
- Chainlink staking economics: https://chain.link/economics/staking
- Current staking operator page: https://staking.chain.link/
- Historical Oracle Olympics onboarding example: https://chain.link/oracle-olympics

Validated facts used:
- Node operators can earn revenue providing oracle infrastructure; APIs/data can be monetized.
- Anyone can technically run a Chainlink node/framework, but major production networks emphasize professional known operators and strong operational standards.
- Node Operator Stakers have a separate staking category from Community Stakers.

Caution:
- Do not infer automatic paid-job admission merely from being able to run node software.

## Gelato
- Node fee mechanism / pricing: https://docs.gelato.cloud/vrf/additional-resources/pricing-and-rate-limits
- Turbo Relayer overview: https://docs.gelato.cloud/gasless-with-relay/gelato-turbo-relayer/overview
- Verifier Node Package: https://docs.gelato.cloud/developer-services/customization/verifier-node-package
- Example OP node deployment: https://docs.gelato.cloud/rollup-as-a-service/how-to-guides/run-an-op-node
- Example Orbit node deployment: https://docs.gelato.cloud/rollup-as-a-service/how-to-guides/run-an-orbit-node

Validated facts used:
- Gelato Nodes charge fees for transaction/off-chain execution services.
- Gelato offers verifier-node infrastructure where projects can require node licenses and distribute rewards.

Not yet validated:
- whether arbitrary external operators can permissionlessly join Gelato core executor supply and earn fees.

## CoW Protocol
- Current official docs landing page: https://docs.cow.fi/

Validated only:
- CoW Protocol uses fair combinatorial batch auctions and a solver-based architecture is part of the mechanism.

Still required:
- current solver onboarding;
- bonding/collateral;
- reward/fee schedule;
- admission restrictions.

## Streamr
- Become an Operator: https://docs.streamr.network/guides/become-an-operator
- Operator role: https://docs.streamr.network/streamr-network/network-roles/operators/
- How to stake and earn: https://docs.streamr.network/guides/how-to-stake-and-earn/
- Run a Streamr node / hardware: https://docs.streamr.network/guides/how-to-run-streamr-node/
- Incentives: https://docs.streamr.network/incentives/
- Network tokenomics: https://docs.streamr.network/streamr-network/incentives/network-incentives/
- Node inspection / automated reviews: https://docs.streamr.network/streamr-network/incentives/node-inspection/
- Operator FAQ: https://docs.streamr.network/help/operator-faq/

Validated facts used:
- Operators run nodes, stake DATA on funded Sponsorships and earn DATA for relaying streams.
- Operator must self-own at least 5% of Operator stake.
- Node wallet needs POL for transactions.
- Node software handles recurring maintenance and automated inspections/reviews.
- Hardware guidance is approximately 4–8 GB RAM, 3–4 virtual cores, ideally 1 Gbps bandwidth, public IP/open port.
- Stake is slashable for protocol failures/misbehavior.

## Source-quality note
The discovery search engine occasionally returned old testnet pages before current network/operator docs. Run classifications therefore deliberately distinguish CURRENT PRIMARY EVIDENCE from historical/testnet leads. No profitability claim in Run 003 is based solely on token marketing or community anecdotes.
