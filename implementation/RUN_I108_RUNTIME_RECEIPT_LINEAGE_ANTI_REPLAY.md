# I108 — Runtime receipt lineage / stale-replay hardening

Date: 2026-08-23
Status: **COMPLETED SAFE CHECKPOINT — EXACT-SOURCE LINEAGE VALIDATOR AUTHORED; RUNTIME RECEIPT STILL ABSENT**
Phase: Implementation / Experiment

## Goal
Continue the exact unfinished runtime-verification safety step without widening discovery, performing the production GET, using repeated PR CI, or moving value. Since a repository-local executable checkout is still not available to this automation runtime, strengthen the future I106 -> I107 binding so a structurally valid but stale runtime receipt cannot satisfy the runtime blocker after tested source bytes or the exact test specification changes.

## Result
Added `i108_runtime_receipt_lineage_validator.py`.

The validator:
- reuses I107 structural PASS-receipt validation rather than inventing a parallel receipt schema;
- recomputes the current local I106 dependency closure from the exact I099-I102 targets and requires the receipt SHA-256 map to match it exactly;
- rejects missing, extra or changed dependency entries;
- requires the receipt `tests` array to match current I106 target order, module filenames and arguments exactly, closing a stale/altered-target replay gap;
- requires the top-level target order to match current I106 targets;
- records current I106 harness and I107 binder SHA-256 values as lineage diagnostics for the checkpoint result;
- preserves I107 fail-closed semantics: a valid receipt can satisfy only `runtime_regression_verification`;
- keeps fresh-real evidence, a current eligible non-synthetic Resource / Execution Router route and exact explicit user authorization independent and non-substitutable;
- remains explicitly network-incapable and never creates an execution token or authorization.

## Why this stage was needed
I107 correctly validated the receipt's own dependency hash map but did not compare that map to the current checkout. Therefore an old PASS receipt could remain structurally valid after a later source change. I108 closes that source-lineage gap before any real observation is allowed.

This is not a claim that runtime verification has passed. `I106_LOCAL_RUNTIME_RECEIPT.json` is still absent, so the runtime blocker remains false.

## Current four independent blockers
1. fresh-real execution evidence: **false**;
2. current materialized eligible non-synthetic Resource / Execution Router route: **false**;
3. exact explicit user authorization: **false**;
4. current exact-source runtime regression receipt: **false**.

Therefore `production_observation_allowed=false` remains unchanged.

## Safety / external effects
No production DNS/HTTP/socket/TLS request, credentials, authorization creation, task acceptance/submission, paid infrastructure, payment, deposit, stake, spend, value movement or GitHub Actions dispatch occurred. The repository workflow remains `workflow_dispatch` + path-scoped `pull_request`; direct pushes do not run it and root `.md` changes do not trigger it.

## Files
- `implementation/i108_runtime_receipt_lineage_validator.py`
- `implementation/RUN_I108_RUNTIME_RECEIPT_LINEAGE_ANTI_REPLAY.md`

## Risks / notes
- I108 does not manufacture a runtime receipt and does not infer PASS from source review.
- The current v1 receipt schema has no trusted wall-clock freshness token; exact current-source matching is the durable anti-stale criterion here. A later single-use execution lineage may add stricter bounded freshness if needed.
- A current exact-source runtime PASS still cannot substitute for fresh market evidence, production Resource Router materialization or explicit authorization.
- Resource / Execution Router economics and selection rules remain unchanged and must be satisfied before a real monetization test.

## Next action — I109
At the first repository-local Python runtime, execute `python3 implementation/i106_local_runtime_receipt.py`; if PASS, immediately run `python3 implementation/i107_runtime_receipt_binding_validator.py` and `python3 implementation/i108_runtime_receipt_lineage_validator.py`. Accept the runtime blocker only if all three agree and I108 reports exact current-source lineage.

If executable runtime remains unavailable, continue deterministic network-inert hardening without widening discovery. A useful next checkpoint is to bind the I108 exact-source lineage result into the I104/I105 preauthorization consistency view while keeping the other three blockers independent. Do not perform the production GET and do not trigger repeated failing PR CI solely for evidence.
