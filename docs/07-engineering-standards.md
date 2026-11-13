# AGU Admission Assistant — Engineering Standards

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Phạm vi | Frontend/API/worker, schema, AI eval, CI và vận hành |
| Approval | Theo [00](00-baseline-decisions.md); bounded foundation có evidence riêng, chưa đạt product gates |

## 1. Principles và repository

Implement documented contracts; vertical slices; immutable evidence; least privilege; observable without raw sensitive payloads; small abstractions at real boundaries. Không coi AI-generated code/output là bằng chứng hoàn thành.

Proposed structure khi bắt đầu implementation:

```text
AGENTS.md / README.md
docs/                         # 00–08, decisions, reviews
apps/web/                     # Next.js public/admin UI
services/api/                 # FastAPI presentation/application
services/worker/              # Job runner, parser adapters
packages/backend/             # Shared Python domain/application code
packages/contracts/           # Optional generated OpenAPI TS client
infra/                        # Compose/deploy/migrations/runbooks
tests/fixtures/               # Labeled synthetic + permitted real fixtures
tests/integration/ / e2e/ / evals/
.github/workflows/
```

Shared domain/application là một package được API/worker dùng, không copy code hai lần. Foundation đã có web/API/shared package/migrations; worker và serving chưa triển khai. Runtime/dependencies được lock và ghi tại [toolchain record](implementation/toolchain.md); không dùng version trong ví dụ như đã chọn thực tế.

Nguồn chuẩn: [00](00-baseline-decisions.md) decisions/status, [02](02-prd.md) FR/BR/AC, [03](03-system-architecture.md) API/serving, [04](04-ai-rag-architecture.md) AI/eval, [05](05-data-architecture.md) data/operations/privacy, [06](06-ui-ux-specification.md) UX, [08](08-implementation-roadmap.md) gates.

## 2. Backend/worker standards

Python có type hints/Pydantic tại boundary; Ruff và một type checker (mypy hoặc pyright chọn ở bootstrap), pytest. Domain không import provider SDK/Docling/LlamaIndex/DB driver; DTO adapters rõ. Không framework orchestration bắt buộc chỉ vì xuất hiện trong ADR.

Async cho I/O phù hợp; CPU/OCR ở worker. Repository/accessors parameterized; không text-to-SQL. Clock, providers, storage, eligibility/policy và repositories inject được để test offline. Explicit error types, không except-pass. Alembic forward migrations, FKs/checks/indexes và restore plan; timestamps UTC-aware, deadline date-only giữ precision nguồn. User-facing timezone Việt Nam, không suy academic_year từ clock.

DB jobs dùng stage identity/checkpoint/lease/fencing; transaction claim ngắn, không giữ lock qua OCR/provider call. Budget reservation transactional, retries không double-charge local accounting hoặc duplicate artifacts. Không log payload trong exception handler.

## 3. Frontend/contracts standards

TypeScript strict, ESLint/Prettier; không any để né contract. Components: UI primitives/domain/page orchestration. Dùng một authoritative OpenAPI contract; generate client khi ổn định, không hand-maintain hai enum/status khác nhau.

Same-origin /api, server session/RBAC. UI không tin role/kind/publication state do client tự gửi. Semantic HTML, labelled controls, source dialog focus, keyboard/IME/mobile states theo 06. Raw model markdown/HTML/URLs không được render trực tiếp. Claim rendering từ typed server response, không tự infer thêm số liệu.

SSE qua fetch parser: started/progress/answer/completed/error; không delta P0. Stop/disconnect không đánh dấu completed và không auto replay generation. Nonstreaming/SSE share một application service; contract tests phải chứng minh answer equivalence và no early content.

## 4. Data/release invariants cần test

- Raw versions/reviewed revisions bất biến; edit tạo revision và invalidates approval/eval liên quan.
- Public eligibility là intersection manifest/review/quality/applicability/safety/freshness, không một document status.
- Block units/facts đồng thời trên dense/lexical/parent/SQL/citation rendering.
- Partial supersession không làm mất unaffected rules, không phục hồi old values sau rollback.
- Bundle chọn đúng embedder/index/runtime/facts; candidate chưa pass không activate.
- Global overrides tăng policy epoch, final commit chặn answer khi policy đổi trước điểm phát hành.
- Query use latest_for_year vẫn áp current-use exclusions cho năm historical; không point-in-time reconstruction P0.
- Restore cách ly/đóng public AI, đối soát safety journal mới hơn backup, reapply TTL/overrides/exclusions/freshness trước mở traffic; không hứa zero-byte retroactive revocation.
- Activate khác effective cutover; test trước/sau cutover và request đi qua cutover, không loại deadline tương lai hoặc mọi historical evidence bằng now filter.

## 5. AI/evaluation standards

