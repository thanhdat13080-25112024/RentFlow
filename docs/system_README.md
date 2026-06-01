# RentFlow — Design System

> **Streamline housing.** RentFlow is a housing & rental platform based in Hà Nội,
> Việt Nam (EST 2026). It helps renters find, tour, and lease homes — and helps
> landlords list and manage them — with a calm, focused, friction-free experience.

This repository is a **design system**: brand foundations (color, type, spacing,
motion), real brand assets (logo, icon), and high-fidelity **UI kits** that recreate
RentFlow's product surfaces so designers and agents can build on-brand artifacts fast.

---

## Sources provided

The system was built from two brand assets uploaded by the team:

| File | What it is |
|------|------------|
| `uploads/Ảnh màn hình 2026-06-01 lúc 13.04.17.png` | Primary logo lockup — `rentflow` wordmark, "EST 2026 / HA NOI CITY, VNA", tagline "Streamline housing" |
| `uploads/Ảnh màn hình 2026-06-01 lúc 13.07.50.png` | App icon mark — house outline with an upward arrow |

> No codebase or Figma file was supplied. Product surfaces in `ui_kits/` are an
> **original, on-brand interpretation** of a rental platform built strictly from the
> brand foundations below — not a copy of an existing RentFlow product. If a real
> codebase or Figma exists, share it and the kits will be re-derived for pixel fidelity.

**Brief from the team (vi):** *"Phong cách minimalism, nhẹ nhàng mềm mại, có chức năng
giúp tăng khả năng tập trung. Font chữ to. Màu sắc tương phản."* →
Minimalist, gentle & soft, designed to **increase focus**, **large type**, **high contrast**.

---

## Brand at a glance

- **Name / wordmark:** `rentflow`, always lowercase, set in a heavy geometric sans.
- **Tagline:** *Streamline housing.*
- **Origin line:** *EST 2026 · HA NOI CITY, VNA* (used as a footer/credential mark).
- **Icon:** a house silhouette with an upward arrow — "find your way up / move up."
- **Core palette:** charcoal ink `#373737` / near-black `#1A1C1D` on warm cream `#F0F0EC`.
- **Personality:** quiet, trustworthy, unhurried. Helps you focus on one decision at a time.

---

## Content fundamentals

**Voice.** Calm, plain-spoken, and reassuring — like a level-headed friend who has
rented before. RentFlow removes anxiety from a stressful process; copy never hypes
or pressures.

- **Person:** Speak to the reader as **"you."** RentFlow refers to itself as **"we."**
- **Casing:** **Sentence case** everywhere — buttons, headings, menus. The only
  all-caps usage is the **overline/eyebrow** label style and the origin mark
  (`EST 2026`). The wordmark is always all-lowercase.
- **Tone:** confident but soft. Short sentences. Verbs first on actions
  ("Book a tour", "Save this home", "Message the host").
- **Numbers & money:** prices shown clearly with currency — `₫6,500,000/mo` (VND) or
  `$280/mo` depending on locale. RentFlow is Vietnam-first, so **VND (₫) is primary**;
  EN/USD is the secondary locale.
- **Bilingual:** product is comfortable in **Vietnamese and English**. Keep strings
  short so both fit. Vietnamese examples: "Tìm nhà", "Đặt lịch xem", "Lưu".
- **Emoji:** **not used** in product UI. Personality comes from type and space, not emoji.
- **Punctuation:** minimal. No exclamation marks in transactional copy.

**Copy examples**
- Hero: *"Find a home you'll actually love. Streamline the search, the tour, the lease."*
- Empty state: *"No saved homes yet. Tap the heart on any listing to keep it here."*
- Confirmation: *"Tour booked. We'll remind you an hour before."*
- Microcopy (button): *"Book a tour"* · *"Message host"* · *"Apply to rent"*
- Origin mark: *"EST 2026 · HÀ NỘI"*

---

## Visual foundations

**Color.** A two-tone foundation does the heavy lifting: **warm cream paper**
(`#F0F0EC`) and **charcoal ink** (`#373737` / `#1A1C1D`). This is the "high contrast"
the brief asks for — but warm, not stark white/black, so it stays gentle on the eyes
and supports long, focused reading. A single **calm sage accent** (`#466B53`) marks
primary actions and selected states; it reads as trustworthy and quiet, never loud.
Semantic colors (success/warning/danger/info) are **desaturated and warm-leaning** so
alerts never break the calm. Avoid introducing new hues — the system is deliberately
near-monochrome.

**Type.** Roboto, self-hosted, across three widths:
- **Roboto SemiCondensed** (Black/Bold) for **display & headings** — tall, confident,
  space-efficient, echoes the tight wordmark.
- **Roboto** (Light → Black) for **body and UI** — set **large** (17px base, up from
  the usual 16) to honor "font chữ to" and reduce reading strain.
- **Roboto Condensed** (Medium/Bold) for **overlines, tags, and dense data**, always
  uppercase with wide tracking (`.14em`).
- Generous line-height (1.6 body), tight negative tracking on big display.

**Space & layout.** Airy. Lots of paper showing through; whitespace is the primary
"separator," not borders. 4px spacing base. Content sits on comfortable max-widths;
single-column reading and one clear primary action per screen support focus. Fixed
elements: a top app bar and (on mobile) a bottom tab bar; both sit on paper with a
hairline, never heavy chrome.

