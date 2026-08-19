from passive_service import HostingTier, PassiveServiceOffer, evaluate_passive_offer, execute_local_capability


def offer(**kw):
    d=dict(platform="mcpize", capability="normalize_text", price_per_call_usd=.01,
           creator_share=.80, variable_cost_per_call_usd=.00001,
           hosting=HostingTier("free",0,250000))
    d.update(kw)
    return PassiveServiceOffer(**d)


def test_unproven_demand_holds_even_with_positive_unit_margin():
    d=evaluate_passive_offer(offer())
    assert d.decision=="hold"
    assert "demand_unproven" in d.reject_reasons
    assert d.contribution_per_call_usd==.00799
    assert d.publication_enabled is False


def test_observed_positive_demand_can_be_ready_for_observation():
    d=evaluate_passive_offer(offer(demand_calls_per_month=100))
    assert d.decision=="ready_for_observation"
    assert d.projected_net_month_usd==.799
    assert d.dry_run_only is True


def test_paid_hosting_break_even_and_negative_projection():
    d=evaluate_passive_offer(offer(hosting=HostingTier("starter",9), demand_calls_per_month=100))
    assert d.break_even_calls_month==1127
    assert "negative_projected_month" in d.reject_reasons


def test_capacity_and_policy_gates():
    d=evaluate_passive_offer(offer(demand_calls_per_month=250001,policy_confirmed=False))
    assert "hosting_capacity_exceeded" in d.reject_reasons
    assert "policy_evidence_insufficient" in d.reject_reasons


def test_local_execution_is_bounded_registry_only():
    assert execute_local_capability("normalize_text",{"text":" a  b "})["text"]=="a b"
    try:
        execute_local_capability("unknown",{})
        assert False
    except ValueError:
        pass
