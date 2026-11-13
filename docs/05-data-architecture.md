# AGU Admission Assistant — Data, Knowledge Governance & Operations

| Thuộc tính | Giá trị |
|---|---|
| Phiên bản | 0.9 — Baseline Candidate |
| Ngày | 2026-11-08 |
| Phạm vi | Ingestion, facts, applicability, release/index, privacy và content operations |
| Approval / evidence | Theo [00](00-baseline-decisions.md); raw identity/private packet có foundation tests, serving/lifecycle chưa được kiểm định |

## 1. Nguyên tắc và identity

Raw bytes bất biến, parsing không đồng nghĩa truth, indexing không đồng nghĩa publish. Dùng units đủ nhỏ để kiểm duyệt/sửa đổi mà không mất ngữ cảnh. Dữ liệu public chỉ đi qua release manifest và current safety policy.

| Entity | Identity / trách nhiệm |
|---|---|
| source | URL/publisher/provenance; một URL có thể đổi bytes |
| document | Văn bản logic, số quyết định/title/year nếu đã xác minh |
| document_version | Raw bytes revision: document + SHA-256, original URL và retrieved_at |
| content_revision | Parsed/curated IR revision: raw version + parser/normalization/edit config digest |
| evidence_unit | Các spans/table cells cùng revision, đủ ngữ nghĩa/scope; có review/quality |
| fact_revision / rule_card_revision | Typed assertion hoặc nội dung điều kiện đã duyệt, provenance tới units |
| index_version | Embedding/model/dimension/chunking/normalization và tập chunks bất biến |
| knowledge_release | Manifest units/facts/rule cards/conflicts/coverage đã duyệt |
| runtime_config | Router/retrieval/generator/verifier/prompt/version/limits |
| serving_bundle | knowledge_release + compatible index_version + runtime_config |

Raw không bị sửa khi curator sửa transcription. Sửa IR/fact/scope đã approved tạo revision mới, có actor/reason/diff và re-review; không mutate evidence đang được citation. Re-embedding không tạo raw version giả mới; tạo index version riêng.

## 2. Source inventory và parsing

