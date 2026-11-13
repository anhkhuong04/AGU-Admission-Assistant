# ADR-001 — Technology Stack for AGU Admission Assistant

| Thuộc tính | Giá trị |
|---|---|
| ADR / revision | 001 / 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Status | Proposed for baseline approval — stack selected for bounded PoC |
| Decision owner | Product Owner |
| Validation | Pending; không có benchmark đạt |
| Phạm vi | Thiết kế MVP, không cam kết provider/chi phí/deployment |

## 1. Context và cách chấp nhận

Một developer + AI coding agent xây website độc lập, chưa có integration AGU. Nhu cầu gồm PDF/HTML tiếng Việt, facts chính xác, citation, review/release/rollback, privacy và vận hành gọn. Không có căn cứ coi một stack tối ưu tuyệt đối; lựa chọn ưu tiên độ đơn giản phù hợp workload dự kiến và khả năng thay parser/model.

ADR phân biệt **design acceptance** và **validation** theo [00](../00-baseline-decisions.md). PO có thể Accepted for design ở G0 trước benchmark; PoC G1/G2 mới quyết định parser mode/model/retrieval config đủ điều kiện pilot. Không yêu cầu benchmark được tạo bằng một scaffold phải có trước khi cho phép scaffold. Mọi code/provisioning vẫn theo task được giao và ngân sách được cấp, không tự bắt đầu từ yêu cầu chỉnh tài liệu.

## 2. Lựa chọn được chọn

| Layer | Lựa chọn / quyết định |
|---|---|
| Frontend | Next.js + React + TypeScript strict; same-origin /api proxy |
| UI | CSS semantic tokens + accessible primitives; academic minimal, không khóa Fluent UI package |
| API/domain | Python + FastAPI, Pydantic/OpenAPI, modular monolith |
| Data | Managed PostgreSQL + pgvector + pg_trgm; SQL migrations qua Alembic |
| Search | Exact vector baseline; exact/alias/normalized lexical + RRF là target hybrid; ANN sau đo |
| Knowledge accuracy | Typed verified facts/aliases/rule cards tối thiểu P0, manual curation được |
| Parsing | Docling adapter cho PDF; HTML parser; DOCX fallback; domain-owned canonical IR |
| AI orchestration | Application services sở hữu router/retrieval/eligibility/citations; LlamaIndex optional utility |
| Models | Provider adapters; embedder/generator/verifier chọn qua G2, không fine-tune |
| Reranker | Optional, chỉ bật nếu đạt contribution/latency/budget rule ở 04 |
| Delivery | Buffered validated response P0, SSE progress + final answer, không raw token delta |
| Jobs | Python worker riêng; PostgreSQL queue/lease/heartbeat/fencing/idempotency |
| Raw files | Private S3-compatible storage, immutable/checksummed; không public mirror mặc định |
| Anonymous state | Single API instance, memory TTL context; không persisted transcript/Redis P0 |
| Admin identity | Managed OIDC + MFA + server RBAC; không custom password/auth system |
| Tests/deploy | pytest/Playwright/CI/offline eval; managed web/API/worker/DB, provider chọn sau |

Runtime/package versions chọn stable supported releases tương thích tại bootstrap, lock và ghi vào implementation record; ADR không bịa số phiên bản chưa được thử. Parser/OCR models có license/weights/version riêng, phải ghi nhận.

## 3. Vì sao chọn và trade-offs

Python phù hợp ingestion/AI ecosystem; TypeScript/Next.js phục vụ web responsive và static pages. Hai ecosystem có overhead CI/contracts; giữ generated OpenAPI client và một backend domain. PostgreSQL thống nhất relational facts/release metadata/vector giảm service count; exact search tránh ANN tuning sớm, không bảo đảm chất lượng semantic relevance.

Docling có hỗ trợ các định dạng liên quan nhưng lỗi bảng/OCR vẫn phải QA; fallback/manual curation quan trọng hơn cố tự động toàn corpus. LlamaIndex không sở hữu publication, data model hoặc truth: chỉ thêm nếu utility tiết kiệm code và không làm mất provenance/filter control.

DB jobs giảm vận hành nhưng phải thử crash/reclaim/fencing; không giữ transaction trong OCR. Single-instance session context dễ quản trị privacy nhưng restart mất phiên; đây là trade-off được công bố cho pilot. Nếu cần nhiều API replicas, làm ADR session/rate-limit store dựa trên số đo.

