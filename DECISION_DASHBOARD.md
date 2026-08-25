# Mining Autonomy — Decision Dashboard

**Updated:** 2026-08-25  
**Purpose:** convert the completed discovery work and current implementation state into a decision surface. This is not a new discovery pass and not production authorization.

## 30-second answer

- **No real profit is proven yet.** Current measured non-synthetic production route surviving conservative economics + watcher overhead: **none**.
- **Discovery is complete (Runs 001–062).** The catalog covered compute/GPU/AI, storage, bandwidth/relay, nodes, proof markets, task/agent markets, home/device paths, capital-yield paths, build-once digital income, and common low-quality/prohibited families.
- **The implementation shortlist is machine-task first.** Canonical I001 ranked: **PayanAgent**, **OKX.AI A2A ASP**, **agent2agent.market**, **AgentGigs.io**, **MCPize**, **OKX.AI A2MCP**, **API Mart**, then compute/inference suppliers.
- **PayanAgent remains the primary dry-run/read-only target.** I002 did not establish quantitative public-feed demand; supply counts must not be mistaken for paid worker demand.
- **OKX.AI A2A remains a strong second target.** I003 did not establish anonymous live task observability and the legitimate provider path appears onboarding-gated.
- **The execution side is still missing real owned-PC cost evidence.** I181 must run on the actual owned PC before local energy economics can be trusted.
- **Resource / Execution Router is already implemented and hardened through I196.** The bottleneck is now evidence, not more repository-only architecture.

## Decision state now

| Decision | Status | Recommendation | Why |
|---|---|---|---|
| Reopen broad discovery | **NO** | Do not reopen | Discovery is complete; current gap is real market + execution evidence. |
| Run I181 on the owned PC | **GO — local/no spend** | **Do next** | Establishes whether a trustworthy built-in cumulative energy counter exists. |
| Buy a power meter | **NO** | Do not buy | Not authorized; I182 is allowed only with an already-available trustworthy whole-system meter. |
| Authorize bounded read-only production observation | **USER DECISION** | Useful for market-side progress | Current authorization is `false`; this can gather public production/economic evidence only where rules permit it. |
| Pay for API / VPS / GPU / account | **NO** | Do not spend yet | No real positive margin has been demonstrated. |
| Accept/fulfil paid work or move value | **NO** | Not ready | Requires real conservative economics plus separate explicit authorization. |

## Evidence funnel

```text
Broad opportunity universe
        ↓
Discovery Runs 001–062 COMPLETE
        ↓
I001 implementation shortlist (8 rows)
        ↓
#1 PayanAgent — primary dry-run target
#2 OKX.AI A2A — primary validation target
        ↓
I002/I003 observability checks: real demand still not established
        ↓
Cross-market evaluator + Resource / Execution Router built and hardened
        ↓
Real execution-cost evidence: MISSING
Real task payout/acceptance/failure/fee evidence: MISSING
Read-only production observation authorization: FALSE
        ↓
Real conservative positive route: NONE YET
        ↓
Bounded monetization test: NOT READY / NOT AUTHORIZED
```

## Evidence labels

| Label | Meaning |
|---|---|
| `PROVEN_REAL` | Non-synthetic measured evidence from a permitted real environment. |
| `PUBLIC_SPEC` | Public documentation/surface supports the mechanism but not our unit economics. |
| `OBSERVED_LOW/EMPTY` | Public snapshot showed weak/zero visible demand; this is a snapshot, not a permanent verdict. |
| `SYNTHETIC_VALIDATED` | Code/fixtures prove routing/accounting behavior, not income. |
| `UNKNOWN` | Required economic input has not been observed. |
| `BLOCKED` | Required measurement or authorization is absent. |
| `PARKED` | Retained but not the current next priority. |

## Canonical candidate board

The table below preserves the current `implementation/RUN_I001_CANDIDATE_RANKING.md` shortlist and folds in the later I002/I003 observability outcomes. Rankings are **validation priorities**, not profitability proofs.

