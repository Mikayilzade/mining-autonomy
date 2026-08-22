# Implementation Run I083 — exact real-read-only invocation decision verifier

Date: 2026-08-22
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Verify a fresh explicit human `authorize`/`deny` decision over the exact I082 human-review request without inferring consent from chat/history, widening scope, exposing a network-capable adapter, or performing DNS/HTTP.

## Changes
Added `implementation/exact_real_read_only_invocation_decision.py` with `verify_exact_real_read_only_invocation_decision()`.

The verifier independently revalidates the I082 request hash/state, exact one-production-GET/no-credentials/no-action scope and scope hash, request TTL, adapter/gate/receipt/preflight/envelope bindings, implementation/source/adapter readiness lineage, and all inert safety flags.

A human decision must:
- be exactly `authorize` or `deny`;
- carry a non-empty decision ID and UTC timestamp within the live I082 request window;
- be hash-bound to `exact_real_read_only_invocation_request_sha256`;
- preserve every adapter/scope/source-lineage binding exactly;
- remain single-use and forbid credentials, task acceptance, submission and value movement.

`deny` emits no authorization. A valid `authorize` may emit only a 30–300 second, request-expiry-capped, single-use unconsumed authorization record for at most one network request. The authorization itself still keeps the network-capable adapter unreachable and transport/network disabled. Optional prior-decision hashes fail closed on replay.

## Verification
Added `implementation/test_exact_real_read_only_invocation_decision.py` with fourteen deterministic offline tests covering clean authorize/deny, request tamper, scope widening/hash mismatch, stale/future timing, wrong bindings, credentials widening, bad/replayed decision hashes, request-capped authorization expiry and UTC/TTL validation.

Local isolated verification: **14 passed**. Syntax/import execution passed through the test run.

## Safety / external actions
No DNS, HTTP, sockets, credentials, login, task acceptance, submission, wallet, payment, settlement or value movement occurred. No network-capable callback is reachable from this verifier. GitHub Actions was not dispatched.

The authorization record is deliberately not a payment/task permission and not an execution result. It can authorize only a future one-shot anonymous read-only invocation after a separate consumption/preflight layer revalidates it.

## Outcome
I082 now has a deterministic fresh-decision boundary with replay awareness and exact scope preservation. The project still has not observed real production demand, so fill rate and positive economics remain unproven.

## Next run — I084
Build a deterministic single-use consumption/preflight over the I083 authorization. Revalidate the exact I082 request and I083 decision/authorization hashes, expiry, unchanged one-GET scope and source lineage; reject replay or stale/tampered authorization; emit at most one immutable zero-network one-attempt envelope plus a consumption receipt. Keep DNS/HTTP and network-capable transport unreachable.

Project state: **IMPLEMENTATION IN PROGRESS**.
