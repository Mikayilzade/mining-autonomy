# I122 — Runtime Connector Capability Audit / Stale Rerun Rejection

Status: **completed scoped operational checkpoint — runtime execution still pending**
Date: 2026-08-23

## Goal
Follow the current immediate action without inventing another source-only gate: re-check whether the available GitHub connector can execute the already-prepared manual runtime backend, and ensure newly exposed rerun controls are not misused as a substitute for an exact current-main run.

## Work performed
- Re-read the mandatory repository state and the I121 notification-safe manual runtime outcome contract.
- Re-inspected the available GitHub Actions connector surface.
- Confirmed there is still **no workflow-dispatch action** exposed, so the current manual-only `implementation-runtime-chain` cannot be started from this environment.
- Confirmed the connector now exposes rerun controls for an already-existing workflow job/run.
- Inspected the known historical failed run attached to PR #1 head `0575cc0a23157a4c4ed0908f0ec1132673bf8592`: workflow run `32574545296`, job `97034830749`. That job used the old `implementation-tests` PR pipeline (`actions/checkout@v4`, `actions/setup-python@v5`, install test runner, run all implementation tests) and failed before the current I115-I121 manual runtime backend existed.
- PR #1 is merged/closed and its head is not current `main`.

## Decision
Do **not** use `rerun_workflow_job` or `rerun_failed_workflow_run_jobs` on historical PR CI to manufacture runtime evidence.

Reasons:
1. it executes stale source/ref rather than current `main`;
2. it executes the historical workflow definition rather than the current manual I113/I118/I121 evidence path;
3. it would fail the exact current-main source-binding requirement;
4. it risks recreating the GitHub failure-email spam that I115/I121 were designed to avoid;
5. rerun capability is not equivalent to manual workflow-dispatch capability.

## Result
No workflow was dispatched or rerun. No runtime receipt was fabricated. No production DNS/HTTP/TLS observation, credentials, paid task action, spend, KYC, wallet action, paid infrastructure, or value movement occurred.

The current state remains blocked on the same four independent conditions:
1. fresh-real execution evidence;
2. current materialized eligible non-synthetic Resource / Execution Router route with positive conservative margin;
3. exact explicit user authorization;
4. current exact-source runtime-regression receipt chain.

## Files
- `implementation/RUN_I122_RUNTIME_CONNECTOR_CAPABILITY_AUDIT.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/RUN_LOG.md`

## Next action
At the first environment exposing either an executable current checkout with Python or authenticated `workflow_dispatch` for the repository, execute exactly one current-main `implementation-runtime-chain` run. Accept runtime evidence only when I118/I119 provenance has `source_binding_pass=true`, I113 v2 returns `PASS_BLOCKED`, and I121 reports `evidence_acceptable=true`.

Until then, preserve the checkpoint. Do not rerun stale PR CI, restore automatic triggers, or perform the production GET.
