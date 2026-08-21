# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I065 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I065_RESOURCE_FEEDBACK_SUMMARY.md`
- `implementation/resource_feedback_summary.py`
- `implementation/test_resource_feedback_summary.py`
- `implementation/RUN_I064_RESOURCE_FEEDBACK_HISTORY.md`
- I063 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I065 result
The I064 append-only resource-feedback chain now has a deterministic verified-history current-state summarizer.

Important behavior:
1. the full I064 chain must verify before any derived current state is exposed;
2. invalid/tampered/regressed histories fail closed and withhold backend/parameter/routing state;
3. the compact snapshot binds history tip, immutable task identity and latest routing hash;
4. current selected backend and every recorded selected-backend transition are derived exactly from history;
5. latest `(backend, parameter)` evidence timestamps and provenance refs are tracked without averaging or inventing parameter values;
6. backend oscillation and repeated parameter updates are surfaced as deterministic churn/anomaly indicators only;
7. snapshot output is canonically hash-bound and post-build tampering is detectable;
8. I064 does not archive the numeric calibrated values, so I065 explicitly marks quantitative repricing as unresolved until exact evidence bundles are replayed;
9. multi-parameter I064 entries do not contain an explicit parameter -> evidence-hash map, so I065 conservatively preserves the complete entry evidence-hash set rather than guessing tuple order;
10. nine deterministic tests passed in an isolated interface-compatible harness; GitHub Actions was not dispatched.

Target flow:
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> provenance-sealed local benchmark -> verified receipt -> narrow measured feedback -> exact I052 replay/provenance gate -> re-attestation -> unchanged-task reroute -> append-only feedback history -> verified compact current-state snapshot -> evidence materialization -> later separately authorized real gates`.

## Immediate next run: I066
Build deterministic evidence materialization over I065. Supply the exact bound resource evidence bundles, revalidate their hashes/freshness and resolve the latest quantitative resource values only when every I065 reference is exactly accounted for. Multi-parameter set-only history bindings remain unresolved unless bundle contents prove the mapping.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. Benchmark feedback may only narrow/reprice a resource path; it cannot manufacture demand, permission, reliability or quality. I064 history records provenance/order; I065 summarizes verified provenance/current routing state; neither layer makes a backend live-authorized.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
