# 📚 Tài liệu RentFlow

Bộ tài liệu kỹ thuật cho học phần **Lập trình Hướng Đối Tượng (OOP)**.

| Tài liệu | Nội dung |
|----------|----------|
| [OOP_Analysis.md](OOP_Analysis.md) | Phân tích 4 nguyên lý OOP (kế thừa, đóng gói, trừu tượng, đa hình) + design pattern, kèm sơ đồ lớp và đề xuất cải tiến |
| [UML_Architecture.md](UML_Architecture.md) | Kiến trúc phân tầng + sơ đồ UML (Use Case, Component, Sequence, State, Activity) bằng Mermaid |
| [Testing_Report.md](Testing_Report.md) | Kết quả chạy `pytest` thật (11/11 pass), điểm mạnh – điểm yếu, rủi ro, khuyến nghị |

**Stack:** Python 3.11 · FastAPI · SQLAlchemy 2.0 · Pydantic v2 · Jinja2 + Alpine.js · SQLite / PostgreSQL.

> 💡 Cả ba tài liệu đều xây trên mã nguồn thật trong `app/`. Hai cải tiến OOP đã được
> **hiện thực** (Strategy Pattern cho tính tiền điện + hành vi `is_paid`/`is_overdue`
> cho model) giúp dự án thể hiện đủ cả bốn nguyên lý OOP ở mức mạnh — chi tiết ở
> `OOP_Analysis.md` mục 3.4, 5.3 và 8.2.
