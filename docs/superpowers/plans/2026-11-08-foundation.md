# AGU Foundation Implementation Plan

> **Execution update 2026-11-13:** Người dùng đã giao triển khai foundation và initial commit/push. Root thực hiện trực tiếp, delegate curation và review độc lập theo AGENTS.md; Superpowers execution skills được dẫn trong bản plan ban đầu không còn cài trong phiên này. Kết quả và các sai khác được ghi tại [foundation results](../../implementation/foundation-results.md).

**Goal:** Tạo foundation local tái lập được, kiểm chứng raw version identity và typed curation packet bằng synthetic fixtures trước parser/RAG.

**Architecture:** Next shell và FastAPI presentation dùng một shared Python package; PostgreSQL local lưu source/raw identity. Typed curation packet là private validation artifact, chưa là serving bundle hoặc public evidence.

**Tech Stack:** Next.js/TypeScript, FastAPI/Pydantic, uv/pytest/Ruff/mypy, npm, PostgreSQL/pgvector/pg_trgm, SQLAlchemy/Alembic, Docker Compose. Versions được kiểm tra/pin khi thực hiện.

**Spec:** [07 Engineering](../../07-engineering-standards.md), [05 Data](../../05-data-architecture.md), [03 System](../../03-system-architecture.md), [08 Roadmap](../../08-implementation-roadmap.md); [readiness review](../../reviews/2026-11-08-implementation-readiness.md).

## Global Constraints

- Task implementation đã được giao ngày 2026-11-13; user cho phép bounded foundation trước G0 theo 00 §9. Không tự nâng version/approval toàn bundle.
- `MONTHLY_AI_BUDGET` và `DAILY_AI_BUDGET` mặc định 0. Không provider/model calls, paid provisioning hoặc public deploy; initial GitHub push đã được cấp quyền.
- Không raw chat persistence/logging, không facts AGU giả. Mọi fixture ghi `synthetic: true`; không secrets trong Git.
- Shared domain không import provider SDK/Docling/LlamaIndex/DB driver. Không triển khai parallel structure `backend/`/`frontend/` ngoài cấu trúc 07.
- Không mark FR hoàn thành chỉ từ foundations. Chưa có chat, public eligibility, auth, parser, worker queue, serving release hoặc G1 pass.

## Review Focus

- Fresh checkout thiếu implicit local state: Task 1 kiểm tra locked install/build/import trong CI.
- Health request làm lộ cấu hình: Task 1 assert response cố định, không secrets/environment dump.
- Cùng URL đổi bytes hoặc retry đồng thời: Task 2 test hai revisions và dedup bằng constraint, không overwrite.
- Unknown scope/date-only bị tự suy diễn: Task 3 round-trip giữ unknown và precision.
- Synthetic/draft/OCR warning bị hiểu là approved: Task 3 packet không có public-ready field, warnings không bị bỏ.

---

## Phạm vi, ownership và dự toán

Milestone đầu: **20–28 giờ developer** là ước lượng ban đầu, gồm review/fix, chưa gồm research, downloads lớn hoặc xử lý dependency incompatibility. Root giữ ownership, specialist data/reviewer theo scope; không spawn mọi role. User yêu cầu initial commit/push nên gom foundation và tài liệu hiện có vào commit đầu sau checks. Runtime version được kiểm tra/pin tại execution.

### Task 1 — Reproducible web/API foundation (6–8 giờ)

**Traceability:** WP-01, khởi đầu WP-13; NFR/engineering, chưa có FR chat hoàn thành.

**Files:** Create `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`, `.env.example`, `package.json`, `package-lock.json`, `apps/web/package.json`, `apps/web/tsconfig.json`, `apps/web/app/layout.tsx`, `apps/web/app/page.tsx`, `services/api/src/agu_api/main.py`, `packages/backend/pyproject.toml`, `packages/backend/src/agu_backend/__init__.py`, `tests/integration/test_health.py`, `.github/workflows/ci.yml`, `docs/implementation/toolchain.md`; modify `README.md`. Generator-owned Next lint/config files thuộc task này và phải ghi trong diff.

**Interfaces:** `agu_api.main.create_app() -> FastAPI`; `GET /api/v1/health` trả HTTP 200, JSON đúng `{"status":"ok"}`; không DB/provider dependency. Root uv workspace đóng gói API/shared package; root npm workspace cho `apps/web`; scripts `lint`, `typecheck`, `build` chạy trên web. Chọn mypy cho Python, không thêm checker thứ hai.

