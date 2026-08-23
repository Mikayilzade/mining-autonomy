# Implementation Runs I145–I147 — PayanAgent source narrowing

Date: 2026-08-23
Status: **COMPLETED AS BROAD SOURCE-EVIDENCE CHECKPOINT — OBSERVATION STILL BLOCKED**
Phase: Implementation / Experiment

## Objective
Advance the existing machine-to-machine paid-task shortlist toward one concrete bounded economic observation without reopening discovery or performing the production market feed GET.

## I145 — reproducible PayanAgent evidence packet
Added `i145_payanagent_source_checkpoint.py` and focused tests. The checkpoint encodes only current first-party facts collected on 2026-08-23 and feeds them through the existing I142 gate.

Current authoritative public documentation resolves six of seven I142 fields:

1. **Task-list read auth** — `GET /api/v1/requests?status=open...` is documented public.
2. **Task-detail read auth** — `GET /api/v1/requests/:id` is documented public.
3. **Platform fee** — current seller/concepts documentation says the marketplace currently does not take a fee; a small settled-receipt fee is described as a future possibility, not a current charge.
4. **Worker payout** — current request settlement is direct buyer-to-provider or escrow release to the provider; current docs do not describe a platform deduction from provider payout.
5. **Rate limit** — public endpoints are explicitly limited to **30 requests/minute per IP**.
6. **Automation permission** — PayanAgent explicitly describes itself as API-first, built for agents, programmatic, and requiring no human in the loop for the marketplace interaction model.

The seventh field, **geography/access rule**, remains unresolved. Current first-party docs reviewed do not state supported countries, a global-access guarantee, or an Azerbaijan-specific eligibility rule. The packet deliberately omits that fact rather than turning documentation silence into permission. Therefore I142 correctly remains `HOLD` with exactly one source blocker: `missing_required_fact:geography_access_rule`.

Authoritative sources reviewed:
- https://payanagent.com/docs/api
- https://payanagent.com/
- https://payanagent.com/docs/seller
- https://payanagent.com/docs/concepts

## I146 — Zentience deferred; shortlist advances without rediscovery
The prior Zentience candidate is explicitly **deferred** for this implementation path rather than repeatedly re-researched. The current public material is strongly agent-oriented and exposes public-looking task GET routes, but the source still lacks sufficiently explicit marketplace polling/geography evidence and cached public representations conflict on fee timing/semantics. This is enough to stop spending implementation cycles on it until its authoritative terms/API surface becomes clearer.

PayanAgent becomes the active source-evidence target because its current first-party API documentation is materially stronger and resolves authentication, economics, rate-limit and automation questions directly.

## I147 — exact bounded-observation parameters prepared but not promoted
The future PayanAgent read-only observation, if and only if the missing geography/access fact is resolved and the independent resource/runtime gates pass, should use the existing I140 framework with conservative parameters:

- endpoint family: public `GET /api/v1/requests` plus optionally public `GET /api/v1/receipts` for settlement evidence;
- no API key, wallet, registration or payment for observation;
- provider public limit: 30 req/min/IP;
- candidate polling interval: **5 seconds** (12 req/min), leaving headroom below the documented ceiling;
- first observation cap: **20 requests maximum**;
- deterministic local hash/dedupe before any AI escalation;
- stop immediately on 401/403/429, Retry-After, CAPTCHA/human challenge, geography/access restriction, changed docs/Terms, or response behavior inconsistent with the public read-only contract;
- never bid, accept, fulfill, approve, buy, register, sign or move value during this phase.

These are prepared parameters only. I140 is **not** instantiated as ready while geography/access evidence is absent, and no production PayanAgent request/receipt feed call was made in this stage.

## New evidence quality conclusion
PayanAgent is now much closer to a defensible real demand measurement than Zentience: only the explicit geography/access fact remains on the source side. Independent resource blockers remain unchanged: exact-current runtime evidence and genuine local energy + explicit tariff provenance are still required before the current `python_local` route can be called measured and conservative.

## Safety / actions not taken
No production market endpoint GET; no registration; no API key; no wallet; no payment; no bid; no task acceptance; no fulfillment; no purchase; no CI dispatch; no paid infrastructure; no value movement.

## Next broad action
First try to resolve PayanAgent's geography/access rule from current authoritative first-party material without guessing. If no explicit rule exists, preserve that blocker and move the source branch to a documented `policy_contact_or_user-local-access-required` state rather than fabricating eligibility. In parallel, whenever exact-current executable checkout becomes available, run the full I113 + I128/I129 -> I136/I138 resource cycle in one stage.

Only after both branches pass should I140/I141 be instantiated and exact bounded read-only observation authorization be requested/used.
