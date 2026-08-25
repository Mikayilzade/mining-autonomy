# I192 — Resource Router positive conservative-margin hardening

Date: 2026-08-25
Status: **COMPLETED — OFFLINE / DRY-RUN ONLY**

## Stage goal
Continue the narrow post-I191 audit of the direct Resource / Execution Router economics boundary. Close a concrete fail-open without adding another packaging layer or enabling any live/value-moving action.

## Concrete defect found
I191 intentionally left `minimum_expected_margin_usd` and `minimum_expected_margin_ratio` as signed finite policy thresholds. That allowed a caller to weaken the project-wide economics invariant with negative thresholds. A zero threshold also allowed exactly zero expected margin because the base comparison was `<`, not strict positivity.

This conflicts with the mandatory routing rule: a backend may be selected only when conservative expected economics remain **strictly positive**.

## Change
`implementation/resource_router.py` now:
- validates both minimum margin policy thresholds as finite, non-boolean and non-negative;
- independently requires `expected_margin_before_fixed_allocation_usd > 0` and `expected_margin_ratio > 0` before a quote can be planning-eligible;
- preserves existing inclusive configured minimum-threshold semantics above zero;
- preserves separation of sunk/fixed cost from incremental task economics;
- preserves lowest-marginal-cost selection among eligible positive-margin backends;
- preserves global execution disablement and all credential/spend/paid-account/live blockers.

## Adversarial verification
Added `implementation/test_i192_resource_router_positive_margin.py` covering:
1. negative USD and ratio policy thresholds fail closed;
2. boolean, NaN and infinity thresholds fail closed;
3. exactly zero expected margin cannot route even with zero configured thresholds;
4. a genuinely positive-margin backend still routes in dry-run mode;
5. already-paid/sunk fixed subscription cost is tracked but not charged wholesale per task;
6. the cheapest eligible positive-margin backend remains selected.

Local focused regression: **38 passed in 0.05s** across the retained I191 semantic-domain suite plus I192 tests. No CI workflow was dispatched.

## Safety / economic conclusion
Policy knobs may make the route stricter; they may no longer weaken the invariant below strict positive conservative marginal economics. No real payout, energy, tariff, credentials, registration, task acceptance, settlement or value movement was assumed or executed.

## Remaining risks
- source/evidence promotion at the I123 -> conservative economics/readiness boundary still needs a narrow audit;
- real owned-PC availability/energy/tariff/opportunity-cost evidence remains absent until I181/I166 materialization occurs on the actual PC;
- real marketplace payout, fees, retry/failure, maintenance and acceptance/dispute/nonpayment evidence remains absent;
- bounded read-only production observation is still not authorized.

## Next action
Audit the direct downstream source/evidence-class boundary for manual promotion or synthetic-to-measured laundering. Fix only a concrete fail-open if found. Do not add packaging layers around missing real evidence. The genuine forward path remains I181 on the owned PC, followed by exact evidence materialization and only then separately authorized bounded observation.
