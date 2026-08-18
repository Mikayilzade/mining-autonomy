# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, and the latest implementation/research files named in STATUS.
3. Trust repository state over chat memory.
4. `STATUS.md` is authoritative.
5. Discovery/research is COMPLETE. Do **not** reopen broad discovery unless implementation exposes a genuinely missing mechanism or the user explicitly requests a refresh.
6. Continue the Implementation / Experiment Phase from the exact queue/checkpoint in STATUS.
7. Re-check time-sensitive platform rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Mission now
Build toward a legitimate autonomous server-native earning stack. Primary target: an agent that can programmatically observe permitted paid tasks/calls, normalize them, estimate execution cost and expected margin, reject non-compliant/negative-EV work, and eventually execute positive-margin work with minimal human input.

Secondary target: passive provider/API/MCP/inference/compute/storage/relay markets.

## Current checkpoint
Discovery Runs **001–062**: COMPLETE.
Implementation Runs **I001–I002**: COMPLETE.
Project state: **IMPLEMENTATION IN PROGRESS**.

Latest implementation files:
- `implementation/RUN_I002_PAYANAGENT_READONLY_SAMPLER.md`
- `implementation/RUN_I001_CANDIDATE_RANKING.md`

## I002 result
PayanAgent's public API contract for discovery, requests and receipts was reconfirmed. Raw public JSON could not be retrieved through the current execution environment, so quantitative demand was deliberately left unmeasured rather than inferred. A common opportunity schema + receipt schema v0.1 and demand metrics were defined. PayanAgent remains architecture/dry-run Rank #1, but no money test is justified from the 24k+ supply count alone.

## Current shortlist
1. PayanAgent — primary dry-run target; repeat quantitative sampling when raw public feed access is available.
2. OKX.AI A2A ASP — immediate live-task observability target.
3. agent2agent.market — adapter-ready but previously observed 0 open tasks/no Base Sepolia activity.
4. AgentGigs.io — technically strong but previously observed 0 jobs; Stripe Connect geography/KYC gate.
5. MCPize — strongest passive paid-endpoint experiment candidate.

Watch/secondary: OKX.AI A2MCP, API Mart, inference suppliers, compute/storage/relay markets.

## Immediate next run
**I003 / E2: OKX.AI A2A ASP task-intake observability.**

Goals:
- use current official sources first;
- determine whether open tasks/order intake can be observed without registration, Agentic Wallet, deposits or acceptance;
- quantify task count, recency, prices/bounties and categories if public surfaces expose them;
- map any observable fields to the I002 common opportunity schema;
- document geography/KYC/onboarding unknowns rather than guessing;
- no account creation, wallet creation/funding, task acceptance, bidding, arbitration deposit or other value-moving action.

If live raw task data is inaccessible, capture the official contract/workflow and proceed with E3 adapter/evaluator fixtures rather than stalling.

## Architecture direction
Platform-neutral components:
1. market adapter;
2. opportunity normalizer;
3. policy/compliance gate;
4. cost estimator;
5. conservative EV/margin engine;
6. capability router;
7. dry-run executor initially;
8. result validator;
9. settlement adapter disabled until explicit authorization;
10. ledger of observed opportunity, decision, estimated/actual cost, payout and realized margin.

## Hard action boundary
Without explicit user authorization do NOT:
- spend money or purchase credits;
- create/fund wallets or sign value-moving transactions;
- stake/deposit collateral;
- rent paid server/GPU infrastructure;
- create paid accounts;
- submit KYC/bank onboarding;
- accept paid work with liability/slashing risk;
- publish a monetized service under the user's identity.

Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue autonomously.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting of human-only work contrary to ToS.

## Evidence discipline
- Supply/listing/provider counts do not prove demand.
- Prefer distinct paid buyers, settled receipts, repeat utilization and attributable settlement.
- Separate organic customer payments from emissions/subsidies/points.
- Stablecoin settlement does not prove profit.
- No Azerbaijan exclusion found is not proof of Azerbaijan eligibility.
- Upstream API/model resale requires independent upstream permission.

## Completion
Implementation Phase is COMPLETE only when either a real permitted autonomous test demonstrates positive economics with the stack documented, or all reasonable candidates are exhausted and control passes confirm no viable implementation. Until then continue staged work and persist every checkpoint.