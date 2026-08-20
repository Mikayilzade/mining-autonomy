# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I050 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I050_RESOURCE_PROFILE_EVIDENCE.md`
- `implementation/resource_profile_evidence.py`
- `implementation/test_resource_profile_evidence.py`
- `implementation/RUN_I049_OBSERVATION_RESOURCE_ROUTING.md`
- I048 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I050 result
`resource_profile_evidence.py` adds a deterministic evidence/calibration boundary over the I048 Resource / Execution Router.

Important behavior:
1. synthetic router defaults remain planning references, never proof of real availability/economics;
2. fourteen critical fields require fresh evidence: availability, programmatic/interface constraints, credential/account/spend blockers, fixed/sunk cost, quota, electricity, latency, reliability/quality, parallelism and rate limits;
3. evidence binds backend, exact reference-backend hash, parameter/value, provenance, source reference, observation time, max age and deterministic evidence hash;
4. reproducible measured/provider/system evidence additionally requires a source-content digest;
5. user declarations are allowed as an explicitly separate `calibrated_declared` state and are never mislabeled as measured;
6. missing, stale, future-dated, conflicting, invalid, tampered or wrong-profile evidence fails closed to `planning_only`;
7. complete reproducible evidence can become `calibrated_reproducible`;
8. calibrated fields can be materialized only after a complete attestation, and the materialized record still has execution/network/value movement disabled;
9. ten deterministic tests passed locally;
10. no real market/network/value-moving action occurred.

Target flow is now:
`cheap source watcher -> local filter/dedupe -> normalized task -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-backed Resource Router -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I051
Integrate I050 attestations into I049 routing. Synthetic/default backend families must be reported as reference/planning routes, not as real calibrated resources. Only complete current I050 attestations may enter the calibrated route set. Add deterministic reporting that separates `reference_route`, `calibrated_declared_route`, `calibrated_reproducible_route` and `resource_evidence_missing`. Preserve upstream policy/demand precedence and keep execution/network/value movement disabled.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or access controls. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume paid ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk resources with quota/capacity and interface constraints. For future live routing, only a genuinely available programmatic backend with current evidence may be selected. Future APIs/VPS/paid services remain planning-only until credentials/spend/ToS/geography gates are cleared.

I050 adds an additional rule: illustrative defaults are never live evidence. Current resource parameters must be measured, provider-attested/system-probed, or explicitly user-declared with clear provenance and freshness. Unknown/stale/conflicting values stay planning-only.

## Routing precedence
Policy/demand evidence precedes resource economics. No backend — regardless of cost, speed or quality — can make unsafe, unsupported, policy-insufficient or unproven-demand work eligible.

## Git/CI
Prefer one coherent commit per implementation run where tooling permits. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
