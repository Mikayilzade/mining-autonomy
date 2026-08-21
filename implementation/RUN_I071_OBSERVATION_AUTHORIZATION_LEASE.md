# Implementation Run I071 — single-use observation authorization lease

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a deterministic offline single-use lease over an explicitly verified I070 read-only authorization record, bound to the exact I069 request, exact one-GET scope and remaining authorization window.

## Changes
Added `implementation/observation_authorization_lease.py` with:
- `build_observation_authorization_lease()`;
- `consume_observation_authorization_lease()`.

Lease issuance independently revalidates the I070 verification hash, requires `explicit_read_only_authorization_verified`, revalidates the I069 request hash and exact anonymous production-GET scope, cross-binds the I070 verification/request/readiness/scope hashes, and refuses deny/tampered/widened/expired inputs.

The lease is short-lived, capped to 300 seconds, and can never outlive the original I069 request expiry. It carries `max_consumptions=1`, preserves no-credentials/no-action scope and remains non-executable/network-disabled.

Synthetic consumption requires an exact one-request production GET attempt fingerprint, forbids credentials/actions and explicitly forbids a network transport callback in I071. Prior consumption receipts are hash-validated; a previously consumed matching lease hash causes replay/double-consumption rejection.

## Verification
Added `implementation/test_observation_authorization_lease.py` with eight deterministic tests covering:
1. exact authorize -> short-lived single-use lease;
2. lease expiry capped by original request expiry;
3. deny record cannot issue a lease;
4. verification tamper / rehashed widened request rejection;
5. exact synthetic attempt consumes once without transport;
6. replay/double-consumption rejection;
7. expiry and widened attempt rejection;
8. network callback and tampered prior receipt fail closed.

Local isolated verification: **8 passed**. Syntax compilation also passed. GitHub Actions was not dispatched.

## Safety / external actions
No DNS/HTTP, credentials, login, KYC, wallet, payment, paid task acceptance/submission, publication, settlement or value movement occurred. All fixtures are synthetic. I071 contains no real transport callback and explicitly rejects one.

## Outcome
The explicit human-decision chain now has deterministic single-use/replay semantics before any future transport integration. An authorization decision can no longer be reused indefinitely or widened beyond one exact anonymous production GET in the modeled path.

The dominant economic unknown remains unchanged: real production demand/fill is still unmeasured.

## Next run — I072
Build a deterministic dependency-injected lease-bound transport handoff over I071. It may accept only a freshly consumed exact I071 synthetic receipt and produce one immutable GET envelope for a network-incapable injected adapter; reject stale/replayed/unbound receipts and preserve zero real network calls. Do not perform real DNS/HTTP.

Project state: **IMPLEMENTATION IN PROGRESS**.
