# Implementation Run I076 — network-capable adapter contract validation

Date: 2026-08-22
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Validate the contract of a future network-capable adapter against the exact I075 single-use authorized-attempt envelope without adding any reachable transport entrypoint or performing DNS/HTTP.

## Changes
Added `implementation/network_adapter_contract.py` with `validate_network_capable_adapter_contract()`.

The validator independently revalidates:
- the full I075 consumption-record hash, mode, successful-consumption state and inert safety flags;
- the embedded authorized-attempt-envelope hash, mode, state, single-use/request-count semantics and exact bindings back to I074/I073;
- exact one-production-GET / no-credentials / no-action scope;
- the complete I075 mandatory DNS/private-address/pinning/rebinding policy;
- zero automatic redirects and `max_redirects=0`;
- the 1 MiB JSON-only response gate before parsing;
- fresh first-party anonymous-read-only source-policy requirements.

A future adapter declaration must itself be hash-bound and must declare exact request/gate enforcement. It may declare `network_capable=true` only as a contract capability; at this checkpoint it must also prove that no execution entrypoint is present or reachable, no transport callable is attached, no credentials are embedded, and execution/network/task acceptance/submission/value movement all remain disabled.

A clean declaration emits only a hash-bound `network_capable_adapter_contract_readiness_artifact` with `ready_for_real_network_execution=false` and `separate_human_review_required=true`. The artifact is explicitly not an execution token.

## Verification
Added `implementation/test_network_adapter_contract.py` with 12 deterministic tests covering:
1. exact contract -> review-only readiness artifact;
2. I075 consumption tamper rejection;
3. envelope tamper rejection;
4. rehashed scope widening rejection;
5. missing DNS destination pinning rejection;
6. redirect widening rejection;
7. response content-type widening rejection;
8. source-policy credential widening rejection;
9. reachable/callable entrypoint rejection;
10. adapter-declaration hash tamper rejection;
11. envelope-binding mismatch rejection;
12. request-contract widening rejection.

Local isolated verification: **12 passed** plus syntax compilation. GitHub Actions was not dispatched.

## Safety / external actions
No DNS/HTTP, login, credentials, task acceptance, submission, KYC, wallet, payment, paid API/server, publication, settlement or value-moving action occurred. No callable transport implementation or network entrypoint was added.

## Outcome
The project now has a deterministic proof layer that a future network-capable adapter contract exactly preserves I075's one-request safety boundary before any real transport implementation is admitted. Contract readiness cannot enable transport and cannot widen upstream policy, demand, resource or authorization state.

## Next run — I077
Build an inert implementation-binding/audit layer for a future HTTPS/JSON adapter. Bind a concrete adapter implementation manifest/source digest to the exact I076 readiness artifact and prove the implementation surface exposes no enabled transport entrypoint yet. Define the future activation interface needed for one separately authorized GET, but keep it unreachable and perform no DNS/HTTP. This should leave the stack one step closer to a reviewable implementation package rather than adding another abstract authorization layer.

Project state: **IMPLEMENTATION IN PROGRESS**.
