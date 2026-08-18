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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I005 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I005_EVALUATOR_HARDENING.md`
- `implementation/evaluator.py`
- `implementation/evaluate_cli.py`
- `implementation/test_evaluator.py`
- `.github/workflows/implementation-tests.yml`
- prior I001–I004 reports named in STATUS.

## I005 result
Evaluator v0.2 is now an offline cross-market skeleton. It adds PayanAgent/OKX A2A/agent2agent.market-style adapters, explicit policy evidence states (`rights_status`, `tos_status`, `automation_allowed`, `source_data_permission`), configurable capability/cost profiles, stale/deadline/duplicate gates, deterministic decision IDs, append-only hash-chained JSONL ledger + verification, offline CLI, stronger hard-disabled settlement invariants, expanded tests and CI workflow.

Adapters are captured-style mappings, not claims that current private/live payload schemas are identical. Conformance must be checked against fresh raw snapshots before live use. No live connector, credentials, wallet, paid API, external executor or settlement exists. Demand/fill rate remains the dominant unknown.

## Current shortlist
1. PayanAgent — primary dry-run target; quantitative demand pending.
2. OKX.AI A2A ASP — architecture confirmed; provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle but prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive paid-endpoint experiment candidate.

## Immediate next run: I006 / E3 integration & robustness
1. Inspect CI/test result and repair failures.
2. Add realistic sanitized snapshots for all three adapters and CLI regression coverage.
3. Add persistent ledger replay/dedup across runs.
4. Add deadline-aware estimated execution duration and confidence/risk reserve.
5. Add result-quality contract/validator stubs per capability.
6. Define adapter conformance contract for future read-only live connectors.
7. If public raw PayanAgent data becomes observable without credentials, sample read-only; otherwise continue without blocking.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, or publish monetized services under the user's identity. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Evidence discipline
Supply/provider counts do not prove demand. Prefer paid buyers, settled receipts, repeat utilization and attributable settlement. Separate organic payments from subsidies. Stablecoin settlement does not prove profit. No Azerbaijan exclusion found is not proof of eligibility. Upstream API/model resale requires independent upstream permission.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.