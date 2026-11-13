# AGU Admission Assistant — UI/UX Specification

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Định hướng | Mobile-first, content-first, tin cậy nhờ nguồn và phạm vi rõ |
| Approval / evidence | Theo [00](00-baseline-decisions.md); chưa có visual/mockup/usability results |

## 1. Experience goals

Người dùng tìm thông tin có nguồn, hiểu năm/phạm vi và bước tiếp theo trong ít thao tác. Nguồn/giới hạn xuất hiện tại điểm đọc; không dùng màu sắc hoặc animation để gợi ý AI luôn chắc chắn. Không ép danh mục/so sánh vào chat khi sau này có structured UI phù hợp.

P0 không phải chatbot raw streaming: có progress đúng phase rồi hiển thị đáp án hoàn chỉnh đã kiểm tra. Tránh đánh máy lại văn bản để tạo cảm giác streaming hoặc gọi progress là TTFT câu trả lời. Không hiển thị phần model output chưa validate.

## 2. Routes và phạm vi

| Route | Mức / nội dung |
|---|---|
| / | P0: câu hỏi chính, 3–5 lối tắt có coverage, disclaimer/official link |
| /assistant | P0: transcript trong tab, year/context, answer/source panel, feedback |
| /help | P0: cách dùng, coverage/last check, privacy/retention, báo sai, AGU links |
| /about | P0: dự án độc lập, chủ thể vận hành, giới hạn |
| /majors, /majors/[slug], /compare | P1, chỉ mở khi verified dataset đủ |
| /admissions | P1; P0 có thể dẫn tới official source, không trang dữ liệu giả/trống |
| /admin/sources | P0: inventory/versions/jobs/freshness |
| /admin/review/[id] | P0: source/IR/unit/facts/scope/QA |
| /admin/releases | P0: candidate, eval, approval/activation/rollback/overrides |
| /admin/evaluation | P0: report tối giản; dataset/editor nâng cao có thể CLI trước |

Không cần full analytics/settings CMS ở P0; provider secrets/config do deployment quản lý, không hiển thị trong UI. Navigation public: Home, Assistant, Help, About.

## 3. Public flows

**First use:** thấy dự án độc lập → chọn prompt có coverage hoặc nhập → chọn năm/clarify → progress → đáp án/state → mở nguồn → feedback hoặc official channel.

**Year/context:** explicit year trong message > selector > context. Khi khác selector, hiện “Đang dùng năm … theo câu hỏi của bạn” và đồng bộ selector. Nếu chưa rõ thì hỏi một câu cụ thể. Year catalog phân verified coverage/historical, không gắn “hiện hành” vì trùng clock year. Năm chưa có nguồn có thể được hỏi trong chat, nhận thiếu dữ liệu; không giấu giới hạn bằng cách chỉ liệt kê năm có dữ liệu.

**Session:** transcript chỉ memory trong tab, không lưu lịch sử lâu dài. Có “Cuộc trò chuyện mới/Xóa phiên”; reload/API restart/session expiry giải thích tạo phiên mới. Disclaimer này hiển thị trước khi người dùng kỳ vọng lưu lịch sử. Không điền lại định danh nhạy cảm vừa bị hệ thống yêu cầu gỡ.

**Sources:** citation inline mở drawer trên desktop hoặc dialog/bottom sheet mobile. Mỗi nguồn có title, academic year/round, page/section, ngày lấy bản nguồn, lần kiểm tra và canonical URL/domain. Nếu nguồn cùng URL đã thay file, cảnh báo bản hiện tại có thể khác bản trích; nếu chưa kiểm tra lại, nói chưa kiểm tra, không gán trạng thái unchanged. Không public private storage URL.

## 4. Answer và state matrix

Answer render từ claims backend, citation ngay cụm claim; số/ngày/đơn vị từ typed facts/rule cards. Narrative summary và excerpt phải phân biệt: excerpt thể hiện là trích nguồn, không giả là kết luận tư vấn mới. Historical banner/reference date nằm ngay trên đáp án; không đưa số liệu năm cũ như câu trả lời năm mới. Rule card sắp áp dụng có nhãn/ngày hiệu lực riêng; không gọi là hiện hành trước cutover.

| State | Nội dung / hành động |
|---|---|
| Idle | Gợi ý có dữ liệu thật; nhập câu hỏi |
| Progress | Đang tìm nguồn/đang kiểm tra, không phần trăm giả; có Dừng |
| answered | Claims + năm/đợt + nguồn + last checked; mở nguồn/feedback |
| clarification_needed | Hỏi 1–2 thông tin quan trọng; lựa chọn phù hợp, không form dài |
| insufficient_evidence | Nêu thiếu nguồn/chưa publish/stale; official link, không tự suy đoán |
| conflicting_sources | Nêu chưa thể kết luận, cho xem nguồn; không chọn giá trị “mới hơn” |
| out_of_scope | Nêu phạm vi và kênh chính thức phù hợp |
| service_unavailable | Timeout/budget/verification failure với thông báo dễ hiểu; thử lại do người dùng chọn |
| Cancelled/disconnected | “Đã dừng” hoặc lỗi kết nối; giữ input; không tự gửi lại request |
| Rate limited | Retry-After dễ hiểu; không lộ budget/config nội bộ |
| Source unavailable/changed | Giữ metadata của bản đã dùng; nêu link lỗi/thay đổi, không hứa file hiện tại giống bản cũ |

