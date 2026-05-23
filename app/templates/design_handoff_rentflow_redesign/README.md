# Handoff: RentFlow UI Redesign (Quản Lý Trọ)

> Gói tài liệu bàn giao cho **Claude Code** để rebuild lại UI của app FastAPI + Alpine.js.

---

## 1. Tổng quan

Đây là gói **wireframe khám phá** cho việc thiết kế lại giao diện app quản lý nhà trọ hiện tại (`templates/index.html` — 836 dòng, một-file-tất-cả-trong-một).

Có **6 hướng wireframe** (A → F) trình bày trên cùng 1 canvas tương tác. Mục đích là user/chủ trọ chọn 1-2 hướng ưng ý, sau đó developer (Claude Code) implement lại trong codebase thật.

**Backend không thay đổi** — toàn bộ FastAPI endpoints, schemas, SQLAlchemy models giữ nguyên. Chỉ thay frontend.

---

## 2. Về các file trong gói này

**Quan trọng:** các file `.html`/`.jsx` trong gói này là **design reference** — prototype thể hiện ý tưởng layout, không phải code production để copy nguyên.

Nhiệm vụ của Claude Code là:
- **Hiểu cấu trúc và pain point** mà mỗi wireframe giải quyết
- **Rebuild lại** trong stack hiện tại của project: **FastAPI (Jinja2 template) + Alpine.js + Tailwind CSS**
- **Giữ nguyên toàn bộ logic Alpine.js và API calls** trong `templates/index.html` hiện tại — chỉ thay đổi HTML/CSS markup
- Không phá vỡ các endpoint hiện có (xem mục API Contract bên dưới)

---

## 3. Fidelity

**Low-fidelity (wireframe).** Đây là sketch hand-drawn với font Patrick Hand, dùng để thảo luận layout và flow. Khi implement thật:
- **Layout, cấu trúc, vị trí** → copy chính xác từ wireframe đã chọn
- **Visual style (font, màu, shadow)** → KHÔNG dùng look hand-drawn. Dùng style modern/professional với:
  - Font: `Inter`, `system-ui`, hoặc font sans-serif chuyên nghiệp khác (tránh font hand-drawn)
  - Màu: theo mục **Design Tokens** bên dưới
  - Tailwind utilities chuẩn (`rounded-xl`, `shadow-sm`, `border`, v.v.)

---

## 4. Pain points cần fix (ưu tiên cao)

Đây là phần **quan trọng nhất** — wireframe được vẽ để giải quyết các vấn đề này, do user chỉ ra:

| # | Vấn đề hiện tại | Giải pháp trong wireframe |
|---|---|---|
| 1 | Bảng 12 cột, phải scroll ngang trên màn nhỏ | **C/D**: rút bảng xuống 5 cột + dùng card view; chi tiết dồn vào side panel hoặc modal |
| 2 | Input số điện nhúng thẳng trong bảng, disabled không trực quan | **C**: tách input điện ra panel chi tiết riêng, có label rõ "Số cũ → Số mới → Sử dụng" |
| 3 | Luồng "Đóng trước" khó hiểu (phải bấm trạng thái 2 lần) | **C**: nút **"📅 Đóng trước nhiều tháng"** đứng riêng, bấm 1 lần là ra modal nhập tháng |
| 4 | Tổng số phòng hardcode `18` | **Tất cả wireframe**: lấy từ `/api/rooms` (count). Sticky note ở wireframe A nhắc fix này |
| 5 | `alert()` cho lỗi, `toast` cho thành công — không nhất quán | Implement: thêm **toast đỏ** cho error (giống toast xanh hiện tại, chỉ đổi màu + icon) |
| 6 | "Dữ liệu trực tuyến: {time}" giả — render 1 lần không cập nhật | **Bỏ hoàn toàn** dòng này. Không cần "live indicator" giả |
| 7 | Không có empty state | Khi filter ra 0 phòng → hiển thị illustration + message ("Tất cả đã được thu! 🎉") |
| 8 | Bảng 12 cột không dùng được trên mobile | **F**: card stack mobile + bottom nav. Below `md` breakpoint chuyển sang card view |

