# Implementation Run I042 — deterministic offline single-use authorization lease

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a replay-safe, single-use offline authorization lease/consumption gate over I041 without enabling real network transport.

## Changes
Added `implementation/authorization_lease.py` with two fail-closed stages:
- `issue_single_use_authorization_lease()` independently revalidates the I041 consent-verification hash and embedded execution-authorization hash, requires exact authorized one-production-GET scope, inherits the original expiry, and emits an inert one-request lease bound to consent/request/scope/decision hashes;
- `consume_single_use_authorization_lease()` validates a hash-bound synthetic execution attempt, enforces one GET / production / no credentials / no action, checks issue/expiry time, validates prior consumption receipts, rejects replay/double-consumption, and emits a zero-remaining-budget receipt.

Transport remains explicitly disabled. I042 consumption models authorization-budget use only; it does not perform DNS/HTTP or imply that a network call happened.

## Verification
Added `implementation/test_authorization_lease.py` with eight deterministic tests covering exact binding, one-use exhaustion, replay rejection, expiry rejection, consent tamper rejection, scope widening rejection, cross-lease attempt binding rejection, deny handling and transport-request rejection.

Isolated local verification: **8 passed** (`python -m pytest -q`). GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions
Synthetic fixtures only. No real user consent was inferred. No DNS/HTTP, credentials, login/KYC, wallet, payment, bid, task acceptance, publication, paid API/server, settlement or value-moving action occurred.

## Outcome
The offline authorization chain now has explicit single-use semantics: an exact I041 authorization can be leased once, consumed once, expires with the original authorization, and cannot be replayed when a prior valid consumption receipt is present. The economic gap remains unchanged because no production demand sample has yet been authorized/captured.

## Next run — I043
Build a deterministic dependency-injected execution wrapper that requires a fresh unconsumed I042 lease, consumes the lease atomically in the wrapper contract before invoking a transport dependency, but keep the default transport a synthetic stub. Add a hard `allow_real_transport=False` default and tests proving no network path exists unless a later separately authorized integration explicitly flips that gate.

Project state: **IMPLEMENTATION IN PROGRESS**.