| Rank | Candidate | I001 verdict | Evidence useful for a decision | Current state | Main blocker | Next safe action |
|---:|---|---|---|---|---|---|
| 1 | **PayanAgent** | **PRIMARY DRY-RUN TARGET** | API-first request/bid/fulfil model documented; public offer/receipt claims existed; I002 did **not** establish quantitative paid request flow | **BLOCKED on real demand/economics** | Real bespoke request density, collectible payout, acceptance/rejection, fees/settlement + current read-only authorization is false | First market-side read-only target once separately authorized |
| 2 | **OKX.AI A2A ASP** | **PRIMARY VALIDATION TARGET** | Official workflow supports browsing/open tasks, negotiation, escrow and approval; I003 did not establish anonymous live feed | **BLOCKED / onboarding-gated** | Live task density/prices, geography/KYC/onboarding and real economics | Keep second; no registration/account action without separate authorization |
| 3 | **agent2agent.market** | WATCH + ADAPTER TARGET, NOT FIRST MONEY TEST | I001 public app snapshot showed **0 open tasks / no activity** on Base Sepolia despite a strong machine-native worker flow | **WATCHLIST — demand weak at observed snapshot** | Production-vs-testnet ambiguity and real paid demand | Keep adapter-compatible; do not prioritize money test without new demand evidence |
| 4 | **AgentGigs.io** | WATCH / GEO-GATED | Full API/webhook/SSE lifecycle documented; I001 public jobs page snapshot showed **0 total/open jobs** | **WATCHLIST — demand + payout geography blocked** | Real job flow; Stripe Connect KYC/bank availability and geography | Do not onboard until both demand and payout eligibility justify it |
| 5 | **MCPize** | PASSIVE SELLER EXPERIMENT CANDIDATE | Monetized MCP hosting/listing model documented; I001 recorded first-party vendor/platform claims and a 20% platform fee | **PARKED passive-seller path** | Actual buyer demand for a specific cheap capability, payout geography/KYC, hosting/model/API economics | Model only; do not publish or onboard yet |
| 6 | **OKX.AI A2MCP** | SECONDARY PASSIVE TARGET | Marketplace listing path exists; volume unmeasured | **PARKED** | Real buyer volume, x402/wallet/review and payout economics | Secondary after stronger market evidence |
| 7 | **API Mart** | WATCHLIST | Discovery evidence was low/unproven | **PARKED** | Current demand, resale/upstream rights, wallet/geography and margin | No priority while primary targets unresolved |
| 8 | **Compute / inference suppliers** | DEFER until task-market tests | Real provider family exists but is platform/hardware specific | **DEFERRED; local-cost evidence missing** | Hardware/provider eligibility, work supply, payout, electricity/opportunity cost | Run I181 first; revisit provider class with real owned-PC economics |

Machine-readable version: [`CANDIDATE_SCORECARD.csv`](CANDIDATE_SCORECARD.csv).

## What the larger discovery covered

The implementation shortlist is intentionally narrow. `CATALOG.md` contains a much larger universe, including:

- server CPU/compute markets (Golem/Akash-style provider paths);
- GPU/AI compute markets (Vast/Nosana/Golem GPU/io.net/Salad-style paths);
- AI incentive networks, transcoding, storage, bandwidth/relay nodes;
- blockchain service nodes, indexing/RPC, ZK/prover and keeper/solver infrastructure;
- legitimate automated jobs and machine-to-machine task markets;
- home/device bandwidth, GPU/CPU and storage sharing;
- physical DePIN and device contribution;
- capital-based yield and automated trading families;
- build-once APIs, micro-SaaS, digital products, licensing and asset rental;
- usually unsuitable families such as faucets/ad-clicking, human microtasks and opaque cloud-mining schemes.

This dashboard does not re-score all discovery leads. Full audit trail stays in `CATALOG.md` and `RUN_LOG.md`.

## Resource / Execution Router — practical view

