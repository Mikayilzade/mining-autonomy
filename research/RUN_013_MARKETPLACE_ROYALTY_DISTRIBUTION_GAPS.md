# Run 013 — Marketplace / royalty / digital-distribution gaps

Date: 2026-08-15
Status: **completed**
Stage: cloud marketplaces, data/MCP marketplaces, digital-asset royalties, creator revenue rails

## Objective
Close major gaps left after the build-once and machine-market runs: identify additional marketplaces that directly pay software/data/asset creators, distinguish true marketplace revenue from mere distribution, and record Azerbaijan eligibility where current primary sources expose it.

## Strongly validated opportunities

### 1. Microsoft Marketplace — transactable SaaS / metered software
Status: **VERIFIED**
Class: BUILD-ONCE / server-native service distribution
Automation: 5 after product is deployed, with monitoring/support

Current Microsoft documentation confirms an agency marketplace model: publishers set prices, Microsoft bills/collects, and publishers receive net revenue after a standard 3% store service fee for transactable offers. Usage-based VM/software licensing and SaaS subscriptions are supported. Microsoft Marketplace publisher-country and payout-region documentation explicitly lists **Azerbaijan** as supported; marketplace payouts are available there, while PayPal payout is not. Current general payout threshold is USD 50.

Economic form:
`Net = customer license/usage revenue - 3% marketplace fee - hosting/cloud/API/data/support/tax costs - refunds/chargebacks where applicable`

Strategic value: one of the strongest Azerbaijan-compatible B2B software channels found so far. It is not passive on day one because publisher onboarding, product creation, compliance and support are required, but successful SaaS/API/metered software can later operate near-autonomously.

### 2. Google Cloud Marketplace — SaaS / cloud software seller
Status: **VERIFIED**
Class: BUILD-ONCE / server-native cloud distribution
Automation: 5 after deployment

Google Cloud Marketplace currently pays vendors their revenue split after collecting customer payments. The Vendor Net Revenue Schedule effective 2025-04-21 gives standard offers a 97% vendor net revenue share, while qualifying private/new/renewal/migration deals can retain 97–98.5% depending on deal type and TCV. Usage can be reported to Cloud Billing and converted into billable units.

Economic form:
`Net = billed marketplace revenue * vendor-net-revenue-% - cloud/runtime/API/data/support/tax costs`

Classification note: this is a true transaction/payment rail, not merely a directory. Seller organization approval and Marketplace Vendor Agreement requirements make it more operationally complex than a simple API store. Azerbaijan-specific seller eligibility still needs a dedicated legal/payout check before implementation.

### 3. Snowflake Marketplace paid listings
Status: **RESTRICTED**
Class: licensed data / data app / marketplace listing
Automation: 4–5 after data pipeline is built

Snowflake allows providers to charge consumers for Marketplace/private listings, create pricing plans and receive payouts through a linked Stripe Express account. However, current official documentation limits paid-listing providers by billing-address country. The current eligible list does **not** include Azerbaijan.

Implication: valid global mechanism, but not presently a direct Azerbaijan-based paid-listing route unless eligibility structure changes or a legitimately established entity in a supported jurisdiction is used. No evasion or false-location strategy is acceptable.

### 4. Databricks Marketplace — commercialized data, models, apps and MCP servers
Status: **VERIFIED / COMMERCIAL-CONTACT MODEL**
Class: data/model/MCP/software marketplace
Automation: 4–5 after product creation

Databricks Marketplace currently supports datasets, AI models, notebooks/apps and **MCP servers**. Official docs explicitly describe commercialized data offerings, paid filters, and listings that require provider approval because they involve a commercial transaction. Providers must join the provider program or use supported private-exchange onboarding and require Premium + Unity Catalog for public marketplace operation.

Important nuance: current docs show that commercial transactions can be arranged through provider-request workflows; this is not yet evidence of a universal self-service per-invocation payout rail comparable to RapidAPI or Apify. Therefore MCP listing itself is distribution; revenue is proven at the commercial-product level, not automatically per tool call.

### 5. Unity Asset Store
Status: **VERIFIED**
Class: digital asset / plugin / code/tool royalty
Automation: 4 after publication, but updates/support matter

Unity's current publisher page confirms creators can sell code tools, 3D models and other assets; there is no publishing fee and publishers retain **70% of revenue**. Submission review and tax/payout setup are required.

Best-fit products for this project: editor tools, automation utilities, reusable systems, procedural generators, code libraries and specialized templates that can be built once and sold repeatedly.

### 6. Fab (Epic) digital asset marketplace
Status: **VERIFIED**
Class: game/3D/design digital asset sales
Automation: 4 after publication

Epic's current Fab docs state publishers receive **88% of product-sales revenue**. Payout occurs roughly 30 days after month-end when the payable amount reaches USD 100; lower balances roll forward, with old unpaid balances eventually paid under the documented policy. Fab unifies several prior Epic creator marketplaces and accepts multiple digital-content formats.

This is a distinct strong build-once route for reusable 3D assets, materials, environments, game systems and compatible creator assets.

### 7. Envato Market
Status: **VERIFIED**
Class: themes/templates/code/plugins/creative assets
Automation: 4 after publication

As of July 2026 Envato uses a non-exclusive model with a standard **50% Author Fee** on the item-price component unless separately agreed otherwise. Current author documentation says authors set item prices on Market and payouts occur once balances meet the USD 50 threshold. Tax forms are required; royalty withholding can apply by source/residency.

This remains a real royalty/sale channel but has materially heavier platform take than Unity/Fab and therefore requires stronger demand or higher-margin products.

