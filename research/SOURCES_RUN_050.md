# Sources — Run 050

Evidence date: 2026-08-17

## Primary / official surfaces

1. x402 official seller quickstart — `https://docs.x402.org/getting-started/quickstart-for-sellers`
   - Confirms API/service owners can charge AI agents/buyers per request.
   - Documents seller prerequisites and mainnet path on Base/Solana.

2. t2000 official marketplace — `https://t2000.ai/`
   - Live A2A store with explicit Sell path, USDC escrow/settlement, receipts, sold counts and current listing examples.
   - Public surface showed settled seller payouts and a visible 5% marketplace deduction on an example settlement.

3. Basilisk official marketplace — `https://www.basilisk.exchange/`
   - Explicit agent registration, bidding, earning and escrow architecture.
   - Supports Base/Solana; public surface states 70% immediate / 30% vested payout structure.
   - During this run public counters were all zero and no jobs were open.

4. x402 Bazaar project repository — `https://github.com/Wintyx57/x402-backend`
   - Documents `/register` marketplace route, 1 USDC registration cost, third-party marketplace services and x402-paid endpoint architecture.
   - Seller payout economics were not explicit enough in retrieved material to classify VERIFIED.

## Secondary/discovery surfaces

5. ClawHub A2A Market skill — `https://clawhub.ai/jamjamzxhy/skills/a2a-market`
   - Skill documentation describes buying/selling agent skills via x402 USDC on Base.
   - Used as a discovery lead, not sole proof of production demand.

6. Additional A2A Market skill mirrors/directories
   - `https://playbooks.com/skills/openclaw/skills/a2a-market`
   - `https://mcp.directory/skills/a2a-market`
   - `https://aiskill.market/skills/a2a-market`
   - Mirrors consistently describe seller listing, pricing and payment flow; production activity still requires first-party validation.

## Empirical/security references

7. Xiong et al., **Can Trustless Agents Be Trusted? An Empirical Study of the ERC-8004 Decentralized AI Agent Ecosystem** — arXiv:2606.26028
   - Finds operationally shallow registration and substantial Sybil/reputation quality problems across observed ERC-8004 deployments.

8. Mafrur & Khusumanegara, **From Agent Identity to Agent Economy: Measuring the Operational Readiness of ERC-8004 AI Agents** — arXiv:2606.12128
   - Finds identity registration much stronger than observable service/reputation/operational readiness.

9. Wang et al., **When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments** — arXiv:2607.19545
   - Documents facilitator/server security failure classes and reinforces need for strict payment binding, replay prevention, validation and gas controls.

10. Ling et al., **How Agentic Is Agentic Commerce? A Population-Scale Measurement of x402 Adoption and Authenticity** — arXiv:2607.12575
   - Shows raw x402 settlement counts can substantially overstate independent adoption because internal/fictitious activity can inflate headline transaction metrics.

## Evidence rule reinforced by this run
Do not rank a machine-payment marketplace from listing counts or transaction counts alone. Prefer independently attributable paid buyers, seller receipts, repeat purchases and externally verifiable settlement value.