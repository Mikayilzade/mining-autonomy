# Implementation Run I085 — real-transport safety preflight

Date: 2026-08-22
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Build the deterministic safety preflight immediately after I084 without performing DNS or HTTP. The stage must accept only injected evidence and prove that an exact one-request anonymous production GET remains bound to fresh first-party policy evidence, public-only DNS resolution/pinning and a strict HTTPS/JSON transport contract.

## Changes
Added `implementation/real_transport_safety_preflight.py` with `build_real_transport_safety_preflight()`.

The verifier independently revalidates the I084 consumption-preflight hash/state, zero-network one-attempt envelope and consumption receipt, exact one-production-GET/no-credentials/no-action scope, one-request/one-adapter ceilings, adapter ID, target fingerprint and implementation/source lineage.

It then validates three injected evidence objects:

1. **First-party policy evidence** — must be fresh, hash-bound, HTTPS-sourced, `provider_first_party`, content-digest-backed and explicitly allow anonymous read-only GET automation without credentials.
2. **DNS-resolution evidence** — must be fresh, hash-bound and source-digest-backed. Resolved and pinned address sets must match. The verifier parses every injected IP literal itself with Python `ipaddress` and rejects private, loopback, link-local, multicast, reserved, unspecified or otherwise non-global addresses even if an evidence flag falsely claims they are public. Alias-chain review, anti-rebinding and address pinning must all be explicitly attested.
3. **HTTPS/JSON transport contract** — must be exact-target/source/adapter/scope bound, HTTPS + TLS only, GET only, at most one network request, zero redirects, credentials/action disabled, JSON-only, decompressed-response-size bounded to at most 1 MiB and pinned-address use mandatory.

A clean result emits only a hash-bound `single_attempt_real_transport_safety_envelope`. It still has `network_capable_adapter_reachable=false`, `transport_enabled=false`, `network_enabled=false`, `network_calls_performed=false` and is explicitly not an execution token.

## Verification
Added `implementation/test_real_transport_safety_preflight.py`.

Local isolated verification: **7 passed**. Syntax compilation passed.

Coverage groups include clean readiness; I084 hash tamper/request-ceiling widening; policy freshness/first-party/rights/source binding; private-address injection, pinning and anti-rebinding/alias failures; HTTPS/TLS/zero-redirect/JSON/size contract; target/hostname substitution; future evidence and invalid UTC verification time.

## Safety / external actions
No DNS lookup, HTTP request, socket, TLS connection, credential use, login, task acceptance, submission, payment, wallet, settlement or value movement occurred. All evidence used by the tests is synthetic/injected. GitHub Actions was not dispatched.

## Outcome
The exact I084 one-attempt authorization path now has a deterministic evidence-only transport-safety boundary. Passing I085 means only that the supplied evidence and transport contract are internally consistent and satisfy the safety gates; it does **not** prove live DNS state, live provider policy, real demand, profitability or successful transport.

## Next run — I086
Build a final immutable human-reviewable one-shot real-observation packet over the exact I085 safety envelope. Revalidate I084/I085 hashes and surface the exact target fingerprint, hostname, pinned addresses, policy/DNS evidence digests and HTTPS/JSON limits. Require a new fresh explicit final decision bound to that packet before any network-capable adapter can become reachable. Perform no DNS/HTTP.

Project state: **IMPLEMENTATION IN PROGRESS**.
