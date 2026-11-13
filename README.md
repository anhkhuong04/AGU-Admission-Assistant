# AGU Admission Assistant

Website độc lập hỗ trợ tra cứu tuyển sinh đại học chính quy Trường Đại học An Giang bằng thông tin có nguồn, đúng năm/đợt và có kiểm duyệt. Dự án chưa được AGU phê duyệt/bảo trợ; không xác nhận kết quả xét tuyển cá nhân.

**Trạng thái hiện tại:** đã có **local foundation**, thiết kế vẫn **0.9 — Baseline Candidate**. Có Next shell, FastAPI health, PostgreSQL raw identity và private curation DTO; chưa có chatbot/RAG, corpus thật hoặc public deployment. User đã giao bounded foundation và initial GitHub commit/push ngày 2026-11-13; G0/1.0 và product gates chưa được xác nhận. Xem [sổ quyết định](docs/00-baseline-decisions.md) và [kết quả foundation](docs/implementation/foundation-results.md).

## Đọc tài liệu

1. Nghiệp vụ: [01 Product Overview](docs/01-product-overview.md) → [02 PRD](docs/02-prd.md).
2. Kiến trúc/AI: [ADR-001](docs/decisions/ADR-001-technology-stack.md) → [03 System](docs/03-system-architecture.md) → [04 AI/RAG & Evaluation](docs/04-ai-rag-architecture.md) → [05 Data & Operations](docs/05-data-architecture.md).
3. Triển khai: [06 UX](docs/06-ui-ux-specification.md) → [07 Engineering](docs/07-engineering-standards.md) → [08 Roadmap](docs/08-implementation-roadmap.md).

Lựa chọn cho candidate: Next.js/TypeScript, FastAPI/Python, PostgreSQL/pgvector, worker riêng và Docling qua adapter. Facts tối thiểu ở P0; reranker và LlamaIndex không bắt buộc. Câu trả lời public được buffer và kiểm tra trước khi hiển thị.

Các lựa chọn model/provider và khả năng đạt quality/latency/cost phải qua PoC. Foundation không gọi provider hoặc cung cấp thông tin tuyển sinh.

## Chạy local

Yêu cầu: Python 3.13.2, uv 0.12.21, Node 22.18.0/npm 10.9.3 và Docker Compose. Versions/dependency caveats ở [toolchain](docs/implementation/toolchain.md).

```powershell
uv sync --locked
npm ci
docker compose --env-file .env.example -f infra/compose.yaml up -d --wait db
$env:DATABASE_URL='postgresql+psycopg://agu_local:agu_local_only@127.0.0.1:55432/agu_foundation_test'
uv run --locked alembic -c infra/migrations/alembic.ini upgrade head
```

Mở hai terminal ở root:

```powershell
# Terminal 1: API (port 8108)
uv run --locked uvicorn agu_api.main:create_app --factory --host 127.0.0.1 --port 8108
# Terminal 2: web
npm run dev
```

Web: `http://127.0.0.1:3000`. Health trực tiếp và qua web: `/api/v1/health` trả `{"status":"ok"}`. Chỉ shell development và health được mở, không nhận câu hỏi/hồ sơ hoặc expose curation packet. Không dùng local DB credentials ở staging/production. `.env.example` chỉ làm mẫu; shell Python không tự nạp file env. Đổi port/credentials thì cập nhật cả Compose, DATABASE_URL và TEST_DATABASE_URL.

```powershell
$env:TEST_DATABASE_URL=$env:DATABASE_URL
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check packages/backend services/api infra tests scripts
uv run --locked mypy packages/backend/src services/api/src
npm run lint
npm run typecheck
npm run format:check
npm run build
uv run --locked python scripts/smoke_foundation.py
```

Smoke dùng hai port riêng 8108/3108, yêu cầu dừng API local ở terminal 1 trước khi chạy; script chỉ dừng processes do nó tạo. DB tests yêu cầu tên DB kết thúc `_test`, dùng synthetic UUID riêng và không xóa dữ liệu có trước. `docker compose -f infra/compose.yaml stop db` dừng DB và giữ volume; không mặc định xóa volume. Xem [G1 handoff](docs/implementation/g1-inputs.md) cho bước tiếp theo.

## Review và baseline

- [Review thiết kế 0.1](docs/reviews/2026-11-08-initial-design-review.md).
- [Ma trận xử lý và kiểm tra candidate](docs/reviews/2026-11-08-baseline-resolution.md).
- [Đánh giá readiness triển khai](docs/reviews/2026-11-08-implementation-readiness.md) và [kế hoạch foundation](docs/superpowers/plans/2026-11-08-foundation.md).
- [Bản lưu nguồn 0.1](docs/reviews/archive/2026-11-08-design-v0.1.zip) để đối chiếu trước khi chỉnh, được tạo trước khi khởi tạo Git.
- Quy tắc cho coding agent: [AGENTS.md](AGENTS.md).
- Bộ 5 agent / 3 skill của dự án, routing và ví dụ dùng: [Agent workflow](docs/agent-workflow.md).

Phê duyệt 1.0 là phê duyệt thiết kế. Chạy thử, dùng dịch vụ trả phí và phát hành public có scope/gates riêng; không ghi nhận kết quả thử nghiệm khi chưa có bằng chứng.
