# Run 041 — Third supplier-tail convergence + authenticity/dedup pass

Date: 2026-08-16
State: COMPLETE
Project state after run: IN PROGRESS

## Purpose
Continue from Run 040 and test whether supplier-tail discovery has converged. Prioritize inference/API-capacity seller markets, compute exchanges, authenticity, current seller economics, and one more non-GPU analog pass.

## Result
Taxonomy remains saturated: **0 new top-level economic mechanisms**.

Project-level supplier saturation is **not complete**. This pass found multiple current independent implementations of already-known mechanisms that were absent from the Run-040 durable checkpoint. Most importantly, the API-capacity-resale tail is materially broader than previously recorded.

## New independent implementations

### 1. Proxygate — VERIFIED / RESTRICTED
Category: API-capacity resale / own-endpoint marketplace / agentic machine-commerce clearing layer.

Current first-party evidence:
- Seller may list authorized upstream API capacity or an endpoint the seller owns and operates.
- Seller sets per-request pricing and capacity fences.
- Seller receives 95% of listing price; platform seller fee is 5%. Buyer also pays 5%.
- Seller earnings settle in USDC on Solana, described as batched roughly every 10 minutes / near-real-time.
- Seller application and moderation are required before listings go live.
- Upstream resale authorization is explicitly the seller's responsibility. Current Certified Reseller Program is planned, not yet a blanket authorization mechanism.
- Own-endpoint listings avoid the upstream-resale issue but require ownership/control of the endpoint.

Autonomy: 5 for an approved own endpoint or authorized API capacity after onboarding; marketplace routing, metering and settlement are automated.

Capital/cost: no public large bond currently; operating cost is underlying API subscription/capacity or endpoint compute plus transaction/operational cost.

Key risk: many retail API terms prohibit credential sharing/resale or require specific reseller agreements. Therefore platform availability does **not** itself make an upstream key lawful to resell.

Azerbaijan/geography: unresolved. Solana payout reduces bank-rail dependency, but seller onboarding/legal eligibility still needs explicit validation.

Economics formula:
`Net = 0.95 * sold_listing_revenue - upstream_API_cost - endpoint_compute - Solana/withdrawal costs - maintenance - expected account/enforcement loss`

Sources:
- https://proxygate.ai/tos
- https://gateway.proxygate.ai/docs
- https://proxygate.ai/whitepaper
- https://proxygate.ai/

### 2. JellyNet — VERIFIED / RESTRICTED
Category: pooled API-capacity sharing / machine-call marketplace.

Current first-party evidence:
- Suppliers contribute idle API capacity and receive revenue from successful calls routed through their keys.
- Terms explicitly warn that upstream providers may suspend/revoke accounts and place responsibility for upstream compliance on the supplier.
- Current supplier split in Terms: native-call mode 60% supplier / 30% buyer discount / 10% platform fee; API-key-only default 50% supplier / 20% buyer discount / 10% platform fee. Public marketing simplifies this as a 10% platform cut, so Terms must control economic modeling.
- Revenue is accounted in 8-hour epochs.
- Withdrawal rails include USDC on Solana and fiat via Stripe Connect where available.
- Soft cap stated as 5 keys per protocol per account.

Autonomy: 5 after setup; calls, routing, accounting and settlement are automated.

Capital/cost: underlying API plans/credits are the major cost; no material public supplier bond found in this pass.

Geography/KYC: account data and Stripe availability imply geography can matter. Azerbaijan eligibility is unresolved.

Critical restriction: only capacity the supplier has a legal/contractual right to share should be used. The Terms explicitly acknowledge upstream account-action risk; therefore do not deploy with ordinary consumer/API plans until each upstream contract is checked.

Economics formula:
`Net = supplier_share * successful_paid_call_revenue - upstream_API_cost - subscription_sunk/avoidable_cost - payout_cost - expected enforcement/account loss`

