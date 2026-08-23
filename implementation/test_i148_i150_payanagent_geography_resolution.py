from i148_payanagent_geography_resolution import branch_decision, local_access_contract, resolve


def test_i148_terms_clause_does_not_promote_geography_permission():
    r = resolve()
    assert r.state == "POLICY_CONTACT_OR_USER_LOCAL_ACCESS_REQUIRED"
    assert r.jurisdiction_legality_clause_found is True
    assert r.explicit_supported_country_rule_found is False
    assert r.explicit_global_access_rule_found is False
    assert r.explicit_azerbaijan_rule_found is False
    assert r.source_gate_state == "HOLD"
    assert r.source_gate_blockers == ("missing_required_fact:geography_access_rule",)
    assert r.production_market_endpoint_called is False
    assert r.spend_or_value_movement is False


def test_i149_local_access_contract_is_design_only_and_reachability_is_not_eligibility():
    c = local_access_contract()
    assert c.state == "DESIGN_ONLY_SEPARATE_AUTHORIZATION_REQUIRED"
    assert c.observation_enabled is False
    assert c.network_enabled is False
    assert c.credentials_enabled is False
    assert c.task_acceptance_enabled is False
    assert c.spend_enabled is False
    assert "treating_plain_http_200_as_proof_of_provider_country_eligibility" in c.forbidden
    assert "explicit policy evidence" in c.promotion_rule


def test_i150_stops_repeated_doc_search_without_reopening_discovery():
    d = branch_decision()
    assert d.active_source == "PayanAgent"
    assert d.state == "WAIT_FOR_POLICY_CONTACT_OR_SEPARATELY_AUTHORIZED_LOCAL_ACCESS"
    assert d.discovery_reopened is False
    assert d.observation_authorized is False
    assert "continue independent resource/runtime branch" in d.next_action


def test_i150_contact_evidence_triggers_reassessment_not_automatic_pass():
    d = branch_decision(contact_evidence_available=True)
    assert d.state == "REASSESS_WITH_EXPLICIT_PROVIDER_CONTACT_EVIDENCE"
    assert d.blockers == ("missing_required_fact:geography_access_rule",)
    assert d.observation_authorized is False