| Backend | Cost treatment | Current usability | Decision |
|---|---|---|---|
| **Pure Python / deterministic local code** | Marginal CPU/energy/time + opportunity cost; fixed/sunk separated | Available for offline/dry-run | **First choice whenever it can satisfy acceptance criteria** |
| **Owned PC CPU/GPU/local model** | Electricity + retry/failure + maintenance + opportunity cost; owned hardware purchase is sunk, not a new per-task purchase | Technically available, exact economics blocked | **Measure via I181 → genuine I166 → I178/I179** |
| **Existing ChatGPT/Codex subscription** | Fixed/sunk/limited capacity; neither “free unlimited API” nor full monthly fee per task | Human-triggered project capability; no assumed autonomous API access | **Useful for project work, not assumed production backend** |
| **Free / conditional-free CI/cloud tier** | Quota/capacity/reliability still matter even when marginal cash price is zero inside allowance | Permitted dry-run/testing only | **Use selectively; never treat quota as infinite** |
| **Cheap external LLM/API** | Per-call/token + retry/failure + credentials/payment | Current gate blocks paid/credential use | **Do not activate yet** |
| **Stronger external API** | Higher marginal cost; justified only by acceptance/quality uplift | Blocked | **Escalate only when cheaper backend cannot clear acceptance + margin** |
| **Future VPS/server** | Rent + bandwidth + maintenance + opportunity cost | Not authorized | **Do not rent before real positive economics** |

Routing rule: **cheap deterministic filter → deterministic/local execution where sufficient → AI only when needed → cheapest backend that clears acceptance probability and conservative positive post-fixed margin.**

## Two independent evidence tracks still missing

### Track A — real execution cost

1. Run **I181 on the actual owned PC**.
2. Use a validated built-in cumulative energy counter if available.
3. Otherwise use **I182 only with an already-available trustworthy whole-system cumulative external meter**.
4. Add genuine electricity tariff, availability, opportunity-cost basis, ownership confirmation and explicit UTC `observed_at`.
5. Run exact **I178/I179**.
6. If no trustworthy measurement route exists, keep energy `BLOCKED`; do not estimate it and do not buy hardware.

### Track B — real market revenue

For a first server-native candidate, the project still needs real permitted evidence for:

- task/request volume and age;
- payout/budget/settlement basis;
- competition/hiring/acceptance probability;
- approval/rejection/dispute/non-payment behavior;
- retry/failure frequency and cost;
- platform/payment/withdrawal/gas/conversion costs;
- watcher/polling overhead;
- maintenance/human time.

Current authorization for bounded read-only production observation is **false**.

## GO rule for a first monetization test

A real bounded test should be proposed only after both evidence tracks exist and the Router shows conservatively:

```text
expected collectible revenue
- platform/payment/withdrawal/conversion costs
- execution marginal cost
- retry/failure cost
- maintenance/human time
- watcher overhead
- allocated non-sunk fixed cost
- opportunity cost
- dispute/non-payment risk adjustment
> configured positive absolute + ratio margin thresholds
```

Even after that, account creation, credentials, KYC/wallets, task acceptance/fulfilment, publication, spend, settlement or value movement still need separate explicit authorization.

## What I would decide today

1. **No spend yet.** No VPS, paid API, GPU rental, hardware, deposits or stakes.
2. **Run I181 on the owned PC.** This is the cleanest local evidence gain and is already the repository’s next genuine step.
3. **Keep PayanAgent first and OKX.AI A2A second for market evidence.** Neither is proven profitable.
4. **If you want market-side progress, separately authorize a bounded read-only public observation pass.** It should still exclude registration, credentials, task acceptance, fulfillment and value movement.
5. **Do not approve a first paid task until this dashboard can replace the important `UNKNOWN` fields with real measurements and show a positive conservative margin.**

## Files for different views

- **This file:** executive decision view.
- [`CANDIDATE_SCORECARD.csv`](CANDIDATE_SCORECARD.csv): sortable canonical shortlist.
- [`TOP_CANDIDATES.md`](TOP_CANDIDATES.md): deeper candidate cards.
- [`REJECTED_SUMMARY.md`](REJECTED_SUMMARY.md): rejected, parked and de-prioritized paths.
- `CATALOG.md`: full discovery universe.
- `RUN_LOG.md`: discovery audit trail.
- `implementation/`: implementation/economics/safety evidence.

## Dashboard rule

**Synthetic router correctness is not real profitability.** A green label must come from permitted real evidence, never from architecture, historical claims or an attractive headline bounty.
