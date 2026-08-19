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
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I014 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I014_PAYAN_SANITIZATION_HISTORY.md`
- `implementation/SOURCES_I014.md`
- `implementation/payan_sanitizer.py`
- `implementation/utilization_history.py`
- `implementation/test_payan_sanitizer.py`
- `implementation/test_utilization_history.py`
- prior I013 evidence replay/utilization files named in STATUS

## I014 result
A PayanAgent-specific raw-public-payload boundary now exists. `sanitize_payan_request` whitelists/normalizes identifiers, content, payout, currency, deadline and skills, while refusing to trust platform-provided metadata for ToS/rights/automation. Trusted policy and estimate evidence must be supplied separately. Non-open requests, conflicting aliases, unsupported currencies, missing payouts and malformed timestamps fail closed.

`sanitize_payan_receipt` normalizes USD/USDC value and UTC settlement time, accepts either direct USD value or cents but never both, hashes recognized buyer identity fields before persistence and emits no raw buyer/wallet/customer/payer identifier.

`compare_utilization_snapshots` aggregates each verified paid-utilization snapshot independently, rejects duplicate hashes and mixed platform/evidence histories, and only emits transaction/value deltas for observation windows with matching coverage duration. Mismatched windows explicitly return `None` deltas; no per-day/month extrapolation exists.

Fresh first-party observation on 2026-08-19 reconfirmed PayanAgent's public API design. The rendered Requests marketplace page exposed `0 open`; the rendered Receipts page exposed a live-feed shell but no attributable rows. Because these surfaces lacked raw payload/source timestamps, no evidence snapshot was fabricated. MCPize's current docs still confirm subscriptions + x402 and the standard 80% developer share; paid utilization remains unmeasured.

Push-triggered CI remains disabled and no manual workflow dispatch occurred. I014 is persisted as one atomic Git commit.

## Current shortlist
1. PayanAgent — parser-ready primary target; actual open-request flow and settled-receipt volume still need attributable observation.
2. OKX.AI A2A ASP — provider-side demand observation appears onboarding-gated.
3. agent2agent.market — adapter-ready; prior public observation showed zero open work.
4. AgentGigs.io — prior public jobs zero; Stripe/KYC geography gate.
5. MCPize — strongest passive endpoint candidate; utilization unknown.

## Immediate next run: I015
Build an offline observation-bundle pipeline joining sanitizer → evidence snapshot → saved-observation import → task replay/orchestrator + receipt aggregation/history → audit export. Add end-to-end fixtures/tests. Continue permitted public read-only observation, but never invent timestamps/demand.

## Hard action boundary
Without explicit user authorization do NOT spend money, create/fund wallets, sign value-moving transactions, stake/deposit collateral, rent paid infrastructure, create paid accounts, submit KYC/bank onboarding, accept paid work with liability/slashing risk, publish monetized services under the user's identity, or settle transactions. Read-only observation, public-data analysis, local/CI dry runs, architecture and capped simulations may continue.

## Compliance boundaries
Never use CAPTCHA bypass, fake activity, ad fraud, spam, prohibited multi-accounting, credential abuse, unauthorized access/scraping, KYC/geofence evasion, stolen resources, or botting human-only work contrary to ToS.

## Completion
Implementation is COMPLETE only when a real permitted autonomous test demonstrates positive economics with the stack documented, or reasonable candidates are exhausted and control passes confirm no viable implementation.
