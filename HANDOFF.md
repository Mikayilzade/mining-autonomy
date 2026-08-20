# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I032 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I032_RESPONSE_CAPTURE_BRIDGE.md`
- `implementation/response_capture_bridge.py`
- `implementation/test_response_capture_bridge.py`
- `implementation/SOURCES_I032.md`
- I031 execution gate and prior receipt-gated capture/archive files named in STATUS.

## I032 result
The synthetic execution boundary now connects to the sanitized durable-evidence pipeline without adding any real transport.

Important behavior:
1. top-level I031 execution receipt is independently hash-verified;
2. exactly one response receipt must match the requested response hash;
3. response receipt hash is independently reconstructed from request/source/status/DNS/media/size/body metadata;
4. the matching I030 request envelope is revalidated and bound to the exact sealed sampling-manifest item;
5. source identity and expected evidence classes must agree across manifest → request → response;
6. response body bytes must match both declared byte count and SHA-256 before parsing;
7. only 2xx application/json or text/plain enter parsing;
8. JSON parsing has bounded nodes/depth; text normalization rejects NUL/control characters and oversized text;
9. an injected platform-specific builder alone may turn parsed content into a sanitized observation bundle;
10. bundle platform/source/source-time/capture-time/evidence-class are independently rechecked;
11. the existing I023 receipt is extended with hash-bound I031 execution provenance and reverified;
12. output is directly shaped for I024 `run_verified_capture_batch()` / `append_capture_report()`.

No raw response body is written to the durable archive. No live HTTP/DNS, account, KYC, API key, wallet, payment, bid, task acceptance, service publication or settlement path was added.

## Immediate next run: I033
Add a deterministic multi-response synthetic capture-session bridge over I032. Require exact planned-session coverage, detect duplicate/missing response receipts, isolate per-request parsing/sanitization failures, emit stable audit states, and pass only successful verified captures to durable ingestion. Missing/failed captures remain production evidence gaps. Still no real network.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
