# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I034 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I034_CAPTURE_SESSION_ATTESTATION.md`
- `implementation/session_attestation.py`
- `implementation/test_session_attestation.py`
- `implementation/RUN_I033_SYNTHETIC_CAPTURE_SESSION.md`
- I033/I032 and prior receipt-gated capture/archive files named in STATUS.

## I034 result
The synthetic capture path now has deterministic replay/coverage attestation over the complete I029→I033 chain.

Important behavior:
1. canonical I029 session-plan SHA-256 is recomputed and must equal the I030 preflight plan hash;
2. the I030 transport-envelope-set SHA-256 is independently recomputed;
3. session-plan step identity and envelope identity are rebound by sequence/platform/source/manifest item/evidence classes;
4. every I033 audit row must bind to exactly one planned request;
5. captured/missing/rejected counts are recomputed from rows rather than trusted from mutable summary fields;
6. `production_gap_count` must equal missing + rejected planned requests;
7. captured audit receipt hashes must exactly match `verified_captures` receipt hashes;
8. verified capture-report attestation receipt hashes must exactly match the successful capture set;
9. duplicate receipt membership fails closed;
10. a canonical coverage payload is hashed separately and the full attestation receives `attestation_sha256`;
11. stored attestations can be rebuilt and exactly verified;
12. missing evidence remains unknown, never zero-demand evidence;
13. no real DNS/HTTP or external action exists in this path.

## Immediate next run: I035
Create a deterministic capture-attestation comparison/delta verifier. Accept two valid attestations only when they share the exact session-plan hash and transport-envelope-set hash. Report coverage transitions, per-request state changes, production-gap delta and verified capture receipt-set changes without inferring demand from missing data. Fail closed on tampered or cross-plan attestations. Perform no network request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
