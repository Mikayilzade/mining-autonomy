# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Do not reopen broad discovery unless implementation exposes a genuinely missing mechanism.
5. Continue Implementation / Experiment Phase from STATUS.
6. Re-check time-sensitive rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Mission now
Build a legitimate autonomous server-native earning stack: observe permitted paid tasks/calls, normalize them, estimate execution cost/margin, reject non-compliant/negative-EV work, and eventually execute positive-margin work with minimal human input. Secondary target: passive provider/API/MCP/inference/compute/storage/relay markets.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I011 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I011_SNAPSHOT_REPLAY_CI_DEMAND.md`
- `implementation/fixtures_i011_synthetic_snapshots.json`
- `implementation/snapshot.py`
- `implementation/test_snapshot.py`
- `implementation/RUN_I010_EVIDENCE_INGESTION.md`
- `implementation/orchestrator.py`
- `implementation/evaluator.py`
- `.github/workflows/implementation-tests.yml`

## I011 result
Evidence snapshots now have a fail-closed replay boundary before task adapters. Replay revalidates evidence class, HTTPS source, payload hash, source/capture timestamps, freshness and records-list shape. The trusted snapshot source timestamp overrides timestamps embedded in raw records. Unknown platforms/tampered/stale/malformed snapshots are rejected.

Synthetic fixture snapshots were added and explicitly marked non-real; never count them as demand evidence.

Historical CI diagnosis is strong but not log-proven: commit `f50e42324d4dd2cfb2f43e3932fe602d1a59268c` shows pytest was previously invoked without an explicit installation step and then added. Push-triggered CI remains disabled to prevent email spam. Do not claim green CI until a safely observed manual/PR run succeeds.

Fresh 2026-08-19 first-party checks reconfirmed PayanAgent public discover/offers/receipts interfaces and MCPize monetization/free-hosting mechanics. They did not provide attributable worker-side utilization, so quantitative demand remains unknown.

No live connector, credentials, wallet, paid API, external executor, publication, CI dispatch or settlement exists.

## Current shortlist
1. PayanAgent — primary task-market target; public receipt/discovery surfaces exist, quantitative worker demand pending.
2. OKX.AI A2A ASP — provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; current free hosting tier improves capped-cost feasibility, paid utilization unknown.

## Immediate next run: I012
1. Add a saved-observation importer contract that performs no network calls itself.
2. Add evidence-strength classification such as `settled_receipt`, `open_paid_request`, `listing_only`, `marketing_claim`.
3. Propagate evidence strength into unified audit output so listing/supply cannot rank as utilization.
4. Continue public PayanAgent receipt/request and MCPize demand checks; save a real sanitized snapshot only if raw permitted payload becomes observable.
5. Keep push CI disabled and preserve one-stage/one-final-commit hygiene.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Evidence discipline
Supply/provider counts do not prove demand. Prefer paid buyers, settled receipts, repeat utilization and attributable settlement. Separate organic payments from subsidies. Stablecoin settlement does not prove profit. No Azerbaijan exclusion found is not proof of eligibility. Upstream API/model resale requires independent upstream permission.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.
