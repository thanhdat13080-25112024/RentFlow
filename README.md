<div align="center">
  <img src="https://via.placeholder.com/150" alt="RentFlow Logo" width="120" height="120" />
  <h1>RentFlow</h1>
  <p>Hệ thống quản lý nhà trọ tinh gọn, đa nền tảng giúp theo dõi phòng, khách thuê và hóa đơn điện nước thông minh.</p>
</div>

<div align="center">

[![Language](https://img.shields.io/badge/Language-Python%203.9+-blue.svg)](https://www.python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![UI](https://img.shields.io/badge/UI-Alpine.js%20%26%20Tailwind-blue.svg)](https://alpinejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 🚀 Tính năng nổi bật

* **Quản lý phòng & khách thuê:** Theo dõi trạng thái phòng trống, thông tin khách thuê, tiền cọc và ngày vào ở.
* **Hóa đơn thông minh:** Tự động tính toán hóa đơn hàng tháng bao gồm tiền phòng, phí dịch vụ và tiền điện (hỗ trợ cả điện theo số và điện khoán).
* **Thanh toán QR Code:** Tự động tạo mã QR VietQR (Vietcombank/MB) giúp khách thuê thanh toán nhanh chóng và chính xác.
* **Lịch sử & Doanh thu:** Lưu trữ lịch sử đóng tiền của từng phòng và biểu đồ tổng hợp doanh thu theo từng tháng.
* **Đa ngôn ngữ:** Hỗ trợ giao diện Tiếng Việt, Tiếng Anh và Tiếng Hàn.
* **Giao diện Responsive:** Hiển thị tối ưu trên cả máy tính (Windows/Mac) và thiết bị di động (iOS/Android).

## 🛠 Yêu cầu hệ thống

* **Hệ điều hành:** macOS 13.0+, Windows 10/11, hoặc Linux.
* **Môi trường:** Python 3.9 trở lên.
* **Công cụ:** pip (quản lý gói thư viện).

## 📂 Cấu trúc dự án

```text
RentFlow/
  📂 app/
    📂 api/           # Các endpoints xử lý API (V1)
    📂 core/          # Cấu hình hệ thống và kết nối Database
    📂 models/         # Định nghĩa cấu trúc dữ liệu SQLAlchemy
    📂 schemas/        # Định nghĩa kiểu dữ liệu Pydantic
    📂 services/       # Logic nghiệp vụ (tính hoá đơn, khởi tạo DB)
    📂 static/         # File tĩnh (Javascript, CSS)
    📂 templates/      # Giao diện HTML (Jinja2 + Alpine.js)
  📄 main.py          # Entry point khởi chạy server Uvicorn
  📄 requirements.txt # Danh sách các thư viện cần thiết
  📄 rentflow.db      # Cơ sở dữ liệu SQLite (tự động khởi tạo)
```

## ⚙️ Cài đặt nhanh

1. Cài đặt các thư viện:
   ```bash
   pip install -r requirements.txt
   ```
2. Chạy ứng dụng:
   ```bash
   python main.py
   ```
3. Truy cập vào trình duyệt: `http://localhost:8000`
