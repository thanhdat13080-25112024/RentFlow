# RentFlow — Glass/Aurora Design Direction

## 1. Tinh thần thiết kế

RentFlow Glass/Aurora lấy cảm hứng từ ánh sáng cực quang lọc qua tấm kính mờ — bề mặt trong suốt, mềm mại, xếp chồng lên nhau tạo chiều sâu thay vì dùng shadow nặng. Màu sắc không tĩnh: gradient dịch chuyển từ violet → indigo → cyan gợi lên cảm giác dữ liệu đang "sống" và chuyển động. Mỗi card là một tấm glass nổi trên nền aurora mờ, ranh giới được định nghĩa bằng ánh sáng thay vì đường viền cứng. Tổng thể hướng đến cảm giác premium, hiện đại, nhẹ nhàng — không phải dark neon mà là "ánh sáng ban ngày đi qua tấm kính".

---

## 2. Palette

### 2.1 Màu chính (6 màu)

| Token | Tên | Hex | Vai trò |
|-------|-----|-----|---------|
| `--aurora-violet` | Aurora Violet | `#7C3AED` | Brand primary, CTA chính, icon accent |
| `--aurora-indigo` | Aurora Indigo | `#4338CA` | Hover state, secondary action, gradient điểm cuối |
| `--aurora-cyan` | Aurora Cyan | `#0891B2` | Accent lạnh, chart bar, link hover |
| `--aurora-teal` | Aurora Teal | `#0D9488` | Điểm nhấn tích cực, icon success phụ |
| `--aurora-midnight` | Midnight | `#1E1B4B` | Text tối nhất, heading chính, nền modal overlay |
| `--glass-bg` | Glass Background | `#F5F3FF` | Nền tổng thể — trắng pha tím nhạt, tạo nền cho hiệu ứng glass |

> **Gradient aurora** (dùng cho logo, hero, stat tile accent):
> `linear-gradient(135deg, #7C3AED 0%, #4338CA 40%, #0891B2 100%)`

### 2.2 Màu trạng thái (4 màu)

| Token | Tên | Hex | Trạng thái |
|-------|-----|-----|------------|
| `--status-paid` | Aurora Emerald | `#059669` | Paid — đã thu |
| `--status-unpaid` | Aurora Red | `#DC2626` | Unpaid — chưa thu |
| `--status-prepaid` | Aurora Violet (reuse) | `#7C3AED` | Prepaid — đóng trước (dùng brand color để tạo cảm giác "đặc biệt/ưu tiên") |
| `--status-warning` | Aurora Amber | `#D97706` | Warning — cần chú ý |

---

## 3. Typography

### Font chọn

| Vai trò | Font | Google Fonts |
|---------|------|-------------|
| **Display** (heading, số lớn, stat) | **Plus Jakarta Sans** | `family=Plus+Jakarta+Sans:wght@400;500;600;700;800` |
| **Body** (nội dung, label, table cell) | **DM Sans** | `family=DM+Sans:wght@400;500;600` |

### Lý do

**Plus Jakarta Sans** — geometric-humanist, có nét cạnh dứt khoát nhưng không lạnh như Inter. Bộ số (0–9) rất cân đối, rendering tốt ở size lớn — phù hợp cho stat tiles hiển thị tiền tệ. Hỗ trợ đầy đủ ký tự tiếng Việt (Latin Extended).

**DM Sans** — optical size nhỏ hơn Inter, stroke weight mềm hơn, cảm giác "thoáng" hơn ở paragraph nhỏ. Kết hợp với Plus Jakarta Sans tạo tương phản rõ ràng giữa heading và body mà không cần tăng font-size. Cũng hỗ trợ tiếng Việt tốt.

### Scale

```
--text-xs:   0.75rem   / 12px  — badge, caption, th-cell
--text-sm:   0.875rem  / 14px  — body, table cell, label
--text-base: 1rem      / 16px  — default body
--text-lg:   1.125rem  / 18px  — subheading
--text-xl:   1.25rem   / 20px  — section title
--text-2xl:  1.5rem    / 24px  — page title
--text-3xl:  1.875rem  / 30px  — stat value lớn
```

---

## 4. Border Radius Scale

Glass/Aurora dùng radius lớn hơn để các bề mặt trông "mềm", tương thích với hiệu ứng blur phía sau.

| Token | Value | Dùng cho |
|-------|-------|----------|
| `--radius-xs` | `0.25rem` / 4px | Dot indicator, progress bar, divider accent |
| `--radius-sm` | `0.5rem` / 8px | Badge, chip, input nhỏ, tooltip |
| `--radius-md` | `0.875rem` / 14px | Button, input field, dropdown item |
| `--radius-lg` | `1.25rem` / 20px | Card, panel, dropdown container, tab nav |
| `--radius-xl` | `2rem` / 32px | Modal dialog, glass sheet lớn, hero card |

> **Rule**: Component càng to, radius càng lớn. Không bao giờ dùng `border-radius: 0` cho element có `backdrop-blur`.

---

## 5. Shadow Scale

Glass/Aurora thay thế shadow truyền thống bằng **glow** có màu — ánh sáng phát ra từ bên trong thay vì đổ xuống. Shadow tối chỉ dùng cho overlay/modal.