**Tính năng mới đã thêm vào wireframe:**
- ⌕ Search bar (tìm phòng / tên khách / SĐT) — header trên cùng
- ⚠ "Phòng cần chú ý" widget — highlight phòng chưa thu, có nút quick action
- 📊 Biểu đồ doanh thu trend (bar chart 6-12 tháng) trong tab Doanh thu/Dashboard
- 🎯 Highlight ô số điện nếu `new_reading === 0` (chưa nhập điện tháng này)
- ⌨ Hiển thị phím tắt `← →` ở footer hoặc tooltip
- 🔀 Tab structure rõ ràng: **Tổng quan / Phòng & Khách / Hóa đơn tháng / Doanh thu / Cài đặt**

---

## 5. Tab structure (quyết định cuối cùng)

App chia thành **5 tab** chính, top navigation:

| Tab | Đường dẫn gợi ý | Nội dung |
|---|---|---|
| **Tổng quan** | `/` hoặc `/dashboard` | Stats, biểu đồ doanh thu, donut trạng thái, "phòng cần chú ý" |
| **Phòng & Khách** | `/rooms` | Danh sách phòng dạng card grid theo tầng, thêm/sửa/xóa phòng |
| **Hóa đơn tháng** | `/bills?month=N&year=Y` | Bảng hóa đơn tháng đang chọn + side detail panel (hoặc modal) |
| **Doanh thu** | `/revenue` | Báo cáo theo tháng, có thể thêm heatmap năm (wireframe E) |
| **Cài đặt** | `/settings` | Cấu hình giá điện, ngân hàng, chủ tài khoản (giữ y như cũ) |

---

## 6. Các wireframe (6 hướng) — chi tiết

> File: `wireframes.html` — mở trong browser, dùng chuột pan/scroll-zoom để xem cả 6. Tweaks panel (góc dưới phải) có nút đổi accent color.

### A · Tổng quan dạng Analytics Dashboard
**Tab:** Tổng quan
**Layout:**
- Header: lời chào ("Chào buổi sáng, Cô Lan") + button "Import CSV" + "Ghi điện tháng này"
- **6 stat tiles** ngang: Tổng phòng / Chưa thu / Đã thu / Đóng trước / Doanh thu T11 / Tiền cọc giữ
- Grid 2 cột:
  - Trái (2/3): biểu đồ bar 6 tháng gần nhất, có toggle 6T/12T/2025
  - Phải (1/3): donut "Đã thu / Chưa thu / Đóng trước" + legend số
- Grid 2 cột dưới:
  - Trái: "⚠ Phòng cần chú ý" — list các phòng chưa thu, mỗi dòng có avatar + tên + tổng + nút "Nhắc" + "✓ Thu"
  - Phải: "Hoạt động gần đây" — feed các sự kiện (đã thanh toán / đóng trước / cập nhật điện) có timestamp

### B · Tổng quan Workflow-first
**Tab:** Tổng quan (variant)
**Layout:**
- Hero card đen lớn: "Tháng 11/2025" + 3 số (Dự kiến / Đã thu / Còn lại) + progress bar 73%
- Mini donut bên phải
- **🎯 "Việc cần làm tháng này"** — 4 ActionCard ngang:
  1. ⚡ Ghi số điện hàng loạt (urgent, có badge "cần xử lý")
  2. 📨 Gửi hóa đơn QR
  3. 📅 Đóng trước nhiều tháng
  4. 📥 Import CSV / sao lưu
- Grid 2 cột dưới: biểu đồ 12 tháng + list phòng chưa thu

**Khi nào dùng:** chủ trọ thao tác theo workflow tháng, không chỉ xem số.

### C · Hóa đơn — Master/Detail
**Tab:** Hóa đơn tháng
**Layout:**
- Filter bar: tabs (Tất cả · 15 / Chưa thu · 4 / Đã thu · 11 / Đóng trước · 3) + search + filter tầng + sort + button "Xuất CSV" + "Gửi nhắc nhở (4)"
- **Grid 2 cột (~ 1:1.1):**
  - **Trái — bảng compact 5 cột:** Phòng (số) / Khách thuê (tên + sđt) / Tổng / Trạng thái pill
    - Row được chọn: highlight nền hồng + border trái accent
  - **Phải — detail panel:**
    - Header: avatar số phòng to + tên + sđt + status pill
    - Card "Số điện tháng N": 3 ô (Số cũ / [input Số mới] / Sử dụng kWh) — input rõ ràng, KHÔNG bị disabled vô lý
    - Card "Chi tiết tháng này": breakdown Tiền phòng / Dịch vụ / Tiền điện (× đơn giá) = Tổng cộng lớn
    - 4 button: ✓ Đánh dấu đã thu / 📅 Đóng trước / 🔲 Xem QR / 🕒 Lịch sử
    - Footer: Tiền cọc + số tháng đã thuê

