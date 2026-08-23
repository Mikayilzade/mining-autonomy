# I158 — local_model no-spend evidence gate

Date: 2026-08-24

## Scope
Advance the existing I134/I137 `local_model` branch without downloads, credentials, network use, paid infrastructure or spend.

## Current execution-environment observation
A local-only executable/device probe found no `ollama`, `llama-server`, `llama-cli`, `lmstudio`, `nvidia-smi`, or `rocminfo` executable; no `/dev/nvidia*` or `/dev/dri/*` device was exposed. The environment identified itself as Linux x86_64. No model was downloaded or installed to change this result.

These observations establish only absence of a usable local-model/GPU interface in the current execution environment. They do not claim that the user's owned PC lacks a GPU/model, and they do not infer hardware from subscription capabilities.

## Gate
Added `i158_local_model_evidence_gate.py`. Production evidence requires all of: bound model interface+identity, verified programmatic access, measured quality acceptance, latency, reliability and parallelism, plus measured per-task energy and explicit tariff provenance. Partial facts cannot promote the backend. Downloads/installations performed merely to make the probe pass, credentials/network use or spend fail closed.

Current branch state: **NO_LOCAL_MODEL_INTERFACE_OBSERVED** in this execution environment.

Therefore `local_model` is exhausted as a no-new-spend branch here. Per the existing fallback ladder, advance to `owned_pc`, but keep it evidence-only: repository automation cannot assume the user's physical PC hardware, availability, energy draw or tariff. A later owned-PC measurement packet may be prepared without executing on that machine.

## Safety / external effects
No model download, model execution, GPU job, network request, credential use, CI dispatch, paid account, infrastructure rental, task acceptance, spend, payment or value movement occurred.

## Next action
Advance I137 to `owned_pc`. Define a portable, fail-closed owned-PC evidence packet/probe that the user can eventually run locally if desired, covering hardware identity, availability, benchmark quality/capacity/latency/reliability, measured energy and explicit tariff/opportunity cost. Do not fabricate measurements and do not reopen discovery.
