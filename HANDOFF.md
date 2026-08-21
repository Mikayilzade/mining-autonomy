# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I055 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I055_CALIBRATION_ROUTING_PACKET.md`
- `implementation/calibration_routing_packet.py`
- `implementation/test_calibration_routing_packet.py`
- `implementation/RUN_I054_RESOURCE_EVIDENCE_ADAPTER.md`
- I053 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I055 result
`calibration_routing_packet.py` composes one fail-closed chain from I053 acquisition inputs through I054 `ResourceEvidence`, I050 attestation and I052 attested routing.

Complete current resource evidence preserves its calibration class and exact evidence-bundle hash into the selected dry-run route. Missing/stale evidence narrows an upstream accept to hold. Complete calibration cannot rescue an upstream reject/hold. Probe observation time remains explicitly collector-supplied.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I053 acquisition -> I054 evidence -> I050 attestation -> I051/I052 attested router -> I055 provenance packet -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I056
Build a deterministic local calibration fixture/runner specification for `python_local`: an opt-in no-network benchmark that writes a portable transcript JSON plus a verifier replaying it through I053–I055. Do not infer accounting/electricity/quota facts and do not perform real market calls.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055 must preserve exact calibration provenance through the routed result; neither cheap nor calibrated resources can rescue upstream ineligible work.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
