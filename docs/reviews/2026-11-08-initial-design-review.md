# AGU Admission Assistant — Review thiết kế ban đầu

> Bản review lịch sử cho thiết kế 0.1. Tài liệu hiện hành đã được chỉnh thành 0.9; xem [resolution matrix](2026-11-08-baseline-resolution.md). Các dẫn chiếu dòng của review này ứng với [bản lưu 0.1](archive/2026-11-08-design-v0.1.zip).

| Thuộc tính | Giá trị |
|---|---|
| Ngày review | 2026-11-08 |
| Bộ tài liệu | 01–08 và ADR-001, phiên bản 0.1 |
| Loại review | Product, tính nhất quán đặc tả, kiến trúc, khả năng vận hành và nghiệm thu |
| Kết luận đề xuất | Giữ Draft/Proposed; chỉnh các mục A trước Approved Baseline |
| Trạng thái báo cáo | Nhận xét để Product Owner thảo luận; không phải quyết định phê duyệt |

Đã đọc theo thứ tự `01 → 02 → ADR-001 → 03 → 04 → 05 → 06 → 07 → 08`. Đây là review thiết kế: không có triển khai, parser PoC, đánh giá model hoặc benchmark tải để xác nhận các mục tiêu. `README.md` và `AGENTS.md` hiện rỗng, phù hợp với việc chưa scaffold nhưng cần bổ sung trước khi giao task coding.

Các dẫn chiếu dòng bên dưới ứng với bản 0.1 tại thời điểm review. Không sửa nội dung chín đặc tả trong lần review này.

## 1. Nhận định về sản phẩm

Hướng sản phẩm có lý: người dùng cần tìm đúng thông báo, hiểu điều kiện và biết bước tiếp theo trong một bối cảnh thay đổi theo năm/đợt. Lợi thế đáng kiểm chứng là giảm thời gian và sai sót khi tra cứu; số lượng tính năng AI không tự chứng minh giá trị này.

Những quyết định nên giữ:

- Giới hạn đại học chính quy, sản phẩm độc lập, không hứa kết quả xét tuyển cá nhân.
- Nguồn có provenance và ngữ cảnh thời gian; không đủ căn cứ thì hỏi lại hoặc từ chối kết luận.
- Quyền kiểm soát của người quản trị, immutable raw, review trước publish, rollback và audit.
- Modular monolith, worker riêng, PostgreSQL thống nhất; chưa thêm graph, agent tự do hoặc fine-tuning.
- Eval và PoC tài liệu trước mở rộng Major Explorer/comparison.

Hai bất định sản phẩm còn lớn: người dùng có hoàn thành tác vụ tốt hơn khi dùng cổng AGU trực tiếp hay không, và một người có duy trì tri thức đủ mới trong mùa tuyển sinh hay không. Cả hai cần được đưa vào gate pilot, bên cạnh chất lượng model.

## 2. Mức ưu tiên của nhận xét

| Mức | Ý nghĩa |
|---|---|
| A | Cần thống nhất contract/phạm vi trước baseline 1.0; có nguy cơ triển khai hai cách trái nhau |
| B | Cần đáp ứng trước public pilot; có thể xác nhận dần trong PoC/implementation |
| C | Cải thiện tài liệu và khả năng bàn giao |

Đây là mức ưu tiên review, độc lập với nhãn P0/P1/P2 của feature backlog. Các mục dưới đây là rủi ro của đặc tả, không phải lỗi đã quan sát trong phần mềm.

## 3. Findings và chỉnh sửa đề xuất

### R01 — A: Structured facts ở P1 nhưng đường trả lời chính xác đã được thiết kế dựa vào chúng

**Căn cứ:** [02, FR-16](../02-prd.md) dòng 76; [04, §3.2](../04-ai-rag-architecture.md) dòng 60–64; [05, typed fact model](../05-data-architecture.md) dòng 154–158; [08, WP-15](../08-implementation-roadmap.md) dòng 63. Alias ngành trong 04 dòng 54 cũng cần một danh mục đã duyệt.

**Tác động:** MVP được mô tả là trả lời mã ngành, tổ hợp, học phí, hạn chót nhưng chưa xác định nó dùng đường nào khi typed accessors chưa tồn tại. AC-06 và QA gate của 05 chỉ chặn facts bảng lỗi; đoạn bảng đó vẫn có thể đi vào RAG nếu publish cả tài liệu.

