# AGU Admission Assistant — Product Requirements Document

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Owner | Product Owner |
| Approval | Chờ ký duyệt theo [00](00-baseline-decisions.md) |
| Phạm vi | Website độc lập, tuyển sinh đại học chính quy AGU |

## 1. Mục tiêu và ưu tiên

Người dùng hoàn thành tác vụ bằng đáp án tiếng Việt có evidence đúng năm/đợt hoặc phản hồi minh bạch khi chưa thể xác minh. Admin duyệt/phát hành/thu hồi tri thức không sửa code. Thành công đồng thời đáp ứng nghiệp vụ, chất lượng và vận hành.

P0 bắt buộc cho public pilot; P1 sau kiểm định P0; P2 nghiên cứu riêng. Mục tiêu chưa là kết quả đạt. Sizing/latency/budget chuẩn tại [00](00-baseline-decisions.md), metric protocol tại [04](04-ai-rag-architecture.md).

## 2. Hành trình

Người dùng chính là thí sinh/phụ huynh dùng mobile; operator là PO/developer, không giả định cán bộ AGU. JTBD tại [01](01-product-overview.md).

**J1:** mở Assistant/disclaimer → nhập câu hỏi/chọn năm → resolve context hoặc hỏi 1–2 điểm quan trọng → progress có thể dừng → nhận đáp án hoàn chỉnh đã kiểm tra với nguồn/năm hoặc state minh bạch → xem nguồn/feedback/kênh chính thức.

**J2:** ingest → QA/review units/facts → index-ready → candidate manifest → eval/critical checks → approve candidate → atomic activate bundle → smoke. Thu hồi và rollback không khôi phục thông tin đã bị chặn.

**J3:** kiểm tra nguồn theo lịch/nhận báo sai → đánh giá ảnh hưởng → chặn current use khi nghi lỗi critical → review sửa đổi theo unit → candidate/eval/release. Nếu không bảo đảm freshness, nêu giới hạn thay vì khẳng định hiện hành.

## 3. Functional requirements

| ID | Mức | Yêu cầu | Acceptance tóm tắt |
|---|---|---|---|
| FR-01 | P0 | Chat tiếng Việt, multi-turn phiên ngắn hạn | Context tối thiểu; reset/xóa; evidence mới mỗi lượt |
| FR-02 | P0 | Chỉ eligible knowledge đúng scope | Draft/revoked/unit lỗi/ngoài hệ không xuất hiện |
| FR-03 | P0 | Claim-level citation | Evidence thật, đúng version/location; không URL do model dựng |
| FR-04 | P0 | Năm/đợt/applicability/lịch sử | Không trộn năm; unknown khác all; historical rõ |
| FR-05 | P0 | Clarification/abstention/conflict | Không đoán giá trị hoặc bỏ ngoại lệ quan trọng |
| FR-06 | P0 | Home/Help/About/official links | Disclaimer tại điểm đọc, link được kiểm tra |
| FR-07 | P0 | Admin OIDC + MFA + server RBAC | Không public/self-registration; roles từ server |
| FR-08 | P0 | Admin ingest và job status | Background, lease/retry/idempotency/report |
| FR-09 | P0 | Review/candidate eval/activate/revoke/rollback | Atomic bundle, safety overrides độc lập |
| FR-10 | P0 | Versioned dev/holdout/eval runner | Critical suite/report gắn candidate/config |
| FR-11 | P0 | Trace/latency/cost/quota | Không raw PII; reservation trước call; hard stop |
| FR-12 | P0 | Input/upload safety và minimization | SSRF/type/size checks; PII trước provider/logs |
| FR-13 | P1 | Major Explorer | Verified theo năm, missing states |
| FR-14 | P1 | Major Comparison | 2–3 ngành; nguồn từng thuộc tính |
| FR-15 | P1 | Guided checklist | Bước/điều kiện/ngày có nguồn |
| FR-16 | P0 | Facts/aliases/rule cards tối thiểu | Manual curation được; typed/scope/provenance; whitelist accessors |
| FR-17 | P0 | Feedback tối giản | Rating/reason code/request ID; không free text/danh tính |
| FR-18 | P1 | Analytics nâng cao | Trên dữ liệu được phép; không raw transcript mặc định |
| FR-19 | P1 | Discovery/extraction tự động | Chỉ tạo đề xuất review, không auto publish |
| FR-20 | P0 | Nguồn/kênh AGU khi cần | Không giả chuyển nội bộ hoặc tự gửi tin |
| FR-21 | P2 | Lịch sử opt-in | Policy/consent/xóa trước khi bật |
| FR-22 | P2 | Định hướng ngành | Nghiên cứu/rubric riêng, không bảo đảm đầu ra |
| FR-23 | P0 | Manual freshness/incident workflow | Owner/lịch/stale/block/release được diễn tập |
| FR-24 | P0 | Bundle tương thích và final eligibility | Đúng index/embedder/facts; policy đổi thì không phát đáp án cũ |
| FR-25 | P0 | Session isolation/privacy | ID không đủ quyền truy cập; TTL/xóa/data-flow có test |

