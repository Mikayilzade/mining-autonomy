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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I013 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I013_EVIDENCE_REPLAY_UTILIZATION.md`
- `implementation/receipt_aggregation.py`
- `implementation/orchestrator.py`
- `implementation/test_i013_bridge.py`
- `implementation/test_receipt_aggregation.py`
- `implementation/RUN_I012_DEMAND_EVIDENCE_IMPORTER.md`
- `implementation/demand_evidence.py`
- `implementation/observation_importer.py`
- `implementation/snapshot.py`

## I013 result
Imported `open_paid_request` snapshots now bridge directly into the unified dry-run orchestrator after provenance/hash/freshness/shape revalidation; the trusted snapshot source timestamp overrides record timestamps and non-open-demand evidence fails closed.

Imported `settled_receipt` / `paid_invocation` snapshots now support strict offline utilization aggregation: transaction count, total/average/median USD value, active days, first/last observation, hashed-buyer recurrence and top-buyer value concentration. Raw buyer/customer/wallet/payer identifiers are rejected; retained recurrence identifiers must already be SHA-256 hashes.

Fresh 2026-08-19 first-party checks reconfirmed PayanAgent public receipt/request mechanics and MCPize subscription/x402 seller mechanics. No attributable raw request/receipt/invocation dataset was captured; quantitative demand remains unknown.

Push-triggered CI remains disabled. No workflow change or manual CI dispatch occurred. The prepared single git commit was blocked by the connector after blob/tree creation, so the stage was persisted with multiple Contents API commits as an exception; those pushes do not trigger current CI.

## Current shortlist
1. PayanAgent — primary task-market target; quantitative worker demand pending.
2. OKX.AI A2A ASP — provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; paid utilization unknown.

## Immediate next run: I014
1. Add normalized platform-specific sanitizer/parser boundaries for future permitted raw PayanAgent request and receipt payloads.
2. Add comparison across multiple saved utilization snapshots without extrapolating mismatched observation windows.
3. Continue public PayanAgent receipt/request and MCPize utilization checks; save real sanitized snapshots only if raw permitted data becomes observable.
4. Prefer one-stage/one-final-commit and do not re-enable push CI.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
