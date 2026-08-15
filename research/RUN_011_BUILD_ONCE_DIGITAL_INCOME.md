# Run 011 — Build-once digital income systems universe

Date: 2026-08-15
Status: **COMPLETED**
Phase: universe construction, not profitability ranking

## Goal
Map digital products/services/assets that require meaningful initial creation but can later earn with high automation and low marginal human input. Priority is models where one server or one reusable asset can serve many paying customers.

This run is mechanism-first. A marketplace is evidence that a family can be monetized, not proof that any specific product will be profitable.

## Core classification
Build-once digital income separates into six economic engines:

1. **Recurring software access** — subscription SaaS, per-seat SaaS, usage-based SaaS.
2. **Metered machine service** — APIs, inference/transformation endpoints, data APIs, automation endpoints.
3. **Reusable digital asset licensing** — code, plugins, themes, templates, media, 3D, fonts/design assets, books, courses.
4. **Audience/distribution monetization** — affiliate content, newsletters, sponsorships, lead generation, advertising where policies permit.
5. **Marketplace-installed software** — Shopify/Atlassian/mobile/browser/app ecosystems where distribution and billing are partly outsourced.
6. **Hosted/managed service layer around an open protocol or operational pain point** — hosted OSS, dashboards, monitoring, fleet orchestration, reconciliation, reporting and optimization.

The same product can combine engines, e.g. a browser extension with a paid SaaS backend and affiliate/referral revenue.

---

# A. Highest-priority server-scalable families

## A1. Micro-SaaS / niche SaaS
Status: **VERIFIED family**
Automation potential: **4–5/5**
Server-native: **YES**

### What customers pay for
Recurring access to a narrow workflow improvement: monitoring, reporting, reconciliation, scheduling, data conversion, alerts, compliance checks, document processing, lightweight analytics, inventory/status synchronization, notification routing, etc.

### Monetization models
- flat monthly subscription;
- per-seat subscription;
- tiered subscription;
- usage-based billing;
- base fee + overage;
- prepaid credits;
- one-time setup + recurring software fee;
- white-label/reseller plan.

Stripe official documentation currently supports flat recurring and usage-based/metered billing, including usage meters and pay-as-you-go models. This validates the economic infrastructure for highly automated micro-SaaS and machine-service products.

### Why this is strategically strong
- one backend can serve many customers;
- marginal compute/storage cost can be low;
- billing/provisioning can be automated;
- high gross margin is possible when output is cheap relative to customer value;
- business customers may pay for time saved rather than raw compute consumed.

### Main costs
hosting + database + email/SMS + third-party APIs/LLMs + payment processing + support + monitoring + customer acquisition.

### Net model
`Net = subscription/usage revenue - infra - API/model costs - payment fees - refunds - support time - acquisition cost - taxes`

### Best candidate subfamilies for later idea generation
- recurring spreadsheet/report automation;
- reconciliation/checking systems;
- monitoring/status-change bots;
- scheduled data exports/transformation;
- compliance/deadline trackers;
- pricing/availability monitoring where source access is allowed;
- accounting/finance utilities;
- workflow glue between services via approved APIs;
- bulk file normalization/conversion;
- alerting for infrastructure/DePIN/node fleets;
- low-code customer portals;
- specialized calculators/estimators;
- document generation from structured inputs;
- lightweight vertical CRM/operations tooling.

Risk: distribution/CAC usually matters more than engineering once software works.

---

## A2. Paid API / machine-to-machine service
Status: **VERIFIED family**
Automation potential: **5/5**
Server-native: **YES**

### Paid commodities
- request/response transformation;
- validation/normalization;
- enrichment using licensed/permitted data;
- document parsing;
- conversion/rendering;
- image/audio/video processing;
- model inference;
- scoring/classification;
- geospatial calculation;
- OCR only where lawful and content rights permit;
- monitoring/aggregation;
- webhook/event routing;
- search/query over owned/licensed datasets.

### Pricing
- per request;
- per successful request;
- per MB/GB transferred;
- per second/minute processing;
- per token/model unit;
- recurring minimum + metered usage;
- prepaid credits.

AWS Data Exchange explicitly supports API products with contract pricing, metered pricing, or both, including per API request, per successful request and per unit of data transferred. Stripe likewise supports usage-based metering.

