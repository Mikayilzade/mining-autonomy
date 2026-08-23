# RUN I155 — Connector blob ingest bridge

Date: 2026-08-24

## Goal
Continue the I154 exact 19-blob runtime materialization without weakening source binding when direct `git clone` is unavailable.

## Observed transport state
A fresh direct clone attempt still failed only at DNS resolution of `github.com` (`Could not resolve host`). GitHub connector reads remained available.

The first five I154 entries were materialized locally with exact Git blob identity preserved: the four seed JSON artifacts plus `i097_offline_packet_verifier.py`. Their computed Git blob SHA values matched I154 exactly.

A sixth attempted manual source transcription (`i098_fresh_execution_evidence_contract.py`) produced Git blob SHA `7b1a8d133ff135a1f483117bf10ae227dcec93e5` instead of expected `d6abaff46530063bf905c7b939e4a69f8eca1ccb`. The mismatch was rejected; the altered source is not eligible for I113. This confirms that visual/manual reformatting is not an acceptable connector transport.

## I155 implementation
Added `i155_connector_blob_ingest.py`, a network-inert fail-closed ingest bridge. Connector-delivered UTF-8 content is written only when the computed Git blob SHA equals the expected SHA. Invalid expected SHA or any byte-level change writes nothing.

Focused local tests: **3 passed**.

## Safety / effects
No production DNS/HTTP/TLS observation was performed. No credentials, registration, task acceptance, submission, spend, payment, wallet operation, CI dispatch, or value movement occurred. I113 was not executed.

## Outcome
**PARTIAL MATERIALIZATION; I113 STILL HOLD.** The source-binding rule held under a real transcription mismatch instead of silently accepting equivalent-looking code.

## Next action
Feed remaining connector-delivered blob contents through I155 without editing/reformatting. After all 19 entries are present and I154 reports `SOURCE_BOUND_I113_CLOSURE_READY`, execute I113 locally. If any blob cannot be transferred byte-for-byte, remain HOLD rather than substituting reconstructed source.
