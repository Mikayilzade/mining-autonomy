# Run I166 — user-PC real-evidence gate

Date: 2026-08-24

## Objective
Harden the last repository-side boundary before a real user-owned-PC materialization so synthetic/unit-test provenance cannot accidentally be promoted into I165/I162/I159 as production evidence.

## Outcome
Added `i166_user_pc_real_evidence_gate.py` and focused tests.

I166 is intentionally narrower than I165. It does not benchmark hardware, measure energy, obtain a tariff, infer availability, or create economics. It validates only the caller-supplied external evidence packet before I165 may consume it.

The gate:
- requires explicit `--confirm-user-owned-pc`;
- accepts only the external fields already allowed by I165;
- requires complete availability, energy-counter, tariff and opportunity-cost groups;
- rejects fixture/example/synthetic/placeholder/dummy/mock provenance labels;
- validates availability range, monotonic non-negative joule counters, positive task count, non-negative tariff and non-negative opportunity cost;
- emits a blank all-null template that is explicitly `TEMPLATE_ONLY_NOT_EVIDENCE`;
- passes accepted facts to I165 only after the real-evidence gate is clean;
- never promotes a rejected packet and never creates a production execution route.

## Safety reason
I165 has a positive-completion unit test containing labelled `test-fixture:*` values. Those values are appropriate for unit testing the merge/control path but must never be reusable as real resource evidence. I166 adds an explicit production boundary preventing that class of accidental promotion.

This remains fail-closed. A source reference string passing the lexical gate is not independently verified truth; the actual measurement/provenance must still be genuine and produced on the user-owned PC or from an applicable real source. The repository must not fabricate those facts.

## Focused tests authored
`test_i166_user_pc_real_evidence_gate.py` covers:
1. blank template remains null/non-evidence;
2. fixture/placeholder provenance rejection;
3. mandatory ownership confirmation;
4. partial energy-group rejection;
5. complete well-formed packet acceptance at the gate only;
6. invalid ranges/counter order rejection.

The tests were authored in this run. No CI workflow was dispatched solely to execute them; do not claim a pass until an exact source-bound local execution is available.

## External effects
No production market/API request, credentials, downloads/paid installs, CI dispatch, account creation, paid infrastructure, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Remaining boundary
The next decisive step is still physical-machine materialization: run I166/I165 on the actual user-owned PC and provide only genuinely observed evidence with provenance. If no trustworthy joule counter/meter exists, remain `PASS_BLOCKED` rather than estimating energy.

If I166 accepts the real packet and I165/I162 reach `USER_PC_PACKET_COMPLETE`, feed that result into the existing I050/I066/I123 -> I130/I131/I133 -> I136/I138 conservative economics/readiness chain. This evidence assembly does not authorize any production market observation, credential use, paid task acceptance, spend or value movement.
