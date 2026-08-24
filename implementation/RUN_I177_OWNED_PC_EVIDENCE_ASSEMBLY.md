# Run I177 — fail-closed owned-PC evidence assembly for I169

Date: 2026-08-24

## Scope

I177 completes the repository-side adapter requested by the I176 checkpoint. It does not create new measurements, infer accounting values, call I050/I066/I123, or touch any market. Its only job is to assemble three already-separated evidence lanes into the existing I169 readiness input without weakening source semantics.

## Inputs

I177 accepts only:

1. a future `PARTIAL_I050_EVIDENCE_READY` I168 result bound to a real I166/I167 source chain and the current I050/I066 source identities;
2. a `PRODUCTION_INTERFACE_CONTROLS_READY` I175 result whose exact I173 executor scope has already been bound through I171;
3. exactly two explicit accounting records:
   - `fixed_monthly_cost_usd`;
   - `sunk_or_already_committed`.

The accounting values are never inferred from ownership, availability, Router defaults, or machine state.

## Interface controls

I177 accepts exactly the five I175 controls:

- `requires_credentials`;
- `requires_paid_account`;
- `requires_new_spend`;
- `quota_units_remaining`;
- `rate_limit_per_minute`.

They must remain `system_probe`, carry non-placeholder source refs and source-content digests, and come from an I175 result with `production_executor_scope_bound=true`.

## Accounting controls

Accounting evidence may use a source class already allowed by current I169. If `provider_first_party` / another current reproducible class is used, a source-content digest remains mandatory. If `user_declared` is truthful, it is preserved as `user_declared` and is never upgraded.

Fixture/example/synthetic/placeholder/dummy/mock-labelled accounting provenance is rejected before I169.

## I169 outcomes preserved

I177 immediately evaluates the assembled seven controls with the existing I169 gate.

Possible meaningful states:

- `ASSEMBLED_READY_FOR_EXACT_I050`: only when I169 returns `READY_FOR_EXACT_I050_EXECUTION`; this permits a later exact I050 attempt only. I066 and I123 remain disabled.
- `ASSEMBLED_DECLARED_ACCOUNTING_BOUNDARY`: when the complete evidence bundle is otherwise valid but the accounting facts remain declarations. Current strict I123 promotion remains blocked.
- `PASS_BLOCKED`: any source drift, missing control, placeholder provenance, wrong source class, invalid timestamp/age, incomplete I175 scope, or I169 validation failure.

I177 never applies the I176 hypothetical hybrid policy proposal.

## Tests

Added `test_i177_owned_pc_evidence_assembly.py` with 7 focused tests covering:

- declared accounting stops at the declared boundary;
- reproducible accounting can reach only exact-I050 readiness;
- missing/placeholder accounting rejection;
- incomplete/non-production I175 scope rejection;
- I168 source/measured-set drift rejection;
- tampered I175 source class/digest rejection;
- invalid timestamp/max-age rejection.

No claim is made here that the full exact Git dependency closure was executed byte-for-byte in this runtime. No CI workflow was dispatched solely for a green result.

## Outcome

The repository now has a complete fail-closed assembly contract from future real owned-PC measurements and exact production-executor interface proof to current I169 readiness. The remaining blocker is no longer evidence plumbing; it is real evidence materialization on the actual owned PC plus truthful accounting provenance.

## Safety / actions not performed

No production market/API request, real credentials, account creation, paid install/service, CI dispatch, infrastructure rental, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Next gate

1. Keep I177 inert until a genuine I168 result exists from the actual user-owned PC.
2. Exact-execute/materialize the I173/I174/I175 source path when exact bytes are available; any source drift requires rebinding.
3. Obtain explicit truthful accounting provenance for the two accounting facts.
4. Feed only those real inputs into I177 -> I169.
5. If I169 reaches strict readiness, execute current exact I050 next; do not jump directly to I066/I123.
6. If the only blocker is the two truthful `user_declared` accounting facts, rebind and review I176 against then-current I050/I123/I172 before any policy change. Do not apply that change prematurely.
