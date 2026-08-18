# Implementation Run I003 — OKX.AI A2A task-intake observability

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E2**

## Objective
Determine how much buyer-side A2A task demand can be observed on OKX.AI without creating an account, Agentic Wallet, ASP identity, depositing funds, accepting work, bidding, or taking any other value-moving action. Map the observable contract to the common opportunity schema from I002.

## Fresh first-party validation
Current OKX.AI / Onchain OS documentation confirms that the A2A ASP mechanism remains live and is explicitly designed for agent-mediated custom paid work.

Confirmed current mechanics:
- ASPs can register an A2A service and earn fees from delivered work.
- A2A is for complex/custom tasks where agents negotiate scope, price and deliverables.
- Users can create tasks with title/description, budget and deadline.
- Matching can be direct assignment, automatic matching, or public listing.
- Tasks are **private by default**; unauthorized ASPs cannot proactively contact users.
- If a task is publicly listed, qualified providers can submit quotes.
- Current ASP registration docs explicitly tell a registered provider to let its Agent **browse open tasks** and negotiate to take an order.
- A2A funds are held in escrow on X Layer and released after buyer acceptance; no action for three days results in auto-acceptance according to current user docs.
- Rejected delivery can enter arbitration; current registration docs say an ASP initiating arbitration posts a 5% bounty deposit, refunded if successful and forfeited otherwise.
- The official open-source `okx/onchainos-skills` task marketplace implementation documents agent-role gates and task lifecycle commands. ASP actions are paymaster/gas-free in the current ASP playbook, but arbitration/deposit flows can still require value.

## Anonymous/public observability result
**No anonymous public task-feed endpoint or public task-board API was established from current first-party documentation in this run.**

The public docs confirm the *capability* for an Agent to browse open tasks, but the documented operational flow begins with:
1. install Onchain OS;
2. log in via Agentic Wallet/email;
3. register an ASP identity/service;
4. list/review the ASP;
5. then browse/open-task and negotiate flows become relevant.

The current open-source task CLI reference exposes account/agent-scoped task operations and ASP lifecycle commands, but this run did not find a documented unauthenticated equivalent of PayanAgent's public request/receipt feeds.

Therefore the following are deliberately **not fabricated**:
- current public open-task count;
- task arrival rate;
- budget distribution;
- category distribution;
- number of paying buyers;
- settlement velocity;
- repeat-buyer rate.

This is an observability/onboarding boundary, not evidence that demand is zero.

## Important architecture implication
OKX.AI A2A is a strong execution target but a weak **anonymous demand-measurement** target.

Unlike a market with a public request/receipt feed, a production OKX adapter is likely to need a legitimate Agentic Wallet + ASP identity before it can observe the provider-side opportunity stream in the intended way. That means the implementation can be prepared in dry-run form now, but live sampling should wait for explicit authorization if registration/login/identity creation is required.

## Common opportunity schema mapping v0.1
Fields inferable from the current documented A2A contract:

```json
{
  "platform": "okx_ai_a2a",
  "external_id": "jobId",
  "observed_at": "ISO-8601",
  "kind": "job",
  "status": "created|accepted|submitted|rejected|disputed|complete|refunded|close|unknown",
  "title": "documented task title",
  "description": "documented task description/summary",
  "tags": [],
  "budget_min_usd": null,
  "budget_max_usd": "max-budget when exposed",
  "fixed_payout_usd": "budget/token amount when normalized",
  "currency": "USDT|USDG|other",
  "deadline": "documented in user task creation flow; exact adapter field pending live payload",
  "bid_count": null,
  "buyer_id": "counterparty/user agent id when exposed",
  "buyer_reputation": null,
  "escrowed": "true after accepted/funded state; state-dependent",
  "input_schema": null,
  "output_schema": null,
  "requires_auth_to_accept": true,
  "requires_value_moving_action": true,
  "source_url": "OKX.AI / Onchain OS task source",
  "raw_observation_hash": "string|null"
}
```

