<div align="center">
  <h1>RentFlow</h1>
  <p><b>Hệ thống quản lý nhà trọ tinh gọn, đa nền tảng</b><br/>theo dõi phòng, khách thuê và hóa đơn điện nước thông minh.</p>
  <p>🌐 <b><a href="https://rentflow-lake.vercel.app/">Demo trực tiếp »</a></b></p>
</div>

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live_Demo-rentflow--lake.vercel.app-success?logo=vercel)](https://rentflow-lake.vercel.app/)
[![Language](https://img.shields.io/badge/Language-Python%203.9+-blue.svg)](https://www.python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![ORM](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-d71f00.svg)](https://www.sqlalchemy.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![UI](https://img.shields.io/badge/UI-Alpine.js%20%2B%20Tailwind-77C1D2.svg)](https://alpinejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 🚀 Tính năng

- **Quản lý phòng & khách thuê** — theo dõi trạng thái phòng (đang thuê / trống), thông tin liên hệ, tiền cọc, ngày vào ở.
- **Hóa đơn tự động** — tính tiền hàng tháng = tiền phòng + phí dịch vụ + tiền điện. Hỗ trợ 2 chế độ điện: **theo số** (meter) hoặc **khoán** (fixed).
- **QR Code thanh toán** — sinh mã VietQR (Vietcombank / MB / …) qua [sepay.vn](https://qr.sepay.vn), kèm nội dung chuyển khoản chuẩn hoá.
- **Lịch sử & doanh thu** — xem lịch sử thanh toán từng phòng, biểu đồ doanh thu 6 tháng gần nhất.
- **Import CSV** — nạp dữ liệu hàng loạt từ file CSV (UTF-8 BOM).
- **Đa ngôn ngữ** — Tiếng Việt 🇻🇳, English 🇺🇸, 한국어 🇰🇷, 日本語 🇯🇵, 中文 🇨🇳.
- **Responsive** — chạy mượt trên desktop và mobile (iOS / Android).
- **Thiết kế OOP** — tính tiền điện theo **Strategy pattern** (meter/fixed), hành vi `is_paid`/`is_overdue` đóng gói trong model. Phân tích đầy đủ trong [`Documentation/`](Documentation/).
- **Chế độ dự án mở** — bản hiện tại bỏ đăng nhập, mở thẳng dashboard với dữ liệu mẫu (hạ tầng JWT/bcrypt vẫn còn trong `app/core/security.py` để bật lại khi cần).

## 🛠 Yêu cầu

- **Python** 3.9+ (đã test trên 3.14)
- **pip** để cài thư viện
- Hệ điều hành: macOS, Windows 10/11, hoặc Linux

## ⚙️ Cài đặt nhanh

```bash
# 1. Clone repo và vào thư mục
git clone <repo-url> RentFlow
cd RentFlow

# 2. Tạo virtualenv (khuyến nghị)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Cài dependencies
pip install -r requirements.txt

# 4. (Tuỳ chọn) Cấu hình
cp .env.example .env
# rồi sửa .env theo nhu cầu — không bắt buộc cho lần chạy đầu

# 5. Chạy
python main.py
```

Mặc định server lắng nghe tại `http://127.0.0.1:8000` — mở thẳng dashboard, **không cần đăng nhập** (chế độ dự án mở, dữ liệu mẫu).

## 🔧 Cấu hình (`.env`)

File `.env` được đọc tự động qua `pydantic-settings`. Tất cả biến đều có default trong `app/core/config.py`.

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `HOST` | `127.0.0.1` | IP server lắng nghe |
| `PORT` | `8000` | Cổng |
| `SECRET_KEY` | _auto-generated_ | JWT key — sinh ngẫu nhiên và ghi vào `.env` lần đầu chạy |
| `ALGORITHM` | `HS256` | Thuật toán JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | Thời gian sống token (7 ngày) |
| `ADMIN_USERNAME` | `admin` | Tài khoản đăng nhập |
| `ADMIN_PASSWORD` | `admin123` | **Nên đổi** trước khi deploy |
| `SQLALCHEMY_DATABASE_URL` | `sqlite:///./rentflow.db` | Connection string |
| `BANK_NAME` | `MB` | Mã ngân hàng (cho QR) |
| `BANK_ACCOUNT` | _empty_ | Số tài khoản |
| `ACCOUNT_HOLDER` | _empty_ | Chủ tài khoản |

## 📂 Cấu trúc dự án

```
RentFlow/
├── app/
│   ├── main.py                  # FastAPI app + startup hooks
│   ├── api/
│   │   ├── deps.py              # Common deps (get_db, get_current_user)
│   │   ├── web.py               # HTML page route ("/")
│   │   └── v1/
│   │       ├── router.py        # Aggregator APIRouter (mọi route công khai)
│   │       └── endpoints/       # rooms, bills, electricity, settings
│   ├── core/
│   │   ├── config.py            # pydantic-settings Settings
│   │   └── security.py          # JWT + password hashing
│   ├── db/
│   │   ├── base.py              # SQLAlchemy declarative Base
│   │   └── session.py           # engine, SessionLocal, get_db
│   ├── models/                  # SQLAlchemy ORM (1 file / model)
│   │   ├── room.py
│   │   ├── electricity_reading.py
│   │   ├── monthly_bill.py
│   │   └── setting.py
│   ├── schemas/                 # Pydantic schemas theo domain
│   │   ├── room.py              # RoomRead, RoomUpdate, RoomHistoryRead
│   │   ├── bill.py              # BillRead, BillPaidUpdate, ...
│   │   ├── electricity.py       # ElectricityReadingCreate
│   │   └── setting.py           # SettingUpdate, SettingRead
│   ├── services/
│   │   ├── billing.py           # Logic tính hoá đơn (compute_bill_fields, update_bill)
│   │   ├── electricity_strategy.py  # Strategy pattern tính tiền điện (Meter/Fixed)
│   │   └── seeder.py            # Seed 12 phòng mẫu lần đầu
│   ├── static/{js,css}/         # Alpine, Tailwind, design tokens
│   └── templates/               # Jinja2 (base, index + components)
├── Documentation/               # Tài liệu OOP (phân tích, UML, báo cáo test)
├── alembic/                     # Migration scaffold (Alembic)
├── tests/                       # Pytest suite (billing, API, strategy, model behavior)
├── main.py                      # Entry point uvicorn
├── rentflow.db                  # DB mẫu (12 phòng + 3 tháng dữ liệu)
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API

Tất cả endpoint REST nằm dưới prefix `/api`. Bản hiện tại ở **chế độ mở** — mọi endpoint công khai, không yêu cầu đăng nhập.

| Method | URL | Mô tả |
|--------|-----|-------|
| `GET`  | `/api/rooms` | Danh sách phòng |
| `POST` | `/api/rooms/update` | Cập nhật phòng (giá, khách, số điện cũ) |
| `GET`  | `/api/rooms/{id}/history` | Lịch sử hoá đơn theo phòng |
| `GET`  | `/api/bills?month=&year=` | Hoá đơn tháng + chi tiết điện |
| `GET`  | `/api/bills/revenue/summary` | Tổng hợp doanh thu theo tháng |
| `POST` | `/api/bills/mark-paid` | Đánh dấu đã thu |
| `POST` | `/api/bills/mark-prepaid` | Đánh dấu đóng trước nhiều tháng |
| `POST` | `/api/bills/import-csv` | Import dữ liệu hàng loạt từ CSV |
| `POST` | `/api/electricity/` | Cập nhật số điện tháng (chế độ meter) |
| `GET`  | `/api/settings/` | Lấy toàn bộ cài đặt (giá điện, ngân hàng) |
| `POST` | `/api/settings/` | Cập nhật cài đặt |

Trang HTML server-rendered:

| URL | Mô tả |
|-----|-------|
| `GET /` | Dashboard chính (render trực tiếp, không cần đăng nhập) |

Tài liệu OpenAPI tự động tại `http://localhost:8000/docs` (Swagger UI) và `/redoc`.

## 🏗 Kiến trúc

- **Layered** — `api` (HTTP) → `services` (business logic) → `models` + `db` (persistence). Schema (Pydantic) tách khỏi model (SQLAlchemy).
- **Dependency injection** — `app/api/deps.py` là single source cho `get_db` và `get_current_user`.
- **Convention naming**:
  - File / module: `snake_case`
  - Class: `PascalCase`
  - Schema suffix theo CRUD: `*Create`, `*Update`, `*Read` (e.g. `RoomRead`, `BillPaidUpdate`)
- **Thiết kế hướng đối tượng** — tính tiền điện dùng **Strategy pattern** (`ElectricityStrategy` ABC ← `MeterStrategy`/`FixedStrategy`); model `MonthlyBill` đóng gói hành vi `is_paid`/`is_overdue`. Phân tích 4 nguyên lý OOP + UML trong [`Documentation/`](Documentation/).
- **Auth** — hiện tắt (chế độ mở). Hạ tầng JWT cookie `httponly` `samesite=lax` + bcrypt vẫn nằm trong `app/core/security.py`, bật lại bằng cách thêm `dependencies=[Depends(get_current_user)]` vào router.

## 🗄 Database

Dự án sử dụng SQLite làm mặc định. Mặc dù `*.db` bị bỏ qua trong `.gitignore`, hệ thống sẽ tự động khởi tạo dữ liệu mẫu nếu không tìm thấy file database.

Dữ liệu mẫu (seeder) gồm:
- 4 cài đặt mặc định (giá điện, thông tin ngân hàng)
- 12 phòng mẫu (3 tầng × 4 phòng): 8 phòng có khách, 4 phòng trống
- Hoá đơn + số điện cho 3 tháng gần nhất (nếu chạy lần đầu)

Để reset về trạng thái ban đầu, bạn chỉ cần xoá `rentflow.db` rồi chạy lại — hàm `seed_initial_data` trong `app/services/seeder.py` sẽ tự động tạo lại mọi thứ.

## 🧰 Lint

Dự án dùng `ruff` cho import sorting + unused-import check:

```bash
pip install ruff
ruff check app/ tests/ alembic/env.py main.py --select I,F
```

## 🧪 Test

```bash
pytest            # 22 ca: billing, API, electricity strategy, model behavior
```

| File | Nội dung |
|------|----------|
| `tests/test_billing.py` | Logic tính/ghi hoá đơn (6) |
| `tests/test_api.py` | Endpoint công khai, validation, shape JSON (5) |
| `tests/test_electricity_strategy.py` | Strategy tính tiền điện — đa hình (6) |
| `tests/test_model_behavior.py` | `is_paid`/`is_overdue` của `MonthlyBill` (5) |

## 📚 Tài liệu

Thư mục [`Documentation/`](Documentation/) chứa tài liệu kỹ thuật cho học phần OOP:

- [`OOP_Analysis.md`](Documentation/OOP_Analysis.md) — 4 nguyên lý OOP + design pattern, sơ đồ lớp.
- [`UML_Architecture.md`](Documentation/UML_Architecture.md) — kiến trúc + sơ đồ UML (Use Case, Component, Sequence, State, Activity).
- [`Testing_Report.md`](Documentation/Testing_Report.md) — kết quả test, điểm mạnh/yếu, rủi ro, khuyến nghị.

## 📜 License

MIT — xem [LICENSE](LICENSE).
