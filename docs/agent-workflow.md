# Agent và skill cho phát triển AGU Admission Assistant

## 1. Mục đích và quyết định

Bộ này hỗ trợ **phát triển dự án bằng Codex**, không thêm runtime agent vào chatbot. Kiến trúc sản phẩm vẫn là modular monolith và RAG có kiểm soát theo [baseline](00-baseline-decisions.md).

Chọn 5 chuyên môn có ranh giới thực tế thay vì một nhóm manager/architect/tester chồng vai trò. Agent chính giữ context sản phẩm, chia slice, quyết định interface và tổng hợp. Mặc định làm trực tiếp; gọi chuyên gia khi giảm tải context hoặc cần review độc lập, không chạy cả 5 cho mỗi task.

Theo [OpenAI Docs về custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents), role project nằm trong `.codex/agents/*.toml`. Theo [OpenAI Docs về skills](https://learn.chatgpt.com/docs/build-skills), workflow project nằm trong `.agents/skills`. Models/provider/permissions của agent kế thừa phiên cha; không gắn model hoặc quyền mới vào bộ này.

## 2. Routing

| Agent | Khi dùng | Ranh giới chính |
|---|---|---|
| [agu_api](../.codex/agents/agu_api.toml) | API/session/admin auth/budget/SSE | services/api và application interfaces được giao |
| [agu_data](../.codex/agents/agu_data.toml) | Parser/IR/facts/scope/release/recovery | Worker, knowledge data, migrations được giao |
| [agu_rag](../.codex/agents/agu_rag.toml) | Retrieval/evidence/answer/eval | AI modules, configs, eval artifacts được giao |
| [agu_web](../.codex/agents/agu_web.toml) | Public/admin Next.js, nguồn/năm/states/accessibility | apps/web, client contract consumers được giao |
| [agu_reviewer](../.codex/agents/agu_reviewer.toml) | Review thay đổi quan trọng hoặc cross-boundary | Đọc và báo findings, không sửa nguồn |

Root không giao một file cho hai writer cùng lúc. Nếu thay đổi xuyên module, root chốt contract trước rồi tách ownership; implementation có dependency chạy tuần tự. Independent reviewer nhận diff/artifact và yêu cầu gốc, không chỉ summary của implementer.

[Project config](../.codex/config.toml) cấu hình tối đa **2 spawned agents đồng thời**, không tính root, khi host nạp project config. AGENTS.md cũng ghi giới hạn này cho phiên điều phối. Agent con không tự spawn thêm. Đây là capacity cap, không bắt buộc delegation. Không thay đổi personal Codex config, sandbox, approval policy, MCP hoặc model mặc định.

Reviewer giữ read-only theo chỉ dẫn vai trò; TOML không tạo một sandbox read-only độc lập. Permissions thực tế vẫn do phiên cha/host quyết định. Nếu host không hỗ trợ custom role selection, root có thể đọc role file và giao scope qua message; không tuyên bố TOML đã được nạp khi chưa kiểm tra.

## 3. Skills và phần tái sử dụng

| Skill | Dùng cho | Tài nguyên |
|---|---|---|
| [$agu-curate-knowledge](../.agents/skills/agu-curate-knowledge/SKILL.md) | Handoff nguồn/unit/facts/rule cards cho human review | Field contract và ví dụ synthetic; không nhân bản schema DB |
| [$agu-evaluate-rag](../.agents/skills/agu-evaluate-rag/SKILL.md) | Audit metric/evidence và chuẩn bị thử nghiệm | Calculator offline phân biệt full evidence recall/support/coverage |
| [$agu-sync-design](../.agents/skills/agu-sync-design/SKILL.md) | Đồng bộ thay đổi FR/ADR/API/data/roadmap | Read-only checker links/JSON/version/IDs/dependencies |

Các skill là reference/workflow ngắn, không lặp policy và thresholds trong 00–08. Không tạo thêm skill generic FastAPI/Next.js/TDD/debugging khi những hướng dẫn hiện có đã đủ. Skills tự được xem xét theo description, cũng có thể gọi rõ bằng `$skill-name`; không cần gọi mọi skill cho mọi task.

Ví dụ prompt:

> Dùng $agu-sync-design kiểm tra tác động khi đổi một response state; cập nhật các contract liên quan trong phạm vi tài liệu.

> Dùng $agu-curate-knowledge chuẩn bị handoff cho file này, giữ unknown fields và liệt kê critical cells cần reviewer kiểm tra.

> Nhờ agu_rag dùng $agu-evaluate-rag phân tích báo cáo này; sau đó agu_reviewer kiểm tra các kết luận dựa trên raw artifacts.

Không cần nạp skill toàn cục hoặc cài thêm plugin. Codex hỗ trợ phát hiện thay đổi skills; nếu selector chưa cập nhật, mở lại phiên. Local loader đã nhận cả 3 skills. Lần CLI kiểm tra cho thấy project config đang bị bỏ qua vì workspace chưa được trust; native cap 2 chưa được áp dụng trong lần đó. Người dùng có thể trust workspace qua Codex theo lựa chọn của mình để nạp project config rồi mở phiên mới; bộ này không tự sửa personal trust. Custom-role live spawn chưa được kiểm chứng. Xem [validation record](reviews/2026-11-08-agent-skills-validation.md) để biết mức kiểm tra thực tế.

## 4. Task packet

Mỗi handoff nêu: goal và FR/AC/WP liên quan; scope/non-goals; exact files/interfaces được sở hữu; inputs/artifacts; acceptance và checks có thật; quyền dữ liệu/chi phí/external action nếu cần. Agent đọc AGENTS và các sections liên quan, không đọc cả repository mặc định.

Kết quả: changed artifacts/findings, IDs/interfaces ảnh hưởng, lệnh/kết quả thực tế, missing evidence và next action. Source curation là proposal; evaluation calculator là diagnostic; design checker là structural. Không đầu ra nào tự ký G0–G4 hoặc human approval.

## 5. Kiểm tra local

```powershell
python -B .agents/skills/agu-sync-design/scripts/check_design.py --root .
python -B .agents/skills/agu-sync-design/scripts/test_check_design.py
python -B .agents/skills/agu-evaluate-rag/scripts/test_summarize_eval.py
python -B .agents/skills/agu-evaluate-rag/scripts/summarize_eval.py .agents/skills/agu-evaluate-rag/references/aggregate-example.json
```

Hai helper chỉ dùng Python standard library, không network/model/API calls, không sửa nguồn. Unit tests dùng temporary fixtures; không phải test của application AGU. Metadata skill được kiểm tra bằng validator đi kèm skill-creator khi có sẵn.
