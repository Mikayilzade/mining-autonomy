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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I023 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I023_MANIFEST_RECEIPTS.md`
- `implementation/SOURCES_I023.md`
- `implementation/sampling_receipt.py`
- `implementation/test_sampling_receipt.py`
- I022 sampling manifest and prior planner/capture/archive/replay files named in STATUS.

## I023 result
The inert sampling manifest now has deterministic canonical JSON serialization, SHA-256 sealing, optional HMAC-SHA256 authentication and per-item hashes bound to the manifest hash + item index.

A new capture-result receipt binds a sanitized bundle SHA-256, source URL/method/platform, expected evidence classes, capture timestamps, environment and transport boundary to the exact sealed manifest item. Receipt hashes are independently verified and never grant execution authority.

There is no built-in HTTP client. `capture_with_injected_transport()` requires an explicit injected transport; network-capable transport is disabled unless a future caller explicitly enables it. Credentials or action-performing results fail closed. Unknown→production environment promotion requires separate environment-evidence hashing.

Local isolated I023 tests: **8 passed**. Push-triggered CI remains disabled and workflow unchanged. I023 is intended as one atomic commit.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I024
Require verified capture receipts at the durable ingestion boundary (`observation_capture` / `evidence_archive`). A sanitized bundle must not enter evidence history unless its receipt verifies against the correct sealed manifest item. Add mismatch/tamper/environment fixtures; keep live transport disabled.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.