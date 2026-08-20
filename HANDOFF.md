# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I033 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I033_SYNTHETIC_CAPTURE_SESSION.md`
- `implementation/session_capture_batch.py`
- `implementation/test_session_capture_batch.py`
- I032 response bridge and prior receipt-gated capture/archive files named in STATUS.

## I033 result
The synthetic capture path now has exact session-level accounting over the planned I029/I030 request set.

Important behavior:
1. declared planned-request count must match exact preflight envelopes;
2. planned request-binding hashes must be unique;
3. supplied duplicate response-receipt hashes are rejected before parsing;
4. duplicate receipt hashes inside the I031 execution receipt are explicit failures;
5. responses absent from the execution receipt or outside the planned session are rejected;
6. multiple distinct responses for one planned request are rejected as ambiguous;
7. every planned request receives one audit state: `captured`, `missing`, or `rejected`;
8. I032 verification/parsing/sanitization errors are isolated per request and retain stable error codes;
9. only successful I032 receipt-verified captures feed `run_verified_capture_batch()`;
10. missing/rejected items remain explicit production evidence gaps and never imply zero demand;
11. session summary includes exact counts, coverage completeness and production-gap count;
12. still no real DNS/HTTP or external action exists in this path.

## Immediate next run: I034
Create a deterministic capture-session replay/coverage attestation over I033. Bind the session audit to exact I029 session-plan hash and I030 transport-envelope-set hash, canonicalize/hash the attestation, and fail closed on plan drift, audit mutation, verified-capture/report mismatch or manipulated coverage/gap counts. Keep it suitable for later comparison with an explicitly authorized real read-only capture, but perform no network request now.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
