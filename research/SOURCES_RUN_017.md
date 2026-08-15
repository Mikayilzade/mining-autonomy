# Sources — Run 017

Evidence date: 2026-08-15
Priority: current primary/official documentation.

## Golem
- Golem provider overview and payment mechanics: https://docs.golem.network/docs/golem/overview
- Provider installation: https://docs.golem.network/docs/providers/provider-installation
- Payment mechanisms: https://docs.golem.network/docs/golem/payments
- Mainnet/testnet and wallets: https://docs.golem.network/docs/golem/overview/testnet-mainnet
- GLM token / earning: https://docs.golem.network/docs/golem/overview/golem-token
- Mainnet funding and withdrawing GLM: https://docs.golem.network/docs/creators/python/guides/switching-to-mainnet

Key evidence: providers earn GLM; Polygon/Ethereum mainnet payment; provider may use/configure wallet; no ordinary provider KYC or Azerbaijan-specific exclusion observed in reviewed docs.

## Vast.ai
- Host payouts: https://docs.vast.ai/host/payment
- Hosting overview / hosting agreement process: https://docs.vast.ai/host/hosting-overview
- Verification stages: https://docs.vast.ai/host/verification-stages
- Datacenter status / identity and business verification: https://docs.vast.ai/host/datacenter-status
- Billing API showing payment-service integrations: https://docs.vast.ai/api-reference/billing/show-invoices
- Host tax guide / international host references: https://docs.vast.ai/host/guide-to-taxes
- PayPal country-of-residence service availability: https://www.paypal.com/mx/legalhub/paypal/residence-full?locale.x=en_MX
- Wise transfer-to-Azerbaijan information: https://wise.com/us/send-money/send-money-to-azerbaijan
- Stripe Connect stablecoin payout supported countries (includes Azerbaijan in current doc): https://docs.stripe.com/connect/stablecoin-payouts

Key evidence: Vast uses multiple payout rails; PayPal cannot be assumed usable for receiving in Azerbaijan; Wise can deliver transfers to Azerbaijani local bank accounts; Stripe has certain Azerbaijan-capable payout products, but Vast-specific exposure of those rails remains unproven.

## EarnFM Fleetshare
- Supplier prerequisites / 20+ IPs / KYC-KYB / agreement: https://sdk-docs.earn.fm/get-started/prerequisits/
- Fleetshare overview / rates / payout / bank transfer: https://sdk-docs.earn.fm/overview/

Key evidence: supplier acceptance required; Didit KYC/KYB; $0.10/GB residential, $0.04/GB datacenter; $15 standard minimum; >$300/month may request invoice bank transfer via SEPA or ACH; geography/IP reputation affects traffic.

## Storj
- Node payout documentation: https://storj.dev/node/payouts
- zkSync payouts: https://storj.dev/node/payouts/zk-sync-opt-in-for-snos
- Exchange-wallet warning: https://storj.dev/node/faq/can-we-use-an-exchange-as-a-wallet-for-storj-tokens
- Node Operator Terms and Conditions: https://www.storj.io/legal/supplier-terms-conditions

Key evidence: STORJ payout via Ethereum L1 or optional zkSync L2; operators should control wallet keys; terms contain export/sanctions restrictions rather than a reviewed Azerbaijan-specific ban; scaling rules include one node per IP and common payout address requirements.

## Sia
- Docker hostd setup / hardware requirements: https://docs.sia.tech/provide-storage/setting-up-hostd/docker
- Windows hostd setup: https://docs.sia.tech/provide-storage/setting-up-hostd/windows
- Legacy Linux host guide retained for wallet/collateral explanation: https://docs.sia.tech/legacy/hosting/hostd/setup-guides/linux

Key evidence: host-owned Siacoin wallet; collateral and proof funding required; recommended multi-TB storage hardware; no centralized fiat payout account in provider path.

## Akash
- Provider getting started: https://akash.network/docs/providers/getting-started/
- Should I run a provider?: https://akash.network/docs/providers/getting-started/should-i-run-a-provider/
- Provider hardware requirements: https://akash.network/docs/providers/getting-started/hardware-requirements/
- Provider playbook / wallet and location inputs: https://akash.network/docs/providers/setup-and-installation/provider-playbook/
- Provider setup preparation / bid deposit and wallet: https://akash.network/docs/providers/setup-and-installation/kubespray/provider-installation-prep/
- Provider attributes / location: https://akash.network/docs/providers/operations/provider-attributes/
- Provider audit: https://akash.network/docs/providers/operations/provider-audit/

Key evidence: provider role is wallet/on-chain and described as open/permissionless; location is an advertised attribute; production audit can impose material resource/network requirements.

## Filecoin
- Block rewards / 10 TiB WinningPoSt threshold: https://docs.filecoin.io/storage-providers/filecoin-economics/block-rewards
- Storage proving / WindowPoSt and slashing: https://docs.filecoin.io/storage-providers/filecoin-economics/storage-proving
- Filecoin Plus: https://docs.filecoin.io/basics/how-storage-works/filecoin-plus
- Filecoin programs / verified deal KYC context: https://docs.filecoin.io/storage-providers/filecoin-deals/filecoin-programs
- FIL token/payment role: https://docs.filecoin.io/basics/assets/the-fil-token

Key evidence: protocol rewards in FIL; ≥10 TiB storage power required for block-reward eligibility; collateral/proving/slashing; some verified-data programs add KYC/due diligence.

## Interpretation cautions
- Failure to find an explicit Azerbaijan exclusion is not equivalent to guaranteed onboarding.
- Payment processors can expose different capabilities through different platform configurations.
- Crypto-native provider admission and fiat off-ramp availability are separate questions.
- Geography can alter demand/utilization even if it does not block account creation.
