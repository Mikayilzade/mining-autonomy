# Mining Autonomy — Decision Dashboard

**Updated:** 2026-08-25  
**Purpose:** turn the completed discovery work and the current implementation state into a decision surface. This file is a summary for decisions, not a new discovery pass and not production authorization.

## 30-second answer

- **There is no proven real profit yet.** No measured non-synthetic production route currently survives conservative economics plus watcher overhead.
- **Discovery is complete (Runs 001–062).** The catalog covered server compute/GPU/AI, storage, bandwidth/relay, nodes, proof markets, task/agent markets, device/home paths, capital yield, build-once products and common low-quality/prohibited paths.
- **The best server-native validation target from the implementation shortlist remains PayanAgent.** It was ranked `SELECT` in I001 because it best matched the machine-to-machine task/agent objective and appeared testable through bounded read-only observation.
- **The execution side is also not yet measured.** The owned-PC energy/availability/opportunity-cost packet is missing; I181 must run on the actual owned PC before exact local economics can be trusted.
- **Resource / Execution Router is implemented and hardened.** It separates sunk/fixed from marginal cost, prefers deterministic execution, escalates to AI only when needed, and requires positive conservative post-fixed margin before production routing.
- **The bottleneck is evidence, not more repository-only architecture.** Real task payout/acceptance/retry/fee/non-payment data and real execution-cost evidence are still unknown.

## Decision state now

| Decision | Status | Recommendation | Why |
|---|---|---|---|
| Keep doing broad discovery | **NO** | Do not reopen it | Discovery is already complete; current gap is real evidence. |
| Run I181 on the owned PC | **GO — local/no spend** | **Do next** | Needed to establish whether a trustworthy built-in cumulative energy counter exists. |
| Buy a power meter | **NO** | Do not buy | Not authorized; I182 is allowed only with an already-available trustworthy whole-system meter. |
| Authorize bounded read-only production observation | **USER DECISION** | Useful once you want market-side evidence | Current authorization is `false`; this can gather public production/economic evidence without credentials or value movement if the target permits it. |
| Pay for API / VPS / GPU / account | **NO** | Do not spend yet | No real positive margin has been demonstrated. |
| Accept/fulfil a paid task or move value | **NO** | Not yet | Requires a separate explicit authorization after real economics clear the gate. |

## Evidence funnel

```text
Broad opportunity universe
        ↓
Discovery Runs 001–062 COMPLETE
        ↓
I001 implementation shortlist: 8 candidates/components
        ↓
#1 PayanAgent selected for next server-native validation
        ↓
Resource / Execution Router built + safety/economics hardened through I196
        ↓
Real execution-cost evidence: MISSING
Real market payout/acceptance evidence: MISSING
Read-only production observation authorization: FALSE
        ↓
Real conservative positive route: NONE YET
        ↓
Bounded monetization test: NOT AUTHORIZED / NOT READY
```

## Evidence labels used here

| Label | Meaning |
|---|---|
| `PROVEN_REAL` | Non-synthetic, measured evidence from a permitted real environment. |
| `PUBLIC_SPEC` | Public documentation/surface supports the mechanism, but does not prove our unit economics. |
| `SYNTHETIC_VALIDATED` | Code/fixtures prove router or accounting behavior, not income. |
| `UNKNOWN` | Required real economic input has not been observed. |
| `BLOCKED` | A required measurement or authorization is absent. |
| `PARKED` | Worth retaining, but not the next priority under the current roadmap. |

## Candidate board

This preserves the I001 shortlist decisions. It does **not** pretend that an old discovery rank is a present profitability proof.

| Rank | Candidate | Market / earning mechanism | Original I001 decision | Current decision state | Main missing evidence | What to do now |
|---:|---|---|---|---|---|---|
| 1 | **PayanAgent** | Server-native machine task/agent market | **SELECT** | **BLOCKED on real market evidence** | Public production demand, payout/settlement/yield, acceptance and full task economics; read-only observation authorization is currently false | Keep as first market-side validation target; request explicit bounded read-only authorization before external observation |
| 2 | **Rider RepLayer** | Machine-readable agent/task concept | WATCHLIST | **PARKED** | Confirmed public production task/offer surface and current economics | Do not outrank PayanAgent without new evidence |
| 3 | **Skyfire** | Machine payment/request infrastructure | WATCHLIST | **PARKED / onboarding-heavy** | Account/credential/payment onboarding plus current supply/yield | Avoid paid/credential path until economics justify it |
| 4 | **io.net** | Compute/GPU provider | WATCHLIST | **PARKED; local cost evidence also missing** | Current provider eligibility, owned-hardware fit, energy/cost and payout path | First measure owned-PC economics via I181/I166 chain |
| 5 | **SaladCloud / Salad provider class** | Consumer CPU/GPU/container work | WATCHLIST | **PARKED** | Provider availability, work supply, payout and exact unit economics | Revisit only after local cost model exists or PayanAgent is exhausted |
| 6 | **Storj** | Storage/bandwidth provider | WATCHLIST | **PARKED** | Eligibility/capacity/payout plus storage/bandwidth costs | Secondary provider path, not current server-native task priority |
| 7 | **Grass** | Bandwidth/data contribution | WATCHLIST | **PARKED / eligibility-sensitive** | Geography/account/device eligibility and current payout quality | Do not automate until rules and economics are explicit |
| 8 | **BTCPay / payment-gated MCP** | Payment infrastructure | COMPONENT | **NOT standalone income** | Upstream paid demand | Use only as a future component if another service already has demand |

Machine-readable version: [`CANDIDATE_SCORECARD.csv`](CANDIDATE_SCORECARD.csv).

## What the larger discovery actually covered

The catalog is much broader than the eight implementation shortlist entries. Major families include:

