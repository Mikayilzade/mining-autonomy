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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I027 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I027_PRODUCTION_GAP_PRIORITIZER.md`
- `implementation/gap_prioritizer.py`
- `implementation/test_gap_prioritizer.py`
- `implementation/RUN_I026_EVIDENCE_AUDIT_EXPORT.md`
- I025–I026 receipt/replay/audit files and prior receipt-gated archive/planner/manifest files named in STATUS.

## I027 result
`prioritize_production_gaps()` now consumes the I026 audit plus the exact sealed sampling manifest and produces a deterministic next-work plan.

Important behavior:
1. manifest hash, source URL, item index and manifest-item hash must all match;
2. only scheduled GET/no-credential/no-action items are eligible;
3. unresolved production gaps are scored by platform priority + evidence value + freshness urgency + conservative source rate budget;
4. gaps needing a new observation are separated from archive/provenance gaps repairable offline;
5. the selected observation queue is globally capped and lower-ranked observations are explicitly deferred;
6. missing evidence remains `unknown_not_negative_demand`;
7. all output remains plan-only with network/action/credentials disabled.

No live transport/network capture, credentials, KYC, wallets, paid infrastructure, service publication, task acceptance or settlement occurred. Push-triggered CI remains disabled and workflow unchanged.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I028
Build a deterministic capture-readiness packet from I027-selected observations. Preserve exact GET source, evidence class, environment/provenance requirements and rate budget, and classify whether a future explicitly-authorized read-only capture is technically ready or blocked by an observability/environment gate. Still do not perform the network request.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
