import unittest
from mcp_benchmark import normalize_text, json_stats, csv_profile, DEFAULT_MODELS, run_suite

class MCPBenchmarkTests(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text({"text":" a  b\n c "})["text"], "a b c")

    def test_json_stats(self):
        r=json_stats({"value":{"a":[1,2]}})
        self.assertEqual(r["leaves"],2)
        self.assertGreater(r["nodes"],r["leaves"])

    def test_csv_profile(self):
        r=csv_profile({"csv":"a,b\n1,2\n3\n"})
        self.assertEqual(r["rows"],2)
        self.assertEqual(r["ragged_rows"],1)

    def test_positive_unit_contribution(self):
        for model in DEFAULT_MODELS.values():
            self.assertGreater(model.contribution_per_call,0)
            self.assertEqual(model.break_even_calls(),0)

    def test_suite(self):
        self.assertEqual(len(run_suite()),3)

if __name__ == "__main__":
    unittest.main()
