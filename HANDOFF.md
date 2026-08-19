# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Do not reopen broad discovery unless implementation exposes a genuinely missing mechanism.
5. Continue Implementation / Experiment Phase from STATUS.
6. Re-check time-sensitive rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I015 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I015_OBSERVATION_BUNDLE.md`
- `implementation/SOURCES_I015.md`
- `implementation/observation_bundle.py`
- `implementation/test_observation_bundle.py`
- prior I014/I013 evidence, sanitizer, snapshot, importer, orchestrator and utilization files named in STATUS

## I015 result
The PayanAgent evidence path is now end-to-end offline.

`build_payan_request_envelope` sanitizes permitted request records, sources trusted policy/estimate evidence only from caller-controlled mappings, and creates a canonical SHA-256-bounded `official_api` snapshot. Empty request feeds default to `unknown` evidence rather than falsely proving open paid demand.

`build_payan_receipt_envelope` sanitizes receipts through the existing buyer-identity minimization boundary and requires explicit source provenance. A paid-utilization evidence claim cannot be made from an empty receipt set.

`build_payan_observation_bundle` imports/revalidates snapshots, replays only genuine `open_paid_request` evidence into the dry-run orchestrator, aggregates settled receipts, optionally compares prior equal-duration utilization windows, then emits one manifest binding all component hashes.

The manifest digest is HMAC-SHA256 signed using a caller-supplied offline key that is never persisted. This signature is only a tamper/authenticity seal for our local evidence bundle; it is not a PayanAgent receipt signature, wallet signature, transaction authorization or permission to act.

Fresh PayanAgent first-party material on 2026-08-19 still documents public `discover`/`receipts`, API-key-gated request operations, x402/USDC and public signed receipts. No trustworthy raw attributable API payload + source timestamp was captured, so no real demand/utilization figures were created.

Push-triggered CI remains disabled and I015 is one atomic commit.

## Current shortlist
1. PayanAgent — end-to-end evidence pipeline ready; measurable public task/receipt utilization still uncaptured.
2. OKX.AI A2A ASP — provider-side demand observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed zero open work.
4. AgentGigs.io — prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; utilization unknown.

## Immediate next run: I016
Add serialization/reload + schema version corruption tests for bundles; generalize the envelope to another task market; continue permitted public PayanAgent observation and deepen MCPize utilization observability if Payan remains quantitatively opaque.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
