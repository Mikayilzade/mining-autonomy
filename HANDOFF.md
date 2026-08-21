# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I054 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I054_RESOURCE_EVIDENCE_ADAPTER.md`
- `implementation/resource_evidence_adapter.py`
- `implementation/test_resource_evidence_adapter.py`
- `implementation/RUN_I053_RESOURCE_CALIBRATION_ACQUISITION.md`
- I052 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I054 result
A deterministic adapter now converts I053 local calibration inputs into I050 `ResourceEvidence` records without fabricating missing resource fields.

Probe-derived facts retain `system_probe` provenance, exact transcript digest, backend/benchmark binding and collector-supplied measurement time. Explicit accounting/interface facts stay `user_declared`. Measured electricity cost is emitted as `measured_local` only when explicit energy-per-task + tariff + source digest are supplied.

Missing fields remain listed as missing and keep the resource profile incomplete. Duplicate parameter inputs fail closed. Synthetic reference values are never copied into evidence. Probe summaries must remain inert and internally consistent with their top-level measurements.

Target flow:
`cheap source watcher -> local filter/dedupe -> normalized task -> policy/rights/quality/demand gate -> TaskEconomics -> I053 resource acquisition -> I054 evidence adapter -> I050 attestation -> I051/I052 attested Resource Router -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I055
Compose the full calibration path from I053 summary/declarations through I054 evidence and I050 attestation into I051/I052 attested dry-run routing. Missing/stale evidence must narrow to hold; complete synthetic fixtures must preserve calibration class/evidence bundle hash end to end.

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
