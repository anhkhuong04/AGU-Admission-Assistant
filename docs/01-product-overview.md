# AGU Admission Assistant — Product Overview

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Cập nhật | 2026-11-08 |
| Chủ sở hữu | Product Owner |
| Approval | Chờ ký duyệt theo [00](00-baseline-decisions.md); validation chưa thực hiện |
| Phạm vi | Website độc lập, tuyển sinh đại học chính quy AGU |

## 1. Sản phẩm và lời hứa

AGU Admission Assistant giúp thí sinh và phụ huynh tìm, hiểu và đối chiếu thông tin tuyển sinh qua hội thoại tiếng Việt có dẫn nguồn. Sản phẩm chỉ dùng nguồn công khai đủ điều kiện sử dụng và được người quản trị duyệt; phân biệt năm/đợt, dữ liệu lịch sử, phần quy định được sửa đổi và thông tin chưa thể xác minh.

Đây là dự án bên thứ ba, chưa được Trường Đại học An Giang phê duyệt hoặc bảo trợ. Mục tiêu dài hạn là chứng minh giá trị và năng lực vận hành để đề xuất hợp tác; không giả định nhà trường sẽ tiếp nhận.

**Lời hứa:** đưa người dùng đến thông tin có bằng chứng và bước tiếp theo phù hợp; hỏi lại hoặc nêu giới hạn khi chưa đủ cơ sở. Không hứa biết mọi quy định, cập nhật tức thì hoặc xác nhận điều kiện xét tuyển cá nhân.

## 2. Vấn đề và giả thuyết giá trị

| Giả thuyết | Giá trị cần kiểm chứng | Bằng chứng phải thu thập |
|---|---|---|
| Nguồn phân tán ở tin tức, trang ngành và file | Tìm đúng bằng chứng nhanh hơn | Thời gian/kết quả trên cùng tác vụ với cổng AGU hoặc FAQ |
| Nhầm năm/đợt hoặc thông báo sửa đổi | Giảm sử dụng sai quy định | Test hiểu năm, nguồn áp dụng và thông tin hết hiệu lực |
| Ngôn ngữ hành chính khó hiểu | Hiểu bước tiếp theo, giữ điều kiện/ngoại lệ | Người dùng giải thích lại và chọn bước đúng |
| Có câu chưa được công bố | Biết giới hạn, đến kênh xác minh phù hợp | Test abstention hữu ích, không tạo niềm tin sai |

Các URL chính thức là nguồn ứng viên, không phải bằng chứng nhu cầu hoặc quyền tái phân phối. Chưa có nghiên cứu, benchmark hoặc kết quả triển khai trong baseline này.

## 3. Người dùng và Jobs-to-be-done

| Nhóm | Công việc | Ưu tiên |
|---|---|---|
| Thí sinh THPT/tự do | Tìm ngành, phương thức, điều kiện, hồ sơ đúng năm | Mobile, tiếng Việt dễ hiểu, không tài khoản |
| Phụ huynh | Hiểu học phí được công bố, quy trình, nguồn xác minh | Đơn vị/năm rõ, citation tại điểm đọc |
| Content operator | Kiểm tra, sửa, duyệt, thu hồi tri thức | Preview nguồn, scope, QA, lịch kiểm tra |
| Developer/maintainer | Kiểm soát lỗi, thời gian, chi phí | Trace không raw PII, eval, quota, runbook |

PO/developer có thể kiêm operator; không giả định có cán bộ AGU tham gia. AI agent hỗ trợ phát triển, không ký duyệt tri thức.

Jobs trọng tâm:

1. Tìm phương thức/điều kiện cho một ngành và năm cụ thể.
2. Tìm mốc thời gian, hồ sơ và bước tiếp theo theo thông báo đã xác minh.
3. Tra mã/tổ hợp/học phí/chỉ tiêu đã công bố, đủ scope và đơn vị.
4. Hiểu phần quy định còn áp dụng sau thông báo sửa đổi.
5. Khi thiếu dữ liệu, biết nơi kiểm chứng chính thức.

G1 chọn 3–5 tác vụ ưu tiên qua research và coverage matrix; không quảng bá chủ đề chưa có evidence đủ chất lượng.

## 4. Ranh giới phát hành

### P0 — public pilot đủ kiểm soát

- Home/Assistant/Help/About, chat trong phiên, không tài khoản public.
- Facts tối thiểu và aliases đã duyệt cho chủ đề cam kết; nhập thủ công được. Mã/số/ngày quan trọng và điều kiện rủi ro cao dùng typed facts hoặc rule cards đã duyệt.
- RAG văn bản đủ scope, claim-level citation, clarification/abstention/conflict, liên kết chính thức.
- Buffer và kiểm tra toàn bộ đáp án trước hiển thị; progress trung thực.
- Admin OIDC + MFA; ingest/review, candidate eval, atomic release, thu hồi/rollback an toàn.
- Eval theo rủi ro, privacy trước provider/logs, quota/hard budget stop, backup/restore, manual freshness.
- Feedback bằng lựa chọn/mã lý do, không free text hoặc danh tính.

### P1/P2

P1: Major Explorer/comparison, guided checklist, tự động đề xuất facts/thay đổi nguồn, analytics nâng cao, claim streaming đã kiểm chứng. P2: opt-in history và định hướng ngành sau nghiên cứu/chính sách riêng. Reranker là tùy chọn qua G2, không phải điều kiện phát hành.

### Ngoài phạm vi

