import dataclasses
import unittest
import i157_free_tier_ci_policy_gate as m


class Tests(unittest.TestCase):
    def test_current_public_repo_is_support_only(self):
        d = m.evaluate(m.current_github_public_repo_evidence())
        self.assertEqual(d.state, "SUPPORT_TESTING_ONLY")
        self.assertFalse(d.production_paid_task_eligible)
        self.assertTrue(d.development_testing_eligible)
        self.assertEqual(d.incremental_runner_price_usd, 0.0)
        self.assertFalse(d.capacity_claim_verified)

    def test_policy_widening_fails_closed(self):
        e = dataclasses.replace(
            m.current_github_public_repo_evidence(),
            generic_external_paid_task_execution_allowed=True,
        )
        d = m.evaluate(e)
        self.assertEqual(d.state, "FAIL_CLOSED")
        self.assertFalse(d.production_paid_task_eligible)

    def test_private_visibility_rejected_for_this_checkpoint(self):
        e = dataclasses.replace(
            m.current_github_public_repo_evidence(),
            repository_visibility="private",
        )
        with self.assertRaises(ValueError):
            m.evaluate(e)


if __name__ == "__main__":
    unittest.main()
