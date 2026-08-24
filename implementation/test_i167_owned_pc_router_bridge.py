import i167_owned_pc_router_bridge as i167


def complete_fixture():
    explicit = {
        "latency_seconds": 2.0,
        "reliability_probability": 0.99,
        "quality_acceptance_probability": 0.98,
        "max_parallelism": 4,
        "measured_available_hours_per_day": 8.0,
        "availability_source_ref": "local-observation:availability:2026-08-24",
        "energy_source_ref": "local-meter:joule-counter:2026-08-24",
        "tariff_usd_per_kwh": 0.08,
        "tariff_source_ref": "utility-bill:applicable-tariff:2026-08",
        "opportunity_cost_usd_per_hour": 0.12,
        "opportunity_cost_source_ref": "owner-declaration:pc-occupation:2026-08-24",
    }
    return {
        "gate": {"state": "REAL_EXTERNAL_EVIDENCE_ACCEPTED", "ownership_confirmation_supplied": True},
        "i165_result": {
            "state": "USER_PC_MATERIALIZED",
            "i162_packet": {
                "state": "USER_PC_PACKET_COMPLETE",
                "derived_energy_kwh_per_task": 0.0002,
                "explicit_measurements": explicit,
                "i159_evaluation": {"production_evidence_ready": True},
            },
        },
    }


def test_complete_chain_maps_only_measured_resource_facts():
    result = i167.build_bridge(complete_fixture())
    assert result.state == "ROUTER_RESOURCE_FACTS_READY"
    assert result.router_backend_patch["backend_id"] == "owned_pc"
    assert result.router_backend_patch["electricity_per_task_usd"] == 0.000016
    assert result.router_backend_patch["opportunity_cost_per_task_usd"] == round(0.12 * 2 / 3600, 12)
    assert result.backend_evidence_candidate["provenance_class"] == "i166_real_owned_pc_measurement_candidate"
    assert result.backend_evidence_candidate["current_reproducible"] is False
    assert result.backend_evidence_candidate["policy_evidence_current"] is False
    assert result.production_execution_enabled is False
    assert "real_task_payout_and_acceptance_criteria" in result.still_required_for_economic_test


def test_incomplete_i166_chain_fails_closed():
    result = i167.build_bridge({"gate": {"state": "PASS_BLOCKED"}, "i165_result": None})
    assert result.state == "PASS_BLOCKED"
    assert result.router_backend_patch == {}
    assert result.source_digest is None


def test_fixture_or_synthetic_provenance_is_rejected_again():
    raw = complete_fixture()
    raw["i165_result"]["i162_packet"]["explicit_measurements"]["energy_source_ref"] = "test-fixture:meter"
    result = i167.build_bridge(raw)
    assert result.state == "PASS_BLOCKED"
    assert any("energy_source_ref" in error for error in result.errors)
