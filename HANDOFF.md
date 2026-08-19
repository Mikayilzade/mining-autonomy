# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open repository `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Do not reopen broad discovery unless implementation exposes a genuinely missing mechanism.
5. Continue Implementation / Experiment Phase from STATUS.
6. Re-check time-sensitive rules/economics with current primary sources before credentials, capital, hardware or paid infrastructure are used.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I028 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I028_CAPTURE_READINESS_PACKET.md`
- `implementation/capture_readiness.py`
- `implementation/test_capture_readiness.py`
- `implementation/RUN_I027_PRODUCTION_GAP_PRIORITIZER.md`
- I026–I027 evidence-audit/gap-priority files and prior receipt-gated archive/planner/manifest files named in STATUS.

## I028 result
`build_capture_readiness_packet()` converts the I027 selected read-only observation queue into exact future capture intents without performing network calls.

Important behavior:
1. sealed-manifest hash, source URL, platform, item index and manifest-item hash must match;
2. only scheduled GET/no-credential/no-action items are accepted;
3. exact expected evidence classes, environment requirement, provenance checklist and conservative source rate limit are preserved;
4. production demand/utilization-capable sources can become `ready_for_future_explicit_read_only_capture`;
5. unknown environment or observability/mechanics-only sources become `blocked_by_observability_or_environment_requirement`;
6. readiness never grants authorization — all network/action/credential flags remain disabled and explicit read-only network authorization is still required;
7. missing evidence remains unknown, never zero/negative demand.

Verification: eight deterministic tests passed in an isolated local harness. GitHub Actions workflow was unchanged and push-triggered CI remains disabled.

No live transport/network capture, credentials, KYC, wallets, paid infrastructure, service publication, task acceptance or settlement occurred.

## Current shortlist
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Immediate next run: I029
Build a deterministic capture-session planner over I028 ready items. Respect an overall request/time budget, group by host/rate contract, produce an exact chronological no-network session plan, and keep blocked items in a separate remediation queue. Still do not perform HTTP requests.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