FR-16 không phụ thuộc extraction tự động. Reranker, orchestration framework và claim streaming không phải requirement P0.

## 4. Business rules

| ID | Quy tắc bắt buộc |
|---|---|
| BR-01 | Hệ duy nhất undergraduate_full_time; file hỗn hợp phân scope từng unit |
| BR-02 | Fact/rule theo thời gian phải có năm/applicability đã xác minh; không tự infer unknown |
| BR-03 | Eligibility = release membership + review/quality + applicability + global safety policy; không một global document status |
| BR-04 | Supersession có reviewer/reason/scope; giữ phần chưa đổi |
| BR-05 | Ngày đăng/hiệu lực/hạn nộp/lần kiểm tra khác nhau |
| BR-06 | Server cấp citation IDs; material admission claims có evidence hỗ trợ |
| BR-07 | Mã/tổ hợp/tiền/chỉ tiêu/deadline chỉ từ typed facts; điều kiện rủi ro cao từ rule cards đủ ngoại lệ |
| BR-08 | Thiếu nguồn → insufficient_evidence; thiếu scope → clarify; conflict → không chọn tùy ý |
| BR-09 | User/source/model là untrusted; không arbitrary SQL/privileged tools |
| BR-10 | Redact/minimize trước provider/telemetry; không tự dùng chat làm training/eval |
| BR-11 | Năm rõ trong câu hỏi > selector > context; nêu thay đổi và đồng bộ UI |
| BR-12 | Chặn draft/bảng lỗi/ngoài scope trên mọi route và parent expansion |
| BR-13 | Revocations/current-use exclusions không bị rollback/cache/context vượt qua |
| BR-14 | P0 buffer toàn bộ đáp án; validate và final eligibility trước phát |
| BR-15 | Nguồn stale không hỗ trợ khẳng định hiện hành rủi ro cao; lịch sử có nhãn |
| BR-16 | Một năm/lượt; không dựng quy định tại ngày tùy ý; giải thích giới hạn |

## 5. Acceptance scenarios

| ID | Given / When | Then |
|---|---|---|
| AC-01 | Eligible facts/nguồn 2026, hỏi ngành X năm đó | Đúng fact/rule/citation, năm và nhãn historical phù hợp |
| AC-02 | Chỉ có 2026, hỏi học phí 2027 | Không khẳng định 2027; thiếu dữ liệu và official link |
| AC-03 | Hai deadline cùng scope trái nhau, một lọt top-k | Conflict record vẫn chặn kết luận |
| AC-04 | Draft/unit rejected có đáp án | Không dùng ở dense/lexical/expansion/SQL |
| AC-05 | Revoke trước final eligibility commit | Không phát đáp án đang chuẩn bị; knowledge_changed |
| AC-06 | Bảng mất header/sai ô số/ngày | Chặn unit/facts/chunks liên quan khỏi public |
| AC-07 | Injection từ user/PDF/HTML | Không lộ secret/vượt scope/gọi privileged functions |
| AC-08 | Timeout/validation fail/hết budget | Không raw/partial answer; state/reason đúng, official link |
| AC-09 | Input CCCD/điện thoại | PII policy trước provider; không raw identifier trong session/telemetry |
| AC-10 | URL giữ nguyên nhưng đổi file | Citation nêu version/ngày lấy/location; không khẳng định bytes hiện tại giống bản đã dùng |
| AC-11 | B chỉ sửa deadline trong A | Deadline từ B; điều kiện chưa đổi từ A |
| AC-12 | Rollback sau đổi embedder | Bundle tương thích; current exclusions/revocations còn hiệu lực |
| AC-13 | Claim không được evidence hỗ trợ | Không hiển thị; citation ID tồn tại chưa đủ pass |
| AC-14 | Dừng/đứt stream trước kết quả | Không giả hoàn tất; hủy best effort, không tự generation lại |
| AC-15 | Session A biết ID của B | Không truy cập/tiếp tục B khi thiếu credential |
| AC-16 | Nguồn lượt trước nay revoked | Assistant text cũ không làm evidence lượt mới |
| AC-17 | Quá freshness window, hỏi deadline hiện hành | insufficient_evidence/stale_knowledge, không hứa hiệu lực |
| AC-18 | File gồm chính quy/thường xuyên | Chỉ units chính quy đã duyệt được dùng |
| AC-19 | Hỏi đợt cụ thể, có quy định chung/riêng | Giữ all-rounds và sửa đổi đúng scope; unknown khác all |
| AC-20 | Điểm tổng đạt nhưng sai deadline critical | Gate fail, block public release |
| AC-21 | Hai request gần hết budget | Atomic reservations không vượt cap cấu hình |
| AC-22 | Năm trong câu hỏi khác selector/context | Ưu tiên năm rõ, UI nêu thay đổi; mơ hồ thì clarify |
| AC-23 | Nguồn có ngày nhưng không có giờ | Không tự dựng giờ hết hạn |
| AC-24 | Candidate chưa QA/eval pass | Không activate public; test trước activate |
| AC-25 | Operator vắng/báo sai critical | Chặn affected units/tác vụ, giữ official links/audit |
| AC-26 | B được activate nhưng supersession chỉ có hiệu lực tương lai | Trước cutover dùng A; sau cutover dùng B; không trộn scheduled/current, không lọc nhầm deadline tương lai hoặc lịch sử |
| AC-27 | Backup trước một revoke, mất DB rồi restore | Public AI đóng đến khi đối soát journal/re-review; nguồn bị revoke không xuất hiện lại |

