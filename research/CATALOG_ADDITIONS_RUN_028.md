# Catalog additions — Run 028

Evidence date: 2026-08-16

This supplemental catalog exists because `CATALOG.md` is large and should not be destructively rewritten merely to append. Future consolidation can merge these entries into the master catalog.

| Name | Category | Status | Server-native | Automation | Capital / recurring cost | Revenue source | Main constraint | Next validation |
|---|---|---:|---:|---:|---|---|---|---|
| Marlin Oyster Confidential VM Provider | TEE/confidential compute marketplace | VERIFIED | Yes | 5 | TEE/cloud infra + POND stake + gas | Customer USDC job payments | utilization, cloud margin, stake/slashing | live rates, jobs/utilization, stake-per-job |
| Marlin Oyster Serverless Executor | serverless TEE compute worker | VERIFIED | Yes | 5 | enclave infra + stake | user fees + possible bootstrap pool | demand, stake/slashing, enclave cost | current executor deployment path + economics |
| Marlin Oyster Serverless Gateway | TEE request/response relay | VERIFIED | Yes | 5 | enclave infra + stake + chain gas | user fee component + bootstrap support | gas exposure, stake/slashing, assignment volume | current gateway setup + net fee economics |
| Lumoz Verifier Node | ZK/AI verification node | VERIFIED | Yes | 5 | verifier license + server + gas | verifier rewards / commission / stake-linked rewards | license availability, token economics | current license secondary path + realized rewards |
| Lumoz Compute Node / zkProver | ZK/AI proving compute | VERIFIED | Yes (GPU) | 5 | GPU + stake + gas | ZK-PoW / compute rewards + protocol fees | GPU economics, stake/slashing, utilization | live setup, hardware, reward realization |
| Fermah Prover Node | universal proof market | WATCHLIST/RESTRICTED | Yes | 5 | high CPU/GPU + operator setup | intended proof-request payments/rewards | current public path remains testnet/whitelist | production mainnet/self-service admission |
| Lagrange Prover | ZK proof network | WATCHLIST/RESTRICTED | Yes | 5 | compute + restaked collateral | paid completed proof work | admission appears operator/program-oriented | current independent self-service operator path |
| Succinct/SP1 Prover | decentralized proof network | WATCHLIST | Yes | 5 | compute + stake/collateral as applicable | proof jobs / network rewards | independent production onboarding unclear | explicit self-service mainnet prover admission |

## Cross-run classification note
Marlin Oyster does not add a new top-level mechanism: it is customer-paid compute/relay infrastructure with confidential-compute guarantees. Lumoz does not add a new top-level mechanism either: it is stake/license-backed compute/verification rewards. Both are nevertheless material project-level discoveries and therefore invalidate completion at Run 028.
