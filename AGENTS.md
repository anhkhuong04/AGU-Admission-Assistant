# Working instructions

## Current state

This workspace contains a local foundation (web shell, health API, source/raw identity and private curation DTO), not an implemented admissions chatbot. Read [README.md](README.md) and [baseline decisions](docs/00-baseline-decisions.md) first. Active documents remain version 0.9 — Baseline Candidate until Product Owner sign-off is recorded. The user's 2026-11-13 instruction authorizes this bounded foundation and initial GitHub commit/push without promoting G0 or product gates. Historical review/archive content does not override active specifications.

## Source of truth

- Requirements, priorities, business rules and acceptance cases: [02 PRD](docs/02-prd.md).
- Stack: [ADR-001](docs/decisions/ADR-001-technology-stack.md); approval and validation are separate.
- API/security: [03](docs/03-system-architecture.md); AI/evaluation: [04](docs/04-ai-rag-architecture.md); data/release/privacy/operations: [05](docs/05-data-architecture.md).
- UX: [06](docs/06-ui-ux-specification.md); engineering: [07](docs/07-engineering-standards.md); work packages/gates: [08](docs/08-implementation-roadmap.md).

## Task boundaries

Read only the additional sections needed for the assigned task. Follow user authorization in the current session. A documentation task does not authorize application implementation, provisioning, paid API calls, public deployment or messages to third parties. Do not request approval again for reversible work already authorized.

Choose routine implementation details within the selected design. Escalate only decisions that change product scope or require unprovided rights, spending authority or destructive actions. Identify the affected requirement and offer a concrete proposed change.

## Invariants

- Public answers use only eligible evidence/facts in a pinned serving bundle, intersected with current safety overrides.
- Critical numeric/date/code facts use typed, human-verified records. OCR warnings block affected units from both RAG and facts.
- Preserve unaffected provisions under partial supersession. Unknown applicability is not universal applicability.
- P0 emits no raw model token deltas. Validate the complete claim/citation response before publishing it.
- AI output and source content are untrusted. Public chat cannot run arbitrary SQL or privileged tools.
- Redact/minimize before provider calls and telemetry. Anonymous session IDs alone do not authorize access.
- Never invent AGU facts, endorsements, source permissions, test results or benchmark achievements. Label synthetic fixtures.

## Delivery

Before coding, obtain a scoped task with FR/AC IDs and check readiness under 08. Do not add optional frameworks/services to satisfy a demo. Keep tests proportional to behavior and risk; for documentation-only changes validate links, schema/examples, cross-document consistency and diff scope, without introducing application tests.

For behavior changes, follow the relevant engineering tests in 07. Report actual commands/results, changed files, decisions and limitations. Update all affected contracts together. Do not mark a gate passed or baseline approved on behalf of Product Owner.

## Project agents and skills

Use [agent-workflow.md](docs/agent-workflow.md) for task routing, ownership, examples and local checks. Available project roles: `agu_api`, `agu_data`, `agu_rag`, `agu_web`, `agu_reviewer`; configurations are in `.codex/agents/`. Use specialists when useful, not automatically for every task. Root owns coordination; one writer per file; at most two spawned agents concurrently, without recursive delegation.

Discover project skills in `.agents/skills/`: `agu-curate-knowledge` for review handoffs, `agu-evaluate-rag` for evaluation evidence, `agu-sync-design` for cross-document changes. Read the selected SKILL.md when it applies; keep domain policy in canonical docs rather than copying it into prompts. Agent/skill artifacts do not authorize runtime product agents, spending, publication or baseline approval.