Sau đại học, vừa làm vừa học/liên thông/khóa ngắn hạn; nộp hồ sơ/đăng nhập AGU/kết quả cá nhân; kết luận đủ điều kiện/đậu/rớt hoặc dự đoán điểm chuẩn; thu học bạ/CCCD/điện thoại; nhắn tin người dùng; tự nhận đại diện AGU. MVP trả một năm mỗi lượt; so sánh nhiều năm trong cùng đáp án và khôi phục quy định tại ngày tùy ý chưa hỗ trợ.

## 5. Tri thức và thời gian

15–30 tài liệu HTML/PDF/DOCX đại diện là tập PoC, không phải tiêu chí đủ nghiệp vụ. Coverage matrix gắn tác vụ với facts/rule cards/evidence, năm, đợt, nguồn và reviewer.

Năm 2026 là tập khởi tạo/lịch sử. Với lịch phát triển bắt đầu cuối năm 2026, năm phục vụ pilot có thể khác: chỉ mở khi có nguồn năm đó, đã QA và có năng lực kiểm tra độ mới. Không gắn nhãn “đang tuyển sinh” từ ngày hiện tại hoặc tiêu đề có năm.

File nhiều hệ đào tạo được tách scope từng section/table. Thông báo mới không tự thay toàn bộ văn bản cũ. Unknown/stale có thể bị chặn trả lời hiện hành theo [05](05-data-architecture.md).

## 6. Nguyên tắc sản phẩm

1. Nguồn/thời gian trước độ trôi chảy; material claims có evidence hỗ trợ.
2. Unknown khác all/current; không tự suy ra năm, đợt, mức tiền hoặc giờ hết hạn.
3. Chỉ eligible units/facts trong bundle đã duyệt được public; safety overrides được chặn ngay.
4. Lỗi bảng không được lọt qua RAG khi fact extraction bị chặn.
5. Con người duyệt tri thức/release; actor và lý do có audit.
6. Tối thiểu hóa dữ liệu trước provider/telemetry, không yêu cầu định danh.
7. Chứng minh tác vụ/corpus/retrieval trước mở rộng chức năng.

## 7. Đo giá trị

North Star nghiên cứu: **verified task resolution** = tác vụ hoàn thành đúng rubric nghiệp vụ, có evidence hợp lệ / toàn bộ tác vụ được giao có thể đánh giá. Không lấy riêng nhóm bấm feedback để suy ra toàn bộ người dùng.

G1: phỏng vấn/thử tác vụ với 5–8 thí sinh/phụ huynh; chọn 3–5 tác vụ và baseline tra cứu hiện tại. G3/G4: usability với tối thiểu 8 người, đổi thứ tự tác vụ/công cụ để giảm learning effect. Mẫu nhỏ dùng phát hiện lỗi và quyết định pilot giới hạn, không khẳng định tỷ lệ đại diện dân số.

| Chỉ số | Mục tiêu/diễn giải |
|---|---|
| Verified task resolution | Mục tiêu ≥85%; báo số đúng/tổng và loại lỗi |
| Hiểu năm/nguồn và dự án độc lập | Không còn hiểu nhầm critical trước public |
| Time to correct evidence | Median/range so với cổng AGU/FAQ cùng tác vụ; chưa chốt mức cải thiện trước baseline |
| Feedback response / audit coverage | Báo riêng; feedback không thay accuracy |
| AI/data quality | Protocol tại [04](04-ai-rag-architecture.md), 0 lỗi critical chưa xử lý |
| Latency/cost/availability | Envelope tại [00](00-baseline-decisions.md), xác minh trước G4 |

Abstention đúng có thể hữu ích nếu giúp hiểu giới hạn và tìm nguồn phù hợp. Không coi mọi lượt answered là thành công hoặc mọi abstention là thất bại.

## 8. Rủi ro và ownership

| Rủi ro | Kiểm soát / owner |
|---|---|
| Nhầm là kênh chính thức | Branding riêng, disclaimer tại điểm đọc, test hiểu; PO |
| Sửa một phần/hết hiệu lực | Applicability manifest, checks, current-use exclusions; operator |
| OCR/diễn giải sai | Chặn unit, facts/rule cards, eval critical; reviewer |
| Quá tải một người | 3–5 tác vụ, 16 tuần tham chiếu, scope cuts ở 08; PO/developer |
| Operator vắng | Stale/giới hạn khẳng định hiện hành; operator |
| Abuse/cost/privacy | Concurrency, quotas, reservation, data-flow; maintainer |
| Điều kiện nguồn/branding chưa rõ | Private staging, OD-04/G4 trước public; PO |

## 9. Nguồn ứng viên và liên kết

- [Cổng tuyển sinh AGU](https://tuyensinh.agu.edu.vn/).
- [Tin tuyển sinh 2026](https://tuyensinh.agu.edu.vn/tin-tuc?tag=Tuy%E1%BB%83n+sinh+2026).
- [Thông báo ứng viên có tên gồm chính quy và thường xuyên](https://tuyensinh.agu.edu.vn/tin-tuc/quyet-dinh-ban-hanh-thong-tin-tuyen-sinh-dai-hoc-hinh-thuc-dao-tao-chinh-quy-hinh-thuc-dao-tao-thuong-xuyen-nam-2026-cua-truong-dai-hoc-an-giang-cap-nhat-3-nganh-moi): kiểm tra scope thực tế khi ingest.

Danh sách không xác nhận nội dung hiện hành/quyền sử dụng. [02 PRD](02-prd.md), [ADR-001](decisions/ADR-001-technology-stack.md) và [00 quyết định/approval](00-baseline-decisions.md) là các tài liệu liên quan.