### Strategic strength
This is one of the closest BUILD-ONCE equivalents to the user's original 'server mines simple tasks' concept: rather than waiting for a reward network, build a useful endpoint and let customers or other software repeatedly purchase small units of automated work.

### Risks
- API dependency can compress margins;
- rate limits and upstream ToS;
- abuse/fraud;
- support burden;
- commoditization;
- customer acquisition.

### Strong later filters
Prefer an API where:
`customer value per request >> variable compute/data cost per request`.

---

## A3. Data product / dataset / continuously updated feed
Status: **VERIFIED but rights-sensitive**
Automation potential: **4–5/5**
Server-native: **YES**

### Economic model
Create/own/license a dataset or continuously updated feed and sell subscriptions/access instead of selling one-time manual research.

### Delivery modes
- file snapshots;
- scheduled revisions;
- database/share access;
- API;
- alerts/deltas;
- dashboards;
- custom enterprise feeds.

AWS Data Exchange confirms providers can sell subscription-based data products with 1–36 month offer durations and can publish API-backed products. Provider onboarding is jurisdiction-limited and requires qualification/support/legal rights. This is important: a technically easy dataset business can be legally invalid if source rights are weak.

### Candidate subfamilies
- public-domain data normalized into useful form;
- first-party collected data;
- opt-in telemetry;
- licensed source aggregation;
- business directories where redistribution rights are explicit;
- historical time series from permitted sources;
- benchmark/reference datasets;
- machine-readable regulatory/public filings with permitted redistribution;
- niche pricing/catalog intelligence using authorized feeds;
- generated synthetic datasets with clear provenance.

### Hard rule
**Do not equate 'publicly viewable webpage' with reusable commercial data rights.** Scraping, database rights, privacy, robots/contract restrictions and redistribution licenses must be checked source by source.

### Azerbaijan relevance
AWS Data Exchange paid-provider eligibility list in current official docs does not list Azerbaijan, so direct paid-provider onboarding there is currently **RESTRICTED** unless a valid business entity in an eligible jurisdiction is used lawfully. The underlying data-product business family remains valid through other infrastructure/platforms.

---

## A4. Automated B2B monitoring / reporting / alerting service
Status: **VERIFIED family by SaaS/API mechanism**
Automation potential: **5/5 after setup**
Server-native: **YES**

This deserves a separate category from generic SaaS because the paid output can be generated on a schedule with almost no interactive usage.

Examples:
- daily/weekly exception reports;
- price/inventory/status alerts using authorized sources;
- payment/reconciliation exception detection;
- SLA/uptime monitoring;
- certificate/domain/license expiry alerts;
- compliance date alerts;
- cloud-cost anomaly reports;
- vendor/master-data change tracking where authorized;
- data-quality checks;
- automated evidence packs;
- node/validator/DePIN fleet health reports.

Economic attraction: customer pays for **not having to check manually**. The daemon may perform thousands of cheap checks and send only exceptions.

Potential pricing: per monitored entity, per account, per check frequency, per alert volume, per workspace, per connected source.

---

## A5. Hosted open-source / managed version
Status: **VERIFIED family**
Automation potential: **4–5/5**
Server-native: **YES**

### Revenue layers
- managed hosting;
- premium cloud features;
- backups/HA;
- enterprise auth/audit;
- support/SLA;
- private deployment;
- commercial license / dual license;
- paid plugins/connectors;
- GitHub Sponsors as supplemental funding.

GitHub Sponsors remains a real recurring/one-time funding path for eligible developer/organization profiles. Personal-account sponsorships currently have no GitHub fee; organization sponsorships can incur up to 6% depending on payment method.

### Important lesson
OSS sponsorship is not equivalent to product revenue. The stronger business pattern is often **open core + paid hosted service/support**, with sponsorship as an optional extra stream.

---

# B. Marketplace-installed software

## B1. Shopify App Store apps
Status: **VERIFIED**
Automation potential: **4–5/5**
Server-native backend: **YES**
Platform dependence: **HIGH**

Current Shopify developer docs say developers keep 100% of the first $1,000,000 USD in gross app revenue earned from Jan 1, 2025, then 85% above that under the standard threshold rules; billing also has a 2.9% processing fee. App Store registration has a one-time fee.

