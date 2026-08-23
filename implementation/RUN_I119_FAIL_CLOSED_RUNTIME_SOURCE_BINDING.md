# I119 — Fail-Closed Runtime Source Binding

Status: **completed scoped operational defect fix — execution pending**
Date: 2026-08-23

## Goal
Close a concrete evidence-integrity gap in the already-selected manual GitHub-hosted runtime backend without adding a new market/policy gate and without dispatching CI.

I118 recorded `GITHUB_SHA` and the checked-out `HEAD`, but the workflow only asked the future reviewer to compare them after execution. That meant I113 could still run first on an unexpected ref/checkout and produce receipts that later had to be rejected manually.

## Changes
- Upgraded the runtime provenance schema to `mining-autonomy/i118-runtime-environment-provenance/v2`.
- Captures `GITHUB_REF` in addition to `GITHUB_SHA` and checked-out `HEAD`.
- Computes and records `head_matches_github_sha`, `ref_matches_main`, and `source_binding_pass`.
- Fails closed before I113 if the checkout does not exactly match the workflow event SHA or if the dispatch ref is not `refs/heads/main`.
- Keeps the provenance JSON in the always-uploaded one-day receipt bundle so a failed binding remains auditable.

## Why this matters
The runtime-regression receipt is intended to attest the exact current `main` source. Provenance that is merely recorded but not enforced still allows wasted execution and ambiguous receipts. I119 makes source/ref binding an executable precondition of the runtime chain itself.

This is operational hardening of the evidence backend, not another authorization gate. It does not create fresh-real market evidence, a Resource / Execution Router route, authorization, credentials, network capability, paid task execution, spend, or value movement.

## Safety / notification boundary
The workflow remains manual-only `workflow_dispatch`, `contents: read`, explicit `ubuntu-24.04`, pinned action SHAs, no persisted checkout credentials, 10-minute timeout, one I113 v2 execution maximum, and one-day artifact retention. No push or pull-request trigger was added.

No workflow was dispatched in I119. No Actions quota was intentionally consumed, no CI email was intentionally generated, no runtime receipt was fabricated, and no production DNS/HTTP/TLS/value-moving action occurred.

## Current blockers
1. fresh-real execution evidence absent;
2. current materialized eligible non-synthetic Resource / Execution Router route absent;
3. exact explicit user authorization absent;
4. current exact-source runtime-regression receipt chain absent.

## Files
- `.github/workflows/implementation-tests.yml`
- `implementation/RUN_I119_FAIL_CLOSED_RUNTIME_SOURCE_BINDING.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/RUN_LOG.md`

## Next action
When manual workflow dispatch capability is available, dispatch `implementation-runtime-chain` once from current `main`. Accept runtime-regression evidence only if the uploaded provenance reports `source_binding_pass=true` and I113 v2 returns `PASS_BLOCKED`. Keep fresh-real evidence, a current eligible non-synthetic positive-margin Resource Router route, and exact explicit authorization as independent blockers before any production observation.
