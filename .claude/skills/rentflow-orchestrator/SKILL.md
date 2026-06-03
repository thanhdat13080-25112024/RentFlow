---
name: rentflow-orchestrator
description: Điều phối đội agent RentFlow (backend, frontend, QA, reviewer) cho công việc full-stack, UI, và review/sửa lỗi. Dùng khi yêu cầu liên quan phát triển tính năng (API + UI), chỉnh giao diện/dashboard, hoặc review/debug trên RentFlow. Trigger cả các yêu cầu tiếp nối: "làm tiếp", "chạy lại", "cập nhật", "sửa lại phần ...", "review thay đổi", "tìm lỗi", "dựa trên kết quả trước cải thiện". Câu hỏi đơn giản thì trả lời trực tiếp, không cần điều phối.
---

# RentFlow Orchestrator

Điều phối đội agent chuyên biệt của RentFlow theo **chế độ sub-agent** (môi trường này không có TeamCreate/SendMessage). Bạn là người điều phối: phân tích yêu cầu, gọi agent qua tool `Agent` (luôn `model: "opus"`), truyền dữ liệu, tổng hợp kết quả.

## Đội hình

| Agent (`subagent_type`) | Skill | Việc |
|---|---|---|
| `rentflow-backend` | rentflow-backend | API, model, schema, billing, Alembic |
| `rentflow-frontend` | rentflow-frontend | Jinja2, Alpine app.js, tokens, i18n |
| `rentflow-qa` | rentflow-qa | Khớp biên API↔UI, chạy app/test |
| `rentflow-reviewer` | rentflow-reviewer | Review diff, debug có hệ thống |

Người dùng đang học FastAPI → tổng hợp kết quả bằng tiếng Việt, rõ ràng, nêu lý do.

## Phase 0 — Kiểm tra ngữ cảnh (luôn chạy đầu tiên)

1. Kiểm tra `_workspace/` có tồn tại không.
2. Quyết định chế độ:
   - **Chạy mới**: chưa có `_workspace/`, hoặc người dùng đưa yêu cầu mới hoàn toàn → tạo `_workspace/`. Nếu đã có và là việc mới khác hẳn, chuyển `_workspace/` cũ thành `_workspace_prev/`.
   - **Chạy lại một phần**: đã có `_workspace/` + người dùng yêu cầu sửa một phần ("sửa lại UI", "đổi logic billing") → chỉ gọi lại agent liên quan, đọc sản phẩm cũ và cải thiện.
3. Phân loại yêu cầu → chọn pipeline ở dưới.

## Phân luồng theo loại yêu cầu

### A. Tính năng full-stack (API + UI) — pipeline sinh-rồi-kiểm
Thứ tự (có phụ thuộc, chạy tuần tự):
1. `Agent(rentflow-backend, model:"opus")` → hiện thực server, ghi `_workspace/backend_changes.md` (kèm shape JSON).
2. `Agent(rentflow-frontend, model:"opus")` → đọc backend_changes, làm UI + i18n, ghi `_workspace/frontend_changes.md`.
3. `Agent(rentflow-qa, model:"opus")` → so khớp biên + chạy thử, ghi `_workspace/qa_report.md`.
4. Nếu QA báo lỗi 🔴/🟡 → gọi lại agent tương ứng để sửa (1 vòng), rồi QA lại.

### B. Chỉ frontend/UI
1. `Agent(rentflow-frontend, model:"opus")` (nếu cần shape dữ liệu hiện có, agent tự đọc code/`backend_changes.md`).
2. `Agent(rentflow-qa, model:"opus")` kiểm i18n + khớp field + render (nhẹ).

### C. Review / sửa lỗi
- Review thay đổi: `Agent(rentflow-reviewer, model:"opus")` → `_workspace/review_report.md`. Nếu người dùng muốn sửa luôn → gọi backend/frontend áp dụng.
- Debug lỗi: `Agent(rentflow-reviewer, model:"opus")` tìm root cause → gọi agent phù hợp sửa → `rentflow-qa` xác minh đã hết.

> Việc độc lập (vd review 2 module không liên quan) có thể chạy song song bằng `run_in_background: true` rồi thu kết quả.

## Giao thức truyền dữ liệu

- **Return value** (chính): kết quả tóm tắt mỗi agent trả về cho orchestrator.
- **File** `_workspace/` cho sản phẩm trung gian lớn / shape JSON: `backend_changes.md`, `frontend_changes.md`, `qa_report.md`, `review_report.md`. Đặt tên `{phase}_{agent}_{artifact}.md` nếu nhiều bước.
- Giữ lại `_workspace/` để truy vết; chỉ code thật ghi vào cây dự án.

## Xử lý lỗi

- Agent thất bại → thử lại 1 lần. Vẫn lỗi → tiếp tục phần còn lại và ghi rõ phần thiếu trong báo cáo tổng hợp, KHÔNG giả vờ thành công.
- Dữ liệu mâu thuẫn (vd CLAUDE.md vs code) → ưu tiên code thật, ghi chú nguồn, không xóa thông tin.
- QA không khởi động được app → báo lỗi cụ thể, không kết luận pass.

## Quy mô đội

Mỗi tính năng thường 2–3 agent là đủ. Đừng gọi cả 4 nếu yêu cầu chỉ là UI hoặc chỉ review.

## Sau khi xong — tiến hóa h.harness

1. Tổng hợp kết quả cho người dùng (tiếng Việt): đã làm gì, file nào đổi, QA/review nói gì, cần chạy migration không.
2. Mời phản hồi: "Có gì cần chỉnh ở kết quả hoặc cách đội agent làm việc không?"
3. Nếu phản hồi lặp lại ≥2 lần hoặc agent hỏng theo mẫu → đề xuất cập nhật agent/skill và ghi vào bảng **변경 이력 / Changelog** trong `CLAUDE.md` (mục "Harness: RentFlow").

## Test scenario

**Luồng bình thường (tính năng full-stack):** "Thêm tính năng ghi chú cho mỗi phòng" → Phase 0 (chạy mới, tạo `_workspace/`) → backend thêm cột `note` + migration + schema, ghi shape → frontend thêm ô nhập + i18n 5 ngôn ngữ → QA đối chiếu field `note` khớp dict↔app.js, chạy thử → tổng hợp + nhắc chạy `alembic upgrade head`.

**Luồng lỗi (debug):** "Tiền điện phòng 101 tính sai" → Phase 0 (debug) → reviewer tái hiện, lập giả thuyết (sai `unit_price`? new<old? bill đã `paid` nên không cập nhật?), kiểm chứng bằng cách đọc reading + chạy `update_bill`, tìm root cause → backend sửa → QA xác minh lại đúng số. Nếu reviewer không tái hiện được → báo cần thêm thông tin, không đoán.
