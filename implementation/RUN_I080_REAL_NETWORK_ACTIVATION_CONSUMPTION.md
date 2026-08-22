# Implementation Run I080 — single-use real-network activation consumption/preflight

Date: 2026-08-22
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Consume an exact I079 activation authorization once into an immutable one-attempt activation envelope while keeping DNS/HTTP, adapter invocation and every value-moving capability disabled.

## Changes
Added `real_network_activation_consumption.py` with `consume_real_network_activation_authorization()`.

The preflight independently revalidates:
- the exact I078 activation-request hash/mode/readiness state;
- the I079 authorization hash, `authorized_single_use_not_consumed` state, `single_use=true` and `consumed=false`;
- authorization issue/expiry times and the parent I078 request expiry;
- exact one-production-GET/no-credentials/no-action scope;
- I077 implementation/source, I076 contract/readiness, adapter and exact-scope bindings;
- authorization lineage equality between I078 and I079;
- one-request ceiling and explicit prohibition of credentials, task acceptance, submission and value movement;
- prior consumption receipts, including their hashes, so a previously consumed authorization fails closed as replay.

A clean consumption emits two inert hash-bound artifacts:
1. `single_attempt_real_network_activation_envelope` — max one adapter invocation / one network request, but transport/network remain disabled and adapter is not invoked;
2. `single_use_real_network_activation_consumption_receipt` — records that the authorization was consumed once without performing network activity.

Neither artifact is an execution result or a reusable execution token.

## Verification
Added `test_real_network_activation_consumption.py` with ten deterministic offline tests covering:
1. clean one-attempt zero-network consumption;
2. expired authorization rejection;
3. activation-request tamper rejection;
4. authorization hash tamper rejection;
5. wrong request binding after rehash rejection;
6. scope widening rejection;
7. credentials widening rejection;
8. pre-consumed authorization rejection;
9. replay via a valid prior consumption receipt rejection;
10. malformed/tampered prior receipt fail-closed behavior.

Local verification: **10 passed**. GitHub Actions was not dispatched.

## Safety / external actions
No DNS, HTTP, adapter invocation, credentials, paid API/server, task acceptance, publication, submission, wallet, payment, settlement or value-moving action occurred. The new module contains no network transport call.

## Outcome
The activation authorization can now be deterministically reduced to exactly one immutable attempt and cryptographically consumed before any future transport layer is even reachable. Reuse requires a new explicit human authorization lineage rather than replaying an old authorization.

## Next run — I081
Build a deterministic activation-envelope adapter invocation gate over I080 and the existing I077 concrete adapter binding. It must revalidate the I080 envelope/receipt hashes, exact source/adapter/scope lineage and consumption uniqueness, then prepare a dependency-injected **network-incapable synthetic invocation path only** for final end-to-end replay. Keep the real network-capable implementation unreachable; DNS/HTTP and all value-moving actions remain disabled. The purpose is to prove the one-attempt envelope cannot be widened between authorization consumption and adapter invocation before any later real-network experiment.

Project state: **IMPLEMENTATION IN PROGRESS**.
