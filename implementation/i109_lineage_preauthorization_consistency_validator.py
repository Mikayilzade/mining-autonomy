#!/usr/bin/env python3
"""I109 network-inert bridge: bind I108 lineage state into the four-gate preauthorization view.

This validator never creates a receipt or authorization and never performs network I/O.
Runtime verification may be projected true only from a present, exact-source-valid I108
result; the other three blockers remain derived independently from I100/I104.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Mapping
import i105_preauthorization_consistency_validator as i105
ROOT=Path(__file__).resolve().parent

def load(path: Path)->Mapping[str,Any]:
    v=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(v,dict): raise ValueError(f'{path} must contain object')
    return v

def validate(i104:Mapping[str,Any],i100:Mapping[str,Any],i108:Mapping[str,Any]|None)->dict[str,Any]:
    errors=[]
    base=i105.validate(i104,i100)
    if base.get('result')!='PASS': errors.append('I105 consistency failed')
    blockers=i104.get('non_substitutable_blockers',{})
    expected=dict(base.get('checked',{}))
    expected.pop('runtime_regression_receipt_present',None); expected.pop('four_gate_and',None)
    runtime_ok=bool(i108 and i108.get('receipt_present') is True and i108.get('exact_source_lineage_valid') is True and i108.get('result')=='PASS' and i108.get('derived_blockers',{}).get('runtime_regression_verification') is True)
    expected['runtime_regression_verification']=runtime_ok
    observed_runtime=bool(isinstance(blockers.get('runtime_regression_verification'),Mapping) and blockers['runtime_regression_verification'].get('satisfied') is True)
    if observed_runtime and not runtime_ok: errors.append('I104 runtime blocker true without current valid I108 lineage projection')
    all_four=all(expected.get(k) is True for k in ('fresh_real_execution_evidence','current_materialized_non_synthetic_resource_route','exact_explicit_user_authorization','runtime_regression_verification'))
    if i104.get('production_observation_allowed') is True and not all_four: errors.append('production observation allowed without four independent satisfied gates')
    return {'schema':'mining-autonomy/i109-lineage-preauthorization-consistency/v1','run':'I109','result':'PASS' if not errors else 'FAIL_CLOSED','network_capable':False,'execution_token':False,'authorization_creator':False,'production_observation_allowed':False,'derived_blockers':expected,'four_gate_and':all_four,'runtime_lineage_projected':runtime_ok,'errors':errors,'note':'I108 may satisfy only runtime regression verification. Fresh-real evidence, non-synthetic eligible Resource Router route, and exact explicit authorization remain independent.'}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--i104',default=str(ROOT/'I104_PREAUTHORIZATION_BLOCKERS.json')); p.add_argument('--i100',default=str(ROOT/'I100_EXECUTION_READINESS_RESULT.json')); p.add_argument('--i108',default=str(ROOT/'I108_RUNTIME_RECEIPT_LINEAGE_RESULT.json')); p.add_argument('--output'); a=p.parse_args()
    ip=Path(a.i108); r=validate(load(Path(a.i104)),load(Path(a.i100)),load(ip) if ip.is_file() else None); text=json.dumps(r,indent=2,sort_keys=True)+'\n'; print(text,end='');
    if a.output: Path(a.output).write_text(text,encoding='utf-8')
    return 0 if r['result']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