Answer validation fail dùng thông báo “Chưa thể tạo câu trả lời có kiểm chứng. Bạn có thể xem nguồn chính thức hoặc thử lại.” Không nói dữ liệu chưa công bố nếu thực tế lỗi ở generator. Link chính thức vẫn sử dụng được khi AI bị khóa budget.

Feedback P0: Hữu ích/Chưa chính xác, reason codes sai năm/sai nguồn/thiếu thông tin/khó hiểu/khác; không ô free text. /help có kênh báo sai do PO chọn ở G4. Không giả lập đã chuyển yêu cầu tới cán bộ AGU.

## 5. Admin flows và kiểm soát

Ingest → processing/report → original/IR/table side-by-side → units/facts/scope/critical cells → approve revision → build candidate → eval/critical checklist → approve release → activate → smoke. Test câu hỏi mẫu/eval diễn ra **trước** activate, không chờ lỗi public mới kiểm tra.

Hiển thị riêng processing, review, quality, release membership và safety override; không một status chip “Published” che giấu unit blocked. Original bất biến; sửa extraction/metadata tạo revision mới, diff/actor/reason. Xem ảnh hưởng: năm/đợt/topic, unit/fact counts, retained/replaced provisions, conflict và freshness.

Activate/rollback có confirm phạm vi/bundle/eval report; rollback nêu units vẫn bị global block. Emergency block là thao tác riêng, lý do bắt buộc, có thể thực hiện ngay không đợi full eval. Mở lại cần review/approval; không nút Delete cho dữ liệu đang được trích.

Admin freshness list có owner/last checked/due/stale; action “đã kiểm tra nguồn” không đồng nghĩa ingest/publish. Không tự báo “mọi dữ liệu mới nhất”. Một operator có thể kiêm roles nhưng UI vẫn ghi actor/action audit.

## 6. Visual language

Academic minimalist, light mode trước; neutral background/accent xanh riêng, không mặc định logo/màu AGU. Sans-serif hỗ trợ tiếng Việt, body mobile ≥16px, line-height khoảng 1,5–1,7; khoảng cách token 4/8px, readable content width. CSS tokens + accessible primitives, không bắt buộc Fluent UI package; không thêm animation/library vì style reference.

Trạng thái có text/icon ngoài màu; không fake social proof, accuracy badge, số người dùng hoặc “100% chính xác”. Label “nguồn đã được quản trị duyệt” mô tả workflow, không biến thành bảo đảm nội dung tuyệt đối. Quick actions chỉ hiện chủ đề có coverage hoặc link official hoạt động.

## 7. Responsive/accessibility acceptance

Mục tiêu WCAG 2.2 AA theo [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/); đây là mục tiêu thiết kế, không phải chứng nhận đã đạt.

- Test 320/375px mobile, tablet và desktop, 200% zoom, mobile keyboard/landscape; input/sticky UI không che nội dung/focus, URLs dài wrap được.
- Keyboard: skip link, thứ tự tab, focus visible và không bị overlay che; Enter gửi/Shift+Enter xuống dòng, xử lý IME tiếng Việt không gửi giữa composition.
- Dialog nguồn: accessible name, focus trap phù hợp, Escape/Close, trả focus về citation; citation buttons có tên rõ.
- Screen reader: semantic headings/labels; aria-live polite chỉ báo đổi phase/kết quả, không đọc từng token hoặc lặp transcript; state lỗi phân biệt được.
- Contrast: normal text ≥4,5:1, large text ≥3:1, meaningful non-text UI ≥3:1; không dùng màu làm tín hiệu duy nhất.
- Web pointer targets tối thiểu 24×24 CSS px hoặc exception hợp lệ; design target 44×44 CSS px cho controls chính mobile. Không thay tiêu chuẩn web bằng pt/dp native.
- Forms có label và inline errors/error summary khi phù hợp; authentication cho phép password manager/paste/OTP autofill theo provider, không tự thêm cognitive puzzle.
- Tôn trọng reduced-motion; không animation chặn thao tác hoặc mất transcript khi resize.

## 8. Deliverables và usability gate

Wireframes Home/Assistant/Admin Review + Release trước UI code; tokens/component inventory và annotated states. Không cần hi-fi toàn bộ P1 trước MVP.

G1 chọn tác vụ với 5–8 người theo 01; G3/G4 ít nhất 8 usability participants, cùng tasks/baseline source lookup. Đo đúng đáp án, đúng nguồn/năm, next action, thời gian và nhận thức dự án độc lập; log critical misunderstandings. Gate ≥85% task resolution là mục tiêu pilot, báo raw counts, mẫu nhỏ không suy rộng dân số.

[02 FR/AC](02-prd.md) · [03 response/SSE](03-system-architecture.md) · [04 evidence modes](04-ai-rag-architecture.md) · [05 session/freshness](05-data-architecture.md) · [08 gates](08-implementation-roadmap.md).
