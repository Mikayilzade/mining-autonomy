# Top Candidates — Decision View

**Updated:** 2026-08-25  
This is a decision-oriented interpretation of the canonical implementation shortlist and later evidence. It does not reopen discovery and does not authorize production actions.

## 1. PayanAgent — primary dry-run/read-only target

### Why it ranked first

Canonical I001 ranked PayanAgent first because it most directly matched the original objective: machine-readable paid work with a programmable request/bid/fulfilment path and very low pre-revenue capital requirements.

### Evidence already obtained

- I001 documented an API-first marketplace with discover/request/bid/fulfil/approve concepts and USDC settlement on Base.
- The first-party surface claimed a large number of offers and exposed receipt/settlement concepts.
- I001 explicitly warned that a large offer count is **supply, not worker demand**.
- I002 designed/rechecked the read-only sampler path but did not establish quantitative public-feed demand from this environment.

### Missing before a profit decision

- current paid bespoke-request density;
- budgets/payouts actually collectible by a worker;
- bid competition and probability of being hired/accepted;
- approval/rejection/dispute/non-payment behavior;
- payment/withdrawal/conversion/gas costs where applicable;
- execution + watcher + maintenance cost.

### Current verdict

**Best first market-side validation target, but unproven.** Current bounded read-only production-observation authorization is false, so no external production probing that depends on that gate should occur yet.

### Next safe action

After separate authorization, run only bounded read-only observation of publicly reachable machine-readable request/receipt/economic surfaces where ToS/API rules permit it. Still no registration, credentials, bidding, task acceptance, fulfillment, wallet/KYC or value movement.

---

## 2. OKX.AI A2A ASP — strong second task-market target

### Why it ranked second

I001 documented an unusually direct workflow: a provider can browse/open tasks, negotiate to take an order, complete work and be paid after approval through escrow. This fits the project better than passive resource markets if real task flow exists.

### Evidence already obtained

- Official workflow supported active task intake and negotiation.
- Escrow/release/arbitration mechanics were documented.
- I003 did **not** establish anonymous live-task observability; the legitimate provider observation path appeared onboarding-gated.

### Main risks/blockers

- current task density and prices remain unmeasured;
- provider onboarding/review is material;
- wallet/geography/KYC eligibility must be confirmed before any account action;
- rejected delivery/arbitration can create downside, so headline bounty is not enough.

### Current verdict

**PRIMARY VALIDATION TARGET, but blocked before real use.** Keep it second; do not register or take orders under current gates.

---

## 3. agent2agent.market — excellent architecture, weak observed demand

### Strength

The documented worker flow was highly machine-native: register, browse task feed, accept, submit a signed deliverable and receive USDC after approval.

### Decisive evidence

At the I001 public snapshot, the app showed **0 open tasks and no live activity on Base Sepolia**. That is a demand warning, not a permanent rejection, and testnet/live-state ambiguity remains.

### Current verdict

**WATCH + ADAPTER TARGET; not first money test.** A future demand change could promote it, but no reason exists to outrank PayanAgent/OKX today.

---

## 4. AgentGigs.io — technically strong, demand + geography gated

### Strength

I001 documented a full autonomous lifecycle through REST API, webhooks/SSE, escrow and Stripe Connect payouts after one-time setup.

### Decisive evidence

The public jobs page snapshot showed **0 total/open jobs**. Even if demand appears later, payout geography and Stripe Connect KYC/bank availability are immediate gates.

### Current verdict

**WATCH / GEO-GATED.** Do not create/verify an account until both demand and payout eligibility justify the effort.

---

## 5. MCPize — passive seller experiment candidate

### Why it differs from task markets

Instead of hunting jobs, the model is to publish a cheap deterministic/MCP capability and wait for paid calls. That could eventually pair well with the Resource Router because deterministic execution can be extremely cheap.

### Evidence already obtained

I001 documented one-command deployment/marketplace listing, subscription or per-call monetization, first-party platform/vendor claims, and a **20% platform fee** for monetized servers under the referenced terms snapshot.

### What is still missing

- buyer demand for a specific capability we can legally provide;
- realistic paid calls/month;
- payout geography/KYC;
- hosting, model/API, maintenance and failure costs;
- conservative break-even and margin using real observations.

### Current verdict

**PASSIVE SELLER EXPERIMENT CANDIDATE / PARKED.** Model it; do not publish or onboard under current gates.

---

## 6. OKX.AI A2MCP — secondary passive target

Marketplace/listing mechanics exist, but buyer volume remains unmeasured and x402/wallet/review dependencies are material.

**Current verdict: SECONDARY PASSIVE TARGET.** Lower priority than the two direct task-market targets and MCPize modeling.

---

## 7. API Mart — low-evidence watchlist

I001 carried API Mart forward with low/unproven discovery evidence. Upstream/resale rights, wallet/geography, demand and actual margin all remain unresolved.

**Current verdict: WATCHLIST / PARKED.** No reason to spend scarce validation effort here while stronger targets remain unresolved.

---

## 8. Compute / inference suppliers — provider reserve, deferred

This is a family rather than a single market. It includes compute/GPU/inference provider opportunities from the larger catalog.

### Why it remains relevant

Provider economics can be programmatic and measurable, and an owned machine may eventually be routed to such work when idle.

### Why it is deferred

Hardware/provider admission, task supply, payout and especially real electricity/opportunity cost are platform-specific. The project still lacks the genuine owned-PC evidence packet.

### Current verdict

**DEFER until task-market tests / real local cost evidence.** The immediate prerequisite is I181 on the actual owned PC.

---

# Portfolio conclusion

There are now **two independent questions**:

1. **Can the available execution backend do the work cheaply/reliably enough?**  
   Answer with I181 → genuine I166 evidence → exact I178/I179 and the Resource Router.

2. **Is there enough real paid demand at a collectible price?**  
   Answer with separately authorized bounded read-only market observation, starting with PayanAgent and then OKX.AI A2A.

Only after both sides have real evidence should the Router decide whether a bounded monetization test has positive conservative expected margin. Until then, router correctness is implementation evidence, not income evidence.