Adapter note: do not force all budgets into USD until the token amount/symbol has a contemporaneous conversion source. Preserve native `tokenAmount` + `tokenSymbol` in raw metadata and normalize separately.

## Policy / risk gates specific to OKX A2A
Before a future live adapter may apply for a task, require:
1. provider identity/account authorized by user;
2. task is visible to the provider through the intended OKX flow;
3. task content passes legality/ToS/rights checks;
4. executor capability confidence above threshold;
5. worst-case model/API/tool cost bounded;
6. expected payout exceeds worst-case cost + failure reserve + minimum margin;
7. no work begins before accepted/escrow-funded state — current ASP playbook explicitly warns against delivering or executing real work before `job_accepted`;
8. arbitration is disabled by default because it can require a 5% bounty deposit; enable only with explicit policy/authorization;
9. no automatic external financial action beyond the specifically authorized settlement path.

## Demand-evidence classification
- Mechanism existence: **CONFIRMED**.
- Provider automation: **CONFIRMED**; current docs explicitly describe Agent browsing, negotiation and delivery.
- Anonymous open-task observability: **NOT ESTABLISHED**.
- Current task density: **UNMEASURED**.
- Current price/bounty distribution: **UNMEASURED**.
- Organic buyer demand: **UNMEASURED**.
- Settlement mechanism: **CONFIRMED** (escrow + acceptance/arbitration contract flow).
- Geography/KYC eligibility for Azerbaijan: **UNRESOLVED**; no assumption made.

## Ranking effect
OKX.AI A2A remains a top implementation candidate because the intended workflow is unusually close to the project's target architecture. However, it should not outrank a candidate with observable organic demand merely because the protocol is technically complete. Live demand remains the dominant unknown.

Provisional architecture ranking after I003:
1. PayanAgent — public contract/receipt surfaces documented; raw quantitative sampling still environment-blocked.
2. OKX.AI A2A — strongest documented autonomous negotiation/delivery workflow; provider-side observation appears gated by legitimate onboarding.
3. agent2agent.market — adapter-ready, but prior observed public state had no open tasks/activity.
4. AgentGigs.io — autonomous lifecycle, prior public jobs empty and Stripe/KYC geography gate.
5. MCPize — passive paid-endpoint candidate; buyer demand needs independent measurement.

## No-action boundary respected
No OKX account was created or logged into. No Agentic Wallet or ASP identity was created. No task was accepted/applied for. No bid/quote was submitted. No wallet was funded. No arbitration deposit was posted. No paid infrastructure was used.

## Result
E2 anonymous observability checkpoint is complete. OKX.AI confirms the target machine-to-machine paid-work architecture, but current quantitative demand cannot be measured anonymously from a documented public feed.

### Next run
**I004 / E3 — cross-market dry-run evaluator v0.1.**

Build the platform-neutral decision engine around the I002 opportunity schema, with captured fixtures for PayanAgent / OKX.AI / agent2agent.market-style jobs. It must include:
- schema validation;
- compliance/policy gate;
- capability matching;
- conservative cost estimator;
- payout normalization;
- EV/margin threshold;
- reject reason codes;
- dry-run executor stub;
- result validation stub;
- append-only decision ledger format;
- settlement adapter hard-disabled.

No credentials or value-moving actions are needed for I004.

Project state: **IMPLEMENTATION IN PROGRESS**.

## Sources checked (2026-08-19)
- OKX.AI official ASP Introduction: https://web3.okx.com/onchainos/dev-docs/okxai/asp-introduction
- OKX.AI official ASP Registration: https://web3.okx.com/onchainos/dev-docs/okxai/registerasp
- OKX.AI official A2A Guide: https://web3.okx.com/onchainos/dev-docs/okxai/how-to-become-a2a
- OKX.AI official User / task flow documentation: https://web3.okx.com/onchainos/dev-docs/okxai/user-introduction
- OKX official open-source Onchain OS skills: https://github.com/okx/onchainos-skills
- Task marketplace CLI reference: `skills/okx-ai/references/task-cli-reference.md`
- ASP role playbook: `skills/okx-ai/references/task-asp.md`
