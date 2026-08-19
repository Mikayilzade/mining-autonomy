# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Do not reopen broad discovery unless implementation exposes a genuinely missing mechanism.
5. Continue Implementation / Experiment Phase from STATUS.
6. Re-check time-sensitive rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I024 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I024_RECEIPT_GATED_INGESTION.md`
- `implementation/SOURCES_I024.md`
- `implementation/observation_capture.py`
- `implementation/evidence_archive.py`
- `implementation/test_evidence_archive.py`
- I023 receipt/sealing files and prior planner/archive/replay files named in STATUS.

## I024 result
The durable evidence boundary is now receipt-gated. `run_verified_capture_batch()` requires `{bundle, manifest_envelope, receipt}` and verifies the receipt against the exact sealed manifest item plus normalized bundle hash/platform/source/timestamps before producing an archive-eligible report.

Plain `run_capture_batch()` remains available for transient offline inspection but explicitly declares itself ineligible for durable archive ingestion.

`evidence_archive.append_capture_report()` independently re-verifies every manifest+receipt pair, requires one attestation per delta, rejects missing/duplicate/unmatched/tampered attestations, and uses receipt `captured_environment` as authoritative. Caller environment mappings may confirm but cannot promote/relabel evidence.

Serialized archives now persist `verified_capture_receipt_required: true` and `environment_policy: receipt_verified_explicit_only`.

No live transport/network capture, credentials, KYC, wallets, paid infrastructure, service publication, task acceptance or settlement occurred. Push-triggered CI remains disabled and workflow unchanged.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I025
Add receipt-derived provenance references to archive replay/audit output and a deterministic sampling audit summary distinguishing scheduled-but-uncaptured, receipt-invalid, receipt-valid non-production and receipt-valid production evidence. Keep live transport disabled.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
