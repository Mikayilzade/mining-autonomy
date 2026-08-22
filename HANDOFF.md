# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I085 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I085_REAL_TRANSPORT_SAFETY_PREFLIGHT.md`
- `implementation/real_transport_safety_preflight.py`
- `implementation/test_real_transport_safety_preflight.py`
- `implementation/RUN_I084_EXACT_REAL_READ_ONLY_INVOCATION_CONSUMPTION.md`
- `implementation/exact_real_read_only_invocation_consumption.py`

## I085 result
The exact I084 one-attempt envelope now has a deterministic injected-evidence safety preflight. It revalidates the I084 envelope/receipt/scope/source lineage and requires fresh first-party anonymous-read-only policy evidence, public-only DNS evidence with exact address pinning plus anti-rebinding/alias checks, and a strict HTTPS/TLS GET-only zero-redirect JSON-only contract capped at one request and 1 MiB.

The preflight independently parses injected IP literals, so private or otherwise non-global addresses cannot pass merely by setting an `all_addresses_public` flag. Its successful safety envelope remains inert: no network-capable adapter is reachable and no DNS/HTTP is performed.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only invocation request -> fresh explicit I083 decision -> single-use I084 preflight -> injected-evidence I085 transport safety -> final exact human review -> separately authorized one-shot real observation`.

## Immediate next run: I086
Build the final immutable human-reviewable one-shot real-observation packet over I085. Revalidate I084/I085 hashes and expose the exact target fingerprint, hostname, pinned addresses, policy/DNS evidence hashes and HTTPS/JSON limits. Require a new fresh explicit decision bound to the exact packet before any network-capable adapter becomes reachable. Do not perform DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