## 6. Non-functional requirements

| ID | Yêu cầu / gate thiết kế, chưa kiểm chứng |
|---|---|
| NFR-01 | Protocol 04: answer accuracy ≥95%, citation support ≥98%, material citation coverage 100%, 0 lỗi critical |
| NFR-02 | Evidence-set Recall@5 ≥90% trên retrieval subset; correct abstention ≥95%; false abstention ≤5% |
| NFR-03 | P95 validated answer ≤10 giây, timeout 20 giây trên envelope ở 00 |
| NFR-04 | Uptime app SLO mục tiêu 99,5%/tháng; AI success đo riêng |
| NFR-05 | Mục tiêu WCAG 2.2 AA, checks tại 06; chưa tuyên bố certification |
| NFR-06 | HTTPS, admin OIDC/MFA, server RBAC, least privilege, upload/SSRF/quota |
| NFR-07 | Data-flow/retention/session policy tại 05; không raw transcript/PII trong logs/analytics mặc định |
| NFR-08 | Request → bundle/policy epoch → evidence/fact/source revision → model/prompt/runtime; không hứa replay prompt không lưu |
| NFR-09 | Migrations, pin versions, offline tests, restore và safe rollback rehearsal |
| NFR-10 | Budget mặc định 0, reservation/hard stop; không tự chi tiền/nâng quota |

## 7. Response states và UX

answered, clarification_needed, insufficient_evidence, conflicting_sources, out_of_scope, service_unavailable. Mỗi state có reason_code. Validation/model failure dùng service_unavailable/answer_validation_failed; thiếu nguồn thật dùng insufficient_evidence. HTTP 429 và user cancellation là transport/UX states riêng.

Disclaimer: “Đây là công cụ tra cứu độc lập, không phải kênh tuyển sinh chính thức của Trường Đại học An Giang. Vui lòng đối chiếu thông báo từ nhà trường.” Wording/branding cuối cùng được PO kiểm tra ở G4.

## 8. Definition of Done cho public pilot

- FR P0 và AC critical có E2E/integration evidence, không chỉ happy path.
- Coverage 3–5 tác vụ, provenance/QA và manual freshness owner/schedule đầy đủ.
- Dev ≥60, holdout ≥200 cases theo 04; frozen report gắn candidate/config; không lỗi critical.
- Staging đã thử SSRF/upload/RBAC/session/PII/provider payload/rate/budget controls.
- Eval trước activate; policy epoch/revocation/re-embedding/rollback được diễn tập.
- Kiểm tra privacy/provider/retention, source permissions, branding, ngân sách và official links.
- Restore, monitoring, incident owner, usability và known limitations được ghi nhận.
- PO ký G4. Đây là yêu cầu, chưa là kết quả pass.

[03 API](03-system-architecture.md) · [04 AI/eval](04-ai-rag-architecture.md) · [05 data/operations](05-data-architecture.md) · [06 UX](06-ui-ux-specification.md) · [07 engineering](07-engineering-standards.md) · [08 delivery](08-implementation-roadmap.md).
