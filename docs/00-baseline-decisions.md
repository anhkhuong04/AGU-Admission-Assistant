# AGU Admission Assistant — Baseline Decisions & Approval Record

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Trạng thái | Ready for Product Owner review |
| Phạm vi phê duyệt | Thiết kế và kế hoạch xác minh; không xác nhận đã triển khai/benchmark |
| Người ký duyệt 1.0 | Product Owner — chưa ghi nhận ký duyệt |

## 1. Cách đọc baseline

Các lựa chọn dưới đây là quyết định thiết kế được chọn trong lần chỉnh sửa theo yêu cầu Product Owner. Chúng thay thế các phương án mơ hồ của bản 0.1, nhưng chưa phải chữ ký phê duyệt của Product Owner. `Selected` mô tả lựa chọn trong candidate; `Validated` chỉ dùng khi có artifact thử nghiệm. Không suy ra một trạng thái từ trạng thái còn lại.

Khi Product Owner phê duyệt bundle, chuyển tài liệu điều hành từ 0.9 sang **1.0 — Approved Baseline**, ghi ngày/actor và ADR sang `Accepted for design`. Các trạng thái xác minh còn `Pending` tiếp tục giữ nguyên. Phê duyệt thiết kế không cấp quyền chi tiền, dùng thương hiệu AGU hoặc phát hành public.

## 2. Các hướng đã cân nhắc

| Hướng | Đánh đổi | Quyết định trong candidate |
|---|---|---|
| Chatbot FAQ/RAG tối giản | Nhanh làm demo, nhưng khó kiểm soát thay đổi, bảng số liệu và thu hồi | Chỉ phù hợp spike, không đủ cho public pilot |
| MVP có kiểm duyệt, facts tối thiểu, release và eval | Tốn công QA ban đầu; phạm vi rõ và vận hành được với một người | **Chọn** cho sản phẩm này |
| Nền tảng tư vấn rộng, recommendation/agent/graph ngay từ đầu | Nhiều tính năng và overhead; chưa có bằng chứng nhu cầu/corpus | Hoãn sau dữ liệu sử dụng và năng lực vận hành |

Lý do chọn: giá trị cốt lõi là tìm thông tin tuyển sinh đúng nguồn/thời điểm và bước tiếp theo. Nguy cơ lớn nhất nằm ở chất lượng và độ mới của tri thức; ưu tiên kiểm soát này trước độ rộng tính năng.

## 3. Sổ quyết định

Tất cả quyết định D-01…D-12 là `Selected`; evidence vận hành là `Pending` cho đến khi gate tương ứng có báo cáo.

| ID | Lựa chọn cho baseline | Lý do / điều kiện xác minh |
|---|---|---|
| D-01 | Đại học chính quy AGU; website độc lập; 3–5 tác vụ tra cứu ưu tiên | Research G1 kiểm chứng utility; không kết luận xét tuyển cá nhân |
| D-02 | Next.js/React/TypeScript + FastAPI/Python; modular monolith + worker riêng | Hai ecosystem có chi phí nhưng phù hợp web và ingestion Python; pin versions khi bootstrap |
| D-03 | Managed PostgreSQL + pgvector + private S3-compatible storage; DB-backed jobs | Exact vector search trước; ANN/Redis/Celery chỉ thêm qua số đo và ADR |
| D-04 | Docling là parser PDF đầu tiên; HTML parser và DOCX fallback; canonical IR thuộc domain | PoC quyết định OCR mode; không phụ thuộc serialization framework làm source of truth |
| D-05 | Structured facts tối thiểu và aliases ở P0; nhập/duyệt thủ công được | Mã ngành, tổ hợp, tiền, chỉ tiêu, hạn chót chỉ trả từ facts đã kiểm duyệt, đủ scope; extraction tự động ở P1 |
| D-06 | Dense baseline → lexical/exact + RRF; reranker tùy bằng chứng | Hybrid là cấu hình mục tiêu; có thể giữ cấu hình đơn giản hơn nếu đạt gates và ghi lý do ở G2 |
| D-07 | Evidence/fact applicability và partial supersession ở mức unit; release bất biến | Draft, bảng lỗi và phần văn bản ngoài scope không vào evidence public |
| D-08 | Pin serving bundle; global safety overrides không bị rollback | Bundle khóa release/index/runtime; final policy/cutover check; restore đóng public tới khi đối soát safety journal mới hơn backup |
| D-09 | P0 buffer và kiểm tra toàn bộ đáp án; SSE chỉ báo tiến trình rồi trả kết quả hoàn chỉnh | Không stream raw token hoặc chạy hiệu ứng gõ lại; claim streaming là P1 nếu chứng minh an toàn |
| D-10 | Gold dev/holdout riêng; gates theo rủi ro và claim/citation | Protocol ở 04; không dùng điểm trung bình để bỏ qua lỗi critical |
| D-11 | Không có tài khoản/lịch sử lâu dài cho public; session ngắn hạn, PII minimization trước provider | TTL và data-flow ở 05; admin dùng OIDC + MFA, không tự xây password system |
| D-12 | Lịch tham chiếu 16 tuần, giả định 20 giờ/tuần; private pilot trước public | Ước lượng 320 giờ, không cam kết; 12 tuần chỉ là kịch bản rút scope có điều kiện ở 08 |

