# Research Methodology

## Unit of research
Every earning opportunity is tracked as either:
- **Category** — a distinct economic mechanism;
- **Project/platform** — a concrete implementation;
- **Strategy** — a way to operate one or more platforms;
- **Rejected/adjacent** — useful to record but not currently viable/compliant.

## Required fields for each serious candidate
- Name
- Category / subcategory
- Official website/docs
- Status: `UNVERIFIED`, `VERIFIED`, `RESTRICTED`, `REJECTED`, `DEAD`, `WATCHLIST`
- What creates economic value / who pays
- Resource supplied: CPU / GPU / RAM / disk / bandwidth / IP / uptime / stake / capital / data / content / service / other
- Can run on normal VPS?
- Can run on bare-metal server?
- Can run on residential/home hardware?
- Automation level: 0–5
  - 0 = manual
  - 1 = mostly manual
  - 2 = recurring manual work
  - 3 = automate most operations
  - 4 = near hands-off with monitoring
  - 5 = daemon/node/API can run autonomously
- Initial capital
- Recurring cost
- Payout currency/token
- Minimum payout / lockup if any
- KYC requirement
- Geography restrictions / Azerbaijan availability if known
- ToS / automation restrictions
- Risk of account loss / slashing / collateral loss
- Revenue drivers
- Expected utilization
- Gross revenue evidence
- Net-profit formula
- Scaling constraints
- Maintenance burden
- Security/privacy/legal risks
- Evidence date
- Confidence level
- Next validation action

## Economics
Never call a project profitable from headline rewards alone.

Base formula:

`Net = payouts - server/hardware depreciation - electricity - bandwidth - storage - API/model costs - transaction fees - taxes/withdrawal fees - expected losses - human maintenance cost`

Also calculate where relevant:
- revenue per server/month;
- revenue per GPU-hour;
- revenue per CPU-core-hour;
- revenue per TB-month;
- revenue per TB egress;
- revenue per unique residential IP;
- capital yield/APY after fees and expected losses;
- break-even utilization;
- break-even electricity price;
- payback period on hardware/capital.

## Evidence hierarchy
Prefer:
1. official docs / Terms / pricing / network explorer;
2. protocol repository / source code / on-chain data;
3. official support articles;
4. reputable independent analytics;
5. community reports only as discovery leads, never sole proof of profitability.

All time-sensitive facts get an evidence date.

## Discovery method
Use repeated passes rather than one giant search.

### Pass families
1. General web discovery
2. DePIN directories and ecosystem maps
3. Decentralized compute
4. GPU marketplaces / AI inference
5. CPU marketplaces
6. Storage markets
7. Bandwidth/proxy/VPN/CDN/relay markets
8. Blockchain validators / RPC / indexers / sequencers / keepers
9. AI/data incentive networks
10. Video transcoding / media infrastructure
11. Search/indexing infrastructure
12. Wireless / mapping / sensor / physical DePIN
13. Crypto mining and proof-of-work
14. Legitimate automated task/API markets
15. Data collection/contribution markets
16. Financial capital yield
17. Digital asset / royalty income
18. Build-once automated businesses
19. Referral/revenue-share systems
20. Adjacent non-paying networks to reject explicitly
21. Scam/dead-project cross-check
22. Saturation/control searches using alternate terminology and languages

## Classification rules
### SERVER-NATIVE
A normal rented or owned server can participate without pretending to be a residential/human device and ToS allows this.

### HOME/RESIDENTIAL-ONLY
Requires personal/residential IP/device, consumer GPU, household storage, phone, browser extension, etc.

### CAPITAL-NATIVE
Return primarily comes from putting capital/stake at risk rather than performing paid computational work.

### BUILD-ONCE
Requires creating a product/asset/business first; later operation can be highly automated.

### RESTRICTED
Potentially legitimate, but important platform/region/hardware/KYC/automation constraints remain.

### REJECTED
Economically irrelevant, non-paying, clearly prohibited for our intended automation, deceptive, illegal, or otherwise outside scope.

## Anti-duplication
Many projects fit multiple buzzwords. Classify by **what actually gets paid for**, not marketing terminology.
Examples:
- GPU DePIN and GPU marketplace = compute if customers pay for compute.
- Browser extension rewarding unused IP = bandwidth/IP, not “AI mining”.
- Validator inflation = capital/stake + network operations, not compute income.

## Saturation rule
Do not declare completion because searches look repetitive. Track new unique candidates per pass. Move toward completion only when multiple differently-worded discovery passes, directory sweeps, and niche ecosystem searches converge and yield no new viable mechanisms and almost no new viable projects.
