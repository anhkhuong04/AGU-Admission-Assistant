# Curation handoff fields

This is a proposal format for a human reviewer/developer. It is not a persisted domain schema or a record of approval. Keep the packet proportional to the supplied source; tables or structured data are both suitable.

| Part | Content |
|---|---|
| Scope/identity | Synthetic or real; source URL/publisher/usage-review state; raw checksum and content/parser revision **only if actually known**; aliases labelled as local proposal IDs |
| Source locations | Original page/section/table/row/cell and required headers/footnotes; distinguish provided snippets from inspected original bytes |
| Unit proposals | Unit purpose, related context, program/year/round/method/audience known values and unknowns |
| Fact/rule proposals | Typed value + unit/basis/precision; conditions and exceptions; exact supporting locations; unresolved fields |
| Allowed/blocked uses | Separate private review from public evidence/facts; affected parents/dependent records; why blocked or reviewable |
| Change relation | Old/new target, field/topic, applicability, effective cutover, retained provisions; unresolved target/scope stays unresolved |
| Review decisions | Missing evidence, QA tasks, reviewer/actor not yet assigned, questions that change eligibility; no AI signature as human approval |
| Acceptance handoff | Relevant AC IDs, concrete input/expected behavior, tests proposed versus actually run, candidate/index/eval evidence still needed |

## One synthetic item

Source B explicitly states quota 120 for fixture major M/round R/full-time, effective 2026-12-01; the academic year and original cell location are not supplied.

```yaml
packet_type: curation_proposal
synthetic: true
proposal_alias: B-quota
system_record_id: null
source_location: null
fact_type: quota
value: 120
academic_year: null
known_scope:
  program_type: undergraduate_full_time
  major_alias: M
  round_alias: R
effective_date: '2026-12-01'
precision: date
review_status: pending
human_approval_actor: null
allowed_uses: [private_review]
blocked_uses: [public_retrieval, public_facts]
unresolved: [academic_year, original_cell_evidence, remaining_applicability, source_usage_review]
```

The scheduled date does not prove a year or present applicability. If A's quota table has mixed-program headers, B does not repair A's missing scope; retain unaffected conditions separately and propose no confirmed supersession target until the old scope is verified. Apply the current [05 temporal/review rules](../../../../docs/05-data-architecture.md), rather than treating this example as a universal source fact.
