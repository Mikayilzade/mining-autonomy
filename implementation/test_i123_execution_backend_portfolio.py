#!/usr/bin/env python3
from dataclasses import replace
import unittest

import i123_execution_backend_portfolio as p
from resource_router import TaskEconomics, default_backend_families


def backend(backends, backend_id):
    return next(x for x in backends if x.backend_id == backend_id)


def measured(b, **kwargs):
    return p.BackendEvidence(
        backend_id=b.backend_id,
        provenance_class=p.MEASURED,
        current_reproducible=True,
        non_synthetic=True,
        capacity_verified=True,
        policy_evidence_current=True,
        credentials_authorized=kwargs.get("credentials_authorized", not b.requires_credentials),
        spend_authorized=kwargs.get("spend_authorized", not b.requires_new_spend),
        infrastructure_authorized=kwargs.get(
            "infrastructure_authorized", b.family != "paid_vps_server"
        ),
        evidence_note="test measured evidence",
    )


class I123PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.backends = default_backend_families()
        self.task = TaskEconomics(
            task_id="paid",
            required_capabilities=frozenset({"extract", "validate"}),
            gross_payout_usd=2.0,
            platform_fee_rate=0.05,
            acceptance_probability=0.85,
            dispute_probability=0.05,
            nonpayment_probability=0.05,
            minimum_success_probability=0.90,
            minimum_expected_margin_usd=0.10,
            minimum_expected_margin_ratio=0.05,
        )

    def test_required_backend_families_exist(self):
        self.assertEqual(
            {x.backend_id for x in self.backends},
            {
                "python_local", "local_model", "subscription_assistant",
                "cheap_external_api", "strong_external_api", "free_tier_ci",
                "owned_pc", "future_paid_vps",
            },
        )

    def test_default_snapshot_is_planning_only(self):
        snap = p.current_snapshot()
        self.assertTrue(snap["synthetic_fixture"])
        self.assertFalse(snap["production_route_created"])
        self.assertFalse(snap["current_route_summary"]["eligible_non_synthetic_route_exists"])
        self.assertTrue(all(x["state"] == "hold" for x in snap["decisions"]))

    def test_deterministic_route_precedes_ai(self):
        py = backend(self.backends, "python_local")
        strong = backend(self.backends, "strong_external_api")
        evidence = (
            measured(py),
            measured(strong, credentials_authorized=True, spend_authorized=True),
        )
        decision = p.route_portfolio(self.task, (strong, py), evidence)
        self.assertEqual(decision.selected_backend_id, "python_local")
        self.assertEqual(decision.escalation_stage, "deterministic_first")

    def test_ai_escalates_only_if_deterministic_cannot_do_task(self):
        py = backend(self.backends, "python_local")
        strong = backend(self.backends, "strong_external_api")
        task = replace(self.task, required_capabilities=frozenset({"research"}))
        decision = p.route_portfolio(
            task,
            (py, strong),
            (measured(py), measured(strong, credentials_authorized=True, spend_authorized=True)),
        )
        self.assertEqual(decision.selected_backend_id, "strong_external_api")
        self.assertIn("ai_only_after", decision.escalation_stage)

    def test_ai_can_be_disallowed(self):
        strong = backend(self.backends, "strong_external_api")
        task = replace(self.task, required_capabilities=frozenset({"research"}))
        decision = p.route_portfolio(
            task,
            (strong,),
            (measured(strong, credentials_authorized=True, spend_authorized=True),),
            ai_allowed=False,
        )
        self.assertIsNone(decision.selected_backend_id)

    def test_subscription_never_becomes_programmatic_from_subscription_alone(self):
        sub = backend(self.backends, "subscription_assistant")
        blockers = p.production_blockers(sub, measured(sub))
        self.assertIn("no_autonomous_programmatic_path", blockers)
        self.assertEqual(sub.allocated_fixed_cost_per_task_usd(), 0.0)
        self.assertGreater(sub.marginal_cost_usd(), 0.0)

    def test_synthetic_or_planning_evidence_cannot_materialize_route(self):
        py = backend(self.backends, "python_local")
        current = next(x for x in p.current_backend_evidence() if x.backend_id == "python_local")
        blockers = p.production_blockers(py, current)
        self.assertIn("backend_not_measured_reproducible", blockers)
        self.assertIn("backend_evidence_synthetic", blockers)

    def test_paid_api_requires_credentials_and_spend_authorization(self):
        api = backend(self.backends, "cheap_external_api")
        ev = replace(
            measured(api, credentials_authorized=False, spend_authorized=False),
            credentials_authorized=False,
            spend_authorized=False,
        )
        blockers = p.production_blockers(api, ev)
        self.assertIn("credentials_not_authorized", blockers)
        self.assertIn("new_spend_not_authorized", blockers)

    def test_future_vps_requires_separate_infrastructure_authorization(self):
        vps = backend(self.backends, "future_paid_vps")
        ev = measured(
            vps,
            credentials_authorized=True,
            spend_authorized=True,
            infrastructure_authorized=False,
        )
        self.assertIn("infrastructure_not_authorized", p.production_blockers(vps, ev))

    def test_fixed_non_sunk_cost_needs_allocation_basis(self):
        vps = backend(self.backends, "future_paid_vps")
        self.assertIsNone(vps.allocated_fixed_cost_per_task_usd())
        self.assertIn("fixed_cost_allocation_basis_unknown", p.production_blockers(vps, measured(vps)))

    def test_quota_exhaustion_blocks_route(self):
        ci = backend(self.backends, "free_tier_ci")
        exhausted = replace(ci, currently_available=True, quota_units_remaining=0.0)
        self.assertIn("quota_insufficient", p.production_blockers(exhausted, measured(exhausted)))

    def test_quality_threshold_is_preserved_from_i048(self):
        py = backend(self.backends, "python_local")
        weak = replace(py, reliability_probability=0.5, quality_probability=0.5)
        q = p.portfolio_quotes(self.task, (weak,), (measured(weak),))[0]
        self.assertIn("success_probability_below_threshold", q.base_quote.planning_reasons)

    def test_negative_margin_is_preserved_from_i048(self):
        py = backend(self.backends, "python_local")
        expensive = replace(py, opportunity_cost_per_task_usd=10.0)
        q = p.portfolio_quotes(self.task, (expensive,), (measured(expensive),))[0]
        self.assertIn("insufficient_conservative_expected_margin", q.base_quote.planning_reasons)

    def test_payment_risk_reduces_expected_value(self):
        py = backend(self.backends, "python_local")
        safe = replace(self.task, acceptance_probability=1.0, dispute_probability=0.0, nonpayment_probability=0.0)
        risky = replace(self.task, acceptance_probability=0.5, dispute_probability=0.2, nonpayment_probability=0.2)
        safe_q = p.portfolio_quotes(safe, (py,), (measured(py),))[0]
        risky_q = p.portfolio_quotes(risky, (py,), (measured(py),))[0]
        self.assertGreater(safe_q.base_quote.expected_revenue_usd, risky_q.base_quote.expected_revenue_usd)

    def test_observation_and_paid_task_types_remain_separate(self):
        py = backend(self.backends, "python_local")
        ev = (measured(py),)
        obs = p.route_portfolio(self.task, (py,), ev, task_kind="observation")
        paid = p.route_portfolio(self.task, (py,), ev, task_kind="paid_task")
        self.assertEqual(obs.task_kind, "observation")
        self.assertEqual(paid.task_kind, "paid_task")

    def test_no_decision_enables_execution_or_value_movement(self):
        py = backend(self.backends, "python_local")
        d = p.route_portfolio(self.task, (py,), (measured(py),))
        self.assertFalse(d.production_execution_enabled)
        self.assertFalse(d.value_movement_enabled)


if __name__ == "__main__":
    unittest.main()
