# Báo cáo sửa lỗi — RentFlow

**Ngày:** 2026-05-24  
**Commit:** `daa54d4`  
**Môi trường:** Python 3.14.4, FastAPI 0.136, SQLAlchemy 2.0.49, Pydantic 2.13.4

---

## Lỗi đã sửa (7 lỗi)

### Nhóm A — Lỗi blocking (app vỡ hoàn toàn)

| # | File | Dòng | Lỗi | Cách sửa |
|---|------|------|-----|----------|
| 1 | `app/static/js/app.js` | 430 | `fetch('/api/import-csv')` gọi sai URL → 404, tính năng Import CSV không hoạt động | Đổi thành `/api/bills/import-csv` |
| 2 | `app/templates/index.html` | 117–119 | Inline `function app()` ghi đè `window.app` rồi gọi ngược lại chính nó → đệ quy vô hạn, Alpine.js không khởi tạo được | Dùng IIFE capture `window.app` gốc vào `_factory` trước khi ghi đè |

### Nhóm B — Lỗi runtime crash

| # | File | Dòng | Lỗi | Cách sửa |
|---|------|------|-----|----------|
| 3 | `app/api/v1/endpoints/bills.py` | 112–123 | `mark-paid` không kiểm tra `room is None` trước khi gọi `update_bill(db, None, ...)` → `AttributeError`; `bill.status` cũng crash nếu `bill` vẫn None | Thêm guard: `if not room → 404`, `if not bill → 404` |

### Nhóm C — Lỗi bảo mật / ổn định

| # | File | Dòng | Lỗi | Cách sửa |
|---|------|------|-----|----------|
| 4 | `app/core/config.py` | 14 | `SECRET_KEY = secrets.token_urlsafe(32)` sinh key mới mỗi lần restart → toàn bộ JWT token bị invalidate, người dùng bị đăng xuất | Hàm `_get_or_create_secret_key()` đọc từ `.env`; nếu chưa có thì sinh mới và ghi vào `.env` để dùng lại |

### Nhóm D — Deprecation warning

| # | File | Dòng | Lỗi | Cách sửa |
|---|------|------|-----|----------|
| 5 | `app/core/database.py` | 1 | `from sqlalchemy.ext.declarative import declarative_base` — deprecated SQLAlchemy 2.0 → `MovedIn20Warning` | Đổi thành `from sqlalchemy.orm import declarative_base` |
| 6 | `app/schemas/data_transfer_objects.py` | 41–42 | `class Config: from_attributes = True` — Pydantic V1 syntax, deprecated V2 → `PydanticDeprecatedSince20` | Đổi thành `model_config = ConfigDict(from_attributes=True)` |
| 7 | `app/core/security.py` | 12, 14 | `datetime.utcnow()` — deprecated Python 3.12+, scheduled for removal; dự án đang chạy Python 3.14.4 | Đổi thành `datetime.now(timezone.utc)` |

---

## Kết quả kiểm tra sau sửa

```
GET /                                   → 307 /login    ✅
GET /login                              → 200 HTML      ✅
POST /api/auth/login (sai mật khẩu)     → 401           ✅
POST /api/auth/login (đúng)             → 200 + cookie  ✅
GET  /api/bills?month=5&year=2026       → 200, 12 bills ✅
GET  /api/rooms                         → 200, 12 rooms ✅
POST /api/bills/mark-paid (room 9999)   → 404           ✅
App import (DeprecationWarning filter)  → CLEAN         ✅
```

---

## Lỗi không sửa (nằm ngoài phạm vi / cần xác nhận)

| File | Vấn đề | Lý do không sửa |
|------|--------|-----------------|
| `tempCodeRunnerFile.py` | File rác của VS Code Code Runner, không nên track trong git | Cần xác nhận trước khi xóa |
| `alembic/versions/25dcf1ebf5c8_initial_migration.py` | Migration trống (`pass`), không phản ánh schema thực | Liên quan schema DB — nằm ngoài phạm vi |
| `app/main.py` | Có pre-existing thay đổi chưa commit (`host=settings.HOST`) | Đã tồn tại trước phiên này, không phải lỗi do code |
| `app/services/billing.py` | `update_bill` tạo hoá đơn cho cả phòng trống (total=0) | Logic có thể intentional — không thay đổi nếu không có yêu cầu rõ |

---

## Cần xác nhận

_Không có mục nào cần xác nhận thêm._
