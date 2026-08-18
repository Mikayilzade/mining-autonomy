"""Offline CLI. Example: python implementation/evaluate_cli.py payanagent snapshot.json --ledger out.jsonl"""
import argparse, json
from pathlib import Path
from evaluator import ADAPTERS, CapabilityProfile, CostProfile, HashChainLedger, evaluate

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("platform", choices=sorted(ADAPTERS)); ap.add_argument("input")
    ap.add_argument("--capabilities", default="extract,summarize,research"); ap.add_argument("--ledger"); args=ap.parse_args()
    raw=json.loads(Path(args.input).read_text()); payloads=raw if isinstance(raw,list) else raw.get("items",[raw])
    caps=CapabilityProfile(set(filter(None,args.capabilities.split(",")))); seen=set(); ledger=HashChainLedger(args.ledger) if args.ledger else None; results=[]
    for p in payloads:
        o=ADAPTERS[args.platform].adapt(p); d=evaluate(o,caps,CostProfile(),seen=seen); seen.add(f"{o.platform}:{o.external_id}")
        if ledger: ledger.append(o,d)
        results.append(d.__dict__)
    print(json.dumps(results,indent=2,sort_keys=True))
    if ledger and not ledger.verify(): raise SystemExit("ledger verification failed")
if __name__=="__main__": main()