**Đề xuất:** Đưa một tập facts tối thiểu cho các chủ đề MVP cam kết sang P0, có thể nhập/duyệt thủ công; extraction tự động và schema ngành đầy đủ vẫn ở P1. Nếu không chọn cách này, PRD phải ghi rõ những truy vấn nào được trả bằng đoạn văn đã QA và những truy vấn nào phải abstain. Chặn nội dung bảng lỗi khỏi cả evidence RAG lẫn structured facts.

**Tiêu chí bổ sung:** Bảng có một ô hạn chót sai OCR không được xuất hiện trong câu trả lời qua bất kỳ đường truy xuất nào. Danh mục alias/mã ngành tối thiểu có owner và provenance.

### R02 — A: Thay thế một phần văn bản chưa có contract thực thi

**Căn cứ:** [02, BR-03/04](../02-prd.md) dòng 90–91; [04, filtering](../04-ai-rag-architecture.md) dòng 69–81; [05, release và supersession](../05-data-architecture.md) dòng 189–191.

**Tác động:** Văn bản A chứa điều kiện và hạn nộp; B chỉ sửa hạn nộp. Nếu đánh dấu toàn bộ A là superseded và loại khỏi retrieval thì mất điều kiện còn hiệu lực. Nếu giữ A thì có thể trả lại hạn cũ. 05 đã nhận diện vấn đề nhưng chưa quy định cách chọn fact/span có hiệu lực.

**Đề xuất:** Chốt phạm vi áp dụng của evidence/fact: năm, đợt, phương thức, ngành/đối tượng khi cần, và quan hệ sửa đổi ở mức fact/section. Với MVP có thể dùng một manifest do curator duyệt để xác định evidence được dùng và evidence bị thay thế, thay vì xây bộ suy luận pháp quy. Truy vấn lịch sử phải có chính sách riêng, không phụ thuộc duy nhất vào trạng thái global của tài liệu.

**Tiêu chí bổ sung:** Sau B, hỏi điều kiện vẫn dùng phần hợp lệ của A; hỏi hạn nộp dùng B; hỏi lịch sử có nhãn thời gian rõ. Các quy định chung và quy định của từng đợt cùng tham gia khi phù hợp; không lọc mất quy định chung chỉ vì `round=null`.

**Case nguồn cần kiểm tra:** URL nguồn ở 01 dòng 129 có tên chứa cả đào tạo chính quy và thường xuyên. Chưa xác minh được nội dung file trong lần review này; nên dùng làm case kiểm tra phân loại scope ở mức section/table, thay vì gắn một `program_type` cho toàn file rồi tin mọi chunk đều đúng phạm vi.

### R03 — A: Snapshot, lifecycle, index và thu hồi cần một mô hình nhất quán

**Căn cứ:** [03, invariants](../03-system-architecture.md) dòng 123–127; [04, snapshot/filter](../04-ai-rag-architecture.md) dòng 68–69; [05, state machine và release](../05-data-architecture.md) dòng 32–54, 189; [06, U3](../06-ui-ux-specification.md) dòng 53.

**Tác động:** State machine gộp tiến trình ingest, approval và publication, trong khi runtime kiểm tra chúng như các thuộc tính riêng. Rollback sang release cũ có thể vẫn bị loại bởi trạng thái global `superseded`. Release chỉ liệt kê document versions nhưng không xác định đầy đủ index/embedding config để rollback sau re-embedding. UX đang đặt kiểm thử câu hỏi mẫu sau publish.

**Đề xuất:** Phân biệt trạng thái xử lý, quyết định duyệt, membership của release và emergency revocation. Release manifest cần khóa phiên bản nội dung, facts, index/embedding và cấu hình liên quan để truy vấn tương thích; trace giữ cấu hình generator/prompt/router của request. Đánh giá candidate release trước atomic switch, rồi smoke test sau switch.

**Tiêu chí bổ sung:** Rollback sau khi đổi embedding model vẫn chọn đúng query embedder/index và facts tương ứng. Thu hồi không bị hoàn tác bởi rollback. Chốt rõ request đang chạy xử lý thế nào khi có thu hồi: snapshot thông thường được pin, nhưng nguồn bị thu hồi có được kiểm tra lại trước khi phát nội dung hay không. Kiểm tra cả cache và hội thoại cũ.

### R04 — A: Streaming chưa thống nhất với kiểm tra claim/citation

**Căn cứ:** [03, SSE](../03-system-architecture.md) dòng 74; [04, generation contract](../04-ai-rag-architecture.md) dòng 85–90; [06, streaming state](../06-ui-ux-specification.md) dòng 94.

