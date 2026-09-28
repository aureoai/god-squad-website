# GOD SQUAD — PHASE 4 HEADER & NAVIGATION

**Project:** God Squad Premium Faith-Driven Streetwear  
**Phase:** 4 — Header & Navigation  
**Date:** 2026-09-22  
**Target:** Shopify Online Store 2.0  
**Predecessors:** Phase 0 foundation, Phase 1 audit, Phase 2 design system, Phase 3 asset system

---

## 0. Note on the specification

The Phase 4 specification as received ends part-way through section 3. Phases 1, 2 and 3 each ran to more than forty sections, including deliverables, completion criteria and a terminal report format. Sections 1 to 3 are complete and unambiguous in themselves: section 2 fixes the scope as thirteen numbered items, and section 3 fixes the target file list. The work below is built strictly to those, and the document follows the structure of the previous phases. If further sections exist, they have not been applied.

Two consequences are recorded rather than guessed:

- Behaviours the specification does not name — whether the header sticks, whether it overlays the first section — are exposed as theme settings with the approved design as the default, rather than being decided silently.
- The completion checklist in section 9 is derived from the thirteen scope items, not from a supplied checklist.

---

## 1. What was built

This is the first phase to produce production code. Before it, the project contained a prototype and four documents; it contained no theme.

| File | Bytes | Purpose |
|---|---|---|
| `layout/theme.liquid` | 3,809 | Minimal layout: head, header group, content slot |
| `sections/header-group.json` | 893 | The header section group |
| `sections/announcement-bar.liquid` | 4,008 | Announcement bar, messages as blocks |
| `sections/header.liquid` | 9,753 | Header, navigation, utility, mobile panel |
| `snippets/icon-search.liquid` | 772 | Inline SVG, `currentColor` |
| `snippets/icon-account.liquid` | 708 | Inline SVG |
| `snippets/icon-cart.liquid` | 856 | Inline SVG |
| `snippets/icon-menu.liquid` | 795 | Inline SVG |
| `snippets/icon-close.liquid` | 759 | Inline SVG |
| `assets/design-tokens.css` | 25,275 | Theme copy of the Phase 2 tokens |
| `assets/header.css` | 11,404 | Header and announcement styles |
| `assets/header.js` | 6,302 | Menu disclosure behaviour |
| `config/settings_schema.json` | 2,539 | Theme settings, deliberately small |
| `config/settings_data.json` | 533 | Defaults |
| `locales/en.default.json` | 413 | Twelve strings |
| `templates/index.json` | 36 | Empty placeholder so the theme is structurally valid |
| **Total** | **68,855** | |

`templates/index.json` carries no sections. A theme needs at least one template to load, and the homepage sections belong to Phases 5 to 7, so it is deliberately empty.

The prototype is untouched and still works. All 44 original files were verified byte-identical by md5 after the build.

---

## 2. Architecture

Section 3 of the specification requires Online Store 2.0 architecture with the header in a section group rather than a static layout section. That is what is built: `layout/theme.liquid` renders `{% sections 'header-group' %}`, and the group orders the announcement bar above the header. Both sections declare `"enabled_on": { "groups": ["header"] }`, so neither can be dropped into a page template by mistake.

No duplicate architecture was created. The project contained no `layout/`, `sections/`, `snippets/`, `assets/`, `config/`, `locales/` or `templates/` directory before this phase; all seven now exist, holding only what the header needs.

---

## 3. Decisions taken, and why

### 3.1 Navigation destinations come from a linklist

Phase 1 recorded every navigation destination as BUSINESS INFORMATION REQUIRED, and the prototype hard-coded six links to `#`. Hard-coding them here would bake in an unanswered question. The header instead renders `linklists[section.settings.menu]`, so the merchant sets destinations in the admin and the theme carries none. This resolves the open question correctly rather than deferring it.

### 3.2 Every control is a real control

The prototype had zero `<button>` elements. Search, account and cart were bare images with `tabIndex -1`, and the menu trigger was a `<span>` with an `aria-label` but no role and no handler, so below 900 px no destination was reachable at all.

The header now has a `<button>` for the menu with `aria-expanded` and `aria-controls`, and anchors for search, account and cart. Every one has a text label in a visually hidden span and a target of at least 44 px.

