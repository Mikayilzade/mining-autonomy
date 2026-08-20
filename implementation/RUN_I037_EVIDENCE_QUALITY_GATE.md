# Implementation Run I037 — deterministic longitudinal evidence-quality/regression gate

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Build a fail-closed offline quality gate over I036 longitudinal attestation history. The gate must classify capture/infrastructure integrity only, require minimum history before assigning a trend, keep economic-demand evidence separate, and emit only an inert recommendation about whether a future explicitly authorized read-only capture could add integrity value.

## Changes
Added `implementation/evidence_quality_gate.py` with:
- independent `history_sha256` verification before evaluation;
- exact I036 schema/mode validation;
- canonical UTC and strictly increasing coverage-timeline validation;
- observation-count/timeline consistency checks;
- recomputation of first-to-last coverage evolution so rehashed mutable counters cannot override timeline evidence;
- transition-frequency validation;
- configurable minimum observation count and minimum elapsed span;
- trend labels: `insufficient_history`, `stable`, `improving`, `regressing`;
- capture-regression and improvement point accounting from missing/rejected/production-gap deltas plus captured-state transitions;
- explicit latest unresolved capture-gap state;
- a separate `economic_evidence_classification = not_evaluated_capture_integrity_is_not_demand` field;
- fail-closed recommendation states for whether another future read-only observation may add capture-integrity value;
- hard-coded `authorization_required = true`, `dry_run_only = true`, `action_enabled = false`, and no-network/no-credentials fields;
- canonical `quality_gate_sha256`.

Added `implementation/test_evidence_quality_gate.py` covering:
1. insufficient sample/span history;
2. improving capture integrity;
3. regressing capture integrity;
4. stable and complete history;
5. stable but incomplete history;
6. raw history-hash tampering;
7. rehashed inconsistent coverage-evolution counters;
8. rehashed non-canonical observation timestamps.

## Verification
An isolated local harness executed the new module tests: **8 passed**. This was not a full repository pytest run and GitHub Actions was not dispatched. Push-triggered CI remains disabled.

## Interpretation rules
- `improving` means capture/evidence availability improved, not that paid demand increased.
- `regressing` means capture/infrastructure evidence quality worsened, not that market demand fell.
- `stable` means the integrity evidence is balanced over the measured span; it says nothing about profitability.
- `insufficient_history` prevents a trend label until both minimum sample count and elapsed span are satisfied.
- Missing/rejected capture remains `unknown_not_negative_demand`.
- A recommendation to repeat is advisory only and cannot authorize DNS/HTTP, credentials, KYC, account actions, bids, publication, payment or settlement.

## Outcome
The I036 longitudinal evidence history now has a deterministic decision gate for evidence-quality trend and future observation value. The stack can decide whether more read-only capture would help diagnose integrity without conflating that decision with economic demand.

## Next run — I038
Build a deterministic authorization-readiness decision packet that combines I037 quality-gate output with the earlier exact I028–I030 capture/readiness contracts. It should identify the smallest exact future read-only capture that would add evidence value, or emit a no-capture-needed state, while preserving exact plan binding, expiry, GET-only/no-credentials/no-action constraints. Do not perform any real network request.

Project state: **IMPLEMENTATION IN PROGRESS**.