### Candidate products
- merchant reporting;
- inventory alerts;
- catalog cleanup;
- order tagging/routing;
- reconciliation/export tools;
- fraud/risk-support utilities that do not make prohibited claims;
- pricing/stock automations;
- localization/content workflows;
- B2B operations helpers.

Strength: marketplace distribution + recurring app charges.
Risk: review rules, API changes, merchant support and platform competition.

---

## B2. Atlassian Marketplace apps
Status: **VERIFIED**
Automation potential: **4–5/5**
Server-native: **YES / Forge or remote backend depending architecture**
Platform dependence: **HIGH**

Current Atlassian docs explicitly support paid apps and revenue sharing. For Jira/JSM/Confluence, rates depend on Forge/Connect/Data Center. As of Apr 1 2026 the published vendor share is 84% Forge, 80% Connect and 75% Data Center, with further changes scheduled Oct 1 2026. Atlassian also states eligible Forge partners can receive 100% of gross revenue up to $1M lifetime Forge revenue under current incentive conditions.

### Candidate product types
- workflow automation;
- reporting;
- project hygiene/quality checks;
- issue synchronization;
- dashboards;
- compliance evidence;
- SLA helpers;
- imports/exports;
- AI-assisted summaries where data handling rules are met.

Strength: concentrated B2B customer base.
Risk: platform rules/security requirements and marketplace competition.

---

## B3. Browser extensions with paid backend
Status: **VERIFIED family**
Automation potential: **4–5/5**
Server-native backend: **YES**

Chrome Web Store documentation allows publishing extensions and states an item may be free or charged for using a payment system chosen by the developer. Current policies require transparent payment disclosures and secure handling of payment/sensitive information. Publishing requires a developer account and one-time registration fee.

### Strong business pattern
Free extension handles UI/context → backend performs valuable processing → subscription or usage billing unlocks premium features.

### Examples
- page-to-structured-data tools only for content users are authorized to process;
- productivity automation;
- email/text helpers;
- internal workflow shortcuts;
- browser-based monitoring/notifications;
- form/template utilities;
- research organizers;
- tab/bookmark/data cleanup.

### Hard restrictions
No deceptive installation, hidden monetization, fake engagement, undisclosed data collection or bypass of site restrictions.

---

## B4. Mobile apps / subscriptions / in-app digital goods
Status: **VERIFIED**
Automation potential: **4–5/5**
Backend server: **optional to central**
Platform dependence: **HIGH**

Google Play currently supports paid apps, one-time in-app products and recurring subscriptions. Service-fee schedules changed in 2026 by region/program; therefore economics must use the live fee rules at implementation time rather than a frozen global percentage.

### Candidate patterns
- utility subscription;
- freemium + premium features;
- usage-credit utility;
- niche reference/database app;
- scanner/calculator/tracker with server sync;
- AI utility where model/API cost is tightly controlled.

Important policy rule: subscriptions must deliver sustained recurring value and must be transparent about cost/renewal.

---

# C. Reusable digital asset licensing

## C1. Templates / spreadsheets / scripts / code packs / prompts / automation recipes
Status: **VERIFIED family**
Automation potential: **5/5 fulfillment; 2–4/5 marketing/support**

Channels can include own storefront, Gumroad-like platforms, app marketplaces, code marketplaces and niche communities.

Gumroad officially supports creator sales, automated payment/file delivery, affiliates and collaborations. Current direct-sale fee is 10% + $0.50 plus payment processing; marketplace-discovery sales use a higher fee. It supports digital creator products and can automate fulfillment.

### High-leverage variants
- Excel/Sheets automation packs;
- finance/reconciliation templates;
- operational checklists;
- niche calculators;
- code boilerplates;
- deployment templates;
- data-cleaning workflows;
- Notion-like templates;
- automation recipes;
- industry document generators.

Strength: almost zero marginal delivery cost.
Weakness: discoverability, piracy, support and low barriers to copying.

---

## C2. Plugins / extensions / themes / add-ons
Status: **VERIFIED family**
Automation potential: **4–5/5**

Distinct marketplaces include e-commerce, collaboration/project management, CMS, browser and IDE ecosystems. Direct paid distribution, freemium upgrades or hosted backends are all possible depending on marketplace policy.

