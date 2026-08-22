# I097 — Offline Packet Verifier / Authorization Binding

Date: 2026-08-22
Status: **COMPLETED AS SCOPED NETWORK-INERT SAFETY CHECKPOINT**

## Objective
Complete the exact safety step recorded by I096 before any real production observation: deterministically revalidate the I096 packet/scope binding, reject host/path/scope drift, require any future explicit authorization to name the exact I096 packet hash, and fail closed when authorization or fresh execution evidence is absent/stale.

## Work completed
Added `i097_offline_packet_verifier.py`, a stdlib-only network-incapable verifier. It:
- canonicalizes JSON as sorted compact UTF-8 JSON and recomputes SHA-256;
- confirms I096 exact-scope SHA-256 `df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e`;
- confirms I096 packet SHA-256 `0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56` after excluding only the packet-hash field itself;
- hard-binds scheme/host/path/query/adapter/fingerprint/method/request-count/environment;
- rejects any safety widening, including network enablement, credentials, task acceptance, submission, execution, value movement or treating the review packet as an execution token;
- requires a future authorization artifact to bind both exact packet and scope hashes, explicitly authorize only `ONE_ANONYMOUS_READ_ONLY_GET`, cap request count at one, forbid credentials/value movement, carry an ID and remain unexpired;
- requires future execution evidence to bind the same packet/scope, include policy/ToS, DNS and TLS evidence hashes, a non-empty pinned public-address set, current validity times, and an anti-rebinding revalidation requirement.

The module has an embedded offline self-test covering the canonical I096 packet plus path and scope tampering cases. No CI workflow was triggered to avoid notification spam.

## Current result
`I097_OFFLINE_PACKET_VERIFICATION_RESULT.json` records:
- packet integrity: **PASS**;
- exact host/path/scope binding: **PASS**;
- explicit authorization: **ABSENT / BLOCKED**;
- fresh policy/DNS/pinning/TLS execution evidence: **ABSENT / BLOCKED**;
- ready for network invocation: **FALSE**.

Therefore I097 closes the verifier/binding gap but deliberately does **not** authorize or perform the production request.

## Risks / boundaries
- No DNS resolution or HTTP request was performed.
- No credentials, wallet, payment, bid, acceptance, submission or value-moving action occurred.
- No authorization was inferred, fabricated or reused.
- A future valid verifier result still cannot itself call the network; the actual one-shot transport remains in the later separately authorized execution chain.
- Evidence freshness is fail-closed: malformed, future-dated, expired or unbound evidence is rejected.

## Files
- `implementation/i097_offline_packet_verifier.py`
- `implementation/I097_OFFLINE_PACKET_VERIFICATION_RESULT.json`
- `implementation/RUN_I097_OFFLINE_PACKET_VERIFIER.md`

## Next action — I098
Build the **fresh evidence acquisition plan/artifact contract** for the later one-shot observation, still network-inert. Define exactly how policy/ToS, DNS resolution, public-IP pinning, TLS/transport and anti-rebinding evidence will be represented, timestamped, hash-bound and consumed immediately before the single authorized GET. Do not perform DNS/HTTP and do not manufacture user authorization. Keep the Resource / Execution Router upstream and unchanged.
