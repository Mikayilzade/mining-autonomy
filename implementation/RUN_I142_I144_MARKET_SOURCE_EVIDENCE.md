# Implementation Runs I142–I144 — market-source evidence before observation

Date: 2026-08-23
Status: **COMPLETED AS BROAD SOURCE CHECKPOINT — OBSERVATION STILL BLOCKED**

## I142 — explicit source-evidence gate
Added `i142_market_source_evidence_gate.py`. A candidate public task market now needs explicit, non-conflicting evidence for public task-list/task-detail authentication requirements, worker/platform fee economics, provider/API rate limit or minimum interval, geography/access rules and automation permission. Missing or conflicting facts fail closed. This prevents a visually public marketplace page from being treated as sufficient authorization for a polling experiment.

## I143 — deterministic observation-source selector
Added `i143_observation_source_selector.py`. It ranks only already-shortlisted server-native machine-task sources and rejects any source whose public observation costs money, is not public-read capable, or lacks a passing I142 evidence packet. It never reopens broad discovery and never performs network access.

## I144 — current source revalidation checkpoint
A narrow current web revalidation was performed specifically to advance the existing highest-priority machine-to-machine paid-task direction, not to restart discovery. Several live machine-agent markets were visible, but the most concrete task-lifecycle candidate reviewed was Zentience because its public page exposes a REST task lifecycle and worker fee split.

Current evidence found on the public Zentience site/search index includes:
- `GET /marketplace/tasks` and `GET /marketplace/tasks/:id` are shown without the `AUTH` marker while bid/deliver endpoints are marked authenticated;
- the marketplace is explicitly agent-oriented and exposes task lifecycle `Open -> In Progress -> In Review -> Completed`;
- one current indexed version says completion pays 90% to the agent / 10% platform;
- another indexed version describes a 10% task-listing fee, creating an economics/policy inconsistency that must be resolved from one current authoritative representation before promotion;
- the site advertises automated bounty scanning, but no sufficiently explicit current public marketplace polling-rate/minimum-interval rule or geography/access rule was established in this checkpoint.

Therefore Zentience is **not promoted** to I140 observation design yet. I142 would fail it on missing rate-limit/minimum-interval, missing geography/access rule, insufficiently explicit marketplace automation permission scope, and conflicting fee semantics. No production marketplace endpoint was called by the implementation chain; no credentials, registration, wallet, payment, bid, claim, delivery or value movement occurred.

Evidence URLs reviewed (public read only):
- https://zentience.org/
- https://www.zentience.org/

Other machine-market search leads were deliberately not converted into a new discovery sweep. They remain outside the active implementation chain until the current candidate is resolved or rejected.

## Practical result
The next useful work is no longer another architecture micro-gate. Resolve one concrete source's policy/economics evidence to I142 completeness. In parallel, the independent resource/runtime blockers from I141 remain unchanged. Only when both resource readiness and a source evidence packet pass should I140/I141 be instantiated and exact bounded observation authorization requested.

## Safety
No spend; no credentials; no paid account; no registration; no task acceptance; no wallet; no production task-list GET; no CAPTCHA/KYC/geofence/rate-limit bypass; automatic CI remains disabled.
