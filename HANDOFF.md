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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I012 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I012_DEMAND_EVIDENCE_IMPORTER.md`
- `implementation/demand_evidence.py`
- `implementation/observation_importer.py`
- `implementation/orchestrator.py`
- `implementation/test_demand_evidence.py`
- `implementation/test_observation_importer.py`
- `implementation/test_orchestrator.py`
- `implementation/RUN_I011_SNAPSHOT_REPLAY_CI_DEMAND.md`
- `implementation/snapshot.py`

## I012 result
Demand evidence is no longer implicit. `settled_receipt` and `paid_invocation` prove attributable paid utilization; `open_paid_request` proves current paid buyer demand; `listing_only`, `marketing_claim`, and `unknown` do not prove demand. Unsupported custom labels fail closed.

Saved observation envelopes can now be imported offline and revalidated for exact schema, HTTPS provenance, payload hash and freshness before use. Only `open_paid_request` evidence can be replayed into task adapters as current work.

The orchestrator propagates evidence strength and separately records `paid_utilization_proven` and `open_paid_demand_proven`. Positive-margin task payloads are held without open-request evidence. Passive projected economics are held without attributable utilization evidence. Audit output counts these evidence classes separately.

Fresh 2026-08-19 first-party checks reconfirmed PayanAgent request/receipt surfaces and MCPize seller/pay-per-call/free-hosting mechanics, but no raw attributable demand/utilization snapshot was captured; quantitative demand remains unknown.

Push-triggered CI remains disabled to avoid email spam. No workflow change or manual CI dispatch occurred. Changed Python files passed local syntax compilation; green Actions CI is not claimed.

## Current shortlist
1. PayanAgent — primary task-market target; public request/receipt surfaces exist, quantitative worker demand pending.
2. OKX.AI A2A ASP — provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; free hosting improves capped-cost feasibility, paid utilization unknown.

## Immediate next run: I013
1. Add an evidence-aware replay-to-orchestrator bridge so imported `open_paid_request` snapshots can become dry-run queue items without manual tuple construction.
2. Add receipt/utilization aggregation for saved `settled_receipt` / `paid_invocation` observations (count, value, recurrence, concentration) while keeping identities sanitized.
3. Continue public PayanAgent receipt/request and MCPize utilization checks; save a real sanitized snapshot only if raw permitted data becomes observable.
4. Preserve one-stage/one-final-commit hygiene and do not re-enable push CI.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Evidence discipline
Supply/provider counts do not prove demand. Open paid requests and settled utilization are different evidence classes. Prefer attributable paid buyers, settled receipts, repeat utilization and settlement value. Separate organic payments from subsidies. Stablecoin settlement does not prove profit. No Azerbaijan exclusion found is not proof of eligibility. Upstream API/model resale requires independent upstream permission.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.
