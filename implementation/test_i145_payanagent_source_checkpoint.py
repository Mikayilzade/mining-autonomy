from i145_payanagent_source_checkpoint import checkpoint, current_facts
from i142_market_source_evidence_gate import assess_source


def test_current_payanagent_facts_resolve_six_of_seven_required_fields():
    decision = assess_source("PayanAgent", current_facts())
    assert decision.state == "HOLD"
    assert decision.required_fields_present == (
        "task_list_read_auth_requirement",
        "task_detail_read_auth_requirement",
        "platform_fee_rate",
        "payout_to_worker_rate",
        "rate_limit_or_minimum_interval",
        "automation_permission",
    )
    assert decision.blockers == ("missing_required_fact:geography_access_rule",)
    assert decision.conflicting_fields == ()


def test_checkpoint_never_promotes_silence_on_geography_to_permission():
    body = checkpoint()
    assert body["state"] == "HOLD"
    assert body["expected_remaining_blocker"] in body["blockers"]
    assert body["production_market_endpoint_called"] is False
    assert body["credentials_used"] is False
    assert body["registration_performed"] is False
    assert body["spend_or_value_movement"] is False
