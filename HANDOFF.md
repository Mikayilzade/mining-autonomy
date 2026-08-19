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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I019 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I019_ENVIRONMENT_ARCHIVE.md`
- `implementation/SOURCES_I019.md`
- `implementation/evidence_archive.py`
- `implementation/test_evidence_archive.py`
- I018 capture/registry and prior bundle/importer/orchestrator/utilization files named in STATUS.

## I019 result
The evidence pipeline now has a deterministic sanitized append-only archive. Capture reports are hash-bound, entries form a SHA-256 chain, duplicate bundle hashes are rejected, canonical JSON import/export is verified, and existing history cannot be rewritten/truncated under append-only comparison.

Environment classification is explicit: `production`, `testnet`, `unknown`. Only `production` observations enter the production scorecard. Testnet and unknown observations are counted as excluded and cannot influence production demand/economics conclusions. Raw platform payloads and buyer identities are not persisted.

Fresh public checkpoint:
- PayanAgent public discovery/receipt mechanics remain documented; raw attributable production demand/utilization remains uncaptured.
- agent2agent.market public zero-open surface is explicitly `base-sepolia`; retain as testnet only.
- MCPize monetization remains documented; attributable utilization remains publisher/dashboard gated.

Eight isolated I019 tests passed locally. Push-triggered CI remains disabled. No workflow change was made. I019 is prepared as one atomic commit.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. AgentGigs.io
5. MCPize

## Immediate next run: I020
Add environment-aware replay/reporting into the unified orchestrator and explicit freshness/age state for production evidence. Continue read-only production demand observation; keep testnet quarantined and do not create accounts/wallets.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