**Tác động:** Nếu `delta` được gửi ngay khi model sinh, người dùng có thể đọc số liệu sai trước khi schema, citation hoặc support check thất bại. Rút nội dung ở event cuối không ngăn được việc người dùng đã dùng thông tin đó. Schema hiện chưa thể hiện rõ mapping từng claim với evidence.

**Đề xuất:** Chọn một contract: buffer toàn bộ câu trả lời để validate trước khi hiển thị, hoặc phát từng claim đã kiểm tra kèm evidence IDs. Dùng `claims[{claim_id, text, evidence_ids}]` hoặc cấu trúc tương đương. Không coi kiểm tra ID hợp lệ là kiểm tra nguồn hỗ trợ nội dung.

**Tiêu chí bổ sung:** Model sinh claim học phí không được evidence hỗ trợ thì claim đó không được hiển thị. Quy định rõ hành vi stop, disconnect, lỗi giữa stream và câu trả lời chưa hoàn tất. Đo thời gian tới nội dung có nghĩa đã được kiểm tra; event `started`/spinner không được tính là TTFT nội dung.

### R05 — A: “Đủ bằng chứng”, “không xung đột” và “support check” mới là tên bước

**Căn cứ:** [04, pipeline và evidence pack](../04-ai-rag-architecture.md) dòng 45–47, 79–87.

**Tác động:** Top 3–6 evidence có thể chỉ chứa một trong hai nguồn mâu thuẫn. Không thấy mâu thuẫn trong retrieval không chứng minh tập nguồn đã thống nhất. Điểm retrieval/reranking cũng chưa có contract để quyết định đủ evidence cho từng câu hỏi.

**Đề xuất:** Phân biệt kiểm tra deterministic (phạm vi, năm, đơn vị, mapping ID, exact fact) với kiểm tra ngữ nghĩa có sai số. Tạo conflict/review record ở lúc chuẩn bị release cho các key đã quản lý, và buộc router đọc record đó. Những chủ đề chưa có kiểm soát này cần giới hạn trả lời rõ. Nếu dùng model judge cho support, ghi version, lỗi có thể gặp và bộ kiểm định riêng.

**Tiêu chí bổ sung:** Hai nguồn có deadline khác nhau vẫn dẫn tới `conflicting_sources` khi chỉ một nguồn lọt top-k. Câu trả lời đúng chủ đề nhưng thiếu ngoại lệ quan trọng không được coi là đủ evidence. Evidence ID đúng nhưng claim diễn giải ngược nghĩa phải bị phát hiện trong eval.

### R06 — A: Các ngưỡng chất lượng cần protocol đo trước khi trở thành release gate

**Căn cứ:** [01, KPIs](../01-product-overview.md) dòng 91–103; [02, release gates](../02-prd.md) dòng 137–142; [04, gold và metrics](../04-ai-rag-architecture.md) dòng 122–137.

**Tác động:** 100–200 câu chia nhiều nhóm có thể để lại rất ít case cho mỗi nhóm. Ví dụ 20 câu unanswerable thì một lần trả sai vẫn tương ứng 95% correct abstention. Accuracy và citation support chưa chốt đơn vị đếm, tiêu chí partial credit hoặc người phân xử. “0 lỗi critical” đã có, nhưng chưa định nghĩa severity và bộ case bắt buộc.

**Đề xuất protocol:**

- Tách tập dùng để tune khỏi tập kiểm định giữ lại; chống trùng/paraphrase gần trùng giữa hai tập. Cố định source snapshot và cấu hình khi so sánh.
- Định nghĩa Recall@5 theo evidence unit: tìm được ít nhất một nguồn hay đủ mọi nguồn cần thiết cho câu nhiều phần.
- Tách citation support khỏi citation coverage; một claim có nguồn đúng không bù cho nhiều claim thiếu nguồn.
- Đo đúng đáp án trên answerable set và tỷ lệ từ chối nhầm; đo correct abstention trên unanswerable set. Chatbot từ chối mọi câu không được đạt gate.
- Có nhóm riêng: sai năm/đợt, điều kiện có ngoại lệ, số liệu/ngày, tài liệu cập nhật một phần, multi-turn đổi năm/ngành, bảng lỗi, prompt injection.
- Công bố mẫu số từng nhóm, raw counts, severity rubric, cách human review và mức bất định; tỷ lệ tổng chỉ là một phần báo cáo.
- Giữ các mục tiêu 95%/98%/90% là proposal; freeze tiêu chí sau baseline PoC và trước đo tập kiểm định. Mọi thay đổi ngưỡng cần lý do và version.

