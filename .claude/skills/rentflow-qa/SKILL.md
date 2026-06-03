---
name: rentflow-qa
description: Phương pháp QA tích hợp RentFlow — so sánh chéo biên API↔UI (Pydantic schema vs dict thật endpoint trả vs field app.js đọc), khởi động app và xác minh hành vi thật, chạy pytest. Dùng BẮT BUỘC khi kiểm tra/nghiệm thu một tính năng, sau khi backend hoặc frontend vừa thay đổi.
---

# RentFlow — QA & Integration Verification

QA của RentFlow tập trung vào **lỗi biên (boundary bugs)** — nơi backend và frontend gặp nhau. Đây là loại bug khó thấy nhất vì mỗi bên đọc riêng đều "đúng".

## Nguyên tắc cốt lõi: so sánh chéo, không chỉ "tồn tại"

Đừng chỉ xác nhận code có mặt. Phải đọc **đồng thời** hai (ba) phía và đối chiếu:

1. **Pydantic schema** `*Read` trong `app/schemas/` — shape khai báo.
2. **Dict thật** mà endpoint trả trong `app/api/v1/endpoints/` — ⚠️ nhiều endpoint RentFlow build dict TAY (vd `/api/bills/`, `/revenue/summary`, `/rooms/{id}/history`) nên **không** bị `response_model` ràng buộc → shape thật là dict này, có thể lệch schema.
3. **Field mà `app.js` đọc** — tìm `fetch('/api/...')` tương ứng và xem nó truy cập `.field` nào trên kết quả.

So từng field: tên có khớp? kiểu có khớp (int/str/bool)? có thể null không và frontend có xử lý null? Lệch bất kỳ điểm nào = bug biên.

## Checklist boundary cho RentFlow

- [ ] Mỗi field `app.js` đọc đều có trong dict thật endpoint trả (đúng tên, đúng cách viết).
- [ ] Field `Optional`/nullable (vd `paid_at`, `contact_info`, `move_in_date`) được frontend xử lý khi null.
- [ ] Số tiền là `int` (VNĐ) — frontend format hiển thị nhất quán.
- [ ] Trạng thái bill chỉ thuộc `unpaid`/`paid`/`prepaid`; `status_map` trong TRANSLATIONS phủ hết.
- [ ] `electricity_type` chỉ `"meter"`/`"fixed"`; UI phân biệt đúng (`is_fixed`).
- [ ] Endpoint ghi dữ liệu có `db.commit()`; đọc lại sau thao tác phản ánh thay đổi.
- [ ] Text hiển thị mới có đủ trong cả 5 ngôn ngữ của `TRANSLATIONS`.

## QA tăng dần (incremental)

Chạy QA **ngay sau mỗi module hoàn thành**, không đợi toàn bộ. Backend xong một endpoint → kiểm shape ngay. Frontend map xong → kiểm khớp ngay. Bắt lỗi sớm rẻ hơn nhiều.

## Xác minh hành vi thật

Ưu tiên chạy thật thay vì chỉ đọc tĩnh:

```bash
# Khởi động app (nền) rồi gọi thử endpoint
python main.py            # hoặc uvicorn app.main:app --reload
curl -s "http://localhost:8000/api/bills/?month=6&year=2026" | head
curl -s "http://localhost:8000/api/rooms/" | head

# Chạy test nếu có
pytest tests/ -q
```

Lưu ý: `tests/conftest.py` hiện là placeholder rỗng, chưa có test thật — nếu `pytest` không có gì để chạy, nói rõ điều đó thay vì coi như pass. App tạo `rentflow.db` (SQLite) và seed dữ liệu mẫu lúc khởi động.

## Báo cáo

Ghi `_workspace/qa_report.md`:
- ✅ **Đã xác minh:** điểm khớp, kèm cách đã kiểm (đọc tĩnh / chạy thật).
- ❌ **Lỗi biên:** mô tả + `file:line` cả hai phía + cách sửa đề xuất.
- ⚠️ **Rủi ro:** điểm chưa chắc chắn, chưa kiểm được.

**Trung thực tuyệt đối:** nói rõ điều gì đã chạy thật, điều gì chỉ đọc. Không khẳng định "hoạt động tốt" khi chưa có bằng chứng. Nếu app không khởi động được, báo lỗi cụ thể.
