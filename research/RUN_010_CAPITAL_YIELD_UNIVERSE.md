# Run 010 — Capital-based passive / semi-passive income universe

Date: 2026-08-15
Status: COMPLETED
Phase: Universe construction, not portfolio recommendation

## Purpose
Map capital-native income mechanisms by **what economically pays the return**, not by marketing labels. This run does not claim any strategy is profitable, safe, guaranteed, or accessible from Azerbaijan without separate broker/platform and legal/tax validation.

## Core taxonomy

### A. Cash and sovereign fixed income
1. **Insured bank savings / current-account interest**
   - Return source: bank net interest margin / deposit funding economics.
   - Automation: 5 once deposited; possible automatic sweeps.
   - Main risks: bank/insurance-limit/currency/inflation/reinvestment risk; jurisdiction limits.
   - Net model: `interest - account fees - tax - FX loss - inflation erosion`.

2. **Term deposits / certificates of deposit**
   - Return source: fixed bank funding cost over a committed tenor.
   - Automation: 5 with auto-renewal, but auto-renewal can lock funds at unattractive future rates.
   - Risks: early-withdrawal penalties, bank credit above insured limits, currency risk.

3. **Money-market deposit / brokerage cash sweep**
   - Return source: bank deposit rate or short-term securities yield depending on sweep vehicle.
   - Important distinction: a bank deposit sweep can have deposit insurance subject to limits; a money-market mutual fund is an investment fund and is not FDIC-insured.
   - Automation: 5.

4. **Money-market mutual funds**
   - Return source: short-term debt/cash-equivalent portfolio yield; distributed as dividends.
   - SEC Investor.gov describes these as relatively low-risk versus most mutual funds but explicitly not FDIC insured; stable NAV can still break and liquidity fees can exist under stress.
   - Automation: 5 through broker/reinvestment.
   - Risks: NAV loss, liquidity fees, credit exposure, inflation, fee drag.

5. **Treasury bills**
   - Return source: sovereign borrowing; bills are sold at par or discount and mature at face value.
   - TreasuryDirect describes bills as maturities of one year or less.
   - Automation: 4–5 via broker ladders/rolls, subject to platform API/features.
   - Risks: mark-to-market if sold early, reinvestment, inflation, FX for non-USD investor, custody/broker access.

6. **Government notes/bonds**
   - Return source: sovereign coupons + principal repayment.
   - Automation: 5 if held to maturity; laddering can be semi-automated.
   - Risks: duration/interest-rate risk, inflation, FX, sovereign risk outside strongest issuers.

7. **Inflation-linked sovereign bonds (e.g. TIPS family)**
   - Return source: sovereign coupon plus inflation-indexed principal mechanics.
   - Automation: 5.
   - Risks: real-yield moves, deflation mechanics, tax treatment, FX and access.

8. **Floating-rate sovereign notes**
   - Return source: sovereign interest reset to a reference mechanism.
   - Automation: 5.
   - Risks: lower income when short rates fall, FX/access.

### B. Public debt / income securities
9. **Investment-grade corporate bonds**
10. **High-yield corporate bonds**
11. **Municipal bonds where available**
12. **Bond ETFs / mutual funds**
13. **Short-duration / ultra-short bond funds**
14. **Floating-rate / leveraged-loan funds**
15. **Preferred shares / preferred-stock funds**
16. **Convertible bonds / funds**
17. **Mortgage-backed / asset-backed income funds**

Economic source: issuer/borrower interest payments and, for funds, portfolio interest/capital changes.

Key distinction: owning a bond to maturity is not economically identical to owning an open-ended bond fund. Investor.gov explicitly notes bond funds can lose money from credit and interest-rate risk, with longer maturities generally more rate-sensitive.

Leveraged-loan/floating-rate funds are a separate family because coupons reset with rates, but SEC material highlights borrower-default, liquidity and weaker-covenant risks.

Automation: normally 4–5 via brokerage recurring investment/dividend reinvestment; true API automation depends on broker ToS/API.