Sources:
- https://www.jellynet.net/legal/terms
- https://www.jellynet.net/legal/privacy
- https://www.jellynet.net/

### 3. cn2.ai — VERIFIED / RESTRICTED
Category: API-key marketplace / machine-payments routing.

Current first-party evidence:
- Sellers list spare API capacity and buyers call proxy endpoints.
- Platform positions itself as routing/payment/discovery intermediary rather than party to upstream provider agreements.
- Seller information includes KYC verification status via Persona and payout preferences including wallet/bank rails.
- Public seller page advertises USDC, Stripe, Lightning or wire payouts.
- Platform uses MPP/x402-style per-request machine payments.

Autonomy: 5 in principle after seller onboarding and key configuration.

Current weakness: exact seller fee/split and detailed payout thresholds were not confirmed from the first-party pages retrieved in this run. Treat economics as incomplete until seller docs are captured.

Upstream ToS: seller remains responsible; authorized resale is a hard deployment gate.

Geography/Azerbaijan: unresolved.

Sources:
- https://www.cn2.ai/
- https://www.cn2.ai/docs
- https://www.cn2.ai/terms
- https://www.cn2.ai/privacy

### 4. CreditSwap — WATCHLIST / RESTRICTED (private beta)
Category: server-agent mediated API-credit/capacity exchange.

Current first-party evidence:
- Private beta / waitlist.
- Seller-side open-source agent is described as running on the seller's own server and executing marketplace jobs while the key stays local.
- Public economics claims: seller recovery 85% of retail; platform fee shown as 5%; buyer discount 10%.
- Supports at least OpenAI/Anthropic in public beta messaging and claims six providers to swap across.

Autonomy: potentially 5 if production beta operates as described.

Restriction: private beta and upstream rights are unresolved. Do not model as deployable production income yet.

Source:
- https://www.creditswap.app/

### 5. GEPU Exchange — UNVERIFIED / WATCHLIST
Category: GPU-hour spot exchange / idle datacenter capacity market.

First-party site claims:
- Six GPU markets, live order books and USDC T+0 settlement.
- Providers attest capacity, list GPU-hours and receive payment when fills settle.
- Auto-listing of idle sleds is explicitly presented.
- Provider flow is server/datacenter native and potentially highly autonomous.

However, the same page labels its displayed flow/network numbers as **devnet**. Public search in this pass did not surface strong independent/legal-company evidence or mature provider terms. Therefore this is **not** yet promoted to a production candidate despite the attractive mechanics.

Autonomy: potentially 5.

Economics: unknown actual production fill rate, fees, staking/collateral and legal geography.

Source:
- https://gepu.ai/

## Existing Run-040 candidate validation updates

### Inpherio
Still `VERIFIED / BETA`.
- First-party site states beta is functional today, with provider self-service, token-metered billing, node rentals, Stripe card top-ups and monthly bank payouts.
- Provider machines use outbound-only connectors.
- Stripe Connect supports payouts in many countries globally, but generic Stripe support is not sufficient proof that Inpherio can onboard an Azerbaijan connected account. Keep geography unresolved.

Sources:
- https://inpherio.co.uk/
- https://stripe.com/connect/marketplaces

### UsePod
Still `VERIFIED / RESTRICTED`.
- Confirmed 80/20 marketplace split.
- $50 USDC provider bond.
- On-demand USDC withdrawal, subject to a minimum and daily cap; large withdrawals may require manual approval.
- Open provider-agent and key-relay supply sides are current.
- Exact minimum/daily cap values and geography were not exposed in retrieved text.

Sources:
- https://docs.usepod.ai/providers/earnings-and-cashout/
- https://docs.usepod.ai/
- https://docs.usepod.ai/marketplace/trust/

