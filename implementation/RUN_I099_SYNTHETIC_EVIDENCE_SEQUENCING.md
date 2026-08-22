# I099 — Synthetic Evidence Acquisition / Sequencing Harness

Date: 2026-08-22
Status: **COMPLETED AS SCOPED NETWORK-INERT CHECKPOINT**

## Goal
Prove the exact I098 evidence acquisition order using synthetic fixtures only, then project the resulting valid synthetic bundle into the older I097 execution-evidence shape without manufacturing authorization or enabling transport.

Required order:

`policy/ToS -> DNS/public-IP pins -> TLS-to-pin -> immediate anti-rebinding -> final I098 bundle -> I097 compatibility projection`

## Implemented
Added `implementation/i099_synthetic_evidence_sequencer.py`.

The harness:
- imports and reuses the exact I098 validators instead of reimplementing looser checks;
- accepts only the next expected evidence type and does not advance state after a rejected/reordered component;
- validates policy freshness/permission fields before DNS;
- validates DNS public-address pins before TLS;
- requires TLS `connected_ip` to be inside the accepted DNS pin set;
- requires anti-rebinding to reproduce the same pin set immediately before the hypothetical request;
- finalizes only after all four ordered components are present;
- builds the I098 bundle with canonical component hashes and earliest-expiry semantics;
- projects that bundle into I097's `execution_evidence` compatibility shape;
- deliberately passes `authorization=None` into the I097 compatibility check, so the full result must remain `BLOCKED` even when packet integrity and synthetic execution evidence pass.

## Embedded negative cases
The self-test rejects:
1. omitted anti-rebinding component;
2. reordered TLS-before-DNS evidence;
3. stale policy evidence;
4. TLS connection to a public IP outside the DNS pin set;
5. exact path/query drift from `GET /api/v1/requests?status=open&limit=1`;
6. anti-rebinding address-set drift.

## Safety properties
- `network_capable=false`
- `execution_token=false`
- no DNS resolution;
- no sockets/TLS connection;
- no HTTP;
- no credentials;
- no bidding/task acceptance/submission;
- no wallet/payment/value movement;
- no user authorization is generated or inferred;
- synthetic fixtures are explicitly marked as synthetic and cannot substitute for fresh production evidence.

## Validation note
The script contains deterministic embedded assertions/self-tests, but no GitHub Actions workflow was dispatched in this run. This is intentional: the repository's recent failing PR runs generated notification spam, and the current connector does not provide an isolated local repository execution environment. The checkpoint therefore records the sequencing implementation and its fail-closed test contract without claiming fresh CI/runtime evidence.

## Result
I099 closes the design/implementation gap between the I098 evidence contract and I097 compatibility semantics. It does **not** remove the production blocker.

The one-shot PayanAgent observation still requires both:
1. fresh real policy/DNS/TLS/anti-rebinding evidence acquired at execution time; and
2. a separate explicit user authorization bound to the exact I096 packet and scope hashes.

## Risks / remaining uncertainty
- Real evidence acquisition has not occurred.
- Real network behavior, live DNS answers, TLS chain and current PayanAgent policy are unmeasured in this checkpoint.
- No live demand observation exists yet, so real economics remain unconfirmed.
- Embedded self-test needs execution in a notification-safe/no-network environment before being treated as runtime evidence.

## Next action
I100: add a **network-inert execution readiness manifest / dry-run verifier** that consumes the I099 sequencing output contract plus I096/I097/I098 bindings, exposes every remaining blocker as machine-readable booleans, and keeps real network invocation impossible. If a notification-safe local execution facility becomes available, run the I099 self-test there; do not trigger repeated PR CI solely for evidence. Do not acquire live evidence or perform the production GET without separate explicit authorization.