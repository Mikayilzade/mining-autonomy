# Implementation Run I040 — deterministic exact-authorization request packet

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Convert I039's exact one-request reduced plan into a human-reviewable, hash-bound authorization request packet without granting authorization or enabling transport.

## Changes
Added `implementation/exact_authorization_request.py` with `build_exact_authorization_request()`.

The builder:
- revalidates the I039 reduction hash and inert safety flags;
- accepts only the I039 `reduced_to_exact_single_get_plan` path for constructing a concrete authorization request;
- independently re-hashes the embedded reduced session plan and transport preflight;
- requires exactly one production `GET` envelope and verifies its request-binding hash against the preserved transport semantics;
- cross-checks the single session-plan step against the single preflight envelope;
- binds the exact scope, reduced session-plan hash and full reduced-preflight hash into a short-lived request packet;
- emits a human-readable summary naming the exact URL/host, one-request ceiling, no-credential/no-action boundary and expiry;
- constrains TTL to 60–900 seconds;
- emits no usable authorization nonce or token;
- preserves I039 no-capture, blocked and already-minimal outcomes without inventing an authorization request.

## Verification
Added `implementation/test_exact_authorization_request.py` with eight deterministic tests covering:
1. exact one-GET request construction with TTL and readable scope;
2. binding to reduced session/preflight/scope hashes;
3. no-capture preservation;
4. already-minimal preservation without fabricating an embedded plan;
5. blocked-state preservation;
6. I039 outer-hash tamper rejection;
7. inner transport/scope tamper rejection even after recomputing the outer I039 hash;
8. invalid TTL and non-UTC time rejection.

Isolated local verification: **8 passed** and syntax compilation passed. GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions
No DNS/HTTP, login, KYC, API key, wallet, payment, bid, task acceptance, publication, paid API/server, settlement or other value-moving action occurred. `authorization_granted` remains false, nonce/token remain null, transport remains disabled and credentials remain forbidden.

## Outcome
The stack now has a deterministic object that can be shown to a human for an exact future permission decision without widening scope beyond the one I039-selected GET. It is a request for authorization, not authorization itself.

The remaining economic gap is unchanged: production demand/utilization cannot be measured until a separately authorized real read-only observation occurs.

## Next run — I041
Build a deterministic authorization-consent verifier that can consume I040 plus a future explicit human decision object, verify exact packet/scope/TTL bindings, and emit a short-lived execution authorization only when the decision is explicit and still valid. For this run, keep the verifier test-only/offline with synthetic consent fixtures; do not create or infer real user consent from chat history and do not enable network transport.

Project state: **IMPLEMENTATION IN PROGRESS**.