**Backgrounds.** Flat warm paper — **no gradients, no patterns, no textures**.
Imagery (listing photos) provides the only color and richness; everything around it
stays neutral so the photos breathe. When photos sit on dark overlays, use a charcoal
scrim at low opacity, never a colored gradient.

**Imagery vibe.** Real interior/exterior **photography**, natural warm daylight,
lived-in and uncluttered. Slightly warm white balance to match the cream. Avoid
cold/blue tones, heavy filters, and stocky staged shots. Photos are presented in
soft-cornered frames (`--r-lg`).

**Corner radii.** Soft and consistent: cards `--r-lg` (20px), buttons/inputs
`--r-md` (14px), pills/avatars `--r-pill`. Nothing sharp; nothing fully circular
except avatars and icon chips.

**Cards.** Surface `#FBFBF9` on paper, **1px `--line` hairline border** plus a
**very soft shadow** (`--shadow-sm`/`--shadow-md`). Radius 20px. Generous internal
padding (20–24px). Cards rarely stack heavy shadows — elevation is whisper-quiet.

**Shadows.** Low, soft, neutral (charcoal at 5–16% alpha). Used sparingly for
raised cards, menus, and modals. No colored or glowing shadows except the accent
**focus ring** (`--shadow-focus`).

**Borders.** Hairline `1px` `--line` (`#DCDCD4`) for dividers and card edges;
`--line-strong` for input borders and stronger separation. Borders are quiet —
prefer space over rules where possible.

**Transparency & blur.** Used lightly: a translucent paper bar (`backdrop-filter:
blur`) when content scrolls under the top bar. Otherwise surfaces are opaque.

**Motion.** Calm and quick. Fades and gentle slides (8–12px), `--dur` 200ms,
`--ease`/`--ease-soft`. **No bounces, no spring overshoot, no parallax.** Motion
should feel like settling, not bouncing — it supports focus.

**Hover states.** Subtle: surfaces shift to `--surface-2`, primary buttons darken to
`--accent-strong`, links gain underline or the accent color. ~`--dur-fast`.

**Press states.** A small scale-down (`transform: scale(.98)`) and/or a step darker.
Quick and tactile, never dramatic.

**Focus.** Always visible — `--shadow-focus` (3px sage ring). Accessibility first;
the brand's calm depends on clarity.

---

## Iconography

- **Style:** **line icons, ~1.75px stroke, rounded caps & joins**, on a 24px grid.
  This matches the open, geometric, friendly feel of the house-arrow mark.
- **Set:** RentFlow does not ship a proprietary icon font. The kits use
  **[Lucide](https://lucide.dev)** (loaded from CDN) as the closest match to the
  brand's rounded-stroke line style. **→ FLAGGED substitution:** if RentFlow has its
  own icon set, drop it into `assets/icons/` and swap the Lucide references.
- **Brand mark vs UI icons:** the **house-with-arrow** is the *logo mark* (in
  `assets/`), not a UI icon — don't use it inline in lists/buttons.
- **Color:** icons inherit text color (`--ink-1` default, `--ink-3` muted,
  `--accent` when active). No multi-color icons.
- **Emoji / unicode-as-icon:** not used.

---

## Assets (`assets/`)

| File | Use |
|------|-----|
| `rentflow-lockup.png` | Full logo lockup (wordmark + origin + tagline) on cream |
| `rentflow-wordmark.png` | `rentflow` wordmark only, charcoal on cream — headers, footers |
| `rentflow-icon.png` | App icon — white house-arrow on near-black tile |
| `rentflow-mark-white.png` | House-arrow mark, white, transparent bg — for dark surfaces |
| `rentflow-mark-charcoal.png` | House-arrow mark, charcoal, transparent bg — for paper |

> The wordmark's exact letterforms are slightly custom; the PNG is canonical. For
> live text, Roboto SemiCondensed/Black lowercase is the approved fallback.

---

## Index — what's in this system

| Path | What |
|------|------|
| `README.md` | This file — context, voice, visual foundations, iconography, index |
| `colors_and_type.css` | All design tokens (color, type, spacing, radii, shadow, motion) + semantic type classes |
| `SKILL.md` | Agent-Skill manifest for using this system in Claude Code |
| `assets/` | Logos, icon marks (see table above) |
| `fonts/` | Self-hosted Roboto / Roboto Condensed / Roboto SemiCondensed (TTF) |
| `preview/` | Design-system preview cards (color, type, spacing, components) |
| `ui_kits/app/` | **Mobile rental app** UI kit — screens + JSX components + `index.html` |
| `ui_kits/web/` | **Marketing & listings website** UI kit — screens + JSX components + `index.html` |

### Quick start
1. Link the tokens: `<link rel="stylesheet" href="colors_and_type.css">`.
2. Use the semantic classes (`.rf-h1`, `.rf-body`, `.rf-overline`…) or the CSS vars.
3. Pull brand assets from `assets/`; Lucide icons from CDN.
4. For product mockups, lift components from the relevant `ui_kits/<product>/`.

---

## Caveats & substitutions
- **Icons:** Lucide (CDN) substituted for an unknown proprietary set — flag above.
- **Mono type:** no brand mono supplied; system-mono stack used. Provide one if needed.
- **Product surfaces:** designed from brand foundations only (no codebase/Figma given).
- **Accent color:** the sage accent is an addition — the source assets are monochrome.
  Confirm or replace it.
