# AGU Admission Assistant — Implementation Roadmap

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Nguồn lực giả định | 1 developer + AI coding agent, 20 giờ/tuần |
| Lịch tham chiếu | 16 tuần / khoảng 320 giờ, chưa cam kết |
| Release target | Private pilot có giám sát trước public pilot độc lập |
| Approval / evidence | Theo [00](00-baseline-decisions.md); chưa có gate thực thi đạt |

## 1. Chiến lược

Research/task coverage → data/facts/QA → retrieval/answer eval → vertical MVP → private pilot/operations → public decision. Slices nhỏ, test rules/auth/privacy/budget ngay từ đầu; hardening không có nghĩa đợi cuối mới xây controls.

G0 chốt thiết kế, không cần benchmark có trước. G1/G2 tạo bằng chứng cho selected stack/config; không buộc PoC phải đợi chính kết quả PoC để được bắt đầu. User phải giao task implementation riêng; tài liệu này không tự triển khai code hoặc mở chi tiêu.

## 2. Lịch tham chiếu và exit gates

| Phase | Tuần / effort | Deliverables | Gate |
|---|---|---|---|
| 0 — Baseline và readiness | 1 / 20 giờ | PO review, tasks/source permissions/effort/budget plan | G0 design sign-off, OD owners rõ |
| 1 — Product/data feasibility | 2–4 / 60 giờ | Research 5–8 người, 3–5 tasks, 15–30 docs/IR, schema, facts/rule cards/aliases tối thiểu, review prototype, dev labels | G1 corpus/task QA khả thi, scope frozen cho AI test |
| 2 — AI evaluation | 5–7 / 60 giờ | Dev ≥60/holdout ≥200, dense/hybrid, conflict/eligibility, templates/excerpts và optional summary | G2 frozen report đạt 04, config/cost/latency quyết định |
| 3 — Vertical MVP | 8–11 / 80 giờ | API/session/SSE final answer, mobile UI, admin OIDC/MFA/review/candidate/activate, quotas/privacy | Demo FR P0 paths; draft/blocked isolation; chưa mở public |
| 4 — Staging và rehearsal | 12–14 / 60 giờ | Security/load/accessibility, provider/privacy review, restore/rollback/revocation/freshness drills | G3 private staging ready, đủ owner/budget/retention |
| 5 — Private pilot và buffer | 15–16 / 40 giờ | Usability ≥8 người, fix critical, content refresh, known limitations, public checklist | G4 PO quyết định public hoặc tiếp tục private |

Tổng 320 giờ là planning assumption, không năng suất đã đo; 40 giờ cuối gồm pilot và contingency, không coi toàn bộ là feature capacity. Nếu research/labeling/OCR vượt effort, giảm scope hoặc dời lịch, không bỏ gate. Tính lịch ngày cụ thể sau khi PO xác nhận giờ/tuần và ngày bắt đầu.

**Kịch bản 12 tuần:** khoảng 240 giờ ở cùng capacity, chỉ khả thi khi G1 chứng minh 3 tác vụ đủ từ corpus gọn, ít OCR, manual facts và managed infrastructure; dùng templates/excerpts, không reranker/summary nếu chưa có lợi ích; admin/eval UI tối giản, không P1. Giữ nguyên critical/eval/security/privacy gates. Đây là kịch bản có điều kiện, không phải lịch 16 tuần đã được chứng minh có thể nén.

P1 chỉ sau G4 và có capacity; không bắt đầu comparison/guidance để lấp thời gian trong khi P0 fail.

## 3. Work packages và dependencies

WP IDs giữ traceability với bản 0.1; WP-09 bỏ yêu cầu reranker bắt buộc, WP-15 chuyển core facts sang P0, thêm WP-18…20 cho research/operations/privacy.

