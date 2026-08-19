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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I025 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I025_RECEIPT_AUDIT_PROVENANCE.md`
- `implementation/sampling_audit.py`
- `implementation/test_sampling_audit.py`
- `implementation/archive_replay.py`
- `implementation/test_archive_replay.py`
- I024 receipt-gated ingestion files and prior planner/manifest/receipt/archive files named in STATUS.

## I025 result
The sampling/replay audit path is now receipt-aware without changing the durable archive schema.

`sampling_audit_summary()` verifies a sealed manifest and deterministically distinguishes:
1. scheduled-but-uncaptured;
2. receipt-invalid;
3. receipt-valid non-production;
4. receipt-valid production.

Duplicate/tampered/unmatched receipts fail closed. Valid testnet/unknown evidence remains non-production and cannot close a production gap.

`receipt_provenance_index()` accepts only a full receipt-gated capture report, revalidates it through the durable-ingestion validator, then exposes exact manifest-item/receipt hash references and authoritative captured environment.

`archive_replay_report()` can consume such receipt-gated reports and attach verified receipt provenance to matching production rows. Missing receipt provenance is explicit; neither archive evidence nor provenance can authorize execution.

The archive replay tests were migrated from the obsolete pre-I024 unverified report fixture to receipt-gated fixtures.

No live transport/network capture, credentials, KYC, wallets, paid infrastructure, service publication, task acceptance or settlement occurred. Push-triggered CI remains disabled and workflow unchanged.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I026
Create a deterministic end-to-end evidence audit export joining sealed schedule + receipt state + archive membership + replay provenance, with unresolved production gaps reported per source/platform. Keep live transport disabled.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