- server CPU/compute markets such as Golem/Akash-style provider paths;
- GPU/AI compute markets such as Vast/Nosana/Golem GPU/io.net/Salad-style paths;
- AI incentive networks, transcoding, decentralized storage and bandwidth/relay nodes;
- blockchain service nodes, indexing/RPC/relay, ZK/prover markets and keeper/solver infrastructure;
- legitimate automated jobs and machine-to-machine task markets;
- home/device bandwidth, GPU/CPU and storage sharing;
- physical DePIN/device contribution;
- capital-based yield and automated trading families;
- build-once APIs, micro-SaaS, digital products, licensing and asset rental;
- low-quality or usually unsuitable families such as ad/click/faucet automation, human microtasks and opaque “cloud mining” schemes.

For the audit trail and all individual leads, use `CATALOG.md` and `RUN_LOG.md`; this dashboard intentionally compresses them.

## Resource / Execution Router — practical view

| Backend | Cost treatment | Current usability | Current decision |
|---|---|---|---|
| **Pure Python / deterministic local code** | Marginal CPU/energy/time + opportunity cost; fixed/sunk separated | Available for offline/dry-run work | **First choice whenever it can meet acceptance criteria** |
| **Owned PC CPU/GPU/local model** | Real electricity + retry/failure + maintenance + opportunity cost; hardware already owned is not charged as a new purchase per task | Technically possible, but exact economics blocked | **Measure first via I181 → genuine I166 → I178/I179** |
| **Existing ChatGPT/Codex subscription** | Fixed/sunk/limited resource; not zero-cost and not allocated as full monthly fee per task | Human-triggered capability only; no assumed programmable unlimited API | **Useful for project work, not assumed autonomous execution backend** |
| **Free / conditional-free CI or cloud tier** | Quota/capacity/reliability are constraints; marginal price may be zero within allowance but opportunity/quota cost is not | Safe for permitted dry-run/testing | **Use selectively; do not treat quota as infinite** |
| **Cheap external LLM/API** | Per-call/token + retry + failure + credential/payment cost | Blocked by current no-spend/no-credentials gate | **Do not activate yet** |
| **Stronger / expensive external API** | Higher per-call cost; only justified by quality/acceptance uplift | Blocked | **Escalate only if cheaper backend cannot clear acceptance + margin** |
| **Future VPS/server** | Rent + bandwidth + energy-in-price + maintenance + opportunity cost | Not authorized | **Do not rent before real positive economics** |

Routing principle: **cheap deterministic filter → local/deterministic execution where sufficient → AI only when necessary → cheapest backend that clears acceptance probability and conservative positive post-fixed margin.**

## Two independent evidence tracks still missing

### Track A — execution cost

1. Run **I181 on the actual owned PC**.
2. If a validated built-in cumulative energy counter exists, collect genuine measurements.
3. If it does not exist, use hardened **I182 only if a trustworthy whole-system cumulative external meter is already available**.
4. Add genuine applicable electricity tariff, actual availability window, opportunity-cost basis, ownership confirmation and explicit UTC `observed_at`.
5. Run exact **I178/I179** accounting/routing checks.
6. If neither measurement route exists, keep energy `BLOCKED`; do not estimate it.

### Track B — market revenue

For the first server-native target, real values are still needed for:

- observable task/request volume;
- payout/reward/settlement basis;
- acceptance probability;
- retry/failure frequency and cost;
- marketplace/payment fees;
- withdrawal/gas/conversion if applicable;
- dispute/non-payment probability;
- watcher/polling overhead;
- maintenance/human time.

Current authorization for bounded read-only production observation is **false**. No external probing requiring that gate should occur until explicitly authorized.

## GO rule for a first monetization test

A real bounded monetization experiment is proposed only after **both** tracks have evidence and the Router shows, conservatively:

```text
expected collectible revenue
- platform/payment/withdrawal/conversion costs
- execution marginal cost
- retries/failures
- maintenance/human time
- watcher overhead
- allocated non-sunk fixed cost
- opportunity cost
- dispute/non-payment risk adjustment
> configured positive absolute + ratio margin thresholds
```

Even then, the test itself still needs separate explicit user authorization if it accepts work, spends money, uses credentials, creates an account, touches KYC/wallets, publishes externally or moves value.

## What I would decide today

1. **Do not spend money.** No VPS, API subscription, GPU rental, hardware or deposits yet.
2. **Finish the owned-PC measurement gate (I181).** This is the cleanest no-spend evidence gain.
3. **Keep PayanAgent as the first market-side candidate.** It remains the implementation shortlist winner, but treat it as unproven until real permitted production/economic evidence exists.
4. **When ready, explicitly authorize only a bounded read-only public observation pass** if you want the project to gather market-side evidence. That authorization should still exclude registration, credentials, task acceptance, fulfillment and value movement.
5. **Do not approve a real paid task test until the dashboard can show actual conservative margin with real inputs instead of `UNKNOWN`.**

## Files for different views

- **This file:** executive decision view.
- [`CANDIDATE_SCORECARD.csv`](CANDIDATE_SCORECARD.csv): sortable candidate table.
- [`TOP_CANDIDATES.md`](TOP_CANDIDATES.md): deeper explanation of the strongest/most decision-relevant paths.
- [`REJECTED_SUMMARY.md`](REJECTED_SUMMARY.md): what is rejected, parked, or deliberately de-prioritized and why.
- `CATALOG.md`: full discovery universe.
- `RUN_LOG.md`: discovery audit trail.
- `implementation/`: implementation/economics/safety evidence.

## Dashboard rule

A green label here must never be inferred from architecture alone. **Synthetic router correctness is not real profitability.** Unknown inputs stay unknown until measured or observed under the project’s authorization and compliance gates.