### C. Public equity income and real assets
18. **Broad-market index funds with distributions**
19. **Dividend-growth / high-dividend equities and ETFs**
20. **Publicly traded REITs**
21. **Mortgage REITs**
22. **Infrastructure equities/funds**
23. **Utilities income portfolios**
24. **BDC / listed private-credit vehicles**
25. **Royalty trusts / listed royalty companies**
26. **Covered-call / option-income funds**

Return sources differ:
- equity dividends: company profits/cash distributions;
- REITs: rents/property operations or mortgage-credit spreads;
- infrastructure/utilities: operating cash flow;
- BDC/private-credit vehicles: borrower interest/fees;
- royalty structures: contractual share of commodity/IP/revenue;
- option-income funds: option premia plus underlying portfolio return.

Investor.gov notes public REITs must distribute at least 90% of taxable income under the REIT structure, while mortgage REITs can be materially more leveraged. High distribution yield is not proof of high total return.

Automation: 5 for buy/hold/reinvestment; market-price and principal risk remain.

### D. Private credit / alternative financing
27. **P2P / marketplace consumer lending**
28. **SME/business marketplace lending**
29. **Invoice / receivables financing**
30. **Factoring participation**
31. **Real-estate debt crowdfunding**
32. **Real-estate equity crowdfunding**
33. **Startup equity crowdfunding**
34. **Revenue-share / revenue-based financing**
35. **Private credit funds**
36. **Private placements / notes / SAFEs / convertible notes**
37. **Litigation-finance participation where legal/available**
38. **Music/IP/royalty marketplace investments**
39. **Equipment/asset leasing participation platforms**

Return source: borrower interest/fees, asset cash flow, sale proceeds, royalties or contractual revenue share.

SEC crowdfunding guidance classifies early-stage crowdfunding as speculative and often illiquid; resale may be restricted and total loss is possible. SAFEs are not equivalent to current equity and may never convert if trigger conditions do not occur.

Automation: typically 2–5 depending on auto-invest/reinvestment support. API botting must never be assumed permitted merely because the website is automatable.

Major risks: default, platform failure, adverse selection, fraud, weak secondary liquidity, servicing interruption, legal enforceability, concentration, KYC/geography.

### E. Native crypto staking and security yield
40. **Solo proof-of-stake validator**
41. **Staking-as-a-service**
42. **Delegated staking**
43. **Pooled staking**
44. **Liquid staking tokens (LSTs)**
45. **Validator node + delegated third-party capital business** — operational/business variant, not merely passive holding.

Ethereum official material provides a clear model: solo staking uses capital plus validator operation; current native Ethereum staking requires a validator balance path beginning at 32 ETH, with rewards for protocol duties and penalties/slashing for failures or malicious behavior. Pooled/liquid staking adds third-party and smart-contract risks.

Return source: protocol issuance, priority/transaction fees and sometimes MEV, depending on chain/protocol.

Automation: delegated/LST 5; solo validator 4–5 with monitoring.

Net model: `protocol rewards + fees/MEV - validator infra - staking service fee - slashing/penalty expectation - token price loss - tax`.

### F. Restaking / shared-security yield
46. **Native restaking**
47. **Liquid restaking tokens**
48. **Operator/delegation restaking services**

Return source: compensation for extending cryptoeconomic security to additional services, often layered on base staking.

Classification: higher-complexity capital yield, never 'free extra APY'. Adds smart-contract, operator, slashing/penalty, rehypothecation/liquidity and dependency risk. Current project/platform economics require dedicated later validation before ranking.

### G. On-chain lending / stablecoin yield
49. **Permissionless money-market lending**
50. **Curated lending vaults**
51. **Stablecoin savings-rate modules / protocol savings tokens**
52. **Tokenized T-bill / RWA yield tokens**
53. **Centralized exchange earn/lending** — separate custodial counterparty family

