# I190 — conservative economics numeric-domain audit

Date: 2026-08-25
Status: **completed audit; concrete fail-open defect identified; patch intentionally deferred to next repository-side run**

## Scope
Audit the first conservative economics path directly consumed by I123: `resource_router.py` (`TaskEconomics`, `ExecutionBackend.effective_success_probability()`, and `quote_backend()`). This is a correctness/safety audit only. No new wrapper, discovery, market observation, credentials, spend, CI dispatch, task action, or value movement.

## Finding
I188 correctly rejects booleans, nonnumeric values, NaN/inf and arithmetic overflow, but several finite values outside their semantic domains are still silently normalized rather than rejected.

### Probability fail-open
`effective_success_probability()` clamps backend `reliability_probability` and `quality_probability` into `[0,1]`. `expected_collect_probability()` likewise clamps `acceptance_probability`, `dispute_probability`, and `nonpayment_probability`.

That means malformed evidence such as:
- `reliability_probability=2.0` becomes `1.0`;
- `quality_probability=2.0` becomes `1.0`;
- `acceptance_probability=2.0` becomes `1.0`;
- `dispute_probability=-1.0` becomes `0.0`;
- `nonpayment_probability=-1.0` becomes `0.0`.

For a conservative production economics gate, silently promoting invalid probability evidence to best-case values is fail-open. These inputs must be rejected, not repaired.

### Negative-cost fail-open
Several monetary/resource fields are passed through `max(0.0, value)`, including backend marginal-cost components and task fees. A malformed negative fee/cost can therefore disappear from conservative accounting instead of invalidating the quote. Examples include negative platform fee, transaction/gas/withdrawal fee, electricity/API/retry/maintenance/opportunity cost, and negative unit cost inputs.

This is especially important downstream of I123 because a quote with silently repaired best-case economics can satisfy `planning_reasons == ()` and participate in production portfolio selection once evidence materializes.

## Required patch contract
The next patch should fail closed before arithmetic:
1. probability fields `reliability_probability`, `quality_probability`, `acceptance_probability`, `dispute_probability`, `nonpayment_probability`, and `minimum_success_probability` must be finite real numbers in `[0,1]`;
2. fee rates must be finite and non-negative; if a rate represents a fraction, explicitly define whether values above `1` are valid rather than silently constraining them;
3. payout, fees, marginal resource costs, electricity, API cost, retry cost, maintenance time, human time value, opportunity cost, units, fixed cost, quota/capacity quantities, latency and rate limits must reject negative values where negative semantics are not explicitly supported;
4. minimum margin thresholds may remain signed only if the project intentionally supports negative thresholds; otherwise make their domain explicit;
5. regression coverage must prove out-of-range finite values fail closed and ordinary valid routes remain unchanged;
6. do not alter I123 authorization/evidence boundaries or enable execution/value movement.

## Safety significance
This is a distinct defect from I188's finite/type hardening and I189's boolean/control-plane hardening. I188 prevents malformed arithmetic types; I190 establishes that semantically impossible but finite numbers can still be promoted into optimistic economics.

## Outcome
A concrete downstream fail-open defect is now isolated with a narrow patch contract. No claim is made that the defect is fixed in I190. Until patched, out-of-domain finite economics/probability values must not be treated as trustworthy production evidence.

## Next action
Patch `implementation/resource_router.py` to enforce semantic numeric domains, add focused regressions, then re-audit I123 selection against the hardened quote contract. Do not proceed to real monetization observation on the basis of silently clamped/repaired economics.