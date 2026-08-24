# I188 — Resource / Execution Router numeric hardening

Date: 2026-08-24
Status: **completed repository-side correctness/safety checkpoint**

## Scope
Audit and harden the base `resource_router.py` arithmetic used underneath I123 so malformed/non-finite economics cannot become a planning-eligible or production-eligible route. This is a distinct correctness defect, not a new packaging layer and not a return to discovery.

## Defect found
The original I048 Router used `max`, `min`, ordinary comparisons and arithmetic directly on caller-supplied numeric fields. Python `NaN`/infinity and booleans can bypass or distort those operations. Examples included:

- `NaN`/infinite marginal-cost components;
- non-finite fixed-cost allocation basis;
- non-finite quota, latency or rate-limit values;
- `NaN` reliability/quality/acceptance/dispute/nonpayment probabilities;
- non-finite payout/fees/minimum margin thresholds;
- multiplication overflow in unit cost, platform-rate fees or expected revenue;
- boolean values being accepted as numeric integers/floats.

Because I123 relies on `quote_backend()` output, this defect sat directly in the Resource / Execution Router path before any real economic test.

## Changes
`implementation/resource_router.py` now:

- requires all arithmetic inputs to be numeric, non-boolean and finite;
- validates optional quota/allocation/rate-limit fields when present;
- fails closed on non-finite multiplication and sums;
- preserves existing clamping semantics for finite probability values while rejecting non-finite/nonnumeric probabilities;
- validates minimum success/margin thresholds as finite;
- validates latency and fixed-cost reference values as finite;
- rejects bool/non-integer `max_parallelism` rather than treating `True` as one worker;
- hardens watcher interval/platform-minimum types without changing the existing no-bypass policy;
- preserves deterministic-first routing, fixed-vs-marginal accounting, all authorization gates and `execution_enabled=False` behavior.

Focused regressions in `test_i188_resource_router_numeric_hardening.py` cover valid routing plus NaN/±Infinity/bool/nonnumeric cost, quota, probability, fee, threshold, latency/rate-limit fields and multiplication overflow.

## Source bindings
- hardened `resource_router.py`: `366a7d5071db02276ecd10d4c66eb3012a4ea7e2`
- I188 regression tests: `5447f4c80c845e84d023ede3f48bbb9aa3e779aa`

## Verification
The current GitHub source was re-read after the patch and the hardened arithmetic/control sections were source-checked. A byte-identical local pytest run was attempted through the normal raw GitHub transport, but the current execution environment could not resolve `raw.githubusercontent.com` (`curl: Could not resolve host`). Therefore this checkpoint does **not** claim a full pytest PASS. CI was not dispatched merely to obtain green status.

## Safety / external actions
No market/API observation, credentials, paid account, software/hardware purchase, CI dispatch, account creation, KYC/wallet action, task acceptance/fulfillment, paid infrastructure, settlement, spend or value movement occurred.

## Outcome
The base Router no longer permits non-finite/artificial numeric economics to silently survive quote construction. This strengthens every downstream portfolio decision that consumes I048 quotes, including I123.

## Risks / remaining blockers
This patch does not create real evidence. The genuine blockers remain the actual owned-PC energy route, real availability/tariff/opportunity-cost/accounting provenance, exact I178/I179 evidence materialization, exact I050/I066, and later real task payout/fee/retry/acceptance/dispute/nonpayment observations under separate authorization.

## Next action
Do not add another abstraction layer unless a distinct defect is found. The real forward step remains on the actual owned PC: run I181; use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative meter; then supply genuine tariff/availability/opportunity-cost/accounting provenance and run exact I178/I179. If repository-side work continues before that real run, audit direct downstream Router consumers only for concrete fail-open behavior rather than repackaging missing evidence.
