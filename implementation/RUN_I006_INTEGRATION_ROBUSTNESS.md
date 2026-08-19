# Implementation Run I006 — integration & robustness v0.3

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E3**

## Objective
Advance the offline evaluator toward safe live-readiness without credentials or value-moving actions.

## Implemented
- evaluator upgraded to v0.3;
- persistent ledger replay/dedup via `HashChainLedger.seen_keys()` and ledger-aware `evaluate_payloads()`;
- execution-duration-aware deadline gate with configurable duration reserve;
- explicit estimate-confidence field/gate;
- uncertainty increases reserved execution cost, making low-confidence economics conservative;
- capability-level quality contracts for extract/summarize/research and fail-closed missing-contract gate;
- dry-run executor now carries a quality contract and validator requires one;
- adapters carry duration/confidence/token/cost estimate metadata into normalized opportunities;
- regression tests expanded for replay dedup, duration, confidence and quality gates;
- `ADAPTER_CONFORMANCE.md` defines evidence/promotion requirements before any live read-only connector.

## CI note
The GitHub connector available in this run could not enumerate Actions runs through the attempted public fetch endpoint, so no false claim is made that CI passed. Code/test changes are persisted for the workflow to exercise. A later run should inspect workflow status through an available Actions-capable path or independently execute the test suite if a runtime checkout becomes available.

## Fixtures decision
No fabricated fixture is labelled as a real platform snapshot. Existing adapter tests use explicitly synthetic payloads. Realistic sanitized fixtures are deferred until fresh raw responses can be observed legitimately; the conformance contract now makes this requirement explicit.

## Safety state
Still dry-run only. No login, registration, KYC, wallet, bid/accept, task execution, paid API, publication, submission or settlement was performed.

## Outcome
The decision layer can now remember opportunities across process runs, reject insufficiently confident economics, account for execution time against deadlines, and require a result-quality contract before even dry-run acceptance. This closes several ways a naive autonomous worker could repeatedly accept stale/duplicate, deadline-impossible, uncertain-cost or unverifiable work.

Demand/fill rate remains unmeasured and the dominant economic unknown.

## Next run — I007 / E4
Move to the passive MCP microservice benchmark while E1/E2 remain observation-gated:
1. choose 2–3 cheap capabilities suitable for deterministic or tightly bounded execution;
2. model per-call cost, platform share, hosting/API cost and break-even calls/month for MCPize and comparable paid endpoint channels;
3. prefer a capability with no questionable upstream resale/licensing dependency;
4. design an offline microservice + benchmark harness, without publishing or paid infrastructure;
5. preserve a later path to plug the service into the common evaluator/orchestrator.

Project state: **IMPLEMENTATION IN PROGRESS**.