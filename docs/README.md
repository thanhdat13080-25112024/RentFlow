# RentFlow Website — Design System & Reference

## Overview
This bundle is the **RentFlow design system** plus a high-fidelity reference design for the
RentFlow marketing + listings website. Use it to **refactor the existing website** so it
matches the RentFlow brand: minimalist, calm, focus-friendly, high-contrast charcoal-on-cream,
large Roboto type, soft radii, one calm sage accent.

RentFlow — "Streamline housing." A housing & rental platform based in Hà Nội, Việt Nam (EST 2026).

## About the design files
The HTML/JSX files in this bundle are **design references created in HTML** — prototypes that
show the intended look and behavior. They are **not production code to copy verbatim**. Your job
is to **recreate this look in the target codebase's existing stack** (React, Vue, Next, Astro,
etc.), using its established component patterns, routing, and data layer. Port the *visual design
and interaction*, not the throwaway prototype scaffolding (inline styles, Babel-in-browser, fake
data, picsum images).

If the existing site already has a component library, map these designs onto it. If it doesn't,
adopt the tokens in `colors_and_type.css` as the foundation.

## Fidelity
**High-fidelity (hifi).** Colors, typography, spacing, radii, and interactions are final and
intended to be matched closely. Recreate pixel-accurately with the codebase's libraries.

## Design tokens
All tokens live in `colors_and_type.css` (copy this file in, or translate to your token system —
Tailwind theme, CSS vars, SCSS, etc.). Key values:

**Color**
| Token | Hex | Use |
|-------|-----|-----|
| `--paper` | `#F0F0EC` | page background (warm cream) |
| `--paper-2` | `#E8E8E1` | sunken panels, segmented track |
| `--surface` | `#FBFBF9` | cards |
| `--surface-2` | `#F5F5F1` | hovered rows |
| `--ink` | `#1A1C1D` | display headings, footer/CTA bg, icon mark |
| `--ink-1` | `#373737` | primary body text (brand charcoal) |
| `--ink-2` | `#5C5E5C` | secondary text |
| `--ink-3` | `#8A8C88` | muted text, placeholders |
| `--line` | `#DCDCD4` | hairline borders |
| `--line-strong` | `#C7C7BE` | input borders |
| `--accent` | `#466B53` | primary buttons, active state, focus (calm sage) |
| `--accent-strong` | `#37553F` | hover/press |
| `--accent-tint` | `#E3EAE3` | soft fills, selected chips |
| `--success / --warning / --danger / --info` | `#3E7A56 / #A9772B / #AE453B / #3F6B86` | semantic, each with a `*-tint` |

**Type** — Roboto family (all three widths are on Google Fonts; install via Google Fonts or
self-host the TTFs in `fonts/`):
- Display / headings: **Roboto SemiCondensed**, weight 900 (Black) / 700.
- Body & UI: **Roboto**, 300–900; **base size 17px** (intentionally large), line-height 1.6.
- Overlines / tags / data: **Roboto Condensed** 500/700, uppercase, letter-spacing `.14em`.
- Scale: overline 13 · xs 14 · sm 15 · **base 17** · lg 19 · xl 22 · 2xl 28 · 3xl 36 · 4xl 48 · 5xl 64 · 6xl 84.

**Radii**: xs 6 · sm 10 · md 14 (buttons/inputs) · lg 20 (cards) · xl 28 (CTA/modal) · pill 999.
**Spacing** (4-base): 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80.
**Shadow**: sm `0 1px 2px rgba(26,28,29,.06)` · md `0 4px 16px -4px rgba(26,28,29,.10)` ·
lg `0 18px 48px -14px rgba(26,28,29,.16)` · focus ring `0 0 0 3px rgba(70,107,83,.28)`.
**Motion**: 120/200/360ms; ease `cubic-bezier(.4,0,.2,1)`. Fades + 8–12px slides. **No bounce/spring.**

## Screens / views (web reference: `web/index.html`)

### 1. Top navigation (`WNav`)
- Sticky, translucent `rgba(240,240,236,.82)` + `backdrop-filter: blur(14px)`, 1px bottom `--line`.
- Height 76px; content max-width **1240px**, 40px side padding.
- Left: `rentflow` wordmark PNG (`assets/rentflow-wordmark.png`), height 26px.
- Center: text links (Browse, How it works, List your home, Help) — 16px, active = weight 700 `--ink`, else 500 `--ink-2`.
- Right: "Sign in" ghost button + "Get started" primary button (sage) with `arrow-right` icon.

### 2. Hero (`WHero`)
- Overline "HÀ NỘI · 1,200+ VERIFIED HOMES".
- Headline `Roboto SemiCondensed` 900, **76px**, line-height .98, tracking −.02em, color `--ink`, max-width 900px: "Find a home you'll actually love."
- Lead paragraph 22px `--ink-2`, max-width 560px.
- **Search bar**: surface card, radius `--r-lg`, `--shadow-md`, padding 10; contains a pill segmented control (Rent / Buy / Short stay), a search input row (lucide `search` + placeholder), and a large sage "Search" button with `arrow-right`. Max-width 880px.
- Trust row: three items with sage lucide icons (`shield-check` Verified listings, `calendar-check` Two-tap tours, `file-check` Digital leases).

