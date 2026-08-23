# I118 — Runtime Environment Provenance + Stable Runner Label

Status: **completed scoped operational hardening — execution pending**
Date: 2026-08-23

## Goal
Harden the already-selected manual GitHub-hosted runtime backend without adding a new policy/safety gate and without dispatching CI. The concrete reproducibility gap was that `ubuntu-latest` is a moving label and a future runtime receipt did not separately record the hosted-runner image/runtime provenance needed to interpret that evidence later.

## Fresh upstream verification
GitHub's current hosted-runner documentation was checked on 2026-08-23. It lists `ubuntu-24.04` as a supported standard x64 GitHub-hosted runner label. Public repositories receive standard hosted runners without metered per-minute billing; private repositories use the account's included minutes and then paid minutes, so this backend remains a fixed/conditional-capacity resource rather than an assumed free unlimited backend.

Official source: https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job

## Changes
- Changed the manual runtime workflow from moving `ubuntu-latest` to the explicit `ubuntu-24.04` label.
- Added a pre-I113 provenance capture that writes `implementation/I118_RUNTIME_ENVIRONMENT_PROVENANCE.json` during the eventual manual run.
- Provenance records the workflow `GITHUB_SHA`, actual checked-out `HEAD`, runner OS/architecture, GitHub image OS/version when exposed, Python version/executable, platform and machine architecture.
- The provenance artifact explicitly records that it does not authorize a network observation, did not perform the production observation, did not use credentials, and did not move value.
- Added the provenance JSON to the existing 1-day artifact bundle.

## Why this is substantive
A source-exact runtime receipt is easier to audit if the execution environment is also recorded. Pinning to an explicit OS family label removes one avoidable alias drift, while recording `ImageOS`/`ImageVersion` acknowledges that GitHub-hosted images themselves still evolve. This does not falsely claim an immutable VM image.

## Safety / cost boundary
The workflow remains manual-only `workflow_dispatch`, `contents: read`, no push/PR trigger, one bounded I113 v2 run, 10-minute timeout, pinned action SHAs and 1-day artifact retention. No workflow was dispatched in I118, so no Actions quota was consumed and no notification was intentionally generated.

No production DNS/HTTP/TLS request, credentials, paid task action, KYC, wallet, spend or value movement occurred. No runtime receipt was fabricated.

## Current blockers
1. fresh-real execution evidence absent;
2. current materialized eligible non-synthetic Resource / Execution Router route absent;
3. exact explicit user authorization absent;
4. current exact-source runtime-regression receipt chain absent.

## Risk
`ubuntu-24.04` is more stable than `ubuntu-latest` as a target family but is not an immutable machine image. The recorded image/version fields are therefore provenance, not a claim that future runs use byte-identical operating-system images.

## Files
- `.github/workflows/implementation-tests.yml`
- `implementation/RUN_I118_RUNTIME_ENVIRONMENT_PROVENANCE.md`
- `STATUS.md`

## Next action
When manual workflow dispatch capability is available, run `implementation-runtime-chain` once on current `main`. Require the uploaded I118 provenance to bind `GITHUB_SHA == checked_out_head` and require I113 v2 `PASS_BLOCKED` before accepting runtime-regression evidence. Keep fresh-real evidence, a current eligible non-synthetic positive-margin Resource Router route and exact explicit authorization as independent blockers before any production observation.