Buffer + verifier có thể chậm hơn raw streaming; đổi metric sang validated answer latency phù hợp lời hứa tin cậy. Narrative summary chỉ bật sau kiểm định verifier; templates/excerpts là cấu hình baseline được phép.

## 4. Alternatives và điều kiện xem lại

| Alternative | Vì sao chưa chọn | Xem lại khi |
|---|---|---|
| Chỉ Next.js backend | Giảm ngôn ngữ nhưng pipeline parser/OCR Python vẫn cần process; dễ chia domain hai nơi | Workload chủ yếu structured/FAQ và đội TypeScript chịu trách nhiệm toàn hệ |
| Spring Boot backend | Thêm overhead tích hợp ingestion Python cho nguồn lực hiện tại | Có đội Java tiếp quản/yêu cầu tổ chức cụ thể |
| Qdrant riêng | Thêm service/metadata synchronization chưa có scale evidence | Exact/pgvector không đạt filtered recall/latency/cost sau tuning hợp lý |
| OpenSearch | Nặng vận hành cho corpus pilot | Lexical tiếng Việt không đạt task-level relevance bằng giải pháp hiện tại |
| Celery/Redis ngay P0 | Thêm queue/cache vận hành | DB jobs/session concurrency không đạt reliability/load gates |
| GraphRAG/agent tự do | Extraction/tool/cost/safety phức tạp, chưa có task cần | Multi-hop/tool use được chứng minh không giải quyết bằng SQL + retrieval |
| Fine-tuning | Không thay quản trị quy định biến đổi | Có task ổn định và labeled dataset phù hợp, eval riêng |
| Raw streaming | Có thể đưa claim chưa kiểm tra tới người dùng | Claim-level verification/atomic emission được chứng minh ở P1 |

Đánh giá lại không có nghĩa tự thêm service/framework; cần impact analysis, benchmark và ADR change record.

## 5. Validation plan và adoption gates

G1: 15–30 tài liệu thật có quyền sử dụng, coverage 3–5 tasks, mixed-program/critical cells QA, schema/release prototype, dev labels. Chấp nhận parser theo từng loại; OCR mode không đạt thì curate thủ công hoặc giảm corpus, không giả OCR đã đúng.

G2: dev ≥60 và holdout ≥200 theo 04; so dense/hybrid/optional rerank, model candidates và summary/extractive mode. Đo quality, latency, failed calls, cost ingest/query, storage và configuration compatibility. Không khóa model theo demo chủ quan.

G3: mobile final-answer/citation UI, admin auth/review/candidate/activate/revoke, safe rollback/re-embedding, worker crash recovery, provider payload/privacy và restore. G4: public permission và operations coverage.

Nếu không đạt: dùng config đơn giản hơn trong boundary này nếu vẫn thỏa gates; thay parser/model qua adapter; scope cuts theo 08; thay core stack cần ADR revision/thay thế. Không sửa lặng lẽ quyết định đã Accepted for design. G0 acceptance không đổi các validation status Pending thành Passed.

## 6. Deliberately deferred

Hosting/provider/region, exact model/dimensions/OCR, mức chi tiêu, OIDC vendor, source rights và public branding nằm trong OD-01…OD-04 của 00. Budget mặc định 0 nên không có call trả phí tự phát. Các điều kiện này có owner và gate, không phải chỗ trống cho agent tự đoán.

## 7. Primary references

- [FastAPI background work](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat).
- [PostgreSQL SELECT/locking](https://www.postgresql.org/docs/current/sql-select.html).
- [pgvector filtering/index trade-offs](https://github.com/pgvector/pgvector#filtering).
- [Docling supported formats](https://docling-project.github.io/docling/usage/supported_formats/).
- [LlamaIndex ingestion API](https://developers.llamaindex.ai/python/framework-api-reference/ingestion/).
- [Next.js authentication](https://nextjs.org/docs/app/guides/authentication).

Các nguồn hỗ trợ khả năng kỹ thuật, không chứng minh product-market fit hoặc hiệu năng AGU. [00 decisions](../00-baseline-decisions.md) · [03 system](../03-system-architecture.md) · [04 AI/eval](../04-ai-rag-architecture.md) · [05 data](../05-data-architecture.md) · [08 roadmap](../08-implementation-roadmap.md).