**Tiêu chí bổ sung:** Eval runner cho thấy được lỗi critical dù điểm trung bình đạt; không thay ground truth hoặc hạ gate chỉ để một model được chọn đạt chuẩn.

### R07 — A: Vòng phụ thuộc phê duyệt ADR và phạm vi reranker chưa nhất quán

**Căn cứ:** [ADR-001, validation before Accepted](../decisions/ADR-001-technology-stack.md) dòng 74–82; [08, phase 0/WP-01](../08-implementation-roadmap.md) dòng 23, 49; [ADR, reranker optional](../decisions/ADR-001-technology-stack.md) dòng 28; [08, WP-09](../08-implementation-roadmap.md) dòng 57.

**Tác động:** ADR chỉ Accepted sau parser/search/DB/cost/frontend proof, nhưng scaffold và các WP tạo proof lại yêu cầu ADR approved trước. WP-09 ghép reranking với validation/citation thành P0, khiến phần được mô tả là optional dễ thành bắt buộc.

**Đề xuất:** Ghi quyết định cho phép thử nghiệm trong phạm vi PoC với stack Proposed; sau kết quả mới quyết định Accepted cho implementation/pilot. Baseline tài liệu có thể phê duyệt quy trình thử nghiệm mà vẫn ghi rõ lựa chọn công nghệ còn có điều kiện. Tách citation/evidence validation bắt buộc khỏi reranker tùy kết quả đo.

**Tiêu chí bổ sung:** Mỗi gate ghi artifact đầu vào, owner, kết quả pass/fail và công việc được phép tiếp tục; không có dependency bắt buộc đi vòng.

### R08 — B: Có workflow phát hành nhưng thiếu cam kết duy trì độ mới và xử lý sự cố nội dung

**Căn cứ:** [01, rủi ro và open questions](../01-product-overview.md) dòng 110, 123; [02, discovery P1](../02-prd.md) dòng 79; [03, stale-content alerts](../03-system-architecture.md) dòng 136.

**Tác động:** Bản đã duyệt vẫn có thể lỗi thời nếu thông báo mới chưa được phát hiện. Đưa auto-discovery sang P1 là hợp lý, nhưng MVP cần quy trình kiểm tra thủ công cụ thể để giữ core promise.

**Đề xuất:** Có owner kiểm tra nguồn, lịch kiểm tra theo giai đoạn tuyển sinh, `last_checked_at`, điều kiện đánh dấu stale, thời hạn nội bộ để triage/cập nhật, kênh tiếp nhận báo sai và quyền emergency unpublish. Không cần tự động crawl toàn bộ ngay P0. Phân biệt thời gian kiểm tra nguồn với thời gian publish knowledge.

**Tiêu chí bổ sung:** Diễn tập một thông báo đổi hạn nộp: phát hiện → khóa thông tin bị nghi sai → review → eval → release → kiểm tra lại câu hỏi. UI hiển thị phạm vi dữ liệu đã xác minh và lần kiểm tra, không hứa “mới nhất” dựa vào timestamp ingest.

### R09 — B: Privacy mới bao phủ logs rõ hơn luồng dữ liệu hội thoại

**Căn cứ:** [02, FR-01/12 và AC-09](../02-prd.md) dòng 61, 72, 111; [03, conversation contract](../03-system-architecture.md) dòng 73, 91; [07, privacy](../07-engineering-standards.md) dòng 153.

**Tác động:** Không lưu raw chat lâu dài vẫn phải quyết định session context nằm ở đâu, tồn tại bao lâu và ai đọc được. Mask trong log không đồng nghĩa nội dung người dùng đã được giảm thiểu trước khi gửi cho model/embedding provider. Conversation ID chưa phải bằng chứng quyền truy cập một phiên.

**Đề xuất:** Bổ sung data-flow nhỏ cho browser → API/session → classifier/embedder/generator → telemetry/backup. Chốt dữ liệu gửi từng provider, retention/session TTL, reset/xóa, session ownership và ranh giới giữa trace metadata với transcript. Những quyết định privacy phải hoàn tất trước pilot theo chính sách được duyệt; báo cáo này không xác nhận nghĩa vụ pháp lý cụ thể.

**Tiêu chí bổ sung:** Session A không đọc/tiếp tục session B khi biết ID; nhập CCCD không rò vào logs/telemetry đã cấu hình; kiểm tra riêng payload gửi provider theo policy đã chọn. Nội dung assistant cũ chỉ là ngữ cảnh hội thoại, không được nâng thành evidence của lượt mới sau khi nguồn bị thu hồi.

