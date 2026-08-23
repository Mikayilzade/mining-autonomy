# I116 — Runtime Runner Stale-Artifact / Timeout Hardening

Status: **completed scoped operational defect fix — execution pending**
Date: 2026-08-23

## Concrete defect found
I113 could misreport a stale expected JSON as if it had been freshly created by a successful step because old step outputs were not removed before execution. Separately, `subprocess.TimeoutExpired` or a process launch `OSError` could escape the runner before I113 wrote its compact fail-closed receipt.

These are operational correctness defects in the already-chosen runtime path, not new safety-policy layers.

## Fix
Updated `implementation/i113_local_runtime_chain_runner.py` to:
- delete each step's expected output immediately before invoking that step;
- require a fresh output file plus return code 0 for the step to count as PASS;
- catch per-step timeout and process-launch failures and serialize them into the I113 receipt;
- keep stopping on first failure;
- preserve source-hash stability checks and all existing no-network/no-authorization/no-value-moving capability flags;
- bump the receipt schema to `mining-autonomy/i113-local-runtime-chain-runner/v2` and explicitly record `fresh_output_required_per_step=true`.

## Result
No runtime execution was performed in this run because the current connector still cannot dispatch the manual workflow and the available shell does not provide the repository checkout. No receipt was fabricated. No DNS/HTTP/TLS request, credentials, paid action, spend, CI dispatch or value movement occurred.

## Risk closed
A stale output from an earlier run can no longer satisfy I113's output-presence check for a later step. Timeout/launch failures now produce deterministic FAIL_CLOSED evidence when the runner itself is executed.

## Next action
Manually dispatch the existing `implementation-runtime-chain` workflow once on current `main` when dispatch capability is available. Accept runtime regression evidence only from a `PASS_BLOCKED` I113 v2 result whose I106-I112 outputs are freshly generated in that invocation. Keep fresh-real evidence, current eligible non-synthetic positive-margin Resource Router route and exact explicit authorization as independent blockers.
