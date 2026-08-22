# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I092 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I092_EXACT_HTTPS_TARGET_BINDING.md`
- `implementation/exact_https_target_binding.py`
- `implementation/test_exact_https_target_binding.py`
- `implementation/RUN_I091_CONCRETE_ATTESTED_TRANSPORT_BOUNDARY.md`

## I092 result
A canonical exact HTTPS origin-form path/query binding contract now exists. It places `https_path_query` inside the exact scope hash, forbids scheme/authority/userinfo/fragment/out-of-band target components, preserves query ordering, and validates unchanged target identity through I086/I087/I088/I089/I090-shaped artifacts and adapter manifest. Nine offline tests passed.

This does not retrofit old hash-bound authorizations. Existing I086–I091 artifacts remain insufficient for any live call.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query binding contract -> I093 builder integration -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I093
Integrate I092 into the actual fresh I086→I090 builders and tests so the human review packet already contains the canonical path/query before its hash/decision is sealed, the same binding survives authorization and fresh-safety consumption, adapter manifest and I089 request spec, and I090 rejects any drift before invoking a callable. Offline only.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only and documentation changes alone do not trigger it.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
