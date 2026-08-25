# Rejected / Parked Summary — Decision View

**Updated:** 2026-08-25  
This is a compact decision layer over the full `CATALOG.md` / `RUN_LOG.md`. It is **not** an exhaustive replacement for those audit files.

## Important distinction

- **REJECTED** = unsuitable, prohibited, non-paying, or structurally incompatible with the objective under known rules.
- **PARKED / WATCHLIST / DEFERRED** = not disproven; simply not worth the next validation slot while stronger candidates or required evidence remain unresolved.
- **BLOCKED** = potentially useful, but a measurement/authorization/eligibility dependency prevents a real decision.

Do not read “not top candidate” as “scam” or “never profitable”.

## Current shortlist: why candidates are not being advanced now

| Candidate | Current treatment | Why it is not moving to money test |
|---|---|---|
| **PayanAgent** | **BLOCKED, not rejected** | Primary target, but real paid request flow and full economics remain unproven; current bounded read-only production-observation authorization is false. |
| **OKX.AI A2A ASP** | **BLOCKED, not rejected** | Strong official task workflow, but anonymous live task density was not established and legitimate provider observation/onboarding introduces wallet/geography/KYC/review gates. |
| **agent2agent.market** | **WATCHLIST** | Excellent machine-native flow, but I001 public snapshot showed 0 open tasks/no activity on Base Sepolia; production-vs-testnet demand remains unclear. |
| **AgentGigs.io** | **WATCH / GEO-GATED** | Full automation interface exists, but I001 public jobs snapshot showed 0 total/open jobs and Stripe Connect payout geography/KYC is material. |
| **MCPize** | **PARKED passive seller experiment** | Monetization model exists, but paid buyer demand for our capability and complete hosting/API/payout economics are not yet measured; publication/onboarding is not authorized. |
| **OKX.AI A2MCP** | **PARKED secondary passive target** | Buyer volume is unmeasured and wallet/x402/review dependencies are material. |
| **API Mart** | **WATCHLIST / low evidence** | Demand, resale/upstream rights, wallet/geography and margin remain insufficiently proven. |
| **Compute/inference suppliers** | **DEFERRED** | Platform-specific hardware/admission/work-supply economics plus real owned-PC energy/opportunity cost are unresolved; I181 comes first. |

## Broad families deliberately de-prioritized

### Capital-based yield / trading

The catalog includes deposits/bonds, securities, P2P/private credit, staking/lending/liquidity provision and automated trading/arbitrage families. These are not the current priority because the project’s primary objective is low/zero-capital autonomous machine earning. They also introduce capital-at-risk, custody, market, smart-contract, liquidation or counterparty risk.

**Treatment:** `SECONDARY / PARKED`, not automatically rejected.

### Physical DePIN / sensor / vehicle/location paths

These can be legitimate but often require hardware purchase, location, mobility or specialized devices.

**Treatment:** `SECONDARY / PARKED` under the current no-purchase gate.

### Build-once digital products / micro-SaaS / APIs

These may have better long-run economics than “mining”, but they require product creation and demand acquisition rather than simply attaching a worker to an existing machine-paid task stream.

**Treatment:** `VALID ALTERNATE MODEL`, but lower priority than the current server-native task-market experiment. MCPize is the bridge candidate inside this family.

## Families commonly rejected or strongly restricted

### Human microtask automation

Surveys, CAPTCHA solving, ad clicking, Mechanical-Turk-like human tasks, app-install chores and similar platforms are not assumed automatable. If a platform contracts for human work, botting it is out of scope unless it explicitly exposes a machine/provider API that permits automation.

**Treatment:** `REJECT by default for automation`.

### Faucets / ad-watching / click-to-earn

Usually very low-value, anti-bot/human-presence based, and automation often violates platform rules.

**Treatment:** `REJECT unless an explicit legitimate machine API changes the mechanism`.

### Non-paying volunteer compute

BOINC/Folding@home/Tor relay style participation can be technically interesting but normally does not directly pay.

**Treatment:** `REJECT as direct income source`; keep only as technical analogues unless a separate legitimate reward mechanism is verified.

### Opaque “cloud mining” investment schemes

Fixed-return/opaque cloud-mining offers have high scam and counterparty-risk exposure; genuine hardware contracts must be separated from Ponzi-like products.

**Treatment:** `HIGH-RISK / generally reject without unusually strong evidence`.

### Airdrop/testnet multi-account farming

Legitimate one-account participation may exist, but Sybil/multi-account evasion is outside project rules and rewards are not dependable recurring income.

**Treatment:** `REJECT prohibited multi-account/Sybil methods`; legitimate participation remains speculative, not core income.

### Residential bandwidth on prohibited server environments

Example from the catalog: EarnApp was marked `RESTRICTED` because official support prohibited VMs/Docker/hosting/cloud/server monetization for the relevant use case. Similar programs must never be assumed VPS-compatible.

**Treatment:** `RESTRICT/REJECT server automation when ToS forbids it`.

## Hard safety exclusions across every category

The project does not pursue:

- CAPTCHA/rate-limit/KYC/geofence/product-limit bypass;
- spam, fake traffic, fake activity or ad fraud;
- credential abuse;
- prohibited multi-accounting/Sybil farming;
- automation of human-only work against ToS;
- unauthorized data access;
- spend, deposits, stakes, paid infrastructure or hardware purchase without separate approval;
- real credentials/accounts/wallet/KYC/task acceptance/fulfilment/settlement/value movement without the required explicit gate.

## Why this matters for decisions

A long opportunity catalog can create the illusion that dozens of “options” are equally actionable. They are not. The current evidence compresses the universe into four buckets:

1. **Primary market evidence targets:** PayanAgent, then OKX.AI A2A.
2. **Demand/eligibility watchlist:** agent2agent.market, AgentGigs, API Mart.
3. **Passive seller / alternate monetization:** MCPize, then OKX.AI A2MCP.
4. **Provider/resource reserve:** compute/inference and other passive provider families, pending real owned-PC economics.

Everything else should stay out of the immediate execution queue unless new evidence creates a genuinely better path.
