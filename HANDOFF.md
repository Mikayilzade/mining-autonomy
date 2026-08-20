# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I037 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I037_EVIDENCE_QUALITY_GATE.md`
- `implementation/evidence_quality_gate.py`
- `implementation/test_evidence_quality_gate.py`
- `implementation/RUN_I036_ATTESTATION_HISTORY.md`
- I036/I035/I034 and prior receipt-gated capture/archive files named in STATUS.

## I037 result
The stack now has a deterministic offline quality/regression gate over I036 same-plan longitudinal capture histories.

Important behavior:
1. I036 `history_sha256` is revalidated before evaluation;
2. history mode/schema, coverage timeline, canonical UTC chronology and observation counts fail closed on mismatch;
3. first-to-last coverage evolution is recomputed from the timeline, so rehashed mutable counters cannot override evidence;
4. minimum observation count and elapsed span are both required before assigning a trend;
5. capture integrity is labeled `insufficient_history`, `stable`, `improving` or `regressing`;
6. missing/rejected/production-gap deltas and captured-state transitions contribute only to capture-integrity scoring;
7. economic demand is explicitly `not_evaluated_capture_integrity_is_not_demand`;
8. latest unresolved capture gaps remain visible;
9. a recommendation to repeat a future read-only capture is advisory only and always requires separate explicit authorization;
10. no DNS/HTTP, credentials or action path exists in I037;
11. eight deterministic I037 tests passed in an isolated local harness.

## Immediate next run: I038
Create a deterministic authorization-readiness decision packet that combines I037 quality-gate output with the exact I028–I030 capture/readiness contracts. Select the smallest exact future read-only observation that could add integrity evidence value, or emit no-capture-needed. Preserve exact plan hash, expiry, GET-only, no-credentials and no-action semantics. Perform no network request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
