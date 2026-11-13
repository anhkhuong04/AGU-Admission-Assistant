# G1 input handoff — sau foundation

Foundation chưa đạt G1. Nguồn chuẩn: [08 gates](../08-implementation-roadmap.md), [05 data](../05-data-architecture.md), [04 evaluation](../04-ai-rag-architecture.md). Chưa có nguồn thật/rights record, human-approved facts, nghiên cứu người dùng hoặc gold dataset trong repo.

## Source intake packet

Mỗi nguồn cần record các trường dưới; thiếu bằng chứng giữ `unknown/pending`, không tự điền từ năm trên clock hoặc model:

| Nhóm | Fields / evidence |
|---|---|
| Identity | official canonical URL, publisher/owner, logical document ID, real raw SHA-256 và storage locator sau khi có bytes |
| Rights | allowed use, usage/redistribution review status, evidence/decision actor/date; public URL không tự là quyền mirror |
| Times | source publication, retrieval/check time, effective interval/cutover, date precision; không copy mặc định giữa các thời điểm |
| Applicability | year/program/round/method/audience: all/specific/unknown tách rõ, không dùng source khác để chữa scope chưa biết |
| Coverage | 3–5 prioritized tasks; mapping task → units/facts và gaps/official fallback |
| QA | original page/table/row/cell, headers/footnotes/exceptions, OCR warning và ảnh hưởng parent/facts |
| Curation | proposed values/types/units/basis, unresolved questions, assigned human reviewer; không AI signature |
| Operations | freshness owner/calendar, previous/new bytes, change/partial supersession targets có căn cứ |

## Task queue tiếp theo

Các task dưới là **chưa thực hiện**, ước lượng 2–8 giờ mỗi slice; trước coding phải giao inputs/acceptance rõ. Root điều phối, data specialist khi cần; một writer/file.

| Task | Traceability / inputs | Files dự kiến | Acceptance / verification cần xây |
|---|---|---|---|
| Local private raw storage adapter, 4–6h | WP-02/04, FR-08/12; permitted synthetic bytes | `packages/backend/src/agu_backend/storage/`, `tests/integration/test_raw_storage.py` | Atomic immutable write/checksum, retries/orphan cases; không coi DB key là proof object đã lưu |
| Allowlisted source fetch, 4–8h | WP-02, FR-08/12; PO-reviewed URLs/use, raw adapter | `packages/backend/src/agu_backend/ingestion/fetch.py`, `tests/integration/test_source_fetch.py` | SSRF/private IP/DNS+redirect checks, max size/time/MIME, changed bytes AC-10; local HTTP fixtures trước network thật |
| Research/coverage, chia 2–4h mỗi vòng | WP-18, FR-06/20; PO/operator tuyển 5–8 người, không tự gửi tin | `docs/research/`, `tests/fixtures/corpus/manifest.json` | 3–5 tasks có evidence và official-site comparator; coverage 15–30 docs đại diện, gaps có nhãn |
| Parser/IR spike, 4–8h mỗi loại | WP-03, FR-08/16; permitted PDF/HTML có tables/footnotes/mixed scope | `packages/backend/src/agu_backend/ingestion/ir.py`, `services/worker/`, `tests/fixtures/corpus/`, `tests/integration/test_parser_ir.py` | Domain IR/provenance; original critical cells/footnotes được QA; OCR warning chặn affected paths AC-06/18; report lỗi/effort, không chỉ text similarity |
| Verified fact schemas + manual intake, 4–8h mỗi fact type | WP-15, FR-16; inspected originals và reviewer | `packages/backend/src/agu_backend/knowledge/facts.py`, new migrations, `tests/unit/test_fact_rules.py` | Critical type/unit/basis/conditions/aliases/provenance; private packet không thay canonical schema; human review còn riêng |
| Applicability/release policy prototype, chia 4–8h mỗi behavior | WP-05, FR-09/24; units/facts fixtures | `packages/backend/src/agu_backend/knowledge/eligibility.py`, `tests/unit/test_eligibility.py` | AC-03/04/11/19/26 fixtures: conflict whole candidate, draft/OCR isolation, partial replacement, future cutover; không phục vụ public trước complete safety boundary |
| Dev labels và eval protocol, 4–8h mỗi batch | WP-06, FR-10; research/coverage reviewed | `tests/evals/`, dataset manifest/rubric | Gold evidence groups, independent dev/holdout provenance; dev≥60/holdout≥200 ở G2, không tune theo holdout |

G1 cần tổng hợp research/corpus permission/coverage/parser report/manual facts/dev labels và review prototype theo 08. Chưa cần chọn model để làm các slice này. Trước paid model tests phải chốt OD-01 budget/data permission; trước UI feature code phải có wireframes 06. Không triển khai tự động queue này từ việc hoàn tất foundation.