| Token | Value | Feel |
|-------|-------|------|
| `--shadow-glass-xs` | `0 1px 2px rgba(30, 27, 75, 0.04), inset 0 1px 0 rgba(255,255,255,0.6)` | Ranh giới nhẹ — glass float sát nền, gần như phẳng |
| `--shadow-glass-sm` | `0 2px 8px rgba(30, 27, 75, 0.06), 0 1px 2px rgba(30, 27, 75, 0.04), inset 0 1px 0 rgba(255,255,255,0.5)` | Card thông thường — nổi nhẹ, có "rim light" trên đỉnh |
| `--shadow-glass-md` | `0 8px 24px rgba(30, 27, 75, 0.08), 0 2px 6px rgba(30, 27, 75, 0.05), inset 0 1px 0 rgba(255,255,255,0.45)` | Panel nổi — modal sub-section, stat tile hover |
| `--shadow-glow-violet` | `0 0 0 3px rgba(124, 58, 237, 0.15), 0 8px 24px rgba(124, 58, 237, 0.12)` | Aurora glow — focus ring, CTA button hover, selected state |
| `--shadow-overlay` | `0 24px 64px rgba(15, 10, 40, 0.28), 0 8px 24px rgba(15, 10, 40, 0.16)` | Modal dialog full — tối, sâu, cắt khỏi nền |

> **Inset highlight** (`inset 0 1px 0 rgba(255,255,255,N)`) là yếu tố tạo cảm giác "kính" — bắt buộc trên card và button.

---

## 6. Motion

### Easing Curves

| Token | Curve | Dùng cho |
|-------|-------|----------|
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Modal open, toast appear, element "bật" vào — có nhảy vượt nhẹ (overshoot) tạo cảm giác vật lý |
| `--ease-smooth` | `cubic-bezier(0.4, 0, 0.2, 1)` | Tab switch, state change, scroll-linked animation — mượt, không quá rõ |
| `--ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | Dismiss, close, fade out — nhanh đầu, chậm cuối, element "thu" lại tự nhiên |

### Duration

| Token | Value | Dùng cho |
|-------|-------|----------|
| `--dur-micro` | `80ms` | Hover background, icon color, border color — phản hồi tức thì |
| `--dur-fast` | `200ms` | Button press, badge change, checkbox toggle — rõ nhưng không chậm |
| `--dur-modal` | `320ms` | Modal open/close, panel slide, toast — đủ thời gian để user nhận ra ngữ cảnh thay đổi |

> **Rule tổng quát**: `--ease-spring` chỉ dùng cho enter (vào), không dùng cho exit — exit luôn dùng `--ease-exit` để không bị "nảy rồi biến mất" trông kỳ.

---

## 7. Iconography

### Style

**Lucide Icons** (line icons, stroke 1.5px) — thay thế Font Awesome.

- **Line (regular)**: dùng mặc định cho navigation, action button, label icon
- **Filled**: dùng cho trạng thái active/selected (tab đang chọn, checkbox checked)
- **Duotone** (Lucide không có sẵn — tự implement bằng 2 element chồng): dùng cho icon lớn trong stat tile và empty state, layer thứ hai tô màu aurora với opacity 40%

### Kích thước mặc định

| Context | Size | Note |
|---------|------|------|
| Nav / tab icon | `16px` | Inline với text label |
| Button icon | `14px` | Tight với label, gap `6px` |
| Stat tile icon | `20px` | Trong icon container 40×40 |
| Empty state icon | `40px` | Standalone, color `--aurora-violet` at 30% opacity |
| Toast / alert icon | `16px` | Vertically centered với text |

### Stroke weight

Tất cả Lucide icons render với `stroke-width="1.5"` — không dùng `2` (quá nặng, phá glass feel) và không dùng `1` (quá mảnh, mất chi tiết ở size nhỏ).

---

## 8. Status Badge — 5 ví dụ phối màu

Tất cả badge dùng **glass formula**: nền màu opacity thấp + viền cùng màu opacity trung bình + text màu đậm + dot indicator.

```
Cú pháp chung:
  background : rgba(R, G, B, 0.12)
  border     : 1px solid rgba(R, G, B, 0.25)
  border-radius: var(--radius-sm)
  padding    : 2px 10px
  font-size  : var(--text-xs) — 12px
  font-weight: 700
```

### Badge 1 — Paid (Đã thu)

```
background : rgba(5, 150, 105, 0.12)    → emerald tint
border     : 1px solid rgba(5, 150, 105, 0.28)
color      : #065F46                    → emerald-800, đủ contrast
dot color  : #10B981                    → emerald-500, sáng hơn text
label      : "Đã thu"
```

### Badge 2 — Unpaid (Chưa thu)

```
background : rgba(220, 38, 38, 0.10)    → red tint nhẹ
border     : 1px solid rgba(220, 38, 38, 0.25)
color      : #991B1B                    → red-800
dot color  : #EF4444                    → red-500
label      : "Chưa thu"
```

### Badge 3 — Prepaid (Đóng trước)

```
background : rgba(124, 58, 237, 0.10)   → violet tint — dùng brand color
border     : 1px solid rgba(124, 58, 237, 0.25)
color      : #4C1D95                    → violet-900
dot color  : #8B5CF6                    → violet-500
label      : "Đóng trước"
```

### Badge 4 — Warning (Cần chú ý)

```
background : rgba(217, 119, 6, 0.10)    → amber tint
border     : 1px solid rgba(217, 119, 6, 0.28)
color      : #92400E                    → amber-800
dot color  : #F59E0B                    → amber-400
label      : "Cần chú ý"
```

### Badge 5 — Vacant (Trống / Neutral)

```
background : rgba(100, 116, 139, 0.08)  → slate tint — chủ động "mờ"
border     : 1px solid rgba(100, 116, 139, 0.18)
color      : #475569                    → slate-600
dot color  : #94A3B8                    → slate-400, dashed border thay dot
label      : "Trống"
```

> **Không dùng** `border-radius: 9999px` (pill) cho badge Aurora — dùng `--radius-sm` (8px) để badge trông "chắc" hơn, hòa với aesthetic glass thay vì lơ lửng.