| ID | Mức | Deliverable / FR | Dependency | Evidence |
|---|---|---|---|---|
| WP-01 | P0 | Scaffold/lockfiles/contracts/CI skeleton | G0; task implementation được giao | Local scripts thực sự chạy, không giả lệnh |
| WP-02 | P0 | Source inventory/allowlist/download, FR-08/12 | WP-01, quyền nguồn phù hợp | Provenance, SSRF/redirect/size/checksum |
| WP-03 | P0 | Parser/IR/unit QA, FR-08/16 | WP-02/04 | Golden docs/critical cells/mixed-program |
| WP-04 | P0 | Version/schema/storage/index config foundations | WP-01 | Migrations, immutable revisions, artifact identity |
| WP-05 | P0 | Applicability/conflict/review/candidate/bundle/override, FR-09/24 | WP-03/04/15 | Partial supersession, activation/rollback/revoke |
| WP-06 | P0 | Dev/holdout labels/rubric/eval runner, FR-10 | WP-02/04/18 | Frozen splits, provenance/gold evidence groups |
| WP-07 | P0 | Dense exact baseline | WP-03/04/05/06 | Filtered Recall/answer failure report |
| WP-08 | P0 | Exact/lexical/RRF + scope filters | WP-07 | Dev ablation vs baseline; decision config |
| WP-09 | P0 | Evidence/conflict/sufficiency/claims/citation validation | WP-05/08/15 | Critical suite; optional reranker ngoài critical path |
| WP-10 | P0 | Chat API/states/SSE progress+final/cancel, FR-01/03/05 | WP-09/20 | Contract, no early claims, errors/ownership |
| WP-11 | P0 | Admin auth/review/release UI, FR-07/09 | WP-01/05 | OIDC/MFA/RBAC, candidate eval trước activate |
| WP-12 | P0 | Home/Assistant/Help/About/feedback/official links | WP-10 | Mobile/accessibility/year/source/cancel states |
| WP-13 | P0 | Observability/reservations/quotas/CI/deploy, FR-11 | Bắt đầu WP-01, hoàn thiện cùng WP-10 | Concurrent budget caps, safe traces, alerts |
| WP-14 | P0 | Security/load/restore/rollback/eval final | WP-10/11/12/13, G2 | G3/G4 evidence, critical closed |
| WP-15 | P0 | Manual typed facts/aliases/rule cards, FR-16 | WP-03/04 | Critical values/exceptions/provenance/cell QA |
| WP-16 | P1 | Major Explorer/comparison, FR-13/14 | G4, WP-15 | Task utility, verified completeness/missing states |
| WP-17 | P1 | Guided checklist/advanced analytics, FR-15/18 | G4, usage/research evidence | Scope/privacy review, useful flows |
| WP-18 | P0 | Research/task baseline/coverage, FR-06/20 | Không cần app; bắt đầu phase 0/1 | 3–5 tasks, research report, comparator |
| WP-19 | P0 | Freshness/incident runbook, FR-23 | WP-02/05 | Owner/calendar/stale/critical drill |
| WP-20 | P0 | Session/provider data-flow/retention controls, FR-12/25 | WP-01 | Binding/TTL/reset/minimization/provider tests |

Manual facts WP-15 không cần model/extraction; WP-05 có thể dùng fixtures của WP-15 trước corpus đầy đủ. Eval endpoint chỉ admin, được chỉ định candidate ID; public không chọn candidate/draft từ client. Tách source QA, dataset labeling và public eligibility để proof private không làm lộ draft.

## 4. Gate records và failure actions

| Gate | Evidence cần có | Nếu chưa đạt |
|---|---|---|
| G0 | PO approval bundle 00–08/ADR, scope/owner/resource assumptions | Hoàn thiện docs, không tự ghi Approved |
| G1 | Research + corpus permissions/coverage + parse/facts QA + dev labels | Giảm tasks/corpus, curate thủ công, không mua thêm complexity |
| G2 | Protocol frozen, report dev/holdout, 0 critical, budget/latency/config | Sửa data/rules, dùng extractive/simple config, version/replenish holdout khi cần |
| G3 | E2E/auth/privacy/provider/cost/load/restore/override/freshness evidence | Giữ staging/private; không mở traffic không giám sát |
| G4 | Usability/coverage freshness, known limits, source/branding terms, PO public permission | Tiếp tục private hoặc chỉ official links/historical coverage |

