# Implementation Runs I151–I153 — source-bound runtime transport

Date: 2026-08-24
Status: **COMPLETED AS BROAD RUNTIME-TRANSPORT CHECKPOINT — FULL I113 EXECUTION STILL PENDING**
Phase: Implementation / Experiment

## Objective
Advance the independent Resource / Execution Router/runtime branch without reopening discovery and without restoring automatic CI. The immediate technical blocker was transport-specific: the available execution container cannot resolve `github.com`, so direct `git clone` cannot produce an exact-current checkout even though the authenticated GitHub connector can read exact repository bytes and Git identities.

## I151 — exact source-bound snapshot contract
Added `i151_source_bound_runtime_snapshot.py`.

The contract allows the exact-current runtime source to be materialized by a trusted transport other than `git clone`, but it does **not** weaken source identity. Every supplied file is verified with the real Git blob algorithm (`SHA1("blob <len>\\0" + bytes)`), and the receipt is explicitly bound to a repository, 40-hex commit SHA and 40-hex tree SHA. Duplicate paths, invalid hashes, missing required I106–I113 top-level runtime files, missing local bytes, or any byte mismatch fail closed.

A successful snapshot receipt only says the source bytes are eligible to be passed to the existing local I113 runner. It explicitly does not authorize I113 execution, network access, credentials, CI dispatch, spend or value movement.

## I152 — current-main identity and transport diagnosis
The current repository state was read through the GitHub connector. Before this stage's writes, `main` was commit `52b487db4aae957da1a089c791297dcb72045796`, tree `2894476287fa900ae8ab0dda715c2e84334774a6`. The exact Git blob identities for the top-level I106–I113 chain were sampled from that commit, including:
- I106 `3c44e9a250a95570ecbc4ad43cefd330a89854c2`
- I107 `3c23db049f03de5682244d1b4fd2d59a610f80b7`
- I108 `d492ae96972e46481a2528a6a289255a8e5d67a1`
- I109 `b2bd5adfdaaa915cacbe2330caee7fe2daa83c5e`
- I110 `991c992324fb407a73d3fb141515d41c3807448a`
- I111 `3346ae0385e7882673e95c9ca075edeac4f12d65`
- I112 `b543b8211fd7d50cd207c09c7e2f6e1e6af0d56c`
- I113 `d65aa8f46a361e68b11f0c456e2673a2bf1f42ca`

A fresh direct clone attempt in the execution container again failed before checkout with `Could not resolve host: github.com`. This is now treated as a transport failure, not evidence that the runtime source itself is unavailable.

## I153 — verification and next executable boundary
Added focused tests in `test_i151_source_bound_runtime_snapshot.py`. The source-bound verifier was executed locally against exact authored I151 source semantics: **2 tests passed**. Tests cover exact required-byte acceptance and fail-closed behavior for tampering, missing required files, duplicate paths and invalid commit identity.

This is not an I113 PASS. To obtain the missing exact-current runtime receipt, a future run must materialize the **complete dependency/artifact closure required by I106–I113**, source-bind those bytes to the then-current commit/tree, and run I113 locally. The snapshot mechanism is only the transport bridge; I106 remains responsible for computing/validating its dependency closure and banned-network-import checks.

## Result
The runtime blocker is narrowed from "exact checkout requires working GitHub DNS" to "materialize a complete exact-current source-bound runtime bundle and execute I113". This creates a practical path through environments where `git clone` is unavailable while preserving the same exact-source standard.

## Safety/actions not taken
No production market request, PayanAgent task-list/receipt GET, registration, credentials, wallet, task acceptance, fulfillment, CI dispatch, paid infrastructure, spend or value movement occurred. Automatic CI remains disabled.

## Files
- `implementation/i151_source_bound_runtime_snapshot.py`
- `implementation/test_i151_source_bound_runtime_snapshot.py`
- `implementation/RUN_I151_I153_SOURCE_BOUND_RUNTIME_TRANSPORT.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/RUN_LOG.md`

## Remaining blockers
1. full exact-current I106–I113 source/artifact closure has not yet been materialized and executed;
2. genuine `python_local` energy measurement + explicit tariff provenance absent;
3. current measured non-synthetic conservative Resource Router route absent;
4. PayanAgent explicit geography/provider-access evidence absent; public-doc search remains converged;
5. exact bounded read-only observation authorization absent.

## Next broad action
Use the source-bound snapshot path to materialize the complete current I106–I113 closure in one broad execution stage where tooling allows, then execute I113. In the same broad cycle, if exact runtime passes, continue I128/I129 -> I050/I066/I123 -> I133/I136 -> I138. If `python_local` cannot be materially evidenced or fails conservative economics, advance through I137/I134 to the next existing no-new-spend backend branch. Do not reopen broad discovery and do not repeat PayanAgent geography searches without new first-party evidence.