### R10 — B: Cần gate xác nhận giá trị sản phẩm, tránh North Star thiên lệch về người có phản hồi

**Căn cứ:** [01, problem assumptions/North Star/research](../01-product-overview.md) dòng 19–27, 91, 123; [06, usability](../06-ui-ux-specification.md) dòng 137–143; [08, phase plan](../08-implementation-roadmap.md) dòng 23–27.

**Tác động:** Tài liệu đã thẳng thắn coi nhu cầu là giả định, nhưng nghiên cứu chưa có exit gate sớm. Verified task resolution dựa vào phản hồi xác nhận có nguy cơ chỉ phản ánh nhóm chủ động trả lời và nhóm được audit.

**Đề xuất:** Chốt 3–5 tác vụ ưu tiên qua nghiên cứu ban đầu, ví dụ tìm đúng điều kiện, tài liệu áp dụng và bước tiếp theo. So sánh với hành trình dùng nguồn AGU trực tiếp/FAQ trên cùng tác vụ; đo đúng kết quả, thời gian, hiểu năm/nguồn và quyết định tiếp theo. Thực hiện trước khi đầu tư sâu UI mở rộng.

**Tiêu chí bổ sung:** Báo riêng task completion, độ đúng qua audit, feedback response rate và audit coverage. Nêu mẫu số và cách chọn mẫu. Nhóm thử nhỏ hữu ích để tìm vấn đề, chưa đủ để khẳng định một tỷ lệ thành công đại diện toàn bộ người dùng. Trường hợp từ chối đúng kèm hướng dẫn có ích cần rubric task resolution riêng.

### R11 — B: Timeline, tải và ngân sách chưa tạo thành kế hoạch pilot đo được

**Căn cứ:** [02, NFR-03/10](../02-prd.md) dòng 120, 127; [08, estimates](../08-implementation-roadmap.md) dòng 8, 17, 23–27.

**Tác động:** Bảng phase hiện trải đủ tuần 1–16; chưa có đường 12 tuần hoặc giả định effort/overlap. TTFT ≤3 giây chưa gắn concurrency, network, context length, cache và bước kiểm chứng. Budget alarm không tự chặn được chi phí vượt trần.

**Đề xuất:** Giữ 12–16 tuần là khoảng dự báo có điều kiện, bổ sung giờ làm/tuần, corpus coverage, công việc song song thực tế và contingency. Nếu chưa có, dùng 16 tuần làm lịch tham chiếu của bảng hiện tại. Chốt expected traffic/concurrency, token/context caps, ngân sách tháng/ngày, hard cap và hành vi khi hết quota. Đo riêng retrieval, rerank, verification, first validated content và full completion.

**Tiêu chí bổ sung:** Load report ghi cấu hình và trạng thái warm/cold/cache; đo cả lỗi/timeout. Khi hết budget, ứng dụng vẫn hiển thị kênh tra cứu chính thức và trạng thái đúng; không lặp request vô hạn. Uptime app và khả năng trả lời có phụ thuộc AI cần cách đo rõ.

### R12 — B/C: Một số chi tiết UX và traceability chưa đồng bộ với priority

**Căn cứ:** [02, J1/FR-17/20](../02-prd.md) dòng 36–38, 77, 80; [06, feedback/year/source UX](../06-ui-ux-specification.md) dòng 69–73, 139; [03, public answer schema](../03-system-architecture.md) dòng 88–104.

**Đề xuất chỉnh nhỏ:**

- Chốt feedback tối giản là P0 hay P1: J1/UX đã mô tả ngay MVP nhưng FR-17 đang P1. Analytics nâng cao vẫn P1. Tương tự, link AGU tối thiểu khi abstain nên là P0; workflow escalation mở rộng có thể P1.
- Quy định precedence giữa năm trong câu hỏi, year selector và ngữ cảnh cũ; thêm case đổi năm/ngành trong cùng phiên và reset context.
- Citation URL có thể giữ nguyên trong khi file nguồn thay đổi. UI/metadata nên cho biết phiên bản/checksum hoặc ngày lấy nguồn đang được trích; không cần công khai file lưu trữ nếu điều kiện sử dụng chưa cho phép.
- Tránh biến ngày/tháng không có giờ thành một timestamp chính xác tự suy ra. Bảo toàn độ chính xác của mốc nguồn công bố và hỏi/xác minh khi cần giờ hết hạn.
- Khi triển khai accessibility, thay từ “cơ bản/đủ lớn” bằng tiêu chí kiểm thử cụ thể, kiểm tra mobile keyboard, focus, source drawer và screen reader trên sản phẩm thật. Chưa có mockup/UI để đánh giá visual hoặc xác nhận WCAG.

