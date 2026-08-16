# Sources — Run 027

Evidence date: 2026-08-16

Primary/current sources used in Run 027.

## Space and Time (SXT Chain)
- Node Types — https://docs.spaceandtime.io/docs/node-types
- Running a Validator Node — https://docs.spaceandtime.io/docs/running-a-validator-node
- Stake SXT — https://docs.spaceandtime.io/docs/stake-sxt
- Delegated Staking — https://docs.spaceandtime.io/docs/delegated-staking
- What is Space and Time? — https://docs.spaceandtime.io/docs/what-is-space-and-time-quick-intro
- Chain Security and Commitments — https://docs.spaceandtime.io/docs/chain-security-and-commitments
- Inserting Verified Data — https://docs.spaceandtime.io/docs/inserting-verified-data
- Overview / SXT Chain architecture — https://docs.spaceandtime.io/docs/overview-1

Key evidence captured:
- permissionless BFT chain with Validator, Indexer and Prover roles;
- public mainnet validator workflow and hardware requirements;
- validator rewards from insertion gas, query fees, subsidies and delegated stake;
- Proof-of-SQL prover race through ZKpay described as open to anyone running the prover repository;
- GPU-based ZK query proving;
- slashing risk for validators;
- indexer public-mainnet onboarding remains less clearly current than validator/prover paths.

## Succinct / SP1
- Succinct Prover Network mainnet announcement — https://blog.succinct.foundation/mainnet/
- Succinct Prover Network repository — https://github.com/succinctlabs/network
- Current Succinct docs root — https://docs.succinct.xyz/
- Succinct Foundation docs — https://docs.succinct.foundation/

Key evidence captured:
- mainnet launched 2025-08-05;
- two-sided prover/requester marketplace;
- PROVE token and staking mechanisms;
- public reference prover and `spn-node` with bidding/proving implementation;
- exact permissionless production-prover admission still not sufficiently explicit in reviewed public docs.

## Gevulot / ZkCloud
- Introduction — https://docs.gevulot.com/gevulot-docs
- Network Actors — https://docs.gevulot.com/gevulot-docs/zkcloud-design/provers
- Prover/Verifier Programs — https://docs.gevulot.com/gevulot-docs/zkcloud-design/programs
- Proving Workloads — https://docs.gevulot.com/gevulot-docs/zkcloud-design/transactions
- Economics — https://docs.gevulot.com/gevulot-docs/zkcloud-design/fees
- Execution Guarantees — https://docs.gevulot.com/gevulot-docs/zkcloud-design/execution-guarantees
- Firestarter Overview — https://docs.gevulot.com/gevulot-docs/firestarter/overview

Key evidence captured:
- permissionless prover/validator design;
- CPU and GPU workload support via declared resource requirements;
- explicit workload fees and prover rewards;
- Firestarter production-ready but permissioned;
- ZkCloud introduction still says in development, so current paid public deployment remains unproven.

## Cysic
- Network Overview — https://docs.cysic.xyz/
- Key Components — https://docs.cysic.xyz/cysic-network-overview/key-components-of-cysic-network
- What is ComputeFi — https://docs.cysic.xyz/cysic-network-overview/what-is-computefi
- How to Run a Prover Node — https://docs.cysic.xyz/tutorial-docs/how-to-run-a-prover-node
- Auction Mechanism — https://docs.cysic.xyz/tec-docs/cysic-auction-mechanism
- Service Products — https://docs.cysic.xyz/readme
- ZK ASIC Products — https://docs.cysic.xyz/hardware-products/zk-asic-products

Key evidence captured:
- open compute-contributor role spanning prover/verifier and multiple hardware classes;
- task bidding / winning providers / verifier validation / rewards;
- current mainnet prover setup and 1,000 CYS reserve per worker;
- future/2026 hardware claims separated from currently deployable software paths.

## Avail
- Operate — https://docs.availproject.org/docs/da/operate
- Node Types — https://docs.availproject.org/docs/da/operate/node-types
- Light Client — https://docs.availproject.org/docs/da/operate/run-a-light-client
- Light Client overview — https://docs.availproject.org/docs/da/operate/run-a-light-client/overview
- Light Client Lift-off challenge — https://docs.availproject.org/docs/da/operate/run-a-light-client/light-client-challenge

Key evidence captured:
- light/full/RPC/validator roles are current;
- validators explicitly earn staking rewards;
- old light-client reward challenge is ended/deprecated;
- no current direct reward evidence found for ordinary light/full/RPC nodes.

## Celestia
- Node overview — https://docs.celestia.org/operate/getting-started/overview/
- Bridge node setup — https://docs.celestia.org/operate/data-availability/bridge-node/
- Hardware requirements — https://docs.celestia.org/operate/getting-started/hardware-requirements/

Key evidence captured:
- current bridge/light/consensus/validator roles;
- bridge node performs erasure coding and serves data availability shares;
- current bridge hardware is substantial;
- no reviewed current primary source proved an independent direct reward stream for bridge/light nodes separate from validator economics.

## Boundless cross-check
- Prover Quick Start — https://docs.boundless.network/provers/quick-start
- Broker Configuration & Operation — https://docs.boundless.network/provers/broker
- Proving Stack — https://docs.boundless.network/provers/proving-stack

Used only as a control/reference against prior Run 026 findings; no new mechanism counted.
