# I094 — Native Exact HTTPS Builder Regression Hardening

Date: 2026-08-22
Status: **COMPLETED AS SCOPED SAFE CHECKPOINT**

## Objective
Move the I093 exact-path invariants into the native I086/I087/I089/I090 builder/executor boundaries so missing or altered `https_path_query` fails closed without relying on the I093 integration adapter. Keep the entire run offline/synthetic and do not perform a real observation.

## Work completed
- Added `native_exact_https_hardening.py` with a shared canonical origin-form path/query validator based on the I092 `canonical_path_query` contract.
- Activated native hardening at `final_real_observation_review_packet.build_final_real_observation_review_packet` (I086).
- Activated native hardening at `final_real_observation_decision.verify_final_real_observation_decision` (I087).
- Activated native hardening at `final_network_adapter_invocation_gate.build_final_network_adapter_invocation_gate` (I089).
- Activated a final pre-call path check at `final_single_use_transport_executor.execute_single_use_dependency_injected_transport` (I090).
- I086 now requires a canonical, hash-bound `exact_scope.https_path_query` and reseals the review packet with `path_query`, `userinfo_allowed=False`, and `fragment_allowed=False`.
- I087 now requires packet path equality and a fresh decision carrying the same `path_query`; an authorization is not issued on drift.
- I089 now requires the adapter manifest `path_query` to equal the bound scope path and emits it into `request_spec.path`.
- I090 independently rejects missing/non-canonical request paths before invoking the injected transport callable; rejected malformed-path attempts do not consume the one-shot attempt because no transport attempt occurred.
- Migrated I086/I089/I090 fixtures to the bound path/query contract and added native fail-closed regressions for missing, absolute-URL, authority-form and fragment-bearing paths plus manifest path drift.

## Validation
Existing pull-request-only workflow `.github/workflows/implementation-tests.yml` was used; no push-triggered CI was enabled.

First full-suite run exposed one I094-specific fixture/assertion ordering issue: deleting `https_path_query` also invalidated the enclosing scope hash, so the shared validator reported hash drift before the more specific missing-path blocker. The validator was tightened to validate path presence/canonicality before validating the scope hash; this preserves fail-closed behavior while making the specific regression deterministic.

Second full-suite result:
- **634 passed**
- **48 failed**
- all I094 exact-path native/downstream regressions passed;
- the 48 remaining failures are broad unrelated repository baseline/fixture debt (notably stale absolute-time fixtures and older routing/calibration expectation mismatches).

The run deliberately did not expand into repairing unrelated test debt because I094 is a narrow authorization/transport safety checkpoint and the project instruction forbids unnecessary return to broad work.

## Safety conclusions
- No DNS lookup, TLS connection, HTTP request or live market observation was performed by project code.
- No real credential was used.
- No money was spent; no deposit/stake/server/GPU rental was created.
- No task was accepted, submitted or settled.
- No value movement occurred.
- Existing pre-I092 authorizations remain inert and cannot be upgraded into this fresh exact-path lineage.
- I094 does not create production authorization. It only makes a future one-shot request narrower and more fail-closed.

## Risks / unresolved items
1. The repository-wide suite is not globally green: 48 unrelated failures remain and must be control-compared against `main` before the project treats full-suite status as a clean release signal.
2. Any future production observation still needs fresh policy and DNS/pinning evidence at execution time.
3. Any future final decision must explicitly bind the exact review-packet hash and exact path/query; no prior decision is reusable.
4. A read-only observation, if later authorized, is not permission for task acceptance, credentials, spend, submission or value movement.

## Files changed
- `implementation/native_exact_https_hardening.py`
- `implementation/final_real_observation_review_packet.py`
- `implementation/final_real_observation_decision.py`
- `implementation/final_network_adapter_invocation_gate.py`
- `implementation/final_single_use_transport_executor.py`
- `implementation/test_final_real_observation_review_packet.py`
- `implementation/test_final_network_adapter_invocation_gate.py`
- `implementation/test_final_single_use_transport_executor.py`
- `implementation/RUN_I094_NATIVE_EXACT_HTTPS_HARDENING.md`
- `implementation/RUN_LOG.md`
- `STATUS.md`
- `HANDOFF.md`

## Next action — I095
Perform a narrowly scoped **baseline-control / regression-debt isolation** pass: compare the same implementation suite against current `main`, identify whether any of the 48 failures differ from the pre-I094 baseline, and record a stable focused I086–I094 regression subset. Do not broaden into unrelated feature work and do not perform a production request.

After that control checkpoint, a future run may prepare a fresh one-shot review packet. Sending the actual anonymous read-only production GET still requires separate explicit user authorization and fresh policy/DNS evidence.
