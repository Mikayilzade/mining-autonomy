# Run 017 — Azerbaijan / KYC / payout / geography filtering

Date: 2026-08-15
Status: **COMPLETED**
Phase: geography/compliance normalization for high-priority autonomous resource markets

## Goal
Filter the strongest server-native / highly autonomous candidates through practical Azerbaijan onboarding, KYC/KYB, settlement and payout constraints. Absence of an explicit country ban is **not** treated as proof of onboarding; unresolved account-opening/payment-provider questions remain marked for empirical validation.

## Executive conclusion
Azerbaijan does **not** eliminate the core crypto-native shortlist. Golem, Akash, Sia, Filecoin and Storj all have protocol/token or wallet-based supplier payment paths that do not depend on PayPal. Current reviewed official documentation did not identify Azerbaijan as an explicitly excluded jurisdiction for these provider roles, although each operator remains responsible for sanctions/export/local-law compliance and local crypto off-ramping/tax treatment remains a separate issue.

Fiat-platform candidates are more nuanced. Vast.ai supports international-host payout infrastructure involving Wise/PayPal/Stripe-type rails, but PayPal's own country documentation says Azerbaijan accounts cannot receive payments. Wise can send transfers to Azerbaijani local bank accounts, and Stripe documentation currently lists Azerbaijan for Connect stablecoin payouts from eligible US platforms, but this does **not** prove Vast exposes every one of those rails to an Azerbaijani host. Vast therefore remains testable but its exact host-payout route must be confirmed during onboarding before hardware deployment.

EarnFM Fleetshare remains attractive but is approval/KYC/KYB gated. Supplier docs require 20+ active IPs, supplier acceptance, Didit identity/business verification and a signed agreement. Standard EarnFM payout remains available after the $15 threshold; traffic over $300/month may request invoice-based SEPA/ACH bank payment. Because Azerbaijan is outside SEPA and ACH, the practical standard payout route must be confirmed in the Supplier Portal before sourcing 20+ IPs.

## Candidate matrix

### 1. Golem Provider — VERIFIED / Azerbaijan practical confidence: HIGH-MEDIUM
- Provider role accepts Linux servers and pays directly in GLM.
- Default production payment rails are Polygon and Ethereum Mainnet.
- Provider can configure the payment wallet address.
- Reviewed provider/payment docs expose no platform KYC step and no country allowlist for running a provider.
- No Azerbaijan-specific exclusion found in the reviewed official provider/payment documentation.
- Main unresolved geography item is not Golem admission but legal/tax treatment and conversion of GLM/POL to locally usable funds.
- **Practical testability from Azerbaijan:** high for a low-cost technical pilot on an already-paid Linux server.
- **Do not assume cash-out:** exchange availability/KYC/off-ramp must be separately verified at implementation time.

### 2. Akash Provider — VERIFIED / Azerbaijan practical confidence: MEDIUM-HIGH
- Provider operation is wallet/on-chain based and current docs describe Akash as permissionless/open.
- Setup requires an Akash wallet, funded balance for bids/gas and provider infrastructure.
- Current provider docs support physical servers or VMs; single-server testing is possible, but audited production-provider requirements can become materially heavier.
- Location is explicitly published as a provider attribute, so geography can affect tenant discovery/demand even when it is not an account-ban mechanism.
- Reviewed current provider docs did not expose an Azerbaijan exclusion or ordinary KYC gate for the base provider protocol.
- **Practical testability:** technically yes; economically less attractive than Golem for a tiny pilot because provider/Kubernetes/network overhead and competitive utilization are higher.
- **Important current update:** Akash documentation now describes lease settlement using ACT compute credits in current provider material; implementation economics must use the then-current settlement model rather than assume old AKT-denominated lease behavior.

### 3. Sia hostd — VERIFIED / Azerbaijan practical confidence: HIGH-MEDIUM
- Host creates/uses its own Sia wallet and is paid through protocol storage contracts.
- No platform-level fiat payout account is needed for the hosting reward path.
- Host must fund Siacoin for collateral and storage proofs; official setup guidance recommends roughly $50 equivalent as a starting point, but actual required collateral varies with stored data.
- Current recommended host hardware is substantial for a storage pilot (official docs currently recommend at least 4 TB HDD plus SSD/system resources), so this is not an ideal rented-VPS arbitrage target.
- No Azerbaijan-specific provider ban was found in the reviewed host setup documentation.
- **Practical testability:** technically feasible where spare owned storage, stable bandwidth and public network access exist; local conversion of SC remains external to Sia.