Nguồn ứng viên: [cổng tuyển sinh AGU](https://tuyensinh.agu.edu.vn/), trang ngành và thông báo/file tuyển sinh công khai. Manifest: source_id, canonical_url, publisher, source_type, discovered/retrieved_at, HTTP etag/last_modified, SHA-256, MIME, license_review_status, crawl_status, last_checked_at và người kiểm tra.

Crawler HTTPS/domain/path allowlist; kiểm tra DNS/private IP/redirect mỗi hop; size/time/rate limits và điều kiện truy cập. Không bypass access restriction hoặc đưa nguồn thứ cấp chưa thẩm định vào facts. Không công khai private object storage để thay thế citation URL. Xác nhận quyền lưu/xử lý/tái phân phối ở G4; link công khai không tự chứng minh mọi quyền này.

| Loại | Parser đầu tiên | QA |
|---|---|---|
| HTML | Trafilatura/BeautifulSoup + site rules | Body/headings/tables, bỏ menu/lặp |
| Digital PDF | Docling standard layout | Text vs render, trang/bảng/chú thích |
| Scan PDF | Docling + OCR mode được chọn qua PoC | Dấu tiếng Việt, mã/ngày/số, merged cells |
| DOCX | Docling hoặc python-docx fallback | Heading/bullets/merged cells/footnotes |
| XLSX | Sau MVP nếu có requirement riêng | Typed cells/formulas/units, không tự mở scope |

Defaults upload/parser theo 03. Parser sandbox không thực thi macro, external entities hoặc fetch tài nguyên nhúng tùy ý. OCR confidence là tín hiệu review, không đủ để approve truth. [Docling supported formats](https://docling-project.github.io/docling/usage/supported_formats/) hỗ trợ chọn parser, không chứng minh chất lượng trên corpus AGU.

## 3. Workflow và các trạng thái độc lập

Không dùng một enum lifecycle gộp approval/publication/processing.

| Dimension | Trạng thái |
|---|---|
| Job processing | queued/running/succeeded/failed/quarantined/cancelled, stage riêng |
| Revision/unit/fact review | pending/approved/rejected, actor/reason/timestamp |
| Quality | pass/blocked, issue severity và affected spans |
| Candidate release | building/ready_for_eval/evaluated/approved/retired |
| Publication | Membership của immutable release + active_bundle pointer; không mutate global document thành published |
| Safety | Global revocation/current-use exclusion riêng, có epoch và scope |

Download → immutable raw → parse/normalize IR → metadata/scope extraction → QA/review → eligible units/facts → chunk/embed/index → candidate manifest → eval → release approval → atomic activate → smoke. Failures không phá bundle đang phục vụ.

Review screen có original/IR/table side-by-side, cells/spans, warnings, applicability, facts/rule cards, version diff và affected topics. Reviewer thấy nội dung trước khi chia chunk; embedding có thể tính trước để thử nhưng không tạo eligibility. Approve facts không tự approve mọi đoạn khác cùng file.

## 4. IR, units và chunking

IR giữ document_version_id, content_revision_id, source_url, checksum, parser/config, blocks/tables, page/section/bounding locations, text gốc và QA issues. Không gộp PDF thành một text stream khi có bảng/điều khoản.

Mỗi unit có unit_id, revision_id, source_locations[], text/table representation, logical_key hoặc rule_topic, applicability, required_context_unit_ids, review_status, quality_status và reviewer. Block/unit ngoài scope hoặc OCR sai phải được đánh dấu blocked trước khi tạo public chunks. Nếu không thể tách phần lỗi an toàn, chặn cả section hoặc revision.

Chunk section-aware khoảng 300–600 tokens, overlap 50–100 chỉ khi chia prose dài; các con số là initial dev config, không benchmark tối ưu. Giữ unit_ids trên chunk; parent expansion chỉ lấy units eligible của cùng revision, không dùng parent text thô để bypass mask. Không cắt bảng thiếu header/chú thích; normalize tìm kiếm không sửa nội dung evidence. Exact code/value dùng facts, không dựa độ gần vector.

Nếu unit chứa cả phần bị sửa và phần còn hiệu lực, tách/review unit trước release; không dùng filter theo document_version duy nhất. Dedupe không được trộn năm/đợt hoặc xóa provenance của nguồn hỗ trợ.

## 5. Applicability và facts P0

Applicability có academic_year, program_type, major_scope, method_scope, audience_scope, round_scope và effective interval/date precision khi nguồn công bố. Mỗi scope dùng all/specific/unknown cùng values khi specific. Null là unknown; all chỉ khi reviewer xác nhận. Global rule không phụ thuộc năm có year_scope=all được xác minh riêng; không biến mọi null year thành all.

Nguồn nhiều hệ đào tạo được phân loại từng unit/table. Query cho một đợt lấy all-rounds cùng specific phù hợp; unknown không tự hợp lệ. Khác value ở scope không chồng lấn không là conflict; nếu query thiếu chiều phân biệt cần clarify.

Typed facts tối thiểu: major_code/name/aliases, combination, quota, tuition, deadline theo coverage; không bắt buộc nhập đủ mọi ngành trước pilot. Fact record có logical key, fact_type, typed value schema, unit/currency/basis, applicability, precision, source_unit_ids, review status. Mỗi fact_type có JSON schema và accessor whitelist, không JSONB tự do/text-to-SQL.

- Tiền: decimal, currency, per_credit/per_term/per_year và phạm vi áp dụng; không tự quy đổi khi thiếu quy tắc.
- Deadline: local date hoặc aware datetime, timezone nếu có căn cứ; date-only giữ date-only, không tự gán 23:59.
- Quota/code/combination: typed values và scope; 0 là giá trị thật, unknown không lưu 0.
- Rule card: câu giải thích do reviewer duyệt, required conditions/exceptions, applicability và supporting units. Kết luận cá nhân đủ điều kiện/trúng tuyển luôn ngoài phạm vi.

Extraction/LLM chỉ đề xuất pending records. Manual curation là đường P0 chính thức. Facts/rule cards được validate cùng evidence: source bị blocked/revoked thì record phụ thuộc cũng không eligible. Review từng critical cell với original, không chỉ đo text similarity.

## 6. Temporal semantics, supersession và conflict

Phân biệt source_published_at, effective_from/until, deadline, retrieved_at, last_checked_at và knowledge_activated_at; các trường không được copy mặc định cho nhau.

P0 query_use là latest_for_year: thông tin được xác minh gần nhất áp dụng cho năm hỏi. Với coverage đang hoạt động, reference_date là ngày Việt Nam của request; với historical, year catalog giữ reference_date và tập quy định cuối kỳ do curator duyệt. Đây là mốc của bản tri thức, không cho người dùng tùy ý chọn ngày để dựng lại lịch sử. Historical không cho phép dùng giá trị đã bị sửa trong tập quy định đó; không lọc toàn bộ lịch sử bằng effective_until < ngày hôm nay. UI ghi năm/reference date/lần kiểm tra, không suy ra đang mở tuyển sinh.

Supersession edge: old_unit/fact → new_unit/fact, applicability, effective date/precision, reason, confirmed_by/at. A chứa điều kiện + deadline, B sửa deadline: manifest chọn điều kiện của A + deadline B; old deadline bị current-use exclusion scoped theo năm/đợt. Trong P0, current-use exclusion áp dụng mọi latest_for_year answer kể cả năm được gắn nhãn historical. Không hard-delete A.

Activation B atomically cập nhật bundle và các current-use exclusions đã duyệt, tăng policy_epoch. Thời điểm activate khác thời điểm supersession áp dụng: nếu B có hiệu lực tương lai, A vẫn dùng đến cutover đã xác minh, B được đánh dấu scheduled và không mô tả là đang có hiệu lực. Manifest giữ applicability/reference-date conditions của cả hai; exclusion chỉ áp khi điều kiện thời gian của edge thỏa. MVP có thể dẫn nguồn thông báo sắp áp dụng bằng rule card có nhãn, không trộn giá trị scheduled vào đáp án hiện hành. Chưa rõ ngày/đợt áp dụng thì chặn kết luận/clarify, không lấy ngày đăng làm ngày hiệu lực. Deadline tương lai là giá trị hợp lệ, không phải lý do loại fact. Date-only cutover so theo ngày Việt Nam, không tự tạo giờ hết hạn.

Final eligibility kiểm tra lại reference date/effective conditions; nếu request đi qua cutover làm thay đổi evidence, trả knowledge_changed thay vì phát kết quả cũ. Rollback không bỏ exclusions; nếu bundle A thiếu B sau cutover thì abstain thay vì trả giá trị cũ. Unaffected rules vẫn dùng được.

Conflict registry keyed bởi logical key/rule topic + overlapping applicability, có involved unit/fact IDs, resolution_status, reason/reviewer. So toàn candidate manifest trong QA; unknown applicability hoặc mâu thuẫn chưa xử lý không được đánh dấu topic covered cho confident answer. Runtime đọc registry ngoài top-k. Không tự coi nguồn mới hơn là đúng; release có unresolved conflict chỉ được expose state conflict ở topic đó.

## 7. Logical schema và storage

| Table/group | Các khóa/constraints chính |
|---|---|
| sources/documents/document_versions | Canonical URL/logical document identity; unique document + raw checksum; provenance |
| content_revisions/blocks/units | Raw version FK; revision config digest; source locations; immutable approved revisions |
| admission_facts/rule_cards/aliases | Typed schema + scope + evidence FKs; versioned approved records |
| document_chunks/chunk_embeddings | Chunk → unit IDs; unique chunk + index_version; model/dimension không trộn |
| index_versions/runtime_configs | Immutable config/model hashes; compatible query embedder |
| knowledge_releases/release_units/release_facts/release_conflicts | Manifest checksum, explicit members, coverage matrix |
| serving_bundles/system_state | FK release/index/runtime; active_bundle_id và policy_epoch transactionally controlled |
| safety_overrides/supersession_edges | Unit/source/fact scope, blocked use/effective conditions, reason/actor/time; không phụ thuộc rollback |
| review_tasks/publication_events | Actor/action/reason/diff/QA/eval audit |
| ingestion_jobs/job_attempts/artifacts | Stage identity, lease/fencing, attempts, unique idempotency keys |
| evaluation_cases/runs/results | Dataset/source/config IDs, labels/raw counts/errors |
| usage_reservations/usage_events/feedback | Quota accounting và safe metadata; không raw chat |

PostgreSQL vector + pg_trgm; FTS simple, normalized aliases/exact/trigram cần dev benchmark. Scope/year/review/index fields dùng columns/constraints/FKs, không chỉ JSON metadata do client cung cấp. Index embeddings theo model/dimension bằng table/namespace tương thích; chọn migration cụ thể khi chọn embedder. Không đưa DDL vector(1024) minh họa thành dimension mặc định.

Raw object paths là private/versioned; download URL public trả metadata/canonical source link. Link có thể đổi bytes: citation giữ raw checksum/version, retrieved_at và location; khi phát hiện changed source, UI cảnh báo sự khác biệt. Không thay evidence đã dùng bằng file mới cùng URL.

## 8. Candidate release và atomic activation

1. Đóng băng units/facts/rule cards/conflict/coverage manifest và index/runtime tương thích.
2. QA: no draft/blocked/out-of-scope/unknown critical scope, provenance đầy đủ; topic conflict phải có state explicit.
3. Eval candidate trước public: targeted affected topics + toàn critical suite; full holdout khi thay AI/parser/chunking hoặc coverage lớn theo 04.
4. Reviewer approve candidate với report IDs/checksums; publisher activate bundle trong transaction có optimistic check pointer/epoch.
5. Smoke sau activate; rollback/restrict nếu lỗi. Approval stale do candidate edit phải chạy lại kiểm định liên quan.

Eligibility public là intersection release members + approved/quality-passed units + query applicability + safety overrides/freshness. Document status đơn lẻ không override kết quả. Final guard và điểm phát hành theo 03. P0 không cache answers/retrieval; query embedding cache chỉ thêm khi có scope/budget/privacy assessment.

## 9. Jobs và reprocessing

Idempotency theo artifact stage: raw download checksum; parse key(raw_version, parser/config); curation revision digest; chunk key(revision, chunk config); embeddings key(chunk, index/model config). Retry không duplicate; đổi một config tạo artifact identity mới thay vì ghi đè.

Worker claim SKIP LOCKED, commit rồi xử lý; lease 60 giây, heartbeat 20 giây, fencing token mỗi claim. Lost lease không được commit stage output. Reaper reclaim expired lease; max attempts 3 cho transient failures, backoff/jitter. Permanent QA/scope errors quarantine, không retry vô hạn. Storage write có checksum/idempotent key; orphan cleanup chỉ xóa unreferenced artifacts theo retention và kiểm tra path/ownership.

Giới hạn file/pages/CPU/RAM/time; worker timeout và max parse duration cấu hình sau PoC. Cần test worker crash giữa raw/parse/embed và transaction commit, không chỉ happy retry. Retry provider phải giữ usage accounting, không phát sinh generation lặp không kiểm soát.

## 10. Data-flow và session privacy P0

| Bước | Dữ liệu được dùng | Lưu trữ / boundary |
|---|---|---|
| Browser | Input/transcript người dùng đang nhìn | Chỉ memory trong tab; reload/reset mất lịch sử, không localStorage mặc định |
| API ingress | Raw input ngắn hạn để kiểm tra/redact | Không request-body logs; định danh nhạy cảm rõ thì yêu cầu gỡ trước model |
| Session context | Entities/year + tối đa 2 user turns đã giảm thiểu, tổng 4.000 ký tự | Memory của một API instance; không assistant prose làm evidence; không backup |
| Classifier/embedder/generator/verifier | Chỉ câu/context đã giảm thiểu và evidence cần thiết | Không raw session cookie/PII/secrets; không tạo provider thread/history mặc định |
| Telemetry/usage/feedback | IDs/config/evidence refs/status/timing/token/cost/reason codes | PostgreSQL metadata; không raw prompt/answer/transcript |

Một API instance là mặc định pilot; restart làm mất anonymous context và UI giải thích tạo phiên mới. Multi-replica session store là thay đổi sau sizing/retention review, không thêm Redis chỉ để dự phòng. Server session idle TTL 30 phút, absolute TTL 24 giờ; kiểm tra expiry ở mọi read, cleanup memory định kỳ tối đa 5 phút. Opaque 256-bit random credential HttpOnly/Secure/SameSite, bound conversation; ID một mình không cấp quyền. Reset xóa memory và rotate credential. Không giữ chat trong DB mặc định.

PII minimization dùng rules/heuristics và không bảo đảm phát hiện tuyệt đối. CCCD/điện thoại/email rõ bị chặn hoặc redact trước các provider; nếu không thể giữ nghĩa an toàn thì hỏi người dùng bỏ định danh. Provider terms, logging/training use, retention và region phải qua G3; không tự khẳng định zero retention nếu chưa xác minh. SDK/APM/edge logs phải kiểm tra riêng, không chỉ app logger.

Không thu public chat làm eval/training hoặc ghi diagnostic payload mặc định. Nghiên cứu usability dùng script/consent và dữ liệu thử đã duyệt; báo audit coverage thật. Trace không có prompt/answer chỉ tái lập config/evidence, không hứa tái tạo nguyên văn phản hồi lỗi. Feedback có thể thiếu thông tin để tái hiện; operator ghi giới hạn thay vì suy diễn nội dung đã mất.

## 11. Retention và backup defaults

Đây là policy kỹ thuật của candidate để PO rà soát trước G3/G4, không mô tả thời hạn pháp luật bắt buộc.

| Dữ liệu | Mặc định |
|---|---|
| Anonymous context/browser transcript | Theo TTL/memory ở §10, không backup |
| App trace/usage metadata | 30 ngày; tổng hợp không định danh để dự báo cost nếu được duyệt |
| Feedback codes/request refs | 90 ngày; request ref hết trace có thể không replay được |
| Security rate-limit keys | Pseudonym HMAC IP xoay hằng ngày, tối đa 24 giờ; không IP raw trong app DB |
| Knowledge raw/IR/facts/releases/audit/safety journal | 36 tháng sau lần tham chiếu cuối; giữ lâu hơn nếu active/historical release hoặc safety policy còn tham chiếu; không expiry một block đang có hiệu lực |
| Backups DB/knowledge objects | Rolling 30 ngày; restore áp dụng lại TTL và safety overrides mới nhất trước mở traffic |

Giữ ít nhất active và 2 bundle trước tương thích để thử rollback, nhưng số lượng giữ không tự bảo đảm chúng an toàn để activate. Khi có yêu cầu gỡ hợp lệ/điều kiện nguồn thay đổi, PO xác định phạm vi purge và backup expiry, ghi audit tối thiểu được phép; không hứa xóa tức thì khỏi mọi backup. Không restore phiên/chat vốn chỉ ở memory.

Backup bao gồm DB/objects/manifests/runtime configs/overrides; secrets quản lý riêng. Safety journal là các event block/current-use exclusion và incident record bất biến trong private object storage đã có, độc lập primary DB và không bị quay về bản cũ khi restore DB. Ghi event ID/checksum/scope/effective conditions trước khi xác nhận mutation thành công; replay bảo thủ có thể giữ một block dư, không tự mở lại nguồn từ event chưa được review. Không ghi chat/PII vào journal. Nếu journal không ghi được, block/suspend public guidance trước, giữ trạng thái chưa hoàn tất để maintainer xử lý; không tiếp tục serving với policy chưa đồng bộ.

Restore luôn đóng public AI serving bằng deployment/recovery control, không tin cờ enabled trong DB backup. Maintainer đối soát snapshot với journal/incident records mới hơn backup, replay các blocks/exclusions, kiểm tra completeness và re-review affected coverage trước khi mở. Không chứng minh được policy mới nhất thì giữ affected coverage bị chặn; nếu không xác định được phạm vi ảnh hưởng thì giữ toàn bộ public AI đóng. Không tự replay unblocking events để mở nguồn. Khi cả DB và journal không còn đủ bằng chứng, full coverage re-review là điều kiện mở lại, không hạ gate để đạt RTO.

RPO/RTO theo 03; restore rehearsal bắt buộc có revoke sau thời điểm backup rồi mất DB, và phải chứng minh nguồn đó vẫn bị chặn. RPO 24 giờ cho dữ liệu không có nghĩa cho phép quên lệnh thu hồi đã xác nhận.

## 12. Freshness và incident runbook

Content operator có tên/coverage calendar trước G4; PO quyết định peak_mode. Default peak_mode=true cho chủ đề có thể ảnh hưởng kỳ đang mở. Kiểm tra nguồn trong coverage ít nhất mỗi 24 giờ ở peak; tối đa 7 ngày ở off-peak. last_checked_at chỉ cập nhật sau kiểm tra bản nguồn/changes, không sau embedding hoặc publish. Nếu không đáp ứng lịch, chuyển topic stale.

Stale high-risk current guidance → insufficient_evidence/stale_knowledge và official link. Historical answer chỉ dùng bản đã QA, nhãn year/last checked/không hiện hành; không cho lịch sử bypass revocation/supersession. Không quảng bá “mới nhất” chỉ từ lần ingest.

Khi phát hiện/báo sai critical: chặn affected current use trước khi tiếp tục review, mục tiêu trong 4 giờ **trong cửa sổ có operator**; xác minh/dựng candidate trong 1 ngày làm việc nếu có nguồn rõ, nếu chưa thì giữ block. Không cam kết trực 24/7. Nếu không bố trí được operator, tạm dừng current guidance và giữ tra cứu lịch sử/official links phù hợp.

Incident record: issue/time/source/topic/severity/affected units & releases, người xử lý, block/epoch, cách xác minh, eval report, quyết định mở lại. Feedback P0 bằng code; /help có kênh báo sai do PO chọn trước G4, không tự gửi email/tin cho AGU hoặc người dùng.

## 13. Evidence phải có trước pilot

Golden parse set 15–30 tài liệu và critical-cell QA; mixed-program isolation; all/specific/unknown round; partial/future-effective supersession và cutover; source URL đổi bytes; unit block trên mọi route/parent; job crash/retry/fencing; candidate atomic activation; re-embedding/rollback giữ current exclusions; in-flight revoke/final guard; session isolation/TTL/reset; provider payload minimization; restore sau revoke mới hơn backup, retention và freshness/incident drill.

[02 AC](02-prd.md), [03 serving/API](03-system-architecture.md), [04 evaluation](04-ai-rag-architecture.md), [08 gates](08-implementation-roadmap.md) quyết định bộ kiểm chứng tương ứng. Các evidence này chưa tồn tại trong candidate.
