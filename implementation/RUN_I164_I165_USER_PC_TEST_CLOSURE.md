# Run I164-I165 — lightweight benchmark core + one-shot user-PC materializer

Date: 2026-08-24

## Objective
Close the pending I163 focused-test blocker without dispatching CI, then reduce the user-PC materialization path to one local command while preserving fail-closed external-measurement boundaries.

## I164 outcome
I163 previously imported `python_local_calibration_fixture.py` only to reuse the fixed JSON-transform benchmark primitives. That pulled a much larger calibration/router import graph into the focused benchmark tests.

I164 extracts those pure primitives into `i164_fixed_benchmark_core.py` and changes I163 to import only the lightweight core. The benchmark identity and deterministic expected digest remain unchanged:

`30b102b8e451d052387927e05e57ee4e5e7e046b0c3e15869a1684a9d52fa419`

Exact connector-materialized focused closure was verified by Git blob SHA:

- `i159_owned_pc_evidence_packet.py` — `b2b9e1a5a7808f75b935751cca64d00326d273e3`
- `i162_user_pc_measurement_procedure.py` — `67319cf4d39b928c04531d4091a373a35d660136`
- `i163_user_pc_benchmark_session.py` — `9e6d0e95004506b6e384c813ddedb9e416e40db4`
- `i164_fixed_benchmark_core.py` — `2a39371bd38b377340c18b1ce77c8bcdbd71c03f`
- `test_i163_user_pc_benchmark_session.py` — `173967851eaee177f9a3727ae4c003ef0d25cc76`
- `test_i164_fixed_benchmark_core.py` — `e71d190dbb7c8f446918735b0c3bb287c2e74d5a`

Focused exact-current local result: **6 passed**.

## I165 outcome
Added `i165_user_pc_one_shot_materializer.py` so the actual user-PC path no longer requires manually copying I163 benchmark metrics into I162.

I165:
- runs I163 locally;
- takes benchmark identity/quality/latency/reliability/parallelism only from I163 and rejects caller overrides;
- optionally merges only explicit availability, energy-counter, tariff and opportunity-cost fields;
- calls I162 using the same I163 environment/identity binding;
- returns `PASS_BLOCKED` until the real external facts and explicit user-owned-PC confirmation are present;
- can return `USER_PC_MATERIALIZED` only as evidence assembly, never as production routing or execution authorization.

New exact blobs:
- `i165_user_pc_one_shot_materializer.py` — `c336efd57f61acf9d7fd7571e729a753ddbf3b91`
- `test_i165_user_pc_one_shot_materializer.py` — `ee7192b00582a3fddf8c34f7db128dd14a9083b8`

Combined I163/I164/I165 focused local result: **9 passed**.

The positive-completion I165 unit test uses clearly labelled `test-fixture:*` values only to prove merge/control logic; it is not production evidence and was not persisted as real resource evidence.

## External effects
No production market/API request, credentials, CI dispatch, downloads/paid installs, account creation, paid infrastructure, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Remaining boundary
The repository-side deterministic implementation for the owned-PC branch is now locally testable and one-shot materializable. The remaining facts cannot be generated honestly inside this execution environment:

1. explicit confirmation that the run is on the user-owned PC;
2. genuinely observed available hours/day and provenance;
3. trustworthy before/after joule-counter readings for the benchmark workload, if such a counter/meter exists;
4. explicit applicable electricity tariff provenance;
5. explicit opportunity-cost provenance.

If trustworthy energy measurement is unavailable, keep that blocker explicit. Do not estimate or synthesize it.

## Next action
Run I165 on the actual user-owned PC with `--confirm-user-owned-pc`. Supply an external JSON only for genuinely observed external fields. If the resulting I162 packet reaches `USER_PC_PACKET_COMPLETE`, pass it into the existing I050/I066/I123 -> economics -> portfolio/readiness chain. Otherwise preserve the missing fact as an explicit blocker and do not reopen broad discovery.
