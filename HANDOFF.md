# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I035 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I035_CAPTURE_ATTESTATION_DELTA.md`
- `implementation/capture_attestation_delta.py`
- `implementation/test_capture_attestation_delta.py`
- `implementation/RUN_I034_CAPTURE_SESSION_ATTESTATION.md`
- I034/I033 and prior receipt-gated capture/archive files named in STATUS.

## I035 result
The stack now has deterministic same-plan comparison for two I034 capture-session attestations.

Important behavior:
1. both baseline and target attestations are independently validated before comparison;
2. coverage hash and full attestation hash must match recomputed canonical content;
3. audit-row state counts and production gaps are recomputed rather than trusted from mutable counters;
4. audit binding coverage must equal the planned request-binding set;
5. captured audit receipts must equal verified-capture and capture-report receipt sets;
6. baseline/target must share exact session-plan and transport-envelope-set hashes;
7. planned request-binding order and per-request identity fields must match;
8. delta output records coverage transition, numeric coverage deltas, request state/error/receipt changes and verified receipt additions/removals;
9. complete comparison is hash-addressed with `delta_sha256`;
10. missing evidence always remains `unknown_not_negative_demand`;
11. counter tampering still fails even if an attacker recomputes outer hashes, because internal replay checks counts against audit rows;
12. no real DNS/HTTP or external action exists in this path.

## Immediate next run: I036
Create a deterministic longitudinal attestation-history/series verifier over multiple same-plan I034 attestations and I035 deltas. Require explicit monotonic observation timestamps, reject duplicate attestation identities, preserve exact plan/envelope identity, summarize transition frequencies and coverage evolution without extrapolating demand, and fail closed on any mismatch. Perform no network request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