Key distinction:
- **pure downloadable plugin** = high passive potential but upgrade/support burden;
- **plugin + SaaS backend** = recurring revenue but ongoing infra cost;
- **free plugin + paid support/add-ons** = distribution-first strategy.

Do not assume every marketplace permits direct paid extensions; validate each ecosystem before implementation.

---

## C3. Stock media / reusable creative assets
Status: **VERIFIED**
Automation potential: **5/5 after upload**, but production/catalog maintenance varies.

Adobe Stock currently pays standard contributor royalties of 33% for photos/vectors/illustrations and 35% for video based on net licensed price under its plans.

Subfamilies:
- photos;
- video;
- vectors/illustrations;
- motion graphics;
- sound effects/music where marketplaces accept it;
- 3D assets;
- icons/UI kits;
- design components;
- fonts where licensing/marketplace rules permit.

Economics: portfolio model. One asset can sell many times; long-tail catalog size/quality/search positioning drives revenue.

Risks: IP/model releases, generative-AI disclosure rules, saturated categories and platform-dependent search ranking.

---

## C4. E-books / reference products / continuously updated guides
Status: **VERIFIED**
Automation potential: **4–5/5 fulfillment; maintenance depends topic**

Amazon KDP currently supports self-published digital and print books; eBooks have 35% and 70% royalty options depending on territory/content/pricing conditions. Print-on-demand royalties are calculated after printing costs.

Distinct strategies:
- evergreen book;
- narrow professional reference;
- workbook/template bundle;
- periodically updated guide;
- serialized/series content;
- print-on-demand reference/manual;
- book that funnels to a paid SaaS/newsletter/service.

Key economic distinction: static evergreen content is more passive; current-information/reference products can become subscription-like but require maintenance.

---

## C5. Online courses / recorded training / reference library
Status: **VERIFIED general family**
Automation potential: **4–5/5 delivery; 2–4/5 support/marketing**

Economic engine is reusable recorded/structured instruction sold repeatedly. Can be one-time purchase, cohort-supported, membership library or bundled with software/templates.

Do not model as passive if success depends on continuous live coaching/community moderation.

---

## C6. Print-on-demand designs/products
Status: **VERIFIED general family**
Automation potential: **4/5**

Economic engine: reusable design/IP + marketplace/customer acquisition while third party handles printing/fulfillment.

Subfamilies:
- apparel;
- posters/art prints;
- books/journals;
- mugs/accessories;
- niche personalized products where automation can generate lawful customer-specific variations.

Net model:
`sale price - manufacturing - marketplace fee - fulfillment/shipping subsidies - ads - returns/refunds - taxes`.

Main weakness versus pure digital: lower margins and physical support/returns.

---

# D. Audience/distribution assets

## D1. Affiliate content sites / comparison/reference pages
Status: **VERIFIED family, distribution-dependent**
Automation potential: **3–4/5**

Revenue source: merchant commission after attributable sale/lead/action.

Possible assets:
- evergreen niche reference site;
- tools/calculators with affiliate links;
- comparison databases using permitted feeds;
- newsletters;
- tutorials tied to relevant products;
- niche directories.

### Compliance rule
No spam, fake reviews, misleading claims, cookie stuffing, unauthorized trademark bidding or auto-generated low-value pages against search/platform policies.

### Economics
`affiliate commission - hosting/content/data/marketing - update labor`.

This is not truly passive when rankings or offers change constantly.

---

## D2. Newsletter subscription / sponsorship / affiliate newsletter
Status: **VERIFIED family**
Automation potential: **3–4/5**

Revenue can combine:
- paid subscription;
- sponsorship/ads;
- affiliate links;
- premium data/report;
- lead generation;
- upsell to software/products.

Automation can handle ingest, formatting, scheduling and segmentation, but editorial trust usually still benefits from human oversight.

---

## D3. Lead-generation asset
Status: **VERIFIED family, compliance-sensitive**
Automation potential: **3–5/5**

Create a legitimate niche directory/calculator/form/service that attracts users who voluntarily request contact or quotes, then sell qualified leads or earn referral fees under disclosed terms.

Hard boundaries: privacy consent, sector regulation, no scraped-person spam, no fabricated leads, no deceptive forms.

---

## D4. Ad-supported content/tool
Status: **VERIFIED family but lower priority**
Automation potential: **3–5/5**