LlamaIndex không phải dependency P0 bắt buộc. Chỉ dùng utility qua adapter khi giảm công việc rõ ràng; router, SQL, publication, eligibility và citation contract do application sở hữu. Không xây agent tự do, GraphRAG, microservices hoặc fine-tuning trong MVP.

## 4. Ranh giới MVP và tiêu chí vận hành được chọn

- Corpus đầu tiên: 15–30 tài liệu đại diện để PoC; số lượng tài liệu không thay thế coverage matrix của 3–5 tác vụ. Dữ liệu 2026 dùng để khởi tạo và đánh giá lịch sử; pilot phục vụ năm nào phải có nguồn năm đó. Không mặc định 2027 đã công bố.
- P0: chat, facts tối thiểu, citation, clarification/abstention/conflict, feedback bằng mã lý do, liên kết AGU, admin review/release/rollback, manual freshness, eval, auth và vận hành.
- P1: Major Explorer/comparison, extraction tự động, discovery tự động, analytics nâng cao, guided checklist và claim streaming có kiểm chứng. P2: opt-in history và định hướng ngành sau nghiên cứu riêng.
- Pilot envelope để benchmark: 100 yêu cầu/ngày, tối đa 5 yêu cầu AI đồng thời. Đây là giả định sizing, chưa là traffic thực tế.
- Độ trễ mục tiêu: P95 tới **đáp án hoàn chỉnh đã kiểm tra ≤10 giây**, timeout request 20 giây, trên envelope và cấu hình đo ở 04. Tiến trình phản hồi ≤0,5 giây ở điều kiện test mạng được ghi nhận; không tính progress là đáp án.
- Giữ uptime app 99,5%/tháng làm SLO mục tiêu sau deployment; đo riêng AI service success. Không hứa SLA công khai trước vận hành.
- Không có mức chi tiêu mặc định. `MONTHLY_AI_BUDGET` và `DAILY_AI_BUDGET` mặc định 0: chặn provider trả phí khi chưa cấu hình. Reservation trước gọi, cảnh báo 80%, hard stop 100%; không tự nâng quota. Budget hạ tầng tách riêng.

## 5. Các lựa chọn có chủ ý để sau thử nghiệm

| ID | Quyết định còn lại | Owner / hạn / bằng chứng cần có |
|---|---|---|
| OD-01 | Mức ngân sách AI/hạ tầng và khả năng chi trả | PO, trước bất kỳ provisioning/call trả phí; dự toán G1/G2, không tự tạo cam kết tài chính |
| OD-02 | Model/embedder, OCR mode, có reranker hay không | Developer đề xuất, PO ghi nhận G2; chất lượng/latency/cost cùng source snapshot |
| OD-03 | Hosting, vùng dữ liệu, OIDC/MFA và điều kiện provider | PO trước G3; compatibility, xử lý dữ liệu, khả năng restore, báo giá hiện hành |
| OD-04 | Tên/domain/branding công khai, quyền sử dụng nguồn và kênh báo sai | PO trước G4; không giả định AGU bảo trợ hoặc quyền tái phân phối |

Các OD không ngăn việc hoàn thiện thiết kế hoặc proof local theo scope được giao; chúng ngăn những hành động phụ thuộc vào quyền, chi phí hoặc deployment tương ứng. Khi bắt đầu coding, task phải chỉ rõ phần được phép làm; yêu cầu chỉnh tài liệu hiện tại không tự mở rộng thành triển khai app.

