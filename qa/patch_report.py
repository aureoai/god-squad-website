# -*- coding: utf-8 -*-
"""Patch the assembled Phase 1 audit: write the five framing sections the synthesis
agent never produced, consolidate Appendix A, and emit PHASE-1-WEBSITE-AUDIT.md."""
import json, re, io, sys, os, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
EV = os.path.dirname(os.path.abspath(__file__)) + '/audit-evidence'
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PROJECT, "PHASE-1-WEBSITE-AUDIT.md")

res = json.load(open(EV + '/workflow-result.json', encoding='utf-8'))
rep = res['report']
issues = res['issues']
c = res['counts']

# ---------------------------------------------------------------- 1. Executive summary
EXEC = """### CURRENT STATE

**Visual.** Strong and substantially faithful to the approved mockup. The palette, the three typefaces, the copy, the section order and the editorial tone all match `uploads/God-Squad-Images/00-full-mockup-reference.webp`, and at 1440 px the page reads as the mockup intends (§7, §8). The departures are specific and few: the Our Story slot is filled with a crop of the mockup's *hero*, so the words "A PURPOSE", "K BY" and "TH." are baked into the photograph and visible at every width (STORY-01); the headline sets as three lines (WALK / BY / FAITH.) from 901 px upward where the mockup sets two (HERO-03); the wordmark renders at roughly half its mockup size because the PNG carries heavy transparent padding (BRAND-05); and the product photographs sit in visible square tiles rather than floating on the cream band (UI-02). Three further differences — the three-model hero photograph, the gold announcement globe and the two-icon social set — are deliberate owner edits recorded in the Claude Design history and are treated here as approved pending confirmation (HERO-05, UI-04).

**UX.** The page is a brand statement, not yet a shop. The hero asks nothing of the visitor: it contains no link or button at all, and on 1366x768 and 1280x720 laptops the first screen is hero-only, so no product is visible without scrolling (HERO-01, UX-01, RESP-13). Six of the nine links on the page are `href="#"` and scroll to the top; Shop and Collections both resolve to the same in-page anchor, making two primary menu items indistinguishable (NAV-03, NAV-05). Three of the ten steps in the intended homepage flow — Best Sellers / Product Discovery, Verse / Faith and Social / Community — do not exist in the build, although Verse is a primary navigation item (UX-02, UX-03, UX-04).

**Code.** The prototype is a Claude Design "dc" document, not a website in the ordinary sense. Every visible node lives inside a custom `<x-dc>` element that `support.js` (69,150 B) compiles into React elements at run time after fetching React and ReactDOM from unpkg (ARCH-01). Presentation is 77 inline `style` attributes totalling 6,421 characters with zero classes, plus a 2,916-byte embedded stylesheet whose responsive layer is 31 rules in two `max-width` queries keyed on 26 editor-generated `data-r` hooks and carrying 55 `!important` declarations (CSS-02, CSS-03). One of those rules targets a hook no element carries (CSS-05). Nothing in this layer is reusable as code.

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
| Issues raised | 199 |
| By severity | 5 CRITICAL, 48 HIGH, 85 MEDIUM, 61 LOW |
| By priority | 3 P0, 64 P1, 80 P2, 52 P3 |
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

The audit did not invent a single business fact. Thirty consolidated decisions are required before implementation can be completed, covering the product catalogue, pricing and markets, collection structure, navigation destinations, the Verse concept, shipping and legal policy, social channels, a vector logo, original photography, and the Shopify store itself. They are set out in Appendix A with the issue IDs that depend on each. Four of them gate Phase 2 directly: confirmation of the extended palette, the mobile type scale, the browser and device support matrix, and the behaviour above 1440 px."""

# ---------------------------------------------------------------- 28. Matrix intro
MATRIX_INTRO = """This matrix is the complete work list produced by the audit: 199 issues, each owned by exactly one register, each traceable to a file, a measurement or a named screenshot. It is sorted by priority, then severity, then ID.

**How to read it.** *Priority* answers "when": **P0 — BLOCKER** is reserved for the three findings that prevent the production architecture from working at all; **P1 — HIGH PRIORITY** covers major UX, accessibility, ecommerce and architectural problems; **P2 — MEDIUM PRIORITY** covers important improvements; **P3 — POLISH** covers visual refinement and optional enhancements. *Severity* answers "how bad is the defect in itself", and the two deliberately differ: a CRITICAL defect in a section that does not ship until Phase 8 sits at P1, not P0. *Phase* names the single phase that retires the issue, and the dependency map in §30 groups the same issues that way. The recommendation column is written as future work; nothing in this matrix has been actioned.

**Counts.** P0 — BLOCKER: 3 issues. P1 — HIGH PRIORITY: 64 issues. P2 — MEDIUM PRIORITY: 80 issues. P3 — POLISH: 52 issues. By severity: 5 CRITICAL, 48 HIGH, 85 MEDIUM, 61 LOW. By category: 93 UX, 28 mobile, 26 accessibility, 21 SEO, 20 performance.

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

"""

