# Implementation Run I044 — inert real-transport integration proposal

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Define, without implementing transport, the exact additional gates that a later separately reviewed integration would need before replacing I043's synthetic dependency for one read-only production GET.

## Changes
Added `implementation/real_transport_proposal.py` with `build_real_transport_integration_proposal()`.

The contract:
- independently revalidates the I042 single-use lease hash and exact one-request scope;
- independently revalidates the I043 execution-request hash and lease/authorization bindings;
- requires exactly one production `GET`, no credentials and no action;
- requires proposal creation inside the lease validity window;
- binds the exact execution request, lease, execution authorization, target and scope into a deterministic proposal hash;
- records seven mandatory future gates: fresh explicit real-user authorization, separate transport implementation review, DNS/destination policy, redirect policy, response timeout/body-size/content-type limits, current source/ToS compliance evidence, and durable receipt binding;
- explicitly states that synthetic or inferred consent is unacceptable;
- emits no authorization token, nonce, callback or network-capable object;
- keeps `authorization_granted=false`, `transport_enabled=false`, `network_capable=false`, `network_calls_performed=false`, `credentials_used=false`, `action_enabled=false` and `money_or_value_movement_enabled=false`.

## Verification
Added `implementation/test_real_transport_proposal.py` with eight deterministic tests covering:
1. exact inert/hash-bound proposal creation;
2. mandatory gate coverage;
3. monkeypatched socket/getaddrinfo proof that proposal construction does not touch network primitives;
4. lease tamper rejection;
5. scope widening rejection even after re-hashing;
6. credential/action widening rejection;
7. cross-lease binding rejection;
8. proposal time/UTC validity rejection.

Isolated local verification: **8 passed** (`python -m pytest -q`). GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions
No DNS/HTTP, login/KYC, credentials, wallet, payment, bid, task acceptance, publication, paid API/server, settlement or value-moving action occurred. The I044 module has no transport dependency or executable callback.

## Outcome
The implementation now has an explicit architectural boundary between "we know exactly what one future read-only observation would require" and "we have permission/implementation to perform it". The proposal cannot itself grant authorization or execute network activity.

The economic gap remains unchanged: no production demand/utilization sample has been captured.

## Next run — I045
Build a deterministic offline review/approval packet over I044 that presents the exact proposal and all unresolved gates as a human-auditable checklist, but still cannot create real authorization. It should distinguish `ready_for_human_decision` from `blocked_by_missing_evidence`, require current source-compliance evidence metadata, and remain transport-free with synthetic fixtures only.

Project state: **IMPLEMENTATION IN PROGRESS**.
