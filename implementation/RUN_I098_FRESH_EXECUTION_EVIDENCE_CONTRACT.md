# I098 — Fresh Execution-Evidence Artifact Contract

Date: 2026-08-22
Status: **COMPLETED AS SCOPED NETWORK-INERT SAFETY CHECKPOINT**

## Objective
Close the next exact safety step after I097: define a deterministic artifact contract for the fresh policy/ToS, DNS/public-IP pinning, TLS/transport and anti-rebinding evidence that must exist immediately before the later separately authorized one-shot PayanAgent observation.

## Work completed
Added `i098_fresh_execution_evidence_contract.py`, a stdlib-only validator/specification module with no DNS, sockets, HTTP, credentials or market actions. It hard-binds every evidence component and final bundle to the exact I096 packet hash `0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56`, exact scope hash `df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e`, host `payanagent.com`, method `GET`, path/query `/api/v1/requests?status=open&limit=1`, and request count `1`.

The contract requires four independently hash-bound components:
- `policy_tos`: official public primary-source URL/content hash, explicit conclusion that the exact anonymous read-only observation is permitted, automation prohibition unresolved = false, credentials required = false, value movement required = false;
- `dns_resolution`: fresh resolver evidence, raw-answer hash, short effective TTL and a non-empty unique set of public IP addresses only;
- `tls_transport`: fresh certificate/chain/handshake hashes, hostname/time validation, TLS 1.2+ and a connected IP inside the current DNS pin set;
- `anti_rebinding`: a second immediately-before-request revalidation whose public-address set must exactly match the pinned DNS set.

Freshness is fail-closed: policy/ToS max age 6h; DNS and TLS max age 5m; anti-rebinding max age 60s. The final bundle expires at the earliest component `valid_until`. Component hashes are recomputed canonically before use, and the bundle pin set must exactly equal the fresh DNS set.

The module explicitly keeps `network_capable=false`, `execution_token=false`, `ready_for_network_invocation=false`. Even a fully valid I098 evidence bundle cannot authorize transport: the separately explicit user authorization required by I097 and the later single-use invocation/executor lineage remain mandatory.

## Validation
The embedded offline self-test was executed in an isolated local environment before repository write and passed. It covers:
- valid synthetic public-IP evidence bundle;
- exact path/query drift rejection;
- private/loopback DNS pin rejection.

No GitHub Actions workflow was dispatched. The repository workflow remains `workflow_dispatch` / `pull_request` only, so direct documentation/implementation writes in this checkpoint did not intentionally trigger CI.

## Resource / Execution Router
No Router redesign was needed: I048–I067 already implement fixed-vs-marginal resource economics, materialized-resource selection, measured feedback and unchanged-task rerouting. I098 remains downstream of those economic/resource gates and does not widen market, policy or demand eligibility.

## Risks / boundaries
- No DNS resolution or HTTP request was performed.
- No live policy page was fetched by this implementation artifact.
- No credentials, account action, task acceptance, bid, submission, wallet, payment, spend or value movement occurred.
- No user authorization was fabricated, inferred or reused.
- Fresh evidence must be acquired again at the actual execution moment; this run defines representation and validation only.
- A valid policy conclusion must come from a current official primary source and may not be replaced by synthetic fixtures.

## Files
- `implementation/i098_fresh_execution_evidence_contract.py`
- `implementation/I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json`
- `implementation/RUN_I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.md`

## Next action — I099
Build a **network-inert evidence acquisition orchestrator/dry-run harness** that consumes the I098 contract and proves the sequencing/fail-closed behavior using synthetic fixtures only: policy evidence -> DNS pins -> TLS binding -> anti-rebinding -> final bundle -> I097 compatibility projection. It must not resolve DNS, fetch policy pages, open sockets, perform HTTP or manufacture authorization. The purpose is to prove that when fresh real evidence is later separately authorized/acquired, only a complete, temporally valid, exact-scope bundle can reach the pre-invocation gate.