## 4. Nhận xét cho năm nhóm quyết định Proposed

| Nhóm | Nhận xét review | Điều kiện cần ghi trong quyết định |
|---|---|---|
| Technology Stack | FastAPI + Next.js + PostgreSQL/pgvector là lựa chọn hợp lý để đưa vào PoC; chưa có bằng chứng để tuyên bố tối ưu | Skill của người vận hành, hosting/cost, corpus, auth; Docling phải thử trên bảng/scan AGU; LlamaIndex chỉ dùng phần có ích qua adapter |
| RAG Architecture | Giữ baseline dense, thử hybrid và exact matching; reranker có điều kiện | Chốt R01–R06; đo contribution trên tập giữ lại và chi phí/latency; tránh đồng nhất retrieval score với độ tin cậy |
| Data Governance | Giữ review, raw versioning, atomic release, rollback | Thực thi partial supersession, release/index compatibility, revocation, freshness và incident owner |
| Quality Metrics | Giữ các con số làm giả thuyết ban đầu | Chốt protocol/mẫu số/risk tiers, false abstention, citation coverage, holdout và định nghĩa critical; chưa coi target là benchmark đạt được |
| MVP/P1 và 12–16 tuần | MVP có định hướng phù hợp nhưng cần giảm độ rộng trong khi giữ các control bắt buộc | Facts tối thiểu theo chủ đề P0, reranker tùy đo; sửa vòng ADR; nêu effort/budget và đường rút scope |

Đối chiếu tài liệu kỹ thuật chính thức cho review:

- pgvector có exact nearest-neighbor mặc định; ANN là đánh đổi recall/tốc độ. Với approximate index, metadata filtering sau scan có thể làm giảm số kết quả. Vì vậy PoC corpus nhỏ nên đo exact trước, và benchmark filter theo năm/release riêng khi dùng ANN; đây là khuyến nghị suy ra từ [pgvector: Indexing và Filtering](https://github.com/pgvector/pgvector#filtering), chưa phải kết quả trên corpus AGU.
- [FastAPI: Background Tasks, Caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat) phân biệt tác vụ nhỏ trong process với heavy background computation. Worker parsing riêng của thiết kế có cơ sở; lựa chọn DB jobs vẫn cần kiểm chứng recovery/idempotency, không mặc nhiên phải thêm Celery/Redis.
- [Docling: Supported formats](https://docling-project.github.io/docling/usage/supported_formats/) xác nhận hỗ trợ các định dạng đầu vào liên quan. Việc hỗ trợ định dạng không chứng minh độ chính xác OCR/bảng tiếng Việt AGU.

Truy cập trực tiếp cổng tuyển sinh AGU qua công cụ web trong lần review trả 403; không kết luận đã kiểm chứng nội dung tuyển sinh hiện hành hoặc quyền sử dụng nguồn.

## 5. Các chỉnh sửa trước khi đề nghị baseline 1.0

| Vòng | Tài liệu | Thay đổi cần thống nhất |
|---|---|---|
| 1 — Nghiệp vụ | 01 → 02 | Chủ đề/corpus MVP, facts P0 tối thiểu hoặc fallback rõ, task research, metric definitions, feedback/escalation priority |
| 2 — Kiến trúc/AI | ADR-001 → 03 → 04 → 05 | Quyền làm PoC với Proposed stack; release/index/lifecycle/revocation; temporal/partial scope; evidence/support/streaming contract; eval protocol |
| 3 — Triển khai | 06 → 07 → 08 | UX năm/nguồn và candidate-release eval; data-flow/session/privacy; ownership/freshness; dependencies, conditional reranker, resource/budget assumptions |

Baseline nên ghi quyết định đã chốt, quyết định còn có điều kiện, owner và gate xác minh của từng quyết định. Có thể phê duyệt thiết kế thử nghiệm trước khi có benchmark; không đổi nhãn benchmark hoặc công nghệ sang “đã kiểm chứng” chỉ vì tài liệu được duyệt.

Sau khi thống nhất các mục A, các mục B được đưa thành acceptance criteria/work packages trước public pilot. Chưa có cơ sở để tự nâng bộ tài liệu sang Approved Baseline trong lần review này.
