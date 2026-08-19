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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I007 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I007_PASSIVE_MCP_BENCHMARK.md`
- `implementation/mcp_benchmark.py`
- `implementation/test_mcp_benchmark.py`
- `implementation/RUN_I006_INTEGRATION_ROBUSTNESS.md`
- `implementation/ADAPTER_CONFORMANCE.md`
- `implementation/evaluator.py`
- `.github/workflows/implementation-tests.yml`

## I007 result
Passive MCP E4 now has an offline deterministic microservice/economics harness. Current MCPize primary sources were rechecked: standard creator share is 80%, documented x402 minimum is $0.01/tool call, Base Sepolia testing is available, and current FAQ advertises a $0 hosting tier. Three bounded local tools (`normalize_text`, `json_stats`, `csv_profile`) avoid upstream API/model resale. Under conservative synthetic marginal-cost reserves, unit contribution at $0.01 is about $0.00797–$0.00799; $9/month fixed hosting would require roughly 1.13k paid calls/month. This is only break-even math: paid demand is still unproven. Tests are committed but were not executed in the connector-only environment.

No live connector, credentials, wallet, paid API, external executor, publication or settlement exists. Demand/fill rate remains the dominant unknown.

## Current shortlist
1. PayanAgent — primary task-market target; quantitative demand pending.
2. OKX.AI A2A ASP — provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; offline benchmark implemented, real paid utilization unknown.

## Immediate next run: I008 / E4 integration
1. Integrate the bounded passive capabilities with the common evaluator/orchestrator contract.
2. Add a passive-service decision model for price, creator share, variable cost, fixed hosting and minimum margin; compare free vs paid hosting tiers.
3. Inspect/update `.github/workflows/implementation-tests.yml` so evaluator and MCP benchmark tests are structurally runnable.
4. Collect public comparable MCP prices/demand signals where possible, but distinguish listings/first-party claims from attributable paid utilization.
5. Keep publication, account creation, KYC, wallet funding and monetized deployment disabled.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, or publish monetized services under the user's identity. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Evidence discipline
Supply/provider counts do not prove demand. Prefer paid buyers, settled receipts, repeat utilization and attributable settlement. Separate organic payments from subsidies. Stablecoin settlement does not prove profit. No Azerbaijan exclusion found is not proof of eligibility. Upstream API/model resale requires independent upstream permission.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.