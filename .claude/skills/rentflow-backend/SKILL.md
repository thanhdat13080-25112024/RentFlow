---
name: rentflow-backend
description: Convention backend thật của RentFlow — cấu trúc file đã tách (models/, schemas/, api/v1/endpoints/), cách thêm endpoint/model/schema, service billing, Alembic, cạm bẫy commit SQLAlchemy và auth. Dùng BẮT BUỘC khi thêm/sửa bất kỳ code server nào: API, model dữ liệu, schema, logic nghiệp vụ, migration. Trigger cả khi "sửa lại endpoint", "thêm field", "cập nhật model".
---

# RentFlow — Backend Conventions

RentFlow là app quản lý nhà trọ một-admin: FastAPI + SQLAlchemy + SQLite, Jinja2/Alpine cho UI (không build step). Skill này ghi convention **thực tế trong code** — nơi nào lệch với `CLAUDE.md`, tin vào đây và code.

## Cấu trúc file thật (KHÔNG phải như CLAUDE.md mô tả)

CLAUDE.md cũ nói model nằm trong `entities.py`, schema trong `data_transfer_objects.py`. **Sai.** Cấu trúc thật đã tách:

```
app/
├── main.py                 # tạo app, create_all + seed, mount static, include router
├── core/
│   ├── config.py           # Settings (pydantic-settings, đọc .env, tự sinh SECRET_KEY)
│   └── security.py         # create_access_token, get_current_user (đọc cookie access_token)
├── db/
│   ├── base.py             # Base = declarative_base()
│   ├── session.py          # engine, SessionLocal, get_db()
│   └── __init__.py         # export Base, SessionLocal, engine, get_db
├── models/                 # MỖI model 1 file
│   ├── room.py, electricity_reading.py, monthly_bill.py, setting.py
│   └── __init__.py         # export Room, ElectricityReading, MonthlyBill, Setting
├── schemas/                # MỖI nhóm schema 1 file
│   ├── bill.py, electricity.py, room.py, setting.py
│   └── __init__.py         # export tất cả schema (import từ đây: from app.schemas import ...)
├── api/
│   ├── deps.py             # re-export get_db, get_current_user
│   ├── web.py              # route HTML (GET / render index.html)
│   └── v1/
│       ├── router.py       # gom các endpoint router, prefix /api
│       └── endpoints/      # auth.py, rooms.py, bills.py, electricity.py, settings.py
└── services/
    ├── billing.py          # update_bill()
    └── seeder.py           # seed_initial_data()
```

## Thêm một endpoint mới

1. Viết handler trong file phù hợp ở `app/api/v1/endpoints/` (vd thêm route phòng → `rooms.py`). Mỗi file có sẵn `router = APIRouter()`.
2. Dùng dependency: `db: Session = Depends(get_db)`. Import `from app.api.deps import get_db`.
3. Import model: `from app.models import Room, MonthlyBill, ...`. Import schema: `from app.schemas import RoomRead, ...`.
4. Nếu tạo file router mới, đăng ký trong `app/api/v1/router.py` bằng `api_router.include_router(...)`.
5. Nhớ `db.commit()` sau khi thay đổi dữ liệu trong handler (xem mục commit bên dưới).

## Auth — trạng thái THẬT

`get_current_user` (security.py) đọc cookie `access_token`, decode JWT. **Nhưng** trong `router.py` hiện tại các router `rooms/bills/electricity/settings` đăng ký dưới comment `# Public routes` và **KHÔNG** có `dependencies=[Depends(get_current_user)]`. Tức là hiện chúng đang **không bị chặn auth**.

→ Nếu cần bảo vệ một endpoint, thêm `dependencies=[Depends(get_current_user)]` vào `APIRouter(...)` của file đó hoặc vào lời gọi `include_router(...)`. Đừng giả định auth đã bật như CLAUDE.md nói — kiểm tra trước.

## Commit SQLAlchemy — cạm bẫy quan trọng

