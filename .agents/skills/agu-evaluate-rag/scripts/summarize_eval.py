"""Summarize supplied evaluation counters; does not run models or approve a release."""

import argparse
import json
from pathlib import Path
import sys


METRICS = {
    "answer_accuracy": ("answer_correct_cases", "answerable_cases"),
    "false_abstention": ("false_abstention_cases", "answerable_cases"),
    "correct_abstention": ("correct_abstention_cases", "unanswerable_cases"),
    "claim_factual_accuracy": ("correct_material_claims", "material_claims"),
    "citation_support": ("supported_citation_pairs", "citation_pairs"),
    "material_citation_coverage": ("claims_with_supporting_citation", "material_claims"),
    "evidence_set_recall_at_5": ("all_groups_top5_cases", "retrieval_cases"),
    "any_group_hit_rate_at_5_diagnostic": ("any_group_top5_cases", "retrieval_cases"),
    "clarification_status_accuracy": ("clarification_correct_cases", "clarification_cases"),
    "conflict_status_accuracy": ("conflict_correct_cases", "conflict_cases"),
    "out_of_scope_status_accuracy": ("out_of_scope_correct_cases", "out_of_scope_cases"),
    "adversarial_safety": ("adversarial_passed_cases", "adversarial_cases"),
}
KNOWN_COUNTS = {field for pair in METRICS.values() for field in pair} | {"critical_errors"}
ARTIFACTS = ("dataset_version", "knowledge_release_id", "index_version_id", "runtime_config_id", "raw_results_ref", "gold_evidence_ref", "critical_suite_ref", "human_audit_ref", "performance_report_ref", "cost_report_ref")


def summarize(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("counts"), dict):
        raise ValueError("Input must be an object containing a counts object")
    counts = payload["counts"]
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be an object")
    for key, value in counts.items():
        if key not in KNOWN_COUNTS:
            raise ValueError(f"Unknown counter: {key}")
        if type(value) is not int or value < 0:
            raise ValueError(f"{key} must be a nonnegative integer, not bool/string/float")
    for key in ("synthetic", "holdout_independent"):
        if key in metadata and type(metadata[key]) is not bool:
            raise ValueError(f"{key} must be boolean when supplied")
    metrics, errors = {}, []
    for name, (numerator, denominator) in METRICS.items():
        n, d = counts.get(numerator), counts.get(denominator)
        if n is not None and d is not None and n > d:
            errors.append(f"{numerator} exceeds {denominator}")
        fraction = n / d if n is not None and d is not None and d > 0 else None
        metrics[name] = {"numerator": n, "denominator": d, "fraction": fraction, "percent": round(fraction * 100, 2) if fraction is not None else None}
    for left, right, total in (("answer_correct_cases", "false_abstention_cases", "answerable_cases"),):
        if all(key in counts for key in (left, right, total)) and counts[left] + counts[right] > counts[total]:
            errors.append(f"{left} + {right} exceeds {total}")
    if all(key in counts for key in ("all_groups_top5_cases", "any_group_top5_cases")) and counts["all_groups_top5_cases"] > counts["any_group_top5_cases"]:
        errors.append("all_groups_top5_cases exceeds any_group_top5_cases")
    if all(key in counts for key in ("claims_with_supporting_citation", "supported_citation_pairs")) and counts["claims_with_supporting_citation"] > counts["supported_citation_pairs"]:
        errors.append("claims_with_supporting_citation exceeds supported_citation_pairs")
    warnings = []
    if metadata.get("holdout_independent") is False:
        warnings.append("holdout_not_independent")
    elif metadata.get("holdout_independent") is not True:
        warnings.append("holdout_independence_not_established")
    if metadata.get("synthetic") is True:
        warnings.append("synthetic_fixture_not_project_benchmark")
    elif "synthetic" not in metadata:
        warnings.append("data_origin_not_established")
    if counts.get("critical_errors", 0) > 0:
        warnings.append("critical_errors_present")
    if "critical_errors" not in counts:
        warnings.append("critical_error_count_unknown")
    missing = [key for key in ARTIFACTS if not isinstance(metadata.get(key), str) or not metadata[key].strip()]
    return {
        "result_type": "aggregate_diagnostic",
        "can_approve_release": False,
        "metrics": metrics,
        "critical_errors": counts.get("critical_errors"),
        "consistency_errors": errors,
        "warnings": warnings,
        "missing_artifacts": missing,
        "artifact_references_are_not_verified": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON with counts and optional metadata")
    args = parser.parse_args()
    try:
        if args.input.stat().st_size > 1_000_000:
            raise ValueError("Aggregate JSON exceeds 1 MB; provide counters, not raw transcripts")
        report = summarize(json.loads(args.input.read_text(encoding="utf-8-sig")))
    except (ValueError, OSError) as error:
        print(json.dumps({"input_error": str(error)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 1 if report["consistency_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
