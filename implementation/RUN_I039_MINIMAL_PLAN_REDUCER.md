# Implementation Run I039 — deterministic minimal-plan reducer

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Consume the I038 authorization-readiness decision and deterministically narrow a multi-request I029/I030 capture contract to the exact one production GET selected by I038, without widening future authorization and without performing network activity.

## Changes
Added `implementation/minimal_plan_reducer.py` with `build_minimal_plan_reduction()`.

The reducer:
- revalidates the I038 decision hash and exact I028/I029/I030 hash bindings;
- verifies every original request-binding hash before using it;
- requires the I038-selected request to match exactly one original preflight envelope and one original session step;
- preserves source URL, host, method, manifest item, production environment, evidence classes, provenance checklist, rate contract and timeout;
- converts the selected step to a one-request I029-compatible session plan while recording all other originally planned requests as deferred by `minimal_authorization_scope_reduction`;
- reconstructs a one-request I030-compatible inert transport preflight bound to the original I028 readiness packet and new reduced session-plan hash;
- records old and new request-binding hashes explicitly because sequence normalization changes the binding while economic/source semantics stay unchanged;
- emits an inert no-op if I038 says no capture is needed;
- emits an already-minimal result if I038's existing plan already contains exactly one GET;
- emits a blocked result if I038 has no exact ready request;
- always leaves authorization false, credentials disabled, network calls false, action disabled and `authorization_scope_widened = false`.

## Verification
Added `implementation/test_minimal_plan_reducer.py` with eight deterministic tests covering:
1. exact multi-request reduction to one GET with preserved source/evidence/provenance/rate/timeout semantics;
2. no leakage of unselected requests into the reduced transport envelope;
3. no-capture no-op behavior;
4. already-minimal single-request behavior;
5. blocked/no-target behavior;
6. I038 decision-hash tampering;
7. original I029 plan-binding tampering;
8. selected I030 request-binding tampering.

Isolated local verification: **8 passed** and syntax compilation passed. GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions
No DNS/HTTP, login, KYC, API key, wallet, payment, bid, task acceptance, publication, paid API/server, or settlement occurred.

## Outcome
The stack can now turn I038's multi-request recommendation into a mechanically narrow one-request authorization target. This removes the last ambiguity between “one request selected” and “multi-request plan would be authorized”.

The main economic gap remains unchanged: attributable production demand/utilization still requires a separately authorized real read-only observation before it can be measured.

## Next run — I040
Build a deterministic exact-authorization request packet over the I039 reduced one-request plan. It should bind the reduced session/preflight hashes, TTL, exact GET scope and a human-readable request summary, but must still keep `authorization_granted = false`, contain no usable nonce/credential and perform no network request. If I039 is no-op/blocked/already-minimal, preserve that state without inventing authorization.

Project state: **IMPLEMENTATION IN PROGRESS**.
