# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I066 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I066_RESOURCE_EVIDENCE_MATERIALIZATION.md`
- `implementation/resource_feedback_materialization.py`
- `implementation/test_resource_feedback_materialization.py`
- `implementation/RUN_I065_RESOURCE_FEEDBACK_SUMMARY.md`
- I064 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I066 result
I066 closes the numeric-materialization gap identified by I065 without weakening provenance.

Important behavior:
1. the I065 snapshot must verify before any values are exposed;
2. every backend requires its exact reference profile;
3. every latest I065 evidence-bundle hash must be supplied explicitly;
4. each bundle is re-run through I050 attestation at current time and must reproduce the recorded bundle hash;
5. stale/tampered/incomplete/reference-mismatched bundles fail closed;
6. exact-single-parameter refs require their exact evidence hash;
7. multi-parameter set-only refs resolve only when ResourceEvidence contents prove one exact backend/parameter/timestamp mapping; order is never guessed;
8. the backend's newest update bundle is the current quantitative anchor;
9. all older evidence hashes still designated current by I065 must be carried into that newest bundle;
10. only then are all I050 critical calibrated values materialized;
11. user declarations remain visibly distinct from reproducible measurements;
12. unresolved paths emit no partial quantitative profile;
13. all execution/network/credential/submission/value movement gates remain disabled.

Target flow:
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> provenance-sealed local benchmark -> verified receipt -> narrow measured feedback -> exact I052 replay/provenance gate -> re-attestation -> unchanged-task reroute -> append-only feedback history -> verified current-state snapshot -> exact evidence materialization -> current-resource repricing -> later separately authorized real gates`.

## Immediate next run: I067
Integrate I066 materialized profiles into a verified current-resource reroute/repricing layer. Preserve the unchanged task/observation/economics identity, accept only materialized current backends, bind output to the I065 history tip + I066 materialization hash, and surface route change/churn as diagnostics only.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. Benchmark feedback may only narrow/reprice a resource path; it cannot manufacture demand, permission, reliability, quality or authorization. I066 can recover numeric current resource facts from exact evidence, but those facts still cannot widen upstream eligibility.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