Prompt/runtime/verifier có IDs/version, output schema và explicit limits. Citation ID validation khác semantic support. Critical values/rules dùng typed templates/cards; narrative summary cần verifier đã kiểm định, nếu chưa thì extractive mode. Không để judge override human conflict hoặc tự sửa gold labels.

Theo protocol 04: dev ≥60, holdout ≥200 với phân nhóm/rubric/critical suite; không tune theo held-out outputs rồi gọi là độc lập. Report raw counts, failed runs và uncertainty. Candidate eval trước activation; targeted affected topics + toàn critical, full evaluation khi thay AI/parser/chunking hoặc coverage lớn. Expected results không đồng nghĩa commands đã chạy.

## 6. Verification matrix

| Level | Cases bắt buộc khi liên quan | Gate |
|---|---|---|
| Unit | Scope all/specific/unknown, year precedence/IME parse, date precision, fact schema, RRF, citation mapping, budget bounds | Offline deterministic rules pass |
| Integration | DB migrations, lease/fencing/crash recovery, reservations concurrent, source revisions, bundle/revocation/rollback/cutover | AC-03/04/06/11/12/19/21/24/26/27 pass |
| Contract | Status/reason schema, claims/citations, SSE final answer, cancel/errors/ownership | Không raw/early answer, không schema divergence |
| E2E | Ask→source; admin QA→candidate eval→activate→revoke/rollback; restart/reset/expiry | Happy/error/authorization paths có evidence |
| AI eval | Answer/citation/recall/abstention/conflicts/critical/adversarial | Protocol 04, report đúng frozen config |
| Security/privacy | RBAC/MFA/session binding, CSRF/XSS/SSRF/redirect/private IP, upload sandbox, provider payload PII, logging/APM, rate/budget | Không critical leakage/control failure |
| Ops/usability | Restore/current exclusions, stale/incident drill, mobile/keyboard/screen reader, task research | G3/G4 evidence và owner |

Không ép coverage % tổng hoặc viết test chỉ phản chiếu implementation. Chọn behavior/risk meaningful; tests tương ứng với thay đổi. Documentation-only dùng link/schema-example/consistency review, không tạo application tests giả khi chưa có code.

## 7. CI/CD và change management

PR: format/lint/types/unit/integration/contract/migration + secret/dependency scans theo modules thay đổi. AI/data changes chạy eval phù hợp. Findings critical không được waive để public pilot; noncritical exceptions có owner/lý do/hạn xử lý.

Staging: riêng DB/object store/credentials, synthetic hoặc permitted corpus, no production PII. Migration job một lần, backward-compatible cho rollout; smoke/restore/rollback trước production. Runtime artifacts và release manifests checksummed; không promote config mới bằng mutable model alias âm thầm.

PRD change cập nhật FR/AC + roadmap; data/model/prompt change cập nhật eval/manifest; core architecture change cập nhật ADR. Accepted decision chỉ sửa qua version/change record, không thay lịch sử để che một benchmark fail. Production secrets chỉ server/secret manager, không repo/front-end/prompt/logs.

## 8. Agent task workflow

Mỗi task cần Goal, FR/AC IDs, source docs, scope/non-goals, files/interfaces, acceptance, allowed dependencies và review focus. Đọc AGENTS và sections liên quan; không đọc lịch sử/archive như requirement hiện hành.

1. Kiểm tra quyền/phạm vi đã có và readiness; giải quyết routine choices trong design, không hỏi lại việc đã được giao.
2. Thực hiện slice nhỏ có thể review; không scaffold/provision app khi task chỉ yêu cầu documents.
3. Giữ code/schema/contracts/docs cùng nhau; không thêm framework/service P1 để làm demo P0.
4. Chạy checks/eval đúng phạm vi; ghi command, exit/result và limitations thực tế.
5. Báo files/decisions/verification/known gaps; chưa đủ evidence thì không gắn Done/Gate pass.
6. Nếu thật sự cần quyền dữ liệu, chi tiêu, destructive action hoặc đổi scope chưa được cấp, làm phần chuẩn bị reviewable trước rồi nêu chính xác quyết định cần PO.

## 9. Definition of Done và review focus

Đúng FR/AC; lỗi/timeout/empty/auth/cancel states có xử lý; contract/schema/migration/docs nhất quán; không secrets/PII/fake AGU data; checks có kết quả thật; logging/budget/rollback phù hợp. Không commit/publish/deploy khi chưa có scope tương ứng.

Review tập trung vào: wrong year/round/unknown; bảng lỗi và partial supersession; races giữa release/revoke/answer; IDOR/session/cancel; provider outage/unknown usage; backup resurrecting blocked facts; semantic verifier false pass; cost/latency trade-off. Không dùng demo trôi chảy thay bằng chứng.
