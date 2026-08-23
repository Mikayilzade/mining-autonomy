# Implementation Run Log

Detailed implementation history is preserved in individual `RUN_Ixxx_*.md` files. This compact index was found truncated at the I122 continuation checkpoint; do not reconstruct missing historical detail from chat memory. Resume from the durable run files and `STATUS.md`.

## I125 — 2026-08-23
Status: **completed scoped model-consistency checkpoint**
Stage: resource promotability audit

Detected a structural contradiction: `sunk_or_already_committed` was declaration-only in I053, while I050 marks declaration-containing bundles non-reproducible and I123 requires strict `measured_reproducible`. Repeated runtime attempts could not solve this source-model defect.

Files: `implementation/RUN_I125_RESOURCE_PROMOTABILITY_AUDIT.md`, `implementation/i125_resource_promotability_audit.py`, `implementation/test_i125_resource_promotability_audit.py`.

Risks: fixing by accepting arbitrary declarations would silently weaken production routing; forbidden.

Next: add a narrow, exact-source-bound reproducible `python_local` configuration invariant.

## I126 — 2026-08-23
Status: **completed scoped structural repair; runtime pending**
Stage: python_local config invariant + I050/I066/I123 reconnect

Added `backend_config_invariant` to I050 as a reproducible source class with hard generic validation. It is restricted to exact `python_local` identity and five fixed software/interface facts only: no credentials, no paid account, no new spend, zero fixed software cost and sunk/committed classification for the zero-cost local software path. Value, source-ref, digest and backend mismatch fail closed.

Added `i126_python_local_config_invariant.py` and negative isolation tests. The invariant cannot cover owned PC, CI, subscription, external APIs, VPS, electricity, quota/rate capacity, latency, reliability, quality or parallelism. A complete independently evidenced bundle is shown to be compatible with I050 -> offline I066 materialization -> I123 strict evidence projection without creating a route.

I124 advanced to schema v2 and now subtracts only I126-covered intrinsic facts from its missing-resource report. Electricity/quota/rate capacity remain explicit blockers.

Files: `implementation/resource_profile_evidence.py`, `implementation/i126_python_local_config_invariant.py`, `implementation/test_i126_python_local_config_invariant.py`, `implementation/i124_runtime_resource_bootstrap.py`, `implementation/RUN_I126_PYTHON_LOCAL_CONFIG_INVARIANT.md`, `STATUS.md`, `HANDOFF.md`, `implementation/RUN_LOG.md`.

Risks: source/runtime tests are authored but the current connector still provides no executable exact-current checkout, so no runtime PASS is claimed. The offline I066 compatibility snapshot is not a substitute for the real I064 history chain.

Next: run I124 v2 once at the first executable exact-current checkout, convert probe + I126 records into real I050 evidence, measure remaining no-spend dynamic facts where reliable telemetry exists, feed a complete bundle through I058-I067, and rerun I123. Keep production GET, credentials, spend and value movement blocked.