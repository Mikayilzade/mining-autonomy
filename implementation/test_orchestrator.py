from datetime import datetime, timezone

from evaluator import CapabilityProfile
from orchestrator import audit_export, build_observation_queue, observe_passive
from passive_service import HostingTier, PassiveServiceOffer

NOW=datetime.now(timezone.utc).isoformat()
POLICY=dict(rights_status="confirmed",tos_status="confirmed",automation_allowed="allowed",source_data_permission="confirmed")


def task(task_id="t1", bounty=5, evidence="open_paid_request"):
    return ("payanagent", {"id":task_id,"title":"extract data","bounty_usd":bounty,"currency":"USD",
        "skills":["extract"],"observed_at":NOW,"metadata":dict(POLICY,estimated_input_tokens=1000,
        estimated_output_tokens=1000,estimated_duration_seconds=120,estimate_confidence=.9,external_cost_cap_usd=0)}, evidence)


def passive(demand=None, fixed=0):
    return PassiveServiceOffer(platform="mcpize",capability="normalize_text",price_per_call_usd=.01,
        creator_share=.80,variable_cost_per_call_usd=.00001,hosting=HostingTier("tier",fixed,250000),
        demand_calls_per_month=demand)


def test_unknown_passive_demand_is_held_and_unrankable():
    item=observe_passive(passive(), demand_evidence_class="unknown")
    assert item.state=="hold"
    assert item.expected_monthly_value_usd is None
    assert "demand_unproven" in item.reasons
    assert item.action_enabled is False


def test_queue_prefers_permitted_positive_task_without_enabling_action():
    q=build_observation_queue([task()], [passive()], capabilities=CapabilityProfile({"extract"}))
    assert q[0].source_type=="task"
    assert q[0].state=="accept_dry_run"
    assert q[0].expected_margin_usd > 0
    assert all(x.dry_run_only and not x.action_enabled for x in q)


def test_observed_passive_economics_can_rank_but_not_publish():
    q=build_observation_queue([], [(passive(demand=2000,fixed=9),"settled_receipt"), passive()], capabilities=CapabilityProfile({"extract"}))
    assert q[0].state=="ready_for_observation"
    assert q[0].expected_monthly_value_usd > 0
    assert q[-1].expected_monthly_value_usd is None
    assert all(not x.action_enabled for x in q)


def test_rejected_task_stays_below_viable_task():
    bad=("payanagent", {"id":"bad","title":"captcha bypass","bounty_usd":100,"currency":"USD",
        "skills":["extract"],"observed_at":NOW,"metadata":dict(POLICY,estimated_input_tokens=100,
        estimated_output_tokens=100,estimated_duration_seconds=60,estimate_confidence=.9,external_cost_cap_usd=0)}, "open_paid_request")
    q=build_observation_queue([bad,task()], [], capabilities=CapabilityProfile({"extract"}))
    assert q[0].external_id=="t1"
    assert q[-1].state=="reject"
    assert "prohibited_task" in q[-1].reasons


def test_listing_task_is_held_even_when_unit_economics_positive():
    q=build_observation_queue([task(evidence="listing_only")],[],capabilities=CapabilityProfile({"extract"}))
    assert q[0].state=="hold"
    assert "open_paid_demand_unproven" in q[0].reasons
    assert q[0].evidence_strength==1


def test_passive_projection_requires_paid_utilization_evidence():
    held=observe_passive(passive(demand=2000),demand_evidence_class="listing_only")
    ready=observe_passive(passive(demand=2000),demand_evidence_class="settled_receipt")
    assert held.state=="hold" and "paid_utilization_unproven" in held.reasons
    assert ready.state=="ready_for_observation" and ready.paid_utilization_proven


def test_audit_export_explains_queue_without_enabling_action():
    q=build_observation_queue([task(),task(task_id="t2", evidence="listing_only")],
        [(passive(demand=2000),"settled_receipt"), passive()], capabilities=CapabilityProfile({"extract"}))
    audit=audit_export(q,generated_at="2026-08-19T04:00:00+00:00")
    assert audit["counts"]=={"accepted":2,"held":2,"rejected":0}
    assert audit["reason_counts"]["demand_unproven"]==1
    assert audit["evidence_counts"]=={"listing_only":1,"open_paid_request":1,"settled_receipt":1,"unknown":1}
    assert audit["paid_utilization_proven_count"]==1
    assert audit["open_paid_demand_proven_count"]==1
    assert audit["dry_run_only"] is True and audit["action_enabled"] is False
