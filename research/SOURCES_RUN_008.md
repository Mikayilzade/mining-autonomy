# Sources — Run 008

Validation date: 2026-08-15

Primary/current sources used for residential/device bandwidth research.

## EarnApp
- VM/Docker/hosting prohibition: https://help.earnapp.com/hc/en-us/articles/10199416541969--Can-I-install-EarnApp-on-Hosting-Services-Virtual-Machines-or-Dockers
- Earnings guide: https://help.earnapp.com/hc/en-us/articles/38640314568721
- IP blocking/datacenter restriction: https://help.earnapp.com/hc/en-us/articles/10201052442897--Why-is-my-IP-address-blocked
- Current payment methods/minimums are exposed through EarnApp support profile/articles, including PayPal/Wise minimum $10 as of 2026 support updates.

Established: residential/personal-device only; VM/Docker/cloud/server use prohibited; datacenter IP blocked; non-US guide rate up to $5/IP/month and US up to $10/IP/month conditional on demand/use.

## Honeygain
- Unusable network / disallowed DCH IP: https://support.honeygain.com/hc/en-us/articles/360011078760-Error-Unusable-network
- VPS/VM/emulator article: https://support.honeygain.com/hc/en-us/articles/360013096900-Can-I-use-a-Virtual-machine-or-an-Emulator-for-Honeygain
- Technical requirements incl. Linux Docker: https://support.honeygain.com/hc/en-us/articles/360011063260-What-are-the-technical-requirements-to-run-Honeygain
- Device/IP limits: https://support.honeygain.com/hc/en-us/articles/360011188779-What-is-the-maximum-number-of-devices-allowed-by-Honeygain
- Minimum payout: https://support.honeygain.com/hc/en-us/articles/4412730754706-What-is-the-minimum-payout-threshold
- Payout country list including Azerbaijan: https://support.honeygain.com/hc/en-us/articles/23549158093980-Is-my-country-supported-to-payout-via-Tipalti-PayPal
- Anti-cheat guidance: https://support.honeygain.com/hc/en-us/articles/4412745227922-How-can-I-ensure-that-my-account-will-not-be-suspended
- Web Intelligence SDK economics: https://support.honeygain.com/hc/en-us/articles/12499929522332-How-much-can-I-earn-by-integrating-Honeygain-Web-Intelligence-SDK

Established: Docker support does not make Honeygain datacenter-compatible; DCH and several non-residential IP classes are unsupported. Max 10 gathering devices/account and 1 active device/IP. Default cash threshold $20; JumpTask provides token-mode alternative. Azerbaijan is in current Tipalti payout-country list.

## PacketStream
- Terms updated 2026-07-20: https://packetstream.io/terms-of-service/
- Share bandwidth: https://packetstream.io/share-bandwidth/
- Main site: https://packetstream.io/

Established: Packeter receives $0.10/GB eligible customer traffic; $5 minimum cashout; USD PayPal; weekly schedule; 3% PacketStream fee; traffic not guaranteed. Product explicitly describes residential proxy network.

## Pawns.app
- Supported devices incl. Linux/Docker: https://help.pawns.app/en/articles/8644266-which-devices-pawns-app-supports
- DCH/VPN-class IP error: https://help.pawns.app/en/articles/15942975-why-does-the-app-show-a-vpn-error-when-i-m-not-using-a-vpn
- Survey country list including Azerbaijan: https://help.pawns.app/en/articles/8646175-which-countries-surveys-are-available-in

Established: Docker exists technically, but DCH-classified IPs are not normal eligible bandwidth connections; therefore no ordinary VPS classification. Azerbaijan availability proven only for surveys in this run, not yet full payout path.

## TraffMonetizer
- Terms: https://traffmonetizer.com/terms-of-service/
- Downloads incl. Docker: https://traffmonetizer.com/downloads/
- Developer SDK: https://traffmonetizer.com/for-developers/

Established: consumer app requires valid residential IP and prohibits servers/VPN/proxy services. Minimum withdrawal $10. Developer SDK is separately reviewed and advertises $0.10/GB from app users' shared traffic.

## Repocket
- Main site: https://repocket.com/
- Terms: https://repocket.com/terms-and-conditions

Established: passive leftover-data feature exists. Public rules prohibit VPNs, proxies, emulators, virtual machines and multiple accounts for ordinary use.

## Grass
- Download/earning page: https://www.grass.io/download
- Stage 2 reward allocation: https://www.grass.io/learn/how-your-stage-2-rewards-allocation-works

Established: unused-internet contribution remains live. Current Stage 2 article documents USDC allocation combining Uptime and Network Points, recommends residential network/not VPN, and describes non-custodial-wallet distribution after claim. Heavy traffic concentration by geography/stability is explicitly reported.

## DAWN
- Terms: https://www.dawninternet.com/terms
- Validator extension: https://www.dawninternet.com/validator-extension
- Reward-system article: https://www.dawninternet.com/blog-posts/dawn-validator-extension-rewards-system
- Current network site/Black Box: https://dawninternet.com/

Established: extension earns reward points/proof-of-bandwidth participation, but Terms explicitly state Rewards have no monetary value and are not redeemable/transferable; do not count extension points as cash income.

## Nodepay
- Reward system: https://docs.nodepay.ai/user-participation-and-rewards/rewards-system
- Participation: https://docs.nodepay.ai/user-participation-and-rewards/participation
- Privacy policy: https://nodepay.ai/privacy-policy
- Current stats transition page: https://stats.nodepay.ai/
- Tokenomics: https://docs.nodepay.ai/nodecoin-usdnc/tokenomics

Established: historical/current privacy text still mentions bandwidth Node Points, but current reward documentation emphasizes genuine active signal/prompt/campaign participation and says rewards are tied to genuine contribution, not spam/random clicks. Current product direction has shifted from passive bandwidth toward predictive intelligence.

## EarnFM / Fleetshare
- Fleetshare overview/rates: https://sdk-docs.earn.fm/overview/
- Supplier prerequisites/KYC/agreement: https://sdk-docs.earn.fm/get-started/prerequisits/
- IP connection limits incl. datacenter: https://help.earn.fm/portal/en/kb/articles/how-many-ips-can-i-connect-on-my-account
- Java/server integration: https://sdk-docs.earn.fm/integration-guides/java/
- NodeJS integration: https://sdk-docs.earn.fm/integration-guides/nodejs/
- Help center: https://help.earn.fm/portal/en/home

Established: supplier program accepts 20+ IPs from users, servers or devices; integration types include SDK, Fleetshare server and Docker. Authorized datacenter IPs have no fixed upper account limit. Current documented Fleetshare rates: residential $0.10/GB, datacenter $0.04/GB; standard payout threshold $15. Supplier path requires approval, KYC/KYB, signed agreement and consent tracking for user devices.

## Source discipline notes
- Technical Docker/Linux support is never sufficient evidence for datacenter permission.
- Payout-country support for one product mode (e.g. Pawns surveys) must not be generalized to all earning modes.
- Points are not money unless current redemption/liquidity is established.
- SDK monetization must be separated from covert bundling; user consent is mandatory where provider rules require it.
