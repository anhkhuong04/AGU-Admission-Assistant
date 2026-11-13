---
name: agu-sync-design
description: Use when AGU requirements, ADRs, API/data contracts, priorities, baseline status or roadmap dependencies change. Applies to design synchronization, not ordinary copy edits.
---

# AGU design synchronization

Keep a design change reviewable across its actual consumers. Repository policy remains in [AGENTS.md](../../../AGENTS.md); decisions and ownership remain in [00](../../../docs/00-baseline-decisions.md).

## Change map

| Change | Read/update when affected |
|---|---|
| Scope/priority | 01 product, 02 FR/BR/AC, 08 work packages |
| API/claim/SSE | 03 contract, 04 answer policy, 06 states, 07 checks |
| Evidence/facts/validity/release/privacy | 04 policy, 05 data, 02 AC, 03 serving, 08 gates |
| Stack | ADR-001, 00 decision record, 03 deployment, 07 bootstrap |
| Approval/version | 00 record and active-document metadata; keep historical reviews intact |

Find the affected identifiers first; read the sections that own them rather than loading every document. An authorized policy change may revise an invariant: record the decision and update consumers together. A wording change needs only the relevant files.

## Read-only structural check

From the workspace root:

```powershell
python -B .agents/skills/agu-sync-design/scripts/check_design.py --root .
```

Exit 0 means structural checks passed; 1 reports document issues; 2 means an input/root error. The script checks local links outside code fences, JSON examples, active version alignment, requirement IDs and work-package dependencies. It does not judge design meaning, run application tests or record approval.

Report the decision/change, affected IDs/files, structural command/result, semantic consistency findings and remaining runtime evidence. Do not promote pending product gates from a clean lint result.