Revenue from legitimate human use of a site/app/tool. This is distinct from ad fraud; bots must never generate the traffic/clicks that trigger payment.

Better version: useful free tool produces organic human traffic; ads are secondary monetization, not the product.

---

# E. Marketplace/repository revenue-share models

## E1. Deployment/template/repository revenue share
Status: **VERIFIED family from earlier Run 006; expand later**
Automation potential: **5/5 after maintenance**

A reusable deployment template/repository/model can earn when other users deploy or consume it on a host/platform that shares usage revenue.

Known earlier example: Runpod Hub repository revenue-share path.

Search targets for later dedicated sweep:
- model hosting marketplaces;
- serverless templates;
- cloud marketplace images;
- workflow/template stores;
- agent/tool marketplaces;
- inference model deployment marketplaces.

This family is especially attractive because the asset can create **recurring infrastructure consumption revenue without owning the end-customer app**.

---

# F. Automated B2B service families worth treating as independent opportunities

These can each become separate products rather than generic freelance work:

1. **Monitoring-as-a-service** — uptime/status/price/stock/compliance changes.
2. **Reporting-as-a-service** — scheduled formatted reports from connected data.
3. **Reconciliation-as-a-service** — compare ledgers/files/systems and report exceptions.
4. **Data transformation-as-a-service** — normalize/convert/validate bulk data.
5. **Alerting-as-a-service** — rules engine + notifications.
6. **Orchestration-as-a-service** — schedule/control jobs/nodes/devices.
7. **Fleet management** — servers, validators, DePIN devices, remote agents.
8. **Optimization-as-a-service** — cost/routing/resource/portfolio recommendations where claims are bounded and lawful.
9. **Evidence/compliance pack generation** — collect authorized system evidence and generate periodic packs.
10. **Backup/archive automation** — managed scheduled backups where credentials/data handling meet security requirements.
11. **Document generation** — invoices/reports/certificates/contracts from structured customer inputs, avoiding unauthorized legal/financial claims.
12. **Webhook/API glue** — translate and route events between systems.
13. **Data quality service** — duplicates, missing fields, schema drift, anomaly detection.
14. **Scheduler/queue service** — recurring customer jobs.
15. **Node/DePIN fleet accounting** — revenue/cost/uptime aggregation from multiple networks.

These are strategically more aligned with an autonomous server than low-price human task marketplaces because the server performs the paid work directly.

---

# G. Physical-DePIN / node ecosystem build-once overlays

Earlier research exposed a horizontal software layer independent of any single network:

## G1. Node fleet dashboard
Track uptime, version, hardware health, rewards, stake/collateral and alerts across multiple node networks.

## G2. Physical-DePIN fleet orchestration
For real devices: location inventory, firmware, connectivity, uptime, reward reconciliation and maintenance queue.

## G3. Reward/accounting normalization API
Convert heterogeneous token/reward histories into common fiat/time/cost metrics.

## G4. Deployment/upgrade automation
Provision legitimate nodes using official installation methods, monitor them and perform safe updates for customers.

## G5. Profitability telemetry
Calculate actual net yield after electricity, bandwidth, hosting, collateral, token price and downtime.

These products monetize the **operator pain** around mining/autonomy and may be more durable than operating the underlying network directly.

---

# H. Ranking framework for build-once systems

Every implementation candidate should later receive 0–5 scores on:
- initial build effort;
- recurring maintenance;
- marginal cost per customer;
- automation level;
- gross-margin potential;
- customer acquisition difficulty;
- marketplace/platform dependence;
- legal/data-rights risk;
- support burden;
- churn risk;
- scalability;
- defensibility;
- ability to serve many customers from one server;
- recurring versus one-time revenue;
- upstream API/provider dependency.

## Preferred shape
Ideal candidate:
- build effort 2–4;
- automation 5;
- low marginal cost;
- recurring revenue;
- customer pain is frequent/measurable;
- no fragile scraping dependency;
- no paid ads required to make unit economics work;
- support can be mostly self-service;
- can run on cheap VPS/serverless infra initially;
- has exportable customer value if one marketplace disappears.

---

# I. Major risks and anti-patterns

## I1. 'Passive' but actually marketing-heavy
Digital products can have zero delivery effort and still require continuous audience acquisition. Separate **fulfillment automation** from **revenue automation**.

