# Implementation Run I004 — cross-market dry-run evaluator v0.1

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E3**

## Objective
Turn the I002/I003 platform-neutral opportunity contract into a credentials-free decision engine that can reject unsafe, unsupported, economically unbounded or value-moving work before any executor is allowed to act.

## Built
- `implementation/evaluator.py` — platform-neutral evaluator;
- `implementation/fixtures_i004.json` — nine synthetic/captured-style fixtures representing PayanAgent / OKX.AI / agent2agent.market-like opportunities and failure cases;
- `implementation/test_evaluator.py` — deterministic assertions for required gates.

## Decision pipeline v0.1
1. required schema fields;
2. explicit prohibited-content marker gate;
3. rights/ToS confirmation gate;
4. capability subset match;
5. payout normalization: only explicit USD/USDC is accepted in v0.1; unknown FX is rejected rather than invented;
6. bounded model/tool cost estimate;
7. 50% default worst-case reserve;
8. minimum absolute margin ($0.25 default) and payout-relative margin (30% default);
9. value-moving-action gate;
10. dry-run executor stub;
11. dry-run result validator;
12. appendable ledger record with hash of normalized opportunity;
13. settlement adapter that always raises and has `enabled = False`.

## Required fixture coverage
The suite contains cases for:
- malformed task;
- prohibited task;
- unknown rights/ToS;
- unsupported capability;
- unknown payout/currency;
- negative/insufficient margin;
- positive simulated margin;
- unbounded external API/tool cost;
- task requiring value-moving action.

The positive fixture is intentionally only `accept_dry_run`: it does not accept external work, execute paid APIs, sign anything or settle value.

## Economics behavior
Cost model v0.1:
`base = input_tokens * input_rate + output_tokens * output_rate + bounded_external_cost`

`reserved_cost = base * (1 + reserve_pct)`

`expected_margin = payout - reserved_cost`

A task fails if expected margin is below either the absolute minimum or the minimum payout-relative ratio. Rates are explicit evaluator inputs; no model/provider price is silently assumed to be current production pricing.

## Safety properties
- Unknown rights => reject.
- Unknown/unsupported payout normalization => reject.
- Unbounded external cost => reject.
- Any opportunity flagged as requiring a value-moving action => reject in v0.1.
- Settlement cannot be called accidentally: adapter is hard-disabled and raises.
- Executor is a stub that reports `executed: false`.

## Limitations / next engineering work
- Policy classification is deliberately conservative and primitive; keyword markers are only an initial fail-closed layer, not sufficient for production.
- No live market adapter is connected yet.
- No live FX oracle is connected.
- No actual LLM/tool executor exists yet.
- Ledger helper returns an appendable record but file persistence/chain integrity is not yet implemented.
- Tests were committed as deterministic Python tests; repository-side CI is not yet configured in this run.

## No-action boundary
No credentials, accounts, KYC, wallets, bids, jobs, paid APIs, paid infrastructure or external value-moving actions were used.

## Result
E3 v0.1 architecture is now represented by executable repository code rather than design prose alone. The stack can normalize a common opportunity object, fail closed on core compliance/economic gates and distinguish a simulated positive-margin opportunity from required rejection classes while keeping execution and settlement disabled.

## Next run — I005 / E3 hardening
1. add adapter interface + concrete fixture adapters for PayanAgent, OKX.AI and agent2agent.market payload shapes;
2. implement append-only JSONL ledger with hash chaining and deterministic decision IDs;
3. separate policy evidence (`rights_status`, `tos_status`, `automation_allowed`) from a single boolean;
4. add configurable capability profiles and cost profiles;
5. add a CLI that evaluates fixture/snapshot files without network or credentials;
6. add tests for duplicate opportunities, stale observations, deadline reserve, zero payout, adversarial text and settlement-disable invariants;
7. if feasible without credentials, add GitHub Actions/standard-library test execution.

Project state: **IMPLEMENTATION IN PROGRESS**.
