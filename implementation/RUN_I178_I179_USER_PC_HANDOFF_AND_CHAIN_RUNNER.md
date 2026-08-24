# I178-I179 — user-PC handoff manifest and inert one-command chain runner

Date: 2026-08-24

## Goal

Close the repository-side operational handoff gap after I177 without fabricating any user-PC, energy, tariff, accounting or market fact.

## I178

`i178_user_pc_handoff_manifest.py` is an inert exact-source handoff validator.

It embeds the current Git blob identities for the owned-PC chain required to reach I177 plus the downstream I050/I066/I123 source bindings. It verifies local files by Git blob hash, validates only structural completeness of caller-supplied measurement/accounting JSON and emits a machine-readable blocker report.

Current I178 blob: `9f227af6402e973b4a3b898b0bd9929cb61393cd`.
Current I178 test blob: `187b764e68c0340935d8fc089341153712ce1012`.

I178 never fills missing values. `READY_TO_RUN_REAL_LOCAL_CHAIN` means only: exact source tree + explicit ownership confirmation + structurally complete caller inputs. It does not mean that the facts are true and it does not authorize I050/I066/I123.

## I179

`i179_user_pc_real_chain_runner.py` turns the real local handoff into one explicit command while preserving existing gates:

`I178 -> I166/I165 -> I167 -> I168 -> I174 -> I175/I171 -> I177/I169`

The runner requires:
- exact local source tree accepted by I178;
- explicit `--confirm-user-owned-pc`;
- caller-provided measurement JSON;
- caller-provided accounting JSON;
- explicit UTC `--observed-at`;
- no implicit/current-time substitution.

Current I179 blob: `e0dac00cba1acbd9d5dbda6362867af298f50a0a`.
Current I179 test blob: `eda4df08e0aeb8aad83aee1380fb65f96c5b9335`.

I179 can finish only in one of these meaningful states:
- `REAL_CHAIN_READY_FOR_SEPARATE_EXACT_I050`: the assembled real evidence chain reached the existing strict I050 boundary; I050 itself is still not executed;
- `REAL_CHAIN_DECLARED_ACCOUNTING_BOUNDARY`: the only surviving source-class boundary is truthful declared accounting; current strict I050/I123 remains unchanged and I176 is not applied;
- `PASS_BLOCKED`: an earlier gate or source/input check failed.

## Exact source bindings embedded by I178

- I159 `b2b9e1a5a7808f75b935751cca64d00326d273e3`
- I162 `67319cf4d39b928c04531d4091a373a35d660136`
- I163 `9e6d0e95004506b6e384c813ddedb9e416e40db4`
- I164 `2a39371bd38b377340c18b1ce77c8bcdbd71c03f`
- I165 `c336efd57f61acf9d7fd7571e729a753ddbf3b91`
- I166 `a58a60c04d394a985f640b795ddb8b9ff2468464`
- I167 `4be411d0fdb7fdc03e4a490d502ef2b9dcb4b804`
- I168 `024b2e29d3eddee2ba94b789ce3c5ef2d2997ff6`
- I169 `26fa086c0c3130a88f2f8dd36a802062c56cdd7f`
- I171 `1d2e0cb92ba5883ee7e4deeb06f0b970b878f56a`
- I173 `29485940ac92c26616a9b60ee9e309110a4fbe62`
- I174 `569ec58988abdfa055cd172358a39ed88e36e5f3`
- I175 `f8b70be5a16479feb1ebeed8489d68bcdcd5ff33`
- I177 `9ecea6cbf9ae9bf023171b734f3750f44ec7a926`
- Resource Router `3dc7a7f7bbe1437ca4cd396767e20a857aa658cd`
- I050 `9b76a2194d15f8277d15b2e46c85df71cca08874`
- I066 `d995821e27ec27d72531dc71b433de702fb8fe7b`
- I123 `a3b7878b9114d3059784a4d3a0d6d6f55fa9fe3c`

## Tests

I178: 6 focused test functions authored.
I179: 4 focused orchestration test functions authored.

This run does **not** claim those tests were executed from a byte-for-byte exact full local checkout. The current environment still does not provide that complete local source tree through normal Git/DNS, and CI was not dispatched merely to obtain a green result.

## Safety outcome

No production market/API request, credentials, downloads/paid installs, account creation, paid infrastructure, task acceptance/submission, I050/I066/I123 execution, hybrid policy patch, spend, settlement, payment or value movement occurred.

## Next action

The repository-side handoff is now operationally one-command. The remaining forward step is a genuine run on the actual owned PC with real measurements/accounting provenance. If that cannot be done yet, the next safe repository task is to build blank non-evidence input templates/instructions and exact-source packaging support without auto-filling any measurement or accounting field.
