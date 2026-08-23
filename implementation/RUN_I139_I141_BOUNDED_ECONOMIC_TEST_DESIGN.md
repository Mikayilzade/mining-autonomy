# Implementation Runs I139–I141 — bounded economic-test design

Date: 2026-08-23
Status: **COMPLETED AS BROAD SOURCE CHECKPOINT — EMPIRICAL EXECUTION STILL PENDING**
Phase: Implementation / Experiment

## I139 — portfolio input-integrity hardening
Hardened `i136_conservative_portfolio_evaluator.py` so one-shot iterables are materialized once, duplicate backend definitions and duplicate evidence fail closed, and watcher budgets cannot silently reference unknown backend IDs. This removes a class of orchestration bugs before real evidence is consumed.

## I140 — bounded read-only observation design
Added `i140_readonly_observation_design.py`. It turns current public/read-only policy facts into a capped observation manifest without performing any request.

The design requires: current policy evidence reference, confirmed public read-only allowance, no credentials, no paid account, no CAPTCHA/human challenge, allowed geography, a caller-supplied minimum allowed interval, a hard request cap, zero external paid-request cost, and explicit local/AI incremental-cost assumptions. Requested polling faster than the known allowed limit fails closed rather than being throttled by circumvention.

The future runner is required to stop on policy drift, rate-limit/Retry-After signals, authentication/CAPTCHA, geography/access restrictions, request-cap exhaustion, or behavior inconsistent with the read-only contract. It must never accept or submit paid work.

The observation result schema now specifies the actual empirical fields needed for economics: unique opportunities, duplicates, public payout/fees, machine-executable eligibility, public availability signals, expiry/deadlines, parse success and latency. This is the bridge from architecture to measured arrival/demand data.

## I141 — integrated economic-test packet
Added `i141_economic_test_packet.py`. It combines I138 readiness, I136 conservative portfolio selection and I140 bounded observation design. The packet reaches `READY_FOR_SEPARATELY_AUTHORIZED_READONLY_ECONOMIC_TEST` only when:
- an exact current conservative backend route already exists;
- runtime/resource/fresh-market-policy/authorization gates represented by I138 are complete;
- the read-only observation plan itself is bounded and no-spend.

Even then, the packet is a manifest only: observation/network execution, credentials, task acceptance, spend and value movement remain disabled in the source object.

The post-observation decision contract is explicit. Zero eligible demand remains a measured negative result rather than being hidden; non-positive conservative margin deprioritizes/rejects the route; positive read-only economics only justifies designing a later tiny real-task test and does not imply permission to accept work.

## Verification added
Added `test_i139_i141_broad_observation_readiness.py` covering generator-safe evidence handling, duplicate backend rejection, bounded observation planning, rate-limit/CAPTCHA/paid-request rejection and the conjunction required for an economic-test packet.

No hosted CI was enabled or dispatched, so no notification spam was generated. No production market request, credentials, KYC, paid account, task acceptance, submission, wallet, settlement, spend or value movement occurred.

## Current practical boundary
The project is now architecturally ready to define a real bounded read-only economic measurement, but empirical execution is still blocked by the earlier independent facts: exact-current runtime receipt, materialized no-spend backend evidence (currently local energy + explicit tariff for `python_local`), fresh market/policy evidence, and exact one-shot observation authorization.

## Next broad stage
Do not add more micro-gates. At the first executable current checkout, run the full local resource/runtime chain and I136/I138. If `python_local` survives, instantiate I140/I141 against the highest-ranked currently permitted public observation source and request/use exactly the bounded observation authorization required by that manifest. If local evidence/economics fails, advance through I137/I134 to free/conditional CI or the next existing no-new-spend branch, then apply the same I136/I140/I141 framework. Do not accept paid work or move value during the observation phase.
