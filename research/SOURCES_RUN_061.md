# Sources — Run 061

Date checked: 2026-08-17

## RELOAD / reloadai.io
Primary sources:
- https://reloadai.io/ — marketplace/routing/seller positioning, model catalog and promotional activity examples.
- https://reloadai.io/sell — live seller surface; observed snapshot showed $0.00 seller earnings, $0.00 pool balance, 0 active offers and 0 models live.
- https://docs.reloadai.io/ — OpenAI-compatible routing, USDG billing, cheapest-healthy-seller routing and API behavior.
- https://reloadai.io/about — buyer/seller model and per-request USDG settlement description.
- https://reloadai.io/terms — seller obligations, USDG payments, upstream-resale rights and termination rules. Last updated July 2026.
- https://reloadai.io/acceptable-use — explicit seller authorization/upstream-provider-Terms requirement and abuse restrictions. Last updated July 2026.
- https://reloadai.io/privacy — wallet/Privy authentication, seller credential handling and on-chain data. Last updated July 2026.

Key evidence used:
- sellers must represent they have the right to resell upstream inference capacity;
- seller credentials are encrypted and health-checked;
- USDG settlement occurs on Robinhood Chain;
- no mandatory KYC flow was found in the reviewed public seller/legal pages;
- current live seller surface had zero active offers/models/earnings in the observed crawl.

## Conduit Protocol / conduitprotocol.net
Primary sources:
- https://www.conduitprotocol.net/ — protocol overview, provider roles, stake/routing language and mainnet positioning.
- https://www.conduitprotocol.net/onboard — capability provider, compute endpoint, workflow and relay supplier paths; USDC settlement and benchmark/stake language.
- https://www.conduitprotocol.net/roadmap — current mainnet/live phase claims for relays, compute endpoints, capability providers and Anchor programs.
- https://www.conduitprotocol.net/whitepaper — provider economics, 5% protocol cut, rewards pool, stake/slashing, temporary bootstrap subsidy and routing-weight design.
- https://www.conduitprotocol.net/terms — experimental-software warning, jurisdiction/sanctions responsibility, irreversible settlement and protocol role definition. Last updated 2026-05-21.

Key evidence used:
- Conduit explicitly describes APIs, compute endpoints, workflows and relays as paid provider roles;
- USDC is the primary settlement asset;
- provider/relay staking can be slashable for objective failures;
- a 5% protocol cut is described in the whitepaper;
- temporary subsidy must be separated from organic customer demand;
- reviewed sources did not establish explicit Azerbaijan eligibility or universal provider KYC;
- some first-party pages conflict on the exact staking asset, so implementation must revalidate current parameters.

## Tiny exact-role control
Queries:
- `decentralized inference USDG seller marketplace`
- `Robinhood Chain inference seller marketplace USDG`
- `capability provider x402 USDC Solana marketplace`
- `compute endpoint x402 USDC provider marketplace`

### New material project: API Mart
Primary sources:
- https://tryapimart.app/ — inference marketplace, seller flow, 1% platform fee, Robinhood Chain/USDG settlement and x402 Agent Skills positioning.
- https://tryapimart.app/docs — detailed buyer/seller routing, wallet auth, 1% fee, 99% seller top-up proceeds, upstream API-key model, agent checkout and x402 skill surface.
- https://tryapimart.app/sell — seller offer flow and stated 99% seller share / 1% platform fee.
- https://tryapimart.app/markets — observed snapshot showed 0 of 0 models and no text models available at crawl time.

Reason completion remains open:
API Mart was not found in the repository before this control and is a concrete independent implementation of an already-known inference-resale / paid-capability mechanism. Its public activity signals conflict, so one narrow validation run is required before final completion.