Aave official docs establish the canonical mechanism: suppliers provide assets to overcollateralized lending pools and receive variable interest driven by borrowing utilization. Morpho Vault docs similarly attribute native yield to borrower-paid interest, with optional incentive rewards and fees layered on top.

Return source must therefore be split into:
- borrower-paid organic interest;
- temporary token incentives;
- RWA interest passed through from off-chain assets;
- platform subsidy.

Automation: 5 on-chain once positioned; reallocation bots/vaults can add automation but also execution and strategy risk.

Risks: smart contract, oracle, collateral/liquidation contagion, stablecoin depeg, bad debt, governance, bridge/network, front-end/geofence, custodial risk for centralized variants.

### H. Automated vault / allocator yield
54. **Lending optimizer vaults**
55. **Multi-protocol yield vaults**
56. **Delta-managed vaults**
57. **Automated treasury allocators**
58. **Structured on-chain earn products**

Morpho's current docs explicitly expose vault operations, APY tracking, rewards integration, APIs and SDKs. This creates two separate project families:
1. capital deposited into automated vaults;
2. BUILD-ONCE/API products that route customers into vaults and potentially monetize the integration/business layer.

Net model: `underlying organic yield + incentives - management/performance fees - gas - expected smart-contract/strategy loss`.

### I. AMM liquidity provision / market making
59. **Constant-product LP (full-range)**
60. **Concentrated-liquidity LP**
61. **Stable-swap LP**
62. **Single-sided/managed LP vaults**
63. **Automated LP rebalancing bots/vaults**

Uniswap official docs confirm LPs deposit token pairs and earn trade fees; v3/v4 concentrated liquidity requires selecting a price range and can increase capital efficiency but requires management. Uniswap's glossary explicitly characterizes LP compensation as trading fees in exchange for taking price risk.

Return source: user swap fees + possible incentives.

Critical model: `fees + incentives - divergence/LVR/price risk - rebalancing gas - MEV/adverse selection - vault fees`.

Do not present quoted APR as passive interest: returns depend on trading volume, volatility, range selection and relative token prices.

Automation: full-range LP 4–5; concentrated LP 2 manually or 4–5 through strategy vault/bot.

### J. Fixed/term yield and yield-token markets
64. **Principal-token fixed/term yield**
65. **Yield-token exposure**
66. **Yield-token AMM liquidity**
67. **Fixed-rate lending markets**

Mechanism: tokenize or contractually separate principal from future yield, allowing an investor to lock an implied return if held to maturity, while another party buys floating/future yield exposure. Pendle is a canonical protocol family for yield-tokenization; dedicated up-to-date platform validation is still required before implementation/ranking.

Risks: underlying yield-bearing asset risk, smart contracts, maturity liquidity, depeg, market pricing, chain risk.

### K. Basis / funding / market-neutral-looking strategies
68. **Spot-perpetual cash-and-carry**
69. **Futures basis capture**
70. **Funding-rate capture**
71. **Cross-venue basis**
72. **Delta-neutral LP/hedged yield**
73. **Options carry / covered-call automation**
74. **Volatility risk-premium strategies**

These are **trading strategies, not passive yield products**. Automation can be 4–5 through permitted exchange/broker APIs, but returns are not guaranteed.

Economic source: basis convergence, funding transfers, option premium or market-making compensation.

Risks: basis reversal, funding sign change, liquidation, margin calls, exchange/custody failure, API outages, hedge mismatch, fees, borrow cost, execution slippage, tax/legal constraints.

Net model: `basis/funding/premium - borrow - trading fees - funding paid - hedge slippage - liquidation loss expectation - custody/counterparty cost - server/API cost`.

### L. Tokenized real-world assets and revenue-sharing assets
75. **Tokenized Treasury products**
76. **Tokenized private credit**
77. **Tokenized real estate**
78. **Tokenized commodities with yield-bearing wrappers where any**
79. **Tokenized revenue-share / royalty claims**

