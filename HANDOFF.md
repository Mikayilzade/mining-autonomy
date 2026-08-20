# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I047 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I047_SOURCE_COMPLIANCE_REVIEW_BRIDGE.md`
- `implementation/source_compliance_review_bridge.py`
- `implementation/test_source_compliance_review_bridge.py`
- `implementation/RUN_I046_SOURCE_COMPLIANCE_ATTESTATION.md`
- I045 and prior authorization/readiness/capture files named in STATUS.

## I047 result
`source_compliance_review_bridge.py` adds the provenance barrier between I046 replay and I045 human-review readiness.

Important behavior:
1. I045 packet hash, exact scope hash and one-production-GET/no-credential/no-action scope are revalidated;
2. I046 replay hash/inert state is independently revalidated;
3. `ready_for_human_decision` is preserved only for `reproducible_evidence_verified` + `reproducible_captured_content`;
4. replayed I045 evidence must exactly equal the evidence already bound into the I045 packet;
5. manual-only metadata cannot become human-decision-ready through the bridge;
6. proposal/scope hashes are preserved without widening request count or capabilities;
7. expiry, chronology, hash tampering or evidence mismatch fail closed;
8. eight deterministic tests passed locally;
9. transport/network/authorization/value movement remain false and no external action occurred.

## Immediate next run: I048
Begin the mandatory **Resource / Execution Router** foundation before any real monetization test. Model available execution backends and distinguish fixed/sunk cost from per-task marginal cost. Minimum backend families: deterministic Python/local; local CPU/GPU/model capacity; subscription-backed ChatGPT/Codex as a fixed/limited non-API resource (never assume free programmatic access); cheap external LLM/API; stronger external LLM/API; free-tier CI/cloud; owned PC; future paid VPS/server. Include quota/capacity, latency, reliability/quality probability, parallelism/rate limits, electricity, retry/failure cost, maintenance time, platform/transaction fees, acceptance/non-payment probability and opportunity cost. Keep all execution synthetic/inert.

Future router direction: cheap polling/webhook/WebSocket watchers may operate more frequently than chat automations when platform ToS/API limits allow; local deterministic filtering/deduplication should occur before invoking AI. Do not attempt to bypass product/platform rate limits.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
