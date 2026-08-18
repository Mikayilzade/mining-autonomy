# Implementation Run I005 — evaluator hardening v0.2

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E3**

## Objective
Harden the credentials-free common evaluator from I004 into a reusable offline decision layer before any live market or value-moving integration.

## Implemented
- `evaluator.py` upgraded to v0.2.
- Explicit policy evidence states replace the old single rights boolean: `rights_status`, `tos_status`, `automation_allowed`, `source_data_permission`. Unknown evidence fails closed.
- `CapabilityProfile` and `CostProfile` make capabilities, token rates, reserve and margin thresholds configurable.
- Offline adapter interface and concrete adapters added for PayanAgent-, OKX A2A-, and agent2agent.market-style payloads. These are payload-shape adapters only; no claim is made that private/current live schemas exactly match without fresh snapshots.
- Freshness, deadline-reserve and duplicate gates added.
- Zero/negative payout rejects explicitly through the payout gate.
- Append-only JSONL `HashChainLedger` added with deterministic decision IDs, opportunity hashes, previous-record hashes and verification/tamper detection.
- `evaluate_cli.py` added for credentials-free local snapshot evaluation and optional ledger persistence.
- Settlement invariant strengthened: both `enable()` and `settle()` raise; no value-moving implementation exists.
- Tests expanded for policy, prohibited/adversarial text, unsupported capability, payout, unbounded cost, value action, stale observation, deadline reserve, duplicate detection, configurable economics, adapters, ledger chain/tampering, executor and settlement invariants.
- GitHub Actions workflow added for implementation tests.

## Safety state
Still **dry-run only**. There is no account login, bid/accept call, paid API call, wallet, KYC, settlement, external executor or live task submission in this stack.

## Engineering caveats
1. Adapter field mappings are deliberately offline/captured-style and must be reconciled against fresh raw payloads before any live read-only connector is considered production-grade.
2. Keyword prohibited-content detection is defense-in-depth only, not a sufficient production policy classifier.
3. Hash chaining is tamper-evident relative to the stored chain, not an externally anchored immutable log.
4. Token cost defaults are explicit test defaults, not claims about current provider prices.
5. CI execution result should be checked on a later run; committing a workflow is not proof it passed.

## Outcome
The project now has a platform-neutral offline skeleton capable of taking heterogeneous task snapshots, normalizing them, applying fail-closed compliance/economic gates, deduplicating observations, recording decisions in a verifiable chain, and producing only dry-run acceptance decisions.

No real economics have been demonstrated yet. Demand/fill rate remains the dominant unknown.

## Next run — I006
Perform an offline integration/robustness pass:
1. inspect CI/test result and fix failures;
2. add realistic sanitized snapshot fixtures for all three adapters and CLI regression tests;
3. add ledger replay/dedup state across runs rather than only in-memory duplicates;
4. add deadline-aware estimated execution duration and confidence/risk reserve;
5. add a result-quality contract/validator stub per capability;
6. define adapter conformance contract needed before a future read-only live connector;
7. if public raw PayanAgent data becomes observable without credentials, sample it read-only; otherwise do not block I006 on it.

Project state: **IMPLEMENTATION IN PROGRESS**.
