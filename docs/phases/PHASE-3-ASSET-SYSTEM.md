# GOD SQUAD — PHASE 3 ASSET SYSTEM

**Project:** God Squad Premium Faith-Driven Streetwear
**Phase:** 3 — Asset Preparation & Image System
**Date:** 2026-09-22
**Companion file:** `PHASE-3-ASSET-MANIFEST.csv` — 62 rows, the full inventory plus production copies
**Production copies:** `phase-3-assets/` — nine authored SVG icons and a five-rung hero WebP ladder
**Predecessors:** `PHASE-0-PROJECT-FOUNDATION.md`, `PHASE-1-WEBSITE-AUDIT.md`, `PHASE-2-DESIGN-SYSTEM.md`

## Scope of this phase

Phase 3 inspected, classified and documented every asset, detected duplicates by hash, and created non-destructive production copies where a copy could be made without taking a design decision.

**The website is functionally unchanged.** No HTML, CSS or JavaScript was touched, no section rebuilt, no navigation, typography or colour altered, no logo replaced, no Liquid written. The page still references exactly the files it referenced before this phase began, and nothing in `phase-3-assets/` is wired into it.

**No original was modified, renamed, destructively processed or deleted.** Two status labels are routinely misread, so both are stated here: **REMOVE** means *candidate for removal after final approval*, never *delete now*; **ARCHIVE** means *move to an archive location after approval*, not *discard*. Every file carrying either label is still in place.

**The constraint that shapes every recommendation.** Every photographic and product asset is a crop of one 1024 by 1536 mockup or a generated frame. That is a sourcing problem, not a processing problem: re-encoding changes how efficiently pixels are delivered, it does not create pixels that were never captured. Everything marked HIGH-RES PRODUCT MASTER REQUIRED, HIGH-RES STORY MASTER REQUIRED or VECTOR LOGO REQUIRED follows from it.


## 1. Asset Overview

Phase 3 is an asset phase. It set out to inspect every file in the project, classify each one against the fixed category and status vocabularies, detect duplicates by hash rather than by filename, document the logo, hero, product, story, icon, social and sprite systems, and create non-destructive production copies where a copy could be made without a design decision. It did not redesign anything.

**The website is functionally unchanged.** No HTML, CSS or JavaScript was touched, no section was rebuilt, no navigation, typography or colour was altered, the logo was not replaced, and no Liquid was written. `God Squad Website.html` still references the same sixteen files it referenced before Phase 3 began.

### What Phase 3 produced

| Deliverable | Detail |
|---|---|
| `PHASE-3-ASSET-MANIFEST.csv` | 62 rows — the 48 scanned files plus the 14 production copies — carrying all seventeen columns the spec fixes: Category, Current Filename, Current Path, File Type, Width, Height, Aspect Ratio, File Size, Hash, Current Usage, Duplicate Group, Status, Canonical Asset, Recommended Production Name, Recommended Format, Recommended Shopify Usage, Notes |
| `phase-3-assets/icons/` | Nine authored SVG UI icons, 2,612 bytes total, drawn to 24x24 / stroke 1.5 / `currentColor`. **Drawn from coordinates, not traced** from the raster PNGs |
| `phase-3-assets/hero/` | A WebP width ladder re-encoded from `images/hero-group.png` at 1672 / 1280 / 960 / 640 / 420, quality 0.82, 311,174 bytes across five rungs |
| `phase-3-assets/README.md` | Provenance, method and the two caveats that carry forward from the ladder |

### Totals

| Measure | Value |
|---|---|
| Files scanned | 48 — 44 originals + 4 phase documents (`PHASE-0-PROJECT-FOUNDATION.md`, `PHASE-1-WEBSITE-AUDIT.md`, `PHASE-2-DESIGN-SYSTEM.md`, `PHASE-2-DESIGN-TOKENS.css`) |
| Bytes scanned | 18,077,379 |
| Image files | 41, totalling 17,100,416 bytes (the remaining seven files — the HTML, `support.js`, the four phase documents and `uploads/God-Squad-Images/README.txt` — account for 976,963 bytes) |
| Files referenced by the page | 16 — fifteen images totalling 2,406,866 bytes, plus `support.js` at 69,150 bytes |
| Exact duplicate groups (md5) | 9, covering 20 files, i.e. 11 redundant copies, 6,733,692 bytes — **39.4% of all image bytes** |
| Production copies created | 14 (9 SVG + 5 WebP) |
| Original assets modified | **0** |
| Original assets deleted | **0** |

Status distribution across the 62 manifest rows: KEEP 20, REPLACE 12, ARCHIVE 12, REFERENCE ONLY 12, OPTIMIZE 4, REMOVE 2.

Category distribution: HERO 10, ICON 16, LOGO 6, MOCKUP 2, OTHER 8, PRODUCT 6, REFERENCE 4, SOCIAL 2, SPRITE 5, STORY 3. COLLECTION, BRAND and BACKGROUND hold zero assets.

### The production-copy folder

`phase-3-assets/` holds only new files. Every file in it is an addition; each original remains exactly where it was, byte for byte. **Nothing in it is wired into the prototype.** The page still loads `images/hero-group.png` and the seven raster UI and feature icons it always loaded. The folder is a staging area for Phase 10, where the Shopify theme is built.

Stated as capability rather than accomplishment: Phase 3 has produced and verified a hero re-encode that **would** cut the hero's delivery cost by 94.0% (1,989,201 bytes down to 119,850 at full size), and drawn SVGs that **would** cut the three UI icons they are eligible to replace by 98.9% (85,933 bytes of `icon-search.png`, `icon-account.png` and `icon-cart.png` down to 948 bytes of SVG). Nothing is wired in; the page is unchanged.

### The preservation guarantee

No original was overwritten, destructively cropped, destructively compressed, renamed or deleted. Two statuses are commonly misread, so both are stated plainly here:

- **REMOVE** means *candidate for removal after final approval*, never *delete now*. Two files carry it: `.thumbnail` and `support.js`. Both are still in place.
- **ARCHIVE** likewise means *move to an archive location after approval*, not discard. Twelve files carry it: six byte-identical duplicates whose canonical sibling is named in the manifest, three canonicals that are themselves unreferenced (`images/icons-sprite.png`, `images/social-sprite.png`, `images/logo.png`), and three unreferenced logo export artefacts that belong to no duplicate group (`white-font-trans-mu98q2ez-zrdd.png`, `white-font-trans-mu98qky0-5tt6.png`, `white-font-300x300-mu98qi59-mytq.png`). Together they hold 8,541,085 bytes. All twelve are still in place.

### The single hard constraint that shapes everything

**Every photographic and product asset in the project is a crop of one 1024x1536 mockup or a generated frame.** `uploads/God-Squad-Images/README.txt` states it directly, and the dimensions confirm it: the tee is 235x230, the hoodie 235x235, the cap 215x190, the story crop 535x348, the hero-model crop 650x480. Those tiles render at 288px on desktop and 327-382px on phones — a device-pixel upscale of roughly 2.8x.

This is a **sourcing problem, not a processing problem**. Re-encoding, sharpening and format conversion change how efficiently those pixels are delivered; they do not create pixels that were never captured. Optimisation cannot substitute for sourcing. Every recommendation in this document that says HIGH-RES PRODUCT MASTER REQUIRED, HIGH-RES STORY MASTER REQUIRED or VECTOR LOGO REQUIRED is downstream of this one fact.

The same constraint has a provenance dimension. The hero, the two sprite sheets and the icon set are AI-generated, and neither their generation history nor their licensing terms have been established. Per the manifest row for `images/hero-group.png`: **ASSET PROVENANCE SHOULD BE VERIFIED**, before launch and before any of these assets is treated as an owned brand asset.

## 2. Asset Inventory

The complete register, grouped by category, from `PHASE-3-ASSET-MANIFEST.csv`, with the manifest's Hash and Notes columns omitted here for width, and colour mode and transparency shown where they were measured.

**How to read the Colour / transparency column.** Transparency is reported only where it is established by measurement or by an explicit manifest note. `images/hero-group.png` is recorded RGB with no alpha channel (brief) and `images/WHITE FONT LOGO.png` as 500x500 RGBA with heavy transparent padding (manifest). `images/logo.png` is recorded as a white wordmark on a solid black square (manifest), i.e. an opaque tile. Everywhere else only the MIME type is on record, and the cell reads **unmeasured** — an RGBA colour mode is not itself evidence that a file contains transparent pixels, and is not presented as such anywhere in this document.

**Current usage** is the manifest's Current Usage column. The two live references that matter most were additionally confirmed against source: `God Squad Website.html` line 65 loads `images/hero-group.png` into the hero, and line 126 loads `./01-hero-model-mu98p88t-7jig.webp` into the Our Story slot.

### LOGO — 6 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/WHITE FONT LOGO.png` | image/png | 500x500 | 1:1 | 37,836 | RGBA, heavy transparent padding (manifest) | Referenced — header 78px, footer 56px | n/a | REPLACE |
| `images/logo.png` | image/png | 500x500 | 1:1 | 47,147 | no — opaque black tile (manifest note); alpha unused | Not referenced | DUP-04 canonical | ARCHIVE |
| `uploads/God-Squad-Images/06-logo.png` | image/png | 500x500 | 1:1 | 47,147 | as DUP-04 canonical | Not referenced | DUP-04 | ARCHIVE |
| `white-font-trans-mu98q2ez-zrdd.png` | image/png | 500x500 | 1:1 | 43,606 | unmeasured | Not referenced | none | ARCHIVE |
| `white-font-trans-mu98qky0-5tt6.png` | image/png | 500x500 | 1:1 | 43,606 | unmeasured | Not referenced | none | ARCHIVE |
| `white-font-300x300-mu98qi59-mytq.png` | image/png | 244x184 | 1.326:1 | 23,444 | unmeasured | Not referenced | none | ARCHIVE |

The two `white-font-trans-*` files are the same 500x500 size and the same 43,606 bytes but carry **different md5 hashes**, so they are separate encodes rather than copies — which is why neither joins a duplicate group. `white-font-300x300-mu98qi59-mytq.png` is 244x184 despite the `300x300` in its filename.

### HERO — 10 assets (5 originals + 5 production copies)

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/hero-group.png` | image/png | 1672x941 | 1.777:1 | 1,989,201 | RGB, **no alpha channel** (brief) | Referenced — the live desktop hero and LCP image | DUP-01 canonical | OPTIMIZE |
| `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` | image/png | 1672x941 | 1.777:1 | 1,989,201 | as DUP-01 canonical | Not referenced | DUP-01 | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png` | image/png | 1672x941 | 1.777:1 | 1,989,201 | as DUP-01 canonical | Not referenced | DUP-01 | ARCHIVE |
| `images/hero-model.webp` | image/webp | 650x480 | 1.354:1 | 39,966 | WebP lossy; unmeasured | Not referenced | DUP-02 canonical | REFERENCE ONLY |
| `uploads/God-Squad-Images/01-hero-model.webp` | image/webp | 650x480 | 1.354:1 | 39,966 | as DUP-02 canonical | Not referenced | DUP-02 | REFERENCE ONLY |
| `phase-3-assets/hero/hero-walk-by-faith-desktop-1672w.webp` | image/webp | 1672x941 | 1.777:1 | 119,850 | WebP q82, no alpha in source | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/hero/hero-walk-by-faith-desktop-1280w.webp` | image/webp | 1280x720 | 1.777:1 | 81,354 | WebP q82 | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/hero/hero-walk-by-faith-desktop-960w.webp` | image/webp | 960x540 | 1.777:1 | 59,210 | WebP q82 | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/hero/hero-walk-by-faith-desktop-640w.webp` | image/webp | 640x360 | 1.777:1 | 31,500 | WebP q82 | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/hero/hero-walk-by-faith-desktop-420w.webp` | image/webp | 420x236 | 1.777:1 | 19,260 | WebP q82 | Production copy; not wired in | n/a | KEEP |

The three byte-identical 1,989,201-byte copies of the hero frame are 5,967,603 bytes between them, **34.9% of all image bytes** (of 17,100,416) for one photograph stored three times.

### PRODUCT — 6 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/product-tee.webp` | image/webp | 235x230 | 1.022:1 | 9,012 | WebP lossy; unmeasured | Referenced | DUP-08 canonical | REPLACE |
| `images/product-hoodie.webp` | image/webp | 235x235 | 1:1 | 12,328 | WebP lossy; unmeasured | Referenced | DUP-07 canonical | REPLACE |
| `images/product-cap.webp` | image/webp | 215x190 | 1.132:1 | 10,002 | WebP lossy; unmeasured | Referenced | DUP-06 canonical | REPLACE |
| `uploads/God-Squad-Images/02-product-oversized-tee.webp` | image/webp | 235x230 | 1.022:1 | 9,012 | as DUP-08 canonical | Not referenced | DUP-08 | REFERENCE ONLY |
| `uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp` | image/webp | 235x235 | 1:1 | 12,328 | as DUP-07 canonical | Not referenced | DUP-07 | REFERENCE ONLY |
| `uploads/God-Squad-Images/04-product-utility-cap.webp` | image/webp | 215x190 | 1.132:1 | 10,002 | as DUP-06 canonical | Not referenced | DUP-06 | REFERENCE ONLY |

**The hoodie alone is square at 235x235. The tee is 235x230 (1.022:1) and the cap 215x190 (1.132:1), so both are edge-cropped inside the 1:1 tile, the cap most severely (manifest DUP-06, DUP-08).** The manifest note on `images/product-cap.webp` currently reads "the only non-square product source" and carries the same error; it should be corrected to match.

### STORY — 3 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `01-hero-model-mu98p88t-7jig.webp` | image/webp | 650x480 | 1.354:1 | 39,966 | WebP lossy; unmeasured | **Referenced** — Our Story background (`God Squad Website.html` line 126) | none — separate re-encode of the DUP-02 frame, not byte-identical | REPLACE |
| `images/our-story.webp` | image/webp | 535x348 | 1.537:1 | 41,004 | WebP lossy; unmeasured | Not referenced | DUP-05 canonical | REPLACE |
| `uploads/God-Squad-Images/05-our-story-models.webp` | image/webp | 535x348 | 1.537:1 | 41,004 | as DUP-05 canonical | Not referenced | DUP-05 | REFERENCE ONLY |

The slot in use carries the wrong image: a crop of the mockup **hero** with the headline fragments "A PURPOSE", "K BY" and "TH." baked into the pixels, rendered at 998x520 — a 1.53x upscale with about 29% of its height cropped away (manifest). The three-model composition the mockup actually intends, `images/our-story.webp`, is not referenced at all and at 535x348 is in any case far too small for a slot roughly 1000px wide.

### ICON — 16 assets (7 raster originals + 9 production SVGs)

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/icon-search.png` | image/png | 110x110 | 1:1 | 28,336 | cream baked into pixels (manifest); alpha unmeasured | Referenced, drawn at 24px | n/a | REPLACE |
| `images/icon-account.png` | image/png | 110x110 | 1:1 | 28,470 | unmeasured | Referenced, drawn at 24px | n/a | REPLACE |
| `images/icon-cart.png` | image/png | 110x110 | 1:1 | 29,127 | unmeasured | Referenced, drawn at 24px | n/a | REPLACE |
| `images/icon-globe.png` | image/png | 110x110 | 1:1 | 35,625 | gold baked in (manifest) | Referenced **twice** — 16px announcement bar, 44px values row | n/a | REPLACE |
| `images/icon-crown.png` | image/png | 130x110 | 1.182:1 | 33,339 | unmeasured | Referenced, drawn at 44px | n/a | OPTIMIZE |
| `images/icon-diamond.png` | image/png | 130x110 | 1.182:1 | 34,556 | unmeasured | Referenced, drawn at 44px | n/a | OPTIMIZE |
| `images/icon-community.png` | image/png | 150x110 | 1.364:1 | 39,978 | unmeasured | Referenced, drawn at 44px | n/a | OPTIMIZE |
| `phase-3-assets/icons/icon-account.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 309 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-arrow.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 281 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-cart.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 346 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-chevron.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 262 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-close.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 287 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-menu.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 305 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-minus.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 252 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-plus.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 277 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |
| `phase-3-assets/icons/icon-search.svg` | image/svg+xml | 24x24 viewBox | 1:1 | 293 | `currentColor`, no fill | Production copy; not wired in | n/a | KEEP |

The nine SVGs are 2,612 bytes together. The set they **are eligible to displace once wired in at Phase 10** is three files — `icon-search.png`, `icon-account.png` and `icon-cart.png`, 85,933 bytes — because the other six SVGs (menu, close, chevron, arrow, plus, minus) have no raster counterpart in the project at all. That exchange is 948 bytes for 85,933, a 98.9% reduction, and it is a Phase 10 action, not one that has happened.

### SOCIAL — 2 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/icon-facebook.png` | image/png | 130x130 | 1:1 | 36,771 | unmeasured | Referenced | n/a | REPLACE |
| `images/icon-instagram.png` | image/png | 130x130 | 1:1 | 42,319 | unmeasured | Referenced | n/a | REPLACE |

Both are circled two-tone badges cut from `images/social-sprite.png`, where the mockup shows a plain glyph. Platform marks are trademarks and belong in each platform's official brand kit rather than being traced from a generated sheet. Which platforms the business actually operates is BUSINESS INFORMATION REQUIRED (manifest, `images/icon-instagram.png`).

### SPRITE — 5 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `images/icons-sprite.png` | image/png | 2172x724 | 3:1 | 833,929 | unmeasured | Not referenced | DUP-03 canonical | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png` | image/png | 2172x724 | 3:1 | 833,929 | as DUP-03 canonical | Not referenced | DUP-03 | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png` | image/png | 2172x724 | 3:1 | 833,929 | as DUP-03 canonical | Not referenced | DUP-03 | ARCHIVE |
| `images/social-sprite.png` | image/png | 2172x724 | 3:1 | 927,973 | unmeasured | Not referenced | DUP-09 canonical | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png` | image/png | 2172x724 | 3:1 | 927,973 | as DUP-09 canonical | Not referenced | DUP-09 | ARCHIVE |

Five files, 4,357,733 bytes, **referenced by nothing**. The two distinct sheets alone are 1,761,902 bytes. They are AI-generated contact sheets from which the individual icon PNGs were cut; the manifest records heavy matting halos on `images/icons-sprite.png`, and `phase-3-assets/README.md` separately records matting halos on the icon PNGs.

### MOCKUP — 2 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `uploads/GODSQUAD WEBSITE MOCKUP.png` | image/png | 1024x1536 | 2:3 | 1,872,888 | unmeasured | Not referenced | none | REFERENCE ONLY |
| `uploads/God-Squad-Images/00-full-mockup-reference.webp` | image/webp | 1024x1536 | 2:3 | 182,250 | WebP lossy; unmeasured | Not referenced | none — same image, different format, so not a hash duplicate | REFERENCE ONLY |

The PNG is **the approved design master**. Every product and story crop in the project was cut from it. It is never a production website image, and any re-cut should take full-quality pixels from the PNG rather than from the WebP derivative.

### REFERENCE — 4 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `uploads/pasted-1789874193900-0.png` | image/png | 1920x1009 | 1.903:1 | 1,541,839 | unmeasured | Not referenced | none | REFERENCE ONLY |
| `uploads/pasted-1789874476205-0.png` | image/png | 1920x1009 | 1.903:1 | 1,550,034 | unmeasured | Not referenced | none | REFERENCE ONLY |
| `uploads/pasted-1789874322321-0.png` | image/png | 1920x1009 | 1.903:1 | 769,319 | unmeasured | Not referenced | none | REFERENCE ONLY |
| `uploads/pasted-1789874083026-0.png` | image/png | 118x77 | 1.532:1 | 17,311 | unmeasured | Not referenced | none | REFERENCE ONLY |

Four pasted images, three at 1920x1009 and one at 118x77, unreferenced and classified REFERENCE ONLY. They are **22.7% of all image bytes (3,878,503 of 17,100,416)** and have no production value. What they depict, and whether they record owner decisions, is not established in the manifest — **BUSINESS INFORMATION REQUIRED** before they are treated as decision evidence. Once identified they should be separated into REFERENCE SCREENSHOTS and WEBSITE SCREENSHOTS per spec section 20, which the current single grouping does not do.

### OTHER — 8 assets

| Path | Type | Dims | Ratio | Bytes | Colour / transparency | Current usage | Dup | Status |
|---|---|---|---|---|---|---|---|---|
| `.thumbnail` | No extension; reports as `application/octet-stream`, recommended format WebP (manifest) | 640x355 | 1.803:1 | 25,542 | unmeasured | Not referenced | none | REMOVE |
| `support.js` | text/javascript | n/a | n/a | 69,150 | n/a | **Referenced** | none | REMOVE |
| `God Squad Website.html` | text/html | n/a | n/a | 15,632 | n/a | The page itself | none | KEEP |
| `uploads/God-Squad-Images/README.txt` | text/plain | n/a | n/a | 556 | n/a | Not referenced | none | KEEP |
| `PHASE-0-PROJECT-FOUNDATION.md` | text/markdown | n/a | n/a | 26,340 | n/a | Not referenced | none | KEEP |
| `PHASE-1-WEBSITE-AUDIT.md` | text/markdown | n/a | n/a | 547,057 | n/a | Not referenced | none | KEEP |
| `PHASE-2-DESIGN-SYSTEM.md` | text/markdown | n/a | n/a | 294,180 | n/a | Not referenced | none | KEEP |
| `PHASE-2-DESIGN-TOKENS.css` | text/css | n/a | n/a | 24,048 | n/a | Not referenced | none | KEEP |

Both REMOVE rows are candidates for removal after approval and remain in place. `support.js` is the Claude Design runtime, which has no place in a storefront and is discarded at Phase 10. `uploads/God-Squad-Images/README.txt` is the primary written evidence for the resolution ceiling and should stay with the assets it describes.

### COLLECTION, BRAND, BACKGROUND — 0 assets each

The manifest records no asset in any of the three. There is no collection imagery and there are no background textures anywhere in the project. For BRAND, what the category is intended to hold — brand marks separate from LOGO, or lifestyle and editorial photography — is not fixed by the spec, whose recommended `brand/` folder sits alongside `editorial/`; the project's six brand marks are already categorised LOGO. Confirm the intended scope before a missing-asset commitment is made against it. BUSINESS INFORMATION REQUIRED.

### Reconciliation

48 files scanned = 44 originals + 4 phase documents. Of the 48, 41 are images (17,100,416 bytes) and 7 are not (976,963 bytes); 17,100,416 + 976,963 = 18,077,379, the scan total. 16 of the 48 are referenced by the page: 15 images (2,406,866 bytes) plus `support.js`. The manifest's 62 rows are those 48 plus the 14 production copies, which are new files and are therefore excluded from every "all image bytes" figure in this document.

## 3. Logo System

Six files carry the LOGO category. One is in use; five are not.

| File | Dims | Bytes | Referenced | Duplicate | Status | Role |
|---|---|---|---|---|---|---|
| `images/WHITE FONT LOGO.png` | 500x500 | 37,836 | **yes** — header 78px, footer 56px | none | REPLACE | **Primary Logo** |
| `images/logo.png` | 500x500 | 47,147 | no | DUP-04 canonical | ARCHIVE | Favicon Candidate / Social-Profile Candidate |
| `uploads/God-Squad-Images/06-logo.png` | 500x500 | 47,147 | no | DUP-04 | ARCHIVE | Redundant copy of the above |
| `white-font-trans-mu98q2ez-zrdd.png` | 500x500 | 43,606 | no | none | ARCHIVE | Alternate export |
| `white-font-trans-mu98qky0-5tt6.png` | 500x500 | 43,606 | no | none | ARCHIVE | Alternate export |
| `white-font-300x300-mu98qi59-mytq.png` | 244x184 | 23,444 | no | none | ARCHIVE | Alternate export |

### The five designations

**Primary Logo: `images/WHITE FONT LOGO.png`.** The white wordmark, 500x500, RGBA with heavy transparent padding, in use in both the header and the footer. It is the only logo the page actually loads. Status REPLACE, recommended production name `logo-god-squad.svg`.

**Secondary Logo: none designated.** `images/logo.png` — the white wordmark on a solid black tile, DUP-04 canonical — is the only lockup variant that exists, and the manifest records it as a possible social/profile candidate once a vector exists, not as a secondary mark. Whether a secondary lockup is wanted at all is **BUSINESS INFORMATION REQUIRED**.

**Inverse Logo: none exists.** The project holds only a white wordmark. There is no dark-ink version for use on cream, paper, packaging or any light surface — and Phase 2 established that cream is a primary surface in the system. Recorded in the missing-asset register: *Inverse Logo — none exists, DOCUMENT AS MISSING.*

**Favicon Candidate: `images/logo.png`.** It is the only square, **opaque**, self-contained lockup in the project: a white wordmark on a solid black square (manifest note), so it needs no background supplied behind it and will not disappear against a dark browser chrome. No favicon of any kind currently exists; `/favicon.ico` returns 404 on every load.

**Social/Profile Candidate: `images/logo.png`,** for the same reasons, with the same caveat — a wordmark inside a circular avatar crop loses its corners, so once the vector master exists the profile mark should be re-laid out inside a safe circle rather than reusing the square tile unchanged.

**Alternate exports.** `white-font-trans-mu98q2ez-zrdd.png`, `white-font-trans-mu98qky0-5tt6.png` and `white-font-300x300-mu98qi59-mytq.png` are alternate exports of the wordmark, none of them referenced. The two 500x500 files are the same byte size but carry different hashes, so they are separate encodes rather than copies; the third is 244x184 despite its filename. **No mockup logo variant exists separate from `uploads/GODSQUAD WEBSITE MOCKUP.png`** — the mockup contains the logo as part of the composition, not as an extractable logo file.

### VECTOR LOGO REQUIRED

**No vector logo — SVG, AI or EPS — exists anywhere in the project.** The entire brand identity currently rests on a 500x500 raster PNG.

Layered PSD sources exist **outside** the project at `C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES`. They were not opened during Phase 3, and they are outside the read boundary of this phase. A vector master may already exist inside them. That should be checked before any vector is commissioned. Phase 3 does not recreate the logo, and explicitly does not reconstruct it with a substitute font.

### The padding problem

The 500x500 canvas is mostly empty. Working back from the measured render — the visible mark renders about **66 x 50** inside the header's 78px box — the ink occupies roughly **426 x 320** of the 500x500 canvas, leaving about **37px on each side horizontally and about 90px top and bottom**.

**The padding is uneven between axes** — about 37px on each side horizontally against about 90px top and bottom — which is exactly why height-based sizing under-delivers (the ink is 64% of the canvas height) while width-based sizing would not (about 85%).

The consequence compounds through the layout:

- At the header's declared **78px** box, 64% of it is ink: **66 x 50**.
- At the footer's **56px** box, the same proportions give roughly **47 x 36** of ink (computed).

Two different comparisons are commonly conflated here, and both are true:

- The ink is about **36% shorter than the 78px box** the layout allocates for it (50 of 78).
- The manifest separately records that the resulting lockup **reads at about half its mockup size**.

Both are consequences of the same baked padding. Neither is a bug in the CSS. The fix is not a larger box — enlarging the box scales the padding too. The fix is a vector master with a tight viewBox, after which the declared box size and the optical size of the mark finally agree.

### Logo usage recommendations

All sizes below are stated as **ink** dimensions — the visible mark, not the padded canvas. Safe area is defined as a clear margin equal to **25% of the ink height** on all four sides, measured from the ink bounding box. The PNG's existing padding is explicitly *not* a safe area: it is unequal between axes and will be stripped when the vector master is produced.

| Context | Minimum display size (ink) | Safe area | Preferred background | Inverse usage |
|---|---|---|---|---|
| Header (desktop) | 40px ink height; today 50px within a 78px box | 25% of ink height, and never less than the header's own vertical padding | Dark `#0d0c0a` | Required on any cream header variant — **does not exist** |
| Footer | 32px ink height; today 36px within a 56px box | 25% of ink height | Dark `#0d0c0a` | Not needed — footer is dark |
| Mobile header | 32px ink height minimum | 25% of ink height; reduce the box, not the clear space | Dark `#0d0c0a` | As desktop |
| Favicon | 32x32 and 16x16 rasters plus an SVG source | None — the mark fills the tile by design | Solid black, as `images/logo.png` already supplies | A light-tile variant is desirable for light browser themes — **does not exist** |
| Social profile | 400x400 minimum; re-laid out inside a circular safe crop | Mark inside a circle of 80% of the tile width | Solid black tile | Not applicable |
| Product photography | 24mm ink width on garment labels and hang tags | 25% of ink height | Garment colour; inverse on light garments | **Required and missing** |
| Packaging | 30mm ink width minimum | 25% of ink height, and never printed into a fold or seam | Kraft or black; inverse on kraft and white | **Required and missing** |
| Marketing (print and digital) | 40px digital / 25mm print, ink | 25% of ink height | Dark preferred; cream permitted only with the inverse mark | **Required and missing** |

