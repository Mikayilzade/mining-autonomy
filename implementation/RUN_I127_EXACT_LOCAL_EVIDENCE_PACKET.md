# Implementation Run I127 — exact local evidence packet

Date: 2026-08-23
Status: **COMPLETED AS SOURCE CHECKPOINT — EXECUTION PENDING**
Phase: Implementation / Experiment

## Objective
Turn the I124 fixed local probe plus I126 narrow configuration invariants into one exact I050 evidence packet, then connect a complete packet through I066 and I123 without inventing any missing host facts or creating a production route.

## Changes
Added `i127_exact_local_evidence_packet.py` and focused tests.

The new one-command wrapper can run I124 in an executable current checkout, consume only a verified inert `python_local` probe, convert its measured availability/programmatic-access/latency/reliability/quality/parallelism facts into hash-bound I050 `system_probe` records, merge the exact I126 config-invariant records, attest through I050, and project the result to I123.

If the resulting I050 bundle is complete and reproducible, I127 also verifies it through the existing I066 materialization compatibility path. This remains evidence materialization only: `current_resource_route_created=false`, no market observation and no authorization are created.

## Remaining dynamic gap
With only I124 + I126, the expected exact remaining parameters are:
- `quota_units_remaining`;
- `electricity_per_task_usd`;
- `rate_limit_per_minute`.

I127 accepts optional additional evidence only for those three parameters through a local JSON file. Each supplied record must already be hash-valid and is still revalidated by I050. No synthetic reference value is copied into them.

## Fail-closed rules
- unverified, under-repeated or non-inert I124 probe is rejected;
- I124 probe evidence cannot fill config or electricity facts;
- I126 cannot fill runtime/electricity/quota/rate facts;
- incomplete evidence remains `PASS_BLOCKED` and never reaches I066;
- a complete resource packet still does not prove market demand, positive paid-task economics or explicit authorization.

## Verification
New module and tests passed source compilation before commit. Runtime execution remains unavailable because the current execution container still cannot resolve `github.com` for a fresh checkout.

## Safety
No market DNS/HTTP, credentials, CI dispatch, paid service, task acceptance/submission, KYC, wallet, settlement, spend or value movement occurred.

## Outcome
The resource bootstrap is now operationally one layer away from current host telemetry rather than a loose collection of planning objects. The next executable checkout can run I127 directly, observe the exact three remaining local-resource gaps, and materialize immediately if trustworthy evidence for them is available.

## Next broad stage
At the first exact-current executable checkout run `python implementation/i127_exact_local_evidence_packet.py --root .`. Measure or explicitly source only the three remaining facts where reliable no-spend telemetry/source evidence exists; otherwise keep them unknown. If the packet becomes complete, rerun I123 with the materialized backend and then proceed toward separately authorized fresh market observation. Free/conditional CI capacity remains a separate evidence branch.