**Đây là hướng giải quyết pain point #1, #2, #3 đẹp nhất.**

### D · Phòng & Khách — Card grid theo tầng
**Tab:** Phòng & Khách
**Layout:**
- Sub-header: "18 phòng · 15 đang thuê · 3 trống" + search + filter tabs + button "+ Thêm phòng"
- Body: **các section theo tầng**, mỗi tầng có heading "Tầng N" + đường kẻ
- Mỗi tầng: **grid 4 cột × N rows** card phòng
- **Card phòng** chứa:
  - Số phòng to (32px, màu theo trạng thái)
  - Status pill (Chưa thu / Đã thu / Đóng trước / Trống)
  - Tên khách + SĐT
  - Tổng tháng + label
  - Mini input điện inline (cũ → mới)
  - 3 button nhỏ: ✓ Thu (nếu chưa thu) / 🔲 QR / ⋯
- Card phòng trống: dashed border, icon mờ, button "+ Thêm khách thuê"

**Responsive:** card grid co từ 4 → 3 → 2 → 1 cột theo viewport. Cực hợp mobile.

### E · Hóa đơn — Heatmap cả năm
**Tab:** Doanh thu (hoặc tab phụ trong Hóa đơn)
**Layout:**
- Sub-header: tabs năm (2024 / **2025** / 2026) + legend màu + button "Xuất Excel"
- Body grid:
  - **Trái (heatmap):** bảng 18 hàng (phòng) × 12 cột (tháng T1..T12) + cột "Tổng năm"
    - Mỗi ô: rectangle nhỏ, màu theo status (xanh=đã thu, đỏ=chưa thu, xanh dương=đóng trước, xám=trống/chưa tới)
    - Ô của tháng hiện tại có border đậm + chấm cảnh báo
    - Hover/click ô → highlight + show popover detail
  - **Phải (sidebar):**
    - Card "Đã chọn ô" — chi tiết bill của ô đang chọn + 2 button (Thu / QR)
    - Card "Doanh thu 2025" — số tổng + mini bar chart 11 tháng

**Mục đích:** audit nhanh cả năm, ai chưa thu tháng nào, ai đóng trước.

### F · Mobile — Card stack + Bottom nav
**Cho mobile (< md breakpoint).** Hiển thị 3 màn:

**F1. Mobile Dashboard:**
- Top bar: title + month nav
- Hero card đen: "ĐÃ THU THÁNG 11" + 45.2M/61.8M + progress bar
- 2×2 mini stats
- "⚠ Cần thu" list 2 phòng có nút ✓ inline
- Bottom nav 4 icon: Tổng quan / Phòng / Hóa đơn / Khác

**F2. Mobile Bill List (card stack):**
- Top bar: "Hóa đơn T11"
- Search input
- Tabs (Tất cả / Chưa thu / Đã thu)
- List **card phòng dọc** — mỗi card: số phòng to + tên + sđt + status pill + tổng + button "✓ Thu / 🔲 QR / ⋯" (chỉ hiện khi card đang select)
- Bottom nav

**F3. Mobile Bill Detail:**
- Top bar: ‹ back + "Hóa đơn T11" + ⋮
- Header card hồng: số phòng to + tên + sđt + ngày thuê
- Card "Số điện": Cũ → Mới (input) → kWh
- Card breakdown: Phòng / Dịch vụ / Điện = Tổng
- Button to "✓ Đánh dấu đã thu"
- 2 button nhỏ: 📅 Đóng trước / 🔲 QR
- Bottom nav

---

## 7. Design Tokens (cho bản hi-fi production)

> Wireframe dùng style hand-drawn, nhưng **bản production phải dùng style modern**. Token gợi ý:

### Màu sắc (Tailwind class)