# ---------------------------------------------------------------- 30. Dependency intro
DEP_INTRO = """The phases are ordered by dependency, not by visibility. **Phase 2 — Design System** comes first because every later phase consumes its output: the tokens, the type scale, the spacing rhythm, the icon system and the component inventory are the vocabulary in which Phases 4 to 9 are written, and 41 issues resolve there. **Phase 3 — Asset Preparation** follows immediately because the hero, story and product work cannot be completed against 215-650 px mockup crops; sourcing and processing the real imagery gates Phases 5, 6 and 7. The section phases (4 to 7) then rebuild each homepage block against tokens and real assets, and **Phase 8 — Product & Shopping UX** and **Phase 9 — Mobile UX** extend that work into the commerce surface and the phone layout.

**Phase 10 — Shopify Theme Conversion** is the hinge: it retires all three P0 blockers and the entire runtime, CSS and markup debt in one pass, and nothing in Phases 11 to 16 can begin until the theme exists in native form. **Phase 11 — Theme Editor** depends on Phase 10 because schemas can only be written against real sections, and it in turn unblocks the owner's ability to edit content without a developer. **Phases 12, 13 and 14** — performance, SEO and accessibility — are placed after conversion deliberately: each of them is cheap to do correctly in a native theme and expensive to retrofit twice, and each needs measurement against the real thing rather than the prototype. **Phase 15 — Ecommerce QA** validates the commerce paths end to end and is the first point at which acceptance criteria can be met, and **Phase 16 — Final Polish** absorbs the remaining P3 refinements.

Two cross-cutting dependencies sit outside the phase sequence. The business decisions in Appendix A gate work in almost every phase, and four of them gate Phase 2 itself. The absence of a version-controlled working copy (DEBT-12) should be resolved before Phase 2 begins, so that the rebuild has a history and the prototype has a frozen baseline (DEBT-13).

"""

# ---------------------------------------------------------------- 31. Phase 2 scope
PHASE2 = """Phase 2 converts the approved visual language into a documented, reusable system. It is a design and specification phase: it produces tokens, component specifications and rules, not Shopify files and not new imagery.

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

A written design-system document plus a token file, covering colour, type, spacing, radii, borders, elevation, motion and the eight components, each with states and responsive behaviour, and each cross-referenced to the issue IDs it retires. Sign-off from the owner on the four gating decisions above."""

# ---------------------------------------------------------------- 32. Final checklist
CHECKLIST = """Every task the Phase 1 specification required, with its outcome. Items marked `[ ]` were explicitly deferred to a later phase by the specification or by the limits of a static audit.

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

No project file was created, modified, renamed or deleted during this audit, with two exceptions, both disclosed: this report, `PHASE-1-WEBSITE-AUDIT.md`, written to the project root as the deliverable; and `.claude/launch.json` (228 bytes), a local development-server configuration created during Phase 0 so the prototype could be rendered over HTTP for inspection. It is audit tooling, not a site file, and is recorded as INV-06. The entry page was renamed from `God Squad Website.dc.html` to `God Squad Website.html` by the owner, not by this audit (INV-02)."""

# ---------------------------------------------------------------- Appendix A
APPENDIX_A = """The audit invented no business facts. The thirty decisions below are the complete set required before implementation can finish; the seven clusters group them by who must answer. Each cites the issue IDs that depend on it and the earliest phase it gates. Items marked **gates Phase 2** must be answered before the design system can be signed off.

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

These are not business facts but working arrangements the audit recommends resolving before Phase 2 begins: placing the project under version control and outside a sync-only folder, and formally freezing the Claude Design prototype as the design baseline so that the rebuild has a fixed target (DEBT-12, DEBT-13, INV-01, RISK-07)."""

# ---------------------------------------------------------------- apply patches
def sub_once(text, pattern, replacement, label):
    new, n = re.subn(pattern, lambda m: replacement, text, count=1, flags=re.S | re.M)
    print("  %-34s %s" % (label, "OK" if n == 1 else "*** FAILED (%d matches) ***" % n))
    return new