Three of the eight contexts need an inverse mark that the project does not have. That is the single largest gap in the logo system after the vector itself.

### Shopify implementation notes

Use `image_url` with explicit `widths:` and `sizes:`, then `image_tag`. Never hand-build a CDN URL. The Shopify CDN serves WebP automatically and does **not** output AVIF, so no AVIF branch is needed.

**While the logo remains a raster**, render it as:

`{{ settings.logo | image_url: width: 234 | image_tag: widths: '78, 117, 156, 234', sizes: '78px', alt: shop.name, class: 'header__logo-image' }}`

The `sizes` value is the element's **layout** width. For the current padded PNG that is **78px** for a 50px optical ink height, because 36% of the box is empty. A vector master with a tight viewBox would carry the same optical ink height in a **66px** box, and the footer's 56px box would become about 47px. Use the box value that matches the asset actually installed, not the ink value.

**Once the vector master exists**, `image_url` no longer applies: Shopify does not transform SVG through `image_url`, and a `widths:` ladder on an SVG does nothing. Upload the vector as the theme logo asset, and inline it from a snippet wherever it must inherit colour — which is the only way the mark can respond to a cream surface, a hover state or a `currentColor` token without shipping a second file.

## 4. Hero System

### The candidates and their verdicts

| Candidate | Dims | Ratio | Bytes | Compression | Visual crop and subject positioning | Desktop suitability | Mobile suitability | Verdict |
|---|---|---|---|---|---|---|---|---|
| `images/hero-group.png` | 1672x941 | 1.777:1 | 1,989,201 | PNG, RGB, **no alpha channel** — lossless container buying nothing on a photograph (brief) | The full crew group; landscape 16:9 framing with the group across the middle band | Adequate resolution for a full-bleed 1440px band; wrong format and 1,989,201 bytes | Poor — a phone crop discards about a third of the width | **PRIMARY DESKTOP HERO** |
| `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` | 1672x941 | 1.777:1 | 1,989,201 | as DUP-01 canonical | Identical pixels | — | — | No independent verdict; byte-identical to DUP-01 canonical. ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png` | 1672x941 | 1.777:1 | 1,989,201 | as DUP-01 canonical | Identical pixels | — | — | No independent verdict; byte-identical to DUP-01 canonical. ARCHIVE |
| `images/hero-model.webp` | 650x480 | 1.354:1 | 39,966 | WebP lossy, 39,966 bytes at 650x480 | A tight crop of the single capped model from the mockup hero | Unsuitable — 650px wide against a 1440px+ band | Unsuitable — 480px tall against a 320px band at 2x or 3x DPR | **REFERENCE ONLY** |
| `uploads/God-Squad-Images/01-hero-model.webp` | 650x480 | 1.354:1 | 39,966 | WebP lossy, byte-identical to the DUP-02 canonical | Identical pixels | Unsuitable on resolution alone | Unsuitable on resolution alone | **REFERENCE ONLY** |
| `01-hero-model-mu98p88t-7jig.webp` (categorised STORY) | 650x480 | 1.354:1 | 39,966 | WebP lossy, 39,966 bytes at 650x480; a separate re-encode of the DUP-02 frame, not byte-identical | Same crop, with the headline fragments "A PURPOSE", "K BY" and "TH." baked into the pixels | Unsuitable — baked type plus 650px width | Unsuitable — baked type plus 650px width | **REFERENCE ONLY** as a hero. It is currently the live Our Story image, where it is also wrong |
| `phase-3-assets/hero/*.webp` (5 rungs) | 1672x941 to 420x236 | 1.777:1 | 119,850 / 81,354 / 59,210 / 31,500 / 19,260 | WebP q82, verified artefact-free | Same crop as the PNG source | Ready to serve as the desktop ladder | Same framing limitation as the source | **KEEP** — production copies, not wired in |

**PRIMARY MOBILE HERO: DOES NOT EXIST — DOCUMENT AS MISSING.**

**ALTERNATE HERO: none.** The only non-duplicate alternative in the category is the 650x480 crop, which is REFERENCE ONLY, so there is no second usable hero frame.

### The WebP ladder already produced

Re-encoded from `images/hero-group.png` at quality 0.82. Originals untouched; these are new files.

| File | Dimensions | Bytes | Of the source |
|---|---|---|---|
| `hero-walk-by-faith-desktop-1672w.webp` | 1672x941 | 119,850 | 6.0% |
| `hero-walk-by-faith-desktop-1280w.webp` | 1280x720 | 81,354 | 4.1% |
| `hero-walk-by-faith-desktop-960w.webp` | 960x540 | 59,210 | 3.0% |
| `hero-walk-by-faith-desktop-640w.webp` | 640x360 | 31,500 | 1.6% |
| `hero-walk-by-faith-desktop-420w.webp` | 420x236 | 19,260 | 1.0% |

The full-size rung is **94.0% smaller** than the PNG. Quality was verified by rendering original and re-encode side by side at full frame and at 1:1 on the two hardest regions — face and garment detail, and the sky gradient where banding would appear first. No visible artefacts, no banding.

In context: swapping the hero PNG for the 1672w rung alone removes **1,869,351 bytes** — 77.7% of the page's image payload (2,406,866 bytes), and 75.0% of everything it loads once the 15,632-byte HTML and the 69,150-byte `support.js` are counted (2,491,648 bytes). This is the single largest available improvement in the entire project, and it is available now, from a file that already exists, at Phase 10.

### Desktop strategy

**Source:** `images/hero-group.png`, served as the WebP ladder above.

The hero section declares `min-height:620px` and the image is absolutely positioned at `width:100%;height:100%;object-fit:cover;object-position:center 30%` (verified in `God Squad Website.html` lines 64-65). At a 1440px viewport that box is roughly **1440 x 620, about 2.32:1**, against a source of **1.777:1**.

Because the box is wider in aspect than the source, `cover` scales the image **to width**: 1440 x 810, of which the 620px box keeps 620 — **discarding about 23.5% of the image height**.

**Horizontal `object-position` is inert at desktop.** The image exactly fills the box horizontally, so the X value does nothing at that geometry. The subject's horizontal placement is fixed by the framing of the source and can only be corrected by reshooting at approximately **2.3:1 with the subject at 70% of the width**. Keep `object-position: center 30%` for the current source — which is what the prototype already declares. The X value becomes live only on narrow viewports, where the crop turns horizontal, and a mobile-specific value should be set there once a portrait source exists.

**Recommended aspect ratio for a future desktop master: 2.3:1 at 2800px wide or more**, framed so the group sits in the right-hand 40% of the frame. That is the shape the layout actually wants, and it is not the shape of the asset in hand.

**Recommended focal point:** the crew group, currently centred; the vertical focal point at 30% from the top is correct and should be preserved.

**The scrim.** The hero carries a two-layer overlay, quoted verbatim from `God Squad Website.html` line 66:

`linear-gradient(90deg,rgba(13,12,10,.92) 0%,rgba(13,12,10,.75) 26%,rgba(13,12,10,.15) 48%,rgba(13,12,10,.1) 68%,rgba(13,12,10,.8) 100%)`

`linear-gradient(180deg,rgba(13,12,10,.55) 0%,rgba(13,12,10,0) 30%,rgba(13,12,10,0) 70%,#0d0c0a 100%)`

The horizontal layer runs from **near-opaque at 92% alpha** on the left, clears to its most transparent stop of **10% alpha at 68% of the width**, and returns to **80% alpha** at the right edge. So the photograph is effectively readable only in a band roughly between 48% and 68% of the width. The left 26% is carrying the headline and is almost entirely covered. Any future hero master must place its subject inside that band or the scrim will bury it — which is the same 70% figure the reshoot recommendation above is built on.

### Mobile strategy

**Source: none exists.** This is a genuine gap, not a processing shortfall.

The prototype's narrow-viewport rules (lines 20-23) restack the hero into a single column and give the image a band of `height:62vw` with `min-height:320px`, keeping `object-position:center 30%`. At a 375px viewport `62vw` is 232px, so the 320px floor applies and the band is **375 x 320, about 1.17:1**.

Covering a 1.17:1 band with a 1.777:1 source inverts the desktop situation: the image now scales **to height**, giving 568 x 320, of which 375px of width is kept — **discarding about 34% of the width**. That crop cuts the third model and the back-print message out of the frame entirely (brief).

**What that costs.** The phone view loses a model and the garment message that the hero exists to communicate, while still downloading a 1,989,201-byte desktop PNG to show a 375 x 320 band. Phones are where the resolution waste and the compositional loss compound.

**Recommended mobile master:** a dedicated, art-directed portrait or square frame at **4:5 or 1:1, 1600px on the short edge or more**, with the subject placed so nothing essential sits in the outer 20% of the width. Recommended production name `hero-walk-by-faith-mobile.webp`, per the naming convention. Recommended `object-position` for that asset: `center 35%`, to be confirmed against the real frame — with a mobile-specific X value set at that point, since X is live on narrow viewports.

Until that source exists, the honest interim position is the current one: the desktop crop, accepting the loss, documented rather than disguised. Phase 3 does not fabricate a mobile hero out of the desktop frame.

### LCP requirement

`images/hero-group.png` is the **likely LCP element**: it is the largest above-the-fold paint, it is absolutely positioned across the full hero band, and at 1,989,201 bytes it is 82.6% of the page's image payload on its own.

The current `<img>` (line 65) sets `src`, `alt="God Squad crew"` and inline positioning styles. It sets **no** `width`, **no** `height`, **no** `srcset`, **no** `sizes` and **no** `fetchpriority`. It sets no `loading` attribute either, so it is eager by default — which is correct, and must not be changed.

Five properties are required of the LCP image at Phase 10 (spec section 24). None is implemented here; all are documented recommendations.

1. **Loaded early and never lazy.** The hero `<img>` must not carry `loading="lazy"`, and must not be moved behind a JavaScript-driven swap.
2. **Responsive delivery**, via `image_url` with explicit `widths:` and `sizes:` plus `image_tag`, matching the ladder: `widths: '420, 640, 960, 1280, 1672'`, `sizes: '100vw'`. Never hand-build a CDN URL. The CDN serves WebP automatically and does not output AVIF, so no AVIF branch is needed.
3. **Explicit dimensions**, so the 620px band reserves its space and the hero contributes nothing to CLS. `image_tag` emits `width` and `height` from the source; keep them.
4. **A preload only if measurement shows it helps**, and then with `imagesrcset` and `imagesizes` mirroring the `image_tag` ladder exactly, so the preloaded URL is the one the browser actually selects. A mismatched preload is the standard way to trigger a double download. With `fetchpriority="high"` on the `<img>`, the preload is usually redundant.
5. **No entrance animation, fade or reveal in front of the hero image.** Spec section 24 requires the LCP element not be hidden behind one, and Phase 10 should not introduce one.

### Provenance

The hero is AI-generated and neither its generation history nor its licensing terms have been established. Per the manifest row for `images/hero-group.png`: **ASSET PROVENANCE SHOULD BE VERIFIED**, before launch and before the frame is treated as an owned brand asset. This applies to the WebP ladder as well, since every rung is derived from it.

## 5. Product Image System

The project holds three product images. All three are crops of the single 1024x1536 design mockup (`uploads/GODSQUAD WEBSITE MOCKUP.png`, REFERENCE ONLY, manifest). None was photographed. Each has a byte-identical duplicate under `uploads/God-Squad-Images/` (manifest DUP-06, DUP-07, DUP-08), so the PRODUCT category's six rows are three assets held twice.

### 5.1 The three files as they stand

| File | Dims | Ratio | Bytes | B/px | Used | Dup | Status |
|---|---|---|---|---|---|---|---|
| `images/product-tee.webp` | 235x230 | 1.022:1 | 9,012 | 0.167 | yes | DUP-08 | REPLACE |
| `images/product-hoodie.webp` | 235x235 | 1:1 | 12,328 | 0.223 | yes | DUP-07 | REPLACE |
| `images/product-cap.webp` | 215x190 | 1.132:1 | 10,002 | 0.245 | yes | DUP-06 | REPLACE |
| `uploads/God-Squad-Images/02-product-oversized-tee.webp` | 235x230 | 1.022:1 | 9,012 | 0.167 | no | DUP-08 | REFERENCE ONLY |
| `uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp` | 235x235 | 1:1 | 12,328 | 0.223 | no | DUP-07 | REFERENCE ONLY |
| `uploads/God-Squad-Images/04-product-utility-cap.webp` | 215x190 | 1.132:1 | 10,002 | 0.245 | no | DUP-06 | REFERENCE ONLY |

The three canonical files together weigh 31,342 bytes — 26.2% of the single largest hero rung (119,850 B, brief: hero ladder). The entire product catalogue's imagery is a rounding error against one hero image, and that is the measure of the problem, not a compliment to the compression.

**Background.** No background was prepared. Each file is a rectangular crop of the mockup (manifest), so it carries whatever the mockup rendered behind that garment at that point in the frame. The three backdrops were not matched to one another because they were never chosen. The product tile paints `background:#ebe6dc` behind the image (prototype markup, product grid), so any mismatch between a baked backdrop and the tile shows as a visible rectangle edge inside the cell.

**Lighting.** No lighting setup exists to describe. Each crop inherits whatever lighting the generated mockup frame carried at that point in the image, so there is no key direction, no fill ratio and no colour temperature that can be measured, matched or repeated. The three garments were not lit as a set and were not lit at all in any reproducible sense — which means there is no existing lighting standard for the replacement shoot to match, and §5.3 must establish one from scratch rather than continue one.

**Positioning.** The garment's placement inside the frame is an artefact of where the crop boundary fell on the mockup, not a composition decision. The tile is `aspect-ratio:1/1` with `object-fit:cover` (prototype markup), so the browser re-crops each file a second time to reach square. The tee loses 2.1% of its width to that second crop, the hoodie loses nothing because it is already 235x235, and the cap — the only non-square source at 1.132:1 — loses 11.6% of its width, which is edge-cropping a garment whose shape is defined by its brim (manifest, `images/product-cap.webp`).

**Consistency.** There is none to speak of. Three different pixel dimensions, three different aspect ratios, three different effective garment scales and three different backdrops, across a three-product catalogue. A visitor sees the inconsistency directly: the three tiles sit side by side in one row on desktop (`grid-template-columns:repeat(3,minmax(0,1fr))`, prototype markup).

**Colourways.** Each product declares three colour swatches in the prototype's product array — tee, hoodie and cap each carry `#0d0c0a`, `#f3efe6` and `#4b5443` (prototype markup, lines 175-177). Not one of those nine colourways has an image. A single crop stands in for all three states of each product, so selecting a swatch cannot change what the shopper sees. The swatch hexes are also unnamed, which is a business item, not an asset one (§20).

### 5.2 The resolution arithmetic, and the verdict

The product tile renders at **288 CSS px** on desktop and **327–382 CSS px** on phones (brief: hard facts; manifest, `images/product-tee.webp`). Device-pixel demand against a 235px source:

| Slot | CSS px | DPR 1 | DPR 2 | DPR 3 |
|---|---|---|---|---|
| Desktop tile | 288 | 288 px — **1.23x upscale** | 576 px — **2.45x** | 864 px — **3.68x** |
| Phone tile, narrow | 327 | 327 px — 1.39x | 654 px — **2.78x** | 981 px — **4.17x** |
| Phone tile, wide | 382 | 382 px — 1.63x | 764 px — **3.25x** | 1,146 px — **4.88x** |

The source never reaches 1:1 with its slot on any device, at any density, including a desktop monitor at DPR 1. The best case in the whole table is a 1.23x upscale; the worst is 4.88x. A Shopify product page, which shows product media far larger than a 288px grid tile and offers zoom, makes the gap wider again.

This is a sourcing problem, not a processing problem. Spec §10 forbids upscaling a low-resolution asset and treating it as an original, and no re-encode, sharpening pass or upscaler creates garment detail that was never captured. The largest real slot measured anywhere in the prototype is 1,146 device pixels; a **2048px square master** covers it with 1.79x headroom and supports a zoom view, which is why 2048 is the floor set in §5.3 and enforced by acceptance check 7 (§12.4).

> **Verdict: HIGH-RES PRODUCT MASTER REQUIRED for all three products** — `images/product-tee.webp`, `images/product-hoodie.webp` and `images/product-cap.webp` (manifest, all three rows). Status REPLACE. The originals are preserved and stay exactly where they are; REPLACE means a new master supersedes them in production once one exists.

### 5.3 The future product standard

Applies to every product master commissioned from here on. It is written so a photographer can shoot to it without further interpretation.

| Property | Standard | Why this value |
|---|---|---|
| Aspect ratio | **1:1**, shot and delivered square | The tile is `aspect-ratio:1/1`; a square master removes the browser's second crop entirely (spec §11) |
| Master dimensions | **2048 x 2048 px** minimum | Covers the largest measured demand, 1,146 device px, with 1.79x headroom for zoom (§5.2) |
| Format | WebP delivered, lossless or high-quality master retained | Shopify's CDN serves WebP automatically and does **not** output AVIF, so an AVIF master buys nothing here |
| Colour | sRGB, profile embedded | Prevents the shift between the shoot and the cream `#ebe6dc` tile |
| Background | One background for the whole catalogue, chosen once, seamless, no visible sweep edge | Three mismatched backdrops is the defect §5.1 records |
| Scale | Consistent garment-to-frame ratio across the set; the same margin on every side | A tee, a hoodie and a cap must read as one catalogue in one row |
| Lighting | **One key and fill setup, one key direction, one colour temperature, one fill ratio, documented and repeated for every future product** | No existing setup can be matched (§5.1, Lighting) — this establishes the standard rather than continuing one |
| Alpha | None on the front view unless the background is deliberately knocked out for the whole set | Half a catalogue on alpha and half on a sweep is worse than either |

Delivery in the eventual theme uses Shopify's own pipeline. Never hand-build a CDN URL:

`{{ product.featured_image | image_url: width: 2048 | image_tag: widths: '288,576,654,864,981,1146,1536,2048', sizes: '(max-width: 749px) calc(50vw - 34px), 288px', loading: 'lazy' }}`

The `sizes` value is derived from the prototype's own measurements: on phones the grid is two columns inside 24px side padding with a 20px gap, giving `calc(50vw - 34px)`; on desktop the tile is a fixed 288px. The 749px breakpoint is the Shopify theme convention and should be aligned to whichever breakpoint the theme adopts in a later phase.

### 5.4 Naming convention, with worked examples

The pattern is `product-[handle]-[view].webp`, lower case, hyphens, no spaces, no version words (spec §§11, 26). Original files are **not** renamed; the convention governs production copies only. The manifest already records the three front-view names:

| Current file | Recommended production name | Source |
|---|---|---|
| `images/product-tee.webp` | `product-signature-tee-front.webp` | manifest, `images/product-tee.webp` |
| `images/product-hoodie.webp` | `product-heavyweight-hoodie-front.webp` | manifest, `images/product-hoodie.webp` |
| `images/product-cap.webp` | `product-utility-cap-front.webp` | manifest, `images/product-cap.webp` |

Extended across the view set for one product:

- `product-signature-tee-front.webp`
- `product-signature-tee-back.webp`
- `product-signature-tee-detail.webp`
- `product-signature-tee-model.webp`
- `product-signature-tee-lifestyle.webp`
- `product-signature-tee-packaging.webp`

Where a colourway needs its own frame, the colour name is the final segment — `product-signature-tee-front-olive.webp`. The prototype carries the three swatches as bare hexes with no names attached, so the colour segment cannot be filled in yet: **BUSINESS INFORMATION REQUIRED** (§20).

### 5.5 Variant views: present or missing

Spec §12 forbids fabricating a missing view. Every row below is marked from what the manifest and the project actually contain.

| View | Signature Oversized Tee | Heavyweight Hoodie | Utility Cap |
|---|---|---|---|
| **Front** | Present, inadequate — 235x230 mockup crop, HIGH-RES PRODUCT MASTER REQUIRED | Present, inadequate — 235x235 | Present, inadequate — 215x190 |
| **Back** | DOCUMENT AS MISSING | DOCUMENT AS MISSING | DOCUMENT AS MISSING |
| **Detail** (fabric, stitching, print texture) | DOCUMENT AS MISSING | DOCUMENT AS MISSING | DOCUMENT AS MISSING |
| **Lifestyle** | DOCUMENT AS MISSING | DOCUMENT AS MISSING | DOCUMENT AS MISSING |
| **Model** (garment worn, identified as this SKU) | DOCUMENT AS MISSING | DOCUMENT AS MISSING | DOCUMENT AS MISSING |
| **Packaging** | DOCUMENT AS MISSING | DOCUMENT AS MISSING | DOCUMENT AS MISSING |

One clarification, because it would otherwise be filled in by assumption: the hero and story images do show people wearing garments, but nothing in the project identifies any garment in those frames as one of the three catalogue SKUs, and the files are categorised HERO and STORY, not PRODUCT (manifest). They are therefore **not** model or lifestyle product photography and must not be reclassified as such. Fifteen of the eighteen cells in the table above are empty, and none of them can be filled from anything already in the project.

## 6. Story Images

### 6.1 The three STORY rows

| Path | Cat | Dims | Bytes | B/px | Used | Dup | Status | Production name |
|---|---|---|---|---|---|---|---|---|
| `01-hero-model-mu98p88t-7jig.webp` | STORY | 650x480 | 39,966 | 0.128 | **yes** | n/a | REPLACE | `story-community.webp` |
| `images/our-story.webp` | STORY | 535x348 | 41,004 | 0.220 | no | DUP-05 | REPLACE | `story-community.webp` |
| `uploads/God-Squad-Images/05-our-story-models.webp` | STORY | 535x348 | 41,004 | 0.220 | no | DUP-05 | REFERENCE ONLY | — |

The third row is the byte-identical duplicate of `images/our-story.webp` (manifest DUP-05) and carries no recommended production name, correctly — a duplicate should not be promoted to a production asset.

The file in use also has a near relation that is *not* a hash duplicate: `images/hero-model.webp` (650x480, 39,966 B, DUP-02, REFERENCE ONLY) is a separate re-encode of the same crop, not byte-identical (manifest, `01-hero-model-mu98p88t-7jig.webp`). The same 650x480 frame therefore exists three times in the project under three names, categorised HERO twice and STORY once.

### 6.2 The canonical story asset question

**The canonical story asset is `images/our-story.webp`** — the three-model composition the mockup intends for Our Story (manifest, `images/our-story.webp`). It is canonical of DUP-05 and it is the only file in the project whose content is actually a story image. It is also unreferenced, and at 535x348 it is far too small for the slot it is meant to fill.

So the honest statement is: the canonical *composition* is identified, and the canonical *asset* does not yet exist at a usable resolution. Both STORY rows that carry a status carry REPLACE for that reason.

**A naming collision must be resolved before any production copy is made.** The manifest assigns two of its three STORY rows the same recommended production name, `story-community.webp` (manifest, `01-hero-model-mu98p88t-7jig.webp` and `images/our-story.webp`). Two files cannot occupy one production name. The resolution follows from §6.2 and §6.3: `story-community.webp` belongs to the eventual high-resolution master of the **three-model composition**, and the file currently wired into the page has no claim on it, because it is not a story image at all. Recorded as risk A-05.

### 6.3 The wrong-asset problem

The Our Story section does not render either STORY-content file. Line 126 of `God Squad Website.html` reads `<img data-r="story-img" src="./01-hero-model-mu98p88t-7jig.webp" alt="God Squad community" ...>`.

That file is a **650x480 crop of the mockup HERO**, not of the story composition, and it has the hero's headline fragments baked into its pixels: **"A PURPOSE"**, **"K BY"** and **"TH."** — visible at every width (manifest, `01-hero-model-mu98p88t-7jig.webp`). These are not a caption or an overlay that CSS can suppress; they are pixels inside the image file. The section therefore shows truncated fragments of the hero's own headline behind the Our Story copy, on a slot whose gradient scrim (`story-fade`, prototype markup) was designed to sit over a clean image.

This is the single clearest defect in the asset set: a file cut from the wrong part of the mockup, carrying another section's typography, wired into a live slot. It is also the exact failure that a duplicate-and-content check at intake would have caught, which is why acceptance check 19 exists (§12.4). Risk A-02, P0.

### 6.4 Resolution against the slot it fills

The desktop story image is `position:absolute; left:30%; width:70%; height:100%` inside a section with `min-height:520px` (prototype markup), which the manifest measures as a rendered **998 x 520** box.

| Source | Native | Slot, DPR 1 | DPR 2 | DPR 3 | Crop taken by `object-fit:cover` |
|---|---|---|---|---|---|
| `01-hero-model-mu98p88t-7jig.webp` (in use) | 650x480 | 998 px — **1.53x upscale** | 1,996 px — **3.07x** | 2,994 px — **4.61x** | ~29% of its height discarded |
| `images/our-story.webp` (canonical) | 535x348 | 998 px — **1.87x upscale** | 1,996 px — **3.73x** | 2,994 px — **5.60x** | ~20% of its height discarded |

The file in use is being enlarged 1.53x before a single retina pixel is considered, and ~29% of its height is thrown away by the cover crop (manifest). The canonical composition is worse on resolution — it is the smaller file of the two — so swapping one for the other is a correctness fix, not a quality fix. Neither reaches 1:1 with the slot at DPR 1.

> **Verdict: HIGH-RES STORY MASTER REQUIRED** for the Our Story slot (manifest, both REPLACE rows).

### 6.5 Desktop and mobile suitability

**Desktop.** The slot is a wide 1.92:1 band (998x520) with a horizontal gradient scrim running `90deg` from solid `#0d0c0a` at 30% to transparent at 56% (prototype markup, `story-fade`). An image for this slot must carry its subject in the **right-hand 45%** of the frame, because the left 30-40% is painted over by the scrim so the story copy can sit on it. Neither existing file was composed for that: the in-use crop places hero headline pixels where the scrim thins out, and the three-model composition at 1.537:1 does not have the width to spare once 20% of its height is cropped to reach 1.92:1.

**Mobile.** At the phone breakpoint the image becomes a full-width band — `width:100%; height:60vw; min-height:280px`, ordered above the copy, with the scrim switching to a vertical `180deg` fade (prototype markup, lines 36-37). On a 390px-wide viewport that is a 390x280 box, so the demand is 1,170 device px at DPR 3 against a 650px source — a **1.80x upscale**, which is the mildest number in this section. But the cover crop on phone takes only ~3% of the height, so on a phone the frame is shown almost whole — and that means the baked-in headline fragments are *more* visible on mobile than on desktop, not less. The asset that reads worst is the one the majority of the frame is shown on.

Both breakpoints are served by one source today. The 1.92:1 desktop band and the ~1.39:1 phone band are different compositions, and §6.6 sets the master wide enough that one art-directed source can serve both with a declared focal point rather than a lucky crop.

### 6.6 The story master standard

| Property | Standard |
|---|---|
| Composition | The three-model community composition (`images/our-story.webp` is the reference for intent, not the source for pixels) |
| Long edge | **2000px minimum**, 2400px preferred |
| Aspect ratio | 16:9 or wider, so the 1.92:1 desktop band crops without loss |
| Subject placement | Subject in the right-hand 45% of the frame; left 35% kept clear for the scrim and copy |
| Focal point | Declared, so the phone band crops to the subject rather than to centre |
| Baked text | None. No headline, no wordmark, no fragment of either |
| Format | WebP; Shopify's CDN serves WebP automatically and does not output AVIF |

The 2000px floor covers DPR 2 on the desktop slot exactly (1,996 device px). DPR 3 on that slot demands 2,994 px and is accepted as a soft shortfall here, because the image sits behind a gradient scrim as a background rather than as detail-critical subject matter — which is not true of product photography, where the floor is a hard 2048 (§5.2). Enforced by acceptance check 7 (§12.4).

Delivery, once a master exists: `{{ section.settings.story_image | image_url: width: 2400 | image_tag: widths: '420,640,960,1280,1600,2000,2400', sizes: '(max-width: 749px) 100vw, 70vw' }}` — the `sizes` values are the slot's own widths from the prototype markup. Never hand-build a CDN URL.

## 7. Collection Images

### 7.1 There is no collection imagery in this project

The manifest's category distribution has ten categories in use — HERO 10, ICON 16, LOGO 6, MOCKUP 2, OTHER 8, PRODUCT 6, REFERENCE 4, SOCIAL 2, SPRITE 5, STORY 3 (brief: category distribution). **COLLECTION is a permitted category with zero rows.** Not a low-resolution collection image, not a placeholder, not a crop that could be pressed into service: none.

The header navigation carries a "Collections" link, and it points at `href="#shop"` — the same in-page anchor as the "Shop" link beside it, so it has no destination of its own and resolves to the New Drop product grid (prototype markup, nav). Collections does not even have a placeholder of its own.

The nearest thing to a collection identity anywhere in the prototype is the New Drop section's heading, `The Faithful`, with the line "Premium Essentials for a Higher Purpose." beneath it (prototype markup, shop section). That is a heading and a strapline over a three-product grid. It has no image of its own, and the section's only imagery is the three product crops audited in §5.

### 7.2 Candidate assessment, collection by collection

Every collection named in the spec's §14 brief, against every asset the project actually holds.

| Collection | Best candidate in the project | Assessment |
|---|---|---|
| **The Faithful** | `images/hero-group.png` (1672x941, HERO, OPTIMIZE) | The only editorial-character asset at a usable size. But it is the homepage hero; reusing it as a collection banner makes the site show one image twice and removes the hero's distinctiveness. **Not recommended.** BUSINESS INFORMATION REQUIRED: whether "The Faithful" is a collection or a drop name (§20) |
| **Shirts** | None | No asset depicts shirts as a group. `images/product-tee.webp` is a single 235x230 product crop |
| **Hoodies** | None | `images/product-hoodie.webp` is a 235x235 product crop |
| **Caps** | None | `images/product-cap.webp` is a 215x190 product crop, and the only non-square product source |
| **Collections** (index) | None | Nothing in the project depicts a grouping of products |
| **Best Sellers** | None | Nothing exists, and nothing could: no sales data determines membership |

Two assets deserve an explicit exclusion so they are not reached for later:

- `uploads/GODSQUAD WEBSITE MOCKUP.png` (1024x1536, MOCKUP, REFERENCE ONLY) is the approved design master and is never a production website image (manifest). Neither it nor its WebP re-encode `uploads/God-Squad-Images/00-full-mockup-reference.webp` may serve a collection banner.
- `images/our-story.webp` (535x348, STORY, REPLACE) is editorial in character and is the closest thing to a collection-style composition — but it is 535px wide, it is already the unfilled canonical story asset (§6.2), and one editorial image cannot be both the story image and a collection banner.

### 7.3 The rule: a product image is not a collection hero

Spec §14 requires PRODUCT and COLLECTION/EDITORIAL images to be kept separate, and forbids using a product image as a collection hero unless it was intentionally designed for that. The rule is not a formality here; it is the thing standing between this project and a visibly broken collection page.

The three product files are 215-235px on their long edge (§5.1). A collection banner is a full-bleed or near-full-bleed slot. Pressing `images/product-hoodie.webp` into a 1440px-wide banner is a **6.13x upscale** at DPR 1 and **12.26x** at DPR 2. Beyond the arithmetic, the two jobs are different: a product image isolates one garment against a controlled background for evaluation; a collection banner establishes mood and category at a glance and usually carries overlaid type, which needs composed negative space no product crop has.

**The rule for this project: no COLLECTION slot is ever filled from the PRODUCT category, and no collection banner is cut from the mockup.** Where a collection needs a banner and none exists, the slot stays empty and the item stays in the missing-asset register (§19, M-09) until purpose-made art is commissioned.

### 7.4 The collection art standard

When collection imagery is commissioned:

| Property | Standard |
|---|---|
| Origin | Purpose-shot or purpose-designed for the collection. Never a product crop, never a mockup extract, never the hero reused |
| Width | **2400px or wider** |
| Aspect ratio | 16:9 for a full-width banner; a 3:1 variant, or a declared focal point, for the short banner a collection header uses |
| Safe area | Composed negative space for overlaid collection type, on the side the theme will place it |
| Baked text | None — the collection name is live text, so it stays translatable, selectable and editable |
| Format | WebP; Shopify's CDN serves WebP automatically and does not output AVIF |
| Set consistency | All collection banners share one treatment, so a collection index page reads as one grid |

Delivery: `{{ collection.image | image_url: width: 2400 | image_tag: widths: '640,960,1280,1600,2000,2400', sizes: '100vw', loading: 'lazy' }}`, with the banner above the fold taking `loading: 'eager'` instead. Never hand-build a CDN URL.

**The honest summary of this section: no purpose-made collection imagery exists in the God Squad project, nothing in the project can substitute for it, and the collection names themselves are not confirmed (§20).** Every collection slot in a future theme is unfilled today. Risk A-07.

## 8. Icon System

The project holds nine raster icon files totalling 308,521 bytes, and nine authored SVG icons totalling 2,612 bytes created in Phase 3. Every raster is referenced by the page; not one SVG is. The website is functionally unchanged, and the SVG set is a staging deliverable in `phase-3-assets/icons/`, wired into nothing.

### 8.1 Every icon, classified

The **Class** column is the spec §15 icon-audit taxonomy — UI / BRAND / FEATURE / SOCIAL / DECORATIVE. It is not the manifest's Category column: the manifest records **ICON** for all seven non-social rasters and **SOCIAL** for the two platform marks, so the two taxonomies are deliberately different and must not be conflated when reading the CSV.

| Icon | Raster today | Dims | Bytes | Displayed at | Class | Status |
|---|---|---|---|---|---|---|
| Search | `images/icon-search.png` | 110x110 | 28,336 | 24px | UI | REPLACE |
| Account | `images/icon-account.png` | 110x110 | 28,470 | 24px | UI | REPLACE |
| Cart | `images/icon-cart.png` | 110x110 | 29,127 | 24px | UI | REPLACE |
| Menu | none | — | — | 24px | UI | KEEP (SVG authored) |
| Close | none | — | — | 24px | UI | KEEP (SVG authored) |
| Chevron | none | — | — | 24px | UI | KEEP (SVG authored) |
| Arrow | none | — | — | 24px | UI | KEEP (SVG authored) |
| Plus | none | — | — | 24px | UI | KEEP (SVG authored) |
| Minus | none | — | — | 24px | UI | KEEP (SVG authored) |
| Crown | `images/icon-crown.png` | 130x110 | 33,339 | 44px | FEATURE | OPTIMIZE |
| Community | `images/icon-community.png` | 150x110 | 39,978 | 44px | FEATURE | OPTIMIZE |
| Diamond | `images/icon-diamond.png` | 130x110 | 34,556 | 44px | FEATURE | OPTIMIZE |
| Globe | `images/icon-globe.png` | 110x110 | 35,625 | 16px **and** 44px | FEATURE | REPLACE |
| Facebook | `images/icon-facebook.png` | 130x130 | 36,771 | footer | SOCIAL | REPLACE |
| Instagram | `images/icon-instagram.png` | 130x130 | 42,319 | footer | SOCIAL | REPLACE |

**BRAND ICON: none.** No icon-form brand mark exists. The wordmark is a LOGO asset (`images/WHITE FONT LOGO.png`), not an icon, and no favicon of any kind exists (brief).

**DECORATIVE ICON: none.** Every icon in the project is functional — it labels a control, a value tile, or a social link.

### 8.2 The nine authored SVGs and their contract

`phase-3-assets/icons/` holds nine files, 2,612 bytes in total, drawn to a single contract (`phase-3-assets/README.md`):

| Property | Value | Token |
|---|---|---|
| Canvas | 24 x 24 | one optical size for the whole set |
| Stroke | 1.5 | `--icon-stroke-width` |
| Colour | `currentColor` | inherits `--accent-current` per surface |
| Caps and joins | round | matches the prototype's drawn-line character |
| Fill | none | outline set |

`icon-search.svg` 293 B · `icon-account.svg` 309 B · `icon-cart.svg` 346 B · `icon-menu.svg` 305 B · `icon-close.svg` 287 B · `icon-chevron.svg` 262 B · `icon-arrow.svg` 281 B · `icon-plus.svg` 277 B · `icon-minus.svg` 252 B (manifest).

**Why they were drawn and not traced.** Spec §16 forbids blindly converting raster artwork and permits conversion only where quality can be preserved. The icon rasters fail that test at source: they were cut from a 2172x724 AI-generated contact sheet carrying heavy matting halos (manifest, `images/icons-sprite.png`), and they have colour baked into their pixels. A trace would carry both defects into the vector. These nine are standard geometric interface glyphs that can be constructed exactly from coordinates, so they were built that way — no auto-trace, no embedded raster, no editor metadata.

**Why `currentColor` matters beyond file size.** A baked-in cream fill cannot respond to hover, focus or surface. `currentColor` is what makes the Phase 2 surface rule enforceable in markup rather than by hand: gold on the dark surface, `--color-accent-strong` on cream. Each icon was verified for a single root element, no hard-coded colour, `aria-hidden="true"`, the correct `viewBox` and the correct stroke width, then rendered at 24, 28 and 44 pixels on the dark surface, the light surface and in accent gold.

**What the set actually replaces.** Today it stands in for three referenced rasters — `icon-account.png`, `icon-cart.png`, `icon-search.png`, 85,933 bytes against 948 bytes of SVG — plus six glyphs (menu, close, chevron, arrow, plus, minus) for which no raster exists at all. `phase-3-assets/README.md` states the reduction against 308,521 bytes, which is the whole nine-file raster icon set; note that that figure includes the four feature icons and two platform marks the SVG set deliberately does **not** cover (§8.4, §9.3), so 85,933 → 948 is the like-for-like comparison.

### 8.3 The three UI rasters

All three are REPLACE, not OPTIMIZE, and the reason is not weight. `images/icon-search.png` is "110x110 raster drawn at 24px with cream baked into the pixels, so it cannot inherit colour or respond to hover" (manifest). Re-encoding a 110x110 PNG that is displayed at 24px and cannot change colour solves nothing an SVG does not solve better. Recommended Shopify mapping is `snippets/icon-search.liquid`, `snippets/icon-account.liquid`, `snippets/icon-cart.liquid` (manifest).

### 8.4 Feature icons — the design decision, and the single rule

Spec §17 requires that the crown, community, globe and diamond preserve their existing visual character and forbids redesign. That makes their treatment a **design decision, not a conversion**, and it is why they are absent from the authored SVG set. The manifest records DESIGN DECISION REQUIRED against the crown and "same treatment as the crown" against community and diamond.

**The rule, stated once and applied everywhere in this document:**

- **Crown, community, diamond → WebP as an interim.** All three are OPTIMIZE with recommended format WebP (manifest). Converting them stops the project paying **107,873 bytes** for three marks displayed at 44px.
- **Globe → SVG only.** The globe is REPLACE with recommended format SVG (manifest), not OPTIMIZE, because a WebP interim does not help it (§8.5). It is therefore **not** a compression candidate.
- **All four → commission a faithful vector trace**, by a designer, preserving character. Only then does the feature set become resolution-independent.

The four together are 143,498 bytes; only 107,873 of that is a WebP-interim candidate. That distinction is carried through §13.1, §14.3 and risk P3-ICON-02.

### 8.5 The globe's double duty

`images/icon-globe.png` is a single 110x110 raster used **twice**: at 16px in the announcement bar and at 44px in the values row (brief; manifest). That is a 2.75x range served by one file. At 16px the 110x110 source is downsampled by nearly seven, which softens the baked-in gold and flattens the glyph; at 44px it has 2.5x of headroom and its matting edge becomes visible. One file cannot serve both ends of that range well.

The globe is classified FEATURE because it is a value-tile glyph (Phase 2 §18.1, "Worldwide"); its double duty in the announcement bar is what makes a single raster untenable. This is the reason its manifest status is REPLACE where its three siblings are OPTIMIZE.

### 8.6 The cart icon's sprite-edge artefact

`images/icon-cart.png` "retains a sliver of the sprite sheet gold badge along its right edge" (manifest) — the cut from `images/icons-sprite.png` was taken a few pixels wide, so a fragment of the neighbouring mark is baked into a file the page renders at 24px in the header. Phase 1 recorded this as ICON-02. It is a visible brand defect on the most-looked-at control in the header, and no compression setting touches it. `phase-3-assets/icons/icon-cart.svg` (346 B) is drawn clean and resolves it. Tracked here as **P3-ICON-04** — the Phase 3 risk ID is deliberately distinct from the Phase 1 issue ID it cites.

## 9. Social Icons

Spec §18 requires that Facebook, Instagram, TikTok, YouTube, X, Pinterest, LinkedIn, Spotify, Email and WhatsApp each be inspected, that the platforms actually present in the project be determined, and that no social account be invented. Each is dispositioned below.

### 9.1 Three different numbers, none of them the answer

Three sources disagree about how many social channels God Squad has:

| Source | Count | Evidence |
|---|---|---|
| Files in the project | **2** | Two SOCIAL rows: `images/icon-facebook.png`, `images/icon-instagram.png` (manifest) |
| The approved mockup | **4** | Facebook, Instagram, TikTok, YouTube (manifest, `icon-instagram.png` note) |
| `images/social-sprite.png` | **10** | "a 2172x724 AI-generated sheet of ten social marks in three styles" (manifest) |

None of the three numbers is the answer, because the answer is a business fact nobody has supplied. The sprite sheet proves only that an image generator drew ten marks; the mockup proves only that four were once drawn into a design. Neither proves an account exists.

The sprite sheet's ten marks are **not enumerated** in any Phase 3 evidence, so per-platform presence on that sheet is established only for Facebook and Instagram — whose PNGs were cut from it (manifest).

| Platform | File in project | On the sprite sheet | In the approved mockup | On the page | Verdict |
|---|---|---|---|---|---|
| Facebook | `images/icon-facebook.png`, 130x130, 36,771 B | yes — the PNG was cut from it | yes | yes, footer | **AVAILABLE** (artwork) · **BUSINESS INFORMATION REQUIRED** (account) |
| Instagram | `images/icon-instagram.png`, 130x130, 42,319 B | yes — the PNG was cut from it | yes | yes, footer | **AVAILABLE** (artwork) · **BUSINESS INFORMATION REQUIRED** (account) |
| TikTok | none | not enumerated | yes | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| YouTube | none | not enumerated | yes | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| X | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| Pinterest | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| LinkedIn | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| Spotify | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |
| Email | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** (a contact channel, not a network; needs a published address before it can be linked) |
| WhatsApp | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** (a contact channel, not a network; needs a published number) |
| Any other platform outside the ten above | none | not enumerated | no | no | **MISSING** · **BUSINESS INFORMATION REQUIRED** |

No social account is asserted here for any platform, including the two whose artwork exists.

### 9.2 What the two available marks actually are

Both are **REPLACE**, and neither is a clean glyph. The manifest records `icon-facebook.png` as a "circled two-tone badge cut from the social sprite, where the mockup shows a plain glyph" — so the artwork in the build does not match the approved design, quite apart from its provenance. `icon-instagram.png` carries the same note. At 130x130 each, they are 79,090 bytes for two footer marks that should be a few hundred bytes of vector apiece.

### 9.3 Trademark: platform marks come from official brand kits

Both marks were cut from an AI-generated sheet. `images/social-sprite.png` is explicitly recorded as "not a licensing-safe source for platform trademarks" (manifest). Platform logos are registered trademarks used under each platform's own brand guidelines, which govern colour, clear space, minimum size and permitted variants.

**The rule for Phase 10: every platform mark is downloaded from that platform's official brand kit as SVG and used unmodified.** None is traced, redrawn, regenerated or recoloured, and none is taken from `images/social-sprite.png`. This applies to Facebook and Instagram — whose current files must be replaced, not optimised — and to every platform later confirmed. Recommended Shopify mapping is `snippets/social-icons.liquid` (manifest). Tracked as **P3-SOC-01**.

### 9.4 What is BUSINESS INFORMATION REQUIRED

1. **Which platforms God Squad actually operates.** Nothing in the project answers this. The two footer anchors are image-only and go nowhere (Phase 1: six of nine links are `href="#"`; the two social anchors are prototype lines 160-161).
2. **The live Facebook URL** (manifest, `icon-facebook.png`).
3. **The live Instagram URL**, and whether the TikTok and YouTube channels shown in the mockup exist (manifest, `icon-instagram.png`).
4. **Whether any of X, Pinterest, LinkedIn, Spotify, Email or WhatsApp is a channel the business wants in the footer.** All six are MISSING as artwork; whether they should exist at all is not an asset question.

Until the network set is confirmed, the footer social row cannot be built and the correct count of brand-kit SVGs to source is unknown. Tracked as **P3-SOC-02**. No account is invented, and no platform is displayed that the business has not confirmed.

## 10. Sprite Audit

The project contains two sprite sheets and three byte-identical copies of them. Together they are **4,357,733 bytes — a quarter (25.5%) of the project's 17,100,416 bytes of image weight — and not one byte of it is reachable from the page.**

### 10.1 The five sprite files

| File | Dims | Bytes | Referenced | Dup group | Status |
|---|---|---|---|---|---|
| `images/icons-sprite.png` | 2172x724 | 833,929 | no | DUP-03 (canonical) | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png` | 2172x724 | 833,929 | no | DUP-03 | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png` | 2172x724 | 833,929 | no | DUP-03 | ARCHIVE |
| `images/social-sprite.png` | 2172x724 | 927,973 | no | DUP-09 (canonical) | ARCHIVE |
| `uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png` | 2172x724 | 927,973 | no | DUP-09 | ARCHIVE |

Both sheets are 2172x724 at a 3:1 aspect ratio. Every row is ARCHIVE — candidate for archiving after final approval, never deletion now.

### 10.2 Actual usage: none

Neither sheet is referenced by `God Squad Website.html`, by CSS, or by anything else in the project. They are not CSS sprites; nothing does background-position arithmetic against them. They never functioned as a delivery mechanism — they are **source sheets**, not sprites in the performance sense, and the word "sprite" in their filenames describes their layout, not their role.

### 10.3 What they are, and what came out of them

`images/icons-sprite.png` is "a 2172x724 AI-generated contact sheet of UI and feature icons, with heavy matting halos. Never referenced by the page; the individual PNGs were cut from it" (manifest). That single sentence explains two defects documented elsewhere in this phase: the matting halos are why tracing the icon rasters was rejected (§8.2), and an imprecise cut is why `images/icon-cart.png` carries a sliver of the neighbouring gold badge (§8.6, P3-ICON-04).

`images/social-sprite.png` is "a 2172x724 AI-generated sheet of ten social marks in three styles" and "not a licensing-safe source for platform trademarks" (manifest).

### 10.4 Duplication and the mismatch with reality

DUP-03 carries **two** byte-identical copies of the icon sheet, DUP-09 **one** of the social sheet: 2,595,831 bytes of pure redundancy inside an unreferenced 4,357,733-byte block (§11.1).

Ten social marks sit on one file. How many the footer will actually carry is BUSINESS INFORMATION REQUIRED (§9.4) — the build shows two, the approved mockup shows four, and no account is confirmed for any of them.

### 10.5 Recommendation: supersede with SVG, archive, delete nothing now

**RECOMMEND REPLACEMENT: individual inline SVG icons supersede both sheets** (spec §19).

1. The nine authored SVGs in `phase-3-assets/icons/` already supersede the UI portion of `icons-sprite.png` — 2,612 bytes against 833,929, individually addressable, colour-inheriting and scalable.
2. The feature portion is superseded once the commissioned trace of the crown, community, globe and diamond lands (§8.4). Until then the sheet stays as the artwork of record for those four marks.
3. The social portion is superseded by official brand-kit SVGs (§9.3), not by anything cut from `social-sprite.png`. After final approval the three duplicate copies in `uploads/` are consolidated (§11.4).
4. **Both sheets are AI-generated and their provenance and licensing are unverified (brief). ASSET PROVENANCE SHOULD BE VERIFIED.**
5. **Do not delete anything now.** Both canonical sheets remain in place as the visual record from which the live icons were cut. ARCHIVE means moved to an archive folder after final approval. Tracked as **P3-SPR-01**.

## 11. Duplicate Assets

Hashing every file with md5 found **nine exact-duplicate groups covering 20 files, i.e. 11 redundant copies, 6,733,692 bytes** (brief: totals) — 39.4% of the project's 17,100,416 bytes of image weight. Duplicates were detected by hash, never by filename (spec §5), and nothing is deleted in this phase.

### 11.1 The nine groups

| Group | Canonical (status) | Redundant copies | Redundant bytes | Copy status | Recommended action |
|---|---|---|---|---|---|
| **DUP-01** | `images/hero-group.png` 1,989,201 B (OPTIMIZE) | `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png`; `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png` | 3,978,402 | ARCHIVE | Archive both copies after approval; canonical stays — it is the live LCP source |
| **DUP-02** | `images/hero-model.webp` 39,966 B (REFERENCE ONLY) | `uploads/God-Squad-Images/01-hero-model.webp` | 39,966 | REFERENCE ONLY | Keep both; the copy belongs to the reference set |
| **DUP-03** | `images/icons-sprite.png` 833,929 B (ARCHIVE) | `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png`; `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png` | 1,667,858 | ARCHIVE | Archive both copies after approval, canonical after the feature-icon trace |
| **DUP-04** | `images/logo.png` 47,147 B (ARCHIVE) | `uploads/God-Squad-Images/06-logo.png` | 47,147 | ARCHIVE | Archive the copy after approval; the canonical is not the wordmark in use |
| **DUP-05** | `images/our-story.webp` 41,004 B (REPLACE) | `uploads/God-Squad-Images/05-our-story-models.webp` | 41,004 | REFERENCE ONLY | Keep both; canonical is REPLACE for resolution, not for duplication |
| **DUP-06** | `images/product-cap.webp` 10,002 B (REPLACE) | `uploads/God-Squad-Images/04-product-utility-cap.webp` | 10,002 | REFERENCE ONLY | Keep both; HIGH-RES PRODUCT MASTER REQUIRED |
| **DUP-07** | `images/product-hoodie.webp` 12,328 B (REPLACE) | `uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp` | 12,328 | REFERENCE ONLY | Keep both; HIGH-RES PRODUCT MASTER REQUIRED |
| **DUP-08** | `images/product-tee.webp` 9,012 B (REPLACE) | `uploads/God-Squad-Images/02-product-oversized-tee.webp` | 9,012 | REFERENCE ONLY | Keep both; HIGH-RES PRODUCT MASTER REQUIRED |
| **DUP-09** | `images/social-sprite.png` 927,973 B (ARCHIVE) | `uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png` | 927,973 | ARCHIVE | Archive the copy after approval, canonical after the network set is confirmed |
| | | **11 copies** | **6,733,692** | | |

### 11.2 Three things the table says that are easy to miss

**Not one of the nine canonicals is a KEEP.** They are OPTIMIZE, REFERENCE ONLY, ARCHIVE, ARCHIVE, REPLACE, REPLACE, REPLACE, REPLACE and ARCHIVE. Deduplicating this project does not leave nine good assets behind — it leaves nine assets that each have a separate, unrelated problem. Consolidation is housekeeping, not remediation.

**DUP-04's canonical is not the wordmark in use.** `images/logo.png` is a "white wordmark on a solid black square" that is not referenced by the page (manifest). The wordmark actually rendered in the header and footer is `images/WHITE FONT LOGO.png` (500x500 RGBA, REPLACE), which is in no duplicate group at all. Anyone consolidating DUP-04 on the assumption that they are handling the live logo is handling the wrong file.

**The `God-Squad-Images` copies are not waste.** Six of the eleven redundant files sit in `uploads/God-Squad-Images/` with a `README.txt` beside them. Five are marked REFERENCE ONLY rather than ARCHIVE; the sixth, `06-logo.png`, is ARCHIVE and is included in the consolidation in §11.4. The `README.txt` "states that the crops in this folder were cut from the 1024x1536 mockup" and is "primary evidence for the resolution ceiling" (manifest) — it only means anything while the files it describes sit next to it. Breaking up the remaining five to save 112,312 bytes would destroy a reference set to reclaim a rounding error.

### 11.3 Six relationships, only one of which is hash duplication

The spec distinguishes exact duplicates, renamed duplicates, resized versions, visually similar versions, alternate crops and different formats of the same image. All six are present in this project, and only the first is what an md5 pass finds.

**1. Exact duplicates — identical bytes.** The nine groups above: 20 files, 11 redundant copies, 6,733,692 bytes.

**2. Renamed duplicates — one image under several names.** `images/hero-group.png`, `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` and `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png` are one 1,989,201-byte image under three names, one of them a generator's timestamp and one a slugged variant of it. The numbered `God-Squad-Images` set is the benign case: descriptive renames of the `images/` files, kept deliberately as a labelled reference set.

**3. Resized versions — the same artwork at a different size.** `white-font-300x300-mu98qi59-mytq.png` is 244x184, 23,444 bytes: a reduced export of a wordmark that also exists at 500x500 in five other files, four distinct by hash (`images/logo.png` and `uploads/God-Squad-Images/06-logo.png` are DUP-04). Its filename claims 300x300 and the file is 244x184, which is why filename-based deduplication is unsafe here. Six LOGO rows, 242,786 bytes, across five distinct hashes.

**4. Visually similar versions — same image, different encode, different hash.** Two pairs, and md5 cannot see either:

- `images/hero-model.webp` (md5 6d545230…) and `01-hero-model-mu98p88t-7jig.webp` (md5 74bc4fd4…): both 650x480, both exactly 39,966 bytes, different hashes. The manifest records the second as a "separate re-encode of DUP-02, not byte-identical".
- `white-font-trans-mu98q2ez-zrdd.png` (md5 f9359a73…) and `white-font-trans-mu98qky0-5tt6.png` (md5 5fc6d35c…): both 500x500, both exactly 43,606 bytes. The manifest records "same 500x500 size as its sibling but a different hash, so it is a separate encode, not a copy".

Identical dimensions and identical byte counts with differing hashes is the signature of a re-encode, not of two different images. Resolving each pair needs a pixel or perceptual diff, which Phase 3 did not run. Neither pair may be archived on the assumption that it is redundant until that diff is done. Tracked as **P3-DUP-NEAR-01**.

**5. Alternate crops — different regions of one source.** The 1024x1536 mockup is one source stretched to do four production jobs: `product-tee.webp` 235x230, `product-hoodie.webp` 235x235, `product-cap.webp` 215x190 and the Our Story image. Two further crops of the mockup's hero band exist as reference only: `images/hero-model.webp` and, in the Our Story slot today, `01-hero-model-mu98p88t-7jig.webp` — the wrong crop, with the headline fragments baked into its pixels (manifest). `.thumbnail` (640x355, 25,542 B, OTHER, REMOVE) is an editor-generated preview of the page, not a crop of the mockup, and is unrelated to this family.

**6. Different formats of the same image — format variants, not hash duplicates.** `uploads/GODSQUAD WEBSITE MOCKUP.png` (1,872,888 B) and `uploads/God-Squad-Images/00-full-mockup-reference.webp` (182,250 B) are the same 1024x1536 frame in two formats; the manifest states plainly that it is "not a duplicate by hash because the format differs". The same relationship holds between `images/hero-group.png` and the five Phase 3 WebP rungs derived from it. **These relationships are format-variants, not hash duplicates, and they must survive consolidation** — a dedupe pass keyed on hash will not touch them, but one keyed on visual similarity would destroy both the PNG design master and the production ladder.

### 11.4 Recommended action

1. **Change nothing today.** Phase 3 is read-only on originals; this section is a proposal for approval, not a change log.
2. **Archive the six redundant copies whose status is ARCHIVE:** two in DUP-01, two in DUP-03, one in DUP-04, one in DUP-09. That is **6,621,380 bytes** — 98.3% of all redundancy, in six file moves.
3. **Leave the five REFERENCE ONLY copies where they are** (112,312 bytes, DUP-02 and DUP-05 through DUP-08). They are the labelled reference set described in §11.2 and are worth more in place than the bytes are worth reclaimed.
4. **Run a pixel or perceptual diff on the two near-duplicate pairs in §11.3 item 4 before either member is archived** (P3-DUP-NEAR-01).
5. **ARCHIVE means moved after approval.** No original is deleted, overwritten, renamed or destructively processed in Phase 3 or by this recommendation. The canonical of every group stays exactly where it is.

## 12. Image Quality

Quality here means four separable things, assessed independently because they have different remedies: **resolution sufficiency** (fixed only by re-sourcing), **compression** (fixed by re-encoding), **artefacts and cropping** (fixed by re-cutting from a better source), and **brand presentation** (a judgement, not a measurement). Each asset can pass one and fail another.

### 12.1 Per-asset quality assessment

| Asset | Resolution sufficiency | Compression | Artefacts / cropping | Brand presentation |
|---|---|---|---|---|
| `images/hero-group.png` 1672x941, 1,989,201 B | **Insufficient at retina.** A full-bleed slot on a 1440px viewport demands 2,880 device px at DPR 2; the source supplies 0.58x | **Wrong container.** RGB with no alpha channel, so PNG buys nothing; the equal-dimension WebP rung is 119,850 B, 94.0% smaller (brief: hero ladder) | Clean. No artefacts or banding at 1:1 on face, garment detail or sky gradient (brief) | Strong. The composition the brand is built on |
| `images/product-tee.webp` 235x230, 9,012 B | **Insufficient.** 1.23x upscale at best, 4.88x at worst (§5.2) | 0.167 B/px — already light; re-encoding saves nothing worth having | 2.1% of width re-cropped by the square tile; mockup backdrop carried in | Cannot support "Premium Quality" (§12.2) |
| `images/product-hoodie.webp` 235x235, 12,328 B | **Insufficient.** Same ladder | 0.223 B/px | No second crop — the only product file already at 1:1 | As above |
| `images/product-cap.webp` 215x190, 10,002 B | **Insufficient.** Same ladder, from the smallest source | 0.245 B/px | **11.6% of width edge-cropped** by the 1:1 tile — the worst crop in the product set (manifest) | As above. Risk A-04 |
| `01-hero-model-mu98p88t-7jig.webp` 650x480, 39,966 B **(in use, Our Story)** | **Insufficient.** 1.53x upscale at DPR 1, 4.61x at DPR 3 (§6.4) | 0.128 B/px — the lightest file in the project per pixel | **Headline fragments baked into the pixels** — "A PURPOSE", "K BY", "TH."; ~29% of height discarded by the cover crop | **Fails.** Another section's typography showing inside the story image. Risk A-02, P0 |
| `images/our-story.webp` 535x348, 41,004 B | **Insufficient.** 1.87x at DPR 1, 5.60x at DPR 3 | 0.220 B/px | ~20% of height discarded to reach the 1.92:1 slot | Correct content, unusable size (§6.2) |
| `images/WHITE FONT LOGO.png` 500x500, 37,836 B | Adequate in pixels — the visible mark renders about 66x50 CSS px (brief: hard facts) | RGBA PNG; correct container for a transparent mark, wrong medium for a wordmark | **Heavy transparent padding** costs the mark display size at a fixed 78px header box | Raster wordmark, filename with spaces and upper case. VECTOR LOGO REQUIRED (manifest) |
| `images/icon-cart.png` 110x110, 29,127 B | 110px into a 24px slot — ample even at DPR 3 | 2.41 B/px | **Retains a sliver of the sprite sheet's gold badge along its right edge** (brief: hard facts) — an unwanted background fragment | Visible defect in the header |
| `images/icon-search.png`, `images/icon-account.png` 110x110 | Ample at 24px | 2.34 / 2.35 B/px | Clean | Colour baked into the pixels, so they cannot follow a surface |
| `images/icon-crown.png` 130x110 · `images/icon-diamond.png` 130x110 | **Marginal.** 110px on the short edge serving a 44px slot is 2.50x at DPR 1, 1.25x at DPR 2 and **0.83x at DPR 3** — below 1:1 on a modern phone | 2.33 / 2.42 B/px | Clean; matting halos at the edges (`phase-3-assets/README.md`) | Approved character, must be preserved (spec §17). Risk A-13 |
| `images/icon-community.png` 150x110 | Marginal — short edge 110, as above | 2.42 B/px | As above | As above |
| `images/icon-globe.png` 110x110, 35,625 B | **Two slots, one raster.** 6.88x oversupply at the 16px announcement-bar use; **0.83x at DPR 3** at the 44px values use (manifest) | **2.94 B/px, the densest of the set per pixel** | As above | Gold baked in, so it cannot invert |
| `images/icon-facebook.png`, `images/icon-instagram.png` 130x130 | Ample — 28x28 slot, 1.55x even at DPR 3 | 2.18 / 2.50 B/px | Clean | **Platform marks redrawn rather than taken from each platform's brand kit.** Risk A-08 |
| `images/icons-sprite.png`, `images/social-sprite.png` 2172x724 | n/a — referenced by nothing | 0.53 / 0.59 B/px, 1,761,902 B for the pair | The individual icon PNGs were cut from these (brief: hard facts) | Dead weight. Audited in §10 |
| `phase-3-assets/hero/` 5 rungs, 311,174 B total | Serves the desktop crop only | q 0.82; full-size rung 94.0% smaller than the PNG | Verified at full frame and 1:1 on face, garment and sky gradient: no artefacts, no banding (brief) | Clean, and the strongest production asset in the project |
| `phase-3-assets/icons/` 9 SVGs, 2,612 B total | Resolution-independent by construction | 290 B average | Single root, no embedded raster, no hard-coded colour, no editor metadata (`phase-3-assets/README.md`) | Drawn to the Phase 2 contract: 24x24, stroke 1.5, `currentColor` |

### 12.2 What compression can and cannot fix here

The product and story WebPs sit between 0.128 and 0.245 B/px. Those are already light encodings. **Re-compressing the entire product set would save a fraction of 31,342 bytes**, and it would buy that saving by degrading the only pixels the project has. The constraint on these files is pixel count, not byte count, and spec §10 forbids upscaling them and treating the result as an original.

The converse holds for the rasters that *are* heavy: `images/hero-group.png` at 1,989,201 B is a container choice, not a quality choice, and the Phase 3 ladder already demonstrates the 94.0% saving with no visible loss.

One brand-presentation consequence has to be stated plainly rather than left to inference. The Values row on the page reads `Premium Quality` / `Crafted To Inspire`, and the shop section reads "Premium Essentials for a Higher Purpose." (prototype markup). **Launching on these images cannot support the page's own claims, because fabric, stitching and print texture are not present in the files at any size.** No encoder setting changes that.

### 12.3 Format and weight findings

- **Icon set.** `phase-3-assets/icons/` holds nine drawn SVGs, 2,612 bytes total. Three of them replace an existing raster directly — `icon-search.svg` 293 B, `icon-account.svg` 309 B and `icon-cart.svg` 346 B, **948 bytes against 85,933 for the three PNGs, a 98.9% reduction**. The remaining six (arrow, chevron, close, menu, plus, minus) have no raster counterpart in the project. The full nine-PNG raster icon set costs 308,521 bytes, but six of those nine — the four feature icons and the two platform marks — await the decisions at M-10 and M-11 and are not replaced by this set.
  - *Erratum, for correction when `phase-3-assets/README.md` is next revised in a later phase:* that file states "2,612 bytes, against 308,521 bytes for the nine raster PNGs they can replace, a 99.2% reduction". The two sets of nine are not the same nine. The like-for-like figure is the 98.9% above. Nothing is changed in Phase 3; this is recorded, not edited.
- **PNG used for alpha-free photography.** `images/hero-group.png` is the single largest saving available in the project and is already demonstrated.
- **No AVIF.** Shopify's CDN serves WebP automatically and does **not** output AVIF, so authoring AVIF masters for this store buys nothing.
- **Duplicates as weight.** Nine exact duplicate groups cover 20 files, 11 of them redundant copies (brief: totals). Duplicate bytes are a quality problem as well as a storage one, because a duplicate is a second chance to wire in the wrong file — which has already happened once (§6.3).

### 12.4 Acceptance checks every incoming master must pass

Quality control is fixed by spec §33. Checks 1-6 and 16-19 are its requirements; 7-15 are the measurable expressions this project needs to make them testable. Every production candidate is checked against all nineteen before it enters `phase-3-assets/` or a Shopify media library.

1. **No unintended cropping** (spec §33) — the composition survives at every aspect ratio the `sizes` attribute will produce, verified at the widest and narrowest.
2. **No pixelation** (spec §33) — verified at 1:1, not at fit-to-window.
3. **No visible compression artefacts** (spec §33) — inspected at 1:1 on the hardest regions: skin, garment weave, and any smooth gradient, where banding appears first.
4. **No unwanted background** (spec §33) — no fragment of a neighbouring asset. This is the check `images/icon-cart.png` fails, with its sliver of the sprite's gold badge.
5. **Correct aspect ratio** (spec §33) — matches the standard for its class: 1:1 product, 16:9 or wider story and collection.
6. **Correct brand presentation** (spec §33) — the garment, the mark and the people are shown as the brand intends.
7. **Short edge meets the largest device-pixel demand for its slot** — 2048px for product (§5.2), 2000px+ for story (§6.6), 2400px+ for collection art (§7.4).
8. **No text baked into the pixels** — no headline, no wordmark, no fragment of either. This is the check `01-hero-model-mu98p88t-7jig.webp` fails.
9. **Focal point survives the crop** — declared, and verified against the desktop band and the phone band separately.
10. **Colour profile is sRGB and embedded.**
11. **Alpha present only where the standard for that class requires it.**
12. **Consistent scale across its set** — same garment-to-frame ratio, same margins.
13. **Consistent background across its set** — one background for the whole catalogue.
14. **Consistent lighting across its set** — the documented key direction, fill ratio and colour temperature from §5.3.
15. **Filename follows the convention** — lower case, hyphens, no spaces, no version words (spec §26).
16. **Orientation correct as shot** (spec §33) — no rotation inherited from EXIF that a stripped file would lose.
17. **No accidental transparency** (spec §33) — alpha is present only where check 11 requires it, never as an unintended matte.
18. **Correct logo placement** (spec §33) — where the garment or scene carries the mark, the wordmark is not cropped, mirrored or occluded.
19. **No duplicate content** (spec §33) — the incoming file is hashed and checked against the manifest before intake, so the project does not acquire a tenth duplicate group. This is the check that would have caught `01-hero-model-mu98p88t-7jig.webp` reaching the Our Story slot.

## 13. Image Format Strategy

The project's 41 original image files total 17,100,416 bytes (brief: totals), almost all PNG or WebP — `.thumbnail` is recorded as `application/octet-stream` and its format is undetermined. Phase 3 added fourteen production copies on top: nine SVG (§8.2) and five WebP (§14.1). No original was converted, overwritten or re-encoded in place.

### 13.1 The format decision, by asset class

| Asset class | Format | Why | Assets |
|---|---|---|---|
| **Photography** — hero, story, product, lifestyle | **WebP** | Lossy photographic compression at a quality no viewer can distinguish, with an alpha channel available if ever needed. The hero ladder demonstrates the margin: 94.0% smaller at full width with no visible artefacts (brief: hero ladder). | `hero-group.png` → the five-rung ladder; the story and product images are already WebP |
| **UI vector icons** | **SVG** | Resolution-independent, colour-inheriting via `currentColor`, hundreds of bytes rather than tens of thousands, and accessible as markup. | The nine authored icons: search, account, cart, menu, close, chevron, arrow, plus, minus |
| **Brand marks** | **SVG** master | A wordmark rendered at 78px in the header and 56px in the footer must be a vector; a 500x500 raster with heavy transparent padding renders the visible mark at about 66x50 (manifest). **PNG only as an interim** until a vector master is located or commissioned. | `images/WHITE FONT LOGO.png` and the other wordmark exports — five files at 500x500, four distinct by hash (`images/logo.png` and `uploads/God-Squad-Images/06-logo.png` are DUP-04) |
| **Feature icons** — crown, community, globe, diamond | **crown, community, diamond → WebP interim; globe → SVG only** | Spec §17 forbids redesign, so a faithful trace is a commissioned design task, not a conversion (§8.4). The WebP interim buys weight back on the three OPTIMIZE marks (107,873 B). The globe is REPLACE, not OPTIMIZE, because one raster cannot serve both 16px and 44px, so a WebP interim does not help it. | `icon-crown.png`, `icon-community.png`, `icon-diamond.png` → WebP; `icon-globe.png` → SVG |
| **Social / platform marks** | **SVG from the official brand kit** | Trademarks used under each platform's brand guidelines; never traced, regenerated or recoloured (§9.3). | `icon-facebook.png`, `icon-instagram.png` → REPLACE |
| **Genuine transparency or lossless need** | **PNG** | Where alpha is real and a lossy encode would fringe it. | The wordmark exports, which are RGBA with real transparent padding (manifest, `images/WHITE FONT LOGO.png`), qualify until a vector master exists. No photographic asset qualifies. |
| **Compatibility fallback** | **JPEG** | Where a consumer genuinely cannot take WebP — print, some email clients, some third-party feeds. | None in the storefront today. Shopify's CDN negotiates format, so no JPEG fallback needs to be authored for the web. |
| **Evidence** — MOCKUP, REFERENCE | **Leave as found** | These are a record, not delivery. Re-encoding evidence damages the thing it is kept for. | The two MOCKUP files (`uploads/GODSQUAD WEBSITE MOCKUP.png` 1,872,888 B; `uploads/God-Squad-Images/00-full-mockup-reference.webp` 182,250 B) and the four REFERENCE editor screenshots |

### 13.2 The hero PNG bought nothing

`images/hero-group.png` is 1672x941, 1,989,201 bytes, **RGB with no alpha channel** (brief). PNG's entire advantage over a lossy format is lossless reproduction plus alpha. This image is a photographic composition with no transparency and no flat colour regions, so it gets no benefit from lossless encoding and pays full price for it: 1.99 MB for the page's LCP image. Re-encoded to WebP at the same 1672x941 it is 119,850 bytes — **94.0% smaller** — with no visible artefacts (brief: hero ladder).

This is the clearest format error in the project, and it is a pure win: nothing about the image changes, only the container. It is not the only large PNG — the two sprite sheets are 1,761,902 bytes between them — but those are unreferenced and superseded rather than mis-encoded (§10.5). Tracked as **P3-FMT-01**.

### 13.3 What Shopify's CDN does, and what it does not

Two facts govern every format recommendation above, and one of them is commonly got wrong:

- **The CDN serves WebP automatically.** Upload a PNG or a JPEG and Shopify negotiates WebP to clients that accept it. Uploading WebP masters is still correct — it keeps the stored master small and removes a transcode — but WebP delivery does not depend on it.
- **The CDN does not output AVIF.** Any recommendation, checklist or audit that asks for an AVIF ladder on Shopify is asking for something the platform will not produce. WebP is the delivery format; there is no AVIF rung to author, and none exists in `phase-3-assets/hero/`.

**Use `image_url` with explicit `widths:` and `sizes:`, together with `image_tag`. Never hand-build a CDN URL.** A hand-assembled `/cdn/shop/files/...` string bypasses `image_tag`, which is the filter that builds the `srcset` from `widths:` — `image_url` returns one URL and emits no `srcset` by itself. A hand-built string also pins a transformation the platform may change, and silently breaks when the file is re-uploaded. Tracked as **P3-FMT-02**.

### 13.4 Provenance constrains format choice

The hero, both sprite sheets and the icon set are AI-generated, and their provenance and licensing are unverified (brief). **ASSET PROVENANCE SHOULD BE VERIFIED.** This bears directly on format work: re-encoding an asset does not establish the right to use it, and committing a five-rung production ladder to a source whose licence is unconfirmed concentrates the exposure rather than reducing it. Verification is a business and legal step, not an asset step. Tracked as **P3-PROV-01**.

## 14. Compression Strategy

Phase 3 compressed exactly one source image and deliberately left everything else alone. The restraint is the strategy: in this project, most oversized files are not badly compressed, they are redundant, unreferenced, or scheduled for replacement — and none of those is an encoder problem.

### 14.1 What was compressed

One source: `images/hero-group.png` (1672x941, 1,989,201 B, RGB with no alpha), re-encoded to a five-rung WebP width ladder at quality 0.82. The original is untouched and remains in place.

| File | Dims | Bytes | Of source |
|---|---|---|---|
| `hero-walk-by-faith-desktop-1672w.webp` | 1672x941 | 119,850 | 6.0% |
| `hero-walk-by-faith-desktop-1280w.webp` | 1280x720 | 81,354 | 4.1% |
| `hero-walk-by-faith-desktop-960w.webp` | 960x540 | 59,210 | 3.0% |
| `hero-walk-by-faith-desktop-640w.webp` | 640x360 | 31,500 | 1.6% |
| `hero-walk-by-faith-desktop-420w.webp` | 420x236 | 19,260 | 1.0% |
| | | **311,174** | |

The full-size rung is **94.0% smaller** than the PNG. The whole five-rung ladder is 311,174 bytes — still 84.4% less than the single PNG it replaces.

**Why the hero and nothing else.** It is the LCP image, it is the largest referenced file in the project, and it was in a format that bought it nothing (§13.2). It is also the one asset where compression alone fixes the whole defect: no re-shoot, no re-crop, no design decision, no business input.

**Why 0.82.** 0.82 was the quality chosen for this encode and it was verified acceptable on this photograph (brief: hero ladder). No lower quality was encoded, so this phase has no measured floor below which artefacts appear. Establishing that floor is part of the numeric gate recommended in §14.2.

### 14.2 How quality was verified

The original and the re-encode were rendered side by side at full frame, then at 1:1 on the two regions where WebP fails first on this image: face and garment detail, and the sky gradient where banding would appear earliest. Result: no visible artefacts, no banding (brief: hero ladder; `phase-3-assets/README.md`).

**This was a visual check, not a numeric measurement.** It is sufficient to approve one image reviewed by eye; it is not sufficient as a repeatable gate for a storefront's worth of assets. **Recommendation for Phase 10: adopt a numeric gate** — a structural-similarity or perceptual metric with a stated pass threshold, run per asset, recorded alongside the file — and use it to establish the quality floor that §14.1 could not. Until then, every encode needs a human look at the two hardest regions of that specific image. Tracked as **P3-CMP-01**.

The nine authored SVGs were not "compressed" in any encoder sense. They were authored minimal: single root element, no embedded raster, no hard-coded colour, no editor metadata (§8.2). 2,612 bytes for nine icons is what authoring to a contract produces, not what a minifier recovers.

### 14.3 What was deliberately not compressed, and why

| Asset / group | Bytes | Why not |
|---|---|---|
| The two MOCKUP files (`uploads/GODSQUAD WEBSITE MOCKUP.png` 1,872,888 B; `uploads/God-Squad-Images/00-full-mockup-reference.webp` 182,250 B) and the four REFERENCE editor screenshots | 5,933,641 | Evidence, not delivery. The PNG mockup is the approved design master and the source of every product and story crop; full-quality pixels must be taken from it (manifest). Compressing a record degrades the only thing it is kept for. None of it is served to a visitor. |
| The two sprite sheets and their three byte-identical copies | 4,357,733 | Unreferenced, and superseded by SVG (§10.5). Compressing dead weight is wasted work; this is a consolidation problem. |
| The eleven redundant duplicate copies | 6,733,692 | A deduplication problem (§11), not an encoder problem. Six file moves reclaim 6,621,380 bytes of it after approval — far more than any re-encode would. |
| The four feature icons (crown, community, globe, diamond) | 143,498 | Design decision pending (§8.4). Of this total, only **107,873 bytes** — crown, community, diamond — is a WebP-interim candidate; the globe is REPLACE and goes to SVG, so it is not a compression target at all. |
| The three UI icon rasters (`icon-account.png`, `icon-cart.png`, `icon-search.png`) | 85,933 | Superseded by 948 bytes of authored SVG (§8.2). Compressing a file you are about to retire is wasted work, and it would not fix the cart's baked-in gold sliver or the inability to inherit colour. |
| The two platform marks (`icon-facebook.png` 36,771 B, `icon-instagram.png` 42,319 B) | 79,090 | REPLACE from official brand kits (§9.3). Re-encoding a trademark cut from an AI-generated sheet does not make it licensable, and both are the wrong artwork against the mockup. |
| The two referenced/canonical story images (`01-hero-model-mu98p88t-7jig.webp` 39,966 B, `images/our-story.webp` 41,004 B) and the six LOGO wordmark exports (242,786 B) | 323,756 | Both REPLACE for reasons no encoder addresses: the story image in use is the wrong crop with headline fragments baked into its pixels, and the wordmark needs a vector master (manifest). |
| The three product WebPs | 31,342 | Already WebP and already tiny. Their defect is resolution — 235x230, 235x235, 215x190 crops of a 1024x1536 mockup rendered at 288px and above — which compression makes worse, not better. HIGH-RES PRODUCT MASTER REQUIRED. |

**These groups overlap and their totals are not additive.** The three redundant sprite copies (2,595,831 B) are counted in both the sprite row and the duplicate row; the two MOCKUP files are in the evidence row only.

The pattern is consistent: **compress only assets that are correct, referenced and staying.** In this project exactly one asset met all three tests.

### 14.4 Targets for future assets

| Asset class | Master | Delivery | Budget |
|---|---|---|---|
| Hero, desktop | ≥2400px wide, no text baked in | WebP ladder, q0.80–0.85 | ≤150 KB at 1672w — the current 1672w rung is 119,850 B, already inside budget |
| Hero, mobile | dedicated portrait or art-directed source | WebP ladder | ≤120 KB at 828w. **This source does not exist** — the 16:9 desktop frame cropped to a phone band loses about a third of its width, cutting the third model and the back-print message (brief) |
| Product | square, ≥2048x2048, consistent background and lighting | WebP | ≤200 KB at 1200w |
| Editorial / story | ≥2000px on the long edge, no headline text in the pixels | WebP | ≤180 KB at 1400w |
| UI icons | authored vector, 24x24, stroke 1.5, `currentColor` | SVG inline | ≤500 B each; no embedded raster, no editor metadata |
| Feature icons | commissioned faithful trace, character preserved | SVG; WebP only as the interim in §8.4 | ≤2 KB SVG, or ≤8 KB WebP at 88px for the three OPTIMIZE marks |
| Social marks | official brand kit, unmodified | SVG | as supplied |

**Four standing rules.**

1. **Never compress an asset that is scheduled for replacement.** Seven of the eight groups in §14.3 are held back on exactly this basis.
2. **Never re-encode an original in place.** Originals are preserved untouched; every optimised file is a new, additional file (spec §31). Phase 3 modified 0 and deleted 0.
3. **Compression cannot fix resolution.** Every product image is a crop of a 1024x1536 mockup and no encoder setting changes that. These are sourcing gaps; they are recorded in the missing-asset register.
4. **The hero, the sprite sheets and the icon set are AI-generated and their provenance and licensing are unverified (brief). ASSET PROVENANCE SHOULD BE VERIFIED** before any of them is committed to as a production master.

## 15. Responsive Image Strategy

Phase 3 does not implement any of this. The prototype is functionally unchanged; every recommendation below describes how these assets should be delivered when the Shopify theme is built in a later phase.

### The geometry this strategy has to serve

The prototype wraps the entire page in `<div style="width:100%;max-width:1440px;margin:0 auto;overflow:hidden">`. Nothing is truly full-bleed: every box stops growing at 1440px. It has exactly two breakpoints, `@media (max-width:900px)` and `@media (max-width:520px)`, which gives three delivery bands: desktop at 901px and above, tablet from 521px to 900px, and phone at 520px and below. Dawn's 750px/990px breakpoints are not this layout's breakpoints and must not be copied into `sizes` strings.

### Behaviour by breakpoint

| Element | Desktop (>=901px) | Tablet (521-900px) | Phone (<=520px) |
|---|---|---|---|
| Hero image | Absolutely positioned behind a three-column grid, full width of the 1440px-capped page, `min-height:620px`, `object-fit:cover`, `object-position:center 30%` | Leaves the absolute layer and becomes a relative band: `position:relative; left:0; width:100%; height:62vw; min-height:320px; order:-1`, stacked above the copy. `min-height:620px` no longer applies | Same relative band. At a 375px viewport the band is 375x320, so covering a 16:9 source discards about a third of its width, cutting the third model and the back-print message (brief: hard facts) |
| Logo | 78px tall in the header, 56px in the footer | 56px in the header (`[data-r=logo]{height:56px}` below 900px), 56px in the footer | Same as tablet |
| UI icons (search, account, cart) | 24px | 24px | 24px |
| Globe | 16px in the announcement bar and 44px in the Brand Values row, from one 110x110 raster (manifest `images/icon-globe.png`) | Same | Same |
| Feature icons (crown, community, diamond) | 44px in the Brand Values row | Same | Same |
| Social marks (Facebook, Instagram) | 28x28 in the footer | Same | Same |
| Product card | 288px, measured at the 1440px cap (brief: hard facts). Grid is `repeat(3,minmax(0,1fr))`, gap 36px, section padding 48px | 2-up: `repeat(2,minmax(0,1fr))`, gap 20px, section padding 24px, so `calc((100vw - 68px) / 2)` - roughly 227px at 521px rising to 416px at 900px | 1-up: `minmax(0,1fr)` inside 24px padding, so `calc(100vw - 48px)` - 327px at 375px, 382px at 430px (brief: hard facts) |
| Story image | `left:30%; width:70%` of the capped page, measured at 998px wide (manifest `01-hero-model-mu98p88t-7jig.webp`); 1008px at a full 1440px container and fixed there above it | `position:relative; width:100%; height:60vw; min-height:280px; order:-1` | Same relative band |

### The Shopify approach

Every image is piped through `image_url` and then through `image_tag`. Never hand-build a `cdn.shopify.com` URL: the path format is not a contract, and a hand-built URL bypasses the transform pipeline that produces the alternate widths.

The division of labour between the two filters is exact and is the thing most often got wrong:

- **`image_url`** accepts `width`, `height`, `crop`, `format` and `pad_color` only. It returns one URL for one rendition. It is the **cap**: it decides the largest pixel size the CDN is asked to produce.
- **`image_tag`** accepts `widths`, `sizes`, `loading`, `fetchpriority`, `alt`, `class`, `width`, `height` and `preload`. It builds the `srcset` from `widths`, writes the `sizes` attribute, and emits any parameter it does not recognise verbatim as an HTML attribute - which is how `fetchpriority` reaches the tag.

So `widths:` and `sizes:` are stated explicitly on every `image_tag` call, never on `image_url`.

**The CDN does not upscale.** A `widths` entry larger than the uploaded master returns the master at its native size while the `srcset` still advertises the larger descriptor. The browser's selection algorithm is then misinformed and a candidate slot is wasted. Every ladder below is therefore capped at the master's real width. Shopify's CDN also negotiates WebP automatically from the uploaded master and **does not output AVIF**, so no AVIF branch, no `<picture>` type fallback and no format juggling is needed for format alone - only for art direction.

### Width ladder rationale

The hero ladder already produced in `phase-3-assets/hero/` is 420 / 640 / 960 / 1280 / 1672 (brief: hero ladder). 1672 is the master's native width (`images/hero-group.png`, 1672x941), so the ladder stops there.

| Step | Ratio | Bytes at the upper rung | Change from the rung below |
|---|---|---|---|
| 420 -> 640 | 1.52x | 31,500 | +64% |
| 640 -> 960 | 1.50x | 59,210 | +88% |
| 960 -> 1280 | 1.33x | 81,354 | +37% |
| 1280 -> 1672 | 1.31x | 119,850 | +47% |

The steps sit between 1.31x and 1.52x apart, which is close enough that no viewport is ever served a rung more than about half again too wide. The byte changes are uneven - the 640 -> 960 step costs more than twice the 960 -> 1280 step - because compressed weight tracks where detail lands in the frame, not pixel area alone. That unevenness is a property of the image, not a defect in the ladder.

**A ceiling to record.** At the 1440px page cap on a 2x display the browser wants roughly 2880 device pixels of hero. The master tops out at 1672, so desktop retina is served at about 0.58x of what it asks for. No re-encoding fixes that; only a larger hero master would (see §20 item 3).

### `sizes` values, derived from the prototype's own CSS

| Slot | `sizes` | Derived from |
|---|---|---|
| Hero | `(min-width: 1440px) 1440px, 100vw` | Full-bleed inside the 1440px page cap; below 901px the band is `width:100%` |
| Product card | `(min-width: 901px) 288px, (min-width: 521px) calc((100vw - 68px) / 2), calc(100vw - 48px)` | Breakpoints at 900px and 520px; 3-up gap 36px / padding 48px, 2-up gap 20px / padding 24px, 1-up padding 24px |
| Story | `(min-width: 1440px) 1008px, (min-width: 901px) 70vw, 100vw` | `left:30%; width:70%` inside the 1440px cap; `width:100%` below 901px |

On the product row, `288px` is the measured render at the cap. Between 901px and 1440px the card is narrower than that, so the value over-states by up to about 40% and errs towards quality rather than starvation. A theme that wants the bytes back can use `calc(24.2vw - 57px)` for that band instead, which is the exact solution of the grid arithmetic.

### Loading strategy

| Element | `loading` | `fetchpriority` | Reason |
|---|---|---|---|
| Hero image | `eager` | `high` | It is the LCP element at every width. Never lazy, never behind an entrance animation |
| Header logo | `eager` | auto | Above the fold, beside the LCP element. It is merchant content rendered from `settings.logo` through `image_url` + `image_tag`, so it is a real request and must never be lazy. No vector logo exists - see §20 item 2 |
| Header UI icons | n/a | n/a | Inlined SVG from `snippets/icon-*.liquid`; there is no request at all |
| Announcement-bar globe | `eager` | auto | Above the hero; 16px, currently a 110x110 raster |
| Product cards | `lazy` | auto | Below the fold at every width |
| Story image | `lazy` | auto | Below the fold at every width |
| Feature icons | `lazy` | auto | Brand Values row, below the fold |
| Social marks | `lazy` | auto | Footer |

For the LCP hero, `image_tag` also accepts `preload: true`, which emits the matching `<link rel="preload" as="image" imagesrcset=... imagesizes=...>`. Use it on the hero only; preloading more than one image cancels its own benefit.

### Intrinsic dimensions, always

`image_tag` writes `width` and `height` from the image object automatically. Do not strip them, and do not override them with CSS that leaves the box undetermined. Where the CSS forces a shape the source does not have - the hero's `height:62vw; min-height:320px` band, the product tile's `aspect-ratio:1/1` - pair `object-fit:cover` with an explicit `aspect-ratio` on the container so the space is reserved before the bytes arrive. Every one of these slots currently uses `object-fit:cover`, so a missing intrinsic size shows up as layout shift, not as distortion.

### Hero, with the art-direction case

No mobile hero exists (brief: hard facts). Cropping the 16:9 desktop frame into the phone band discards about a third of its width. That is an art-direction problem, not a resolution problem, so it needs a second source and a `<picture>` - not another rung:

```liquid
{%- assign hero_alt = section.settings.hero_desktop.alt | default: 'God Squad crew' -%}
{%- if section.settings.hero_mobile != blank -%}
  {%- capture hero_mobile_srcset -%}
    {{ section.settings.hero_mobile | image_url: width: 420 }} 420w,
    {{ section.settings.hero_mobile | image_url: width: 640 }} 640w,
    {{ section.settings.hero_mobile | image_url: width: 900 }} 900w,
    {{ section.settings.hero_mobile | image_url: width: 1200 }} 1200w
  {%- endcapture -%}
  <picture>
    <source media="(max-width: 900px)" srcset="{{ hero_mobile_srcset }}" sizes="100vw">
{%- endif -%}
{{ section.settings.hero_desktop
   | image_url: width: 1672
   | image_tag:
       widths: '420, 640, 960, 1280, 1672',
       sizes: '(min-width: 1440px) 1440px, 100vw',
       loading: 'eager',
       fetchpriority: 'high',
       preload: true,
       alt: hero_alt,
       class: 'hero__image' }}
{%- if section.settings.hero_mobile != blank -%}
  </picture>
{%- endif -%}
```

The `<source>` srcset is assembled from repeated `image_url` calls, which is still the filter doing the work - not a hand-built CDN URL. Until `hero_mobile` is supplied the `<picture>` collapses and the desktop frame is used at every width, which is the present behaviour and the reason RA-03 is a P0.

### Product, capped at the master that actually exists

```liquid
{%- assign p_alt = product.featured_media.alt | default: product.title -%}
{{ product.featured_media
   | image_url: width: 235
   | image_tag:
       widths: '215, 235',
       sizes: '(min-width: 901px) 288px, (min-width: 521px) calc((100vw - 68px) / 2), calc(100vw - 48px)',
       loading: 'lazy',
       alt: p_alt,
       class: 'card__image' }}
```

The alt fallback is assigned first. Written inline as `alt: product.featured_media.alt | default: product.title`, Liquid applies `default` to the output of `image_tag`, not to the alt argument, and the fallback silently never fires.

The masters are 235x230, 235x235 and 215x190 (brief: hard facts), so the ladder cannot honestly exceed 235. Rungs of 576, 764 or 1200 would be dead descriptors on the store's only commerce imagery. The ladder opens up to `'288, 576, 864, 1200'` with `image_url: width: 1200` the moment a high-resolution master lands (§20 item 3) - and not before.

### Story, same discipline

The slot renders 998px wide and the current source is 650x480 (manifest `01-hero-model-mu98p88t-7jig.webp`). Today the only honest call is `image_url: width: 650` with `widths: '520, 650'`. Once HIGH-RES STORY MASTER REQUIRED is satisfied it becomes:

```liquid
{%- assign story_alt = section.settings.story_image.alt | default: 'God Squad community' -%}
{{ section.settings.story_image
   | image_url: width: 2016
   | image_tag:
       widths: '520, 780, 1008, 1512, 2016',
       sizes: '(min-width: 1440px) 1008px, (min-width: 901px) 70vw, 100vw',
       loading: 'lazy',
       alt: story_alt }}
```

## 16. Naming Convention

### The rules

1. **Lower case throughout.** No upper case anywhere in the stem or the extension.
2. **Hyphens as the only separator.** No spaces, no underscores, no commas, no parentheses.
3. **ASCII only**, no accents and no punctuation beyond the hyphen and the single extension dot.
4. **No version words.** `final`, `final2`, `new`, `latest`, `copy`, `v2`, `updated`, `FINAL-FINAL` are all banned. Version belongs in the manifest and in the phase history, not in a filename.
5. **No generator hashes.** Strings such as `-mu98p88t-7jig`, `-mu98j9xl-evm9` or `-34af7243` carry no meaning to anyone reading the theme.
6. **No numeric ordering prefixes.** `01-`, `02-` encode a position in one export set, not the asset's identity.
7. **Semantic order: type, subject, qualifier.** `product-signature-tee-front`, not `front-tee-product`.
8. **One extension, matching the real bytes.** A WebP is `.webp`; `.thumbnail` with no extension at all fails this.

### Worked examples, from the spec

| Class | Production name |
|---|---|
| Logo | `logo-god-squad.svg` |
| Hero, desktop | `hero-walk-by-faith-desktop.webp` |
| Hero, mobile | `hero-walk-by-faith-mobile.webp` |
| Product, tee | `product-signature-tee-front.webp` |
| Product, hoodie | `product-heavyweight-hoodie-front.webp` |
| Product, cap | `product-utility-cap-front.webp` |
| Story | `story-community.webp` |
| UI icons | `icon-search.svg`, `icon-account.svg`, `icon-cart.svg`, `icon-menu.svg` |

### Width suffix for ladder rungs

A rung of a responsive ladder appends `-{width}w` to the base production name: `hero-walk-by-faith-desktop-1672w.webp`, `-1280w`, `-960w`, `-640w`, `-420w`. The suffix is a measurement, not a version word, and it is the last element before the extension. The five files in `phase-3-assets/hero/` follow this exactly.

This suffix is for **staged local rungs**. Once a master is uploaded to Shopify, the CDN generates the alternate widths and the suffix disappears from the workflow - a single `hero-walk-by-faith-desktop.webp` master is uploaded and `image_tag: widths: '420, 640, 960, 1280, 1672'` does the rest. The local ladder exists to prove the weights and to let the team review quality before the theme is built.

### What the current names get wrong

Five representative offenders, from the 44 originals:

| Current name | Breaks |
|---|---|
| `images/WHITE FONT LOGO.png` | Spaces, upper case |
| `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png` | Spaces, commas, upper case, underscores, generator tail |
| `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` | Underscores, generator hash |
| `white-font-trans-mu98q2ez-zrdd.png` | Generator hash |
| `01-hero-model-mu98p88t-7jig.webp` | Numeric prefix, generator hash, and the name describes a hero while the file is used in the Our Story slot |

Two of those carry spaces, one carries commas, several carry generator hashes, and one is a byte-identical duplicate of `images/icons-sprite.png` (DUP-03), distinguishable from its twin `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png` only by a `-34af7243` tail.

### Two sources, one production name

The manifest recommends `story-community.webp` as the production name for **both** `01-hero-model-mu98p88t-7jig.webp` (the file actually in use) and `images/our-story.webp` (the intended three-model crop, unreferenced at 535x348). Only one file can carry that name. Which one becomes `story-community.webp` - or whether both are superseded by new photography - is §20 item 3.

### No original file is renamed

Phase 3 renames nothing. Every one of the 44 originals keeps the name it had, byte for byte, in the place it was found. The convention above governs **production copies only**: the 14 files in `phase-3-assets/` were created under it, and any future copy is created under it.

If the owner confirms different product names, the **production copies** are re-named before upload, not after - a Shopify product media filename is baked into its CDN URL and changing it later invalidates every cached reference. The originals keep their names in every case.

## 17. Folder Structure

### Where the assets live now

| Location | Contents | Character |
|---|---|---|
| Project root | `.thumbnail`, `01-hero-model-mu98p88t-7jig.webp`, `God Squad Website.html`, `support.js`, `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png`, `white-font-300x300-mu98qi59-mytq.png`, `white-font-trans-mu98q2ez-zrdd.png`, `white-font-trans-mu98qky0-5tt6.png`, plus four phase documents and the manifest | Mixed: two live assets (the Our Story image and the script the page loads), editor debris, duplicates and documentation |
| `images/` | 19 files - the live hero, 2 logos (`WHITE FONT LOGO.png` in use, `logo.png` the DUP-04 canonical), 3 products, 7 UI/feature icon PNGs (account, cart, community, crown, diamond, globe, search), 2 social icon PNGs (facebook, instagram), 2 unreferenced sprite sheets, 2 unreferenced masters (`hero-model.webp`, `our-story.webp`) | The de facto production folder, flat, with archive material mixed into it |
| `uploads/` | 4 ChatGPT exports, 4 `pasted-*` screenshots, the 1024x1536 design mockup | Raw generator output and reference screenshots, never curated |
| `uploads/God-Squad-Images/` | 6 WebP derivatives, `06-logo.png` and a `README.txt`. Six of the eight are duplicates of `images/` (DUP-02, 04, 05, 06, 07, 08); `00-full-mockup-reference.webp` is a unique 182,250 B mockup derivative and `README.txt` is status KEEP | A curated export set, mostly duplicative |
| `phase-3-assets/` | The Phase 3 production copies - see below | Staging only; wired into nothing |

The consequence is that no folder answers the question "is this shippable?". `images/` holds the live hero next to an 833,929 B sprite sheet nothing references. The root holds a live asset next to the identical 1,989,201 B PNG it was cut from.

### What `phase-3-assets/` currently contains

| Path | Files | Bytes | Status |
|---|---|---|---|
| `phase-3-assets/icons/` | 9 authored SVGs - `icon-search`, `icon-account`, `icon-cart`, `icon-menu`, `icon-close`, `icon-chevron`, `icon-arrow`, `icon-plus`, `icon-minus` | 2,612 | KEEP |
| `phase-3-assets/hero/` | 5 WebP rungs at 1672 / 1280 / 960 / 640 / 420 | 311,174 | KEEP |
| `phase-3-assets/README.md` | Provenance and caveats for both folders | - | Documentation |

14 production copies in total. Every one is a **new, additional file**. Nothing in the original project was modified, renamed, deleted or destructively processed to produce them, and none of them is wired into the prototype - the page still references its original assets and is functionally unchanged.

The SVG icons were **drawn to the Phase 2 contract (24x24, stroke 1.5, `currentColor`), not traced** from the raster PNGs. The hero rungs were re-encoded from `images/hero-group.png` at quality 0.82, with the original preserved untouched.

**Weight, stated precisely.** The nine authored SVGs total 2,612 bytes. Three of them directly displace raster predecessors - `icon-search.png` 28,336 B, `icon-account.png` 28,470 B, `icon-cart.png` 29,127 B, 85,933 B in total - at 948 bytes, a 98.9% reduction. The other six (`arrow`, `chevron`, `close`, `menu`, `plus`, `minus`, 1,664 B) have no raster predecessor at all. The remaining 222,588 bytes of icon PNGs - crown, community, diamond, globe, facebook, instagram - are deliberately **not** replaced and are covered by §20 items 4 and 8.

> `phase-3-assets/README.md` currently states that the nine SVGs replace "the nine raster PNGs ... a 99.2% reduction". That sentence is wrong on the same premise and should be corrected at source to the three-icon / 98.9% figure above.

### Recommended production tree

The spec's target structure, with `social/` and `collections/` added ahead of the assets that will fill them:

```
assets/
  brand/         logo-god-squad.svg, logo-god-squad-inverse.svg, favicon-god-squad.png
  hero/          hero-walk-by-faith-desktop.webp, hero-walk-by-faith-mobile.webp
  products/      product-signature-tee-front.webp, product-heavyweight-hoodie-front.webp,
                 product-utility-cap-front.webp
  collections/   collection-the-faithful.webp  (none exists yet)
  editorial/     story-community.webp
  icons/         icon-search.svg, icon-account.svg, icon-cart.svg, icon-menu.svg,
                 icon-close.svg, icon-chevron.svg, icon-arrow.svg, icon-plus.svg,
                 icon-minus.svg, icon-crown.*, icon-community.*, icon-globe.*, icon-diamond.*
  social/        icon-facebook.svg, icon-instagram.svg
  reference/     GODSQUAD-WEBSITE-MOCKUP.png, mockup-reference.webp, pasted-*.png
_archive/        every ARCHIVE-status original, unchanged
```

### Mapping: where each asset lives now and where it belongs

| Current location | Destination | Manifest status |
|---|---|---|
| `images/hero-group.png` + `phase-3-assets/hero/*.webp` | `assets/hero/` | OPTIMIZE / KEEP |
| (none exists) mobile hero | `assets/hero/` | DOCUMENT AS MISSING |
| `images/WHITE FONT LOGO.png` | `assets/brand/` | REPLACE (VECTOR LOGO REQUIRED) |
| `images/logo.png`, `uploads/God-Squad-Images/06-logo.png` (DUP-04) | `_archive/` | ARCHIVE |
| `white-font-300x300-*.png`, `white-font-trans-*.png` x2 (root) | `_archive/` | ARCHIVE |
| `images/product-tee.webp`, `product-hoodie.webp`, `product-cap.webp` | `assets/products/` | REPLACE (HIGH-RES PRODUCT MASTER REQUIRED) |
| `01-hero-model-mu98p88t-7jig.webp` (root, live) | `assets/editorial/` | REPLACE (HIGH-RES STORY MASTER REQUIRED) |
| `images/our-story.webp` | `assets/editorial/` | REPLACE |
| `images/hero-model.webp` | `_archive/` | REFERENCE ONLY |
| `phase-3-assets/icons/*.svg` (9) | `assets/icons/` | KEEP |
| `images/icon-search.png`, `icon-account.png`, `icon-cart.png` | `_archive/` once the SVGs are adopted | REPLACE |
| `images/icon-crown.png`, `icon-community.png`, `icon-diamond.png` | `assets/icons/` | OPTIMIZE |
| `images/icon-globe.png` | `assets/icons/` | REPLACE |
| `images/icon-facebook.png`, `icon-instagram.png` | `assets/social/` | REPLACE |
| `images/icons-sprite.png`, `images/social-sprite.png` | `_archive/` | ARCHIVE |
| `uploads/GODSQUAD WEBSITE MOCKUP.png` | `assets/reference/` | REFERENCE ONLY |
| `uploads/God-Squad-Images/00-full-mockup-reference.webp` | `assets/reference/` | REFERENCE ONLY |
| `uploads/God-Squad-Images/README.txt` | Stays with the assets it documents | KEEP |
| `uploads/God-Squad-Images/01-,02-,03-,04-,05-*.webp`, `06-logo.png` | `_archive/` | REFERENCE ONLY / ARCHIVE |
| `uploads/pasted-*.png` (4) | `assets/reference/` | REFERENCE ONLY |
| `uploads/ChatGPT Image *.png` (4) | `_archive/` | ARCHIVE |
| `chatgpt-image-sep-20-2026-11_06_34-am-*.png` (root) | `_archive/` | ARCHIVE |
| `.thumbnail`, `support.js` | Neither; see RA-14 | REMOVE - candidate for removal after final approval |

The 1024x1536 mockup and its WebP derivative are **design masters and reference only**. Crops taken from them are what produced the present resolution ceiling; nothing cut from them should reach production. See §20 item 3.

`_archive/` is a destination in a future reorganisation, not an instruction to move anything now. Phase 3 moved nothing. Every ARCHIVE and REMOVE status is a **candidate for action after final approval**, never a deletion.

## 18. Shopify Asset Mapping

Nothing here is implemented. No Liquid file, section schema or JSON template is created in Phase 3.

### Theme asset versus merchant content

The distinction decides where a file lives, who can change it, and whether the CDN will resize it:

- **Theme assets** sit in the theme's `assets/` directory or are inlined from `snippets/`. They ship with the theme, are versioned with it, and a merchant cannot swap one from the admin. Vector UI icons belong here. They are **not** served through `image_url`, because the image transform pipeline operates on uploaded image objects, not on theme files.
- **Merchant content** is uploaded through the admin - theme settings (`settings.logo`, `settings.favicon`), section and block `image_picker` settings, product media, and collection images. These are image objects, they pass through `image_url` and `image_tag`, and the CDN produces their alternate widths and WebP renditions.

**Product photography is merchant content, not a theme asset.** Putting product images in the theme's `assets/` folder breaks variant media, the product media gallery, zoom, and the merchant's ability to change a photograph without a theme deploy. The three product WebPs go to Shopify product media.

### Mapping table

| Current asset or class | Category | Status | Shopify destination | Kind |
|---|---|---|---|---|
| `images/WHITE FONT LOGO.png` | LOGO | REPLACE | Theme setting `settings.logo`, rendered `settings.logo \| image_url: width: 600 \| image_tag: widths: ..., sizes: ...` | Merchant content |
| `images/hero-group.png` + `phase-3-assets/hero/*.webp` | HERO | OPTIMIZE / KEEP | Hero section image setting `section.settings.hero_desktop` (`image_picker`) | Merchant content |
| (none exists) mobile hero | HERO | DOCUMENT AS MISSING (asset); BUSINESS INFORMATION REQUIRED (which crop) | Hero section image setting `section.settings.hero_mobile`, consumed by a `<source media="(max-width: 900px)">` | Merchant content |
| `01-hero-model-mu98p88t-7jig.webp`, `images/our-story.webp` | STORY | REPLACE | Our Story section image setting `section.settings.story_image` | Merchant content |
| `images/product-tee.webp`, `product-hoodie.webp`, `product-cap.webp` | PRODUCT | REPLACE | **Shopify product media** - `product.featured_media`, `product.media` | Merchant content |
| `images/icon-search.png`, `icon-account.png`, `icon-cart.png` -> `phase-3-assets/icons/icon-search.svg`, `icon-account.svg`, `icon-cart.svg` | ICON | REPLACE / KEEP | `snippets/icon-search.liquid`, `snippets/icon-account.liquid`, `snippets/icon-cart.liquid`, inlined into the header | Theme asset |
| `phase-3-assets/icons/icon-menu.svg`, `icon-close.svg`, `icon-chevron.svg`, `icon-arrow.svg`, `icon-plus.svg`, `icon-minus.svg` | ICON | KEEP | `snippets/icon-*.liquid` - drawer toggle, drawer close, dropdown affordance, link arrows, quantity stepper | Theme asset. No raster predecessor in the project; the prototype draws its hamburger as three 22x2 CSS spans |
| `images/icon-crown.png`, `icon-community.png`, `icon-diamond.png` | ICON | OPTIMIZE | Brand Values **block** icon setting (`image_picker` per block) | Merchant content today; becomes a theme asset if the owner approves SVG (§20 item 8) |
| `images/icon-globe.png` | ICON | REPLACE | Announcement bar **and** Brand Values block - two settings, one source, at 16px and 44px | Merchant content; same caveat |
| `images/icon-facebook.png`, `icon-instagram.png` | SOCIAL | REPLACE | `snippets/social-icons.liquid`, driven by the theme's social URL settings | Theme asset - marks should come from each platform's official brand kit |
| (none exists) favicon | LOGO | DOCUMENT AS MISSING (asset); BUSINESS INFORMATION REQUIRED (which mark) | Theme setting `settings.favicon` | Merchant content |
| (none exists) collection imagery | COLLECTION | DOCUMENT AS MISSING (asset); BUSINESS INFORMATION REQUIRED (which collections) | Collection record image, surfaced by a collection-list section | Merchant content |
| `images/icons-sprite.png`, `images/social-sprite.png` | SPRITE | ARCHIVE | **Nothing.** Referenced by nothing; individual SVGs supersede them | - |
| `uploads/GODSQUAD WEBSITE MOCKUP.png`, `uploads/God-Squad-Images/00-full-mockup-reference.webp` | MOCKUP | REFERENCE ONLY | **Nothing.** Design master. Never ship mockup pixels as a production image | - |
| `uploads/pasted-*.png` (4) | REFERENCE | REFERENCE ONLY | **Nothing.** Working screenshots | - |
| Root duplicates and `white-font-*` variants | HERO / LOGO | ARCHIVE | **Nothing** | - |
| `images/hero-model.webp`, `uploads/God-Squad-Images/01--06-*` | HERO / PRODUCT / STORY / LOGO | REFERENCE ONLY / ARCHIVE | **Nothing.** Duplicates of `images/` canonicals | - |
| `.thumbnail`, `support.js` | OTHER | REMOVE (candidate after approval) | **Nothing.** `support.js` is the prototype runtime and is loaded by the page; it has no storefront equivalent | - |
| `uploads/God-Squad-Images/README.txt`, `God Squad Website.html` | OTHER | KEEP | Project documentation and design baseline only | - |

The table has 19 rows. Twelve name a Shopify destination - and three of those twelve are gaps with a destination but no asset (mobile hero, favicon, collection imagery). Seven have no Shopify destination at all.

Across the 62 manifest rows the same picture holds: 30 asset rows carry a named destination, 27 carry `None`, and the remaining 5 are the four phase documents (Project documentation) and the prototype HTML (Design baseline only). Rather more than half of what is in the project has no place in the store.

### Rendering rules that apply to every mapped asset

- Merchant content: `image_url` for the cap, `image_tag` for `widths`, `sizes`, `loading`, `fetchpriority` and `alt`. Never a hand-built CDN URL.
- Theme-asset SVGs: inline them through `{% render 'icon-cart' %}`, do not load them through `<img>`. Inlining removes the request, lets `currentColor` inherit the surface colour, and lets the accessible name come from the enclosing control.
- Alt text: product images describe the product and the view; decorative icons take `alt=""` and `aria-hidden="true"`; the logo takes the brand name; an interactive icon takes its label from the button, not from the glyph.

## 19. Missing Assets

Spec §37 permits an entry here only where the project **genuinely lacks** the asset. Every row below was checked against the manifest's 62 rows and the 48 scanned files before it was written. Nothing is listed because it would be nice to have; a thing is listed because it is not in the project.

The Phase 3 production copies in `phase-3-assets/` are a staging area for Phase 10, where the Shopify theme is built (`phase-3-assets/README.md`). That is the only phase attribution the README supports; the sub-scopes named in the Blocks column below are this document's allocation of work within that phase, not README text. Where no phase can be attributed, the entry names the work blocked instead.

| ID | Missing asset | What depends on it | Blocks | Risk |
|---|---|---|---|---|
| **M-01** | **High-resolution product masters** — 2048px square, tee, hoodie and cap front views | The product grid, every Shopify product page, product zoom, and any collection tile that shows a product | Phase 10 — product templates and media | A-01 (P0) |
| **M-02** | **Product back views**, all three products | Product media galleries; back-print garments cannot be shown at all | Phase 10 — product media | A-01 |
| **M-03** | **Product detail views** — fabric, stitching, print texture | The Values row claims "Premium Quality" / "Crafted To Inspire" (prototype markup) with nothing to substantiate them | Phase 10 — product media | A-01 |
| **M-04** | **Model and lifestyle product photography** identifying a garment as a catalogue SKU | Lifestyle sections, collection art, editorial. The hero and story frames show people in garments but nothing identifies those garments as the three SKUs (§5.5) | Phase 10 — product media; collection art (M-09) | A-01 |
| **M-05** | **Mobile hero** — a portrait or art-directed phone source | Phone LCP. The Phase 3 ladder covers the desktop crop only (`phase-3-assets/README.md`), so a phone visitor receives an unmanaged crop of the 16:9 source, which loses about a third of its width, cutting the third model and the back-print message (brief: hard facts) | Phase 10 — hero section | A-06 (P1) |
| **M-06** | **High-resolution story master** — the three-model composition, 2000px+ long edge, no baked text | The Our Story section. The canonical composition is identified (`images/our-story.webp`) but exists only at 535x348 (§6.2) | Phase 10 — Our Story section | A-02, A-03 |
| **M-07** | **Vector logo** (SVG / AI / EPS) | Theme logo setting, favicon, social profile, packaging, print, every size above the raster's ceiling. No vector has been located; layered PSD sources exist outside the project at `C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES` and were never opened, so a vector master may yet exist inside them (brief: hard facts) | Phase 10 — theme logo setting; M-08, M-14, M-16 all depend on this | VECTOR LOGO REQUIRED |
| **M-08** | **Favicon** — no favicon of any kind exists; `/favicon.ico` returns 404 on every load (brief: hard facts) | Browser tab, bookmarks, mobile home-screen icon | Phase 10 — theme setup. Gated on M-07 | — |
| **M-09** | **Collection / editorial banner imagery** — 2400px+, purpose-made | Every collection slot. The manifest has zero COLLECTION rows, and no asset in the project can substitute (§7) | Phase 10 — collection templates. Gated on the collection names (§20) | A-07 (P2) |
| **M-10** | **Feature-icon masters** — crown, community, globe and diamond in a scalable or optimised format | The Brand Values row. All four exist only as 110px-short-edge PNGs that fall to 0.83x at DPR 3 (§12.1). Spec §17 requires their visual character be preserved and forbids redesign, so no SVG was authored in Phase 3 (`phase-3-assets/README.md`) | Phase 10 — values block. **DESIGN DECISION REQUIRED**: faithful trace, or WebP re-encode, or commissioned redraw | A-13 (P2) |
| **M-11** | **Official platform brand marks** for the platforms actually in use | The footer social row. The project holds AI-generated approximations of the Facebook and Instagram marks, not the platforms' own artwork (`phase-3-assets/README.md`) | Phase 10 — footer. Gated on which platforms are active (§20) | A-08 (P2) |
| **M-12** | **Packaging photography** | Unboxing and brand-experience content; the packaging view in the §5.5 variant set | Editorial and marketing work; no phase attributed | A-17 (P3) |
| **M-13** | **Fabric, texture and craft imagery** supporting the Values row | "Premium Quality" and "Crafted To Inspire" as claims the page can support rather than assert (prototype markup) | Phase 10 — values block | A-01, A-17 |
| **M-14** | **Social share and profile assets** — Open Graph image, profile avatar | Link previews in every share of the site; platform profiles | Phase 10 — theme setup. Gated on M-07 | A-08 |
| **M-15** | **Size guide, fabric and care imagery** | Product pages. Nothing of the kind exists in the project | Phase 10 — product templates | A-17 (P3) |
| **M-16** | **Email and profile logo lockups** | Transactional email headers, platform profile images | Sourcing, gated on M-07. `images/logo.png` — a white wordmark on a solid black square, 500x500, ARCHIVE and canonical of DUP-04 — is the nearest candidate, and the manifest already records it as a possible social/profile candidate once a vector exists, under the production name `logo-god-squad-on-black.png` (manifest, `images/logo.png`) | A-17 |
| **M-17** | **Colourway photography** — nine frames, three colours for each of three products | Swatch selection. The prototype declares three swatches per product (`#0d0c0a`, `#f3efe6`, `#4b5443`) and no image changes when one is chosen (§5.1) | Phase 10 — variant wiring. Gated on the colour names (§20) | A-01 |

**Four things are deliberately *not* listed as missing**, to keep this register honest:

- A **desktop hero** is not missing. `images/hero-group.png` exists at 1672x941 and the Phase 3 ladder delivers it at five widths (brief: hero ladder). Its shortfall is retina coverage, recorded in §12.1, not absence.
- The **nine UI icons** are not missing. They were authored in Phase 3 and are KEEP (manifest).
- The **story composition** is not missing — the *composition* is identified. What is missing is a usable-resolution master of it, which is M-06.
- A **product image per SKU** is not missing. A front view exists for all three; it is inadequate, which is M-01, and its status is REPLACE. REPLACE and REMOVE both mean *after approval* — nothing is deleted in this phase, and every original is preserved exactly where it is.

## 20. Assets Requiring Business Approval

None of these is a technical question and none can be answered inside Phase 3. Each needs a named owner decision before the asset it governs can be finalised.

**1. Which logo is official.** Six LOGO-category files exist and they are not the same artwork. `images/WHITE FONT LOGO.png` (500x500, 37,836 B) is the one the page actually uses, in the header at 78px and the footer at 56px. `images/logo.png` (500x500, 47,147 B) is the DUP-04 canonical, unreferenced, and a different file. `white-font-300x300-mu98qi59-mytq.png` is 244x184 at 23,444 B. `white-font-trans-mu98q2ez-zrdd.png` and `white-font-trans-mu98qky0-5tt6.png` are the same byte count (43,606 B) at the same dimensions and differ only in their generator hash - but they are **not** byte-identical: md5 places neither in a duplicate group. The owner must name one file as the official mark. *Decision: which single file is the brand's logo.*

**2. Vector logo.** No SVG, AI or EPS logo has been located anywhere in the project. The wordmark in use is a 500x500 PNG whose transparent padding leaves the visible mark rendering at roughly 66x50 inside a 78px box (brief: hard facts); the manifest additionally records that it "reads half its mockup size" (manifest `images/WHITE FONT LOGO.png`) - a visual judgement, not a measurement. Layered PSD sources exist **outside** the project at `C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES` and have never been opened, so a vector master may already exist. Status: **VECTOR LOGO REQUIRED**. Phase 3 has not recreated it and must not: redrawing a wordmark in a guessed typeface produces a different logo. *Decision: authorise opening the PSD sources, or commission a vector master.*

**3. Which photography is final.** Every product image is a crop of the 1024x1536 mockup - tee 235x230, hoodie 235x235, cap 215x190 - rendering at 288px on desktop and 327-382px on phones (brief: hard facts). The Our Story slot uses `01-hero-model-mu98p88t-7jig.webp`, a 650x480 crop of the mockup **hero** with the headline fragments "A PURPOSE", "K BY" and "TH." baked into the pixels and visible at every width, rendered at 998x520 (manifest `01-hero-model-mu98p88t-7jig.webp`). Status: **HIGH-RES PRODUCT MASTER REQUIRED** and **HIGH-RES STORY MASTER REQUIRED**. No processing fixes either; both are sourcing problems. A crop of the mockup is not a substitute - it is the origin of the defect. The manifest also proposes `story-community.webp` as the production name for **two** different sources (§16), so the owner must say which becomes canonical. *Decision: commission photography, and name the canonical story source.*

**4. Social marks.** `images/icon-facebook.png` (130x130, 36,771 B) and `images/icon-instagram.png` (130x130, 42,319 B) are circled two-tone badges cut from `images/social-sprite.png`, where the mockup shows a plain glyph (manifest `images/icon-facebook.png`), with colour baked into the pixels. Platform marks are trademarks and should come from each platform's official brand kit rather than being traced or redrawn - which is why Phase 3 did not author SVG versions of them. *Decision: approve sourcing the official marks.*

**5. Which social platforms are active.** The project contains Facebook and Instagram only. The manifest records that the mockup also shows TikTok and YouTube (manifest `images/icon-instagram.png`), and both footer links are `href="#"` - no live URL exists for either platform that is present. Phase 3 will not invent an account or display a platform the business does not use. Status: **BUSINESS INFORMATION REQUIRED**. *Decision: the live URL for every active platform, and confirmation that TikTok, YouTube, X, Pinterest, LinkedIn, Spotify, WhatsApp and email are or are not in use.*

**6. Collection naming and imagery.** The prototype shows one collection, "The Faithful". The spec anticipates The Faithful, Shirts, Hoodies, Caps, Collections and Best Sellers. No editorial or collection image exists for any of them, and a product crop must not be promoted into a collection hero. Status: **DOCUMENT AS MISSING** (the imagery) and **BUSINESS INFORMATION REQUIRED** (the collection list and names). *Decision: the final collection names, and whether each gets editorial imagery.*

**7. The sprite sheets.** `images/icons-sprite.png` (2172x724, 833,929 B) and `images/social-sprite.png` (2172x724, 927,973 B) are referenced by nothing, and each has duplicates in `uploads/` (DUP-03, DUP-09). Together the group accounts for 1,761,902 B of source artwork, and the nine individual icon PNGs cut from those sheets - seven UI and feature icons plus the two social marks - are what the page actually loads. Manifest status ARCHIVE: **candidate for removal after final approval, not a deletion**. They are the only source for the feature-icon artwork, so they must survive until item 8 is settled. *Decision: confirm they can be archived once the feature icons are resolved.*

**8. Feature icon treatment.** Crown, community, diamond and globe carry an approved visual character that Phase 3 is forbidden to redesign, so they were deliberately excluded from `phase-3-assets/icons/`. Manifest status: **OPTIMIZE** for crown, community and diamond; **REPLACE** for globe. The choice between a straight WebP conversion, a faithful SVG trace and a redesign is **BUSINESS INFORMATION REQUIRED**. The globe is the sharpest case: one 110x110 raster serves 16px in the announcement bar and 44px in the Brand Values row (manifest `images/icon-globe.png`), which no single raster does well. *Decision: WebP, trace, or redesign - per icon.*

**9. Favicon.** No favicon of any kind exists; `/favicon.ico` returns 404 on every load (brief: hard facts). Status: **DOCUMENT AS MISSING** (the asset) and **BUSINESS INFORMATION REQUIRED** (which mark, and whether it is a cropped monogram or the full wordmark - the full 500x500 wordmark is illegible at 32x32). *Decision: which mark becomes the favicon.*

**10. Product naming and pricing.** The prototype hard-codes "Signature Oversized Tee" at PHP 1,290, "Heavyweight Hoodie" at PHP 2,490 and "Utility Cap" at PHP 890, with a currency property defaulting to PHP and offering USD and EUR. These drive the production filenames (`product-signature-tee-front.webp` and so on), the product handles, and the media filenames baked into CDN URLs. Status: **BUSINESS INFORMATION REQUIRED**. *Decision: final names, final prices, final currency - confirmed before any media is uploaded.*

**11. Provenance and licensing of the AI-generated assets.** The hero, both sprite sheets and the icon set derived from them are AI-generated (brief: hard facts). That covers `images/hero-group.png` and its two duplicates at 1,989,201 B each, both sprite sheets, and the nine icon PNGs cut from them - the single largest block of artwork in the project. Provenance, licensing and commercial-use rights are unverified. Status: **ASSET PROVENANCE SHOULD BE VERIFIED**. Phase 3 has removed nothing and assumes no ownership. *Decision: confirm the generator, its terms, and the right to use these commercially - before launch, not after.*

## 21. Phase 4 Asset Dependencies

Phase 4 is Header and Navigation. It has not started, and Phase 3 does not start it. What follows is the asset-side handoff only.

### What the header consumes today

The header region of the prototype loads five image assets: the logo (`images/WHITE FONT LOGO.png`, 78px desktop / 56px below 900px), search, account and cart (24px each), and the globe in the announcement bar immediately above it (16px). The hamburger is **not** an asset - it is three 22x2 CSS spans, revealed below 900px by `[data-r=nav-menu]{display:flex}`.

Phase 4 turns that into **six glyph dependencies** - logo, search, account, cart, menu and globe - **plus two more**, close and chevron, for the drawer and dropdown states Phase 4 introduces and the prototype does not have. Eight in all, not one.

### Ready now

| Dependency | What is ready | Note |
|---|---|---|
| Search glyph | `phase-3-assets/icons/icon-search.svg`, 293 B | Drawn to the Phase 2 contract: 24x24, stroke 1.5, `currentColor`, no embedded raster, no editor metadata |
| Account glyph | `icon-account.svg`, 309 B | Same |
| Cart glyph | `icon-cart.svg`, 346 B | Same - and it resolves a live defect once Phase 4 adopts it: the raster `images/icon-cart.png` retains a sliver of the sprite sheet's gold badge along its right edge (brief: hard facts). The prototype still loads the PNG and is unchanged |
| Drawer toggle (hamburger) | `icon-menu.svg`, 305 B | Replaces three CSS spans with a real glyph that can carry an accessible label |
| Drawer / modal close | `icon-close.svg`, 287 B | For a state the prototype does not yet have |
| Dropdown affordance | `icon-chevron.svg`, 262 B | For a state the prototype does not yet have |
| Link arrows | `icon-arrow.svg`, 281 B | Used in the two call-to-action buttons |
| Quantity stepper | `icon-plus.svg` 277 B, `icon-minus.svg` 252 B | For the cart drawer |
| Header geometry | Measured: 78px logo above 900px, 56px at and below, 24px UI icons, 26px gap, 22px 48px padding, `position:absolute` over the hero above 900px and `position:relative; order:-2` below | §15 |
| Announcement-bar geometry | 12px 48px, 11px type, globe at 16px; below 520px it stacks to a column at 10px 16px | §15 |
| Hero LCP handling | `phase-3-assets/hero/` ladder plus the `image_url` -> `image_tag` pattern in §15 | The header sits over the LCP element, so Phase 4 must not introduce an entrance animation that delays it |

### Not ready

| Dependency | Blocked by | Consequence for Phase 4 |
|---|---|---|
| Header logo | **VECTOR LOGO REQUIRED** (§20 item 2). The mark in use is a 500x500 PNG whose transparent padding leaves the visible glyph at about 66x50 inside a 78px box, and about 47x36 inside the 56px mobile box | Phase 4 can build the header with the existing PNG through `settings.logo`, but must not treat the current 78px/56px values as final: they were chosen to compensate for padding, and a trimmed vector will need different numbers |
| Globe | **Feature-icon decision** (§20 item 8). Manifest status REPLACE. One 110x110 raster serves 16px and 44px | Phase 4 can ship the raster at 16px, where the mismatch is least visible |
| Favicon | **DOCUMENT AS MISSING** (§20 item 9). `/favicon.ico` returns 404 on every load | `settings.favicon` stays empty. A one-line gap, but it is a Phase 4 surface |
| Social marks | **Official brand kits required** (§20 item 4), and no live URL for any platform (§20 item 5) | Footer social row, not the header. Does not block Phase 4 |
| Mobile hero | **DOCUMENT AS MISSING** (§20 item 3, RA-03) | The header sits over the hero. Phase 4 should not tune mobile header contrast against a crop that will be replaced |

### What Phase 4 can proceed without

Product photography, story photography, collection imagery, the sprite decision and the AI provenance review. None touches the header. Phase 4 is gated on the **logo** and nothing else - and even that only for final sizing, not for construction.

### Handoff conditions

Phase 4 may start when: the eight header glyphs (search, account, cart, menu, close, chevron, plus logo and globe) have a named source, six of them inlined from `phase-3-assets/icons/` and two still raster; the header and announcement-bar geometry in §15 is treated as measured fact; and the owner has acknowledged that logo sizing is provisional pending §20 item 2.

---

## Asset-related performance risk register

Severity is scored on the spec's areas of particular attention: large PNGs, oversized sprites, duplicate assets, low-resolution product images, unnecessary images, incorrect formats, a missing mobile hero and excessive image count. Every mitigation is a recommendation. Phase 3 implemented none of them and the website is functionally unchanged.

| ID | Pri | Risk | Impact | Mitigation |
|---|---|---|---|---|
| RA-01 | P0 | `images/hero-group.png` ships as a 1,989,201 B PNG and is the LCP element at every width | LCP catastrophically slow on mobile data; the PNG is RGB with no alpha, so the format buys nothing | Pipe the drop through `image_url: width: 1672` and then through `image_tag` with `widths: '420, 640, 960, 1280, 1672'`, `sizes: '(min-width: 1440px) 1440px, 100vw'`, `loading: 'eager'` and `fetchpriority: 'high'`. The 1672w rung measures 119,850 B locally, 94.0% smaller than the PNG (brief: hero ladder); delivered bytes are whatever the CDN emits from the uploaded master. Prefer uploading the PNG master or a near-lossless WebP so the CDN compresses once, not twice |
| RA-02 | P0 | Product masters are 235x230, 235x235 and 215x190 mockup crops rendered at 288px desktop and 327-382px phone | About a 2.8x device-pixel upscale on the tee at the narrow end (manifest `images/product-tee.webp`), rising to roughly 3.5x on the 215px-wide cap at 382 CSS px (manifest `images/product-cap.webp`). Visible softness on the only commerce imagery | HIGH-RES PRODUCT MASTER REQUIRED. Do not upscale and do not add ladder rungs above 235 - the CDN will not upscale and the descriptors would be dead |
| RA-03 | P0 | No mobile hero exists | The 16:9 frame cropped to a 375x320 phone band discards about a third of its width, cutting the third model and the back-print message (brief: hard facts) | Commission an art-directed portrait source and deliver it through a `<picture>` with `<source media="(max-width: 900px)">`, per §15. Not solvable with rungs |
| RA-04 | P1 | Two 2172x724 sprite sheets, 833,929 B and 927,973 B, referenced by nothing, each with duplicates in `uploads/` | 1,761,902 B of source artwork carried through every clone and backup for no delivery benefit | ARCHIVE after §20 item 8 is settled - candidate for removal after final approval, never a deletion. They are the only source for the feature-icon artwork |
| RA-05 | P1 | Three raster icon PNGs at 85,933 B where 948 B of drawn SVG will do | Three extra HTTP requests above the fold, and raster glyphs that cannot inherit surface colour or scale cleanly | Adopt `icon-search.svg`, `icon-account.svg` and `icon-cart.svg` from `phase-3-assets/icons/` in Phase 4, inlined via `snippets/icon-*.liquid`. A 98.9% reduction on those three |
| RA-06 | P1 | The Our Story slot uses the wrong asset: a 650x480 crop of the mockup **hero** with headline fragments baked into the pixels, rendered at 998x520 | A 1.53x upscale plus visible stray typography on a primary brand section (manifest `01-hero-model-mu98p88t-7jig.webp`) | Source a high-resolution story master. Status HIGH-RES STORY MASTER REQUIRED. A crop of the 1024x1536 mockup is not a substitute - it is the source of the present defect - and the mockup remains REFERENCE ONLY |
| RA-07 | P1 | No vector logo; the header mark is a 500x500 PNG whose transparent padding leaves the visible glyph at about 66x50 | The brand's primary identifier is raster-only and cannot be scaled, trimmed or recoloured for favicon, social or print | VECTOR LOGO REQUIRED. Open the PSD sources outside the project before commissioning new work (§20 item 2) |
| RA-08 | P2 | 9 duplicate groups by md5 cover 20 files - 11 redundant copies | Wasted storage, and a real risk of editing a copy that is not the canonical file | Archive the non-canonical members after approval. Canonicals are recorded per group in the manifest |
| RA-09 | P2 | 222,588 B of feature and social icon PNGs remain unreplaced - crown, community, diamond, globe, facebook, instagram | Six raster requests below the fold with colour baked in, unable to follow surface colour | Blocked on §20 items 4 and 8 by design: Phase 3 is forbidden to redesign approved feature icons or to trace trademarked platform marks |
| RA-10 | P2 | No favicon; `/favicon.ico` returns 404 on every page load | A 404 on every load, a blank tab icon, a blank bookmark | DOCUMENT AS MISSING. Blocked on §20 item 9 - which mark, at 32x32 legibility |
| RA-11 | P2 | `images/icon-globe.png`, one 110x110 raster, serves 16px in the announcement bar and 44px in the Brand Values row | Soft at 44px, wastefully large at 16px, and gold baked into the pixels so it cannot follow the surface (manifest `images/icon-globe.png`) | Two renditions or one vector. Blocked on §20 item 8 |
| RA-12 | P2 | 3,878,503 B of reference screenshots in `uploads/`, plus a 1,872,888 B mockup PNG and its 182,250 B WebP derivative | Reference material sits beside production assets with nothing marking the difference; a screenshot could be shipped by mistake | Segregate into `assets/reference/`, all REFERENCE ONLY. Spec item 20 is explicit: a mockup must never become a production image |
| RA-13 | P3 | The homepage loads 15 distinct images totalling 2,406,866 B, of which 308,521 B is icon PNGs | Request count and byte weight both higher than a page of this complexity needs | Inlining the three UI SVGs removes three requests; the hero ladder removes the great majority of the bytes |
| RA-14 | P3 | `.thumbnail` (25,542 B, unreferenced) and `support.js` (69,150 B, loaded by the prototype in its document head) are carried in the tree | Non-production files in a handoff package | Both are status REMOVE - **candidate for removal after final approval**. `support.js` must not be removed until the Shopify build supplies its behaviour; removing it from the prototype would change the website, which Phase 3 forbids |
| RA-15 | P3 | The hero, both sprite sheets and the icon set cut from them are AI-generated with unverified provenance and licensing | Commercial-use rights over the largest block of artwork in the project are unestablished | ASSET PROVENANCE SHOULD BE VERIFIED before launch. Nothing removed, no ownership assumed (§20 item 11) |

## Appendix A. Asset performance risk register

Asset-related risks only. The four drafting clusters raised 52 entries describing roughly 25 distinct risks, each scoring severity on its own reading; they are consolidated and rescored here against one definition so the register does not inflate against Phase 1, which reserved P0 for three architecture blockers.

**P0** — cannot launch without resolving, and no workaround exists inside the project, because the fix requires external sourcing or a business decision. Every P0 here is a sourcing or licensing gap, not a defect in the work.  
**P1** — a major problem with a known fix, or a visible defect shipping today.  
**P2** — an important improvement.  
**P3** — polish.

| ID | Priority | Risk | Impact | Mitigation | Owning phase |
|---|---|---|---|---|---|
| AR-01 | P0 | No production-grade product photography exists. All three product images are crops of the 1024x1536 mockup: tee 235x230, hoodie 235x235, cap 215x190. | Product media is soft at every render size, about 2.8x device-pixel upscale on a 2x phone. Re-encoding cannot create pixels that were never captured. | Commission or supply original product photography at 2000px or more on the long edge, square, consistent lighting and background. | PHASE 3 sourcing, consumed by PHASE 6 and PHASE 8 |
| AR-02 | P0 | No Our Story master exists. The intended three-model composition is 535x348 and the slot renders about 1000px wide. | Phase 7 cannot be completed at production quality from anything in the project. | Supply an Our Story photograph at 2000px or more on the long edge. | PHASE 3 sourcing, consumed by PHASE 7 |
| AR-03 | P0 | No vector logo in SVG, AI or EPS form has been located. The wordmark in use is a 500x500 PNG whose transparent padding leaves the visible mark at about 66x50. | The header mark renders around half its mockup size and cannot scale cleanly. Favicon and social profile assets cannot be derived properly. | Supply a vector master, or authorise extraction from the unopened Desktop PSD sources. | PHASE 3 sourcing, consumed by PHASE 4 |
| AR-04 | P0 | No mobile hero source exists. The 1.777:1 desktop frame cropped into a phone band discards about a third of its width. | The phone hero loses the third model and the back-print message, which is the content the hero exists to carry, while still paying for a wide image. | Supply a portrait or art-directed phone crop, or a separate mobile frame. | PHASE 3 sourcing, consumed by PHASE 5 and PHASE 9 |
| AR-05 | P0 | The hero, both sprite sheets and the nine icon PNGs cut from them are AI-generated. Neither generation history nor licensing has been established. | Ownership and licensing of the most prominent brand imagery are unverified before a commercial launch. | ASSET PROVENANCE SHOULD BE VERIFIED. Confirm generation terms and commercial rights, or replace with owned photography. | BUSINESS DECISION, before launch |
| AR-06 | P1 | The live LCP image is a 1,989,201-byte PNG served unchanged at every viewport, with no srcset, sizes, intrinsic dimensions or fetch priority. | Largest Contentful Paint is dominated by a two-megabyte transfer on every first load, worst on mobile data. | A verified WebP ladder already exists in phase-3-assets/hero at 94% smaller. Wire it in at Phase 10 with explicit widths and sizes. | PHASE 10, measured in PHASE 12 |
| AR-07 | P1 | The Our Story slot loads the wrong asset: a 650x480 crop of the mockup hero with the headline fragments A PURPOSE, K BY and TH. baked into the pixels. | Another section typography shows inside the story image at every width, and CSS cannot suppress it because it is pixels, not text. | Replace the reference when the story master lands. Until then it is a known visible defect. | PHASE 7 |
| AR-08 | P1 | The Facebook and Instagram marks in the project were cut from an AI-generated sprite sheet rather than taken from each platform official brand kit. | Platform logos are trademarks with published usage rules. Approximations risk both visual incorrectness and trademark non-compliance. | Take each mark from the platform own brand resources. Do not trace or redraw. | PHASE 3 sourcing, consumed by PHASE 4 |
| AR-09 | P1 | The nine raster UI and feature icons total 308,521 bytes with colour baked into the pixels at 110 to 150px canvases drawn at 16 to 44px. | Icons cannot inherit colour, respond to hover or focus, or serve two sizes cleanly, and they carry weight out of proportion to their display size. | Nine drawn SVGs now exist at 2,612 bytes total, a 99.2% reduction. Adopt at Phase 4 and Phase 10. | PHASE 4 and PHASE 10 |
| AR-10 | P1 | No favicon of any kind exists; /favicon.ico returns 404 on every load. | A failed request on every page view and no brand mark in the browser tab, bookmarks or search results. | Derive a favicon set once a vector logo exists. Blocked by AR-03. | PHASE 13 |
| AR-11 | P1 | The four feature icons (crown, community, globe, diamond) have no resolved format decision. The spec requires their visual character be preserved and forbids redesign. | They cannot be replaced by the drawn set without changing approved brand artwork, yet they remain low-resolution rasters with gold baked in. | DESIGN DECISION REQUIRED: keep as optimised raster, or commission a faithful vector trace. | BUSINESS DECISION, consumed by PHASE 4 |
| AR-12 | P2 | Nine md5 duplicate groups cover 20 files, leaving 11 redundant copies worth 6,733,692 bytes, 39.4% of all image bytes. | Every future edit risks being applied to a stale copy, and the working tree is inflated. | After approval, keep the canonical named in the manifest and archive the rest. Nothing is deleted in Phase 3. | PHASE 3 approval, then PHASE 10 |
| AR-13 | P2 | Two 2172x724 AI-generated sprite sheets totalling 1,761,902 bytes, plus three byte-identical copies, are referenced by nothing. | Dead weight and a licensing-unsafe source for the platform marks cut from them. | Superseded by the SVG set. Archive after approval; retained for now. | PHASE 3 approval |
| AR-14 | P2 | images/icon-globe.png is one 110x110 raster used twice, at 16px in the announcement bar and 44px in the values row. | One raster cannot be optically correct at both sizes; it is over-detailed at 16px and under-resolved at 44px. | Resolve with the feature-icon decision in AR-11. | PHASE 4 |
| AR-15 | P2 | images/icon-cart.png retains a sliver of the sprite sheet gold badge along its right edge. | A visible artefact of a neighbouring icon ships inside a header control. | Superseded by the drawn icon-cart.svg. | PHASE 4 |
| AR-16 | P2 | images/product-cap.webp is 215x190, the only non-square product source, inside a 1:1 tile with object-fit cover. | The cap is edge-cropped where the other two products are not, so the row is visually inconsistent. | Shoot or crop all products square to the standard in section 5. | PHASE 6 |
| AR-17 | P2 | No purpose-made collection imagery exists. COLLECTION is a permitted category with zero assets. | Collection pages and any Best Sellers row have no editorial imagery, and product images are not a substitute. | Commission collection or editorial photography, or design collection cards that do not require it. | PHASE 6 |
| AR-18 | P2 | No social account is confirmed for any platform. The build shows two marks, the mockup showed four, and the sprite sheet contains ten. | The footer cannot be completed without knowing which channels exist and their URLs. | BUSINESS INFORMATION REQUIRED: confirm live channels and profile URLs. | BUSINESS DECISION, consumed by PHASE 4 |
| AR-19 | P2 | Two misconceptions about Shopify image delivery would waste effort if carried forward: that the CDN outputs AVIF, and that image_url alone emits srcset. | Incorrect delivery code and an unachievable format expectation. | The CDN serves WebP automatically and does not output AVIF. Pass explicit widths and sizes and render with image_tag; never hand-build CDN URLs. | PHASE 10 and PHASE 12 |
| AR-20 | P2 | 3,878,503 bytes of editor reference screenshots sit in uploads/, 22.7% of all image bytes, and their content is undocumented beyond this phase. | They are valuable as the record of owner decisions but are easily mistaken for production assets. | Classified REFERENCE ONLY. Move to a reference folder after approval. | PHASE 3 approval |
| AR-21 | P3 | Two files carry REMOVE and both remain in place: .thumbnail and support.js. | Minor dead weight. Removing support.js would change the page, so it is out of scope for an asset phase. | Retire .thumbnail after approval and support.js when the theme replaces the prototype. | PHASE 10 |
| AR-22 | P3 | Exactly one source was compressed, at one quality, verified by eye rather than by a difference metric. | No quality ladder exists to compare against, so the q82 choice is defensible but not optimised. | When real photography arrives, encode two or three qualities and compare before fixing a project default. | PHASE 12 |
| AR-23 | P3 | Two file pairs share identical dimensions and byte counts but different md5 hashes, the signature of a separate re-encode rather than a copy. | A hash-only duplicate check reports them as distinct, so a later clean-up may keep both. | Documented in section 11 as format or encode variants rather than exact duplicates. | PHASE 3 approval |
| AR-24 | P3 | No size guide, fabric, care, packaging or craft imagery exists anywhere in the project. | Product pages will have no supporting imagery beyond a single front view per item. | Add to the photography brief alongside the product masters in AR-01. | PHASE 8 |
| AR-25 | P3 | The homepage loads 15 distinct images totalling 2,406,866 bytes, of which 308,521 is icon PNGs drawn at 16 to 44px. | Payload is dominated by assets that could be a few kilobytes of inline SVG. | Adopt the SVG set and the hero ladder; both already exist. | PHASE 10 and PHASE 12 |

## Appendix B. Missing and required assets

Listed only where the project genuinely lacks the asset. Nothing here is invented, and no view has been assumed to exist.

- Vector logo master (SVG/AI/EPS). No vector logo exists anywhere in the project; the identity rests on a 500x500 raster whose transparent padding makes the visible mark render about 66x50. VECTOR LOGO REQUIRED. Check the unopened PSD sources outside the project before commissioning.
- Inverse Logo. Only a white wordmark exists; there is no dark-ink version for cream surfaces, paper, packaging or light garments. DOCUMENT AS MISSING.
- Favicon. No favicon of any kind exists and /favicon.ico returns 404 on every load. `images/logo.png` is the candidate source once a vector master exists.
- Social profile assets. No square profile-ready export exists; `images/logo.png` is a candidate but a wordmark loses its corners inside a circular avatar crop and needs re-laying out. DOCUMENT AS MISSING.
- Primary mobile hero. No mobile-specific hero source exists. The 1.777:1 desktop frame cropped into the phone band (about 375x320) discards roughly 34% of its width, cutting the third model and the back-print message. DOCUMENT AS MISSING.
- High-resolution product masters for the tee, hoodie and cap. The existing files are 235x230, 235x235 and 215x190 crops of the 1024x1536 mockup, rendered at 288px desktop and 327-382px on phones. HIGH-RES PRODUCT MASTER REQUIRED. Do not upscale and treat as originals.
- Product views other than front — back, detail, lifestyle, model and packaging — for all three products. None exists in the project. DOCUMENT AS MISSING; not fabricated.
- High-resolution story master. The referenced Our Story image is a 650x480 crop of the mockup hero with headline fragments baked into the pixels; the intended three-model composition is 535x348 and unreferenced. Both are far too small for a slot rendering about 1000px wide. HIGH-RES STORY MASTER REQUIRED.
- Collection imagery for The Faithful, Shirts, Hoodies, Caps, Collections and Best Sellers. The COLLECTION category holds zero assets, and no product image should be promoted to a collection hero unless it was designed for it.
- Background textures. The BACKGROUND category holds zero assets; the project has no background or surface texture of any kind.
- Official platform brand-kit marks for whichever social platforms the business confirms. The two present marks were cut from a generated sprite sheet, which is not a licensing-safe source for trademarks.
- Note, not a commitment: BRAND holds zero assets in the manifest. What the BRAND category is intended to hold — brand marks separate from LOGO, or lifestyle and editorial photography — is not fixed by the spec, so confirm the intended scope before a missing-asset commitment is made against it. BUSINESS INFORMATION REQUIRED.
- M-01 High-resolution product masters, 2048px square, front views of tee, hoodie and cap. Depends: product grid, every Shopify product page, zoom, product tiles in collections. Blocks: Phase 10 product templates and media. Evidence: all three are 215-235px mockup crops, HIGH-RES PRODUCT MASTER REQUIRED (manifest, all three PRODUCT rows).
- M-02 Product back views, all three products. Depends: product media galleries; back-print garments cannot be shown. Blocks: Phase 10 product media. DOCUMENT AS MISSING (§5.5).
- M-03 Product detail views — fabric, stitching, print texture. Depends: substantiating the Values row's "Premium Quality" / "Crafted To Inspire" (prototype markup). Blocks: Phase 10 product media. DOCUMENT AS MISSING.
- M-04 Model and lifestyle product photography identifying a garment as a catalogue SKU. Depends: lifestyle sections, collection art, editorial. The hero and story frames show people in garments but nothing identifies those garments as the three SKUs, and those files are categorised HERO and STORY, not PRODUCT (manifest). DOCUMENT AS MISSING.
- M-05 Mobile hero — a portrait or art-directed phone source. Depends: phone LCP. The Phase 3 ladder covers the desktop crop only (phase-3-assets/README.md), so a phone visitor receives an unmanaged crop of the 16:9 source, which loses about a third of its width, cutting the third model and the back-print message (brief: hard facts). Blocks: Phase 10 hero section.
- M-06 High-resolution story master — the three-model composition, 2000px+ long edge, no baked text. Depends: the Our Story section. The canonical composition is identified (images/our-story.webp) but exists only at 535x348. Blocks: Phase 10 Our Story section. HIGH-RES STORY MASTER REQUIRED (manifest).
- M-07 Vector logo (SVG/AI/EPS). Depends: theme logo setting, favicon, social profile, packaging, print. No vector located; layered PSD sources exist outside the project at C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES and were never opened, so a vector master may yet exist inside them (brief: hard facts). Blocks: Phase 10 theme logo setting, and M-08, M-14, M-16. VECTOR LOGO REQUIRED.
- M-08 Favicon. No favicon of any kind exists; /favicon.ico returns 404 on every load (brief: hard facts). Depends: browser tab, bookmarks, mobile home-screen icon. Blocks: Phase 10 theme setup. Gated on M-07.
- M-09 Collection / editorial banner imagery, 2400px+ and purpose-made. Depends: every collection slot. The manifest has zero COLLECTION rows and no asset in the project can substitute (§7). Blocks: Phase 10 collection templates. Gated on the collection names.
- M-10 Feature-icon masters — crown, community, globe, diamond — in a scalable or optimised format. All four exist only as 110px-short-edge PNGs that fall to 0.83x at DPR 3. Spec §17 requires their character be preserved and forbids redesign, so none was authored in Phase 3 (phase-3-assets/README.md). Blocks: Phase 10 values block. DESIGN DECISION REQUIRED.
- M-11 Official platform brand marks for the platforms actually in use. The project holds AI-generated approximations of the Facebook and Instagram marks, not the platforms' own artwork (phase-3-assets/README.md). Blocks: Phase 10 footer. Gated on which platforms are active. BUSINESS INFORMATION REQUIRED.
- M-12 Packaging photography. Depends: unboxing and brand-experience content, and the packaging view in the §5.5 variant set. No phase attributed; blocks editorial and marketing work. DOCUMENT AS MISSING.
- M-13 Fabric, texture and craft imagery supporting the Values row. Depends: "Premium Quality" and "Crafted To Inspire" being claims the page can support rather than assert (prototype markup). Blocks: Phase 10 values block.
- M-14 Social share and profile assets — Open Graph image and profile avatar. Depends: link previews in every share of the site, and platform profiles. Blocks: Phase 10 theme setup. Gated on M-07.
- M-15 Size guide, fabric and care imagery. Depends: product pages. Nothing of the kind exists in the project. Blocks: Phase 10 product templates.
- M-16 Email and profile logo lockups. Depends: transactional email headers and platform profile images. images/logo.png — a white wordmark on a solid black square, 500x500, ARCHIVE and canonical of DUP-04 — is the nearest candidate, and the manifest already records it as a possible social/profile candidate once a vector exists, under the production name logo-god-squad-on-black.png (manifest, images/logo.png). Gated on M-07.
- M-17 Colourway photography — nine frames, three colours for each of three products. The prototype declares three swatches per product (#0d0c0a, #f3efe6, #4b5443) and no image changes when one is selected. Blocks: Phase 10 variant wiring. Gated on the colour names.
- Vector masters for the four feature icons — crown, community, globe and diamond. A commissioned faithful trace that preserves their existing visual character (spec section 17 forbids redesign). The globe is the urgent case: one 110x110 raster currently serves both a 16px announcement-bar use and a 44px value-tile use, a 2.75x range no single raster covers well (section 8.5, risk P3-ICON-03).
- Official brand-kit SVGs for every platform the business confirms. DOCUMENT AS MISSING for TikTok, YouTube, X, Pinterest, LinkedIn, Spotify, Email and WhatsApp — no file for any of them exists in the project. Facebook and Instagram artwork exists but is not usable: both marks were cut from an AI-generated sheet the manifest records as not a licensing-safe source for platform trademarks, so both require brand-kit replacements too (section 9).
- A licence and provenance record for the AI-generated assets — images/hero-group.png, images/icons-sprite.png, images/social-sprite.png and the nine raster icons cut from the icon sheet. Provenance and licensing are unverified (brief). ASSET PROVENANCE SHOULD BE VERIFIED.
- A numerically verified WebP quality floor. Phase 3 encoded exactly one source at one quality (0.82) and verified it by eye at full frame and at 1:1 on face, garment and sky-gradient detail. No lower quality was encoded, so no measured artefact threshold exists for this imagery. A structural-similarity or perceptual metric with a stated pass threshold is required before encoding a storefront's worth of assets (section 14.2, risk P3-CMP-01).
- A pixel or perceptual diff resolving the two near-duplicate pairs that md5 cannot see: images/hero-model.webp against 01-hero-model-mu98p88t-7jig.webp (both 650x480, both 39,966 bytes, different hashes), and white-font-trans-mu98q2ez-zrdd.png against white-font-trans-mu98qky0-5tt6.png (both 500x500, both 43,606 bytes, different hashes). Neither pair may be archived as redundant until this is done (section 11.3, risk P3-DUP-NEAR-01).
- Mobile hero. No phone-specific hero source exists. The 16:9 desktop frame cropped into the 375x320 phone band discards about a third of its width, cutting the third model and the back-print message (brief: hard facts). DOCUMENT AS MISSING - an art-direction gap that no width ladder can close; it needs a second source consumed by `<source media="(max-width: 900px)">`.
- Vector logo (SVG/AI/EPS). None located anywhere in the project. VECTOR LOGO REQUIRED. PSD sources exist outside the project and have never been opened.
- Favicon. No favicon of any kind exists; /favicon.ico returns 404 on every load. DOCUMENT AS MISSING (asset); BUSINESS INFORMATION REQUIRED (which mark). Destination is the theme setting settings.favicon.
- High-resolution product masters for all three products. Present sources are 235x230, 235x235 and 215x190 mockup crops rendered at 288-382px. HIGH-RES PRODUCT MASTER REQUIRED. Until they land, the product srcset must stay capped at width 235 - larger descriptors would be dead, because the CDN does not upscale.
- Product views other than front: back, detail, lifestyle, model and packaging. None exists for any of the three products (manifest images/product-tee.webp, images/product-hoodie.webp). DOCUMENT AS MISSING - Phase 3 does not fabricate a view that does not exist.
- High-resolution Our Story master. The slot renders 998x520 from a 650x480 crop of the mockup hero with headline fragments baked in; the intended three-model crop images/our-story.webp is 535x348 and unreferenced. HIGH-RES STORY MASTER REQUIRED.
- Collection and editorial imagery for The Faithful and any other collection. None exists. DOCUMENT AS MISSING (asset); BUSINESS INFORMATION REQUIRED (which collections). A product crop must not serve as a collection hero.
- Social profile assets - square avatar and open-graph share image. None exists in any size. DOCUMENT AS MISSING; dependent on the vector logo decision.
- A larger hero master for 2x desktop. At the 1440px page cap on a 2x display the browser wants roughly 2880 device pixels; the master tops out at 1672, so desktop retina is served at about 0.58x. Not a defect in the ladder - a ceiling in the source.

## Appendix C. Assets requiring business approval

Decisions Phase 3 could not take on the business's behalf.

- Confirm which logo file is the official primary mark. `images/WHITE FONT LOGO.png` is the one the page loads, but five other logo files sit unreferenced in the project, including two 500x500 exports that are the same byte size with different hashes. Phase 3 does not decide this on the business's behalf.
- Authorise the search of the layered PSD sources at `C:\\Users\\TEST\\OneDrive\\Desktop\\GODSQUAD\\PSD FILES` for an existing vector master before any vector logo is commissioned. They sit outside the project and were not opened during Phase 3. VECTOR LOGO REQUIRED stands until that check is done.
- Approve the disposition of the twelve ARCHIVE files after final sign-off. They are not one set. Six are byte-identical duplicates (`chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png`, `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png`, `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png`, `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png`, `uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png`, `uploads/God-Squad-Images/06-logo.png`); three are DUP canonicals that are themselves unreferenced (`images/icons-sprite.png`, `images/social-sprite.png`, `images/logo.png`); three are non-duplicate unreferenced logo exports (`white-font-trans-mu98q2ez-zrdd.png`, `white-font-trans-mu98qky0-5tt6.png`, `white-font-300x300-mu98qi59-mytq.png`). Together 8,541,085 bytes. Nothing is deleted; ARCHIVE means move to an archive location after approval.
- Note separately that five of the eleven redundant duplicate copies carry REFERENCE ONLY, not ARCHIVE, and are not covered by the item above: `uploads/God-Squad-Images/01-hero-model.webp`, `05-our-story-models.webp`, `02-product-oversized-tee.webp`, `03-product-heavyweight-hoodie.webp` and `04-product-utility-cap.webp`. They stay where they are unless the business decides otherwise.
- Decide the feature-icon question, which the manifest splits two ways. Crown, community and diamond (OPTIMIZE, recommended format WebP, `icon-*.webp`): convert to WebP preserving the approved visual character as-is, or commission faithful vector traces. Globe (REPLACE, recommended format SVG, `icon-globe.svg`): the manifest already recommends a vector because one 110x110 raster currently serves both a 16px and a 44px slot; confirm a faithful trace is commissioned rather than a redesign. DESIGN DECISION REQUIRED (manifest, `images/icon-crown.png`).
- Confirm which social platforms the business actually operates, and supply the live URLs. The project holds Facebook and Instagram marks only; the mockup also shows TikTok and YouTube. No account is assumed and none is invented. BUSINESS INFORMATION REQUIRED (manifest, `images/icon-instagram.png`).
- Establish and document the generation provenance and licensing terms of the AI-generated assets — the hero frame, both sprite sheets and the icon set — before launch. ASSET PROVENANCE SHOULD BE VERIFIED (manifest, `images/hero-group.png`).
- Identify the four REFERENCE-category pasted images (three at 1920x1009, one at 118x77, 3,878,503 bytes, 22.7% of all image bytes). Whether they record owner decisions is not established in the manifest, and they cannot be treated as decision evidence until it is. BUSINESS INFORMATION REQUIRED.
- Confirm the intended scope of the BRAND category, which holds zero assets. The spec's recommended `brand/` folder sits alongside `editorial/`, and the project's six brand marks are already categorised LOGO, so whether BRAND means brand marks or a lifestyle and editorial photography library is not fixed. BUSINESS INFORMATION REQUIRED.
- Approve commissioning high-resolution product masters and a high-resolution story master. Every product and story asset in the project is a crop of the 1024x1536 mockup and cannot be fixed by processing. This is the largest cost item in the asset system and it gates Phase 6 and Phase 8.
- Approve commissioning a dedicated mobile hero. Confirm the shape (4:5 or 1:1) and that the back-print message must remain inside the phone crop; the current desktop frame loses it along with the third model.
- Confirm whether an inverse (dark-ink) logo is wanted. Three of the eight documented logo contexts — product photography, packaging and marketing on light surfaces — require one, and none exists.
- Confirm the final product prices and the display currency. The prototype's product array carries 1,290 / 2,490 / 890 behind a runtime currency variable (`const cur = this.props.currency ?? '₱'`, prototype markup lines 175-177), so neither the amounts nor the currency is established, and nothing in the project establishes the price tier the photography standard in §5.3 should serve. Spec §38 lists final prices as a business decision.
- Confirm which product names are final — the prototype uses "Signature Oversized Tee", "Heavyweight Hoodie" and "Utility Cap". Every recommended production name in the manifest is derived from these handles (`product-signature-tee-front.webp`, `product-heavyweight-hoodie-front.webp`, `product-utility-cap-front.webp`), so a name change invalidates the naming convention's worked examples (§5.4).
- Confirm the colourway names for the three swatches each product carries. The prototype declares bare hexes (`#0d0c0a`, `#f3efe6`, `#4b5443`) with no names, so the colour segment of `product-[handle]-[view]-[colour].webp` cannot be filled in, and the nine colourway frames at M-17 cannot be specified or briefed.
- Confirm which collection names are final and whether "The Faithful" is a collection or a drop name. It appears in the prototype only as the New Drop section heading over a three-product grid. Nothing can be commissioned against M-09 until the collection set is fixed (spec §38).
- Confirm the desktop/mobile traffic split from analytics. It sets the priority of M-05, the missing mobile hero. No analytics, traffic data or device split exists anywhere in the brief, the manifest, the README or the prototype, so the priority assigned to A-06 is based on the measured crop loss alone.
- Confirm which social platforms the business actually uses. The project holds marks for Facebook and Instagram only, and spec §18 forbids inventing accounts or displaying platforms the business does not use. This gates M-11 and M-14.
- Confirm whether the approved design master `uploads/GODSQUAD WEBSITE MOCKUP.png` may be used as a source for full-quality pixel extraction. The manifest records it as the source every product and story crop was cut from and as never usable as a production website image; taking better pixels from it is a different decision from using it directly.
- Confirm provenance, licensing and ownership of the AI-generated assets — the hero, the two sprite sheets and the icon set (brief: hard facts). Spec §21 forbids assuming licensing or ownership. This carries commercial risk into every phase that ships them. ASSET PROVENANCE SHOULD BE VERIFIED.
- Confirm that the three-model composition in `images/our-story.webp` is the approved Our Story image, before a high-resolution master of it is commissioned at M-06. §6.2 identifies it as canonical on the evidence of the mockup's intent, not on a business decision.
- Confirm that model releases exist for the people depicted in the hero and story frames, and whether the same people are to appear in the replacement story shoot commissioned at M-06.
- Decide the feature-icon treatment for crown, community, globe and diamond (M-10): faithful trace to SVG, WebP re-encode at current resolution, or a commissioned redraw. Spec §17 requires their visual character be preserved and forbids redesign, so Phase 3 did not author replacements. DESIGN DECISION REQUIRED.
- Confirm the product photography background for the whole catalogue before the shoot at M-01. The prototype paints the tile `#ebe6dc`, so a cream sweep, a white sweep and a knocked-out alpha each produce a visibly different grid, and the choice must be made once for all three products and every product added later.
- Confirm which social platforms God Squad actually operates. Nothing in the project answers this: the build shows two marks, the approved mockup shows four, and images/social-sprite.png carries ten, none of which proves an account exists. The two footer anchors are image-only and go nowhere (Phase 1: six of nine links are href="#"; the two social anchors are prototype lines 160-161). Until the network set is confirmed the footer social row cannot be built (section 9.4, risk P3-SOC-02). BUSINESS INFORMATION REQUIRED.
- Confirm the live Facebook and Instagram URLs, and confirm whether the TikTok and YouTube channels shown in the approved mockup exist (manifest, icon-facebook.png and icon-instagram.png). Also confirm whether X, Pinterest, LinkedIn, Spotify, Email or WhatsApp is a channel the business wants in the footer; all six are MISSING as artwork and BUSINESS INFORMATION REQUIRED as channels. No account is assumed or invented for any platform.
- Approve sourcing every platform mark from that platform's own official brand kit as unmodified SVG, and approve replacing images/icon-facebook.png and images/icon-instagram.png rather than optimising them. Both were cut from images/social-sprite.png, which the manifest records as not a licensing-safe source for platform trademarks, and both are circled two-tone badges where the approved mockup shows a plain glyph (section 9.3, risk P3-SOC-01).
- Approve the feature-icon direction as a DESIGN DECISION REQUIRED item: convert crown, community and diamond to WebP as an interim to stop paying 107,873 bytes for three 44px marks (manifest: OPTIMIZE, recommended format WebP), and commission a faithful vector trace of all four including the globe, which is REPLACE rather than OPTIMIZE because one raster cannot serve both 16px and 44px (section 8.4). Spec section 17 forbids redesign, so the trace must preserve their existing visual character and is a commissioned design task, not a conversion.
- Confirm that the crown, community, globe and diamond are approved brand assets whose visual character must be preserved, rather than placeholder artwork that may be redrawn. The entire feature-icon recommendation in section 8.4 depends on this answer.
- Approve retiring the three UI icon rasters (icon-account.png, icon-cart.png, icon-search.png, 85,933 bytes) in favour of the nine authored SVGs in phase-3-assets/icons/ (948 bytes for the like-for-like three). The SVGs were drawn to the Phase 2 contract, not traced, and they resolve two defects the rasters cannot: colour is baked in so they cannot inherit currentColor or respond to hover, and icon-cart.png retains a sliver of the sprite sheet's gold badge along its right edge (Phase 1 ICON-02; risk P3-ICON-04). Nothing is wired in Phase 3 — the website is functionally unchanged.
- Approve RECOMMEND REPLACEMENT for both sprite sheets: individual inline SVG icons supersede images/icons-sprite.png and images/social-sprite.png (section 10.5). The two canonical sheets remain in place as the visual record from which the live icons were cut, and are archived only after the feature-icon trace lands and the social network set is confirmed. Nothing is deleted.
- Confirm licence and ownership of the AI-generated hero, both sprite sheets and the icon set. Provenance and licensing are unverified (brief) — ASSET PROVENANCE SHOULD BE VERIFIED (risk P3-PROV-01). This is a business and legal decision, not an asset decision, and it should be settled before a five-rung production ladder is committed to the hero source.
- Approve the duplicate consolidation: move the six redundant copies whose status is ARCHIVE — 6,621,380 bytes across DUP-01, DUP-03, DUP-04 and DUP-09 — into an archive folder. That is 98.3% of all redundancy in six file moves. The five REFERENCE ONLY copies (112,312 bytes) stay where they are beside uploads/God-Squad-Images/README.txt, which is the primary evidence for the resolution ceiling. ARCHIVE means moved after final approval; no original is deleted, renamed or overwritten.
- Approve the removal candidate support.js (69,150 bytes, OTHER, REMOVE, currently referenced by the page — the Claude Design runtime, manifest). REMOVE means candidate for removal after final approval, never delete now, and removal would change the page, so it is out of Phase 3 scope and belongs to a later phase when the prototype is retired. The other REMOVE row, .thumbnail (640x355, 25,542 bytes, OTHER, an editor-generated preview of the page, unreferenced and of no production value), carries no such dependency.
- Which logo is official. Six LOGO files exist and are not the same artwork: images/WHITE FONT LOGO.png (500x500, 37,836 B, the one actually in use), images/logo.png (500x500, 47,147 B, DUP-04 canonical, unreferenced), white-font-300x300-mu98qi59-mytq.png (244x184, 23,444 B) and two stray root PNGs. The last two are the same byte count (43,606 B) at the same dimensions and differ only in their generator hash, but they are not byte-identical - md5 places neither in a duplicate group. Owner must name one file as the brand's mark.
- Vector logo. No SVG, AI or EPS logo exists anywhere in the project; the mark in use is a 500x500 PNG whose transparent padding leaves the visible glyph at about 66x50 inside a 78px box (brief: hard facts). Layered PSD sources exist outside the project at C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES and have never been opened. Status VECTOR LOGO REQUIRED. Phase 3 has not recreated it and must not.
- Which photography is final. Every product image is a crop of the 1024x1536 mockup (tee 235x230, hoodie 235x235, cap 215x190) rendering at 288px desktop and 327-382px phone; the Our Story slot uses a 650x480 crop of the mockup hero with headline fragments baked into the pixels, rendered at 998x520. Status HIGH-RES PRODUCT MASTER REQUIRED and HIGH-RES STORY MASTER REQUIRED. A crop of the mockup is not a substitute - it is the origin of the defect. The manifest also proposes story-community.webp as the production name for two different sources, so the owner must name the canonical story source.
- Social marks. icon-facebook.png and icon-instagram.png are circled two-tone badges cut from images/social-sprite.png, where the mockup shows a plain glyph (manifest images/icon-facebook.png), with colour baked into the pixels. Platform marks are trademarks and should come from each platform's official brand kit rather than being traced - which is why Phase 3 authored no SVG versions of them.
- Which social platforms are active. Only Facebook and Instagram are present in the project; the manifest records that the mockup also shows TikTok and YouTube (manifest images/icon-instagram.png), and both footer links are href="#" with no live URL. BUSINESS INFORMATION REQUIRED: the live URL for every active platform, and confirmation that TikTok, YouTube, X, Pinterest, LinkedIn, Spotify, WhatsApp and email are or are not in use.
- Collection naming and imagery. The prototype shows one collection, "The Faithful"; the spec anticipates The Faithful, Shirts, Hoodies, Caps, Collections and Best Sellers. No collection or editorial image exists for any of them and a product crop must not be promoted into a collection hero. DOCUMENT AS MISSING (the imagery); BUSINESS INFORMATION REQUIRED (the final collection list and names).
- The sprite sheets. images/icons-sprite.png (2172x724, 833,929 B) and images/social-sprite.png (2172x724, 927,973 B) are referenced by nothing and each has duplicates in uploads/ (DUP-03, DUP-09) - 1,761,902 B in total. The nine individual icon PNGs cut from those sheets - seven UI and feature icons plus the two social marks - are what the page loads. Manifest status ARCHIVE: candidate for removal after final approval, never a deletion, and they must survive until the feature-icon decision is settled.
- Feature icon treatment for crown, community, diamond and globe. Manifest status: OPTIMIZE for crown, community and diamond; REPLACE for globe. The choice between WebP conversion, a faithful SVG trace and a redesign is BUSINESS INFORMATION REQUIRED. Phase 3 deliberately excluded all four from phase-3-assets/icons/ because their visual character is approved and redesign is forbidden. The globe is the sharpest case: one 110x110 raster serves 16px in the announcement bar and 44px in the Brand Values row (manifest images/icon-globe.png).
- Favicon. No favicon of any kind exists; /favicon.ico returns 404 on every load. DOCUMENT AS MISSING (the asset); BUSINESS INFORMATION REQUIRED (which mark, and whether it is a cropped monogram or the full wordmark - the 500x500 wordmark is illegible at 32x32).
- Product naming and pricing. The prototype hard-codes "Signature Oversized Tee" at PHP 1,290, "Heavyweight Hoodie" at PHP 2,490 and "Utility Cap" at PHP 890, with a currency property defaulting to PHP and offering USD and EUR. These drive production filenames, product handles and the media filenames baked into CDN URLs. BUSINESS INFORMATION REQUIRED: final names, prices and currency, confirmed before any media is uploaded.
- Provenance and licensing of the AI-generated assets. The hero (images/hero-group.png, 1,989,201 B, plus two duplicates of the same size), both sprite sheets and the nine icon PNGs cut from them are AI-generated (brief: hard facts) - the single largest block of artwork in the project. Provenance, licensing and commercial-use rights are unverified. Status ASSET PROVENANCE SHOULD BE VERIFIED, before launch. Phase 3 has removed nothing and assumes no ownership.

## Appendix D. Phase 3 completion checklist

Every item the Phase 3 specification lists, with how it was satisfied.

- [x] **All assets inspected** — 48 files scanned recursively, 41 of them images (§2).
- [x] **Dimensions recorded** — parsed directly from PNG IHDR and WebP VP8/VP8L/VP8X headers, since no imaging library is installed and none was installed (§2).
- [x] **File sizes recorded** — every row of the manifest.
- [x] **Hashes calculated** — md5 for every file, with a sha256 prefix retained in the working inventory.
- [x] **Duplicates identified** — 9 exact groups covering 20 files, 11 redundant copies, 6,733,692 bytes (§11).
- [x] **Canonical assets identified** — one canonical per group, chosen by live reference first, then location, then path length (§11).
- [x] **Logo system documented** — every logo file, the padding defect, usage rules, and VECTOR LOGO REQUIRED (§3).
- [x] **Hero system documented** — candidates, verdicts, the WebP ladder and the missing mobile hero (§4).
- [x] **Product assets documented** — three files, all HIGH-RES PRODUCT MASTER REQUIRED, with views marked present or missing (§5).
- [x] **Story assets documented** — including that the live slot uses a crop of the mockup hero with headline text baked in (§6).
- [x] **Collection assets documented** — none purpose-made exists; the product-image rule is stated (§7).
- [x] **Icons documented** — classified UI, FEATURE, SOCIAL; nine drawn SVGs delivered (§8).
- [x] **Social icons documented** — present, missing and business-decision platforms separated; no account invented (§9).
- [x] **Sprites audited** — both sheets, unreferenced, superseded but retained (§10).
- [x] **Mockups separated** — the master mockup and the editor screenshots are REFERENCE ONLY (§2, §12).
- [x] **Production and reference distinction established** — carried in the manifest Status column and in §17.
- [x] **Naming system established** — with the explicit rule that no original is renamed (§16).
- [x] **Folder system established** — recommended tree plus the mapping from today's layout (§17).
- [x] **Responsive image strategy established** — width ladder, `image_url` with explicit `widths:` and `sizes:`, `image_tag`, loading strategy (§15).
- [x] **Shopify mapping established** — asset to destination, theme assets separated from merchant-uploaded media (§18).
- [x] **Missing assets documented** — Appendix B.
- [x] **Business approvals documented** — Appendix C.
- [x] **Performance risks documented** — Appendix A, at P0 to P3.
- [x] **Original assets preserved** — 0 modified, 0 deleted, verified by md5 against the Phase 0 inventory.
