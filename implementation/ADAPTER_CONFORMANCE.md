# Adapter Conformance Contract v0.1

No adapter may be promoted from offline/captured-style to live read-only until all items below are evidenced from a fresh, permitted raw snapshot.

## Required evidence
1. Source endpoint/transport and official permission to read it automatically.
2. Raw response retained in sanitized fixture form; secrets/PII removed.
3. Stable external task ID mapped without synthesis.
4. Observation timestamp and open/closed status semantics established.
5. Payout amount and currency semantics established; ranges/auctions are not coerced to fixed payout.
6. Deadline semantics/timezone established.
7. Required capabilities mapped conservatively.
8. Rights/ToS/automation/source-data evidence is independently populated; payload absence MUST remain `unknown` and fail closed.
9. Auth required merely to observe vs accept vs settle is documented separately.
10. Any deposit, escrow, arbitration bond, fee, gas, stake, wallet signature or other value-moving prerequisite is represented and cannot be hidden in metadata.
11. Pagination, rate limits, retries and stale-cache behavior are documented.
12. Schema-change detection exists; missing/renamed critical fields fail closed.

## Promotion tests
- sanitized fixture parses deterministically;
- malformed/missing payout rejects;
- unknown policy evidence rejects;
- duplicate task IDs replay-reject across persisted ledger runs;
- deadline/duration reserve works;
- low-confidence cost estimates reject;
- unsupported capability rejects;
- quality contract exists before dry-run acceptance;
- no connector can call accept/bid/submit/settle methods in read-only mode.

## Live-action boundary
Conformance only permits observation. Accepting work, signing, bidding, funding, KYC, paid APIs, publishing a monetized endpoint, or settlement remains separately authorization-gated.