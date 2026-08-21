# Implementation Run I075 — single-use real-transport authorization consumption/preflight

Date: 2026-08-22
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add the deterministic single-use consumption/preflight gate required by I074 without adding DNS/HTTP or any network-capable adapter.

## Changes
Added `implementation/real_transport_authorization_consumption.py` with `consume_real_transport_authorization()`.

The gate independently revalidates:
- the full I074 verification-record hash, mode, verified-authorize state and inert flags;
- the embedded I074 authorization-record hash/state;
- exact review, decision and scope-hash bindings;
- exact one-production-GET / no-credentials / no-action scope;
- `max_consumptions=1` and single-use semantics;
- issue/expiry/consumption timestamps;
- caller-supplied prior-consumption history to reject replay/double-consumption.

A successful consumption emits only an immutable `single_use_real_transport_authorized_attempt_envelope`. The envelope carries mandatory preflight requirements for:
- DNS resolution before connect, private/loopback/link-local/reserved rejection, destination pinning and DNS-rebinding recheck;
- zero automatic redirects (`max_redirects=0`) with future redirect-target revalidation if redirects are ever enabled;
- response-size cap of 1 MiB, JSON-only content type and body-size gating before parsing;
- fresh first-party source-policy evidence and anonymous read-only access.

The envelope explicitly keeps `transport_adapter_present=false`, `transport_enabled=false`, `network_enabled=false`, `network_calls_performed=false`, credentials/task acceptance/submission/execution/value movement disabled, and cannot be reused.

## Verification
Added `implementation/test_real_transport_authorization_consumption.py` with 12 deterministic tests covering exact consumption, mandatory gates, hash tamper, invalid state, authorization tamper, scope widening, binding mismatch, replay, expiry, pre-issue consumption, non-single-use mutation and unsafe flags.

Local isolated verification: **12 passed**. GitHub Actions was not dispatched.

## Safety / external actions
No DNS/HTTP, login, credentials, task acceptance, submission, KYC, wallet, payment, paid API/server, publication, settlement or value-moving action occurred. No network-capable adapter was added.

## Outcome
The explicit I074 authorization can now be deterministically consumed exactly once into a hash-bound preflight envelope while remaining network-incapable. This closes the authorization-consumption layer and leaves the next work focused on validating a strictly constrained network-capable adapter contract without performing real transport.

## Next run — I076
Build a deterministic network-capable adapter contract validator only over the I075 authorized-attempt envelope. Require an adapter declaration that can enforce the exact DNS/redirect/response/source-policy gates and one-request/no-credentials/no-action scope, but keep its execution entrypoint disabled/unreachable and perform no DNS/HTTP. Produce a separately reviewable adapter-readiness artifact before any real transport implementation.

Project state: **IMPLEMENTATION IN PROGRESS**.
