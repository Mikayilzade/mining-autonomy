# I121 — Notification-Safe Manual Runtime Outcome Semantics

Status: **completed scoped operational hardening — execution still pending**
Date: 2026-08-23

## Goal
Reduce GitHub/Gmail notification risk for the already-selected manual runtime backend without weakening evidence semantics, re-enabling automatic CI, or adding another source-only authorization gate.

## Concrete defect addressed
The I115-I120 manual workflow correctly used `workflow_dispatch` only, but an expected fail-closed runtime outcome or source-binding refusal could still make the GitHub Actions job fail. A manual failure can generate a GitHub failure email even though the project intentionally treats the generated runtime receipt — not the green/red workflow badge — as the authoritative evidence object.

This created an avoidable notification-spam risk and conflated transport/job status with evidence status.

## Change
Updated `.github/workflows/implementation-tests.yml` so that:
- source provenance is always written first and exported as a boolean workflow output;
- I113 runs only when exact current-main source binding passes;
- the I113 step uses `continue-on-error: true`, so a deterministic `FAIL_CLOSED` receipt does not itself mark the whole manual workflow failed;
- an always-run I121 outcome step writes `I121_RUNTIME_WORKFLOW_OUTCOME.json`;
- `evidence_acceptable=true` only when both `source_binding_pass=true` and the fresh I113 receipt reports `PASS_BLOCKED`;
- workflow success/failure is explicitly declared non-authoritative for runtime evidence;
- the I121 outcome is uploaded together with I106-I113/I118 receipts for one day.

The workflow remains manual-only, read-only, bounded to `ubuntu-24.04`, pinned action SHAs, `persist-credentials: false`, 10-minute timeout, and no production observation/value-moving behavior.

## Evidence semantics
A green manual workflow is **not** proof that runtime verification passed. Only the generated artifact chain is authoritative. Runtime-regression evidence is acceptable only when:
1. I118/I119 provenance says `source_binding_pass=true`;
2. the exact current I113 v2 receipt exists;
3. I113 says `PASS_BLOCKED`;
4. I121 says `evidence_acceptable=true`.

A skipped/refused/fail-closed I113 run may still leave the GitHub job green solely to avoid notification noise; its artifacts remain fail-closed and cannot satisfy the runtime blocker.

## Boundary
No workflow was dispatched in I121. No production DNS/HTTP/TLS observation, credentials, paid task action, paid infrastructure, KYC, wallet action, spend, or value movement occurred. The three non-runtime blockers remain unchanged and false.

Infrastructure-level failures before the receipt/outcome steps (for example checkout/setup runner outages) can still fail the workflow; this stage only prevents expected evidence-level fail-closed states from becoming noisy CI failures.

## Files
- `.github/workflows/implementation-tests.yml`
- `implementation/RUN_I121_NOTIFICATION_SAFE_MANUAL_RUNTIME_OUTCOME.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/RUN_LOG.md`

## Next action
At the first environment with authenticated manual Actions dispatch capability, dispatch exactly one `implementation-runtime-chain` run from current `main`. Accept runtime-regression evidence only from the uploaded receipts when source binding passes, I113 returns `PASS_BLOCKED`, and I121 reports `evidence_acceptable=true`.

If dispatch remains unavailable, preserve the checkpoint. Do not restore push/PR triggers and do not perform the production GET.