### KeyMart
Still `VERIFIED / RESTRICTED`.
- Current public site claims 12 verified providers and a live order book.
- Provider requirements are enterprise/qualified: identity, API provenance, upstream ToS, SLA, capacity and uptime.
- Provider fee tiers reconfirmed: 0% first 7 days; 2.8% standard; 1.6% pro; 0.5% enterprise.
- Onboarding is invitation/compliance-review based, so it is not a simple open spare-key path.

Sources:
- https://keymart.ai/
- https://keymart.ai/providers/

### Compute Exchange / TCEX
Authenticity improved; keep `VERIFIED / RESTRICTED`.
- Current marketplace Terms identify The Compute Exchange Inc., a Delaware corporation.
- Provider is a legal entity offering Compute through the service.
- Current provider workflow is institutional: TCEX partner network, qualified RFQs, provider quote response, direct introduction and contracting.
- It supports monetizing unused compute, but this is not a hands-off retail server bot in the current commercial workflow.

Sources:
- https://compute.exchange/marketplace-terms
- https://compute.exchange/providers
- https://compute.exchange/about

### Exascale / Hyperlink
Remain `UNVERIFIED / WATCHLIST`.
- First-party page continues to make highly specific production claims: 34,120 GPUs, regional order books, T+0 settlement, per-second payout, central-counterparty workflow.
- This pass still did not establish sufficiently strong independent/legal/company evidence to trust those claims for deployment modeling.

Source:
- https://www.hyperlink.org/

## Non-GPU analog rerun
The broad CPU/storage/bandwidth search mostly returned known mechanisms and previously represented families.

Notable current storage confirmation:
- EthStorage mainnet has a storage-provider/mining path, but earning as a miner is currently limited by whitelist status during initial mainnet rollout. This is not a new mechanism; retain as restricted implementation if not already catalogued.
- Filecoin continues to expose a provider path, including PDP warm storage positioned as lower-complexity onboarding. Again, not a new mechanism.

No new top-level CPU/storage/bandwidth mechanism emerged.

Sources:
- https://docs.ethstorage.io/storage-provider-guide
- https://www.filecoin.io/provide-storage

## Deduplication conclusions
- Proxygate, JellyNet, cn2.ai, CreditSwap, UsePod and KeyMart all belong under the already-known **API/inference capacity resale or endpoint-service market** family. They are independent implementations, not new economic mechanisms.
- GEPU belongs under the already-known **compute exchange / GPU-hour marketplace** family.
- Compute Exchange/TCEX is an institutional broker/RFQ implementation of compute-capacity selling, not a new mechanism.
- No taxonomy expansion occurred.

## Durable lesson added by Run 041
The biggest unsaturated tail is no longer generic GPU rental; it is **machine-native API/endpoint capacity markets** using x402/MPP/USDC-style settlement. This family can look fully autonomous technically while remaining commercially unusable unless the upstream API contract expressly permits resale/sublicensing/capacity sharing.

For future deployment ranking, split this family into:
1. own endpoint / own model service — generally cleaner rights position;
2. explicit enterprise/reseller-authorized upstream capacity — viable after contract validation;
3. ordinary retail API-key resale — default `RESTRICTED` until the upstream contract says yes.

## Completion decision
Do **not** mark project COMPLETE.

Run 041 produced several new independent current projects, so the completion gate requiring negligible project-level novelty has not been met.

## Next run
Run 042 should **not** be the final broad control pass yet. First perform a dedicated **API-capacity / x402 / MPP / own-endpoint supplier saturation pass** because Run 041 revealed a materially productive cluster.

Search targets:
- `x402 API marketplace seller`
- `MPP API marketplace seller`
- `sell API capacity x402`
- `monetize API key capacity`
- `agent marketplace own endpoint seller USDC`
- `machine payments API seller`
- `API clearinghouse provider`
- `unused API quota marketplace`
- `sell endpoint per request`
- `agent service marketplace x402`

Also verify Proxygate/cn2/JellyNet legal identity, seller geography/Azerbaijan eligibility, exact withdrawal constraints and live activity. Promote only when primary-source evidence supports production status.
