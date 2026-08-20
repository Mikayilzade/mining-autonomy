# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I046 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I046_SOURCE_COMPLIANCE_ATTESTATION.md`
- `implementation/source_compliance_attestation.py`
- `implementation/test_source_compliance_attestation.py`
- `implementation/RUN_I045_TRANSPORT_HUMAN_REVIEW.md`
- I044 and prior authorization/readiness/capture files named in STATUS.

## I046 result
`source_compliance_attestation.py` adds deterministic offline provenance over I045-compatible source-compliance evidence.

Important behavior:
1. nested I045 evidence hash and first-party HTTPS evidence class are independently revalidated;
2. attestation binds exact source URL, platform, checked/retrieved/attested UTC timestamps, policy conclusion and source-content SHA-256;
3. `manual_metadata_only` is explicitly separated from `reproducible_captured_content`;
4. captured source content is never embedded in the attestation;
5. replay requires exact caller-supplied captured bytes to reproduce the stored digest;
6. stale/non-permitted policy, missing bytes, digest mismatch, chronology errors and tampering fail closed;
7. only `reproducible_evidence_verified` replay exposes an I045 evidence object;
8. eight deterministic tests passed locally;
9. transport/network/authorization remain false and no external action occurred.

## Immediate next run: I047
Build a deterministic offline bridge from I046 replay into I045 human-review state. Require `reproducible_evidence_verified` before `ready_for_human_decision`; preserve exact I044 proposal/scope bindings and prove manual-only metadata cannot reach the ready state. Synthetic fixtures only; no DNS/HTTP.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
