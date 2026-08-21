# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I067 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I067_MATERIALIZED_ATTESTED_ROUTING.md`
- `implementation/materialized_attested_routing.py`
- `implementation/test_materialized_attested_routing.py`
- `implementation/RUN_I066_RESOURCE_EVIDENCE_MATERIALIZATION.md`
- I065 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I067 result
I067 closes the resource-feedback loop back into attested routing.

Important behavior:
1. upstream observation/policy/capability/quality/demand runs before resource materialization;
2. only upstream `accept_dry_run` proceeds;
3. I067 re-runs I066 from the exact I065 snapshot + exact current reference backends + explicitly supplied bound I050 evidence bundles;
4. the I066 materialization hash must verify;
5. only `materialized_reproducible` profiles with nested `calibrated_reproducible` state, no declaration and complete current evidence are converted into I051 attestations;
6. declared/stale/missing/tampered/incomplete/reference-mismatched resource state cannot enter the selectable route set;
7. existing I052/I051 routing is reused rather than bypassed;
8. replay output binds to I065 `history_tip_hash` + I066 `materialization_hash`;
9. route drift records reference vs calibrated marginal cost, success probability, latency and planning state;
10. selected backend before/after and route churn are diagnostics only;
11. all execution/network/credentials/submission/value movement flags remain disabled.

Target flow:
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> provenance-sealed local benchmark -> verified receipt -> narrow measured feedback -> exact I052 replay/provenance gate -> re-attestation -> unchanged-task reroute -> append-only feedback history -> verified current-state snapshot -> exact evidence materialization -> I067 current-resource attested reroute -> market-side readiness packet -> later separately authorized real observation`.

## Immediate next run: I068
Build the deterministic market-side readiness checkpoint. Join the exact one-read-only-request authorization/compliance chain (I038–I047) with the current I067 resource-route readiness, without performing network access. The packet must state the exact observation needed, why it closes the dominant demand unknown, which resource route will evaluate it, and which authorization/compliance/evidence gates are still unresolved.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current reproducible evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. Benchmark feedback may only narrow/reprice a resource path; it cannot manufacture demand, permission, reliability, quality or authorization. I067 makes current resource measurements operational only for dry-run repricing.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
