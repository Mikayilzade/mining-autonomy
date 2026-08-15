# Sources — Run 011 Build-once Digital Income

Evidence date: 2026-08-15

Primary/current sources used in this run.

## SaaS / usage billing
- Stripe — Usage-based billing documentation: https://docs.stripe.com/billing/subscriptions/usage-based
- Stripe — How usage-based billing works: https://docs.stripe.com/billing/subscriptions/usage-based/how-it-works
- Stripe — Pay-as-you-go implementation guide: https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide
- Stripe — Subscription integration design: https://docs.stripe.com/billing/subscriptions/design-an-integration

Key evidence: subscriptions can be flat/per-seat/tiered/usage-based; usage meters can record API requests/processing units and bill customers automatically.

## Shopify App Store
- Shopify Dev — Revenue share for Shopify App Store developers: https://shopify.dev/docs/apps/launch/distribution/revenue-share

Key evidence current 2026: standard developers keep 100% of first $1M gross app revenue measured from Jan 1 2025 and 85% above; 2.9% processing fee; one-time App Store registration fee.

## Atlassian Marketplace
- Atlassian Developer — Pricing, payment, and billing: https://developer.atlassian.com/platform/marketplace/pricing-payment-and-billing/
- Atlassian Marketplace platform docs: https://developer.atlassian.com/platform/marketplace/

Key evidence current 2026: paid-via-Atlassian apps, explicit revenue-sharing rates by Forge/Connect/Data Center; current Forge incentive up to $1M lifetime Forge revenue under eligibility rules.

## Chrome Web Store
- Chrome for Developers — What is the Chrome Web Store?: https://developer.chrome.com/docs/webstore/about
- Chrome Web Store policies: https://developer.chrome.com/docs/webstore/program-policies/policies
- Chrome developer registration: https://developer.chrome.com/docs/webstore/register
- Chrome Web Store API: https://developer.chrome.com/docs/webstore/api

Key evidence: extensions can be published and monetized using developer-selected payment systems; payments must be transparent and secure; publishing requires developer registration.

## Google Play
- Google Play Console Help — Service fees: https://support.google.com/googleplay/android-developer/answer/112622
- Google Play Console Help — Understanding subscriptions: https://support.google.com/googleplay/android-developer/answer/12154973
- Google Play Console Help — Payments policy: https://support.google.com/googleplay/android-developer/answer/9858738
- Google Play Console Help — Subscription policy: https://support.google.com/googleplay/android-developer/answer/9900533

Key evidence: paid apps/in-app digital goods/subscriptions are live mechanisms; 2026 fee structures vary by region/program; subscriptions must provide sustained recurring value and transparent renewal/cost terms.

## AWS Data Exchange / data APIs
- AWS Data Exchange — Product subscriptions: https://docs.aws.amazon.com/data-exchange/latest/userguide/product-subscriptions.html
- AWS Data Exchange — Creating offers: https://docs.aws.amazon.com/data-exchange/latest/userguide/prepare-offers.html
- AWS Data Exchange — Provider onboarding/eligibility: https://docs.aws.amazon.com/data-exchange/latest/userguide/provider-getting-started.html
- AWS Data Exchange — Publishing API products: https://docs.aws.amazon.com/data-exchange/latest/userguide/publish-API-product.html
- AWS Marketplace — Data products: https://docs.aws.amazon.com/marketplace/latest/userguide/data-products.html

Key evidence: providers can sell subscription data products and metered APIs, including per request/per successful request/per data transfer pricing. Current paid-provider jurisdiction list does not include Azerbaijan, so direct paid-provider onboarding from Azerbaijan is restricted under these docs.

## Gumroad
- Gumroad Help — Fees: https://gumroad.com/help/article/66-gumroads-fees.html
- Gumroad Help — Getting paid: https://gumroad.com/help/article/13-getting-paid.html
- Gumroad Help — Affiliates: https://gumroad.com/help/article/333-affiliates-on-gumroad
- Gumroad Help — Collaborations: https://gumroad.com/help/article/341-collaborations.html

Key evidence: digital creator storefront with automated payment/file delivery, affiliates/collaborators and creator payouts. Current direct-site fee and discovery-marketplace fee differ materially.

## Adobe Stock
- Adobe Stock Contributor — Royalty rates: https://helpx.adobe.com/stock/contributor/payments-earnings/royalties-pricing/royalty-rates-assets.html

Key evidence current Jun 2026: standard royalties listed as 33% photos/vectors/illustrations and 35% video on applicable net licensed price.

## Amazon KDP
- Amazon KDP — Digital book pricing: https://kdp.amazon.com/en_US/help/topic/G200634500
- Amazon KDP — eBook royalties: https://kdp.amazon.com/en_US/help/topic/G200644210
- Amazon KDP — Earn page: https://kdp.amazon.com/en_US/earn

Key evidence current 2026: eBook 35%/70% royalty options under stated conditions; print-on-demand royalty mechanics and Kindle Unlimited revenue path exist.

## GitHub Sponsors
- GitHub Docs — Sponsorships, fees and taxes: https://docs.github.com/en/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes

Key evidence: recurring/one-time sponsorship mechanism; GitHub currently charges no platform fee on personal-account sponsorships and up to 6% on organization-account sponsorships depending on payment mode.

## Evidence notes
- Marketplaces validate monetization mechanisms, not profitability.
- Current fees/revenue-share terms are time-sensitive and must be revalidated at implementation.
- Data-product legality requires source-specific licensing/privacy/redistribution checks.
- Marketplace policy compliance is mandatory; no fake engagement, deceptive monetization, spam or unauthorized scraping/data resale is in scope.
