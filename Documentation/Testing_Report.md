# Báo Cáo Kiểm Thử — RentFlow

> Báo cáo tổng hợp kết quả kiểm thử **RentFlow**, phân tích điểm mạnh – điểm yếu,
> rủi ro và khuyến nghị cải thiện. Khác với app tham chiếu (không có test tự động),
> RentFlow **đã có bộ test `pytest` chạy thật** — báo cáo này dựa trên kết quả chạy
> thực tế, không phải số liệu ước lượng.

---

## Mục lục

1. [Thông tin chung](#1-thông-tin-chung)
2. [Phạm vi & phương pháp kiểm thử](#2-phạm-vi--phương-pháp-kiểm-thử)
3. [Kết quả chạy test tự động](#3-kết-quả-chạy-test-tự-động)
4. [Chi tiết các ca kiểm thử](#4-chi-tiết-các-ca-kiểm-thử)
5. [Điểm mạnh của dự án](#5-điểm-mạnh-của-dự-án)
6. [Điểm yếu & thiếu sót](#6-điểm-yếu--thiếu-sót)
7. [Phân tích rủi ro](#7-phân-tích-rủi-ro)
8. [Khuyến nghị cải thiện](#8-khuyến-nghị-cải-thiện)
9. [Kết luận & đánh giá](#9-kết-luận--đánh-giá)

---

## 1. Thông tin chung

| Mục | Giá trị |
|-----|---------|
| Tên dự án | RentFlow — Quản lý nhà trọ |
| Phiên bản | Một quản trị viên, dữ liệu mẫu (chế độ mở) |
| Nền tảng | Python 3.11, FastAPI 0.136, SQLAlchemy 2.0, Pydantic v2 |
| Cơ sở dữ liệu | SQLite (dev) / PostgreSQL (prod) |
| Khung kiểm thử | `pytest` 9.0 + `TestClient` (Starlette) |
| File test | `tests/test_billing.py`, `tests/test_api.py`, `tests/test_electricity_strategy.py`, `tests/test_model_behavior.py`, `tests/conftest.py` |
| Ngày chạy | 2026-06-05 |

---

## 2. Phạm vi & phương pháp kiểm thử

| Phương pháp | Áp dụng |
|-------------|---------|
| **Unit test (hộp trắng)** | Logic tính tiền thuần (`compute_bill_fields`) và ghi DB (`update_bill`) |
| **Integration / API test (hộp đen)** | Gọi endpoint qua `TestClient`, kiểm tra status code + hình dạng JSON |
| **Kiểm thử ràng buộc (validation)** | Pydantic từ chối tháng/năm ngoài khoảng |
| **Kiểm thử thủ công (exploratory)** | Chạy `python main.py`, thao tác UI dashboard, dark mode, đổi ngôn ngữ |

`conftest.py` dựng một **database SQLite trong bộ nhớ** riêng cho mỗi test và tráo
`get_db` qua `dependency_overrides` — test không đụng vào DB thật, chạy độc lập.

---

## 3. Kết quả chạy test tự động

```
$ pytest -q
......................                                                   [100%]
22 passed, 2 warnings in 0.33s
```

| Chỉ số | Giá trị |
|--------|:------:|
| Tổng số ca | **22** |
| ✅ Pass | **22** |
| ❌ Fail | 0 |
| Tỉ lệ pass | **100%** |
| Thời gian | 0.33s |
| Cảnh báo | 2 (deprecation của thư viện bên thứ ba — `httpx`/`crypt`, không phải lỗi của RentFlow) |

> So với app tham chiếu (báo cáo 81% pass, không có unit test thật), RentFlow đạt
> 100% trên một bộ test **chạy được, lặp lại được**.

---

## 4. Chi tiết các ca kiểm thử

### 4.1. Unit test — `test_billing.py` (6 ca)

| # | Ca kiểm thử | Kiểm chứng | KQ |
|---|-------------|-----------|:--:|
| 1 | `test_compute_meter_with_reading` | (150−100)×4000 = 200.000đ; total cộng đúng | ✅ |
| 2 | `test_compute_meter_without_reading_is_zero_elec` | Không có chỉ số → tiền điện = 0 | ✅ |
| 3 | `test_compute_fixed_ignores_reading` | Phòng "fixed" dùng phí cố định, bỏ qua chỉ số | ✅ |
| 4 | `test_update_bill_creates_unpaid` | Tạo bill mới với `status="unpaid"` | ✅ |
| 5 | `test_update_bill_refreshes_unpaid` | Sửa giá phòng → bill chưa thu được tính lại | ✅ |
| 6 | `test_update_bill_never_overwrites_paid` | Bill **đã thu** không bị ghi đè dù sửa phòng | ✅ |

> Ca #6 là ca quan trọng nhất về nghiệp vụ: bảo vệ lịch sử thu tiền khỏi bị tính lại.

### 4.2. API test — `test_api.py` (5 ca)

| # | Ca kiểm thử | Kiểm chứng | KQ |
|---|-------------|-----------|:--:|
| 7 | `test_api_is_public` | `GET /api/rooms/` trả 200 + có dữ liệu seed (chế độ mở) | ✅ |
| 8 | `test_validation_rejects_bad_month` | `month=99` → 422 (Pydantic chặn) | ✅ |
| 9 | `test_receivables_shape` | `/receivables` có đủ khoá `total`, `count`, `rooms` | ✅ |
| 10 | `test_revenue_excludes_vacant` | `/revenue/summary` trả list, chỉ gộp phòng đang thuê | ✅ |
| 11 | `test_export_csv_headers` | Export trả `text/csv` + header `attachment` | ✅ |

### 4.3. Strategy tính tiền điện — `test_electricity_strategy.py` (6 ca)

| # | Ca kiểm thử | Kiểm chứng | KQ |
|---|-------------|-----------|:--:|
| 12 | `test_meter_strategy_with_reading` | `MeterStrategy.fee` = (mới−cũ)×đơn giá | ✅ |
| 13 | `test_meter_strategy_without_reading_is_zero` | Không có chỉ số → 0 | ✅ |
| 14 | `test_fixed_strategy_uses_flat_fee` | `FixedStrategy.fee` dùng phí khoán, bỏ qua chỉ số | ✅ |
| 15 | `test_fixed_strategy_none_fee_is_zero` | Phí khoán None → 0 | ✅ |
| 16 | `test_strategy_for_returns_subtype` | `strategy_for` trả đúng lớp con của `ElectricityStrategy` | ✅ |
| 17 | `test_electricity_fee_dispatches_by_type` | `electricity_fee` chọn đúng strategy theo `electricity_type` | ✅ |

### 4.4. Hành vi model — `test_model_behavior.py` (5 ca)

| # | Ca kiểm thử | Kiểm chứng | KQ |
|---|-------------|-----------|:--:|
| 18 | `test_is_paid_true_for_paid` | `status="paid"` → `is_paid` | ✅ |
| 19 | `test_is_paid_true_for_prepaid` | `status="prepaid"` → `is_paid` | ✅ |
| 20 | `test_is_paid_false_for_unpaid` | `status="unpaid"` → không `is_paid` | ✅ |
| 21 | `test_is_overdue_true_only_for_unpaid` | Chỉ `unpaid` mới `is_overdue` | ✅ |
| 22 | `test_is_paid_and_is_overdue_are_opposite` | Hai property luôn đối nhau | ✅ |

> Ca #16–17 chứng minh **đa hình** (chọn lớp lúc chạy); ca #12–15 khoá công thức tính
> tiền của từng strategy — là lưới an toàn cho refactor Strategy pattern.

---

## 5. Điểm mạnh của dự án

1. **Có test tự động thật**, chạy nhanh (0.5s), cô lập bằng DB in-memory.
2. **Tách ĐỌC/GHI rõ ràng**: endpoint GET tính ảo (`compute_bill_fields`), không
   ghi DB; chỉ luồng GHI mới gọi `update_bill` → tránh tạo rác bill mỗi lần xem.
3. **Một nguồn sự thật cho giá điện** (`get_unit_price`): hết tình trạng hardcode
   4000 ở endpoint và 3500 ở seeder.
4. **Bảo vệ dữ liệu đã thu**: bill `paid`/`prepaid` bất biến trước recalc.
5. **Validation tập trung bằng Pydantic** (`ge`/`le` cho tháng, năm, room_id).
6. **Kiến trúc phân tầng sạch** (web / api / service / model / infra).
7. **Import CSV bền với dữ liệu bẩn**: một dòng lỗi không làm hỏng cả file.
8. **Hỗ trợ đa ngôn ngữ** (vi/en/ko/ja/zh) và **dark mode** ở frontend.
9. **Cấu hình theo môi trường** linh hoạt (SQLite dev ↔ PostgreSQL prod, cookie
   `secure` theo `ENVIRONMENT`).
10. **Tài liệu đầy đủ**: `OOP_Analysis.md`, `UML_Architecture.md`, báo cáo này.

---

## 6. Điểm yếu & thiếu sót

| # | Vấn đề | Mức độ |
|---|--------|:------:|
| 1 | ~~Model anemic~~ → **đã thêm hành vi `is_paid`/`is_overdue`** cho `MonthlyBill` | ✅ Đã khắc phục |
| 2 | ~~Tính tiền điện dùng `if/elif`~~ → **đã refactor sang Strategy pattern** (đa hình) | ✅ Đã khắc phục |
| 3 | **`except Exception` quá rộng** trong `import-csv` — nuốt cả lỗi lập trình lẫn dữ liệu | 🟡 Trung bình |
| 4 | **Chưa có test cho `import-csv`, `mark-prepaid`, `electricity`** — vùng phức tạp nhất lại ít test nhất | 🟡 Trung bình |
| 5 | **Không có test cho lớp web/Jinja2 và Alpine.js** (frontend chưa được kiểm thử tự động) | 🟡 Trung bình |
| 6 | **Mã xác thực còn nhưng không dùng** — dễ gây hiểu nhầm về bảo mật | 🟡 Trung bình |
| 7 | **Mật khẩu admin mặc định `admin123`** trong `config.py` | 🟡 Trung bình |
| 8 | **Schema dùng `int` cho tiền** (đồng VND) — đúng cho VND nhưng không có kiểu Money rõ nghĩa | 🟢 Thấp |
| 9 | **Không có kiểm thử migration Alembic** dù schema do cả `create_all` lẫn Alembic quản | 🟢 Thấp |
| 10 | **Trùng logic tạo bill** giữa `update_bill`, `mark-prepaid`, `import-csv` | 🟢 Thấp |

---

## 7. Phân tích rủi ro

| Rủi ro | Khả năng | Ảnh hưởng | Giảm thiểu |
|--------|:--------:|:---------:|------------|
| `except Exception` che giấu bug thật khi import | Trung bình | Cao | Bắt cụ thể `ValueError`/`KeyError`, log dòng lỗi kèm số dòng |
| Thiếu test ở vùng phức tạp (import, prepaid) | Cao | Cao | Bổ sung ca test cho 3 endpoint còn trống |
| Lệch schema giữa `create_all` và Alembic | Thấp | Cao | Luôn tạo migration khi thêm cột; thêm test "schema khớp model" |
| Mật khẩu mặc định lọt lên production | Trung bình | Cao | Bắt buộc đặt `ADMIN_PASSWORD` qua `.env`, chặn giá trị mặc định ở prod |
| Frontend hồi quy (đổi field API) không bị test bắt | Trung bình | Trung bình | Thêm smoke test so khớp khoá JSON ↔ field `app.js` đọc |
| Hiểu nhầm app đang "có bảo mật" | Thấp | Trung bình | Ghi rõ trạng thái "chế độ mở" trong README |

---

## 8. Khuyến nghị cải thiện

**Đã hoàn thành ✅ (cải tiến OOP):**
- ✅ Refactor tính tiền điện sang **Strategy Pattern** (`MeterStrategy`/`FixedStrategy`
  kế thừa `ElectricityStrategy`) → `if/elif` đã thành **đa hình thực sự**.
- ✅ Thêm **`@property`** `is_paid`/`is_overdue` cho `MonthlyBill` → chống anemic,
  tăng đóng gói. (Chi tiết: `OOP_Analysis.md` mục 3.4 & 5.3.)

**Ưu tiên trung bình (còn lại):**
- Viết test cho `import-csv`, `mark-prepaid`, `electricity`.
- Thu hẹp `except Exception` → bắt lỗi cụ thể + log dòng.
- Quyết định dứt khoát: bật lại auth (gắn `Depends(get_current_user)`) **hoặc**
  gỡ hẳn `security.py` để tránh hiểu nhầm.

**Ưu tiên thấp:**
- Gộp logic tạo bill trùng lặp về một hàm chung trong `billing.py`.
- Thêm test kiểm tra schema model khớp với migration.

---

## 9. Kết luận & đánh giá

RentFlow là một ứng dụng web **chỉn chu về kiến trúc và có kiểm thử thật** — vượt
app tham chiếu ở chỗ test chạy được 100% và tách ĐỌC/GHI sạch sẽ. Sau hai refactor
OOP (Strategy pattern cho tính tiền điện + hành vi `is_paid`/`is_overdue` cho model),
cả bốn nguyên lý nay đều thể hiện ở mức **mạnh**: **đa hình** qua việc chọn strategy
lúc chạy, **đóng gói** qua hành vi nằm trong model, bên cạnh **kế thừa** và **trừu
tượng** vốn đã rõ. Bộ test tăng từ 11 lên **22 ca, 100% pass**.

| Tiêu chí | Điểm /10 |
|----------|:--------:|
| Kiến trúc & tổ chức code | 8.5 |
| Độ phủ & chất lượng test | 7.5 |
| Thể hiện nguyên lý OOP | 8.5 |
| Tài liệu | 8.5 |
| Bảo mật / sẵn sàng production | 6.0 |
| **Trung bình** | **🟢 7.8 / 10 — Khá–Tốt** |

---

*RentFlow — Báo cáo Kiểm thử. Học phần Lập trình Hướng Đối Tượng.*
