# I117 — Manual Runtime Backend Supply-Chain Pinning

Status: **completed scoped operational hardening — execution pending**
Date: 2026-08-23

## Goal
Harden the already-selected manual GitHub-hosted runtime backend without adding another policy/safety gate and without reviving automatic CI. The concrete issue was mutable major-version action references (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`) in the exact runtime-evidence path.

## Fresh upstream verification
Checked the official GitHub release/commit pages on 2026-08-23 before changing the workflow:
- `actions/checkout` v4.4.0 -> `11d5960a326750d5838078e36cf38b85af677262`
- `actions/setup-python` v5.6.0 -> `a26af69be951a213d495a4c3e4e4022e16d87065`
- `actions/upload-artifact` v4.6.2 -> `ea165f8d65b6e75b540449e92b4886f43607fa02`

Official sources:
- https://github.com/actions/checkout/releases
- https://github.com/actions/setup-python/releases
- https://github.com/actions/upload-artifact/releases

## Changes
Updated `.github/workflows/implementation-tests.yml` so the three third-party GitHub-maintained actions are referenced by immutable full commit SHA rather than mutable major tags. Human-readable release comments remain beside each SHA.

Also set `persist-credentials: false` on checkout. The runtime chain only reads repository files and does not need the workflow token persisted into Git config after checkout.

The workflow remains:
- manual-only `workflow_dispatch`;
- `contents: read` only;
- no push or pull-request trigger;
- one manual concurrency group;
- 10-minute job timeout;
- Python 3.12;
- exact I113 v2 runner only;
- 1-day receipt artifact retention;
- no production market request, credentials, paid task action, KYC, wallet, spend or value movement.

## Why this is substantive
Runtime-regression evidence is intended to bind exact current source. Allowing the execution bootstrap actions to move underneath a future run through mutable major tags weakens reproducibility and creates unnecessary supply-chain drift. Pinning the action commits makes the free/conditional CI backend materially more deterministic without consuming CI quota in this run.

## Result
No workflow was dispatched. No I106-I113 runtime receipt was fabricated. No production DNS/HTTP/TLS request or value-moving action occurred.

Current blockers remain independent and unchanged:
1. fresh-real execution evidence absent;
2. current materialized eligible non-synthetic Resource / Execution Router route absent;
3. exact explicit user authorization absent;
4. current exact-source runtime-regression receipt chain absent.

## Risk / maintenance note
Pinned actions do not auto-receive future fixes. Any future action upgrade must be an explicit reviewed maintenance step using a newly verified immutable commit SHA. This is preferred here because this workflow is infrequent, manual-only evidence infrastructure rather than a continuously evolving CI pipeline.

## Next action
When workflow-dispatch capability is available, run `implementation-runtime-chain` once on current `main`. Accept runtime regression evidence only if I113 v2 returns `PASS_BLOCKED` and all freshly generated I106-I112 outputs agree with the exact current source chain. Do not perform the production GET from runtime verification alone; fresh-real evidence, a current positive-margin eligible non-synthetic route, and exact explicit authorization remain separate blockers.
