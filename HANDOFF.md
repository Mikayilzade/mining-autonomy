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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I008 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I008_PASSIVE_INTEGRATION.md`
- `implementation/passive_service.py`
- `implementation/test_passive_service.py`
- `implementation/RUN_I007_PASSIVE_MCP_BENCHMARK.md`
- `implementation/mcp_benchmark.py`
- `implementation/evaluator.py`
- `.github/workflows/implementation-tests.yml`

## I008 result
The passive MCP branch now has a reusable dry-run decision layer. It refuses to treat positive per-call contribution as sufficient: unknown utilization produces `demand_unproven`; fixed-hosting break-even and tier capacity are explicit. Publication is hard-disabled. Current normalize-text assumptions yield $0.00799 contribution/call and 1,127 calls/month break-even on $9 fixed hosting. These are synthetic/model economics, not demand evidence.

CI now explicitly installs pytest and runs all implementation tests, but I008 did not inspect a completed Actions run, so green CI remains to be verified.

No live connector, credentials, wallet, paid API, external executor, publication or settlement exists. Demand/fill rate remains the dominant unknown.

## Current shortlist
1. PayanAgent — primary task-market target; quantitative demand pending.
2. OKX.AI A2A ASP — provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; offline benchmark + decision model implemented, real paid utilization unknown.

## Immediate next run: I009
1. Inspect the latest GitHub Actions result for `implementation-tests`; fix real failures if present.
2. Build a small offline orchestrator that consumes both task decisions (`evaluator.py`) and passive-service decisions (`passive_service.py`) into one ranked observation queue while keeping execution/publication disabled.
3. Never invent demand to rank passive services: unknown utilization must remain held/incomparable.
4. Continue read-only attributable demand evidence collection for PayanAgent and MCPize where publicly observable.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, or publish monetized services under the user's identity. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Evidence discipline
Supply/provider counts do not prove demand. Prefer paid buyers, settled receipts, repeat utilization and attributable settlement. Separate organic payments from subsidies. Stablecoin settlement does not prove profit. No Azerbaijan exclusion found is not proof of eligibility. Upstream API/model resale requires independent upstream permission.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.