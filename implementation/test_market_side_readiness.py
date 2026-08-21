from market_side_readiness import build_market_side_readiness_packet


def compliance(ready=True):
    return {
        "bridge_state": "ready_for_human_decision" if ready else "blocked_by_nonreproducible_or_unbound_evidence",
        "human_decision_requested": ready,
        "compliance_review_bridge_sha256": "a" * 64,
        "exact_scope_sha256": "b" * 64,
        "exact_scope": {"method":"GET","required_environment":"production","request_count":1,"credentials_allowed":False,"action_enabled":False,"target_fingerprint":"payan-public-feed"},
    }


def route(ready=True):
    return {"state":"rerouted_dry_run" if ready else "hold","selected_backend_after":"python_local" if ready else None,"history_tip_hash":"c"*64,"materialization_hash":"d"*64,"execution_enabled":False,"network_enabled":False,"value_movement_enabled":False}


def test_ready_packet_is_review_only_and_inert():
    p=build_market_side_readiness_packet(compliance(),route(),candidate="PayanAgent",built_at_utc="2026-08-21T14:53:00Z")
    assert p["checkpoint_state"]=="ready_for_human_review_only"
    assert p["single_observation_needed"]["request_count"]==1
    assert p["current_resource_route"]["selected_backend_id"]=="python_local"
    assert p["authorization_granted"] is False and p["network_enabled"] is False and p["value_movement_enabled"] is False


def test_compliance_hold_fails_closed():
    p=build_market_side_readiness_packet(compliance(False),route(),candidate="PayanAgent",built_at_utc="2026-08-21T14:53:00Z")
    assert p["checkpoint_state"]=="blocked_before_human_review"
    assert "source_compliance_not_ready" in p["unresolved_gates"]


def test_resource_hold_fails_closed():
    p=build_market_side_readiness_packet(compliance(),route(False),candidate="PayanAgent",built_at_utc="2026-08-21T14:53:00Z")
    assert p["checkpoint_state"]=="blocked_before_human_review"
    assert "current_resource_route_not_ready" in p["unresolved_gates"]


def test_scope_widening_is_blocked():
    c=compliance(); c["exact_scope"]["request_count"]=2
    p=build_market_side_readiness_packet(c,route(),candidate="PayanAgent",built_at_utc="2026-08-21T14:53:00Z")
    assert "exact_scope_not_single_anonymous_read_only_get" in p["unresolved_gates"]


def test_packet_never_claims_market_economics_measured():
    p=build_market_side_readiness_packet(compliance(),route(),candidate="PayanAgent",built_at_utc="2026-08-21T14:53:00Z")
    assert "real_market_demand_fill_acceptance_payment_economics_unmeasured" in p["unresolved_gates"]
    assert p["packet_is_authorization"] is False
