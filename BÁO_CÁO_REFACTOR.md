# Báo cáo tái cấu trúc — RentFlow

**Ngày:** 2026-05-24
**Phạm vi:** 11 commits refactor, KHÔNG thay đổi hành vi, KHÔNG đụng DB schema / endpoint URLs / response field names.

---

## 1. Cây thư mục — Before / After

### Trước
```
app/
├── main.py                              # FastAPI app + HTML routes + seed
├── api/
│   └── v1/
│       ├── api.py                       # router aggregator
│       └── endpoints/ (5 file)
├── core/
│   ├── config.py
│   ├── database.py                      # engine + Base + SessionLocal + get_db
│   └── security.py
├── models/
│   └── entities.py                      # 4 model trong 1 file
├── schemas/
│   └── data_transfer_objects.py         # 11 schema trong 1 file
└── services/
    ├── billing.py
    └── database_seeder.py
```

### Sau
```
app/
├── main.py                              # CHỈ mount + startup (28 dòng -> 18 dòng)
├── api/
│   ├── deps.py                          # ✨ get_db + get_current_user
│   ├── web.py                           # ✨ HTML routes ("/", "/login")
│   └── v1/
│       ├── router.py                    # 🔄 api.py → router.py
│       └── endpoints/ (5 file)
├── core/
│   ├── config.py
│   └── security.py
├── db/                                  # ✨ tách layer DB
│   ├── base.py                          # Base = declarative_base()
│   ├── session.py                       # engine, SessionLocal, get_db
│   └── __init__.py                      # re-export
├── models/                              # 🔀 1 file → 4 file
│   ├── room.py
│   ├── electricity_reading.py
│   ├── monthly_bill.py
│   ├── setting.py
│   └── __init__.py
├── schemas/                             # 🔀 1 file → 4 file
│   ├── room.py
│   ├── bill.py
│   ├── electricity.py
│   ├── setting.py
│   └── __init__.py
└── services/
    ├── billing.py
    └── seeder.py                        # 🔄 database_seeder.py → seeder.py

tests/                                   # ✨ scaffold (empty)
├── __init__.py
└── conftest.py
```

---

## 2. Bảng đổi tên — Schemas (Pydantic)

| Cũ | Mới | Lý do |
|----|-----|-------|
| `ElectricityInput` | `ElectricityReadingCreate` | `Input` không chuẩn; entity là `ElectricityReading`, suffix `Create` đúng convention |
| `PaidInput` | `BillPaidUpdate` | Là cập nhật trạng thái → `Update` |
| `PrepaidInput` | `BillPrepaidUpdate` | Tương tự |
| `SettingResponse` | `SettingRead` | Convention: `Read` thay `Response` |
| `RoomResponse` | `RoomRead` | Tương tự |
| `RevenueSummaryResponse` | `RevenueSummaryRead` | Tương tự |
| `BillResponse` | `BillRead` | Tương tự |
| `RoomHistoryResponse` | `RoomHistoryRead` | Tương tự |
| `RoomUpdate` | (giữ) | Đã đúng |
| `SettingUpdate` | (giữ) | Đã đúng |

## 3. Bảng đổi tên — File / Module

| Cũ | Mới | Lý do |
|----|-----|-------|
| `app/core/database.py` | `app/db/session.py` + `app/db/base.py` | Tách `Base` (metadata) khỏi `engine/Session` để tránh circular import |
| `app/models/entities.py` | `app/models/{room,electricity_reading,monthly_bill,setting}.py` | "entities" mơ hồ; mỗi entity 1 file |
| `app/schemas/data_transfer_objects.py` | `app/schemas/{room,bill,electricity,setting}.py` | Tên dài lê thê; gộp theo domain |
| `app/api/v1/api.py` | `app/api/v1/router.py` | "api.py" trùng folder "api/" → confusing |
| `app/services/database_seeder.py` | `app/services/seeder.py` | "database_" thừa |

## 4. Bảng đổi tên — Hàm

| Cũ | Mới | Lý do |
|----|-----|-------|
| `init_data` | `seed_initial_data` | "init_data" quá generic, không mô tả đúng (chỉ seed khi DB rỗng) |

## 5. File MỚI tạo

| File | Mục đích |
|------|----------|
| `app/db/base.py` | Single source cho `Base = declarative_base()` |
| `app/db/session.py` | engine + SessionLocal + get_db |
| `app/db/__init__.py` | Re-export 4 symbols |
| `app/api/deps.py` | Single source cho FastAPI dependencies |
| `app/api/web.py` | Server-rendered HTML routes (tách khỏi main.py) |
| `app/models/__init__.py` | Re-export 4 models |
| `app/schemas/__init__.py` | Re-export 10 schemas |
| `tests/__init__.py` | Scaffold test directory |
| `tests/conftest.py` | Placeholder cho pytest fixtures |

