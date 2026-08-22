# Implementation Run I088 — final authorization consumption preflight

Date: 2026-08-22
Status: **completed**

## Goal
Consume the exact I087 final one-shot authorization only after revalidating the exact I086 packet plus fresh injected I085-style policy/DNS/transport evidence, while keeping all network transport unreachable.

## Added
- `final_real_observation_authorization_consumption.py`
- `test_final_real_observation_authorization_consumption.py`

## Behavior
`consume_final_real_observation_authorization()` independently revalidates the I086 packet hash/state/TTL/inert flags/one-GET transport ceiling and the I087 authorization hash, expiry, single-use/unconsumed state, exact packet/adapter/target/scope/source/hostname/pinned-address/evidence/transport bindings and mandatory execution-time revalidation flags.

At consumption time it requires newly injected evidence in the existing I085 formats:
- fresh first-party anonymous read-only policy evidence;
- fresh DNS evidence with literal public-IP validation, unchanged hostname and exact pinned-address set, alias review and anti-rebinding attestations;
- an exact HTTPS/TLS GET-only, one-request, zero-redirect, JSON-only <=1 MiB transport contract with pinning and decompressed-size protection.

Fresh evidence hashes may differ from the historical I085/I086 evidence digests; the immutable I086 packet remains authoritative for target, scope, implementation source, hostname, pinned addresses and transport limits. Drift in those bindings fails closed.

A clean consumption emits only:
1. one immutable `single_attempt_final_real_observation_execution_envelope`; and
2. one hash-bound `single_use_final_real_observation_consumption_receipt`.

Both remain zero-network. The envelope caps future adapter/network attempts at one, retains no-credentials/no-task/no-submission/no-value permissions and explicitly keeps the network-capable adapter unreachable. Replay of an already produced receipt hash is rejected.

## Verification
Local deterministic verification: syntax compilation passed and **8 scenario checks passed** covering clean readiness, replay rejection, stale authorization, private/pin-changing DNS, hostname drift, stale policy evidence, transport widening and packet tamper.

GitHub Actions was not dispatched. No DNS, TLS, HTTP, sockets, credentials, task acceptance/submission, payment, wallet, settlement or value movement occurred.

## Risks / boundaries
I088 still does not prove current live DNS, live provider policy, demand, acceptance or profitability. It does not make any network-capable adapter reachable and is not permission for task/payment/value movement. A future real observation must consume this exact envelope through a separate adapter gate that revalidates the envelope/receipt and performs at most the single explicitly scoped read-only request.

## Next
I089: build the final network-capable adapter invocation gate over the exact I088 envelope + receipt. Keep it fail-closed and one-attempt only; require the same exact target/host/pins/scope/transport limits and expose a dependency-injected transport boundary. Do not perform a live request unless the required real-observation authorization and current safety evidence are explicitly supplied and all existing gates still pass.
