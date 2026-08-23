# I126 — Narrow reproducible `python_local` configuration invariant

Status: **completed scoped structural repair; runtime execution still pending**

I126 fixes the I125 source-class contradiction without weakening I123. The generic I050 evidence model now recognizes one new reproducible source class, `backend_config_invariant`, but its acceptance is hard-limited to the exact `python_local` backend and five intrinsic software/interface facts only:

- `requires_credentials = false`
- `requires_paid_account = false`
- `requires_new_spend = false`
- `fixed_monthly_cost_usd = 0.0`
- `sunk_or_already_committed = true`

Each record is bound to the exact backend reference hash, a fixed source-ref namespace, and a canonical content digest derived from backend id + parameter + exact value + invariant scope. Generic I050 validation rejects wrong backend, wrong parameter, wrong value, wrong source-ref or wrong digest.

## Isolation boundary

The invariant cannot evidence or normalize:

- `owned_pc` hardware/electricity/depreciation;
- free/conditional CI quota or capacity;
- ChatGPT/Codex subscription cost or quota;
- cheap/strong external API pricing, credentials or spend;
- future VPS/server cost or authorization;
- electricity per task;
- quota/rate-limit capacity;
- latency, reliability, quality or parallelism.

Those facts remain measured, first-party evidenced, or unknown.

## I050 -> I066 -> I123 compatibility

`i126_python_local_config_invariant.py` provides:

1. exact invariant record construction;
2. merge with separately collected dynamic ResourceEvidence;
3. I050 attestation;
4. an explicitly offline/non-production I066 compatibility snapshot proving that a complete reproducible bundle containing I126 records can survive I066 materialization;
5. I123 `BackendEvidence` projection only when the I050 bundle is actually complete and `calibrated_reproducible`.

The I066 fixture is not an I064 production-history substitute and cannot create a production route or authorization.

## I124 integration

I124 is advanced to schema v2. Its local probe now builds the I126 invariant set and subtracts only those exact five facts from the raw missing-resource list. Electricity, quota and rate-limit facts remain explicit blockers. I124 therefore no longer treats the I125 contradiction as an unsolvable missing declaration, but it still cannot claim `measured_reproducible` from a local fixture alone.

## Tests authored

`test_i126_python_local_config_invariant.py` covers:

- exact allowlist emission;
- refusal for local model, subscription, cheap/strong API, CI, owned PC and VPS families;
- reference drift refusal;
- tampered value/digest refusal in generic I050;
- refusal to use the invariant for quota/capacity;
- incomplete dynamic evidence staying planning-only;
- complete independent dynamic evidence passing I050 -> I066 and projecting to strict I123 evidence;
- no route/network/auth/spend/value-movement widening.

The current connector still does not provide an executable exact-current checkout, so no runtime PASS is claimed and no CI workflow was dispatched.

## Safety / notification policy

No DNS/HTTP, credentials, paid infrastructure, workflow dispatch, task acceptance, production observation, authorization creation, spend or value movement occurred. Automatic push/PR CI remains disabled; this stage did not intentionally generate GitHub Actions notification traffic.

## Files

- `implementation/resource_profile_evidence.py`
- `implementation/i126_python_local_config_invariant.py`
- `implementation/test_i126_python_local_config_invariant.py`
- `implementation/i124_runtime_resource_bootstrap.py`
- `implementation/RUN_I126_PYTHON_LOCAL_CONFIG_INVARIANT.md`

## Next broad stage

At an executable exact-current checkout, run I124 v2 once. In the same stage, convert its probe transcript plus I126 records into real I050 records, then close only the remaining dynamic gaps that can genuinely be measured without spend. Priority remaining resource facts are electricity-per-task and explicit local quota/rate-limit semantics/capacity. Preserve unknowns where reliable telemetry/evidence is absent. Feed a complete bundle through the real I058-I067 history/materialization chain and rerun I123. Do not perform the production GET or any value-moving action.