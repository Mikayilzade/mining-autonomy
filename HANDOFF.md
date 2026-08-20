# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I036 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I036_ATTESTATION_HISTORY.md`
- `implementation/attestation_history.py`
- `implementation/test_attestation_history.py`
- `implementation/RUN_I035_CAPTURE_ATTESTATION_DELTA.md`
- I035/I034 and prior receipt-gated capture/archive files named in STATUS.

## I036 result
The stack now has deterministic longitudinal replay for multiple same-plan I034 capture-session attestations.

Important behavior:
1. every observation is independently validated using the I035 internal replay verifier;
2. timestamps must be explicit canonical UTC seconds and strictly increasing;
3. duplicate attestation identities fail closed;
4. every observation must share the exact I029 session-plan hash and I030 transport-envelope-set hash;
5. ordered request-binding identities must remain identical across the series;
6. per-request sequence/platform/source/evidence-class identity drift fails closed;
7. every adjacent I035 delta is recomputed from the stored attestations;
8. optional supplied deltas must exactly equal the freshly replayed delta;
9. coverage timeline and first-to-last captured/missing/rejected/production-gap evolution are recorded;
10. request state-transition frequencies are summarized without translating them into demand claims;
11. the complete series receives canonical `history_sha256`;
12. missing/rejected capture always remains unknown evidence rather than negative demand;
13. no real DNS/HTTP or external action exists in this path.

## Immediate next run: I037
Create a deterministic longitudinal evidence-quality/regression gate over I036 history. Require minimum observation count/span before assigning stable/improving/regressing capture-integrity labels; distinguish capture/infrastructure evidence quality from economic demand evidence; produce a fail-closed recommendation for whether another future explicitly authorized read-only observation would add value. Perform no network request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
