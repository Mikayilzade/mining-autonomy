# Run I173-I176 — concrete offline executor, exact interface proof path, and hybrid comparator

Date: 2026-08-24

## Scope

This run completes the repository-side action that followed I172 without calling a production market or changing I050/I123 policy.

### I173 — concrete deterministic executor

Selected an existing Router capability, `transform`, and defined a concrete permitted offline/dry-run task family: `structured_json_normalization_v1`.

Executor identity:
- `owned-pc-structured-json-normalizer-v1`
- acceptance contract: `structured-json-normalization-acceptance-v1`
- source: `implementation/i173_structured_json_transform_executor.py`
- exact current Git blob: `29485940ac92c26616a9b60ee9e309110a4fbe62`

The executor validates non-empty structured records, normalizes/sorts them deterministically, computes exact count/sum/checksum, and accepts an artifact only if independent recomputation exactly matches. It is dry-run only and contains no market/task acceptance, submission, settlement or value-moving path.

### I174 — exact-source interface probe

Added a source-only probe bound to the exact I173 Git blob. It does not import or execute the target. The probe:
- recomputes Git blob SHA over target bytes;
- parses the target AST;
- permits only a narrow pure-stdlib import whitelist;
- rejects dynamic import/eval/exec/open/input and known network/process/filesystem dependency roots;
- verifies executor/task/acceptance identities;
- verifies inert `ExecutionResult` defaults;
- fails closed on any source drift.

Only for the exact I173 closure it may project these five I170 interface facts:
- `requires_credentials = false`
- `requires_paid_account = false`
- `requires_new_spend = false`
- `quota_units_remaining = None` meaning provider quota not applicable, not infinite host capacity
- `rate_limit_per_minute = None` meaning provider rate limit not applicable, not infinite throughput

A defect found during self-review was fixed: source closure can no longer remain marked complete after target blob drift.

Current I174 blob after the fix: `569ec58988abdfa055cd172358a39ed88e36e5f3`.

### I175 — I171 production-scope binding

Added a fail-closed bridge from an accepted I174 proof into current I171 `production_task_executor` scope. It binds:
- exact I173 path/blob;
- executor identity;
- `structured_json_normalization_v1` task family;
- machine-checkable acceptance-contract identity;
- I174 source digest/interface probe identity.

Only after I171 returns `PRODUCTION_EXECUTOR_SCOPE_BOUND` does I175 emit the five interface facts as `system_probe` facts. I175 creates no I050 records, executes no I066 materialization, and cannot promote I123.

Current I175 blob: `f8b70be5a16479feb1ebeed8489d68bcdcd5ff33`.

### I176 — review-only narrow hybrid patch comparator

No patch was applied. I176 models the narrowest hypothetical future exception for comparison only:
- backend must be exactly `owned_pc`;
- only `fixed_monthly_cost_usd` and `sunk_or_already_committed` may remain `user_declared`;
- every other I050 critical parameter must remain in current reproducible source classes;
- I172 must already be `NARROW_HYBRID_REVIEW_READY` and digest-bound;
- non-synthetic, capacity, current policy and credential/spend/infrastructure gates remain unchanged;
- no I050/I123 source is edited and no promotion is performed.

The comparator also preserves the existing all-reproducible strict path unchanged.

Current I176 blob: `671304a98e0090a0b2dc144eac8dae630d45b7cb`.

## Tests

Focused tests were added for I173, I174, I175 and I176: 19 test functions total. They cover deterministic acceptance, tamper rejection, exact blob drift, forbidden dependency rejection, benchmark/executor substitution, non-owned-PC rejection, declaration-scope confinement, non-synthetic/capacity/policy preservation and credential/spend authorization preservation.

This run does **not** claim a new exact-local 19/19 execution closure. The repository connector supplies exact current source identity, but the full exact checkout/materialization needed to execute all new test modules locally was not materialized in this runtime. No CI workflow was dispatched merely to obtain a green result.

## Outcome

The previous blocker “no concrete deterministic production-shaped executor + acceptance contract” is resolved at repository design/source level. The previous five I170 interface controls now have an exact-source, production-scope proof path tied to I173, rather than benchmark-only I163 evidence.

They are still not real I050 evidence until I174/I175 are actually executed against exact source bytes and then bound to the real owned-PC I166/I168 resource packet.

The two accounting facts remain intentionally separate and truthful. The proposed hybrid exception remains review-only and unapplied.

## Safety / actions not performed

No production market/API request, credentials, account creation, paid install/service, CI dispatch, infrastructure rental, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Next gate

1. Exact-source execute I173/I174/I175 focused path when a byte-materialized checkout is available; any I173 source drift invalidates I174/I175 proof bindings.
2. Real user-PC path remains I166/I165 -> I167 -> I168.
3. Combine future real I168 measured records with exact production-scoped I175 interface facts and truthful accounting evidence, then evaluate I169.
4. Do not apply any I050/I123 hybrid patch unless the real path reaches exactly the two accounting declarations as the only remaining source-class blocker; if it does, rebind I176 to then-current I050/I123/I172 blobs and rerun non-widening tests before review.
