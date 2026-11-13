# Foundation execution record — 2026-11-13

## Scope và authorization

User yêu cầu thực hiện [foundation plan](../superpowers/plans/2026-11-08-foundation.md), commit/push đầu lên `https://github.com/anhkhuong04/AGU-Admission-Assistant.git`. Scope này thay điều kiện chờ G0 và cấm push trong riêng plan; [00 §9](../00-baseline-decisions.md) giữ version 0.9/G0 Pending. Không có paid model call, cloud provisioning, public deployment, nguồn thật hoặc human knowledge approval.

Implemented: uv/npm workspaces, locked dependencies, Next development shell, API factory + health, same-origin API rewrite, PostgreSQL/pgvector/pg_trgm Compose và Alembic, immutable raw-version adapter, private typed curation packet, CI backend/web/secrets, local smoke harness. WP-01 nền tảng; WP-04/15 và WP-02 identity mới một phần. Không đánh dấu FR-08/16 hoặc AC sản phẩm hoàn thành toàn bộ từ slice này.

## Verification đã chạy tại local

| Check | Kết quả thực tế |
|---|---|
| `uv sync --locked` | Pass trên Windows Python 3.13.2 |
| `uv run --locked pytest -q` với dedicated migrated test DB | 32 pass: 2 health/surface, 8 raw identity/DB và 22 curation cases |
| Alembic upgrade head hai lần; `alembic check` | Pass, không schema drift; vector 0.8.1/pg_trgm 1.6 trên PostgreSQL 17.8 |
| Alembic revision --autogenerate ở temporary copy của migrations | Pass; template tạo revision mới, không sửa live migration chain |
| Ruff lint/format, mypy backend/API | Pass; source checks không thay security/AI eval |
| Clean `npm ci`, lint, typecheck, Prettier check, production build | Pass sau tái tạo lockfile sạch |
| `uv run --with playwright python scripts/smoke_foundation.py --browser --browser-channel msedge` | Pass: shell HTML và web → API health; Chromium Edge 375×812, 812×375, 1440×900, không horizontal overflow/pageerror, keyboard skip link và reduced motion |
| `pip-audit --local --skip-editable` | Không known vulnerabilities được báo; workspace editable source không có advisory registry |
| `npm audit --omit=dev --audit-level=moderate` | 0 vulnerabilities; full dev tree còn 10 moderate, 0 high/critical theo toolchain record |
| Gitleaks v8.30.0 dir scan, redacted | Không leaks được phát hiện; generated dependencies/local artifacts excluded, không là bảo đảm không còn mọi secret |

API health là liveness không gọi DB; DB boundary được kiểm tra riêng qua migrations/repository tests, không bịa health → DB/readiness integration. Web shell không tự gọi AI/DB, không có form nhập dữ liệu hay route serving facts. Raw storage keys trong tests là synthetic locators, không phải object-upload evidence.

Smoke screenshot/logs ở `.local/smoke` được xem local, không commit. Không kiểm định toàn WCAG hoặc usability từ ba viewports. Linux/GitHub Actions chỉ được coi pass sau khi có run kết thúc thật; workflow file riêng không là bằng chứng run thành công.

## Review, failures và corrections

- Health test fail vì module chưa tồn tại trước implementation; curation specialist quan sát cùng red→green; raw test fail vì sources module chưa có trước adapter. Sau triển khai, đầy đủ 32 tests pass.
- Root từng để hai npm install chồng nhau, làm tar/lockfile không hoàn chỉnh. Đã dừng mutation, cách ly generated modules/lock bị lỗi dưới `.local`, tái tạo install và xác minh `npm ci` sạch; không commit damaged artifacts. Không coi lần build trước sửa lock là clean-install evidence.
- Current Starlette TestClient cảnh báo HTTPX cũ: chuyển dev client sang HTTPX2 theo dependency hiện hành; lần chạy cuối không warning đó.
- Browser smoke đầu không có Chromium bundled revision phù hợp; dùng installed Edge channel hỗ trợ Playwright rồi chạy lại thành công. HTTP/proxy boundary đã pass trước browser check.
- Reviewer độc lập chạy lại 32 tests, không tìm material core correctness issue; phát hiện thiếu Alembic authoring template. Đã thêm và kiểm tra tạo revision ở temporary copy. Review này không bao phủ toàn CI/dependency/web.
- Design helper trước đây scan `.next`/`.local` artifacts như docs: thêm regression fixture (fail trước sửa), prune generated directories bằng `os.walk`; 7 helper tests pass. Sáu eval-helper tests vẫn là tests tooling, không AI benchmarks.

## Giới hạn và bước tiếp theo

Foundation không có parser/OCR, download/SSRF, object store, worker jobs, canonical fact schemas, public eligibility, serving bundle/safety journal, session/admin OIDC, RAG/LLM, eval datasets hoặc operations recovery. Không có corpus thật/source permissions hoặc G1–G4 pass. Budgets trong env mẫu bằng 0 nhưng concurrent budget enforcement chưa implement vì chưa có provider calls.

Giữ [toolchain dependency exception](toolchain.md) có owner/hạn; G1 queue ở [handoff](g1-inputs.md). Research/curation effort và Docling compatibility cần được đo trước mở rộng. Estimate 20–28h là planning assumption; lượt agent-assisted này không đo giờ công người nên không dùng để xác nhận năng suất hoặc lịch 320h.

## Fresh-source verification và Git delivery

Đã export 80 staged files bằng `git checkout-index` vào `.local/fresh-source`, không mang theo `.venv`, node_modules, env hoặc build outputs. Trên bản export: `uv sync --locked`, hai lần migration upgrade + drift check và 32 tests pass trên DB mới `agu_foundation_clean_test`; Ruff/mypy pass. `npm ci`, lint, typecheck, production build và HTTP smoke web → API đều pass. Đây là source-export proof local Windows; không thay bằng chứng Linux CI.

Design checker cuối: 25 Markdown files, 208 local links, 10 active design docs version 0.9, không structural issues; 7 design-helper và 6 eval-helper tests pass. Gitleaks scan cuối không phát hiện leak, `git diff --cached --check` không whitespace errors. Generated artifacts/`.env` không nằm trong staging; chỉ `.env.example` chứa local-only credentials.

Git target: branch `main`, origin `https://github.com/anhkhuong04/AGU-Admission-Assistant.git`, commit đầu gom docs/agent kit hiện có và foundation. Trạng thái remote delivery/Actions phải xem actual commit và [GitHub Actions](https://github.com/anhkhuong04/AGU-Admission-Assistant/actions), không suy ra từ file workflow hoặc pass local. Không force push, không tự mở cloud deployment.