### 3. Featured listings (`WFeatured`)
- Section header: overline "NEWLY LISTED" + h2 "Homes in Tây Hồ & nearby" + secondary "See all homes" button (→ Browse).
- 3-column grid, 24px gap, of **listing cards** (`WListingCard`).

### 4. Listing card (`WListingCard`) — the signature component
- Surface card, 1px `--line`, radius `--r-lg`, `--shadow-sm`; on hover → `--shadow-md` + `translateY(-3px)`.
- Photo area 210px, `object-fit: cover`, `filter: saturate(.92)`. Overlays: a tag chip top-left (Roboto Condensed 700, uppercase; Verified = `--success`, else `--accent-strong`) and a circular favorite button top-right (`heart`, fills `--danger` when active).
- Body: price in `Roboto Condensed` 700 **27px** `--ink` with `/mo` in 15px `--ink-3` (currency **₫ VND**); title 18px/700; location row with `map-pin`; a divider then a meta row (beds / baths / m² / rating ★) in Roboto Condensed, `white-space: nowrap`.

### 5. How it works (`WHowItWorks`)
- Full-width band on `--surface` with top/bottom `--line` borders, 72px vertical padding.
- Overline + h2 "Three calm steps from searching to keys." then a 3-col grid: each step = a 56px `--accent-tint` rounded tile with a sage lucide icon, a "0N" Roboto-Condensed step number, h4 title, body text `--ink-2`.

### 6. Host CTA (`WCta`)
- Dark `--ink` block, radius `--r-xl`, 64px padding. Left: display headline 48px in `--on-dark` + muted subcopy. Right: invert (cream) button "List your home" with `arrow-right`.

### 7. Footer (`WFooter`)
- `--ink` background, `--on-dark` text. 4-col grid (brand blurb + white icon mark; Renters / Hosts / Company link columns). Bottom bar: "EST 2026 · HÀ NỘI, VNA" overline + "© 2026 RentFlow".

### 8. Browse view (`WBrowse`)
- Overline + h1 "{n} homes available", a wrap of filter chips (active = `--ink` fill, cream text; inactive = surface + `--line-strong`), then the 3-col card grid.

### 9. Listing detail modal (`WDetailModal`)
- Fixed overlay `rgba(26,28,29,.5)` + 2px blur. Centered card max-width 960px, radius `--r-xl`.
- 380px photo hero with a circular close (`x`) button. Two-column body (1.6fr / 1fr): left = badges, h2 title, location+rating, three spec tiles (sage icons), description, "What's included" amenities grid (2-col, lucide icons); right = sticky booking card with price, "Book a tour" (primary) + "Message host" (secondary) buttons, and a "Deposit protected" reassurance line.

## Interactions & behavior
- **Nav**: clicking Browse → browse view; wordmark → home. `window.scrollTo(0,0)` on view change.
- **Hero/Featured "Search"/"See all"** → browse view.
- **Card click** → opens detail modal; **heart** toggles saved (stops propagation); **close / overlay click** → closes modal.
- Hover: cards lift + deepen shadow; primary buttons darken to `--accent-strong`; buttons press to `scale(.98)`.
- Focus: 3px sage focus ring (`--shadow-focus`) — keep visible for accessibility.

## State management (reference prototype)
- `view`: `'home' | 'browse'`.
- `detail`: the selected listing object or `null` (drives the modal).
- Per-card local `saved`/`fav` boolean. In production, lift to real saved-listings state + persistence.
- Listing data: replace `WEB_LISTINGS` with your real API/data source.

## Content / voice
Sentence case everywhere except the overline label style and `EST 2026`. Voice is calm, plain,
reassuring; "you" for the reader, "we" for RentFlow; no emoji; no exclamation marks in
transactional copy. **VND (₫) primary**, Hà Nội locale; product is comfortable in Vietnamese + English.

## Assets (in `assets/`)
| File | Use |
|------|-----|
| `rentflow-wordmark.png` | nav/header wordmark (charcoal on transparent-ish cream) |
| `rentflow-lockup.png` | full logo lockup (wordmark + origin + tagline) |
| `rentflow-icon.png` | app icon (white house-arrow on near-black) |
| `rentflow-mark-white.png` | house-arrow mark, white, transparent — for dark surfaces (footer) |
| `rentflow-mark-charcoal.png` | house-arrow mark, charcoal, transparent — for light surfaces |

Icons throughout: **Lucide** (https://lucide.dev), ~1.75px stroke, rounded. Install the
`lucide` / `lucide-react` package in the real app instead of the CDN.
Listing photos in the prototype are **picsum placeholders** — swap for real warm interior photography.

## Files in this bundle
| Path | What |
|------|------|
| `README.md` | this design reference (self-sufficient) |
| `colors_and_type.css` | all design tokens + `.rf-*` semantic type classes |
| `system_README.md` | the full design-system guide (voice, visual foundations, iconography) |
| `web/index.html` | website reference — shell + view state + modal |
| `web/web-components.jsx` | nav, button, listing card, footer |
| `web/web-sections.jsx` | hero, featured, how-it-works, CTA, browse, detail modal |
| `web/web-README.md` | notes on the web kit |
| `assets/` | logos + icon marks |

> Tip: open `system_README.md` and `colors_and_type.css` first to absorb the
> tokens and rules, then implement screen-by-screen from the "Screens / views" section above,
> matching the reference files in `web/`.