### 3.3 The scrim is not optional, and it had to be stronger than specified

Phase 1 measured three navigation links at 2.4 to 2.9:1 over the hero sky, against a 4.5:1 requirement. Phase 2 responded with a `--scrim-header` token. **Phase 4 measured that token against the real hero and found it insufficient.**

The original ramp went from 0.85 alpha at the top of the header to 0.55 at 60% and to zero at the bottom. By the time it reached the band the links occupy, it had already faded. Measured against the actual hero image with all header text hidden, the brightest pixels behind the links sat at 1.1 to 1.7:1 — worse than the prototype.

The required alpha is arithmetic, not taste. For cream text to reach 4.5:1 over a worst-case near-white sky, the ink layer must hold at least 0.85 alpha. The token now holds about 0.86 through the entire header and fades only below it, using a companion `--scrim-header-overhang` so the fade happens outside the content band.

| Measurement of the nav band backing | Median | p90 | p98 | Worst pixel |
|---|---|---|---|---|
| No scrim (the Phase 1 condition) | 4.11:1 | 1.43:1 | 1.39:1 | 1.09:1 |
| Phase 2 scrim as specified | 6.11:1 | 1.73:1 | 1.43:1 | 1.11:1 |
| Phase 4 scrim as shipped | 17.38:1 | 14.82:1 | 14.55:1 | **13.61:1** |

The worst single pixel in the whole band now passes AA for 12 px text. Both the canonical `PHASE-2-DESIGN-TOKENS.css` and the theme copy were updated, so the design system and the implementation agree.

### 3.4 The overlay header keeps its static position

A first implementation gave the overlay header `top: 0`, which placed it at the top of the page and pulled it over the announcement bar, where its scrim dimmed that text. An absolutely positioned box with no offset keeps its static position, so removing `top` lands the header exactly where it would have sat in flow, directly below the announcement bar, while still lifting out of flow so the first section rises behind it. This was found by looking at the render, not by reading the code.

### 3.5 Behaviours the specification did not name

| Behaviour | Default | Why |
|---|---|---|
| Overlay the first section on the home page | On | Matches the approved mockup, where the nav sits over the hero. Carries the mandatory scrim. |
| Stick to the top on scroll | Off | Matches the prototype. When both are on, the header overlays at rest and becomes a solid fixed bar once scrolled, because past the first section there is no artwork for a scrim to sit on. |
| Search destination | `routes.search_url` | The search results page is explicitly out of scope, so the trigger is a link, not a drawer. |
| Cart destination | `routes.cart_url` | The cart drawer is explicitly out of scope. |
| Account visibility | Only when customer accounts are enabled | Avoids a link that leads nowhere on a store that has not enabled them. |

---

## 4. Theme Editor settings

Phase 2 asked for a deliberately small merchant surface. The header section exposes twelve settings in four groups: logo and its two heights, the menu, search and account visibility, and the two behaviour switches. The announcement bar exposes one setting and repeatable message blocks, limited to three.

Theme-level settings are confined to what Phase 2 marked as merchant-editable: the three brand colours, two font choices, the content width, the corner radius and a favicon slot. The spacing scale, type scale, z-index ladder, motion, focus and status colours stay developer-owned, so the Theme Editor cannot break the contrast rules.

---

## 5. Verification performed

The theme cannot be rendered without a Shopify store, so a static harness was built using the real `header.css`, `header.js` and icon snippets, driven in a browser at several widths.

**Structural**, all passing: every JSON file and both `{% schema %}` blocks parse; the section group resolves to both sections; all five `render` calls resolve to snippets; all three `asset_url` references resolve; every one of the 192 tokens referenced by `header.css` exists; no raw hex, no `!important`, no reach into the `--gs-*` palette layer; the canonical and theme token files carry identical token sets; all twelve translation keys are defined and all twelve are used.

**Measured in a browser:**

| Check | Desktop 1440 | Mobile 390 |
|---|---|---|
| Header height | 122 px | 88 px |
| Logo height | 78 px | 56 px |
| Navigation | 5 links, flex | hidden, panel instead |
| Menu button | hidden | 44 x 44 |
| Utility controls | 44 x 44 each | 44 x 44 each |
| Horizontal overflow | none | none |

