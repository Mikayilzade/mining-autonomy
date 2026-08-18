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
Implementation Runs **I001–I004**: COMPLETE.
Project state: **IMPLEMENTATION IN PROGRESS**.

Latest implementation files:
- `implementation/RUN_I004_CROSS_MARKET_EVALUATOR.md`
- `implementation/evaluator.py`
- `implementation/fixtures_i004.json`
- `implementation/test_evaluator.py`
- `implementation/RUN_I003_OKX_A2A_OBSERVABILITY.md`
- `implementation/RUN_I002_PAYANAGENT_READONLY_SAMPLER.md`
- `implementation/RUN_I001_CANDIDATE_RANKING.md`

## I002 result — PayanAgent
PayanAgent's public API contract for discovery, requests and receipts was reconfirmed. Raw public JSON could not be retrieved through the execution environment, so quantitative demand was deliberately left unmeasured rather than inferred. A common opportunity schema + receipt schema v0.1 and demand metrics were defined. PayanAgent remains architecture/dry-run Rank #1, but no money test is justified from the 24k+ supply count alone.

## I003 result — OKX.AI A2A
Current OKX.AI docs and the official open-source Onchain OS task marketplace reconfirm that A2A ASPs can receive/browse open tasks, negotiate, deliver and settle via escrow. Users can create budgeted tasks and use direct, automatic or public matching.

No documented anonymous public task-feed endpoint was established. Provider-side task browsing appears to sit behind legitimate Agentic Wallet/login + ASP identity/listing. Consequently current task density, budgets and organic buyer activity remain unmeasured. Do not create/login/register/fund anything merely to sample the feed without user authorization.

Important OKX gate: real work must not begin before `job_accepted`/escrow state. Arbitration can require a 5% bounty deposit and remains disabled by default for our future stack unless explicitly authorized.

## I004 result — common evaluator v0.1
Executable repository code now implements the first platform-neutral fail-closed decision engine. It includes required-field validation, prohibited-content marker gate, explicit rights confirmation, capability matching, USD/USDC-only payout normalization, bounded token/tool cost estimation, 50% default reserve, absolute + relative margin gates, reject reason codes, dry-run executor/result stubs, ledger-record hashing and a settlement adapter that is hard-disabled and raises.

Nine fixtures and tests cover malformed, prohibited, rights-unknown, unsupported, unknown-payout, negative-margin, positive-margin, unbounded-cost and value-moving cases. The only positive path is `accept_dry_run`; it never executes or settles external work.

Known I004 limitations: policy evidence is still simplified, adapters are not yet concrete, ledger persistence/hash chaining is not yet built, no offline CLI exists, and tests are not yet wired into CI.

## Current shortlist
1. PayanAgent — primary dry-run target; repeat quantitative sampling when raw public feed access is available.
2. OKX.AI A2A ASP — architecture confirmed; provider-side live observation appears onboarding-gated.
3. agent2agent.market — adapter-ready but previously observed 0 open tasks/no activity.
4. AgentGigs.io — technically strong but previously observed 0 jobs; Stripe/KYC geography gate.
5. MCPize — strongest passive paid-endpoint experiment candidate.

Watch/secondary: OKX.AI A2MCP, API Mart, inference suppliers, compute/storage/relay markets.

## Immediate next run
**I005 / E3 hardening.**

Build on the committed evaluator without external credentials:
1. adapter interface + concrete offline payload adapters for PayanAgent / OKX.AI / agent2agent.market-style snapshots;
2. append-only JSONL ledger with deterministic decision IDs and hash chaining;
3. explicit policy evidence states: rights, platform ToS/automation permission, source-data permission;
4. configurable capability + cost profiles;
5. offline CLI for evaluating fixture/snapshot files;
6. tests for duplicates, stale observations, deadlines, zero payout, adversarial text and settlement-disable invariants;
7. add standard-library/CI test execution if feasible.

Do not connect credentials or live execution in I005.

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
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, or publish a monetized service under the user's identity.

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