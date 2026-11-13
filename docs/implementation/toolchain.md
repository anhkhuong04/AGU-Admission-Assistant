# Foundation toolchain — 2026-11-13

Phạm vi local foundation theo [plan](../superpowers/plans/2026-11-08-foundation.md). `uv.lock` và `package-lock.json` là nguồn dependency resolution; không dùng một số version trong docs làm lockfile thay thế.

| Thành phần | Quan sát / lựa chọn |
|---|---|
| OS local | Windows, PowerShell; Git 2.46.2.windows.1 |
| Python / uv | 3.13.2 / 0.12.21; root uv workspace, shared `agu-backend` và `agu-api` |
| API / schema | FastAPI 0.162.5, Pydantic 2.14.3; uvicorn factory |
| Persistence | SQLAlchemy 2.0.57, psycopg 3.3.9, Alembic 1.20.1 |
| Python QA | pytest 9.2.0, Ruff 0.17.5, mypy 1.20.2, HTTPX2 2.16.0 cho Starlette TestClient |
| Node / npm | 22.18.0 / 10.9.3; npm workspaces, không pnpm/Turborepo |
| Web | Next.js 16.4.6, React/ReactDOM 19.3.1; TypeScript strict, ESLint 10.14.0, Prettier 3.6.2 |
| Database local | PostgreSQL 17.8, vector 0.8.1, pg_trgm 1.6; image tag + immutable digest trong Compose |
| Docker | Client/server 29.1.3; project riêng `agu-foundation`, loopback port 55432, volume `agu-foundation_agu_db` |
| CI | Ubuntu jobs backend/web/secrets; action SHAs pin theo upstream tags; dependency installs locked |

Next yêu cầu Node tối thiểu 20.9 theo [official installation](https://nextjs.org/docs/app/getting-started/installation); workspace chọn Node 22 đang có và đã chạy build. Root uv workspace theo [official workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/). pgvector image theo [upstream Docker guidance](https://github.com/pgvector/pgvector#docker). Chưa kiểm tra Docling/OCR trên Python 3.13: parser spike phải xác minh compatibility/weights/license trước khi thêm dependency, không suy ra từ foundation pass.

## Commands và environment

Quickstart ở [README](../../README.md); các lệnh CI ở [workflow](../../.github/workflows/ci.yml). Root `.env.example` là mẫu local, **không tự nạp** trong uv/Alembic. Compose dùng `--env-file .env.example` hoặc shell overrides; Python nhận DATABASE_URL/TEST_DATABASE_URL qua shell. Không log URL hoặc dump environment trong API. API health không dùng DB/provider và chỉ là liveness, không chứng minh DB readiness.

`API_ORIGIN` là server-side Next rewrite target, mặc định `http://127.0.0.1:8108`; thay nó trước `npm run build` khi dùng production build. Không tạo NEXT_PUBLIC secrets. Anonymous sessions/admin OIDC chưa triển khai. AI budget example bằng 0 và không có provider adapter/code path trong milestone này; đây chưa phải bằng chứng concurrent budget enforcement.

Migration authoring: `uv run --locked alembic -c infra/migrations/alembic.ini revision --autogenerate -m "describe change"`; review migration trước apply. Template hỗ trợ forward-only revisions; `downgrade` cố ý từ chối. Khôi phục backup/retention policy production chưa triển khai. Migrations không tạo schema qua ORM `create_all`.

Optional browser smoke: `uv run --with playwright python scripts/smoke_foundation.py --browser --browser-channel msedge` trên Windows có Edge. Với Chromium bundled, bỏ channel và cài browser tương ứng trước. Playwright là diagnostic tool tạm thời, không dependency runtime/CI bắt buộc. Script tạo screenshots và logs trong `.local/smoke`, không commit; HTTP smoke không cần browser dependency.

## Dependency exceptions cần theo dõi

`npm audit` ngày 2026-11-13 báo **10 moderate, 0 high/critical**, trong nhánh tooling lint qua minimatch; `npm audit --omit=dev --audit-level=moderate` báo 0 vulnerabilities. Advisory [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249) liên quan globparts amplification; audit đề xuất thay major/downgrade tooling, chưa áp dụng tự động. Next lint config còn kéo ESLint 9.39.5 transitive deprecated dù direct ESLint là 10.14.0. Owner: maintainer; review lại trước **2026-11-20**, và trước nhận repo/config không tin cậy hoặc mở staging. CI chặn high/critical; không coi exception này là G3 security approval.

Không có known vulnerability được pip-audit báo tại lần kiểm tra; editable workspace packages được skip bởi advisory lookup, vẫn phải review source/tests. Kết quả audit phụ thuộc database advisory tại thời điểm chạy, không chứng minh an toàn tuyệt đối.