Return source remains the off-chain underlying asset or contract; tokenization is only the ownership/settlement wrapper. Must validate securities status, issuer/SPV structure, redemption rights, KYC/geography and bankruptcy remoteness separately.

Automation: often 4–5 after onboarding, but legal/custodial constraints dominate.

## Server-adjacent capital opportunities discovered by this run
These should stay visible because they bridge the primary 'autonomous server' mission and the capital-income layer.

1. **Solo validators / validator fleets** — capital + server operation; can become near-autonomous but require monitoring and slashing controls.
2. **Validator-as-a-service / delegation business** — build infrastructure once, earn service commissions from third-party stake where protocol rules permit.
3. **Restaking operator services** — analogous shared-security operator model; separate platform validation required.
4. **Automated on-chain treasury allocator** — daemon rebalances capital among approved markets based on explicit risk constraints; income belongs to the capital, while bot is an optimization layer.
5. **Automated lending/vault allocator product** — Morpho and similar protocols expose APIs/SDKs, creating a BUILD-ONCE integration/business opportunity distinct from merely depositing capital.
6. **Concentrated-liquidity management service** — server bot manages ranges/fees/rebalancing for owned capital or clients; strategy risk and regulatory/custody questions become central.
7. **Cash-and-carry/funding bot** — legitimate only through APIs and account structures that explicitly allow automation; not guaranteed and must survive full cost/stress testing.
8. **Broker cash/treasury sweep automation** — low-complexity capital routing where broker API/terms permit.

## Automation classification lesson
Capital income can look autonomous because human work is low, but the economic engine differs sharply:
- **pure passive holding**: return arises without ongoing machine work;
- **capital + node operation**: server work is necessary to earn protocol rewards;
- **capital + trading bot**: software manages market exposure; return is strategy P&L, not a fixed yield;
- **capital + build-once product**: software earns fees from other users' assets/activity.
These must not be combined in profitability rankings.

## Azerbaijan/KYC note
This run deliberately does **not** assert that U.S. TreasuryDirect, U.S. crowdfunding portals, any named broker, exchange or DeFi front-end accepts an Azerbaijan resident. Accessibility is a separate Run-level filter because residency, securities law, sanctions/geofence policy, KYC and payment rails can change. Permissionless smart contracts and front-end access must also be distinguished.

## New independent mechanism families added
Compared with prior runs, this stage formally adds/normalizes at least these capital-native families:
- bank deposit yield and automated cash sweeps;
- sovereign bill/note/bond ladders;
- money-market funds;
- bond/floating-rate/loan funds;
- public equity-dividend/REIT/infrastructure/BDC/royalty income;
- private/P2P/invoice/real-estate/startup/revenue-share credit/equity;
- native/delegated/liquid staking;
- restaking/shared-security capital yield;
- on-chain lending and curated lending vaults;
- stablecoin/RWA yield;
- AMM LP and managed concentrated liquidity;
- fixed/term yield-token markets;
- basis/funding/market-neutral-looking automated strategies;
- tokenized RWA/revenue-share wrappers;
- server-adjacent validator, allocator and liquidity-management businesses.

## What remains unresolved
- Azerbaijan-specific access/KYC/tax treatment for each concrete platform and broker.
- Current product-level rates/APYs; these are intentionally not frozen into the catalog because they are highly time-sensitive and can mislead.
- Exact current restaking products/operator admission and slashing regimes.
- Fixed-yield protocol-by-protocol validation.
- Centralized exchange earn products and jurisdiction restrictions.
- Concrete P2P/private-credit platforms accessible cross-border.
- Broker APIs/ToS for automated securities and cash-management strategies.
- Product-level profitability/stress testing.

## Conclusion
Run 010 substantially expands the secondary passive-income universe and identifies several bridges back into the primary server-autonomy mission. Discovery is still productive, so the project remains **IN PROGRESS**. Next stage should move to BUILD-ONCE digital income systems before returning to platform-level capital normalization and Azerbaijan filtering.
