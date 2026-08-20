# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I045 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I045_TRANSPORT_HUMAN_REVIEW.md`
- `implementation/transport_review_packet.py`
- `implementation/test_transport_review_packet.py`
- `implementation/RUN_I044_REAL_TRANSPORT_PROPOSAL.md`
- I043 and prior authorization/readiness/capture files named in STATUS.

## I045 result
`build_real_transport_human_review_packet()` adds a deterministic offline human-audit boundary over I044.

Important behavior:
1. I044 proposal and exact-scope hashes are independently revalidated;
2. scope remains exactly one production GET with no credentials/action;
3. the complete seven-gate I044 set must remain intact;
4. review must occur before proposal expiry;
5. current source-compliance evidence is hash-bound and must use an HTTPS first-party source;
6. evidence must be fresh, UTC-dated, and explicitly confirm anonymous read-only access with no credentials or human-only requirement;
7. inadequate evidence yields `blocked_by_missing_evidence`;
8. adequate evidence yields only `ready_for_human_decision`, never authorization;
9. all future transport/DNS/redirect/resource-limit/receipt gates remain unresolved;
10. eight deterministic tests passed locally, including network-monkeypatch proof that no DNS/HTTP primitive is used;
11. no external action occurred.

## Immediate next run: I046
Build a deterministic offline source-compliance evidence attestation/replay layer. Bind source URL, retrieval/check timestamps, content digest and policy conclusion; distinguish manually supplied metadata from reproducible captured evidence. Keep all fixtures synthetic and transport disabled.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