- [ ] Kiểm tra G0/task scope; `git init` local, bỏ qua env/secrets/build outputs; giữ review/archive hiện có. Không xóa các thư mục rỗng chỉ để dọn workspace.
- [ ] Kiểm tra runtime/package compatibility, bootstrap tối thiểu để test runner import được API. Ghi versions và pin lockfiles; `.env.example` chỉ placeholders, AI budgets bằng 0.
- [ ] Viết `test_health_returns_only_status`: TestClient gọi endpoint, assert 200 và exact JSON ở interface; gọi hai lần không thay đổi. Chạy `uv run pytest tests/integration/test_health.py -q`, quan sát fail vì route chưa implement.
- [ ] Implement health factory và web shell ghi rõ môi trường development, không có chat giả hoặc số liệu tuyển sinh. API config không in environment hoặc request body.
- [ ] CI dùng locked installs. Chạy `uv sync --locked`, `uv run pytest tests/integration/test_health.py -q`, `uv run ruff check .`, `uv run mypy packages/backend/src services/api/src`, `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`. Expected: tất cả exit 0; build không cần provider/DB secrets. Đây là lệnh **dự kiến**, chỉ có hiệu lực sau scaffold này.
- [ ] Ghi actual results và local run commands vào README/toolchain; review diff/secrets rồi commit các file thuộc task.

### Task 2 — PostgreSQL và immutable raw identity (6–8 giờ)

**Traceability:** WP-04, phần nền WP-02; hỗ trợ FR-08, AC-10. Không crawler, download URL hoặc raw object store implementation ở task này.

**Files:** Create `infra/compose.yaml`, `infra/migrations/alembic.ini`, `infra/migrations/env.py`, `infra/migrations/versions/0001_source_raw_identity.py`, `packages/backend/src/agu_backend/sources/models.py`, `packages/backend/src/agu_backend/sources/repository.py`, `tests/integration/test_raw_identity.py`; modify root Python lock/config, CI và toolchain record.

**Interfaces:** `record_raw_version(source_id: UUID, sha256: str, storage_key: str, retrieved_at: datetime) -> UUID` trong repository adapter. `source` giữ canonical URL; `raw_version` giữ FK/source, checksum, storage key, UTC retrieval timestamp; unique `(source_id, sha256)`. Storage keys trong test chỉ là fixture locators, không xác nhận object thật đã upload. Không update raw row khi retry. Migration bật `vector` và `pg_trgm`; chưa chọn embedding dimensions/model.

- [ ] Viết tests trên dedicated test DB: same source+checksum retry trả cùng ID; changed checksum trả ID khác và row cũ không đổi; hai concurrent retries chỉ có một revision; retrieval time naive bị reject; extensions hiện diện. Chạy để quan sát fail trước implementation.
- [ ] Pin PostgreSQL/pgvector image đã kiểm tra compatibility trong Compose, bind local loopback, không dùng production credentials. Thêm migration/repository parameterized SQL và transaction conflict handling; không giữ DB transaction qua network call.
- [ ] Chạy `docker compose -f infra/compose.yaml up -d db`, `uv run alembic -c infra/migrations/alembic.ini upgrade head`, `uv run pytest tests/integration/test_raw_identity.py -q`. Expected tests pass trên DB test mới; chạy `upgrade head` lần hai không đổi revision. Test harness phải từ chối DB không mang tên test để tránh cleanup nhầm.
- [ ] CI tạo DB isolated và chạy cùng migration/tests. Chạy lại checks Task 1; ghi kết quả rồi commit. Không dùng `down -v` như default cleanup hoặc reset một DB chưa xác minh.

### Task 3 — Private typed curation packet (4–6 giờ)

**Traceability:** phần WP-15, chuẩn bị FR-16; hỗ trợ AC-06/18/19/23, chưa implement public eligibility của chúng.

**Files:** Create `packages/backend/src/agu_backend/knowledge/curation_packet.py`, `tests/fixtures/synthetic/curation-packet.json`, `tests/unit/test_curation_packet.py`; dùng [curation packet reference](../../../.agents/skills/agu-curate-knowledge/references/curation-packet.md).

**Interfaces:** Pydantic `CurationPacket` chứa `synthetic: bool`, `raw_version_id: UUID`, `academic_year: int | None`, `program_scope: Literal['all','specific','unknown']`, `program_ids: list[str]`, `review_state: Literal['draft','in_review','approved','rejected']`, `quality_warnings: list[str]`, `facts: list[FactDraft]`. `FactDraft` chứa `key: str`, `value: str`, `value_type: Literal['text','number','date','code']`, `source_locator: str`, `date_precision: Literal['date','datetime'] | None`. Đây là interchange DTO tối thiểu, chưa phải schema canonical đầy đủ của 05; approval enum nhập liệu không cấp quyền serving và không có endpoint nhận approval.

