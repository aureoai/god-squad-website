# phase-3-assets — production copies

Created in Phase 3 (Asset Preparation), 2026-09-21.

**Nothing in the original project was modified, renamed, deleted or destructively
processed to produce anything in this folder.** Every file here is a new,
additional copy. Each original remains exactly where it was, byte for byte.

These files are **not wired into the prototype**. The prototype still references
its original assets and is functionally unchanged. This folder is a staging area
for Phase 10, where the Shopify theme is built.

---

## icons/ — nine UI icons, authored

Drawn to the contract in `PHASE-2-DESIGN-TOKENS.css`:

| Property | Value | Token |
|---|---|---|
| Canvas | 24 x 24 | one optical size for the set |
| Stroke | 1.5 | `--icon-stroke-width` |
| Colour | `currentColor` | inherits `--accent-current` per surface |
| Caps and joins | round | matches the prototype's drawn-line character |
| Fill | none | outline set |

`icon-search` · `icon-account` · `icon-cart` · `icon-menu` · `icon-close` ·
`icon-chevron` · `icon-arrow` · `icon-plus` · `icon-minus`

**These were drawn, not traced.** Phase 3 forbids blindly converting raster
artwork, and the existing icon PNGs are AI-generated with colour baked into the
pixels and matting halos at their edges; tracing them would carry those defects
across. These nine are standard geometric interface glyphs that can be
constructed exactly, so they were built from coordinates.

Each was checked for a single root element, no embedded raster, no hard-coded
colour, no editor metadata, `aria-hidden="true"`, the correct viewBox and the
correct stroke width. All nine were then rendered at 24, 28 and 44 pixels on the
dark surface, the light surface and in accent gold, and visually confirmed.

Total 2,612 bytes, against 308,521 bytes for the nine raster PNGs they can
replace, a 99.2% reduction.

**Not included, deliberately.** The crown, community, globe and diamond feature
icons are not here: Phase 3 section 17 requires their visual character be
preserved and forbids redesign, so replacing them is a design decision rather
than a conversion. The Facebook and Instagram marks are not here either, because
platform logos are trademarks and should come from each platform's official
brand kit rather than being redrawn.

---

## hero/ — desktop hero, WebP width ladder

Re-encoded from `images/hero-group.png` (1672 x 941, 1,989,201 bytes, RGB with
no alpha channel, so PNG bought nothing) at quality 0.82.

| File | Dimensions | Bytes | Of the source |
|---|---|---|---|
| `hero-walk-by-faith-desktop-1672w.webp` | 1672 x 941 | 119,850 | 6.0% |
| `hero-walk-by-faith-desktop-1280w.webp` | 1280 x 720 | 81,354 | 4.1% |
| `hero-walk-by-faith-desktop-960w.webp` | 960 x 540 | 59,210 | 3.0% |
| `hero-walk-by-faith-desktop-640w.webp` | 640 x 360 | 31,500 | 1.6% |
| `hero-walk-by-faith-desktop-420w.webp` | 420 x 236 | 19,260 | 1.0% |

The full-size rung is 94.0% smaller than the PNG. Quality was verified by
rendering the original and the re-encode side by side at full frame and at 1:1
on the two hardest regions, the face and garment detail and the sky gradient
where banding would appear first. No visible artefacts and no banding.

**Two caveats carry forward.**

1. This ladder serves the **desktop** crop only. No mobile hero exists. The
   16:9 source cropped into a phone band loses about a third of its width,
   cutting the third model and the back-print message. A portrait or
   art-directed phone source is a genuine gap, recorded in the missing-asset
   register.
2. The source is AI-generated. Its provenance and licensing have not been
   established, and that should be verified before launch.

---

## Naming

Production copies follow the Phase 3 convention: lower case, hyphens, no
spaces, no version words. Width-suffixed rungs use `-{width}w`.

## What is still missing

The ladder above improves delivery of an image that remains a single generated
frame. It does not solve the resolution ceiling: every product image in the
project is a crop of a 1024 x 1536 mockup, and no vector logo has been located.
Those are sourcing problems, not processing problems, and they are listed in
`PHASE-3-ASSET-SYSTEM.md`.
