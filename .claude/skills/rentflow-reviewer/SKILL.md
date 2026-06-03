---
name: rentflow-reviewer
description: Phương pháp review code & debug có hệ thống cho RentFlow — checklist review riêng (billing, auth/cookie JWT, commit SQLAlchemy, i18n, dict-vs-schema), quy trình debug khoa học (giả thuyết → bằng chứng → kết luận), giải thích cho người mới học FastAPI. Dùng BẮT BUỘC khi review thay đổi/diff hoặc khi truy lỗi/hành vi lạ.
---

# RentFlow — Review & Debugging

Mục tiêu kép: bắt vấn đề THẬT và giúp người dùng (đang học FastAPI) **hiểu tại sao**. Luôn nêu lý do, giải thích bằng tiếng Việt, ví dụ cụ thể.

## Chế độ REVIEW

Phân loại phát hiện: 🔴 bug/nghiêm trọng · 🟡 nên sửa · 🟢 gợi ý. Mỗi mục: vấn đề là gì → **tại sao** là vấn đề → `file:line` → cách sửa.

### Checklist review riêng cho RentFlow

**Billing & dữ liệu**
- `update_bill` chỉ ghi đè bill khi `status == "unpaid"` — thay đổi có vô tình ghi đè bill `paid`/`prepaid` không?
- `update_bill` TỰ `db.commit()`. Handler gọi nó trong vòng lặp có chấp nhận commit từng vòng không? Có double-commit không?
- Tính tiền: `total = rent + service + elec`; elec theo `electricity_type` (`fixed` dùng `fixed_electricity_fee`, `meter` dùng `(new-old)*unit_price`). Công thức có đúng và không âm (new ≥ old) không?
- Endpoint ghi dữ liệu có `db.commit()`/`db.rollback()` đúng chỗ? (xem pattern try/except trong `import-csv`).

**Auth / bảo mật**
- `get_current_user` đọc cookie `access_token`. Hiện `rooms/bills/electricity/settings` đang là `# Public routes` (KHÔNG có `dependencies=[Depends(get_current_user)]`). Thay đổi có cần bảo vệ endpoint không? Có vô tình mở thêm dữ liệu nhạy cảm không?
- `SECRET_KEY` phải ổn định (đổi → mất hết session). `ADMIN_PASSWORD` mặc định `admin123` — code có làm lộ không?
- Input người dùng (CSV, body) có ép kiểu/validate? `int()` có thể ném lỗi với input bẩn.

**Shape API ↔ UI**
- Endpoint build dict tay (không `response_model`) → schema `*Read` chỉ là tài liệu, shape thật là dict. Review có dựa vào shape THẬT không? Field `app.js` đọc có khớp dict?

**Frontend / i18n**
- Text mới có đủ 5 ngôn ngữ trong `TRANSLATIONS`? Hardcode chuỗi trong template/JS?
- Dùng token/Tailwind class hay hardcode màu phá design system? Sửa `tokens.css` có bump `?v=`?

**Chất lượng chung**
- Trùng lặp có thể gộp? Tên rõ nghĩa? Có magic number nên thành token/setting? Có giá trị hardcode đáng lẽ đọc từ bảng `settings`?

## Chế độ DEBUG — có hệ thống, không vá mù

1. **Tái hiện**: xác định bước tái hiện lỗi rõ ràng. Không tái hiện được → nói rõ, xin thêm thông tin.
2. **Giả thuyết**: liệt kê nguyên nhân khả dĩ dựa trên triệu chứng.
3. **Kiểm chứng bằng bằng chứng**: đọc code đường đi, chạy lệnh, thêm log/print tạm, gọi endpoint thật. KHÔNG đoán rồi sửa đại.
4. **Khoanh vùng**: thu hẹp tới dòng/hàm gây lỗi. Với RentFlow, nghi ngờ thường ở: tính billing, lệch shape dict↔frontend, thiếu `commit`, cookie/JWT, ép kiểu input.
5. **Kết luận root cause** kèm bằng chứng dẫn tới nó, rồi mới đề xuất sửa. Sửa nguyên nhân gốc, không che triệu chứng.
6. **Xác minh sau sửa**: chạy lại bước tái hiện để chắc đã hết.

## Báo cáo

Ghi `_workspace/review_report.md` (review) theo mức ưu tiên, hoặc nêu root cause + bằng chứng (debug). Tôn trọng quyết định người dùng: đề xuất, không tự refactor lớn trừ khi được yêu cầu. Giải thích đủ để người mới học rút kinh nghiệm, không chỉ đưa lệnh sửa.
