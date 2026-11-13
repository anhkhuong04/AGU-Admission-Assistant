# Implementation Readiness Review — 2026-11-08

## Kết luận

**Đủ đặc tả để bắt đầu foundation và PoC theo task có phạm vi; chưa đủ bằng chứng để gọi MVP sẵn sàng hoặc phát hành.** Không cần mở rộng bộ tài liệu/agent/skill trước khi bắt đầu. Điều kiện mở implementation theo quy trình hiện tại là PO ghi nhận G0 và giao task triển khai; lần yêu cầu này là kiểm tra và lập kế hoạch, chưa phải lệnh xây app.

Baseline vẫn **0.9 — Baseline Candidate**. Không có chữ ký PO trong [00](../00-baseline-decisions.md); G1–G4 chưa chạy. Các thiếu hụt về corpus, model và runtime là đầu ra của các phase tiếp theo, không phải lý do yêu cầu thiết kế chứng minh benchmark trước khi cho phép PoC.

## Mức sẵn sàng và bằng chứng

| Mặt kiểm tra | Đánh giá | Căn cứ / việc còn lại |
|---|---|---|
| Product và scope | Đủ để giao task; utility chưa kiểm chứng | 01/02 xác định JTBD, P0/P1/P2, 25 FR và 27 AC; research G1 vẫn cần 5–8 người và chọn 3–5 tác vụ |
| Kiến trúc và governance | Đủ để implement từng slice; chưa được chạy thử | ADR/03–05 có boundary, typed facts, versioning, eligibility, partial supersession, bundle, revoke/cutover/restore; các race và invariants phải có tests thật |
| Engineering và roadmap | Đủ hướng dẫn khởi tạo | 07 có cấu trúc đích; 08 có 20 work packages và gates. Chưa có package manifests, lockfiles, migrations, CI hoặc app |
| Agent/skills | Đủ hỗ trợ phát triển | 5 role files, 3 skills, 2 offline helpers. Không thay reviewer nội dung, operator hoặc PO; không cần thêm vai trò trước task đầu tiên |
| Context | Có thể quản lý theo task | Nguồn chuẩn đã phân chia; không cần nạp tất cả docs/review/archive vào mỗi lượt. Độ đúng dưới context dài và năng suất agent chưa được đo |
| Máy local | Có tool nền tảng; compatibility chưa xác minh | Git, Python, Node/npm, uv và Docker có; Docker client/server trả version. Chưa chứng minh dependencies của app/Docling, pgvector hoặc browser build chạy được |
| Dữ liệu/eval | Chưa sẵn sàng cho G1/G2 | Chưa có corpus thật, source permissions record, coverage, human-reviewed facts hoặc gold dev/holdout. Synthetic helper samples không thay dữ liệu sản phẩm |
| UI | Có spec, chưa có prototype | Wireframe Home/Assistant/Admin Review + Release cần được review trước UI code theo 06 |
| Approval/vận hành | Chưa mở implementation/public gates | G0 chưa ký; budget, provider/region/OIDC và source/branding có OD owners, phải chốt trước hoạt động phụ thuộc |

## Kiểm tra thực tế trong lượt review này

Các lệnh dưới đây đã chạy tại workspace; không gọi model, không cài dependency hoặc khởi tạo app:

- `python -B .agents/skills/agu-sync-design/scripts/check_design.py --root .`: exit 0 trước khi thêm báo cáo, không structural issues; 10 tài liệu active, 25 FR/27 AC/16 BR/10 NFR và 20 work packages. Checker không xác nhận semantic correctness hoặc approval.
- `python -B -m unittest discover -s .agents/skills/agu-sync-design/scripts -p 'test_*.py'`: 6 tests pass.
- `python -B -m unittest discover -s .agents/skills/agu-evaluate-rag/scripts -p 'test_*.py'`: 6 tests pass. Đây là helper tests, không phải app/RAG benchmarks.
- `git rev-parse --is-inside-work-tree`: báo không phải Git repository. `git --version`: 2.46.2.windows.1.
- `python --version`: 3.13.2; `node --version`: v22.18.0; `npm --version`: 10.9.3; `uv --version`: 0.12.21.
- `docker version --format '{{.Client.Version}} / {{if .Server}}{{.Server.Version}}{{end}}'`: 29.1.3 / 29.1.3. Không chứng minh image PostgreSQL/pgvector đã có hoặc migration chạy được.
- `Get-Command`: không tìm thấy pnpm và psql trên PATH. Không phải blocker: có thể dùng npm và client trong container khi triển khai. Chưa kiểm tra quyền tải package/image, disk/RAM hoặc tốc độ OCR.
- Kiểm kê đệ quy `backend/`, `frontend/`, `tests/`, `Plan/`: không trả file. Những thư mục rỗng không phải application scaffold; dùng cấu trúc đích trong 07 thay vì duy trì hai cấu trúc song song.

