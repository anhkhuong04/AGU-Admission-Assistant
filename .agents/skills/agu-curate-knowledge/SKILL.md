---
name: agu-curate-knowledge
description: Use when AGU source documents, OCR tables, typed facts or rule cards need a review handoff, especially mixed program scope or partially superseding notices. Not for answering public admissions questions.
---

# AGU knowledge curation reference

Prepare a reviewable handoff from source material, preserving what is known and what still needs a human decision. The result is a curation proposal, not approved knowledge.

Read [05](../../../docs/05-data-architecture.md) for identity/IR, applicability, typed facts and temporal rules. Read [02](../../../docs/02-prd.md) only for the affected FR/AC. Use [curation-packet.md](references/curation-packet.md) for the handoff fields; it is a work-artifact contract, not a database migration.

For actual source files, inspect the original locations needed to verify critical cells/conditions. Hash real bytes only when available; fixture labels are not verified checksums. Identify independently reviewable units and dependent context before proposing retention, replacement or blocking. A new notice cannot fill unknown scope in an old source without evidence.

The packet names sources/locations, known values and unknown applicability, proposed units/facts/rule cards, affected uses, scoped supersession/conflicts, review questions and executable acceptance expectations. Link evidence when present; otherwise keep fields unknown and state what the reviewer must inspect.

Public eligibility, activation and human approval remain governed by the current project documents and user authorization. A private handoff can be completed while those remain pending. Reuse existing parser/domain contracts when implementing an authorized slice; do not create a second schema from this reference.