## 6. Approval và verification gates

| Gate | Điều được xác nhận | Bằng chứng / hành động được mở |
|---|---|---|
| G0 | Baseline thiết kế được PO ký duyệt | Bundle 00–08 + ADR; không cần benchmark có trước; mở implementation theo task được giao |
| G1 | Nhu cầu/tác vụ, corpus/QA và facts tối thiểu khả thi | Research, inventory/coverage, parser report, source permissions; cho phép đóng băng scope thử AI |
| G2 | Retrieval/answer config và metric protocol đạt thử nghiệm | Dev/holdout report, chi phí/latency; runtime/model config được chọn; không tự mở public |
| G3 | Vertical MVP trong private staging vận hành được | E2E, auth/MFA, privacy/provider review, budget, restore, revocation/rollback; mở private pilot có giám sát |
| G4 | Public pilot được PO cho phép | Critical cases pass, usability, freshness coverage, incident drill, branding/data terms; ghi known limitations |

Mọi gate hiện `Not run / Pending`; bảng này định nghĩa điều phải chứng minh. Chỉ G0 là phê duyệt tài liệu; G1–G4 là kiểm định sản phẩm sau này.

## 7. Ownership và nguồn chuẩn

PO chịu trách nhiệm scope, ngân sách, điều kiện nguồn, policy và ký duyệt phát hành. Developer là maintainer kiêm content operator ban đầu; tách actor/role trong audit dù một người có nhiều vai trò. AI agent không là reviewer nguồn hoặc người ký duyệt.

| Chủ đề | Tài liệu chuẩn |
|---|---|
| Quyết định, trạng thái approval, sizing assumptions | 00 (tài liệu này) |
| Product/JTBD/research | [01](01-product-overview.md) |
| FR/BR/AC và ưu tiên | [02](02-prd.md) |
| API, serving và security boundary | [03](03-system-architecture.md) |
| Evidence/answer policy, metric definitions | [04](04-ai-rag-architecture.md) |
| Schema, temporal/release, data-flow/retention/freshness | [05](05-data-architecture.md) |
| UX và accessibility | [06](06-ui-ux-specification.md) |
| Engineering/CI/agent workflow | [07](07-engineering-standards.md) |
| Work packages, gate evidence và timeline | [08](08-implementation-roadmap.md) |
| Stack và alternatives | [ADR-001](decisions/ADR-001-technology-stack.md) |

Xung đột: 00 quyết định trạng thái/phạm vi; 02 quyết định nghiệp vụ; 04/05 quyết định contract chuyên biệt. Sửa đồng thời các tài liệu ảnh hưởng, không chọn một câu thuận tiện để bỏ qua requirement khác. Bản review 0.1 là lịch sử; xem [resolution matrix](reviews/2026-11-08-baseline-resolution.md) để theo dõi xử lý.

## 8. Record phê duyệt 1.0

- [x] Có quyết định thiết kế rõ và phân biệt validation với approval.
- [x] Các rủi ro review 0.1 có contract hoặc acceptance gate tương ứng.
- [ ] PO xác nhận nội dung candidate và ghi actor/ngày phê duyệt.
- [ ] Cập nhật version/status tài liệu điều hành 00–08, ADR-001 và README/AGENTS sang 1.0; giữ nguyên các review/archive lịch sử và trạng thái G1–G4 theo bằng chứng thực tế.

Không đánh dấu các ô còn lại thay cho Product Owner. Mọi thay đổi scope sau baseline phải ghi decision/change record và impact lên FR, schema, UX, eval và roadmap.

## 9. Quyền triển khai foundation — 2026-11-13

Người dùng/PO yêu cầu đọc plan, bắt đầu xây nền tảng và commit/push đầu tiên lên `anhkhuong04/AGU-Admission-Assistant`. Yêu cầu này cấp scope triển khai bounded foundation theo [plan](superpowers/plans/2026-11-08-foundation.md), thay điều kiện chờ G0 trong riêng milestone này và cấp quyền Git push. Không suy diễn thành chữ ký phê duyệt toàn bundle 1.0. Version 0.9, record G0 và G1–G4 vẫn Pending; không cấp paid provider/provisioning/public deployment hoặc quyền nguồn/branding. Evidence implementation được ghi riêng trong [foundation results](implementation/foundation-results.md).
