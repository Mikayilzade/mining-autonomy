# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Do not reopen broad discovery unless implementation exposes a genuinely missing mechanism.
5. Continue Implementation / Experiment Phase from STATUS.
6. Re-check time-sensitive rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I020 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I020_ARCHIVE_REPLAY_FRESHNESS.md`
- `implementation/SOURCES_I020.md`
- `implementation/archive_replay.py`
- `implementation/test_archive_replay.py`
- I019 archive and prior capture/registry/importer/orchestrator files named in STATUS.

## I020 result
Sanitized archive evidence can now be replayed into the offline orchestrator without contaminating production conclusions. Testnet/unknown entries are excluded before replay. Latest production evidence gets explicit `fresh`, `stale`, or `future_invalid` age state.

Archive-derived `ObservationItem` records are intentionally HOLD-only and can never enable action because sanitized evidence lacks raw executable payloads, trusted policy context and bounded execution-cost estimates. Paid utilization can be reported as evidence, but archive replay does not sum values across snapshots or infer profitability.

Fresh public checkpoint:
- PayanAgent public discovery/receipt and request/bid/fulfill mechanics remain documented; attributable raw production demand/utilization is still uncaptured.
- MCPize still documents standard 80% creator share and Base x402 pay-per-call; current 900+ server / 450+ publisher counts are supply only, not paid utilization.
- agent2agent.market `base-sepolia` evidence remains testnet-only and quarantined.

Push-triggered CI remains disabled. Workflow unchanged. I020 is prepared as one atomic commit.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. AgentGigs.io
5. MCPize

## Immediate next run: I021
Build a deterministic read-only sampling/watchlist planner driven by evidence freshness, missing evidence class and candidate priority. The planner should emit what to re-check and why, but must not perform network calls or enable actions. Continue public production observation where anonymously accessible.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
