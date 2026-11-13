"""Behavior checks for the read-only design linter; no application tests."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name("check_design.py")


class DesignCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("docs/00-baseline-decisions.md", "# Decisions\n\n| Version | 0.9 |\n")
        self.write("docs/02-prd.md", "# PRD\n\n| Version | 0.9 |\n\n| FR-01 | P0 | Chat |\n| AC-01 | A | B |\n")
        self.write("docs/08-implementation-roadmap.md", "# Roadmap\n\n| Version | 0.9 |\n\n| ID | Level | Deliverable | Dependency | Evidence |\n|---|---|---|---|---|\n| WP-01 | P0 | Setup | G0 | Check |\n| WP-02 | P0 | Data | WP-01 | Check |\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_check(self):
        return subprocess.run(
            [sys.executable, "-B", str(CHECKER), "--root", str(self.root)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_clean_workspace_does_not_require_application_or_fixed_id_counts(self):
        self.write("README.md", "[PRD](docs/02-prd.md)\n\n```md\n[example](does-not-exist.md)\n```\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report["structural_checks_passed"])
        self.assertTrue(report["semantic_review_required"])
        self.assertFalse(report["approval_recorded_by_checker"])

    def test_missing_link_and_duplicate_requirement_are_reported(self):
        self.write("README.md", "[Missing](docs/missing.md)\n")
        path = self.root / "docs/02-prd.md"
        path.write_text(path.read_text(encoding="utf-8") + "| FR-01 | P0 | Duplicate |\n", encoding="utf-8")
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
        codes = {item["code"] for item in json.loads(result.stdout)["issues"]}
        self.assertIn("missing_local_link", codes)
        self.assertIn("duplicate_requirement", codes)

    def test_generated_and_local_artifacts_are_not_design_inputs(self):
        for directory in (".local/checkout", "apps/web/.next", "node_modules", ".venv"):
            self.write(directory + "/README.md", "[Generated](missing-generated-file.md)\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(json.loads(result.stdout)["markdown_files"], 3)

    def test_shorthand_dependencies_are_expanded_and_cycles_fail(self):
        self.write("docs/08-implementation-roadmap.md", "# Roadmap\n\n| Version | 0.9 |\n\n| ID | Level | Deliverable | Dependency | Evidence |\n|---|---|---|---|---|\n| WP-01 | P0 | A | WP-02/03 | Check |\n| WP-02 | P0 | B | G0 | Check |\n| WP-03 | P0 | C | WP-01 | Check |\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
        codes = {item["code"] for item in json.loads(result.stdout)["issues"]}
        self.assertIn("dependency_cycle", codes)
        self.assertNotIn("unknown_work_package", codes)

    def test_invalid_json_and_version_drift_fail_without_modifying_sources(self):
        self.write("docs/03-system-architecture.md", '# Architecture\n\n| Version | 0.8 |\n\n```json\n{"broken": }\n```\n')
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
        codes = {item["code"] for item in json.loads(result.stdout)["issues"]}
        self.assertIn("version_mismatch", codes)
        self.assertIn("invalid_json", codes)
        after = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_missing_project_root_is_an_input_error(self):
        result = subprocess.run([sys.executable, "-B", str(CHECKER), "--root", str(self.root / "absent")], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 2, result.stderr or result.stdout)

    def test_requirement_shorthand_does_not_hide_unknown_ids(self):
        self.write("docs/03-system-architecture.md", "# Architecture\n\n| Version | 0.9 |\n\nAffected: FR-01/99 and AC-01.\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
        unknown = [item["detail"] for item in json.loads(result.stdout)["issues"] if item["code"] == "unknown_requirement"]
        self.assertIn("FR-99", unknown)
        self.assertNotIn("FR-01", unknown)


if __name__ == "__main__":
    unittest.main()
