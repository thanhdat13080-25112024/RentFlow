<div align="center">
  <h1>RentFlow</h1>
  <p><b>Hệ thống quản lý nhà trọ tinh gọn, đa nền tảng</b><br/>theo dõi phòng, khách thuê và hóa đơn điện nước thông minh.</p>
</div>

<div align="center">

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
- **Auth** — JWT cookie + bcrypt, `SECRET_KEY` được tự sinh và persist vào `.env` ngay lần chạy đầu.

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

Mặc định server lắng nghe tại `http://127.0.0.1:8000`.
Tài khoản admin mặc định: **`admin / admin123`** (đổi qua `.env`).

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
│   │   ├── web.py               # HTML page routes ("/", "/login")
│   │   └── v1/
│   │       ├── router.py        # Aggregator APIRouter
│   │       └── endpoints/       # auth, rooms, bills, electricity, settings
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
│   │   ├── billing.py           # Logic tính hoá đơn
│   │   └── seeder.py            # Seed 12 phòng mẫu lần đầu
│   ├── static/{js,css}/         # Alpine, Tailwind, design tokens
│   └── templates/               # Jinja2 (base, index, login + components)
├── alembic/                     # Migration scaffold (Alembic)
├── tests/                       # Scaffold (chưa có test)
├── main.py                      # Entry point uvicorn
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API

Tất cả endpoint REST nằm dưới prefix `/api`. Endpoint không phải `auth` đều yêu cầu cookie `access_token`.

| Method | URL | Mô tả |
|--------|-----|-------|
| `POST` | `/api/auth/login` | Đăng nhập, set cookie `access_token` |
| `POST` | `/api/auth/logout` | Xoá cookie |
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
| `GET /` | Dashboard chính (redirect `/login` nếu chưa đăng nhập) |
| `GET /login` | Trang đăng nhập |

Tài liệu OpenAPI tự động tại `http://localhost:8000/docs` (Swagger UI) và `/redoc`.

## 🏗 Kiến trúc

- **Layered** — `api` (HTTP) → `services` (business logic) → `models` + `db` (persistence). Schema (Pydantic) tách khỏi model (SQLAlchemy).
- **Dependency injection** — `app/api/deps.py` là single source cho `get_db` và `get_current_user`.
- **Convention naming**:
  - File / module: `snake_case`
  - Class: `PascalCase`
  - Schema suffix theo CRUD: `*Create`, `*Update`, `*Read` (e.g. `RoomRead`, `BillPaidUpdate`)
- **Auth** — JWT trong cookie `httponly` `samesite=lax`; password lưu bcrypt; `SECRET_KEY` persist trong `.env`.

## 🌱 Dữ liệu seed

Lần đầu chạy, hàm `seed_initial_data` trong `app/services/seeder.py` sẽ:
1. Thêm 4 cài đặt mặc định (giá điện, thông tin ngân hàng)
2. Tạo 12 phòng mẫu (3 tầng × 4 phòng), 9 phòng có khách + 3 phòng trống
3. Sinh dữ liệu hoá đơn + số điện cho 3 tháng gần nhất

Để reset, xoá file `rentflow.db` rồi chạy lại.

## 🧰 Lint

Dự án dùng `ruff` cho import sorting + unused-import check:

```bash
pip install ruff
ruff check app/ tests/ alembic/env.py main.py --select I,F
```

## 📄 Tài liệu kèm theo

- [`BÁO_CÁO_FIX.md`](BÁO_CÁO_FIX.md) — danh sách 7 lỗi đã sửa (URL CSV sai, đệ quy Alpine.js, deprecated APIs, …)
- [`BÁO_CÁO_REFACTOR.md`](BÁO_CÁO_REFACTOR.md) — chi tiết tái cấu trúc 11 commit theo chuẩn FastAPI layered

## 📜 License

MIT — xem [LICENSE](LICENSE).
