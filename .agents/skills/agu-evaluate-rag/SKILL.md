---
name: agu-evaluate-rag
description: Use when AGU retrieval, answer, citation or abstention evaluation results need analysis, or a candidate RAG configuration needs a quality-gate recommendation. Not for general application tests.
---

# AGU evaluation reference

Use the current [04 evaluation protocol](../../../docs/04-ai-rag-architecture.md), especially dataset groups, metric definitions and release discipline. Numeric targets belong there, not in this skill. Read [00](../../../docs/00-baseline-decisions.md) only for gate/approval ownership.

## Inputs and optional arithmetic helper

Collect the run's dataset, source release, index/runtime IDs, raw case/claim/citation rows and audit/performance/cost references. Missing evidence stays missing; an aggregate summary is not a qualifying benchmark.

For supplied counters, use [aggregate-example.json](references/aggregate-example.json) as the input shape. It is an intentionally failing **synthetic** example, not a project result. From workspace root:

```powershell
python -B .agents/skills/agu-evaluate-rag/scripts/summarize_eval.py path/to/aggregate.json
```

The helper does arithmetic only. Exit 0 means summary produced, 1 inconsistent counters, 2 invalid input. Zero/missing denominators yield unknown metrics. Any-group hit rate is diagnostic, distinct from full evidence-set Recall@5. It does not verify referenced artifacts, judge semantic support, apply thresholds or approve a release.

## Analysis output

Return: recommendation and blocking evidence; metric numerator/denominator versus current protocol; critical errors and dataset independence; missing/unverifiable artifacts; next experiment or repair and the gate it could inform. Distinguish reported aggregates from verified raw results. If no run exists, produce an evaluation plan and required inputs instead of a scorecard.
