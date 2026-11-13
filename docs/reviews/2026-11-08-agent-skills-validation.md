# AGU Agent/Skill Kit — Validation Record

| Thuộc tính | Giá trị |
|---|---|
| Ngày | 2026-11-08 |
| Phạm vi | 5 project roles, 3 repo skills và 2 offline helpers |
| Codex CLI quan sát | 0.162.0-alpha.17.2 |
| Ảnh hưởng sản phẩm | Không scaffold app, không gọi model/provider, không thay approval 0.9 |

## 1. Thiết kế và baseline samples

Hướng dẫn thường trực giữ trong AGENTS.md và thiết kế 00–08. Role files tập trung ownership và đầu ra; skills tập trung reference/work artifact và automation, không nhân bản toàn bộ policy hoặc thêm model/provider/settings cá nhân.

Hai fresh-agent samples chạy trước khi viết skill curation/evaluation, chỉ đọc active docs và synthetic inputs:

- Curation: agent đã giữ điều kiện/ngoại lệ không bị sửa, block bảng mixed-program, không dùng B để chữa scope A, giữ quota tương lai pending và không giả human approval. Không quan sát thấy policy failure cần thêm một discipline skill.
- Evaluation: agent đã tính full evidence Recall=53/60 thay vì 58/60, tách support=255/260 khỏi coverage=236/240, nhận diện critical error/holdout contamination/missing runtime evidence và không xác nhận G2. Không có cơ sở thêm tường hướng dẫn chung.

Vì vậy tạo reference skills ngắn và tools tái sử dụng, không tuyên bố đã sửa một lỗi hành vi không xuất hiện. Không thực hiện micro-test wording 5 reps vì không thiết kế một discipline/pressure-enforcement policy mới; không suy ra tác dụng cải thiện statistically từ single samples.

## 2. Helper verification

Trước khi viết mỗi helper, chạy một behavior test tương ứng và quan sát fail do helper chưa tồn tại. Sau triển khai:

| Command | Kết quả thực tế |
|---|---|
| `python -B .agents/skills/agu-sync-design/scripts/test_check_design.py` | 6 tests pass: minimal workspace/code examples, broken links/duplicate IDs, shorthand cycles, JSON/version drift và no writes, invalid root, requirement shorthand không giấu unknown ID |
| `python -B .agents/skills/agu-evaluate-rag/scripts/test_summarize_eval.py` | 6 tests pass: correct denominators, missing/zero data, inconsistent subsets, invalid counter types, perfect aggregates vẫn diagnostic, supporting pairs không được ít hơn covered claims |
| `python -B .agents/skills/agu-sync-design/scripts/check_design.py --root .` | Exit 0 trên working bundle; semantic review vẫn required; không record approval |
| `python -B .agents/skills/agu-evaluate-rag/scripts/summarize_eval.py .agents/skills/agu-evaluate-rag/references/aggregate-example.json` | Exit 0 là tạo diagnostic; critical=1, recall=88,33%, coverage=98,33%, holdout không độc lập, can_approve_release=false |

Helper standard-library only, không network/model calls hoặc writes vào nguồn. Tests dùng local temporary fixtures, không phải tests/benchmark application AGU. Mọi sample là synthetic.

Ba SKILL.md đã chạy quick_validate.py đi kèm skill-creator: hợp lệ. TOML của 5 role parse bằng tomllib, required fields name/description/developer_instructions có đủ, names không trùng, không model/permission override. UI metadata có tên/default prompt trỏ đúng skill; implicit invocation giữ mặc định.

## 3. Forward samples

- Fresh agent dùng agu-evaluate-rag: chạy helper thực, so protocol hiện hành, nêu rõ critical/citation coverage/recall và evidence thiếu; không xác nhận G2 dù CLI exit 0.
- Fresh agent dùng agu-curate-knowledge: tạo packet cụ thể từ synthetic A/B, giữ unknowns/allowed uses, tách partial replacement và future cutover, không tạo IDs/approval thật. Các AC là đề xuất chưa chạy.
- agu-sync-design: đã kiểm tra hành vi bằng temporary fixtures và trên bundle thực; lượt review độc lập cho toàn kit ghi nhận ở §5.

Đây là kiểm tra chức năng/reference usability ở phạm vi mẫu, không đo mức cải thiện năng suất hay độ tin cậy thống kê của agent.

## 4. Native discovery và giới hạn activation

Qua local app-server protocol trên CLI đã quan sát, initialize với strict-config thành công; skills/list forceReload cho đúng workspace trả cả 3 project skills ở trạng thái enabled, không loader errors. Không có thread/turn hoặc model call nào được tạo để kiểm tra này.

config/read xác nhận project layer `.codex/config.toml` tồn tại nhưng **bị bỏ qua vì workspace chưa được trust trong cấu hình cá nhân**. Effective agents cap của lần CLI diagnostic chưa nhận giá trị 2. Không sửa personal config/trust tự động; giới hạn hai agent còn được ghi trong AGENTS.md để hướng dẫn phiên hiện tại. Cap native có hiệu lực khi host nạp project config được trust.

Role files đã được kiểm tra schema theo OpenAI Docs và cú pháp TOML; chưa chạy live custom-role spawn qua native client. Sự xuất hiện tên role trong prompt AGENTS.md không được coi là bằng chứng native registration. Nếu client chưa nhận role, dùng role file làm hướng dẫn delegation hoặc mở phiên hỗ trợ project custom agents sau khi xử lý workspace trust theo lựa chọn người dùng.

CLI `--strict-config` không hỗ trợ subcommand `features`; không dùng lần gọi đó làm bằng chứng config pass. Native initialize/config-read và skill loader ở trên là các kiểm tra thực tế được dùng.

## 5. Review cuối và scope

Independent kit review đã hoàn tất qua message-based agu_reviewer instructions và agu-sync-design workflow. Review phát hiện 3 vấn đề: role wording chặn cả paid task đã được cho phép; aggregate consistency chưa so covered claims với supporting pairs; requirement shorthand FR-01/99 giấu unknown ID. Đã xác minh hai lỗi helper bằng regression tests fail trước sửa, sửa từng helper rồi chạy lại suite; cập nhật role wording để giữ quyền đã được task/session cấp mà không tự mở quyền từ role selection.

Targeted recheck của reviewer xác nhận cả 3 finding đã xử lý, không còn finding trong phạm vi corrections. Kiểm tra cuối: 12 helper tests pass; 3 skill validators pass; 6 TOML files parse đúng, 5 role names duy nhất; 3 UI manifests hợp lệ, entrypoints 222–249 words. Bundle checker exit 0 với 20 Markdown files, 10 active design documents, 179 local links, 25 FR/27 AC/16 BR/10 NFR, 20 work packages và không structural issues. Không có project __pycache__ được để lại.

Đây là targeted review và samples, không là chứng minh không còn mọi lỗi hoặc live custom-role activation. Giới hạn native activation ở §4 tiếp tục giữ nguyên.

Giữ nguyên baseline candidate/product gates và các OD; không commit/push vì workspace chưa có Git repository. [Agent workflow](../agent-workflow.md) mô tả routing/cách dùng; [baseline resolution](2026-11-08-baseline-resolution.md) là lịch sử của đợt chỉnh thiết kế trước, không phải kết quả của các tests mới.
