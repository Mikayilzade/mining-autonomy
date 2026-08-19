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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I021 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I021_SAMPLING_WATCHLIST_PLANNER.md`
- `implementation/SOURCES_I021.md`
- `implementation/sampling_planner.py`
- `implementation/test_sampling_planner.py`
- I020 replay/freshness bridge and I019 archive files named in STATUS.

## I021 result
The offline stack now has a deterministic production-evidence watchlist planner. It ranks observation work by platform priority, explicit production-evidence presence, freshness, positive-open-demand gap and paid-utilization gap.

Testnet/unknown observations never satisfy a production gap. The planner is plan-only: `network_calls_performed=False`, `action_enabled=False`, and it contains no HTTP client, credentials, task acceptance, service publication or settlement path.

Fresh public checkpoint:
- PayanAgent public discovery/receipt and request/bid/fulfill mechanics remain documented; attributable raw production demand/utilization is still uncaptured.
- MCPize still documents standard 80% creator share and Base x402 pay-per-call; 900+ server / 450+ publisher counts remain supply-only.
- agent2agent.market testnet evidence remains quarantined.

Push-triggered CI remains disabled. Workflow unchanged. I021 is one atomic commit.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I022
Build an inert deterministic sampling manifest/execution contract from the watchlist. Include source URL, expected evidence class, freshness/capture deadline, rate-limit budget and provenance requirements. The manifest may describe public read-only checks but must not execute them. Future successful permitted captures should flow through `observation_capture` → evidence archive → production-only replay.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