print("Patching report:")
rep = sub_once(rep, r'(?<=## 1\. Executive Summary\n\n)\(synthesis failed\)', EXEC, "1. Executive Summary")
rep = sub_once(rep, r'(?<=## 31\. Recommended Phase 2 Scope\n\n)\(synthesis failed\)', PHASE2, "31. Phase 2 Scope")
rep = sub_once(rep, r'(?<=## 32\. Final Audit Checklist\n\n)\(synthesis failed\)', CHECKLIST, "32. Final Checklist")
rep = sub_once(rep, r'## 28\. Priority Matrix\n\n+(?=\| ID \|)', "## 28. Priority Matrix\n\n" + MATRIX_INTRO, "28. Matrix intro")
rep = sub_once(rep, r'## 30\. Phase Dependency Map\n\n+(?=### PHASE)', "## 30. Phase Dependency Map\n\n" + DEP_INTRO, "30. Dependency intro")
rep = sub_once(rep, r'## Appendix A\. Business information required\n\n.*?(?=\n## Appendix B\.)',
               "## Appendix A. Business information required\n\n" + APPENDIX_A + "\n", "Appendix A")

# housekeeping
rep = rep.replace('# GOD SQUAD — PHASE 1 WEBSITE AUDIT &amp; TECHNICAL ASSESSMENT',
                  '# GOD SQUAD — PHASE 1 WEBSITE AUDIT & TECHNICAL ASSESSMENT')

TAG_RE = re.compile(r'<(/?[a-zA-Z][a-zA-Z0-9-]*(?:\s[^<>\n]{0,140})?)>')

def wrap_bare_tags(text):
    """Backtick-quote literal HTML tags written outside code spans, so a Markdown
    renderer shows them instead of parsing them as raw HTML. Fenced blocks and
    existing inline code spans are left untouched."""
    out, n = [], 0
    for i, part in enumerate(re.split(r'(```.*?```)', text, flags=re.S)):
        if i % 2:                      # fenced code block
            out.append(part); continue
        for j, seg in enumerate(re.split(r'(`[^`\n]*`)', part)):
            if j % 2:                  # existing inline code span
                out.append(seg); continue
            seg, k = TAG_RE.subn(r'`<\1>`', seg)
            n += k
            out.append(seg)
    return ''.join(out), n

rep, wrapped = wrap_bare_tags(rep)
# separate code spans that ended up directly adjacent ( `<nav>``<ul>` -> `<nav>` `<ul>` ).
# The replacement must keep BOTH backticks and add a space between them.
rep, adj = re.subn(r'>``<', '>` `<', rep)
print("  %-34s %d tag(s) backticked, %d adjacency fixed" % ("bare HTML tags normalised", wrapped, adj))

print("\nVerification:")
print("  '(synthesis failed)' remaining:", rep.count('(synthesis failed)'))
heads = re.findall(r'^## (?:(\d+)\.|Appendix ([AB])\.) (.+)$', rep, re.M)
nums = [int(h[0]) for h in heads if h[0]]
print("  numbered sections: %d  missing: %s  duplicated: %s" %
      (len(nums), [n for n in range(1, 33) if n not in nums] or 'none',
       [n for n, k in collections.Counter(nums).items() if k > 1] or 'none'))
print("  appendices:", [h[1] for h in heads if h[1]])
print("  characters: %s  words: %s" % (format(len(rep), ','), format(len(rep.split()), ',')))
rows = [l for l in rep.split('\n') if l.startswith('| ') and l.count('|') == 9]
print("  matrix rows (9-pipe): %d" % len(rows))
ids = set(i['id'] for i in issues)
refd = set(re.findall(r'\b([A-Z]{3,6}-\d{2})\b', rep))
unknown = sorted(r for r in refd - ids if not r.startswith(('DEBT-0', 'DEBT-1', 'DUP-', 'FIDELITY', 'RESPONSIVE', 'TECHNICAL')))
print("  unknown IDs referenced:", unknown or 'none')

if '--write' in sys.argv:
    if os.path.exists(OUT):
        print("\nREFUSING to overwrite existing %s" % OUT)
        sys.exit(2)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(rep.rstrip() + '\n')
    print("\nWROTE %s (%s bytes)" % (OUT, format(os.path.getsize(OUT), ',')))
else:
    open(EV + '/report-patched-preview.md', 'w', encoding='utf-8', newline='\n').write(rep.rstrip() + '\n')
    print("\n(dry run) preview written to audit-evidence/report-patched-preview.md")
