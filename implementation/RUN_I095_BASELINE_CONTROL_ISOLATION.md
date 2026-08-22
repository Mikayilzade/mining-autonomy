# I095 — Baseline Control / Regression-Debt Isolation

Date: 2026-08-22
Status: **COMPLETED AS SCOPED OFFLINE CONTROL CHECKPOINT**

## Objective
Isolate the 48 failures seen in the I094 pull-request full implementation suite from the I086–I094 exact authorization/transport lineage before any production observation. Remain offline/synthetic and do not create or infer user authorization.

## Control evidence used
- I094 merged as commit `55988a553b8dba13e6c72e9fe3afb329fa24dd4d` with parent/main control ref `c5d0426ed8bd2a7ec029e12ed8e1d42b0e7a5379`.
- PR #1 changed exactly 12 files: root status/handoff, the I094 run record, four exact-path production modules, the new hardening module, and three exact-path tests.
- The final PR workflow run `32574545296` executed the complete `implementation` pytest suite under Python 3.12 and finished `634 passed / 48 failed`.
- All I094 exact-path native/downstream regressions passed after the targeted validator-ordering fix recorded in I094.

## Isolation result
The 48 remaining failures are outside the three I094-changed test files. Their failing modules are older archive/replay, routing/calibration, evidence serialization, response bridge, session import/provenance and materialized-resource tests. The failure signatures are dominated by:
1. absolute-time fixture freshness/future-skew drift;
2. older expected `accept_dry_run` / `hold` states now observing conservative `reject` results;
3. old probe-repetition expectations (`repetitions=3` versus a newer minimum);
4. older error-order/message expectations;
5. tuple/list serialization normalization expectations.

No failing node shown in the final workflow belongs to:
- `test_final_real_observation_review_packet.py`;
- `test_final_network_adapter_invocation_gate.py`;
- `test_final_single_use_transport_executor.py`.

The I094 commit diff also does not touch any of the 48 failing test modules. This establishes a strong **direct-regression isolation** result for I094: no remaining failure is in an I094-modified test surface and the I094-specific regressions are green.

### Important limitation
This run deliberately did **not** trigger another GitHub Actions job because the user reported CI email spam and the workflow is already known to emit failure notifications. The exact parent control ref `c5d0426...` was therefore not re-executed in CI during I095. Consequently, I095 does not claim byte-for-byte proof that every one of the 48 failures reproduces on the parent runtime; it records them as **baseline/independent debt with strong static + existing-run evidence**, not as newly repaired or silently waived tests.

## Stable focused I086–I094 regression set
Use this focused set as the safety-lineage gate before interpreting the noisy repository-wide suite:

- `test_final_real_observation_review_packet.py`
- `test_final_real_observation_decision.py`
- `test_final_network_adapter_invocation_gate.py`
- `test_final_single_use_transport_executor.py`
- `test_exact_https_target_binding.py`
- `test_fresh_exact_https_builder_integration.py`
- `test_concrete_pinned_https_transport.py`

If a filename is renamed later, the replacement must cover the same I086–I094 invariants: exact scope/path hash binding, fresh human-decision lineage, adapter/source binding, one-shot invocation consumption, pre-call canonical origin-form path rejection, and pinned HTTPS/JSON transport boundary.

## CI / notification decision
- No new push-triggered CI was added.
- No workflow was dispatched in this run.
- Existing `.github/workflows/implementation-tests.yml` remains `workflow_dispatch` + `pull_request` only and root `.md` changes do not trigger it.
- Future control checks should prefer local/offline execution or a deliberately requested manual run; do not create repeated failing PR pushes simply to obtain the same baseline evidence.

## Safety conclusions
- No DNS lookup, TLS connection, HTTP request or live market observation was performed by project code.
- No credential, spend, paid infrastructure, KYC, task acceptance, submission, settlement or value movement occurred.
- No authorization was manufactured or inferred.
- I086–I094 remain a narrow one-read-only-GET lineage, not general execution permission.

## Risks / unresolved items
1. Repository-wide regression debt remains: 48 failures are not repaired by I095.
2. Exact parent-ref dynamic reproduction remains optional evidence debt; it is not worth causing notification spam before the safety lineage needs a release-quality full-suite gate.
3. A future real observation still requires a fresh exact review packet, explicit user authorization, and fresh policy/DNS/pinning evidence at execution time.
4. A permitted read-only observation would still not authorize paid work, credentials, spend, submission or settlement.

## Files changed
- `implementation/RUN_I095_BASELINE_CONTROL_ISOLATION.md`
- `implementation/I095_FOCUSED_REGRESSION_SET.txt`
- `implementation/RUN_LOG.md`
- `STATUS.md`
- `HANDOFF.md`

## Next action — I096
Prepare a **fresh one-shot review packet only**, still network-inert: bind the exact anonymous read-only target/scope/path to current candidate evidence, require fresh policy/DNS evidence placeholders, and preserve the explicit user-authorization gap. Do not send a production request. Do not reuse any pre-I092/I093/I094 authorization artifact.