```css
/* Brand */
--accent-primary: #2563eb;       /* blue-600 — nút chính, link, focus */
--accent-soft: #dbeafe;          /* blue-100 — nền nhạt */

/* Status */
--success: #16a34a;              /* green-600 — đã thu */
--success-soft: #dcfce7;         /* green-100 */
--danger: #dc2626;               /* red-600 — chưa thu, lỗi, urgent */
--danger-soft: #fee2e2;          /* red-100 */
--info: #2563eb;                 /* blue-600 — đóng trước */
--info-soft: #dbeafe;
--warning: #d97706;              /* amber-600 — cảnh báo */
--warning-soft: #fef3c7;

/* Neutrals */
--ink-900: #111827;              /* text chính */
--ink-700: #374151;              /* text phụ */
--ink-500: #6b7280;              /* placeholder, label */
--ink-300: #d1d5db;              /* border, divider */
--ink-100: #f3f4f6;              /* nền nhẹ */
--paper: #ffffff;                /* nền chính */
--paper-2: #f9fafb;              /* nền card phụ */
```

User chọn "Decide for me" cho màu accent — gợi ý **blue-600** vì giữ tinh thần hiện tại (đã có nhiều `blue-600` trong code cũ) nhưng có thể đổi sang teal/indigo nếu user muốn.

### Typography (production)

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;

/* Scale */
text-xs:   12px   /* labels, hint, badge */
text-sm:   14px   /* body phụ, mô tả */
text-base: 16px   /* body chính */
text-lg:   18px   /* heading nhỏ */
text-xl:   20px   /* heading section */
text-2xl:  24px   /* heading page */
text-3xl:  30px   /* số liệu lớn (stat tile) */
text-4xl:  36px   /* hero number */
```

**KHÔNG dùng** font hand-drawn (Patrick Hand, Caveat) trong production. Đó chỉ là phong cách wireframe.

### Spacing scale (Tailwind)
- Gap card: `gap-4` (16px) hoặc `gap-6` (24px)
- Padding card: `p-4` đến `p-6`
- Page padding: `px-6 py-8`
- Border radius: `rounded-lg` (8px) cho input/button, `rounded-xl` (12px) cho card, `rounded-2xl` (16px) cho modal/hero

### Shadow
- Card thường: `shadow-sm` hoặc `border border-gray-200` (chọn 1, đừng dùng cả 2)
- Card hover: `shadow-md`
- Modal: `shadow-2xl`
- **Tránh** `shadow-lg shadow-blue-200` (style cũ hơi loè loẹt)

### Border radius
- Input/button: `rounded-lg` (8px)
- Card: `rounded-xl` (12px)
- Modal: `rounded-2xl` (16px) — không cần `rounded-[2.5rem]` như cũ
- Pill/badge: `rounded-full`

### Components conventions
- Button primary: `bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg font-medium`
- Button secondary: `bg-white border border-gray-300 hover:bg-gray-50 px-4 py-2 rounded-lg`
- Status pill: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {bg-X-100 text-X-700}`
- Input: `border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500`

---

## 8. API Contract (giữ nguyên 100%)

