# Top Candidates — Decision View

**Updated:** 2026-08-25  
This is a decision-oriented interpretation of the existing research and implementation evidence. It does not reopen discovery and does not authorize production actions.

## 1. PayanAgent — first market-side validation target

### Why it is first

I001 ranked PayanAgent `SELECT` because it was the closest match to the project’s preferred mechanism: a server-native machine-to-machine task/agent surface that could potentially be watched and fulfilled programmatically. The next useful validation was designed to be read-only rather than account creation or paid commitment.

### What is actually known

- Discovery found a documented machine-readable surface and accountless/free-path claims.
- It was considered a high autonomous-fit candidate.
- A bounded read-only production validation was selected as the next market-side evidence step.

### What is **not** known

- Real current task/request volume usable by this project.
- Real payout/settlement/yield at the task level.
- Acceptance probability and rejection/dispute/non-payment behavior.
- Full platform/payment/withdrawal/conversion costs.
- Real end-to-end conservative margin after execution and watcher overhead.

### Current verdict

**Best market-side candidate, but unproven and blocked on evidence.** Current authorization for bounded read-only production observation is false. Do not register, use credentials, accept tasks or move value under this status.

### Next safe decision

If the user wants market-side progress, separately authorize a **bounded read-only public production observation** that still excludes registration, credentials/API keys, identity creation with side effects, task acceptance/fulfillment, wallet/KYC and payment/settlement actions.

---

## 2. Owned-PC provider economics — prerequisite across several paths

This is not one marketplace; it is the execution-cost prerequisite shared by compute/provider candidates such as io.net/Salad-style work and potentially by task-market execution itself.

### Why it matters

Without measured owned-PC energy, availability and opportunity cost, the Router cannot honestly say whether a small payout is profitable. Treating owned hardware as “free” would be a false margin signal even though the purchase itself is sunk.

### What is already implemented

The Resource / Execution Router distinguishes fixed/sunk cost from marginal task cost and rejects production routes that fail conservative post-fixed margin thresholds. The accounting architecture therefore exists; the missing part is genuine input evidence.

### Current blocker

I181 has not run on the actual owned PC, so built-in cumulative energy-counter availability is unknown. No genuine I166 evidence packet exists yet.

### Next safe decision

**Run I181 locally with no spend.** If a valid built-in cumulative counter exists, collect genuine observations. If it does not, use I182 only with an already-owned/available trustworthy whole-system cumulative external meter. Do not estimate energy and do not buy hardware under the current gate.

---

## 3. Rider RepLayer — high-fit reserve candidate

### Why it stayed high

I001 ranked it second because the machine-readable Repls/task concept fit the desired server-native autonomous model.

### What blocks promotion

A public production task/offer surface and current real economics were not confirmed sufficiently to promote it ahead of PayanAgent.

### Current verdict

**WATCHLIST / PARKED.** Preserve as a reserve candidate, but do not spend another broad discovery cycle on it while the first target and the execution-cost evidence are unresolved.

---

## 4. io.net / compute-provider class — economically measurable, hardware-sensitive

### Why it matters

Compute-provider paths are attractive because work and resource consumption can in principle be measured programmatically. They can also fit an owned machine better than human-task platforms.

### Why it is not first

Provider eligibility, supported hardware/geography/terms, work supply, payout path and the project’s real electricity/opportunity cost are all material. A nominal provider payout without those inputs does not establish profit.

### Current verdict

**WATCHLIST / PARKED until local cost evidence exists.** I181 is a prerequisite to a serious economic decision here.

---

## 5. Salad provider class — consumer-resource reserve

### Strength

Discovery confirmed the broader Salad consumer CPU/GPU/internet reward model, so this is a real provider-style mechanism rather than a purely speculative category.

### Weakness

The exact provider/server applicability, current work supply, payout and unit economics for this project remain unresolved. It is less aligned with the preferred server-native machine-task route than PayanAgent.

### Current verdict

**WATCHLIST / PARKED.** Revisit after owned-PC cost evidence is real or if higher-priority server-native task candidates fail.

---

## 6. Storj — established but lower-priority spare-resource path

### Strength

Storage/bandwidth provider mechanics are conceptually straightforward and can run for long periods with limited interaction.

### Weakness

Capacity utilization, payout, egress/bandwidth costs, maintenance and time-to-meaningful-revenue all matter. It is less aligned with the project’s first-priority paid machine-task market.

### Current verdict

**WATCHLIST / secondary provider path.** Useful as diversification later, not as the next experiment while the primary evidence gates are open.

---

## 7. Grass — eligibility-sensitive device/bandwidth path

The mechanism fits passive contribution better than machine-task execution, but geography/account/device policy and payout quality are material. It should not be automated on assumptions about server/VPS/device eligibility.

**Current verdict: WATCHLIST / PARKED.** Require explicit current rules and economics before any automation.

---

## 8. Skyfire and BTCPay/MCP — infrastructure before income

Skyfire is interesting for machine payments, but its onboarding/account/payment dependencies make it a poor first zero-spend validation target. BTCPay/payment-gated MCP is even clearer: it can help collect payment for a service, but it does not create paid demand by itself.

**Current verdict:** Skyfire = `WATCHLIST`; BTCPay/payment-gated MCP = `COMPONENT`, not standalone income.

---

# Portfolio conclusion

The project currently has **two different questions**, and they should not be mixed:

1. **Can the machine execute cheaply enough?** → answer with I181 → genuine I166 → I178/I179.
2. **Is there enough real paid demand at a collectible price?** → answer with separately authorized bounded read-only market observation, starting with the I001-selected PayanAgent target.

Only after both answers are supported by real evidence should the Router be used to decide whether a bounded monetization test is economically justified. Until then, a sophisticated routing stack is evidence of implementation quality, not evidence of profit.
