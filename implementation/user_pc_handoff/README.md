# User-PC handoff (NON_EVIDENCE templates)

These two JSON files are intentionally invalid as evidence. Do not invent values just to make the gate pass.

1. Keep the repository source files unchanged. I178 verifies exact Git blob identities.
2. Copy `measurement.NON_EVIDENCE.json` to a working JSON file and replace every null only with a genuine observed value/provenance from the owned PC.
3. Energy requires trustworthy before/after joule-counter or meter readings. If no trustworthy meter/counter exists, leave the real chain blocked; do not estimate energy.
4. Copy `accounting.NON_EVIDENCE.json` to a working JSON file and replace both accounting rows with truthful values and provenance. `user_declared` is allowed as a truthful source class but remains blocked by current strict I050/I123 semantics.
5. Run the structural/source check first:

```bash
python implementation/i178_user_pc_handoff_manifest.py --root . --measurement-json <real-measurement.json> --accounting-json <real-accounting.json> --confirm-user-owned-pc
```

6. Only after I178 returns `READY_TO_RUN_REAL_LOCAL_CHAIN`, run the local evidence chain with an explicit UTC timestamp:

```bash
python implementation/i179_user_pc_real_chain_runner.py --root . --measurement-json <real-measurement.json> --accounting-json <real-accounting.json> --observed-at <YYYY-MM-DDTHH:MM:SSZ> --confirm-user-owned-pc --output user_pc_chain_result.json
```

I179 still does not execute I050/I066/I123, contact a market, accept a task, use credentials, spend money or move value.
