# RentFlow — Web UI Kit (marketing + listings)

A high-fidelity, click-through recreation of the **RentFlow website**, built on the brand
foundations in `../../colors_and_type.css`. Interpretation derived from the brand (no
production site code was supplied) — cosmetic, not production logic.

## Run it
Open `index.html`:
- **Home** — sticky nav, search hero, featured listings, "How it works", host CTA, footer.
- **Browse** (nav → "Browse" or the hero **Search**) — filter chips + a 6-up listing grid.
- Click any card → **Listing detail modal** (gallery, specs, amenities, sticky booking card).

## Files
| File | What |
|------|------|
| `index.html` | Site shell + view state (home / browse) + detail modal |
| `web-components.jsx` | `WIcon`, `WEB_LISTINGS`, `WButton`, `WNav`, `WListingCard`, `WFooter` |
| `web-sections.jsx` | `WHero`, `WFeatured`, `WHowItWorks`, `WCta`, `WBrowse`, `WDetailModal` |

## Notes
- Max content width **1240px**, 40px gutters; sticky translucent (`blur`) nav.
- Display headlines use **Roboto SemiCondensed Black**; body is large **Roboto** (17px).
- Icons: **Lucide** (CDN). Listing photos are **seeded placeholders** — replace with real
  warm interior photography.
- The dark footer + CTA band use `--ink`; everything else sits on warm `--paper`.