### 4. Storj Storage Node Operator — VERIFIED / Azerbaijan practical confidence: HIGH-MEDIUM
- Node operators are paid for storage/bandwidth actually used by Storj satellites.
- Payout path is token/wallet based: STORJ via Ethereum L1 by default or optional zkSync L2.
- Operator should control the payout wallet private keys; exchange deposit addresses are discouraged and can break L2 withdrawal flows.
- Terms prohibit one operator from using different payout addresses for different nodes and prohibit more than one node behind the same IP. These rules directly constrain scaling architecture.
- Terms prohibit operation in U.S.-embargoed/sanctioned countries/regions and require compliance with applicable export/local law, but the reviewed terms do not name Azerbaijan as excluded.
- No ordinary supplier KYC flow was found in the reviewed node documentation/terms.
- **Practical testability:** high on spare owned disk/bandwidth; weak on rented cloud storage because current storage rates are thin.

### 5. Filecoin Storage Provider — VERIFIED / Azerbaijan practical confidence: MEDIUM
- Core provider economics are protocol/wallet based and rewards are paid in FIL.
- Minimum 10 TiB storage power is required for WinningPoSt/block-reward eligibility.
- Continuous proving and collateral are mandatory; missed WindowPoSt can cause slashing.
- Filecoin Plus verified-data workflows can add separate client/dataset KYC/due-diligence requirements even though the base storage-provider protocol is not a normal centralized payout account.
- No Azerbaijan-specific base storage-provider exclusion was found in the reviewed current Filecoin docs.
- **Practical testability:** technically possible but **not** a low-capital first experiment. Infrastructure, collateral, proof reliability and deal acquisition make this an operator business rather than a simple VPS daemon.

### 6. Vast.ai Host — VERIFIED / Azerbaijan practical confidence: MEDIUM / payout route unresolved
- Vast hosts can range from individuals to datacenters; hosting requires signing the hosting agreement and operating dedicated compatible GPU infrastructure.
- Current host payout docs say first payout takes about two weeks and reference PayPal, Wise, Stripe and related payment services.
- Current API billing documentation also exposes invoice service identifiers for transfer, Stripe payments, BitPay, Coinbase, Crypto.com, PayPal and Wise, proving the platform has multiple payment integrations; this does **not** prove every host can choose every rail.
- PayPal's own country-of-residence documentation says Azerbaijan Republic accounts do **not** have the ability to receive payments. Therefore PayPal must not be assumed as a usable Vast host payout route for an Azerbaijan-resident operator.
- Wise documentation confirms transfers can be sent to local Azerbaijani bank accounts without the recipient needing a Wise account. Whether Vast's Wise host-payout workflow can target such an Azerbaijani bank recipient still requires onboarding confirmation.
- Stripe documentation currently lists Azerbaijan among countries supported for certain Connect stablecoin payouts from eligible US platforms, but again this does not establish that Vast offers that exact Stripe configuration to hosts.
- Datacenter status requires a registered business, hosting agreement and identity verification; ordinary single-machine hosting verification is largely machine/performance based.
- **Practical testability:** account/onboarding pilot is warranted before any GPU CAPEX. Do not buy/rent hardware assuming payout works.

### 7. EarnFM Fleetshare Supplier — VERIFIED / Azerbaijan practical confidence: MEDIUM / onboarding-gated
- Supplier program is explicitly designed for 20+ IP addresses and can use Fleetshare server or Docker integrations.
- Every supplier application is reviewed.
- Supplier onboarding requires KYC for individuals or KYB for companies through Didit plus online signature of the Supplier Agreement.
- Published traffic rates remain $0.10/GB residential and $0.04/GB datacenter; actual traffic varies by IP geography and IP reputation.
- Standard payout uses the EarnFM payment system with a $15 minimum.
- Supplier traffic above $300/month can request invoice-based bank transfer using SEPA or ACH.
- Azerbaijan is outside SEPA and ACH, so that special bank-transfer route should not be assumed usable through an Azerbaijani bank account. Standard EarnFM payout method availability for an Azerbaijan supplier must be confirmed in the supplier portal.
- **Practical testability:** only after confirming KYC acceptance + payout route; then a small controlled-IP pilot should measure GB/IP/day before scaling.