## 6. File ĐÃ XÓA (qua merge và refactor)

| File | Lý do |
|------|-------|
| `app/core/database.py` | Move vào `app/db/` |
| `app/models/entities.py` | Split thành 4 file |
| `app/schemas/data_transfer_objects.py` | Split thành 4 file |
| `app/services/database_seeder.py` | Rename → `seeder.py` |
| `app/api/v1/api.py` | Rename → `router.py` |
| `tempCodeRunnerFile.py` (root) | Rác từ VS Code Code Runner |
| `rentflow.db` (tracking) | Untrack — file runtime, thêm `*.db` vào `.gitignore` |

## 7. Lint / Format

Chạy `ruff check --select I,F --fix` toàn dự án:
- 12 file sắp xếp lại import thành 3 nhóm (stdlib / third-party / local)
- Xóa 7 unused imports

Kết quả: **`All checks passed!`**

## 8. RÀNG BUỘC ĐƯỢC TÔN TRỌNG

- ✅ DB schema (table names, column names) **không thay đổi**
- ✅ API endpoint URLs **không thay đổi** (`/api/auth/login`, `/api/bills/import-csv`, ...)
- ✅ JSON response field names **không thay đổi** (frontend Alpine.js không cần update)
- ✅ Cookie name `access_token` **không thay đổi**
- ✅ Logic kinh doanh **không thay đổi**

## 9. KIỂM TRA CUỐI — Endpoint integration test

12/12 endpoint test PASS sau lint cuối cùng:

```
[OK] GET /                              -> 307
[OK] GET /login                         -> 200
[OK] POST /api/auth/login (sai pw)      -> 401
[OK] POST /api/auth/login (đúng)        -> 200
[OK] GET /api/rooms                     -> 200 (12 rooms)
[OK] GET /api/bills                     -> 200 (12 bills)
[OK] GET /api/bills/revenue/summary     -> 200
[OK] GET /api/rooms/1/history           -> 200
[OK] GET /api/settings/                 -> 200
[OK] POST /api/electricity/             -> 200
[OK] POST /api/bills/mark-paid          -> 200
[OK] POST /api/bills/mark-paid (404)    -> 404
```

App boot: **CLEAN** (không DeprecationWarning từ app.*).
Ruff: **All checks passed!**

## 10. Chuỗi commit refactor

| Commit | Mô tả |
|--------|-------|
| `fc7ab31` | refactor(schemas): đổi tên Create/Update/Read convention |
| `1923bed` | refactor(seeder): init_data → seed_initial_data |
| `28240c3` | refactor(db): tách app/db/ từ core/database.py |
| `b5f097f` | refactor(models): split entities.py thành per-model file |
| `e96764e` | refactor(schemas): split data_transfer_objects.py thành per-domain file |
| `7c56f98` | refactor(services): rename database_seeder.py → seeder.py |
| `baf45af` | refactor(api): rename api/v1/api.py → router.py |
| `30e70e4` | refactor(api): tạo app/api/deps.py |
| `1fdbb6f` | refactor(api): tách HTML routes ra app/api/web.py |
| `57f5dda` | chore(tests): scaffold tests/ |
| `27bfdef` | chore(lint): ruff --fix toàn dự án |

Cộng thêm 2 commit phụ trợ giữa các bước:
- `45d2bc5` — chore: merge origin/main, resolve conflicts (do user `git pull` giữa session)
- `01193fd` — chore(gitignore): thêm `*.db`

## 11. KHÔNG làm (cố ý)

- **`app/repositories/`** — Tách query ra repository sẽ là refactor logic (di chuyển query khỏi endpoints). Vượt phạm vi "không sửa logic". Để dành cho phiên sau nếu cần.
- **Đổi tên model `MonthlyBill` → `Bill`** — Sẽ phải đụng nhiều chỗ; tên hiện tại vẫn miêu tả tốt domain.
- **Refactor `get_revenue_summary`** — Logic update bill cho tất cả periods rất chậm với DB lớn, nhưng đó là logic, để sau.
- **Thêm test thực tế** — Đã scaffold `tests/` nhưng không viết test (out of scope).

## 12. Khuyến nghị tiếp theo (nếu bạn muốn)

1. Bổ sung `app/repositories/` để tách query → endpoint chỉ làm việc với DTOs
2. Viết unit test cho `app/services/billing.py:update_bill` (logic phức tạp nhất)
3. Bổ sung mypy stub / type hints chặt hơn
4. Bổ sung `pre-commit` config với ruff để check tự động
