# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I051 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I051_ATTESTED_RESOURCE_ROUTING.md`
- `implementation/resource_routing_attestation.py`
- `implementation/test_resource_routing_attestation.py`
- `implementation/RUN_I050_RESOURCE_PROFILE_EVIDENCE.md`
- I049 and prior resource-routing / authorization / readiness / capture files.

## I051 result
The Resource / Execution Router now has an explicit evidence-backed selection boundary:
1. synthetic/default backends remain visible only as reference/planning quotes;
2. no reference-only backend can be selected even if its illustrative cost is cheapest;
3. only complete current I050 attestations may enter the calibrated route set;
4. user-declared evidence remains `calibrated_declared_route`;
5. measured/provider/system-backed evidence remains `calibrated_reproducible_route`;
6. missing/planning-only evidence yields `resource_evidence_missing`;
7. calibrated backends still pass the existing capability/quota/policy/success/margin gates;
8. execution/network/value movement remain disabled;
9. seven deterministic tests were added and syntax compilation passed;
10. GitHub Actions was not dispatched.

Target flow:
`cheap source watcher -> local filter/dedupe -> normalized task -> policy/rights/quality/demand gate -> TaskEconomics -> I050 resource attestation -> I051 attested Resource Router -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I052
Build the end-to-end bridge over I049 + I051: upstream observation/policy/demand acceptance must happen before attested resource routing; combined records must preserve upstream economics/evidence plus resource calibration state/evidence bundle hash. Reference-only resources must never make a task routable. Keep execution/network/value movement disabled.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing. Future APIs/VPS/paid services remain planning-only until credentials/spend/ToS/geography gates are cleared.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence then precedes backend selection. Neither a cheap backend nor a calibrated backend can rescue an upstream hold/reject.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
