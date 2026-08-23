# I115 — Notification-Safe Manual Runtime Backend

Status: **completed scoped operational checkpoint — manual runtime backend authored; execution pending**
Date: 2026-08-23

## Goal
Close the concrete execution-environment gap found in I113/I114 without adding another safety gate and without reviving PR-triggered CI spam.

## What changed
- Reworked `.github/workflows/implementation-tests.yml` into a **manual-only** `workflow_dispatch` runtime backend.
- Removed the `pull_request` trigger, so implementation pushes/PR updates no longer automatically run this workflow or generate repeated CI failure emails.
- Removed the external `pytest` install step from this runtime path; the job now uses the repository's own stdlib-based `i113_local_runtime_chain_runner.py`.
- Added a 10-minute timeout, read-only repository permissions, single manual concurrency group, and 1-day receipt artifact retention.
- The job runs only the exact current I113 local chain and uploads I106-I113 receipt files for inspection.

## Why this is substantive
The current automation/container cannot obtain a repository-local checkout because DNS to github.com is unavailable. GitHub-hosted Actions, when manually dispatched, provides an exact checkout plus Python without requiring a paid server or a persistent external API. This is therefore a concrete free/conditional CI execution backend in the Resource / Execution Router sense, not a policy shortcut.

## Safety / cost boundary
The workflow is not scheduled and has no push/PR trigger. It performs no production market observation, credentials, paid task acceptance/submission, KYC, wallet action, deposit, paid infrastructure rental, or value movement. It consumes only manually invoked GitHub Actions capacity/quota. That capacity is limited/fixed rather than economically free; no per-task monthly subscription allocation is invented.

## Result
The runtime backend is now available in source, but this run did not dispatch it because the current connector exposes no workflow-dispatch action and repeated CI activity is intentionally avoided. Therefore runtime verification remains unproven until one manual run returns I113 `PASS_BLOCKED` on the current checkout.

## Risks
- GitHub-hosted runner availability/quota is external and limited.
- A failing manual run can still create one GitHub failure notification, so it should be dispatched only when needed, not per push.
- PASS_BLOCKED can satisfy only the runtime-regression checkpoint; fresh-real evidence, a current eligible non-synthetic Resource Router route with positive conservative margin, and exact explicit authorization remain separate blockers.

## Files
- `.github/workflows/implementation-tests.yml`
- `implementation/RUN_I115_NOTIFICATION_SAFE_MANUAL_RUNTIME_BACKEND.md`
- `STATUS.md`
- `implementation/RUN_LOG.md`

## Next action
When a manual GitHub Actions dispatch is available, run `implementation-runtime-chain` once on current `main`. Inspect the uploaded I106-I113 receipts. Do not perform the production GET or any value-moving action from that result alone.
