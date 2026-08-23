# I154 — exact I113 runtime closure

Date: 2026-08-24

## Outcome

I154 closes the ambiguity around the source-bound local I113 bundle. The pre-stage current `main` snapshot was commit `3699c39aa3e61f217afd37cb44b7cfa0c33a1082`, tree `efb9a4d06e18a5d2ec9421aaaa1c7d379c6e8db9`.

The complete known seed/source closure required for the local chain is encoded in `i154_exact_i113_runtime_closure.py` as 19 exact Git blobs: four seed JSON artifacts plus fifteen Python modules spanning I097/I098, I099–I102, I105 and I106–I113. Every path is bound to its Git blob SHA.

The verifier is fail closed: a missing file, duplicate/invalid identity, or byte mismatch prevents `SOURCE_BOUND_I113_CLOSURE_READY`. The contract explicitly does not execute I113 and grants no network, credentials, authorization, spend, task action, payment, or value movement.

Focused local tests: **3 passed**.

A fresh direct clone attempt again failed only at container DNS resolution of `github.com`. This does not weaken the source identity requirement; connector transport remains the intended materialization route.

## New durable files

- `implementation/i154_exact_i113_runtime_closure.py`
- `implementation/test_i154_exact_i113_runtime_closure.py`

## Remaining runtime action

Materialize all 19 exact blobs from the bound source snapshot into one local directory, run the I154 byte verifier, and only if it reports `SOURCE_BOUND_I113_CLOSURE_READY`, execute I113. I113 remains **not yet executed** in this run.

## Safety state

No network observation, credentials use, registration, wallet, task acceptance, fulfillment, CI dispatch, spend, payment, or value movement was performed or authorized.