- `update_bill(db, room, month, year)` trong `services/billing.py` **TỰ gọi `db.commit()`** ở cuối. Chỉ gọi từ **luồng GHI** (mark-paid, nhập điện, sửa phòng). Các endpoint **GET KHÔNG gọi** `update_bill` nữa — chúng tính ảo bằng `compute_bill_fields(room, reading)` (thuần, không ghi DB) để GET không tạo bill/commit khi chỉ xem.
- Giá điện mặc định: dùng `get_unit_price(db)` (đọc Setting → fallback `config.DEFAULT_ELECTRICITY_UNIT_PRICE`). Không hardcode 4000/3500 trong endpoint.
- Trong handler tự sửa dữ liệu (không qua `update_bill`): nhớ tự `db.commit()`. Dùng `db.flush()` khi cần id/giá trị trước khi commit (xem `rooms.py` update_room).
- Khối `import-csv` (bills.py) dùng try/except + `db.rollback()` khi lỗi — theo pattern này cho thao tác ghi hàng loạt.

## Logic billing (services/billing.py)

`update_bill`:
1. Tìm `ElectricityReading` cho room+month+year.
2. Tính `elec_fee`: nếu `room.electricity_type == "fixed"` → `room.fixed_electricity_fee`; nếu có reading → `(new_reading - old_reading) * reading.unit_price`; ngược lại 0.
3. `total = rent_price + service_fee + elec_fee`.
4. Nếu bill đã tồn tại: **chỉ cập nhật khi `status == "unpaid"`** — không bao giờ ghi đè bill `paid`/`prepaid`. Nếu chưa có: tạo mới status `unpaid`.
5. Gọi `db.commit()`.

Trạng thái bill: `unpaid` / `paid` / `prepaid`. `electricity_type`: `"meter"` / `"fixed"`.

## Model — convention

- Kế thừa `from app.db import Base`. Cột tiền dùng `Integer` (VNĐ, không có phần thập phân). Ngày tháng (`move_in_date`) lưu dạng `String`.
- Quan hệ khai báo `relationship(..., back_populates=...)` hai chiều (xem `room.py`).
- Sau khi tạo model file mới: thêm vào `app/models/__init__.py`.

## Schema — convention

- `BaseModel` của Pydantic. Đặt trong file theo nhóm (`bill.py`...), export qua `app/schemas/__init__.py`.
- ⚠️ Nhiều endpoint trả **dict thủ công** chứ không dùng `response_model` (vd `/api/bills/` build dict tay). Khi đó schema `*Read` chỉ là tài liệu — shape thật là dict trong handler. Khi đổi shape, sửa CẢ dict thật, và báo frontend/QA. Endpoint khác (vd `GET /rooms/`) có `response_model=List[RoomRead]` thì Pydantic kiểm soát shape.

## Settings runtime

Bảng `settings` (key/value) lưu cấu hình chỉnh qua UI: `electricity_unit_price`, `bank_account`, `bank_name`, `account_holder`. **Không hardcode** các giá trị này; đọc từ DB (xem cách `bills.py`/`settings.py` query `Setting`). Default khi thiếu: giá điện 4000.

## Migration (Alembic)

Khi thêm/đổi cột model:
```bash
alembic revision --autogenerate -m "mô tả thay đổi"
alembic upgrade head
```
`Base.metadata.create_all()` chạy lúc khởi động chỉ tạo bảng MỚI, không sửa cột bảng cũ → bắt buộc migration cho thay đổi schema.

## Chạy & kiểm tra nhanh

```bash
python main.py                      # hoặc: uvicorn app.main:app --reload  → http://localhost:8000
pip install -r requirements.txt     # nếu thiếu dependency
```

## Checklist trước khi xong

- [ ] Import đúng từ `app.models` / `app.schemas` / `app.api.deps`
- [ ] Có `db.commit()` (hoặc dùng `update_bill` đã tự commit) cho thao tác ghi
- [ ] Đổi shape response → sửa dict thật + báo frontend/QA shape mới
- [ ] Thêm cột model → tạo Alembic migration
- [ ] Không hardcode giá trị thuộc bảng `settings`
- [ ] Tóm tắt shape JSON của endpoint mới cho QA & frontend