- [ ] Viết tests: unknown scope không sinh program IDs/year; specific thiếu IDs bị reject; all/unknown kèm IDs bị reject; date-only `2026-12-01` giữ nguyên và không thành midnight; fixture draft có `ocr_table_warning` giữ warning sau JSON round-trip; extra `public_ready: true` bị reject. Chạy `uv run pytest tests/unit/test_curation_packet.py -q`, quan sát fail khi DTO chưa có.
- [ ] Implement DTO validation, forbid extra fields; fixture synthetic không gắn AGU hoặc human approval. Không có suy luận program/year từ URL/clock hoặc tự chuyển approved khi parse thành công.
- [ ] Chạy test trên và Ruff/mypy, full integration suite Task 1/2. Expected pass; reviewer đối chiếu 05 và reference, ghi phần contract còn thiếu trước production; commit.

### Task 4 — Foundation evidence và handoff G1 (4–6 giờ)

**Traceability:** WP-01/04/15 partial; chuẩn bị WP-02/03/06/18. Task nghiệm thu, không viết tests mới chỉ để mirror code.

**Files:** Create `docs/implementation/foundation-results.md`, `docs/implementation/g1-inputs.md`; modify README với actual run commands và trạng thái implementation đúng phạm vi. Không đổi gate sang Passed nếu evidence chưa đủ.

- [ ] Thử locked install/build/migration/tests ở checkout hoặc môi trường sạch tương đương, ghi khác biệt Windows/CI. Chạy các commands Tasks 1–3; chỉ ghi pass khi có output thực. Kiểm tra synthetic packet không được route nào trả như public answer.
- [ ] Ghi source intake template trong g1-inputs: official URL/owner, allowed use, checksum/retrieval date, year/program/round, task coverage, table/OCR/footnote risks, reviewer và freshness owner; chưa điền dữ kiện AGU khi chưa xác minh nguồn.
- [ ] Lập task kế tiếp 2–8 giờ/task: allowlisted download/SSRF+size checks; representative parser/IR spike; manual verified facts; applicability/conflict/release policy prototype; dev labels. Mỗi task map FR/AC/files/checks theo 08. Raw storage adapter và worker jobs nằm trong các task kế tiếp, không giả đã có từ Task 2.
- [ ] Đối chiếu actual effort với 20–28 giờ và ghi dependency failures/risks; chạy design checker, review evidence và commit. Báo foundation Done hoặc còn thiếu theo kết quả, G1/G2 vẫn chưa đạt.

## Workstream song song ngoài milestone code

PO/operator tổ chức research 5–8 người và quyền sử dụng corpus 15–30 tài liệu; developer lập coverage cho 3–5 tác vụ. Không tự nhắn người tham gia. G1 cần parser QA, manual facts, labels và review prototype theo 08; foundation này không thay toàn bộ G1. Trước UI feature code, review wireframes theo 06. Trước model tests, chốt budget/provider data permission rồi lập plan G2 theo 04.

## Plan self-review

Execution summary 2026-11-13 (chi tiết/commands trong foundation results):

- [x] Task 1: locked scaffold + health + web shell và CI definition, local checks pass.
- [x] Task 2: raw identity migration/repository, retry/concurrency/immutability tests pass.
- [x] Task 3: private curation DTO/fixture, 22 unit cases pass.
- [x] Task 4: source export sạch, DB mới, install/build/smoke và G1 handoff đã kiểm tra.

Các checkbox chi tiết ở trên được giữ như breakdown gốc; summary này ghi mức hoàn thành foundation local, không ghi product gate hay hosted CI pass. Commit/push theo scope user mới thay per-task commits của plan gốc.

Plan chỉ bao phủ foundation, không tuyên bố bao phủ toàn FR P0. Health/raw identity/packet có interfaces và behavior checks; các rủi ro trong Review Focus có task sở hữu. Domain DTO tách DB adapter; không nhầm raw checksums với stored object proof hoặc packet approval với eligibility. Không tạo model/vector dimension/OIDC decisions trước gate thích hợp. Commands/results thực tế xem foundation results; checkbox cũ là task breakdown, không tự suy ra product acceptance từ chúng.
