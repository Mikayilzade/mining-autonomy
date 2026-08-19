# Implementation Run I016 — portable multi-market observation bundles

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Make the I015 evidence bundle durable across serialization/reload and prove that the same fail-closed audit contract can cover a second task market without adding credentials, task acceptance or payment authority.

## Changes

### 1. Deterministic bundle serialization + fail-closed reload
Extended `implementation/observation_bundle.py` with:
- `BUNDLE_SCHEMA_VERSION = 1`;
- deterministic `serialize_observation_bundle`;
- `load_observation_bundle` for JSON text, bytes, local path or mapping;
- exact top-level and manifest schema checks;
- supported-version enforcement;
- request/receipt child snapshot payload-hash verification;
- manifest-to-component hash binding checks;
- immutable `dry_run_only=True` / `action_enabled=False` verification;
- HMAC verification with a caller-supplied key that is never persisted.

A saved bundle is therefore rejected if its schema/version changes unexpectedly, a child payload is edited, component hashes diverge, action flags are changed, the manifest is modified, or the signature is wrong.

### 2. Second task-market envelope: agent2agent.market
Added `sanitize_agent2agent_task`, `build_agent2agent_request_envelope` and `build_agent2agent_observation_bundle`.

The sanitizer:
- accepts only `OPEN` tasks;
- requires a positive bounty;
- normalizes `task_id/id`, `bounty/bounty_usd`, `deadline/deadline_at`, skills/tags and USD/USDC currency;
- ignores platform-supplied metadata for rights/ToS/automation authorization;
- accepts trusted policy and cost-estimate evidence only from caller-controlled mappings.

The resulting `agent2agent_market` bundle goes through the existing snapshot → saved-observation importer → evidence-aware dry-run orchestrator → signed manifest path. It contains no signed acceptance, task claim, result submission, wallet, escrow or settlement function.

### 3. Expanded tests
`implementation/test_observation_bundle.py` now covers:
1. deterministic serialize → reload → reserialize roundtrip;
2. unsupported schema-version rejection;
3. unknown top-level field rejection;
4. child snapshot tamper rejection even when the old manifest/signature remain;
5. second-market positive dry-run replay with trusted policy/estimates;
6. proof that agent2agent payload metadata cannot self-authorize compliance;
7. the prior Payan positive replay, zero-open, provenance and tamper tests.

The connector/runtime did not provide a local repository checkout or manual CI execution in this run, so no green-CI claim is made. The Python sources were syntax-checked before persistence. Push-triggered CI remains disabled to avoid notification-email spam.

## Fresh public read-only checkpoint

### PayanAgent
Current first-party material still documents:
- anonymous `GET /api/v1/discover`;
- anonymous `GET /api/v1/receipts`;
- API-key-gated request bid/fulfill/approve operations;
- x402/USDC and public signed receipts.

No raw attributable API response with a trustworthy source timestamp was captured in this environment. No positive or negative quantitative utilization figure is inferred from the `24,000+` catalog claim.

### agent2agent.market
Current first-party site documents:
- anonymous `GET /api/tasks/{skill}` browsing;
- machine-native accept/submit lifecycle;
- USDC settlement after client approval;
- direct API/CLI onboarding.

Its current rendered app surface showed `Open tasks 0` and `no activity yet`. This is retained as a zero-open public observation, not as evidence of positive demand.

### MCPize
Current first-party material confirms:
- subscriptions and x402 pay-per-call;
- standard 80% developer subscription revenue / 20% platform fee for new monetization;
- Stripe Connect identity/tax onboarding for subscription payouts;
- x402 direct USDC settlement;
- publisher-side payment ledger, last-7-day revenue and transaction links in the Payments view.

This clarifies observability: attributable utilization appears strongest inside a publisher/account view. Public marketplace counts, example MRR calculators and creator anecdotes are not promoted to demand evidence. No account was created.

## Safety / external actions
No login, API key, account creation, KYC, wallet creation/funding, signed task acceptance, task submission, service publication, paid API/server, transaction or settlement occurred.

## Git / CI
Push-triggered CI remains disabled. This stage is designed as one atomic Git commit containing code, tests, sources, run log and checkpoint updates.

## Outcome
The offline control plane can now persist and reload signed evidence bundles safely and apply the same evidence/authorization separation to more than one task market. The remaining bottleneck is still real attributable demand/utilization, not internal architecture.

## Next — I017
Create a deterministic multi-platform bundle registry/history and evidence scorecard, preserving zero-open versus positive-paid-demand classes and rejecting duplicate bundle hashes. Continue anonymous/public PayanAgent and agent2agent.market observation; document MCPize's gated utilization surface without creating an account.
