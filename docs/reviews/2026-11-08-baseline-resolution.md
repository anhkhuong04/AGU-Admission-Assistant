# Baseline Candidate — Decision & Review Resolution

| Thuộc tính | Giá trị |
|---|---|
| Ngày | 2026-11-08 |
| Bản nguồn | 0.1, lưu trong [archive](archive/2026-11-08-design-v0.1.zip) |
| Bản điều chỉnh | 0.9 — Baseline Candidate |
| Approval | Ready for Product Owner review, chưa ký duyệt 1.0 |
| Runtime validation | Not run; chưa có application hoặc benchmark |

## 1. Quyết định trong lần chỉnh sửa

Chọn MVP có kiểm duyệt với facts/rule cards tối thiểu, hybrid retrieval có benchmark và vận hành gọn. Các phương án/trade-offs, phạm vi chi tiêu và gate phê duyệt được ghi tại [00](../00-baseline-decisions.md). Các lựa chọn do lần chỉnh sửa này đề xuất/chọn không được ghi là lời xác nhận hay chữ ký của Product Owner.

Giữ chín tài liệu gốc, thêm 00 làm sổ quyết định để tránh lặp status/assumptions; bổ sung README/AGENTS cho việc giao task sau này. Không scaffold code, gọi model, provisioning hoặc phát hành public.

## 2. Ma trận xử lý review 0.1

“Specified” nghĩa là đã đưa cách xử lý vào contract/acceptance, không nghĩa là phần mềm đã được kiểm chứng.

| Finding | Quyết định / chỉnh sửa | Nơi chuẩn | Validation sau này |
|---|---|---|---|
| R01 — facts P1/P0 và bảng lỗi | FR-16 sang P0, manual typed facts/aliases/rule cards; block cả RAG/facts | [02](../02-prd.md), [04](../04-ai-rag-architecture.md), [05](../05-data-architecture.md) | AC-06/13/18, G1/G2 |
| R02 — partial supersession | Applicability từng unit, all/specific/unknown; preserve unaffected, current-use exclusions và future-effective cutover | [05 §5–6](../05-data-architecture.md) | AC-11/19/23/26, G2/G3 |
| R03 — snapshot/lifecycle/index/revoke | Tách states; immutable serving bundle; epoch/final commit; rollback giữ overrides, journal độc lập DB cho restore | [03](../03-system-architecture.md), [05 §1/3/8/11](../05-data-architecture.md) | AC-05/12/16/24/27, G3 |
| R04 — streaming/citation | P0 buffer; SSE progress/final, claim mapping; stop/disconnect không auto replay | [03 §4](../03-system-architecture.md), [04 §2.5](../04-ai-rag-architecture.md), [06](../06-ui-ux-specification.md) | AC-08/13/14, contract/E2E |
| R05 — sufficiency/conflict/support | Whole-corpus conflict registry; deterministic checks; high-risk templates/cards; optional validated semantic verifier | [04 §1–2](../04-ai-rag-architecture.md) | AC-03/13, G2 |
| R06 — metric protocol | Dev/holdout, fixed groups/mẫu số, citation coverage, false abstention, severity và no critical | [04 §5–6](../04-ai-rag-architecture.md) | AC-20, G2/G4 |
| R07 — ADR loop/reranker | G0 accepts design trước proof; validation G1/G2 riêng; WP-09 không buộc reranker | [00](../00-baseline-decisions.md), [ADR-001](../decisions/ADR-001-technology-stack.md), [08](../08-implementation-roadmap.md) | Dependency review; G0/G2 |
| R08 — freshness/incident | Owner/calendar, peak daily/off-peak weekly, stale high-risk block, incident runbook | [05 §12](../05-data-architecture.md), WP-19 ở [08](../08-implementation-roadmap.md) | AC-17/25, G3/G4 |
| R09 — privacy/session | Single-instance memory context TTL; credential binding; minimize trước provider; retention/edge/APM review | [03 §5](../03-system-architecture.md), [05 §10–11](../05-data-architecture.md) | AC-09/15/16, WP-20/G3 |
| R10 — product utility/biased metric | 3–5 tasks, research sớm, comparator, North Star mẫu số tác vụ giao, audit/feedback coverage riêng | [01 §2/7](../01-product-overview.md), WP-18 ở [08](../08-implementation-roadmap.md) | G1/G4 research/usability |
| R11 — timeline/cost/latency | 16 tuần/320h reference; 12 tuần có điều kiện; budget 0 mặc định; validated latency/envelope | [00 §4](../00-baseline-decisions.md), [03 §6](../03-system-architecture.md), [04 §6](../04-ai-rag-architecture.md), [08](../08-implementation-roadmap.md) | AC-21, G2/G3/G4 |
| R12 — UX/traceability priority | Feedback/official links P0; year precedence; changed-source metadata; date precision/accessibility | [02](../02-prd.md), [05](../05-data-architecture.md), [06](../06-ui-ux-specification.md) | AC-10/22/23 + UX checks |

Disposition của R01–R12: **Specified in candidate; runtime verification pending**. Report 0.1 giữ lại làm lịch sử, các số dòng trong report cũ trỏ bản archive.

## 3. Trạng thái kiểm tra tài liệu

- Kiểm tra độc lập từ góc nhìn người lập kế hoạch: hoàn tất. Hai finding bổ sung về restore sau revoke mới hơn backup và supersession tương lai đã được chỉnh, thêm AC-26/27 và được reviewer xác nhận đã xử lý ở mức đặc tả. Không còn câu hỏi quan trọng được reviewer nêu trong phạm vi đã kiểm tra.
- Kiểm tra read-only bằng Python qua PowerShell: exit 0; 10 active design documents cùng version 0.9, 14 Markdown files không có local link thiếu target/JSON fence lỗi/fence chưa đóng/Unicode replacement character; 25 FR và 27 AC không trùng ID; 20 work packages không dependency cycle hoặc reference WP không tồn tại.
- Archive 0.1: 11 file nguồn, ZIP CRC check không có lỗi; giữ nguyên bản để đối chiếu. Workspace chưa là Git repository nên không có commit/diff Git được báo cáo.
- Implementation tests, AI eval, load/security/accessibility trên app: chưa thực hiện vì chưa có implementation.
- PO approval và G1–G4: pending, không tự đánh dấu pass.

Những kiểm tra trên xác nhận tính nhất quán cơ bản của artifact và kết quả review đặc tả, không chứng minh ứng dụng đạt quality/latency/cost/security. Không dùng chúng để ghi benchmark hoặc product gate đạt.
