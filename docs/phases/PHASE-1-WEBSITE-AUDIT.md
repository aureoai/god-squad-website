# GOD SQUAD — PHASE 1 WEBSITE AUDIT & TECHNICAL ASSESSMENT

**Project:** God Squad Premium Faith-Driven Streetwear  
**Audit date:** 2026-09-20  
**Subject:** "God Squad Website.html" (Claude Design export, formerly "God Squad Website.dc.html") + support.js + assets, in `C:\Users\TEST\OneDrive\Documents\GodSquad Website`  
**Target:** Production-ready Shopify Online Store 2.0 theme  
**Method:** Static inspection of every file (md5-hashed inventory, source-verified usage), runtime analysis of support.js, live rendering over HTTP at 375/390/430/720/768/900/901/920/1024/1280/1366/1440/1920 px with DOM measurements and full-page captures, network/console/font/bundle measurements, pixel-sampled contrast checks, and a three-lens inspection with adversarial verification (48 findings confirmed by three independent skeptics each). Nothing in the project was modified.  
**Status of this document:** Audit report and implementation blueprint. Phase 1 is inspection-only; no fixes were applied.


## 1. Executive Summary

### CURRENT STATE

**Visual.** Strong and substantially faithful to the approved mockup. The palette, the three typefaces, the copy, the section order and the editorial tone all match `uploads/God-Squad-Images/00-full-mockup-reference.webp`, and at 1440 px the page reads as the mockup intends (§7, §8). The departures are specific and few: the Our Story slot is filled with a crop of the mockup's *hero*, so the words "A PURPOSE", "K BY" and "TH." are baked into the photograph and visible at every width (STORY-01); the headline sets as three lines (WALK / BY / FAITH.) from 901 px upward where the mockup sets two (HERO-03); the wordmark renders at roughly half its mockup size because the PNG carries heavy transparent padding (BRAND-05); and the product photographs sit in visible square tiles rather than floating on the cream band (UI-02). Three further differences — the three-model hero photograph, the gold announcement globe and the two-icon social set — are deliberate owner edits recorded in the Claude Design history and are treated here as approved pending confirmation (HERO-05, UI-04).

**UX.** The page is a brand statement, not yet a shop. The hero asks nothing of the visitor: it contains no link or button at all, and on 1366x768 and 1280x720 laptops the first screen is hero-only, so no product is visible without scrolling (HERO-01, UX-01, RESP-13). Six of the nine links on the page are `href="#"` and scroll to the top; Shop and Collections both resolve to the same in-page anchor, making two primary menu items indistinguishable (NAV-03, NAV-05). Three of the ten steps in the intended homepage flow — Best Sellers / Product Discovery, Verse / Faith and Social / Community — do not exist in the build, although Verse is a primary navigation item (UX-02, UX-03, UX-04).

**Code.** The prototype is a Claude Design "dc" document, not a website in the ordinary sense. Every visible node lives inside a custom `<x-dc>` element that `support.js` (69,150 B) compiles into React elements at run time after fetching React and ReactDOM from unpkg (ARCH-01). Presentation is 77 inline `style` attributes totalling 6,421 characters with zero classes, plus a 2,916-byte embedded stylesheet whose responsive layer is 31 rules in two `max-width` queries keyed on 25 distinct editor-generated `data-r` hooks (26 occurrences) and carrying 55 `!important` declarations (CSS-02, CSS-03). One of those rules targets a hook no element carries (CSS-05). Nothing in this layer is reusable as code.

**Ecommerce.** Absent in its entirety. There is no product page, collection page, search, cart, cart drawer, add-to-cart, quantity control, variant model, availability state, checkout pathway or customer account; the page contains zero `<form>` and zero `<button>` elements, the cart badge is the literal character `0`, and the product grid holds no anchors at all (ECOM-01 through ECOM-06, PROD-01, PROD-02). The three products, their prices, their images and their colour swatches exist only as object literals inside a JavaScript class (DATA-01).

**Mobile.** Structurally sound, visually flawed. There is no horizontal overflow at any width tested from 375 to 1920 px, and the stacking order is sensible. But below 900 px the hero's fade overlay is anchored to the section while the photograph sits below the 88 px in-flow navigation, so the gradient reaches solid black 88 px above the image's lower edge: a black band crosses the photograph and the image ends in a hard seam at 375, 390, 430, 720, 768 and 900 px alike (RESP-01). Below 900 px there is no navigation of any kind, because the links are hidden and the hamburger is an inert `<span>` (NAV-01). Product tiles render at 327-382 px from 235 px sources, a 2.8x device-pixel upscale on a 2x phone (ASSET-03), and the phone page runs 4,382-4,547 px, about 5.4 screens, with a header that scrolls away and no way back (RESP-02).

**Accessibility.** The weakest dimension, and the one with the clearest legal and commercial exposure. The page exposes no operable controls beyond nine links: search, account and cart are bare `<img>` elements with `tabIndex -1`, and the hamburger is a `<span>` carrying an `aria-label` but no role (A11Y-01, HTML-04, A11Y-07). There is no skip link, no `<main>`, no `<header>`, and no `lang` attribute on `<html>` (A11Y-02, HTML-01, HTML-02). No `:focus` or `:focus-visible` rule exists anywhere, so the browser default ring is the only focus indicator (A11Y-04). Measured against the rendered pixels, three of the five navigation links fall below the 4.5:1 AA threshold over the bright sky between the models, reaching 2.4:1 at the brightest points (A11Y-03, HERO-02). The nine colour swatches are unnamed empty spans (A11Y-05), and the Our Story alt text describes a subject the file does not show (A11Y-09, HTML-11).

**SEO.** Effectively a blank slate. The document has no `<title>`, no meta description, no canonical link, no Open Graph or Twitter tags, no structured data and no favicon of any kind — every load also produces a 404 for `/favicon.ico` (SEO-01 through SEO-07). The whole store is one URL whose nine links are hash anchors (SEO-09). The homepage carries roughly 120 words of indexable copy, and the product and value content is rendered by JavaScript that depends on a third-party CDN (SEO-10, SEO-11).

**Performance.** Heavy for what it delivers. The hero is a 1,989,201-byte RGB PNG with no alpha channel, served unchanged at every viewport including a 375 px band (PERF-01). Nine raster icon PNGs totalling 308,521 bytes are drawn at 16-44 px (ICON-01). No image carries `width`, `height`, `srcset`, `sizes`, `loading` or `decoding`, so all fifteen files download at once and nothing is deferred (HTML-06, PERF-05). First paint requires three dependent network hops and about 211 KB of JavaScript, and because the runtime hides the template until React mounts, a CDN failure yields a blank page rather than degraded content (JS-02, ARCH-03). Fonts add 152,880 bytes from a third party, including one family downloaded for a single three-word phrase and one weight never used (PERF-03, PERF-04).

**Shopify readiness.** Zero at the code level, high at the design level. No `layout/`, `sections/`, `snippets/`, `templates/`, `assets/`, `config/` or `locales/` directory exists; there are no JSON templates, no section schemas, no section groups and no `settings_schema.json`, and the only editable value in the entire project is a currency prop in the Claude Design editor (SHOP-01, SHOP-02, SHOP-03). Most consequentially, the prototype's template delimiters are `{{ }}` — Liquid's own — so pasting this markup into a Shopify section would make Liquid evaluate `{{ products }}` and `{{ p.name }}` as undefined and silently render empty tiles (ARCH-02). That single fact makes a copy-and-adapt migration path unsafe.

### Overall conclusion

The existing website is a visual prototype/reference and should be preserved as the design baseline while the production Shopify implementation is rebuilt using Shopify-native architecture.

This is not a stylistic preference; it follows from four measured properties of the actual files. First, the presentation layer cannot be carried across: 69 % of the CSS lives in inline `style` attributes, there are no classes to hook, and the responsive behaviour is 55 `!important` declarations keyed to editor-generated `data-r` attributes that will not exist in a theme (CSS-02, CSS-03). Second, the template language collides with Liquid at the delimiter level, so the markup is not merely unhelpful but actively hazardous to paste (ARCH-02). Third, the content layer is a JavaScript class literal, not data: products, prices, swatches, value tiles, navigation and every copy string are hard-coded and must be re-expressed as Shopify objects, section settings, blocks and menus regardless of what happens to the markup (DATA-01 through DATA-09). Fourth, the runtime itself — a 1,911-line generated editor/streaming harness that evaluates code with `new Function`, posts messages to its parent frame and fetches React from unpkg — has no place in a storefront and must be discarded rather than adapted (JS-01, JS-04, JS-05).

What *is* reusable is considerable and should be protected: the approved palette and typography, the copy, the section order and proportions, the editorial layout intent, and the design decisions already signed off in the Claude Design editor. Phase 2 should lift these into tokens and components; Phase 10 should rebuild the markup natively against them.

### Headline numbers

| Measure | Value |
|---|---|
| Files inspected | 44 (17,185,754 bytes) |
| Assets inspected | 41 image files |
| Files actually referenced by the page | 17 (2,491,648 bytes, 14.5 % of the folder) |
| Exact duplicate groups | 9 groups, 11 redundant copies, 6,733,692 bytes (39 % of the folder) |
| Issues raised | 200 |
| By severity | 5 CRITICAL, 49 HIGH, 85 MEDIUM, 61 LOW |
| By priority | 3 P0, 65 P1, 80 P2, 52 P3 |
| Shopify blockers (P0) | 3 |
| Business decisions required | 30 consolidated items (Appendix A) |

### What is approved and must be preserved

- **Palette:** `#0D0C0A` ink, `#F3EFE6` bone, `#D8C08A` gold, with the secondary neutrals `#bdb6a8`, `#e9e4d8`, `#ebe6dc` and the olive `#4b5443` swatch value to be confirmed as part of the system (BRAND-02).
- **Typography:** Playfair Display 900 for display, Jost 400/500/600 for interface and body, Kaushan Script for the hand-lettered accents; the tracked-uppercase label convention is a brand signature and should be codified, not abandoned (BRAND-04).
- **Copy:** every headline, eyebrow, tagline, verse reference and the Our Story paragraph as written.
- **Section order and proportions:** announcement, header, hero, New Drop, Our Story, brand values, footer.
- **Imagery direction:** urban, low-angle, natural light, black and cream garments on location.
- **Deliberate owner edits** recorded in the editor history: the three-model hero photograph, the gold announcement globe, and the removal of two placeholder social icons. These are treated as approved and are listed in Appendix A only for formal confirmation.

### Decisions the owner must make

The audit did not invent a single business fact. Thirty consolidated decisions are required before implementation can be completed, covering the product catalogue, pricing and markets, collection structure, navigation destinations, the Verse concept, shipping and legal policy, social channels, a vector logo, original photography, and the Shopify store itself. They are set out in Appendix A with the issue IDs that depend on each. Four of them gate Phase 2 directly: confirmation of the extended palette, the mobile type scale, the browser and device support matrix, and the behaviour above 1440 px.

## 2. Project Inventory

### 2.1 Scope and method

The project root is `C:/Users/TEST/OneDrive/Documents/GodSquad Website` (inside the owner's personal OneDrive; not a git repository; no package.json, no build tooling, no CLAUDE.md) (evidence-render.md line 6). The recursive inventory in inventory.tsv lists **44 files totalling 17,185,754 bytes** across four folders. Usage was verified against the two source files, not against filenames: an asset counts as "used" only when `God Squad Website.html` or `support.js` references it by path. The result is that the page references **17 files (15 images + support.js + the HTML itself) totalling 2,491,648 bytes**, i.e. 14.5 % of the folder; the remaining 27 files (14,694,106 bytes) serve no page (measurements.md line 32). Byte-identical duplicates were established by md5 in inventory.tsv (nine DUP groups, eleven redundant copies); their KEEP/ARCHIVE/REMOVE classification belongs to the ASSET register and is only cross-referenced here.

**Rename note.** The entry page was exported from Claude Design as `God Squad Website.dc.html` and was deliberately renamed by the owner to `God Squad Website.html` on 2026-09-20 at 15:34; the content is stated unchanged by the audit lead (evidence-render.md line 7). The directory listing shows the file at 15,632 bytes with an mtime of 11:26:45, three minutes after the 11:23:43 extraction time of every other exported file. Every reference in the Phase 1 spec to `God Squad Website.dc.html` means this file. The runtime is indifferent to the suffix: `rootNameForDocument()` tests the path against `/\.dc\.html?$/i` and otherwise falls back to `doc.baseURI` (support.js lines 133-142), `dcNameFromPath()` strips either suffix (line 82), and `boot()` marks the root as fetched before anything else (line 155), so no `.dc.html` request is ever made for the root; verified booting over HTTP and file:// (evidence-render.md line 7). See INV-02.

### 2.2 Totals by folder

| Folder | Files | Bytes | Referenced by the page | Notes |
|---|---|---|---|---|
| (root) | 8 | 2,250,147 | 3 (HTML, support.js, story image) | 5 unreferenced export artefacts (INV-03) |
| images/ | 19 | 4,256,919 | 14 | icons-sprite.png, social-sprite.png, logo.png, hero-model.webp, our-story.webp unreferenced |
| uploads/ | 9 | 10,336,423 | 0 | reference material and duplicate generations |
| uploads/God-Squad-Images/ | 8 | 342,265 | 0 | mockup crop set + README |
| **Total** | **44** | **17,185,754** | **17 (2,491,648 B)** | |

(inventory.tsv: `referenced_by=html` on rows 3, 6, 10, 11, 13-21 and 25-27; the HTML itself is the entry file.)

### 2.3 Root folder

| # | Path | Type | Bytes | Dimensions | Purpose | Actively used (verified) | DUP group | Production-ready | Migrate to Shopify |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `.thumbnail` | WebP (no extension) | 25,542 | 640x355 | Claude Design editor preview of the page | No: no reference in HTML or support.js (the inventory's "README" tag is a loose name match, measurements.md line 32) | none | No (editor artefact) | No |
| 2 | `01-hero-model-mu98p88t-7jig.webp` | WebP | 39,966 | 650x480 | Our Story background image | Yes: `src="./01-hero-model-mu98p88t-7jig.webp"` (God Squad Website.html line 126) | none (same byte count as DUP-02 but a different md5; separate re-encode, findings-verified.json C1) | No: mockup-hero crop with baked-in headline text, upscaled 1.53x at 1440 (C1; see the STORY and ASSET registers) | No: replace |
| 3 | `God Squad Website.html` | HTML | 15,632 | n/a | Entry page; Claude Design "dc" document (renamed from `.dc.html`) | Yes: entry file | none | No: prototype template, needs the dc-runtime to render (ARCH-01) | No: rebuild as Liquid; archive as design baseline |
| 4 | `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` | PNG RGB | 1,989,201 | 1672x941 | Export copy of the hero group photo | No: no reference | DUP-01 (= images/hero-group.png) | No | No (see the ASSET register) |
| 5 | `support.js` | JavaScript | 69,150 | n/a | Claude Design dc-runtime (template compiler + React mount + editor bridge) | Yes: `<script src="./support.js">` (line 6) | none | No (see §6) | No: REMOVE DURING SHOPIFY CONVERSION |
| 6 | `white-font-300x300-mu98qi59-mytq.png` | PNG RGBA | 23,444 | 244x184 | Small white wordmark export | No: no reference | none | No | No |
| 7 | `white-font-trans-mu98q2ez-zrdd.png` | PNG RGBA | 43,606 | 500x500 | White wordmark on transparent (export copy) | No: no reference | none (different md5 from #8 despite identical size) | No | No |
| 8 | `white-font-trans-mu98qky0-5tt6.png` | PNG RGBA | 43,606 | 500x500 | White wordmark on transparent (second export copy) | No: no reference | none | No | No |

### 2.4 images/

| # | Path | Type | Bytes | Dimensions | Purpose | Actively used (verified) | DUP group | Production-ready | Migrate to Shopify |
|---|---|---|---|---|---|---|---|---|---|
| 9 | `images/WHITE FONT LOGO.png` | PNG RGBA | 37,836 | 500x500 | Wordmark in nav (78 px box) and footer (56 px box) | Yes: lines 69 and 155 | none (same byte count, 37,836 B, as external `WHITE FONT Trans.png`; identity not hashed, evidence-render.md line 13) | Partly: raster with large transparent padding, URL-unsafe name (FIDELITY-4, INV-04) | Yes, renamed; replace with SVG when a vector master exists (INV-05) |
| 10 | `images/hero-group.png` | PNG RGB, no alpha | 1,989,201 | 1672x941 | Hero photograph at every width | Yes: line 65 | DUP-01 (x3) | No: 2 MB PNG for a photo (C10; see the ASSET/PERF register) | BUSINESS DECISION REQUIRED (approved deviation from the mockup, to confirm, evidence-render.md line 68); if kept, only after re-encoding (see the ASSET register) |
| 11 | `images/hero-model.webp` | WebP | 39,966 | 650x480 | Mockup hero crop (single capped model) | No: no reference ("README" tag is a name match only) | DUP-02 (= uploads/God-Squad-Images/01-hero-model.webp) | No | No: archive |
| 12 | `images/icon-account.png` | PNG RGBA | 28,470 | 110x110 | Account icon, drawn at 24 px | Yes: line 77 | none | No: raster UI icon (TECHNICAL-6; see the ASSET register) | No: replace with SVG snippet |
| 13 | `images/icon-cart.png` | PNG RGBA | 29,127 | 110x110 | Cart icon, 24 px | Yes: line 78 | none | No | No: replace with SVG snippet |
| 14 | `images/icon-community.png` | PNG RGBA | 39,978 | 150x110 | Community value icon, 44 px | Yes: data script line 181 | none | No | No: replace with SVG snippet |
| 15 | `images/icon-crown.png` | PNG RGBA | 33,339 | 130x110 | Faith Driven value icon, 44 px | Yes: line 180 | none | No | No: replace with SVG snippet |
| 16 | `images/icon-diamond.png` | PNG RGBA | 34,556 | 130x110 | Premium Quality value icon, 44 px | Yes: line 183 | none | No | No: replace with SVG snippet |
| 17 | `images/icon-facebook.png` | PNG RGBA | 36,771 | 130x130 | Footer social icon, 28 px | Yes: line 160 | none | No | No: replace with SVG snippet |
| 18 | `images/icon-globe.png` | PNG RGBA | 35,625 | 110x110 | Announcement globe (16 px) and Worldwide value icon (44 px) | Yes: lines 60 and 182 | none | No | No: replace with SVG snippet |
| 19 | `images/icon-instagram.png` | PNG RGBA | 42,319 | 130x130 | Footer social icon, 28 px | Yes: line 161 | none | No | No: replace with SVG snippet |
| 20 | `images/icon-search.png` | PNG RGBA | 28,336 | 110x110 | Search icon, 24 px | Yes: line 76 | none | No | No: replace with SVG snippet |
| 21 | `images/icons-sprite.png` | PNG RGBA | 833,929 | 2172x724 | AI-generated icon sheet the individual icons were cut from | No: no reference | DUP-03 (x3) | No | No (see the ASSET register) |
| 22 | `images/logo.png` | PNG RGBA | 47,147 | 500x500 | White-on-black wordmark | No: no reference | DUP-04 (= 06-logo.png) | No | No: archive |
| 23 | `images/our-story.webp` | WebP | 41,004 | 535x348 | Mockup Our Story crop (three models), the composition the mockup intends | No: no reference | DUP-05 (= 05-our-story-models.webp) | No: too small for the slot (critic addition 4) | No: reference only |
| 24 | `images/product-cap.webp` | WebP | 10,002 | 215x190 | Utility Cap card image | Yes: line 177 | DUP-06 | No: mockup crop upscaled 1.34x-2.8x (C2) | No: placeholder until product photography exists |
| 25 | `images/product-hoodie.webp` | WebP | 12,328 | 235x235 | Heavyweight Hoodie card image | Yes: line 176 | DUP-07 | No (C2) | No: placeholder |
| 26 | `images/product-tee.webp` | WebP | 9,012 | 235x230 | Signature Oversized Tee card image | Yes: line 175 | DUP-08 | No (C2) | No: placeholder |
| 27 | `images/social-sprite.png` | PNG RGBA | 927,973 | 2172x724 | AI-generated social icon sheet | No: no reference | DUP-09 (x2) | No | No (see the ASSET register) |

### 2.5 uploads/

| # | Path | Type | Bytes | Dimensions | Purpose | Actively used (verified) | DUP group | Production-ready | Migrate to Shopify |
|---|---|---|---|---|---|---|---|---|---|
| 28 | `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png` | PNG RGBA | 833,929 | 2172x724 | Icon sheet generation (copy) | No | DUP-03 | No | No |
| 29 | `uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png` | PNG RGBA | 833,929 | 2172x724 | Icon sheet generation (copy) | No | DUP-03 | No | No |
| 30 | `uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png` | PNG RGBA | 927,973 | 2172x724 | Social sheet generation (copy) | No | DUP-09 | No | No |
| 31 | `uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png` | PNG RGB | 1,989,201 | 1672x941 | Hero group photo generation (copy) | No | DUP-01 | No | No |
| 32 | `uploads/GODSQUAD WEBSITE MOCKUP.png` | PNG RGB | 1,872,888 | 1024x1536 | Master approved mockup (design baseline) | No: reference only | none | n/a (reference) | Archive as design baseline |
| 33 | `uploads/pasted-1789874083026-0.png` | PNG RGB | 17,311 | 118x77 | Globe icon crop pasted into the editor | No | none | No | No: archive |
| 34 | `uploads/pasted-1789874193900-0.png` | PNG RGB | 1,541,839 | 1920x1009 | Claude Design editor screenshot (hero replacement history) | No | none | n/a (reference) | No: archive |
| 35 | `uploads/pasted-1789874322321-0.png` | PNG RGB | 769,319 | 1920x1009 | Editor screenshot (globe swap, social box removal, currency prop visible) | No | none | n/a (reference) | No: archive |
| 36 | `uploads/pasted-1789874476205-0.png` | PNG RGB | 1,550,034 | 1920x1009 | Editor screenshot (gold globe confirmation) | No | none | n/a (reference) | No: archive |

### 2.6 uploads/God-Squad-Images/

| # | Path | Type | Bytes | Dimensions | Purpose | Actively used (verified) | DUP group | Production-ready | Migrate to Shopify |
|---|---|---|---|---|---|---|---|---|---|
| 37 | `00-full-mockup-reference.webp` | WebP | 182,250 | 1024x1536 | Mockup in WebP (the file this audit uses as the approved reference) | No: reference only | none | n/a | Archive as design baseline |
| 38 | `01-hero-model.webp` | WebP | 39,966 | 650x480 | Mockup hero crop | No | DUP-02 | No | No: archive |
| 39 | `02-product-oversized-tee.webp` | WebP | 9,012 | 235x230 | Tee crop (source of images/product-tee.webp) | No | DUP-08 | No | No: archive |
| 40 | `03-product-heavyweight-hoodie.webp` | WebP | 12,328 | 235x235 | Hoodie crop | No | DUP-07 | No | No: archive |
| 41 | `04-product-utility-cap.webp` | WebP | 10,002 | 215x190 | Cap crop | No | DUP-06 | No | No: archive |
| 42 | `05-our-story-models.webp` | WebP | 41,004 | 535x348 | Three-model story crop | No | DUP-05 | No | No: archive |
| 43 | `06-logo.png` | PNG RGBA | 47,147 | 500x500 | White-on-black wordmark | No | DUP-04 | No | No: archive |
| 44 | `README.txt` | Text | 556 | n/a | States that files 00-06 are crops of the 1024x1536 mockup, not original photography (README.txt lines 15-16) | No (documentation) | none | n/a | Archive with the baseline |

### 2.7 Tooling and external sources (not site files)

| Path | Type | Bytes | Purpose | Status |
|---|---|---|---|---|
| `.claude/launch.json` | JSON | 228 | Audit tooling added by the audit lead: `python -m http.server 8765 --bind 127.0.0.1` so the page can be served over HTTP for measurement | Not a site file; not part of the 44; must never be copied into the theme (evidence-render.md line 10; launch.json lines 4-9). Created inside the project root during Phase 1 (folder mtime 2026-09-20 13:23), which the spec's "Do not modify the website during this phase" does not allow; the final checklist must disclose it, or the owner should remove it after the audit, so that the mandated statement "NO PROJECT FILES WERE MODIFIED" is accurate (INV-06) |
| `C:/Users/TEST/OneDrive/Desktop/GODSQUAD/PSD FILES/` | Folder, outside the project | OG LOGO.psd 613,320; OG LOGO 300x300.psd 209,976; BLACK FONT.png 182,337; WHITE FONT.png 41,377; WHITE FONT Trans.png 37,836; WHITE FONT 300x300.png 17,674; OG LOGO-assets/ | Layered logo sources; `WHITE FONT Trans.png` matches the byte count of images/WHITE FONT LOGO.png (not hashed) | Read-only; the only masters seen. No SVG/AI/EPS vector logo has been located anywhere (INV-05) |
| `C:/Users/TEST/Downloads/GODSQUAD WEBSITE.zip` | Zip, outside the project | ~17 MB | Original Claude Design export (11:23 on 2026-09-20) | Reference copy of the pre-rename state (evidence-render.md line 12) |

### 2.8 Inventory observations

- Every raster in the project is either a crop of the 1024x1536 mockup (products, story, hero-model), an AI-generated sheet or photo (sprites, hero-group), an editor export of the wordmark, or a screenshot. There is **no original photography and no vector logo** in the project (README.txt lines 15-16; evidence-render.md line 13). Masters live outside the folder or do not exist: INV-05, BUSINESS INFORMATION REQUIRED.
- The root folder carries 2,125,399 bytes of unreferenced export artefacts with unstable hash-suffixed names (INV-03), and the one live root asset also has a hash-suffixed name.
- One referenced asset has a URL-unsafe name (`images/WHITE FONT LOGO.png`, requested as `/images/WHITE%20FONT%20LOGO.png`, used twice at lines 69 and 155, findings-verified.json TECHNICAL-10); the unreferenced uploads/ names additionally contain spaces and commas (INV-04).
- There is no version control and no tagged baseline of the audited state (INV-01), and one non-site file was added to the root during the audit (INV-06).
- Byte-identical duplicates (DUP-01 to DUP-09) are documented here but classified in the ASSET register.

## 3. Current Architecture

### 3.1 What the entry file is

`God Squad Website.html` is not a conventional HTML page; it is a Claude Design "dc" (design component) document. The real `<head>` holds only a charset meta, a viewport meta and a synchronous `<script src="./support.js">` (God Squad Website.html lines 3-7). Everything visible sits inside one custom `<x-dc>` element (lines 9-168). Its first child, `<helmet>` (lines 10-54), carries the Google Fonts `<link>`, a preconnect and the only `<style>` block (2,916 bytes). After `</x-dc>` a `<script type="text/x-dc" data-dc-script data-props="...">` (lines 169-188) declares `class Component extends DCLogic` whose `renderVals()` returns the `products[]` and `values[]` arrays. The browser cannot execute that script (unknown MIME type); only support.js reads it.

### 3.2 Render chain (diagram in text)

```
Browser parses God Squad Website.html
 |- <head> <script src=./support.js> (sync, blocks parsing)                        html line 6
 |    |- hideRawTemplate(): <style>x-dc{display:none!important}</style>            support.js 1818-1822, 1906
 |    '- loadReactUmd(): appends react@18.3.1 + react-dom@18.3.1 UMD from unpkg
 |         in parallel (Promise.all), SRI hashes, async=false so they execute in
 |         order; failure -> console.error + rethrow, no fallback                  1143-1146, 1823-1847, 1907-1910
 |         '- init(): prepend BASE_CSS; expose window.__dcUpdate/__dcSetProps/DCLogic...;
 |              on DOMContentLoaded -> __dcBoot()                                     1848-1904
 |              '- boot():                                                            150-200
 |                   |- parseDcDocument(): x-dc.innerHTML -> template string;
 |                   |     script[data-dc-script] -> js text + data-props JSON       24-37, 56-74
 |                   |- markFetched(rootName): root never fetched as .dc.html        155
 |                   |- adoptParsed(): updateHtml() -> compileTemplate()
 |                   |     (encodeCase renames <helmet>-><sc-helmet>, stamps data-dc-tpl on
 |                   |      every element, walk() builds React element factories)     372, 467-482, 1687-1700
 |                   |     updateJs() -> evalDcLogic(): new Function(...) -> Component 842-851, 1701-1724
 |                   |- fetch(location.href) -> parseDcText() -> updateHtml() again
 |                   |     (second document request + second compile/render;
 |                   |      fails silently on file://)                                158-164
 |                   |- <x-dc> replaced by <div id="dc-root">; FULL_PAGE_CSS appended  165-173
 |                   '- ReactDOM.createRoot(hostEl).render(<StandaloneRoot/>)         174-198
 |                        '- StreamableComponent.render(): vals = {...props(currency), ...logic.renderVals()}
 |                             -> r.tpl(vals)                                          1080-1104
 |                             |- <sc-helmet> -> helmet.compile(): clones <link>/<style> into <head> 1420-1493
 |                             |- <sc-for list="{{ products }}" as="p"> -> walkFor()  611-645
 |                             |- <sc-if value="{{ p.img }}"> -> walkIf()             646-660
 |                             |- {{ p.name }} text -> walkText() -> <span class="sc-interp"> 569-610
 |                             |- attr="...{{ s }}..." -> compileAttr()/resolve()     401-412, 205-236
 |                             '- style-hover="..." -> pseudoClass() -> .scpN:hover{...!important} 428-430, 1567-1589
 '- Meanwhile the HTML parser has already built the raw <img src="{{ p.img }}"> and
    <img src="{{ v.icon }}"> inside the hidden x-dc -> two 404s per load             evidence-render.md line 29
```

Nothing is painted until the last step; the page is a black rectangle until React has mounted (findings-verified.json TECHNICAL-7; ARCH-03, JS-02).

### 3.3 Custom elements and attributes and who consumes them

| Construct | Where in HTML | Consumer in support.js | Meaning outside the dc-runtime |
|---|---|---|---|
| `<x-dc>` | line 9 | `parseDcDocument` (25), `boot` (165-168) | Unknown element; content stays in DOM, hidden only if support.js ran |
| `<helmet>` | lines 10-54 | `encodeCase` -> `sc-helmet` (372-378), `createHelmetManager.compile` (1420-1493) | Unknown element in body; browser still applies the `<style>` inside it |
| `<script type="text/x-dc" data-dc-script data-props>` | lines 169-188 | `parseDcDocument` (27-30), `evalDcLogic` (842-851), `StandaloneRoot` defaults (185-193) | Inert text |
| `DCLogic` | line 170 | Alias of `StreamableLogic` (817-841, 1898) | Undefined identifier |
| `<sc-for list as hint-placeholder-count>` | lines 107, 115, 143 | `walkFor` (611-645) | Unknown element; children render once with literal `{{ }}` text |
| `<sc-if value hint-placeholder-val>` | lines 110, 145 | `walkIf` (646-660) | Unknown element |
| `{{ expr }}` in text and attributes | lines 107-120, 143-149 | `walkText` (569-610), `compileAttr` (401-412), `resolve` (205-236) | Literal text; **identical to Liquid output syntax** (ARCH-02) |
| `style-hover="..."` | lines 104, 132 | `collectProps` (428-430), `createPseudoSheet` (1567-1589) | Ignored attribute; hover disappears (JS-07) |
| `data-r`, `data-screen-label` | 25 distinct hooks, 26 occurrences; 4 sections | Not read by the runtime (evidence-render.md line 22); `data-r` is the CSS selector hook for the media queries | CSS hooks only (see the CSS and HTML registers) |
| `hint-placeholder-*`, `data-dc-tpl`, `.sc-interp` | template / rendered DOM | Streaming placeholders and editor mapping (614, 648, 474, 607) | Editor bookkeeping (JS-05) |

The runtime supports far more than this page uses (`<x-import>` with Babel-transpiled JSX, `<dc-import>` sibling components, deck-stage slide keying, streaming placeholders, design-doc canvas mode); §6 quantifies the unused share.

### 3.4 Data system

There is exactly one data source: the `renderVals()` return value (lines 171-186), merged over the editor props. Props come from the `data-props` JSON on the script tag: a single `currency` prop declared as `{editor:"enum", default:"₱", options:["₱","$","€"], section:"Shop"}` (line 169; css-html-stats.txt line 213), which the Claude Design editor exposes as a dropdown (pasted-1789874322321-0.png, top-left "currency ₱"). `renderVals()` string-concatenates `cur + '1,290'` etc., so the prop swaps the symbol only (TECHNICAL-4). Products are three object literals (`name`, `price`, `img`, `swatches[3]`); values are four (`title`, `sub`, `icon`). No other page state exists; `StreamableLogic.state` is never used. The full hardcoded-content map and its Shopify destinations are in §23 (DATA-01 to DATA-09).

### 3.5 CSS architecture

One embedded `<style>` (2,916 B) plus 77 inline `style=""` attributes totalling 6,421 characters; zero `class` attributes in the source (the runtime adds `scp0`/`scp1`); 55 `!important` declarations, all in the media queries; two breakpoints, `@media (max-width:900px)` (26 rules) and `@media (max-width:520px)` (5 rules), keyed on `[data-r=...]` attribute selectors; one dead hook, `[data-r=pad]`, styled but absent from markup (css-html-stats.txt lines 2-6; God Squad Website.html lines 13-53). Palette literals repeat (`#0d0c0a` x14, `#d8c08a` x10, `#f3efe6` x9 in the stats' de-duplicated count). Architecturally this is an inline-first prototype with an `!important` responsive override layer; nothing is tokenised. Detailed findings are in the CSS register; the brand tokens in the BRAND register.

### 3.6 Fonts

Google Fonts CSS is requested from inside `<helmet>` (line 12) for Playfair Display 700/900, Jost 400/500/600 and Kaushan Script 400 with `display=swap`; only Jost 400/500/600, Kaushan Script 400 and Playfair Display 900 are actually used and downloaded (152,880 B of woff2 plus 7,461 B CSS) (evidence-render.md lines 35-37). The `<link>` reaches `<head>` only because the helmet manager clones it at render time (support.js 1447-1474); the preconnect covers fonts.googleapis.com only, without `crossorigin`, and there is none for fonts.gstatic.com (TECHNICAL-9). The peso sign and the arrow glyph fall back to a per-platform system font (see the BRAND register). See ARCH-04.

### 3.7 Image loading

Fifteen raster files (17 references) are loaded through plain `<img>` elements with no `srcset`, `sizes`, `loading`, `decoding`, `width` or `height` attributes (evidence-render.md line 50). The hero is a 1,989,201-byte RGB PNG at every width (C10); product images are 215-235 px mockup crops upscaled everywhere (C2); the story image is a 650x480 crop with baked-in text (C1). Because the raw template is parsed by the browser before the runtime runs, image downloads start before layout, and the two templated `<img src="{{ p.img }}">` / `{{ v.icon }}` produce two 404s per load (C3; JS-06). Weight, format and resolution findings are in the ASSET/PERF register.

### 3.8 Interaction handling

The runtime maps `on*` attributes to React handlers (EVENT_MAP, support.js 317-359, 438-439) but the markup contains none, and the runtime attaches no UI event handlers of its own; its only listeners are the editor `message` listener (1407-1419, JS-05) and `DOMContentLoaded` for boot (1904). There are zero `<button>`, zero `<form>`, zero `tabindex` attributes (css-html-stats.txt line 209). The hamburger is a `<span data-r="nav-menu" aria-label="Menu">` with no role or handler (line 75); search, account and cart are bare `<img>` (lines 76-78). The only behaviours on the page are native anchor navigation for nine links (six of them `href="#"`), the global `a:hover{color:#d8c08a}` (line 16) and the two runtime-generated CTA hover rules (TECHNICAL-2). See JS-08; the inert controls and placeholder links are in the NAV register.

### 3.9 Responsive handling

Desktop-first: the base inline styles describe the 1440 layout inside a `max-width:1440px` wrapper (line 55), and the 900 px query re-flows every section with `!important` (hero to one column with the image `order:-1` and the nav `position:relative; order:-2`; products to two columns; values to two columns; footer to a column), while the 520 px query collapses products, values and the announcement bar to one column (lines 18-52). The measured outcomes per width, including the 88 px hero-fade offset caused by the in-flow nav (RESPONSIVE-1), are in the RESP register.

### 3.10 Runtime dependencies (external origins)

| Dependency | Version | Origin | Loaded when | Bytes (raw / gz) |
|---|---|---|---|---|
| support.js | generated build of dc-runtime/src/*.ts | local | always, sync in head | 69,150 / 19,037 |
| react.production.min.js | 18.3.1 | unpkg.com (SRI sha384) | always, before boot (parallel with react-dom) | 10,751 / 4,263 |
| react-dom.production.min.js | 18.3.1 | unpkg.com (SRI sha384) | always, before boot | 131,835 / 42,818 |
| @babel/standalone | 7.29.0 | unpkg.com (SRI sha384) | only if an `<x-import>` of .jsx/.tsx exists (none on this page) | 3,137,752 / 653,872 |
| Google Fonts CSS + woff2 | n/a | fonts.googleapis.com, fonts.gstatic.com | at render (helmet clone) | 7,461 + 152,880 |

(bundle-sizes.txt; support.js 1143-1148, 1843-1846; evidence-render.md lines 32-37.) The page boots from file:// but still needs the network for unpkg and Google Fonts (evidence-render.md lines 7, 19-20).

### 3.11 Verdict on suitability for a Shopify theme

**REPLACE the architecture; KEEP the visual design as the baseline.** The current page is a client-rendered React template driven by a proprietary editor runtime, with its data in a JavaScript class evaluated by `new Function`, its styles inline, its head assembled at runtime and its template syntax colliding with Liquid's own `{{ }}` delimiters. Shopify Online Store 2.0 is the inverse model: server-rendered Liquid sections with JSON templates, section groups and schema-driven settings, where product and collection data arrive as Liquid objects and the Theme Editor owns layout. None of `x-dc`, `helmet`, `sc-for`, `sc-if`, `DCLogic`, `data-dc-script`, `style-hover` or support.js has a place in that model, and the two constructs that look portable (`{{ }}` and the section order) are exactly the ones that would fail silently (ARCH-02). The correct read of this prototype is a rendered-DOM and pixel reference: section order, palette, typefaces and copy are to be preserved (they match the approved mockup, evidence-render.md line 67); composition deviates in the hero photo, headline and story-heading line breaks, wordmark size, product tiles, social icon style and globe colour (FIDELITY-1 to FIDELITY-9; C18 refuted), and those deviations are decided in the HERO, STORY and BRAND sections, not carried over blindly. Every mechanism that produces the page is rebuilt with Shopify-native architecture in Phase 10 (ARCH-01, JS-01). Theme structure itself is specified in the SHOP register.

## 4. HTML Audit

Scope: a single entry page, "God Squad Website.html" (15,632 B). It was exported by Claude Design as "God Squad Website.dc.html" and deliberately renamed on 2026-09-20; content is unchanged and every spec reference to the old name means this file (evidence-render.md). The static source parses to 116 start tags including template markup; the rendered DOM is 166 elements at every width (css-html-stats.txt; measurements.md). Verified counts used throughout: 0 `<button>`, 0 `<form>`, 0 `<input>`, 0 `tabindex`, 0 `role`, 3 `aria-*`, 0 `class`, 77 `style`, 12 `<img>`, 12 `<br>`, 9 `<a>`, 2 `id`, duplicate attributes: none (css-html-stats.txt).

### 4.1 Document skeleton

| Part | What is there | Verdict |
|---|---|---|
| `<html>` (line 2) | No `lang` attribute | MISSING — HTML-02 |
| `<head>` (lines 3-7) | `charset`, `viewport`, `<script src="./support.js">` only; no `<title>`, description, canonical, OG, favicon, robots, JSON-LD (css-html-stats.txt) | see the SEO register |
| `<body>` | One `<x-dc>` custom element (line 9) wrapping `<helmet>` (lines 10-54: preconnect, Google Fonts `<link>`, the only `<style>`) and a 1440px wrapper `<div>` (line 55); then `<script type="text/x-dc" data-dc-script data-props>` (lines 169-188) holding all product and value data | REBUILD — HTML-09, HTML-05; data see the DATA register |

The page's stylesheet, font link and preconnect live inside the body and are only hoisted into `<head>` by the runtime's helmet manager at render time (evidence-render.md). Without the runtime the document has no head-level presentation at all (HTML-09).

### 4.2 Landmarks and section structure

| Region (spec flow) | Element | Landmark exposed | Issue |
|---|---|---|---|
| Announcement bar | `<div data-r="announce">` (line 58) | none | HTML-01 |
| Header / nav | `<nav data-r="nav">` nested inside the hero `<section>`, `position:absolute` (line 68) | navigation, unnamed | HTML-01, HTML-10 |
| Hero | `<section data-screen-label="Hero">` (line 64) | not a region (no accessible name) | HTML-01 |
| New Drop | `<section id="shop">` (line 98) | not a region; has h2 but no `aria-labelledby` | HTML-01 |
| Our Story | `<section id="story">` (line 125) | not a region | HTML-01 |
| Brand values | `<section data-screen-label="Values">` (line 142) | not a region; no heading at all | HTML-01, HTML-03 |
| Footer | `<footer>` (line 153) | contentinfo | KEEP |
| Main | absent | no `main` landmark | HTML-01 |

There is no `<header>` and no `<main>` (evidence-render.md; findings-verified.json C7). The header is structurally welded to the hero: the nav is absolutely positioned over the hero image and the hero copy columns are padded `170px` / `190px` top to clear it (lines 82, 90). This coupling is what forces the nav in-flow with `order:-2` under 900px and produces the hero-fade offset and the nav-over-sky contrast failures (findings-verified.json TECHNICAL-11; see the RESP and A11Y registers for those outcomes). In a Shopify 2.0 theme the announcement bar and header must be separate sections in the header group, so the current nesting is REBUILD, not IMPROVE (HTML-01, severity HIGH).

### 4.3 Heading hierarchy

The complete outline is: h1 "Walk By Faith." (line 84) → h2 "The`<br>`Faithful" (line 101) → h2 "Real People.`<br>`Bigger Purpose." (line 130). Nothing else is a heading (css-html-stats.txt). Product names (line 112) and value titles (line 146) are `<div>`s; the values section has no heading of any level; the section eyebrows "New Drop /" and "Our Story" (lines 100, 129) are `<div>`s. Heading navigation therefore cannot reach a product or a value, and "The Faithful" is a campaign name rather than a descriptive heading for a product grid (HTML-03, severity HIGH; the SEO consequence is in the SEO register). The two h2s carry hard `<br>` line breaks (lines 101, 130); the h1 has none and wraps by column width — its WALK / BY / FAITH. stack on three lines at 1440 and 1024 comes from a copy column of roughly 450px plus `text-wrap:balance` (findings-verified.json FIDELITY-2; desktop-1440.png). Even with its `<br>`, the Our Story h2 wraps to three lines at 1440 and four at 1024 (findings-verified.json FIDELITY-5; desktop-1440.png), while "THE FAITHFUL" holds its intended two lines (desktop-1440.png) (HTML-07).

### 4.4 Navigation structure

`<nav>` (lines 68-80) holds: a logo wrapper `<div style="background:#0230">` with a non-linked logo `<img>` (line 69); a `<div data-r="nav-links">` with five bare `<a>` elements and no `<ul>/<li>` (lines 70-73); and a utility `<div>` containing the hamburger `<span data-r="nav-menu" aria-label="Menu">` built from three identical inline-styled bar `<span>`s (line 75), three bare `<img>` icons with alt Search / Account / Cart (lines 76-78) and a cart badge `<span>` with the literal text `0` (line 78). The `<nav>` has no `aria-label`; the Home active state is a hard-coded inline underline (line 71); the wordmark is not a link (the destination question is in the NAV register; the hard-coded state and badge are in the DATA register). Semantically, the hamburger is an `aria-label` on a generic `<span>` with no role — a construct ARIA 1.2 prohibits and most screen readers ignore (findings-verified.json critic addition on the hamburger) — and the three utility icons are images that announce as controls but are not controls (HTML-04, severity HIGH). The wiring of these controls is owned by the NAV register; this register records that the elements themselves must become `<button>`/`<a>` before any wiring can work.

### 4.5 Buttons (zero) and links (nine)

| # | Text / name | `href` | Line | Note |
|---|---|---|---|---|
| 1 | Home | `#` | 71 | placeholder; hard-coded active style |
| 2 | Shop | `#shop` | 72 | in-page anchor |
| 3 | Collections | `#shop` | 72 | same target as Shop |
| 4 | Our Story | `#story` | 72 | in-page anchor |
| 5 | Verse | `#` | 72 | placeholder; no verse section exists |
| 6 | View All Products → | `#` | 104 | CTA styled as button; `style-hover` |
| 7 | Our Story → | `#` | 132 | CTA styled as button; `style-hover` |
| 8 | Facebook (`aria-label`) | `#` | 160 | placeholder; also `alt="Facebook"` on the image |
| 9 | Instagram (`aria-label`) | `#` | 161 | placeholder; also `alt="Instagram"` on the image |

Six of nine links are `href="#"` (css-html-stats.txt); the destinations and the inert product tiles are documented in the NAV and ECOM registers. Empty links: none; the two image-only social anchors carry `aria-label` and image `alt`, so every link has an accessible name (lines 160-161). Markup-level observations: the page has zero `<button>` elements, so every future control (menu toggle, search, cart, add-to-cart, swatch selection) is new markup, not a port (HTML-04); both CTAs append a bare `<span>→</span>` that is not `aria-hidden` (labelling is in the A11Y register; the glyph's font fallback is in the BRAND register); the two social anchors name themselves twice (aria-label plus image alt), which is harmless but redundant (HTML-11).

### 4.6 Images and alt text

| Line | `src` | `alt` | Assessment |
|---|---|---|---|
| 60 | images/icon-globe.png | `""` | decorative — correct |
| 65 | images/hero-group.png | God Squad crew | informative; acceptable but thin for the LCP image |
| 69 | images/WHITE FONT LOGO.png | God Squad | correct; file name contains spaces (see the ASSET register) |
| 76-78 | icon-search / account / cart | Search / Account / Cart | names a control on a non-control (HTML-04) |
| 110 | `{{ p.img }}` | `{{ p.name }}` | product alt = product name — correct pattern; the raw template triggers a 404 before render (see the ARCH/JS register) |
| 126 | ./01-hero-model-mu98p88t-7jig.webp | God Squad community | mismatch: the file shows one capped model with baked-in headline fragments (findings-verified.json C1; see the STORY register) |
| 145 | `{{ v.icon }}` | `""` | decorative — correct |
| 155 | images/WHITE FONT LOGO.png | God Squad | second identical alt; acceptable |
| 160-161 | icon-facebook / icon-instagram | Facebook / Instagram | redundant with the link's aria-label |

Every image has an `alt` attribute (12 of 12), which is the one clean result in this section. No image carries `width`, `height`, `srcset`, `sizes`, `loading` or `decoding` (evidence-render.md), so the browser cannot reserve space or choose a responsive candidate (HTML-06, severity MEDIUM). Resolution and weight of the files themselves are in the ASSET/PERF register.

### 4.7 Forms

None: 0 `<form>`, 0 `<input>` (css-html-stats.txt). There is no search field, newsletter capture, cart form or variant form, so nothing exists to migrate and every form will be authored fresh in Liquid (the feature gaps are classified in the ECOM register).

### 4.8 Duplicate attributes

Verified none across all 116 start tags (css-html-stats.txt). Lines 104 and 132 carry both `style` and `style-hover`; these are distinct attribute names, not duplicates.

### 4.9 Invalid and nonstandard attributes and elements

| Construct | Count | Lines | Purpose | Validity | Port action |
|---|---|---|---|---|---|
| `<x-dc>` | 1 | 9 | runtime root; hidden until React mounts (support.js lines 1818-1822) | custom element, unknown semantics | REMOVE |
| `<helmet>` | 1 | 10 | container the runtime hoists into `<head>` | nonstandard element | REMOVE; move children to `<head>` |
| `<sc-for list as hint-placeholder-count>` | 3 | 107, 115, 143 | loop over products / swatches / values | nonstandard element + attributes | REPLACE with `{% for %}` (see the ARCH/JS register) |
| `<sc-if value hint-placeholder-val>` | 2 | 110, 145 | conditional render | nonstandard | REPLACE with `{% if %}` |
| `style-hover` | 2 | 104, 132 | runtime generates `.scp0:hover` / `.scp1:hover` rules with `!important` (support.js lines 428-429, 1567-1589) | nonstandard attribute; works only under support.js | REPLACE with CSS `:hover` (CSS-07) |
| `data-screen-label` | 4 | 64, 98, 125, 142 | Claude Design screen label; not read by CSS or runtime (evidence-render.md) | valid `data-*`, editor-only | REMOVE |
| `data-r` | 26 occurrences, 25 distinct | 58-163 | editor hooks doubling as the only CSS selectors (34 selector uses) | valid `data-*`, misused as styling hooks | REPLACE with classes (CSS-03) |
| `data-dc-script`, `data-props`, `type="text/x-dc"` | 1 | 169 | data + editor prop schema (`currency` enum ₱/$/€) | nonstandard script type | REPLACE with Liquid objects and settings (DATA register) |
| `{{ … }}` in `src`, `alt`, text and `style="background:{{ s }}"` | 15 occurrences (11 distinct expressions) | 107-147 | interpolation | collides with Liquid delimiters | see the ARCH/JS register |
| `background:#0230` | 2 | 69, 155 | 4-digit hex = rgba(0,34,51,0) (findings-verified.json TECHNICAL-10) | valid CSS Color 4, but alpha 0: dead | REMOVE (CSS-06) |

Collectively these mean the markup cannot be copied into a `.liquid` file as-is; it must be transcribed (HTML-05, severity MEDIUM; the runtime dependency itself is the ARCH/JS register's blocker).

### 4.10 Unnecessary wrappers and layout markup

- Two empty `<div data-r="spacer">` grid-column placeholders (lines 89, 134), hidden again under 900px (line 28); grid placement (`grid-column`) makes them unnecessary (HTML-08).
- The 1440px wrapper (line 55) carries the page background and `overflow:hidden`; because section backgrounds sit inside it, nothing is full-bleed above 1440 (the 1920 outcome is in the RESP register; the structural fix — full-width sections with an inner container — belongs to HTML-08 and the CSS architecture in §5.13).
- Two logo wrapper `<div>`s exist only to carry the dead `#0230` background (lines 69, 155).
- The hamburger is three inline-styled `<span>`s (line 75), the identical string repeated 3 times (css-html-stats.txt).
- Twelve `<br>` elements set line breaks inside the two h2s, the hero and story taglines and the footer (lines 87, 91, 93, 101, 103, 130, 136, 156); the h1 carries none. Copy that becomes a Theme Editor setting cannot carry them, and they fight `text-wrap:balance` (HTML-07).
- After render the runtime adds 137 `data-dc-tpl` attributes and 14 `.sc-interp` spans (findings-verified.json TECHNICAL-7); this bookkeeping disappears with the runtime (ARCH/JS register).
- Running text is almost entirely `<div>`/`<span>`: the story paragraph (line 131) is the only `<p>` in the document (HTML-12).

### 4.11 Accessibility and maintainability at the markup level

Markup-level accessibility problems are: no `main`/`header` landmarks and unnamed sections (HTML-01), no `lang` (HTML-02), a two-level outline that omits products and values (HTML-03), controls built from `<span>`/`<img>` with zero `<button>`s (HTML-04), swatches as nine empty `<span>`s with no name (findings-verified.json TECHNICAL-5; labelling is in the A11Y register), unlabelled arrow glyphs, and no skip link (A11Y register). Keyboard reach, focus styling and contrast are measured in the A11Y register.

Maintainability: the file is 190 lines and readable, and its six HTML comments (`<!-- announcement -->` … `<!-- footer -->`, lines 57, 63, 97, 124, 141, 152) plus `data-screen-label` give a usable section map for the port. Against that, every visual property is co-located with content in 77 `style` attributes, copy is inline with hard line breaks, and only two elements have ids. The content and structure are KEEP as the design baseline; the markup itself is REBUILD.

### 4.12 Severity summary

| ID | Finding | Severity |
|---|---|---|
| HTML-01 | No `header`/`main`; nav nested in the hero; announcement bar is a div; sections unnamed | HIGH |
| HTML-02 | `<html>` has no `lang` | MEDIUM |
| HTML-03 | Outline stops at two h2s; product names and value titles are divs; values section has no heading | HIGH |
| HTML-04 | Zero `<button>`; hamburger is a role-less span with aria-label; search/account/cart are bare images | HIGH |
| HTML-05 | Runtime-only elements and attributes (x-dc, helmet, sc-for, sc-if, style-hover, data-screen-label, hint-*) | MEDIUM |
| HTML-06 | No width/height/srcset/sizes/loading/decoding on any of 12 images | MEDIUM |
| HTML-07 | Twelve `<br>` layout breaks, including inside both h2s and every multi-line tagline | MEDIUM |
| HTML-08 | Spacer divs, dead-background logo wrappers and a background-carrying 1440 wrapper | LOW |
| HTML-09 | Stylesheet, font link and preconnect live in the body inside `<helmet>` | MEDIUM |
| HTML-10 | Nav links are bare anchors in a div with no list and no `aria-label` on `<nav>` | MEDIUM |
| HTML-11 | Alt text quality: story alt describes the wrong picture; control-like alts on inert images; doubled social names | LOW |
| HTML-12 | Only one `<p>`; all other running text in generic elements | LOW |

No CRITICAL markup issue exists in isolation; the CRITICAL item is the runtime and template dialect that the markup depends on, recorded once in the ARCH/JS register and cross-referenced in §26.1.

## 5. CSS Audit

### 5.1 Where the CSS lives

| Source | Size | Rules / declarations | Location |
|---|---|---|---|
| Inline `style=""` attributes | 77 attributes, 6,421 chars (≈69% of all authored CSS) | 0 `!important` | throughout lines 55-164 |
| Embedded `<style>` | 2,916 B | 36 rules: 5 base (lines 14-17), 26 in `@media (max-width:900px)` (lines 19-44), 5 in `@media (max-width:520px)` (lines 47-51); 32 rules keyed on `[data-r=…]` (34 selector uses); 55 `!important` | inside `<helmet>` in `<body>` (lines 13-53) |
| Runtime-generated | 2 hover rules + 1 hide rule | `.scp0:hover{background:rgb(42,40,35)!important;color:rgb(243,239,230)!important}`, `.scp1:hover{background:rgb(230,211,166)!important;color:rgb(13,12,10)!important}`, `x-dc{display:none!important}` | inserted into `<head>` by support.js (lines 1567-1589, 1818-1822) |
| External | Google Fonts CSS 7,461 B | 19 `@font-face` blocks | `<link>` in the body (line 12) |
| Classes | 0 in source | runtime adds `scp0`/`scp1` only | — |

(css-html-stats.txt; bundle-sizes.txt; evidence-render.md; God Squad Website.html lines 14-51.) The consequence of this split is a cascade that runs backwards: every layout property is set inline at specificity 1,0,0,0, so the responsive layer can only win with `!important`. Of the 55 `!important` declarations, 48 override a property that is also set inline on the same element, which is why they are needed at all; the other 7 (the dead `[data-r=pad]` pair on line 19, `min-height` on hero-img and story-img on lines 21 and 36, `height` on hero-fade and story-fade on lines 22 and 37, `flex-direction` on the footer on line 42) target properties with no inline value and were flagged by habit. Conversely, every un-flagged declaration in the queries (`order` on lines 21, 29, 36; `gap` on line 25; `display` on lines 26, 28, 31, 44; `flex-direction`/`gap` on line 31; `border-bottom` on line 41; `flex-wrap` on line 43; `flex-direction`/`gap`/`text-align` on line 50) targets a property that its element does not set inline. This is CSS-02 and CSS-03.

### 5.2 Duplicated declarations and identical style strings

| Kind | Evidence |
|---|---|
| Identical inline strings | `width:22px;height:2px;background:#f3efe6;display:block` ×3 (hamburger bars, line 75); `height:24px;width:auto` ×3 (utility icons, lines 76-78); `display:inline-flex` ×2 (social links); `height:28px;width:28px` ×2 (css-html-stats.txt) |
| Repeated declarations (4+ times inline) | `display:flex` ×22, `text-transform:uppercase` ×20, `align-items:center` ×14, `width:auto` ×7, `position:relative` ×7, `flex-direction:column` ×7, `background:#0d0c0a` ×6, `background:#f3efe6` ×6, `letter-spacing:.3em` ×6, `position:absolute` ×6, `letter-spacing:.22em` ×5, `color:#d8c08a` ×5, `font-size:12px` ×5, `font-size:13px` ×5, `font-weight:600` ×5 (css-html-stats.txt) |
| Repeated font stacks | `'Playfair Display',Georgia,serif` written out 3 times (lines 84, 101, 130) |
| Duplicate inline/media value | `object-position:center 30%` is inline on the hero image (line 65) and repeated with `!important` in the 900px query (line 23); the value is identical, so the rule is redundant |
| Split rule | `[data-r=hero-img]` is declared twice in the same query (lines 21 and 23) |
| Parallel near-identical rules | hero-img/hero-fade (lines 21-22) and story-img/story-fade (lines 36-37) differ only in `62vw/320px` vs `60vw/280px` — one media-band component with two parameters |

The eyebrow (13px, `.3em`, uppercase), the tracked caption (14px, `.3em`), the label (12px, `.2-.22em`, 600) and the CTA (12px, `.22em`, padding `16px 26px`, `inline-flex`, gap 12px) each recur as complete inline recipes; they are the components the design system in Phase 2 should name.

### 5.3 Media queries and breakpoints

| Query | Rules | `!important` | What it does |
|---|---|---|---|
| base | 5 | 0 | reset, body colours, `a` colour/underline reset, `a:hover` gold, hamburger hidden |
| `@media (max-width:900px)` | 26 | 49 | hero and story become single-column with in-flow image bands (`62vw`/`60vw`, min 320/280px) and section-anchored fades; nav goes in-flow with `order:-2`; nav links hidden, hamburger shown; logo 56px; drop/story/footer padding to 24px; products and values 2-up; footer stacks; `[data-r=pad]` gutter rule (dead) |
| `@media (max-width:520px)` | 5 | 6 | products and values 1-up; value `border-right:none`; announcement bar stacks and centres with 16px padding; hero-side stacks |

Behaviour at the boundary: 900px applies the mobile rules, 901px the desktop rules (measurements.md 900/901; breakpoint-900.png, breakpoint-901.png). Findings on the system itself (per-width outcomes are the RESP register's):

- Two states only, both `max-width`, no `min-width`: the design is desktop-first and 768px tablets receive phone rules with 2-up grids (measurements.md 768; tablet-768.png), while the 901-1023 band receives the full three-column hero with 8.5vw type and wraps everything (measurements.md 920; band-920.png). There is no intermediate step for 1024-1279 laptops, where the h1 stacks on three lines (findings-verified.json FIDELITY-2). CSS-04.
- Dead rule: the first rule of the 900px query targets `[data-r=pad]`, and no element carries `data-r="pad"` (css-html-stats.txt "hooks styled in `<style>` but absent from markup: ['pad']"). The announcement bar therefore keeps its inline `padding:12px 48px` between 521 and 900px while every other section moves to 24px (measurements.md 768; findings-verified.json RESPONSIVE-6). CSS-05.
- Three gutter values coexist: 48px desktop (inline), 24px under 900 (query), 16px for the announcement bar under 520 (line 50). CSS-09.
- Visual reordering with `order:-2`/`order:-1` (lines 21, 29) is what puts the nav in flow above the hero image, while `[data-r=hero-fade]{top:0;height:max(62vw,320px)}` (line 22) stays anchored to the section; the 88px offset this produces at every width under 900 is measured and owned in the RESP register (measurements.md; findings-verified.json RESPONSIVE-1). The mechanism — a fade positioned against a container that the nav also occupies — is a direct cost of HTML-01.
- No `prefers-reduced-motion` query (css-html-stats.txt). There are 0 transitions and 0 animations; the only two `transform` uses are static rotations of the script caption (lines 27, 91), and the remaining 20 hits in the stats' substring count are `text-transform:uppercase`. Nothing needs the query today; the design system must add it before any motion is introduced.
- `border-right:none` for value tiles exists only in the 520px query (line 49), so the 2-up tablet grid paints a stray rule at the viewport edge (RESP register, RESPONSIVE-5).

### 5.4 Hardcoded colour inventory

| Literal | Occurrences | Role (inferred from use) | Token status |
|---|---|---|---|
| `#0d0c0a` | 14 in the stats block; 18 on a whole-file grep (15 in markup and style, 3 as swatch data in lines 175-177) | ink / page background | primary — needs token |
| `#f3efe6` | 9 (13 whole-file) | cream / text on ink | primary — needs token |
| `#d8c08a` | 10 | gold accent, CTA, active nav, badge | primary — needs token |
| `#bdb6a8` | 3 | muted caption text (value subs, footer) | BUSINESS INFORMATION REQUIRED — approved brand value or prototype improvisation |
| `#ebe6dc` | 1 | product tile background (never paints, findings-verified.json FIDELITY-3) | BUSINESS INFORMATION REQUIRED |
| `#e9e4d8` | 1 | story paragraph colour | BUSINESS INFORMATION REQUIRED |
| `#2a2823`, `#e6d3a6` | 1 each, only inside `style-hover` (lines 104, 132) | CTA hover shades | undocumented; BUSINESS INFORMATION REQUIRED |
| `#4b5443` | 3, swatch data only | olive colourway | product data (DATA register) |
| `#0230` | 2 | none (alpha 0) | dead (CSS-06) |
| `rgba(13,12,10,…)` at 0 / .1 / .15 / .55 / .75 / .8 / .92 (7 variants) | 12 | gradient stops and fades | derive from the ink token |
| `rgba(255,255,255,.08/.1/.2)` (3 variants) | 6 | hairline borders and divider | derive from a `--line` token |
| `rgba(0,0,0,.25)` | 1 | swatch ring | derive |

(css-html-stats.txt COLOURS block; God Squad Website.html; findings-verified.json TECHNICAL-11 grep counts.) Eighteen distinct literals in the stats block (3 primary, 3 secondary, the dead `#0230`, 11 rgba variants), 21 once the two `style-hover` shades and the swatch olive are counted — for what is a three-colour brand. Nothing can be driven by `settings_schema.json` until they become custom properties (CSS-01, severity HIGH).

### 5.5 Hardcoded typography inventory

| Property | Values in use (count) |
|---|---|
| `font-family` | `'Jost',Helvetica,Arial,sans-serif` (body, 1); `'Playfair Display',Georgia,serif` (3, inline on each heading); `'Kaushan Script',cursive` (1) |
| `font-size` | 9px (1, cart badge), 11px (4), 12px (5), 13px (5), 14px (4), 15px (1); `clamp(56px,8.5vw,112px)` h1; `clamp(40px,4.6vw,64px)` h2 drop; `clamp(32px,4vw,40px)` h2 story; `clamp(30px,3vw,44px)` script |
| `font-weight` | 400 (default), 500 (3), 600 (5), 900 (3); Playfair 700 is requested by the font URL but never used (evidence-render.md) |
| `letter-spacing` | `.3em` (6), `.22em` (5), `.2em` (3), `.26em` (2), `.24em` (1), `-.01em` (2) |
| `line-height` | .88, .9, 1.05, 1.1, 1.65 (2), 1.7, 1.75, 1.8, 1.9 |
| `text-transform:uppercase` | 20 |

(css-html-stats.txt.) Six body sizes between 9 and 15px with no size at or above 16px, six tracking values that differ by hundredths of an em, and nine line-heights: a scale exists implicitly but is not named anywhere (CSS-08). Whether the 11-13px tracked caps are brand-mandated on phones is BUSINESS INFORMATION REQUIRED (the mockup uses them; findings-verified.json RESPONSIVE-11).

### 5.6 Hardcoded spacing, grid and border inventory

| Property | Distinct strings | Notes |
|---|---|---|
| `padding` | 22 | 9 carry `!important` (11 occurrences); gutters 48 / 24 / 16px; hero copy `170px 48px 56px`, hero side `190px 48px 56px 0` exist only to clear the absolute nav |
| `margin` | 14 | 14px (3), 36px (2), 26px 0 0 (2), 38px 0 26px, 36px 0 30px, 30px 0 22px … |
| `gap` | 17 | 5, 6, 8, 10, 12, 18, 20, 24, 26, 28, 32, 36, 40, 44px |
| `grid-template-columns` | 7 | bespoke fr ratios per section: `1.1fr 1.1fr .7fr` (hero), `.9fr 2.4fr` (drop), `.9fr 1.6fr .4fr` (story), `repeat(3/4,…)` |
| `border` | 6 | four hairline variants |
| distinct px values anywhere | 44 (from -10 to 1440) | (css-html-stats.txt) |

No base unit is observable (values include 5, 6, 18, 22, 26, 38, 44px). This is CSS-09, and it is the reason the Phase 2 spacing scale must be derived from the mockup rather than from the code.

### 5.7 `!important` usage (55)

All 55 are in the `<style>` block (0 inline): 49 in the 900px query and 6 in the 520px query (God Squad Website.html lines 19-51; css-html-stats.txt). The runtime adds four more in the generated hover rules and one on `x-dc`. They are not stylistic excess; they are structurally required by inline styling (see 5.1 — 48 of the 55 override an inline value). The cost is that nothing downstream can override them — a Theme Editor colour scheme or a section padding setting emitted as a custom property would lose to them — so the responsive layer cannot be carried into the theme in any form (CSS-03, severity HIGH).

### 5.8 Nonstandard attributes used for styling

`style-hover` (2) drives hover through the runtime; `data-r` (25 distinct hooks, 26 occurrences, 34 selector uses) is the only selector system and is editor metadata by origin; `style="…background:{{ s }}…"` (line 116) interpolates data into an inline style, which would be a Liquid `{{ s }}` on the Shopify side but is not a maintainable pattern for swatches; `data-screen-label` and `hint-placeholder-*` are inert (evidence-render.md). None survives the port (HTML-05, CSS-03).

### 5.9 Hover, focus and interaction states

| Element | Hover | Mechanism | Focus |
|---|---|---|---|
| Nav links Shop / Collections / Our Story / Verse | text turns gold | global `a:hover{color:#d8c08a}` (line 16) | browser default ring only |
| Nav link Home | no visible change (already gold) | same rule | default |
| View All Products CTA | background `#0d0c0a` → `#2a2823` | runtime `.scp0:hover` with `!important` (support.js 428-429, 1567-1589; evidence-render.md) — works, but only under support.js | default |
| Our Story CTA | background `#d8c08a` → `#e6d3a6` | runtime `.scp1:hover` — works under support.js | default |
| Facebook / Instagram links | none (`color` cannot tint a PNG) | — | default |
| Hamburger, search, account, cart | none; not interactive | — | unreachable |
| Swatches | none | — | not focusable |

Additional facts: `a{text-decoration:none}` (line 16) removes the underline affordance from all nine links (CSS-11); there are no `:focus`/`:focus-visible` rules, no `transition`, no `:active` and no `aria-current` mechanism (css-html-stats.txt; evidence-render.md). The CTA hover works under support.js through the `style-hover` attribute (findings-verified.json TECHNICAL-2), but it lives in a Claude-Design-only attribute and must be re-expressed as ordinary CSS. The interaction-state system as a whole is fragmentary and undocumented (CSS-07; keyboard and contrast measurements are in the A11Y register).

### 5.10 Responsive behaviour (mechanics)

Desktop: hero and story images are absolutely positioned covers (`position:absolute; object-fit:cover`, lines 65, 126) under absolutely positioned gradient overlays (lines 66, 127), with copy columns laid out by grid over them. Under 900px the images become in-flow bands sized in `vw` with px minimums and no `vh` cap (lines 21, 36), the fades are re-anchored to the section top (lines 22, 37), grids collapse via `!important`, and fixed px type stays fixed while only the four `clamp()` sizes scale. The 520px query then forces single columns. Measured outcomes at 375-1920 (fade offset, orphaned captions, product upscale, footer stacking, dark gutters at 1920) are in the RESP register; the CSS-level causes are CSS-03, CSS-04, CSS-05 and HTML-01. No horizontal overflow occurs at any tested width (findings-verified.json C11), and the modern idioms used — `clamp()`, `aspect-ratio`, `inset`, `max()`, `object-fit`, grid `minmax()` — are sound and should be kept in the rewrite. `text-wrap:balance` (line 84) and `overflow-wrap:anywhere` (line 101) need the support matrix confirmed (CSS-10; BUSINESS DECISION REQUIRED).

### 5.11 Dead and redundant declarations

`[data-r=pad]` rule (line 19, no matching element); `background:#0230` ×2 (lines 69, 155); `flex-wrap:wrap` on a `display:grid` container (line 98, no-op); the duplicated `object-position` (line 23); `[data-r=hero-img]` split across two rules (lines 21, 23). Small, but they show the style block was accreted, not designed (CSS-05, CSS-06).

### 5.12 Maintainability and migratability verdict

| Layer | Verdict | Reason |
|---|---|---|
| Design values (palette, type families, clamp ranges, gradient recipes, section ratios) | KEEP as the token source | they are the approved look (desktop-1440.png matches the mockup in palette, type and order; evidence-render.md) |
| Inline `style` attributes (6,421 chars) | REPLACE | 69% of the CSS, zero classes, unthemeable |
| `<style>` responsive layer (2,916 B, 55 `!important`, `data-r` hooks) | REPLACE | cannot be overridden or carried into sections |
| `style-hover` / runtime pseudo sheet | REPLACE with CSS | works only under support.js |
| Google Fonts `<link>` in body | REPLACE | see the PERF and SEO registers |
| Modern CSS idioms | KEEP | `clamp`, `aspect-ratio`, grid `minmax`, `object-fit` |

Verdict: the CSS cannot reasonably be migrated; it must be rewritten. The good news is scale: the entire authored style surface is about 9.3 KB and 36 rules, so the rewrite is small and the real work is extraction of tokens and components, which Phase 2 owns.

### 5.13 Recommended future CSS architecture

1. Tokens as CSS custom properties on `:root`, emitted by `layout/theme.liquid` from `settings_schema.json` (colour scheme groups, `font_picker` settings): `--color-ink:#0d0c0a`, `--color-cream:#f3efe6`, `--color-gold:#d8c08a`, plus `--color-muted`, `--color-tile`, `--color-body-copy`, `--color-gold-hover`, `--color-ink-hover` once their values are confirmed (BUSINESS INFORMATION REQUIRED); alpha variants derived with `rgb(var(--ink-rgb) / .55)` rather than 11 separate rgba literals. Typography tokens `--font-heading` (Playfair Display 900), `--font-body` (Jost 400/500/600), `--font-script` (Kaushan Script); a named size scale (`--text-xs 11px … --text-md 15px`, four fluid heading clamps); three tracking tokens (`.2em`, `.22em`, `.3em`); a 4px-based spacing scale with a `--gutter` that steps 16 / 24 / 48px and a `--page-max: 1440px` applied to inner containers only, so section backgrounds are full-bleed.
2. Files: `assets/base.css` (reset, tokens fallback, typography, buttons, focus-visible, utilities) loaded in the layout; one stylesheet per section (`section-announcement.css`, `section-header.css`, `section-hero.css`, `section-featured-collection.css`, `section-our-story.css`, `section-brand-values.css`, `section-footer.css`) loaded from within the section via `{{ 'section-hero.css' | asset_url | stylesheet_tag }}`; component files for `product-card`, `button`, `icon`, `swatch`.
3. Naming: BEM-ish block/element/modifier (`.hero`, `.hero__media`, `.hero__fade`, `.hero__copy`, `.hero__side`; `.product-card__media`, `.product-card__title`, `.product-card__price`; `.button--gold`), state via `.is-active`/`[aria-current="page"]`, no `data-r` hooks, no ids for styling.
4. Mobile-first: base rules are the phone layout; `@media (min-width: 750px)` and `@media (min-width: 990px)` (Shopify Dawn's steps) replace `max-width:520/900`, with an optional `min-width: 1200px` step for the hero copy column so the h1 can hold its two-line lockup. Map: today's ≤520 → base; 521-900 → 750+; ≥901 → 990+. The steps are defined in Phase 2 and their outcomes verified in Phase 9 (CSS-04).
5. No `!important` anywhere; the only inline styles are Liquid-generated custom properties on a section root (for example `style="--section-padding-top: {{ section.settings.padding_top }}px"`), which is the OS 2.0 convention.
6. Interaction states defined once in `base.css`: `:hover`, `:focus-visible` (2px gold outline with offset), `:active`, `transition` on colour/background only, wrapped in `@media (prefers-reduced-motion: no-preference)`.
7. Header as its own section inside the header section group (alongside the announcement-bar section), with a fixed, measurable height; the hero owns its own media and fade inside one relative container so no overlay is ever anchored to a parent the header shares (retires the hero-fade offset by construction).
8. Fonts from `font_picker` settings via `font_face` with `preload`, or self-hosted subsets in `assets/`; no Google Fonts `<link>`, no unused weights.

## 6. JavaScript Audit

### 6.1 Purpose of support.js

`support.js` (69,150 bytes, 1,911 lines; 19,037 bytes gzipped) is the Claude Design **dc-runtime**: a generated IIFE bundle ("GENERATED from dc-runtime/src/*.ts — do not edit. Rebuild with `cd dc-runtime && bun run build`", support.js line 1) whose job is to (a) turn a `.dc.html` document into a React tree in the browser and (b) stay connected to the Claude Design editor so templates, logic and props can be streamed in and mapped back to source nodes. It is not application code written for God Squad; the only God Squad-specific JavaScript in the project is the 18-line `Component` class inside the HTML (God Squad Website.html lines 170-187), which is data, not behaviour.

### 6.2 Dependencies

| Dependency | How it is loaded | Required for this page | Notes |
|---|---|---|---|
| React 18.3.1 UMD | `loadReactUmd()` injects a `<script>` from unpkg with SRI and `async=false` (1838-1847) | Yes, hard requirement: `getReact()` throws without it (9-13) | Overridable only via `window.__resources` (1149-1153), which nothing sets |
| ReactDOM 18.3.1 UMD | same, appended in the same `Promise.all` (1843-1846) | Yes | `createRoot` preferred, `render` fallback (196-198) |
| @babel/standalone 7.29.0 | `ensureBabel()` on first `.jsx/.tsx` `<x-import>` (1176-1192) | No: no `<x-import>` on this page | 3.1 MB latent dependency |
| `window.__resources`, `window.__resourceBlobs` | read in `cdnScriptFor`, `bundledBlob`, `ensureFetched`, helmet (1136-1140, 1149-1153, 1455-1457, 1647-1650) | No | Export-bundle hooks; absent here, which is also why `boot()` re-fetches the document (158) |
| Google Fonts | authored in `<helmet>`, cloned to head by the runtime | Yes for typography | Not a JS dependency but a runtime-mediated one (ARCH-04) |

### 6.3 Runtime architecture (module map)

| Source module (from the bundle's comments) | Lines | Role | Exercised by this page |
|---|---|---|---|
| react.ts | 8-21 | `getReact`/`getReactDOM`/`h` wrappers | Yes |
| parse.ts | 23-83 | `parseDcDocument`, `parseDcText`, `parseDataProps`, `dcNameFromPath` | Yes |
| boot.ts | 85-200 | BASE_CSS (placeholder shimmer + print rules), `boot()` with self-fetch and React mount | Yes (shimmer CSS unused) |
| expr.ts | 202-294 | Custom expression resolver: paths, `[ ]` indexing, `== != === !==`, `!`, literals; no arithmetic, no filters | Yes |
| encode.ts | 296-412 | Tag/attribute encoding for the HTML parser (`sc-camel-*`, `sc-raw-*`, `sc-helmet`), EVENT_MAP, `cssToObj`, `compileAttr` | Partly (no events, no camel attrs, no tables) |
| compile.ts | 414-814 | Template walker: `collectProps`, `walkFor`, `walkIf`, `walkText`, `walkElement`, plus `walkComponent`, `walkXImport`, deck-stage keying, content-keyed React keys | `walkFor`/`walkIf`/`walkText`/`walkElement` yes; `walkComponent`, `walkXImport`, deck helpers (486-549, 661-770) no |
| logic.ts | 816-851 | `StreamableLogic` (= `DCLogic`) base class; `evalDcLogic` via `new Function` | Yes |
| component.ts | 853-1133 | `StreamableComponent` (error boundary, logic hot-swap, streaming flags, circular-import guard), `Placeholder`, `getDC` dispatcher | Yes for mount; error/streaming branches idle |
| bundled.ts, cdn.ts | 1135-1153 | Export-bundle blob lookup; CDN URLs and SRI | cdn yes; bundled no |
| external.ts | 1155-1354 | `<x-import>` loader: Babel, `fetch` + `new Function` module eval, global polling (50 ms, 30 s timeout) | No |
| atomics.ts | 1356-1360 | Utility-class CSS injected only for `data-dc-atomics` helmets | No |
| helmet.ts | 1362-1495 | Clones `<link>/<meta>/<script>` into head; design-doc canvas mode; `postMessage` to parent; `message` listener | Clone path yes; canvas/theme messaging no |
| pseudo.ts | 1497-1589 | `style-*` attributes -> generated `.scpN:pseudo` rules with `importantify()` | Yes (two CTAs) |
| registry.ts, runtime.ts | 1591-1789 | Per-component registry with subscriptions; `ensureFetched` sibling `.dc.html` fetch; `updateHtml`/`updateJs`/`dcUpdate`/`setProps` streaming API | Registry and update paths yes; sibling fetch and streaming no |
| stream-state.ts | 1791-1815 | Stale-stream tracker | No |
| index.ts | 1817-1911 | `hideRawTemplate`, `loadScript`, `loadReactUmd`, `init` (window API, `__dc_booted` postMessage), entry | Yes |

**Event handling.** `EVENT_MAP` (317-359) maps `on*` attributes to React handler props inside `collectProps` (438-439); the markup carries no `on*` attribute, so no UI handler is ever attached. The runtime's only listeners of its own are the editor `message` listener (1407-1419, see JS-05) and the `DOMContentLoaded` hook that triggers boot (1904). There is no custom event system, no delegation and no keyboard handling anywhere in the bundle.

By line range, roughly 600 of the 1,911 lines (about a third: external.ts, deck helpers, `walkComponent`/`walkXImport`, `Placeholder`, stream tracker, canvas/theme messaging, sibling fetch, streaming/props update API, atomics, bundled, shimmer and print CSS) are code paths this page never enters. The remainder exists to do what Liquid does server-side: loop over three products and four values and substitute strings.

### 6.4 Bundle sizes

| File | Raw bytes | Gzip bytes | Executed on this page |
|---|---|---|---|
| support.js (local) | 69,150 | 19,037 | Yes |
| react.production.min.js 18.3.1 | 10,751 | 4,263 | Yes |
| react-dom.production.min.js 18.3.1 | 131,835 | 42,818 | Yes |
| God Squad Website.html | 15,632 | 4,081 | Yes (fetched twice, JS-03) |
| @babel/standalone 7.29.0 | 3,137,752 | 653,872 | No (latent) |
| **JS executed per load** | **~211,736** | **~66,118** | all effectively render-blocking (measurements.md line 30) |

(bundle-sizes.txt.) For comparison, the Liquid rebuild of this homepage needs no framework: the same DOM is 166 elements (measurements.md line 21) and the real behaviours it lacks today (menu toggle, cart drawer) are ordinary theme JavaScript. Target budget for the theme's own JS: under 20 KB gzipped, to be verified in PHASE 12 — PERFORMANCE.

### 6.5 Functionality unnecessary for a store

| Feature | Lines | Why it exists | Store relevance |
|---|---|---|---|
| Hide-until-React (`x-dc{display:none!important}`) | 1818-1822, 1906 | Prevent flash of raw template in the editor | Harmful: blank page on CDN failure, JS-gated first paint (ARCH-03, JS-02) |
| Document self-fetch and second render | 158-164 | Refresh from raw text when not running from an export bundle | Pure overhead (JS-03) |
| Streaming placeholders, shimmer CSS, `hint-placeholder-*`, `sc-missing`/`sc-unresolved` spans, `sc-dc-streaming` class | 86-131, 583-601, 614-631, 653, 862-882, 1725-1739, 1791-1815 | Show skeletons while the editor streams a template | None |
| `<x-import>` + Babel + `new Function` module eval + 30 s global polling | 690-770, 1155-1354 | Import external React components/JSX | None (and a 3.1 MB latent download) |
| `<dc-import>` sibling components and `ensureFetched` `.dc.html` fetch | 661-689, 1642-1685 | Multi-component design projects | None; the sibling URL convention (`<name>.dc.html`, line 1646) is unused on this page (INV-02) |
| deck-stage slide keying (`data-om-slide-id`) | 486-549 | Slide-deck documents | None |
| Design-doc canvas mode, theme sync, `__dc_probe` | 1363-1419 | Editor canvas background | None |
| Editor bridge API on `window` (`__dcUpdate`, `__dcSetProps`, `__dcAnnotatedTemplate`, `__dcRegistry`, ...) and `__dc_booted` postMessage | 1854-1901 | Editor pushes template/logic/props into the live page | None; unauthenticated write surface (JS-05) |
| `data-dc-tpl` stamping (137 attributes in the rendered DOM) and `.sc-interp` wrappers (14) | 472-477, 607, 799 | Map rendered nodes back to source | DOM noise (TECHNICAL-7) |
| Content-keyed React keys (`contentKey`) | 771-791 | Stable keys across streamed edits | None |
| Print baseline CSS | 117-130 | Deck export | None |
| `style-*` pseudo-class generator | 1497-1589 | Author hover/focus inline | Must be replaced by CSS (JS-07) |

### 6.6 Shopify compatibility

- **Template syntax collision.** The runtime's `{{ }}` interpolation is the same as Liquid's output tag. A `.liquid` section containing `{{ products }}` or `{{ p.name }}` compiles on Shopify but outputs empty strings, and `<sc-for>`, `<sc-if>`, `<x-dc>`, `<helmet>` remain as unknown elements (TECHNICAL-3; ARCH-02). There is no configuration that would let Liquid pass the template through untouched short of wrapping everything in `{% raw %}`, which defeats the purpose of a theme.
- **Rendering model.** Shopify sections are rendered server-side and re-rendered by the Theme Editor via the Section Rendering API; a client-side compiler that replaces the DOM after mount would break editor previews, section reordering and block selection. `DCLogic` classes have no counterpart in a theme's `{% schema %}`.
- **Data flow.** Product, collection, cart and menu data arrive as Liquid objects (`product.title`, `product.price | money`, `cart.item_count`, `linklists`); the runtime's `renderVals()` object literals cannot be fed by them (see §23).
- **Asset pipeline.** Theme JS lives in `assets/` and is loaded with `asset_url | script_tag` or `<script type="module">`; loading React from unpkg at runtime is possible but pointless here and would keep first paint dependent on a third-party origin (ARCH-03).
- **Theme Editor.** The `data-props` currency enum is the runtime's substitute for settings; Shopify replaces it with `settings_schema.json` and section/block settings (DATA-02).

Net: zero compatibility. Nothing in support.js should be adapted, wrapped or ported.

### 6.7 Maintainability

The file is a generated, unminified IIFE bundle (module banners such as `// src/boot.ts`, prose comments at lines 117-118, 821, 897-914 and 1879-1889) whose TypeScript sources (`dc-runtime/src/*.ts`, line 1) are not in the project; the owner cannot rebuild it. It is single-purpose to the Claude Design product and versioned nowhere in the project. The template it compiles has zero classes and 77 inline styles, so any behaviour change requires touching the runtime or the template, both of which are outside normal front-end tooling. Debuggability is poor: failures surface as `[dc-runtime]` console errors or a red `.sc-logic-error` overlay (1056-1071), and warnings for unresolved holes are deduplicated (562-568) so silent empties are the norm. The rendered DOM carries editor bookkeeping (`data-dc-tpl`, `.sc-interp`) that would confuse any theme developer.

### 6.8 Security concerns

1. **Code evaluation.** `evalDcLogic` executes the `data-dc-script` text with `new Function` (842-851); `<x-import>` would execute fetched module source the same way (1216-1223). Both require `'unsafe-eval'` in any Content-Security-Policy and mean that whoever can edit the HTML can run arbitrary JS (JS-04). The risk is bounded today because the script is part of the same file, but it is architecture that must not be carried into a storefront.
2. **Cross-window messaging.** `postMessage(..., "*")` to `window.parent` for `__dc_booted` and `__dc_design_mode` (1384-1390, 1855-1866), and a `message` listener that acts on `__dc_theme`/`__dc_probe` from any origin without checking `e.origin` (1407-1419). Exposure is limited to theme/canvas toggling, but the pattern is wrong for a store (JS-05).
3. **Global write API.** `Object.assign(window, api)` exposes `__dcUpdate`, `__dcSetProps`, `__dcRegistry`, `DCLogic` (1871-1901); any script on the page or a same-origin frame can replace the template or props at runtime.
4. **Third-party runtime dependency.** React/ReactDOM come from unpkg.com with SRI (good) but with no fallback and no self-hosting; availability, not integrity, is the exposure (ARCH-03).
5. **innerHTML compile.** `compileTemplate` assigns `tpl.innerHTML = encodeCase(html)` (470) inside a `<template>`; safe for the author's own markup but another sign the bundle is an editor tool.

### 6.9 Replacement strategy

1. Phase 10: extract the **rendered** DOM (after React mount, with `data-dc-tpl`, `.sc-interp`, `scp0/scp1` and `x-dc` remnants stripped) as the markup reference, not the template source; rebuild each block as a Liquid section with schema.
2. Move the two CTA hover states and the `a:hover` gold into the Phase 2 stylesheet as ordinary `:hover` rules (JS-07).
3. Author the theme's own JavaScript from scratch, deferred and framework-free: menu toggle and drawer, cart drawer with the Ajax Cart API, product form/variant picker, predictive search, all re-initialising on the Theme Editor events `shopify:section:load` / `shopify:section:unload` (JS-08). Target budget: under 20 KB gzipped in total, to be verified in PHASE 12 — PERFORMANCE.
4. Serve fonts through `font_picker` settings or self-hosted `assets/` with preloads set in `theme.liquid` (ARCH-04).
5. Delete support.js, the unpkg loads and the `data-dc-script` block; keep a copy of the prototype in the archived baseline for comparison only.

### 6.10 Verdict

**REMOVE DURING SHOPIFY CONVERSION.** support.js is an editor runtime, not site code; it has no Shopify-compatible role, roughly a third of it is dead for this page, it gates first paint on a third-party CDN, and its only page-specific behaviour (string substitution for three products and four values) is exactly what Liquid provides natively. The two CTA hover rules are the sole visual behaviour to re-express in CSS.

## 7. Brand Audit

### 7.1 Verdict on the identity

The visual identity is coherent and should not be changed: a near-black ink, a warm cream and a muted gold, carried by Playfair Display 900 display type, tracked Jost caps and a single Kaushan Script accent, over low-key city photography. Section order, palette, typefaces, copy, the three-product grid, the four value tiles and the footer structure all match the approved mockup (evidence-render.md, Mockup vs render; 00-full-mockup-reference.webp; desktop-1440.png). What the audit finds is not a direction problem but a systematisation problem: every colour, size, tracking and spacing value is a raw literal in one of 77 inline `style` attributes or the 2,916-byte `<style>` block, with zero classes and no tokens (css-html-stats.txt SIZES). The design system in Phase 2 must name what already exists, not invent anything.

### 7.2 Colour

| Proposed token | Value | Count in source | Used for | Contrast on partner (computed from the hex pairs) | Classification |
|---|---|---|---|---|---|
| ink | #0d0c0a | 14 (css-html-stats.txt COLOURS) | page, hero, story, values, footer backgrounds; primary CTA fill; text on cream | 17.0:1 vs cream, 11.0:1 vs gold | KEEP UNCHANGED |
| cream | #f3efe6 | 9 | body text on ink, New Drop background, hamburger bars, rules | 17.0:1 vs ink | KEEP UNCHANGED |
| gold | #d8c08a | 10 | announcement text, eyebrows, active nav, h1 accent, hero rule, cart badge, accent CTA fill | 11.0:1 vs ink | KEEP UNCHANGED |
| muted | #bdb6a8 | 3 | value subtitles (line 147), footer taglines (lines 156, 164) | 9.7:1 vs ink | NEEDS STANDARDIZATION (no role name) |
| body-on-ink | #e9e4d8 | 1 | story paragraph (line 131) | 15.4:1 vs ink | NEEDS STANDARDIZATION (near-duplicate of cream) |
| tile | #ebe6dc | 1 | product media box (line 109) | n/a | INCONSISTENT — the box behind each product reads as a visible square (findings-verified.json FIDELITY-3) |
| olive | #4b5443 | data only (lines 175-177) | third swatch on every product | n/a | NEEDS STANDARDIZATION (variant colour has no name) |
| ink-hover / gold-hover | #2a2823 / #e6d3a6 | lines 104, 132 (`style-hover`) | CTA hover fills | 12.8:1 vs cream text / about 13:1 vs ink text | NEEDS STANDARDIZATION (exist only as editor attributes) |
| scrims | rgba(13,12,10, 0 / .1 / .15 / .55 / .75 / .8 / .92) | 7 alphas in 12 stops (css-html-stats.txt) | hero and story gradients (lines 66, 127; media rules lines 22, 37) | n/a | NEEDS STANDARDIZATION (four gradient recipes, none named) |
| hairlines | rgba(255,255,255, .08 / .1 / .2), rgba(0,0,0,.25) | 7 | announcement border, value borders, footer divider, swatch border | n/a | NEEDS STANDARDIZATION (three alphas for one hairline) |
| dead | #0230 | 2 (lines 69, 155) | logo wrapper, alpha 0 | n/a | REMOVE — see the CSS register |

The three brand colours are used exactly as the spec defines them, and the computed contrast of gold, cream and muted text on ink is comfortably above 4.5:1 wherever the background is solid. The only contrast failures are where text sits on the photograph without a solid backing (nav links over the hero sky, evidence-render.md) — that is a composition problem, logged as HERO-02, with the WCAG figures and classification in the A11Y register. Issues: BRAND-01 (core tokens), BRAND-02 (neutrals and scrims).

### 7.3 Typography

| Role | Face / weight | Size | Tracking | Line-height | Source line | Classification |
|---|---|---|---|---|---|---|
| Display XL (h1) | Playfair Display 900, uppercase | clamp(56px, 8.5vw, 112px) | -.01em | .88 | 84 | KEEP UNCHANGED (face); REFINE (lockup, HERO-03) |
| Display L (h2 New Drop) | Playfair 900, uppercase | clamp(40px, 4.6vw, 64px) | -.01em | .9 | 101 | KEEP UNCHANGED |
| Display M (h2 Story) | Playfair 900, uppercase | clamp(32px, 4vw, 40px) | 0 | 1.05 | 130 | REFINE (wraps 3-4 lines, STORY-05) |
| Script accent | Kaushan Script 400, rotate(-8deg) | clamp(30px, 3vw, 44px) | 0 | 1.1 | 91 | KEEP UNCHANGED |
| Eyebrow | Jost 400 (lines 83, 129) or 500 (line 100) | 13px | .3em | default | 83, 100, 129 | INCONSISTENT (weight varies; tracking is consistent) |
| Verse / tagline stack (hero) | Jost 400 | 14px | .3em | default / 1.65 / 1.7 | 85, 87, 93 | KEEP UNCHANGED |
| Tagline (New Drop) | Jost 400 | 13px | .24em | 1.75 | 103 | INCONSISTENT (a fifth caption device: 13px .24em where the hero taglines are 14px .3em) |
| Nav link | Jost 500 | 12px | .2em | default | 70 | KEEP UNCHANGED |
| Button label | Jost 500 (line 104) vs 600 (line 132) | 12px | .22em | default | 104, 132 | INCONSISTENT (weight differs per button) |
| Product name / price | Jost 600 / 600 | 12px / 14px | .2em / 0 | default | 112-113 | KEEP UNCHANGED |
| Value title / subtitle | Jost 600 / 400 | 13px / 11px | .22em / .2em | default | 146-147 | KEEP UNCHANGED |
| Announcement, footer taglines, story caption | Jost 400 | 11px / 11px / 12px | .22em / .26em / .22em | default / 1.9 / 1.8 | 58, 156, 164, 136 | INCONSISTENT (three trackings for one caption role) |
| Body | Jost 400 | 15px | 0 | 1.65 | 131 | REFINE (only paragraph on the page; below 16px on phones — see the RESP register) |
| Badge | Jost 600 | 9px | 0 | — | 78 | REFINE (UI-03) |

The stats confirm the spread: six fixed sizes (9, 11, 12, 13, 14, 15 px) plus four clamps, six letter-spacing values (.2, .22, .24, .26, .3, -.01em), nine line-heights (css-html-stats.txt FONT-SIZE / LETTER-SPACING / LINE-HEIGHT). Playfair Display 700 is requested but never used (evidence-render.md Fonts; findings-verified.json C12). The tracked-caps convention itself is the strongest brand device on the page and must be kept; it needs a fixed set of label roles rather than per-element tuning (BRAND-04).

One real defect sits inside the type system: the peso sign U+20B1 in every price and the arrow U+2192 in both CTAs are not in Jost's loaded faces, so the browser substitutes a per-platform glyph — measured by glyph width on this machine, and the mockup's ₱ is a sans glyph matching the digits (evidence-render.md Fonts; findings-verified.json critic addition on ₱/→; lines 104, 113, 132, 172-177; the substituted ₱ is visible next to the Jost digits in scratchpad/crops/d1440-price-row.png). Prices and buttons will therefore look different on Windows, macOS, iOS and Android (BRAND-03).

### 7.4 Spacing rhythm

There is no scale. Forty-four distinct px values of all kinds appear in the source (font sizes, widths, breakpoints, min-heights included; css-html-stats.txt DISTINCT PX VALUES), of which roughly two dozen are spacing values. Section paddings are 12/48 (announcement), 22/48 (nav), 170/48/56 and 190/48/56/0 (hero columns), 48/48/44 (New Drop), 56/48 (story), 44/24 (value tile), 26/48 (footer); gaps use 14 distinct values (17 listed entries) from 5px to 44px; margins use 14, 26, 36, 38 px in different combinations (css-html-stats.txt PADDING / GAP / MARGIN). The hero copy's 170px and 190px top padding exists only to clear the absolutely positioned nav (lines 68, 82, 90) — a structural coupling the HTML/CSS registers own, but its consequence for rhythm is that hero spacing cannot be expressed as a token. Classification: NEEDS STANDARDIZATION (BRAND-06). Most spacing values sit within one step of a 4/8-based ramp (4, 8, 12, 16, 24, 32, 48, 64, 96); the hero's 170/190px offsets are the exception and disappear once the header leaves the hero section.

### 7.5 Grid

A single 1440px centred wrapper (line 55) with 48px gutters on desktop, 24px under 900px and 16px for the announcement bar under 520px (measurements.md announce pad-left). Each section defines its own fr-ratio grid: hero 1.1fr/1.1fr/.7fr, New Drop minmax(240px,.9fr)/2.4fr, products repeat(3), story .9fr/1.6fr/.4fr, values repeat(4) (css-html-stats.txt GRID-TEMPLATE-COLUMNS). The fr ratios, not the type sizes, are why the h1 lockup and the story heading break at 1024-1440 (findings-verified.json FIDELITY-2, FIDELITY-5). Above 1440 the wrapper leaves dark gutters and the cream band is not full-bleed (wide-1920-fold.png) — see the RESP register. Classification: REFINE — keep the 1440 content width and the 48/24 gutters, replace per-section fr guesses with a 12-column grid and minimum column widths for headline columns.

### 7.6 Imagery direction

Direction — low-key, cinematic city photography, garments carrying the wordmark, ink scrims fading into the layout, one gold accent — is right for the brand and matches the mockup: KEEP UNCHANGED. The assets do not: the hero is a three-model generated image (images/hero-group.png, byte-identical to uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png, inventory.tsv DUP-01) that the user chose to replace the mockup's single model (pasted-1789874193900-0.png), and the story photo is a crop of the mockup's hero with headline fragments baked in (findings-verified.json C1). Product images are 215-235 px mockup crops (README.txt; C2). Classification of the asset set: INCONSISTENT; details in §11, §14 and the ASSET register. Whether real photography exists is BUSINESS INFORMATION REQUIRED.

### 7.7 Buttons

Two rectangular CTAs, 16px 26px padding, 12px .22em caps, inline-flex with a 12px gap to a text arrow (lines 104, 132); rendered 242x50 and 169x50 (measurements.md). The primary CTA is an ink fill with cream text (weight 500) on the cream section; the accent CTA is a gold fill with ink text (weight 600) on the ink section. Hover exists and works — the runtime turns `style-hover` into `.scp0:hover`/`.scp1:hover` rules (support.js line 428 in collectProps, lines 1567-1590 createPseudoSheet; evidence-render.md) — but it is an editor-only attribute with no focus, active or disabled state. Classification: REFINE (UI-01).

### 7.8 Navigation (visual)

Five tracked-caps links at 12px .2em weight 500 with 44px gaps, gold active state with a 1px gold underline and 4px padding-bottom, gold hover via `a:hover` (lines 16, 70-72). Visually correct to the mockup; the problem is that it sits on the photograph with a scrim that thins to zero by 30% of the hero height (line 66), so three of five links land on open sky (evidence-render.md contrast). Classification: REFINE — the header needs its own backing. Behaviour, placeholders and the inert hamburger are in the NAV register.

### 7.9 Icons

Three icon vocabularies coexist: gold outline value icons at 44px (crown, community, globe, diamond) with the same gold globe reused at 16px in the announcement bar, cream outline utility icons at 24px (search, account, cart) plus a three-bar hamburger, and circled social glyphs at 28px where the mockup shows plain glyphs (desktop-1440.png header, values row and footer; 00-full-mockup-reference.webp; FIDELITY-8). All are RGBA PNGs with colour baked in, 28-42 KB each, so none can follow a token or a hover colour, and icon-globe.png is drawn at both 16px and 44px (findings-verified.json TECHNICAL-6). Classification: INCONSISTENT (BRAND-07). Format and weight belong to the ASSET register.

### 7.10 Product cards

Centered stack: 1:1 media box, name (12px .2em 600), price (14px 600), three 16px swatches with a rgba(0,0,0,.25) border (lines 108-119). The type treatment matches the mockup and should be kept (scratchpad/crops/d1440-price-row.png). The media box does not: the mockup floats the garments on the cream section, the build shows each crop's own off-white background as a square and edge-crops the cap (FIDELITY-3; scratchpad/crops/d-cap.png and d-tee.png show the box edge and the brim at the left edge). Classification: REFINE (UI-02).

### 7.11 Editorial sections

Hero and Our Story share one composition grammar: copy column left, photo bleeding right under a horizontal scrim, a side caption column right, tracked-caps stacks and a short rule. This is the brand's signature and should be KEPT UNCHANGED as a pattern. Where it fails is below 900px, where the side captions become orphan text blocks (RESPONSIVE-3), and in the story asset itself (C1). The caption rules are inconsistent — 36px gold (line 86), 80px cream (line 92), 40px ink (line 102), 40px cream (line 137) — UI-05.

### 7.12 Footer

Logo at 56px, a two-line tagline in muted 11px .26em, two circled social icons, a 1px divider, a second tagline (lines 153-166). Matches the mockup's band minus TikTok/YouTube (C14, deliberate). Classification: REFINE — the visual is fine; the icon style (UI-04) and the tagline system (BRAND-08) need decisions.

### 7.13 Visual hierarchy

At 1440 the hierarchy reads exactly as intended: gold eyebrow, 112px Playfair headline with the gold word, verse, rule, tagline (scratchpad/crops/d1440-hero.png). It degrades with width: three-line headline at 1024-1920 (FIDELITY-2; wide-1920-fold.png), four-line story heading at 1024 (laptop-1024.png; scratchpad/crops/l-storyhead.png), and on phones five stacked taglines under a 320px band (scratchpad/crops/m375-hero.png). Classification: KEEP UNCHANGED at desktop, INCONSISTENT below 1024.

### 7.14 Summary

| Area | Classification |
|---|---|
| Colour — core three | KEEP UNCHANGED |
| Colour — neutrals, scrims, hairlines, hover tints | NEEDS STANDARDIZATION |
| Typography — faces and tracked-caps convention | KEEP UNCHANGED |
| Typography — scale, label roles, ₱/→ glyphs | NEEDS STANDARDIZATION / INCONSISTENT |
| Spacing | NEEDS STANDARDIZATION |
| Grid | REFINE |
| Imagery — direction / assets | KEEP UNCHANGED / INCONSISTENT |
| Buttons | REFINE |
| Navigation (visual) | REFINE |
| Icons | INCONSISTENT |
| Product cards | REFINE |
| Editorial sections | KEEP UNCHANGED (pattern), REFINE (mobile) |
| Footer | REFINE |
| Visual hierarchy | KEEP UNCHANGED at 1440, INCONSISTENT below 1024 |

## 8. UI Audit

### 8.1 Method

Each component was read from the source (God Squad Website.html, line numbers below), measured in the live DOM (measurements.md) and checked against the renders and the mockup. The page has 166 DOM elements after render, zero `<button>`, zero classes and 77 inline style attributes (css-html-stats.txt), so every component described here exists only as a one-off block of inline CSS. The output of this section is the component list the Phase 2 design system must specify.

### 8.2 Announcement bar (lines 58-61)

Flex row, 12px 48px padding, 11px .22em gold caps left, cream "Worldwide Shipping" with a 16px globe right, hairline rgba(255,255,255,.08) bottom border. Under 520px it stacks to two centred lines with 10px 16px padding (line 50). Inconsistencies: the globe is gold in the build where the mockup shows a white glyph (FIDELITY-9, deliberate user edit; pasted-1789874476205-0.png; 00-full-mockup-reference.webp), and the same gold file is reused at 44px in the values row (line 182), while search/account/cart are cream outline — the icon set is split between gold and cream (BRAND-07); the side gutter is 48px on desktop, 48px at 521-900 (the 900px rule targets a `[data-r=pad]` that no element carries — see the CSS register) and 16px under 520, so the bar never aligns with the 24px gutter used by every other section on tablets (tablet-768.png top edge; RESPONSIVE-6). The bar is a plain `div` with no link, no dismiss and no rotation — fine as a single static message; it is hard-coded copy that must become a section setting (see the DATA register).

### 8.3 Header (lines 68-80)

Absolutely positioned `nav` inside the hero section, 22px 48px padding, three groups: logo box (78px high, 56px under 900px), five links, and a utility cluster with 26px gaps (hamburger 22x16, search/account/cart 24x24 PNGs, a 14px gold badge with 9px text at top:-8px right:-10px). Component-level findings, distinct from the behaviour findings in the NAV and A11Y registers:

- The wordmark renders at 66x50 px at 1440 against 114x87 on the 1024-wide mockup, because the 500x500 PNG has large transparent padding (FIDELITY-4; scratchpad/crops/d1440-logo-nav.png; d-logo.png vs m-logo.png). Half the intended presence — BRAND-05.
- No hover, focus or active state is defined for any icon control; the only hover on the page is `a:hover{color:#d8c08a}` (line 16), which cannot recolour a PNG. Home is already gold so it has no hover change (evidence-render.md Hover).
- The badge is the smallest text on the site (9px, C16) in a 14px circle.
- The logo wrapper carries `background:#0230`, an alpha-0 no-op (TECHNICAL-10) — CSS register.

UI-03 covers the state spec and badge minimums.

### 8.4 Buttons (lines 104, 132)

| Property | View All Products | Our Story |
|---|---|---|
| Fill / text | #0d0c0a / #f3efe6 | #d8c08a / #0d0c0a |
| Weight | 500 | 600 |
| Padding, size, tracking | 16px 26px, 12px, .22em (same) | same |
| Rendered size | 242x50 | 169x50 |
| Hover | #2a2823 / #f3efe6 via `style-hover` | #e6d3a6 / #0d0c0a via `style-hover` |
| Arrow | `<span>→</span>` text glyph, fallback font | same |
| Focus / active / disabled | none | none |
| Destination | href="#" | href="#" |

The hover works today because support.js compiles `style-*` attributes into `.scpN:hover` rules with `!important` (support.js line 428 in collectProps, lines 1567-1590 createPseudoSheet; evidence-render.md), but the attribute is Claude-Design-only and disappears the moment the markup leaves the runtime. The weight mismatch (500 vs 600) is an inconsistency, not a hierarchy signal. The arrow glyph is drawn by a fallback face (BRAND-03) and is announced by screen readers — labelling is in the A11Y register. Issue UI-01.

### 8.5 Product card (lines 108-119)

Vertical stack, centred text: media box (`width:100%; aspect-ratio:1/1; background:#ebe6dc; overflow:hidden`) with `object-fit:cover` image, name 12px .2em 600 at 14px margin, price 14px 600 at 6px, swatch row with 10px gap at 14px. Rendered media 288x288 at 1440 from 235px sources, 327x327 at 375 (measurements.md). Findings: the crop's own off-white background is visible against the #f3efe6 section and every garment reads as a boxed square; the cap (215x190) is scaled and edge-cropped so the brim touches the tile edge (FIDELITY-3; scratchpad/crops/d-cap.png and d-tee.png); the mockup floats the garments with clear space. Name and price alignment breaks at 1024 when "Signature Oversized Tee" wraps (C9; laptop-1024.png). Nothing in the card is a link and swatches are inert spans — ECOM, NAV and A11Y registers. Issue UI-02: the card spec must fix the media treatment (contain on section cream or transparent masters; a fixed ratio; a name line-clamp so prices align) before Phase 6 builds it.

### 8.6 Value tile (lines 144-148)

44px 24px padding, centred column with 10px gap, a 44px icon box with 10px bottom margin, 13px .22em 600 title, 11px .2em muted subtitle, `border-right:1px rgba(255,255,255,.1)` on every tile including the last. Under 900px a border-bottom is added and under 520px the right border is removed (lines 41, 49). Component inconsistencies: the divider logic lives on each tile rather than on the grid, so the second column at 521-900 paints a rule on the viewport edge and the last row doubles the section's own bottom border (RESPONSIVE-5) — VAL-02; the four icons have equal height but widths of 44, 60, 52, 52 px (TECHNICAL-6 measurements), so the row does not sit on one optical size — VAL-03. Detailed audit in §15.

### 8.7 Editorial captions

Five caption devices recur: the eyebrow (13px .3em: gold weight 400 at lines 83 and 129, ink weight 500 at line 100), the tagline stack (14px .3em, 1.65-1.7 line-height, `<br>`-separated: lines 87, 93; a 13px .24em 1.75 variant at line 103), the story side caption (12px .22em 1.8, line 136) and the script accent (Kaushan, rotate(-8deg) desktop / -6deg mobile, lines 91 and 27). Each is paired with a short rule whose width and colour differ every time: 36px gold (line 86), 80px cream (line 92), 40px ink (line 102), 40px cream (line 137), with margins 38/26, 36/30, 30/22 and 18px. This is one component drawn five ways — UI-05. The tracked caps are consistent enough in spirit that a single "caption" component with three sizes and one rule component with two widths would reproduce the page without visible change.

### 8.8 Footer (lines 153-166)

Flex row, 26px 48px padding, 32px gap, `flex-wrap:wrap`; left group logo (56px) + tagline, right group social links (28x28 circled PNGs, 18px gap) + 1px divider + tagline. The mockup shows four plain glyphs (Instagram, Facebook, TikTok, YouTube); the build shows two circled ones after the user removed two placeholder boxes (pasted-1789874476205-0.png; C14; FIDELITY-8). Under 900px it stacks into a 164px column even at 768 where both groups (230 + 271 px) fit in one row (RESPONSIVE-9) — RESP register. Issue UI-04 for the icon style and channel decision. Legal links, contact and navigation are absent in both build and mockup — Footer audit (§16) and BUSINESS INFORMATION REQUIRED there.

### 8.9 Inconsistency ledger

| # | Component | Inconsistency | Evidence | Issue |
|---|---|---|---|---|
| 1 | Buttons | weight 500 vs 600; hover via editor attribute; no focus state | lines 104, 132 | UI-01 |
| 2 | Product card | boxed tile vs floated mockup garments; cap edge-cropped | FIDELITY-3 | UI-02 |
| 3 | Header icons | no states; badge 9px | lines 76-78; C16 | UI-03 |
| 4 | Social icons | circled vs mockup plain | FIDELITY-8 | UI-04 |
| 5 | Rules | 36/80/40/40 px, four colour/margin combos | lines 86, 92, 102, 137 | UI-05 |
| 6 | Eyebrow | weight 400 vs 500 at the same 13px .3em | lines 83, 100, 129 | BRAND-04 |
| 7 | Taglines and captions | 14px .3em vs 13px .24em taglines; .22 / .26 / .2em at 11-12px captions | lines 87, 93, 103, 58, 136, 147, 156 | BRAND-04 |
| 8 | Icon colour | gold globe (bar and values) vs cream outline utilities; gold vs the mockup's white globe | FIDELITY-9; TECHNICAL-6 | BRAND-07 |
| 9 | Announcement gutter | 48 / 24 / 16 px across widths | RESPONSIVE-6 | CSS / RESP registers |
| 10 | Value dividers | per-tile borders leak at 2-col | RESPONSIVE-5 | VAL-02 |

### 8.10 Component list for the Phase 2 design system

| Component | Variants / states to specify | Present today as |
|---|---|---|
| Colour tokens | ink, cream, gold, muted, body-on-ink, ink-hover, gold-hover, olive; hairline; scrim recipes hero-h, hero-v, story-h, mobile-v | raw literals (BRAND-01, BRAND-02) |
| Type ramp | display-xl/l/m, script, eyebrow, label-l/m/s, body, badge; fixed tracking per role | 14 ad-hoc combinations (BRAND-04) |
| Spacing scale | 4-96 px ramp; section padding tokens; gutters 48/24 | roughly two dozen distinct spacing values (BRAND-06) |
| Grid | 1440 container, 12 columns, headline min-widths | per-section fr grids |
| Announcement bar | single message + icon; stacked mobile variant | lines 58-61 |
| Header | logo (min sizes), nav link (default/hover/active/focus), icon button (44px hit area), cart badge, menu button | lines 68-80 |
| Button | primary (ink), accent (gold), states, SVG arrow | lines 104, 132 |
| Eyebrow, tagline stack, side caption, script accent | sizes s/m/l | lines 83-93, 100-103, 129, 136 |
| Rule / divider | horizontal s (36-40px) and m (80px); vertical 28px | five one-offs |
| Product card | media (ratio, fit), name (2-line clamp), price, swatch row; hover and link states with ECOM | lines 108-119 |
| Swatch | 16px, border, selected/unavailable states, accessible name | line 116 |
| Value tile | icon, title, subtitle, optional link; grid dividers | lines 144-148 |
| Editorial media section | copy column + bleed photo + scrim + side caption; mobile order rules | hero, story |
| Footer | logo, tagline, social icon link, divider; row/stack breakpoint | lines 153-166 |
| Icon set | search, account, cart, menu, close, arrow, globe, crown, community, diamond, facebook, instagram — SVG, currentColor | nine PNGs (BRAND-07) |

## 9. UX Audit

### Scope, method and the flow-level finding

This section walks the spec's ten-step homepage flow against the one page in the project, "God Squad Website.html" (190 lines; the runtime renders it into 166 DOM elements at every width, measurements.md). Evidence is the source file, the live DOM measurements, the full-page renders in scratchpad/shots and the verified findings register. Three of the ten intended steps do not exist in the build: the page contains exactly four `<section>` elements (hero, `#shop`, `#story`, values) and one `<footer>` (css-html-stats.txt tag counts) and nothing else between the announcement bar and the footer (desktop-1440.png).

The central UX fact is commercial, not visual. The page has zero `<form>`, zero `<button>` and zero `<input>` elements and nine links, six of them `href="#"` (css-html-stats.txt). The only path toward a purchase is nav Shop → in-page anchor `#shop` → three product cards that contain no link, button or price action → nothing (findings-verified.json TECHNICAL-4: 0 anchors inside `[data-r=products]`). Below 900px even that path disappears: the nav links are `display:none` (God Squad Website.html line 30) and the hamburger is a `<span>` with no handler (line 75; support.js binds no click listener of its own — it only maps the `onclick` attribute name at line 318 and listens for `message` and `DOMContentLoaded` at lines 1407 and 1904, and never references `nav-menu`). The prototype persuades well but cannot sell (see the ECOM register) and its navigation does not navigate (see the NAV register).

### 1. Announcement Bar (lines 58-61)

| | |
|---|---|
| PURPOSE | Brand line plus a shipping reassurance above the header. |
| CURRENT IMPLEMENTATION | A plain `<div data-r="announce">`, flex space-between, 11px gold tracked caps: "Good People. Higher Purpose." left; 16px globe PNG + "Worldwide Shipping" in cream right. Not a link, no dismiss, no rotation. It sits outside the hero as a sibling of the `<section>`, not inside a header. At ≤520px it stacks to two centred lines (line 50; mobile-375-true.png y 0-59); at 521-900px it keeps a 48px gutter while everything else uses 24px because the `[data-r=pad]` rule targets nothing (see the CSS register). |
| UX QUALITY | Reads cleanly on desktop (desktop-1440.png) and matches the mockup apart from the deliberately gold globe (findings-verified.json FIDELITY-9). |
| PROBLEMS | "Worldwide Shipping" is a commercial promise with no policy, rates or destination list behind it — BUSINESS INFORMATION REQUIRED (UX-05). The bar cannot be part of a Shopify header group as structured (see the SHOP register). |
| OPPORTUNITIES | Link the shipping label to the shipping policy; allow multiple messages; optional close control. |
| SHOPIFY IMPLEMENTATION | `sections/announcement-bar.liquid` in the header section group with `announcement` blocks (text, optional link), colour settings from the design system. |
| PRIORITY | P3 |
| VERDICT | **IMPROVE** |

### 2. Header (lines 68-80)

| | |
|---|---|
| PURPOSE | Brand mark, primary navigation, search, account and cart entry points. |
| CURRENT IMPLEMENTATION | A `<nav>` absolutely positioned inside the hero `<section>` (line 68); logo drawn in a 78px box that yields a 66x50 wordmark at 1440 (evidence-render.md); five links (Home `#`, Shop `#shop`, Collections `#shop`, Our Story `#story`, Verse `#`); a hamburger span hidden on desktop (line 17) and shown ≤900px (line 31) with no role, tabindex or handler; Search, Account and Cart as bare `<img>` elements with `tabIndex -1` (lines 76-78, evidence-render.md); a cart badge that is the literal text "0" at 9px (line 78). |
| UX QUALITY | At 1440 the left-logo / centre-links / right-utilities arrangement follows the mockup, but the wordmark is about half the mockup's relative size (findings-verified.json FIDELITY-4) and the links sit over the hero sky rather than the mockup's dark facade (see the A11Y register). Functionally it is inert: nothing in the header except the five links can be clicked to any effect, and under 900px there is no navigation at all (measurements.md 375/768: nav links hidden, hamburger shown 22x16). |
| PROBLEMS | NAV-01 to NAV-09 (NAV-04 Verse destination and NAV-07 hover feedback are detailed in §10). Nav-link contrast over the hero sky and tap-target sizes: see the A11Y register. Header structurally welded to the hero: see the CSS register. |
| OPPORTUNITIES | Admin-editable menu, a drawer for phones, working search/account/cart, an optional sticky mode for the 5.4-screen mobile page (see the RESP register). |
| SHOPIFY IMPLEMENTATION | `sections/header.liquid` in the header group: `linklists[section.settings.menu]`, `routes.search_url`, `routes.account_url`, `routes.cart_url`, `cart.item_count`, `link.current` for the active state. |
| PRIORITY | P1 |
| VERDICT | **REBUILD** |

### 3. Hero (lines 64-95) — UX flow only; visual and image findings belong to the Hero Audit (§11)

| | |
|---|---|
| PURPOSE | Brand statement and the first conversion nudge. |
| CURRENT IMPLEMENTATION | Three-column grid over `images/hero-group.png`; copy column: eyebrow, `<h1>` "Walk By Faith.", "2 Corinthians 5:7", rule, "Different / People / Same Purpose"; side column: script "More Than Clothing.", rule, "A Higher Purpose." There is no link or button anywhere in lines 82-94. |
| UX QUALITY | The statement is strong and on-brand, but the section asks nothing of the visitor. On 1366x768 and 1280x720 laptops the first screen is the hero alone with no product or CTA visible (laptop-1366-fold.png, laptop-1280-fold.png). On phones the hero is 970px tall with five stacked taglines under a 320px photo (findings-verified.json RESPONSIVE-3; see the RESP register). |
| PROBLEMS | UX-01 (no CTA). Hero-fade offset and orphaned side captions: see the RESP register. Nav contrast: see the A11Y register. Photo choice vs mockup: Hero Audit (§11). |
| OPPORTUNITIES | One primary CTA to the drop collection and an optional secondary CTA to Our Story; all copy as section settings. |
| SHOPIFY IMPLEMENTATION | `sections/hero.liquid` with `image_picker`, text settings for eyebrow/heading/verse/taglines, and up to two `button` blocks (label + URL). |
| PRIORITY | P1 |
| VERDICT | **IMPROVE** (from the UX standpoint: keep the composition, add the CTA) |

### 4. New Drop (lines 98-122)

| | |
|---|---|
| PURPOSE | Showcase the current drop and funnel visitors into the shop. |
| CURRENT IMPLEMENTATION | Cream section: left column with eyebrow "New Drop /", `<h2>` "The Faithful", rule, "Premium Essentials for a Higher Purpose.", and the "View All Products →" button (`href="#"`, line 104); right column a three-card grid generated by `<sc-for list="{{ products }}">` from the data script (lines 174-178). |
| UX QUALITY | Well composed at 1440 (desktop-1440.png). Cards are not clickable and have no hover state; at 375 the section is 1,695px tall with the only control above the grid (findings-verified.json RESPONSIVE-4). Per-width layout outcomes at 1024, 768 and 375 (C9, C8, RESPONSIVE-4): see the RESP register. |
| PROBLEMS | PROD-01 to PROD-07 (detailed in §12), COLL-03, NAV-03 (View All → `#`). Hard-coded product data: see the DATA register. |
| OPPORTUNITIES | Featured-collection section with a collection picker, a shared product-card snippet, "View all" bound to `collection.url`, a 2-up phone grid. |
| SHOPIFY IMPLEMENTATION | `sections/featured-collection.liquid` looping `collection.products` (limit from a setting) and `snippets/product-card.liquid`. |
| PRIORITY | P1 |
| VERDICT | **REBUILD** |

### 5. Best Sellers / Product Discovery

| | |
|---|---|
| PURPOSE | A second merchandising surface: best sellers and category entry points for product discovery. |
| CURRENT IMPLEMENTATION | Does not exist. The DOM goes straight from `#shop` (line 122) to `#story` (line 125); the page has four `<section>` elements in total (css-html-stats.txt) and desktop-1440.png shows New Drop followed immediately by Our Story. |
| UX QUALITY | The homepage exposes exactly three products and no category, best-seller or "shop by" entry point; browse depth is one screen of cards. |
| PROBLEMS | UX-02. Which products would qualify as best sellers for a launch catalogue, and whether a category set (tees, hoodies, caps or otherwise) exists: BUSINESS INFORMATION REQUIRED. |
| OPPORTUNITIES | A featured-collection variant bound to a collection whose admin sort order is "Best selling", or manual product picks; optional category tiles; reuse of the New Drop product-card snippet. |
| SHOPIFY IMPLEMENTATION | `sections/best-sellers.liquid` with a collection picker and limit (or `product` blocks), rendering `snippets/product-card.liquid`. |
| PRIORITY | P2 |
| VERDICT | **ADD LATER** |

### 6. Our Story (lines 125-139)

| | |
|---|---|
| PURPOSE | Brand narrative and trust. |
| CURRENT IMPLEMENTATION | Dark section with eyebrow, `<h2>` "Real People. Bigger Purpose.", a 15px paragraph (the only `<p>` on the page, line 131), a gold "Our Story →" CTA to `#` (line 132), and a side caption "Faith Lives Different Here." The image is the 650x480 hero crop with mockup headline fragments baked into the pixels (findings-verified.json C1; see the STORY register). |
| UX QUALITY | The copy is concise and credible. The section's CTA and the nav item promise a fuller story that has no destination: nav "Our Story" scrolls to this section (`#story`) and the section's own button scrolls to the top (`#`). Below 900px the side caption becomes an orphan block under the button (FIDELITY-7; see the RESP register). |
| PROBLEMS | UX-07, NAV-03. Story page content: BUSINESS INFORMATION REQUIRED. |
| OPPORTUNITIES | Image-with-text section, CTA to a real page, richtext copy. |
| SHOPIFY IMPLEMENTATION | `sections/our-story.liquid` (`image_picker`, `richtext`, `url` + label). |
| PRIORITY | P2 |
| VERDICT | **IMPROVE** |

### 7. Brand Values (lines 142-150)

| | |
|---|---|
| PURPOSE | USP / reassurance strip. |
| CURRENT IMPLEMENTATION | Four tiles from `values[]` (lines 180-183): 44px PNG icon, 13px title, 11px subtitle in #bdb6a8, hairline borders; 2 columns ≤900px, 1 column ≤520px (698px tall on a phone, findings-verified.json RESPONSIVE-5). |
| UX QUALITY | Clean and consistent with the mockup (desktop-1440.png). No tile links anywhere; "Worldwide / Shipping Available" repeats the announcement claim; "Community / People With Purpose" is asserted with no community content on the page (see step 9). |
| PROBLEMS | UX-06. Raster icons: see the ASSET register (format and weight) and the BRAND register (icon style). Titles as `<div>`: see the HTML and A11Y registers. |
| OPPORTUNITIES | Blocks with icon, title, subtitle and optional link (e.g. shipping policy, size/quality guide). |
| SHOPIFY IMPLEMENTATION | `sections/brand-values.liquid` with up to four `value` blocks. |
| PRIORITY | P3 |
| VERDICT | **KEEP** (convert to blocks) |

### 8. Verse / Faith

| | |
|---|---|
| PURPOSE | A faith statement in its own section: the scripture that anchors the brand, with room to change or rotate it. |
| CURRENT IMPLEMENTATION | Does not exist. The only scripture on the page is the hero's "2 Corinthians 5:7" line (line 85); the primary nav item "Verse" is `href="#"` (line 72); the DOM goes from the values section (line 150) straight to the footer (line 153). |
| UX QUALITY | A visitor who clicks the brand's most distinctive menu item is returned to the top of the page; the faith positioning has no dedicated moment after the hero. |
| PROBLEMS | UX-03, NAV-04. Which verse(s), whether they rotate, the translation to be quoted and that translation's attribution requirements: BUSINESS INFORMATION REQUIRED. |
| OPPORTUNITIES | Editable verse text and reference, an optional image or pattern, placed after Brand Values per the spec's order, with the nav item bound to it. |
| SHOPIFY IMPLEMENTATION | `sections/verse.liquid` with `richtext` and `text` settings; a blog could hold a rotating verse later. |
| PRIORITY | P2 |
| VERDICT | **ADD LATER** |

### 9. Social / Community

| | |
|---|---|
| PURPOSE | Social proof and community: a feed, gallery or customer imagery that substantiates the "Community" value. |
| CURRENT IMPLEMENTATION | Does not exist. The only social presence is two footer icons linking to `#` (lines 160-161); no feed, gallery, handle, hashtag or customer imagery appears anywhere (desktop-1440.png). |
| UX QUALITY | The "Community / People With Purpose" tile (line 181) is asserted with nothing on the page to back it; the page carries no social proof. |
| PROBLEMS | UX-04, FOOT-02. Handles, networks, image source and user-generated-content permissions: BUSINESS INFORMATION REQUIRED. |
| OPPORTUNITIES | Manual image blocks with a handle/link setting; a feed app is a later app decision outside Phase 1. |
| SHOPIFY IMPLEMENTATION | `sections/social-gallery.liquid` with image blocks and a handle/link setting. |
| PRIORITY | P3 |
| VERDICT | **ADD LATER** |

### 10. Footer (lines 153-166) — detail in §16

| | |
|---|---|
| PURPOSE | Site-wide navigation, trust and legal links, contact, newsletter and social; the last chance to route a visitor onward. |
| CURRENT IMPLEMENTATION | A decorative band: logo, "Different People. Same Purpose.", two `#` social links, divider, "A Brighter Tomorrow" (lines 153-166). No navigation, policy, contact, copyright, newsletter or payment icons (findings-verified.json critic addition on the footer). |
| UX QUALITY | Matches the mockup's minimal band at 1440 (desktop-1440.png y 1960-2055) but gives a buyer nothing to check and a phone user no way back to the menu at the end of a 4,382px page (measurements.md 375). |
| PROBLEMS | FOOT-01, FOOT-02, FOOT-03, FOOT-04. Every link, policy, contact detail and copyright holder: BUSINESS INFORMATION REQUIRED. |
| OPPORTUNITIES | SHOP / ABOUT / HELP / FOLLOW menu columns beneath the preserved brand band; a legal row; newsletter; social links from theme settings. |
| SHOPIFY IMPLEMENTATION | `sections/footer.liquid` in the footer section group with `link_list`, `text`, `newsletter` and `social` blocks. |
| PRIORITY | P1 |
| VERDICT | **REBUILD** |

### Verdict summary

| Step | Exists | Verdict | Priority | Register IDs |
|---|---|---|---|---|
| Announcement Bar | Yes | IMPROVE | P3 | UX-05 |
| Header | Yes (inert) | REBUILD | P1 | NAV-01…NAV-09 |
| Hero | Yes | IMPROVE (UX) | P1 | UX-01 |
| New Drop | Yes | REBUILD | P1 | PROD-01…PROD-07, COLL-03, NAV-03 |
| Best Sellers / Discovery | No | ADD LATER | P2 | UX-02 |
| Our Story | Yes | IMPROVE | P2 | UX-07, NAV-03 |
| Brand Values | Yes | KEEP (blocks) | P3 | UX-06 |
| Verse / Faith | No | ADD LATER | P2 | UX-03, NAV-04 |
| Social / Community | No | ADD LATER | P3 | UX-04, FOOT-02 |
| Footer | Yes (decorative) | REBUILD | P1 | FOOT-01…FOOT-04 |

## 10. Navigation Audit

### Desktop navigation (≥901px)

The `<nav data-r="nav">` (God Squad Website.html line 68) is absolutely positioned over the hero photo inside the hero `<section>`, with the hero copy padded 170px/190px to clear it (lines 82, 90). Left: the wordmark in a 78px box. Centre: five links in 12px Jost 500 tracked caps with a 44px gap (line 70). Right: hamburger (hidden by line 17), Search, Account, Cart with badge. At 1440 the left-logo / centre-links / right-utilities arrangement follows the mockup, but the wordmark is about half the mockup's relative size (findings-verified.json FIDELITY-4) and the links sit over the hero sky rather than the mockup's dark facade (desktop-1440.png vs 00-full-mockup-reference.webp). The runtime attaches no handlers, so every behaviour is native anchor behaviour (evidence-render.md; support.js has no click binding and no reference to `nav-menu`).

Problems specific to desktop:
- Three of the five links (Collections, Our Story, Verse) sit on the bright sky between the two models at 1024-1440: effective contrast 2.4-2.8:1 at 1440 and 2.4-2.9:1 at 1024 (findings-verified.json critic addition); pixel-sampled brightest-2% 2.4-2.5:1 with medians 4.6-5.7:1 (evidence-render.md). The judgement is the A11Y register's; the structural coupling of header to hero photo is the CSS register's (findings-verified.json TECHNICAL-11).
- Focus order is Home, Shop, Collections, Our Story, Verse, then the two CTAs and the two social links; the hamburger and the three utility icons are unreachable by keyboard (measurements.md).

### Mobile navigation (≤900px)

There is none (NAV-01). Line 30 hides `[data-r=nav-links]`; line 31 shows the hamburger; the hamburger is `<span data-r="nav-menu" aria-label="Menu">` with three bar spans (line 75) — no role, no tabindex, no `href`, no handler, and the runtime never references it. At 375, 390, 430 and 768 the header shows logo + hamburger + three icons and none of them does anything (measurements.md; mobile-375-true.png y 59-147 (header); tablet-768.png y 41-129 (header)). The nav is `position:relative` below 900px (line 29), so it scrolls away; on a 4,382px phone page there is no sticky header, no back-to-top and no footer navigation to return to (findings-verified.json RESPONSIVE-10; see the RESP register for the page-length outcome, FOOT-01 for the footer). Tap targets are 22x16 (hamburger) and 24x24 (icons) — see the A11Y register (C15).

### Logo

`images/WHITE FONT LOGO.png` is a 500x500 RGBA PNG with large transparent padding drawn at `height:78px` in the nav (line 69) and `height:56px` in the footer (line 155) and under 900px (line 32). The visible wordmark is 66x50 at 1440 and 47x36 in the footer, against 114x87 and 70x53 on the mockup's 1024 canvas — roughly half the relative size (findings-verified.json FIDELITY-4; desktop-1440.png y 77-126 (nav wordmark) vs 00-full-mockup-reference.webp). The wrapper's `background:#0230` is a zero-alpha no-op (TECHNICAL-10). NAV-08: the header needs a trimmed logo asset (see the ASSET register for the trim and a vector master) and a `logo_width` setting. The only layered sources seen are the PSD files at Desktop/GODSQUAD/PSD FILES (not inspected; no SVG/AI/EPS master has been seen — evidence-render.md); whether a vector master exists is BUSINESS INFORMATION REQUIRED.

### Search, Account, Cart

| Control | Line | Current markup | Behaviour | Target |
|---|---|---|---|---|
| Search | 76 | `<img alt="Search">`, `tabIndex -1`, no wrapper | none | `<a href="{{ routes.search_url }}">` or a `<button>` opening a search modal with predictive search (`routes.predictive_search_url`) |
| Account | 77 | `<img alt="Account">`, no wrapper | none | `<a href="{{ routes.account_url }}">` (falls back to `routes.account_login_url` when logged out); depends on whether customer accounts are enabled — BUSINESS DECISION REQUIRED |
| Cart | 78 | `<span><img alt="Cart"><span>0</span></span>` | none; badge is the literal "0" at 9px | `<a href="{{ routes.cart_url }}">` with `{{ cart.item_count }}`, optionally opening a cart drawer |

NAV-02 (bare images) and NAV-09 (hard-coded badge). The 9px badge text: see the A11Y register (C16). The icons are 28-29 KB raster PNGs with baked colour (see the ASSET register), so no hover or focus recolour is possible.

### Announcement bar

A sibling `<div>` above the hero (lines 58-61), not part of any header element; content and UX are assessed in §9 step 1 (UX-05). For Shopify it must become its own section in the header group (see the SHOP register).

### Active state

The Home link carries an inline `color:#d8c08a;border-bottom:1px solid #d8c08a` (line 71). It is hard-coded, does not respond to scroll position or hash, and would remain "active" on every page of a multi-template theme (NAV-06). Shopify derives it from `link.current` / `link.child_active` on the menu object.

### Hover state

The only nav hover is the global `a:hover{color:#d8c08a}` (line 16). Home is already gold, so it has no visible hover change; the utility icons have no hover or focus state; the social icon links have none at all because the colour is in the PNG. The two CTAs have a working hover generated by the runtime from the `style-hover` attribute (findings-verified.json TECHNICAL-2); that attribute is Claude-Design-only and its re-expression as ordinary CSS when the markup leaves the runtime is the CSS register's item. NAV-07.

### URL inventory — all nine hrefs

| # | Element | Line | href now | What happens now | Should connect to | Shopify object | Status |
|---|---|---|---|---|---|---|---|
| 1 | Home | 71 | `#` | scrolls to top | HOME | `routes.root_url` | ready |
| 2 | Shop | 72 | `#shop` | anchor to New Drop | SHOP — the all-products collection or a designated shop collection | `routes.all_products_collection_url` or `collection.url` | BUSINESS INFORMATION REQUIRED (which collection) |
| 3 | Collections | 72 | `#shop` | same anchor as Shop | COLLECTIONS — collection index | `routes.collections_url` | BUSINESS INFORMATION REQUIRED (collection taxonomy) |
| 4 | Our Story | 72 | `#story` | anchor to story section | OUR STORY page | `pages['our-story'].url` (handle TBD) | BUSINESS INFORMATION REQUIRED (page content) |
| 5 | Verse | 72 | `#` | scrolls to top | VERSE — undefined | page, blog or section anchor | BUSINESS INFORMATION REQUIRED |
| 6 | View All Products | 104 | `#` | scrolls to top | the drop / shop collection | `collection.url` | BUSINESS INFORMATION REQUIRED (same as #2) |
| 7 | Our Story CTA | 132 | `#` | scrolls to top | same as #4 | page URL | BUSINESS INFORMATION REQUIRED |
| 8 | Facebook | 160 | `#` (aria-label) | scrolls to top | brand profile | theme setting (e.g. a `social_facebook_link` text setting) | BUSINESS INFORMATION REQUIRED |
| 9 | Instagram | 161 | `#` (aria-label) | scrolls to top | brand profile | theme setting | BUSINESS INFORMATION REQUIRED |

The two remaining `href` values in the file are the Google Fonts preconnect and stylesheet (lines 11-12), not navigation. NAV-03 covers the six `#` placeholders; NAV-05 covers Shop and Collections sharing one destination; NAV-04 covers Verse having no destination or content.

### Target navigation architecture (recommendation only)

- Header group: announcement-bar section + header section. Main menu from a Shopify navigation menu (`main-menu`): HOME, SHOP, COLLECTIONS, OUR STORY, VERSE, editable in admin without code.
- Utilities: SEARCH (modal with predictive search), ACCOUNT (conditional on the accounts decision), CART (badge from `cart.item_count`, drawer optional — see §25).
- Mobile: a drawer opened by a real `<button aria-expanded>` containing the same menu plus the utilities; consider a sticky header setting given the page length.
- Active state from `link.current`; hover/focus styles as plain CSS on tokens (Phase 2 design system).

## 11. Hero Audit

### 11.1 Copy elements

| Element (spec) | Markup | Style | Role in hierarchy | Finding |
|---|---|---|---|---|
| STREETWEAR WITH A PURPOSE | div, line 83 | 13px .3em gold | eyebrow | correct; wraps to two lines at 920 (band-920.png) |
| WALK BY FAITH. | h1, line 84, gold span on "Faith." | Playfair 900, clamp(56px, 8.5vw, 112px), .88, -.01em, text-wrap:balance | primary | stacks three lines at ≥901px, one line at 768-900, two lines only at the measured phone widths 375-430 (measurements.md h1 lines; FIDELITY-2; the findings-verified.json gaps note places the switch at roughly 540px) — HERO-03 |
| 2 CORINTHIANS 5:7 | div, line 85 | 14px .3em cream | verse attribution | correct; a div, not associated with the h1 — HTML register |
| DIFFERENT PEOPLE. SAME PURPOSE | div, line 87 | 14px .3em, 1.65, `<br>` stack, no punctuation | tertiary tagline | punctuation differs from the footer's "Different People. Same Purpose." (line 156) — BRAND-08 |
| MORE THAN CLOTHING. | div[data-r=script], line 91 | Kaushan clamp(30px, 3vw, 44px), rotate(-8deg) | decorative accent, right column | overlaps the right model's back print at 1024-1440 (C17) — HERO-07; repeated as the Faith Driven subtitle (line 180) |
| A HIGHER PURPOSE. | div, line 93 | 14px .3em, 1.7 | right-column tagline | same overlap; becomes an orphan block below 900 (RESPONSIVE-3) — HERO-04 |

Six copy elements and no call to action. Nothing in lines 64-95 is a link or button; the first actionable element after the nav is "View All Products" in the next section, and it points to `#` (line 104).

### 11.2 Visual hierarchy and readability

At 1440 the left column reads in the intended order — eyebrow, headline, verse, rule, tagline — over the strongest part of the scrim (.92 to .75 alpha across the first 26%, line 66), so the cream and gold text has a near-solid backing (scratchpad/crops/d1440-hero.png). The right column is the weak point: the script and "A HIGHER PURPOSE." are placed by a .7fr column and 190px top padding (line 90) straight onto the back-print model, whose grey "God Squad" and "BUILT DIFFERENT" lettering competes with the caption at 1024 and 1440 (desktop-1440.png right third of the hero; laptop-1024.png). The headline's three-line stack at desktop also changes the hierarchy: "BY" becomes a line of its own and the gold "FAITH." drops below the model's shoulder, so the lockup the mockup relies on ("WALK BY" over "FAITH.") is never seen on a desktop screen (desktop-1440.png; wide-1920-fold.png at the 112px cap).

Readability changes with width rather than with the scrim. At 920 the eyebrow wraps to two lines (band-920.png) and at 768 the h1 collapses to one 65px line, so the verse sits under a headline that has lost its lockup (scratchpad/crops/t768-hero.png). On a 375 phone the h1 is 56px on two lines, but everything beneath it is tracked caps at 13px .3em (eyebrow) and 14px .3em (verse, taglines) — the visible text sizes on the page are 9-15px apart from the headings and script (measurements.md 375; RESPONSIVE-11), and letter-spacing of .3em at 14px makes each short line long and light (scratchpad/crops/m375-hero.png). The per-width type outcomes are owned by the RESP register (RESPONSIVE-11); the hero-specific consequence is that the copy stack must be ranked (HERO-04) so the small tracked lines are not all present on phones.

### 11.3 Image composition

The mockup's hero is one capped model in sunglasses to the right of the headline on a dark building (00-full-mockup-reference.webp). The build uses images/hero-group.png, a 1672x941 three-model group, chosen by the user in the editor (pasted-1789874193900-0.png: the hero "already uses the group photo you attached"). This is an approved deviation to confirm, not a defect (evidence-render.md; FIDELITY-1) — HERO-05 records it as a decision. Consequences of the swap that are defects: the sky between the two left models sits under the nav (11.4); the announcement bar is a solid strip outside the hero so the photo begins beneath it with sky and tower tops, a visible seam at 1440 and 1024 (FIDELITY-6; scratchpad/crops/d-topedge.png) — HERO-06; and the mockup's single model now appears only in Our Story (§14), inverting the two sections' imagery. The `object-position:center 30%` crop is fine at 16:9-ish desktop widths; at 375 the 375x320 band shows only the central two-thirds of the photo (96px cropped each side) and the back-print model is cut through mid-body (RESPONSIVE-8; scratchpad/crops/m375-hero.png) — HERO-08.

### 11.4 Contrast

Measured on the render pixels at 1440 (evidence-render.md): Collections median 5.7:1, brightest-10% 5.0:1, brightest-2% 2.5:1; Our Story 4.7 / 4.4 / 2.4; Verse 4.6 / 4.2 / 2.4; Home and Shop on dark hair about 15:1. A second method that composites photo luminance with the gradient alphas gives Collections 2.8:1, Our Story 2.4:1, Verse 2.4:1 at 1440 and the gold Home link 3.5:1 at 1024 (findings-verified.json critic addition on nav contrast). Both agree that three of five links fall below 4.5:1 on their brightest backing. The two methods disagree on the utility icons: pixel-sampled they pass at 10-15:1 (evidence-render.md), while the composited-luminance model puts search, account and cart at 3.7-4.8:1 at 1440, just above the 3:1 UI-component floor (critic addition); the A11Y register carries the definitive classification. The cause is the vertical scrim, .55 at 0% thinning to 0 by 30% (line 66), combined with the photo swap; the mockup's nav sits on a dark facade. The copy column itself passes: gold eyebrow and cream text over a .75-.92 ink scrim. The fix is a hero/header composition decision — HERO-02.

### 11.5 Typography

The h1 is right in face, weight, case and leading; it is wrong in its container. The copy column is 1.1fr of 2.9fr (about 546px at 1440) minus 96px padding, roughly 450px, which cannot hold "WALK BY" at 112px, so `text-wrap:balance` produces WALK / BY / FAITH. (FIDELITY-2). Below 900px the column is full width and the phrase collapses to one 65px line at 768 (scratchpad/crops/t768-hero.png) and to two lines only at phone widths (measurements.md 375-430). The two-line lockup should be the invariant: the column needs a minimum width tied to the clamp, or the clamp needs to be derived from the column, and the break after "BY" should be explicit rather than balanced — HERO-03. The script accent is correct; its rotation changes from -8deg to -6deg under 900px (line 27), harmless.

### 11.6 CTA strategy

The hero has no CTA (lines 82-94). On 1366x768 and 1280x720 the first screen is the hero alone; no product is visible without scrolling (laptop-1366-fold.png, laptop-1280-fold.png; evidence-render.md). At 1440 the announcement bar plus hero is about 760px (read from desktop-1440.png; the findings-verified.json gaps note gives the same estimate), so the same is true on any 768px-high laptop. A faith-streetwear store's hero should carry one primary action (a collection) and optionally a secondary one (the story or the verse); the destination handle and label are BUSINESS INFORMATION REQUIRED. HERO-01 is the highest-priority hero issue. Placeholder destinations elsewhere belong to the NAV register.

### 11.7 Desktop, tablet and mobile layouts

- Desktop 1440 / 1920: three-column grid, absolute cover image 1425x719 from 1672x941 (0.85x, evidence-render.md), nav absolute over the photo, hierarchy correct, lockup broken (11.5), nav contrast failing (11.4), right column colliding (11.2). At 1920 the wrapper stops at 1440 with dark gutters (wide-1920-fold.png) — RESP register.
- Laptop 1024: same composition at an 87px h1; eyebrow, headline and captions still fit; gold Home now on a brighter area (laptop-1024.png; critic addition 3.5:1). At 920 the eyebrow wraps and "FAITH." overflows its content box by 17px (band-920.png; findings-verified.json gaps).
- Tablet 768: one column; photo band 753x476 on top, nav in flow above it, h1 65px on one line, script and "A HIGHER PURPOSE." in a row beneath the copy (scratchpad/crops/t768-hero.png). The fade overlay is anchored to the section, not the image, so it reaches solid black 88px above the photo's bottom and the last 88px of photo reappear unfaded before a hard edge (fade 41-517 vs image 129-605, measurements.md 768) — the offset defect is owned by the RESP register (TECHNICAL-1 / RESPONSIVE-1) and is visible in scratchpad/crops/t768-hero.png and m375-hero.png as a black band across the hoodie.
- Mobile 375-430: band 375x320 (fade 59-379 vs image 147-467, same 88px offset), h1 56px on two lines, then verse, rule, tagline, script and "A HIGHER PURPOSE." stacked: 563px of text under a 320px image, hero 970px tall, 1.2 phone screens before the shop section (RESPONSIVE-3; scratchpad/crops/m375-hero.png). No CTA anywhere in that 970px. HERO-04 asks Phase 5 to rank the six copy elements so that mobile shows the essential three; the layout mechanics are in the RESP register.

### 11.8 LCP implications

The LCP candidate is images/hero-group.png: 1,989,201 bytes, RGB PNG with no alpha, served at every width including the 375px band (C10; critic addition on PNG alpha). It cannot paint until support.js has hidden the template (`x-dc{display:none!important}`, support.js lines 1818-1822), React and ReactDOM have arrived from unpkg (lines 1143-1145) and the runtime has mounted — about 211 KB raw / 66 KB gzipped of effectively render-blocking JS (measurements.md external bundle sizes). There is no `width`/`height`, no `srcset`, no `<picture>`, no `fetchpriority` or preload (evidence-render.md). Format, weight, responsive variants and the runtime chain are owned by the ASSET/PERF and ARCH/JS registers; the hero-specific requirement is that Phase 5 design a hero whose image is a plain `<img>` with dimensions, an art-directed portrait source for phones (HERO-08) and a solid header band so the LCP element is never a dependency of the nav's legibility.

### 11.9 Image quality

1672x941 is adequate at 1x for the 1425px render (0.85x) and marginal on 2x displays, where 2850 device pixels are needed (1.7x upscale — arithmetic from the measured sizes). The file is a generated image by filename (uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png, inventory.tsv) rather than a photograph of the brand's garments; garments carry the wordmark convincingly, but whether real photography exists and whether a larger master can be produced is BUSINESS INFORMATION REQUIRED. Resolution and format decisions are in the ASSET register.

### 11.10 Accessibility (hero-specific)

The photo has alt "God Squad crew" (line 65) — acceptable for a decorative-informative hero, though the fade div carries no semantics (correct). The h1 is the page's only h1 and is correctly the headline. The verse reference and the taglines are divs; the nav is a child of the hero section rather than a header landmark (C7) — HTML register. Nav contrast is above (11.4); keyboard access to the hamburger and icons is in the A11Y register. Motion: `transform` is used 22 times and there is no reduced-motion query (css-html-stats.txt), but nothing animates.

### 11.11 Verdict: REBUILD (implementation), keeping the approved composition

The design — copy, palette, Playfair lockup, script accent, photo bleeding right under an ink scrim — is right and is the reference for Phase 5. The implementation cannot be polished into production because the header is welded into the section (170/190px paddings, absolute nav), the fade is anchored to the wrong box, the h1 container breaks the lockup at every desktop width, the mobile flow stacks all six copy elements and there is no CTA. Exact recommendations for Phase 5:

1. Move the announcement bar and header out of the hero into the header group; give the header a solid ink band (or a scrim that stays at or above .8 alpha under the nav) so link contrast never depends on the photo (HERO-02, HERO-06).
2. Add one primary CTA (collection link) and optionally a secondary one; make it visible on 1280x720 and 1366x768 (HERO-01).
3. Lock the headline to two lines: explicit break after "BY", copy column minimum width derived from the clamp, remove `text-wrap:balance` from the h1 (HERO-03).
4. Rank the copy: eyebrow, h1, verse essential; tagline stack, script and "A HIGHER PURPOSE." optional and hidden or merged on phones (HERO-04).
5. Confirm the three-model photo (HERO-05); then source a higher-resolution master and a portrait crop for phones (HERO-08), re-encoded with dimensions and priority hints (ASSET/PERF register).
6. Move the script column off the back-print model or shift the crop so the caption sits on a quiet area (HERO-07).
7. Anchor scrims to the image container so the mobile fade tracks the photo (RESP register).

## 12. Product UX Audit

### What a product card is today

Each card is generated by `<sc-for list="{{ products }}" as="p">` (God Squad Website.html lines 107-120) from three literal objects in the data script (lines 174-178). Anatomy, top to bottom:

| Part | Line | Markup | Notes |
|---|---|---|---|
| Tile | 109 | `div` 1:1 `aspect-ratio`, `background:#ebe6dc`, `overflow:hidden` | a visible boxed square on the cream section |
| Image | 110 | `<img src="{{ p.img }}" alt="{{ p.name }}" object-fit:cover>` inside `<sc-if>` | no `width`/`height`, `srcset`, `sizes`, `loading` |
| Name | 112 | `div` 12px Jost 600 tracked caps | not a heading, not a link |
| Price | 113 | `div` 14px Jost 600 | string built in JS |
| Swatches | 114-118 | three 16px `<span>` circles with `background:{{ s }}` | inert, unnamed |

Nothing in the card is an `<a>`, `<button>` or `<form>` (findings-verified.json TECHNICAL-4: 0 anchors in `[data-r=products]`; css-html-stats.txt: buttons 0, forms 0).

### Product image quality

The three files are crops of the 1024x1536 mockup (uploads/God-Squad-Images/README.txt): product-tee.webp 235x230, product-hoodie.webp 235x235, product-cap.webp 215x190 (inventory.tsv). They render at 288x288 at 1440 (1.23x; cap 1.34x with a non-square source), 343 at 768 and 327 CSS px = 654 device px at 375/DPR2 (2.8x) (measurements.md). Resolution, weight and the need for real product photography are owned by the ASSET register (C2). What belongs here is the presentation: the mockup floats the garments on the cream section, while the build boxes each image in a 1:1 tile with `object-fit:cover`, so the crops' own off-white background reads as a square and the cap's brim touches the tile edge (findings-verified.json FIDELITY-3; desktop-1440.png y 808-1096 (product tiles) vs 00-full-mockup-reference.webp). PROD-05.

### Names

"Signature Oversized Tee", "Heavyweight Hoodie", "Utility Cap" — three literals (lines 175-177). Rendered as `<div>`s in 12px tracked caps. No link, no heading, no vendor/type line. Semantics: see the HTML and A11Y registers. The 1024 wrap and price misalignment: see the RESP register (C9). PROD-07 covers the missing merchandising hierarchy.

### Pricing

| Product | Literal | Source |
|---|---|---|
| Signature Oversized Tee | `cur + '1,290'` | line 175 |
| Heavyweight Hoodie | `cur + '2,490'` | line 176 |
| Utility Cap | `cur + '890'` | line 177 |

`cur` is the `currency` editor prop, an enum ₱ / $ / € defaulting to ₱ (`data-props`, line 169; line 172). Switching it changes only the symbol, so "$1,290" and "₱1,290" are the same number (findings-verified.json TECHNICAL-4). There is no money formatting, no compare-at / sale price, no "from" price for variant ranges, no sold-out state and no tax/shipping note. The ₱ glyph itself is not in the loaded Jost faces and falls back to a system font (see the BRAND register). The prices are prototype values — whether they are real launch prices is BUSINESS INFORMATION REQUIRED. PROD-04; the literal data itself is the DATA register's item.

### Swatches

Nine `<span>` elements, three per card, with inline backgrounds #0d0c0a, #f3efe6 and #4b5443 (lines 116, 175-177; live DOM rgb(13,12,10), rgb(243,239,230), rgb(75,84,67)). They have no text, `title`, `aria-label` or `role` (findings-verified.json TECHNICAL-5 — labelling is the A11Y register's item), are not interactive, do not change the image, and are not tied to any variant. At 16px they would be far below a usable target if made interactive. Colour names for the three values are not stated anywhere — BUSINESS INFORMATION REQUIRED. PROD-03.

### Hierarchy, hover, quick add, links

- Hierarchy: image → name → price → swatches, all centred. No badge (New / Sold out), no size information, no rating, no variant count. The "New Drop" framing lives at section level only. PROD-07.
- Hover: none on cards; there is no link and the global `a:hover` cannot apply. The two CTAs have a working runtime-generated hover (TECHNICAL-2). No secondary image on hover. PROD-06.
- Quick add: none; there is no add-to-cart anywhere on the page. PROD-02.
- Product links: none; a product cannot be opened. PROD-01.
- Collection links: "View All Products" → `#` (line 104); nav Shop and Collections → `#shop`, the id of this very section (line 98). See NAV-03 and NAV-05.

### Mobile behaviour

At ≤520px the grid is one column (line 47): 327px images and ~108px of labels per card, 1,695px for the section (2.1 screens at 375x812), with "View All Products" above the grid and nothing tappable after it (findings-verified.json RESPONSIVE-4; mobile-375-true.png y 1029-2724 (New Drop)). At 521-900px it is two columns (line 34) and the cap is orphaned (C8; tablet-768.png y 1895-2190 (cap tile)). Tap-size and layout outcomes are the RESP register's items; the UX consequence relevant here is that the phone experience is a long gallery with no action.

### What is hard-coded and how it becomes Shopify data

| Hard-coded today | Where | Shopify object / filter | Notes |
|---|---|---|---|
| The set of three products | `products[]`, lines 174-178 | `collection.products` from a section `collection` setting, `limit` setting | the featured-collection section replaces the JS array |
| Name | `p.name` | `product.title` | wrap in `<h3>` and `<a href="{{ product.url }}">` |
| Price | `p.price` | `product.price \| money` (or `money_with_currency`), `product.compare_at_price`, `product.price_varies` for "from" | formatting from store settings, never string concatenation |
| Image | `p.img` | `product.featured_image \| image_url: width` with `image_tag` widths/srcset, `alt` from `product.featured_image.alt` | second image `product.images[1]` for hover |
| Swatch colours | `p.swatches` hex list | `product.options_by_name['Color'].values` / `variant.option1`, `variant.featured_image`; option-value swatch data or a colour-name → hex map in theme settings | names come from the product data, not the theme |
| Sizes (absent) | — | `product.variants`, `product.options_with_values` | size run BUSINESS INFORMATION REQUIRED |
| Availability (absent) | — | `product.available`, `variant.available` | "Sold out" badge, disabled add |
| Link (absent) | — | `product.url` (with `within: collection`) | |
| Section copy "New Drop / The Faithful / Premium Essentials…" | lines 100-103 | section settings | Theme Editor |
| "View All Products" | line 104 | `collection.url` | |
| Currency | `data-props` enum, line 169 | store currency / Shopify Markets, `money` filters | not a theme prop (see ECOM-09 and the DATA register) |
| Cart badge "0" | line 78 | `cart.item_count` | NAV-09 |

### Verdicts

| Element | Verdict |
|---|---|
| Card composition (image / name / price / swatches order, centred, cream section) | KEEP as the design baseline |
| Card markup and data binding | REBUILD as `snippets/product-card.liquid` |
| Boxed 1:1 tile with `object-fit:cover` | IMPROVE (float on the section or use a consistent studio background per the mockup) |
| Product images | REPLACE (see the ASSET register) |
| Swatches | REBUILD as variant-driven, named controls |
| Hover / quick add / links | ADD LATER within Phase 8 |

## 13. Collection Audit

### Current state: no collection exists

The project contains one HTML file (inventory.tsv: God Squad Website.html is the only `.html`). There is no collection page, no collection template, no collection object and no collection data: the only product surface is the New Drop grid, a hard-coded array of three items (God Squad Website.html lines 174-178) rendered by `<sc-for>` (lines 107-120). The word "Collections" occurs in the page once, as the nav label (line 72).

### What the Collections link does now

`<a href="#shop">Collections</a>` (line 72) points at the same in-page anchor as `<a href="#shop">Shop</a>`: the `id="shop"` on the New Drop `<section>` (line 98). On desktop, clicking either scrolls to a section with three products and a "View All Products" button that goes to `#` (line 104). A visitor who clicks "Collections" expecting an index of ranges lands on a single mini-grid with no way onward. Below 900px the link is hidden (line 30) and there is no menu, so the word "Collections" is not reachable at all on phones and tablets (measurements.md 375/768). COLL-01, COLL-02, NAV-05.

### What the merchandising model implies

The section is titled "New Drop / The Faithful" (lines 100-101), which frames the catalogue as drops rather than categories, while the nav offers both "Shop" and "Collections" as if a category structure existed. Neither is defined anywhere. Whether collections are per drop ("The Faithful"), per product type (tees, hoodies, caps), per theme, or a mix — and what "Shop" opens versus "Collections" — is BUSINESS INFORMATION REQUIRED and must be settled before Phase 6 can build templates or menus. COLL-03.

### What a collection template needs (Shopify Online Store 2.0)

| Component | Shopify mechanism | Status | Business input |
|---|---|---|---|
| `templates/collection.json` with a main section | `sections/main-collection-product-grid.liquid` looping `collection.products` | MISSING / REQUIRED | — |
| Collection banner | `collection.title`, `collection.description`, `collection.image` | MISSING / REQUIRED | titles, descriptions, banner images: BUSINESS INFORMATION REQUIRED |
| Product card | `snippets/product-card.liquid` shared with the homepage (see §12) | MISSING (prototype markup exists to port) | — |
| Pagination | `{% paginate collection.products by N %}` | MISSING / REQUIRED | products per page: BUSINESS DECISION REQUIRED |
| Sorting | `collection.sort_options`, `?sort_by=` (best-selling, price, newest, manual) | MISSING / REQUIRED | default sort per collection |
| Filtering | `collection.filters` configured through Shopify's Search & Discovery app | MISSING / OPTIONAL | BUSINESS DECISION REQUIRED — depends on the launch catalogue size (BUSINESS INFORMATION REQUIRED); no apps in Phase 1 |
| Product count | `collection.products_count` | MISSING | — |
| Empty state | `collection.products_count == 0` branch | MISSING / REQUIRED | copy |
| Collection index page | `templates/list-collections.json`, `routes.collections_url`, `collections` loop | MISSING / REQUIRED for the COLLECTIONS nav item | taxonomy and collection images: BUSINESS INFORMATION REQUIRED |
| "All products" | `routes.all_products_collection_url` | MISSING / REQUIRED for SHOP | whether SHOP = all products |
| Breadcrumb | `collection.url`, `routes.collections_url` | OPTIONAL | — |
| Collection SEO title/description | `collection.title`, `page_description` | MISSING | see the SEO register |
| Mobile grid | 2-up at phone widths (findings-verified.json RESPONSIVE-4 suggests ~154px cards at 375; layout decision: see the RESP register) | — | — |

### Product-discovery gaps that live on the collection page

Search, filters, sorting, availability badges and recommendations are classified in §25 (ECOM-03, ECOM-04, ECOM-06, ECOM-07). The collection page is where sorting and filtering surface, so ECOM-06 is scheduled with this section in Phase 6.

### Data that does not exist yet

For even one collection to render, the store needs: real products with titles, descriptions, images, prices, variants and inventory (§12 lists what the prototype has); the collection's name, handle, description and image; its default sort order; and the menu wiring from Shop, Collections and "View All Products". All of this is BUSINESS INFORMATION REQUIRED — none of it can be inferred from the three prototype products (₱1,290 / ₱2,490 / ₱890 with three unnamed colours each).

### Classification

| Item | Classification |
|---|---|
| "Collections" nav destination (`#shop`) | REPLACE with `routes.collections_url` once the taxonomy is decided |
| "Shop" nav destination (`#shop`) | REPLACE with the shop / all-products collection URL |
| New Drop grid as the only product surface | REBUILD as a featured-collection section |
| Collection page (`collection.json`) | ADD LATER — Phase 6, REQUIRED |
| Collection index (`list-collections.json`) | ADD LATER — Phase 6, REQUIRED if COLLECTIONS stays in the menu |
| Collection taxonomy, names, images, sort defaults | BUSINESS INFORMATION REQUIRED |
| Filters | ADD LATER — OPTIONAL / BUSINESS DECISION REQUIRED |

## 14. Our Story Audit

### 14.1 What is on the page

Section#story (lines 125-139): a three-column grid (minmax(260px,.9fr) / minmax(0,1.6fr) / minmax(170px,.4fr)), an absolute image at left:30% width:70% with `object-fit:cover; object-position:center top`, a horizontal scrim (#0d0c0a to 30%, .55 at 42%, 0 at 56%), a copy column — eyebrow "Our Story" (13px .3em gold), h2 "Real People.`<br>`Bigger Purpose." (Playfair 900, clamp(32px, 4vw, 40px), 1.05), a 15px/1.65 paragraph in #e9e4d8 at max-width 320px, a gold CTA "Our Story →" to `#` — and a side column with the caption "Faith / Lives / Different / Here." (12px .22em, 1.8) and a 40px cream rule. Rendered image 998x520 at 1440, 753x461 at 768, 375x280 at 375 (measurements.md).

### 14.2 Storytelling and emotional hierarchy

The copy does its job in four beats: eyebrow, a two-line claim, one 25-word paragraph, an action. "Real People. Bigger Purpose." is the strongest line on the page after the headline and the paragraph states origin (Philippine), pillars (faith, creativity, community) and mission ("inspire a generation to live different — with purpose") without filler. The hierarchy weakens at the edges: the side caption "Faith Lives Different Here." is a fourth tagline competing with "Different People Same Purpose" (hero), "Good People. Higher Purpose." (bar) and "A Brighter Tomorrow" (footer) — the tagline system needs a canonical set (BRAND-08). The section's emotional promise is "real people" and "community"; the image delivers one stylised model with sunglasses and no second person or place cue, whereas the mockup's story image shows three people together (00-full-mockup-reference.webp; images/our-story.webp unused, inventory.tsv). The claim and the picture disagree — STORY-01's impact.

### 14.3 Readability

At 1440 the paragraph sets on a 320px measure at 15px (roughly 45 characters per line, estimated from the max-width) on a 15.4:1 background (computed from #e9e4d8 on #0d0c0a) — comfortable. The heading, however, wraps to three lines at 1440 ("REAL PEOPLE." / "BIGGER" / "PURPOSE.") and four at 1024 ("REAL" / "PEOPLE." / "BIGGER" / "PURPOSE.") because the copy column is .9fr minus 96px padding (about 350px at 1440, 220px at 1024) while the mockup sets it on two lines (FIDELITY-5; desktop-1440.png; laptop-1024.png; scratchpad/crops/l-storyhead.png). At 1024 the paragraph then runs several lines beside the photo and the CTA is pushed well down the column (laptop-1024.png). On phones the 15px paragraph is the largest running text on the page and still under the 16px mobile floor (RESPONSIVE-11) — RESP register. STORY-05 covers the heading container.

### 14.4 Image composition

Three separate problems, in order of severity:

1. Wrong asset with baked-in text. The file is ./01-hero-model-mu98p88t-7jig.webp, a 650x480 crop of the mockup's hero; fragments of the mockup headline — "A PURPOSE", "K BY", "TH." — and the "More Than Clothing" script are pixels in the image and are visible at every width, most obviously where the scrim thins: at 1440 between the copy column and the model (desktop-1440.png story region; scratchpad/crops/d1440-story-values-footer.png), and at 768 and 375 across the top of the band (scratchpad/crops/t768-story-values-footer.png; m375-story-values.png). The mockup's story image is the three-model group, which exists as images/our-story.webp (535x348) and is referenced nowhere (C1; inventory.tsv DUP-05). STORY-01, HIGH.
2. Resolution. Neither the current file nor the unused three-model crop is large enough for the slot; the required master resolution and delivery strategy are in the ASSET register, and whether a master exists is BUSINESS INFORMATION REQUIRED.
3. Crop and placement. `object-position:center top` with cover scaling discards about 29% of the picture's height at 1440 (the hands and chest, which are the gesture the mockup relies on; crop arithmetic in the findings-verified.json critic addition on the story slot), and the image starts at 30% of the section so the face sits under the copy column's right edge (scratchpad/crops/d1440-story-values-footer.png). STORY-02.

The scrim recipe itself (solid to 30%, .55 at 42%, 0 at 56%) is good and can be kept as a token (BRAND-02).

### 14.5 CTA

"Our Story →" repeats the eyebrow word-for-word, gives no hint of what lies behind it, and points to `#` (line 132) — placeholders belong to the NAV register. No About or Our Story page, and no long-form story copy, has been seen in the project; whether one exists is BUSINESS INFORMATION REQUIRED. The gold CTA is the only gold-filled element on the page and correctly signals the secondary action; its label and destination are STORY-03.

### 14.6 Mobile experience

Under 900px the section becomes one column: image band on top (`height:60vw; min-height:280px; order:-1`, line 36), then eyebrow, heading, paragraph, CTA, and finally the side caption with its rule as a 145px orphan block after the button (FIDELITY-7; RESPONSIVE-3; scratchpad/crops/m375-story-values.png shows "FAITH / LIVES / DIFFERENT / HERE." under the gold button). The vertical fade here is correctly anchored — the story has no in-flow element above the image, so it does not suffer the hero's 88px offset (RESPONSIVE-1) — but the baked-in headline fragments become the most legible thing in the band because the vertical fade only starts at 55% (scratchpad/crops/t768-story-values-footer.png, "K BY / TH." beside the model's head). Layout mechanics are in the RESP register; the content decision — hide the side caption on phones or fold it into the copy — is STORY-04.

### 14.7 Authenticity

The copy is specific (Philippine, faith, creativity, community) and reads as genuine. The imagery is not yet: the story photo is a mockup fragment of a hero model, the hero is a generated group image, and the brand's real people, city and workshop appear nowhere. Whether the brand has photography of its actual community, founders or customers is BUSINESS INFORMATION REQUIRED; with it, this section is where it belongs.

### 14.8 Theme Editor editability

Everything in the section is inline copy or a hard path (lines 125-138). The following must become section settings so the story can change without a code deploy — STORY-06 (global content inventory in the DATA register):

| Field | Current source | Proposed setting type |
|---|---|---|
| Eyebrow | line 129 text | text |
| Heading | line 130 with hard `<br>` | inline_richtext (no line breaks; either two text settings for the two lines, or rely on the minimum column width from STORY-05 to produce the two-line wrap) |
| Body | line 131 | richtext |
| CTA label | line 132 text | text |
| CTA link | line 132 href="#" | url |
| Side caption | line 136 with `<br>`s | textarea or inline_richtext |
| Image | line 126 src | image_picker (focal point set on the file) |
| Image alt | line 126 "God Squad community" | from Shopify file alt (current alt describes the unused three-model crop, not the file shown — A11Y register) |
| Image side | fixed right | select left/right |
| Scrim strength | line 127 gradient | range (with the recipe as a token) |
| Colour scheme | fixed ink | color_scheme |
| Mobile caption | n/a | checkbox show/hide (STORY-04) |

### 14.9 Classification: REBUILD

Keep the copy, the scrim recipe and the composition grammar; replace the asset, rebuild the section with a minimum copy-column width for the two-line heading, and expose the fields above.

## 15. Brand Values Audit

### 15.1 What is on the page

Section[data-r=values] (lines 142-150): a four-column grid with a hairline top and bottom border; each tile rendered from `values[]` in the data-dc-script (lines 179-184) via `<sc-for>`: a 44px icon box (`<img alt="">`), a title (13px .22em 600) and a subtitle (11px .2em #bdb6a8). Values: Faith Driven / More Than Clothing (icon-crown), Community / People With Purpose (icon-community), Worldwide / Shipping Available (icon-globe), Premium Quality / Crafted To Inspire (icon-diamond). The row is roughly 200px tall on desktop (read from scratchpad/crops/d1440-story-values-footer.png, not DOM-measured); the only measured heights are the 375 tiles, 174px each and 698px in total (measurements.md 375).

### 15.2 Icons

Four gold outline icons that match the mockup's style (00-full-mockup-reference.webp values row). They are RGBA PNGs with the gold baked in — crown 130x110, community 150x110, globe 110x110, diamond 130x110, 33-40 KB each (inventory.tsv) — drawn into a 44px-high box, so their rendered widths are 52, 60, 44 and 52 px (TECHNICAL-6). The row therefore does not sit on one optical size: Community is a third wider than Worldwide (scratchpad/crops/d1440-story-values-footer.png). The globe is the same file the announcement bar draws at 16px (line 60). Because colour is in the pixels, the icons cannot follow a colour-scheme setting, a hover or a light-background variant. Style consistency is BRAND-07; the per-icon optical box is VAL-03; format, weight and the unused sprite sheets they were cut from are in the ASSET register.

### 15.3 Hierarchy

Icon, title, subtitle is the right order and the weights are right (600 title, 400 muted subtitle). Two content issues: "More Than Clothing" duplicates the hero script word-for-word (lines 91 and 180), so the first value restates the hero instead of adding a proof point (BRAND-08); and "Worldwide / Shipping Available" is the only value that is a checkable business claim — no shipping policy, destination list or rate table has been seen in the project, so it is BUSINESS INFORMATION REQUIRED and must be verified before it ships (VAL-04). None of the tiles links anywhere; a shipping value normally links to the shipping policy — an optional block link setting (VAL-01).

### 15.4 Spacing and consistency

Tile padding 44px 24px, 10px gap, 10px icon-box margin, so icon-to-title is 20px and title-to-subtitle 10px; under 900px the padding drops to 32px 16px (line 41). The values are consistent with each other but not with any scale (BRAND-06). Dividers are the inconsistency: every tile carries `border-right:1px rgba(255,255,255,.1)` including the last (line 144), a `border-bottom` is added under 900px (line 41) and the right border removed only under 520px (line 49). At 521-900 the second column paints a 1px rule on the viewport edge and the last row's bottom border doubles with the section's own (RESPONSIVE-5; measurements.md 768). The divider logic belongs on the grid (gap plus `:nth-child` rules or a background hairline), not on each tile — VAL-02; the per-width outcome is in the RESP register.

### 15.5 Mobile layout

Under 520px the grid is one column: four tiles of 375x174 stacked to 698px, 86% of a phone screen, for four two-line labels (mobile-375-true.png values region; scratchpad/crops/m375-story-values.png; RESPONSIVE-5). Each tile's content (44px icon plus about 160px of text) fits comfortably two-up at 375 — the 768 render already shows 2x2 at 376.5px tiles with slack (measurements.md 768). Recommendation for Phase 9: 2x2 on phones with hairline dividers, 4-up from 768; the layout change itself is the RESP register's issue. Between 521 and 900 the 2x2 layout is correct apart from the stray border (15.4).

### 15.6 Accessibility

The icons are `alt=""` (line 145), which is correct — they are decorative and the title carries the meaning. The titles and subtitles are `div`s (lines 146-147), so the four values are invisible to heading navigation and read as an undifferentiated run of text; a screen reader hears "Faith Driven More Than Clothing Community People With Purpose…" with no structure (findings-verified.json critic addition on divs). Each tile should be a list item with an h3 title — HTML and A11Y registers. Contrast is fine: title cream on ink 17:1, subtitle #bdb6a8 on ink 9.7:1 (computed from the hex pairs). The 11px .2em subtitle is legible on desktop but is part of the small-tracked-caps problem on phones (RESPONSIVE-11).

### 15.7 Consistency with the mockup

Matches: four tiles, gold outline icons, vertical dividers, cream title, muted subtitle (00-full-mockup-reference.webp). Differences: none in content; the render's icon widths vary (15.2) and the mobile stacking is the build's own behaviour (the mockup has no mobile view).

### 15.8 Recommendation: Shopify section with blocks — IMPROVE

The values are marketing content the business will edit (add a fifth value, rename a subtitle, retire the shipping claim for a market), so they should be a `brand-values` section whose tiles are blocks, not hard-coded data (VAL-01; the data inventory is in the DATA register):

| Level | Setting | Type | Note |
|---|---|---|---|
| Block `value` (max 6, default 4) | icon | select from the theme's SVG icon snippet set (crown, community, globe, diamond, plus a few generic) with an image_picker fallback | resolves BRAND-07 / VAL-03 |
| | title | text | becomes an h3 |
| | subtitle | text | |
| | link | url (optional) | shipping value to policy page |
| Section | columns desktop / mobile | range 2-6 / select 1-2 | default 4 / 2 |
| | dividers | checkbox | grid-level hairlines (VAL-02) |
| | colour scheme | color_scheme | |
| | padding top / bottom | range | on the spacing scale |

The section should also allow reorder in the editor by default; the tiles' current order (faith, community, shipping, quality) reads well and can be the preset. Whether the four values are final, their order, and whether any should link are BUSINESS INFORMATION REQUIRED.

## 16. Footer Audit

### Current elements (God Squad Website.html lines 153-166)

| Element | Line | Markup | Observation |
|---|---|---|---|
| Logo | 155 | `<img src="images/WHITE FONT LOGO.png" alt="God Squad" height:56px>` in a `background:#0230` div | visible wordmark 47x36 at 1440, about half the mockup's relative size (findings-verified.json FIDELITY-4; NAV-08); wrapper colour is a zero-alpha no-op (see the CSS register) |
| Tagline | 156 | "Different People. Same Purpose." 11px #bdb6a8 tracked caps | matches mockup |
| Facebook | 160 | `<a href="#" aria-label="Facebook"><img alt="Facebook" 28x28>` | placeholder link; circled raster icon |
| Instagram | 161 | `<a href="#" aria-label="Instagram"><img alt="Instagram" 28x28>` | placeholder link |
| Divider | 163 | 1px x 28px `rgba(255,255,255,.2)` | hidden ≤900px (line 44) |
| Closing line | 164 | "A Brighter Tomorrow" 11px #bdb6a8 | matches mockup |

That is the entire footer: two taglines, one logo, two dead links. No copyright, no policy links, no contact, no newsletter, no navigation, no payment icons, no country/currency selector (findings-verified.json critic addition: "Footer has no copyright, policy, contact or navigation links"). The `<footer>` element is a proper landmark (evidence-render.md).

### Render and fidelity

At 1440 it is a single band (desktop-1440.png y 1960-2055 (footer)). At 521-900px it is forced to a column although both groups would fit one row (findings-verified.json RESPONSIVE-9 — see the RESP register); at 375 it stacks logo + tagline over icons + closing line (mobile-375-true.png y 4218-4382 (footer)). The approved mockup shows four plain glyphs (Instagram, Facebook, TikTok, YouTube); the build shows two circled icons because the user removed two placeholder boxes in the editor (C14, FIDELITY-8; uploads/pasted-1789874476205-0.png: "Removed the two placeholder boxes; footer now shows only Facebook and Instagram"). Which networks the brand actually operates is therefore an open decision — BUSINESS INFORMATION REQUIRED (FOOT-02). Icon style versus the mockup's plain glyphs: see the BRAND register; raster format and weight: see the ASSET register.

### What a production ecommerce footer needs

The spec's potential categories are SHOP, ABOUT, HELP, FOLLOW. Nothing below is invented as a link; every destination is marked.

| Column / element | Status | Shopify source | Business input |
|---|---|---|---|
| SHOP: all products, each collection, current drop | MISSING | `link_list` block bound to a footer menu | menu items and collection list: BUSINESS INFORMATION REQUIRED |
| ABOUT: Our Story, Verse, Contact | MISSING | `link_list` block; `pages[...]` | page existence and copy: BUSINESS INFORMATION REQUIRED |
| HELP: Shipping, Returns/Exchanges, Refund policy, Size guide, FAQ, Privacy, Terms | MISSING | `shop.shipping_policy`, `shop.refund_policy`, `shop.privacy_policy`, `shop.terms_of_service` (policy pages managed in admin) plus pages for size guide / FAQ | policy texts, size guide: BUSINESS INFORMATION REQUIRED |
| FOLLOW: Facebook, Instagram (+ TikTok / YouTube per mockup) | PRESENT as `#` placeholders | social URL settings in `settings_schema.json`, SVG icons | profile URLs and network set: BUSINESS INFORMATION REQUIRED (FOOT-02) |
| Newsletter / email capture | MISSING | `{% form 'customer' %}` with `contact[email]` plus `contact[tags]` = newsletter (and `contact[accepts_marketing]` where marketing consent is captured); Shopify Email or an ESP decision | BUSINESS DECISION REQUIRED (provider, copy, incentive) (FOOT-03) |
| Contact details (email, phone, address) | MISSING | text block / `shop.email` | BUSINESS INFORMATION REQUIRED |
| Copyright | MISSING | `© {{ 'now' \| date: '%Y' }} {{ shop.name }}` | legal entity name: BUSINESS INFORMATION REQUIRED |
| Payment icons | MISSING | `shop.enabled_payment_types` with `payment_type_svg_tag` | enabled gateways: BUSINESS INFORMATION REQUIRED (Phase 15) (FOOT-04) |
| Country / currency selector | MISSING | `{% form 'localization' %}` | Markets decision: BUSINESS DECISION REQUIRED (see ECOM-09) (FOOT-04) |
| Taglines "Different People. Same Purpose." / "A Brighter Tomorrow" | PRESENT | section text settings | KEEP |
| Logo | PRESENT | `image_picker` setting, trimmed asset | KEEP (asset: see the ASSET register) |
| Back-to-top / repeated primary nav for the 5.4-screen phone page | MISSING | footer menu block | see RESPONSIVE-10 (RESP register); FOOT-01 |

### Why this matters beyond completeness

- Trust: a store whose prototype shows ₱890-₱2,490 price points (real prices: BUSINESS INFORMATION REQUIRED) and a "Worldwide Shipping" promise (line 60), with no shipping, returns or contact information anywhere on the page, gives a first-time buyer nothing to check (FOOT-01, UX-05).
- Mobile wayfinding: the header scrolls away and the footer is the natural place for the menu to reappear on a 4,382px page (measurements.md 375).
- Growth: there is no email capture on the page at all (css-html-stats.txt forms 0) (FOOT-03).
- Legal/compliance: policy pages and a copyright line are standard for a Shopify store and are generated from admin content, but the content has not been seen.

### Shopify implementation

`sections/footer.liquid` inside the footer section group (`sections/footer-group.json`) with blocks: `link_list` (menu picker + heading), `text` (contact / tagline), `newsletter`, `social`; section settings for the closing line, copyright text, payment-icon toggle and localization toggle. The brand band (logo + "Different People. Same Purpose." + "A Brighter Tomorrow") should be preserved as the first row so the mockup's look survives above the utility rows.

### Classification

| Element | Classification |
|---|---|
| Brand band (logo, two taglines) | KEEP |
| Social links | IMPROVE (real URLs, decided network set, SVG icons) (FOOT-02) |
| Footer structure and content | REBUILD (SHOP / ABOUT / HELP / FOLLOW + legal row) (FOOT-01) |
| Newsletter (FOOT-03), payment icons and localization (FOOT-04) | ADD LATER — BUSINESS DECISION REQUIRED |
| Every URL, policy, contact, copyright holder | BUSINESS INFORMATION REQUIRED |

## 17. Responsive Audit

### 17.1 The responsive CSS as written

The whole responsive layer is 31 rules in two max-width queries, keyed on `[data-r]` attribute hooks and carrying 55 `!important` declarations (css-html-stats.txt: 26 rules in the 900px query, 5 in the 520px query). The base layer is the 1440 desktop composition written as 77 inline `style` attributes; the queries only subtract from it. The mechanism (inline CSS, `!important`, attribute hooks, the dead pad rule) is assessed in the CSS register; this section assesses what it produces.

All 31 rules, verbatim:

```css
@media (max-width:900px){
  [data-r=pad]{padding-left:24px!important;padding-right:24px!important}
  [data-r=hero]{grid-template-columns:minmax(0,1fr)!important;min-height:0!important}
  [data-r=hero-img]{position:relative!important;left:0!important;width:100%!important;height:62vw!important;min-height:320px!important;order:-1}
  [data-r=hero-fade]{inset:auto 0 auto 0!important;top:0!important;height:max(62vw,320px)!important;background:linear-gradient(180deg,rgba(13,12,10,0) 55%,#0d0c0a 100%)!important}
  [data-r=hero-img]{object-position:center 30%!important}
  [data-r=hero-copy]{padding:24px 24px 32px!important}
  [data-r=hero-side]{padding:0 24px 40px!important;flex-direction:row!important;align-items:center!important;gap:24px}
  [data-r=hero-side] [data-r=rule]{display:none}
  [data-r=hero-side] [data-r=script]{margin-left:0!important;transform:rotate(-6deg)!important}
  [data-r=spacer]{display:none}
  [data-r=nav]{position:relative!important;padding:16px 24px!important;order:-2}
  [data-r=nav-links]{display:none!important}
  [data-r=nav-menu]{display:flex;flex-direction:column;gap:5px}
  [data-r=logo]{height:56px!important}
  [data-r=drop]{grid-template-columns:minmax(0,1fr)!important;gap:32px!important;padding:40px 24px!important}
  [data-r=products]{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:20px!important}
  [data-r=story]{grid-template-columns:minmax(0,1fr)!important;min-height:0!important}
  [data-r=story-img]{position:relative!important;left:0!important;width:100%!important;height:60vw!important;min-height:280px!important;order:-1}
  [data-r=story-fade]{inset:auto 0 auto 0!important;top:0!important;height:max(60vw,280px)!important;background:linear-gradient(180deg,rgba(13,12,10,0) 55%,#0d0c0a 100%)!important}
  [data-r=story-copy]{padding:8px 24px 40px!important}
  [data-r=story-side]{padding:0 24px 40px!important}
  [data-r=values]{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  [data-r=value]{padding:32px 16px!important;border-bottom:1px solid rgba(255,255,255,.1)}
  [data-r=footer]{flex-direction:column!important;align-items:flex-start!important;padding:28px 24px!important;gap:24px!important}
  [data-r=footer-right]{flex-wrap:wrap;gap:18px!important}
  [data-r=vdiv]{display:none}
}
@media (max-width:520px){
  [data-r=products]{grid-template-columns:minmax(0,1fr)!important}
  [data-r=values]{grid-template-columns:minmax(0,1fr)!important}
  [data-r=value]{border-right:none!important}
  [data-r=announce]{flex-direction:column;gap:6px;text-align:center;padding:10px 16px!important}
  [data-r=hero-side]{flex-direction:column!important;align-items:flex-start!important}
}
```
(God Squad Website.html lines 18-52; the 900px query occupies lines 19-44 and the 520px query lines 47-51.) One further responsive-adjacent rule sits outside both queries: `[data-r=nav-menu]{display:none}` at line 17, which is what keeps the hamburger hidden on desktop.

The first rule in the 900px query, `[data-r=pad]` (line 19), is dead: no element in the markup carries that hook (css-html-stats.txt, "hooks styled in `<style>` but absent from markup: `pad`"). Its intended target is the announcement bar, and the consequence is measured in 17.10.

What this gives: exactly three layouts. **Desktop** (>=901px) is the absolute-overlay hero with a five-link nav; **tablet** (521-900px) flips the hero and story to stacked flow with `order:-1`/`-2`, hides the nav links, drops the hero side rule and re-rotates the script block (lines 26-27), and forces two-column products and values; **phone** (<=520px) forces one column for products and values, stacks the announcement bar and returns the hero side column to a vertical stack. There is no tier between 901 and 1440 although every grid is fluid, no min-width or container queries, and no height query. Because both queries are max-width, the tablet layout is also what a 1440 desktop gets at 160% zoom (1440/1.6 = 900 CSS px) and what any laptop up to 1800px gets at 200% (zoom200-720.png).

### 17.2 Results per width

| Width | Render | Nav | Hero | Products | Story | Values | Footer | docH |
|---|---|---|---|---|---|---|---|---|
| 375 (DPR2) | mobile-375-true.png | links hidden; inert hamburger 22x16 | 1 col; 375x320 band on top; fade offset 88px; h1 56px on 2 lines | 1 col, 327x327 tiles (2.8x device upscale) | image 375x280 on top; caption orphan after CTA | 1 col, 4x174 = 698px | column, 164px | 4,382 (5.4 screens) |
| 390 | mobile-390-true.png | same | 390x320; 88px offset; h1 2 lines | 1 col 342x342 | 390x280 | 1 col | column | 4,427 |
| 430 | mobile-430-true.png | same | 430x320; 88px offset; h1 2 lines | 1 col 382x382 | 430x280 | 1 col | column | 4,547 |
| 720 (200% zoom of 1440) | zoom200-720.png | links hidden; hamburger | 720x446 band; 88px offset; h1 1 line | 2 col, cap orphaned | on top | 2 col, stray rule | column | ~3,400 |
| 768 | tablet-768.png | links hidden; hamburger | 753x476 band; fade 41/img 129 (88 off); h1 65px 1 line | 2 col 343x343; cap alone on row 2 | 753x461 on top; caption orphan | 2 col 376.5; stray right rule | column although 230+271 fits in 705 | 3,837 |
| 900 | breakpoint-900.png | links hidden | 885x558 band; 88 off; h1 76.5px 1 line | 2 col 409x409 (1.74x) | 885x540 | 2 col | column | 4,151 |
| 901 | breakpoint-901.png | links shown | overlay; h1 ~76px on 3 lines | 3 col ~230 | overlay 70% | 4 col | row | ~2,400 |
| 920 | band-920.png | shown | 78px, 3 lines; side column overlaps the back-print model | 3 col ~235; eyebrow, names and View All wrap | overlay | 4 col | row | ~2,400 |
| 1024 | laptop-1024.png | shown; gold Home over bright photo | 87px, 3 lines | 3 col ~250; tee name wraps, price misaligned | h2 on 4 lines | 4 col | row | ~2,400 |
| 1280x720 / 1366x768 | laptop-1280-fold.png, laptop-1366-fold.png | shown | ~109/112px; first screen is hero only | not visible above the fold | - | - | - | - |
| 1440 | desktop-1440.png | shown | 1425x719 photo (0.85x); 112px on 3 lines | 3 col 288x288 (1.23x; cap 1.34x) | 998x520 (1.53x); h2 3 lines | 4 col | row | 2,055 |
| 1920 | wide-1920-fold.png | shown | 1440px box, 240px dark gutters each side; 112px cap | 288 | - | borders stop at 1440 | row | - |

(measurements.md; evidence-render.md.) Three qualifications on this table:

- **1280x720, 1366x768 and 1920 are first-screen captures only.** The blank cells are not "nothing there" but "not measured": no full-page render or docH was taken at those widths. 1280 and 1366 fall inside the 1024-1440 desktop tier with no rule change between them, so their full-page layout is expected to match 1440 at a narrower grid; 1920's below-fold behaviour is asserted from the wrapper CSS and the live 1920 DOM read, not from a full-page render (findings-verified.json gaps, TECHNICAL-8).
- **Product-name and View All wrapping is first recorded at 920**, not at 901: the 901 measurement carries only the column width (measurements.md 901: "3 | ~230"), while evidence-render.md records "At 920 the eyebrow, product names and the View All button all wrap". The exact onset between 901 and 920 is unverified.
- **The two-line "WALK BY" / "FAITH." lockup appears only below about 540px.** 375, 390 and 430 are simply the widths that were captured; the headline stays on one line at 56px down to at least 560px (findings-verified.json gaps).

No width shows measurable horizontal overflow (C11), subject to the measurement caveat in 17.11.

### 17.3 Navigation

Above 900 the nav is `position:absolute` over the photo with five text links at 12px/.2em and 44px gaps (lines 68-73). Below 900 `[data-r=nav-links]{display:none!important}` (line 30) removes the links and `[data-r=nav-menu]` (line 31) shows the three-bar span, which has no handler; the nav becomes an 88px in-flow strip (`order:-2`, line 29). The result is that tablets, phones and any zoomed desktop have no navigation at all (C5; the inert controls and placeholder hrefs are in the NAV register). The nav is `position:relative`, so on a 4,382px phone page every header control scrolls away and nothing sticky or in the footer brings it back (RESPONSIVE-10; RESP-12). At 1024 the gold Home link sits on a bright part of the photo (see the A11Y register, A11Y-03).

### 17.4 Hero

**Fade offset defect (RESP-01).** Below 900 the nav is the first in-flow child of the hero grid (88px tall at 375 and 768) and the image follows it, but `[data-r=hero-fade]` keeps `top:0` and `height:max(62vw,320px)` measured from the section (line 22). At 375 the fade spans y 59-379 while the image spans y 147-467; at 768 fade 41-517 vs image 129-605; the same 88px at 812x375 and 720 (measurements.md 375/768; findings-verified.json RESPONSIVE-1). The gradient reaches solid #0d0c0a 88px above the photo's bottom, painting a black band through the seated model, then the last 88px of photo reappear unfaded and end in a hard edge (tablet-768.png, pixel run 13,12,11 at y 450-515 then 197,180,168 at y 518; mobile-375-true.png). The story section does not have this problem because nothing precedes its image (RESPONSIVE-1, TECHNICAL-1). This is 100% of the phone/tablet hero, i.e. the LCP element on the majority of likely devices.

**Cover maths.** The single 1672x941 landscape PNG (weight and format: ASSET/PERF register) is cropped by `object-fit:cover`:

| Slot | Viewport | Box (CSS px) | Source | Cover scale | Scaled | Cropped |
|---|---|---|---|---|---|---|
| Hero | 1440 | 1425x719 | 1672x941 | 0.852 | 1425x802 | 83px vertical (10%): ~25 top / 58 bottom via `center 30%` |
| Hero | 768 | 753x476 | 1672x941 | 0.506 | 846x476 | 93px horizontal (11%); all three models visible |
| Hero | 375 | 375x320 | 1672x941 | 0.340 | 568x320 | 193px horizontal (34%), 96-97 each side; `object-position:center 30%` has no effect (no vertical slack) |
| Hero | 812x375 landscape | 797x503 | 1672x941 | 0.535 | 894x503 | 97px horizontal; band is 1.34x the viewport height |

At 375 the third model and the only on-garment message ("Built Different For A Higher Purpose") are cut mid-body (mobile-375-true.png; RESPONSIVE-8; RESP-10). `height:62vw` has no vh cap, so on landscape phones the h1 begins at y=689 (RESPONSIVE-7; RESP-09).

**Copy stack.** Under 900 the decorative side column (`More Than Clothing.` script + `A Higher Purpose.`) is kept in flow after the main copy, so at 375 a phone shows the 88px nav, a 320px image, then 352px of main copy (eyebrow, 56px h1 on two lines, the verse, the 36px rule and the three-line "Different / People / Same Purpose" tagline) and a further 211px of orphaned side-column taglines; the hero is 970px and Shop starts at y=1029 (findings-verified.json RESPONSIVE-3: heroCopy y=467 h=352, heroSide y=819 h=211, drop y=1029; RESP-04). Only the 211px side block is orphaned content; the 352px above it is the hero's own copy.

**Headline lines:** 2 lines below about 540px (56px floor, 327x99 at 375), 1 line from about 540 to 900 (65px at 768, 76.5px at 900), 3 lines "WALK / BY / FAITH." from 901 to 1920 (78, 87, ~109, 112px) because the copy column is ~450px at 1440 with `text-wrap:balance` (FIDELITY-2; findings-verified.json gaps; RESP-07).

**Side column over the back print.** From 1024 to 1440 the right-hand side column (`More Than Clothing.` and `A HIGHER PURPOSE.`) sits on top of the right model's back-print text (C17), and the same overlap is visible at 920 (band-920.png, evidence-render.md). It is present at 1440 too, so it is a desktop-wide hero-composition item owned by the hero register, not a consequence of the missing 901-1100 tier; the contrast of that overlap was not measured (18.8).

**Fold:** on 1280x720 and 1366x768 the first screen is the hero alone; no product is visible (laptop-1280-fold.png, laptop-1366-fold.png; RESP-13). Above 1440 the photo and cream band stop at the 1440 wrapper with dark gutters (wide-1920-fold.png; TECHNICAL-8; RESP-14). The seam where the photo starts under the solid nav strip is a hero-composition item for the hero register (FIDELITY-6).

### 17.5 Product grid

`repeat(3,...)` at desktop, 2 columns at 521-900, 1 column at <=520 (lines 106, 34, 47). At 375 each tile is 327x327 CSS px (654 device px) from a 235px source, a 2.8x device upscale, and the section is 1,695px tall (2.1 screens) with `View All Products` above the grid and no tappable card (RESPONSIVE-4, C2; RESP-02). At 521-900 and at 200% zoom the Utility Cap sits alone on row 2 (tablet-768.png, zoom200-720.png; C8; RESP-03). In the 901-1100 band the three columns are ~230-250px: at 920 the eyebrow, the product names and `View All Products` all wrap (band-920.png; evidence-render.md), and at 1024 "Signature Oversized Tee" wraps to two lines so the tee's price sits a line lower than the others (laptop-1024.png; C9; RESP-08). The cap crop is edge-clipped at every width: 215x190 into 288x288 = 1.516x scale, 38px cut (19 each side); into 327x327 = 1.721x, 43px cut (FIDELITY-3).

### 17.6 Our Story

Below 900 the image moves on top (`order:-1`, `height:60vw`, min 280px, line 36) and the copy follows. Cover maths: 1440 998x520 from 650x480 = 1.535x with 217px (29%) cut from the bottom; 768 753x461 = 1.158x, 95px (17%) cut; 375 375x280 = 0.583x, 4px cut, i.e. the entire crop is shown. Because the phone shows the whole crop, the baked-in headline fragments ("K BY", "TH.", "PURPOSE") are fully exposed on phones (mobile-375-true.png, tablet-768.png); the asset itself is in the STORY register (C1). The `Faith Lives Different Here.` caption plus rule becomes a 145px orphan block under the Our Story CTA at 768 and 375 (findings-verified.json RESPONSIVE-3: storyCta y=3285 h=50, storySide y=3375 h=145; FIDELITY-7; RESP-04). The h2 wraps to 3 lines at 1440 and 4 at 1024 (FIDELITY-5; hero/story registers).

### 17.7 Values

4 columns at desktop, 2 at 521-900, 1 at <=520. At 375 four tiles of 375x174 make a 698px strip (86% of a screen) for four two-line labels (RESPONSIVE-5; RESP-05). At 521-900 every tile keeps the inline `border-right:1px` (line 144), so the second column paints a stray 1px rule at the viewport edge, and the added `border-bottom` (line 41) doubles with the section's own border on the last row (tablet-768.png). Only the 520px query removes the right border (line 49).

### 17.8 Footer

`flex-direction:column` at <=900 (line 42) gives a 164px stacked footer at 768 and 375 although at 768 the two groups (230px + 271px) fit in the 705px content box with room for the 32px gap (RESPONSIVE-9; RESP-06). The footer carries no navigation links to compensate for the scrolled-away header (NAV/ECOM registers).

### 17.9 Typography

The only responsive type is the four heading clamps: h1 `clamp(56px,8.5vw,112px)` (56px at <=659, 112px at >=1318), New Drop h2 `clamp(40px,4.6vw,64px)`, story h2 `clamp(32px,4vw,40px)`, script `clamp(30px,3vw,44px)`. Everything else is fixed px:

- 9px cart badge (line 78)
- 11px/.22em announcement bar (line 58), 11px/.2em value subtitles (line 147), 11px/.26em footer taglines (lines 155, 163)
- 12px/.2em nav links (line 70) and product names (line 112), 12px/.22em both CTAs (lines 104, 132) and the story side caption (line 136)
- 13px/.3em eyebrows (lines 83, 100, 129), 13px/.24em New Drop copy (line 103), 13px/.22em value titles (line 146)
- 14px/.3em hero verse and taglines (lines 85, 87, 93), 14px untracked prices (line 113: `font-size:14px;font-weight:600`, no `letter-spacing`)
- 15px story paragraph (line 131)

(css-html-stats.txt FONT-SIZE: 5x 12px, 5x 13px, 4x 11px, 4x 14px, 1x 9px, 1x 15px.) Visible phone sizes are 9, 11, 12, 13, 14, 15 and 56px; no running text reaches 16px (RESPONSIVE-11; RESP-11). This reproduces the mockup's proportions rather than a phone scale; the 9px badge (C16) is the extreme case.

### 17.10 Spacing

Desktop gutters are 48px everywhere (announce, nav, hero-copy, drop, story-copy, footer). Below 900 the nav, hero, drop, story and footer switch to 24px, but the announcement bar keeps 48px because the rule that should change it targets `[data-r=pad]` (line 19), which no element carries (dead rule; CSS register), so at 768 the announcement text starts at x=48 while the logo and eyebrow start at x=24 (tablet-768.png). Below 520 the bar gets a third gutter, 16px (line 50). Vertical rhythm on a phone: announce 59 + hero 970 + drop 1,695 + story 797 + values 698 + footer 164 ≈ 4,382px measured docH (the section boxes sum to 4,383; 1px of rounding across them. measurements.md 375; findings-verified.json RESPONSIVE-10).

### 17.11 Touch targets, overflow, readability, CTA accessibility

**Targets** are identical at every phone width: hamburger 22x16, search/account/cart 24x24, social links 28x28, CTAs 242x50 and 169x50 (measurements.md); the size assessment is in the A11Y register (A11Y-10).

**Overflow.** `scrollWidth` equals `clientWidth` at 375, 768, 1024 and 1440 — that is, `innerWidth` minus the scrollbar where one is present (C11 correction) — and no element was found extending past the edge. That measurement is weaker than it looks: the outer wrapper carries `overflow:hidden` (God Squad Website.html line 55, `width:100%;max-width:1440px;margin:0 auto;background:#0d0c0a;overflow:hidden`), so anything extending past the wrapper box is clipped rather than reported by `scrollWidth`. "None found" therefore means "none visible through that mask", not "none exists". The one measured excess — "FAITH." exceeding its 247px content box by 17px into the section padding at 920 (findings-verified.json gaps) — sits inside the padding and never reaches the wrapper edge, which is why it produces no scrollbar. **320px was not captured**, and Phase 2 must re-test overflow at 320, 375, 390, 430, 768, 900, 920, 1024, 1440 and 1920 with the wrapper's `overflow:hidden` temporarily removed.

**Readability.** The story paragraph is 15px/1.65 with `max-width:320px` (line 131), ~45-50 characters per line at 375 (good) but 8 lines in the ~222px copy column at 1024 (laptop-1024.png).

**CTA accessibility.** Both CTAs are 50px tall, keep their full label at every width, and have working hover rules generated by the runtime (`.scp0:hover` / `.scp1:hover`; TECHNICAL-2). At 375 `View All Products` sits above the grid and the story CTA is followed by the 145px orphan caption, so neither CTA closes its section (RESP-02, RESP-04).

### 17.12 200% zoom

zoom200-720.png (720 CSS px, equivalent to 200% on a 1440 screen) shows: no horizontal scroll, text reflows, but the page enters the tablet layout: nav links gone, inert hamburger, 88px fade offset, cap orphaned, stray value rule, stacked footer, 48px announcement gutter.

At 720 CSS px there is no horizontal scroll and text reflows, but **SC 1.4.10 Reflow is defined at 320 CSS px** (400% zoom of a 1280px viewport), not at 720, and 320px was not captured — so Reflow is **UNVERIFIED**. **SC 1.4.4 Resize Text was not tested either**: findings-verified.json gaps records that "Browser zoom at 200% and OS text scaling" were not checked for wrapping or overlap under enlarged text, and every size on the page except the four heading clamps is a fixed px value (17.9). What the 720 capture does establish is a usability failure independent of conformance: a zoomed desktop user loses the entire primary navigation and is left with an inert hamburger (RESP-12; A11Y-01, A11Y-02).

### 17.13 Desktop-first problems

1. The base layer is a 1440 absolute-overlay composition; phones are produced by subtraction with `!important` (mechanism: CSS register).
2. The nav is welded into the hero and re-ordered with `order:-2`, which is the direct cause of the 88px fade offset (RESP-01).
3. Decorative side columns are kept as flow content on small screens (RESP-04).
4. A single phone tier at <=520 forces one-column products and values (RESP-02, RESP-05).
5. Image bands are sized in vw with no vh guard and from one landscape source with no art direction (RESP-09, RESP-10).
6. No phone type scale: px sizes are the mockup's (RESP-11).
7. No tier between 901 and 1440, so the fluid grids break in the 901-1100 band (RESP-08).
8. A fixed 1440 box above 1440 (RESP-14).
9. The nav disappears at <=900 with nothing functional in its place; zoomed desktops inherit that (RESP-12; NAV register).

### 17.14 Classification

| Area | Classification | Basis |
|---|---|---|
| Breakpoint strategy (two max-width tiers) | REBUILD | mobile-first tiers incl. a 901-1100 tier and a phone tier that keeps 2-up grids |
| Mobile navigation (<=900px) | REBUILD | nav links removed with an inert hamburger in their place; no menu, no sticky header (RESP-12; NAV register) |
| Hero stacking concept (image band, copy below) | IMPROVE | sound concept; anchor the fade to the image, cap band height, drop or fold side captions |
| Hero image delivery | REPLACE | art-directed portrait source delivered through `<picture>`/`srcset` (weight: ASSET/PERF register) |
| Product grid phone layout | IMPROVE | 2-up at <=520 |
| Story mobile layout | IMPROVE | caption must stay with the photo or be dropped |
| Values mobile layout | IMPROVE | 2-up on phones; border logic per column |
| Footer breakpoint | IMPROVE | stack below ~560px, not 900 |
| Phone typography | IMPROVE | add a phone scale in Phase 2 |
| Gutter system | REBUILD | one token set (CSS register) |
| Layout above 1440px | REBUILD | full-bleed section backgrounds with an inner container (RESP-14) |
| Horizontal overflow | IMPROVE | no overflow measurable, but `overflow:hidden` on the 1440 wrapper (line 55) masks it; re-test without the mask, and at 320px, in Phase 2 |

Evidence footnote: mobile-375.png and mobile-375-raw.png are clipped ~490px captures and are not cited anywhere in this section; phone composition claims use mobile-375-true.png, mobile-390-true.png and mobile-430-true.png (FIDELITY-10).

## 18. Accessibility Audit

### 18.1 Method and limits

Findings come from the source (God Squad Website.html), the rendered DOM inventory (evidence-render.md), live per-width measurements (measurements.md), pixel and composited contrast measurements (findings-verified.json critic additions) and the renders. No axe/Lighthouse run, no screen-reader session and no hands-on keyboard walkthrough were performed (findings-verified.json gaps); every claim below is tagged as source-verified, DOM-verified or inferred.

On severity: only the in-page anchors (Shop and Collections to `#shop`, Our Story to `#story`) and the two social links do anything today; the header controls — hamburger, search, account, cart — are inert for every user, so most findings below are latent rather than live, and nothing that depends on a control being operable is rated CRITICAL on that basis. The exception is document-level semantics. The missing `lang` attribute and the empty `<title>` are outright **WCAG 2.1 Level A failures** (SC 3.1.1 Language of Page, SC 2.4.2 Page Titled) and are live today for every assistive-technology user. They are carried by the HTML and SEO registers for remedy, because the fix lands in `layout/theme.liquid` during the Shopify port, but they are scored here as A11Y-11 (HIGH, P1) so that they are not lost between registers. Two further HIGH items — A11Y-01 and A11Y-03 — are what become blockers the moment the header is wired.

### 18.2 Semantic HTML and landmarks (DOM-verified)

Rendered sectioning elements: `SECTION` (hero, containing the `NAV`), `SECTION#shop`, `SECTION#story`, `SECTION` (values), `FOOTER`. No `<header>`, no `<main>`, no `lang`, empty `document.title`; the announcement bar is a `div` (C7; A11Y-11; markup and head semantics also carried by the HTML and SEO registers). Zero `<button>`, zero `<form>`, zero `tabindex`, zero `role`, three `aria-` attributes (css-html-stats.txt).

The four `<section>` elements have no accessible name, so they are exposed as generic containers and do not appear in the landmark list at all; `data-screen-label` is editor metadata and names nothing. **The only landmarks on the page are the unnamed `<nav>` inside the hero and the `<footer>`, which maps to `contentinfo` because it is not nested in a sectioning element (line 153, a direct child of the 1440 wrapper). There is no banner, no main and no named region.**

Before the runtime replaces them, `<x-dc>`, `<helmet>`, `<sc-for>` and `<sc-if>` are unknown elements; with JavaScript off the raw template renders, including a card that reads `{{ p.name }}` (ARCH/JS register). For bypass-blocks purposes there is no skip link and no `main` to skip to (A11Y-02).

### 18.3 Heading hierarchy (source-verified)

| Level | Text as authored | DOM textContent | Note |
|---|---|---|---|
| h1 | `Walk By <span>Faith.</span>` | "Walk By Faith." | correct |
| h2 | `The<br>Faithful` | "TheFaithful" | `<br>` inserts no whitespace; heading lists that concatenate text nodes read one word |
| h2 | `Real People.<br>Bigger Purpose.` | "Real People.Bigger Purpose." | same |
| (none) | product names `<div>` x3, value titles `<div>` x4 | - | products and values unreachable by heading navigation; Values and footer have no heading at all |

(God Squad Website.html lines 84, 101, 130, 112, 146; evidence-render.md.) The outline is h1 > h2 > h2 with nothing beneath; a screen-reader user jumping by heading lands on two section titles and never on a product (A11Y-08). The twelve `<br>` line breaks in hero-copy, hero-side and story-side ("Different`<br>`People`<br>`Same Purpose", "Faith`<br>`Lives`<br>`Different`<br>`Here.") are presentational breaks inside plain divs; the same concatenation applies to text search and to some heading/rotor lists.

### 18.4 Alt text and decorative images (source-verified)

| Image | alt | Context | Verdict |
|---|---|---|---|
| icon-globe.png (announcement) | "" | beside visible "Worldwide Shipping" | KEEP: correctly decorative |
| hero-group.png | "God Squad crew" | LCP photo; the right model's back print reads "Built Different For A Higher Purpose" | IMPROVE: generic; the on-garment message and setting are not conveyed; wording is BUSINESS INFORMATION REQUIRED (who is pictured, campaign name) |
| WHITE FONT LOGO.png (nav) | "God Squad" | not a link | KEEP alt; the logo should become the home link (NAV register) |
| icon-search / icon-account / icon-cart | "Search" / "Account" / "Cart" | bare `<img>`, not interactive | WRONG in context: announces functions that do not exist; when wrapped in buttons the img should be `alt=""` and the button named |
| `{{ p.img }}` | `{{ p.name }}` | product tile with the name in a div below | REDUNDANT: name announced twice; in Shopify use `product.featured_image.alt` or `""` with the card link named by the title |
| 01-hero-model-mu98p88t-7jig.webp | "God Squad community" | shows one man; pixels contain baked headline fragments | WRONG: does not describe the picture, and the baked text is invisible to AT (asset: STORY register, C1) |
| `{{ v.icon }}` x4 | "" | icon above a visible title | KEEP: correctly decorative |
| WHITE FONT LOGO.png (footer) | "God Squad" | not a link | KEEP |
| icon-facebook / icon-instagram | "Facebook" / "Instagram" inside `<a aria-label="Facebook">` | | REDUNDANT: `aria-label` and `alt` duplicate the name; make the img `alt=""` |

(God Squad Website.html lines 60, 65, 69, 76-78, 110, 126, 145, 155, 160-161; css-html-stats.txt images list.) Net, of the 12 image tags in the source: **4 correct** (announcement globe, both wordmarks, the value icons), **4 wrong** (Search, Account and Cart name functions that do not exist; the story alt describes a group that is not in the picture), **3 redundant** (the product template alt and both social alts), **1 generic** (hero). **8 of 12 need work** (A11Y-09).

### 18.5 Interactive icons and buttons (DOM-verified)

The page has no `<button>`. Search, Account and Cart are `<img>` with no link or button wrapper and are not focusable (tabIndex -1); the hamburger is `<span data-r="nav-menu" aria-label="Menu">` with no `role`, no `tabindex` and no handler (line 75); the runtime attaches no event handlers of its own (evidence-render.md). The cart badge is a bare `0` span next to the cart image (line 78), so AT reads "Cart, image, zero" by accident rather than by design. Wiring these controls is the NAV register's item (C5, C6); the semantics (button elements, names, focusability) are A11Y-01. `aria-label` on a role-less `span` is prohibited by ARIA in HTML and ignored by most screen readers (A11Y-07); support.js passes `aria-*` through to DOM elements unchanged (support.js lines 432-441), so the attribute is present in the live DOM but does nothing.

### 18.6 Keyboard navigation (DOM-verified; no live walkthrough)

Tab order at >=901px is DOM order: Home, Shop, Collections, Our Story, Verse, View All Products, Our Story CTA, Facebook, Instagram (nine stops; measurements.md). At <=900px, and therefore at 200% zoom on a 1440 display, the five nav links are `display:none` and leave the tab order, so a keyboard user has four stops (two CTAs, two social links) and no way to open a menu (zoom200-720.png; RESP-12). Unreachable at every width: hamburger, search, account, cart, swatches. No skip link (A11Y-02). All nine links are native anchors, so Enter works; there is nothing that needs Space. Enter on the six `href="#"` links scrolls to the top (NAV register).

### 18.7 Focus states (source-verified)

There is no `:focus` or `:focus-visible` rule anywhere; the only pseudo-class rules are `a:hover{color:#d8c08a}` (line 16) and the two runtime-generated `.scp0:hover`/`.scp1:hover` CTA rules (TECHNICAL-2). Focus indication is therefore the browser default ring, unbranded and different in Chromium, Firefox and Safari, and its visibility over the dark photo and on the cream band was not observed (gaps). Hover feedback exists only for text links and the two CTAs; the two social icon links have no hover or focus state at all because the icons are raster PNGs (TECHNICAL-6; A11Y-04).

### 18.8 Contrast (computed from the source hex values; nav figures measured on the render)

| Pair | Where | Ratio | Result |
|---|---|---|---|
| #f3efe6 on #0d0c0a | hero copy, value titles, story caption, CTA text | 17.0:1 | pass AAA |
| #d8c08a on #0d0c0a | eyebrows, announcement text, "Faith.", Home link, icons | 11.0:1 | pass AAA |
| #bdb6a8 on #0d0c0a | value subtitles 11px, footer taglines 11px | 9.7:1 | pass AAA |
| #e9e4d8 on #0d0c0a | story paragraph 15px | 15.4:1 | pass AAA |
| #0d0c0a on #f3efe6 | New Drop copy, product names, prices | 17.0:1 | pass AAA |
| #f3efe6 on #2a2823 (hover) | View All Products hover | 12.8:1 | pass |
| #0d0c0a on #d8c08a / #e6d3a6 | Our Story CTA and hover; cart badge | 11.0:1 / 13.3:1 | pass (the badge's 9px size, not its contrast, is the issue) |
| #f3efe6 nav links over the hero sky at 1440 | Collections / Our Story / Verse | pixel median 5.7 / 4.7 / 4.6; brightest-10% 5.0 / 4.4 / 4.2; brightest-2% 2.5 / 2.4 / 2.4; composited model 2.8 / 2.4 / 2.4 | FAIL AA (4.5:1 needed for 12px) except Collections' median |
| #f3efe6 nav links over dark hair | Home, Shop at 1440 | ~7.4-15:1 | pass |
| #d8c08a Home over the photo at 1024 | Home | ~3.5:1 | FAIL AA |
| Search/account/cart icons over the photo at 1440 | | 3.7-4.8:1 | pass 3:1 non-text, marginal |
| Cream swatch #f3efe6 with rgba(0,0,0,.25) border on the #f3efe6 section | swatch row | fill 1:1; border ~1.8:1 | FAIL 3:1 non-text if the swatch conveys availability |

(evidence-render.md nav contrast; findings-verified.json critic addition 1; God Squad Website.html lines 104, 116, 132.) Across 1440 and 1024 the three failing links span **2.4-2.9:1** (critic addition 1). The failure is a consequence of the hero photo swap plus a top fade that thins from .55 to 0 by 30% height (line 66); in the mockup the nav sits on a dark facade (A11Y-03). The h1, eyebrow and verse sit under the .92-.75 left band and are effectively on near-black; the right-column script over the back print (C17; 17.4) was not measured.

### 18.9 Touch and pointer targets (DOM-verified)

| Control | Size | WCAG 2.5.8 (24x24 AA) | 44x44 (AAA / platform guidance) | Interactive today |
|---|---|---|---|---|
| Hamburger | 22x16 | FAIL | FAIL | no |
| Search / Account / Cart | 24x24, 26px gaps | pass at the minimum | FAIL | no |
| Facebook / Instagram | 28x28, 18px gap | pass | FAIL | yes (`#`) |
| Nav links (desktop only) | 12px text, 44px gaps (line 70) | pass via spacing | pointer only | yes |
| View All Products / Our Story | 242x50 / 169x50 | pass | pass | yes |
| Swatches | 16x16, 10px gap | FAIL | FAIL | no |

(measurements.md; C15.) The header controls only become a live failure once wired, but the sizes come from the mockup and will be inherited by the rebuild unless the token is changed (A11Y-10).

### 18.10 Mobile navigation

At <=900px the accessibility tree contains no navigation links (`display:none` removes them), the hamburger is a generic span with an ignored label, and the utility icons are images (tablet-768.png, mobile-375-true.png). Assistive-technology users on phones and tablets therefore have no navigation and cannot tell that a menu is intended; the same is true of any desktop user at 200% zoom (17.12). The fix is the NAV register's menu build (C5) plus A11Y-01/A11Y-07 semantics and A11Y-10 target sizes.

### 18.11 Screen-reader labelling (source-verified)

- No `lang` on `<html>` and an empty `document.title`, so the synthesiser falls back to its default language rules and the page announces no name on load or in a tab/window list (css-html-stats.txt `<title>: ABSENT; lang attr: ABSENT`; A11Y-11).
- `aria-label="Menu"` on a `span` with no role (line 75): prohibited on generic elements, ignored (A11Y-07).
- Nine colour swatches are empty spans with inline backgrounds rgb(13,12,10), rgb(243,239,230), rgb(75,84,67) and no text, `title`, `aria-label` or `role`; no colour name appears anywhere on the page (line 116; TECHNICAL-5; A11Y-05).
- Both CTAs contain `<span>→</span>` without `aria-hidden`, so the link names are "View All Products rightwards arrow" and "Our Story rightwards arrow" (lines 104, 132; A11Y-06); the glyph's system-font fallback is in the BRAND register.
- `TheFaithful` / `Real People.Bigger Purpose.` heading textContent (A11Y-08).
- The `₱` in every price is read as "peso sign" plus digits, which is acceptable; `cur + '1,290'` string prices are the DATA register's item.
- Social links: accessible name from `aria-label`, duplicated by the img alt (A11Y-09).
- The four `<section>` elements have no accessible name, so they are generic rather than regions; `data-screen-label` is editor metadata only (18.2; HTML register).
- The rendered DOM carries 137 `data-dc-tpl` attributes and 14 `.sc-interp` wrapper spans inside text runs (TECHNICAL-7); these are inert for AT but are runtime bookkeeping (ARCH/JS register).

### 18.12 Reduced motion (source-verified)

No `prefers-reduced-motion` query, and none is needed yet: the stylesheet and inline styles contain zero `transition` and zero `animation` declarations; of the 22 `transform` matches, 20 are `text-transform:uppercase` and the two real transforms are static `rotate(-8deg)` on the Kaushan Script block (line 91) and its `rotate(-6deg)` override inside the 900px query (line 27, quoted in 17.1); css-html-stats.txt: `reduced-motion query present: False; transition 0, animation 0, transform 22`. No carousel, parallax, autoplay or scroll effects exist. The menu drawer, cart drawer and hover transitions planned for Phases 4 and 8 are the point at which the query becomes required.

### 18.13 Links (DOM-verified)

Nine links: Home `#`, Shop `#shop`, Collections `#shop`, Our Story `#story`, Verse `#`, View All Products `#`, Our Story CTA `#`, Facebook `#`, Instagram `#`. Six are placeholders and two destinations collide (NAV register). Link text is descriptive for all text links; the two social links have empty visible text but a valid `aria-label` name (pass). The active Home state is colour plus a 1px underline (line 71), so it does not rely on colour alone; hover is colour-only (gold) on text links and absent on the icon links.

### 18.14 Severity summary and classification

| ID | Issue | Severity | Priority |
|---|---|---|---|
| A11Y-01 | Header controls are images/spans: not focusable, not operable, no button semantics | HIGH | P1 |
| A11Y-03 | Nav links fail contrast over the hero sky (2.4-2.9:1) | HIGH | P1 |
| A11Y-11 | Missing `lang` and empty `<title>` — WCAG 2.1 Level A failures (SC 3.1.1, SC 2.4.2) | HIGH | P1 |
| A11Y-02 | No skip link, no main landmark, no named regions (only nav and contentinfo exist) | MEDIUM | P2 |
| A11Y-04 | No focus styling; default ring only; icon links have no state at all | MEDIUM | P2 |
| A11Y-05 | Swatches have no accessible name; cream swatch 1.8:1 | MEDIUM | P2 |
| A11Y-08 | Heading outline stops at two h2s; "TheFaithful" | MEDIUM | P2 |
| A11Y-09 | Wrong, redundant or generic alt text on 8 of 12 images | MEDIUM | P2 |
| A11Y-10 | Targets 16-28px in the header and swatches | MEDIUM | P2 |
| A11Y-06 | CTA arrow announced as "rightwards arrow" | LOW | P3 |
| A11Y-07 | aria-label on a role-less span | LOW | P3 |

Classification: colour tokens and text contrast on solid backgrounds KEEP (all pairs 9.7:1 or better); nav-over-photo treatment REBUILD; header control semantics REBUILD; document-level semantics (`lang`, `<title>`, `main`, `header`) REBUILD in the theme layout; alt text IMPROVE; heading structure IMPROVE (product and value titles as headings); focus styling ADD LATER in Phase 2 tokens, applied in Phase 14; reduced-motion handling ADD LATER with the first animated component; accessibility conformance target BUSINESS INFORMATION REQUIRED.

Untested, and therefore unscored: SC 1.4.10 Reflow at 320 CSS px, SC 1.4.4 Resize Text, the keyboard walkthrough, a screen-reader pass, an axe/Lighthouse run and forced-colors mode (findings-verified.json gaps). Phase 14 must run all six before any conformance statement is made.

## 19. SEO Audit

### Scope and evidence
The static `<head>` holds only a charset meta, a viewport meta and the runtime script (God Squad Website.html lines 3-7). Everything else the page declares lives inside the design's `<helmet>` (lines 10-53): the Google Fonts preconnect and stylesheet link plus one `<style>` block, which support.js clones into `<head>` at boot (evidence-render.md). css-html-stats.txt reports `<title>` ABSENT, lang ABSENT, meta description ABSENT, canonical ABSENT, og ABSENT, favicon link ABSENT, robots meta ABSENT, ld+json ABSENT; viewport and charset present. Live at 1440 `document.title` is empty (evidence-render.md), and, because no icon of any kind is declared, a normal browser tab will request `/favicon.ico` and receive a 404 (evidence-render.md; not exercised by the headless capture or the Browser pane, findings-verified.json gaps).

### Exists / missing

| Element | Prototype | Evidence | What the Shopify theme must provide |
|---|---|---|---|
| `<title>` | MISSING; `document.title` empty | css-html-stats.txt; evidence-render.md | `page_title` + `shop.name` pattern in `layout/theme.liquid`; homepage title copy (BUSINESS INFORMATION REQUIRED) |
| Meta description | MISSING | css-html-stats.txt | `page_description` with a shop-level fallback; description copy (BUSINESS INFORMATION REQUIRED) |
| Canonical | MISSING | css-html-stats.txt | `canonical_url` on every template |
| Open Graph / Twitter card | MISSING; no share-format image among the 44 site files | css-html-stats.txt; inventory.tsv | `snippets/meta-tags.liquid` (og:site_name, og:url, og:title, og:type, og:description, og:image, twitter:card); a 1200x630 share image via theme settings (BUSINESS INFORMATION REQUIRED) |
| Favicon / touch icon | MISSING; no icon of any kind is declared, so a normal tab will request `/favicon.ico` and receive a 404 (predicted; not observed in this capture) | css-html-stats.txt (favicon link: ABSENT); findings-verified.json gaps | Theme `image_picker` rendered with `image_url: width: 32` plus Apple touch icon; a square mark asset (BUSINESS INFORMATION REQUIRED; no square or vector mark seen, section 21) |
| Robots meta, robots.txt, sitemap.xml | MISSING (none of the 44 site files) | inventory.tsv; css-html-stats.txt | Shopify-native `/robots.txt` (`robots.txt.liquid` only for custom rules) and `/sitemap.xml`; Shopify noindexes cart, search and account itself |
| Structured data | MISSING (no `ld+json`) | css-html-stats.txt | JSON-LD Organization (name, url, logo, sameAs), Product + Offer (price, priceCurrency, availability) on product templates, BreadcrumbList on collection and product |
| `<html lang>` | MISSING (HTML register) | css-html-stats.txt | `lang="{{ request.locale.iso_code }}"` |
| Viewport, charset | PRESENT | HTML lines 4-5 | Keep |
| `content_for_header` | n/a in the prototype | - | Mandatory in `layout/theme.liquid` |

### Semantic headings
The outline is h1 "Walk By Faith." (line 84), h2 "The Faithful" (line 101) and h2 "Real People. Bigger Purpose." (line 130) and nothing else (evidence-render.md). Product names (line 112) and value titles (line 146) are `<div>`s, the values section and footer have no heading, and the `<nav>` sits inside the hero `<section>` (line 68). A crawler therefore sees one hero heading and two editorial headings and no product-level structure; the shop section's only crawlable label with commerce meaning is the eyebrow div "New Drop /" (line 100), because its h2 reads "The Faithful". The markup fix (product names as h3, `<header>`/`<main>`, section headings) belongs to the HTML register; in Shopify the product-card snippet will output `product.title` as a heading linked to `product.url`.

### Image alt text
All 12 `<img>` elements carry an alt attribute (css-html-stats.txt). Correctly decorative: announcement globe alt="" (line 60) and value icons alt="" (line 145). Informative: hero "God Squad crew" (line 65), wordmark "God Squad" (lines 69, 155), products `{{ p.name }}` (line 110), story "God Squad community" (line 126), Facebook/Instagram (lines 160-161, duplicating the link aria-label). Two SEO-relevant defects (SEO-08): the story alt describes a community while the file shows one capped model (findings-verified.json C1; tablet-768.png), and product alts are bare names, so the cap image is described only as "Utility Cap". The Search/Account/Cart alts (lines 76-78) label images that are not controls, which is a labelling matter for the A11Y register. In Shopify alt comes from `image.alt` set in the admin, so alt copy per product image must be written (BUSINESS INFORMATION REQUIRED).

### URLs
One document, nine links: Home `#`, Shop `#shop`, Collections `#shop`, Our Story `#story`, Verse `#`, View All Products `#`, Our Story CTA `#`, Facebook `#`, Instagram `#` (css-html-stats.txt). Six are placeholders (NAV register). Two distinct labels resolve to one hash, so "Collections" and "Shop" are not distinguishable destinations; there are no product, collection, policy, search or account URLs and no internal-link graph for a crawler to follow (SEO-09). The document itself is requested as `God%20Squad%20Website.html` (evidence-render.md), a space-in-URL pattern that must not carry into theme asset names (ASSET-07).

### Content hierarchy and indexability
Indexable copy is roughly 120 words in total, with one 25-word paragraph (line 131) that is the only mention of the brand name and category ("Philippine streetwear brand") in running text, and no product descriptions (SEO-11). The product grid and the value tiles exist only as an `<sc-for>` template with literal `{{ p.name }}` / `{{ v.title }}` placeholders (lines 107-120, 143-149) plus data in a `text/x-dc` script (lines 169-188). support.js hides the whole `<x-dc>` at parse time (support.js lines 1818-1821, 1906) and reveals content only after React and ReactDOM arrive from unpkg (evidence-render.md). A crawler that does not execute JavaScript therefore indexes raw template text containing `{{ p.name }}`, while a client that does execute the script but cannot reach unpkg indexes a blank page, because `hideRawTemplate()` hides `<x-dc>` before React is even requested and `boot()` never runs to reveal it (support.js lines 1818-1821, 1906-1910; findings-verified.json C13 corrections). Googlebot's renderer will see the products, but only through the CDN dependency (SEO-10; the runtime itself is in the ARCH register). Liquid renders products and blocks server-side, which removes this class of problem by construction.

### What the Shopify theme must provide
1. `layout/theme.liquid`: `lang`, the `<title>` pattern, `page_description`, `canonical_url`, `content_for_header`, the favicon setting and the preconnects (PERF-03).
2. `snippets/meta-tags.liquid` for Open Graph and Twitter, with a settings-driven share image.
3. `snippets/structured-data.liquid`: Organization on every page (logo = the vector or square mark from section 21, sameAs = confirmed social URLs), Product + Offer on `templates/product.json`, BreadcrumbList on collection and product.
4. Headings: one h1 per template (hero on index, `product.title` on product), h2 per section, h3 per product card.
5. Alt text from `image.alt`; decorative SVG icons `aria-hidden` (section 22).
6. Real URLs: `routes.*`, `collection.url`, `product.url`, policy pages; the "Verse" destination and the "Collections" target are undefined (BUSINESS INFORMATION REQUIRED).
7. Sitemap and robots are Shopify-native; nothing to build.

Issues raised in this section: SEO-01 to SEO-11.

## 20. Performance Audit

### First-load payload (served over HTTP, cold cache)

| Group | Files | Bytes | Share of local page weight | Source |
|---|---|---|---|---|
| images/hero-group.png (RGB PNG, no alpha, 1672x941) | 1 | 1,989,201 | 79.8% | inventory.tsv |
| Icon PNGs (RGBA, 110-150 px) | 9 | 308,521 | 12.4% | inventory.tsv |
| images/WHITE FONT LOGO.png (500x500 RGBA, two placements) | 1 | 37,836 | 1.5% | inventory.tsv |
| ./01-hero-model-mu98p88t-7jig.webp (story, 650x480) | 1 | 39,966 | 1.6% | inventory.tsv |
| Product WebP (235x230, 235x235, 215x190) | 3 | 31,342 | 1.3% | inventory.tsv |
| support.js | 1 | 69,150 (19,037 gz) | 2.8% | bundle-sizes.txt |
| God Squad Website.html (fetched twice per load) | 1 | 15,632 (4,081 gz) | 0.6% | bundle-sizes.txt; evidence-render.md |
| Local total referenced | 17 | 2,491,648 | 100% | measurements.md |
| react 18.3.1 UMD (unpkg) | 1 | 10,751 (4,263 gz) | external | bundle-sizes.txt |
| react-dom 18.3.1 UMD (unpkg) | 1 | 131,835 (42,818 gz) | external | bundle-sizes.txt |
| Google Fonts CSS + 5 woff2 files | 6 | 7,461 + 152,880 | external | evidence-render.md |

Over the wire this is roughly 2.6 MB on a cold cache, of which about 2.4 MB is image data; the hero alone is four fifths of everything the page owns. @babel/standalone (3,137,752 B) is referenced by the runtime but not loaded by this page (bundle-sizes.txt). The 17.2 MB (17,185,754 B) project folder is a disk problem, not a network one (section 21).

### Images: size, dimensions, format
- hero-group.png: 1,989,201 B, 1672x941, PNG colour type 2, RGB with no alpha (findings-verified.json, critic addition "Hero PNG has no alpha"). There is no transparency to preserve, so the PNG container buys nothing over a lossy photographic format; the reviewers expect roughly an order of magnitude reduction at equal visual quality, to be measured in Phase 3. Rendered at 1425x719 CSS px at 1440 (0.85x) and as a 375x320 band at 375, where the cover crop discards about 34% of the scaled width and roughly 66% of the picture remains visible (measurements.md 375; God Squad Website.html lines 21, 65 object-fit:cover — below 900px the image becomes an in-flow box of height max(62vw,320px), so the 1672x941 file is drawn at 320/941 = 0.34 scale, a scaled width of about 569 px inside a 375 px viewport). One file serves every viewport (PERF-01); the crop itself is in the RESP register.
- Icons: nine RGBA PNGs of 28-42 KB on four canvases (110x110, 130x110, 150x110, 130x130), drawn at 16-44 px (evidence-render.md): about 30 KB per placement for glyphs an SVG expresses in under 1 KB (findings-verified.json TECHNICAL-6; ICON-01).
- Wordmark: 500x500 RGBA, 37,836 B, drawn in a 78 px / 56 px box with only a 66x50 px visible mark (FIDELITY-4; ASSET-06).
- Products: 9-12 KB WebP, the right format at the wrong resolution: 235 px natural rendered at 288 px (1.23x) at 1440 and at 327 CSS px = 654 device px (2.8x) at 375 DPR2 (C2; measurements.md).
- Story: 39,966 B WebP, 650x480 rendered at 998x520 (1.53x; 3.07x on a 2x display) (findings-verified.json, critic addition on the story slot).
- Request-level duplicates: none (icon-globe.png is one request for two placements). Disk-level duplicates are in section 21.
- Sprites: icons-sprite.png (833,929 B) and social-sprite.png (927,973 B) are not requested by the page (inventory.tsv referenced_by none); they cost disk, not bandwidth.

The pattern is inverted: far too many pixels where they do not matter (hero on phones, icons, padded logo) and too few where they do (products, story).

### JavaScript and the render chain

| Script | Raw | Gzip | How loaded |
|---|---|---|---|
| support.js | 69,150 | 19,037 | `<script src>` in `<head>`, synchronous and parser-blocking (HTML line 6) |
| react.production.min.js | 10,751 | 4,263 | appended by support.js with `async=false` and SRI (support.js 1143-1146, 1823-1846) |
| react-dom.production.min.js | 131,835 | 42,818 | same |
| Executed per load | ~211 KB | ~66 KB | measurements.md |

Sequence (support.js 1906-1910): `hideRawTemplate()` injects `x-dc{display:none!important}` synchronously (1818-1821); `loadReactUmd()` appends both unpkg scripts; only when both resolve do `init()`/`boot()` parse the template, evaluate the data block and mount React. `boot()` also re-fetches `location.href` and re-renders from the raw text (line 159), so the HTML is requested twice and the page renders twice per load (TECHNICAL-7). Nothing paints until three dependent network hops (HTML, then support.js, then React and ReactDOM) complete, so the JavaScript is render-blocking in effect even though the CDN scripts are not parser-blocking. If unpkg fails the page stays blank (C13 and its critic additions). Each load also produces two observed 404s for `/{{ p.img }}` and `/{{ v.icon }}` (C3); a third, for `/favicon.ico`, is predicted for a normal browser tab but was exercised by neither the headless capture nor the Browser pane (SEO-05; findings-verified.json gaps). The hero `<img>` is created by the parser inside the hidden template, so its download does start early (the placeholder 404s prove images inside `<x-dc>` are requested before the runtime runs), but its paint waits for React. The runtime is owned by the ARCH register; the performance requirement for the theme is that none of it survives.

### CSS
2,916 B in the embedded `<style>` plus 6,421 characters across 77 inline `style` attributes, 55 `!important` declarations and two media queries (css-html-stats.txt); the runtime adds a page stylesheet and the generated `:hover` sheet at boot (evidence-render.md). Byte-wise negligible; the cost is structural and belongs to the CSS register. The Google Fonts `<link>` and the `<style>` live inside the body `<helmet>` and are cloned into `<head>` during render (TECHNICAL-9).

### Fonts

| Face | Files | Bytes | Used by |
|---|---|---|---|
| Jost 400 / 500 / 600 | 3 | 79,728 (26,576 each) | body, nav, labels, CTAs |
| Kaushan Script 400 | 1 | 34,748 | "More Than Clothing." only (line 91) |
| Playfair Display 900 | 1 | 38,404 | h1 and both h2 |
| Playfair Display 700 | 0 | 0 (declared, never used) | - (C12) |
| Google Fonts CSS | 1 | 7,461 | 19 @font-face blocks (latin, latin-ext, cyrillic, vietnamese) |

152,880 B of woff2 in total (evidence-render.md). The only preconnect is to fonts.googleapis.com, without `crossorigin` (line 11); the files come from fonts.gstatic.com, which has no preconnect, so each face waits for the CSS and then a fresh connection (TECHNICAL-9). `display=swap` means the 112 px Playfair 900 headline first paints in Georgia and re-flows on swap; whether that changes the three-line stack was not measured (findings-verified.json gaps). Kaushan Script is 23% of the font bytes for one three-word line (PERF-04). The peso sign and the arrow fall back to system glyphs because Jost lacks them (BRAND register). PERF-03.

### External resources
Three third-party origins at runtime: unpkg.com (two scripts), fonts.googleapis.com (CSS) and fonts.gstatic.com (font files) (evidence-render.md). None has a complete preconnect. unpkg disappears with the runtime; the fonts should move to Shopify's font settings or to `assets/` (PERF-03). Whether fonts may be fetched from Google's servers at all is a privacy-policy question for the business (BUSINESS INFORMATION REQUIRED).

### Lazy loading, decoding, dimensions
None of the 12 `<img>` elements in the source has `loading`, `decoding`, `srcset`, `sizes`, `width` or `height` (evidence-render.md). All 15 image files (17 placements) download on every load at every width, the 11 below-fold placements competing with the hero. Layout shift is mostly contained by fixed boxes: the hero and story images are absolutely positioned above 900px and the hero becomes an in-flow box of height max(62vw,320px) below it (God Squad Website.html line 21), so either way its height is reserved; product tiles use `aspect-ratio:1/1` (line 109) and value icons sit in a 44 px box (line 145), but the wordmark is `height:78px;width:auto` (line 69), so the nav's left column has no width until the PNG arrives (PERF-05).

### Hero image and LCP
The LCP element at every width is hero-group.png: 1425x719 at 1440, 753x476 at 768, 375x320 at 375 (measurements.md). It is a 1.99 MB PNG with no `<link rel="preload">`, no `fetchpriority`, no responsive candidates and no intrinsic dimensions, and its paint is gated behind about 66 KB gz of JavaScript in three hops. On 1366x768 and 1280x720 laptops the first screen is the hero alone (laptop-1366-fold.png, laptop-1280-fold.png), so nothing else competes for the fold. No LCP figure exists: LCP did not report and CLS read 0 only on a warm localhost load; no throttled run was made (findings-verified.json gaps). PERF-01, PERF-02, PERF-06.

### DOM complexity
166 elements after render at every width (measurements.md): trivial. The rendered DOM does carry 137 `data-dc-tpl` attributes and 14 `.sc-interp` wrapper spans (TECHNICAL-7), editor bookkeeping that vanishes with the runtime.

### Performance requirements the theme inherits from this audit
- Hero delivered through the Shopify CDN as WebP with a width ladder and a phone-specific crop, preloaded and marked `fetchpriority="high"` on the `<img>` itself (PERF-01, PERF-02).
- Every icon inline SVG, removing about 308 KB (ICON-01); wordmark as SVG (ASSET-06).
- Fonts through Shopify font settings or self-hosted woff2 with preload for the two above-the-fold faces and correct preconnects (PERF-03, PERF-04).
- Below-fold images lazy with intrinsic dimensions (PERF-05).
- No render-blocking JavaScript; theme scripts deferred (ARCH register for the runtime removal).
- A measured Lighthouse baseline before and after (PERF-06).

Issues raised in this section: PERF-01 to PERF-06.

## 21. Asset Audit

### Inventory summary
44 site files, 17,185,754 B (inventory.tsv). Two further files in the folder are not site assets and are excluded from the classification below: `.claude/launch.json` (228 B), dev-server tooling added by the audit lead (evidence-render.md), and PHASE-1-WEBSITE-AUDIT.md (493,032 B), this report; counting them the folder is 46 files and 17,679,014 B. No pre-existing project file was created, modified or deleted.

The page references 17 files totalling 2,491,648 B, 14.5% of the site files: 15 image files, support.js and the HTML itself (measurements.md). Nine md5 duplicate groups contain 11 redundant copies, 6,733,692 B or 39% of the site files. The remaining unreferenced files are mockups, editor screenshots, generated exports and two AI icon sheets.

No file was created, renamed or deleted by this audit. The entry page's rename from "God Squad Website.dc.html" to "God Squad Website.html" on 2026-09-20 at 15:34 was the owner's own deliberate change, with content unchanged (evidence-render.md). Every class below is a Phase 3 recommendation.

Roles used: MASTER (highest-resolution source seen), WEB (referenced by the page), MOCKUP (crop of the approved mockup), REFERENCE (screenshots and mockups kept for comparison), TEMP (editor-generated or stray upload). "Referenced" is taken from the source only; the inventory's README tag is a loose name match, not a reference (measurements.md).

### Classification of every asset

| # | Path | Bytes | Dims / type | Referenced by | Role | Class | Reason |
|---|---|---|---|---|---|---|---|
| 1 | God Squad Website.html | 15,632 | HTML | entry page | WEB | KEEP | Design baseline; deliberately renamed from "God Squad Website.dc.html" by the owner on 2026-09-20, content unchanged (evidence-render.md); never copied into the theme |
| 2 | support.js | 69,150 | JS | HTML line 6 | WEB | KEEP | Prototype runtime required to view the baseline; its conversion fate is in the ARCH register; not a theme asset |
| 3 | .thumbnail | 25,542 | 640x355 WebP | none | TEMP | REMOVE | Claude Design editor preview, regenerated by the editor (evidence-render.md) |
| 4 | 01-hero-model-mu98p88t-7jig.webp | 39,966 | 650x480 WebP | HTML line 126 (story) | MOCKUP / WEB | REPLACE | Hero crop of the mockup with baked-in headline fragments (C1), 1.53x upscaled; wrong subject for Our Story (STORY register); sits at the project root |
| 5 | chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png | 1,989,201 | 1672x941 RGB PNG | none | TEMP | REMOVE | DUP-01, byte-identical to images/hero-group.png |
| 6 | white-font-300x300-mu98qi59-mytq.png | 23,444 | 244x184 RGBA | none | TEMP | ARCHIVE | Trimmed wordmark export; differs by md5 from the Desktop "WHITE FONT 300x300.png" (md5 check); unused |
| 7 | white-font-trans-mu98q2ez-zrdd.png | 43,606 | 500x500 RGBA | none | TEMP | UNKNOWN | Same byte size as #8 but different md5; which encode is the approved wordmark is undocumented |
| 8 | white-font-trans-mu98qky0-5tt6.png | 43,606 | 500x500 RGBA | none | TEMP | UNKNOWN | As #7 |
| 9 | images/WHITE FONT LOGO.png | 37,836 | 500x500 RGBA | HTML lines 69, 155 | WEB | REPLACE | Raster wordmark on a padded canvas (visible mark 66x50 px in a 78 px box, FIDELITY-4); byte-identical to Desktop "WHITE FONT Trans.png" (md5 c247ae94); class REPLACE (SVG wordmark, ASSET-06); if Phase 3 cannot obtain vector artwork the fallback is a trimmed re-export of this PNG, a Phase 3 decision rather than a second class here |
| 10 | images/hero-group.png | 1,989,201 | 1672x941 RGB PNG | HTML line 65 | MASTER / WEB | OPTIMIZE | Only original-resolution hero; no alpha; deliver as CDN WebP derivatives (PERF-01); approval and higher-resolution source open (ASSET-05) |
| 11 | images/hero-model.webp | 39,966 | 650x480 WebP | none | MOCKUP | ARCHIVE | DUP-02 with uploads 01; mockup hero crop, low resolution |
| 12 | images/icon-account.png | 28,470 | 110x110 RGBA | HTML line 77 | WEB | REPLACE | Raster UI icon; SVG target (ICON-01) |
| 13 | images/icon-cart.png | 29,127 | 110x110 RGBA | HTML line 78 | WEB | REPLACE | Raster; residual badge sliver at the right edge (ICON-02); SVG target |
| 14 | images/icon-community.png | 39,978 | 150x110 RGBA | data block line 181 | WEB | REPLACE | Raster value icon; SVG target |
| 15 | images/icon-crown.png | 33,339 | 130x110 RGBA | data block line 180 | WEB | REPLACE | Raster value icon; SVG target |
| 16 | images/icon-diamond.png | 34,556 | 130x110 RGBA | data block line 183 | WEB | REPLACE | Raster value icon; SVG target |
| 17 | images/icon-facebook.png | 36,771 | 130x130 RGBA | HTML line 160 | WEB | REPLACE | Two-tone circled badge; official SVG glyph target (ICON-03) |
| 18 | images/icon-globe.png | 35,625 | 110x110 RGBA | HTML line 60; data block line 182 | WEB | REPLACE | One raster used at 16 px and 44 px; SVG target |
| 19 | images/icon-instagram.png | 42,319 | 130x130 RGBA | HTML line 161 | WEB | REPLACE | As #17 |
| 20 | images/icon-search.png | 28,336 | 110x110 RGBA | HTML line 76 | WEB | REPLACE | Raster UI icon; SVG target |
| 21 | images/icons-sprite.png | 833,929 | 2172x724 RGBA | none | TEMP (AI sheet) | ARCHIVE | Sheet the nav and value icons were cut from; heavy red/yellow matting and baked labels (icons-sprite.png); provenance only (ASSET-02) |
| 22 | images/logo.png | 47,147 | 500x500 RGBA | none | MOCKUP | ARCHIVE | White wordmark on solid black; byte-identical to uploads/God-Squad-Images/06-logo.png (DUP-04), so it belongs to the mockup crop set, not the web set; possible avatar source, not a theme asset |
| 23 | images/our-story.webp | 41,004 | 535x348 WebP | none | MOCKUP | ARCHIVE | The mockup's three-model story crop; DUP-05; too small for the slot and carries caption fragments at its right edge (our-story.webp) |
| 24 | images/product-cap.webp | 10,002 | 215x190 WebP | data block line 177 | MOCKUP / WEB | REPLACE | Mockup crop (README.txt), non-square, upscaled everywhere (C2, FIDELITY-3); placeholder until photography exists (ASSET-03) |
| 25 | images/product-hoodie.webp | 12,328 | 235x235 WebP | data block line 176 | MOCKUP / WEB | REPLACE | As #24 |
| 26 | images/product-tee.webp | 9,012 | 235x230 WebP | data block line 175 | MOCKUP / WEB | REPLACE | As #24 |
| 27 | images/social-sprite.png | 927,973 | 2172x724 RGBA | none | TEMP (AI sheet) | ARCHIVE | Source of the social badges; 30 badges in three styles with matting artefacts (social-sprite.png) |
| 28 | uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png | 833,929 | 2172x724 | none | TEMP | REMOVE | DUP-03 copy of #21 |
| 29 | uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png | 833,929 | 2172x724 | none | TEMP | REMOVE | DUP-03 copy of #21 |
| 30 | uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png | 927,973 | 2172x724 | none | TEMP | REMOVE | DUP-09 copy of #27 |
| 31 | uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png | 1,989,201 | 1672x941 | none | TEMP | REMOVE | DUP-01 copy of #10 |
| 32 | uploads/GODSQUAD WEBSITE MOCKUP.png | 1,872,888 | 1024x1536 RGB PNG | none | MASTER (mockup) | KEEP | The approved design master; archive outside the theme, never shipped |
| 33 | uploads/pasted-1789874083026-0.png | 17,311 | 118x77 RGB | none | TEMP | REMOVE | Globe icon crop pasted into the editor |
| 34 | uploads/pasted-1789874193900-0.png | 1,541,839 | 1920x1009 | none | REFERENCE | ARCHIVE | Claude Design editor screenshot; collectively these three record the deliberate hero-photo replacement, the gold-globe request and the footer-social removal (evidence-render.md, editor history); which screenshot shows which decision is not recorded |
| 35 | uploads/pasted-1789874322321-0.png | 769,319 | 1920x1009 | none | REFERENCE | ARCHIVE | As #34 |
| 36 | uploads/pasted-1789874476205-0.png | 1,550,034 | 1920x1009 | none | REFERENCE | ARCHIVE | As #34 |
| 37 | uploads/God-Squad-Images/00-full-mockup-reference.webp | 182,250 | 1024x1536 WebP | none | REFERENCE | KEEP | Web-weight copy of the mockup used for every fidelity comparison in this audit |
| 38 | uploads/God-Squad-Images/01-hero-model.webp | 39,966 | 650x480 | none | MOCKUP | REMOVE | DUP-02 copy of #11 |
| 39 | uploads/God-Squad-Images/02-product-oversized-tee.webp | 9,012 | 235x230 | none | MOCKUP | REMOVE | DUP-08 copy of #26 |
| 40 | uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp | 12,328 | 235x235 | none | MOCKUP | REMOVE | DUP-07 copy of #25 |
| 41 | uploads/God-Squad-Images/04-product-utility-cap.webp | 10,002 | 215x190 | none | MOCKUP | REMOVE | DUP-06 copy of #24 |
| 42 | uploads/God-Squad-Images/05-our-story-models.webp | 41,004 | 535x348 | none | MOCKUP | REMOVE | DUP-05 copy of #23 |
| 43 | uploads/God-Squad-Images/06-logo.png | 47,147 | 500x500 | none | MOCKUP | REMOVE | DUP-04 copy of #22 |
| 44 | uploads/God-Squad-Images/README.txt | 556 | text | none | REFERENCE | ARCHIVE | Provenance note stating the crops come from the 1024x1536 mockup, i.e. no original product photography exists (README.txt) |

Class totals: KEEP 4, OPTIMIZE 1, REPLACE 14, ARCHIVE 10, REMOVE 13, UNKNOWN 2 (44 site files).

### Duplicate groups (md5)

| Group | md5 prefix | Canonical copy | Redundant copies | Bytes wasted |
|---|---|---|---|---|
| DUP-01 | c5f73461 | images/hero-group.png | root chatgpt-image-...-evm9.png; uploads/ChatGPT Image ... 11_06_34 AM.png | 3,978,402 |
| DUP-02 | 6d545230 | images/hero-model.webp | uploads/God-Squad-Images/01-hero-model.webp | 39,966 |
| DUP-03 | e5f38184 | images/icons-sprite.png | uploads/ChatGPT Image ... 10_11_00 AM.png; ...-34af7243.png | 1,667,858 |
| DUP-04 | 01f17bc1 | images/logo.png | uploads/God-Squad-Images/06-logo.png | 47,147 |
| DUP-05 | 07accc16 | images/our-story.webp | uploads/God-Squad-Images/05-our-story-models.webp | 41,004 |
| DUP-06 | 6953fcaf | images/product-cap.webp | uploads/God-Squad-Images/04-product-utility-cap.webp | 10,002 |
| DUP-07 | 935f2d96 | images/product-hoodie.webp | uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp | 12,328 |
| DUP-08 | 1f0e2e02 | images/product-tee.webp | uploads/God-Squad-Images/02-product-oversized-tee.webp | 9,012 |
| DUP-09 | 59f7085f | images/social-sprite.png | uploads/ChatGPT Image ... 10_56_48 AM.png | 927,973 |
| Total | | 9 groups | 11 copies | 6,733,692 |

Near-duplicates that are not byte-identical: ./01-hero-model-mu98p88t-7jig.webp versus images/hero-model.webp (same 650x480, same 39,966 B, different md5: a separate re-encode, C1 corrections), and the two root white-font-trans PNGs (same 43,606 B, different md5).

### Asset roles
- Master assets: uploads/GODSQUAD WEBSITE MOCKUP.png (design master, 1024x1536) and images/hero-group.png (the only full-resolution image; AI-generated according to its upload filename, unconfirmed by the business). No product, story or logo master exists inside the project.
- Web assets (referenced): 15 images, support.js and the HTML.
- Mockup assets: the six crops in uploads/God-Squad-Images, their images/ copies (including images/logo.png, DUP-04) and the root story re-encode; README.txt states they are crops of the mockup.
- Reference screenshots: three 1920x1009 editor screenshots and 00-full-mockup-reference.webp.
- Temporary/generated: .thumbnail, the hash-suffixed root exports (chatgpt-image-..., white-font-...), the pasted globe crop, the "ChatGPT Image ..." uploads, and the two AI icon sheets images/icons-sprite.png and images/social-sprite.png, generated artwork kept only for provenance (ASSET-02).

### External logo sources (outside the project, read-only)
C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES holds OG LOGO.psd (613,320 B), OG LOGO 300x300.psd (209,976 B), OG LOGO-assets/OG LOGO.png (45,633 B), BLACK FONT.png (182,337 B), WHITE FONT.png (41,377 B), WHITE FONT Trans.png (37,836 B, md5-identical to images/WHITE FONT LOGO.png) and WHITE FONT 300x300.png (17,674 B) (directory listing; md5 check). No SVG, AI or EPS was seen anywhere. The PSDs were not opened; whether their layers are vector shapes exportable as SVG is BUSINESS INFORMATION REQUIRED (ASSET-06).

### Image quality

| Asset | Natural | Rendered (1440 / 768 / 375) | Usage | Sufficient? | Higher-resolution master needed? |
|---|---|---|---|---|---|
| product-tee.webp | 235x230 | 288x288 / 343x343 / 327x327 (654 device px at DPR2) | product card image | NO: 1.23x at 1x desktop, 2.8x device upscale on phones, visibly soft (C2) | YES: original photography, 2000 px or more on the long edge, consistent square framing (BUSINESS INFORMATION REQUIRED) |
| product-hoodie.webp | 235x235 | same | same | NO | YES |
| product-cap.webp | 215x190 | 289x289 (1.34x, edge-cropped) / 343 / 327 | same | NO: also non-square, brim clipped (FIDELITY-3) | YES |
| hero-group.png | 1672x941 | 1425x719 / 753x476 / 375x320 | hero background, LCP | 1x desktop YES (0.85x); 2x desktop NO (about 2850 px needed, 1.7x upscale); phones limited by composition, not pixels — the 375x320 cover box draws the file at 0.34 scale and crops about 34% of its scaled width (RESP register) | YES for HiDPI and for a portrait phone crop; approval, provenance and usage rights of the image are also open (BUSINESS INFORMATION REQUIRED) |
| hero-model.webp (and the root re-encode in use) | 650x480 | 998x520 / 753x461 / 375x280 | Our Story background | NO: 1.53x at 1x, 3.07x at 2x, 29% of height cropped, mockup text baked in (C1) | YES: a photograph at least 2000 px wide (BUSINESS INFORMATION REQUIRED) |
| our-story.webp | 535x348 | not rendered (unused) | candidate story image | NO: 1.87x at 1x, 3.7x at 2x; caption fragments at the right edge | YES |

None of these should be upscaled or replaced in Phase 1; they remain placeholders until masters arrive (ASSET-03, ASSET-04, ASSET-05).

### Shopify delivery strategy (recommendation for Phases 3, 10 and 12)
- Upload masters at full resolution to product media and Files; let the CDN derive sizes. Render with `image_tag`, which writes `src`, `width` and `height` from the `image_url` it is given, and pass the ladder explicitly — `{{ product.featured_image | image_url: width: 1600 | image_tag: widths: '375,550,750,1100,1500', sizes: '(min-width:990px) 33vw, 50vw', loading: 'lazy' }}` — because `image_url: width:` on its own emits no `srcset` and no `sizes`. The CDN negotiates WebP automatically for supporting browsers (`image_url`'s `format:` accepts jpg, pjpg, png and webp; AVIF is not a Shopify CDN output format).
- Hero: `preload: true` (emits `<link rel="preload" as="image">`; `fetchpriority="high"` must be added on the `<img>` itself, which image_tag does not write), a width ladder from phone to 2x desktop (roughly 750 to 2880), `sizes` tied to the 1440 max-width, plus an art-directed portrait crop for phones via `crop:` or a second image setting.
- Product cards: `sizes` matched to the grid (about 33vw desktop, 50vw tablet, and 100vw or 50vw on phones depending on the Phase 9 decision), `loading="lazy"` below the fold, square framing from `product.featured_image` with a centre crop.
- Story: widths 750 to 2000, `sizes` tied to the 70% column, lazy.
- Logo: SVG in `assets/` via a theme `image_picker`; favicon 32/180/512 derived from the square mark.
- Icons: inline SVG snippets (section 22), no image requests.

Issues raised in this section: ASSET-01 to ASSET-08.

## 22. Icon Audit

### Inventory

| Icon | File | Canvas / bytes | Rendered | Colour in file | Problems observed | Target |
|---|---|---|---|---|---|---|
| Search | images/icon-search.png | 110x110 RGBA / 28,336 | 24x24 nav (line 76) | cream line glyph | Raster; colour baked; soft cut edge; bare `<img>` that is not a control (NAV and A11Y registers) | SVG snippet with `currentColor` inside a button or link |
| Account | images/icon-account.png | 110x110 / 28,470 | 24x24 (line 77) | cream | As Search | SVG snippet linked to `routes.account_url` |
| Cart | images/icon-cart.png | 110x110 / 29,127 | 24x24 plus CSS badge (line 78) | cream | As Search; a sliver of the sheet's gold "0" badge remains at the right edge of the file (icon-cart.png) while the page draws its own 14 px badge (ICON-02) | SVG snippet plus a Liquid `cart.item_count` badge |
| Crown | images/icon-crown.png | 130x110 / 33,339 | 52x44 values (data line 180) | gold | Raster; heavier stroke than the nav set; non-square canvas | SVG in the values section block |
| Community | images/icon-community.png | 150x110 / 39,978 | 60x44 (data line 181) | gold | Raster; widest canvas, so optically larger than its neighbours (ICON-05) | SVG block icon |
| Globe | images/icon-globe.png | 110x110 / 35,625 | 16x16 announcement (line 60) and 44x44 values (data line 182) | gold | One raster at two sizes; strokes blur at 16 px; gold in the bar versus the mockup's white is a deliberate edit (FIDELITY-9; BRAND register) | SVG, colour set by CSS per placement |
| Diamond | images/icon-diamond.png | 130x110 / 34,556 | 52x44 (data line 183) | gold | Raster | SVG block icon |
| Facebook | images/icon-facebook.png | 130x130 / 36,771 | 28x28 footer (line 160) | gold ring, light disc, gold glyph | Two-tone badge cut from the social sheet; differs from the mockup's plain glyph (FIDELITY-8); cannot take `a:hover` gold; alt duplicates aria-label (A11Y register) | Official monochrome SVG glyph, `currentColor` (ICON-03) |
| Instagram | images/icon-instagram.png | 130x130 / 42,319 | 28x28 (line 161) | same | As Facebook | Same |
| Nav/feature sheet | images/icons-sprite.png | 2172x724 / 833,929 | not used | mixed cream and gold | AI-generated sheet with red/yellow matting halos, baked labels and mixed sets (icons-sprite.png); source of the nine cut-outs | None: ARCHIVE (ASSET-02) |
| Social sheet | images/social-sprite.png | 2172x724 / 927,973 | not used | gold and cream | Same class of artefacts; 30 badges in three styles; its own baked footer text claims "PNG & SVG" but no SVG exists (social-sprite.png) | None: ARCHIVE (ASSET-02) |
| Hamburger | none (three CSS spans, line 75) | - | 22x16 | cream | Pure CSS; no close state; not a control (NAV register) | SVG `icon-menu` and `icon-close` inside a button (ICON-04) |
| CTA arrow | none (text "→", lines 104 and 132) | - | 12 px glyph | inherits | Glyph is not in Jost and renders in a system fallback (BRAND register); announced as "rightwards arrow" (A11Y register) | SVG `icon-arrow`, `aria-hidden` (ICON-04) |

Totals: nine files, 308,521 B, ten placements (evidence-render.md).

### Problems across the set
1. Raster. Every icon is a PNG cut from an AI-generated sheet; edges are anti-aliased against the sheet's matte, so at 16-28 px they read slightly soft. The 110 px nav masters hold 4.6x headroom at 24 px, but the value icons at 44 px have only 2.5x (110 px canvas height drawn at 44 px; widths 130/150/130/110 drawn at 52/60/52/44), and none can be regenerated at another size without returning to the sheet.
2. Colour baked. Cream for the nav set, gold for values and social; no hover, focus, active or theme-colour state is possible without CSS filters, and the global `a:hover{color:#d8c08a}` (line 16) has no effect on the social links (TECHNICAL-6).
3. Matting and artefacts. The sheets show heavy red/yellow fringing; icon-cart.png carries a badge remnant; the social badges include a light disc that will not sit on a cream background. The footer is dark today, but the theme's colour settings must not be constrained by an icon file.
4. Geometry. Four canvas sizes (110x110, 130x110, 150x110, 130x130), two stroke weights and rendered widths of 52/60/44/52 px at the same 44 px height (inventory.tsv dims; findings-verified.json TECHNICAL-6); no grid.
5. Weight. About 30 KB per placement versus under 1 KB for an SVG path; 308 KB in total.
6. Coverage. No close, chevron, plus/minus, check, filter, external-link or arrow icon exists for the mobile drawer, cart drawer, accordions and product page, and the mockup's TikTok and YouTube glyphs have no counterpart (C14).

### Target: one inline-SVG snippet system
- A single `snippets/icon.liquid` taking `name`, `size` (default 24) and `class`, emitting `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false">` with a `case` on the name (or the per-icon snippets the spec lists: icon-search, icon-account, icon-cart, icon-menu, icon-close, icon-arrow). One grid, one stroke weight, colour inherited from the parent through the Phase 2 colour tokens, so hover and focus states and the theme colour settings apply everywhere.
- Value icons (crown, community, globe, diamond): SVG paths in the same snippet chosen by a `select` block setting, with an optional `image_picker` fallback for merchant-supplied artwork.
- Social icons: official monochrome glyphs from each network's brand resources as SVG; which networks are shown and their URLs are a business decision (BUSINESS INFORMATION REQUIRED); circled versus plain is a BRAND decision.
- Cart badge: Liquid `cart.item_count` in a span sized for two digits (its 9 px size is a UX register item).
- Hamburger: SVG rather than CSS spans, so menu and close share one system and one button.
- PNG: none. External asset (icon font, CDN sprite): none; an inline system needs no requests and cannot flash unstyled glyphs. CSS-only drawing is kept for the badge dot and dividers, never for glyphs.

Issues raised in this section: ICON-01 to ICON-05, plus ASSET-02 for the sheets.

## 23. Data Architecture Audit

### 23.1 Method

Every literal that a store would expect to manage was located in `God Squad Website.html` (the only place content exists; support.js carries no God Squad data) and assigned a future home in the Shopify model: **Product data** (products, variants, images, prices), **Collection data**, **Theme settings** (`config/settings_schema.json`), **Section settings**, **Block settings**, **Navigation menus** (linklists), **Metafields**, **Shopify settings** (store admin: currency, markets, money format, shop name, policies) or **Business configuration** (facts the owner must supply). Where a value is unknown or unconfirmed it is marked BUSINESS INFORMATION REQUIRED; nothing below is invented. Ownership note: brand colour and font tokens are catalogued here for completeness but their issues sit in the BRAND and CSS registers; placeholder hrefs and inert controls sit in the NAV register; head/meta data in the SEO register.

### 23.2 Product data (DATA-01, DATA-02, DATA-03)

The entire catalogue is three object literals in `renderVals()` (God Squad Website.html lines 174-178):

| Field today | Values (verbatim) | Form | Future home |
|---|---|---|---|
| `name` | Signature Oversized Tee; Heavyweight Hoodie; Utility Cap | string in JS | `product.title` (Product data) |
| `price` | `cur + '1,290'`; `cur + '2,490'`; `cur + '890'` | symbol + formatted string, no numeric value | `product.price \| money` (Product data + Shopify settings money format); the amounts are placeholders until confirmed: BUSINESS INFORMATION REQUIRED |
| `img` | images/product-tee.webp (235x230); images/product-hoodie.webp (235x235); images/product-cap.webp (215x190) | relative file path | `product.featured_image \| image_url` with `srcset` (Product data); current files are mockup crops (C2) and cannot be the production images: BUSINESS INFORMATION REQUIRED (photography) |
| `swatches` | `['#0d0c0a','#f3efe6','#4b5443']` on all three (hoodie order differs) | unnamed hex array, inert | `product.options_by_name['Color'].values` + colour metafield or the Color category metafield (Product data + Metafields); colour names and per-product availability: BUSINESS INFORMATION REQUIRED |
| Missing entirely | handle, description, variants (size run), SKU, inventory, compare-at price, vendor, type, tags, secondary images, availability, `product.url` | n/a | Product data and Metafields; all BUSINESS INFORMATION REQUIRED |
| Card link | none (`[data-r=products] a` count = 0, TECHNICAL-4) | n/a | `product.url` |
| Grid membership | "New Drop / The Faithful" is a fixed list of three | JS array | Collection data: a `collection` section setting (`type: "collection"`) with `collection.products` limited by a range setting; which collection this is and what "View All Products" targets (`collection.url` or `routes.all_products_collection_url`): BUSINESS INFORMATION REQUIRED |

### 23.3 Currency and the editor prop (DATA-02)

`data-props` declares `{"currency":{"editor":"enum","default":"₱","options":["₱","$","€"],"tsType":"string","section":"Shop"}}` (line 169), consumed as `this.props.currency ?? '₱'` (line 172) and exposed as a dropdown in the Claude Design editor (pasted-1789874322321-0.png). It is the prototype's only "setting" and it only changes the symbol: choosing `$` renders `$1,290` for the same item (TECHNICAL-4). In Shopify the concept does not exist as a theme setting: the store currency, money format and any additional presentment currencies are **Shopify settings** (store admin and Markets), and prices are rendered with `| money` / `| money_with_currency`. The prop must be dropped, not ported. Whether the store sells in PHP only or in multiple currencies/markets is a BUSINESS DECISION REQUIRED. Separately, the ₱ glyph falls back to a system font (see the BRAND register).

### 23.4 Brand values (DATA-04)

Four objects (lines 180-183): Faith Driven / More Than Clothing / icon-crown.png; Community / People With Purpose / icon-community.png; Worldwide / Shipping Available / icon-globe.png; Premium Quality / Crafted To Inspire / icon-diamond.png. Rendered by `<sc-for list="{{ values }}">` (143-149). Future home: a `brand-values` section with **Block settings** per tile (icon select or `image_picker`, `title`, `subtitle`), max four blocks, defaults seeded with the current strings. "Worldwide / Shipping Available" is a policy claim, not copy: BUSINESS INFORMATION REQUIRED (shipping zones).

### 23.5 Navigation, utility bar and footer links (DATA-05, DATA-08)

| Item | Location | Current value | Future home |
|---|---|---|---|
| Main menu | lines 71-72 | Home `#`; Shop `#shop`; Collections `#shop`; Our Story `#story`; Verse `#` | **Navigation menus**: `linklists[section.settings.menu]` with a `link_list` section setting (default `main-menu`); active state from `link.current` instead of the hard-coded gold underline on Home (line 71). Destinations for Shop, Collections, Verse and the Our Story page: BUSINESS INFORMATION REQUIRED |
| Search / Account / Cart (binding only; the inert controls are in the NAV register) | lines 76-78 | bare `<img>`, no hrefs | `routes.search_url`, `routes.account_url` (guarded by `shop.customer_accounts_enabled`), `routes.cart_url` (Shopify settings/routes) |
| Cart badge | line 78 | literal text `0` | `cart.item_count` (live cart object) |
| Announcement bar | lines 58-61 | "Good People. Higher Purpose." / globe / "Worldwide Shipping" | `announcement-bar` section in the header group with text/link **Section settings**; the shipping claim is BUSINESS INFORMATION REQUIRED |
| Hero CTA target | (none; hero has no CTA) | n/a | Section setting `url` if a CTA is added in PHASE 5 — HERO |
| View All Products | line 104 | `#` | `collection.url` or `routes.all_products_collection_url` (Collection data) |
| Our Story CTA | line 132 | `#` | Section setting `url` pointing at a page: which page: BUSINESS INFORMATION REQUIRED |
| Social links | lines 160-161 | Facebook `#`, Instagram `#`; TikTok/YouTube removed by a deliberate edit (C14) | **Theme settings** `social_facebook_link`, `social_instagram_link`, `social_tiktok_link`, `social_youtube_link`, rendered only when populated; URLs and final set: BUSINESS INFORMATION REQUIRED / BUSINESS DECISION REQUIRED |
| Footer legal, policies, contact, newsletter | absent (critic addition 7) | n/a | `shop.policies`, `routes`, `shop.email`, `customer_form` newsletter: content BUSINESS INFORMATION REQUIRED (see the ECOM register for the feature gap) |

### 23.6 Copy (DATA-06, DATA-09)

All text is inline in the template, often with layout-bearing `<br>` tags (12 in the source, css-html-stats.txt line 181):

| Section | Strings (verbatim) | Lines | Future home |
|---|---|---|---|
| Announcement | Good People. Higher Purpose.; Worldwide Shipping | 59-60 | Section settings (text) |
| Hero | Streetwear with a Purpose; Walk By Faith. ("Faith." gold); 2 Corinthians 5:7; Different / People / Same Purpose; More / Than / Clothing.; A Higher / Purpose. | 83-93 | Section settings: eyebrow (text), heading (`inline_richtext` so the gold word survives), verse reference (text), tagline (richtext), script caption (text), side caption (richtext) |
| New Drop | New Drop /; The / Faithful; Premium Essentials / for a Higher Purpose.; View All Products | 100-104 | Section settings: eyebrow, heading, subheading, button label + `url`; collection picker (23.2) |
| Our Story | Our Story; Real People. / Bigger Purpose.; paragraph "God Squad is a Philippine streetwear brand built on faith, creativity, and community. We create pieces that inspire a generation to live different — with purpose."; Our Story (button); Faith / Lives / Different / Here. | 129-136 | Section settings: eyebrow, heading, richtext body, button label + `url`, caption. The "Philippine" origin statement and any long-form story page copy: BUSINESS INFORMATION REQUIRED |
| Values | see 23.4 | 180-183 | Block settings |
| Footer | Different People. / Same Purpose.; A Brighter Tomorrow | 156, 164 | Footer section settings (text); copyright entity and year: BUSINESS INFORMATION REQUIRED |
| Image alt text | God Squad crew; God Squad; God Squad community; Search; Account; Cart; Facebook; Instagram; `{{ p.name }}` | 60-161 | `image.alt` from the picker / `product.featured_image.alt`; UI labels ("Search", "Cart", "Menu", "Account") from `locales/en.default.json` |
| Shop name | "God Squad" as logo alt only | 69, 155 | `shop.name` (Shopify settings) |

### 23.7 Images (DATA-07)

Fifteen image files referenced 17 times (icon-globe and the logo twice each), all as relative paths in the template or the data script: `images/icon-globe.png` (x2), `images/hero-group.png`, `images/WHITE FONT LOGO.png` (x2), `images/icon-search.png`, `images/icon-account.png`, `images/icon-cart.png`, `./01-hero-model-mu98p88t-7jig.webp`, `images/icon-facebook.png`, `images/icon-instagram.png`, three product WebPs, `images/icon-crown.png`, `images/icon-community.png`, `images/icon-diamond.png` (lines 60-183; css-html-stats.txt lines 185-197; 17 image requests per load, evidence-render.md line 28). Future homes: logo -> **Theme settings** `image_picker` (SVG once a vector master exists, INV-05); hero and story photographs -> **Section settings** `image_picker` rendered with `image_url`/`image_tag` and `srcset`; product images -> **Product data**; UI and value icons -> theme SVG snippets (`icon-search.liquid` etc.) or a block `select` of named icons, not image files. Every current photographic asset is a mockup crop or AI generation; production masters are BUSINESS INFORMATION REQUIRED.

### 23.8 Tokens, layout constants and editor metadata (cross-referenced)

| Item | Location | Future home | Register |
|---|---|---|---|
| Colours `#0d0c0a`, `#f3efe6`, `#d8c08a`, `#bdb6a8`, `#e9e4d8`, `#ebe6dc`, hover `#2a2823`/`#e6d3a6`, swatch `#4b5443` | inline + `<style>` (css-html-stats.txt lines 8-26; hover values from `style-hover` at lines 104 and 132; swatch value from lines 175-177) | Theme settings colour scheme(s) -> CSS custom properties | BRAND / CSS |
| Fonts Playfair Display 900, Jost 400/500/600, Kaushan Script 400 | line 12 | Theme settings `font_picker` (heading, body); Kaushan Script as a decorative setting or self-hosted asset | BRAND / CSS |
| Page width `max-width:1440px`, gutters 48/24/16 px, breakpoints 900/520 | lines 18-55 | Theme settings (page width) and the Phase 2 spacing scale | CSS / RESP |
| `data-r`, `data-screen-label`, `hint-placeholder-*` | 25 distinct hooks (26 occurrences), 4 sections | Dropped; replaced by BEM/section classes | HTML / CSS |
| `data-props` currency enum | line 169 | Dropped (23.3) | DATA-02 |
| `<title>`, description, canonical, OG, favicon | absent | `theme.liquid` head from `page_title`, `page_description`, `canonical_url`, settings favicon | SEO |

### 23.9 Target data model summary

| Shopify home | Items from this page |
|---|---|
| Product data | 3 products: title, price, featured image, images, variants (size/colour), availability, url, description, SKU, inventory |
| Collection data | the "New Drop / The Faithful" grid source; "View All Products" target; future Collections nav target |
| Theme settings | logo, favicon, colour scheme, fonts, page width, social links, (money format is a store setting) |
| Section settings | announcement text; hero eyebrow/heading/verse/taglines/image; New Drop eyebrow/heading/subheading/button/collection/limit; Our Story eyebrow/heading/body/button/url/image/caption; footer taglines; header menu picker |
| Block settings | 4 value tiles (icon, title, subtitle); optionally hero taglines as blocks |
| Navigation menus | main menu (Home, Shop, Collections, Our Story, Verse); footer menus (SHOP / ABOUT / HELP, once defined) |
| Metafields | colour swatch hex/name per variant option value; optional verse reference per product/collection |
| Shopify settings | shop name, currency and markets, money format, policies, customer accounts, routes |
| Business configuration | shipping zones behind "Worldwide Shipping", brand origin statement, social profile set, legal entity, story page copy, real prices, size runs, photography and vector logo |

### 23.10 Data findings

The prototype contains no data model at all: three products and four values as JS literals, one symbol-only currency prop, nine links of which six are `#`, a literal cart count, and copy welded to markup with `<br>`. None of it is wrong as a design baseline, but every item must be re-homed (DATA-01 to DATA-09) and most of the real values do not yet exist in the project (BUSINESS INFORMATION REQUIRED list below).

## 24. Shopify Compatibility Audit

### 24.1 What was evaluated and the verdict

The prototype was measured against every structural requirement of a Shopify Online Store 2.0 theme: the seven-directory tree, `layout/theme.liquid`, Liquid syntax, JSON templates, sections with `{% schema %}`, blocks, snippets, the flat `assets/` folder, `config/settings_schema.json` and `settings_data.json`, `locales/`, the `product`, `collection`, `cart`, `search` and `customer` objects, section groups and the Theme Editor.

Verdict: the prototype is a Claude Design 'dc' document, not a theme, and no part of it is compatible as code. It consists of one 190-line HTML file (15,632 B) whose entire visible markup sits inside a custom `<x-dc>` element (God Squad Website.html lines 9-168) and a generated 69,150 B runtime, support.js, which hides that template synchronously (support.js lines 1818-1822), loads React 18.3.1 and ReactDOM from unpkg.com (lines 1143-1146), evaluates the page's data class with `new Function` (lines 844-850) and mounts it with `ReactDOM.createRoot` (lines 196-197). The project root holds `images/`, `uploads/`, `.claude/`, `.thumbnail` and loose PNG/WebP exports (inventory.tsv, 44 files); none of `layout/`, `sections/`, `snippets/`, `templates/`, `assets/`, `config/` or `locales/` exists (SHOP-01). The only editor-facing setting in the project is the `currency` enum in `data-props` on line 169, which the Claude Design editor exposes as a dropdown (pasted-1789874193900-0.png, top-left 'currency ₱'); Shopify's Theme Editor has no way to see it (SHOP-02).

The owner renamed the file from 'God Squad Website.dc.html' to 'God Squad Website.html' on 2026-09-20 at 15:34; the content is unchanged and no Phase 1 work touched the file (evidence-render.md). Phase 1 is inspection-only and the spec forbids renaming production files (PHASE-1-SPEC.md line 30), so the rename is recorded here as the owner's act, not the audit's. The spec's references to the old name mean this file, and the rename changes nothing about compatibility: the runtime still boots under the new suffix, and it boots from `file://` as well — only the React fetch from unpkg needs the network (evidence-render.md).

### 24.2 Compatibility table

Prototype status uses CURRENT / MISSING; Shopify need uses REQUIRED / OPTIONAL / BUSINESS DECISION REQUIRED; disposition uses KEEP / IMPROVE / REBUILD / REPLACE / REMOVE / ADD LATER.

Citation note, used in §24, §27 and §29: findings-verified.json holds 48 `confirmed` findings with ids (C1-C18, FIDELITY-1..10, RESPONSIVE-1..11, TECHNICAL-1..11), two `refuted` ids (C4, C18) and eight `critic_additions` entries that carry **no ids of their own**. This report numbers those eight ADD-1 to ADD-8 in file order: **ADD-1** nav links fail contrast over the hero sky at 1024 and 1440; **ADD-2** the whole page is blank if React cannot be fetched (`file://` itself is fine); **ADD-3** the peso sign and the arrow are not in Jost and fall back to a system face; **ADD-4** the Our Story slot needs an image of at least 2,000 px; **ADD-5** the hero PNG has no alpha, so PNG buys nothing; **ADD-6** no favicon, meta description, canonical or Open Graph/Twitter tags; **ADD-7** the footer has no copyright, policy, contact or navigation links (the mockup omits them too; open decision); **ADD-8** product names and value titles are plain divs, CTA arrows are unlabelled glyphs and the hamburger's `aria-label` sits on a role-less span.

| # | OS 2.0 requirement | Prototype status | Shopify need | Disposition | What must change | Evidence |
|---|---|---|---|---|---|---|
| 1 | Theme directory tree (`assets/ config/ layout/ locales/ sections/ snippets/ templates/`) | MISSING | REQUIRED | REBUILD | Create the seven directories; `images/` and `uploads/` do not map to any of them (SHOP-01). | inventory.tsv; project root listing |
| 2 | `layout/theme.liquid` with `content_for_header` and `content_for_layout` | MISSING | REQUIRED | REBUILD | The `<head>` is charset, viewport and `<script src="./support.js">` only (lines 3-7); the layout must carry the section groups, the meta-tags snippet and the CSS variables snippet. Head tags: see the SEO register. | God Squad Website.html lines 1-8 |
| 3 | Liquid output tags `{{ }}` | CURRENT as dc interpolation (14 placeholders, lines 107-149) | n/a | REPLACE | Identical delimiters: Liquid resolves `{{ products }}`, `{{ p.name }}`, `{{ s }}` to nil and outputs empty strings; `{{ false }}` (lines 110, 145) prints the word false. Rewrite as `{% for product in section.settings.collection.products %}` with `product.title`, `product.price \| money`, `product.featured_image`. Runtime/delimiter issue: see the ARCH register. | findings-verified.json TECHNICAL-3; support.js 407-409 |
| 4 | Control flow `{% for %}` / `{% if %}` | CURRENT as `<sc-for>` (x3) and `<sc-if>` (x2) | n/a | REPLACE | Runtime-only tags parsed by `walkFor`/`walkIf` (support.js 555-556, 611, 646); Liquid leaves them as unknown elements. See the ARCH register. | css-html-stats.txt custom elements |
| 5 | Data source | CURRENT as `class Component extends DCLogic { renderVals() }` (lines 170-187) | n/a | REPLACE | Products come from a collection object, values from section blocks, the currency symbol from the store money format. Hardcoded content: see the DATA register. | support.js 1708 (class is mandatory for boot) |
| 6 | Standard HTML only | CURRENT with `<x-dc>`, `<helmet>`, `style-hover`, `data-r`, `data-screen-label`, `hint-placeholder-*` | n/a | REMOVE | None is recognised outside support.js; `helmet` is rewritten to `sc-helmet` by the runtime (support.js 377-378); the working `style-hover` rules (TECHNICAL-2 — support.js generates `.scp0:hover` / `.scp1:hover`, verified live) must be re-expressed as ordinary `:hover` CSS. Markup attributes: see the HTML register. | css-html-stats.txt nonstandard attributes; evidence-render.md style-hover |
| 7 | JSON templates (`templates/*.json`) | MISSING | REQUIRED | REBUILD | `index.json` plus the storefront set in §29.5. | project root listing |
| 8 | Sections with `{% schema %}` | MISSING | REQUIRED | REBUILD | Four `<section>` elements, a `<nav>`, a `<footer>` and an announcement `<div>` exist as markup only; the `<nav>` is absolutely positioned inside the hero `<section>` (line 68 inside line 64) so header and hero cannot be separate sections as built (SHOP-04). | lines 58-166; TECHNICAL-11 |
| 9 | Blocks | MISSING | REQUIRED | REBUILD | The four value tiles (data lines 179-183), the hero side captions (lines 91-93) and the two announcement messages (lines 59-60) are natural blocks; the footer has no link groups today (lines 153-166 hold the logo, 'Different People. Same Purpose.', two `href="#"` social links, a divider and 'A Brighter Tomorrow'), so footer link-list blocks are an ADD LATER recommendation and BUSINESS INFORMATION REQUIRED (ADD-7). | lines 59-60, 91-93, 153-166; data-dc-script 179-183; findings-verified.json ADD-7 |
| 10 | Snippets | MISSING | REQUIRED | REBUILD | The product card is inline inside `<sc-for>` (lines 108-119); it becomes `snippets/product-card.liquid`. | lines 106-121 |
| 11 | Section groups (`sections/header-group.json`, `footer-group.json`) | MISSING | REQUIRED | REBUILD | Announcement bar and header into the header group, footer into the footer group; requires SHOP-04 to be resolved first. | spec §23 |
| 12 | Flat `assets/` | MISSING (files live in `images/`, root and `uploads/`) | REQUIRED | REBUILD | Shopify `assets/` has no subfolders; `images/WHITE FONT LOGO.png` (spaces, requested as `WHITE%20FONT%20LOGO.png`) and the `./01-hero-model-mu98p88t-7jig.webp` root reference must be renamed and relocated (SHOP-06). 44 files totalling 17,185,754 B sit in the folder; only 17 (2,491,648 B) are referenced by the page, and 9 md5 duplicate groups account for 11 redundant copies. Content and product images belong in Shopify Files and product media, not `assets/`. Weight, format and duplicates: see the ASSET register. | TECHNICAL-10; inventory.tsv; measurements.md inventory summary |
| 13 | `config/settings_schema.json` + `settings_data.json` | MISSING | REQUIRED | REBUILD | Brand colours are literals repeated across the 77 inline styles and the 2,916 B `<style>` block (all sources: `#0d0c0a` x14, `#d8c08a` x10, `#f3efe6` x9, `#bdb6a8` x3; inline-only the repeats are `background:#0d0c0a` x6, `background:#f3efe6` x6, `color:#d8c08a` x5); fonts are hardcoded in the `<style>` and in a body-level Google Fonts link (line 12); the logo is a hardcoded `<img src>` (lines 69, 155); and no social URLs exist at all — both social links are `href="#"` (BUSINESS INFORMATION REQUIRED). All of it must become settings (SHOP-03). | css-html-stats.txt colours, sizes and links |
| 14 | `locales/en.default.json` (+ `.schema.json`) | MISSING | REQUIRED | REBUILD | Every string is inline; store language(s) unknown (SHOP-05). | lines 59-164 |
| 15 | Theme CSS in `assets/` | CURRENT as one 2,916 B `<style>` inside `<helmet>` plus 77 inline styles and 55 `!important` | REQUIRED | REBUILD | Tokens from settings via CSS custom properties; per-section stylesheets loaded with `stylesheet_tag`. See the CSS register. | css-html-stats.txt sizes |
| 16 | Theme JavaScript | CURRENT support.js + React/ReactDOM from unpkg (211 KB raw executed per load) | REQUIRED | REPLACE | No React, no dc runtime; small vanilla modules for menu drawer, cart drawer and predictive search take its place. See the ARCH register. | bundle-sizes.txt; measurements.md |
| 17 | Fonts via `font_picker` + `font_face` or self-hosted assets | CURRENT as a Google Fonts `<link>` inside the body `<helmet>` (line 12) | REQUIRED | REPLACE | Verify Playfair Display, Jost and Kaushan Script against Shopify's font library; any family absent must be self-hosted as woff2 under its licence (SHOP-07). Glyph fallback for ₱ and →: see the BRAND register. | evidence-render.md fonts |
| 18 | Product data (`product.title`, `product.price`, `product.featured_image`, `product.images`, `product.url`, `product.variants`, `product.available`) | CURRENT as three hardcoded objects (lines 174-178); prices are strings with the symbol concatenated | REQUIRED | REPLACE | Real catalogue is BUSINESS INFORMATION REQUIRED; swatches (hex only, lines 175-177) must derive from a colour option or variant metafield; the card needs `product.images` for hover/secondary media as well as `featured_image`. | TECHNICAL-4; spec §9 object list |
| 19 | Collections | MISSING (Shop and Collections both `href="#shop"`, line 72) | REQUIRED | ADD LATER | `collection` picker on the featured-collection section, `templates/collection.json`, `templates/list-collections.json`; handles are BUSINESS INFORMATION REQUIRED. | line 72 |
| 20 | Cart (`cart.item_count`, `routes.cart_url`, cart template/drawer) | MISSING (badge is the literal `0`, line 78; no add-to-cart) | REQUIRED | ADD LATER | See the ECOM register for feature scope. | TECHNICAL-4 |
| 21 | Search (`routes.search_url`, `templates/search.json`) | MISSING (bare `<img alt="Search">`, line 76) | REQUIRED | ADD LATER | Predictive search is OPTIONAL. See the ECOM and NAV registers. | line 76 |
| 22 | Customer accounts (`routes.account_url`, `templates/customers/*`) | MISSING (bare `<img alt="Account">`, line 77) | BUSINESS DECISION REQUIRED | ADD LATER | Classic vs new customer accounts, or none, is a business decision; with new customer accounts the pages are Shopify-hosted and the theme's `customers/*` templates are never rendered. | line 77 |
| 23 | Theme Editor (schema-driven settings, presets, `block.shopify_attributes`) | MISSING; the only editable value is the Claude Design `currency` prop | REQUIRED | REBUILD | Every text, image, colour and menu in §29.7 must be a schema setting (SHOP-02). | line 169; pasted-1789874193900-0.png |
| 24 | Navigation menus (`linklists`) | CURRENT as five hardcoded links, six of nine `href="#"`, active state hardcoded (line 71) | REQUIRED | REPLACE | `link_list` setting on the header. Destinations: see the NAV register. | evidence-render.md links |
| 25 | In-page anchors `id="shop"` / `id="story"` (lines 98, 125) | CURRENT | n/a | REPLACE | Section wrappers receive generated `shopify-section-*` ids; the destinations become collection and page URLs. See the NAV register. | lines 98, 125 |
| 26 | Currency and markets | CURRENT as a symbol enum ₱/$/€ that swaps the sign only | BUSINESS DECISION REQUIRED | REPLACE | Store currency, money format and Shopify Markets own this; the theme only renders `money` (SHOP-08). | line 169; TECHNICAL-4 |
| 27 | Metafields | MISSING | OPTIONAL | ADD LATER | Verse text, size guide, swatch hex values are candidates. | none |
| 28 | Templates beyond the homepage (product, collection, cart, search, page, 404, customers, password, gift card) | MISSING; no design exists for any of them | REQUIRED | ADD LATER | The prototype covers the homepage only; every other route must be designed (SHOP-09). | desktop-1440.png |

### 24.3 The Liquid delimiter collision, spelled out

The New Drop grid and the values strip are driven by `<sc-for list="{{ products }}" as="p">` (line 107), `<sc-if value="{{ p.img }}" hint-placeholder-val="{{ false }}">` (line 110), `{{ p.name }}` (line 112), `{{ p.price }}` (line 113), `background:{{ s }}` (line 116), and `{{ v.icon }}`, `{{ v.title }}`, `{{ v.sub }}` (lines 145-147). support.js resolves each placeholder by splitting the text on `\{\{ ... \}\}` (support.js 407-409) against the object returned by `renderVals()` (lines 170-187). Liquid uses the same delimiters, so a verbatim paste into a section would not error: Liquid would evaluate every placeholder as an undefined variable and print nothing, `{{ false }}` would print the word false into an attribute, and `<sc-for>`, `<sc-if>`, `<x-dc>` and `<helmet>` would remain in the DOM as unknown elements (findings-verified.json TECHNICAL-3). The two 404 requests for `/%7B%7B%20p.img%20%7D%7D` and `/%7B%7B%20v.icon%20%7D%7D` on every load (findings-verified.json C3) are the same collision seen by the browser's own HTML parser, and they disappear as soon as nothing on the page carries dc syntax. The mechanism is owned by the ARCH register; the compatibility consequence is that the grid and the values strip must be re-authored, not transposed.

### 24.4 What is not reusable, and what is

Nothing in the prototype is reusable as code: not the HTML (dc wrappers, dc control flow, 77 inline styles, 0 class attributes: css-html-stats.txt), not the CSS (55 `!important` declarations across 34 `[data-r=…]` selectors inside the 2,916 B `<style>`, with none inline: css-html-stats.txt), not support.js (a generated editor/streaming runtime that fetches `location.href` a second time, support.js 159, and posts `__dc_booted` / `__dc_design_mode` to `window.parent` with origin `*`, support.js 1387, 1858-1860: findings-verified.json TECHNICAL-7), and not the data class. Copying any of it into `sections/` would produce a blank or broken page.

What is reusable, and must be carried forward deliberately:

- The visual system: palette `#0d0c0a`, `#f3efe6`, `#d8c08a` with secondaries `#bdb6a8`, `#ebe6dc`, `#e9e4d8` and the swatch green `#4b5443` (css-html-stats.txt; line 175); type roles Playfair Display 900 for display, Jost 400/500/600 for UI and body, Kaushan Script 400 for the script accent (evidence-render.md fonts); the tracking scale `.2em`-`.3em`; the h1 clamp `clamp(56px,8.5vw,112px)` (line 84). Token ownership: see the BRAND register.
- The copy: every string on lines 59-164 and the product and value labels on lines 174-183, as default values for section settings and blocks.
- The layout intent: section order announcement, header, hero, New Drop, Our Story, values, footer, which matches the approved mockup (evidence-render.md mockup vs render); the hero grid `1.1fr 1.1fr .7fr` (line 64), the New Drop split `.9fr 2.4fr` (line 98), the story split `.9fr 1.6fr .4fr` (line 125), the four-column values strip (line 142), the 1440 px page width (line 55), and the two gradient fades (lines 66, 127) as the technique, not the numbers.
- The mockup `uploads/God-Squad-Images/00-full-mockup-reference.webp` (1024x1536) as the design baseline, subject to the approved deviations recorded in evidence-render.md (group hero photo, gold globe, two-icon social set).
- The product concepts (Signature Oversized Tee ₱1,290, Heavyweight Hoodie ₱2,490, Utility Cap ₱890) as placeholders only; real titles, prices and variants are BUSINESS INFORMATION REQUIRED.
- The idea behind the `currency` prop (₱/$/€) as a requirement for Shopify Markets, which is BUSINESS DECISION REQUIRED.

### 24.5 Theme Editor and configuration readiness

The Theme Editor edits `settings_schema.json` values and section/block settings declared in `{% schema %}`; the prototype declares neither, so today the merchant could change nothing in Shopify (SHOP-02). Colours would have to be settings because they are repeated as literals (SHOP-03); fonts would have to come from `font_picker` settings or self-hosted assets rather than the body-level Google Fonts `<link>` (SHOP-07); the announcement bar and header must be extractable into the header group, which the hero-welded `<nav>` prevents (SHOP-04); strings need `locales/` (SHOP-05); assets need flat, URL-safe names, and the non-theme files — mockup PNG, editor screenshots, sprites, the editor-generated `.thumbnail` preview, and `.claude/launch.json`, which is dev-server tooling added by the audit lead and not a site file — must stay out of the theme (SHOP-06); the currency symbol must come from the store, not a prop (SHOP-08); and every non-homepage route needs a template that has never been designed (SHOP-09). §29 sets out the target structure that satisfies each of these.

## 25. Missing Ecommerce Features

### Baseline

The prototype is a single static composition: one HTML file (inventory.tsv), zero `<form>`, zero `<button>`, zero `<input>`, nine links of which six are `href="#"` (css-html-stats.txt), a hard-coded cart badge "0" (God Squad Website.html line 78), three hard-coded products with a symbol-only currency prop (lines 169-178), and utility icons that are bare images (lines 76-78). No ecommerce feature in the spec's list is CURRENT. The classification below states, per feature, the status (CURRENT / MISSING), the need (REQUIRED / OPTIONAL / BUSINESS DECISION REQUIRED) and the Shopify-native mechanism that will provide it; nothing here is implemented in Phase 1. The launch catalogue size (product and SKU count) has not been seen anywhere in the project and is BUSINESS INFORMATION REQUIRED; several OPTIONAL rows below depend on it.

### Classification

| Feature | Status | Need | Shopify note | Business input |
|---|---|---|---|---|
| Product page | MISSING | REQUIRED | `templates/product.json` → `sections/main-product.liquid`: media gallery from `product.media`, `product.description`, variant picker, `{% form 'product', product %}` (ECOM-01) | product descriptions, images, size guide: BUSINESS INFORMATION REQUIRED |
| Collection page | MISSING | REQUIRED | `templates/collection.json` → grid over `collection.products` with `paginate` (§13, COLL-01) | taxonomy: BUSINESS INFORMATION REQUIRED |
| Search | MISSING (icon is an inert `<img>`, line 76) | REQUIRED | `templates/search.json`; `<form action="{{ routes.search_url }}" role="search">` with `name="q"`; predictive search via `routes.predictive_search_url` and the Section Rendering API (ECOM-03) | — |
| Cart | MISSING (badge is literal "0") | REQUIRED | `templates/cart.json`; `{% form 'cart', cart %}`; `cart.items`, `cart.item_count`, `cart.total_price`; `routes.cart_url` (ECOM-02) | — |
| Cart drawer | MISSING | OPTIONAL — BUSINESS DECISION REQUIRED (drawer vs page; catalogue size at launch is BUSINESS INFORMATION REQUIRED) | Cart Ajax API (`/cart/add.js`, `/cart/change.js`, `/cart.js`) re-rendering a `cart-drawer` section via `?sections=` (ECOM-02) | drawer vs page |
| Add to cart | MISSING (no form or button on the page) | REQUIRED | `{% form 'product' %}` with `<input name="id" value="{{ variant.id }}">` and `<button type="submit" name="add">`; `routes.cart_add_url` (PROD-02, ECOM-02) | — |
| Quantity controls | MISSING | REQUIRED | `<input type="number" name="quantity" min="1">` respecting `variant.quantity_rule`; cart line `updates[]` (ECOM-02) | — |
| Variants | MISSING (swatches are inert spans, lines 114-118; no sizes anywhere) | REQUIRED | `product.options_with_values`, `product.variants`, `product.selected_or_first_available_variant`, `?variant=` URL state (ECOM-04, PROD-03) | size run and colour names: BUSINESS INFORMATION REQUIRED |
| Availability | MISSING | REQUIRED | `product.available`, `variant.available`, `variant.inventory_quantity` / `inventory_policy` for backorder; "Sold out" badges and disabled add (ECOM-04) | inventory policy: BUSINESS DECISION REQUIRED |
| Checkout pathway | MISSING | REQUIRED | cart form `<button type="submit" name="checkout">` to Shopify Checkout; optional `{{ form \| payment_button }}` for accelerated checkout on the product form (ECOM-02) | payment gateways: BUSINESS INFORMATION REQUIRED |
| Customer account | MISSING (icon inert, line 77) | BUSINESS DECISION REQUIRED | `routes.account_url` / `routes.account_login_url`; account templates only if accounts are enabled; classic vs new customer accounts is an admin setting (ECOM-05) | enable accounts? which type? |
| Wishlist | MISSING | OPTIONAL / BUSINESS DECISION REQUIRED | not native; app or theme-level implementation; no apps are to be installed in Phase 1 (ECOM-08) | wanted at launch? |
| Filters | MISSING | OPTIONAL / BUSINESS DECISION REQUIRED | `collection.filters` configured in Shopify's Search & Discovery app (app decision) (ECOM-06) | catalogue size at launch: BUSINESS INFORMATION REQUIRED |
| Sorting | MISSING | REQUIRED (low effort) | `collection.sort_options`, `?sort_by=` (ECOM-06) | default sort |
| Product recommendations | MISSING | OPTIONAL | `routes.product_recommendations_url?product_id=…&intent=related` rendered through a section (ECOM-07) | — |
| Related products | MISSING | OPTIONAL | same API with `intent=complementary` (needs Search & Discovery configuration) or a manual `product_list` setting (ECOM-07) | curated pairings, if any |

### Supporting features not in the spec's list but implied by the prototype

| Feature | Status | Need | Shopify note |
|---|---|---|---|
| Cart count badge | MISSING (literal "0") | REQUIRED | `cart.item_count` (NAV-09) |
| Currency / markets | MISSING (₱/$/€ symbol toggle only, line 169) | BUSINESS DECISION REQUIRED | store currency, Shopify Markets, `money` filters, optional `localization` form (ECOM-09) |
| Shipping / returns / size guide content | MISSING ("Worldwide Shipping" claim only, line 60) | REQUIRED | policy pages in admin, linked from footer and product page (FOOT-01, UX-05) |
| Newsletter capture | MISSING | BUSINESS DECISION REQUIRED | `{% form 'customer' %}` (FOOT-03) |
| Product URLs / structured data | MISSING | REQUIRED | `product.url`; see the SEO register |

### Order of dependency for Phases 6-8 and 15

1. Product data, variants and collections must exist in admin before any template can be verified (BUSINESS INFORMATION REQUIRED throughout).
2. Product page + add to cart + cart + checkout form the minimum sellable path (ECOM-01, ECOM-02, ECOM-04) — Phase 8.
3. Collection page + sorting (COLL-01, ECOM-06) — Phase 6; filters only when the catalogue justifies the app.
4. Search (ECOM-03) and account (ECOM-05) with the header rebuild — Phases 4 and 8.
5. Recommendations, related products, wishlist, cart drawer — after the sellable path is verified in Phase 15 — ECOMMERCE QA.

No functionality has been invented: every mechanism above is a standard Online Store 2.0 object, route, form or template, and every content-dependent item is flagged as business input.

## 26. Technical Debt

This register consolidates the debt found across the runtime, CSS, markup, assets and data into one ledger, so that each item has a cost of carrying it and a phase that retires it. Every ledger entry is owned by exactly one issue register, and that register holds the finding's severity, priority and categories; the DEBT-nn code is the ledger row, not a second issue. Only two ledger rows — DEBT-12 (process debt) and DEBT-13 (baseline drift) — are owned by this register and appear in its issue list, because no other register covers them. Rows DEBT-01 to DEBT-11 are cross-references and must not be counted a second time in any priority matrix or terminal total.

Definitions used: cost-to-carry is what it costs to keep the debt alive while the theme is built — the rework it forces, the defects it regenerates, the phases it blocks — rated HIGH (blocks or re-breaks later phases), MEDIUM (forces rework inside one phase), LOW (contained or cosmetic). Effort-to-retire is an engineering planning estimate, not a quote: S under half a day, M half a day to two days, L two to five days. Business inputs that gate an item are marked BUSINESS INFORMATION REQUIRED.

### 26.1 Debt register

| ID | Debt | Evidence | Cost-to-carry | Effort (est.) | Retired in | Notes / prerequisite | Owned by |
|---|---|---|---|---|---|---|---|
| DEBT-01 | Claude Design runtime and its template dialect: support.js (69,150 B) plus React/ReactDOM (142,586 B) from unpkg; template hidden until React mounts, blank page if the CDN fails; HTML fetched twice; `new Function` eval; `{{ }}` / `sc-for` / `sc-if` / `x-dc` / `helmet` / `data-dc-script` | evidence-render.md; support.js lines 1818-1910; bundle-sizes.txt; findings-verified.json C13, TECHNICAL-3, TECHNICAL-7 | HIGH — nothing in the JS layer is reusable, the `{{ }}` dialect silently blanks tiles if pasted into Liquid, every preview needs network | M — discard, then re-express three loops and two conditions as Liquid | PHASE 10 — SHOPIFY THEME CONVERSION | — | ARCH/JS register (its P0 SHOPIFY-BLOCKER; counted there only) |
| DEBT-02 | CSS architecture: 77 inline `style` attributes (6,421 chars, 69% of CSS), 0 classes, 36 rules of which 32 are keyed on `data-r` (34 selector uses), 55 `!important`, 18 colour literals (21 whole-file), no tokens | css-html-stats.txt; §5 | HIGH — no Theme Editor colour or type control is possible; every responsive fix demands another `!important` | L — tokens, base stylesheet and seven section stylesheets replacing ≈9.3 KB | PHASE 10 — SHOPIFY THEME CONVERSION | tokens defined in PHASE 2 — DESIGN SYSTEM | CSS-01, CSS-02, CSS-03 (this cluster) |
| DEBT-03 | Header welded to the hero: nav absolutely positioned inside the hero section, hero copy padded 170/190px to clear it, announcement bar a sibling div | God Squad Website.html lines 58-95; findings-verified.json TECHNICAL-11; §4 | HIGH — generates the 88px hero-fade offset under 900px and the nav-over-sky contrast failures, and blocks the header section group | M | PHASE 4 — HEADER & NAVIGATION | — | HTML-01 (this cluster); outcomes in the RESP register (fade) and A11Y register (contrast) |
| DEBT-04 | Hard-coded content and commerce data: three products with string-concatenated currency symbol, swatch hexes, four values, nav labels, cart badge `0`, active Home state, all copy inline | God Squad Website.html lines 71, 78, 169-188; findings-verified.json TECHNICAL-4 | HIGH — nothing is editable, prices cannot convert, no product URLs | M for schema design; data entry is business work | PHASE 10 — SHOPIFY THEME CONVERSION | settings exposed in PHASE 11 — THEME EDITOR | DATA register |
| DEBT-05 | Asset hygiene: 44 files / 17,185,754 B for a page that references 17 files / 2,491,648 B; 9 md5 duplicate groups (11 redundant copies); two unreferenced 2172x724 AI sprites (1.76 MB); 1.87 MB mockup PNG; 3.86 MB editor screenshots; 1.99 MB RGB PNG hero; 215-235px product crops; `WHITE FONT LOGO.png` with spaces | inventory.tsv; measurements.md inventory summary; findings-verified.json C2, C10, TECHNICAL-10 | HIGH — copying the folder into `assets/` ships 17 MB; without masters Phases 5-7 cannot produce sharp imagery | M for hygiene | PHASE 3 — ASSET PREPARATION | masters are BUSINESS INFORMATION REQUIRED | ASSET/PERF register |
| DEBT-06 | Raster icon system: nine RGBA PNGs (308,521 B) drawn at 16-44px with colour baked in; no hover or theme colouring possible | findings-verified.json TECHNICAL-6; inventory.tsv | MEDIUM — blocks icon hover/focus states and Theme Editor colour | S-M — SVG snippets with `currentColor` | PHASE 3 — ASSET PREPARATION | — | ASSET/PERF register |
| DEBT-07 | Our Story image: a 650x480 crop of the mockup hero with headline fragments baked into the pixels, upscaled 1.53x (≈3x on 2x screens); the intended three-model crop (images/our-story.webp, 535x348) is unused and also too small | findings-verified.json C1 and the story-slot critic addition; desktop-1440.png; tablet-768.png | HIGH — the most visible brand defect on every width | S to swap | PHASE 7 — OUR STORY | source photography ≥2000px is BUSINESS INFORMATION REQUIRED | STORY register |
| DEBT-08 | Head and metadata: no `<title>`, `lang`, description, canonical, Open Graph, favicon, robots or JSON-LD; stylesheet and font link inside the body; preconnect incomplete; unused Playfair 700 | css-html-stats.txt; findings-verified.json C7, TECHNICAL-9 and the metadata critic addition; §4 | MEDIUM — the port inherits no chosen title, description or OG image | S | PHASE 13 — SEO | title, description and OG image copy are BUSINESS INFORMATION REQUIRED | SEO register; `lang` and body-hosted head content are HTML-02, HTML-09 (this cluster) |
| DEBT-09 | Accessibility: zero buttons; hamburger, search, account and cart unreachable by keyboard; no skip link; no focus styles; three of five nav links at 2.4-2.8:1 over the hero sky at 1440 (2.4-2.9:1 at 1024); nine unnamed swatches; arrow glyphs announced | evidence-render.md; findings-verified.json C5, C6, C15, TECHNICAL-5 and the contrast critic addition; §4 | HIGH — every header and product control must be re-authored, not wrapped | M | PHASE 14 — ACCESSIBILITY | controls authored during PHASE 4 — HEADER & NAVIGATION through PHASE 8 — PRODUCT & SHOPPING UX; colour names for swatches are BUSINESS INFORMATION REQUIRED | A11Y register; markup semantics are HTML-03, HTML-04 (this cluster) |
| DEBT-10 | Responsive layer: two `max-width` queries (900/520), desktop-first; hero-fade 88px offset; dead `[data-r=pad]` gutter rule; orphaned side captions; 2.8x product upscale at 375; 5.4-screen phone page; footer stacked at 768 | measurements.md; findings-verified.json RESPONSIVE-1, -3, -4, -6, -9, -10; §5 | HIGH — the phone experience is where a streetwear store sells | M | PHASE 9 — MOBILE UX | breakpoints defined in PHASE 2 — DESIGN SYSTEM | RESP register (outcomes); CSS-04, CSS-05 (mechanics, this cluster) |
| DEBT-11 | Glyph fallback: U+20B1 (₱) in every price and U+2192 (→) in both CTAs are not in Jost and render in a per-OS system face | evidence-render.md fonts; findings-verified.json glyph critic addition | MEDIUM — every price looks different per device | S | PHASE 2 — DESIGN SYSTEM | — | BRAND register |
| DEBT-12 | Process debt: not a git repository, no package.json or build tooling, project lives inside a personal OneDrive folder, the spec still names "God Squad Website.dc.html", four unreferenced root-level exports (`chatgpt-image-…png`, `white-font-300x300-…png`, two `white-font-trans-…png`); the referenced story WebP also sits in the root outside images/ (ASSET/PERF register) | evidence-render.md lines 6-14; inventory.tsv | MEDIUM — no history to diff the prototype against; sync conflicts and accidental edits are unrecoverable | S | PHASE 10 — SHOPIFY THEME CONVERSION | a baseline repository can be created before PHASE 2 — DESIGN SYSTEM; store and Git host availability are BUSINESS INFORMATION REQUIRED | DEBT-12 (this register) |
| DEBT-13 | Baseline drift: the prototype is still editable in Claude Design and has already diverged from the mockup by deliberate edits (group hero photo, gold globe, two social boxes removed); each further edit adds inline styles and invalidates this audit's measurements | evidence-render.md editor history; uploads/pasted-1789874193900-0.png, pasted-1789874322321-0.png, pasted-1789874476205-0.png; inventory.tsv (html md5 787068e3…) | MEDIUM — the audit's numbers are only valid for this file's md5 | S — freeze the file, record its hash, log open design decisions | PHASE 2 — DESIGN SYSTEM | confirmation of the three departures from the mockup is BUSINESS DECISION REQUIRED | DEBT-13 (this register) |

### 26.2 Retirement order by phase

| Phase | Retires | Prerequisite business input |
|---|---|---|
| PHASE 2 — DESIGN SYSTEM | DEBT-11, DEBT-13; defines the tokens that DEBT-02 needs and the breakpoints that DEBT-10 needs | confirmation of the extended palette and mobile type scale; support matrix |
| PHASE 3 — ASSET PREPARATION | DEBT-05, DEBT-06 | original photography or masters for hero, story and products |
| PHASE 4 — HEADER & NAVIGATION | DEBT-03 | link destinations (NAV register) |
| PHASE 7 — OUR STORY | DEBT-07 | story photograph ≥2000px |
| PHASE 9 — MOBILE UX | DEBT-10 | — |
| PHASE 10 — SHOPIFY THEME CONVERSION | DEBT-01, DEBT-02, DEBT-04, DEBT-12 | Shopify store / dev store and Git host |
| PHASE 13 — SEO | DEBT-08 | title, description, OG image copy (SEO register) |
| PHASE 14 — ACCESSIBILITY | DEBT-09 | colour names for swatches |

### 26.3 Debt that should be carried deliberately

The prototype itself — runtime, inline CSS, `{{ }}` templates — must not be refactored. The spec forbids it (spec §27) and the executive conclusion names the file as the preserved design baseline (spec §29). Carrying it costs nothing provided two conditions hold: it is frozen (DEBT-13) and nobody copies markup or CSS from it verbatim into the theme (DEBT-01, DEBT-02). The two 404s for `/{{ p.img }}` and `/{{ v.icon }}` on every load (findings-verified.json C3) and the double HTML fetch are runtime artefacts of the same kind: document, do not fix.

### 26.4 What is not debt

The following are assets to carry forward, not liabilities: the three-colour palette and the three type families (spec §5; desktop-1440.png); the section order and copy; the modern CSS idioms (`clamp`, `aspect-ratio`, grid `minmax`, `object-fit`, gradient fade recipes) whose values seed the token set; the six HTML comments and `data-screen-label` values that give the port its section map (God Squad Website.html lines 57, 63, 97, 124, 141, 152); the `renderVals()` shape (`products[]` with name / price / img / swatches, `values[]` with title / sub / icon, lines 170-187) as the seed for the featured-collection and brand-values section schemas; and the three product WebPs as placeholders until masters arrive. The audited state is reproducible from the file hash recorded in inventory.tsv, which is the reference point every later phase should cite.

## 27. Risk Assessment

### 27.1 Method

Each risk is rated on likelihood (HIGH / MEDIUM / LOW) and impact on the conversion programme (HIGH / MEDIUM / LOW), tied to a trigger that is visible in the evidence today, given a mitigation phrased as future work, and assigned one owning phase. The owning phase is the phase in which the risk is actually decided, not the phase in which it is later observed. Risks are registered as RISK-01 to RISK-14 so the priority matrix can track them beside defects; where the underlying defect belongs to another cluster, the register entry points to it. ADD-1 to ADD-8 below are the eight `critic_additions` entries of findings-verified.json, numbered in file order as defined in §24.2; the file gives them no ids of their own.

### 27.2 Risk register

| ID | Risk | Likelihood | Impact | Trigger visible today | Mitigation | Owning phase |
|---|---|---|---|---|---|---|
| RISK-01 | Asset resolution gap: no asset in the project is fit for its slot at 2x | HIGH | HIGH | Product images are 215-235 px mockup crops upscaled 2.8x on a 2x phone (findings-verified.json C2; measurements.md 375 row); story image 650x480 in a ~1000 px slot needing ~2,000 px (ADD-4); hero is a 1,989,201 B RGB PNG with no alpha (C10, ADD-5); logo is a 500x500 padded PNG rendering at 66x50 (FIDELITY-4); no vector logo seen, only PSDs outside the project (evidence-render.md) | Phase 3 acquires original photography and a vector wordmark before any section is built; the mockup crops are ARCHIVE-class references only. Resolution and weight defects: see the ASSET register. | PHASE 3 — ASSET PREPARATION |
| RISK-02 | Missing business information stalls content-complete templates | HIGH | HIGH | Six of nine links are `href="#"` (evidence-render.md links); no policies, contact, copyright, social URLs, catalogue, sizes, markets or verse content exist anywhere in the project (ADD-7; TECHNICAL-4) | Run the intake checklist at the end of this report before Phase 4; gate Phase 4 on navigation URLs, Phase 8 on the catalogue, Phase 15 on legal text. Nothing is to be invented. | PHASE 2 — DESIGN SYSTEM |
| RISK-03 | Brand fidelity drift: two baselines disagree and the rebuild could inherit either | MEDIUM | HIGH | The build already departs from the mockup in hero photo, headline lockup, wordmark size, product tiles, social icons and globe colour (findings-verified.json C18 refuted as overstated; FIDELITY-1 to FIDELITY-10) | Phase 2 records a signed decision per deviation (mockup wins / build wins) and freezes the design baseline; the rebuild targets the frozen baseline, never the live prototype. | PHASE 2 — DESIGN SYSTEM |
| RISK-04 | Runtime dependency confusion: someone reuses support.js or pastes dc markup into Liquid | MEDIUM | HIGH | `{{ }}` collision renders silent empty tiles (TECHNICAL-3); the page boots from `file://` but stays blank if React cannot be fetched from unpkg (C13, ADD-2; support.js 1818-1822, 1906-1910); the runtime is labelled generated, do not edit (support.js line 1) | Phase 10 starts from an empty theme scaffold; the prototype is read-only reference; a written rule that no file from the project folder is copied into the theme. Runtime removal: see the ARCH register. | PHASE 10 — SHOPIFY THEME CONVERSION |
| RISK-05 | Mobile layout regression during the rebuild | HIGH | HIGH | The mobile layer is 31 rules across two queries (26 in `@media (max-width:900px)`, 5 in `@media (max-width:520px)`) that override the desktop rules with `!important` (55 in the `<style>`, none inline: css-html-stats.txt), plus a live hero-fade defect (RESPONSIVE-1 / TECHNICAL-1: 88 px offset at 375, 390, 430, 768, 900 and 720: measurements.md); the two-line hero lockup appears only below roughly 540 px — the h1 is 56 px on two lines at 375 (327x99), 390 (342x99) and 430 (382x99), one line at 768 and 900, and three lines from 901 up (measurements.md; FIDELITY-2 as refined in findings-verified.json gaps); no genuine device captures exist (findings-verified.json gaps) | Phase 9 defines acceptance renders per width (375, 390, 430, 768, 900, 1024, 1440, 1920) from the mobile-*-true.png series and rebuilds mobile-first. Layout outcomes: see the RESP register. | PHASE 9 — MOBILE UX |
| RISK-06 | Scope creep: the 'conversion' is a full theme build | HIGH | HIGH | The commerce surface is inert: zero `<a>` in the product grid, no cart, search, account, product or collection page (TECHNICAL-4; SHOP-09); only the homepage exists (desktop-1440.png) | Phase 8 fixes the launch feature set with CURRENT / MISSING / REQUIRED / OPTIONAL classification from the ECOM register and budgets every template in §29.5 explicitly. | PHASE 8 — PRODUCT & SHOPPING UX |
| RISK-07 | OneDrive working copy with no version control | MEDIUM | HIGH | Project lives in the user's personal OneDrive, is not a git repository, has no package.json (evidence-render.md); the owner renamed the page in place on 2026-09-20; a sibling 'Original-Assets' folder has already disappeared from its recorded path; the export zip sits in Downloads | Before Phase 2 work: initialise git for the theme in a non-synced folder, archive the prototype folder and zip as a read-only baseline, and develop with Shopify CLI against a development theme. | PHASE 2 — DESIGN SYSTEM |
| RISK-08 | Font availability and licensing on Shopify | MEDIUM | MEDIUM | Three families are pulled from Google Fonts (line 12); presence in Shopify's font library is unverified; Playfair Display 700 is requested but unused (C12); no licence file is in the project | Phase 2 checks each family in the `font_picker` library; any absent family is self-hosted as subset woff2 in `assets/` after confirming its licence permits it. | PHASE 2 — DESIGN SYSTEM |
| RISK-09 | Peso and arrow glyphs render differently per device once prices come from `money` | HIGH | MEDIUM | `₱` (U+20B1) and `→` (U+2192) are absent from Jost's loaded faces and fall back to a per-OS system face (ADD-3); the store money format has not been chosen | Phase 2 picks the price typeface or a symbol subset and replaces the text arrow with an SVG; Phase 15 checks price rendering on Windows, macOS, iOS and Android. Glyph fallback: see the BRAND register. | PHASE 2 — DESIGN SYSTEM |
| RISK-10 | Performance budget missed by carrying prototype assets over | HIGH | HIGH | 1.99 MB hero PNG at every width (C10); 308,521 B of PNG icons drawn at 16-44 px (TECHNICAL-6); ~211 KB raw JS executed per load, all effectively render-blocking (measurements.md) | Phase 2 sets the budget (LCP image, above-fold bytes, JS bytes); Phase 3 enforces it at asset acceptance, which is where the budget is actually met or missed; Phase 12 confirms it with Lighthouse on Slow 4G. | PHASE 3 — ASSET PREPARATION |
| RISK-11 | Theme Editor expectations mismatch | MEDIUM | MEDIUM | The owner has been editing by natural-language prompt in Claude Design (pasted-1789874193900-0.png, left panel) where anything can change; Shopify only exposes what schemas declare | Phase 11 agrees the settings surface in §29.6-29.7 with the owner before build, including what stays locked to protect the design. | PHASE 11 — THEME EDITOR |
| RISK-12 | Currency and markets misconfiguration at launch | MEDIUM | HIGH | The prototype's `currency` prop swaps only the symbol, so `$` shows `$1,290` for a ₱1,290 item (TECHNICAL-4; line 172) | Decide the selling currencies (BUSINESS DECISION REQUIRED); if more than ₱, configure Shopify Markets and test converted prices in Phase 15. | PHASE 15 — ECOMMERCE QA |
| RISK-13 | No test baseline for acceptance | HIGH | MEDIUM | No Lighthouse, axe, screen-reader, throttled-load, cross-browser or real-device results exist (findings-verified.json gaps) | Phase 2 defines the QA matrix (devices, browsers, throttling, tools) so Phases 9, 12 and 14 have pass criteria before they run; Phase 15 executes it as ecommerce QA. | PHASE 2 — DESIGN SYSTEM |
| RISK-14 | Accessibility debt carried into the rebuild | MEDIUM | HIGH | Nav links over the hero sky measure 2.4-2.9:1 at 1024 and 1440 for Collections, Our Story and Verse when the fade alpha is composited over sampled photo luminance (ADD-1), and 4.6-5.7:1 median but 2.4-2.5:1 over the brightest 2% when measured from the render's own pixels (evidence-render.md); at 1024 the gold Home link also drops to ~3.5:1, a fourth failing link. WCAG AA requires 4.5:1 at this size. Plus zero buttons, unreachable hamburger and utility icons (C6) and no landmarks (C7) | Phase 4 builds the header on a solid or strengthened band and as real controls; Phase 14 runs axe and a keyboard pass against the RESP and A11Y acceptance renders. Defects: see the A11Y register. | PHASE 14 — ACCESSIBILITY |

### 27.3 The four risks that can sink the programme

RISK-01 (assets). Every image on the page is a derivative of the 1024x1536 mockup or a single AI-generated PNG (uploads/God-Squad-Images/README.txt; inventory.tsv). There is no photograph that survives a 2x display, and the Our Story slot cannot be fixed by swapping to `images/our-story.webp` because that file is 535x348 (ADD-4). If Phase 3 does not deliver originals, Phases 5, 6 and 7 will build pixel-perfect sections around soft images and the premium positioning fails on the first phone. The vector wordmark is the same story: the PSD masters exist only on the Desktop outside the project (evidence-render.md), and the Shopify logo setting needs an SVG or a clean high-resolution PNG.

RISK-02 (business information). The prototype contains no store facts at all. The nav has five labels and no destinations, the footer has no legal line and no link groups (lines 153-166; ADD-7), the catalogue is three placeholders with round prices, and 'Worldwide Shipping' is a claim with no shipping policy behind it (line 60). Each Shopify template in §29.5 needs real data before it can be signed off, and the temptation during a rebuild is to fill gaps with plausible text. The rule from the spec stands: anything not supplied is labelled BUSINESS INFORMATION REQUIRED and shipped empty or hidden, never invented.

RISK-04 (runtime confusion). The prototype looks like a website and boots from a double-click — `file://` is fine on its own — which invites reuse. Two facts make reuse dangerous rather than merely wasteful: its template syntax is Liquid's own, so a paste fails silently (TECHNICAL-3), and its first paint depends on fetching React from unpkg.com, so an offline demo or an ad-blocker produces a black page with one console error (ADD-2). The mitigation is procedural: the theme starts from an empty scaffold, the prototype folder becomes a read-only archive, and the design tokens and copy are transcribed, not copied.

RISK-06 (scope). The spec calls this a conversion, but the audit shows a homepage prototype with no commerce, so the honest scope is a complete Online Store 2.0 theme with one designed page and at least nine undesigned storefront templates — product, collection, list-collections, cart, search, page, page.our-story, 404 and password — rising to about twenty once the seven customer templates, the gift card, blog and article are counted (§29.5). If that is not priced and sequenced in Phase 8, the product, collection, cart and search experiences will be built last and worst.

### 27.4 Risk interactions and sequencing

- RISK-01 x RISK-03: new photography changes composition. Phase 2 must fix the hero rules (nav band, headline lockup, mobile crop) before Phase 3 briefs the shoot, or Phase 5 will crop twice.
- RISK-07 x RISK-04: while the prototype stays editable in Claude Design and syncs through OneDrive, the baseline keeps moving. Archive first, then convert.
- RISK-02 x RISK-06: templates beyond the homepage cannot be designed until the catalogue, collections and policies arrive; the intake checklist is therefore on the critical path for Phases 6 and 8, not an administrative afterthought.
- RISK-10 x RISK-01: the performance budget is met or missed at asset acceptance in Phase 3; Phase 2 sets the numbers and Phase 12 can only confirm them. That is why RISK-10 is owned by Phase 3.
- RISK-05 x RISK-13: without device captures and pass criteria, mobile regressions will be argued from screenshots. The QA matrix must therefore be written in Phase 2, ahead of the phases it judges, and executed in Phase 15. The mobile-375-true.png, mobile-390-true.png and mobile-430-true.png series (shotsFolder) are the reference set; mobile-375.png and mobile-375-raw.png are clipped ~490 px captures and must not be used (measurements.md).

## 28. Priority Matrix

This matrix is the complete work list produced by the audit: 200 issues, each owned by exactly one register, each traceable to a file, a measurement or a named screenshot. It is sorted by priority, then severity, then ID.

**How to read it.** *Priority* answers "when": **P0 — BLOCKER** is reserved for the three findings that prevent the production architecture from working at all; **P1 — HIGH PRIORITY** covers major UX, accessibility, ecommerce and architectural problems; **P2 — MEDIUM PRIORITY** covers important improvements; **P3 — POLISH** covers visual refinement and optional enhancements. *Severity* answers "how bad is the defect in itself", and the two deliberately differ: a CRITICAL defect in a section that does not ship until Phase 8 sits at P1, not P0. *Phase* names the single phase that retires the issue, and the dependency map in §30 groups the same issues that way. The recommendation column is written as future work; nothing in this matrix has been actioned.

**Counts.** P0 — BLOCKER: 3 issues. P1 — HIGH PRIORITY: 65 issues. P2 — MEDIUM PRIORITY: 80 issues. P3 — POLISH: 52 issues. By severity: 5 CRITICAL, 49 HIGH, 85 MEDIUM, 61 LOW. By category: 93 UX, 28 mobile, 27 accessibility, 22 SEO, 20 performance.

### 28.1 Consolidation map

Issues were kept separate where they have different causes, owners or fix locations, so several rows describe facets of one piece of work. The clusters below are listed so that planning treats them as single jobs rather than as a dozen tickets. No issue was deleted; every ID in the matrix is cited by the section that raised it.

| Cluster | Issue IDs | Single job |
|---|---|---|
| Header controls are not controls | A11Y-01, HTML-04, NAV-02, NAV-07, NAV-09, A11Y-07, UI-03, JS-08 | Build a real header component with buttons, links, labels, focus and hover states |
| No navigation below 900 px | NAV-01, RESP-12, A11Y-10 | Build the mobile menu panel and its trigger |
| Navigation over the hero fails contrast | A11Y-03, HERO-02, HERO-06 | Decide the header backing treatment and re-measure |
| Placeholder destinations | NAV-03, NAV-04, NAV-05, NAV-06, DATA-05, DATA-08, FOOT-02, SEO-09, UX-07 | Resolve every destination once the menus and pages exist |
| No design tokens | CSS-01, CSS-08, CSS-09, BRAND-01, BRAND-02, BRAND-04, BRAND-06, UI-05 | Define the token set in Phase 2 |
| Inline-style architecture | CSS-02, CSS-03, CSS-05, CSS-06, CSS-11, HTML-05, HTML-08 | Replace with a class-based, tokenised stylesheet during conversion |
| Hardcoded content and data | DATA-01 to DATA-09, VAL-01, STORY-06, PROD-03 | Re-express as Shopify objects, section settings and blocks |
| Product imagery is unfit | ASSET-03, ASSET-04, ASSET-05, PROD-05, UI-02, STORY-02 | Source original photography at production resolution |
| Raster icon system | ICON-01 to ICON-05, ASSET-02, ASSET-06, BRAND-07 | Build one inline-SVG icon snippet set |
| Redundant and stray files | ASSET-01, ASSET-07, ASSET-08, INV-03, INV-04, SHOP-06 | One asset clean-up and naming pass in Phase 3 |
| Head metadata missing | SEO-01 to SEO-08 | One head snippet plus theme settings |
| Image delivery | HTML-06, PERF-01, PERF-02, PERF-05 | Responsive image pipeline with Shopify's image filters |
| Hero fade and crop on small screens | RESP-01, RESP-09, RESP-10, HERO-08 | Re-cut the hero for phones with an anchored scrim |

| ID | AREA | PROBLEM | IMPACT | RECOMMENDATION | SEVERITY | PRIORITY | PHASE |
|---|---|---|---|---|---|---|---|
| ARCH-01 | Rendering architecture | The page is a Claude Design dc document: every visible node sits inside `<x-dc>` and is compiled by support.js into React elements at runtime (sc-for/sc-if/helmet custom elements, {{ }} interpolation, style-hover, a DCLogic class evaluated with new Function), so there is no static HTML page at all. | Shopify Online Store 2.0 renders Liquid sections server-side under Theme Editor schema; a client-side React template compiler cannot be hosted by that model, so nothing in the current render pipeline can be carried over. | Treat the prototype as a visual baseline only and rebuild the markup as Liquid sections in Phase 10, starting from the rendered DOM rather than the template source. | CRITICAL | P0 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ARCH-02 | Template syntax | The template uses {{ products }}, {{ p.name }}, {{ p.price }}, background:{{ s }}, {{ v.icon }} and similar expressions, the same delimiters as Liquid output tags, and the data they reference exists only in the data-dc-script. | Pasted into a .liquid file the expressions evaluate as undefined and silently output empty product and value tiles, while `<sc-for>`, `<sc-if>`, `<x-dc>` and `<helmet>` remain as unknown elements. | In Phase 10 rewrite the loops as {% for product in collection.products %} and section blocks with schema; never copy the sc-* template verbatim into a section. | CRITICAL | P0 | PHASE 10 — SHOPIFY THEME CONVERSION |
| SHOP-01 | Theme structure | No Shopify theme structure exists: the deliverable is a single Claude Design dc document plus a generated runtime, with none of layout/, sections/, snippets/, templates/, assets/, config/ or locales/. | Nothing can be uploaded to a Shopify store or opened in the Theme Editor, so the production architecture does not exist yet in any form. | Phase 10 will scaffold god-squad-theme/ with the seven directories and the layout, groups, sections, snippets and templates listed in §29, starting from an empty scaffold rather than from the prototype files. | CRITICAL | P0 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ECOM-01 | Product page | No product page or product template exists. | There is no way to view details, choose variants or buy any product. | Build templates/product.json with a main-product section (media, description, variant picker, product form) once product data is supplied. | CRITICAL | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| ECOM-02 | Cart and checkout | There is no cart, cart drawer, add-to-cart, quantity control or checkout pathway; the cart icon is an inert image with a literal 0 badge. | No purchase can be completed. | Implement the product form, cart template, quantity controls and checkout button using Shopify's cart forms and Ajax API; decide drawer vs page. | CRITICAL | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| A11Y-01 | Header controls | Search, Account and Cart are bare img elements and the hamburger is a span, so none of them is focusable, operable or exposed as a control, and the page has zero button elements. | Keyboard and screen-reader users cannot reach any header function at any width, and below 900px they have no navigation of any kind. | In Phase 4 build each control as a button or link with a visible focus state and an accessible name (menu, search, account, cart with item count); the functional wiring is the NAV register's item. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| A11Y-03 | Nav contrast over the hero | Collections, Our Story and Verse are 12px white text over the bright sky between the models where the top fade has thinned to about 0.4 alpha, measuring 2.4-2.9:1 composited across 1440 and 1024, and the gold Home link drops to about 3.5:1 at 1024px. | Three of five primary links fail WCAG AA at 1440 and 1024, and legibility varies with whatever photo is uploaded. | In Phase 4 give the header a solid or stronger top band (or move it out of the hero as the header section), so contrast no longer depends on the photo. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| A11Y-11 | Document-level semantics | The html element carries no lang attribute and document.title is empty, so the page declares neither its language nor a name. | Two outright WCAG 2.1 Level A failures (SC 3.1.1 Language of Page, SC 2.4.2 Page Titled) that are live today for every assistive-technology user: screen readers fall back to their default pronunciation rules and the page announces no title on load, in a tab list or in a window switcher. These are the only Level A failures on the page and, unlike the header findings, they do not depend on any control being wired. | In Phase 10 set lang on the html element and a real title in layout/theme.liquid (page_title plus shop name); the title copy and the store's content language are BUSINESS INFORMATION REQUIRED, and the SEO register owns the same head work (title, meta description, canonical, Open Graph) so the two should be specified together. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ARCH-03 | Runtime availability | support.js hides `<x-dc>` synchronously with x-dc{display:none!important} and reveals content only after React 18.3.1 and ReactDOM are fetched from unpkg.com; the failure path only logs and rethrows with no fallback. | Any blocked CDN (ad-blocker, corporate proxy, captive portal, offline, SRI mismatch) leaves the entire page black with no message, and with JavaScript disabled the raw template shows literal {{ p.name }} placeholders and a broken image. | Remove the runtime dependency entirely in Phase 10; do not self-host React as a workaround, because the theme needs no React at all. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ASSET-03 | Assets / product imagery | The three product images are 215-235 px WebP crops of the 1024x1536 mockup, upscaled 1.23-1.34x at 1440 and 2.8x in device pixels on phones, with the cap non-square. | The only commercial imagery on the store looks soft on every screen and cannot support a product page, zoom or additional views. | Phase 3 will source original product photography (2000 px or more on the long edge, consistent square framing, one set per colour) and upload it as product media; the crops remain placeholders until then (BUSINESS INFORMATION REQUIRED). | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| ASSET-04 | Assets / story imagery | The Our Story slot is filled by a 650x480 mockup-hero crop rendered at 998x520 (1.53x, 3.07x on 2x screens) with 29% of its height cropped, and the unused alternative images/our-story.webp is smaller still (535x348) with caption fragments at its right edge. | The editorial section is a cropped fragment of an upscaled fragment at every width, and no file in the project can fix it. | Phase 3 will obtain an original photograph at least 2000 px wide for the story section (BUSINESS INFORMATION REQUIRED); subject and composition, including the baked-in text, are in the STORY register. | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| COLL-01 | Collection page | No collection page, template or collection data exists; the Collections and Shop links resolve to the homepage anchor #shop. | There is no browse surface beyond three hard-coded products, so the store cannot present a catalogue. | Build templates/collection.json with a main product grid (paginate, sort, empty state) once collections and products exist in admin. | HIGH | P1 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| CSS-01 | Colour tokens | Colours are hard-coded literals with no custom properties: 18 distinct in the stats block (3 primaries #0d0c0a/#f3efe6/#d8c08a, 3 secondaries #bdb6a8/#ebe6dc/#e9e4d8, the dead #0230, 11 rgba variants) and 21 once the two style-hover shades #2a2823/#e6d3a6 and the swatch olive #4b5443 are counted; #0d0c0a alone appears 18 times whole-file. | Nothing can be driven by settings_schema.json colour schemes, and any palette change means editing every occurrence including the swatch data. | Define the palette as :root custom properties fed by theme settings, derive alpha variants from rgb triplets, and confirm the three secondary, the olive and the two hover values with the owner (BUSINESS INFORMATION REQUIRED). | HIGH | P1 | PHASE 2 — DESIGN SYSTEM |
| CSS-02 | Inline-style architecture | 77 style attributes (6,421 chars, 69% of the CSS) carry all layout and typography, the source has zero classes, and complete recipes (eyebrow, label, CTA, hamburger bar, icon size) are repeated verbatim. | No component can be restyled in one place, the cascade is inverted so every override needs !important, and Theme Editor settings cannot reach any property. | Replace inline styles with BEM-ish component and section classes in a base stylesheet plus per-section CSS files, keeping only Liquid-generated custom properties on section roots. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| CSS-03 | Responsive layer / !important | The responsive layer is 31 rules in two max-width queries keyed on 25 distinct editor data-r hooks (26 occurrences) (32 data-r rules including the base hamburger rule; 34 selector uses) with 55 !important declarations (49 in the 900px query, 6 in the 520px query), plus order:-2/-1 reordering of hero children. | Nothing downstream — colour schemes, section padding settings, later media queries — can override these rules, so the layer cannot be carried into a theme in any form. | Rewrite mobile-first with class selectors and min-width queries so that no !important is needed, and keep source order equal to visual order instead of using order. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| DATA-01 | Product catalogue | The three products (name, price string, image path, three swatch hexes) exist only as object literals inside the data-dc-script class; there are no handles, descriptions, variants, sizes, inventory, SKUs, compare-at prices, vendor, type, tags, secondary images or product URLs. | Nothing about the catalogue can be managed in Shopify admin and the product card has no product.url to link to. | In Phase 6 render the New Drop grid from a collection chosen in section settings (collection.products, product.title, product.price / money, product.featured_image, product.url); the actual catalogue content is BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| DATA-02 | Price and currency | Prices are string concatenations of a symbol and a literal (cur + '1,290') and the Claude Design editor prop currency (enum ₱/$/€, default ₱, section "Shop") only swaps the symbol without converting the amount; no numeric price exists and the prop has no Shopify equivalent. | Selecting $ renders $1,290 for the same item, the amounts are unverified placeholders, and the prop would have to be dropped rather than ported. | Drop the data-props prop entirely; render product.price through the store money format and, if multi-currency is wanted, through Shopify Markets: the market and currency strategy is a BUSINESS DECISION REQUIRED and real prices are BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| DATA-05 | Navigation and utility data | The five menu labels and hrefs (Home #, Shop #shop, Collections #shop, Our Story #story, Verse #) and the hard-coded gold active underline on Home are literals in the markup, the utility icon destinations are not bound to any route object, and the cart badge is the literal text 0 rather than a cart value. | Menus cannot be managed in Navigation admin, the active state is not derived from the current page, and the badge never reflects the cart. | Drive the menu from a link_list section setting with active state from link.current, bind the icon destinations to routes.search_url / routes.account_url / routes.cart_url and the badge to cart.item_count, and obtain the real destinations for Shop, Collections, Verse and Our Story: BUSINESS INFORMATION REQUIRED; the inert controls and placeholder hrefs themselves are in the NAV register. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| ECOM-03 | Search | There is no search form or search template; the search icon is a bare image. | Visitors cannot find products by name or keyword. | Add a search form to the header (modal with predictive search) and templates/search.json. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| ECOM-04 | Variants and availability | There is no variant model (no sizes anywhere, colours as inert hex swatches) and no availability or sold-out state. | A streetwear store cannot sell without size selection and stock awareness. | Model colour and size as product options in admin (size run BUSINESS INFORMATION REQUIRED) and render a variant picker with availability from variant.available. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| FOOT-01 | Footer content | The footer holds only a logo, two taglines and two placeholder social links; it has no navigation, policy, contact, copyright or newsletter content. | Buyers have nowhere to check shipping, returns or contact details, mobile users have no way back to the menu, and standard legal links are absent. | Rebuild the footer as a section-group footer with SHOP / ABOUT / HELP / FOLLOW menu blocks, policy links from shop policies, contact, copyright and newsletter, using business-supplied content. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| HERO-01 | Hero — CTA strategy | The hero contains no link or button; on 1366x768 and 1280x720 the first screen is the hero alone and the nearest CTA ("View All Products", href="#") is below the fold. | The store's primary conversion surface offers no path to a collection, so laptop and phone visitors see a full screen with nothing to act on. | Phase 5 should add one primary hero CTA to a collection (handle and label are BUSINESS INFORMATION REQUIRED) and optionally a secondary link, placed to be visible on 720-768px-high laptops and on phones above the copy stack. | HIGH | P1 | PHASE 5 — HERO |
| HERO-02 | Hero — header backing and scrim | The vertical scrim under the nav thins from .55 to 0 by 30% of the hero height, so Collections, Our Story and Verse sit on open sky between the models where the mockup's nav sits on a dark facade; the measured contrast figures and WCAG classification are in the A11Y register. | Primary navigation legibility depends on the photograph, and the current photo makes three of five links fail on their brightest backing. | Phase 5 (with Phase 4) should give the header a solid ink band or a scrim that stays at or above .8 alpha under the nav, so the header never depends on the hero image; moving the header out of the hero section resolves it structurally. | HIGH | P1 | PHASE 5 — HERO |
| HTML-01 | Document structure / landmarks | There is no `<header>` or `<main>`; the `<nav>` is nested inside the hero `<section>` and absolutely positioned over it, the announcement bar is a plain div, and no section carries an accessible name. | Assistive technology gets no header/main landmarks, the header cannot become a Shopify header-group section without re-laying out the hero, and the coupling is the direct cause of the hero-fade offset and nav-contrast failures recorded in the RESP and A11Y registers. | Rebuild the header (announcement bar + nav) as independent sections in the header group with a `<header>` landmark, wrap page sections in `<main>`, and give each section an aria-labelledby pointing at its heading. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| HTML-03 | Heading hierarchy | The outline is one h1 and two h2s; product names and value titles are `<div>`s and the values section has no heading at all. | Heading navigation cannot reach any product or value and the document outline does not describe the page. | Make each product-card title an h3 inside the product-card snippet, give the brand-values section an h2 (visually hidden if the design requires) with h3 block titles, and keep one h1 per template. | HIGH | P1 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| HTML-04 | Interactive element semantics | The page has zero `<button>` elements: the hamburger is a role-less `<span>` carrying an aria-label and the search, account and cart controls are bare `<img>` elements. | None of these can receive focus or activation, and the aria-label on a generic span is prohibited by ARIA 1.2 and ignored by most screen readers. | Author the menu toggle, search and cart controls as `<button>` elements (or `<a>` for account/cart routes) with SVG icons and visible text or aria-label; the wiring and destinations are in the NAV register. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| INV-05 | Inventory completeness / master sources | The only layered logo sources (OG LOGO.psd 613,320 B, OG LOGO 300x300.psd 209,976 B and PNG exports) live outside the project at Desktop/GODSQUAD/PSD FILES, the original export zip lives in Downloads, and no vector logo (SVG/AI/EPS) or original photography master has been located anywhere; every image in the project is a mockup crop, an AI-generated sheet or a padded PNG export. | The rebuild cannot produce a crisp SVG wordmark or full-resolution hero, story and product imagery from what the project contains. | In Phase 3 gather masters into a source/ folder adjacent to (not inside) the theme and obtain a vector logo and original photography from the owner: BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| JS-01 | support.js purpose and fit | support.js is a 69,150 B (19,037 B gz), 1,911-line generated Claude Design editor/streaming runtime ("GENERATED from dc-runtime/src/*.ts — do not edit") whose job is to compile the dc template into React and talk to the design editor; roughly 600 of its lines (x-import/Babel loader, deck-stage keying, streaming placeholders, sibling-component fetch, stream tracker, canvas mode, editor bridge API) are code paths this page never enters. | A store would ship an unmodifiable editor runtime plus React to render three products and four value tiles that Liquid renders server-side for free. | REMOVE DURING SHOPIFY CONVERSION: carry nothing from support.js into the theme and author the small amount of real interaction JS fresh in Phases 4 and 8. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| JS-02 | Render-blocking JavaScript chain | First paint requires three dependent network hops after the document (support.js synchronous in head; React and ReactDOM fetched in parallel with async=false; then boot() on DOMContentLoaded), about 211 KB raw / 66 KB gzipped of JavaScript that is all effectively render-blocking because the template is hidden until React mounts. | On a throttled mobile connection the page stays black for the whole chain and LCP is gated by script delivery rather than by the hero image. | Resolved by removing the runtime in Phase 10; in Phase 12 verify the Liquid theme ships no framework and that the hero image is the LCP element. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| NAV-01 | Mobile navigation | Below 900px the nav links are display:none and the hamburger is a span with no role, tabindex or handler, so there is no navigation at all on phones and tablets. | Mobile visitors cannot reach Shop, Collections, Our Story or Verse except by scrolling; the store is unnavigable on its most important device class. | Build a real menu button (button with aria-expanded) opening a drawer that holds the menu and utility links, driven by the Shopify navigation menu. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| NAV-02 | Header utilities | Search, Account and Cart are bare img elements with tabIndex -1 and no link or button wrapper. | None of the three utility functions can be used by mouse, touch or keyboard. | Wrap each in a link or button bound to routes.search_url, routes.account_url and routes.cart_url, with accessible names and 44px targets. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| NAV-03 | Navigation URLs | Six of nine links (Home, Verse, View All Products, Our Story CTA, Facebook, Instagram) are href="#" and scroll to the top of the page. | Most calls to action produce a jarring jump instead of a destination, and crawlers see six identical placeholder targets. | Bind each link to its Shopify route, page or setting (routes.root_url, collection.url, page URL, social settings) once the destinations are supplied. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| PERF-01 | Performance / hero image weight | images/hero-group.png is a 1,989,201-byte 1672x941 RGB PNG with no alpha channel and is served unchanged at every viewport, including a 375x320 band. | One file is 80% of the page's bytes and the largest contentful paint at every width; on a phone it downloads 2 MB to show about two thirds of the picture, the 375x320 cover crop discarding roughly 34% of the scaled width. | Phase 3 will keep the PNG as the master and generate responsive WebP derivatives through the Shopify CDN (image_url widths); the reviewers expect the format change alone to cut the file by roughly an order of magnitude at equal visual quality, to be measured. | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| PERF-02 | Performance / LCP delivery | The hero image has no preload, fetchpriority, srcset/sizes or width/height, and its paint is gated behind the runtime's three-hop JavaScript chain. | The LCP element starts at default priority, cannot be resized per viewport, and paints only after about 66 KB gz of JavaScript has executed and the page has rendered twice. | Phase 5 will build the hero section with image_tag (explicit widths and sizes, intrinsic dimensions, preload: true) plus a fetchpriority="high" attribute written on the img itself, and no JavaScript dependency; Phase 12 will measure the result. | HIGH | P1 | PHASE 5 — HERO |
| PROD-01 | Product cards | No product card contains a link; product names are divs and the grid holds zero anchors. | A product cannot be opened, so the homepage cannot lead to a purchase. | Wrap image and title in an anchor to product.url in a product-card snippet, with the title as a heading. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| PROD-02 | Quick add | There is no add-to-cart or quick-add control on the cards or anywhere on the page (zero forms, zero buttons). | Nothing can be added to a cart from the homepage. | Add a quick-add control on cards (product form with the first available variant, or a variant chooser for sized products) once the product form and cart exist. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| RESP-01 | Hero (<=900px) | Below 900px the hero fade is anchored to the section top while the image sits under the 88px in-flow nav, so the gradient goes solid black 88px above the photo's bottom and the last 88px of photo reappear unfaded with a hard edge. | Every phone and tablet hero (the LCP element) shows a black band through the seated model and a hard cut instead of a fade, and zoomed desktops get the same. | In Phase 5 anchor the fade to the image (wrap image and fade in one relative container or offset the fade by the nav height) or move the nav out of the hero section; verify at 375, 768, 812x375 and 720. | HIGH | P1 | PHASE 5 — HERO |
| RISK-01 | Risk: assets | Every image in the project is a mockup crop or a single AI PNG, and no vector logo has been seen, so no asset is fit for its slot at 2x. | Sections rebuilt around these files will look soft on phones and the premium positioning fails regardless of code quality. | Phase 3 will acquire original photography and a vector wordmark before any section build, treating the mockup crops as ARCHIVE-class references. Resolution and weight defects: see the ASSET register. | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| RISK-02 | Risk: business information | The prototype contains no store facts: no destinations, policies, contacts, social URLs, catalogue, sizes, markets or verse content, and the footer has no copyright, policy or navigation links in either the build or the mockup. | Templates cannot be completed without invention, and invention is prohibited by the spec. | Phase 2 will run the business-information intake checklist and gate Phase 4 on navigation URLs, Phase 8 on the catalogue and Phase 15 on legal text. | HIGH | P1 | PHASE 2 — DESIGN SYSTEM |
| RISK-03 | Risk: brand fidelity | The build already departs from the approved mockup in hero photo, headline lockup, wordmark size, product tiles, social icons and globe colour, leaving two competing baselines. | The rebuild could inherit either baseline at random, producing a theme that matches neither the mockup nor the owner's edits. | Phase 2 will record a signed decision per deviation and freeze the design baseline that the rebuild targets. | HIGH | P1 | PHASE 2 — DESIGN SYSTEM |
| RISK-04 | Risk: runtime confusion | The prototype boots from a double-click and looks reusable, but its template syntax collides with Liquid and its first paint depends on fetching React from unpkg.com. | Reuse produces silently empty tiles in Liquid or a blank page when unpkg is unreachable, and wastes conversion effort on a generated editor runtime. | Phase 10 will start from an empty theme scaffold under a written rule that no prototype file is copied, with the prototype archived read-only. Runtime removal: see the ARCH register. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| RISK-05 | Risk: mobile regression | The mobile layer is 31 media-query rules (26 at max-width 900px, 5 at max-width 520px) that override the desktop rules with !important, it carries a live hero-fade defect, and no genuine device captures or pass criteria exist for the rebuild. | Phone layouts can regress unnoticed while desktop parity is being chased. | Phase 9 will define acceptance renders per width from the mobile-*-true.png series and rebuild mobile-first. Layout outcomes: see the RESP register. | HIGH | P1 | PHASE 9 — MOBILE UX |
| RISK-06 | Risk: scope | The programme is framed as a conversion but the prototype is a homepage with no commerce, so the real scope is a complete theme with one designed page and at least nine undesigned storefront templates, about twenty once the customer, gift card and blog routes are counted. | Product, collection, cart and search experiences will be built last and worst if the scope is not priced and sequenced. | Phase 8 will fix the launch feature set using the ECOM register's CURRENT / MISSING / REQUIRED / OPTIONAL classification and budget every template in §29.5. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| RISK-07 | Risk: working copy | The project lives in a personal OneDrive folder with no git history, no build tooling, an in-place rename performed by the owner and a sibling assets folder that has already disappeared. | The design baseline can drift or be lost silently, and there is no history to recover from. | Before Phase 2 work, the theme will be initialised in git outside OneDrive and the prototype folder and export zip archived as a read-only baseline. | HIGH | P1 | PHASE 2 — DESIGN SYSTEM |
| RISK-10 | Risk: performance budget | No performance budget exists and the prototype carries a 1.99 MB hero PNG, 308 KB of PNG icons and ~211 KB of render-blocking JavaScript. | Assets carried over uncritically will miss any reasonable LCP target on mobile networks, and the outcome is fixed at asset acceptance rather than at the later performance pass. | Phase 2 will set the budget (LCP image, above-fold bytes, JS bytes), Phase 3 will enforce it at asset acceptance — where it is actually met or missed — and Phase 12 will confirm it with throttled Lighthouse runs. | HIGH | P1 | PHASE 3 — ASSET PREPARATION |
| RISK-14 | Risk: accessibility debt | The transparent nav over the hero photo measures below WCAG AA for Collections, Our Story and Verse at 1024 and 1440 — 2.4-2.9:1 when the fade alpha is composited over sampled photo luminance, and 2.4-2.5:1 over the brightest 2% of the render's pixels although 4.6-5.7:1 on the median — while at 1024 the gold Home link drops to ~3.5:1 and the header has no operable controls. | A theme that reproduces the prototype's header composition fails WCAG AA before any content is added. | Phase 4 will build the header on a solid or strengthened band, sized to pass on the brightest sample rather than the median, with real buttons; Phase 14 will verify with axe and a keyboard pass. Defects: see the A11Y register. | HIGH | P1 | PHASE 14 — ACCESSIBILITY |
| SEO-01 | SEO / head metadata | The document has no `<title>` element, so document.title is empty at runtime. | The page has no name in tabs, bookmarks, history, share sheets or search results, and no title copy exists to carry into the theme. | Phase 13 will define the `<title>` pattern (page_title plus shop name) in layout/theme.liquid; the homepage title copy is BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 13 — SEO |
| SEO-02 | SEO / head metadata | No meta description exists anywhere in the document. | Search engines and link previews must synthesise a snippet from about 120 words of tracked-caps copy, and no approved description exists for the theme. | Phase 13 will output page_description with a shop-level fallback; the description copy is BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 13 — SEO |
| SHOP-02 | Theme Editor | No section schemas, JSON templates or section groups exist; the only editable value in the project is the Claude Design currency prop in data-props. | The merchant could change no text, image, colour, menu or product selection in Shopify's Theme Editor. | Phase 11 will implement the schema settings and blocks in §29.7 with presets and block.shopify_attributes, after agreeing the settings surface with the owner. | HIGH | P1 | PHASE 11 — THEME EDITOR |
| SHOP-03 | Configuration | There is no config/settings_schema.json or settings_data.json: brand colours are literals repeated across the 77 inline styles and the 2,916 B `<style>` block (all sources: #0d0c0a x14, #d8c08a x10, #f3efe6 x9, #bdb6a8 x3; inline-only the repeats are background:#0d0c0a x6, background:#f3efe6 x6, color:#d8c08a x5); fonts are hardcoded in the `<style>` and in a body-level Google Fonts link (line 12); the logo is a hardcoded `<img src>` (lines 69, 155); and no social URLs exist at all, both social links being href="#" (BUSINESS INFORMATION REQUIRED). | Global theme settings cannot exist, and the palette, type, logo and social set cannot be changed or themed without editing markup. | Phase 10 will create settings_schema.json with the areas in §29.6 and a css-variables snippet that maps settings to custom properties; token definitions themselves are owned by the BRAND register, and the social URLs are BUSINESS INFORMATION REQUIRED. | HIGH | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| SHOP-04 | Section groups | The nav is absolutely positioned inside the hero section and the hero copy reserves 170 px / 190 px of top padding to clear it, so the announcement bar and header cannot be extracted into a header section group without re-laying the hero. | The header group required by Online Store 2.0 cannot be formed from the current composition, and the hero-fade offset defect below 900 px is a direct consequence of the coupling. | Phase 4 will build header and announcement-bar as independent sections in sections/header-group.json with a transparent_over_hero option and a solid top band; the hero will stop reserving padding for the nav. Markup semantics: see the HTML register. | HIGH | P1 | PHASE 4 — HEADER & NAVIGATION |
| SHOP-09 | Template coverage | Only the homepage exists; product, collection, list-collections, cart, search, page, page.our-story, 404, password, gift card and customer templates that Shopify serves have no prototype design at all. | Shopify serves an error page for a storefront route whose template is missing, so the conversion cannot launch without designing and building at least nine additional templates, rising to about twenty once the seven customer templates, gift card, blog and article are counted; templates/customers/* are needed only if classic customer accounts are chosen, and password and gift_card only if those features are enabled. | Phase 8 will design the storefront template set in §29.5 with minimal but on-brand sections, classifying each as REQUIRED, OPTIONAL or BUSINESS DECISION REQUIRED. Feature behaviour: see the ECOM register. | HIGH | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| STORY-01 | Our Story — image asset | The section uses ./01-hero-model-mu98p88t-7jig.webp, a 650x480 crop of the mockup's hero with the headline fragments "A PURPOSE", "K BY", "TH." and the "More Than Clothing" script baked into the pixels, while the mockup's three-model story image (images/our-story.webp) is unused. | Visible stray lettering appears at every width and a section titled "Real People" shows one model instead of the community the copy describes. | Replace the asset with a purpose-shot or re-rendered story image that matches the mockup's three-model intent (Phase 3 sources it, Phase 7 places it); the required master resolution and delivery strategy are in the ASSET register. | HIGH | P1 | PHASE 7 — OUR STORY |
| UX-01 | Hero / conversion path | The hero contains no link or button, so the first screen asks nothing of the visitor and on 1366x768 and 1280x720 laptops no product or CTA is visible without scrolling. | The primary above-the-fold conversion opportunity is unused and the only route into the shop is the nav Shop link or scrolling. | Add one primary CTA to the drop collection (and an optional secondary CTA to Our Story) as button blocks in the hero section, with label and URL editable. | HIGH | P1 | PHASE 5 — HERO |
| CSS-04 | Breakpoint system | Only two desktop-first max-width breakpoints exist (900px and 520px) with no min-width queries and no step between 901 and 1440. | 768px tablets receive phone rules while 920-1279px laptops receive the full three-column hero with 8.5vw type, producing the wrapping and orphaning measured in the RESP register. | Define mobile-first min-width steps (750px and 990px, with an optional 1200px step for the hero copy column) in the design system rather than from the current code, then apply and verify them per width in the mobile UX phase. | MEDIUM | P1 | PHASE 2 — DESIGN SYSTEM |
| CSS-07 | Interaction states | Hover exists only as a global a:hover colour (invisible on Home and on the image-only social links) and two runtime-generated .scp0/.scp1 :hover rules from style-hover; there are no :focus-visible, :active or transition rules and the hover shades #2a2823/#e6d3a6 are undocumented. | The CTA hover works today but only under support.js, keyboard users get the browser default ring only, and the theme has no defined state system to implement. | Define hover, focus-visible, active and reduced-motion-guarded transition rules once in base.css with named hover tokens; contrast and keyboard measurements are in the A11Y register. | MEDIUM | P1 | PHASE 2 — DESIGN SYSTEM |
| CSS-08 | Typography tokens | Typography is hard-coded as six px sizes between 9 and 15px plus four clamp() headings, six letter-spacing values, nine line-heights and three repeated font-family stacks, with no named scale. | Type cannot be set from font_picker settings or adjusted per breakpoint in one place, and the mobile scale never reaches 16px. | Extract a named type scale (sizes, tracking, leading, families) into custom properties in Phase 2 and confirm whether the 11-13px tracked caps are brand-mandated on phones (BUSINESS INFORMATION REQUIRED). | MEDIUM | P1 | PHASE 2 — DESIGN SYSTEM |
| DEBT-12 | Process debt | The project is not a git repository, has no package.json or build tooling, lives inside a personal OneDrive folder, the spec still names the old file name, and four unreferenced root-level exports (chatgpt-image-…png, white-font-300x300-…png, two white-font-trans-…png) sit beside the referenced story WebP in the root. | There is no history to diff the prototype against, sync conflicts or accidental edits are unrecoverable, and naming drift confuses every later phase. | Create a repository for the theme via Shopify CLI in the conversion phase, and commit the frozen prototype and this audit's evidence as the baseline before then (store and Git host availability: BUSINESS INFORMATION REQUIRED); the root-level asset placement itself is classified in the ASSET/PERF register. | MEDIUM | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| DEBT-13 | Baseline drift | The prototype remains editable in Claude Design and has already diverged from the mockup by deliberate edits (group hero photo, gold globe, two social boxes removed); each further edit adds inline styles and invalidates this audit's measurements. | The audit's numbers are only valid for the file at md5 787068e3…; unlogged edits would silently move the design baseline. | Freeze the file as the design baseline, record its hash, and log the open design decisions (hero photo, globe colour, social set) for confirmation in Phase 2 (BUSINESS DECISION REQUIRED). | MEDIUM | P1 | PHASE 2 — DESIGN SYSTEM |
| HERO-05 | Hero — photo direction decision | The build's hero is a three-model generated group image (images/hero-group.png, identical to the ChatGPT upload) that the user substituted for the mockup's single capped model, so hero and story imagery are inverted relative to the approved mockup. | Until the direction is confirmed, Phase 3 cannot know which image to master and Phase 5 cannot finalise the composition, scrim and nav backing. | Record the group photo as the approved direction or revert to the single model (BUSINESS INFORMATION REQUIRED), and confirm whether real photography or a higher-resolution master exists for whichever is chosen. | MEDIUM | P1 | PHASE 5 — HERO |
| HTML-02 | Root element | The `<html>` element has no lang attribute. | Screen readers pick a default voice and search engines cannot confirm the page language. | Set lang from Shopify's request.locale.iso_code in layout/theme.liquid once the store locale is confirmed (BUSINESS INFORMATION REQUIRED). | MEDIUM | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| HTML-05 | Nonstandard elements and attributes | The markup depends on runtime-only constructs: `<x-dc>`, `<helmet>`, three `<sc-for>`, two `<sc-if>`, two style-hover, four data-screen-label, five hint-placeholder-* attributes and a text/x-dc data script. | The file is not valid standalone HTML and cannot be copied into a Liquid section; every construct must be transcribed by hand. | Transcribe the sections into Liquid with {% for %}/{% if %}, ordinary CSS hover rules and no editor metadata; the runtime dependency and Liquid-delimiter collision are recorded in the ARCH/JS register. | MEDIUM | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| HTML-06 | Image attributes | None of the 12 images carries width, height, srcset, sizes, loading or decoding attributes. | The browser cannot reserve layout space (layout shift risk) or choose a size-appropriate candidate, so the 1.99 MB hero and the upscaled product crops are served identically at every width. | Emit every image through Shopify's image_tag filter with widths and sizes, eager/high-priority for the hero and lazy for below-fold images; file resolution and weight are in the ASSET/PERF register. | MEDIUM | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| HTML-09 | Head content in body | The stylesheet, the Google Fonts link and the preconnect live inside `<helmet>` in the body and are only hoisted into `<head>` by the runtime. | Without support.js the document has no head-level presentation, the font request starts late, and no head snippet exists to port. | Author a head snippet in layout/theme.liquid that carries fonts, base stylesheet, preconnects and metadata; font loading strategy is in the PERF register and meta tags in the SEO register. | MEDIUM | P1 | PHASE 10 — SHOPIFY THEME CONVERSION |
| INV-01 | Project inventory / source control | The project is a single working copy inside the owner's personal OneDrive with no git repository, no package manifest and no build tooling, so the audited state (44 files, 17,185,754 bytes) has no tagged baseline. | Any later edit or OneDrive sync conflict silently changes the design baseline that the Shopify rebuild must be measured against. | Before Phase 2 work starts, place the folder under version control (or at minimum create a dated read-only archive alongside the original export zip) and tag it as the Phase 1 baseline. | MEDIUM | P1 | PHASE 2 — DESIGN SYSTEM |
| JS-08 | Interaction layer | The runtime wires only on* attributes present in markup and the markup has none, so zero interaction JavaScript exists: no menu toggle, search, account, cart, variant or quick-add behaviour is available to port. | Every store interaction must be written from scratch; there is no behaviour to preserve, only visual states, and the hamburger and utility icons are inert (their controls are in the NAV register). | Plan Phase 4 (menu drawer, predictive search, cart drawer) and Phase 8 (product form, variant picker) as new framework-free theme JavaScript that re-initialises on the shopify:section:load and shopify:section:unload Theme Editor events. | MEDIUM | P1 | PHASE 4 — HEADER & NAVIGATION |
| NAV-09 | Cart badge | The cart badge is the literal text 0 with no relationship to any cart. | The header signals an empty cart regardless of state and cannot reflect purchases. | Bind the badge to cart.item_count inside a cart link and update it after Ajax cart changes. | MEDIUM | P1 | PHASE 4 — HEADER & NAVIGATION |
| PROD-04 | Pricing display | Prices are displayed without money formatting, compare-at/sale, from-pricing or sold-out states, and the currency prop only swaps the symbol on the same number. | Pricing cannot express sales, ranges or availability and would show wrong amounts if the symbol were changed. | Render product.price and product.compare_at_price with the money filters and add sale/sold-out badges; remove the symbol prop in favour of store currency and Markets. | MEDIUM | P1 | PHASE 8 — PRODUCT & SHOPPING UX |
| A11Y-02 | Bypass blocks and landmarks | There is no skip link and no main landmark; the nav lives inside the hero section, and the four section elements have no accessible name so they are exposed as generic containers rather than regions (data-screen-label is editor metadata and names nothing). The only landmarks on the page are the unnamed nav and the footer as contentinfo. | Keyboard and screen-reader users must tab through the header on every page load, cannot jump to content, and a landmark list offers two entries with no banner, no main and no named regions to orient by. | In Phase 10 add a skip link as the first focusable element in layout/theme.liquid pointing at a main landmark that wraps the template content, with header and footer as their own landmarks, and give each section an accessible name (aria-labelledby on its heading) so it is exposed as a region. | MEDIUM | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| A11Y-04 | Focus states | No :focus or :focus-visible rule exists; the browser default ring is the only indicator, and the two raster social icon links have no hover or focus state at all. | Focus is unbranded, inconsistent across browsers and unverified against the dark photo and cream band. | In Phase 14 add a token-driven :focus-visible style (gold ring with offset) for links, buttons and icon controls, and verify it on every background. | MEDIUM | P2 | PHASE 14 — ACCESSIBILITY |
| A11Y-05 | Colour swatches | The nine swatches are empty spans with inline backgrounds and no name, role or text, and the cream swatch on the cream section is distinguished only by a ~1.8:1 border. | Screen-reader users get no colour information and low-vision users cannot see the cream option. | In Phase 8 render swatches from variant options with a visually hidden colour name (or aria-hidden swatches plus text), a 3:1 border and, once selectable, real controls. | MEDIUM | P2 | PHASE 8 — PRODUCT & SHOPPING UX |
| A11Y-08 | Heading outline | The outline is one h1 and two h2s whose DOM text is TheFaithful and Real People.Bigger Purpose. (line breaks via br), while product names and value titles are divs. | Heading navigation never reaches a product or value, and heading lists can read the section titles as single words. | In Phase 14 make product titles h3 inside the product card snippet, value titles h3 inside the block, add headings for Values and the footer, and replace layout br elements with block elements or spans. | MEDIUM | P2 | PHASE 14 — ACCESSIBILITY |
| A11Y-09 | Alt text | Of the 12 image tags in the source, 4 are wrong (Search, Account and Cart name functions that do not exist; the story alt says community but the picture shows one man and carries baked-in headline fragments), 3 are redundant (the product template alt repeats the name shown below it, and both social alts repeat the link's aria-label) and 1 is generic (the hero alt omits the on-garment message and the setting). Only 4 are correct: the announcement globe, both wordmarks and the value icons. | Screen-reader users hear inaccurate or doubled descriptions on 8 of 12 images, including the LCP photo and every product card. | In Phase 14 set descriptive alts for the two photos from business-supplied descriptions (BUSINESS INFORMATION REQUIRED), empty alts on images inside named controls and links, and drive product alts from product.featured_image.alt. | MEDIUM | P2 | PHASE 14 — ACCESSIBILITY |
| A11Y-10 | Target sizes | The hamburger is 22x16, the utility icons 24x24, the social links 28x28 and the swatches 16x16 at every width. | The hamburger and swatches fail the 24px minimum and nothing in the header reaches the 44px phone guidance, which the rebuild will inherit from the mockup. | In Phase 9 set a 44x44 minimum hit area token for header, social and swatch controls (icon glyphs can stay 24px inside the larger target). | MEDIUM | P2 | PHASE 9 — MOBILE UX |
| ARCH-04 | Head and asset delivery | The only stylesheet (2,916 B `<style>`) and the Google Fonts `<link>` are authored inside `<helmet>` in the body and reach `<head>` only because the helmet manager clones them at render time; the real `<head>` holds only charset, viewport and the runtime script. | Without the runtime the page has no head-managed styles or preloads, and there is no place today for title, meta, canonical, favicon or font preload hints (the tags themselves are in the SEO register). | In Phase 10 author theme.liquid's `<head>` explicitly (content_for_header, stylesheet_tag, font preloads) and move the CSS into assets/. | MEDIUM | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ASSET-05 | Assets / hero master | The hero master is a 1672x941 image whose upload filename ("ChatGPT Image Sep 20, 2026, 11_06_34 AM.png") indicates AI generation, unconfirmed by the business (BUSINESS INFORMATION REQUIRED); it is 0.85x at 1440 on 1x displays but about 1.7x upscaled on 2x displays, with no portrait or higher-resolution source. | HiDPI desktops and the phone crop both run out of pixels, and the image's status (provenance, approved final, licensed, regenerable) is undocumented. | Phase 3 will confirm with the business whether the group image is final and how it was produced, obtain a higher-resolution or regenerated source plus a phone crop, and record usage rights if it is AI-generated (BUSINESS INFORMATION REQUIRED). | MEDIUM | P2 | PHASE 3 — ASSET PREPARATION |
| ASSET-06 | Assets / logo | The only logo files are raster PNGs; the wordmark in use is a 500x500 canvas with large transparent padding (visible mark 66x50 px in a 78 px box), byte-identical to a Desktop PNG, and no SVG, AI or EPS was seen anywhere. | The mark renders at half the mockup's relative size, cannot scale cleanly for HiDPI, favicon, share image or print, and cannot be recoloured. | Phase 3 will export a trimmed SVG wordmark and a square mark from the Desktop PSDs if their layers are vector, otherwise obtain vector artwork from the designer (BUSINESS INFORMATION REQUIRED); if no vector can be obtained the fallback is a trimmed PNG re-export, a Phase 3 decision. The padded rendering size itself is in the BRAND register. | MEDIUM | P2 | PHASE 3 — ASSET PREPARATION |
| BRAND-01 | Brand — colour tokens | The three brand colours exist only as raw literals (#0d0c0a x14, #d8c08a x10, #f3efe6 x9 in the stats) with no named tokens, and the CTA hover tints #2a2823/#e6d3a6 exist only inside editor-only style-hover attributes. | Nothing can be driven by Shopify colour or colour-scheme settings and every re-implementation risks colour drift from the approved identity. | Phase 2 should name the tokens (ink, cream, gold, ink-hover, gold-hover) with their computed contrast pairs and map them to settings_schema colour-scheme roles before any section is written. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| BRAND-03 | Brand — currency and arrow glyphs | Jost's loaded faces do not contain U+20B1 (₱) or U+2192 (→), so every price and both CTA arrows are drawn by a per-platform fallback font that differs from the mockup's sans ₱. | Prices and buttons — the most commercial typography on the site — look different on Windows, macOS, iOS and Android and never match the approved design. | Phase 2 should decide the currency treatment (a face that includes ₱, a small subset font for the symbol, or a money format tested with Shopify's currency settings) and replace text arrows with an SVG icon in the button component. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| BRAND-04 | Brand — type scale and label roles | The type system is six fixed sizes (9-15px) plus four clamps, six letter-spacings and nine line-heights, with the tracked-caps label drawn in several unrelated variants (eyebrow 13px .3em at weight 400 or 500; taglines 14px .3em and 13px .24em; captions 11-12px at .2/.22/.26em), and Playfair 700 requested but unused. | Labels and captions cannot be built as reusable components, and the mobile page is dominated by 11-14px tracked caps with no role definitions. | Define a type ramp (display xl/l/m, script, eyebrow, label l/m/s, body, badge) with fixed tracking and leading per role, and drop the unused 700 weight from the font request. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| BRAND-05 | Brand — wordmark asset and scale | images/WHITE FONT LOGO.png is a 500x500 PNG with large transparent padding, so the wordmark renders at 66x50 px at 1440 (mockup 114x87 on a 1024 canvas) and 47x36 in the footer, and no vector master has been seen (only PSDs outside the project). | The brand mark has about half its intended presence in the header and footer, and cannot be scaled crisply for HiDPI, favicon or social preview uses. | Obtain or trace an SVG wordmark trimmed to its ink bounds and set minimum rendered sizes for nav, footer and mobile in the design system; file duplication and format belong to the ASSET register. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| BRAND-07 | Brand — icon system | Three icon vocabularies coexist (gold outline value icons plus the same gold globe in the announcement bar, cream outline utility icons, circled social glyphs vs the mockup's plain glyphs), all as raster PNGs with colour baked in, and the same globe file is drawn at 16px and 44px. | Icons cannot follow colour tokens, hover or colour-scheme settings, and the header, values and footer read as three different icon styles. | Specify one SVG icon set on a 24px grid with a single stroke weight using currentColor (search, account, cart, menu, close, arrow, globe, crown, community, diamond, facebook, instagram); social style to follow the mockup unless the circled style is confirmed. Format and weight are in the ASSET register. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| COLL-02 | Collection index | There is no collection index and no defined collection taxonomy, so Collections and Shop are indistinguishable. | The COLLECTIONS nav item cannot be wired and category-led discovery is impossible. | Confirm the collection structure with the business (BUSINESS INFORMATION REQUIRED) and add templates/list-collections.json with collection images and descriptions. | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| COLL-03 | Merchandising model | The New Drop / The Faithful section implies drop-based merchandising but no collection is defined for it and its three products are a hard-coded array. | The drop cannot be updated without editing code and the relationship between drops and categories is undefined. | Define The Faithful (and future drops) as collections and bind the featured-collection section to a collection picker. | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| CSS-09 | Spacing tokens | Spacing uses 44 distinct px values across 22 padding, 14 margin and 17 gap strings, three competing gutters (48/24/16px) and bespoke fr ratios per section grid. | No base unit exists, so section padding settings and consistent rhythm cannot be expressed. | Derive a 4px-based spacing scale and a stepped --gutter token from the mockup in Phase 2 and express section grids as reusable column templates. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| DATA-03 | Colour swatches | Each product carries the same three hex values (#0d0c0a, #f3efe6, #4b5443) as an unnamed array not tied to any variant, rendered as inert spans. | The swatches cannot represent real stock or be selected, and have no accessible colour name (labelling is in the A11Y register). | Model colour as a variant option and drive swatches from variant option values plus a colour metafield or the native Color category metafield; real colour names and per-product availability are BUSINESS INFORMATION REQUIRED. | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| DATA-04 | Brand values data | The four value tiles (title, sub, icon path) are an array in the data-dc-script rendered through sc-for, with icons as paths to raster PNGs. | The strip cannot be edited without editing JavaScript, and the "Worldwide / Shipping Available" tile asserts a shipping policy nobody has confirmed. | Make the strip a section with up to four blocks (icon select or image_picker, title, subtitle) in Phase 11, seeded with the current strings; confirm the shipping claim: BUSINESS INFORMATION REQUIRED. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| DATA-06 | Copy strings | All copy (announcement, hero eyebrow/heading/verse/taglines, New Drop heading and subheading, story heading/paragraph/caption, footer taglines, button labels) is inline text in the template, frequently with layout-bearing `<br>` tags. | No copy can be changed in the Theme Editor and the intended line breaks are welded to the strings. | Expose each string as a text, inline_richtext or richtext section setting in Phase 11 with the current strings as schema defaults, and move UI labels (Search, Cart, Menu, Account) to locales/en.default.json. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| DATA-07 | Image references | All 15 referenced image files (17 references) are relative file paths hard-coded in the template or the data script (images/..., ./01-hero-model-mu98p88t-7jig.webp), including the logo path with spaces used twice. | No image can be swapped from the Theme Editor or served through Shopify's image CDN with srcset. | Map logo, hero and story images to image_picker settings rendered with image_url/image_tag, product images to product.featured_image, and UI/value icons to SVG snippets during Phases 10 and 11. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| DATA-08 | Social links | Facebook and Instagram point to "#" and the mockup's TikTok and YouTube are absent by a deliberate editor removal, so no social destination exists in the data. | Nothing connects to a real profile and the final network set is undecided. | Use theme settings (social_facebook_link, social_instagram_link, social_tiktok_link, social_youtube_link) rendered only when populated; the URLs are BUSINESS INFORMATION REQUIRED and the final set is a BUSINESS DECISION REQUIRED. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| ECOM-05 | Customer account | The account icon is inert and no account pathway or decision on customer accounts exists. | Returning customers have no login, order history or saved details. | Decide whether accounts are enabled and which type (BUSINESS DECISION REQUIRED), then link the icon to routes.account_url and include the account templates. | MEDIUM | P2 | PHASE 8 — PRODUCT & SHOPPING UX |
| ECOM-06 | Filters and sorting | No sorting or filtering exists because there is no collection page. | Browse cannot be ordered or narrowed once the catalogue grows. | Implement native sort_by on the collection template in Phase 6; add storefront filters only if the catalogue size (BUSINESS INFORMATION REQUIRED) justifies the Search & Discovery app (BUSINESS DECISION REQUIRED). | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| ECOM-09 | Currency and markets | The prototype implies PHP pricing with a ₱/$/€ symbol-only toggle and no market, shipping-destination or currency strategy is defined. | International selling (promised by Worldwide Shipping) cannot be configured and the toggle would misprice products. | Decide store currency, selling markets and shipping zones (BUSINESS DECISION REQUIRED); use store currency, money filters and Shopify Markets instead of a theme prop. | MEDIUM | P2 | PHASE 8 — PRODUCT & SHOPPING UX |
| FOOT-02 | Footer social links | Facebook and Instagram link to # and the network set (two in the build, four in the mockup) is an undecided editor change. | Social entry points are dead and the brand's actual channels are unknown. | Confirm profile URLs and the channel set (BUSINESS INFORMATION REQUIRED) and drive the links from theme settings with SVG icons. | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| FOOT-03 | Newsletter | There is no email capture anywhere on the page. | No mechanism exists to retain visitors who do not buy on first visit or to announce drops. | Add a newsletter block using the customer form once the provider, copy and incentive are decided (BUSINESS DECISION REQUIRED). | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| HERO-03 | Hero — headline lockup | The h1 stacks WALK / BY / FAITH. on three lines at 1024, 1440 and 1920 and collapses to one line at 768-900, reproducing the mockup's two-line lockup only at phone widths, because the copy column (about 450px at 1440) cannot hold "WALK BY" at the 112px clamp and text-wrap:balance redistributes the break. | The signature lockup — gold FAITH. under WALK BY — is never seen on a desktop or laptop screen. | Lock the headline to two lines with an explicit break after BY, derive the copy column's minimum width from the clamp (or the clamp from the column) and remove text-wrap:balance from the h1. | MEDIUM | P2 | PHASE 5 — HERO |
| HERO-04 | Hero — copy hierarchy on small screens | Six copy elements carry no priority rule, so below 900px all of them stack under the photo band (five taglines, 563px of text under a 320px image, hero 970px tall at 375) and the side captions become orphan blocks. | Phone visitors scroll 1.2 screens of taglines before the shop section and the hero's message dilutes into five competing lines. | Phase 5 should rank the copy (eyebrow, h1, verse essential; tagline stack, script and "A Higher Purpose." optional) and specify which elements hide or merge on phones; the layout mechanics are in the RESP register. | MEDIUM | P2 | PHASE 5 — HERO |
| HTML-07 | Copy markup | Twelve `<br>` elements set layout line breaks, including inside both h2s and every multi-line tagline; the h1 carries none and wraps by column width. | Copy that moves into Theme Editor settings cannot carry the breaks, the breaks fight text-wrap:balance, and the Our Story h2 already wraps to three lines at 1440 and four at 1024 despite its break. | Store copy as plain settings text and control line breaks with column width and max-width tokens; where a deliberate lockup is required, use a richtext setting or a span with display:block. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| HTML-10 | Navigation markup | The five navigation links are bare anchors in a `<div>` with no `<ul>`/`<li>`, and the `<nav>` has no aria-label; the utility controls sit outside any list. | Screen readers cannot announce the number of items or distinguish the primary nav from future footer navs. | Render the primary menu from a Shopify linklist as `<nav aria-label="Primary">` `<ul>` `<li>` `<a aria-current="page">`…, with the utility group in its own labelled list. | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| ICON-01 | Icons / raster icon system | All ten icon placements are nine raster RGBA PNGs (308,521 B on four canvases: 110x110, 130x110, 150x110, 130x130) with cream or gold colour baked into the pixels and soft cut edges from an AI sprite sheet. | About 30 KB per glyph, no hover, focus or theme-colour states, edges that soften at 16-28 px, and icons that cannot follow the Phase 2 colour tokens. | Phase 2 will define a single inline-SVG icon snippet system (24 px grid, 1.5 px stroke, currentColor, aria-hidden) covering search, account, cart, menu, close, arrow, crown, community, globe, diamond and the social glyphs, replacing every PNG. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| ICON-04 | Icons / coverage | No icons exist for the interactions the store will need (close, chevron, plus/minus, check, filter, external link), the hamburger is three CSS spans, and the CTA arrows are a text glyph outside Jost. | The mobile drawer, cart drawer, accordions, product options and buttons cannot be built from the current asset set. | Phase 2 will extend the SVG set with the utility icons and an icon-arrow so every control shares one system; the arrow glyph fallback is in the BRAND register. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| JS-04 | Security: code evaluation and CSP | The data-dc-script class is evaluated with new Function (evalDcLogic) and any x-import module would be executed the same way after a fetch, which requires 'unsafe-eval' under a Content-Security-Policy. | The prototype cannot run under a strict CSP and anyone who can edit the HTML text can execute arbitrary JavaScript; this is not a pattern a storefront should carry. | Removed with the runtime in Phase 10; the theme's own JavaScript must not use eval or new Function. | MEDIUM | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| JS-07 | Runtime-generated hover styles | The only hover states on the two CTAs come from the style-hover attribute, which support.js converts at runtime into .scp0:hover and .scp1:hover rules with !important; the attribute has no meaning outside the dc-runtime. | Removing support.js silently removes both button hover states unless they are re-expressed as ordinary CSS. | Define the two button hover states (#2a2823/#f3efe6 and #e6d3a6/#0d0c0a) and the gold link hover as tokenised :hover rules in the Phase 2 design system. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| NAV-04 | Verse nav item | The Verse menu item has no destination (href="#") and no corresponding page or section exists. | A primary navigation item is a dead end and its intended target is undefined. | Decide whether Verse is a page, a blog or a homepage section (BUSINESS INFORMATION REQUIRED) and bind the menu item to it. | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| NAV-05 | Shop / Collections | Shop and Collections both point at the in-page anchor #shop (the New Drop section), so two primary menu items are indistinguishable and neither reaches a collection. | Visitors expecting an all-products page or a collection index land on a three-card grid with no way onward. | Map Shop to the all-products or designated shop collection and Collections to routes.collections_url once the collection taxonomy is decided. | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| NAV-08 | Logo | The wordmark renders at 66x50 in the nav and 47x36 in the footer, about half its relative size in the mockup, because the 500x500 PNG has large transparent padding drawn at 78px/56px. | Brand presence in the header and footer is weaker than the approved design. | Use a trimmed logo asset (see the ASSET register) with a logo-width setting in the header section so the wordmark matches the mockup's proportion; confirm whether a vector master exists (BUSINESS INFORMATION REQUIRED). | MEDIUM | P2 | PHASE 4 — HEADER & NAVIGATION |
| PERF-03 | Performance / font loading | Five Google Fonts files (152,880 B) plus 7,461 B of CSS load from a third party with a preconnect only to fonts.googleapis.com (no crossorigin) and none to fonts.gstatic.com, with display=swap on the 112 px headline face. | Each face waits for the CSS and a fresh connection to gstatic, and the Playfair 900 headline paints in Georgia first and then reflows. | Phase 12 will serve the faces through Shopify font settings or self-hosted woff2 in assets/ with preload for the two above-the-fold faces and correct preconnects; the typeface choices are settled in Phase 2 (BRAND register). Whether Google-hosted fonts may be used at all is BUSINESS INFORMATION REQUIRED (privacy policy). | MEDIUM | P2 | PHASE 12 — PERFORMANCE |
| PERF-05 | Performance / image loading attributes | None of the 12 `<img>` elements in the source carries loading, decoding, width or height, so all 15 image files download at once and the wordmark's width is unknown until its PNG arrives. | The 11 below-fold placements compete with the LCP hero for bandwidth on every load and the nav can shift horizontally when the logo loads. | Phase 12 will apply loading="lazy" and decoding="async" to below-fold images and let image_tag write intrinsic width and height everywhere; icons become inline SVG (ICON-01). | MEDIUM | P2 | PHASE 12 — PERFORMANCE |
| PROD-03 | Swatches | The nine colour swatches are inert 16px spans bound to hex literals with no colour names, no selection behaviour and no variant mapping. | They suggest colour choice without offering it and are too small to become controls as-is. | Drive swatches from product colour option values with named, focusable controls of adequate size that switch the card image to the variant image. | MEDIUM | P2 | PHASE 8 — PRODUCT & SHOPPING UX |
| PROD-05 | Product tile framing | Each product image is boxed in a 1:1 #ebe6dc tile with object-fit:cover, so the crop backgrounds read as visible squares and the non-square cap is edge-cropped with its brim touching the tile edge. | The cards depart from the mockup's floating-garment look and the cap is visually clipped. | Present images on the section background (or a consistent studio background) with object-fit:contain and padding, using properly shot product images from the asset phase. | MEDIUM | P2 | PHASE 8 — PRODUCT & SHOPPING UX |
| RESP-02 | Product grid (<=520px) | The phone rule forces one column, producing 327-382px square tiles from 235px sources and a 1,695px New Drop section whose only control sits above the grid. | Three products cost 2.1 screens of scrolling with 2.8x device-pixel upscaling and nothing to tap at the end. | In Phase 9 use a two-column grid at phone widths (about 154px tiles at 375) and place the collection CTA after the grid; pair it with responsive product images rendered through the theme's image_url: width filters and image_tag with an explicit sizes attribute, so each tile is served at its real display width instead of one fixed source (weight and format: ASSET/PERF register). | MEDIUM | P2 | PHASE 9 — MOBILE UX |
| RESP-04 | Hero and story side captions (<=900px) | The desktop overlay captions (More Than Clothing. / A Higher Purpose. and Faith Lives Different Here.) are kept as in-flow blocks after the main copy on small screens. | At 375 the phone hero appends 211px of orphaned side-column text after the 352px of main copy that follows the 320px image band (hero 970px total, Shop starts at y=1029), and the story CTA is followed by a 145px orphan caption. | In Phase 9 hide the side columns below 900px or fold one line into the main copy, and keep the story caption on the photo or drop it; hiding the hero side column recovers 211px at 375. | MEDIUM | P2 | PHASE 9 — MOBILE UX |
| RESP-07 | Hero headline line breaks | The h1 renders on three lines (WALK / BY / FAITH.) from 901 to 1920px and on one line from about 540 to 900px; the approved two-line lockup appears only below about 540px. | The brand's primary lockup is wrong on every desktop and tablet width. | In Phase 5 size the hero copy column and the h1 clamp together so WALK BY fits on line one at every desktop width, and force the break before FAITH. at tablet widths. | MEDIUM | P2 | PHASE 5 — HERO |
| RESP-10 | Hero crop on phones | At 375px object-fit:cover scales the 1672x941 landscape photo by 0.34 to 568x320 and crops 193px (34%), cutting the third model and the back-print message, while object-position:center 30% has no effect. | The phone hero shows a two-person crop that loses the group composition and the only on-garment message. | In Phase 5 art-direct the phone hero: expose a separate mobile image setting on the hero section and render a `<picture>` whose sources are built with image_url: width: … and image_tag, so the phone crop is its own theme-editor image rather than a CSS crop of the desktop file (availability of a portrait source is BUSINESS INFORMATION REQUIRED); image weight and format are in the ASSET/PERF register. | MEDIUM | P2 | PHASE 5 — HERO |
| RESP-12 | 900px breakpoint and 200% zoom | The 900px max-width query removes the primary navigation and shows the inert hamburger, and that layout is also what a 1440 desktop gets from 160% zoom (1440/1.6 = 900 CSS px) and any laptop up to 1800px gets at 200%. A 1366 laptop stays on the desktop layout at 150% (1366/1.5 = 911 CSS px) and only crosses the breakpoint at the next zoom step, 175% (781 CSS px). | Zoomed desktop users lose all navigation, and on phones the header (position:relative) scrolls away on a 5.4-screen page with no sticky header or back-to-top. | In Phase 9 make the mobile header functional at every width the query covers (menu build: NAV register) and add a sticky or re-appearing header; consider raising or lowering the breakpoint once the menu exists. | MEDIUM | P2 | PHASE 9 — MOBILE UX |
| RISK-08 | Risk: fonts | Three Google Fonts families are assumed available on Shopify, with no library check and no licence file in the project. | A family absent from Shopify's library must be self-hosted, which changes loading strategy and requires licence confirmation. | Phase 2 will verify each family in the font_picker library and confirm licences before specifying self-hosting; any self-hosted woff2 goes in the flat assets/ folder, which has no subfolders. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| RISK-09 | Risk: price glyphs | The peso sign and arrow fall back to a per-OS system face because Jost's loaded faces lack them, and the store money format has not been chosen. | Prices and CTAs will look different on Windows, macOS, iOS and Android and none will match the mockup. | Phase 2 will choose the price typeface or a symbol subset and an SVG arrow; Phase 15 will check rendering across platforms. Glyph fallback: see the BRAND register. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| RISK-11 | Risk: editor expectations | The owner has been editing by natural-language prompt in Claude Design, whereas Shopify exposes only what section schemas declare. | A settings surface that is too thin frustrates the owner; one that is too wide lets the design hierarchy be broken. | Phase 11 will agree the settings and locked values in §29.6-29.8 with the owner before implementation. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| RISK-12 | Risk: currency and markets | The prototype's currency selector swaps only the symbol, and no decision exists on selling currencies. | A store launched with ₱/$/€ without Shopify Markets would display wrong prices. | Decide the selling currencies (BUSINESS DECISION REQUIRED); if more than ₱, Phase 15 will configure and test Shopify Markets conversions. | MEDIUM | P2 | PHASE 15 — ECOMMERCE QA |
| RISK-13 | Risk: acceptance baseline | No Lighthouse, axe, screen-reader, throttled-load, cross-browser or real-device results exist for the prototype, and no QA matrix has been written. | Phases 9, 12 and 14 have no pass criteria and regressions will be argued from screenshots; a matrix owned by Phase 15 would arrive after the phases it is meant to judge. | Phase 2 will define the QA matrix (devices, browsers, throttling, tools) so that each of Phases 9, 12 and 14 has measurable acceptance before it runs; Phase 15 will execute it as ecommerce QA. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| SEO-03 | SEO / head metadata | No canonical link is declared. | Content reachable through several URLs (hash variants, the space-encoded filename, and later the myshopify versus custom domain) has no declared preferred URL. | Phase 13 will emit canonical_url on every template. | MEDIUM | P2 | PHASE 13 — SEO |
| SEO-04 | SEO / social metadata | No Open Graph or Twitter Card tags exist and no share-format image (1200x630 or similar) exists among the 44 site files. | Sharing the URL on Facebook, Messenger, Instagram DMs or X produces a card with no title, description or image for a brand whose footer is built around social channels. | Phase 13 will add a meta-tags snippet driven by page data and a theme-settings share image; the image and copy are BUSINESS INFORMATION REQUIRED. | MEDIUM | P2 | PHASE 13 — SEO |
| SEO-05 | SEO / favicon | No favicon of any kind is declared, so a normal tab will request /favicon.ico and receive a 404 (predicted; not observed in this capture). | The tab, bookmarks and mobile home screen show a generic document icon, and no icon asset exists to carry into the theme. | Phase 13 will wire the theme favicon setting (image_url width 32 plus an Apple touch icon); a square brand mark must first be sourced (section 21, BUSINESS INFORMATION REQUIRED). | MEDIUM | P2 | PHASE 13 — SEO |
| SEO-07 | SEO / structured data | No structured data (JSON-LD) is present for the organization, products or breadcrumbs. | Search engines cannot surface rich results (price, availability, brand logo, sitelinks) for the products or the brand. | Phase 13 will add a structured-data snippet emitting Organization on every page and Product plus Offer and BreadcrumbList on product and collection templates; price, currency, availability and social URLs are BUSINESS INFORMATION REQUIRED. | MEDIUM | P2 | PHASE 13 — SEO |
| SEO-09 | SEO / URL architecture | The whole store is a single URL whose nine links are hash anchors, six of them href="#", with Shop and Collections both pointing at #shop. | There are no crawlable product, collection or policy URLs, no internal-link graph and no distinct destinations for two primary navigation labels. | Phase 13 will validate the Shopify URL architecture (routes, collection.url, product.url, policy pages) once the intended destinations for Verse and Collections are supplied (BUSINESS INFORMATION REQUIRED); the placeholder hrefs themselves are in the NAV register. | MEDIUM | P2 | PHASE 13 — SEO |
| SEO-10 | SEO / indexability | Product and value content exists only as hidden template placeholders and a JS data block that React renders after loading from unpkg, so a client that does not run the script reads the raw template — product cards reading literal {{ p.name }} with broken {{ p.img }} images — while a client that runs the script but cannot reach unpkg gets a blank page, because hideRawTemplate() hides `<x-dc>` before React is even requested. | Any crawler or fetcher that does not execute JavaScript indexes raw placeholders, one that executes it but is blocked from unpkg indexes a blank page, and even Googlebot depends on the CDN to see the products. | Phase 10 will render all content server-side in Liquid, which removes the dependency by construction; the runtime itself is covered in the ARCH register. | MEDIUM | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| SHOP-05 | Locales | No locales/ directory exists; every storefront string and every future schema label is inline in the markup, and the store's language set is unknown. | The theme cannot be translated, schema labels cannot be localised, and Shopify's translation tooling has nothing to read. | Phase 10 will add locales/en.default.json and en.default.schema.json and route all strings through the t filter; launch languages are BUSINESS DECISION REQUIRED. | MEDIUM | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| SHOP-06 | Assets folder | Assets live in an images/ subfolder, the project root and uploads/, with space-containing names (images/WHITE FONT LOGO.png) and non-theme files mixed in — the mockup PNG, editor screenshots, sprites, the editor-generated .thumbnail preview, and .claude/launch.json, which is dev-server tooling added by the audit lead and not a site file; Shopify assets/ is flat, has no subfolders and must contain only theme files. | None of the current paths or names can be reproduced in a theme, and copying the folder would upload 17,185,754 B of which only 2,491,648 B is referenced by the page at all. | Phase 3 will produce a clean asset manifest: URL-safe flat names for the few true theme assets (logo SVGs, CSS, JS, optional woff2 fonts) and Shopify Files or product media for every content image; the non-theme files stay in the archived prototype. Weight, format and duplicates: see the ASSET register. | MEDIUM | P2 | PHASE 3 — ASSET PREPARATION |
| SHOP-07 | Fonts | Fonts are delivered by a Google Fonts link inside the body-level helmet element (Playfair Display 700/900, Jost 400/500/600, Kaushan Script), with no font_picker settings and no verification that the families exist in Shopify's font library. | The theme would either depend on an external font host that Shopify settings cannot control or ship families whose availability and licence for self-hosting are unconfirmed. | Phase 2 will check each family against Shopify's font_picker library and specify font_face output in theme.liquid, self-hosting subset woff2 files with flat names directly in assets/ (no fonts/ subfolder) only for families that are absent and whose licence permits it. Glyph fallback for the peso sign and arrow: see the BRAND register. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| SHOP-08 | Currency | Currency is a template prop enum (₱/$/€) concatenated onto string prices, with no Shopify mechanism (store money format, money filter, Shopify Markets) behind it. | Selecting another symbol shows the same number with a different sign, and the theme has no correct way to present prices until the store currency and markets are decided. | Phase 15 will validate prices rendered through the money filter against the store's money format and, if more than one selling currency is required, Shopify Markets; the selling currencies are BUSINESS DECISION REQUIRED. Hardcoded price data: see the DATA register. | MEDIUM | P2 | PHASE 15 — ECOMMERCE QA |
| STORY-02 | Our Story — slot composition | The image slot (left:30%, width:70%, object-fit:cover, object-position:center top) discards about 29% of the picture's height at 1440 — the hands and chest that carry the mockup's gesture — and starts the photo at 30% of the section so the subject's face lands under the copy column's right edge, with no aspect-ratio or focal-point rule for the slot. | Even after the asset swap the section will show a cropped fragment whose subject collides with the copy, and the visible crop changes unpredictably per width. | Phase 7 should define the slot's aspect ratio per breakpoint and a focal-point rule (using the Shopify image focal point) so the subject and gesture stay visible; the required master resolution and delivery strategy are in the ASSET register. | MEDIUM | P2 | PHASE 7 — OUR STORY |
| STORY-06 | Our Story — Theme Editor editability | Eyebrow, heading, paragraph, CTA label and link, side caption, image, alt and scrim are all inline copy or hard paths with no settings schema. | The brand cannot change its story, photo or CTA without a code deploy, which defeats the purpose of an Online Store 2.0 section. | Build our-story.liquid with settings for eyebrow, heading (inline_richtext, which has no line breaks — use two text settings for the two lines or rely on the STORY-05 column width for the wrap), body (richtext), CTA label and url, side caption, image_picker, image side, scrim strength, colour scheme and mobile caption visibility; the global content inventory is in the DATA register. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| UI-01 | UI — button component | The two CTAs differ in font weight (500 vs 600) for no hierarchical reason, their hover exists only through the Claude-Design style-hover attribute, the arrow is a text glyph, and no focus, active or disabled state is defined. | Buttons cannot be reproduced consistently outside the dc-runtime and give keyboard users no visible state. | Specify primary (ink fill, cream text) and accent (gold fill, ink text) buttons with default, hover, focus-visible, active and disabled states in plain CSS, an SVG arrow slot and a 48px minimum height; keep the existing hover tints as tokens. | MEDIUM | P2 | PHASE 2 — DESIGN SYSTEM |
| UI-02 | UI — product card media treatment | Each product image sits in a 1:1 box with object-fit:cover over a #ebe6dc background, so the crop's own off-white box is visible against the cream section, garments run to the box edges and the 215x190 cap is edge-cropped with its brim touching the tile edge, unlike the mockup's floated garments. | The New Drop grid looks boxed and soft rather than premium, and the card cannot be reused for products with different aspect ratios. | Specify the card with a fixed media ratio, object-fit:contain on the section cream (or transparent product masters), a two-line name clamp so prices align, and hover/link states defined with the ECOM register; resolution is in the ASSET register. | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| UX-02 | Homepage flow / Best Sellers | The Best Sellers / Product Discovery step of the intended flow does not exist; the page has four sections and goes straight from New Drop to Our Story. | The homepage exposes exactly three products with no category or best-seller entry points, limiting discovery and depth of browse. | Add a best-sellers / featured-collection section bound to a collection whose admin sort order is Best selling, or manual product blocks, reusing the product-card snippet. | MEDIUM | P2 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| UX-03 | Homepage flow / Verse | There is no Verse / Faith section although Verse is a primary nav item; the only scripture is the hero's 2 Corinthians 5:7 line. | The brand's most distinctive menu promise leads nowhere, weakening the faith-driven positioning and creating a dead end. | Add a verse section (verse text, reference, optional image) with editable settings once the verse selection, translation and attribution terms are confirmed. | MEDIUM | P2 | PHASE 7 — OUR STORY |
| UX-07 | Our Story | The nav Our Story item scrolls to the story section while the section's own Our Story CTA scrolls to the top, and neither leads to fuller story content. | Two prominent promises of a story page resolve circularly, eroding trust in the navigation. | Point the CTA at a real Our Story page once its content is supplied, and decide whether the nav item targets the page or the homepage section. | MEDIUM | P2 | PHASE 7 — OUR STORY |
| VAL-01 | Brand Values — section blocks | The four values are hard-coded objects in the data-dc-script rendered by sc-for, with no way to add, reorder, relabel or link a value. | Marketing content that will change per market or season is locked in code; the templating collision itself is in the ARCH register. | Build brand-values.liquid with value blocks (icon select from an SVG snippet set or image_picker, title, subtitle, optional link; max 6, preset 4) and section settings for columns, dividers, colour scheme and padding; the data inventory is in the DATA register. | MEDIUM | P2 | PHASE 11 — THEME EDITOR |
| VAL-04 | Brand Values — shipping claim | "Worldwide / Shipping Available" is a checkable business claim and no shipping policy, destination list or rate table has been seen in the project. | If shipping is regional the tile and the announcement bar make a false promise at launch. | Confirm the shipping scope and policy (BUSINESS INFORMATION REQUIRED) before Phase 15 sign-off and make the value's subtitle and optional link editable so it can be corrected per market. | MEDIUM | P2 | PHASE 15 — ECOMMERCE QA |
| CSS-05 | Dead rule | The first rule of the 900px query targets [data-r=pad], and no element in the markup carries data-r="pad". | The announcement bar keeps its 48px inline gutter between 521 and 900px while every other section moves to 24px, so the left edges disagree on tablets. | Give the announcement bar the same gutter token as the header when it is rebuilt as a header-group section. | LOW | P2 | PHASE 4 — HEADER & NAVIGATION |
| CSS-11 | Global link reset | a{color:inherit;text-decoration:none} removes the underline affordance from all nine links and a:hover applies the gold colour to every anchor including image-only links. | Links in running text are indistinguishable from text and the hover rule is inconsistent across link types. | Scope the reset to navigation and button-style links and give in-copy links an underline or visible affordance in base.css. | LOW | P2 | PHASE 2 — DESIGN SYSTEM |
| DATA-09 | Business facts embedded in copy | The page asserts business facts that have not been confirmed: "Worldwide Shipping" (announcement), "Worldwide / Shipping Available" (values), "Philippine streetwear brand" (story) and peso pricing. | Publishing unconfirmed shipping, market or origin claims creates customer-service and legal exposure on day one. | Confirm shipping zones, selling markets and the brand-origin statement with the owner before Phase 11 copy is finalised: BUSINESS INFORMATION REQUIRED. | LOW | P2 | PHASE 11 — THEME EDITOR |
| HTML-08 | Wrappers | Two empty spacer `<div>`s stand in for grid columns, two logo wrappers exist only to carry a dead background, and the single 1440px wrapper carries the page background and overflow:hidden for every section. | Extra DOM without meaning, and section backgrounds cannot be full-bleed above 1440px (outcome measured in the RESP register). | Place grid items with grid-column instead of spacer elements, drop the logo wrappers, and make each section full-width with its own inner max-width container. | LOW | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| HTML-11 | Alt text quality | The story image alt says "God Squad community" but the file shows a single capped model with baked headline text; the inert search/account/cart images announce as controls; the social images duplicate their link's aria-label. | Screen-reader users receive a description that contradicts the picture and control names for things that do nothing. | Rewrite alt text when the story asset is replaced, make icon images inside labelled controls alt="" (or inline SVG aria-hidden), and keep a single accessible name per control. | LOW | P2 | PHASE 14 — ACCESSIBILITY |
| INV-03 | Root folder hygiene | The project root mixes the entry page and runtime with five unreferenced Claude Design export artefacts (.thumbnail, chatgpt-image-...-evm9.png, white-font-300x300-...png, two white-font-trans-...png; 2,125,399 bytes) carrying unstable hash-suffixed names, and the one live root asset (01-hero-model-mu98p88t-7jig.webp) also has a hash suffix. | Root-level files that serve no page would be copied into a theme's assets/ by any naive migration, and hash-suffixed names cannot be referenced reliably by hand. | In Phase 3 move export artefacts to an archive folder outside the theme source and give the one live root asset a stable name under images/; byte-identical duplicates are classified in the ASSET register. | LOW | P2 | PHASE 3 — ASSET PREPARATION |
| INV-04 | Asset naming | The live logo asset is images/WHITE FONT LOGO.png (spaces, uppercase, requested as /images/WHITE%20FONT%20LOGO.png, the only referenced file with an unsafe name) and the unreferenced uploads folder uses names with spaces and commas such as "ChatGPT Image Sep 20, 2026, 10_11_00 AM.png". | Shopify asset_url and CSS url() handling of names with spaces invites double-encoding bugs and makes paths error-prone to type in Liquid. | Adopt a lowercase kebab-case naming convention in Phase 3 and rename on copy into the theme, never in place during Phase 1. | LOW | P2 | PHASE 3 — ASSET PREPARATION |
| JS-05 | Security: editor bridge and cross-window messaging | The runtime posts __dc_booted and __dc_design_mode to window.parent with target origin "*", acts on __dc_theme/__dc_probe messages from any origin without checking e.origin, exposes __dcUpdate/__dcSetProps/__dcRegistry/DCLogic on window, and stamps 137 data-dc-tpl attributes and 14 .sc-interp spans into the rendered DOM. | Editor bookkeeping and an unauthenticated global write surface ship to every visitor; exposure today is limited to theme and canvas toggling, but any same-origin script could replace the template or props at runtime. | Removed with the runtime in Phase 10; the theme should expose no global write API and no cross-window listeners. | LOW | P2 | PHASE 10 — SHOPIFY THEME CONVERSION |
| NAV-06 | Active state | The Home link's active gold underline is hard-coded inline and never changes with scroll position or page. | In a multi-template theme every page would show Home as current, misleading orientation. | Derive the active state from link.current / link.child_active on the menu object and style it from design-system tokens. | LOW | P2 | PHASE 4 — HEADER & NAVIGATION |
| A11Y-06 | CTA arrow glyph | Both CTAs contain a bare span with the arrow character and no aria-hidden. | The links are announced as View All Products rightwards arrow and Our Story rightwards arrow. | In Phase 14 mark the arrow aria-hidden or replace it with an inline SVG icon snippet (the font fallback of the glyph is in the BRAND register). | LOW | P3 | PHASE 14 — ACCESSIBILITY |
| A11Y-07 | Hamburger label | aria-label="Menu" sits on a span with no role. | ARIA prohibits naming generic elements, so the label is ignored and the control is invisible to assistive technology even before its handler exists. | In Phase 4 replace the span with a button carrying aria-expanded and aria-controls for the menu panel. | LOW | P3 | PHASE 4 — HEADER & NAVIGATION |
| ASSET-01 | Assets / duplicates | Nine md5 duplicate groups hold 11 byte-identical redundant copies totalling 6,733,692 bytes, 39% of the 17.2 MB of site files. | Three copies of the hero, three of the icon sheet and duplicated crops make it unclear which file is canonical and risk the wrong copy being uploaded to the theme. | Phase 3 will designate one canonical copy per group and move the other 11 to an archive outside the theme; nothing is deleted in Phase 1. | LOW | P3 | PHASE 3 — ASSET PREPARATION |
| ASSET-02 | Assets / icon sheets | Two unreferenced AI-generated icon sheets (icons-sprite.png 833,929 B, social-sprite.png 927,973 B) with heavy matting halos and baked-in labels sit in images/ alongside three duplicate uploads. | 1.76 MB of unusable raster sits in the production images folder, and the sheets are the source of every soft-edged icon on the page. | Phase 3 will archive one copy of each sheet for provenance and exclude them from the theme; Phase 2 replaces their cut-outs with SVG (ICON-01). | LOW | P3 | PHASE 3 — ASSET PREPARATION |
| ASSET-07 | Assets / naming and location | Production assets have URL-unsafe or generated names and stray locations: "WHITE FONT LOGO.png" (spaces and upper case, requested as WHITE%20FONT%20LOGO.png), the live story image at the project root with a hash suffix, and uploads named "ChatGPT Image Sep 20, 2026, 10_11_00 AM.png". | Such names need encoding or break in Shopify assets/ and make provenance unreadable. | Phase 3 will adopt a lower-case hyphenated naming convention (for example logo-wordmark-white.svg, hero-group.jpg) and place every web asset under one folder before theme upload. | LOW | P3 | PHASE 3 — ASSET PREPARATION |
| ASSET-08 | Assets / generated and reference files | Unreferenced generated and reference files (the editor .thumbnail, three root wordmark exports of which two are same-size different-md5 encodes, three 1920x1009 editor screenshots totalling 3,861,192 B, a pasted globe crop and the 1.87 MB mockup PNG) live next to production images with no separation. | A 17.2 MB working folder serves a 2.5 MB page, with no way to tell master from export from screenshot. | Phase 3 will split the project into masters, web assets and an archive (mockups, screenshots, README) and record which white-wordmark export is the approved one (BUSINESS INFORMATION REQUIRED). | LOW | P3 | PHASE 3 — ASSET PREPARATION |
| BRAND-02 | Brand — secondary neutrals and scrims | Three near-identical creams (#e9e4d8 paragraph, #ebe6dc tile, #f3efe6 base), the muted #bdb6a8, the olive #4b5443 swatch (data only) and seven rgba alphas of ink across 12 gradient stops plus three hairline alphas have no roles or names. | The design system cannot reproduce the page's tonal relationships and gradient recipes, so scrims and neutrals will be re-guessed per section. | Define a neutral ramp (ink, cream, body-on-ink, muted, tile) and four named scrim recipes (hero-h, hero-v, story-h, mobile-v) plus one hairline alpha; retire #ebe6dc if the product media treatment changes (UI-02). | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| BRAND-06 | Brand — spacing rhythm | Roughly two dozen distinct spacing values (out of 44 distinct px values of all kinds) are used with no scale: section paddings 12/22/26/44/48/56/170/190, 14 distinct gap values (17 listed entries) from 5 to 44px, margins 14/26/36/38. | Spacing cannot be tokenised or exposed as theme settings and every section will be re-tuned by eye during conversion. | Adopt a 4/8-based scale (4, 8, 12, 16, 24, 32, 48, 64, 96) with section padding tokens; most current values sit within one step of it, and the hero's 170/190px offsets disappear once the header leaves the hero section. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| BRAND-08 | Brand — tagline system | Four taglines are used with inconsistent punctuation and repetition: "Different People Same Purpose" (hero, no punctuation) vs "Different People. Same Purpose." (footer), and "More Than Clothing." appears both as the hero script and as the Faith Driven value subtitle. | The brand voice reads as unedited and the first value tile restates the hero instead of adding a proof point. | Produce a brand copy deck that fixes the canonical taglines, punctuation and placement (BUSINESS INFORMATION REQUIRED), then apply it as section settings in Phase 11. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| CSS-06 | Dead and redundant declarations | background:#0230 (alpha 0) on both logo wrappers, flex-wrap:wrap on a grid container, an object-position value duplicated between inline and the 900px query, and a [data-r=hero-img] rule split in two. | No visual effect today, but they signal an accreted style block and would be copied into the theme by anyone porting mechanically. | Drop them during transcription and lint the new stylesheets for no-op declarations. | LOW | P3 | PHASE 10 — SHOPIFY THEME CONVERSION |
| CSS-10 | Browser support of modern CSS | text-wrap:balance and overflow-wrap:anywhere are used on the headings alongside aspect-ratio, inset, max() and clamp(), with no confirmed support matrix. | Older Safari versions render the h1 without balancing, changing the line breaks the design depends on. | Confirm the target browser matrix (BUSINESS DECISION REQUIRED) and keep these idioms with progressive-enhancement fallbacks in the design system. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| ECOM-07 | Recommendations and related products | No product recommendations or related products exist. | Cross-sell and basket depth opportunities are absent. | Add a recommendations section on the product page using the Product Recommendations API (related intent; complementary if configured) after the product page exists. | LOW | P3 | PHASE 8 — PRODUCT & SHOPPING UX |
| ECOM-08 | Wishlist | No wishlist exists and Shopify has no native wishlist. | Visitors cannot save items for later; relevance depends on the launch catalogue size (BUSINESS INFORMATION REQUIRED). | Treat as optional; decide after launch whether an app or theme-level wishlist is wanted (BUSINESS DECISION REQUIRED; no apps in Phase 1). | LOW | P3 | PHASE 16 — FINAL POLISH |
| FOOT-04 | Footer trust and localization | No payment icons and no country/currency selector exist. | Checkout trust cues and the market/currency choice implied by the ₱/$/€ prop are not surfaced. | Add payment icons from shop.enabled_payment_types and a localization form if Markets are enabled, after the payment and market decisions are made. | LOW | P3 | PHASE 15 — ECOMMERCE QA |
| HERO-06 | Hero — top edge seam | The announcement bar is a solid strip outside the hero section and the photo begins directly beneath it with sky and tower tops, producing a hard horizontal edge at 1024 and 1440 and under the nav strip below 900px, while the mockup's top edge is continuously dark. | The hero looks pasted in under the bar rather than bleeding behind the header. | Phase 5 should either extend the photo behind the header group with a solid-to-transparent top band, or start the hero with an ink band that the scrim dissolves into. | LOW | P3 | PHASE 5 — HERO |
| HERO-07 | Hero — right column collision | The "More Than Clothing." script and "A HIGHER PURPOSE." caption are placed by a .7fr column and 190px padding directly over the right model's back-print lettering at 1024-1440. | Two lines of copy compete with two lines of printed garment text and both lose legibility. | Reposition the side column (or the crop's horizontal focal point) so the caption sits on a quiet area of the photo, or drop the side column at widths where it collides. | LOW | P3 | PHASE 5 — HERO |
| HERO-08 | Hero — mobile art direction | There is no portrait source for phones: the 375x320 band is filled from the 16:9 image by height, cropping 96px from each side so the third model and the back-print message are cut and object-position has no effect. | The group composition the hero relies on becomes a two-person crop on the device most visitors use. | Phase 5 should specify a portrait or square art-directed crop delivered through `<picture>`/srcset for widths under 768px; the master, format and weight are in the ASSET/PERF register. | LOW | P3 | PHASE 5 — HERO |
| HTML-12 | Text semantics | Only one `<p>` exists (the story paragraph); every other piece of running text — eyebrows, taglines, prices, footer lines — is a `<div>` or `<span>`. | Text has no paragraph semantics for assistive technology and copy cannot be targeted by a sensible base stylesheet. | Use `<p>` for running text and small `<span>`/`<small>` only for inline fragments when the sections are transcribed. | LOW | P3 | PHASE 10 — SHOPIFY THEME CONVERSION |
| ICON-02 | Icons / cart icon artefact | icon-cart.png retains a sliver of the sprite sheet's gold "0" badge along its right edge while the page overlays its own CSS badge. | At larger sizes or on light backgrounds a stray gold arc appears beside the bag, and the badge is effectively drawn twice. | Phase 2 will replace the file with the SVG cart glyph and a Liquid cart.item_count badge. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| ICON-03 | Icons / social icons | The Facebook and Instagram icons are two-tone circled badges (gold ring, light disc, gold glyph) cut from the social sheet, unlike the mockup's plain glyphs, and the mockup's TikTok and YouTube have no counterpart. | The badges cannot take the theme's link hover colour, will clash with any light footer background, and the set of networks is undecided. | Phase 2 will adopt official monochrome SVG glyphs for the networks the business confirms (BUSINESS INFORMATION REQUIRED); the circled-versus-plain style decision belongs to the BRAND register. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| ICON-05 | Icons / geometry consistency | The icon set has four canvas sizes (110x110, 130x110, 150x110, 130x130), two stroke weights (thin cream nav set, heavier gold feature set) and rendered widths of 52/60/44/52 px at the same 44 px height. | The value row reads optically uneven and the nav and feature icons do not look like one family. | Phase 2 will draw all icons on one 24 px grid with one stroke weight and one optical size. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| INV-02 | Entry file naming | The entry page was renamed from "God Squad Website.dc.html" to "God Squad Website.html" on 2026-09-20 15:34 while the Phase 1 spec, the runtime's naming convention (rootNameForDocument tests /\.dc\.html?$/i and ensureFetched builds "`<name>`.dc.html") and the original export zip still use the .dc.html name. | The runtime is indifferent to the suffix: the root is marked fetched at boot (support.js line 155) and dcNameFromPath strips either suffix (line 82); the only place the .dc.html convention survives is ensureFetched's sibling URL (line 1646), which this page never exercises. The remaining cost is documentary: the spec, the export zip and the runtime's convention all say .dc.html while the file does not. | Record the rename in the Phase 1 baseline notes and treat "God Squad Website.html" as the canonical prototype name in every later phase; do not rename it again. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| INV-06 | Phase 1 tooling inside the project root | .claude/launch.json (228 B, a python http.server dev-server configuration) was created inside the project root at 13:23 on 2026-09-20 by the audit lead so the page could be served over HTTP, although the spec states that the website must not be modified during Phase 1. | The mandated closing statement "NO PROJECT FILES WERE MODIFIED" is only accurate if this addition is disclosed or reverted, and a naive copy of the folder would carry a non-site file into the theme source. | Disclose the file in the final audit checklist and have the owner remove it (or move it outside the project) after the audit; it must never be copied into the theme. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| JS-03 | Boot double fetch | boot() calls fetch(location.href) and recompiles and re-renders the whole template from the raw text whenever window.__resources is absent, so the HTML document is requested twice and React renders twice on every load (the fetch fails silently on file://). | One wasted document request and a duplicate render per page view, and evidence that the runtime is built for editor streaming rather than a static page. | No separate action; disappears with the runtime removal in Phase 10. | LOW | P3 | PHASE 10 — SHOPIFY THEME CONVERSION |
| JS-06 | Parser-time side effects of the hidden template | Because the raw template is real DOM hidden by display:none rather than a `<template>`, the browser requests "{{ p.img }}" and "{{ v.icon }}" literally (two 404s per load) and starts downloading all 15 images before the runtime replaces `<x-dc>`. | Two failed requests and two console errors on every page view; visually harmless. | No fix in the prototype; the artefact disappears once the markup is ported to Liquid in Phase 10. | LOW | P3 | PHASE 10 — SHOPIFY THEME CONVERSION |
| NAV-07 | Hover / focus feedback | Nav hover relies solely on the global a:hover gold (no visible change for the already-gold Home), the utility icons have no hover or focus state, and the social icon links have none at all because their colour is baked into PNGs. | Interactive feedback is inconsistent across the header and footer and absent on every icon control. | Define hover and focus states for nav links, utility icons and social links as ordinary CSS on design-system tokens with SVG icons that can be recoloured; re-expression of the CTAs' style-hover as CSS: see the CSS register. | LOW | P3 | PHASE 4 — HEADER & NAVIGATION |
| PERF-04 | Performance / font payload | Kaushan Script (34,748 B) is downloaded for a single three-word phrase and Playfair Display 700 is requested but never used. | 23% of the font payload serves one decorative line, and the unused weight adds CSS noise (no file download). | Phase 2 will decide whether "More Than Clothing." becomes a subset font, an SVG lockup or stays editable text with the full face, and will drop the 700 weight from the request. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| PERF-06 | Performance / measurement | No performance measurement exists: Lighthouse was not run, LCP did not report and CLS read 0 only on a warm localhost load. | The cost of the 2 MB hero and the runtime chain cannot be quantified, so there is no baseline to prove improvement against. | Phase 12 will record a throttled Lighthouse baseline (Slow 4G, 4x CPU) for the prototype and set a Core Web Vitals budget the theme must meet. | LOW | P3 | PHASE 12 — PERFORMANCE |
| PROD-06 | Card hover / focus | Product cards have no hover or focus feedback and no secondary image. | Cards do not read as interactive and give no confirmation on pointer or keyboard focus. | Add hover/focus states (image swap to product.images[1], subtle lift or underline) in the product-card snippet. | LOW | P3 | PHASE 8 — PRODUCT & SHOPPING UX |
| PROD-07 | Card hierarchy | Cards carry no merchandising signals: no New / Sold out badge, no size information, no variant count and no from-price. | Shoppers cannot tell availability, size range or price range from the grid. | Add badge, availability and from-price slots to the product-card snippet, driven by product.available, product.price_varies and product tags or metafields. | LOW | P3 | PHASE 8 — PRODUCT & SHOPPING UX |
| RESP-03 | Product grid (521-900px and 200% zoom) | The two-column tablet grid leaves the Utility Cap alone on a second row. | The three-product set reads as an unfinished grid on tablets and on zoomed laptops. | In Phase 6 make the tablet column count depend on the collection's product count or use a three-column grid with smaller tiles from about 600px. | LOW | P3 | PHASE 6 — COLLECTIONS & BEST SELLERS |
| RESP-05 | Values strip (<=900px) | Phones get a 698px single-column stack for four short labels, and at 521-900px every tile keeps border-right so a stray 1px rule paints at the viewport edge and the last row's bottom border doubles with the section's own border. | 86% of a phone screen is spent on four labels and the tablet layout shows visible rendering artefacts. | In Phase 9 keep the values two-up on phones and compute tile borders per column and row (for example with gap plus background instead of per-tile borders). | LOW | P3 | PHASE 9 — MOBILE UX |
| RESP-06 | Footer (521-900px) | The footer is forced into a column at <=900px although at 768px the two groups (230px + 271px) fit on one row in a 705px content box. | Tablets get a 164px stacked footer that loses the single-band composition of the mockup for no layout reason. | In Phase 9 move the footer stacking breakpoint down to roughly 560px and verify the row with the final footer content. | LOW | P3 | PHASE 9 — MOBILE UX |
| RESP-08 | 901-1100px desktop band | There is no tier between 901 and 1440px, so the fluid three-column grid is squeezed to ~230-250px: at 920 the eyebrow, the product names and the View All Products CTA all wrap, and at 1024 "Signature Oversized Tee" wraps to two lines so the tee's price drops a line below the other two. | Common laptop widths (1024, and 1366 at 125% scaling = 1093 CSS px) show misaligned prices and wrapped labels. | In Phase 2 add a tablet-landscape tier (about 901-1100px) with narrower gaps, a smaller label size and a two-column hero. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| RESP-09 | Hero image band height | The mobile hero band is height:62vw with min-height 320px and no viewport-height cap. | On an 812x375 landscape phone the band is 503px (1.34 screens) and the headline starts at y=689, nearly two screens down. | In Phase 5 cap the band with a vh-based max-height or clamp() on both the image and the fade. | LOW | P3 | PHASE 5 — HERO |
| RESP-11 | Phone typography | Apart from the four heading clamps there is no phone type scale: secondary text is 11-13px tracked uppercase, prices are 14px, the paragraph 15px and the cart badge 9px, all fixed px inherited from the desktop mockup. | Labels are small and light on a 375px screen and nothing responds to user font-size preferences (browser zoom still works). | In Phase 2 define a phone scale (a 16px body floor, 12-13px minimum for tracked caps, badge at least 11px) alongside the desktop scale. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| RESP-13 | Laptop fold | On 1280x720 and 1366x768 the hero fills the first screen and no product is visible without scrolling. | The most common laptop viewports give no commerce signal above the fold. | In Phase 5 cap the desktop hero height (for example min(100vh - header, 720px)) or surface a product cue above the fold. | LOW | P3 | PHASE 5 — HERO |
| RESP-14 | Widths above 1440px | Everything sits in a max-width:1440px box with section backgrounds on the inner sections, so the cream New Drop band, the hero photo and the value borders stop at 1440 with dark gutters either side. | On 1920px and wider screens the page reads as a boxed layout rather than the full-bleed composition of the mockup. | In Phase 2 give each section a full-width background and constrain only an inner container; the wrapper's overflow:hidden should not be carried over, since it currently masks any horizontal overflow from measurement (17.11). | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| SEO-06 | SEO / crawl control | There is no robots meta, robots.txt or sitemap.xml in the project. | Nothing tells crawlers what to index or lists URLs; immaterial for a one-file prototype but a required foundation for the store. | Phase 13 will rely on Shopify's native /robots.txt and /sitemap.xml and add robots.txt.liquid only if custom rules are needed. | LOW | P3 | PHASE 13 — SEO |
| SEO-08 | SEO / image alt text | Alt text is present on all 12 images, but the Our Story alt ("God Squad community") describes a subject the file does not show and product alts are bare names with no brand or product-type context. | Image search and assistive descriptions misrepresent the story image and add nothing for the products. | Phase 13 will define alt-text rules (brand, product and colour for product media; accurate scene description for editorial images) and the copy will be entered in Shopify image.alt fields (BUSINESS INFORMATION REQUIRED). | LOW | P3 | PHASE 13 — SEO |
| SEO-11 | SEO / content depth | The homepage carries roughly 120 words of indexable copy, one 25-word paragraph that is the only mention of the brand name and category in running text, and no product descriptions. | There is almost no textual signal for the brand, its category ("Philippine streetwear", faith) or its products beyond three names and prices. | Phase 13 will define the copy the index, collection and product templates need (product descriptions, an about paragraph, footer text); the copy is BUSINESS INFORMATION REQUIRED. | LOW | P3 | PHASE 13 — SEO |
| STORY-03 | Our Story — CTA | The gold CTA repeats the eyebrow word-for-word ("Our Story" → "Our Story"), points to "#", and no About/Our Story page or long-form story copy has been seen in the project. | The section's only action has no destination and no promise, so the secondary conversion path is undefined. | Confirm whether an Our Story page exists and its copy (BUSINESS INFORMATION REQUIRED), then set the CTA label and url as section settings; the placeholder href is in the NAV register. | LOW | P3 | PHASE 7 — OUR STORY |
| STORY-04 | Our Story — side caption on small screens | Below 900px the "Faith Lives Different Here." caption and its rule stack as a 145px orphan block after the CTA instead of overlaying the photo. | An unrelated four-line tagline follows the button on tablets and phones and lengthens the section with no purpose. | Phase 7 should decide the caption's mobile behaviour (hide, or fold into the copy above the CTA) and expose it as a show/hide setting; the layout outcome is in the RESP register. | LOW | P3 | PHASE 7 — OUR STORY |
| STORY-05 | Our Story — heading container | "Real People. Bigger Purpose." wraps to three lines at 1440 and four at 1024 (mockup: two) because the copy column is .9fr minus 96px padding, about 350px at 1440 and 220px at 1024. | The heading loses its two-line rhythm and pushes the paragraph and CTA down beside the photo on laptops. | Give the copy column a minimum width tied to the heading clamp and keep the explicit break after "Real People." as the only break. | LOW | P3 | PHASE 7 — OUR STORY |
| UI-03 | UI — header utility controls | Search, account, cart and the hamburger are 22-24px raster icons with no hover, focus or active state, and the cart badge is 9px text in a 14px circle. | The header's controls give no feedback and the badge is the least legible text on the site; keyboard reachability and inertness are separate issues in the A11Y and NAV registers. | Define an icon-button component with a 44px hit area, gold hover, focus ring and pressed state, and a badge spec of at least 16px diameter and 10px text. | LOW | P3 | PHASE 4 — HEADER & NAVIGATION |
| UI-04 | UI — footer social icons | The footer shows two circled Facebook and Instagram icons where the mockup shows four plain glyphs (Instagram, Facebook, TikTok, YouTube); the reduction to two was a deliberate user edit but the circled style is not. | The footer icon style disagrees with the rest of the icon set and the channel list is undecided. | Decide the social channel set (BUSINESS INFORMATION REQUIRED) and render them with the single SVG icon system in the mockup's plain-glyph style unless the circled style is explicitly approved. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| UI-05 | UI — rules and dividers | The short horizontal rule is drawn five times with four widths (36px gold, 80px cream, 40px ink, 40px cream) and four margin pairs, and hairlines use three alphas (.08, .1, .2). | A single decorative device looks accidental across sections and cannot be built once. | Specify one rule component with two widths (40px, 80px), colour from the current scheme, fixed margins, plus one hairline token for borders and dividers. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| UX-04 | Homepage flow / Social | There is no Social / Community section; the only social presence is two footer icons linking to #. | The Community value tile is unsupported by any community content and no social proof exists on the page. | Add a social-gallery section with image blocks and a handle setting once profile URLs and image sources are confirmed; feed apps are a later decision. | LOW | P3 | PHASE 16 — FINAL POLISH |
| UX-05 | Announcement bar | The announcement bar is a static, unlinked div whose Worldwide Shipping label is a commercial promise with no policy, destinations or rates behind it. | Visitors receive a shipping claim they cannot verify and have no path to shipping information. | Convert to an announcement-bar section with text and link blocks, and link the shipping message to the shipping policy once it exists; confirm the claim with the business first. | LOW | P3 | PHASE 4 — HEADER & NAVIGATION |
| UX-06 | Brand Values | The four value tiles link nowhere, Worldwide / Shipping Available duplicates the announcement claim, and Community is asserted without community content. | Reassurance claims cannot be checked and the strip is a dead end rather than a route to policies or content. | Rebuild as section blocks with optional links (shipping policy, quality/size guide, community page) and keep the four current values as defaults. | LOW | P3 | PHASE 11 — THEME EDITOR |
| VAL-02 | Brand Values — divider logic | Every tile carries border-right including the last, a border-bottom is added under 900px and the right border is removed only under 520px, so the divider logic lives on tiles rather than on the grid. | At 521-900px the second column paints a 1px rule on the viewport edge and the last row's border doubles with the section's own bottom border. | Specify grid-level dividers (gap with :nth-child rules or a hairline background) in the value-tile component so dividers are correct at any column count; the per-width outcome is in the RESP register. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |
| VAL-03 | Brand Values — icon optical size | The four value icons share a 44px height but render at 44, 60, 52 and 52 px wide (globe, community, crown, diamond), and their gold is baked into 33-40 KB PNGs. | The row does not sit on one optical size and the icons cannot follow a colour scheme, hover or light-background variant. | Redraw the four as SVGs on a common 48px optical box with one stroke weight, using currentColor, as part of the icon system (BRAND-07); format and weight are in the ASSET register. | LOW | P3 | PHASE 2 — DESIGN SYSTEM |

## 29. Future Shopify Architecture

### 29.1 Recommended tree

Recommendation only; nothing is to be created in Phase 1. Every entry is justified by a block in the prototype, by the spec's section list (spec §24), or by a route Shopify serves regardless of design.

```
god-squad-theme/
  assets/                           flat: Shopify assets/ has no subfolders (§24.2 row 12)
    base.css                        tokens as custom properties, reset, type scale, buttons, grid
    section-header.css              one stylesheet per section, loaded with stylesheet_tag
    section-hero.css
    section-featured-collection.css
    section-our-story.css
    section-brand-values.css
    section-footer.css
    component-product-card.css
    component-cart-drawer.css
    theme.js                        menu drawer, details/summary helpers, focus trap
    cart.js                         AJAX add, cart drawer, item count
    predictive-search.js            OPTIONAL
    logo-white.svg, logo-black.svg  derived from OG LOGO.psd (BUSINESS INFORMATION REQUIRED: vector source)
    jost-400.woff2, jost-500.woff2, jost-600.woff2,
    kaushan-script-400.woff2, playfair-display-900.woff2
                                    flat names, no fonts/ subfolder; only for families absent
                                    from Shopify's font library (SHOP-07). Playfair Display 700
                                    is requested by the prototype but unused (C12) and is not shipped.
  config/
    settings_schema.json
    settings_data.json
  layout/
    theme.liquid
    password.liquid               OPTIONAL
  locales/
    en.default.json
    en.default.schema.json
  sections/
    header-group.json, footer-group.json
    announcement-bar.liquid, header.liquid, footer.liquid
    hero.liquid, featured-collection.liquid, our-story.liquid, brand-values.liquid
    verse.liquid, social-gallery.liquid            ADD LATER
    main-product.liquid, product-recommendations.liquid (OPTIONAL)
    main-collection.liquid, main-list-collections.liquid
    main-cart.liquid, main-search.liquid, main-page.liquid, main-404.liquid
    main-password.liquid (OPTIONAL), rich-text.liquid (OPTIONAL), newsletter.liquid (ADD LATER)
    main-login.liquid, main-register.liquid, main-account.liquid, main-order.liquid,
    main-addresses.liquid, main-reset-password.liquid, main-activate-account.liquid
                                                    BUSINESS DECISION REQUIRED (accounts)
  snippets/
    product-card.liquid, price.liquid, swatch.liquid, image.liquid, section-heading.liquid
    icon-search.liquid, icon-account.liquid, icon-cart.liquid, icon-menu.liquid,
    icon-close.liquid, icon-arrow.liquid, icon-globe.liquid, icon-crown.liquid,
    icon-community.liquid, icon-diamond.liquid, icon-facebook.liquid, icon-instagram.liquid,
    icon-tiktok.liquid, icon-youtube.liquid       last two only if URLs are supplied
    social-links.liquid, logo.liquid, meta-tags.liquid, css-variables.liquid, cart-drawer.liquid
  templates/
    index.json, product.json, collection.json, list-collections.json, cart.json,
    search.json, page.json, page.our-story.json, 404.json
    password.json (OPTIONAL), gift_card.liquid (BUSINESS DECISION REQUIRED)
    customers/login.json, register.json, account.json, order.json, addresses.json,
    reset_password.json, activate_account.json      BUSINESS DECISION REQUIRED
    blog.json, article.json                        OPTIONAL (no blog content seen)
```

Content images (hero, story, social gallery) are not theme assets: they are chosen through `image_picker` settings and served from Shopify Files so `image_url` can resize them per width; product images come from product media. Only the logo SVGs, CSS, JS and self-hosted fonts belong in `assets/`, all with flat, URL-safe names. Nothing from `images/`, `uploads/` or the project root is copied across (RISK-04); the non-theme files — mockup PNG, editor screenshots, sprites, the editor-generated `.thumbnail` preview, and `.claude/launch.json`, which is dev-server tooling added by the audit lead and not a site file — stay in the archived prototype (SHOP-06).

### 29.2 Layout and section groups

`layout/theme.liquid` carries `<html lang="{{ request.locale.iso_code }}">`, the `meta-tags` snippet (title, description, canonical, Open Graph, favicon: requirements in the SEO register), the `css-variables` snippet that turns settings into custom properties, `font_face` output for the chosen fonts with `preconnect` to the font host, `content_for_header`, `{% sections 'header-group' %}`, `<main id="MainContent">{{ content_for_layout }}</main>`, `{% sections 'footer-group' %}` and the cart drawer. This alone resolves C7 (no lang, header, main).

`sections/header-group.json` (type `header`) holds `announcement-bar` then `header`; `sections/footer-group.json` (type `footer`) holds `footer` and, later, `newsletter`. Both sections declare `enabled_on: { groups: ["header"] }` / `["footer"]`. Making the header its own section requires the hero to stop reserving 170 px / 190 px of top padding for an absolutely positioned nav (lines 82, 90; SHOP-04); the recommended pattern is a header section with a `transparent_over_hero` setting that, when on, overlays the next section via a small CSS hook and a solid top band, and when off simply stacks.

The band is not cosmetic. Nav-link contrast over the hero sky measures 2.4-2.9:1 at 1024 and 1440 for Collections, Our Story and Verse when the fade's alpha is composited over sampled photo luminance (ADD-1), and 4.6-5.7:1 on the median but 2.4-2.5:1 over the brightest 2% when measured from the render's own pixels (evidence-render.md); at 1024 the gold Home link also drops to ~3.5:1. WCAG AA requires 4.5:1 at this size, so whichever basis is used the transparent treatment cannot be reproduced as-is: the band must be strong enough to pass on the brightest sample, not the median (RISK-14).

### 29.3 Sections

| Section | Purpose | Source in prototype | Classification |
|---|---|---|---|
| announcement-bar | Two-message strip with optional globe icon | lines 58-61 | REBUILD |
| header | Logo, menu, hamburger drawer, search, account, cart with live count | lines 68-80 | REBUILD |
| hero | Full-bleed image with fades, eyebrow, split-colour h1, verse, subline, caption blocks | lines 64-95 | REBUILD |
| featured-collection | Eyebrow, heading, subheading, button plus N product cards from a collection; presets New Drop and Best Sellers | lines 98-122 | REBUILD |
| best-sellers | Listed by spec §24; recommended as a second preset of featured-collection unless its layout differs (e.g. a mobile scroller, RESPONSIVE-4). Whether a Best Sellers row launches is BUSINESS DECISION REQUIRED | none | ADD LATER |
| our-story | Image with fade, eyebrow, heading, paragraph, CTA, side caption | lines 125-139 | REBUILD |
| brand-values | 1-6 icon tiles as blocks | lines 142-150 | REBUILD |
| verse | Verse and reference; content BUSINESS INFORMATION REQUIRED (only a nav label exists, line 72) | none | ADD LATER |
| social-gallery | Image grid or feed; content source BUSINESS DECISION REQUIRED | none | ADD LATER |
| footer | Logo, tagline, social links, secondary tagline (lines 153-166). Link-list blocks, a legal/copyright line and payment icons do **not** exist in the prototype or the mockup (ADD-7) and are additions, not transpositions | lines 153-166 | REBUILD (existing parts); link lists, legal line and payment icons ADD LATER + BUSINESS INFORMATION REQUIRED |
| main-product, main-collection, main-list-collections, main-cart, main-search, main-page, main-404 | Route templates Shopify serves | none | ADD LATER (REQUIRED, see SHOP-09 and the ECOM register) |
| product-recommendations, rich-text, newsletter, main-password | Supporting | none | OPTIONAL / ADD LATER |
| customers/* mains | Account routes | none | BUSINESS DECISION REQUIRED |

### 29.4 Snippets

| Snippet | Replaces | Notes |
|---|---|---|
| product-card | inline card, lines 108-119 | `render 'product-card', product: product, show_swatches: ...`; image via `image` snippet with `widths` and `sizes`; title as a heading element linking to `product.url` (C6; ADD-8: product names are plain divs today) |
| price | `{{ p.price }}`, line 113 | `product.price \| money`, compare-at handling, optional ISO code |
| swatch | lines 114-118 | colour dots from the product's colour option; hex from a variant or option metafield; accessible name (TECHNICAL-5: see the A11Y register) |
| image | every `<img>` | `image_url` + `image_tag` with `widths`, `sizes`, `loading`, `width`/`height` (C10) |
| section-heading | eyebrow + heading + rule pattern, lines 100-103 and 129-130 | one implementation for both light and dark schemes |
| icon-* | nine RGBA PNGs, 308,521 B (TECHNICAL-6) | inline SVG using `currentColor`; conversion owned by the ASSET/ICON work |
| social-links | lines 159-162 | renders only the networks with a URL in settings; both current links are `href="#"`, so every URL is BUSINESS INFORMATION REQUIRED |
| logo | lines 69, 155 | settings image or SVG asset, sized by height per context (78 px nav, 56 px footer) |
| meta-tags | nothing today (ADD-6: no favicon, meta description, canonical or Open Graph/Twitter tags) | see the SEO register |
| css-variables | inline literals | writes `--color-bg`, `--color-fg`, `--color-accent`, `--font-heading` etc. from settings |
| cart-drawer | nothing | rendered from the layout; see the ECOM register |

### 29.5 Templates

| Template | Sections (in order) | Status |
|---|---|---|
| index.json | hero, featured-collection (New Drop preset), our-story, brand-values, [featured-collection Best Sellers preset], [verse], [social-gallery] | REBUILD; bracketed items ADD LATER / BUSINESS DECISION REQUIRED |
| product.json | main-product (blocks: title, price, variant picker with swatches, quantity, buy buttons, description, collapsible rows for size guide and shipping), product-recommendations | ADD LATER; row content BUSINESS INFORMATION REQUIRED |
| collection.json | main-collection (banner + product grid; filtering and sorting OPTIONAL) | ADD LATER |
| list-collections.json | main-list-collections | ADD LATER |
| cart.json | main-cart | ADD LATER |
| search.json | main-search | ADD LATER |
| page.json | main-page | ADD LATER |
| page.our-story.json | our-story, rich-text, brand-values | ADD LATER; narrative BUSINESS INFORMATION REQUIRED |
| 404.json | main-404 | ADD LATER |
| password.json | main-password | OPTIONAL |
| customers/*.json | respective mains | BUSINESS DECISION REQUIRED |
| gift_card.liquid | static | BUSINESS DECISION REQUIRED |
| blog.json, article.json | main-blog, main-article | OPTIONAL |

That is one designed page and at least nine undesigned storefront templates (product, collection, list-collections, cart, search, page, page.our-story, 404, password), rising to about twenty once the seven customer templates, the gift card, blog and article are counted — the figure RISK-06 and SHOP-09 are scoped against.

Shopify serves an error page for a storefront route whose template is missing, so the full storefront set must exist even where the design is minimal. Two qualifications: `templates/customers/*` are used only if classic customer accounts are chosen — with new customer accounts the pages are Shopify-hosted and the theme's customer templates are never rendered (BUSINESS DECISION REQUIRED, §24.2 row 22) — and `password.json` / `gift_card.liquid` apply only when the password page and gift cards are enabled.

### 29.6 settings_schema.json areas

| Area | Settings (defaults from the prototype) | Evidence |
|---|---|---|
| theme_info | name, version, author, documentation | required first entry |
| Colours | `color_background` #0d0c0a, `color_text` #f3efe6, `color_accent` #d8c08a, `color_light_background` #f3efe6, `color_light_text` #0d0c0a, `color_muted` #bdb6a8, `color_tile` #ebe6dc, `border_opacity` range (borders are rgba(255,255,255,.1) today, which colour settings cannot express) | css-html-stats.txt colours; lines 41-42, 142 |
| Typography | `type_heading_font` (Playfair Display 900), `type_body_font` (Jost), `type_accent_font` (Kaushan Script, or an asset fallback if absent from the library), `heading_scale` range, `body_scale` range; tracking stays static | evidence-render.md fonts; line 84 |
| Layout | `page_width` (1440), `full_bleed` checkbox (TECHNICAL-8 gutters above 1440), gutter sizes 48/24/16 as a select or static | line 55; measurements.md 1920 |
| Logo and favicon | `logo`, `logo_height_desktop` (78), `logo_height_mobile` (56), `favicon` (none exists today: ADD-6). Height, not width: the wordmark is sized by `height` with `width:auto` in both places, so a width setting would not reproduce it | lines 69 (`height:78px;width:auto`), 155 (`height:56px;width:auto`); FIDELITY-4 |
| Announcement bar | global style only: `announcement_background`, `announcement_text_color`, `announcement_border`; messages live in the section | line 58 |
| Product cards | `card_image_ratio` (square / adapt), `card_image_fit` (cover / contain: FIDELITY-3), `card_show_swatches`, `card_show_vendor` | lines 109-118 |
| Cart | `cart_type` (drawer / page), `show_cart_count` | line 78 |
| Social | `social_facebook_link`, `social_instagram_link`, `social_tiktok_link`, `social_youtube_link` (all BUSINESS INFORMATION REQUIRED; both current links are `href="#"`) | lines 160-161; C14 |
| Currency | `currency_code_enabled` checkbox only; the currency itself and its format are store settings and Shopify Markets, not theme settings (SHOP-08) | line 169 |

### 29.7 Section and block schemas per homepage section

| Section | Settings | Blocks (type: fields, limit) | Presets |
|---|---|---|---|
| announcement-bar | `show_icon`, `icon` (globe / none), `text_alignment` | `announcement`: text, link; max 3 (default two: 'Good People. Higher Purpose.', 'Worldwide Shipping') | Announcement bar |
| header | `logo` (falls back to global), `logo_height_desktop` (78), `logo_height_mobile` (56), `menu` (link_list, default main-menu), `show_search`, `show_account`, `sticky` (none / always / on scroll up: RESPONSIVE-10), `transparent_over_hero`, `mobile_menu_style` (drawer) | none (menu comes from Navigation) | Header |
| hero | `image`, `image_mobile` (RESPONSIVE-8), `image_position`, `overlay_strength` range, `min_height` range, `eyebrow` ('Streetwear with a Purpose'), `heading` ('Walk By'), `heading_accent` ('Faith.'), `verse` ('2 Corinthians 5:7'), `subline` richtext, `heading_size` range (FIDELITY-2) | `caption`: style (script / caps), text; max 2 (defaults 'More Than Clothing.' and 'A Higher Purpose.'); `button`: label, link; max 1, OPTIONAL | Hero |
| featured-collection | `collection`, `products_to_show` (3-12, default 3), `columns_desktop` (3), `columns_mobile` (1 / 2), `eyebrow` ('New Drop /'), `heading` ('The Faithful'), `subheading`, `button_label` ('View All Products'), `button_link` (defaults to `collection.url`), `color_scheme` (light / dark), `show_swatches` | none; products come from the collection | New Drop; Best Sellers |
| our-story | `image` (≥2,000 px), `image_mobile`, `image_position`, `overlay_strength`, `eyebrow`, `heading` ('Real People. Bigger Purpose.'), `text` richtext, `button_label` ('Our Story'), `button_link` (page), `side_caption` ('Faith Lives Different Here.') | none | Our Story |
| brand-values | `columns_desktop` (4), `columns_mobile` (1 / 2), `show_dividers`, `color_scheme` | `value`: icon (crown / community / globe / diamond / custom), custom_icon image, title, subtitle; max 6, default 4 with the prototype's four | Brand values |
| verse | `verse_text`, `reference`, `background_image`, `alignment` | none | ADD LATER |
| social-gallery | `heading`, `handle`, `columns` | `image`: image, link; max 8 | ADD LATER |
| footer | `show_logo`, `tagline` ('Different People. Same Purpose.'), `secondary_tagline` ('A Brighter Tomorrow'), `show_social`, `show_policy_links`, `show_copyright`, `copyright_text` (BUSINESS INFORMATION REQUIRED), `show_payment_icons` | `link_list`: heading, menu; max 4 — no footer link groups exist in the prototype (lines 153-166) or in the mockup (ADD-7), so both the group headings and their contents are BUSINESS INFORMATION REQUIRED and the blocks ship empty until the owner supplies them; `text`: richtext; `newsletter`: ADD LATER | Footer |

Every block wrapper carries `{{ block.shopify_attributes }}` and every section scopes its CSS with `#shopify-section-{{ section.id }}` so the Theme Editor can select and reorder them.

### 29.8 What stays static

Not every value should be a setting; the brand reads as premium because the composition is tight. Recommended to stay in CSS: the section grid ratios (lines 64, 98, 125, 142), the gradient fade technique (lines 66, 127; one strength variable only), the letter-spacing scale and uppercase treatment, the rule lines (36 / 40 / 80 px), the 16 px swatch dots, the button padding and arrow, the value-tile border pattern, the h1 clamp shape (with only a size range exposed), the breakpoints (to be redefined by the CSS and RESP work) and the 1440 px maximum width unless `full_bleed` is on. Anything a merchant could change to break the hierarchy is left out of the schema (RISK-11).

### 29.9 Mapping from current homepage blocks

| Current block (line) | Future section | Setting or block | Data source / decision |
|---|---|---|---|
| Announcement left text (59) | announcement-bar | `announcement` block 1 | copy |
| Globe + 'Worldwide Shipping' (60) | announcement-bar | `announcement` block 2 + `icon` | copy; shipping scope BUSINESS INFORMATION REQUIRED |
| Wordmark, nav and footer (69, 155) | header, footer | global `logo`, `logo_height_*` | SVG from OG LOGO.psd (BUSINESS INFORMATION REQUIRED); size decision FIDELITY-4 |
| Nav links (71-72) | header | `menu` link_list | Shopify Navigation; destinations: NAV register |
| Hamburger (75) | header | `mobile_menu_style` | theme.js drawer |
| Search / account / cart + badge (76-78) | header | `show_search`, `show_account`, `cart_type` | `routes.*`, `cart.item_count` |
| Hero image (65) | hero | `image`, `image_mobile` | new asset (RISK-01); group photo confirmation BUSINESS DECISION REQUIRED |
| Hero fade (66) | hero | `overlay_strength` | static CSS |
| Eyebrow, h1, verse, subline (83-87) | hero | text settings | copy |
| Script + 'A Higher Purpose.' (91-93) | hero | `caption` blocks | copy |
| New Drop copy + button (100-104) | featured-collection | `eyebrow`, `heading`, `subheading`, `button_*` | copy; link = `collection.url` |
| Product grid (106-121) | featured-collection + product-card | `collection`, `products_to_show` | Shopify products (BUSINESS INFORMATION REQUIRED) |
| Swatches (114-118) | product-card + swatch | `card_show_swatches` | colour option / metafield |
| Story image + fade (126-127) | our-story | `image`, `overlay_strength` | new asset (C1, ADD-4) |
| Story copy + CTA (129-132) | our-story | `eyebrow`, `heading`, `text`, `button_*` | copy; page handle BUSINESS INFORMATION REQUIRED |
| Side caption (136-137) | our-story | `side_caption` | copy |
| Values (142-150; data 179-183) | brand-values | four `value` blocks | copy; icons as SVG snippets |
| Footer logo + tagline (154-157) | footer | `show_logo`, `tagline` | copy |
| Social links (159-162) | footer + social-links | global social settings | both are `href="#"`; URLs BUSINESS INFORMATION REQUIRED; TikTok/YouTube C14 |
| 'A Brighter Tomorrow' (164) | footer | `secondary_tagline` | copy |
| (nothing today) | footer | `link_list` blocks, `copyright_text`, policy links | ADD LATER; BUSINESS INFORMATION REQUIRED (ADD-7) |
| `currency` prop (169-172) | none | store currency + Markets | BUSINESS DECISION REQUIRED (SHOP-08) |
| `<style>` block (13-53) | assets/base.css + section CSS | `css-variables` snippet | CSS register |
| Google Fonts link (11-12) | theme.liquid | typography settings + `font_face` | SHOP-07 |
| support.js, `<x-dc>`, `<helmet>` (6, 9-10, 168) | none | REMOVE | ARCH register |
| 1440 px wrapper (55) | theme.liquid | `page_width`, `full_bleed` | static + setting |

### 29.10 Delivery notes

Build with Shopify CLI against a development theme (`shopify theme dev`, `shopify theme check`, `shopify theme push --development`) from a git repository outside OneDrive (RISK-07). Keep the prototype and the mockup as a read-only design baseline; the rebuild transcribes tokens and copy from them and never copies files. Sequence the theme work as the phases dictate: tokens, schema areas and the QA matrix in Phase 2, assets and the performance budget's enforcement in Phase 3, header group in Phase 4, hero in Phase 5, featured-collection and product card in Phase 6, our-story in Phase 7, the remaining templates in Phase 8, then the conversion, Theme Editor, performance, SEO and accessibility passes.

## 30. Phase Dependency Map

The phases are ordered by dependency, not by visibility. **Phase 2 — Design System** comes first because every later phase consumes its output: the tokens, the type scale, the spacing rhythm, the icon system and the component inventory are the vocabulary in which Phases 4 to 9 are written, and 41 issues resolve there. **Phase 3 — Asset Preparation** follows immediately because the hero, story and product work cannot be completed against 215-650 px mockup crops; sourcing and processing the real imagery gates Phases 5, 6 and 7. The section phases (4 to 7) then rebuild each homepage block against tokens and real assets, and **Phase 8 — Product & Shopping UX** and **Phase 9 — Mobile UX** extend that work into the commerce surface and the phone layout.

**Phase 10 — Shopify Theme Conversion** is the hinge: it retires all three P0 blockers and the entire runtime, CSS and markup debt in one pass, and nothing in Phases 11 to 16 can begin until the theme exists in native form. **Phase 11 — Theme Editor** depends on Phase 10 because schemas can only be written against real sections, and it in turn unblocks the owner's ability to edit content without a developer. **Phases 12, 13 and 14** — performance, SEO and accessibility — are placed after conversion deliberately: each of them is cheap to do correctly in a native theme and expensive to retrofit twice, and each needs measurement against the real thing rather than the prototype. **Phase 15 — Ecommerce QA** validates the commerce paths end to end and is the first point at which acceptance criteria can be met, and **Phase 16 — Final Polish** absorbs the remaining P3 refinements.

Two cross-cutting dependencies sit outside the phase sequence. The business decisions in Appendix A gate work in almost every phase, and four of them gate Phase 2 itself. The absence of a version-controlled working copy (DEBT-12) should be resolved before Phase 2 begins, so that the rebuild has a history and the prototype has a frozen baseline (DEBT-13).

### PHASE 2 — DESIGN SYSTEM (41 issues)
- CSS-01 [P1/HIGH] Colours are hard-coded literals with no custom properties: 18 distinct in the stats block (3 primaries #0d0c0a/#f3efe6/#d8c08a, 3 secondaries #bdb6a8/#ebe6dc/#e9e4d8, the dead #0230, 11 rgba variants) and 21 once the two style-hover shades #2a2823/#e6d3a6 and the swatch olive #4b5443 are counted; #0d0c0a alone appears 18 times whole-file.
- RISK-02 [P1/HIGH] The prototype contains no store facts: no destinations, policies, contacts, social URLs, catalogue, sizes, markets or verse content, and the footer has no copyright, policy or navigation links in either the build or the mockup.
- RISK-03 [P1/HIGH] The build already departs from the approved mockup in hero photo, headline lockup, wordmark size, product tiles, social icons and globe colour, leaving two competing baselines.
- RISK-07 [P1/HIGH] The project lives in a personal OneDrive folder with no git history, no build tooling, an in-place rename performed by the owner and a sibling assets folder that has already disappeared.
- CSS-04 [P1/MEDIUM] Only two desktop-first max-width breakpoints exist (900px and 520px) with no min-width queries and no step between 901 and 1440.
- CSS-07 [P1/MEDIUM] Hover exists only as a global a:hover colour (invisible on Home and on the image-only social links) and two runtime-generated .scp0/.scp1 :hover rules from style-hover; there are no :focus-visible, :active or transition rules and the hover shades #2a2823/#e6d3a6 are undocumented.
- CSS-08 [P1/MEDIUM] Typography is hard-coded as six px sizes between 9 and 15px plus four clamp() headings, six letter-spacing values, nine line-heights and three repeated font-family stacks, with no named scale.
- DEBT-13 [P1/MEDIUM] The prototype remains editable in Claude Design and has already diverged from the mockup by deliberate edits (group hero photo, gold globe, two social boxes removed); each further edit adds inline styles and invalidates this audit's measurements.
- INV-01 [P1/MEDIUM] The project is a single working copy inside the owner's personal OneDrive with no git repository, no package manifest and no build tooling, so the audited state (44 files, 17,185,754 bytes) has no tagged baseline.
- BRAND-01 [P2/MEDIUM] The three brand colours exist only as raw literals (#0d0c0a x14, #d8c08a x10, #f3efe6 x9 in the stats) with no named tokens, and the CTA hover tints #2a2823/#e6d3a6 exist only inside editor-only style-hover attributes.
- BRAND-03 [P2/MEDIUM] Jost's loaded faces do not contain U+20B1 (₱) or U+2192 (→), so every price and both CTA arrows are drawn by a per-platform fallback font that differs from the mockup's sans ₱.
- BRAND-04 [P2/MEDIUM] The type system is six fixed sizes (9-15px) plus four clamps, six letter-spacings and nine line-heights, with the tracked-caps label drawn in several unrelated variants (eyebrow 13px .3em at weight 400 or 500; taglines 14px .3em and 13px .24em; captions 11-12px at .2/.22/.26em), and Playfair 700 requested but unused.
- BRAND-05 [P2/MEDIUM] images/WHITE FONT LOGO.png is a 500x500 PNG with large transparent padding, so the wordmark renders at 66x50 px at 1440 (mockup 114x87 on a 1024 canvas) and 47x36 in the footer, and no vector master has been seen (only PSDs outside the project).
- BRAND-07 [P2/MEDIUM] Three icon vocabularies coexist (gold outline value icons plus the same gold globe in the announcement bar, cream outline utility icons, circled social glyphs vs the mockup's plain glyphs), all as raster PNGs with colour baked in, and the same globe file is drawn at 16px and 44px.
- CSS-09 [P2/MEDIUM] Spacing uses 44 distinct px values across 22 padding, 14 margin and 17 gap strings, three competing gutters (48/24/16px) and bespoke fr ratios per section grid.
- ICON-01 [P2/MEDIUM] All ten icon placements are nine raster RGBA PNGs (308,521 B on four canvases: 110x110, 130x110, 150x110, 130x130) with cream or gold colour baked into the pixels and soft cut edges from an AI sprite sheet.
- ICON-04 [P2/MEDIUM] No icons exist for the interactions the store will need (close, chevron, plus/minus, check, filter, external link), the hamburger is three CSS spans, and the CTA arrows are a text glyph outside Jost.
- JS-07 [P2/MEDIUM] The only hover states on the two CTAs come from the style-hover attribute, which support.js converts at runtime into .scp0:hover and .scp1:hover rules with !important; the attribute has no meaning outside the dc-runtime.
- RISK-08 [P2/MEDIUM] Three Google Fonts families are assumed available on Shopify, with no library check and no licence file in the project.
- RISK-09 [P2/MEDIUM] The peso sign and arrow fall back to a per-OS system face because Jost's loaded faces lack them, and the store money format has not been chosen.
- RISK-13 [P2/MEDIUM] No Lighthouse, axe, screen-reader, throttled-load, cross-browser or real-device results exist for the prototype, and no QA matrix has been written.
- SHOP-07 [P2/MEDIUM] Fonts are delivered by a Google Fonts link inside the body-level helmet element (Playfair Display 700/900, Jost 400/500/600, Kaushan Script), with no font_picker settings and no verification that the families exist in Shopify's font library.
- UI-01 [P2/MEDIUM] The two CTAs differ in font weight (500 vs 600) for no hierarchical reason, their hover exists only through the Claude-Design style-hover attribute, the arrow is a text glyph, and no focus, active or disabled state is defined.
- CSS-11 [P2/LOW] a{color:inherit;text-decoration:none} removes the underline affordance from all nine links and a:hover applies the gold colour to every anchor including image-only links.
- BRAND-02 [P3/LOW] Three near-identical creams (#e9e4d8 paragraph, #ebe6dc tile, #f3efe6 base), the muted #bdb6a8, the olive #4b5443 swatch (data only) and seven rgba alphas of ink across 12 gradient stops plus three hairline alphas have no roles or names.
- BRAND-06 [P3/LOW] Roughly two dozen distinct spacing values (out of 44 distinct px values of all kinds) are used with no scale: section paddings 12/22/26/44/48/56/170/190, 14 distinct gap values (17 listed entries) from 5 to 44px, margins 14/26/36/38.
- BRAND-08 [P3/LOW] Four taglines are used with inconsistent punctuation and repetition: "Different People Same Purpose" (hero, no punctuation) vs "Different People. Same Purpose." (footer), and "More Than Clothing." appears both as the hero script and as the Faith Driven value subtitle.
- CSS-10 [P3/LOW] text-wrap:balance and overflow-wrap:anywhere are used on the headings alongside aspect-ratio, inset, max() and clamp(), with no confirmed support matrix.
- ICON-02 [P3/LOW] icon-cart.png retains a sliver of the sprite sheet's gold "0" badge along its right edge while the page overlays its own CSS badge.
- ICON-03 [P3/LOW] The Facebook and Instagram icons are two-tone circled badges (gold ring, light disc, gold glyph) cut from the social sheet, unlike the mockup's plain glyphs, and the mockup's TikTok and YouTube have no counterpart.
- ICON-05 [P3/LOW] The icon set has four canvas sizes (110x110, 130x110, 150x110, 130x130), two stroke weights (thin cream nav set, heavier gold feature set) and rendered widths of 52/60/44/52 px at the same 44 px height.
- INV-02 [P3/LOW] The entry page was renamed from "God Squad Website.dc.html" to "God Squad Website.html" on 2026-09-20 15:34 while the Phase 1 spec, the runtime's naming convention (rootNameForDocument tests /\.dc\.html?$/i and ensureFetched builds "`<name>`.dc.html") and the original export zip still use the .dc.html name.
- INV-06 [P3/LOW] .claude/launch.json (228 B, a python http.server dev-server configuration) was created inside the project root at 13:23 on 2026-09-20 by the audit lead so the page could be served over HTTP, although the spec states that the website must not be modified during Phase 1.
- PERF-04 [P3/LOW] Kaushan Script (34,748 B) is downloaded for a single three-word phrase and Playfair Display 700 is requested but never used.
- RESP-08 [P3/LOW] There is no tier between 901 and 1440px, so the fluid three-column grid is squeezed to ~230-250px: at 920 the eyebrow, the product names and the View All Products CTA all wrap, and at 1024 "Signature Oversized Tee" wraps to two lines so the tee's price drops a line below the other two.
- RESP-11 [P3/LOW] Apart from the four heading clamps there is no phone type scale: secondary text is 11-13px tracked uppercase, prices are 14px, the paragraph 15px and the cart badge 9px, all fixed px inherited from the desktop mockup.
- RESP-14 [P3/LOW] Everything sits in a max-width:1440px box with section backgrounds on the inner sections, so the cream New Drop band, the hero photo and the value borders stop at 1440 with dark gutters either side.
- UI-04 [P3/LOW] The footer shows two circled Facebook and Instagram icons where the mockup shows four plain glyphs (Instagram, Facebook, TikTok, YouTube); the reduction to two was a deliberate user edit but the circled style is not.
- UI-05 [P3/LOW] The short horizontal rule is drawn five times with four widths (36px gold, 80px cream, 40px ink, 40px cream) and four margin pairs, and hairlines use three alphas (.08, .1, .2).
- VAL-02 [P3/LOW] Every tile carries border-right including the last, a border-bottom is added under 900px and the right border is removed only under 520px, so the divider logic lives on tiles rather than on the grid.
- VAL-03 [P3/LOW] The four value icons share a 44px height but render at 44, 60, 52 and 52 px wide (globe, community, crown, diamond), and their gold is baked into 33-40 KB PNGs.

### PHASE 3 — ASSET PREPARATION (15 issues)
- ASSET-03 [P1/HIGH] The three product images are 215-235 px WebP crops of the 1024x1536 mockup, upscaled 1.23-1.34x at 1440 and 2.8x in device pixels on phones, with the cap non-square.
- ASSET-04 [P1/HIGH] The Our Story slot is filled by a 650x480 mockup-hero crop rendered at 998x520 (1.53x, 3.07x on 2x screens) with 29% of its height cropped, and the unused alternative images/our-story.webp is smaller still (535x348) with caption fragments at its right edge.
- INV-05 [P1/HIGH] The only layered logo sources (OG LOGO.psd 613,320 B, OG LOGO 300x300.psd 209,976 B and PNG exports) live outside the project at Desktop/GODSQUAD/PSD FILES, the original export zip lives in Downloads, and no vector logo (SVG/AI/EPS) or original photography master has been located anywhere; every image in the project is a mockup crop, an AI-generated sheet or a padded PNG export.
- PERF-01 [P1/HIGH] images/hero-group.png is a 1,989,201-byte 1672x941 RGB PNG with no alpha channel and is served unchanged at every viewport, including a 375x320 band.
- RISK-01 [P1/HIGH] Every image in the project is a mockup crop or a single AI PNG, and no vector logo has been seen, so no asset is fit for its slot at 2x.
- RISK-10 [P1/HIGH] No performance budget exists and the prototype carries a 1.99 MB hero PNG, 308 KB of PNG icons and ~211 KB of render-blocking JavaScript.
- ASSET-05 [P2/MEDIUM] The hero master is a 1672x941 image whose upload filename ("ChatGPT Image Sep 20, 2026, 11_06_34 AM.png") indicates AI generation, unconfirmed by the business (BUSINESS INFORMATION REQUIRED); it is 0.85x at 1440 on 1x displays but about 1.7x upscaled on 2x displays, with no portrait or higher-resolution source.
- ASSET-06 [P2/MEDIUM] The only logo files are raster PNGs; the wordmark in use is a 500x500 canvas with large transparent padding (visible mark 66x50 px in a 78 px box), byte-identical to a Desktop PNG, and no SVG, AI or EPS was seen anywhere.
- SHOP-06 [P2/MEDIUM] Assets live in an images/ subfolder, the project root and uploads/, with space-containing names (images/WHITE FONT LOGO.png) and non-theme files mixed in — the mockup PNG, editor screenshots, sprites, the editor-generated .thumbnail preview, and .claude/launch.json, which is dev-server tooling added by the audit lead and not a site file; Shopify assets/ is flat, has no subfolders and must contain only theme files.
- INV-03 [P2/LOW] The project root mixes the entry page and runtime with five unreferenced Claude Design export artefacts (.thumbnail, chatgpt-image-...-evm9.png, white-font-300x300-...png, two white-font-trans-...png; 2,125,399 bytes) carrying unstable hash-suffixed names, and the one live root asset (01-hero-model-mu98p88t-7jig.webp) also has a hash suffix.
- INV-04 [P2/LOW] The live logo asset is images/WHITE FONT LOGO.png (spaces, uppercase, requested as /images/WHITE%20FONT%20LOGO.png, the only referenced file with an unsafe name) and the unreferenced uploads folder uses names with spaces and commas such as "ChatGPT Image Sep 20, 2026, 10_11_00 AM.png".
- ASSET-01 [P3/LOW] Nine md5 duplicate groups hold 11 byte-identical redundant copies totalling 6,733,692 bytes, 39% of the 17.2 MB of site files.
- ASSET-02 [P3/LOW] Two unreferenced AI-generated icon sheets (icons-sprite.png 833,929 B, social-sprite.png 927,973 B) with heavy matting halos and baked-in labels sit in images/ alongside three duplicate uploads.
- ASSET-07 [P3/LOW] Production assets have URL-unsafe or generated names and stray locations: "WHITE FONT LOGO.png" (spaces and upper case, requested as WHITE%20FONT%20LOGO.png), the live story image at the project root with a hash suffix, and uploads named "ChatGPT Image Sep 20, 2026, 10_11_00 AM.png".
- ASSET-08 [P3/LOW] Unreferenced generated and reference files (the editor .thumbnail, three root wordmark exports of which two are same-size different-md5 encodes, three 1920x1009 editor screenshots totalling 3,861,192 B, a pasted globe crop and the 1.87 MB mockup PNG) live next to production images with no separation.

### PHASE 4 — HEADER & NAVIGATION (24 issues)
- A11Y-01 [P1/HIGH] Search, Account and Cart are bare img elements and the hamburger is a span, so none of them is focusable, operable or exposed as a control, and the page has zero button elements.
- A11Y-03 [P1/HIGH] Collections, Our Story and Verse are 12px white text over the bright sky between the models where the top fade has thinned to about 0.4 alpha, measuring 2.4-2.9:1 composited across 1440 and 1024, and the gold Home link drops to about 3.5:1 at 1024px.
- DATA-05 [P1/HIGH] The five menu labels and hrefs (Home #, Shop #shop, Collections #shop, Our Story #story, Verse #) and the hard-coded gold active underline on Home are literals in the markup, the utility icon destinations are not bound to any route object, and the cart badge is the literal text 0 rather than a cart value.
- FOOT-01 [P1/HIGH] The footer holds only a logo, two taglines and two placeholder social links; it has no navigation, policy, contact, copyright or newsletter content.
- HTML-01 [P1/HIGH] There is no `<header>` or `<main>`; the `<nav>` is nested inside the hero `<section>` and absolutely positioned over it, the announcement bar is a plain div, and no section carries an accessible name.
- HTML-04 [P1/HIGH] The page has zero `<button>` elements: the hamburger is a role-less `<span>` carrying an aria-label and the search, account and cart controls are bare `<img>` elements.
- NAV-01 [P1/HIGH] Below 900px the nav links are display:none and the hamburger is a span with no role, tabindex or handler, so there is no navigation at all on phones and tablets.
- NAV-02 [P1/HIGH] Search, Account and Cart are bare img elements with tabIndex -1 and no link or button wrapper.
- NAV-03 [P1/HIGH] Six of nine links (Home, Verse, View All Products, Our Story CTA, Facebook, Instagram) are href="#" and scroll to the top of the page.
- SHOP-04 [P1/HIGH] The nav is absolutely positioned inside the hero section and the hero copy reserves 170 px / 190 px of top padding to clear it, so the announcement bar and header cannot be extracted into a header section group without re-laying the hero.
- JS-08 [P1/MEDIUM] The runtime wires only on* attributes present in markup and the markup has none, so zero interaction JavaScript exists: no menu toggle, search, account, cart, variant or quick-add behaviour is available to port.
- NAV-09 [P1/MEDIUM] The cart badge is the literal text 0 with no relationship to any cart.
- FOOT-02 [P2/MEDIUM] Facebook and Instagram link to # and the network set (two in the build, four in the mockup) is an undecided editor change.
- FOOT-03 [P2/MEDIUM] There is no email capture anywhere on the page.
- HTML-10 [P2/MEDIUM] The five navigation links are bare anchors in a `<div>` with no `<ul>`/`<li>`, and the `<nav>` has no aria-label; the utility controls sit outside any list.
- NAV-04 [P2/MEDIUM] The Verse menu item has no destination (href="#") and no corresponding page or section exists.
- NAV-05 [P2/MEDIUM] Shop and Collections both point at the in-page anchor #shop (the New Drop section), so two primary menu items are indistinguishable and neither reaches a collection.
- NAV-08 [P2/MEDIUM] The wordmark renders at 66x50 in the nav and 47x36 in the footer, about half its relative size in the mockup, because the 500x500 PNG has large transparent padding drawn at 78px/56px.
- CSS-05 [P2/LOW] The first rule of the 900px query targets [data-r=pad], and no element in the markup carries data-r="pad".
- NAV-06 [P2/LOW] The Home link's active gold underline is hard-coded inline and never changes with scroll position or page.
- A11Y-07 [P3/LOW] aria-label="Menu" sits on a span with no role.
- NAV-07 [P3/LOW] Nav hover relies solely on the global a:hover gold (no visible change for the already-gold Home), the utility icons have no hover or focus state, and the social icon links have none at all because their colour is baked into PNGs.
- UI-03 [P3/LOW] Search, account, cart and the hamburger are 22-24px raster icons with no hover, focus or active state, and the cart badge is 9px text in a 14px circle.
- UX-05 [P3/LOW] The announcement bar is a static, unlinked div whose Worldwide Shipping label is a commercial promise with no policy, destinations or rates behind it.

### PHASE 5 — HERO (15 issues)
- HERO-01 [P1/HIGH] The hero contains no link or button; on 1366x768 and 1280x720 the first screen is the hero alone and the nearest CTA ("View All Products", href="#") is below the fold.
- HERO-02 [P1/HIGH] The vertical scrim under the nav thins from .55 to 0 by 30% of the hero height, so Collections, Our Story and Verse sit on open sky between the models where the mockup's nav sits on a dark facade; the measured contrast figures and WCAG classification are in the A11Y register.
- PERF-02 [P1/HIGH] The hero image has no preload, fetchpriority, srcset/sizes or width/height, and its paint is gated behind the runtime's three-hop JavaScript chain.
- RESP-01 [P1/HIGH] Below 900px the hero fade is anchored to the section top while the image sits under the 88px in-flow nav, so the gradient goes solid black 88px above the photo's bottom and the last 88px of photo reappear unfaded with a hard edge.
- UX-01 [P1/HIGH] The hero contains no link or button, so the first screen asks nothing of the visitor and on 1366x768 and 1280x720 laptops no product or CTA is visible without scrolling.
- HERO-05 [P1/MEDIUM] The build's hero is a three-model generated group image (images/hero-group.png, identical to the ChatGPT upload) that the user substituted for the mockup's single capped model, so hero and story imagery are inverted relative to the approved mockup.
- HERO-03 [P2/MEDIUM] The h1 stacks WALK / BY / FAITH. on three lines at 1024, 1440 and 1920 and collapses to one line at 768-900, reproducing the mockup's two-line lockup only at phone widths, because the copy column (about 450px at 1440) cannot hold "WALK BY" at the 112px clamp and text-wrap:balance redistributes the break.
- HERO-04 [P2/MEDIUM] Six copy elements carry no priority rule, so below 900px all of them stack under the photo band (five taglines, 563px of text under a 320px image, hero 970px tall at 375) and the side captions become orphan blocks.
- RESP-07 [P2/MEDIUM] The h1 renders on three lines (WALK / BY / FAITH.) from 901 to 1920px and on one line from about 540 to 900px; the approved two-line lockup appears only below about 540px.
- RESP-10 [P2/MEDIUM] At 375px object-fit:cover scales the 1672x941 landscape photo by 0.34 to 568x320 and crops 193px (34%), cutting the third model and the back-print message, while object-position:center 30% has no effect.
- HERO-06 [P3/LOW] The announcement bar is a solid strip outside the hero section and the photo begins directly beneath it with sky and tower tops, producing a hard horizontal edge at 1024 and 1440 and under the nav strip below 900px, while the mockup's top edge is continuously dark.
- HERO-07 [P3/LOW] The "More Than Clothing." script and "A HIGHER PURPOSE." caption are placed by a .7fr column and 190px padding directly over the right model's back-print lettering at 1024-1440.
- HERO-08 [P3/LOW] There is no portrait source for phones: the 375x320 band is filled from the 16:9 image by height, cropping 96px from each side so the third model and the back-print message are cut and object-position has no effect.
- RESP-09 [P3/LOW] The mobile hero band is height:62vw with min-height 320px and no viewport-height cap.
- RESP-13 [P3/LOW] On 1280x720 and 1366x768 the hero fills the first screen and no product is visible without scrolling.

### PHASE 6 — COLLECTIONS & BEST SELLERS (11 issues)
- COLL-01 [P1/HIGH] No collection page, template or collection data exists; the Collections and Shop links resolve to the homepage anchor #shop.
- DATA-01 [P1/HIGH] The three products (name, price string, image path, three swatch hexes) exist only as object literals inside the data-dc-script class; there are no handles, descriptions, variants, sizes, inventory, SKUs, compare-at prices, vendor, type, tags, secondary images or product URLs.
- DATA-02 [P1/HIGH] Prices are string concatenations of a symbol and a literal (cur + '1,290') and the Claude Design editor prop currency (enum ₱/$/€, default ₱, section "Shop") only swaps the symbol without converting the amount; no numeric price exists and the prop has no Shopify equivalent.
- HTML-03 [P1/HIGH] The outline is one h1 and two h2s; product names and value titles are `<div>`s and the values section has no heading at all.
- COLL-02 [P2/MEDIUM] There is no collection index and no defined collection taxonomy, so Collections and Shop are indistinguishable.
- COLL-03 [P2/MEDIUM] The New Drop / The Faithful section implies drop-based merchandising but no collection is defined for it and its three products are a hard-coded array.
- DATA-03 [P2/MEDIUM] Each product carries the same three hex values (#0d0c0a, #f3efe6, #4b5443) as an unnamed array not tied to any variant, rendered as inert spans.
- ECOM-06 [P2/MEDIUM] No sorting or filtering exists because there is no collection page.
- UI-02 [P2/MEDIUM] Each product image sits in a 1:1 box with object-fit:cover over a #ebe6dc background, so the crop's own off-white box is visible against the cream section, garments run to the box edges and the 215x190 cap is edge-cropped with its brim touching the tile edge, unlike the mockup's floated garments.
- UX-02 [P2/MEDIUM] The Best Sellers / Product Discovery step of the intended flow does not exist; the page has four sections and goes straight from New Drop to Our Story.
- RESP-03 [P3/LOW] The two-column tablet grid leaves the Utility Cap alone on a second row.

### PHASE 7 — OUR STORY (7 issues)
- STORY-01 [P1/HIGH] The section uses ./01-hero-model-mu98p88t-7jig.webp, a 650x480 crop of the mockup's hero with the headline fragments "A PURPOSE", "K BY", "TH." and the "More Than Clothing" script baked into the pixels, while the mockup's three-model story image (images/our-story.webp) is unused.
- STORY-02 [P2/MEDIUM] The image slot (left:30%, width:70%, object-fit:cover, object-position:center top) discards about 29% of the picture's height at 1440 — the hands and chest that carry the mockup's gesture — and starts the photo at 30% of the section so the subject's face lands under the copy column's right edge, with no aspect-ratio or focal-point rule for the slot.
- UX-03 [P2/MEDIUM] There is no Verse / Faith section although Verse is a primary nav item; the only scripture is the hero's 2 Corinthians 5:7 line.
- UX-07 [P2/MEDIUM] The nav Our Story item scrolls to the story section while the section's own Our Story CTA scrolls to the top, and neither leads to fuller story content.
- STORY-03 [P3/LOW] The gold CTA repeats the eyebrow word-for-word ("Our Story" → "Our Story"), points to "#", and no About/Our Story page or long-form story copy has been seen in the project.
- STORY-04 [P3/LOW] Below 900px the "Faith Lives Different Here." caption and its rule stack as a 145px orphan block after the CTA instead of overlaying the photo.
- STORY-05 [P3/LOW] "Real People. Bigger Purpose." wraps to three lines at 1440 and four at 1024 (mockup: two) because the copy column is .9fr minus 96px padding, about 350px at 1440 and 220px at 1024.

### PHASE 8 — PRODUCT & SHOPPING UX (17 issues)
- ECOM-01 [P1/CRITICAL] No product page or product template exists.
- ECOM-02 [P1/CRITICAL] There is no cart, cart drawer, add-to-cart, quantity control or checkout pathway; the cart icon is an inert image with a literal 0 badge.
- ECOM-03 [P1/HIGH] There is no search form or search template; the search icon is a bare image.
- ECOM-04 [P1/HIGH] There is no variant model (no sizes anywhere, colours as inert hex swatches) and no availability or sold-out state.
- PROD-01 [P1/HIGH] No product card contains a link; product names are divs and the grid holds zero anchors.
- PROD-02 [P1/HIGH] There is no add-to-cart or quick-add control on the cards or anywhere on the page (zero forms, zero buttons).
- RISK-06 [P1/HIGH] The programme is framed as a conversion but the prototype is a homepage with no commerce, so the real scope is a complete theme with one designed page and at least nine undesigned storefront templates, about twenty once the customer, gift card and blog routes are counted.
- SHOP-09 [P1/HIGH] Only the homepage exists; product, collection, list-collections, cart, search, page, page.our-story, 404, password, gift card and customer templates that Shopify serves have no prototype design at all.
- PROD-04 [P1/MEDIUM] Prices are displayed without money formatting, compare-at/sale, from-pricing or sold-out states, and the currency prop only swaps the symbol on the same number.
- A11Y-05 [P2/MEDIUM] The nine swatches are empty spans with inline backgrounds and no name, role or text, and the cream swatch on the cream section is distinguished only by a ~1.8:1 border.
- ECOM-05 [P2/MEDIUM] The account icon is inert and no account pathway or decision on customer accounts exists.
- ECOM-09 [P2/MEDIUM] The prototype implies PHP pricing with a ₱/$/€ symbol-only toggle and no market, shipping-destination or currency strategy is defined.
- PROD-03 [P2/MEDIUM] The nine colour swatches are inert 16px spans bound to hex literals with no colour names, no selection behaviour and no variant mapping.
- PROD-05 [P2/MEDIUM] Each product image is boxed in a 1:1 #ebe6dc tile with object-fit:cover, so the crop backgrounds read as visible squares and the non-square cap is edge-cropped with its brim touching the tile edge.
- ECOM-07 [P3/LOW] No product recommendations or related products exist.
- PROD-06 [P3/LOW] Product cards have no hover or focus feedback and no secondary image.
- PROD-07 [P3/LOW] Cards carry no merchandising signals: no New / Sold out badge, no size information, no variant count and no from-price.

### PHASE 9 — MOBILE UX (7 issues)
- RISK-05 [P1/HIGH] The mobile layer is 31 media-query rules (26 at max-width 900px, 5 at max-width 520px) that override the desktop rules with !important, it carries a live hero-fade defect, and no genuine device captures or pass criteria exist for the rebuild.
- A11Y-10 [P2/MEDIUM] The hamburger is 22x16, the utility icons 24x24, the social links 28x28 and the swatches 16x16 at every width.
- RESP-02 [P2/MEDIUM] The phone rule forces one column, producing 327-382px square tiles from 235px sources and a 1,695px New Drop section whose only control sits above the grid.
- RESP-04 [P2/MEDIUM] The desktop overlay captions (More Than Clothing. / A Higher Purpose. and Faith Lives Different Here.) are kept as in-flow blocks after the main copy on small screens.
- RESP-12 [P2/MEDIUM] The 900px max-width query removes the primary navigation and shows the inert hamburger, and that layout is also what a 1440 desktop gets from 160% zoom (1440/1.6 = 900 CSS px) and any laptop up to 1800px gets at 200%. A 1366 laptop stays on the desktop layout at 150% (1366/1.5 = 911 CSS px) and only crosses the breakpoint at the next zoom step, 175% (781 CSS px).
- RESP-05 [P3/LOW] Phones get a 698px single-column stack for four short labels, and at 521-900px every tile keeps border-right so a stray 1px rule paints at the viewport edge and the last row's bottom border doubles with the section's own border.
- RESP-06 [P3/LOW] The footer is forced into a column at <=900px although at 768px the two groups (230px + 271px) fit on one row in a 705px content box.

### PHASE 10 — SHOPIFY THEME CONVERSION (27 issues)
- ARCH-01 [P0/CRITICAL] The page is a Claude Design dc document: every visible node sits inside `<x-dc>` and is compiled by support.js into React elements at runtime (sc-for/sc-if/helmet custom elements, {{ }} interpolation, style-hover, a DCLogic class evaluated with new Function), so there is no static HTML page at all.
- ARCH-02 [P0/CRITICAL] The template uses {{ products }}, {{ p.name }}, {{ p.price }}, background:{{ s }}, {{ v.icon }} and similar expressions, the same delimiters as Liquid output tags, and the data they reference exists only in the data-dc-script.
- SHOP-01 [P0/CRITICAL] No Shopify theme structure exists: the deliverable is a single Claude Design dc document plus a generated runtime, with none of layout/, sections/, snippets/, templates/, assets/, config/ or locales/.
- A11Y-11 [P1/HIGH] The html element carries no lang attribute and document.title is empty, so the page declares neither its language nor a name.
- ARCH-03 [P1/HIGH] support.js hides `<x-dc>` synchronously with x-dc{display:none!important} and reveals content only after React 18.3.1 and ReactDOM are fetched from unpkg.com; the failure path only logs and rethrows with no fallback.
- CSS-02 [P1/HIGH] 77 style attributes (6,421 chars, 69% of the CSS) carry all layout and typography, the source has zero classes, and complete recipes (eyebrow, label, CTA, hamburger bar, icon size) are repeated verbatim.
- CSS-03 [P1/HIGH] The responsive layer is 31 rules in two max-width queries keyed on 25 distinct editor data-r hooks (26 occurrences) (32 data-r rules including the base hamburger rule; 34 selector uses) with 55 !important declarations (49 in the 900px query, 6 in the 520px query), plus order:-2/-1 reordering of hero children.
- JS-01 [P1/HIGH] support.js is a 69,150 B (19,037 B gz), 1,911-line generated Claude Design editor/streaming runtime ("GENERATED from dc-runtime/src/*.ts — do not edit") whose job is to compile the dc template into React and talk to the design editor; roughly 600 of its lines (x-import/Babel loader, deck-stage keying, streaming placeholders, sibling-component fetch, stream tracker, canvas mode, editor bridge API) are code paths this page never enters.
- JS-02 [P1/HIGH] First paint requires three dependent network hops after the document (support.js synchronous in head; React and ReactDOM fetched in parallel with async=false; then boot() on DOMContentLoaded), about 211 KB raw / 66 KB gzipped of JavaScript that is all effectively render-blocking because the template is hidden until React mounts.
- RISK-04 [P1/HIGH] The prototype boots from a double-click and looks reusable, but its template syntax collides with Liquid and its first paint depends on fetching React from unpkg.com.
- SHOP-03 [P1/HIGH] There is no config/settings_schema.json or settings_data.json: brand colours are literals repeated across the 77 inline styles and the 2,916 B `<style>` block (all sources: #0d0c0a x14, #d8c08a x10, #f3efe6 x9, #bdb6a8 x3; inline-only the repeats are background:#0d0c0a x6, background:#f3efe6 x6, color:#d8c08a x5); fonts are hardcoded in the `<style>` and in a body-level Google Fonts link (line 12); the logo is a hardcoded `<img src>` (lines 69, 155); and no social URLs exist at all, both social links being href="#" (BUSINESS INFORMATION REQUIRED).
- DEBT-12 [P1/MEDIUM] The project is not a git repository, has no package.json or build tooling, lives inside a personal OneDrive folder, the spec still names the old file name, and four unreferenced root-level exports (chatgpt-image-…png, white-font-300x300-…png, two white-font-trans-…png) sit beside the referenced story WebP in the root.
- HTML-02 [P1/MEDIUM] The `<html>` element has no lang attribute.
- HTML-05 [P1/MEDIUM] The markup depends on runtime-only constructs: `<x-dc>`, `<helmet>`, three `<sc-for>`, two `<sc-if>`, two style-hover, four data-screen-label, five hint-placeholder-* attributes and a text/x-dc data script.
- HTML-06 [P1/MEDIUM] None of the 12 images carries width, height, srcset, sizes, loading or decoding attributes.
- HTML-09 [P1/MEDIUM] The stylesheet, the Google Fonts link and the preconnect live inside `<helmet>` in the body and are only hoisted into `<head>` by the runtime.
- A11Y-02 [P2/MEDIUM] There is no skip link and no main landmark; the nav lives inside the hero section, and the four section elements have no accessible name so they are exposed as generic containers rather than regions (data-screen-label is editor metadata and names nothing). The only landmarks on the page are the unnamed nav and the footer as contentinfo.
- ARCH-04 [P2/MEDIUM] The only stylesheet (2,916 B `<style>`) and the Google Fonts `<link>` are authored inside `<helmet>` in the body and reach `<head>` only because the helmet manager clones them at render time; the real `<head>` holds only charset, viewport and the runtime script.
- JS-04 [P2/MEDIUM] The data-dc-script class is evaluated with new Function (evalDcLogic) and any x-import module would be executed the same way after a fetch, which requires 'unsafe-eval' under a Content-Security-Policy.
- SEO-10 [P2/MEDIUM] Product and value content exists only as hidden template placeholders and a JS data block that React renders after loading from unpkg, so a client that does not run the script reads the raw template — product cards reading literal {{ p.name }} with broken {{ p.img }} images — while a client that runs the script but cannot reach unpkg gets a blank page, because hideRawTemplate() hides `<x-dc>` before React is even requested.
- SHOP-05 [P2/MEDIUM] No locales/ directory exists; every storefront string and every future schema label is inline in the markup, and the store's language set is unknown.
- HTML-08 [P2/LOW] Two empty spacer `<div>`s stand in for grid columns, two logo wrappers exist only to carry a dead background, and the single 1440px wrapper carries the page background and overflow:hidden for every section.
- JS-05 [P2/LOW] The runtime posts __dc_booted and __dc_design_mode to window.parent with target origin "*", acts on __dc_theme/__dc_probe messages from any origin without checking e.origin, exposes __dcUpdate/__dcSetProps/__dcRegistry/DCLogic on window, and stamps 137 data-dc-tpl attributes and 14 .sc-interp spans into the rendered DOM.
- CSS-06 [P3/LOW] background:#0230 (alpha 0) on both logo wrappers, flex-wrap:wrap on a grid container, an object-position value duplicated between inline and the 900px query, and a [data-r=hero-img] rule split in two.
- HTML-12 [P3/LOW] Only one `<p>` exists (the story paragraph); every other piece of running text — eyebrows, taglines, prices, footer lines — is a `<div>` or `<span>`.
- JS-03 [P3/LOW] boot() calls fetch(location.href) and recompiles and re-renders the whole template from the raw text whenever window.__resources is absent, so the HTML document is requested twice and React renders twice on every load (the fetch fails silently on file://).
- JS-06 [P3/LOW] Because the raw template is real DOM hidden by display:none rather than a `<template>`, the browser requests "{{ p.img }}" and "{{ v.icon }}" literally (two 404s per load) and starts downloading all 15 images before the runtime replaces `<x-dc>`.

### PHASE 11 — THEME EDITOR (11 issues)
- SHOP-02 [P1/HIGH] No section schemas, JSON templates or section groups exist; the only editable value in the project is the Claude Design currency prop in data-props.
- DATA-04 [P2/MEDIUM] The four value tiles (title, sub, icon path) are an array in the data-dc-script rendered through sc-for, with icons as paths to raster PNGs.
- DATA-06 [P2/MEDIUM] All copy (announcement, hero eyebrow/heading/verse/taglines, New Drop heading and subheading, story heading/paragraph/caption, footer taglines, button labels) is inline text in the template, frequently with layout-bearing `<br>` tags.
- DATA-07 [P2/MEDIUM] All 15 referenced image files (17 references) are relative file paths hard-coded in the template or the data script (images/..., ./01-hero-model-mu98p88t-7jig.webp), including the logo path with spaces used twice.
- DATA-08 [P2/MEDIUM] Facebook and Instagram point to "#" and the mockup's TikTok and YouTube are absent by a deliberate editor removal, so no social destination exists in the data.
- HTML-07 [P2/MEDIUM] Twelve `<br>` elements set layout line breaks, including inside both h2s and every multi-line tagline; the h1 carries none and wraps by column width.
- RISK-11 [P2/MEDIUM] The owner has been editing by natural-language prompt in Claude Design, whereas Shopify exposes only what section schemas declare.
- STORY-06 [P2/MEDIUM] Eyebrow, heading, paragraph, CTA label and link, side caption, image, alt and scrim are all inline copy or hard paths with no settings schema.
- VAL-01 [P2/MEDIUM] The four values are hard-coded objects in the data-dc-script rendered by sc-for, with no way to add, reorder, relabel or link a value.
- DATA-09 [P2/LOW] The page asserts business facts that have not been confirmed: "Worldwide Shipping" (announcement), "Worldwide / Shipping Available" (values), "Philippine streetwear brand" (story) and peso pricing.
- UX-06 [P3/LOW] The four value tiles link nowhere, Worldwide / Shipping Available duplicates the announcement claim, and Community is asserted without community content.

### PHASE 12 — PERFORMANCE (3 issues)
- PERF-03 [P2/MEDIUM] Five Google Fonts files (152,880 B) plus 7,461 B of CSS load from a third party with a preconnect only to fonts.googleapis.com (no crossorigin) and none to fonts.gstatic.com, with display=swap on the 112 px headline face.
- PERF-05 [P2/MEDIUM] None of the 12 `<img>` elements in the source carries loading, decoding, width or height, so all 15 image files download at once and the wordmark's width is unknown until its PNG arrives.
- PERF-06 [P3/LOW] No performance measurement exists: Lighthouse was not run, LCP did not report and CLS read 0 only on a warm localhost load.

### PHASE 13 — SEO (10 issues)
- SEO-01 [P1/HIGH] The document has no `<title>` element, so document.title is empty at runtime.
- SEO-02 [P1/HIGH] No meta description exists anywhere in the document.
- SEO-03 [P2/MEDIUM] No canonical link is declared.
- SEO-04 [P2/MEDIUM] No Open Graph or Twitter Card tags exist and no share-format image (1200x630 or similar) exists among the 44 site files.
- SEO-05 [P2/MEDIUM] No favicon of any kind is declared, so a normal tab will request /favicon.ico and receive a 404 (predicted; not observed in this capture).
- SEO-07 [P2/MEDIUM] No structured data (JSON-LD) is present for the organization, products or breadcrumbs.
- SEO-09 [P2/MEDIUM] The whole store is a single URL whose nine links are hash anchors, six of them href="#", with Shop and Collections both pointing at #shop.
- SEO-06 [P3/LOW] There is no robots meta, robots.txt or sitemap.xml in the project.
- SEO-08 [P3/LOW] Alt text is present on all 12 images, but the Our Story alt ("God Squad community") describes a subject the file does not show and product alts are bare names with no brand or product-type context.
- SEO-11 [P3/LOW] The homepage carries roughly 120 words of indexable copy, one 25-word paragraph that is the only mention of the brand name and category in running text, and no product descriptions.

### PHASE 14 — ACCESSIBILITY (6 issues)
- RISK-14 [P1/HIGH] The transparent nav over the hero photo measures below WCAG AA for Collections, Our Story and Verse at 1024 and 1440 — 2.4-2.9:1 when the fade alpha is composited over sampled photo luminance, and 2.4-2.5:1 over the brightest 2% of the render's pixels although 4.6-5.7:1 on the median — while at 1024 the gold Home link drops to ~3.5:1 and the header has no operable controls.
- A11Y-04 [P2/MEDIUM] No :focus or :focus-visible rule exists; the browser default ring is the only indicator, and the two raster social icon links have no hover or focus state at all.
- A11Y-08 [P2/MEDIUM] The outline is one h1 and two h2s whose DOM text is TheFaithful and Real People.Bigger Purpose. (line breaks via br), while product names and value titles are divs.
- A11Y-09 [P2/MEDIUM] Of the 12 image tags in the source, 4 are wrong (Search, Account and Cart name functions that do not exist; the story alt says community but the picture shows one man and carries baked-in headline fragments), 3 are redundant (the product template alt repeats the name shown below it, and both social alts repeat the link's aria-label) and 1 is generic (the hero alt omits the on-garment message and the setting). Only 4 are correct: the announcement globe, both wordmarks and the value icons.
- HTML-11 [P2/LOW] The story image alt says "God Squad community" but the file shows a single capped model with baked headline text; the inert search/account/cart images announce as controls; the social images duplicate their link's aria-label.
- A11Y-06 [P3/LOW] Both CTAs contain a bare span with the arrow character and no aria-hidden.

### PHASE 15 — ECOMMERCE QA (4 issues)
- RISK-12 [P2/MEDIUM] The prototype's currency selector swaps only the symbol, and no decision exists on selling currencies.
- SHOP-08 [P2/MEDIUM] Currency is a template prop enum (₱/$/€) concatenated onto string prices, with no Shopify mechanism (store money format, money filter, Shopify Markets) behind it.
- VAL-04 [P2/MEDIUM] "Worldwide / Shipping Available" is a checkable business claim and no shipping policy, destination list or rate table has been seen in the project.
- FOOT-04 [P3/LOW] No payment icons and no country/currency selector exist.

### PHASE 16 — FINAL POLISH (2 issues)
- ECOM-08 [P3/LOW] No wishlist exists and Shopify has no native wishlist.
- UX-04 [P3/LOW] There is no Social / Community section; the only social presence is two footer icons linking to #.

## 31. Recommended Phase 2 Scope

Phase 2 converts the approved visual language into a documented, reusable system. It is a design and specification phase: it produces tokens, component specifications and rules, not Shopify files and not new imagery.

### 31.1 In scope

**1. Colour tokens.** Name and record the three primaries (`#0D0C0A`, `#F3EFE6`, `#D8C08A`), the three secondary neutrals in use (`#bdb6a8` muted caption, `#e9e4d8` story body, `#ebe6dc` product tile), the olive `#4b5443` that currently exists only as swatch data, and the rgba scrim values used by the hero and story gradients. Resolve whether the three near-identical creams are intentional or drift (BRAND-02), and define the pairs that must meet 4.5:1 so that the header decision in Phase 4 has a rule to satisfy (CSS-01, BRAND-01, A11Y-03).

**2. Type scale.** Codify Playfair Display 900, Jost 400/500/600 and Kaushan Script into a named scale replacing the current six fixed sizes, four `clamp()` headings, six letter-spacing values and nine line-heights. The tracked-uppercase label style is a brand signature and should become a documented token pair (size plus tracking), not an ad-hoc value. Two specific decisions belong here: a phone floor for secondary text, which is currently 9-13 px, and the handling of the peso sign and the arrow glyph, which Jost does not contain and which therefore render in a per-platform fallback face today (BRAND-03, BRAND-04, RESP-11, PERF-04).

**3. Spacing, grid and rules.** Replace roughly two dozen ad-hoc spacing values and three competing page gutters (48/24/16 px) with one scale and one gutter token. Define the page grid, the section rhythm, and the short horizontal rule that currently appears five times in four widths and four margin pairs (CSS-09, BRAND-06, UI-05).

**4. Component specifications.** Announcement bar, header (with its mobile panel), primary button, secondary button, product card, value tile, editorial caption, footer. Each needs its states defined — default, hover, focus-visible, active, disabled where applicable — because the prototype has essentially none (CSS-07, UI-01, PROD-06, NAV-07).

**5. Breakpoint and layout rules.** Replace the two desktop-first `max-width` queries with a mobile-first set, add the missing tier between 901 and 1440 px where names and buttons currently wrap, and decide the behaviour above 1440 px (CSS-04, RESP-08, RESP-14).

**6. Icon system.** Specify one inline-SVG set with a single stroke weight, a single optical size and `currentColor` inheritance, covering the ten current placements plus the interactions a store needs and the prototype lacks: close, chevron, plus, minus, check, filter, external link (ICON-01, ICON-04, ICON-05).

**7. Accessibility rules baked into the system.** Minimum contrast pairs, a visible focus token, a 44x44 px minimum target size, and a labelling convention for icon-only controls, so that Phases 4 to 9 inherit compliance rather than retrofitting it (A11Y-04, A11Y-10).

### 31.2 Explicitly out of scope for Phase 2

No Shopify files, schemas or Liquid of any kind. No asset replacement, re-encoding or deletion. No changes to the prototype's markup, CSS or JavaScript. No change to the visual identity: Phase 2 documents and standardises what is approved, it does not redesign it.

### 31.3 Inputs required before Phase 2 can complete

Four decisions from Appendix A gate this phase: confirmation of the extended palette beyond the three primaries; whether the 9-13 px tracked labels are brand-mandated on phones or may be raised to a 14/16 px floor; the target browser and device support matrix, which determines whether `text-wrap:balance`, `aspect-ratio` and container queries are available; and the intended behaviour above 1440 px. Typeface confirmation and the font-hosting decision are also needed to close the type token set.

### 31.4 Definition of done

A written design-system document plus a token file, covering colour, type, spacing, radii, borders, elevation, motion and the eight components, each with states and responsive behaviour, and each cross-referenced to the issue IDs it retires. Sign-off from the owner on the four gating decisions above.

## 32. Final Audit Checklist

Every task the Phase 1 specification required, with its outcome. Items marked `[ ]` were explicitly deferred to a later phase by the specification or by the limits of a static audit.

**Specification tasks**

- [x] **1. Inspect the entire project** — 44 files inspected recursively; md5-hashed inventory with dimensions, byte sizes and source-verified usage (§2).
- [x] **2. Current project architecture audit** — entry file, runtime, rendering chain, custom elements, data system and responsive handling documented; suitability verdict given (§3).
- [x] **3. HTML / markup audit** — semantics, hierarchy, landmarks, links, images, attributes and wrappers assessed with CRITICAL/HIGH/MEDIUM/LOW severities (§4).
- [x] **4. CSS audit** — inline vs embedded, duplication, breakpoints, hardcoded values, `!important`, hover behaviour and migratability, with a recommended future architecture (§5).
- [x] **5. Brand & design audit** — colour, typography, spacing, grid, imagery, buttons, navigation, icons, cards, editorial sections, footer and hierarchy, each classified (§7).
- [x] **6. Homepage UX audit** — all ten intended flow steps documented with purpose, implementation, quality, problems, opportunities, Shopify implementation and priority (§9).
- [x] **7. Header & navigation audit** — every placeholder and non-functional interaction identified; all nine hrefs listed with intended destinations (§10).
- [x] **8. Hero audit** — all six copy elements, hierarchy, contrast, composition, CTA strategy, three layouts, LCP implications and accessibility; verdict given (§11).
- [x] **9. Product / collection UX audit** — cards, imagery, names, pricing, swatches, hover, quick add and links audited; hardcoded data mapped to Shopify objects (§12, §13).
- [x] **10. Shopping UX gap analysis** — all sixteen features classified CURRENT / MISSING / REQUIRED / OPTIONAL / BUSINESS DECISION REQUIRED (§25).
- [x] **11. Our Story audit** — storytelling, readability, composition, CTA, mobile, authenticity and Theme Editor editability (§14).
- [x] **12. Brand values audit** — icons, hierarchy, spacing, consistency, mobile layout and accessibility; section-block recommendation given (§15).
- [x] **13. Footer audit** — current elements assessed against production requirements; every unknown marked BUSINESS INFORMATION REQUIRED, no links invented (§16).
- [x] **14. Responsive / mobile audit** — both media queries analysed; 375, 390, 430, 768, 900, 1024, 1280 and 1440+ evaluated against live measurements and full-page captures (§17).
- [x] **15. Accessibility audit** — semantics, headings, alt text, controls, keyboard order, focus, contrast, targets and labelling, each categorised by severity (§18).
- [x] **16. SEO audit** — title, description, canonical, Open Graph, favicon, robots, structured data, headings, alt text and URLs (§19).
- [x] **17. Performance audit** — image weight and format, JavaScript, CSS, fonts, external resources, render blocking, lazy loading and DOM complexity, with `hero-group.png`, `icons-sprite.png` and `social-sprite.png` examined specifically (§20).
- [x] **18. Asset audit** — every asset classified KEEP / OPTIMIZE / REPLACE / ARCHIVE / REMOVE / UNKNOWN; nine duplicate groups identified by md5; master, web, mockup, reference and generated assets distinguished (§21).
- [x] **19. Image quality audit** — the three product images, `hero-group.png`, `hero-model.webp` and `our-story.webp` assessed for resolution, sufficiency and delivery strategy (§21).
- [x] **20. Icon audit** — all nine icons and both sprite sheets assessed with a target format for each (§22).
- [x] **21. JavaScript audit** — purpose, dependencies, architecture, bundle size, redundancy, compatibility, maintainability and security; verdict REMOVE DURING SHOPIFY CONVERSION (§6).
- [x] **22. Data architecture audit** — every hardcoded value mapped to its future Shopify home (§23).
- [x] **23. Shopify compatibility audit** — evaluated against Online Store 2.0 across structure, Liquid, JSON templates, sections, blocks, snippets, config, locales and the Theme Editor (§24).
- [x] **24. Future Shopify architecture recommendation** — directory tree, sections, snippets, templates and section groups recommended, with a block-to-section mapping (§29).
- [x] **25. Priority matrix** — 199 issues with ID, area, problem, impact, recommendation, priority, severity and phase (§28).
- [x] **26. Phase dependency map** — every issue assigned to exactly one of the fifteen implementation phases (§30).
- [x] **27. Do not fix anything** — no CSS, JavaScript, HTML, asset, image, colour, typeface or content was modified; no Shopify file was created; no dependency or app was installed.

**Deferred to later phases**

- [ ] Lighthouse and axe-core runs against a deployed build — meaningful only against the native theme (Phases 12 and 14; PERF-06, RISK-13).
- [ ] Screen-reader pass with NVDA, JAWS and VoiceOver (Phase 14).
- [ ] Real-device testing on iOS Safari and Android Chrome (Phase 9).
- [ ] Cross-browser verification in Firefox and Safari, and Windows High Contrast mode (Phase 15).
- [ ] Throttled cold-cache load measurement and a performance budget (Phase 12).
- [ ] Inspection of the layered PSD logo sources on the Desktop, which lie outside the project folder and were not opened (Phase 3; INV-05).

**Statement of non-modification**

No project file was created, modified, renamed or deleted during this audit, with two exceptions, both disclosed: this report, `PHASE-1-WEBSITE-AUDIT.md`, written to the project root as the deliverable; and `.claude/launch.json` (228 bytes), a local development-server configuration created during Phase 0 so the prototype could be rendered over HTTP for inspection. It is audit tooling, not a site file, and is recorded as INV-06. The entry page was renamed from `God Squad Website.dc.html` to `God Squad Website.html` by the owner, not by this audit (INV-02).

## Appendix A. Business information required

The audit invented no business facts. The thirty decisions below are the complete set required before implementation can finish; the seven clusters group them by who must answer. Each cites the issue IDs that depend on it and the earliest phase it gates. Items marked **gates Phase 2** must be answered before the design system can be signed off.

### A.1 Catalogue, pricing and markets

| # | Decision required | Depends on | Gates |
|---|---|---|---|
| 1 | Real product catalogue: titles, descriptions, launch prices, and whether ₱1,290 / ₱2,490 / ₱890 are actual prices or placeholders | DATA-01, PROD-04, ECOM-01 | Phase 8 |
| 2 | Variant model per product: size run, the names of the three swatch colours (`#0d0c0a`, `#f3efe6`, `#4b5443`), variant images, inventory and backorder policy | DATA-03, PROD-03, ECOM-04, A11Y-05 | Phase 8 |
| 3 | Store currency and money format (₱ symbol vs PHP code), and whether the prototype's $/€ options represent planned Shopify Markets | DATA-02, SHOP-08, ECOM-09, RISK-12, BRAND-03 | Phase 8 |
| 4 | Compare-at and sale pricing policy, and whether from-pricing applies | PROD-04 | Phase 8 |
| 5 | Launch catalogue size in products and SKUs, which determines whether filters, sorting and a cart drawer are justified | ECOM-06, ECOM-08 | Phase 8 |

### A.2 Collections, navigation and site structure

| # | Decision required | Depends on | Gates |
|---|---|---|---|
| 6 | Which collection feeds "New Drop / The Faithful", how many products it shows, and what "View All Products" opens | COLL-03, DATA-01, NAV-03 | Phase 6 |
| 7 | Collection taxonomy: names, handles, descriptions, banner images, default sort, and whether a Collections index page is wanted | COLL-01, COLL-02, NAV-05 | Phase 6 |
| 8 | Destinations for all five menu items — Home, Shop, Collections, Our Story, Verse — and for the six `href="#"` links | NAV-03, NAV-04, NAV-05, DATA-05, SEO-09 | Phase 4 |
| 9 | What "Verse" is: a page, a homepage section, or a rotating scripture; and which scriptures beyond 2 Corinthians 5:7 are approved | NAV-04, UX-03 | Phase 4 |
| 10 | Whether an About / Our Story page exists, its long-form copy, and whether the nav item targets the page or the homepage section | UX-07, STORY-03 | Phase 7 |
| 11 | Whether a Best Sellers row launches, and which products qualify | UX-02 | Phase 6 |
| 12 | Whether a Social / Community section launches, and its content source: an Instagram feed app or uploaded images with usage permissions | UX-04 | Phase 16 |

### A.3 Brand assets and design decisions

| # | Decision required | Depends on | Gates |
|---|---|---|---|
| 13 | A vector wordmark (SVG/AI/EPS), or authorisation to derive one from `OG LOGO.psd` on the Desktop; also the intended wordmark size, since the build renders it at about half the mockup's relative scale | INV-05, ASSET-06, BRAND-05, NAV-08 | Phase 3 |
| 14 | Original photography or high-resolution masters for the hero (2000 px+), Our Story (2000 px+) and the three products (2000 px+ on the long edge); every current image is a mockup crop or an AI generation | ASSET-03, ASSET-04, ASSET-05, STORY-01 | Phase 3 |
| 15 | Confirmation of the extended palette beyond the three primaries: `#bdb6a8`, `#e9e4d8`, `#ebe6dc`, the olive `#4b5443`, and the scrim values | BRAND-01, BRAND-02, CSS-01 | **gates Phase 2** |
| 16 | Whether the 9-13 px tracked uppercase labels are brand-mandated on phones or may be raised to a 14/16 px floor | BRAND-04, RESP-11 | **gates Phase 2** |
| 17 | Target browser and device support matrix, which decides availability of `text-wrap:balance`, `aspect-ratio` and container queries | CSS-10, RESP-08 | **gates Phase 2** |
| 18 | Intended behaviour above 1440 px: full-bleed backgrounds with an inner container, or the current boxed canvas with dark gutters | RESP-14 | **gates Phase 2** |
| 19 | Formal confirmation of the three deliberate deviations from the mockup: the three-model hero photograph, the gold announcement globe, and the two-icon social set with circled badges | HERO-05, UI-04, ICON-03 | Phase 5 |
| 20 | Typeface confirmation and font hosting: whether Playfair Display, Jost and Kaushan Script are final, and whether Shopify's font library or self-hosting is preferred | SHOP-07, RISK-08, PERF-03 | Phase 2 |
| 21 | Descriptions of who and what the hero and story photographs show, so accurate alt text can be written | A11Y-09, HTML-11, SEO-08 | Phase 5 |

### A.4 Commercial policy and claims

| # | Decision required | Depends on | Gates |
|---|---|---|---|
| 22 | Shipping scope behind "Worldwide Shipping" and "Worldwide / Shipping Available": countries served, rates, duties handling, and the policy text | VAL-04, UX-05, DATA-09 | Phase 8 |
| 23 | Returns, refunds, privacy and terms text, or confirmation that Shopify admin policy pages will be used | FOOT-01, DATA-09 | Phase 8 |
| 24 | Legal entity name for the copyright line, plus contact email, phone and address for the footer | FOOT-01 | Phase 4 |
| 25 | Confirmation of the brand-origin statement "a Philippine streetwear brand built on faith, creativity, and community" | DATA-09 | Phase 7 |
| 26 | Live social profile URLs for Facebook and Instagram, and whether the TikTok and YouTube channels shown in the mockup exist | FOOT-02, DATA-08, UI-04 | Phase 4 |

### A.5 Store features and platform facts

| # | Decision required | Depends on | Gates |
|---|---|---|---|
| 27 | Customer accounts: enabled at launch or not, and classic vs new customer accounts | ECOM-05 | Phase 8 |
| 28 | Newsletter capture: wanted or not, provider, copy and incentive; plus wishlist, payment icons and whether a blog or gift cards are needed | FOOT-03, FOOT-04, ECOM-08 | Phase 8 |
| 29 | Shopify store facts: store URL or custom domain, plan, whether a store or development store already exists, who administers it, and the primary language and locale | SEO-03, SHOP-05, HTML-02 | Phase 10 |
| 30 | Homepage `<title>`, meta description and an Open Graph share image (about 1200x630), plus a square mark for the favicon; none of these assets or copy exists | SEO-01, SEO-02, SEO-04, SEO-05 | Phase 13 |

### A.6 Process decisions recommended alongside the above

These are not business facts but working arrangements the audit recommends resolving before Phase 2 begins: placing the project under version control and outside a sync-only folder, and formally freezing the Claude Design prototype as the design baseline so that the rebuild has a fixed target (DEBT-12, DEBT-13, INV-01, RISK-07).

## Appendix B. Evidence base

- Evidence files: evidence-render.md, measurements.md, inventory.tsv, css-html-stats.txt, bundle-sizes.txt, findings-verified.json (audit scratchpad).
- Renders: desktop-1440, laptop-1024, band-920, breakpoint-901, breakpoint-900, tablet-768, zoom200-720, mobile-430-true, mobile-390-true, mobile-375-true, wide-1920-fold, laptop-1366-fold, laptop-1280-fold.
- Approved mockup: uploads/God-Squad-Images/00-full-mockup-reference.webp (1024x1536).
- Duplicate issues merged during consolidation: none.

## Appendix C. Revision history

**2026-09-20 — initial issue.** Sections 2-16, 23, 25, 26 and 28 were produced through a draft, adversarial-review and revision cycle. Sections 17-22, 24, 27 and 29 were issued as first drafts because their reviewers could not complete. The executive summary, both matrix introductions, the Phase 2 scope, the final checklist and Appendix A were written by the audit lead.

**2026-09-21 — review pass.** The nine previously unreviewed sections (§17, §18, §19, §20, §21, §22, §24, §27, §29) were put through the same hostile-review and revision cycle as the rest of the report. Every claim in them was re-verified against the evidence base. The issue register, the priority matrix in §28, the dependency map in §30 and all counts quoted in §1 and §28 were regenerated from the corrected register. Corrections applied:

- **responsive-a11y** — BLOCKER (abridged CSS exhibit): 17.1 now reproduces all 26 rules of the 900px query and all 5 of the 520px query verbatim from God Squad Website.html lines 18-52, including the previously dropped `[data-r=hero-side] [data-r=rule]{display:none}` (line 26) and `[data-r=hero-side] [data-r=script]{margin-left:0!important;transform:rotate(-6deg)!important}` (line 27), and the full `[data-r=story-fade]` declaration in place of the `...` elision. The `/* no element carries data-r="pad" */` annotation was moved out of the code block into prose so the quote is strictly verbatim, and line 17's out-of-query `[data-r=nav-menu]{display:none}` is now noted. 17.1's tier summary also names the hero-side rule/script changes that lines 26-27 make.
- **responsive-a11y** — MAJOR (false zoom arithmetic): RESP-12's problem no longer claims a 1366 laptop at 150% gets the tablet layout. Verified: 1366/1.5 = 911 CSS px, above the 900px breakpoint. Replaced with the checked figures — 1366 stays on desktop at 150% (911 CSS px) and crosses only at the next zoom step, 175% (781 CSS px) — and 17.1 keeps the correct 1440/1.6 = 900 and 1800/2 = 900 statements.
- **responsive-a11y** — MAJOR (unsupported Reflow conformance claim): 17.12 no longer says "Reflow passes". It now states that 720 CSS px shows no horizontal scroll and text reflows, but SC 1.4.10 Reflow is defined at 320 CSS px (400% of 1280) and 320px was not captured, so Reflow is UNVERIFIED; SC 1.4.4 Resize Text was not tested either (findings-verified.json gaps: "Browser zoom at 200% and OS text scaling ... were not checked"). 320px added to the Phase 2 re-test list in 17.11 and to the untested list in 18.14.
- **responsive-a11y** — MAJOR (overflow masked by the wrapper): 17.11 now states that the outer wrapper sets overflow:hidden (God Squad Website.html line 55), so scrollWidth cannot reveal anything extending past the wrapper box and "none found" means "none visible through a mask"; the 17px "FAITH." excess at 920 is explained as sitting inside the section padding. The 17.14 row changed from "Horizontal overflow | KEEP | none found" to IMPROVE with the re-test instruction, and 17.2's closing line now says "no measurable horizontal overflow" with a pointer to the caveat. RESP-14's recommendation also flags not carrying overflow:hidden into the rebuild.
- **responsive-a11y** — MAJOR (563px misattributed to the side column): 17.4's copy stack paragraph and RESP-04's impact now follow the verified DOM split — heroCopy y=467 h=352 (eyebrow, 56px h1 on two lines, verse, rule, three-line tagline) and heroSide y=819 h=211 (orphaned side-column taglines), hero 970px, Shop at y=1029 (findings-verified.json RESPONSIVE-3). RESP-04's recommendation now states that hiding the side column recovers 211px, not 563px.
- **responsive-a11y** — MAJOR (landmark fact wrong): 18.2 no longer says "a landmark list reads four unnamed regions". Corrected to: the four section elements have no accessible name, so they are exposed as generic containers and do not appear in the landmark list at all; the only landmarks are the unnamed nav inside the hero and the footer as contentinfo (verified: the footer at line 153 is a direct child of the 1440 wrapper, not nested in a sectioning element), with no banner and no main. Folded into A11Y-02's problem, impact, recommendation and evidence, and echoed in 18.11.
- **responsive-a11y** — MAJOR (alt tally did not match its own table): 18.4's net line now reads 4 correct / 4 wrong / 3 redundant / 1 generic = 8 of 12 needing work, against the 12 img tags in css-html-stats.txt. The two social rows and the product-template row were relabelled REDUNDANT (they were marked IMPROVE while being counted as redundant). A11Y-09's problem and impact rewritten to 8 of 12, and the 18.14 row updated from "6 of 12" to "8 of 12".
- **responsive-a11y** — MAJOR (Level A failures unscored): added A11Y-11 "Missing lang and empty `<title>`", HIGH / P1 / PHASE 10 — SHOPIFY THEME CONVERSION, evidenced by css-html-stats.txt (`<title>`: ABSENT; lang attr: ABSENT), evidence-render.md and findings-verified.json C7, cross-referencing the SEO register rather than deferring outright. 18.1 rewritten to name SC 3.1.1 and SC 2.4.2 as the only Level A failures on the page, 18.11 gained a bullet for them, and they appear in the 18.14 table and in the classification line (document-level semantics REBUILD).
- **responsive-a11y** — MAJOR (category error + missing rows in 17.14): deleted the "Headless mobile-375.png / mobile-375-raw.png | REMOVE (from evidence)" row — the KEEP/IMPROVE/REBUILD/REPLACE/REMOVE labels classify site components, not the audit's own working files, and REMOVE reads as an instruction to delete in an inspection-only phase. The caution survives as a prose footnote under the table (FIDELITY-10). Added the two missing rows: "Mobile navigation (<=900px) | REBUILD" (RESP-12; NAV register) and "Layout above 1440px | REBUILD" (RESP-14).
- **responsive-a11y** — MAJOR (collision wrongly attributed to the missing tier): removed the side-column/back-print collision from RESP-08's problem and dropped the C17 citation from its evidence; RESP-08 now covers only the grid wrapping at 920 and the price misalignment at 1024. The collision is reported in 17.4 as a desktop-wide hero-composition item at 1024-1440 (C17, title "Right hero column collides with the model's back print at 1024-1440"), also visible at 920 (band-920.png; evidence-render.md), owned by the hero register, with its contrast unmeasured.
- **responsive-a11y** — MINOR (arithmetic): 17.10's phone rhythm now reads "announce 59 + hero 970 + drop 1,695 + story 797 + values 698 + footer 164 ≈ 4,382px measured docH (the section boxes sum to 4,383; 1px of rounding)" citing measurements.md 375 and findings-verified.json RESPONSIVE-10.
- **responsive-a11y** — MINOR (two-line lockup width): RESP-07's problem and 17.2's and 17.4's parallel statements now say the approved two-line lockup appears only below about 540px, captured at 375, 390 and 430, per findings-verified.json gaps ("the headline stays on one line at 56px down to at least 560px ... the two-line lockup only appears below roughly 540px"). RESP-07's evidence cites that gaps entry alongside FIDELITY-2.
- **responsive-a11y** — MINOR (wrap recorded at 920, not 901): dropped the "names wrap; View All wraps to 2 lines" note from the 901 row of 17.2 (measurements.md 901 carries only "3 | ~230"), added a footnote that wrapping is first recorded at 920 and the onset between 901 and 920 is unverified, and rewrote 17.5 accordingly (920: eyebrow, names and View All wrap; 1024: tee name wraps and its price drops). Chose the "drop the note" option rather than re-inspecting breakpoint-901.png, to avoid introducing an unverified visual claim.
- **responsive-a11y** — MINOR (type inventory): 17.9 rebuilt as an itemised list with line numbers — 14px/.3em hero verse and taglines (lines 85, 87, 93), 14px untracked prices (line 113, verified `font-size:14px;font-weight:600` with no letter-spacing), 13px/.3em eyebrows (83, 100, 129), 13px/.24em New Drop copy (103), 13px/.22em value titles (146) — so all five 13px and all four 14px uses are accounted for against css-html-stats.txt. RESP-11's problem and evidence updated to match. Also corrected "three heading clamps" to four (h1, New Drop h2, story h2, script).
- **responsive-a11y** — MINOR (nav link size): 18.9's Nav links row changed from "~14px text" to "12px text, 44px gaps (line 70)", verified at God Squad Website.html line 70 (`font-size:12px;letter-spacing:.2em`), now consistent with 17.3 and 17.9.
- **responsive-a11y** — MINOR (C11 correction respected): 17.11 now reads "scrollWidth equals clientWidth at 375, 768, 1024 and 1440 — that is, innerWidth minus the scrollbar where one is present (C11 correction)".
- **responsive-a11y** — MINOR (contrast range truncated): A11Y-03's problem and the 18.14 row now use 2.4-2.9:1 per findings-verified.json critic addition 1 ("Effective contrast is 2.4-2.9:1"); the per-link composited figures (2.8 / 2.4 / 2.4 at 1440) stay in the 18.8 table, and 18.8 gained a sentence stating the 2.4-2.9 span across 1440 and 1024. A11Y-03's evidence quotes the source range.
- **responsive-a11y** — MINOR (fold-only rows not labelled): 17.2 now carries an explicit qualification that the 1280x720, 1366x768 and 1920 rows are first-screen captures only, that the blank cells mean "not measured" rather than "nothing there", and that 1280/1366 fall inside the 1024-1440 desktop tier with no rule change between them (findings-verified.json gaps, TECHNICAL-8). RESP-13's and RESP-14's evidence note the same.
- **responsive-a11y** — MINOR (platform mechanism missing from responsive recommendations): RESP-10's recommendation now names a `<picture>` built from a separate mobile image setting on the hero section, rendered with image_url: width: … and image_tag, so the phone crop is its own theme-editor image rather than a CSS crop; RESP-02's now names image_url: width: filters plus image_tag with an explicit sizes attribute. 17.14's "Hero image delivery" row reworded to match.
- **responsive-a11y** — No review finding was rejected; all nineteen were verified against the evidence before application. No issue was removed and no id was renumbered; the register grew from 24 to 25 with the addition of A11Y-11.
- **seo-perf-assets-icons** — Section 20 hero bullet: corrected the inverted crop figure. I re-derived the geometry myself — line 21 makes the hero an in-flow box of height max(62vw,320px) below 900px and line 65 sets object-fit:cover, so at 375 the 1672x941 file draws at 320/941 = 0.34 scale, a scaled width of ~569 px of which 375 px (~66%) is visible; 34% is the fraction cropped away. Confirmed measurements.md contains no 34% figure, so the citation now points at God Squad Website.html lines 21 and 65 alongside measurements.md 375 (answers major finding 1).
- **seo-perf-assets-icons** — PERF-01 impact: "to show a third of the picture" replaced with "to show about two thirds of the picture, the 375x320 cover crop discarding roughly 34% of the scaled width", and God Squad Website.html lines 21 and 65 added to the evidence field (answers major finding 2).
- **seo-perf-assets-icons** — Section 21 image-quality table, hero-group row: the phone cell now states the 0.34 draw scale and the ~34% crop instead of leaving "limited by composition" unquantified (consequential fix from findings 1 and 2).
- **seo-perf-assets-icons** — Favicon 404 hedged in all three places the review named — the section 19 scope paragraph, the section 19 Favicon table row and SEO-05 — and SEO-05's "wasted round trip on every page view" impact clause dropped. Verified findings-verified.json gaps records "neither the headless capture nor the Browser pane requested /favicon.ico" (answers major finding 3).
- **seo-perf-assets-icons** — Section 20's render-chain paragraph additionally hedged: it asserted the same favicon 404 as observed ("and one for /favicon.ico"). It now reads as a predicted third 404 exercised by neither capture, while the two template-placeholder 404s stay stated as observed (C3). Not in the review list, but it is the same unverified claim and would have contradicted the three corrected places.
- **seo-perf-assets-icons** — Section 21 delivery strategy: corrected the image_tag fact. `image_url: width:` alone emits neither srcset nor sizes; the bullet now passes `widths:` and `sizes:` explicitly with a worked Liquid example (answers major finding 4).
- **seo-perf-assets-icons** — AVIF dropped from all three places: the section 21 delivery strategy ("the CDN negotiates WebP automatically... AVIF is not a Shopify CDN output format"), section 20's requirements bullet ("as WebP with a width ladder") and PERF-01's recommendation ("responsive WebP derivatives"). Row 10 of the classification table also read "CDN WebP/AVIF derivatives" and was corrected for the same reason (answers major finding 5).
- **seo-perf-assets-icons** — Section 21 inventory summary: "Nothing was deleted or renamed" replaced with an explicit statement that no file was created, renamed or deleted by this audit, and that the 2026-09-20 15:34 rename was the owner's own deliberate change with content unchanged. Row 1's reason now names the owner as the agent of the rename (answers major finding 6).
- **seo-perf-assets-icons** — Section 21 inventory summary: now states 44 site files at 17,185,754 B and names the two excluded non-site files — .claude/launch.json (228 B, dev-server tooling added by the audit lead) and PHASE-1-WEBSITE-AUDIT.md (493,032 B, this report) — with the 46-file / 17,679,014 B folder total. I verified both directly against the folder: 46 files, 17,679,014 B, and 17,679,014 - 228 - 493,032 = 17,185,754 (answers major finding 7).
- **seo-perf-assets-icons** — One folder figure used throughout: section 20 now reads "The 17.2 MB (17,185,754 B) project folder" and ASSET-08 "A 17.2 MB working folder serves a 2.5 MB page", matching ASSET-01. The 16.9 MB figure (16.9 MiB of the whole folder including this report) is gone (answers minor finding 8).
- **seo-perf-assets-icons** — Section 22 problem 1: "2.5-3.4x" replaced with "only 2.5x (110 px canvas height drawn at 44 px; widths 130/150/130/110 drawn at 52/60/52/44)". Verified against findings-verified.json TECHNICAL-6 and inventory.tsv dims; 3.4x mixed the community canvas width with the rendered height (answers minor finding 9).
- **seo-perf-assets-icons** — Section 20 icons bullet: the canvas range is now "four canvases (110x110, 130x110, 150x110, 130x130)", which includes the 130x130 Facebook and Instagram files the old two-value range excluded (answers minor finding 10).
- **seo-perf-assets-icons** — ICON-05 evidence: the per-icon render sizes are now cited to findings-verified.json TECHNICAL-6, not evidence-render.md, which records only "drawn at 16-44 px". Confirmed TECHNICAL-6's evidence field carries crown 52x44, community 60x44, diamond 52x44 and icon-globe 16x16 / 44x44 (answers minor finding 11).
- **seo-perf-assets-icons** — Section 22 problem 4 carried the identical misattribution (rendered widths cited to evidence-render.md) and was corrected the same way. Not in the review list; it is finding 11's error repeated in the prose.
- **seo-perf-assets-icons** — Section 20 lazy-loading paragraph: the absolute-positioning claim is now scoped to above 900px, with the below-900px in-flow box of height max(62vw,320px) stated and cited to God Squad Website.html line 21. The conclusion (height reserved either way) is unchanged (answers minor finding 12).
- **seo-perf-assets-icons** — Row 22 (images/logo.png): Role changed from "WEB (unused)" to MOCKUP. Verified inventory.tsv shows referenced_by = README (the loose name match, not a reference) and the file is byte-identical to uploads/God-Squad-Images/06-logo.png, which row 43 already classes MOCKUP. Class stays ARCHIVE; class totals unchanged. The Mockup-assets roles bullet now names it (answers minor finding 13).
- **seo-perf-assets-icons** — The Asset-roles "Temporary/generated" bullet now names images/icons-sprite.png and images/social-sprite.png, so the two heaviest TEMP files belong to a role group as spec section 18 requires (answers minor finding 14).
- **seo-perf-assets-icons** — Row 9 (images/WHITE FONT LOGO.png): the double class label is gone. The Reason cell states class REPLACE with the trimmed-PNG fallback framed as a Phase 3 decision, not a second class, and ASSET-06's recommendation was aligned to the same wording. Class totals (REPLACE 14, OPTIMIZE 1) unchanged (answers minor finding 15).
- **seo-perf-assets-icons** — SEO-10's problem rewritten to separate the two failure modes — a client that does not run the script reads the raw template with literal {{ p.name }} and broken {{ p.img }} images; one that runs it but cannot reach unpkg gets a blank page — with findings-verified.json C13 and its critic addition added to the evidence. Section 19 amended to "indexes raw template text" and given the same two-mode explanation (answers minor finding 16).
- **seo-perf-assets-icons** — Rows 34, 35 and 36: the per-file decision attributions are gone. Row 34 carries one collective reason citing evidence-render.md's editor history and stating that which screenshot shows which decision is not recorded; rows 35 and 36 refer to it. I did not open the screenshots, so the collective option was taken rather than claiming a viewing (answers minor finding 17).
- **seo-perf-assets-icons** — The hero preload parenthetical is corrected: `preload: true` emits `<link rel="preload" as="image">` and does not set fetch priority; fetchpriority="high" must be written on the img itself. PERF-02's recommendation and section 20's requirements bullet were aligned, since both previously implied one setting delivered both (answers minor finding 18 on preload).
- **seo-perf-assets-icons** — ASSET-05's provenance hedged in the problem and impact, with the recommendation now asking the business to confirm how the image was produced. Section 21's asset-roles bullet gained "unconfirmed by the business"; section 21's existing hedge ("according to its upload filename") was already correct and is kept (answers the ASSET-05 finding).
- **seo-perf-assets-icons** — Section 19 and SEO-04 / SEO-06 / ASSET-08 changed from "the 44 files" to "the 44 site files" so the file-count statements agree with the corrected section 21 inventory summary.
- **seo-perf-assets-icons** — PERF-03's recommendation now carries the Google-fonts privacy question as BUSINESS INFORMATION REQUIRED, which section 20 stated but the register did not. No other field changed.
- **seo-perf-assets-icons** — ICON-01's problem tightened from "110-150 px canvases" to the four exact canvases, for consistency with the section 20 fix. Wording only; meaning, severity, priority and phase unchanged.
- **seo-perf-assets-icons** — No issue was added, removed or renumbered. The register is the same 30 ids: SEO-01 to SEO-11, PERF-01 to PERF-06, ASSET-01 to ASSET-08, ICON-01 to ICON-05.
- **seo-perf-assets-icons** — No review finding was rejected. All 18 were checked against the evidence before being applied; the two crop-geometry findings and the 46-file folder total were re-derived from the source files and the folder itself rather than accepted on the review's word.
- **shopify-risk** — BLOCKER (fabricated footer link groups, §29.7): removed SHOP / ABOUT / HELP / FOLLOW entirely. The footer block row now states that no link groups exist in the prototype (verified: lines 153-166 hold the logo, 'Different People. Same Purpose.', two href="#" social links, a divider and 'A Brighter Tomorrow') or in the mockup (ADD-7), so headings and contents are both BUSINESS INFORMATION REQUIRED and the blocks ship empty.
- **shopify-risk** — MAJOR (§24.2 row 9 stated the same fabrication as current fact): rewritten to the four value tiles (data lines 179-183), the hero side captions (lines 91-93) and the two announcement messages (lines 59-60) as natural blocks, with footer link-list blocks flagged ADD LATER + BUSINESS INFORMATION REQUIRED. All line references re-read in God Squad Website.html.
- **shopify-risk** — MAJOR (invalid Shopify structure in the §29.1 tree): assets/fonts/*.woff2 replaced with flat file names (jost-400/500/600, kaushan-script-400, playfair-display-900) plus an explicit note that assets/ has no subfolders, matching §24.2 row 12. Playfair Display 900 added and 700 excluded per evidence-render.md (700 requested but unused, C12).
- **shopify-risk** — MAJOR (FIDELITY-2 mis-stated as 375-only): RISK-05's trigger now reads 'below roughly 540 px', with the h1 at 56 px on two lines at 375 (327x99), 390 (342x99) and 430 (382x99), one line at 768 and 900 and three lines from 901 up (measurements.md; findings-verified.json gaps refinement).
- **shopify-risk** — MAJOR (untraceable ADD-* citations): added a citation note in §24.2 defining ADD-1..ADD-8 as the eight findings-verified.json critic_additions in file order, each glossed by title, and stating that the file gives them no ids. §27.1 back-references that definition, and every register evidence field that used an ADD id now names the addition's subject as well.
- **shopify-risk** — MAJOR (Phase 15 could not supply pass criteria to Phases 9/12/14): RISK-13's owning phase moved to PHASE 2 — DESIGN SYSTEM in both the table and the issue record, reworded so Phase 2 defines the QA matrix and Phase 15 executes it; §27.4's RISK-05 x RISK-13 bullet updated to match.
- **shopify-risk** — MAJOR (three errors in the SHOP-03 sentence, repeated in §24.2 row 13): corrected to brand colours across the 77 inline styles and the 2,916 B `<style>` (all-sources counts #0d0c0a x14, #d8c08a x10, #f3efe6 x9, #bdb6a8 x3; inline-only background:#0d0c0a x6, background:#f3efe6 x6, color:#d8c08a x5), fonts hardcoded in the `<style>` and the line 12 Google Fonts link, the logo a hardcoded `<img src>` (lines 69, 155), and no social URLs at all (both links href="#", BUSINESS INFORMATION REQUIRED). Applied in SHOP-03, §24.2 row 13 and §29.6/§29.9.
- **shopify-risk** — MAJOR (wrong provenance for .thumbnail and .claude/launch.json): all three places (§24.5, §29.1, SHOP-06) now say 'non-theme files … the editor-generated .thumbnail preview, and .claude/launch.json — dev-server tooling added by the audit lead, not a site file', per evidence-render.md.
- **shopify-risk** — MINOR (RISK-10 owning phase contradicted §27.4): moved to PHASE 3 — ASSET PREPARATION in the table and the issue record, with the mitigation noting Phase 2 sets the budget and Phase 12 confirms it; §27.4's RISK-10 x RISK-01 bullet now states why Phase 3 owns it.
- **shopify-risk** — MINOR (wrong mobile metric): '26 !important overrides' replaced with '31 rules across two queries (26 in max-width:900px, 5 in max-width:520px)' overriding with !important (55 in the `<style>`, none inline) per css-html-stats.txt, in the RISK-05 trigger and the RISK-05 issue record. The review's suggested phrase 'almost all carrying !important' was softened to 'override … with !important' because the per-rule split is not in the evidence.
- **shopify-risk** — MINOR (overbroad missing-template claim): §29.5's closing sentence now qualifies that templates/customers/* apply only under classic customer accounts (BUSINESS DECISION REQUIRED, §24.2 row 22) and password/gift_card only when those features are enabled; §24.2 row 22 and SHOP-09 carry the same qualification.
- **shopify-risk** — MINOR (§29.6 vs §29.7 contradiction on logo sizing): §29.6 now specifies logo, logo_height_desktop (78), logo_height_mobile (56), favicon, with the reason (line 69 height:78px;width:auto, line 155 height:56px;width:auto), matching §29.7's header row.
- **shopify-risk** — MINOR (template count inconsistent): standardised on 'one designed page and at least nine undesigned storefront templates (product, collection, list-collections, cart, search, page, page.our-story, 404, password), rising to about twenty with the seven customer templates, gift card, blog and article' in §27.3, §29.5, RISK-06 and SHOP-09.
- **shopify-risk** — MINOR (wrong labels on §24.2 rows 15-16): row 15 Theme CSS is now Shopify need REQUIRED / REBUILD, row 16 Theme JavaScript is REQUIRED / REPLACE (its own 'what must change' cell recommends replacement vanilla modules, not removal).
- **shopify-risk** — MINOR (ADD-1 contrast basis unstated and a fourth failing link omitted): RISK-14's trigger, the RISK-14 issue record and §29.2 now give both measurements — 2.4-2.9:1 composited over sampled photo luminance (ADD-1) and 4.6-5.7:1 median / 2.4-2.5:1 over the brightest 2% from the render's pixels (evidence-render.md) — plus the gold Home link at ~3.5:1 at 1024 and the 4.5:1 AA threshold.
- **shopify-risk** — MINOR (passive rename sentence): §24.1 now reads 'The owner renamed the file … on 2026-09-20 at 15:34; the content is unchanged and no Phase 1 work touched the file', with the spec's prohibition cited (PHASE-1-SPEC.md line 30); RISK-07's trigger names the owner too.
- **shopify-risk** — MINOR (incomplete product object list): §24.2 row 18 now lists product.title, product.price, product.featured_image, product.images, product.url, product.variants, product.available per spec §9 (PHASE-1-SPEC.md line 151), with a note that the card needs product.images for secondary media.
- **shopify-risk** — MINOR (assets row carried no numbers): §24.2 row 12 now cites 44 files totalling 17,185,754 B, 17 referenced (2,491,648 B) and 9 md5 duplicate groups accounting for 11 redundant copies (inventory.tsv; measurements.md); SHOP-06's impact uses the same figures instead of the looser '14 MB'.
- **shopify-risk** — Consistency follow-through on the blocker (not in the review list): §29.3's footer row previously listed 'link-list blocks, legal line' as sourced from lines 153-166. Corrected to mark link lists, the legal/copyright line and payment icons as additions that do not exist today, and a row was added to the §29.9 mapping table recording them as ADD LATER / BUSINESS INFORMATION REQUIRED.
- **shopify-risk** — Accuracy tightening in §24.4 (not in the review list): '55 !important overrides keyed on [data-r=...], lines 17-52' replaced with '55 !important declarations across 34 [data-r=…] selectors inside the 2,916 B `<style>`, none inline' — the counts are in css-html-stats.txt, whereas the line range 17-52 was not verifiable and conflicted with the 13-53 range used in §29.9.
- **shopify-risk** — Known-correction sweep applied throughout: style-hover is described as working (support.js generates .scp0:hover/.scp1:hover, §24.2 row 6), the page is described as booting from file:// with only the unpkg React fetch needing the network (§24.1, RISK-04, §27.3), and no clipped ~490 px capture (mobile-375.png / mobile-375-raw.png) is cited anywhere.