Không được thay đổi endpoint hoặc payload. Liệt kê để Claude Code biết:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/bills?month=N&year=Y` | List hóa đơn tháng |
| GET | `/api/rooms` | List tất cả phòng (dùng để fix pain point #4 — không hardcode 18) |
| POST | `/api/rooms/update` | Cập nhật thông tin phòng |
| GET | `/api/rooms/{room_id}/history` | Lịch sử phòng |
| POST | `/api/electricity` | Cập nhật số điện |
| POST | `/api/bills/mark-paid` | Đánh dấu đã thu |
| POST | `/api/bills/mark-prepaid` | Đóng trước nhiều tháng (`months: [6, 7, 8]`) |
| POST | `/api/import-csv` | Import CSV |
| GET | `/api/settings` | Lấy settings |
| POST | `/api/settings` | Lưu settings |
| GET | `/api/revenue/summary` | Doanh thu summary |

Xem `schemas/schemas.py` để biết payload chính xác.

### Function helpers cần giữ trong Alpine app:
`formatMoney`, `formatInput`, `parseInput`, `formatDate`, `fixDate`, `fixMoney`, `getQRUrl`, `prevMonth`, `nextMonth`, `updateUrl`, `handleKeydown`, `getFloorColor`, `showToast`, `loadData`, `loadSettings`, `loadRevenueSummary`, `handleImport`, `saveSettings`, `openEditModal`, `saveQuickEdit`, `showHistory`, `saveInvoiceAsImage`, `updateElectricity`, `toggleStatus`, `confirmPrepaid`, `showQR`.

---

## 9. State management (Alpine.js)

Giữ nguyên structure `x-data="app()"`. Chỉ refactor các UI state object cho rõ:

```js
{
  // routing/state
  activeTab: 'dashboard',   // 'dashboard' | 'rooms' | 'bills' | 'revenue' | 'settings'
  month, year,
  searchQuery: '',          // MỚI — pain point fix (search)
  filterFloor: 'all',       // MỚI — filter theo tầng

  // data
  bills: [], settings: {}, rooms: [], revenueSummary: [],

  // modals
  qrModal, editRoomModal, roomHistory,
  confirmModal, prepaidModal,
  showSettings, showRevenueModal,

  // notification (MỚI: tách thành 2 loại)
  toast: { show, message, type: 'success' | 'error' },  // pain #5

  // computed
  get filteredBills() { /* tab + searchQuery + filterFloor */ },
  get stats() { /* lấy từ rooms.length, không hardcode 18 */ },
}
```

---

## 10. Implementation order (gợi ý cho Claude Code)

1. **Setup tab structure** — chia `templates/index.html` thành 5 tab views (`<div x-show="activeTab === '...'">`)
2. **Build tab Tổng quan** dựa trên wireframe **A** (đơn giản hơn B)
3. **Build tab Hóa đơn tháng** dựa trên wireframe **C** (master/detail) — đây là tab quan trọng nhất, fix nhiều pain point
4. **Build tab Phòng & Khách** dựa trên wireframe **D** (card grid)
5. **Build tab Doanh thu** — giữ table cũ + thêm bar chart trên cùng (có thể dùng Chart.js hoặc inline SVG)
6. **Build tab Cài đặt** — giữ y như modal cũ nhưng dạng full page
7. **Mobile pass** — test < md breakpoint, đảm bảo bảng → card view (wireframe F)
8. **Empty states** — thêm illustration + message cho mỗi tab khi data rỗng
9. **Toast error** — bổ sung `toast.type = 'error'` (màu đỏ + icon ⚠) cho các `alert()` hiện có
10. **Cleanup**: bỏ "Dữ liệu trực tuyến" timestamp giả, bỏ hardcode 18

---

## 11. Files in this bundle

| File | Mô tả |
|---|---|
| `README.md` | File này |
| `wireframes.html` | Entry point — mở trong browser để xem 6 wireframe |
| `wf-shared.jsx` | Sample data + components dùng chung (TopNav, StatTile, SketchBarChart, SketchDonut, StickyNote) |
| `wf-desktop.jsx` | Components cho wireframe A, C, D |
| `wf-extra.jsx` | Components cho wireframe B (workflow), E (heatmap), F (mobile) |
| `wf-app.jsx` | Main React app — wires design canvas + tweaks panel |
| `design-canvas.jsx` | Starter component — canvas pan/zoom (giúp hiển thị 6 wireframe side-by-side) |
| `tweaks-panel.jsx` | Starter component — tweaks panel (đổi font/color thử) |

---

## 12. Assets

Không có asset hình ảnh. Tất cả emoji icon (⌂ ✓ ⚠ 📅 🔲 ⌕ v.v.) hoặc dùng symbol có sẵn. Trong production có thể thay bằng **Heroicons** hoặc **Lucide** thay cho FontAwesome hiện tại (gọn hơn, không cần CDN nặng).

---

## 13. Câu hỏi trước khi code

Trước khi bắt tay implement, Claude Code nên xác nhận với user:
1. Chốt **1 hướng cho mỗi tab** (mặc định gợi ý: A cho Dashboard, C cho Bills, D cho Rooms, E cho Revenue, F cho Mobile)
2. Chốt **màu accent chính** (gợi ý: blue-600)
3. Có cần giữ FontAwesome không, hay đổi sang Heroicons?
4. Tailwind CSS — giữ CDN (`cdn.tailwindcss.com`) hay build local? CDN ổn cho dev nhưng không nên dùng production lâu dài.
