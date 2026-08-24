# I172 — Owned-PC Narrow Hybrid Evidence Contract

Date: 2026-08-24
Status: **completed review-only policy checkpoint**

## Goal
Execute the exact repository-side next action from I170: define and test the narrowest possible owned-PC hybrid evidence contract without changing I050 or I123 and without creating any production authorization.

## Contract
The proposed review boundary is restricted to backend `owned_pc` only.

`user_declared` provenance may appear only for:
- `fixed_monthly_cost_usd`;
- `sunk_or_already_committed`.

Every other I050 critical parameter must remain in current reproducible source classes (`provider_first_party`, `measured_local`, `system_probe`) and reproducible records must carry a source-content digest.

The contract explicitly cannot:
- apply to `python_local`, external APIs, free-tier CI, subscription assistant, local-model or VPS backends;
- convert a dynamic/resource/interface fact into `user_declared` evidence;
- consume or create credentials authorization;
- consume or create spend authorization;
- consume or create infrastructure authorization;
- modify I050;
- modify I123;
- enable I123 promotion or production execution.

## Results
Two valid review states exist:
1. `NARROW_HYBRID_REVIEW_READY` — all non-accounting facts are reproducible and one/both accounting facts genuinely remain `user_declared`.
2. `STRICT_REPRODUCIBLE_PATH_AVAILABLE_NO_HYBRID_NEEDED` — even the accounting facts have acceptable reproducible/provider-first-party provenance, so no hybrid exception is needed.

Any declaration outside the two accounting parameters fails closed.

Focused logic verification: **7 passed** in the current local runtime. The local test materialization exercised the authored logic but this run does not claim a new exact-Git-blob byte-for-byte execution closure.

## I171 relationship
I171 was added in the same continuation as an extra safety prerequisite: benchmark-only source evidence cannot be substituted for a future production task executor. The five I170 interface controls must ultimately be bound to the exact production-scoped deterministic executor and its acceptance contract.

## Safety
No market/API request, credentials, CI dispatch, paid install, account creation, infrastructure rental, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Next action
Keep I050/I123 unchanged. Build or select one concrete deterministic offline/dry-run executor for a permitted task family with machine-checkable acceptance criteria, bind its complete source closure through I171, and then compare the strict I050 path against the I172 review-only hybrid proposal. Any future policy patch must remain `owned_pc`-only and prove by tests that no other backend, source class, or authorization gate can widen.
