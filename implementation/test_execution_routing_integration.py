from datetime import datetime, timezone

from evaluator import CapabilityProfile
from execution_routing_integration import (
    build_routed_task_queue,
    observe_and_route_task,
    routed_task_record,
)
from resource_router import default_backend_families

NOW = datetime.now(timezone.utc).isoformat()
POLICY = dict(
    rights_status="confirmed",
    tos_status="confirmed",
    automation_allowed="allowed",
    source_data_permission="confirmed",
)


def task(task_id="t1", bounty=5.0, *, skills=None, title="extract data", evidence="open_paid_request",
         routing_economics=None):
    payload = {
        "id": task_id,
        "title": title,
        "bounty_usd": bounty,
        "currency": "USD",
        "skills": skills or ["extract"],
        "observed_at": NOW,
        "metadata": dict(
            POLICY,
            estimated_input_tokens=1000,
            estimated_output_tokens=1000,
            estimated_duration_seconds=120,
            estimate_confidence=.9,
            external_cost_cap_usd=0,
        ),
    }
    if routing_economics is not None:
        payload["routing_economics"] = routing_economics
    return "payanagent", payload, evidence


def test_open_permitted_task_routes_to_cheapest_eligible_backend():
    platform, payload, evidence = task()
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class=evidence,
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.upstream_gate_passed is True
    assert result.state == "route_dry_run"
    assert result.selected_backend_id == "python_local"
    assert result.routing_decision is not None
    assert result.routing_decision.execution_enabled is False
    assert result.task_economics.gross_payout_usd == 5.0


def test_high_bounty_prohibited_task_never_reaches_router():
    platform, payload, evidence = task(task_id="bad", bounty=1000, title="spam automation")
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class=evidence,
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "reject"
    assert "prohibited_task" in result.reasons
    assert result.upstream_gate_passed is False
    assert result.routing_decision is None
    assert result.selected_backend_id is None


def test_unsupported_capability_never_becomes_routable_because_backend_is_cheap():
    platform, payload, evidence = task(task_id="unsupported", skills=["translate"])
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class=evidence,
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "reject"
    assert "unsupported_capability" in result.reasons
    assert result.routing_decision is None


def test_listing_only_positive_economics_stays_held_before_router():
    platform, payload, _ = task(task_id="listing", bounty=100)
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class="listing_only",
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.state == "hold"
    assert "open_paid_demand_unproven" in result.reasons
    assert result.upstream_gate_passed is False
    assert result.routing_decision is None


def test_explicit_payment_risk_can_turn_upstream_accept_into_routing_hold():
    platform, payload, evidence = task(
        task_id="risky",
        bounty=5,
        routing_economics={
            "acceptance_probability": 0.10,
            "dispute_probability": 0.10,
            "nonpayment_probability": 0.10,
        },
    )
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class=evidence,
        capabilities=CapabilityProfile({"extract"}),
    )
    assert result.upstream_state == "accept_dry_run"
    assert result.upstream_gate_passed is True
    assert result.state == "hold"
    assert "resource_route_unavailable" in result.reasons
    assert result.routing_decision is not None
    assert result.selected_backend_id is None


def test_subscription_support_resource_is_visible_but_not_selectable_as_free_api():
    subscription_only = tuple(
        backend for backend in default_backend_families()
        if backend.backend_id == "subscription_assistant"
    )
    platform, payload, evidence = task(task_id="sub")
    result = observe_and_route_task(
        platform, payload,
        demand_evidence_class=evidence,
        capabilities=CapabilityProfile({"extract"}),
        backends=subscription_only,
    )
    assert result.state == "hold"
    quote = result.routing_decision.quotes[0]
    assert quote.backend_id == "subscription_assistant"
    assert "no_autonomous_programmatic_execution_path" in quote.planning_reasons
    assert result.selected_backend_id is None


def test_combined_record_remains_inert_even_when_route_exists():
    q = build_routed_task_queue(
        [task(task_id="good"), task(task_id="held", evidence="listing_only")],
        capabilities=CapabilityProfile({"extract"}),
    )
    assert q[0].state == "route_dry_run"
    assert q[1].state == "hold"
    record = routed_task_record(q[0])
    assert record["dry_run_only"] is True
    assert record["execution_enabled"] is False
    assert record["network_enabled"] is False
    assert record["value_movement_enabled"] is False
    assert record["routing_decision"]["selected_backend_id"] == "python_local"
