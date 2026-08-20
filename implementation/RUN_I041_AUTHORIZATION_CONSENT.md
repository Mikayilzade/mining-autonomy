# Implementation Run I041 — deterministic offline authorization-consent verifier

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a fail-closed offline verifier that can evaluate a future explicit human authorization decision only when it is bound to the exact I040 packet/scope and remains inside the I040 TTL, without enabling transport or inferring consent from chat history.

## Changes
Added `implementation/authorization_consent.py` with `verify_explicit_authorization_consent()`.

The verifier:
- independently revalidates the I040 wrapper hash, exact request hash and exact scope hash;
- requires the I040 state `exact_single_get_ready_for_explicit_user_authorization`;
- requires exactly one production `GET`, max_requests=1, no credentials and no action;
- requires an explicit decision object with mode `explicit_human_read_only_authorization_decision`;
- binds the decision to the exact I040 wrapper hash, inner authorization-request hash and scope hash;
- requires explicit `human_scope_acknowledged=true`;
- requires the decision timestamp to be inside the I040 request window and not in the future relative to verification time;
- accepts only `authorize` or `deny`;
- rejects widened request count/method/credential/action scope;
- on a valid synthetic authorize decision emits a hash-bound, short-lived execution-authorization object while keeping `transport_enabled=false` and `network_calls_performed=false`;
- never infers real user consent and records `real_user_consent_inferred=false`.

## Verification
Added `implementation/test_authorization_consent.py` with eight deterministic synthetic-fixture tests covering:
1. exact authorize decision -> bound offline execution authorization;
2. explicit deny -> no execution authorization;
3. expired I040 request rejection;
4. scope-binding tamper rejection;
5. outer wrapper tamper rejection;
6. scope widening rejection;
7. missing human acknowledgement rejection;
8. decision timestamp boundary/future-time rejection.

Isolated local verification: **8 passed**. GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions
All consent fixtures were synthetic. No prior chat text was interpreted as authorization. No DNS/HTTP, login, KYC, credentials, wallet, payment, bid, task acceptance, publication, paid API/server, settlement or other external action occurred. The verifier itself contains no transport implementation.

## Outcome
The stack can now distinguish an exact, explicit, time-valid human decision from stale, unbound, widened or synthetic/non-real input without enabling network access. This closes the offline consent-verification layer while preserving the requirement for a separate real explicit authorization before any production capture.

The economic gap is unchanged: no real production demand/utilization sample has been taken.

## Next run — I042
Build a deterministic offline single-use authorization lease/consumption gate over I041. Bind one future execution attempt to the exact execution-authorization hash, enforce max_requests=1 and expiry, reject replay/double-consumption, and keep transport dependency-injected/disabled with synthetic fixtures only. Do not perform real DNS/HTTP.

Project state: **IMPLEMENTATION IN PROGRESS**.