## Geography effects that matter even without a country ban
1. **Bandwidth/proxy markets:** IP geography directly changes demand and therefore paid GB/IP/day. EarnFM explicitly documents this.
2. **Compute marketplaces:** location influences latency, tenant preference and sometimes search/ranking even if providers are globally allowed. Akash exposes provider location attributes.
3. **Storage networks:** demand is less directly country-gated, but network quality, egress economics, uptime and public reachability dominate.
4. **Fiat payout platforms:** supplier eligibility and payout eligibility are different questions. A marketplace account can exist while a chosen payment processor cannot receive in the operator's country.
5. **Crypto-native rails:** protocol admission can be geography-light while centralized conversion to fiat remains KYC/geography dependent.

## Azerbaijan-specific operational classification

### Best current low-capital experiments later
1. **Golem** — strongest geography fit of the current shortlist because provider payment is directly in GLM and no centralized supplier payout account is required by the reviewed docs.
2. **Storj** — good if spare disk/bandwidth exists; wallet-based STORJ payout and no explicit Azerbaijan exclusion found.
3. **Sia** — similar geography advantage, but higher practical hardware/storage/collateral burden.
4. **EarnFM Fleetshare** — potentially excellent measured economics, but only after supplier KYC + payout route are confirmed.
5. **Vast.ai** — only with existing GPU hardware and only after host payout route is confirmed for Azerbaijan.
6. **Akash** — technically open/testable, but operational overhead makes it a later infrastructure experiment.
7. **Filecoin** — valid business category, not an early low-capital pilot.

## KYC/KYB classification
- **Explicit supplier KYC/KYB:** EarnFM Fleetshare.
- **Explicit identity/business verification for elevated datacenter status:** Vast.ai datacenter program.
- **No ordinary centralized supplier KYC found in reviewed base-provider docs:** Golem, Akash, Sia, Storj, Filecoin protocol provider role.
- **Context-dependent KYC:** Filecoin Plus verified-client/deal programs can require due diligence/KYC; crypto exchanges/off-ramps used to convert earned tokens may impose separate KYC.

## Payout classification
- **Direct protocol token:** Golem (GLM), Sia (SC), Filecoin (FIL), Storj (STORJ), Akash current provider settlement via network compute-credit/token mechanism as documented at implementation time.
- **Centralized multi-rail payout:** Vast.ai.
- **Centralized supplier payout + conditional invoice bank transfer:** EarnFM Fleetshare.

## Unknowns deliberately left unresolved
- Exact exchange/off-ramp and tax treatment for GLM, STORJ, SC, FIL and Akash settlement assets in Azerbaijan.
- Whether Vast currently exposes Wise transfer, Stripe stablecoin or another workable host payout method to an Azerbaijan-resident host during live onboarding.
- Whether EarnFM/Didit supplier onboarding accepts an Azerbaijan individual/business in practice and which standard cash-out methods appear after verification.
- Demand/utilization by Azerbaijan/datacenter IP geography for EarnFM and compute marketplaces.
- Azerbaijan-specific licensing/tax treatment for running commercial infrastructure services from home versus a rented datacenter.

These should be tested during implementation planning; they do not block the current theoretical universe/saturation phase.

## Run result
Run 017 completed its intended geography/KYC/payout filtering for the representative highest-priority autonomous resource shortlist. No candidate was upgraded to guaranteed-profit status. Golem, Storj and Sia remain especially clean from a platform-payout-geography perspective because their reward paths are wallet/protocol based. Vast and EarnFM require explicit Azerbaijan onboarding/payout confirmation before deployment.

## Next run
Begin **Run 018 — broad saturation/control pass #1** using deliberately different vocabulary from prior discovery: machine economy, idle-resource monetization, node operator income, supplier network, capacity marketplace, work marketplace, daemon earnings, distributed infrastructure rewards, host/provider/reseller programs, partner/supplier portals and decentralized service markets. Track new unique mechanisms and viable projects per query family; do not count renamed duplicates.