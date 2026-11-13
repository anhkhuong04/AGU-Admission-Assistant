"""Tests for aggregate arithmetic and invalid-input handling, not AI quality."""

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("summarize_eval.py")


class AggregateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.is_file():
            return
        spec = importlib.util.spec_from_file_location("agu_eval_summary", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def summarize(self, payload):
        self.assertTrue(SCRIPT.is_file(), "Aggregate summarizer is not implemented")
        return self.module.summarize(payload)

    def test_full_evidence_recall_and_citation_coverage_have_separate_denominators(self):
        report = self.summarize({"counts": {"answerable_cases": 100, "answer_correct_cases": 97, "false_abstention_cases": 3, "retrieval_cases": 60, "all_groups_top5_cases": 53, "any_group_top5_cases": 58, "material_claims": 240, "claims_with_supporting_citation": 236, "citation_pairs": 260, "supported_citation_pairs": 255, "critical_errors": 1}, "metadata": {"synthetic": True, "holdout_independent": False}})
        self.assertAlmostEqual(report["metrics"]["evidence_set_recall_at_5"]["fraction"], 53 / 60)
        self.assertAlmostEqual(report["metrics"]["citation_support"]["fraction"], 255 / 260)
        self.assertAlmostEqual(report["metrics"]["material_citation_coverage"]["fraction"], 236 / 240)
        self.assertIn("holdout_not_independent", report["warnings"])
        self.assertIn("critical_errors_present", report["warnings"])
        self.assertFalse(report["can_approve_release"])

    def test_zero_or_missing_denominator_is_unknown_instead_of_a_pass(self):
        report = self.summarize({"counts": {"retrieval_cases": 0, "all_groups_top5_cases": 0}})
        self.assertIsNone(report["metrics"]["evidence_set_recall_at_5"]["fraction"])
        self.assertIsNone(report["metrics"]["answer_accuracy"]["fraction"])
        self.assertIn("runtime_config_id", report["missing_artifacts"])
        self.assertIn("holdout_independence_not_established", report["warnings"])

    def test_inconsistent_subset_counts_are_reported(self):
        report = self.summarize({"counts": {"answerable_cases": 10, "answer_correct_cases": 9, "false_abstention_cases": 2, "retrieval_cases": 5, "all_groups_top5_cases": 4, "any_group_top5_cases": 3}})
        self.assertTrue(any("answer_correct_cases + false_abstention_cases" in item for item in report["consistency_errors"]))
        self.assertTrue(any("all_groups_top5_cases" in item for item in report["consistency_errors"]))
        self.assertFalse(report["can_approve_release"])

    def test_negative_boolean_and_noninteger_counts_are_rejected(self):
        self.assertTrue(SCRIPT.is_file(), "Aggregate summarizer is not implemented")
        for value in (-1, True, 1.5, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.module.summarize({"counts": {"answerable_cases": value}})

    def test_even_perfect_aggregates_are_diagnostic_only(self):
        report = self.summarize({"counts": {"answerable_cases": 10, "answer_correct_cases": 10, "critical_errors": 0}, "metadata": {"synthetic": False, "holdout_independent": True, "dataset_version": "d1", "knowledge_release_id": "r1", "index_version_id": "i1", "runtime_config_id": "c1"}})
        self.assertFalse(report["can_approve_release"])
        self.assertEqual(report["result_type"], "aggregate_diagnostic")

    def test_covered_claims_require_at_least_as_many_supporting_pairs(self):
        report = self.summarize({"counts": {"material_claims": 10, "claims_with_supporting_citation": 10, "citation_pairs": 10, "supported_citation_pairs": 0}})
        self.assertTrue(any("claims_with_supporting_citation" in item and "supported_citation_pairs" in item for item in report["consistency_errors"]))


if __name__ == "__main__":
    unittest.main()
