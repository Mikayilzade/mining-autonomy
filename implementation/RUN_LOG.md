Next: execute exactly one current-main `implementation-runtime-chain` when valid dispatch/runtime capability appears. Require `source_binding_pass=true`, I113 v2 `PASS_BLOCKED`, and I121 `evidence_acceptable=true`; otherwise preserve the checkpoint without restoring automatic CI or performing the production GET.

## I125 — 2026-08-23
Status: **completed source audit**
Stage: resource promotability consistency

Detected a structural contradiction in strict python_local resource promotion; generic source classes could not satisfy all reproducible parameters without a declaration-only fact.

## I126 — 2026-08-23
Status: **completed source checkpoint — runtime pending**
Stage: narrow reproducible python_local config invariant

Added exact python_local-only backend-config invariant evidence for intrinsic software/interface facts, with strict value/source-ref/digest/reference binding and negative isolation. Runtime/electricity/quota/rate facts remain separate.

## I127 — 2026-08-23
Status: **completed source checkpoint — runtime pending**
Stage: exact local evidence packet

Added `i127_exact_local_evidence_packet.py` and tests. I127 can run I124, convert its verified inert fixed local probe into exact I050 evidence, merge I126 invariants, attest through I050, project to I123, and verify a complete reproducible bundle through I066.

The default exact gap after I124 + I126 is reduced to three dynamic parameters only: `quota_units_remaining`, `electricity_per_task_usd`, and `rate_limit_per_minute`. Optional local additional evidence is restricted to these parameters and remains subject to hash and I050 validation. No current route, market evidence, authorization, credentials, spend or value movement is created.

Files: `RUN_I127_EXACT_LOCAL_EVIDENCE_PACKET.md`, `i127_exact_local_evidence_packet.py`, `test_i127_exact_local_evidence_packet.py`, `STATUS.md`, `HANDOFF.md`.

## I128 — 2026-08-23
Status: **completed source checkpoint — runtime / real energy evidence pending**
Stage: python_local resource completion and quota/rate semantic closure

Added `i128_python_local_resource_completion.py`, focused tests and `RUN_I128_PYTHON_LOCAL_RESOURCE_COMPLETION.md`.

I128 resolves two of I127's three remaining local fields without manufacturing host capacity. For exact `python_local` / `deterministic_python` only, `quota_units_remaining=None` and `rate_limit_per_minute=None` are now documented and hash-bound as local-interface semantics meaning no external provider quota/rate primitive. They are explicitly not interpreted as infinite CPU, unlimited parallelism or zero opportunity cost.

The resulting source path is: fixed I056/I053 local probe + I126 config invariants + I128 interface semantics + optional measured energy/tariff -> I050 -> I066 -> I123. With valid probe/config/interface evidence and no energy input, the exact strict resource gap is only `electricity_per_task_usd`. Supplying measured energy plus an explicit tariff can close the resource source path, but does not create market demand, a production route or authorization.

`run_no_spend_bundle()` also consumes I113 once; `RESOURCE_AND_RUNTIME_READY` requires both complete reproducible resource evidence and a fresh I113 `PASS_BLOCKED` receipt. Current connector/runtime limitations prevented execution, so no PASS was claimed.

A temporary duplicate I127 draft created because STATUS lagged behind this log was deleted and the new work was renumbered I128. Authoritative sequence is I127 exact local evidence packet -> I128 resource completion.

Files: `RUN_I128_PYTHON_LOCAL_RESOURCE_COMPLETION.md`, `i128_python_local_resource_completion.py`, `test_i128_python_local_resource_completion.py`, `STATUS.md`, `HANDOFF.md`, `implementation/RUN_LOG.md`.

Risks: electricity-per-task remains unknown until genuinely measured; local interface `None` semantics must never be reused as a physical capacity claim or for CI/API/VPS/subscription backends; exact-current runtime evidence is still absent.

Next: at the first executable exact-current checkout run I128 once, measure energy only if reliable no-spend telemetry exists, combine with an explicit real tariff, materialize through I050/I066, rerun I123, and emit one current resource-readiness/economics packet before any separately authorized market observation.