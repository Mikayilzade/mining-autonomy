import json, tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from evaluator import (Opportunity,evaluate,SettlementAdapter,dry_run_execute,validate_result,CapabilityProfile,CostProfile,HashChainLedger,PayanAgentAdapter,OKXA2AAdapter,Agent2AgentAdapter,evaluate_payloads)
CAPS=CapabilityProfile({"extract","summarize","research"});POLICY=dict(rights_status="confirmed",tos_status="confirmed",automation_allowed="allowed",source_data_permission="confirmed");NOW=datetime(2026,8,19,tzinfo=timezone.utc)
def good(**kw):
 d=dict(platform="fixture",external_id="good",observed_at=NOW.isoformat(),kind="paid_task",status="open",fixed_payout_usd=5,currency="USD",estimated_input_tokens=1000,estimated_output_tokens=1000,estimated_duration_seconds=120,estimate_confidence=.9,metadata={"required_capabilities":["extract"]},**POLICY);d.update(kw);return Opportunity(**d)
def test_core_gates():
 assert evaluate(good(),CAPS,now=NOW).decision=="accept_dry_run"
 assert "prohibited_task" in evaluate(good(description="please do captcha bypass"),CAPS,now=NOW).reject_reasons
 assert "policy_evidence_insufficient" in evaluate(good(rights_status="unknown"),CAPS,now=NOW).reject_reasons
 assert "unsupported_capability" in evaluate(good(metadata={"required_capabilities":["video"]}),CAPS,now=NOW).reject_reasons
 assert "unknown_payout" in evaluate(good(fixed_payout_usd=0),CAPS,now=NOW).reject_reasons
 assert "unbounded_external_cost" in evaluate(good(external_cost_cap_usd=None),CAPS,now=NOW).reject_reasons
 assert "requires_value_moving_action" in evaluate(good(requires_value_moving_action=True),CAPS,now=NOW).reject_reasons
def test_stale_deadline_duplicate_confidence_quality():
 assert "stale_observation" in evaluate(good(observed_at=(NOW-timedelta(days=2)).isoformat()),CAPS,now=NOW).reject_reasons
 assert "deadline_too_close" in evaluate(good(deadline_at=(NOW+timedelta(minutes=17)).isoformat(),estimated_duration_seconds=600),CAPS,now=NOW).reject_reasons
 assert "duplicate_opportunity" in evaluate(good(),CAPS,now=NOW,seen={"fixture:good"}).reject_reasons
 assert "insufficient_estimate_confidence" in evaluate(good(estimate_confidence=.2),CAPS,now=NOW).reject_reasons
 assert "quality_contract_missing" in evaluate(good(metadata={"required_capabilities":["extract","research"]}),CAPS,now=NOW).reject_reasons
def test_cost_profile_changes_decision():
 assert evaluate(good(fixed_payout_usd=1,estimated_output_tokens=100000),CAPS,CostProfile(output_per_million=20),now=NOW).decision=="reject"
def test_adapters():
 meta=dict(POLICY,estimated_input_tokens=100,estimated_output_tokens=100,estimated_duration_seconds=60,estimate_confidence=.9)
 p=PayanAgentAdapter().adapt({"id":"p1","title":"x","bounty_usd":2,"currency":"USD","skills":["extract"],"observed_at":NOW.isoformat(),"metadata":meta});assert p.platform=="payanagent" and p.fixed_payout_usd==2 and p.estimate_confidence==.9
 o=OKXA2AAdapter().adapt({"task_id":"o1","budget_usd":3,"skills":["research"],"observed_at":NOW.isoformat(),"metadata":meta});assert o.platform=="okx_a2a"
 a=Agent2AgentAdapter().adapt({"task_id":"a1","bounty":4,"tags":["summarize"],"observed_at":NOW.isoformat(),"metadata":meta});assert a.platform=="agent2agent_market"
def test_ledger_chain_tamper_and_replay_dedup():
 with tempfile.TemporaryDirectory() as td:
  path=Path(td)/"ledger.jsonl";ledger=HashChainLedger(path);o=good();d=evaluate(o,CAPS,now=NOW);ledger.append(o,d);assert ledger.verify() and "fixture:good" in ledger.seen_keys()
  meta=dict(POLICY,estimated_input_tokens=100,estimated_output_tokens=100,estimated_duration_seconds=60,estimate_confidence=.9)
  payload={"id":"p1","bounty_usd":2,"skills":["extract"],"observed_at":NOW.isoformat(),"metadata":meta}
  first=evaluate_payloads("payanagent",[payload],ledger=ledger)[0];second=evaluate_payloads("payanagent",[payload],ledger=ledger)[0];assert first.decision=="accept_dry_run" and "duplicate_opportunity" in second.reject_reasons
  assert ledger.verify();lines=path.read_text().splitlines();row=json.loads(lines[0]);row["decision"]["decision"]="tampered";lines[0]=json.dumps(row);path.write_text("\n".join(lines)+"\n");assert not ledger.verify()
def test_executor_and_settlement_invariants():
 assert validate_result(dry_run_execute(good()));s=SettlementAdapter();assert s.enabled is False
 for fn in(s.enable,s.settle):
  try:fn()
  except RuntimeError:pass
  else:assert False,"settlement invariant broken"
