---
name: rentflow-frontend
description: Convention frontend RentFlow — Jinja2 template + components, component Alpine app() trong app.js, design tokens (tokens.css + Tailwind config trong base.html), i18n TRANSLATIONS (vi/en/ko/ja/zh). Dùng BẮT BUỘC khi thêm/sửa giao diện, component, dashboard, modal, hoặc bất kỳ text hiển thị nào. Trigger cả khi "đổi màu/layout", "thêm nút", "sửa chữ".
---

# RentFlow — Frontend Conventions

UI là **server-rendered Jinja2 + Alpine.js, không có build step**. Tailwind nạp qua CDN; Alpine nạp local. Mọi state nằm trong một component Alpine duy nhất.

## Cấu trúc frontend

```
app/templates/
├── base.html               # <head>: tailwind.config (map sang CSS token) + nạp CDN; <body x-data="app(month,year)">
├── index.html              # trang chính, include các component
├── login.html
└── components/
    ├── dashboard.html, rooms.html, bills.html, revenue.html, settings.html
    ├── modals.html, toast.html, _lg_filters.html
app/static/
├── js/
│   ├── app.js              # TRANSLATIONS (đầu file) + function app(initialMonth, initialYear) (Alpine component)
│   ├── alpine.min.js, html2canvas.min.js   # nạp local
└── css/
    └── tokens.css          # design tokens (biến CSS :root)
```

## Design system — dùng token, đừng đặt giá trị thô

`tokens.css` định nghĩa biến CSS trong `:root`. `base.html` map các biến này vào Tailwind config (script PHẢI đặt TRƯỚC `<script src="cdn.tailwindcss.com">`). Hệ quả:

- Dùng Tailwind class như `bg-blue-500`, `text-gray-900`, `rounded-lg`, `shadow-md` — chúng **đã được map sang token** (vd `blue-500` → `var(--accent)`, `gray-900` → `var(--ink)`). Cứ dùng class, sẽ ăn theo design system.
- Token chính: màu `--accent`/`--accent-strong`/`--accent-tint`, `--success`/`--warning`/`--danger`/`--info` (mỗi cái có `-tint`), nền `--paper`/`--surface`/`--surface-2`, chữ `--ink`/`--ink-1..3`, viền `--line`/`--line-strong`. Bo góc `--radius-sm..2xl`, shadow `--shadow-xs..xl`, easing/`--duration-*`.
- Font: `--font-body` (Roboto), `--font-display` (Roboto SemiCondensed). Dùng class `font-sans`/`font-display`.
- **Đừng** hardcode hex màu hay px tùy tiện phá vỡ token. Cần giá trị mới → thêm token vào `tokens.css` rồi tham chiếu.
- Đổi `tokens.css` → tăng query version trong base.html (`tokens.css?v=10` → `?v=11`) để bust cache.

## Alpine component — app.js

- Một hàm `app(initialMonth, initialYear)` trả về object chứa **toàn bộ** state (bills, rooms, settings, trạng thái modal, filter, ngôn ngữ...) và method.
- `init()` chạy lúc load: `await Promise.all([this.loadData(), this.loadSettings(), this.loadRooms()])`.
- Giao tiếp backend bằng `fetch('/api/...')`. Pattern có sẵn: `loadData()` (bills theo tháng), `loadRooms()`, `loadSettings()`. Sau khi thao tác ghi (mark-paid...), gọi lại `loadData()` để refresh.
- Khi thêm tính năng cần dữ liệu mới: thêm method `fetch` mới theo đúng pattern, gọi trong `init()` hoặc khi cần.
- **Map field đúng tên** với shape JSON backend trả. Đọc `_workspace/backend_changes.md` nếu backend vừa đổi. Sai tên field = lỗi biên (QA sẽ bắt).

## i18n — TRANSLATIONS (BẮT BUỘC)

- Object `TRANSLATIONS` ở đầu `app.js` có 5 ngôn ngữ: `vi`, `en`, `ko`, `ja`, `zh`.
- **Mọi text hiển thị mới phải thêm key vào CẢ 5 ngôn ngữ.** Không hardcode chuỗi trong template hay JS.
- Một số key lồng object (vd `tabs`, `status_map`, `settingLabels`) — thêm vào đúng nhánh cho cả 5 ngôn ngữ.
- Trong template/JS lấy text qua cơ chế dịch hiện có (tra cách `t(...)` / truy cập theo `lang` đang dùng trong app.js trước khi thêm key).

## Thêm/sửa UI — quy trình

1. Đọc component tương tự trong `app/templates/components/` để bắt chước cấu trúc + class.
2. Sửa markup (Jinja2 + Tailwind class theo token). Logic động dùng directive Alpine (`x-data` đã có ở body, dùng `x-show`/`x-for`/`@click`/`x-text`...).
3. Cần state/hành vi mới → thêm vào object `app()` trong `app.js`.
4. Text mới → thêm key vào `TRANSLATIONS` (5 ngôn ngữ).
5. Cần dữ liệu từ server → thêm/gọi `fetch`, map đúng field.

## Khi cần thẩm mỹ cao

Với giao diện mới cần chất lượng thiết kế cao (layout mới, component phức tạp), cân nhắc dùng kèm skill `frontend-design` để có hướng thẩm mỹ tốt — nhưng vẫn tuân thủ token và i18n của RentFlow ở trên.

## Checklist trước khi xong

- [ ] Dùng Tailwind class/token, không hardcode màu/spacing phá design system
- [ ] Text mới đã có đủ trong 5 ngôn ngữ của `TRANSLATIONS`
- [ ] State/method mới đặt trong component `app()`, không tách rời
- [ ] Field đọc từ API khớp đúng shape backend trả
- [ ] Nếu sửa `tokens.css` → đã bump `?v=` trong base.html
