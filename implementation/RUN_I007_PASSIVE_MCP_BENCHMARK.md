# Implementation Run I007 — passive MCP microservice benchmark

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E4**

## Objective
Advance the passive paid-endpoint branch without credentials, publication, paid infrastructure, wallet funding or settlement. Revalidate current MCPize economics, choose bounded capabilities with no questionable upstream API resale, and build an offline benchmark/economics harness.

## Current primary-source revalidation
Evidence checked 2026-08-19 against current MCPize first-party pages/docs:
- standard creator revenue share for new monetized servers: **80%**;
- subscription payouts use Stripe Connect and are monthly;
- x402 pay-per-call supports USDC on Base and free testing on Base Sepolia;
- documented x402 per-tool price range: **$0.01–$100**;
- MCPize FAQ currently advertises a **Free $0 hosting tier** with 250K requests/month, 0.5 vCPU and 512 MB;
- paid hosting starts at $9/month;
- marketplace/developer pages make substantial first-party demand/payout claims, but these remain platform claims and are **not treated as independent demand proof**.

Primary URLs:
- https://mcpize.com/docs/monetization
- https://mcpize.com/faq
- https://mcpize.com/developers
- https://mcpize.com/hosting

Important ambiguity: a May 2026 MCPize x402 blog post says 100% of USDC settles directly to the publisher wallet while also discussing a revenue-share rate. Current monetization docs state new servers default to 80% revenue share. Economics here therefore conservatively model **80% creator revenue**, not 100%, until a real test/receipt clarifies fee treatment.

## Selected bounded capabilities
Three deliberately boring local capabilities were selected because they have deterministic outputs, essentially zero external marginal cost, simple validation and no upstream API/model resale dependency:
1. `normalize_text` — whitespace normalization + basic counts.
2. `json_stats` — canonical JSON serialization + structural statistics.
3. `csv_profile` — local CSV shape/header/ragged-row profiling.

These are benchmark primitives, **not claims of buyer demand**. Their purpose is to validate the economics/serving path cheaply before investing in richer tools.

## Implementation
Added:
- `implementation/mcp_benchmark.py`
- `implementation/test_mcp_benchmark.py`

The harness:
- executes all three capabilities offline;
- benchmarks repeated local execution;
- carries an explicit per-capability economics model;
- calculates creator revenue/call, contribution/call, break-even calls/month and net at 100/1,000 calls/month;
- contains no network client, MCPize credential, wallet, publishing action or settlement path.

## Conservative economics
Initial experiment price assumption: **$0.01/call**, matching the documented x402 minimum.
Creator share assumption: **80%**.
Synthetic variable-cost reserves:
- normalize_text: $0.00001/call;
- json_stats: $0.00002/call;
- csv_profile: $0.00003/call.

At $0 fixed hosting on the advertised free tier, contribution is approximately:
- normalize_text: $0.00799/call;
- json_stats: $0.00798/call;
- csv_profile: $0.00797/call.

Illustrative monthly net before taxes/withdrawal/maintenance, **if paid demand existed**:
- 100 calls: about $0.797–$0.799;
- 1,000 calls: about $7.97–$7.99.

If forced onto the $9/month Starter tier, break-even at the same assumptions is roughly **1,127–1,130 paid calls/month**. At $29/month Pro it is roughly **3,630–3,639 calls/month**.

Therefore compute cost is not the bottleneck for deterministic microtools. **Demand and willingness-to-pay dominate.** A free hosting tier makes a zero-cash live experiment potentially attractive later, but account creation/publication/wallet/Stripe onboarding remain outside the current authorization boundary.

## Compliance / geography / KYC
- No questionable upstream resale is used by these three capabilities.
- Stripe subscription payout requires Stripe Connect; exact Azerbaijan eligibility must be verified before choosing that rail.
- x402 wallet settlement avoids bank onboarding at the protocol layer but wallet/off-ramp/local legal/tax obligations remain separate.
- No claim is made that Azerbaijan is eligible merely because no exclusion was observed.

## Test-status honesty
Files and tests are committed, but this run did not have a repository checkout/runtime path to execute the new unit tests. No false test-pass claim is made. Existing GitHub Actions workflow may need import-path adjustment or explicit inclusion before it exercises this new module.

## Outcome
E4 now has a concrete offline microservice/economics harness. For very cheap deterministic services, marginal execution cost is negligible relative to MCPize's minimum documented x402 price; the economic question is almost entirely whether paid calls actually arrive. This reinforces the project's main conclusion that utilization/fill rate must be measured before profitability can be claimed.

## Next run — I008
1. Integrate the benchmark capabilities with the common evaluator/orchestrator contract rather than leaving them standalone.
2. Add a passive-service decision model that can reject pricing below conservative marginal cost + margin and model free-vs-paid hosting tiers.
3. Inspect/update CI workflow so evaluator + MCP benchmark tests are both structurally runnable.
4. If possible without credentials, collect public marketplace evidence on comparable deterministic paid tools/prices; do not mistake listing counts for demand.
5. Keep publication, account creation, KYC, wallet funding and monetized deployment disabled.

Project state: **IMPLEMENTATION IN PROGRESS**.