Nhật ký gate ghi date/actor/artifact IDs/result/remaining risks; mặc định Not run/Pending. Không coi một report lỗi thời, demo chat hoặc bản tài liệu đã duyệt là bằng chứng gate sản phẩm pass.

## 5. Scope cuts và contingency

Giữ controls bắt buộc; giảm breadth trước: 3 tasks thay vì 5, corpus có nguồn rõ, manual facts/rule cards, extractive mode, no reranker, minimal admin/report viewer, fixed allowlisted URLs/upload thay spider. Hoãn toàn P1/P2. Nếu vẫn không đạt quality/capacity thì dời public, không hạ critical gate.

Không OCR đáng tin: chặn affected units, curate từ original hoặc loại coverage. Thiếu năm nguồn mới: pilot lịch sử có nhãn hoặc chờ dữ liệu, không gọi 2026 là 2027. Model đắt/chậm: giảm tokens/candidates trong semantic budget, templates/excerpts, cấu hình đơn giản hơn; không bỏ exceptions/citation checks. Operator vắng: current guidance stale/blocked theo 05.

## 6. Task handoff và Ready/Done

Task template: Goal; FR/AC; source sections; scope/non-goals; files/interfaces; permitted dependencies/data/spending; exact acceptance cases; review focus; verification commands có thật.

Ready: requirements không mâu thuẫn, inputs/fixtures có quyền dùng, core choices phù hợp baseline, owner và budget nếu cần, success/error states rõ. Routine choices không cần xin lại approval. Một task khoảng 2–8 giờ effort; tasks dài được chia theo behavior kiểm chứng được.

Done: thỏa AC, checks/eval tương ứng có kết quả thật, schema/API/docs đồng bộ, không secrets/PII/fake public facts, error/privacy/budget/rollback phù hợp. Chưa có code thì không ghi dev/test scripts pass.

## 7. Public pilot checklist

- [ ] G0–G3 có record thật; FR P0 và critical AC pass.
- [ ] Candidate/config đúng report 04, không critical regression; latest-for-year/current exclusions/freshness đúng.
- [ ] Source/branding/data/provider/retention/budget decisions hoàn tất theo OD-01…04.
- [ ] OIDC/MFA/RBAC, session, SSRF/upload/PII/rate/reservation controls có evidence.
- [ ] Backup/restore/re-embedding/rollback/in-flight revoke/effective cutover rehearsal; restore phải gồm revoke mới hơn backup, đối soát safety journal và không resurrect blocked facts.
- [ ] Operator calendar/incident channel/alerts và official links hoạt động.
- [ ] Mobile/keyboard/screen reader/usability report, known limitations và privacy notice.
- [ ] PO ghi ngày/actor cho phép G4 public pilot; chưa phải AGU endorsement hoặc institutional production.

## 8. Việc tiếp theo sau baseline review

PO ký G0 khi nội dung candidate được chấp nhận; xác nhận giờ/tuần và budget trước hoạt động cần chi tiền. Sau khi được giao implementation, chạy WP-01/02/04/18 rồi WP-03/06/15, review G1 trước thử AI sâu. Không có task triển khai hoặc provisioning nào được thực hiện chỉ từ lần chỉnh document hiện tại.

Update 2026-11-13: người dùng đã giao riêng bounded foundation và initial commit/push; scope exception trước G0 được ghi trong 00 §9. Xem [foundation results](implementation/foundation-results.md) để phân biệt phần WP đã làm và product gates còn Pending; không dùng report readiness 2026-11-08 như trạng thái workspace hiện tại.
