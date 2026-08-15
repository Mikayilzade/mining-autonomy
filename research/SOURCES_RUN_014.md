# Sources — Run 014

Evidence date: 2026-08-15.

Primary/current sources were preferred. Where a platform page was JavaScript-heavy, only mechanism-level claims visible in official pages/search results were retained and detailed fee claims were left pending.

## Mining pools / merged mining

1. f2pool — Mining pools info, payout schemes and thresholds (updated 2026-07-16)
   - https://f2pool.zendesk.com/hc/en-us/articles/360058887912-Mining-pools-info-payout-schemes-and-thresholds-at-f2pool
   - Supports current fee / payout-scheme / threshold normalization for BTC, LTC, BCH, ETC, DASH, ETHW and others.

2. f2pool — What payout schemes does f2pool use? (updated 2026-07-10)
   - https://f2pool.zendesk.com/hc/en-us/articles/360058808011-What-payout-schemes-does-f2pool-use-to-calculate-rewards
   - Confirms PPS, PPLNS, PPS+ and FPPS usage.

3. f2pool — Merged mining (updated 2026-06-29)
   - https://f2pool.zendesk.com/hc/en-us/articles/16927494808985-Merged-mining
   - Defines AuxPoW/merged mining and current BTC/LTC auxiliary-chain sets.

4. f2pool — Web merged mining guide (updated 2026-07-14)
   - https://f2pool.zendesk.com/hc/en-us/articles/22972592277401-Web-Merged-mining-guide
   - Current wallet/payout requirements and thresholds.

5. f2pool — Mining updates
   - https://f2pool.io/mining/updates/
   - Current auxiliary-chain additions and payout notes.

6. Poolin — Fractal Bitcoin merge mining
   - https://help.poolin.me/hc/en-us/articles/37567129615897-We-are-now-support-FB-Fractal-Bitcoin-Merge-Mining
   - Confirms BTC + FB merged-mining mechanism and PPLNS/threshold example.

7. Poolin — Bellscoin merge mining
   - https://help.poolin.me/hc/en-us/articles/36747619233177-We-are-now-support-Bellscoin-BEL-Merge-Mining
   - Confirms LTC/DOGE/BEL merged-mining example.

## Hashpower marketplaces / rentals

8. MiningRigRentals — For Rig Owners
   - https://www.miningrigrentals.com/helpcenter/For-Rig-Owners/76
   - Current rig-owner fee: 3% of rental received.

9. MiningRigRentals — payout / rental proceeds
   - https://www.miningrigrentals.com/helpcenter/For-Rig-Owners/29
   - Current hold/disbursement, owner fee and payout notes.

10. MiningRigRentals — Hashrate Resale / Broker Policy
    - https://www.miningrigrentals.com/helpcenter/User-Account/117
    - Explicitly permits third-party hashrate sourcing/resale, API-based listing/pricing/routing, and margin retention subject to disclosures, platform rules, performance and withdrawal controls.

11. NiceHash — Mining Hardware / marketplace navigation
    - https://www.nicehash.com/mining-hardware
    - Current official site continues to identify NiceHash as a hashrate marketplace and exposes CPU/GPU, ASIC, algorithms, marketplace, pricing, compatible-pool and profitability tooling.

12. NiceHash — Hash Power Marketplace help
    - https://www.nicehash.com/support/hash-power-marketplace/general-help/how-is-buying-hash-power-at-nicehash-different-from-cloud-mining-contracts
    - Current official marketplace help route; JS rendering prevented reliable extraction of detailed current fees in this run.

## Cloud / VPS policy

13. AWS Security Blog — Detecting and preventing crypto mining in your AWS environment (2026-05-13)
    - https://aws.amazon.com/blogs/security/detecting-and-preventing-crypto-mining-in-your-aws-environment/
    - States written approval is required for crypto mining on AWS; Free Tier and credits cannot be used.

14. Google Cloud Platform Terms of Service (current)
    - https://cloud.google.com/terms/
    - Section 3.3 restrictions: cryptocurrency mining requires Google's prior written approval.

15. Google Cloud — Policy violations FAQ
    - https://support.google.com/cloud/answer/7002354?hl=en
    - Free Trial Services cannot be used for cryptocurrency mining; prior written approval is required for mining.

16. DigitalOcean — Acceptable Use Policy (updated 2026-03-20)
    - https://www.digitalocean.com/legal/acceptable-use-policy
    - Mining any cryptocurrency without explicit written permission is prohibited.

17. Hetzner — Terms and Conditions
    - https://www.hetzner.com/legal/terms-and-conditions/
    - Explicit prohibition on cryptocurrency mining, including mining, farming and plotting.

18. Hetzner — Dedicated Server Service Agreement
    - https://www.hetzner.com/legal/dedicated-server
    - Explicit prohibition on applications used to mine cryptocurrencies.

19. Hetzner — Storage Box Service Agreement
    - https://www.hetzner.com/legal/storage-box
    - Explicit prohibition on cryptocurrency mining applications.

20. Linode — Can I Cryptomine on Linode?
    - https://www.linode.com/community/questions/24646/can-i-cryptomine-on-linode
    - Current accessible support guidance: shared CPU mining can trigger termination/resource-policy issues; dedicated CPU may be permissible but support ticket/approval context is recommended and approval is not guaranteed.

21. Linode — can I mine coins with cpu?
    - https://www.linode.com/community/questions/23627/can-i-mine-coins-with-cpu
    - Reinforces shared-resource constraints and dedicated-CPU distinction; also notes VPS mining generally lacks economic attractiveness.

## Secondary analytical background

22. Rosenfeld, M. — Analysis of Bitcoin Pooled Mining Reward Systems
    - https://arxiv.org/abs/1112.4980
    - Background on pooled-mining reward systems. Not used as primary evidence for current platform fees.

23. Can, Hougaard, Pourpouneh — On Reward Sharing in Blockchain Mining Pools
    - https://arxiv.org/abs/2107.05302
    - Analytical background on reward-sharing schemes.

## Evidence-quality notes

- Current platform rules/fees may change; revalidate before implementation.
- NiceHash fee details were not promoted to a specific current percentage because current official JS-heavy pages did not yield reliable fee text in this pass.
- Linode evidence is official community/support material rather than a freshly extracted clause from the AUP; therefore classify as RESTRICTED and require a current support confirmation before deployment.
- No profitability claim in Run 014 is based solely on calculators or historical anecdotal earnings.