### 8. Envato Elements
Status: **VERIFIED**
Class: subscription royalty pool / subscriber-share digital assets
Automation: 4 after publication

Current Envato documentation states authors share **50% of net base-subscription revenue** using a subscriber-share model linked to customer usage of eligible items. This is economically different from per-item sales: creator income is usage-weighted subscription-pool allocation.

Mechanism family added: `subscription-pool usage royalty`.

### 9. Shutterstock contributor marketplace
Status: **VERIFIED**
Class: stock image/video licensing royalties
Automation: 4 after portfolio creation

Current contributor documentation states image/video contributors earn a percentage of Shutterstock licensing revenue, with six annual earnings levels ranging from **15% to 40%**. Levels reset each January. Monthly payouts are automatic once the applicable minimum and valid payout setup are satisfied.

This is passive only after asset creation; unit economics may be weak for generic assets, so portfolio scale and differentiated demand matter.

### 10. Shutterstock data licensing / Contributor Fund
Status: **VERIFIED**
Class: data/AI licensing royalty pool
Automation: 4 after eligible content contribution

Shutterstock separately documents data-licensing compensation: contributors receive an average **20% corporate royalty rate** of revenue Shutterstock receives for data licenses, distributed through the Contributor Fund based on assets used in licensed datasets/related eligible uses.

Mechanism family added: `dataset / AI-training-data pooled royalty`, distinct from ordinary stock downloads.

## New mechanism taxonomy added in Run 013
1. Cloud-procured usage-metered software resale.
2. Cloud marketplace private-offer revenue share.
3. Paid data listing with marketplace-collected payout.
4. Commercial data/MCP listing with negotiated/provider-approved transaction.
5. Engine/plugin marketplace unit sale royalty.
6. 3D/game/design asset marketplace unit sale royalty.
7. Creative marketplace item-sale royalty with author fee.
8. Subscription-pool usage royalty.
9. Stock license royalty ladder.
10. Dataset/AI-data pooled royalty.

## Azerbaijan relevance
### Direct positive evidence
- **Microsoft Marketplace**: Azerbaijan appears in both supported publisher-country documentation and payout-region tables. Marketplace payouts are supported; PayPal payout is not. This makes Microsoft one of the clearest locally actionable global B2B software marketplaces identified so far.

### Direct negative evidence
- **Snowflake paid listings**: current provider billing-address eligibility list does not include Azerbaijan. Classify as RESTRICTED for a directly Azerbaijan-based seller.

### Still unresolved
- Google Cloud Marketplace vendor onboarding/payout specifics for Azerbaijan.
- Databricks public-provider commercial payout mechanics by country.
- Unity/Fab/Envato/Shutterstock payout-provider availability and tax friction specifically for Azerbaijan; platform earning mechanisms themselves are verified.

## Strategic ranking from this run
Highest strategic value for autonomous/server income:
1. Microsoft Marketplace metered SaaS/API/software — strong because Azerbaijan support is explicit and enterprise billing is native.
2. Google Cloud Marketplace SaaS/usage software — strong enterprise channel; local seller eligibility still needs validation.
3. Databricks commercial data/model/MCP offerings — strong fit for AI/data services but more curated and transaction structure is less self-service.
4. Snowflake paid data listings — economically valid but locally restricted.

Highest strategic value for build-once digital royalties:
1. Fab — 88% creator share.
2. Unity Asset Store — 70% creator share, excellent for code/tools.
3. Envato Market/Elements — broad demand but higher effective platform share / pooled economics.
4. Shutterstock — mature licensing channel, but commodity content economics can be thin.

## Dead/non-paying distinction strengthened
A marketplace/catalog should not be counted as a separate earning source merely because a developer can list an integration, template, MCP server or app. It qualifies only if at least one of these is proven:
- platform processes customer payment and pays seller;
- listing explicitly supports a commercial transaction;
- creator receives a documented revenue/royalty share;
- marketplace routes to an owned paid service whose customer billing is independently real.

Therefore a free integration directory, template gallery, MCP directory or app showcase without creator payment remains **distribution only**, not autonomous income.

## Economics templates
### Software/cloud marketplace
`Net/month = paid seats + usage charges + private-offer revenue - marketplace share - compute - APIs/models - storage/egress - support - refunds - taxes`

### Data listing
`Net/month = listing/license revenue - marketplace/payment fees - data acquisition/licensing - refresh pipeline - storage/egress - compliance - tax`

### Digital asset royalty
`Net/month = paid licenses * creator share - creation amortization - update/support cost - refunds - taxes`

### Subscription royalty pool
`Expected income = distributable subscription pool * portfolio usage share - maintenance/tax`

## Completion assessment
Run 013 closes several major marketplace-distribution gaps but does **not** satisfy project completion. New independent mechanisms were still found, especially paid data/MCP distribution and dataset/AI-data pooled royalties. Saturation passes remain at zero.

## Next run
Run 014 should normalize proof-of-work/mining and remaining resource-mining families, including:
- CPU/GPU/ASIC mining mechanisms and pool economics;
- proof-of-capacity/storage mining variants not already classified as storage service;
- cloud/VPS mining ToS and profitability rejection patterns;
- auto-switching/hashpower marketplaces;
- NiceHash-style buyer/seller hashpower markets;
- merge mining;
- explicit dead/scam/non-paying mining projects;
- distinguish mining emissions from customer-paid compute/resource markets.

After that: scam/dead cross-checks, profitability normalization, Azerbaijan/KYC filtering, then repeated saturation/control passes.