**Menu disclosure**, verified by driving it: opening sets `aria-expanded="true"`, reveals the panel and overlay, moves focus into the panel and locks body scroll. Tab from the last item wraps to the first rather than escaping. All three close paths — Escape, the close button and the overlay — hide the panel, restore scroll and return focus to the trigger.

One real defect was found and fixed during this testing: focus was returned to whatever was focused when the panel opened, which stranded focus inside the closed panel if the trigger had not been focused first. A disclosure should always return focus to its own trigger.

**A measurement caveat worth recording.** Both the desktop preview pane and headless Chromium under a virtual time budget freeze CSS transitions at their start value, so the panel reads as off-screen even when it is open. Measuring with transitions disabled shows the true resting position: the panel sits at 0 to 351 px in a 390 px viewport, the close button at 283 to 327 inside it, and menu links 47 px tall. Any later phase measuring animated state should disable transitions first.

---

## 6. Phase 1 findings retired

| Finding | How |
|---|---|
| NAV-01 no navigation below 900 px | Real button, real panel, full keyboard contract |
| NAV-02 / A11Y-01 utility icons not controls | Anchors and a button, each labelled, each 44 px |
| NAV-06 hard-coded active state | `link.active` with `aria-current="page"` |
| NAV-09 cart badge was the literal 0 | `cart.item_count`, hidden entirely when empty |
| A11Y-02 no skip link, no main landmark | Both in `layout/theme.liquid` |
| A11Y-03 / HERO-02 nav contrast 2.4-2.9:1 | Scrim measured to 13.61:1 worst case |
| A11Y-07 aria-label on a role-less span | Now on a `<button>` |
| HTML-02 no lang attribute | `lang="{{ request.locale.iso_code }}"` |
| SEO-01 empty title | Real title in the layout |
| ICON-01 raster icons, colour baked in | Inline SVG inheriting `currentColor` |
| CSS-02 / CSS-03 inline styles, `!important` | Class-based, mobile-first, zero `!important` |

Partially retired: **SEO-05**, the favicon. A slot exists in theme settings, but no favicon asset exists and none can be derived properly until a vector logo is supplied.

---

## 7. Still blocked

- **A vector logo.** The header renders whatever the merchant uploads, but the only wordmark available is a 500 by 500 PNG whose transparent padding makes the visible mark render at roughly half its intended size. Phase 3 records VECTOR LOGO REQUIRED.
- **Navigation destinations.** The theme is correct without them, but the menu cannot be populated until Shop, Collections, Our Story and Verse have real targets, and until it is decided what Verse is.
- **Social channels and a favicon**, both dependent on business decisions already registered in Phase 1 Appendix A and Phase 3 Appendix C.

---

## 8. Not built, by scope

Hero, featured collection, best sellers, our story, brand values, verse, social gallery, product page, collection page, cart drawer and search results page are all explicitly out of Phase 4 scope and were not started. The footer group is also absent: the specification's scope list does not include it.

---

## 9. Completion against the thirteen scope items

- [x] **1. Announcement bar** — section with message blocks, dark or light surface, optional link and icon per message.
- [x] **2. Desktop header** — 122 px, logo left, navigation centre, utility right, constrained to the content width.
- [x] **3. Primary navigation** — from a linklist, with active state and hover.
- [x] **4. Utility navigation** — search, account and cart, each a real control with a label and a 44 px target.
- [x] **5. Mobile header** — 88 px, menu button, logo, utility cluster.
- [x] **6. Mobile menu** — panel with overlay, focus trap, Escape, focus return, scroll lock.
- [x] **7. Search trigger** — links to the search route; the results page is out of scope.
- [x] **8. Account trigger** — links to the account route, shown only when accounts are enabled.
- [x] **9. Cart trigger** — links to the cart route with a real item count.
- [x] **10. Header responsive behaviour** — mobile-first, one breakpoint at 1024 px, no overflow at any width tested.
- [x] **11. Accessibility behaviour** — verified by driving the component, not by inspection alone.
- [x] **12. Header Theme Editor settings** — twelve section settings, one announcement setting, blocks for messages.
- [x] **13. Header section-group architecture** — `sections/header-group.json`, both sections restricted to the header group.
