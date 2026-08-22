# Implementation Run I090 — single-use dependency-injected transport executor

Date: 2026-08-22
Status: **completed**

## Goal
Complete the exact I089 safety step by adding a one-shot executor that can consume a dependency-injected transport result, while exercising it only with synthetic fixtures and making no live DNS/HTTP request.

## Added
- `final_single_use_transport_executor.py`
- `test_final_single_use_transport_executor.py`

## Behavior
`execute_single_use_dependency_injected_transport()` revalidates the I089 builder hash/state, nested invocation-gate hash/state, expiry, replay lineage and exact read-only request limits before it invokes the injected callable. Invalid/stale/replayed gates are rejected before the callable is touched.

Once the callable is invoked, the one-shot is consumed even when the transport raises or its result is rejected. A result is accepted only when it reports exactly one request, a public peer IP in the pinned set, verified TLS with the exact hostname, no DNS re-resolution after connect, zero redirects, JSON media type, valid JSON body and both compressed/decompressed sizes within the bound. Accepted responses receive a hash-bound response attestation plus a hash-bound single-use invocation receipt.

The executor itself contains no DNS/HTTP implementation and does not supply credentials, task acceptance/submission, payment, wallet, settlement or value movement authority. A future live adapter must enforce the reported socket/TLS properties itself; these fields cannot be trusted merely because an arbitrary callable claims them.

## Verification
- Python syntax compilation: **PASS**.
- 8 deterministic synthetic tests: **PASS**.
- Covered success, transport exception consumption, invalid peer/redirect, replay before transport, expiry, decompressed-size ceiling, non-JSON rejection and tampered I089 state.
- GitHub Actions not dispatched; repository workflow remains `workflow_dispatch` / `pull_request` only.
- No DNS/HTTP, credentials, paid action or value movement occurred.

## Risks / conclusion
The authorization/replay executor is now deterministic and fail-closed, but a real network measurement still requires a concrete transport implementation whose peer-IP, TLS-SNI, redirect and decompression claims are derived from the actual connection rather than self-asserted metadata.

## Next
I091: build and test a concrete network transport adapter boundary that derives its safety attestation from the actual socket/TLS/HTTP implementation, but keep testing offline/synthetic (e.g. injected socket/response doubles). Preserve address pinning, hostname certificate verification, no re-resolution, one request, zero redirects and byte ceilings. Do not perform the first real read-only observation until a fresh exact authorization/safety chain separately permits it.