## I2. AI wrapper with negative unit economics
If each user request incurs expensive LLM/image/video API cost, gross margin may collapse. Meter usage and cap abuse.

## I3. Unauthorized scraping/data resale
Reject any business whose core economics require violating access rules, privacy rights, copyright/database rights or contractual restrictions.

## I4. Marketplace captivity
Apps/extensions/assets can lose distribution after policy/API/algorithm changes. Prefer portable backend/customer relationships where permitted.

## I5. Fake passive ad/affiliate models
Bots may automate publishing/operations, but must not create fake clicks/views/leads/purchases.

## I6. One-time digital-product treadmill
A catalog that only earns when constantly launching new items is semi-active, not passive. Track revenue half-life and update load.

## I7. Support explosion
A $5 product with 30 minutes of support per buyer can be worse than a $50/month niche SaaS with self-service onboarding.

---

# J. Evidence-backed platform examples validated this run

1. **Stripe Billing** — recurring and usage-based billing infrastructure; validates SaaS/API metering models.
2. **Shopify App Store** — paid recurring app ecosystem with explicit current developer revenue share.
3. **Atlassian Marketplace** — paid B2B app marketplace with explicit current revenue share and Forge incentive structure.
4. **Chrome Web Store** — extension distribution with external payment systems allowed subject to policy and disclosure.
5. **Google Play** — paid apps, one-time digital products and recurring subscriptions with current service-fee rules.
6. **AWS Data Exchange** — paid subscription data products and metered API products; provider jurisdiction restrictions explicitly documented.
7. **Gumroad** — digital product storefront, payment/file delivery, affiliates and creator payouts.
8. **Adobe Stock** — reusable media licensing with current contributor royalty rates.
9. **Amazon KDP** — reusable eBook/print-on-demand publishing with current royalty mechanics.
10. **GitHub Sponsors** — recurring/one-time open-source sponsorship mechanism.

---

# K. Outcome of Run 011

Build-once digital income is not one category; it contains at least these independent mechanisms:

- subscription SaaS;
- usage-based SaaS;
- paid API;
- subscription data product;
- metered data API;
- automated scheduled B2B service;
- marketplace app recurring revenue;
- browser extension + paid backend;
- mobile app/subscription;
- downloadable template/code asset;
- plugin/theme/add-on licensing;
- stock media licensing;
- book/POD royalty;
- course/reference library;
- affiliate content asset;
- newsletter subscription/sponsorship/affiliate;
- compliant lead generation;
- ad-supported useful tool/content;
- OSS sponsorship;
- hosted OSS/open-core service;
- repository/deployment-template revenue share;
- DePIN/node fleet SaaS;
- reward/accounting normalization service.

This substantially expands the secondary passive-income universe and also produces several **primary-target-like server businesses** where an autonomous daemon repeatedly performs small paid tasks for many customers.

## Strongest categories for later prioritization
1. niche SaaS with recurring B2B pain;
2. paid API with large value/cost spread;
3. automated monitoring/reporting/reconciliation;
4. marketplace B2B apps (Shopify/Atlassian or similar);
5. browser extension + SaaS backend;
6. data product built only from owned/licensed/permitted sources;
7. node/DePIN fleet management;
8. hosted OSS / managed operational tooling;
9. reusable templates/assets as low-cost portfolio experiments;
10. deployment/model/template revenue share.

## Not yet done
- no product-specific profitability model;
- no exhaustive marketplace-by-marketplace sweep;
- no dedicated automated task/API labor-market sweep;
- no full dead/scam sweep;
- no Azerbaijan/KYC/platform-access normalization except the explicit AWS Data Exchange restriction noted above;
- no saturation/control pass.

## Next run
**Run 012 — legitimate automated task/API/job markets deep sweep.**

Search for systems where software can legally accept paid machine-executable jobs: data processing, inference, rendering, testing, benchmarking, verification, crawling only with authorized targets, webhooks, automation/action marketplaces, bounty/solver systems, agent/tool marketplaces and other machine-to-machine work exchanges. Explicitly reject human-only microtask sites that prohibit bots.

Saturation passes completed: **0**.
Conclusion: research remains **IN PROGRESS**; discovery is still productive.
