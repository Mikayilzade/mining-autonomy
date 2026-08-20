# Implementation Run I032 — synthetic response-to-sanitized-capture bridge

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Close the remaining offline integrity gap between I031 synthetic HTTP-like response receipts and the existing I023/I024 sanitized receipt-gated durable evidence path. Use synthetic response bodies only and make malformed, oversized, unexpected or provenance-mismatched responses fail before durable evidence.

## Changes
Added `implementation/response_capture_bridge.py`.

The bridge:
- accepts only an already-produced I031 synthetic execution receipt plus explicit response bytes;
- independently verifies the top-level execution receipt hash;
- locates exactly one requested response receipt by its SHA-256;
- reconstructs and verifies the response receipt hash;
- binds that response to the exact I030 request envelope and reuses the I031 request-envelope integrity validation;
- rebinds the request to the exact sealed I023 sampling-manifest item;
- requires platform/source/evidence-class identity to agree across manifest, request and response;
- requires 2xx status and the already-allowlisted I031 media types;
- rechecks response byte count and body SHA-256 before any parser/builder runs;
- parses `application/json` with strict UTF-8, JSON syntax, bounded node count and bounded depth;
- normalizes `text/plain` as UTF-8 with CRLF normalization and rejects NUL/control characters or excessive characters;
- accepts only a dependency-injected platform-specific payload builder that returns an already-sanitized `SanitizedCapture`;
- re-indexes the resulting observation bundle and verifies platform/source/source timestamp/capture timestamp/evidence class;
- creates the existing I023 capture receipt and extends it with exact I031 execution provenance;
- recomputes and re-verifies the final receipt so the output can flow unchanged into I024 `run_verified_capture_batch()` and `append_capture_report()`.

The durable provenance now contains:
`sealed manifest item -> I030 request binding -> I031 response receipt -> body SHA-256 -> sanitized observation bundle -> I023 capture receipt -> I024 verified durable archive`.

## Tests
Added `implementation/test_response_capture_bridge.py` with deterministic coverage for:
1. full synthetic PayanAgent JSON response → sanitized observation bundle → verified capture batch → durable production evidence archive;
2. response-body hash mismatch;
3. response-receipt metadata tampering;
4. unexpected evidence-class output from a builder;
5. malformed JSON rejected before builder invocation;
6. parse-byte limit rejection.

The integration test uses the existing PayanAgent observation-bundle builder and existing I024 receipt-gated archive rather than a parallel mock archive contract.

## Verification
The new module and test module were syntax-checked while preparing the run. Push-triggered CI remains disabled and no manual Actions dispatch was performed, so this run does not reintroduce notification-email spam.

A full repository pytest/green-CI claim is deliberately not made in this run.

## Safety / external actions
No DNS lookup, HTTP request, login, KYC, API key, wallet, payment, bid, task acceptance, fulfillment, service publication, paid API/server or settlement occurred.

No network-capable transport implementation was added. The bridge can process only response bytes supplied by a caller and every returned capture remains `dry_run_only=True`, `action_enabled=False`, `network_calls_performed=False`, `credentials_used=False`.

## Outcome
The synthetic control plane now reaches the durable sanitized evidence boundary end-to-end. A future explicitly authorized read-only transport can therefore be added upstream without inventing a second evidence path: its responses must satisfy the same request/response/body/evidence bindings before they can influence production evidence.

## Next — I033
Build multi-response/session-level synthetic capture coverage over I032:
- exact coverage of the planned I029/I030 session;
- duplicate/missing response receipt detection;
- per-response success/rejection states with stable reason codes;
- failure isolation so one malformed response cannot corrupt successful captures;
- only successful receipt-verified captures enter durable evidence;
- missing/failed items stay explicit unresolved production gaps.

Still perform no real network request.

Project state: **IMPLEMENTATION IN PROGRESS**.
