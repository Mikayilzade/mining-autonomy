# Implementation Run I091 — concrete attested pinned HTTPS/JSON transport boundary

Date: 2026-08-22
Status: **completed**

## Goal
Implement the concrete transport boundary requested by I090 without performing a live request: connect only to an already-pinned public IP, use TLS SNI/hostname verification for the original hostname, send exactly one read-only HTTPS GET, never re-resolve DNS or follow redirects, bound wire and decompressed bytes while reading, and derive transport metadata from connection/TLS/HTTP state rather than accepting caller-supplied assertions.

## Added
- `concrete_pinned_https_json_transport.py`
- `test_concrete_pinned_https_json_transport.py`

## Behavior
`execute_concrete_pinned_https_json_transport()` accepts the I090 request mapping plus injected `connector` and TLS context primitives. The module intentionally bundles no live connector/resolver.

Fail-closed rules:
- the request must preserve the exact one-GET HTTPS/no-credentials/no-action/zero-redirect/JSON-only contract;
- an explicit bound `path` is mandatory; it cannot be supplied out-of-band;
- only the deterministic first address from the validated pinned public set is dialed;
- raw and TLS peer addresses must both equal that selected pin;
- TLS context must have hostname checking enabled and `CERT_REQUIRED`; the exact original hostname is passed as SNI;
- the adapter never calls DNS and never follows a redirect; 3xx is rejected after the single request;
- response headers are capped at 32 KiB;
- identity, content-length and HTTP/1.1 chunked bodies are read with an on-wire byte ceiling;
- gzip is supported with a separate decompressed-byte ceiling, blocking zip-bomb-shaped responses;
- content type must be JSON, body must be UTF-8 and parse as JSON;
- result metadata is computed from adapter operations/state.

## Verification
- Python syntax compilation: **PASS**.
- 9 deterministic offline tests: **PASS**.
- Covered pinned-IP-only connect + SNI, mandatory exact path, raw-peer mismatch, TLS-peer drift, insecure TLS context, redirect rejection with one request, compressed limit, gzip decompression limit and bounded chunked JSON.
- Tests used only in-memory socket/TLS/HTTP doubles.
- No DNS, HTTP, credentials, paid action or value movement occurred.
- GitHub Actions was not dispatched.

## Important safety finding
The current I089-produced `request_spec` binds hostname/pins/transport limits but does **not** carry an exact HTTP path/query. I091 therefore deliberately fails closed when `path` is absent. This prevents a future live adapter from inventing or receiving the endpoint out-of-band after human review.

This is an upstream binding gap, not permission to widen scope.

## Risks / conclusion
The concrete transport mechanics are now implemented and offline-verified, but the existing authorization lineage cannot yet instantiate this adapter for a real observation because the exact request path/query is not cryptographically carried through I089/I090.

## Next
I092: extend the exact authorization/adapter invocation lineage so the reviewed target binds a canonical HTTPS request path/query (no fragment/userinfo; no out-of-band target component), propagate it through adapter manifest -> I089 request spec -> I090 validation, and add deterministic replay/tamper tests. Keep the test synthetic/offline. Only after that should a separate fresh explicit authorization chain be considered for exactly one read-only production observation.