Native discovery/trust lấy từ [validation record cùng ngày](2026-11-08-agent-skills-validation.md), không chạy lại trong lượt này: 3 skills được loader nhận; project config bị bỏ qua vì workspace chưa trust, custom-role live spawn chưa kiểm chứng. Đây là giới hạn tự động hóa, không chặn một agent triển khai theo AGENTS.md. Không tự sửa personal trust config.

## Những quyết định nên giữ và điều cần kiểm chứng sớm

Giữ modular monolith, PostgreSQL, manual typed facts, buffer-before-answer và quản trị dữ liệu ở P0. Chưa đưa reranker, LlamaIndex, ANN, Redis hoặc extraction tự động vào critical path. Chúng chỉ được thêm khi giải quyết bottleneck có bằng chứng.

Rủi ro lớn nhất là **độ phủ và công sức kiểm duyệt**, tiếp theo là tính đúng của temporal/release/restore và chi phí làm hai ecosystem. Kế hoạch 320 giờ bao gồm khá nhiều công việc research/curation/ops cho một developer; chưa có throughput thật để chứng minh khả thi. Ghi effort theo task và số tài liệu/facts phải sửa; re-estimate ở G1, không hứa mốc public sau 16 tuần.

Không khóa model trước corpus/gold labels; cũng không để toàn bộ pipeline đợi model. Slice đầu nên chứng minh môi trường, contract và raw source identity bằng synthetic inputs, không cần API trả phí. Parser/OCR cần spike trên tài liệu đại diện sau đó, trước khi xây quá nhiều ingestion UI.

## Trình tự bắt đầu đề xuất

| Thứ tự | Task / owner | Điều kiện hoàn thành |
|---|---|---|
| 0 | PO ghi G0, xác nhận capacity và phạm vi foundation | Actor/ngày và version/status đồng bộ; G1–G4 vẫn Pending; không đồng nghĩa cấp budget/public permission |
| 1 | Developer: foundation có thể tái lập | Git local, runtime compatibility record/lockfiles, FastAPI health + Next shell, lint/types/build/CI commands chạy thật |
| 2 | Developer/data: schema và raw source identity | Local PostgreSQL extensions/migration; cùng URL đổi bytes tạo version mới; không overwrite provenance |
| 3 | Developer/data: typed curation contract | Synthetic packet giữ unknown scope, date-only, draft/OCR warning; không giả human approval hoặc public eligibility |
| 4 | PO/operator + developer: research và corpus | Research 5–8 người; 3–5 tasks; 15–30 nguồn đại diện có quyền, coverage/provenance/QA và owner freshness |
| 5 | Developer/data: parser spike, facts, release policy prototype và dev labels | Đo lỗi bảng/footnotes/OCR, partial supersession/cutover fixtures; G1 review thực tế |
| 6 | Developer/RAG: eval và baseline retrieval/answers | Dev ≥60/holdout ≥200, protocol 04, budget trước paid calls; G2 trước chọn runtime phục vụ pilot |
| 7 | Developer/web/API: vertical MVP và rehearsal | Wireframes trước UI, session/SSE/admin/auth/budget/privacy, G3 rồi usability/G4 theo 08 |

[Kế hoạch foundation chi tiết](../superpowers/plans/2026-11-08-foundation.md) bao phủ các task code đầu tiên, ước lượng 20–28 giờ developer sau G0; research/corpus chạy thành workstream riêng theo khả năng tuyển người. Đây không phải tổng effort G1. Chỉ lập kế hoạch chi tiết phase kế tiếp sau khi có kết quả phase trước; roadmap 08 tiếp tục quản lý phần còn lại.

## Cách dùng context và agents khi triển khai

- Root giữ task brief, FR/AC, quyết định, file ownership và kết quả thật. Mỗi task đọc AGENTS + sections liên quan, không đọc archive như yêu cầu hiện hành.
- Data task đọc 05 và phần 02/04 liên quan; RAG đọc 04 + eligibility 05; API đọc 03 + data-flow 05; web đọc 06 + API contract. Reviewer đọc diff và invariant bị ảnh hưởng.
- Dùng skill curation khi bàn giao nguồn/facts, skill eval khi phân tích report, skill sync khi contract thay đổi. Không tạo skill mới cho mỗi framework/task.
- Tối đa hai child agents theo AGENTS; chỉ chia việc độc lập, một writer/file. Chưa coi native role activation/cap đã có hiệu lực; nếu cần dùng custom roles thì kiểm tra trust và live discovery riêng.
- Handoff gồm inputs có quyền dùng, trạng thái chưa biết, test commands/results và phần chưa làm; không dùng số lượng token/docs/skills làm điểm sẵn sàng.

Không thiếu một “lớp tài liệu tổng quát” nữa. Việc tiếp theo có giá trị là G0 và foundation nhỏ có kiểm chứng, rồi đo khả thi của corpus trước mở rộng tính năng.
