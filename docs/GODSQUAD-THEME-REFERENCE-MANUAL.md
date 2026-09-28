# GOD SQUAD — SHOPIFY THEME REFERENCE MANUAL

**The consolidated record of Phases 0–18, organised by subject.**  
**Date:** 2026-09-26  
**Theme:** `god-squad-theme/` — 75 files  
**Status:** code-complete and internally coherent; **not launchable** until the
merchant content in §14 exists.

---

## About this document

This replaces twenty phase documents — **17,475 lines, 1.6MB** — with one
reference. It is organised **by subject rather than by phase**, because the next
step is a Shopify integration and "what does the theme need from Shopify" is a
more useful question than "what happened in Phase 13".

**How it was built.** Each of the twenty source documents was read in full and
indexed by its own agent, which extracted the decisions that still bind the theme
today, the items left open, and the content a later phase had superseded —
**514 governing decisions and 346 open items** in total. Fifteen further agents each
wrote one section of this manual from those indexes and from the sources directly.

**Two rules governed the rewrite:**

1. **Later phases override earlier ones.** Where a rule changed, only the current
   form appears. Phase 2 states gold as a palette colour; Phase 2 §3 later
   prohibits it on light surfaces at 1.55:1 — the prohibition is what you will
   find here.
2. **Where a document and the code disagree, the code is the truth**, and the
   disagreement is noted rather than smoothed over.

**The original twenty documents are unchanged and remain in the project root.**
Nothing here is a substitute for them as a historical record; this is the working
reference.

### How much to trust it — read this before relying on any list

Sixteen independent critics audited this manual, one per section plus two on
its structure. Each was given its section **in full**, the index of all twenty
sources, and the theme itself, and asked to break it. They converged on one
verdict, in almost identical words:

> **Trustworthy on mechanism and measurement. Unreliable on enumeration and
> totals.**

What that means in practice:

- **Concrete facts hold.** Byte sizes, line-number citations, file counts,
  token counts, consumer counts, gzip figures, contrast ratios, media-query
  censuses — the critics re-measured these against disk and found them exact,
  repeatedly to the byte. Several said they tried hard to break a section and
  could not. Where this manual gives you a number or a `file:line`, it is good.
- **Lists may not be complete.** Much of the manual is phrased as though its
  enumerations are exhaustive. Compressing 1.6MB to this size necessarily drops
  detail, and the critics logged **228 governing rules** from the sources that
  no section carries. The appendix lists every one.

**So: this is the working reference, not a replacement.** Use it to understand
the system, to find the rule that governs a decision, and to plan the
integration. When you are about to change something and the manual’s account
of it reads as a complete list, **check the phase document** — the twenty
originals remain the authority on detail, and §16 maps each subject to its
source.

### What this manual cannot tell you

There is **no merchant photography, catalogue, or business information** in this
project. Phase 3 recorded sourcing — not processing — as the ceiling. Every
measurement quoted anywhere in these nineteen phases was taken against **invented
fixture data**, and Phase 18 proved that hides real defects: a typography bug was
invisible on the fixtures’ short product names and visible on realistic ones.
Read every measured claim with that in mind.

---

## Contents

1. [Project identity, scope and standing rules](#project-identity-scope-and-standing-rules)
2. [The theme as built — architecture and conventions](#the-theme-as-built-architecture-and-conventions)
3. [Design system — colour](#design-system-colour)
4. [Design system — typography](#design-system-typography)
5. [Design system — spacing, container and grid](#design-system-spacing-container-and-grid)
6. [Design system — components](#design-system-components)
7. [Surfaces — header, navigation, hero, collections, Our Story, footer](#surfaces-header-navigation-hero-collections-our-story-footer)
8. [Surfaces — product, cart, checkout, search and filtering, accounts, 404 and pages](#surfaces-product-cart-checkout-search-and-filtering-accounts-404-and-pages)
9. [The Shopify integration contract](#the-shopify-integration-contract)
10. [The store-setup runbook](#the-store-setup-runbook)
11. [Accessibility posture](#accessibility-posture)
12. [Performance and SEO posture](#performance-and-seo-posture)
13. [Analytics and marketing posture](#analytics-and-marketing-posture)
14. [QA harness and test inventory](#qa-harness-and-test-inventory)
15. [Open decisions, business information required, and known limitations](#open-decisions-business-information-required-and-known-limitations)
16. [Phase-by-phase record](#phase-by-phase-record)

---

## Project identity, scope and standing rules

### The brand

GOD SQUAD is positioned as **faith-driven premium streetwear**. That positioning was fixed by the owner before any code existed and has never been re-opened; Phase 2 §2 ratifies it rather than proposing it, and Phase 2 records that the specification "forbids introducing a new brand identity."

Eleven personality traits are fixed and each one costs the system something concrete: premium, faith-driven, editorial, modern, urban, minimal, purposeful, cinematic, community-oriented, confident, authentic. The governing aesthetic principle is **LUXURY THROUGH RESTRAINT** — when a decision is open, choose the quieter option: contrast and spacing before borders, borders before shadows, and no motion unless it serves comprehension.

Five brand messages are canonical, and each is permitted at exactly one level of the page. This is a hierarchy, not a word list — a message used at two adjacent levels is a defect.

| Message | Permitted level | Ships today in |
|---|---|---|
| `Good People. Higher Purpose.` | Announcement bar | `sections/header-group.json` (message-1) |
| `Walk By Faith.` | Hero headline — one per page | `templates/index.json`, split `heading: "Walk By"` + `heading_accent: "Faith."` |
| `More Than Clothing.` | Script accent — one per page | `templates/index.json`, our-story `faith` value block |
| `Different People. Same Purpose.` | Hero support **and** footer signature — the sole two-placement exception | `templates/index.json`, hero `description` |
| `Streetwear With A Purpose.` | Section eyebrow | `templates/index.json`, hero `eyebrow` |

Rules that bind: one message per level per page; the hero headline is the only message permitted at display size; **gold may carry at most one word inside a headline** (`Faith.` is both the precedent and the ceiling); and any string that is not one of the five is section copy with no reserved level. `The Faithful`, `Premium Essentials for a Higher Purpose.`, `Real People. Bigger Purpose.` and `Faith Lives Different Here.` are section copy and may not be promoted into the canonical set.

**The brand-origin statement is unconfirmed.** The copy `God Squad is a Philippine streetwear brand built on faith, creativity, and community.` ships as the default `body` of the our-story section (`sections/our-story.liquid:342`, `templates/index.json`) but is Appendix A decision 25 — *confirmation of the brand-origin statement* — and is still open. It is the prototype's claim, carried forward because the prototype is the approved baseline, not because anyone on this project verified it.

### The approved visual direction

The design is the fixed point of the programme. It is preserved as `uploads/GODSQUAD WEBSITE MOCKUP.png` (1024 × 1536, 1,872,888 bytes) — the master, to be used whenever full-quality pixels are needed — and as `uploads/God-Squad-Images/00-full-mockup-reference.webp` (182,250 bytes), the reference Phases 1 and 2 cite.

| Element | Approved value |
|---|---|
| Palette | Near black `#0D0C0A`, warm cream `#F3EFE6`, muted gold `#D8C08A` (in code as `--gs-ink`, `--gs-cream`, `--gs-gold`, `assets/design-tokens.css:49-51`) |
| Typography | Playfair Display 900 display, Jost 400/500/600 interface and body, Kaushan Script hand-lettered accents (`--font-display`, `--font-body`, `--font-script`) |
| Type signature | Tracked uppercase labels — a brand signature to be codified, not abandoned |
| Composition | Urban, low-angle, natural-light photography; black and cream garments on location; generous whitespace; asymmetric editorial layouts; thin separators and restrained gold accents; alternating dark and light bands |
| Section order | Announcement bar, header, hero, New Drop, Our Story, brand values, footer |

Three deviations from the mockup are **owner decisions recorded in the Claude Design editor history and treated as approved, not as defects**: the hero photograph replaced with a three-model group image where the mockup shows a single capped model; the announcement-bar globe changed to gold, then restored and kept gold after a deliberate second request; and two placeholder social icons removed from the footer, leaving Facebook and Instagram where the mockup shows four networks. They appear in the Phase 1 business register (Appendix A decision 19) for formal confirmation only.

**One later correction you must not undo:** Phase 2 §3 established THE PROHIBITION — muted gold `#D8C08A` measures **1.55:1 on warm cream `#F3EFE6`** and **1.43:1 on the tile cream `#EBE6DC`**. Gold is a dark-surface accent only and may never carry text, an icon, a border or any other perceivable mark on a light surface. On light surfaces the accent is `--color-accent-strong` `#82672B` (4.66:1 on cream, `assets/design-tokens.css:63`). Phase 0 §5 lists gold as a palette colour without this constraint; the constraint is current.

### What existed at the start, and why the project is a rebuild

The starting artefact was a **single-page visual prototype exported from Claude Design** — a homepage only, with no commerce of any kind — plus its runtime and a folder of images: 44 files, 17,185,754 bytes, at `C:\Users\TEST\OneDrive\Documents\GodSquad Website`.

It is not a static website. It is a Claude Design "dc" document: all visible markup sits inside a custom `<x-dc>` element, and `support.js` (69,150 bytes, 1,911 generated lines) fetches React 18.3.1 from unpkg, compiles the template, evaluates a data class with `new Function`, and mounts the result. Products, prices, swatches and brand values exist only as object literals inside that class. The page executes ~211 KB of JavaScript (~66 KB gzipped) per load and shows nothing at all if unpkg is unreachable.

**The single fact that determined the programme's shape:** the prototype's template delimiters are `{{ }}` — Liquid's own. Pasting that markup into a Shopify section would make Liquid evaluate `{{ products }}` and `{{ p.name }}` as undefined variables and render empty tiles **silently, with no error**. That makes copy-and-adapt actively hazardous, not merely unhelpful.

The objective is therefore: *transform the approved visual direction into a production-ready Shopify Online Store 2.0 theme, without losing the design that has already been signed off.* Phase 1 stated the conclusion as **KEEP the design, REPLACE the architecture** — the project is a **rebuild against a preserved design, not a conversion**, and everything in the phase plan follows from that distinction.

Phase 1 hardened this into an operating rule: the theme starts from an empty scaffold, the prototype folder becomes a **read-only archive**, and design tokens and copy are **transcribed, not copied**. Nothing from the prototype may be pasted into a Liquid file.

### Where the work stands now

| Fact | Value |
|---|---|
| Theme root | `C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme` (moved there in Phase 10) |
| Theme size | 75 files — verified by listing, matching Phase 18's count |
| Theme identity | `theme_name` "God Squad", `theme_version` 0.5.0, `theme_author` "God Squad" (`config/settings_schema.json`) |
| Prototype | Unchanged and archived in the project root alongside the theme |
| Version control | **None.** The project is still a plain folder inside a personal OneDrive; there is no `.git`. Phase 1 logged this as DEBT-12/DEBT-13 and recommended fixing it before Phase 2; it was not done and is now long overdue |
| Real Shopify store | None. The theme has never been uploaded, opened in a real Theme Editor, or served by Shopify's CDN |
| Launch status | **Code-complete and internally coherent; not launchable** |

Phase 18's verdict is the current one and its reasons are not development tasks: no merchant photography (the hero ships an AI-generated image with unconfirmed rights), no vector logo master and no favicon, and the outstanding business information — including the two `ValidJSON` Theme Check offenses for missing `theme_support_email` and `theme_documentation_url`.

### Scope

**In scope for the programme**

- A complete Shopify Online Store 2.0 theme: layout, sections, snippets, templates, assets, config, locales.
- Faithful reproduction of the approved visual system in native Shopify architecture.
- The commerce surface the prototype entirely lacks: product pages, collections, cart, search, customer accounts.
- Performance, accessibility and SEO foundations.
- A design system and asset system to support all of the above.

**Out of scope, or deferred pending a business decision**

- **Brand redesign.** The visual identity is approved and preserved, not revisited.
- Product photography and copywriting. The project can specify what is needed; it cannot originate it.
- Merchandising strategy, pricing, catalogue structure and policy content.
- Any third-party Shopify app selection.
- Marketing, email and social operations.

Two scope facts discovered later and now binding. **Customer account surfaces are out of reach, not deferred:** Shopify deprecated legacy customer accounts on 2026-02-26, and `templates/customers/` must remain absent — its absence is the trigger that auto-upgrades the merchant to new customer accounts, so shipping those templates would *withhold the merchant's upgrade* (Phase 15). Order history, order details, tracking and customer information have no theme surface at all. **Analytics is likewise out of reach:** a theme cannot legitimately contain tracking code on current Shopify — partners and merchants cannot publish standard events, and snippets that bypass the consent framework violate Shopify's Terms of Service (Phase 17).

### The phase model

Work proceeds only within the phase the owner has specified and authorised. Each phase is **gated**: its specification arrives in writing, the work is done, the deliverable is produced, and the programme stops until the next phase is authorised. Phase 0 operated under the rule but did not formalise it; every phase from 1 onward states it, and each phase document ends by declining to start the next.

The ordering is dependency-driven, not cosmetic: the design system precedes every section phase because those phases consume its vocabulary; asset preparation precedes the hero, collection and story phases because none can be completed against mockup crops; theme conversion precedes the editor, performance, SEO and QA phases because each is cheap to do correctly in a native theme and expensive to retrofit twice.

**Phase 0 §3's 17-row roadmap (Phases 0–16) is superseded.** Delivery ran to Phase 18 and Phases 12–18 were re-scoped from the original plan. What was actually delivered:

| # | Phase as delivered | Delivered |
|---|---|---|
| 0 | Project Foundation (written retrospectively) | 2026-09-21 |
| 1 | Website Audit & Technical Assessment | 2026-09-21 |
| 2 | Design System & Visual Language | 2026-09-21 |
| 3 | Asset Preparation & Image System | 2026-09-22 |
| 4 | Header & Navigation | 2026-09-22 |
| 5 | Hero Section | 2026-09-22 |
| 6 | Collections & Best Sellers | 2026-09-22 |
| 7 | Our Story + Brand Purpose | 2026-09-23 |
| 8 | Product & Shopping UX | 2026-09-23 |
| 9 | Mobile UX + Responsive Polish | 2026-09-23 |
| 10 | Shopify Theme Architecture + Conversion | 2026-09-24 |
| 11 | Theme Editor + Merchant Customization | 2026-09-24 |
| 12 | Product + Collection + Catalog UX | 2026-09-24 |
| 13 | Search, Filtering & Product Discovery | 2026-09-24 |
| 14 | Cart + Cart Drawer + Checkout Experience | 2026-09-24 |
| 15 | Customer Account + Order Tracking + Post-Purchase UX | 2026-09-24 |
| 16 | Performance + SEO + Conversion Optimization | 2026-09-24 |
| 17 | Analytics + Tracking + Marketing Integration | 2026-09-25 |
| 18 | Final Polish + Award-Level UI/UX QA | 2026-09-25 |

Phase 0 was written retrospectively on 2026-09-21 from the preserved evidence base, not from recollection, because the phase itself produced no contemporaneous deliverable. Phase 19 has not been started. The next step is the Shopify integration.

### The standing rules

These six are Phase 0 §11 and all six are still current.

1. **The visual direction is approved and preserved.** Branding, imagery, typography and content structure are not revisited.
2. **Phases are gated.** No phase begins without its written specification and the owner's authorisation.
3. **Inspect and document before changing anything.** Every phase begins by verifying the ground it stands on rather than trusting the previous report alone.
4. **Business facts are never invented.** Anything unknown is marked as requiring business information and is escalated, not guessed.
5. **Original assets are preserved.** Optimised copies are additions; originals are never overwritten, renamed or destructively processed.
6. **The prototype is the design baseline, not the codebase.** It is read for intent; it is not the thing being edited.

Later phases added four more that now carry equal weight.

7. **Shopify is the source of truth for all commerce data.** There is no product, price, currency, rating, review, inventory figure, availability claim, colour value or bestseller ranking anywhere in the theme (Phase 6). No currency symbol is hardcoded — every price goes through the `money` filter against the store's own format. Collections arrive through a `collection` picker, never a handle in code; navigation through `link_list` settings, so **no hardcoded menu label exists anywhere in the theme** — not HOME, SHOP, COLLECTIONS, OUR STORY or VERSE. Cart state is Shopify's: no client-side cart object, no `localStorage`, no second source of truth. The two `featured-collection` sections in `templates/index.json` ship with **no collection handle at all**, so both rows render nothing until a merchant picks one.
8. **No fake data, and empty beats invented.** Anything not supplied is labelled BUSINESS INFORMATION REQUIRED and ships **empty or hidden, never invented**. The hero CTA has no `button_link` in `templates/index.json`, so the button does not render. The two footer social URL settings are empty and guarded, and the whole social row is suppressed. `theme_documentation_url` and `theme_support_url` are omitted rather than filled with a fabricated URL. A product description "must not be synthesised — a generated sentence about a garment nobody on this project has seen is invented product copy." A collection banner is never cut from the mockup and never filled from a product image.
9. **No invented claims, reviews, awards, statistics or testimonials.** Phase 7: no founder, founding date, location, partnership, statistic, testimonial or theological claim; no star ratings, customer counts, "trusted by", press mentions or endorsements. "Every value line is brand messaging, never a measurable claim," and the block's help text says so in the editor. `Worldwide / Shipping Available` was deliberately **not shipped** as a fourth Our Story value tile because it is the one checkable commercial promise with no shipping policy, destination list or rate table behind it. `BreadcrumbList` and `Organization` JSON-LD are deliberately absent for the same reason — "a fabricated trail is exactly the fake structure the brief forbids," and "a `sameAs` array that is empty half the time is worse than no block."
10. **Negative-control every test.** "A test that cannot fail proves nothing" (Phase 10). Every absence assertion is seeded with a real violation and required to catch it, because "an absence assertion that has never been seen to fail is indistinguishable from a typo in a regex" (Phase 15). Phase 10 found the harness had passed with a P0 bug present; Phase 16 found the Theme Check runner had been scanning a directory containing no theme and reporting zero offenses.

**One live claim the rules have not resolved.** `Worldwide Shipping` ships in the announcement bar on every page (`sections/header-group.json`, message-2) while the same claim is withheld from the Our Story values row. Phase 18 flagged this to the owner rather than removing or propagating it: it is a business claim, true of the business or not, and not the developer's to assert.

### Vocabulary you will meet throughout

**BUSINESS INFORMATION REQUIRED** means genuinely unknown — "not a placeholder to be filled with a plausible guess" (Phase 2). It appears 169 times in the Phase 1 audit, with **BUSINESS DECISION REQUIRED** a further 52 times. One caveat for merchant-facing text: Phase 18 removed project vocabulary from schema `info` strings and settings labels — a merchant never sees "Phase 2 §26.1", "the prototype", "the approved mockup" or "BUSINESS INFORMATION REQUIRED" — while keeping every instruction's substance.

Phase 1 classified each of its 200 issues with a fixed disposition vocabulary: **KEEP** (43), **IMPROVE** (24), **REBUILD** (48), **REPLACE** (45), **REMOVE** (31), **ADD LATER** (44). In asset work these labels are deliberately non-destructive: "REMOVE means candidate for removal after final approval, never delete now"; "ARCHIVE likewise means move to an archive location after approval, not discard" (Phase 3).

### The open business register

Phase 1's Appendix A consolidates thirty decisions in seven clusters, each citing the issue IDs that depend on it and the phase it gates. They remain the programme's largest external dependency and none can be answered from inside the code. Four were identified as gating the design system itself: confirmation of the extended palette beyond the three primaries (`#bdb6a8`, `#e9e4d8`, `#ebe6dc`, the olive `#4b5443`, and the scrim values); whether the 9–13 px tracked uppercase labels are brand-mandated on phones or may be raised to a 14/16 px floor; the target browser and device support matrix; and the intended behaviour above 1440 px.

The unknowns most likely to bite a Shopify integration:

- **The entire commercial layer** — catalogue, real prices (whether ₱1,290 / ₱2,490 / ₱890 are actual or placeholder), currency and money format, markets, collection taxonomy, variants and inventory.
- **Every navigation destination**, including what "Verse" is intended to be — a page, a homepage section, or a rotating scripture — and which scriptures beyond `2 Corinthians 5:7` are approved.
- **Shipping scope, and all policy and legal text**; the legal entity name for the copyright line; contact email, phone and address.
- **Which social channels are live.** Phase 3 found three conflicting counts: 2 files, 4 in the mockup, 10 on the sprite sheet. No account may be invented and no platform displayed that the business has not confirmed.
- **A vector logo master and original photography.** Layered logo sources (two PSDs and several PNG exports) were located **outside** the project on the owner's Desktop and were never opened, so a vector master may yet exist inside them — unverified. This is a sourcing problem, not a processing problem: "optimisation cannot substitute for sourcing."
- **The Shopify store itself** — whether one exists, its plan, domain, administrator, primary language and locale.

### Two working constraints inherited from Phase 0

**Measurement technique.** Headless Edge on this machine cannot lay out narrower than roughly 490 CSS pixels; a capture requested at 375 px is laid out at about 490 and clipped, silently misrepresenting the phone layout. **True phone captures require a wrapper page containing an iframe of the target width, captured and then cropped**, and every capture must be verified to actually contain the photograph before it is measured. Two early evidence files, `mobile-375.png` and `mobile-375-raw.png`, are clipped ~490 px layouts and are **marked never to be cited**; the valid phone captures are `mobile-375-true.png`, `mobile-390-true.png` and `mobile-430-true.png`. Separately, transitions must be disabled before measuring animated state — headless virtual time freezes CSS transitions at their start value, and a probe that forgets this reports the start value as the result.

**Tooling.** Node 22.23.2, npm 10.9.8, Python 3.12.10, git 2.54.0 and the GitHub CLI are present; **Bun and the Shopify CLI are not**. One Phase 0 statement has been corrected: Phase 16 established that **Theme Check was available all along** as `@shopify/theme-check-node` and that the Phase 10 runner had been pointing at the project root, which stopped being the theme root the moment Phase 10 moved the theme into `god-squad-theme/`. Any phase document before Phase 16 that says "Theme Check was never run" is superseded — it runs, against the theme root, and currently reports 2 offenses, both business information. Lighthouse is genuinely unavailable, and **no Lighthouse score appears anywhere in this programme's documents** because inventing one is forbidden and there is nothing real to report.

### Integrity of the original files

No original project file has been edited or deleted at any point. All 44 original prototype files were checked byte-identical by md5 against the Phase 0 inventory after each phase deliverable through Phase 10, which confirmed them unchanged after the theme was relocated into `god-squad-theme/`. Two changes to the tree did occur and are both recorded: the owner renamed the entry page from `God Squad Website.dc.html` to `God Squad Website.html` on 2026-09-20 at 15:34, deliberately and with the content unchanged at 15,632 bytes (specifications written before that time refer to the old name and mean this file); and new files — the phase documents, the token file, `phase-3-assets/`, `.claude/launch.json` and the theme itself — were added alongside the originals. `.claude/launch.json` is audit tooling, not a site file.

---

## The theme as built — architecture and conventions

### Where the theme lives, and what uploads

```
C:\Users\TEST\OneDrive\Documents\GodSquad Website\      the project
├── god-squad-theme\                THE THEME — this is what uploads to Shopify
├── God Squad Website.html          the frozen prototype, read-only archive
├── support.js, images\, uploads\, phase-3-assets\
├── PHASE-0 … PHASE-18 *.md         the phase documents
├── PHASE-2-DESIGN-TOKENS.css       canonical token file (see "Tokens" below)
└── PHASE-3-ASSET-MANIFEST.csv
```

Phase 10 moved 49 files out of the project root into `god-squad-theme/`. Nothing from `images/`, `uploads/`, `phase-3-assets/` or the project root is copied across, and nothing outside `god-squad-theme/` is part of the theme. Any tool pointed at the project root is pointed at the wrong place — Phase 16 found the Theme Check runner still aimed at the project root, scanning a directory with no theme in it and reporting zero offenses.

### The file tree — 75 files, verified against disk

| Directory | Files | Contents |
|---|---:|---|
| `assets/` | 25 | 21 CSS, 4 JS. **No images, no fonts.** |
| `config/` | 2 | `settings_schema.json`, `settings_data.json` |
| `layout/` | 1 | `theme.liquid` |
| `locales/` | 1 | `en.default.json` — 117 leaf strings in 8 top-level groups (`accessibility`, `cart`, `collection`, `footer`, `general`, `header`, `products`, `sections`) |
| `sections/` | 16 | 14 `.liquid` + `header-group.json` + `footer-group.json` |
| `snippets/` | 23 | 9 icons, 5 cart, 4 product, 5 infrastructure |
| `templates/` | 7 | `index`, `product`, `collection`, `page`, `cart`, `search`, `404` — all `.json` |

Five absences are decisions, not gaps:

- **No `blocks/`.** Theme blocks are an optional newer capability; Dawn's `main` has none and nothing here needs one.
- **No `templates/customers/*`, and it must stay absent.** Publishing without those templates is what auto-upgrades the merchant to Shopify's hosted new customer accounts; shipping them withholds that upgrade (Phase 15). Eight assertions hold the absence, including "no `main-account`/`main-order`/`main-login` section" and "no customer `{% form %}` tag anywhere".
- **No imagery in `assets/`.** Content images arrive through `image_picker` settings and product media so Shopify's CDN can resize them per width. Putting a product photo in `assets/` breaks variant media, the gallery, zoom and the merchant's ability to change a photograph without a theme deploy.
- **No `theme.css`.** The Phase 1 §29.1 target tree names one; there is no third CSS layer to put in it. The per-section stylesheet architecture stands.
- **No `locales/en.default.schema.json`, and schema labels are plain English rather than `t:` keys.** Carried from Phase 10 → 11 → 12 and still not done. Customer-facing strings *are* all in the locale file; merchant-facing schema labels are not.

Also still missing, deliberately: `list-collections`, `blog`, `article`, `password` and `gift_card` templates. Phase 1 §29.5 classifies each OPTIONAL or BUSINESS DECISION REQUIRED, and nothing the theme renders links to them. Shopify serves an error page for a route whose template is missing, so anything a shopper can actually reach must have one — which is why the other seven exist.

### `layout/theme.liquid` — the only layout

284 lines, roughly half comment. It carries no page content. Head output, in order, and the order is load-bearing:

| # | Output | Why here |
|---|---|---|
| 1 | charset, X-UA-Compatible, viewport | |
| 2 | `{% render 'css-variables', part: 'meta' %}` | emits only `<meta name="theme-color">`; the meta belongs early |
| 3 | `<link rel="canonical">` | the theme's **only** canonical, on every template |
| 4 | favicon ×3 — `32`, `192x192`, `apple-touch-icon 180x180` | all three resized by Shopify from one `settings.favicon` |
| 5 | `<title>` — `page_title` + tags + page number + `shop.name` unless already contained | |
| 6 | `<meta name="description">` when `page_description` exists | |
| 7 | `{% render 'meta-social' %}` | Open Graph / Twitter card |
| 8 | `{% style %}` wrapping **four** `font_face` calls | see below |
| 9 | `{{ content_for_header }}` | **once, unmodified.** Shopify's analytics and consent hook; a standing Phase 17 assertion protects it |
| 10 | `design-tokens.css`, `base.css`, `header.css` | tokens first, element layer second — `base.css` consumes them |
| 11 | `component-container.css`, `component-button.css`, `component-pagination.css`, `component-quantity.css`, `component-cart-line.css` | the shared components; container first because everything sits inside it |
| 12 | `{% render 'css-variables', part: 'style' %}` | **after** the stylesheets, or its `:root` declarations lose to `design-tokens.css` |
| 13 | `no-js` → `js` inline swap, then `header.js` and `cart.js`, both `defer` | |

**Two P0 defects were fixed here in Phase 10 and must not regress.**

1. `font_face` returns a bare `@font-face` *rule*, not a style element. Emitted unwrapped it registered no face at all — Playfair Display and Jost never loaded storewide — and because a non-whitespace character token ends the HTML parser's "in head" insertion mode, the CSS text rendered as visible content above the logo and everything after it in source order was parsed in body context. **All `font_face` output stays inside one `{% style %}` block.**
2. **Shopify Liquid does not interpolate inside a string literal.** `"--logo-height-desktop: #{logo_h_desktop}px"` produced a *valid declaration with a garbage value* on the `<img>`, shadowing the good `:root` defaults, so `height` fell back to `auto` and the logo drew at intrinsic size the first time a merchant uploaded one. Strings are built with `append`. Verified: no Ruby-style interpolation remains in any Liquid file.

The font block now emits four faces, not two — Phase 16 found `--type-eyebrow-weight: 500` and `--type-label-weight`/`--type-price-weight: 600` were being faux-bolded from Jost 400 across 19+ rules:

```liquid
assign body_medium   = settings.type_body_font | font_modify: 'weight', '500'
assign body_semibold = settings.type_body_font | font_modify: 'weight', '600'
```

Each `font_modify` result is `{%- if -%}` guarded, because the filter returns nil when the family has no such variant. `font_display: swap` on all four. Note the consequence: `--weight-semibold` gives 600 only on the **body** family — the display font ships as `playfair_display_n9` with no `font_modify`, so 600 resolves to the 900 face there.

Body, in order: skip link → `{% sections 'header-group' %}` → `<main id="MainContent" tabindex="-1">{{ content_for_layout }}</main>` → the cart drawer → the cart's live region and string bag → `{% sections 'footer-group' %}`.

The drawer is double-gated and both gates matter:

```liquid
{%- if settings.cart_type != 'page' -%}
  {%- unless template.name == 'cart' -%}
    {% section 'cart-drawer' %}
  {%- endunless -%}
{%- endif -%}
```

It is rendered from the layout, not a template, for three reasons: it must exist wherever the header's cart control exists (everywhere); rendered statically its section id is its filename, `cart-drawer`, which never changes, so `cart.js` can name it as a Section Rendering target without runtime discovery; and it must be a direct child of `<body>` because the script marks the page's other top-level regions `inert`. It is never rendered on `/cart` — doing so put two views of one cart on one screen and gave every line a duplicate DOM id.

`#CartStatus` (`role="status" aria-live="polite" data-cart-no-inert`) sits in the layout, empty, because a live region created in the same moment as its text announces nothing, and because an `inert` subtree is removed from the accessibility tree. It sits *after* the drawer and *before* the footer group so it stays reachable whatever the footer contains. A sibling `[data-cart-strings]` element carries every sentence the cart script is allowed to say, from the locale file — `cart.js` writes no English of its own.

### JSON templates

Every template is JSON; there are no `.liquid` templates. Six of the seven hold exactly one section named `main`; only `index.json` is multi-section.

| Template | Sections | Notable shipped settings |
|---|---|---|
| `index.json` | `hero`, `new-drop`, `best-sellers`, `our-story` (in that `order`) | two `featured-collection` instances with different presets; `hero.button_link` is **absent**, so the CTA does not render |
| `product.json` | `main-product` | `media_layout: stacked`, `sticky_info: true`, `low_stock_threshold: 3`, `surface: light` |
| `collection.json` | `main-collection` | `products_per_page: 24`, `columns_desktop: 4/2/2`, `surface: light` |
| `search.json` | `main-search` | `search_types: product`, `results_per_page: 24` |
| `page.json` | `main-page` | `show_heading: true`, `surface: light` |
| `cart.json` | `main-cart` | `empty_link_label: "Shop the collection"` |
| `404.json` | `main-404` | none — all defaults |

`index.json` is also where the approved copy lives: the hero lockup (`Walk By` / `Faith.` / `2 Corinthians 5:7` / `Streetwear With A Purpose.`), the two collection-row headings, and Our Story's hard-broken `"Real People.\nBigger Purpose."` with its three `value` blocks. No collection handle is bound in either row — both render nothing on a live store until a merchant picks one.

### Section groups

Two groups, both rendered from the layout. `header-group.json` (`"type": "header"`) orders `announcement-bar` above `header`; `footer-group.json` (`"type": "footer"`) holds `footer` alone.

- `header-group.json` ships two announcement `message` blocks — `"Good People. Higher Purpose."` and `"Worldwide Shipping"` — plus `menu: "main-menu"`, `logo_height_desktop: 78`, `logo_height_mobile: 56`, `show_search`/`show_account` on, `sticky: false`, `overlay_first_section: true`. (The `"Worldwide Shipping"` string is flagged as an unsupported business claim, Phase 18 decision 4.)
- `footer-group.json` ships `tagline: "Different People. Same Purpose."` and `strapline: "A Brighter Tomorrow"` — prototype lines 156 and 164, not invented — and **`block_order: []`, with no menu bound.** Phase 10 initially bound Shopify's auto-created `footer` handle, which printed the admin vocabulary "Footer menu" as a customer-facing `<h2>` on every page.
- Both group sections carry `"enabled_on": { "groups": [...] }`, so neither can be dropped into a page template by mistake.

### Sections — the schema conventions

Measured from the schemas on disk: **104 section settings across 13 schema-bearing sections.**

| Section | Settings | `header` groupings | Blocks (limit) | Presets | `tag` | `enabled_on` |
|---|---:|---:|---|---:|---|---|
| `announcement-bar` | 2 | 0 | `message` (3) | 1 | `aside` | groups: header |
| `header` | 8 | 4 | — | — | `div` | groups: header |
| `hero` | 14 | 4 | — | 1 | `div` | — |
| `featured-collection` | 19 | 8 | — | 2 | `section` | — |
| `our-story` | 14 | 5 | `value` (6) | 1 | `section` | — |
| `footer` | 6 | 4 | `link_list` (4), `text` (2) | — | `div` | groups: footer |
| `main-product` | 10 | 4 | — | — | `section` | templates: product |
| `main-collection` | 11 | 5 | — | — | `section` | templates: collection |
| `main-search` | 6 | 3 | — | — | `section` | templates: search |
| `main-page` | 4 | 3 | — | — | `section` | templates: page |
| `main-cart` | 3 | 0 | — | — | `section` | templates: cart |
| `main-404` | 2 | 0 | — | — | `section` | templates: 404 |
| `cart-drawer` | 5 | 1 | — | — | — | — |
| `cart-icon-bubble` | **no schema** | | | | | |

The conventions these encode:

1. **Every section declares `tag` and `class`.** `footer`'s tag is `div` on purpose: `<footer>` maps to the `contentinfo` role only while it is not a descendant of `article`, `aside`, `main`, `nav` or `section`, so a `section` wrapper would silently demote the site's only `contentinfo`. `footer.liquid` writes the landmark out itself. `announcement-bar` takes `aside`.
2. **`enabled_on` is on every section that belongs somewhere specific** — template-bound sections name their template, group sections name their group. It is absent from `hero`, `featured-collection` and `our-story`, which are reusable on any page, and from the two statically rendered sections.
3. **`cart-icon-bubble.liquid` carries no schema, and no `enabled_on`/`disabled_on`, deliberately.** It exists only so the Section Rendering API has a stable id to return; a standalone render target cannot receive settings, and a preset would put it in the merchant's Add-section list. Its whole body is `{% render 'cart-icon-bubble' %}` — the same snippet `header.liquid` renders inline, so server markup and swapped markup cannot drift.
4. **Every setting uses a correct Shopify setting type** — `collection`, `link_list`, `image_picker`, `url`, `range`, `select`, `checkbox`, `text`, `textarea`, `richtext`. There is not one handle text field and not one pasted-CDN-URL field anywhere in the theme. This is what makes metafield dynamic sources available with no code change (none is wired today — it cannot be demonstrated without a real store).
5. **One surface vocabulary.** Eight sections expose a setting with id `surface`, labelled **"Colour scheme"**, options `light` = *Cream* and `dark` = *Ink*. Phase 11 brought the announcement bar into line; it had called the same concept "Surface" with *Dark (near black)* / *Light (warm cream)*.
6. **Spacing is a select of system values, never free pixels.** Three sections expose `spacing_top`/`spacing_bottom`. There is no spacing, size, colour, tracking or z-index setting anywhere below theme level except `surface`.
7. **The level test, applied every time:** would two different values on two pages be a bug? Then it is a theme setting. Is it a legitimate per-placement choice? Section setting. Does the merchant need to add, remove or reorder it? Block. No setting is duplicated across levels — which is why `logo` is global while its two *heights* stay on the header, and why `product_image_ratio` is global with a validator asserting no section-level `image_ratio` exists.
8. **Blocks only where the count genuinely varies**, and every block wrapper carries `{{ block.shopify_attributes }}` — verified in all three block-bearing sections. The hero deliberately takes no blocks: a reorderable eyebrow / heading / accent / scripture would let a merchant put the scripture above the headline and destroy the lockup.
9. **`shopify:block:select` is not implemented**, deliberately: no section hides or sequences block content, so there is nothing for a select to reveal.
10. **A setting must not silently do nothing, and must not be able to break the purchase flow.** Where a real cost exists it is written into the setting's own `info` — the announcement control is labelled "Alignment on desktop" because the bar always stacks below `--bp-md`; header `show_cart` says that with it off "a customer who has added something can only reach the cart by typing the address". The canonical near-miss: `show_quantity` once wrapped the *only* quantity input, so turning a presentational setting off submitted no quantity, and any variant with `quantity_rule.min > 1` was refused with an unactionable 422. The hidden branch now submits `qty_min` and carries `data-quantity-input` so `product.js` keeps it in step.
11. **Every `request.design_mode` branch is a configuration notice, never a different layout.** Four sections carry one — `featured-collection`, `our-story`, `main-page`, `footer` — and they render *nothing at all* on the live storefront, so an unconfigured section costs no requests either.

**Per-instance dynamic values arrive as section-scoped custom properties, never as inline style.** Three sections do this, all the same way:

```liquid
{% style %}
  #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_m }}; }
  @media (min-width: 768px)  { #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_t }}; } }
  @media (min-width: 1024px) { #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_d }}; } }
{% endstyle %}
```

An inline declaration on the grid would outrank every media query and pin the mobile count to all three tiers. Scoping by `section.id` is also what lets two instances of `featured-collection` on one page carry different counts, and nothing in the theme derives from a hardcoded section id.

**Code-versus-document note.** Seven sections emit `{{ section.shopify_attributes }}` on their root — `hero`, `main-404`, `main-cart`, `main-collection`, `main-page`, `main-product`, `main-search`. Phase 6 §4 established that `shopify_attributes` exists on the **block** object only, not on `section`, and `featured-collection.liquid` correctly omits it. Those seven calls therefore emit nothing. Harmless, but they are dead output and the Phase 5 §10 claim that the hero "emits `section.shopify_attributes`" is superseded by Phase 6's finding.

The header publishes its own clearance rather than the hero reading its settings:

```liquid
{%- if overlay -%}<style>
  :root { --header-overlay-offset: var(--header-height-mobile); }
  @media (min-width: 1024px) { :root { --header-overlay-offset: var(--header-height-desktop); } }
</style>{%- endif -%}
```

and `section-hero.css:31` consumes it behind `#MainContent > .shopify-section:first-child .hero`, because *which section the header overlays* is a fact only a selector can know — not a setting a merchant would have to keep in sync with the order they just dragged.

### Global settings — `config/settings_schema.json`

Nine entries: `theme_info` plus eight groups, **14 settings total.** (Phase 11 recorded eleven; Phases 12, 15 and 16 added three.)

| Group | Setting | Type | Default | Drives |
|---|---|---|---|---|
| `theme_info` | — | — | God Squad, v0.5.0 | `theme_support_email` and `theme_documentation_url` are **absent** — see below |
| Colours | `color_scheme` | select | `godsquad` | the whole palette, one option today; labelled "Brand palette" so it stops colliding with every section's "Colour scheme" |
| Typography | `type_display_font` | font_picker | `playfair_display_n9` | `--font-display` |
| | `type_body_font` | font_picker | `jost_n4` | `--font-body`, plus the 500/600 faces |
| Layout | `container_width` | range 1200–1800 step 20 | 1440 | `--container-standard` |
| | `radius_sm` | range 0–8 step 1 | 2 | `--radius-sm` |
| Products | `product_image_ratio` | select square/portrait | `square` | `--product-aspect` — one ratio for the whole catalogue |
| | `card_hover_secondary_image` | checkbox | `false` | CSS-only second-photo hover (Phase 12) |
| Brand | `logo` | image_picker | empty | header **and** footer |
| | `favicon` | image_picker | empty | three icon sizes |
| | `share_image` | image_picker | empty | `og:image` fallback (Phase 16) |
| Cart | `cart_type` | select drawer/page | `drawer` | the drawer gate in the layout |
| Customer accounts | `customer_account_menu` | link_list | `customer-account-main-menu` | `<shopify-account menu="…">` (Phase 15) |
| Social | `social_facebook_url` | url | empty | footer row, rendered only when set |
| | `social_instagram_url` | url | empty | footer row, rendered only when set |

`config/settings_data.json` carries a `current` block and one preset, `"God Squad"`, with the same values. The two social keys are absent from both — blank is the shipped state and no profile was invented.

**The colour guardrails.** A Shopify `color` setting is unconstrained: `settings_schema.json` has no validation hook and no on-save callback, so a merchant nudging cream darker would silently invalidate every measured pairing in the system (G1). And `--color-accent-strong` `#82672B` is a fixed hex, not computed from the gold, so changing the gold alone leaves the light-surface accent behind (G2). Both are answered by replacing three free pickers with a **scheme select resolved in exactly one place** — `snippets/css-variables.liquid` — which emits `--gs-ink`, `--gs-cream`, `--gs-gold` and `--gs-gold-strong` *together*, so the pair cannot desynchronise. The snippet takes a `part` parameter (`meta` | `style`) and is rendered twice from the layout rather than resolving the scheme twice, which would be the exact drift G2 exists to prevent.

One scheme ships, and that is a deliberate limitation. Adding a second is not an engineering decision: it needs brand approval of the values and a measurement pass across the Phase 2 §3 matrix.

`theme_documentation_url` and `theme_support_url` originally shipped as empty strings against a `format: uri` schema, which was the theme's only Theme Check ERROR; Phase 10 omitted them rather than fabricate URLs. Theme Check now asks for `theme_support_email` and `theme_documentation_url` in `theme_info` — those are the **two remaining offenses**, both business information.

### The snippet set — 23 files

| Family | Files | Contract |
|---|---|---|
| Icons (9) | `icon-account`, `icon-arrow`, `icon-cart`, `icon-chevron`, `icon-close`, `icon-menu`, `icon-minus`, `icon-plus`, `icon-search` | Inline SVG only. `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`, round caps and joins, `aria-hidden="true" focusable="false"`, `class="icon icon--NAME {{ class }}"`. Every one is decorative — the consuming control carries the accessible name. No raster, no colour baked in. |
| Product (4) | `product-card`, `product-media-gallery`, `product-variant-picker`, `quantity-selector` | `quantity-selector` has three consumers (product form, cart line, drawer line). |
| Cart (5) | `cart-line-item`, `cart-note`, `cart-totals`, `cart-empty-state`, `cart-icon-bubble` | `cart-empty-state` and `cart-icon-bubble` each serve two surfaces. |
| Infrastructure (5) | `css-variables`, `meta-social`, `grid-sizes`, `pagination`, `facets` | |

Rules worth knowing before you touch any of them:

- **`product-card.liquid` is the only card, and no second one should be created.** Three sections render it — `featured-collection`, `main-collection`, `main-search` — with zero page-scoped CSS overrides. Its accepted parameters are `product` (required), `heading_level` (default 3), `sizes`, `eager` (default false), `show_price`/`show_compare_at`/`show_swatches` (default true) and `quick_add` (default false, off in every shipped configuration). The caller computes `sizes` because the caller is what knows the grid.
- **`grid-sizes.liquid` is the single shared `sizes` derivation** for `main-collection` and `main-search`. It encodes two rules learned the hard way: a clause may not claim a width before the layout that produces it applies (desktop threshold floored at 1024), and a clause may not divide by more columns than actually fit. `featured-collection` is deliberately *not* consolidated into it and carries its own copy — a change to the shared rules must be applied there too. The reason this snippet exists at all: Phase 10 fixed the desktop-clause bug in one of three copies, and the other two carried it for two more phases because the fix was applied to an instance rather than the rule.
- **`pagination.liquid` + `component-pagination.css` are one implementation**, rendered by both collection and search. Phase 18 merged two divergent per-template paginators, taking type and the current-page marker from collection and the accessibility treatment from search.
- **`meta-social.liquid` contains no written copy.** Every value is a Shopify object. The `og:image` chain is product → collection → `settings.share_image` → logo, each branch guarded so a store with no image emits no `og:image`. `og:image:width` is the literal `1200` with height derived from `image.width`/`image.height` and guarded against zero — never from `aspect_ratio`, which is not populated on every image drop and threw a division by zero in the head of all seven templates.
- Snippets are rendered with `{% render %}` only. **Zero `{% include %}` in the theme.**

### The asset set — 21 CSS, 4 JS

Three layers, and no fourth:

1. **`design-tokens.css` (26,309 B)** — custom property definitions and the two surface-context classes. Nothing else. It is the theme copy of the canonical `PHASE-2-DESIGN-TOKENS.css` in the project root; **change the canonical file first and keep the two in step.**
2. **`base.css` (3,722 B)** — the only stylesheet that styles bare elements: `box-sizing`, `body { margin: 0; font-family: var(--font-body) }`, the one focus ring, and the reduced-motion suppression block. Loaded immediately after the token file because it consumes those tokens.
3. **Components and sections** — everything else, class-based.

Who links what:

| Loaded from `layout/theme.liquid` (8) | Loaded from its own section (13 links, 11 files) |
|---|---|
| `design-tokens.css`, `base.css`, `header.css` | `section-hero.css`, `section-featured-collection.css`, `section-our-story.css`, `section-footer.css`, `section-main-product.css`, `section-main-collection.css`, `section-main-search.css`, `section-main-page.css`, `section-main-cart.css`, `section-main-404.css`, `section-cart-drawer.css` |
| `component-container.css`, `component-button.css`, `component-pagination.css`, `component-quantity.css`, `component-cart-line.css` | `component-product-card.css` (by `featured-collection`, `main-collection`, `main-search`), `component-facets.css` (by `main-collection`, behind `has_filters`) |

The promotion rule, written into the stylesheets themselves: **a component stylesheet with more than one consumer on the same page moves to the layout.** `component-product-card.css` has three consumers but is never double-linked on one page, so it stays with its sections — promoting it would load the theme's largest stylesheet onto pages with no cards. `section-main-collection.css` carries the trigger in a comment ("the moment a second surface renders it, the block moves to `assets/component-pagination.css`"), and Phase 18 executed it.

**Stylesheets sit inside their section's render guard, not at the top of the file.** `featured-collection.liquid` emits both of its links inside the `{%- else -%}` arm of `if has_products == false and request.design_mode == false`, so an unconfigured collection row costs no requests either. `main-search.liquid` emits the card sheet inside its results branch, because the landing state of `/search` is a form and one line of copy with not a single `.product-card` on it. `main-collection.liquid` emits `component-facets.css` *and* `facets.js` only when `has_filters`.

JavaScript — four files, no dependencies, no framework, no polyfill, every one `defer`:

| File | Bytes | Loaded from | Notes |
|---|---:|---|---|
| `cart.js` | 39,750 | layout | 12,073 B gzipped, above Shopify's 10,000 B `AssetSizeJavaScript` threshold. 4,930 B with comments stripped — the threshold is not reachable by deleting prose. Recorded, not fixed. |
| `header.js` | 13,963 | layout | |
| `product.js` | 18,096 | `main-product.liquid` | |
| `facets.js` | 10,937 | `main-collection.liquid`, behind `has_filters` | |

One global: `window.GodSquad.cart`. `window.Shopify` is never written to. `cart.js` adds a `cart-js` class to `<html>` itself rather than relying on the layout's `no-js`→`js` swap, because the `.main-cart__update` no-JS fallback keys on `cart-js` specifically.

**`{% stylesheet %}` and `{% javascript %}` tags are not used anywhere** — zero occurrences. All CSS and JS are separate files under `assets/`.

### The surface-context model

This is the mechanism that makes it structurally impossible to put gold on cream. A section declares its surface as a class and everything inside inherits; **no section sets `background-color` directly.**

```css
.surface-dark {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  --color-border-current: var(--color-border);
  --color-border-current-subtle: var(--color-border-subtle);
  --color-border-current-interactive: var(--color-border-interactive);
  --color-text-current-muted: var(--color-text-muted);
  --accent-current: var(--color-accent);
  --focus-ring: var(--focus-ring-on-dark);
  --shadow-current: var(--shadow-on-dark);
}
.surface-light {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-inverse);
  --color-border-current: var(--color-border-inverse);
  --color-border-current-subtle: var(--color-border-inverse-subtle);
  --color-border-current-interactive: var(--color-border-interactive-inverse);
  --color-text-current-muted: var(--color-text-inverse-muted); /* NOT --color-text-muted, 1.76:1 here */
  --accent-current: var(--color-accent-strong);   /* NOT --color-accent, 1.55:1 here */
  --focus-ring: var(--focus-ring-on-light);
  --shadow-current: var(--shadow-elevated);
}
```

The rules that follow from it:

- **A component reads `--accent-current`, `--color-border-current` and `--focus-ring`; it never chooses a colour.** On a light surface those names do not resolve to gold, so a component *cannot* put gold on cream. Muted gold `#D8C08A` measures 1.55:1 on warm cream `#F3EFE6` and 1.43:1 on the tile cream `#EBE6DC`; on light surfaces the accent is `--color-accent-strong` `#82672B`, 4.66:1 on cream.
- **Nothing outside `design-tokens.css` may reference `--gs-*`.** That is the raw palette layer; components read the semantic layer.
- **A component never chooses its focus ring.** The surface class reassigns `--focus-ring`, and `base.css` applies it once, at zero specificity: `:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible { outline: var(--focus-width) solid var(--focus-ring); outline-offset: var(--focus-offset); }`.
- **A cream band authored as `background-color` instead of `.surface-light` inherits the root's gold focus ring at 1.55:1.** That is the failure the model exists to prevent.
- Where the surface is not a merchant choice the class is hardcoded — both cart surfaces hardcode `surface-dark`, and neither schema exposes a surface setting, so `.surface-light` selectors in the cart stylesheets are unreachable. Phase 18 deleted four of them and recorded the single reinstatement condition once, in `component-cart-line.css`.

### Tokens

`design-tokens.css` declares **193 distinct custom properties** (207 declarations including breakpoint and reduced-motion redefinitions; 187 distinct names inside `:root` blocks), organised into 17 numbered groups:

1 Core palette · 2 Semantic colour · 3 Typography families · 4 Type scale · 5 Spacing (4px grid) · 6 Containers · 7 Grid · 8 Breakpoints · 9 Borders and radius · 10 Shadow · 11 Motion · 12 Focus · 13 Touch targets · 14 Header and announcement · 15 Product media · 16 Z-index · 17 Component primitives.

Values you will need constantly:

| Token | Value |
|---|---|
| `--gs-ink` / `--gs-cream` / `--gs-gold` / `--gs-gold-strong` | `#0D0C0A` / `#F3EFE6` / `#D8C08A` / `#82672B` |
| `--container-wide` / `--container-standard` / `--container-narrow` | `1680px` / `1440px` / `760px` |
| `--gutter-mobile` / `-tablet` / `-desktop` | `24px` / `32px` / `48px`, switched on `:root` at 768 and 1024 |
| `--bp-sm` … `--bp-2xl` | `480` / `768` / `1024` / `1280` / `1440` px — **reference only; custom properties cannot be used inside media queries** |
| `--product-col-min` | `17rem` (272px) — the auto-fill column floor |
| `--split-rail` / `--split-40-60` / `--split-60-40` | `0.9fr 1.6fr 0.4fr` / `0.9fr 1.6fr` / `1.6fr 0.9fr` |
| `--target-min` / `--target-min-aa` | `44px` / `24px` |
| `--measure-narrow` / `--measure-body` | `40ch` / `68ch` |

Only a small subset is merchant-reachable, emitted by `css-variables.liquid` after the stylesheets: `--gs-ink`, `--gs-cream`, `--gs-gold`, `--gs-gold-strong`, `--container-standard`, `--radius-sm`, `--product-aspect`, `--font-display`, `--font-body`. Everything else is developer-owned, which is what keeps the Theme Editor incapable of breaking the contrast system.

Media-query census across all 21 stylesheets (comments stripped), 65 blocks:

| Query | Blocks |
|---|---:|
| `(hover: hover) and (pointer: fine)` | 27 |
| `(min-width: 768px)` | 11 |
| `(prefers-reduced-motion: reduce)` | 10 |
| `(min-width: 1024px)` | 9 |
| `(max-width: 767px)` | 3 |
| `(max-height: 540px) and (max-width: 1023px)` | 2 |
| `(min-width: 1440px)` | 2 |
| `(min-width: 1280px)` | 1 |

Mobile-first: base rules are the phone, tiers only add. `max-width` queries are deliberately rare — a `max-width` query is an admission that the phone needs something the larger screens must not inherit. Landscape adaptation is gated on **height and bounded on both axes**; there is no `orientation: landscape` query anywhere, on purpose, because orientation says nothing about how much height there is.

One stale comment to be aware of: `design-tokens.css`'s own header still says three values "are overridden at runtime from theme settings, in an inline block emitted by `layout/theme.liquid`". Since Phase 10 that block lives in `snippets/css-variables.liquid` and emits four colour tokens plus container, radius, aspect and both font families. The code is the truth.

### The conventions the theme holds itself to

Each of these is mechanically checkable, and most are asserted by the suites in `scratchpad/phaseNN/`:

1. **No `!important` outside `base.css`.** Exactly four declarations exist, all inside `@media (prefers-reduced-motion: reduce)` in `base.css`, where a user preference must beat an author declaration. Verified by stripping comments from all 21 stylesheets and counting.
2. **No raw hex outside `design-tokens.css`.** Measured: 17 hex literals in the token file (the palette) and four `#000` keywords inside `section-our-story.css` mask gradients. Nothing else.
3. **No inline `style` attribute** except the Liquid-generated custom-property form on a section root, and no `style:` parameter is ever passed to `image_tag` — it writes the focal point as an inline style that outranks every stylesheet rule.
4. **No `{% include %}`, no `#{}` interpolation, no hardcoded storefront route.** Cart URLs are built from `window.Shopify.routes.root`; a literal `/cart/add.js` 404s silently on a store with Markets or a second language.
5. **No hand-built CDN URL.** Every image goes through `image_url` with an explicit `widths` ladder and an explicit `sizes`, then `image_tag`. `image_url: width:` alone emits neither a `srcset` nor a `sizes`. The CDN does not upscale and does not output AVIF — WebP is the delivery format.
6. **Every `<img>` carries `width` and `height`, and any CSS rule for one must set both axes.** `image_tag` writes them as attributes; setting only `width` in CSS once left a cart thumbnail 948px tall and made `aspect-ratio` inert.
7. **Exactly one non-lazy image per page**, and `fetchpriority` at most once.
8. **Every hover rule sits inside `@media (hover: hover) and (pointer: fine)`** so a touch tap never leaves an element stuck in a hover state. Phase 18's `hovergate.py`: 29 rules, 29 gated, 0 ungated.
9. **No merchandising or business data in code.** No product name, price, currency symbol, collection handle, ranking rule, analytics ID, pixel, social URL or hardcoded year appears in any Liquid file. `money` filters everywhere; the footer copyright is `shop.name` + `'now' | date`.
10. **No hardcoded menu label anywhere** — not HOME, SHOP, COLLECTIONS, OUR STORY or VERSE. Navigation is entirely `link_list` settings iterating `link.title` / `link.url`.
11. **Every customer-facing string comes from `locales/en.default.json`**, and the check runs both directions: every `| t` key resolves and no locale key is unused.
12. **Merchant-facing schema strings carry instructions, never project vocabulary.** Phase 18 stripped "Phase 2 §26.1", "the prototype", "the approved mockup", "the rebuild" and "BUSINESS INFORMATION REQUIRED" from ten strings while keeping every instruction's substance.
13. **Shopify Liquid does not escape output.** Untrusted input — cart line-item properties, the cart note, both settable via `/cart/add.js` and `/cart/update.js` — carries `| escape`. This closed a live stored-XSS vector in Phase 17.
14. **Editor-lifecycle discipline for every script that binds outside its own subtree:** idempotent per element, every global binding recorded in one registry and released as a unit, teardown on `shopify:section:unload`. `header.js`, `cart.js` and `facets.js` all follow it; `product.js` needs nothing and deliberately adds no no-op handler.
15. **Comments are held to the same standard as code.** A wrong citation in a comment is a defect and is fixed as one.

### What is unverified, and by what

- **The theme has never run on a real Shopify store.** Everything measured in eighteen phases was rendered through a strict mini-Liquid harness against mock Shopify data, plus headless Edge and Chrome. Unverified against the platform: Section Rendering API behaviour, real `content_for_header` output, real image-CDN behaviour, `paginate.parts` URLs (modelled as `?page=N`), and whether `product_added_to_cart` fires for an Ajax add.
- **Theme Check has been run** — against `god-squad-theme/` with 84 checks, since Phase 16 — and reports **2 offenses**, both `ValidJSON` for the missing `theme_support_email` and `theme_documentation_url`. Both are business information. (Phase 11's "Theme Check has never been run" is superseded; the Phase 10 runner had been pointed at the project root.)
- **Lighthouse and field Core Web Vitals were never measured**, and no score is stated anywhere. TTFB, FCP and field LCP/INP are reported as unavailable, not estimated.
- **Safari was never tested.** Edge 153 and Chrome, zero console errors across 38 pages.
- **One colour scheme, one `settings_data.json` preset.** A second scheme needs brand-approved values and a fresh measurement pass, not an engineering decision.

---

## Design system — colour

Colour is the constraint that shapes the whole God Squad theme. One measured fact — muted gold is illegible on cream — produced the surface-context mechanism, the focus-ring design, the button variant matrix and the Theme Editor's colour guardrails. Read this section before touching any other part of the system.

Canonical files:

| File | Role |
|---|---|
| `god-squad-theme/assets/design-tokens.css` | The shipped token file. 193 unique custom properties. Loaded first in `layout/theme.liquid` (line 135), before `base.css`. |
| `PHASE-2-DESIGN-TOKENS.css` (project root) | The canonical reference copy. 192 properties. |
| `god-squad-theme/snippets/css-variables.liquid` | The only bridge between Theme Editor settings and the token layer. Emits one `{% style %}` block **after** the stylesheets. |

The two token files are byte-equivalent for every colour token. They diverge by exactly one property, `--type-label-lh`, which Phase 18 added to the theme copy and did not backport — a typography token, so it does not affect anything in this section, but it does mean the Phase 4 rule "the canonical file and the theme copy carry identical token sets" is currently violated by one line.

---

### The prohibition

State it precisely, because a loose paraphrase of it is how it gets violated.

> **Muted gold `#D8C08A` measures 1.55:1 on warm cream `#F3EFE6` and 1.43:1 on the tile cream `#EBE6DC`.** Both fail WCAG 2.2 AA at every text size, and both fail the 3:1 floor of SC 1.4.11 for the visual boundary of a UI component. Gold is a **dark-surface accent only**. On a light surface it may never carry text, an icon, a border, a focus ring, a button fill, or any other perceivable mark. On light surfaces the accent is `--color-accent-strong` `#82672B`, **4.66:1 on cream**.

Three clarifications that matter in practice:

1. The prohibition is about **perceivability, not aesthetics**. Gold on cream is not "low contrast but acceptable for decoration" — a mark at 1.55:1 is not reliably visible at all, so there is no decorative exemption. The one legitimate `#000`/gold-adjacent usage anywhere in the theme is inside a CSS `mask` gradient (`assets/section-our-story.css:468,470`), where the colour is a mask channel and is never painted.
2. It applies to the **composited** pixel, not the declared colour. A gold mark over a photograph is governed by the worst pixel behind it, which is why the scrims exist.
3. It is inherited by everything derived from gold. `--color-warning-on-dark` *is* `#D8C08A`; a warning on a light surface is `--color-warning` `#82672B`, never gold.

`--gs-gold-strong` `#82672B` is a **fixed hex, not computed from the gold**. Any change to the gold that does not also change its light-surface partner silently breaks the system. That fact is what produced guardrail G2 below.

---

### Group 1 — the core palette

Three approved colours, seven derived values. Spec-approved and not revisitable: Phase 0 standing rule 1 preserves the visual direction, and no phase may add a colour or a second accent hue.

| Token | Hex | Role | Measured |
|---|---|---|---|
| `--gs-ink` | `#0D0C0A` | The page ground. The site is dark-led, so "primary" means dark | — |
| `--gs-cream` | `#F3EFE6` | Text on dark; the one light band | 17.04:1 on ink |
| `--gs-gold` | `#D8C08A` | Accent | 11.01:1 on ink; **1.55:1 on cream** |
| `--gs-cream-200` | `#E9E4D8` | Long-form body that should recede from a headline | 15.41:1 on ink |
| `--gs-cream-300` | `#EBE6DC` | Product media ground | Ground only; text on it is **unmeasured** |
| `--gs-stone` | `#BDB6A8` | Muted text on dark | 9.70:1 on ink; **1.76:1 on cream** |
| `--gs-olive` | `#4B5443` | Product swatch value | 6.91:1 on cream |
| `--gs-gold-strong` | `#82672B` | The light-surface accent | 4.66:1 on cream |
| `--gs-gold-hover` | `#E6D3A6` | Gold button hover fill | 13.25:1 on ink |
| `--gs-ink-raised` | `#2A2823` | Dark button hover fill | 12.83:1 against cream text |

Every one of the seven derived values either already existed in the prototype or was tuned in **lightness only**, hue and saturation held, so it stays inside the palette family. `--gs-gold-strong` and the six status colours are the only values that exist because the source palette had no equivalent.

**Admission test for a new colour.** All four must hold: derived from an existing palette colour by lightness alone; does a job the existing ten cannot; ratio measured and recorded on **both** surfaces; added under a MINOR version bump. Sampling a colour from photography is out of scope for every phase of this project. A second accent hue is out of scope permanently.

---

### Group 2 — the semantic layer, and the two-group rule

**R1 — token-first.** A component declares no colour literal. The only permitted literal is a value with no token, and that case is a token request, not a licence.

**R2 — group 2 is the only layer a component may read.** Nothing outside `design-tokens.css` may reference a `--gs-*` name. The palette layer feeds group 2 and the two surface-aware focus tokens; that is its whole job, and it exists in one place so the palette can be re-pointed once.

The theme holds to this. Grepping every `.css`, `.liquid` and `.js` file for `--gs-` outside the token file returns **four matches, all of them explanatory comments** (`component-button.css:101`, `section-our-story.css:25`) **plus the four assignments inside `css-variables.liquid`**, which is the one file whose job is to write the palette layer. There is no palette-layer leak in the theme.

R2 carries four documented raw-value exceptions, all declared once inside group 2 and read semantically thereafter: `--color-text-inverse-muted` `#5F5A50`, the six status colours, the border `rgba()` values, and the scrim gradients.

#### Surfaces (5)

| Token | Value | Use |
|---|---|---|
| `--color-bg-primary` | `--gs-ink` | The dark ground — the default |
| `--color-bg-secondary` | `--gs-cream` | The light band |
| `--color-bg-inverse` | `--gs-cream` | Alias of the above, for a light block nested in a dark section. **Not a third surface** — one value under two names. Currently referenced by nothing in the theme |
| `--color-surface-raised` | `--gs-ink-raised` `#2A2823` | Hover fill on dark |
| `--color-surface-tile` | `--gs-cream-300` `#EBE6DC` | Product media ground. 7 consumers |

#### Text (5)

| Token | Value | Ratio | Surface |
|---|---|---|---|
| `--color-text-primary` | `--gs-cream` | 17.04:1 | Dark |
| `--color-text-secondary` | `--gs-cream-200` | 15.41:1 | Dark |
| `--color-text-muted` | `--gs-stone` | 9.70:1 | Dark. **Never on light — 1.76:1** |
| `--color-text-inverse` | `--gs-ink` | 17.04:1 | Light |
| `--color-text-inverse-muted` | `#5F5A50` | 5.97:1 | Light. Declared as a literal precisely so nobody reaches for `--gs-stone` here |

#### Accent (3)

| Token | Value | Ratio | Rule |
|---|---|---|---|
| `--color-accent` | `--gs-gold` | 11.01:1 on ink | **Dark surfaces only** |
| `--color-accent-hover` | `--gs-gold-hover` | 13.25:1 on ink | Gold button hover only |
| `--color-accent-strong` | `--gs-gold-strong` | 4.66:1 on cream | **Light surfaces only** |

A component should name **neither** directly. It reads `--accent-current`, which resolves per surface. In the shipped theme `--accent-current` has 31 consumers; `--color-accent` is named directly only inside `component-button.css`'s `.surface-dark .button--accent` rules, where the surface is already in the selector.

#### Borders — two families, and the distinction is load-bearing (7)

The four decorative border tokens **composite to 1.17–1.35:1**. That is correct for a hairline separator, which carries no information, and it **fails SC 1.4.11 for the boundary of a control**, which needs 3:1. Two interactive tokens were added to close that gap.

| Token | Value | Composited | Permitted on |
|---|---|---|---|
| `--color-border` | `rgba(243,239,230,0.12)` | ~1.32:1 on ink | Decorative hairline, dark |
| `--color-border-subtle` | `rgba(243,239,230,0.08)` | — | Lighter separation, dark |
| `--color-border-strong` | `--gs-gold` | 11.01:1 on ink | **Accent rules only, dark only.** Not the successor to a heavier alpha. Currently referenced by nothing |
| `--color-border-inverse` | `rgba(13,12,10,0.14)` | ~1.35:1 on cream | Decorative hairline, light |
| `--color-border-inverse-subtle` | `rgba(13,12,10,0.08)` | — | Lighter separation, light |
| `--color-border-interactive` | `rgba(243,239,230,0.36)` | **3.02:1 on ink** | Form fields, checkboxes, radios, selects, outlined buttons, swatch rings — dark |
| `--color-border-interactive-inverse` | `rgba(13,12,10,0.46)` | **3.13:1 on cream** | The same, light |

**The rule a reviewer should check:** any element whose boundary is the only thing telling the customer it is a control reads `--color-border-current-interactive`, never `--color-border-current`. `component-button.css` documents this for the Secondary variant; 15 rules in the theme read the interactive token.

Alpha rather than opaque hex is deliberate — it keeps separators tied to whatever surface sits beneath them.

The prototype's brighter footer divider (`rgba(255,255,255,.2)`) was tokenised as `--color-divider` `rgba(243,239,230,0.20)`. **The theme does not use it**: `section-footer.css:27,202` draws the footer hairline with `--color-border-current-subtle` instead. The token is live and unreferenced; if you need that heavier rule, it is there, but the shipped footer is quieter than the token implies.

#### Status (6)

Each status has a light form and a dark form. **They are not interchangeable.**

| Token | Value | Ratio | Surface |
|---|---|---|---|
| `--color-success` | `#3E4636` | 8.57:1 on cream | Light |
| `--color-success-on-dark` | `#8FA07E` | 6.98:1 on ink | Dark |
| `--color-warning` | `#82672B` | 4.66:1 on cream | Light |
| `--color-warning-on-dark` | `#D8C08A` | 11.01:1 on ink | Dark |
| `--color-error` | `#8C3F2E` | 6.39:1 on cream | Light |
| `--color-error-on-dark` | `#D98C7A` | 7.43:1 on ink | Dark |

`--color-warning-on-dark` is gold itself — the one place gold carries meaning rather than emphasis — and it inherits the prohibition without exception.

**How status colour is actually used in the shipped theme, and the pattern to copy.** No status colour is ever a text colour. Every consumer paints a `2px` (`--border-width-strong`) inline-start rule and leaves the text at `inherit`:

```css
/* assets/section-main-product.css:423 */
.main-product__error {
  border-inline-start: var(--border-width-strong) solid var(--color-error);
  color: inherit;
}
.surface-dark .main-product__error { border-inline-start-color: var(--color-error-on-dark); }
```

The sentence itself says what happened, so the colour is never the signal (SC 1.4.1) and never a contrast liability. Four surfaces do this: the product add error and add confirmation (`section-main-product.css:423,453`), the cart-line error (`component-cart-line.css:125,352`) and the product-card error (`component-product-card.css:405`). `--color-warning` / `--color-warning-on-dark` have **no consumer at all** — nothing in the theme is a warning.

Two cart stylesheets record that they deliberately carry **no** `.surface-light` override, because both cart surfaces hardcode `surface-dark` and neither schema exposes a surface setting; Phase 18 deleted three such unreachable selectors. Do not reinstate them without also exposing the setting.

---

### Surface-aware tokens — the enforcement mechanism

**R3 — colour arrives by surface class, not by property.** `.surface-dark` and `.surface-light` are defined at the bottom of `design-tokens.css` and reassign seven custom properties each:

```css
.surface-dark {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  --color-border-current: var(--color-border);
  --color-border-current-subtle: var(--color-border-subtle);
  --color-border-current-interactive: var(--color-border-interactive);
  --color-text-current-muted: var(--color-text-muted);
  --accent-current: var(--color-accent);
  --focus-ring: var(--focus-ring-on-dark);
  --shadow-current: var(--shadow-on-dark);
}

.surface-light {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-inverse);
  --color-border-current: var(--color-border-inverse);
  --color-border-current-subtle: var(--color-border-inverse-subtle);
  --color-border-current-interactive: var(--color-border-interactive-inverse);
  --color-text-current-muted: var(--color-text-inverse-muted); /* NOT --color-text-muted, 1.76:1 here */
  --accent-current: var(--color-accent-strong);   /* NOT --color-accent, 1.55:1 here */
  --focus-ring: var(--focus-ring-on-light);
  --shadow-current: var(--shadow-elevated);
}
```

This is the whole mechanism. **A component that reads `--accent-current`, `--color-text-current-muted`, `--color-border-current-interactive` and `--focus-ring` cannot put gold on cream, because on a light surface those names do not resolve to gold.** A component that hard-codes `--color-accent` can. That is why R2 exists.

Consumer counts in the shipped theme: `--color-text-current-muted` 47, `--accent-current` 31, `--color-border-current-interactive` 15.

#### The focus ring is surface-aware for the same reason

| Token | Value | Ratio |
|---|---|---|
| `--focus-width` | `2px` | — |
| `--focus-offset` | `2px` | — |
| `--focus-ring-on-dark` | `--gs-gold` | 11.01:1 on ink |
| `--focus-ring-on-light` | `--gs-ink` | 17.04:1 on cream |
| `--focus-ring` | resolves to the above by surface | — |

One rule owns focus for the entire theme, in `assets/base.css:58`:

```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}
```

`:where()` contributes **zero specificity**, so any component-level `outline` would silently win. `component-button.css` declares no outline anywhere and says so in a header comment, and that is a standing review check. A component never chooses its own ring.

**The `2px` offset is load-bearing, not cosmetic.** On the hero's cream CTA face, gold-on-cream is 1.55:1 and a ring touching the button would fail SC 1.4.11. The offset puts dark backdrop (measured 9.24:1) on both sides of the ring.

#### Operating rules

1. **Dark sections.** `.surface-dark` is the default. Text `--color-text-primary`, secondary copy `--color-text-secondary`, muted `--color-text-current-muted`, accents `--accent-current` (gold), hairlines `--color-border-current`, focus gold at 11.01:1.
2. **Light sections.** `.surface-light` flips all of it. Muted text becomes `#5F5A50` — never `--gs-stone` — accents become `#82672B`, focus becomes ink at 17.04:1.
3. **Nesting, and what "inverse" means.** "Inverse" is not a third surface. An inverse block is a `.surface-light` nested inside a `.surface-dark`, or the reverse. Nesting the class re-declares all the context variables at that scope, so the nested block is correct by construction. **A nested block must never be styled by overriding individual colour properties** — that is exactly the path that produces gold on cream.
4. **Every `<section>` declares its surface and never sets `background-color` directly.** A cream band authored as a bare `background-color` inherits the root's gold focus ring at 1.55:1. **No seam treatment crosses a surface boundary** — no gradient, hairline or shadow. The colour change *is* the transition. A hairline at `--color-border-current` separates two bands of the *same* surface. A scrim never crosses a surface boundary; the scrim tokens are for photography only.
5. **A page template may not alternate surface more than twice**, which caps any page at three bands of alternating ground. The shipped `templates/index.json` complies exactly: hero (dark) → New Drop (light) → Best Sellers (dark) → Our Story (dark) → footer (dark). Two alternations. This is enforced by configuration, not by code — a merchant adding a third alternation will not be stopped.

#### Which sections choose, and which are fixed

Eight sections expose a `surface` select. All eight use one vocabulary — label **"Colour scheme"**, options **`dark` → "Ink"** and **`light` → "Cream"** (Phase 11 brought the announcement bar's older "Surface / Dark (near black) / Light (warm cream)" wording into line):

| Section | Default |
|---|---|
| `announcement-bar` | `dark` |
| `our-story` | `dark` |
| `footer` | `dark` |
| `featured-collection` | `light` |
| `main-collection` | `light` |
| `main-page` | `light` |
| `main-product` | `light` |
| `main-search` | `light` |

Five sections hardcode `surface-dark` and expose no setting: `header`, `hero`, `cart-drawer`, `main-cart`, `main-404`. On a section whose surface cannot vary, reading the surface-specific token directly (`--color-text-muted` rather than `--color-text-current-muted`) is legal — `header.css:568` does it — but the `-current` form is never wrong, so prefer it.

Two sections state the consequence of the switch in their own merchant-facing `info` string, which is the right place for it:

- `our-story`: *"Ink is the approved treatment for this band. On cream the gold button is replaced automatically, because gold on cream is 1.55:1 and its own edge would disappear."*
- `announcement-bar`: *"Dark is the approved default. On a light surface the accent becomes the darker gold automatically, because muted gold measures 1.55:1 on cream and cannot carry text there."*

---

### Gold budgets

Gold must not become the dominant interface colour. Expressed as surface-scoped ceilings rather than bans:

- **On dark**, gold may fill **at most one button per page** and mark **one selected state per navigation bar**. The cart badge is the one gold status mark.
- Gold may **not** fill a section, a card or a tile.
- Gold may **not** colour body copy, product names or prices, on any surface.
- **On light**, gold may not appear at all. The accent is `--color-accent-strong`.
- Per editorial band, **two accent marks maximum**.

The button system implements the ceiling structurally rather than by convention. `component-button.css` defines `.surface-dark .button--accent` and **no `.surface-light` counterpart at all** — the file's own comment: *"there is no `.surface-light` rule for this variant, so it simply does not paint."* On cream the accent button renders as an unstyled transparent box, which is a visible failure rather than an invisible one.

Two worked applications of the budget:

- **Hero.** Gold appears exactly twice: the heading accent span and the 32px hairline above the supporting statement. **The eyebrow is cream, not gold, and that is a measured decision.** Gold at 13px is normal text and needs 4.5:1, which needs a backdrop at or below 0.081 relative luminance — about half what cream tolerates at 0.153. Rendered at 375px on the *Subtle* overlay, the worst pixel behind the eyebrow carries **cream at 4.67:1 and gold at 3.02:1**. Cream passes, gold fails, and rescuing gold would mean a heavier wash on every setting. Gold stays on the heading accent, which is large text needing 3:1 and clears it everywhere measured (worst case 8.18:1).
- **Our Story.** *Gold is spent once per band.* The eyebrow is the band's single accent mark. An earlier revision also set the three value titles in gold, which made four; the titles now inherit the band's text colour, which also lifts them from 11.01:1 to 17.04:1. Weight, tracking and caps carry the hierarchy instead.

Primary and Accent **never share a hover fill**. The hero's early private copy of the button system turned the cream Primary gold on hover, which collapsed two variants into one and made gold dominant. Primary on dark now lifts to `--color-text-secondary` (15.41:1); Primary on light lifts to `--color-surface-raised` `#2A2823` (12.83:1).

---

### Scrims

A scrim is the only permitted way to darken a photograph. **Never an inline `rgba()` on the media, and never `filter: brightness()`** — a filter dims the garment along with the background.

Two structural rules, both derived from real defects:

1. **A scrim is always a child of the media wrapper and sized to the media, never to the section.** The prototype's mobile black band came from a fade anchored to the section while the image sat below an 88px in-flow nav, so the gradient went solid 88px above the image bottom.
2. **The header scrim is never anchored to the hero section.** It belongs on the header's own box. `header.css:174` draws `.header__scrim` at `height: calc(100% + var(--scrim-header-overhang))`.

#### The header backing rule

Any header sitting over imagery is either opaque `--color-bg-primary` or carries `--scrim-header` on its own box. Acceptance: **nav text measures ≥ 4.5:1 against the composited pixel at its worst point, verified per hero image** — the band must pass on the brightest sample, not the median. Phase 1 measured three prototype nav links at **2.4–2.9:1 over open sky**.

`--scrim-header` is `linear-gradient(180deg, rgba(13,12,10,.93) 0%, rgba(13,12,10,.86) 66%, rgba(13,12,10,0) 100%)` with `--scrim-header-overhang: 4rem`.

**The alpha is measured, not chosen, and it was corrected in Phase 4.** For cream text to reach 4.5:1 over a worst-case near-white sky the ink layer must hold **≥ 0.85 alpha**. Phase 2's original `.85 → .55 at 60% → transparent` ramp left the brightest pixels behind the nav at **1.1–1.7:1**, because it had already faded by the time it reached the link band. The shipped value holds ~0.86 through the **entire** header and fades only below it, which is why the overhang token exists. Both the canonical file and the theme copy were updated together.

When the header is sticky and scrolled it takes a solid ground instead of a scrim (`header.css:190`), because past the first section there is no artwork for a scrim to sit on.

#### Where the code and the token file diverge

The token file declares four photographic scrims plus two additions. Three of them have **no consumer in the shipped theme**:

| Token | Consumers | Reality |
|---|---|---|
| `--scrim-header` | 2 (`header.css`) | Used as specified |
| `--scrim-bottom` | 1 (`section-our-story.css:126`) | Used as it stands, below the split |
| `--scrim-hero-horizontal` | **0** | Superseded. `section-hero.css` authors its own washes |
| `--scrim-top-heavy` | **0** | Unreferenced |
| `--scrim-story-horizontal` | **0** | Deliberately not used — `section-our-story.css:114` records two measured reasons |
| `--color-overlay` `rgba(13,12,10,0.72)` | 2 (`header.css:440`, `section-cart-drawer.css:47`) | The UI backdrop for panels and drawers — **not** a photographic scrim |

**The hero's wash is the current rule, and it is not `--scrim-hero-horizontal`.** The hero exposes four overlay settings and drives the gradient through two custom properties, `--hero-wash-hold` and `--hero-wash-end`, which hold the alpha across the copy column and then release the photograph: **66%/90% at ≥1024px, 54%/82% at ≥1280px, 48%/76% at ≥1440px**. The ≥1024 step exists for contrast; 1280 and 1440 exist to *relax* the wash and give the photograph back. Below 1024 the wash is vertical and bottom-weighted, because the copy sits low.

Measured worst single pixel inside each text element's box, against the shipped copy:

| Setting | 375 eyebrow | 375 heading | 1440 eyebrow | 1440 heading | Verdict |
|---|---|---|---|---|---|
| Subtle | 4.67 | 5.71 | 7.88 | 5.16 | PASS (cream) |
| Medium *(default)* | 11.98 | 12.97 | 13.67 | 12.16 | PASS |
| Strong | 14.52 | 14.96 | 15.29 | 13.50 | PASS |
| **None** | **1.00** | **1.00** | **1.00** | **1.00** | **FAIL** |

With the scrim removed, the worst backdrop pixel behind every one of the four hero text elements carries cream at **1.00:1**. The wash is not a stylistic choice — without it the hero has no readable text at all. **`None` cannot be made safe over the current image**; it is retained only because a merchant may later supply a photograph already dark where the words sit, and the setting's help text says exactly that.

The `hero--align-centre` and `hero--align-right` gradients have **not** been contrast-measured, because they are not the approved configuration. Treat them as unverified.

**Our Story's scrim is mandatory and not a merchant choice** — the Phase 2 `overlay_style` select is deliberately not exposed. Its direction derives from `image_side` so it always fades toward the copy, and its base colour follows the surface through `--os-scrim-rgb`: `13, 12, 10` on ink, `243, 239, 230` on cream. The caption rail's backing is anchored to the rail, not to the photograph.

---

### Colour is never the only carrier of meaning

WCAG 2.2 AA is the acceptance bar for every phase, and SC 1.4.1 is enforced case by case rather than asserted:

| State | Colour | The non-colour counterpart |
|---|---|---|
| Sold out | Media dims to `opacity: .6` | A solid ink badge with a cream label (17.04:1 over any photograph), and the state is inside the card link's accessible name |
| On sale | Compare-at struck through in `--color-text-inverse-muted` (5.97:1) | Visually hidden "Sale price" / "Regular price" labels on each figure |
| Desktop nav current page | `--accent-current` | A bottom border |
| Footer current page | `--accent-current` | An underline |
| **Mobile panel current page** | `--accent-current` | An underline — **added in Phase 18.** Before that this was the one navigation marked by colour alone, and the panel is the *only* navigation below `--bp-lg` |
| Pagination current page | `--accent-current` on the bottom border | Weight plus a rule, plus `aria-current`. Phase 18 merged two paginators; the search version had marked the current page with gold alone |
| Add error / add success | A 2px inline-start rule in a status colour | The sentence itself |
| Swatch selected | — | A 2px ring offset 2px, plus the native checked state |

**Every hover rule in the theme sits inside `@media (hover: hover) and (pointer: fine)`** — 29 rules, 29 gated, 0 ungated as of Phase 18. Phase 18 moved nine ungated hover rules across five stylesheets inside the query. Without it a touch tap leaves an element stuck in its hover colour with no pointer present to clear it. Hover is never the only signal, and a global `a:hover { color: gold }` is prohibited system-wide — that exact rule in the prototype turned every link in the light New Drop band to 1.55:1 on hover.

The merchant rich-text inline link must carry a pointer-scoped `:hover` to `var(--accent-current)` in **all five** stylesheets that declare its rest state: collection description, product description, Our Story body, page content, footer.

---

### Merchant-facing colour: the scheme select

Phase 2 raised two guardrails and assigned both to Phase 10, which implemented them.

- **G1 — the colours cannot be free pickers.** A Shopify `color` setting is unconstrained. `settings_schema.json` has no validation hook and no on-save callback, so **there is no mechanism to check a ratio at save time**. A merchant nudging warm cream darker silently invalidates every measured pairing in the system.
- **G2 — a gold scheme must ship its light-surface partner.** `--color-accent-strong` is a fixed hex, not computed from the gold. Changing gold alone leaves the light-surface accent behind.

Both are answered the same way: **the merchant chooses a whole scheme, and each scheme sets its dark-surface gold and its light-surface partner together, so the two cannot desynchronise.** `config/settings_schema.json` exposes exactly one colour setting:

```json
{ "type": "select", "id": "color_scheme", "label": "Brand palette",
  "options": [ { "value": "godsquad", "label": "God Squad (approved palette)" } ],
  "default": "godsquad" }
```

`snippets/css-variables.liquid` resolves it in **one `case` statement** and emits all four values together:

```liquid
--gs-ink: {{ c_ink }};
--gs-cream: {{ c_cream }};
--gs-gold: {{ c_gold }};
/* G2. The light-surface partner travels with the gold it belongs to. */
--gs-gold-strong: {{ c_gold_strong }};
```

**Two mechanics that are easy to get wrong:**

1. The snippet takes a `part` parameter and is rendered **twice** — `part: 'meta'` early in `<head>` for `<meta name="theme-color">`, and `part: 'style'` **after** the stylesheets. The style element must come after `design-tokens.css` or its `:root` declarations lose the cascade. Resolving the scheme in two places is the exact desynchronising G2 exists to prevent, which is why it is one snippet rendered twice rather than two blocks.
2. **One scheme ships, and adding a second is not an engineering decision.** It needs brand approval of the values and a full measurement pass across the contrast register. Inventing alternates would be the identity redesign every phase is forbidden from doing.

**Not exposed at any level:** the status colours, the scrims, the focus tokens, the border tokens, the spacing and type scales, z-index, motion, breakpoints. A merchant cannot break a verified pairing from the Theme Editor. The only colour-adjacent choice below theme level is the per-section `surface` select, and both of its values are pre-measured.

Note one stale artefact: the `[THEME SETTING]` comment block at the foot of `design-tokens.css` still lists `--gs-ink, --gs-cream, --gs-gold -> Colors` as though they were three pickers. The shipped schema has one `select`. **The code is the truth**; the comment predates the Phase 10 guardrail work.

---

### The contrast register

**R4 — no colour pairing ships without a measured ratio.** A pairing absent from this register is unverified and may not be used until it is measured and added. AA needs 4.5:1 for normal text, 3:1 for large text (≥24px, or ≥19px bold) and 3:1 for UI component boundaries.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `#F3EFE6` cream | `#0D0C0A` ink | 17.04:1 | AAA — primary text on dark |
| `#0D0C0A` ink | `#F3EFE6` cream | 17.04:1 | AAA — primary text on light |
| `#D8C08A` gold | `#0D0C0A` ink | 11.01:1 | AAA — the only accessible gold pairing |
| `#D8C08A` gold | `#F3EFE6` cream | **1.55:1** | **PROHIBITED** |
| `#D8C08A` gold | `#EBE6DC` tile | **1.43:1** | **PROHIBITED** |
| `#BDB6A8` stone | `#0D0C0A` ink | 9.70:1 | AAA — muted text on dark |
| `#BDB6A8` stone | `#F3EFE6` cream | **1.76:1** | **PROHIBITED** |
| `#E9E4D8` cream-200 | `#0D0C0A` ink | 15.41:1 | AAA — secondary text on dark |
| `#82672B` gold-strong | `#F3EFE6` cream | 4.66:1 | AA — the light-surface accent |
| `#5F5A50` muted | `#F3EFE6` cream | 5.97:1 | AA — muted text on light |
| `#4B5443` olive | `#F3EFE6` cream | 6.91:1 | AA |
| `#E6D3A6` gold hover | `#0D0C0A` ink | 13.25:1 | AAA |
| `#2A2823` ink-raised | cream text | 12.83:1 | AAA — Primary-on-light hover |
| `#FFFFFF` white | `#0D0C0A` ink | 19.55:1 | AAA — available; cream preferred for warmth |
| `rgba(243,239,230,.36)` | `#0D0C0A` ink | 3.02:1 | AA control boundary |
| `rgba(13,12,10,.46)` | `#F3EFE6` cream | 3.13:1 | AA control boundary |
| `rgba(0,0,0,.25)` swatch ring | cream / tile | **1.82 / 1.81:1** | **FAILED** — replaced by `--color-text-current-muted` |

Standing measured results: **73 contrast measurements pass, 0 fail**, re-run after every change from Phase 14 through Phase 18. Our Story carries 48 pixel-sampled readings across both surfaces at four widths, with the cream-surface eyebrow at 4.66:1 and body at 5.80–5.97:1.

Every figure above was computed from hex values or sampled from rendered pixels. **Sampling protocol, because it has produced wrong numbers:** disable CSS transitions before measuring — both the desktop preview pane and headless Chromium under a virtual time budget freeze transitions at their start value, and a transitioned colour reads as its start value in the same frame. Captures below ~492 CSS px must go through an iframe wrapper of the exact target width and be cropped, because headless Edge will not lay out narrower than that and `--screenshot` crops or scales the result. Verify the photograph actually rendered before measuring anything composited against it.

---

### Open, and deliberately so

| Item | Status |
|---|---|
| **Ink on tile cream `#EBE6DC`** | **Never measured.** No shipped text sits on it — the product name and price fall on the section background, and the sold-out badge is solid ink with a cream label (17.04:1) precisely so it does not depend on the ground. Anything that ever draws text directly on the tile must measure this pairing and add it to the register first. |
| A second colour scheme | Open. Needs brand approval of values plus a full measurement pass. Not an engineering decision. |
| `--focus-ring-companion` | A two-tone ring for an indicator straddling a dark/light boundary. Recorded as a recommendation, not added — it needs a design decision. |
| `--color-border-strong`, `--color-divider`, `--color-bg-inverse`, `--gs-olive`, `--swatch-ring`, `--color-warning*`, three of the scrims | Declared and unreferenced. Phase 16 measured **40 of 192 tokens unreferenced** and left them: a design system is allowed a vocabulary larger than its current usage. Do not delete them, and do not assume a token's existence means it is the shipped rule — check the consumer count. |
| `prefers-color-scheme`, `forced-colors`, `prefers-contrast` | **No handling anywhere in the theme.** Confirmed by grep across `assets/`, `sections/`, `snippets/`, `layout/`. Surface is an authored editorial decision, not a user preference, and no phase specified light/dark-mode behaviour. If a Shopify integration needs it, it is new work. |
| Colourway names for swatches | BUSINESS INFORMATION REQUIRED. The prototype data carries hex only. A hex value is not an accessible name, and colour is never the name. |
| The permitted badge vocabulary | BUSINESS INFORMATION REQUIRED. Only `SOLD OUT` ships. No `SALE` badge, no `NEW` badge; if `NEW` is ever wanted the only approved mechanism is a merchant-set tag name, default empty, with `SOLD OUT` always winning the slot. |
| `--type-label-lh` | Present in `god-squad-theme/assets/design-tokens.css`, **absent** from the canonical `PHASE-2-DESIGN-TOKENS.css`. Backport it, or retire the canonical copy — the two files are supposed to carry identical token sets. Every **colour** token is identical between them. |

---

## Design system — typography

### The two typefaces, and the third that is specified but unused

The brand was approved with three families and they were never revisited (Phase 0 §5, standing rule 1: "The visual direction is approved and preserved"). Phase 2 §5 did not choose faces — it fixed which face does which job and which jobs each face is barred from. The shipped theme consumes two of the three.

| Token | Stack (`assets/design-tokens.css:140-142`) | Faces actually registered | For | Explicitly not for |
|---|---|---|---|---|
| `--font-display` | `'Playfair Display', Georgia, 'Times New Roman', serif` | `playfair_display_n9` (900) only | Hero headline, page titles, section/campaign headlines, merchant rich-text `h1`/`h2`, the wordmark | Interface text, navigation, buttons, labels, prices, product names, body copy, form text |
| `--font-body` | `'Jost', Helvetica, Arial, system-ui, sans-serif` | `jost_n4` plus 500 and 600 via guarded `font_modify` | Everything the customer reads to transact — nav, product titles, prices, body copy, buttons, labels, eyebrows, captions, H3/H4 interface headings | Hero and collection headlines. Jost also carries neither `₱` U+20B1 nor `→` U+2192 |
| `--font-script` | `'Kaushan Script', 'Brush Script MT', cursive` | none — no `font_face` call, no setting | Specified for one editorial accent per section, max two per page | Navigation, buttons, prices, product information, long paragraphs, eyebrows, captions, form labels |

**Measured against the code (grep over the 21 stylesheets):** 92 rules declare `font-family: var(--font-body)`, 11 declare `var(--font-display)`, **0 declare `var(--font-script)`**. `--font-script`, `--type-script-size` and `--type-script-lh` have zero consumers anywhere in the 75-file theme, and `config/settings_schema.json` exposes only two `font_picker` settings, so a merchant cannot select a script face either. The script accent is a specified role with no implementation — treat it as open, not as shipped.

The eleven display-family rules are the entire Playfair inventory: `.header__wordmark`, `.header__panel-link`, `.hero__heading`, `.featured-collection__heading`, `.our-story__heading`, `.main-404__title`, `.main-cart__title`, `.main-collection__title`, `.main-page__title`, `.main-page__content h1, h2`, `.main-search__title`.

#### How the faces are loaded

Two `font_picker` theme settings, both with the approved defaults:

| Setting id | Label | Default |
|---|---|---|
| `type_display_font` | Display font | `playfair_display_n9` |
| `type_body_font` | Body and interface font | `jost_n4` |

`snippets/css-variables.liquid:105-110` redefines `--font-display` and `--font-body` from `settings.*.family` + `fallback_families`, so a merchant font change reaches every one of those 103 rules without touching CSS. `layout/theme.liquid` emits the faces:

```liquid
assign body_medium   = settings.type_body_font | font_modify: 'weight', '500'
assign body_semibold = settings.type_body_font | font_modify: 'weight', '600'
{% style %}
  {{ settings.type_display_font | font_face: font_display: 'swap' }}
  {{ settings.type_body_font    | font_face: font_display: 'swap' }}
  {%- if body_medium %}{{ body_medium | font_face: font_display: 'swap' }}{% endif %}
  {%- if body_semibold %}{{ body_semibold | font_face: font_display: 'swap' }}{% endif %}
{% endstyle %}
```

Three rules here, each of which was a live defect at some point:

1. **`font_face` must stay inside `{% style %}`.** The filter returns a bare `@font-face` rule, not a style element. Phase 10 found it emitted unwrapped: no face was ever registered (every heading and every line of body copy fell to a generic fallback on every page), and because a non-whitespace character token ends the HTML "in head" insertion mode, the CSS text rendered as visible content above the logo and everything after it in source order was parsed in body context.
2. **The weights the tokens spend must have real faces.** Phase 16 found `--type-eyebrow-weight` (500) and `--type-label-weight` / `--type-price-weight` (600) had no face at all across 19+ rules, so the browser synthesised them from Jost 400. Faux bold is thicker, wider and tracks differently, which on a type system built out of tracked caps was visible on every surface. Fixed by the two `font_modify` calls above.
3. **Each `font_modify` call is guarded**, because the filter returns nil when the family has no such variant. A merchant who picks a single-weight font gets synthesis back silently — there is no `font-synthesis: none` anywhere in the theme, deliberately or otherwise.

**`--weight-semibold` does not give 600 on the display family.** Only `playfair_display_n9` is registered and no `font_modify` is applied to the display setting, so `--weight-semibold` on `--font-display` resolves to the 900 face. Phase 18 found three rules doing exactly that. Never pair a sub-900 weight token with `--font-display`.

#### The floor under the two-typeface rule

`assets/base.css:44` is the only global type declaration in the theme:

```css
body { margin: 0; font-family: var(--font-body); }
```

There are no global `h1`–`h6`, `p` or element type rules. Every component declares its own type. The `body` line was added in Phase 18 as a safety net after measuring 223 elements across thirteen surfaces inheriting Times New Roman (all screen-reader-only, so nothing looked wrong). Its blast radius was measured first: 1 element of 919 across 8 surfaces, against a probe noise floor of 756. It does **not** reach form controls — the user agent does not inherit a font into `button`, `input`, `select` or `textarea`, so every component that has one declares `font-family` itself.

### The type scale

Fifteen size steps, `assets/design-tokens.css:158-228`. Every step is a token triplet or quartet (`-size`, `-lh`, `-ls`, `-weight`); nothing is a literal. Weight, transform and family are stated by the system, not by the token file, except in the tracked set where `-weight` is tokenised.

| Token group | Size | Weight | Line-height | Tracking | Transform | Family | Role |
|---|---|---|---|---|---|---|---|
| `--type-display-xl-*` | `clamp(3.5rem, 8.5vw, 7rem)` 56→112px | 900 | `0.88` | `-0.01em` | uppercase | display | Hero headline, one per page |
| `--type-display-l-*` | `clamp(2.5rem, 4.6vw, 4rem)` 40→64px | 900 | `0.90` | `-0.01em` | uppercase | display | Campaign / collection-row headline |
| `--type-display-m-*` | `clamp(2rem, 4vw, 2.5rem)` 32→40px | 900 | `1.05` | `0em` | uppercase | display | Story and major section headline; **in practice every page title** |
| `--type-h1-*` | `clamp(2rem, 3.4vw, 3rem)` 32→48px | 900 | `1.05` | — | uppercase | display | Specified for template page titles — **zero consumers in the theme** |
| `--type-h2-*` | `clamp(1.625rem, 2.6vw, 2.25rem)` 26→36px | 900 | `1.15` | — | uppercase | display | Sub-section heading; shipped only on merchant rich text |
| `--type-h3-*` | `clamp(1.25rem, 1.8vw, 1.5rem)` 20→24px | 600 | `1.25` | — | sentence | **body** | Interface heading |
| `--type-h4-*` | `1.125rem` 18px | 600 | `1.35` | — | sentence | **body** | Card and block heading |
| `--type-script-*` | `clamp(1.875rem, 3vw, 2.75rem)` 30→44px | 400 | `1.10` | — | none | script | The single script accent — **zero consumers** |
| `--type-body-lg-*` | `1.125rem` 18px | 400 | `1.65` | — | none | body | Lead paragraph |
| `--type-body-*` | `1rem` 16px | 400 | `1.65` | — | none | body | Default paragraph |
| `--type-body-sm-*` | `0.875rem` 14px | 400 | `1.55` | — | none | body | Legal, helper text, secondary links |
| `--type-eyebrow-*` | `0.8125rem` 13px | `--weight-medium` 500 | inherit | `0.30em` | uppercase | body | Section eyebrow, verse, tagline |
| `--type-label-*` | `0.75rem` 12px | `--weight-semibold` 600 | `--type-label-lh` `1.45` | `0.22em` | uppercase | body | Navigation, buttons, product name, control labels |
| `--type-caption-*` | `0.75rem` 12px | `--weight-regular` 400 | inherit | `0.20em` | uppercase | body | Announcement, footer, counts, badges |
| `--type-price-*` | `0.9375rem` 15px | `--weight-semibold` 600 | inherit | `0em` | none | body | Price |

Plus one line-height that is not a step: `--type-tagline-lh: 1.70` (line 228), for stacked tracked-uppercase blocks. It modifies the eyebrow/label roles; it does not add a sixteenth size. Three rules consume it: `.hero__description`, `.featured-collection__description`, `.footer__tagline`.

Weight tokens, `design-tokens.css:144-147`: `--weight-regular: 400`, `--weight-medium: 500`, `--weight-semibold: 600`, `--weight-black: 900`. Weights are referenced by name; a numeric literal in a component is a defect.

#### Corrections to this scale since Phase 2

- **H3 and H4 are body-family interface headings, weight 600, sentence case.** The token file has always said so at `design-tokens.css:170` — *"Playfair for H1-H2, Jost for H3-H4 (interface headings)"* — and Phase 2 §6.1 assigns both rows Family = body. Three shipped rules did the opposite and were moved to `--font-body` in **Phase 18 (2026-09-25)**, which also made the weight honest (see the 900-face trap above). All three interface-heading consumers now agree: `.cart-empty__title`, `.main-collection__empty-title`, `.main-search__empty-title` — each `font-family: var(--font-body); font-size: var(--type-h3-size); font-weight: var(--weight-semibold); line-height: var(--type-h3-lh);` and **no `text-transform`**.
- **`--type-label-lh: 1.45` was added in Phase 18** (`design-tokens.css:217`). The label role shipped size, tracking and weight and no leading for seventeen phases, so every consumer either invented one or inherited `normal`, which for Jost resolves to **1.167** — tight for 12px uppercase carrying 0.22em. Measured: the same product name rendered **14.0px per line in the cart against 17.4px on a product card**, and at 375px the fixture title already wraps to two lines, so it was live on phones. Applied only to the two consumers whose text wraps: `.cart-line__title` directly, and `.product-card__title` through `--product-title-lh: var(--type-label-lh)` (`component-product-card.css:302`). The other 22 single-line label consumers are untouched, because `normal` and 1.45 render identically on one line.
- **Empty-state titles stopped duplicating the page `<h1>`.** Before Phase 18, `.cart-empty__title` and `.main-collection__empty-title` carried the same four type declarations as their own page's `h1` (Playfair 40px/900/uppercase), which renders unconditionally above them. They now take the interface-heading row.

#### What the scale computes to, 375 → 1920 CSS px (16px root)

| Step | 375 | 390 | 430 | 768 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|---|---|
| `--type-display-xl` | 56 | 56 | 56 | 65.3 | 87.0 | 108.8 | 112 | 112 |
| `--type-display-l` | 40 | 40 | 40 | 40 | 47.1 | 58.9 | 64 | 64 |
| `--type-display-m` | 32 | 32 | 32 | 32 | 40 | 40 | 40 | 40 |
| `--type-h1` (unused) | 32 | 32 | 32 | 32 | 34.8 | 43.5 | 48 | 48 |
| `--type-h2` | 26 | 26 | 26 | 26 | 26.6 | 33.3 | 36 | 36 |
| `--type-h3` | 20 | 20 | 20 | 20 | 20 | 23.0 | 24 | 24 |
| `--type-script` (unused) | 30 | 30 | 30 | 30 | 30.7 | 38.4 | 43.2 | 44 |
| `--type-h4`, `--type-body-lg` | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 |
| `--type-body` | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| `--type-price` | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| `--type-body-sm` | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 14 |
| `--type-eyebrow` | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| `--type-label`, `--type-caption` | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |

Three consequences that are load-bearing:

- **Phones are a fixed design.** At 375, 390 and 430 every fluid step sits on its floor. `--type-display-xl` holds 56px below 659px, `--type-display-l` below 870px. Mobile type does not shrink with the viewport, and Phase 9 confirmed body copy is 16px at every viewport and never reduced on mobile.
- **Above 1440 type stops moving.** Every cap is reached at or below 1440 except `--type-script-size`, which reaches 44px at 1467px. What changes on a large screen is the container, not the type. No type breakpoint exists above 1440.
- **The 1440 headline is a copy question.** `--type-display-xl-size` caps at 112px from 1318px up, so 1440 and 1920 render identically; line count follows column width and string length.

#### Why `clamp()` and not breakpoint overrides

Fifteen steps × five tiers is a 75-cell override matrix; fluid it is fifteen declarations. The real argument is that a breakpoint system fails *between* its breakpoints — the prototype had no tier between 901 and 1440, which is exactly where Phase 1 measured the three-column grid squeezed to ~230-250px with the eyebrow, product names and CTA all wrapping (RESP-08). Two constraints on how a clamp is written: **endpoints in `rem`, preferred value in `vw`** (a `vw`-only size ignores the user's root size and fails SC 1.4.4), and **the floor is the phone design, not a fallback**.

Phase 2 §25.5 rule 2: **no breakpoint-specific font-size overrides — if a size needs a tier-specific value, the clamp is wrong.** Verified against the shipped CSS: exactly one `font-size` exists inside a media query in the whole theme, and it is the documented Phase 9 landscape exception (below).

### Family, weight and transform per row, as actually shipped

Measured by parsing all 24 component/section stylesheets. This is the assignment a new surface must match.

| Role / token group | Declarations | Shipped consumers |
|---|---|---|
| `--type-display-xl` | 2 | `.hero__heading` (Playfair 900, uppercase, `text-wrap: balance`) |
| `--type-display-l` | 2 | `.featured-collection__heading` (an `h2`) |
| `--type-display-m` | 15 across 8 files | `.our-story__heading`, `.main-404__title`, `.main-cart__title`, `.main-collection__title`, `.main-page__title`, `.main-search__title`, `.main-product__title` (body family — see exceptions), `.header__wordmark` (its `-ls` only) |
| `--type-h2` | 1 | `.main-page__content h1, h2` (merchant rich text) |
| `--type-h3` | 6 across 5 files | `.cart-empty__title`, `.main-collection__empty-title`, `.main-search__empty-title`, `.main-page__content h3`, `.header__wordmark`, `.header__panel-link` |
| `--type-h4` | 3 | `.facets__bar-title`, `.main-search__other-title`, `.main-page__content h4` |
| `--type-body-lg` | 4 | `.main-404__body`, `.main-page__content blockquote`, `.main-product__price` (size), `.cart-totals__row--final` |
| `--type-body` | 13 across 14 files | Paragraph copy, all text inputs (`.facets__price-input`, `.header__search-input`, `.main-search__input`, `.cart-note__field`, `.quantity__input`) |
| `--type-body-sm` | 27 across 12 files | Helper text, notices, errors, variant/property lines, footer links, sort select, cart totals rows |
| `--type-eyebrow` | 16 across 5 files | `.hero__eyebrow`, `.featured-collection__eyebrow`, `.our-story__eyebrow`, `.header__panel-title`, `.main-search__group-heading` |
| `--type-label` | 65 across 15 files | `.button`, `.header__nav-link`, `.skip-link`, `.product-card__title`, `.cart-line__title`, `.cart-drawer__title`, `.variant-picker__legend`/`__value`, `.main-product__details-summary`, `.facets__summary`, `.cart-note__summary`, `.footer__heading`, sort label, `th` |
| `--type-caption` | 49 across 11 files | `.announcement-bar__item`, `.header__cart-count`, `.product-card__badge`, `.pagination__link`, `.facets__count`/`__chip`, `.our-story__caption`, `.footer__copyright`/`__strapline`/`__tagline`, `.main-product__vendor`/`__low-stock`, `.main-collection__count` |
| `--type-price` | 11 across 4 files | `.product-card__price`, `.main-product__price`, `.cart-line__price`, `.cart-totals__row dd`, `.quantity__input` (weight only) |

Every page `<h1>` in the theme, for reference: `hero__heading` (display-xl), then `main-404__title`, `main-cart__title`, `main-collection__title`, `main-page__title`, `main-search__title` (display-m, Playfair 900, uppercase) and `main-product__title` (display-m metrics, Jost 600). **`--type-h1-*` is defined and consumed by nothing** — if you add a template title, match the display-m set the six shipped titles use rather than reaching for `--type-h1`, or the new page will not match any existing one.

### Tracked uppercase: the brand signature and its rules

Small Jost, uppercase, tracked wide is the single most recognisable typographic gesture on the site (Phase 0 §5 records it as "a brand signature rather than an accident"). The prototype spelled it twenty-plus times with six tracking values and no names; Phase 2 reduced it to four steps.

| Step | Size | Tracking | Weight | Transform |
|---|---|---|---|---|
| `--type-eyebrow` | 13px | `0.30em` | 500 | uppercase |
| `--type-label` | 12px | `0.22em` | 600 | uppercase |
| `--type-caption` | 12px | `0.20em` | 400 | uppercase |
| `--type-price` | 15px | `0em` | 600 | none |

Price is the deliberate exception inside the set: it is the one small-Jost step that is neither tracked nor uppercased, because a tracked price is harder to compare and `₱` sits badly at 0.22em.

The rules, each one violable and worth checking in review:

1. **Size and tracking travel together as one token pair.** Quoting a size without its tracking is a defect (Phase 2 §5.3).
2. **Tracking is never reduced to make text fit.** `0.22em` and `0.30em` are fixed; text wraps to another line instead (Phase 2 §25.5 rule 3).
3. **Tracking stops at numerals.** Prices, quantities, sizes and order numbers are untracked; the 0.20–0.30em signature applies to words only (Phase 2 §27.6 rule 1).
4. **Uppercase is CSS, never the string.** 57 rules across the theme declare `text-transform: uppercase`; **zero** declare `none`, `capitalize` or `lowercase`. Of the 117 strings in `locales/en.default.json` exactly one is all-caps, and it is the initialism `SKU`. Keep it that way: baked caps change what a screen reader announces and cannot be undone by a merchant's locale override.
5. **Multi-line tracked caps take `--type-tagline-lh: 1.70`.** Single-line tracked caps inherit. Wrapping *label* text takes `--type-label-lh: 1.45` (the Phase 18 addition) — those are two different answers to two different problems and must not be merged.
6. **Long tracked blocks have no bounded copy length.** `--type-tagline-lh` assumes a short block and does not constrain one; maximum copy length for the hero taglines is still open.
7. **Nothing load-bearing is hard-broken.** Hard breaks and `text-wrap: balance` belong to headlines and taglines; a product title, price or availability string is never hard-broken (Phase 2 §27.6 rule 2, honoured explicitly at `section-main-product.css:148`).
8. **No scrim over commerce text.** Prices and titles sit on a flat surface token, never on a gradient.

### The label, eyebrow and caption roles, and how to choose between them

The three roles are the same gesture at three jobs, and mixing them up is the most common way to make a new surface look wrong:

- **Eyebrow (13px / 500 / 0.30em)** — the *opening* of an editorial band, and the two hero lines that behave like one: section eyebrow, scripture reference, tagline. Widest tracking, one step up in size, medium weight. Five consumers. It is never a control label and never a count.
- **Label (12px / 600 / 0.22em / lh 1.45)** — anything the customer *acts on or identifies*: navigation links, button labels, product names, fieldset legends, variant values, disclosure summaries, table headers, the skip link. Heaviest weight of the three. Largest role in the theme (65 declarations, 15 files).
- **Caption (12px / 400 / 0.20em)** — *ambient* system text that is read but not acted on: announcement bar, cart badge, footer copyright and strapline, filter counts, sold-out badge, product vendor, low-stock line, pagination, editorial captions. Lightest weight, tightest tracking of the tracked set.

A single-line caption or label with no wrapping needs no line-height token. Anything that can wrap needs `--type-label-lh` (label) or `--type-tagline-lh` (multi-line tracked block) explicitly, because Jost's `normal` is 1.167 and 12px uppercase at 0.22em is unreadable at that leading once it stacks.

Numerals inside these roles: `font-variant-numeric: tabular-nums` appears exactly once, on `.facets__count` (`component-facets.css:194`). It is not a system-wide rule.

### Documented exceptions in the shipped code

These are all deliberate, all reasoned in the file that carries them, and none should be "harmonised" away without reading the reason first.

| Where | What it does | Why |
|---|---|---|
| `.hero__scripture` (`section-hero.css`) | `--type-label-size` 12px with `--type-eyebrow-ls` 0.30em, weight 400 | Documented in Phase 5 §6's rendered-size table as the intended treatment; the one place two tracked steps are mixed |
| `.hero__description`, `.featured-collection__description` | Label size + label tracking, `--type-tagline-lh`, weight 400 (not the label's 600) | Multi-line tracked tagline block, not a control label |
| `.main-product__title` | `--type-display-m` size/lh/ls with `--font-body` and `--weight-semibold` | Phase 2 §5.5 — "if a piece of text tells the customer what something is, what it costs, or where to go, it is Jost." Phase 2 defines **no product-page title scale**; the file records this as a token gap rather than inventing a value. It is the only page title not in the display family |
| `.header__wordmark` | `--type-h3-size` on `--font-display` at `--weight-black`, `--type-display-m-ls` | Phase 18 left it on the display family on purpose: a logotype is not an interface heading |
| `.hero__heading` in `(max-height: 540px) and (max-width: 1023px)` | `font-size: clamp(1.75rem, 9svh, 3rem)` — the **only** `font-size` inside a media query in the theme, and the only size literal | Phase 9: the display scale is normally set from viewport *width*, which in landscape is the dimension that is not scarce. Re-clamped against height so the lockup keeps two lines. 9svh is 34px on a 375px-tall phone; the 28px floor only binds below ~356px of viewport height |
| `.quantity__input` | `letter-spacing: 0` written as a literal rather than `var(--type-price-ls)` | Commented against §27.6 rule 1 (tracking stops at numerals). The only tracking literal in the theme |
| `.header__nav-link` | `font-weight: var(--weight-medium)` beside `--type-label-size`/`-ls` | Preserves the prototype's 500 nav weight. Phase 2 §19 asked for a `--type-label-weight-nav` token instead of an inline weight; that token was never added, so two thirds of the label triplet sit beside a hand-picked weight |
| `.header__panel-link` | Playfair 900 at `--type-h3-size`, uppercase | Phase 2 §19.6 specifies the eyebrow triplet for mobile menu links. Phase 18 confirmed the deviation is real and **recorded it without changing it**, because re-typing a primary navigation surface is a visible design change, not polish. Same for the footer, which stacks two link type systems |

### Reading measure

Two tokens, `design-tokens.css:447-448`: `--measure-narrow: 40ch` (the prototype's 320px story paragraph — an editorial caption measure) and `--measure-body: 68ch` (a reading measure, inside the 60-75 character target). Consumers: `--measure-narrow` on `.hero__description`, `.featured-collection__description`, `.footer__tagline`, `.footer__text`, `.main-404__body`, `.cart-line` copy, and `.our-story__body` **at the ≥1024px rail only**; `--measure-body` on `.main-collection__description`, `.main-search__empty-title`, `.main-page__content` and `.our-story__body` when stacked. Phase 7 records the reasoning: stacked, the copy is a full-width reading column and takes the reading measure; in the rail beside the photograph (~416px track) the narrow cap is what draws. Phase 9 quotes the same cap as "605px", which is the pixel width of 68ch — i.e. `--measure-body`, not `--measure-narrow`; the tokens are the authority.

### Where type meets the contrast rules

WCAG 2.2 AA is the acceptance bar (Phase 2 §24): 4.5:1 for normal text, 3:1 for large text, which Phase 2 states as **≥24px or ≥19px bold**. Read against the computed table above, only `--type-display-xl`, `-l`, `-m`, `--type-h1` and `--type-h2` clear 24px at every width; `--type-h3` reaches 24px only at its 1440 ceiling and must be measured as normal text. Everything in the tracked set (13px and 12px) is normal text and needs 4.5:1 — which is the measured reason the hero eyebrow is cream and not gold: at 375px on the *Subtle* overlay the worst backdrop pixel behind it carries **cream at 4.67:1 and gold at 3.02:1**, while the gold heading accent is large text needing 3:1 and clears it everywhere measured (worst case 8.18:1). Gold on cream is 1.55:1 and may never carry text at all; on light surfaces the accent is `--color-accent-strong` #82672B at 4.66:1.

### Open, unconfirmed, or not measured

Nothing below was decided; do not close any of it by inference.

- **The 12px interface floor and the two downward moves.** The floor (12px persistent interface text, 16px body) raises the prototype's 9px cart badge, 11px announcement, 11px value subtitle and 11px footer lines, and **lowers** the hero verse and taglines 14→13px and the value-tile title 13→12px. The reductions are downward changes to the proportions of a brand-approved mockup. Phase 2 Appendix C asks for explicit sign-off on the reductions, not just the raises; it is still outstanding and the theme ships the reduced values.
- **Typeface finality and hosting.** Whether Playfair Display, Jost and Kaushan Script are final, and whether the faces come from Shopify's library or self-hosted woff2 — specifically whether the library carries Kaushan Script, which is what decides if a third `font_picker` setting should exist at all. The settings schema says as much to the merchant in its own paragraph string.
- **The peso sign.** Jost's loaded faces contain no `₱` U+20B1, so every price renders Jost digits beside a per-platform fallback glyph, shifting optical alignment across devices. Options remain a subset face carrying U+20B1, a different body face, or documented acceptance. Phase 8 §13 lists "check the peso glyph" as a merchant step. The arrow half of this gap **was** closed: `snippets/icon-arrow.liquid` renders a 24×24 `currentColor` SVG with `aria-hidden="true"`, and no literal `→` exists anywhere in the theme or its locale file.
- **Support matrix.** `clamp()` across the whole scale and `text-wrap: balance` on the hero heading were never confirmed against a browser/device support matrix. The hero lockup no longer *depends* on `balance` — `.hero__heading-accent { display: block }` makes the break structural — but a long merchant headline's wrap still does.
- **Whether the 1440 hero headline must hold two lines** as the mockup sets. Measured as 2 lines at every width from 375 up and 3 at 320; at 112px the count follows copy length, not the type scale.
- **Maximum copy length for the tracked tagline blocks**, which `--type-tagline-lh` assumes and does not bound.
- **Font-swap CLS was not measured.** Phase 16 lists it as unmeasurable in this environment; `font_display: swap` ships on all four faces and no Lighthouse or field number exists for the theme. No number should be quoted for it.

---

## Design system — spacing, container and grid

Everything in this section is implemented and shipped. The authority order is: `god-squad-theme/assets/design-tokens.css` defines the values, `god-squad-theme/assets/component-container.css` owns the content column, and each section stylesheet consumes them. Where the phase documents and the code disagree, the code is quoted and the divergence is named.

### The spacing scale

Ten tokens on a 4px base grid, defined at `design-tokens.css:239-248`. There is no eleventh.

| Token | rem | px | Typical use |
|---|---|---|---|
| `--space-1` | `0.25rem` | 4 | Optical nudges; icon-to-text on one line |
| `--space-2` | `0.5rem` | 8 | Tight stacks: value title to subtitle, price to swatch row |
| `--space-3` | `0.75rem` | 12 | Button block padding; announcement bar block padding |
| `--space-4` | `1rem` | 16 | Eyebrow to headline; product name to price; **mobile product-grid column gap** |
| `--space-5` | `1.5rem` | 24 | Grid gaps, mobile gutter, button inline padding |
| `--space-6` | `2rem` | 32 | Tablet gutter; large grid gaps; product-grid row gap |
| `--space-7` | `2.5rem` | 40 | `--nav-gap`; headline to CTA; section padding floor |
| `--space-8` | `3rem` | 48 | Desktop gutter; tile block padding |
| `--space-9` | `4rem` | 64 | Separation between stacked blocks inside one section |
| `--space-10` | `6rem` | 96 | Section padding ceiling only — no direct `var()` consumer exists, and none should |

The scale is deliberately non-linear: 4-8-12-16 in 4px steps, 24-32-40-48 in 8px steps, then 64 and 96. Fine control where spacing is optical, coarse where it is compositional, so two bands cannot end up 8px apart in rhythm and read as a mistake.

**The audit rule (Phase 2 §7.2), and it still holds in the shipped code.** Any spacing value that is not one of these ten tokens, `--gutter`, or a section-rhythm token is a defect. It is checkable with a regular expression, and that is the point of the 4px grid. Verified across all 25 files in `god-squad-theme/assets/`: the only raw pixel values in a `padding`/`margin`/`gap` declaration are

- `header.css:17` — `margin: -1px` inside the `.visually-hidden` clip idiom;
- `header.css:370` — `padding-inline: 4px` on `.header__cart-count`, an 18px badge circle.

Both are the category Phase 2 §7.2 exempts by name: component-intrinsic geometry and header clearance are **dimensions, not rhythm**. Nothing else in the theme sets a spacing value off-scale.

**What the code does *not* do, contrary to Phase 2 §7.5.** Phase 2 required vertical rhythm to run one direction — `margin-block-start` on the element that follows, never a trailing margin. The shipped CSS carries 51 leading-margin declarations and 20 non-zero trailing ones, all from the token scale. The one-direction rule is a strong default, not an invariant, and at least one trailing margin is deliberate: Phase 18 put `margin-block-end: var(--space-7)` on `.main-collection__header` (`section-main-collection.css:77-79`) **precisely** so it would collapse against `.main-collection__toolbar`'s own top margin and leave the unfiltered page unchanged at 40px. Treat "leading margins by default, trailing only when you want collapse and have written down why" as the current rule.

### Section rhythm

Two clamps, `design-tokens.css:251-252`:

| Token | Expression | Floor | Ceiling | For |
|---|---|---|---|---|
| `--section-pad-block` | `clamp(var(--space-7), 6vw, var(--space-10))` | 40px | 96px | Default vertical rhythm for a band |
| `--section-pad-block-tight` | `clamp(var(--space-6), 4vw, var(--space-8))` | 32px | 48px | Structural rather than editorial bands |

Computed (Phase 2 §7.4), in CSS px:

| | 375 | 768 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|
| `--section-pad-block` | 40 | 46.1 | 61.4 | 76.8 | 86.4 | 96 |
| `--section-pad-block-tight` | 32 | 32 | 41 | 48 | 48 | 48 |

Rules that bind:

- **`padding-block` only, never `margin-block`, for band rhythm.** Adjacent bands must meet without margin collapse so a dark band and a cream band share an exact seam. A margin between them is a visible hairline of whatever is behind the page.
- **Inline padding never comes from a `--space-*` token.** It comes from `--gutter`. A section that sets its own inline padding has left the container system.
- **No fixed section heights.** Height is content plus rhythm. Where a minimum is genuinely wanted it is clamped and uses `svh`/`dvh`, never `vh` (see *Responsive rules*).

Two shipped patterns, and you need to recognise both:

1. **Fixed rhythm.** `padding-block: var(--section-pad-block)` on the section root. Used by footer, 404, cart page, collection, product, search.
2. **Merchant-adjustable rhythm.** Three sections — `featured-collection`, `our-story`, `main-page` — expose `spacing_top`/`spacing_bottom` selects with options `none` / `tight` / `standard` (default `standard`). The select emits a modifier class which sets a section-local custom property, and the root composes it:

```css
/* assets/section-featured-collection.css:26-36 */
padding-block: calc(var(--fc-header-clearance, 0px) + var(--fc-space-top)) var(--fc-space-bottom);

.featured-collection--pt-standard { --fc-space-top: var(--section-pad-block); }
.featured-collection--pt-tight    { --fc-space-top: var(--section-pad-block-tight); }
.featured-collection--pt-none     { --fc-space-top: 0px; }
```

The spacing select carries **system values, never free pixels** — a merchant picks a rung, not a number.

**Header clearance is composed into the top padding, and it is a selector, not a setting.** `sections/header.liquid:52-66` publishes `--header-overlay-offset` on `:root` only when the header actually overlays (`--header-height-mobile` 88px, `--header-height-desktop` 122px from 1024). The first section of `<main>` consumes it:

```css
/* assets/section-hero.css:27-33 */
.hero { --hero-header-clearance: 0px; }
#MainContent > .shopify-section:first-child .hero {
  --hero-header-clearance: var(--header-overlay-offset, 0px);
}
```

Four sections carry the same `#MainContent > .shopify-section:first-child` pattern (hero, featured-collection, our-story, and the 404/collection/search stylesheets document why it resolves to zero for them). Position is a fact only a selector can know; a merchant who reorders the home page must not have to keep a setting in sync. Shipped hero rhythm, for reference: base `padding-block: calc(clearance + var(--space-7)) var(--space-8)`, from 1024 `calc(clearance + var(--space-8)) var(--space-9)`.

The hero owns its bottom padding and reserves nothing for what follows — **the section below the hero owns its own top spacing**.

### The container

One utility, `god-squad-theme/assets/component-container.css`, loaded from `layout/theme.liquid:151` (after `design-tokens.css`, `base.css` and `header.css`, so it wins any equal-specificity collision). This file was **only created in Phase 18**; before that the four declarations were copy-pasted into twelve elements across eleven stylesheets. All twelve were verified byte-identical, all used `--container-standard` with `--gutter`, and none was overridden at a breakpoint, before the sweep. Rendered geometry did not change.

```css
.container {
  width: 100%;
  max-width: var(--container-standard);
  margin-inline: auto;
  padding-inline: var(--gutter);
}
.container--wide   { max-width: var(--container-wide); }
.container--narrow { max-width: var(--container-narrow); }
```

The pattern is **full-bleed band, constrained content**: the `<section>` runs edge to edge at every width and carries `.surface-dark` or `.surface-light`; only the inner div is capped. A section never writes `background-color` itself — the surface class is what reassigns `--accent-current` and `--focus-ring`, and a cream band authored with a raw background inherits the root's gold focus ring at 1.55:1.

| Token | Value | Merchant-editable | Live consumers |
|---|---|---|---|
| `--container-wide` | 1680px | No | **None.** `.container--wide` exists and nothing uses it |
| `--container-standard` | 1440px | **Yes** — `settings.container_width`, range 1200–1800 step 20px, default 1440, emitted by `snippets/css-variables.liquid:93` | `.container` (12 elements), `.header__search-form`, `.our-story__notice`, `.our-story__values` cap |
| `--container-narrow` | 760px | No | `.main-page__column`, `.main-search__form` — **directly, not through `.container--narrow`** |

The twelve `.container` consumers, one per section root except Our Story which has two siblings:

`sections/featured-collection.liquid:346` · `footer.liquid:159` · `header.liquid:78` · `hero.liquid:125` · `main-404.liquid:69` · `main-cart.liquid:42` · `main-collection.liquid:298` · `main-page.liquid:105` · `main-product.liquid:151` · `main-search.liquid:140` · `our-story.liquid:205` (`__inner`) and `our-story.liquid:269` (`__values`)

**Three rules were deliberately left out of the sweep, and the reason is written into the component file so nobody "finishes the job":** `.header__search-form`, `.main-page__column` and `.main-search__form`. Each caps a width but takes **no gutter padding**, because its parent already applies `--gutter`. Giving them `.container` or `.container--narrow` would pad them twice — which is the same failure as Phase 2 §8.5's *containers do not nest*: a nested `.container` inherits `--gutter` twice and silently doubles the inline padding. In the shipped markup no container nests inside another.

Other container rules:

- **No page-level `overflow: hidden`.** Overflow is fixed at its source. The prototype masked it on a 1440px wrapper, which is why its "no overflow at any width" finding was a property of the mask. Every `overflow: hidden` in the theme today is on a media box, a scrim wrapper or a clipped card image.
- **A grid never sets its own `max-width`.** It inherits the container.
- **Full-bleed media inside a constrained band** breaks out with its own rule, not by unsetting `max-width` on the container. `.our-story__media` is 70% of the band with no cap; only the copy container and the values row are capped.
- **`html { scrollbar-gutter: stable }` is a global rule that lives in a section stylesheet** — `assets/section-cart-drawer.css:23`, deliberately, with the comment explaining that toggling it with the scroll lock would cause the shift it prevents. Consequence worth knowing before integration: that stylesheet is only loaded when the drawer renders, and `layout/theme.liquid:232-236` skips the drawer on `/cart` and skips it everywhere when `settings.cart_type == 'page'`. So the reservation is absent on the cart page, and absent site-wide for a merchant who chooses the cart page. The size of the resulting difference was never measured.

### The gutter ladder

`--gutter` is the only inline-padding value a container may use. Defined at `design-tokens.css:266-269`, switched by the token file's own two queries at `design-tokens.css:503-504`.

| Token | Value | Applies |
|---|---|---|
| `--gutter-mobile` | `--space-5` 24px | default, below 768px |
| `--gutter-tablet` | `--space-6` 32px | `@media (min-width: 768px)` |
| `--gutter-desktop` | `--space-8` 48px | `@media (min-width: 1024px)` |

Resulting content box inside a 1440px `--container-standard` (computed):

| Viewport | 375 | 390 | 430 | 768 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|---|---|
| Gutter | 24 | 24 | 24 | 32 | 48 | 48 | 48 | 48 |
| Content box | 327 | 342 | 382 | 704 | 928 | 1184 | 1344 | 1344 (capped) |

327, 342 and 382 are the product tile widths Phase 1 measured on the prototype at those widths, so the phone composition was formalised rather than changed.

**Bands that are not containers still bind to `--gutter`.** Five places consume it outside `.container`, and each is a full-bleed band whose inline padding must match the page: `.announcement-bar__inner` (`header.css:75`), `.header__panel` (`:472`, plus `max(var(--gutter), env(safe-area-inset-left))` at `:489`), `.header__search` (`:594`), `.our-story__caption` (`section-our-story.css:314`) and `.our-story__notice` (`:314`+). Drawer chrome (cart drawer, filter drawer) uses `--space-*` directly — a drawer is not a band.

The rule this replaces: the prototype had a media query targeting a `[data-r=pad]` hook no element carried, so the announcement bar kept 48px of inline padding between 521 and 900px while every other band dropped to 24px. **No band carries its own inline-padding value, and no rule may target a hook that does not exist in the markup.**

### Breakpoints

Mobile-first without exception: base rules describe the phone, every tier is `min-width`, and a tier may only add — it never undoes a base rule. Tokens at `design-tokens.css:298-302`. Custom properties cannot appear in a media query condition, so the tokens are reference values and the literal is written in the query.

| Tier | Token | Width | Uses in shipped CSS | What arrives |
|---|---|---|---|---|
| Base | — | < 768px | — | The phone layout |
| Small | `--bp-sm` | 480px | **0** | Nothing. The token is defined and no query uses it |
| Medium | `--bp-md` | 768px | 11 | Announcement bar goes horizontal; hero copy 38rem; Our Story media 4:5 → 3:2; footer two columns; facets become a horizontal row; cart line layout; collection toolbar; search field |
| Large | `--bp-lg` | 1024px | 9 | Desktop header and primary nav; hero overlay composition and copy 42rem; featured-collection copy rail; Our Story three-track rail; product page `--split-60-40`; cart page two columns; footer `auto-fit` row |
| XL | `--bp-xl` | 1280px | 1 | Hero wash hold/end only |
| 2XL | `--bp-2xl` | 1440px | 2 | Hero wash hold/end; Our Story caption-rail floor 9rem → 11rem |
| Above 2XL | — | > 1440px | — | Bands full-bleed, content capped |

Plus, outside the min-width ladder:

- **Three `max-width: 767px` queries, and that is the whole phone-only budget.** `component-product-card.css:90` (grid gap and track floor), `component-facets.css:323` (the filter drawer becomes `position: fixed`), `section-hero.css:58` (full-height hero subtracts the stacked announcement height). A `max-width` query is an admission that the phone needs something larger screens must not inherit; there are three, each justified in its own file.
- **Two landscape queries, bounded on both axes:** `(max-height: 540px) and (max-width: 1023px)` — hero (`section-hero.css:401`) and cart drawer. **There is no `orientation: landscape` query anywhere, on purpose:** orientation says nothing about how much height there is. A tablet in landscape has 1024px of height and needs no help; a phone in landscape has 375px and needs a lot. Height is the thing being reacted to, so height is what the query asks about. The `max-width` half exists so a short desktop window does not get re-proportioned.
- 28 `(hover: hover) and (pointer: fine)` blocks and 10 `prefers-reduced-motion: reduce` blocks. Every hover rule in the theme is inside the first (29 rules, 0 ungated, guarded by a test).

**Test widths.** The current responsive suite is the nine widths Phase 18 fixed — **375, 390, 430 / 768, 820, 1024 / 1280, 1440, 1920** — plus 480 and both landscape orientations. 820 is the specified tablet width; earlier phases had tested 834 (iPad Pro) and therefore only eight of the nine. Phase 2 §25.7's wider list (adding 320, 900/901 as a pair, and 1440 at 160% and 200% zoom) remains the reference for anything touching the old prototype's structural switch. Result across the suite, every phase from 9 onward: **zero horizontal overflow and zero targets below 24px at any tested viewport.**

### The grid

**Start here: three of Phase 2 §8-9's named utilities were never built, and should not be built now without a reason.** There is no `.section` class, no `.grid-12`, and no `.grid--1/2/3/4`. `--grid-columns: 12` has zero `var()` consumers, and so does `--grid-gap` (24px) — every grid in the theme uses `--grid-gap-large` (32px) or `--product-grid-gap`. Each section owns its own root class, its own rhythm custom properties, and its own track list. That is the shipped architecture.

#### The product grid — one mechanism, everywhere

`assets/component-product-card.css:33-46`. This grid serves the home page's featured-collection rows, the collection page and the search page; there is one card snippet (`snippets/product-card.liquid`) and no page-scoped overrides.

```css
.product-grid {
  --product-cols: 2;
  --product-track-ideal: calc(
    (100% - (var(--product-cols) - 1) * var(--product-grid-gap)) / var(--product-cols)
  );
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(max(var(--product-track-floor, var(--product-col-min)), var(--product-track-ideal)), 1fr)
  );
  gap: var(--product-grid-gap);
}

@media (max-width: 767px) {
  .product-grid {
    --product-grid-gap: var(--space-4);   /* 16px column gap */
    row-gap: var(--space-6);              /* 32px row gap, unchanged */
    --product-track-floor: 8rem;          /* 128px */
  }
}
```

Read it as: `auto-fill` asks how many tracks of at least `max(floor, ideal)` fit. When the row can carry the requested count at 272px or wider, `ideal` is larger and the count comes out exactly as asked. When it cannot, the floor wins and the grid **drops a column instead of squeezing one**. There is no breakpoint gap for a layout to fail in, and **no setting a merchant can choose that produces a broken grid**.

Constants and where they come from:

| Value | Token | Why that number |
|---|---|---|
| Column gap ≥ 768 | `--product-grid-gap` = `--space-6` **32px** | Normalised from the prototype's 36px. Note: Phase 2 §9.3 described the shipped token as 24px and flagged the file as disagreeing with itself; the shipped token is **32px** and the ladder below is the 32px ladder |
| Column gap < 768 | `--space-4` 16px | Phase 9 fix. At 375 a 32px gap sat between two 147px cards inside a 24px gutter — the space *between* the cards exceeded the space *around* the row, and each card paid 8px. Row gap left at 32px: vertical space is not the scarce dimension on a phone |
| Catalogue floor | `--product-col-min` 17rem = 272px | Phase 2 §9.3. The prototype squeezed three columns into ~230px between 901 and 1100, where the eyebrow, the product names and the CTA all wrapped. 272px makes a third column impossible below the width where it works |
| Phone floor | `--product-track-floor: 8rem` = 128px | Measured, not chosen. Two columns need 2F + 32px; 8rem is what lets a merchant who asks for two columns get two at 336px of layout width. 320px still gets one, correctly |

**The merchant's column count is a ceiling, not a command.** It arrives as a section-scoped custom property, never inline style, because an inline declaration would outrank every media query and pin the mobile count to all three tiers:

```liquid
{% style %}
  #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_m }}; }
  @media (min-width: 768px)  { #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_t }}; } }
  @media (min-width: 1024px) { #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_d }}; } }
{% endstyle %}
```

Setting ranges and defaults: `columns_mobile` 1-2 (default 2), `columns_tablet` 2-3 (default 2), `columns_desktop` 2-4 — **default 3 in `featured-collection`, default 4 in `main-collection`**.

Measured rendered geometry — these are iframe-cropped captures with transitions disabled, and they are the authority over arithmetic. Home page, `New Drop` preset (3/2/2 ceiling, copy rail from 1024), from Phase 9 §5 and confirmed unchanged by Phase 18 §8:

| Viewport | 320 | 375 | 390 | 430 | 480 | 768 | 834 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Columns | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 |
| Card | 128 | 156 | 163 | 183 | 208 | 336 | 369 | 301 | 396 | 297 | 297 |
| Column gap | 16 | 16 | 16 | 16 | 16 | 32 | 32 | 32 | 32 | 32 | 32 |

Collection page (4/2/2 ceiling, no copy rail), Phase 18 §7: **2 columns / 156px / 16px gap at 375; 4 / 312 / 32 at 1440** — the ladder Phase 2 §25.3 specified (2 phone, 2 tablet, 3 at 1024, 4 at 1280+) produced by the ceiling and the floor rather than by a media query per tier.

One live item to check on a real store: `--split-30-70` is `0.9fr 2.4fr` with **no `minmax(0, …)`**, which Phase 2 §9.6 requires of every track ("`minmax(0, …)` where the track may shrink freely"). `featured-collection` is the only place a `--split-*` token is consumed raw, and an `fr` track's automatic minimum is its content's min-content width, so the copy rail can exceed its nominal share when the heading is long. `.featured-collection__products { min-width: 0 }` exists for exactly that reason on the other track. The measured card widths at 1024 and 1280 are narrower than the fr arithmetic alone predicts; the phase record does not decompose the difference, so re-measure rather than recompute.

**The `sizes` attribute must be recomputed whenever a grid constant moves.** A narrower gap makes cards *wider*, and a `sizes` value computed against the old gap under-declares the slot, which is the direction that costs image quality. The geometry is duplicated in Liquid in **two** places and both must be kept in step with the CSS:

- `snippets/grid-sizes.liquid` — shared by `main-collection` and `main-search`. Constants: `gap = 32`, `gap_m = 16`, `col_min = 272`, `col_min_m = 128`, `chrome_m = 48`, `chrome_t = 64`, `chrome_d = 96` (128 for the copy-column preset), and `container = settings.container_width | default: 1440`.
- `sections/featured-collection.liquid:89-230` — its own copy, deliberately not consolidated because of the copy-rail arithmetic, with a note saying a change to the shared rules must be applied here too.

Two correctness rules the snippet encodes, both learned by shipping them wrong:

1. **A clause may not claim a width before the layout that produces it applies.** The desktop threshold is floored at 1024, because at three columns the arithmetic alone computes 976 — and the desktop column count does not take effect until `--bp-lg`.
2. **A clause may not divide by more columns than actually fit.** At the container cap the row stops growing, but the grid is `auto-fill` with a 272px floor. With 4 requested columns and the container at its 1200px minimum, dividing by 4 declares 253px for a track that paints 346px — a 27% under-declaration.

`capped_track` also adds `| plus: 1` because Liquid's integer division truncates (296 declared against 297 rendered at 1440).

#### Editorial splits

Tokens at `design-tokens.css:283-289`. They are the recorded ratios; the consumers write the track list out with explicit minima, as Phase 2 §9.6 requires.

| Token | Value | Rendered | Live `var()` consumer |
|---|---|---|---|
| `--split-50-50` | `1fr 1fr` | 50/50 | none |
| `--split-40-60` | `0.9fr 1.6fr` | 36/64 | none |
| `--split-60-40` | `1.6fr 0.9fr` | 64/36 | none — `main-product` writes `minmax(0, 1.6fr) minmax(22rem, 0.9fr)` and cites the token in a comment |
| `--split-30-70` | `0.9fr 2.4fr` | 27/73 | `section-featured-collection.css:148`, the one raw consumer |
| `--split-rail` | `0.9fr 1.6fr 0.4fr` | — | none — `our-story` writes `minmax(26rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr)` |

The minima are measured, not decorative:

- **`22rem` on the product page's buying column** so a wide photograph cannot push the purchase controls narrower than their own content.
- **`26rem` on Our Story's copy track.** With the real face and tracking, the two lines of the approved heading set at 253/325 (32px), 285/366 (36px) and 316/406 (40px); the scale caps at 40px from a 1000px viewport, so the track must clear 406px or the browser re-breaks the second line even with the break already in the markup. A 397px track did exactly that. The width comes out of the empty middle track, not out of the photograph.
- **`9rem` → `11rem`** on the caption rail at `--bp-2xl`.

Splits collapse to a single track below their tier in DOM order. The featured-collection copy rail arrives at `--bp-lg` 1024 and not before, because a 0.9fr rail inside a 704px tablet row is ~190px and cannot hold the display heading without breaking every word.

#### The two wrapping rows, and `auto-fill` versus `auto-fit`

They are not interchangeable, and both choices are reasoned in the code.

- **Product grid: `auto-fill`.** Empty tracks are held, so tile width stays constant across collections of different sizes.
- **Our Story values row: `auto-fit`**, `section-our-story.css:273` — `repeat(auto-fit, minmax(min(17rem, 100%), 1fr))` with `gap: var(--grid-gap-large)`. 17rem, not 14: the row is capped at `--container-standard`, and a 14rem floor fits five tracks at 1440, so the schema's sixth permitted block would sit alone on a second row. A 17rem floor fits four, so six tiles read 4 + 2. `auto-fit` collapses the tracks nobody fills, so the shipped three still span the full width. Measured column step: **1 → 2 → 3** across the tiers (Phase 9 §6). Note this supersedes Phase 2 §9.2's "a four-column grid never collapses to one" and §25.3's 2×2 phone values grid — those described the `.grid--4` utility that was never built. A phone genuinely reads a different layout here, deliberately.
- **Footer: `auto-fit` with a floor, and two tiers.** `repeat(2, minmax(0, 1fr))` at 768; at 1024, `repeat(auto-fit, minmax(11rem, 1fr))` with `grid-auto-columns: minmax(0, 1fr)`. The ceiling is six, not four — the section declares `link_list` at limit 4 and `text` at limit 2 — and one track per block would be 128px at the breakpoint. `auto-fit` with a floor degrades to more **rows** instead of thinner columns. `grid-template-columns` has to be cleared explicitly at 1024 because the two-column rule still applies.

#### Two more shipped grids

- **Cart page**, `section-main-cart.css:139-145`: one column below 1024, then `minmax(0, 1fr) 24rem` with `gap: var(--space-8)`. 24rem is fixed rather than a fraction, and the summary is `position: sticky` at `--header-offset-desktop` with its own `max-height` and scroll (SC 2.4.11).
- **Product page**, `section-main-product.css:569-576`: single column in DOM order below 1024, then `minmax(0, 1.6fr) minmax(22rem, 0.9fr)` with `gap: var(--grid-gap-large)`, `align-items: start`.

#### Reading measures

These are not containers and must not be confused with them.

| Token | Value | Used for |
|---|---|---|
| `--measure-body` | `68ch` | Prose that is the page's main reading column: Our Story body at base and tablet, page content, product description, search copy, collection description |
| `--measure-narrow` | `40ch` | Editorial copy over an image, captions, footer text, hero supporting line, and **Our Story's body once it moves into the rail at 1024** |

Measured (Phase 9 §6): the Our Story paragraph is **605px at 768 and 834** and **356px at 1024 and 1440**. Phase 9's prose labels the 605px cap `--measure-narrow`; the code (`section-our-story.css:193` and `:421`) shows the 605px cap is `--measure-body` 68ch and the 356px cap is `--measure-narrow` 40ch. **The code is correct and the Phase 9 sentence mislabels the token.** Body copy is 16px at every viewport and is never reduced on mobile.

### Responsive rules that bind on any new work

1. **Mobile-first, `min-width` only.** Base rules are the phone. A tier may add; it never undoes a base rule. Mobile is designed, not derived — the hero, the story and the collection band each have their own phone arrangement, not a collapsed desktop one.
2. **No `!important`** anywhere except the `prefers-reduced-motion` block in `base.css`, which holds the only four in the theme.
3. **No layout value in a `style=""` attribute.** Merchant-derived layout numbers arrive as section-scoped custom properties inside `{% style %}`, scoped by `#shopify-section-{{ section.id }}` so two instances of a section on one page can differ.
4. **No breakpoint-specific `font-size` overrides.** If a size needs a tier-specific value the `clamp()` is wrong. Tracking is never reduced to make text fit — the text wraps.
5. **No fixed heights; full-height uses the visible viewport.** `svh` for the hero (`clamp(24rem, 52svh, 34rem)` / `clamp(32rem, 68svh, 45rem)` / `clamp(38rem, 82svh, 55rem)`, and `calc(100svh - clearance - announcement)` for full), `100dvh` for the gallery cap and the cart drawer (with a `100vh` line first as the fallback), `60svh` for the cart page.
6. **Landscape re-proportions; it never removes.** The hero's landscape block drops `min-height` to `calc(100svh - clearance)`, pads the top to clear the overlaid header exactly with no extra band, re-clamps the heading against **height** (`clamp(1.75rem, 9svh, 3rem)`) because the display scale is normally set from width, and steps each lockup element down one spacing rung. Every element of the approved composition is still present.
7. **A `padding-block` shorthand inside a media query overrides an earlier `@supports` rule at equal specificity.** Safe-area reservations (`max(var(--space-5), env(safe-area-inset-bottom))`) must be re-stated inside the landscape block, not left outside it. Note that `env(safe-area-inset-*)` resolves to 0 under the current `viewport-fit=auto`, so those reservations are inert until `viewport-fit=cover` is enabled — which is a sequenced four-step job (meta change, header top inset, make `--header-overlay-offset` account for it, re-measure the hero everywhere), not a one-line change.
8. **DOM order equals visual order at every breakpoint.** No section uses `order`, `row-reverse` or explicit grid placement to move content away from the order a screen reader reads. Nothing is hidden on mobile.
9. **Two target floors:** `--target-min` 44px and `--target-min-aa` 24px. Targets are never reduced at any breakpoint — if a row cannot hold four 44px targets at 375px, an item moves into the menu panel rather than shrinking. The one standing exception is `.cart-line__title` at 24-28px, a deliberate AA call for a text link inside a cart line, flagged rather than fixed.
10. **Do not add JavaScript to make CSS responsive.** Phase 9 corrected nine responsive defects with zero lines of JavaScript.

### Open and unresolved

- **`--bp-sm` 480px is defined and never used.** Either a tier is missing or the token is dead; no phase decided which.
- **`--container-wide` 1680px and `.container--wide` have no consumer**, and neither do `--split-50-50`, `--split-40-60`, `--split-60-40`, `--split-rail`, `--grid-gap` (24px) or `--grid-columns`. Phase 16 recorded 40 unreferenced tokens theme-wide and left them; they are a specification surface, not dead weight, but a reader should not assume a token is proven because it exists.
- **`auto-fill` versus `auto-fit` for the product grid** was made a decision for the catalogue size, and the catalogue size is still **BUSINESS INFORMATION REQUIRED**. `auto-fill` ships.
- **Whether the featured-collection copy rail survives** a four-column collection page — open.
- **Support matrix** for `clamp()`, `aspect-ratio`, `:has()`, `text-wrap: balance` and container queries was never supplied. Container queries would let the product grid respond to its track rather than the viewport, which is the correct shape for this grid; it has not been attempted.
- **Recorded, not changed, by Phase 18** (all verified, all cosmetic, all left for a deliberate decision rather than a silent edit): the eyebrow-to-headline gap differs between the hero (16px) and the two content bands (24px); five templates put three different distances under the same `display-m` h1; the footer column gap gets *smaller* as the viewport grows.

---

## Design system — components

Every component in this theme is a class in one stylesheet, built from tokens defined in `god-squad-theme/assets/design-tokens.css`. The written specification is `PHASE-2-DESIGN-SYSTEM.md` §10–22; where that document and the shipped code disagree, the code below is the truth and the divergence is called out.

### The component contract

Four rules govern every subsection that follows. They come from Phase 2's "How to use this document" and are the reason the theme has no `!important` outside one reduced-motion block.

| # | Rule |
|---|---|
| R1 | A component declares no colour, size, spacing, radius or duration literal. It reads a token. A value with no token is a token request, not a licence. |
| R2 | Components read the **semantic** layer only. Nothing outside `design-tokens.css` may reference a `--gs-*` palette token. |
| R3 | **Colour arrives by surface class, not by property.** A section carries `.surface-dark` or `.surface-light` and never sets `background-color` directly. |
| R4 | No colour pairing ships without a measured ratio. An unmeasured pairing may not be used. |

The surface classes are what make R3 work. They are the whole mechanism by which a component moved between bands stays legal:

| Reassigned property | `.surface-dark` | `.surface-light` |
|---|---|---|
| `background-color` | `--color-bg-primary` (ink `#0D0C0A`) | `--color-bg-secondary` (cream `#F3EFE6`) |
| `color` | `--color-text-primary` | `--color-text-inverse` |
| `--accent-current` | `--color-accent` (gold, 11.01:1) | `--color-accent-strong` `#82672B` (4.66:1) |
| `--color-border-current` | `--color-border` (1.32:1) | `--color-border-inverse` (1.35:1) |
| `--color-border-current-subtle` | `--color-border-subtle` | `--color-border-inverse-subtle` |
| `--color-border-current-interactive` | `--color-border-interactive` `rgba(243,239,230,.36)` (3.02:1) | `--color-border-interactive-inverse` `rgba(13,12,10,.46)` (3.13:1) |
| `--color-text-current-muted` | `--color-text-muted` (9.70:1) | `--color-text-inverse-muted` `#5F5A50` (5.97:1) |
| `--focus-ring` | `--focus-ring-on-dark` (gold) | `--focus-ring-on-light` (ink) |
| `--shadow-current` | `--shadow-on-dark` | `--shadow-elevated` |

A component that reads `--accent-current` **cannot** put gold on cream, because on a light surface that name does not resolve to gold. That is the entire defence against the project's governing prohibition (gold is dark-surface-only; it measures 1.55:1 on cream and 1.43:1 on the tile cream).

**Where component CSS lives.** `layout/theme.liquid` loads, in order: `design-tokens.css`, `base.css`, `header.css`, `component-container.css`, `component-button.css`, `component-pagination.css`, `component-quantity.css`, `component-cart-line.css`. Everything else is requested by the section that uses it (`{{ 'component-product-card.css' | asset_url | stylesheet_tag }}` inside the section's render guard), so a page without the component never downloads it. `base.css` is the only stylesheet that styles bare elements; it defines no tokens. Note that the base `.icon` rule and the `.visually-hidden` utility live in `header.css`, which is layout-loaded — so they are global despite the filename.

The width of the content column is `component-container.css`: `.container` / `.container--wide` / `.container--narrow`. Phase 18 built this and swept up twelve private copies across eleven stylesheets. **No component declares its own container width.** Three rules deliberately stay out — `.header__search-form`, `.main-page__column`, `.main-search__form` — because they use a narrow measure with no gutter padding and `.container--narrow` would add padding they do not have. Do not "finish the job" by sweeping them in.

---

### Buttons

`assets/component-button.css`, loaded from the layout. One class, four variants, no modifier classes for surface — each variant reads the surface-context properties.

**Geometry (all tokens, no literals):**

| Property | Value |
|---|---|
| `min-height` | `--target-min` 44px |
| `padding` | `--space-4` 16px block / `--space-5` 24px inline |
| `gap` (label → icon) | `--space-3` 12px |
| `border` | `--border-width` 1px solid transparent (so a variant can colour it without moving the box) |
| `border-radius` | `--radius-sm` 2px — a rectangle, never a pill |
| Type | `--type-label-size` 12px, `--type-label-weight` 600, `--type-label-ls` .22em, `text-transform: uppercase`, `line-height: 1.2` |
| Trailing icon | `--icon-sm` 16px, via `.button .icon` |
| Shadow | none |

**Variants and their measured states:**

| Variant | Surface | Rest | Hover | Active |
|---|---|---|---|---|
| `button--primary` | `.surface-light` | fill `--color-bg-primary`, label `--color-text-primary` (17.04:1) | fill `--color-surface-raised` `#2A2823` (12.83:1) | returns to `--color-bg-primary` |
| `button--primary` | `.surface-dark` | fill `--color-text-primary`, label `--color-text-inverse` (17.04:1) | fill `--color-text-secondary` `#E9E4D8` (15.41:1) | returns to `--color-text-primary` |
| `button--secondary` | either | transparent, `currentColor` label, border `--color-border-current-interactive` | fill `--color-border-inverse` (light) / `--color-border` (dark) as a wash | fill returns to transparent |
| `button--accent` | `.surface-dark` **only** | fill `--color-accent`, label `--color-text-inverse` (11.01:1) | fill `--color-accent-hover` `#E6D3A6` (13.25:1) | returns to `--color-accent` |

Rules a new button must obey:

- **Primary and Accent never share a hover fill.** A cream primary that turns gold collapses the two variants and makes gold the dominant interface colour. The hero's original stylesheet had this wrong; it was corrected when the system was promoted out of `section-hero.css` in Phase 6.
- **The accent variant is prohibited on light surfaces**, and the prohibition is enforced twice. There is no `.surface-light .button--accent` rule, so it would paint with no fill; and every consumer picks the variant in Liquid from the section's surface setting — `sections/our-story.liquid` and `sections/main-collection.liquid` both assign `button--accent` on dark and fall back to `button--primary` on cream. A new section must make the same derivation. The reason is the boundary, not the label: gold's ink label passes at 11.01:1 but the button's own edge against cream is 1.55:1, below SC 1.4.11's 3:1.
- **Secondary's boundary uses `--color-border-current-interactive`, never `--color-border-current`.** The decorative border tokens composite to 1.32:1 on ink and 1.35:1 on cream.
- **`:active` must be written at the same specificity as `:hover`.** `.button--secondary:active` unscoped is (0,2,0) and loses to the (0,3,0) surface-scoped hover, so a pointer press — which is necessarily also a hover — would never paint the pressed state while a keyboard activation would. Both actives are therefore written `.surface-light .button--secondary:active, .surface-dark .button--secondary:active`.
- **No `outline` anywhere in this file.** `base.css` owns the ring through a `:where()` rule at zero specificity, so any component-level `outline` would silently win.
- **Disabled** is `opacity: .45`, `cursor: default`, `pointer-events: none`, keyed on `[aria-disabled='true']` as well as `:disabled`. `aria-disabled` is the expected authoring pattern because the control stays focusable and announceable; it is always paired with a reason in text (a sold-out line, a quantity already at its minimum). Opacity is never the only signal.
- **Transitions:** `background-color`, `color`, `border-color`, `opacity` only, all at `--transition-fast`. Never `width`, `padding` or `transform`. No `transform: scale()` on press.
- `.button--full` is mobile-only, except the product card's quick action, which is full width at every width because it is the card's sole action (`snippets/product-card.liquid`).
- **Never a `<span>` or `<div>` wearing button classes.** An anchor navigates, a `<button>` acts; add-to-bag and quick-add are `<button>`, and an unavailable quick-add renders a real `<button aria-disabled="true">`.
- Uppercase labels stay at three words or fewer — at .22em tracking a longer string stops reading as a phrase.
- The trailing mark is `{% render 'icon-arrow' %}` at `--icon-sm`, `aria-hidden`. Never the literal `→`: Jost carries neither U+2192 nor U+20B1, so a text glyph falls back to a per-platform face and its weight and baseline shift between devices.
- **"Add to bag" is a decided term**, not drift (PHASE-2 line 943, PHASE-12 §5). Phase 18 rejected a finding that wanted it unified with the theme's fourteen "cart" strings: the action is "add to bag", the container is the "cart", by choice.

"One primary per band, at most." `button--primary` carries the band's single most important action; everything else is secondary or a text link.

---

### Links

There is **no global `a {}` reset and no global `a:hover`** in this theme. The prototype's `a:hover{color:#d8c08a}` painted gold on every link in the document including links on cream at 1.55:1; it is prohibited system-wide. Hover colour comes from `--accent-current`.

| Link type | Where | Rest | Hover | Target |
|---|---|---|---|---|
| Desktop nav | `header.css` | `--type-label-size` .22em uppercase, band text colour | `color` → `--accent-current` | `--target-min` 44px |
| Mobile panel | `header.css` | same, with a `--color-border-subtle` divider | `color` → `--accent-current` (pointer-scoped) | 44px |
| Footer / policy / social | `section-footer.css` | `color: inherit`, `--type-body-sm-size`, no underline | `color` → `--accent-current` **plus** `text-decoration: underline` at `--link-underline-offset` / `--link-underline-thickness` | `--target-min-aa` 24px |
| Merchant rich-text inline | five stylesheets | `color: inherit`, native underline, `--link-underline-offset` 0.2em, `--link-underline-thickness` 1px | `color` → `--accent-current` | inline exception |
| Product card | `component-product-card.css` | one anchor over media + title, no underline | title `text-decoration-color` transparent → `currentColor` | whole card |
| Editorial CTA | section stylesheets | `.button` classes + `icon-arrow` | see Buttons | 44px |

- **The five rich-text surfaces are one rule repeated five times and must stay in step**: `.main-collection__description a`, `.main-product__description a`, `.our-story__body a`, `.main-page__content a`, `.footer__text a`. Phase 18 found the identical three-declaration rest rule on all five with the `:hover` half on only two, so the same merchant link responded on some pages and not others. All five now carry a pointer-scoped hover to `--accent-current`. **A new surface that styles merchant rich text must declare both halves.**
- **Footer links deviate from Phase 2 §11.6 and the code is the truth.** §11.6 specified rest at `--color-text-muted` and hover to `--color-text-primary`, explicitly *not* gold. As built, `.footer__link` rests at `color: inherit` and hovers to `--accent-current`. Phase 18 verified the footer's two stacked link type systems (policy/menu at 14px sentence case, social at 12px uppercase tracked) and left them as RECORDED — re-typing the footer is a design change, not polish.
- **State is never carried by colour alone** (SC 1.4.1). The desktop nav's current item uses `border-bottom-color`; the mobile panel's current item was split out of its `:hover` block in Phase 18 and given an underline as well as colour; `.footer__link.is-active` carries a persistent underline; the shared paginator marks the current page with weight plus a rule, not gold.
- `--link-underline-thickness` (1px) and `--link-underline-offset` (0.2em) exist as tokens and are used by twelve rules. **Thickness is never animated** — a thickness change is a layout or optical jump. Underline reveals are done with `text-decoration-color` transparent → `currentColor`, which transitions cleanly.
- Standalone links meet `--target-min` 44px. Footer and announcement links take `--target-min-aa` 24px, with the reason written into the stylesheet: they are secondary navigation, not primary controls.
- Link text must be meaningful out of context. No "click here", never a bare arrow as the whole accessible name, and no `href="#"` anywhere — a CTA with no destination does not render at all (the hero's button and Our Story's button both gate on `link != blank`).

---

### Forms

The theme authors **no** newsletter, contact, login or registration form. Customer accounts are Shopify's `<shopify-account>` component; legacy `templates/customers/*` must stay absent. The controls that exist are: the quantity selector, the product variant radios, the header and `/search` search inputs, the collection sort select, the facet checkboxes and price inputs, and the cart note textarea. All of them live inside a Shopify `{% form %}` or a plain `<form method="get">`.

**Field anatomy, as shipped:**

| Property | Value | Consumers |
|---|---|---|
| `min-height` | `--control-height` 48px (the preferred value; `--control-height-min` = `--target-min` 44px is the floor) | search inputs, sort select |
| `padding-inline` | `--space-3` 12px — *not* the button system's 24px | all text fields |
| `border` | `--border-width` solid `--color-border-current-interactive` | all fields |
| `border-radius` | `--radius-sm` 2px | all fields |
| `background-color` | `transparent` at every state, so the control sits on whichever band it is in | all fields |
| `font-size` | `--type-body-size` 16px | all fields |
| Shadow | none | all fields |

**The border rule is absolute: a field never uses `--color-border-current`.** SC 1.4.11 needs 3:1 for a control's visual boundary and the decorative tokens composite to 1.32:1 / 1.35:1. Phase 2 §15.2 recorded this as a token gap; the interactive tokens now exist and are measured (3.02:1 on ink, 3.13:1 on cream). The same substitution is made for `.button--secondary` and the variant chips.

**16px is not cosmetic.** Below 16px iOS zooms the viewport the moment the field takes focus and reflows the whole page around a two-character input. Every field in the theme carries `--type-body-size`, including the compact cart-line quantity input.

Rules for any new control:

- **A real `<label for>` always.** A placeholder is not a label. Several labels are `.visually-hidden` (header search, quantity, cart note) — hidden is acceptable, absent is not.
- **A hidden native input stays in the document and stays focusable.** Radios and checkboxes use the shared `.visually-hidden` utility, never `display: none`, and the focus ring is drawn on the label they control: `.variant-picker__input:focus-visible + .variant-picker__value`, `.facets__checkbox:focus-visible + .facets__label`.
- **Variant chips**: `min-width`/`min-height` `--target-min` 44px, `--space-3` 12px apart, `--radius-none`, label type. Checked state is `border-width: var(--border-width-strong)` and `border-color: currentColor` with the padding reduced by exactly `--border-width` on each side, so choosing a value does not nudge the row. An unavailable value is struck through and muted — never removed, never `disabled`, so a customer can discover the size exists.
- **Checkboxes are drawn, not native**: a `1rem` `::before` box with the interactive border, filled with `--accent-current` when checked. Native `accent-color` cannot be measured against the surface it lands on.
- **The select is native and has no chevron.** `.main-collection__sort-select` sets no `appearance: none` and renders no icon; the `<option>` colours are pinned to `--color-bg-secondary` / `--color-text-inverse` because some engines paint the popup list with the select's own colour over the system background, which on the ink surface means cream text on white. **No control auto-submits on change** (WCAG SC 3.2.2) — the sort form has a visible submit button.
- **Quantity selector** (`assets/component-quantity.css`, three consumers): minus `<button>` / `<input type="number">` / plus `<button>`. The two steppers are `display: none` until `assets/cart.js` puts `.cart-js` on the page, and the native spinners are left in place until then, so the field is steppable with scripting off. Buttons are 44px (SC 2.5.8's spacing exception cannot rescue two flush 24px targets). The value is 16px, `letter-spacing: 0`, `min-width: 3ch` (`2ch` on a cart line). Floor is 1, expressed as `aria-disabled` on the minus button plus `min` on the input; the ceiling is Shopify's own `variant.quantity_rule`, carried **per variant**. No inventory number is ever rendered. The ring is drawn around the whole control with `:has(.quantity__input:focus-visible)` — `:focus-within` painted two concentric rings when the minus button took focus.
- **The 250ms quantity debounce is a deliberate literal**, `QUANTITY_DEBOUNCE_MS = 250` at `assets/cart.js:53`. It must never become a motion token: `--duration-*` collapses to 1ms under `prefers-reduced-motion`, which would remove the debounce for exactly the people most likely to be stepping a quantity from a keyboard.
- **Error and success lines are left-ruled, not boxed**: `border-inline-start: var(--border-width-strong) solid var(--color-error)` on light, `--color-error-on-dark` on dark, at `--type-caption-size`. Errors are `role="alert"` and visible; the add-to-cart confirmation is `role="status"`, not alert. Never colour alone, and **no raw API error, status code or stack** ever reaches the page.
- Every error line sits **outside** the node a section render replaces, or the message dies with the re-render that produced it.
- No `novalidate` on the product form (with scripting off, `min="1"` is the only thing between a typed `-3` and a POST to `/cart/add`). No `autofocus`. No custom dropdown library. No image CAPTCHA. No gold border on a light surface. No shadow on any field.

---

### Product cards

**One snippet, `snippets/product-card.liquid`, one stylesheet, `assets/component-product-card.css`.** Three consumers: `featured-collection`, `main-collection`, `main-search`. There are zero page-scoped overrides and no second card was created — and none should be.

The contract: **one anchor wrapping the media and the title with no other interactive element inside it**; swatches, price and the optional action sit outside it; the focus ring is drawn around the whole card; the title is a real heading at a caller-chosen level; every value is read from the Shopify product object.

**Closed part order:** media → title → price → swatches, plus at most one badge overlaid on the media and one optional action below. The list is closed — a fourth unconditional part would have to survive being multiplied across a whole catalogue.

| Part | Rule as built |
|---|---|
| Focus ring | `.product-card:has(.product-card__link:focus-visible)` draws `--focus-width` solid `--focus-ring` at `--focus-offset`; the anchor's own ring is suppressed with `outline: none`. An `@supports not selector(:has(*))` block gives `:focus-within` as the fallback. This is the one sanctioned place a component touches `outline` — it removes one ring and immediately draws an equivalent on a larger box. |
| Media | `aspect-ratio: var(--product-aspect)` (one ratio for the whole catalogue, from the `product_image_ratio` **theme** setting — never per section, never per product), `overflow: hidden`, ground `--color-surface-tile` `#EBE6DC`. |
| Hover scale | `transform: scale(var(--hover-image-scale))` 1.03 over `--transition-medium`, inside `@media (hover: hover) and (pointer: fine)`. |
| Secondary image | Off by default via the global `card_hover_secondary_image` setting. Absolutely positioned `inset: 0` over the primary inside the same ratio box, `opacity: 0` → 1, and the reveal rule exists **only** inside the hover query, so a touch device has no state that can show it. It picks the first image that is **not** the featured one, never `images[1]`. Always `loading="lazy"`. |
| Sold-out dim | `.product-card--sold-out .product-card__image:not(.product-card__image--secondary) { opacity: .6 }`. **The `:not()` is load-bearing**: the secondary image carries both classes, so a bare selector at (0,2,0) out-specifies the (0,1,0) rule that hides it and repaints two superimposed garments on every device including touch. A separate rule dims the secondary when it is legitimately revealed. |
| Title | Real heading, level follows the section — `h3` normally, `h2` when the merchant clears the section heading, so the outline never skips. Two-line clamp with `min-height: calc(2em * var(--product-title-lh))` where `--product-title-lh` = `--type-label-lh` 1.45, so prices align across a row whatever the titles do. Clamping is visual only: the full title stays in the DOM and in the link's accessible name. Underline reveal via `text-decoration-color`, thickness fixed at `--border-width`, offset `0.25em`. |
| Price | `--type-price-size` / `--type-price-weight` / `--type-price-ls` **0** — the one place the brand's tracking is switched off. Always the `money` filter; no currency symbol is hardcoded anywhere in the theme. A varying price renders "From X" and **no** compare-at. On sale, the compare-at is struck in `--color-text-current-muted`, never red, with visually hidden "Sale price" / "Regular price" labels so the strike-through is not the only signal. |
| Badge | **One badge only: SOLD OUT**, from `product.available`. Solid `--color-bg-primary` fill with a `--color-text-primary` label (17.04:1 over any photograph), `--radius-none`, inset `--space-3`, caption type. No SALE badge and no NEW badge. If NEW is ever wanted, the only approved mechanism is a merchant-set tag name with SOLD OUT always winning the slot. The state is also in the link's accessible name; the `.6` dim is the secondary cue. |
| Swatches | **Information, not controls** on the card, so SC 2.5.8 does not govern their size: `--swatch-size` 16px, `--radius-full`, ring `--color-text-current-muted` (deliberately **not** `--swatch-ring`, which composites to 1.82:1 and cannot reveal a cream colourway on the cream tile). Rendered only from native Shopify swatch data (`value.swatch.color` / `.image`) — no colour is ever guessed from an image or a name. The dots are `aria-hidden`; the colourway names sit beside them as visually hidden text. On the product page the same dot becomes a real control inside a 44px label. |
| Missing image | The tile ground renders and nothing stands in for a photograph that does not exist. Fewer products than requested renders what exists — no placeholders, ever. |
| Alt text | From the image object. When Shopify has defaulted it to the product title, which is already inside the same link, it is emitted empty rather than announcing the name twice. |
| Error line | `.product-card__error` is owned by `component-product-card.css` alone. Phase 18 moved it out of the cart-line grouping, where it had been defined twice at equal specificity and was inheriting the cart's padding and line-height. |
| Card container | **No background, no border, no shadow, no lift, at any state.** |

**Grid.** `.product-grid` is `grid-template-columns: repeat(auto-fill, minmax(max(var(--product-track-floor, var(--product-col-min)), var(--product-track-ideal)), 1fr))`.

- `--product-cols` is the merchant's column count and it is **a ceiling, not a command**: when the viewport can carry the requested count above the floor the count comes out exactly as asked; when it cannot, the grid drops a column instead of squeezing one. There is no setting a merchant can choose that produces a broken grid, and no horizontal overflow at any width including 320.
- Floors: `--product-col-min` 17rem (272px) above 768px; `8rem` (128px) below, because the 272px catalogue floor would force one column on a phone where Phase 2 §13.9 permits two. The 128px track was rendered and read before it was adopted.
- Gap: `--product-grid-gap` 32px, tightening to `--space-4` 16px on the **column** axis only below 768px; the row gap stays 32px because vertical space is not the scarce dimension on a phone.
- **Any change to the gap or the column count must be followed through the `sizes` arithmetic.** `snippets/grid-sizes.liquid` is the shared derivation for `main-collection` and `main-search`; `featured-collection` computes its own and was deliberately not consolidated, so a change to the rules must be applied there too. Two rules bind: a clause may not claim a width before the layout that produces it applies (desktop thresholds floored at 1024), and a clause may not divide by more columns than actually fit.

**Never add to a card:** star ratings or review counts, a second badge, stacked buttons, countdown timers, "only 2 left" urgency, wishlist hearts, a "+3 colours" line, shadows, rounded corners, hover panels revealing extra copy, compare checkboxes, or a vendor name while the catalogue is single-brand. **Nothing may be revealed on hover alone** — a pointer-only affordance is prohibited; the quick action is present at rest or absent, and it is off in every shipped configuration.

---

### Images

Merchant photography does not exist yet, so everything below governs the **reservation** — the aspect box, the fit, the scrim, the alt path — and never the picture. The image half of a visual audit is not assessable on this theme.

| Rule | Detail |
|---|---|
| One delivery path | `image_url` then `image_tag`. `image_url: width:` is the **cap** only — on its own it emits neither `srcset` nor `sizes` and would ship one fixed width to every device. `widths:` and `sizes:` are stated explicitly on every `image_tag` call, never on `image_url`. |
| No hand-built CDN URLs | Asserted by the validators. The single exception is the hero's `<picture>` mobile `<source>`, whose `srcset` rungs are separate `image_url` calls because a `source` cannot come from `image_tag` — still filters, never string concatenation. |
| Intrinsic dimensions | `image_tag` writes `width` and `height` **attributes** automatically. Do not strip them, and **any CSS box for such an image must constrain both axes** — setting only `width` left a cart thumbnail 948px tall and made `aspect-ratio` inert. |
| Never pass `style:` to `image_tag` | It writes the focal point as an inline `object-position`, which outranks every stylesheet rule. Cropping is `object-fit` only, and the focal point is Shopify admin's — the theme offers no focal-point control of its own. Our Story's default with no admin focal point is `object-position: center 33%`. |
| One eager image per page | The LCP image is never lazy. `loading: 'eager'`, `fetchpriority: 'high'`, `decoding: 'async'` on the hero and on the gallery's active medium; `fetchpriority` at most once per page. Everything else is `loading: 'lazy'`, `decoding: 'async'`, no `fetchpriority` (auto is the default). In the gallery, `fetchpriority` follows `is_active` while `forloop.first` keeps `eager`, because the stacked desktop layout renders every slide in document order. |
| Alt | From the image object, never invented. An empty merchant alt correctly announces a mood photograph as decorative. `alt: img.alt \| default: …` does **not** work — Liquid applies `default` to `image_tag`'s output, not to the argument, so the fallback silently never fires. |
| No baked text | No headline, wordmark or fragment of either in the pixels. The current Our Story source violates this and is in the missing-asset register. |
| Format | WebP is the delivery format. The Shopify CDN serves WebP automatically from any uploaded master; **it does not output AVIF** and **it does not upscale** — a `widths` entry above the master's real width returns the master while the `srcset` advertises the larger descriptor. |
| Not theme assets | `assets/` holds only CSS and JS. Content imagery arrives through `image_picker` settings and product media so `image_url` can resize it per width. |

**Scrims.** A photograph that sits under text always carries a scrim token, never an inline `rgba()` and never `filter: brightness()` (a filter dims the garment along with the background). Three structural rules:

1. **A scrim is a child of the media wrapper and sized to the media, never to the section.** Anchoring a scrim to a box the header shares is what produced the prototype's black band and hard seam at every phone width, and it is prohibited system-wide.
2. Every scrim is `aria-hidden="true"` and `pointer-events: none`, and sits behind the content layer. Nothing overlays a focusable element.
3. The scrim only ever softens an edge — it never carries meaning. Each band is complete and legible with CSS gradients unsupported.

| Token | Value / note | Live consumers |
|---|---|---|
| `--scrim-header` | `linear-gradient(180deg, rgba(13,12,10,.93) 0%, rgba(13,12,10,.86) 66%, rgba(13,12,10,0) 100%)` — mandatory on any header over imagery. The alpha is measured, not chosen: cream needs ≥0.85 over a worst-case near-white sky to reach 4.5:1. | `.header__scrim` |
| `--scrim-header-overhang` | `4rem`, added to the scrim's height so the fade happens *below* the content band rather than inside it | `.header__scrim` |
| `--scrim-bottom` | `linear-gradient(180deg, rgba(13,12,10,0) 55%, var(--gs-ink) 100%)` | `.our-story__scrim` |
| `--scrim-hero-horizontal`, `--scrim-top-heavy`, `--scrim-story-horizontal` | **Zero consumers.** The hero authors a gradient per `overlay` setting (`hero--overlay-subtle/medium/strong`) with per-breakpoint `--hero-wash-hold` / `--hero-wash-end` stops; Our Story authors its own from `--os-scrim-rgb`, which flips to cream on the light surface. Both are documented, measured departures — but they are inline gradients in a stylesheet, which is the one place the "tokens only" rule bends for this system. |
| `--color-overlay` | `rgba(13,12,10,.72)` — the **UI** backdrop for drawers and panels, added after Phase 2 flagged that all four scrim tokens are photographic and none could serve a modal | header overlay, facets drawer |

The hero currently ships an AI-generated image with unconfirmed rights. Its schema `info` instructs the merchant to replace it with their own photography or confirm clearance **before launch**; that instruction must not be softened.

---

### Borders

| Token | Value | Contrast | Permitted use |
|---|---|---|---|
| `--border-width` | 1px | — | every border in the system |
| `--border-width-strong` | 2px | — | reserved; see below |
| `--color-border-current` | `--color-border` / `--color-border-inverse` | 1.32:1 ink / 1.35:1 cream | **decorative separation only** |
| `--color-border-current-subtle` | `.08` alpha either way | below 1.3:1 | the lightest permissible separation (announcement underline, panel dividers) |
| `--color-border-current-interactive` | `rgba(243,239,230,.36)` / `rgba(13,12,10,.46)` | 3.02:1 ink / 3.13:1 cream | **every control boundary** |
| `--color-border-strong` | `--gs-gold` | 11.01:1 on ink | accent rules, current-state markers — **dark only** |
| `--color-divider` | `rgba(243,239,230,.20)` | — | the footer's content-group divider, brighter than `--color-border` on purpose |

**The governing split:** neither `--color-border-current` value reaches 3:1, so it may carry only decorative separation, which SC 1.4.11 exempts. Anything that is the visual boundary of a control — a field, a swatch ring, a secondary button, a variant chip, a checkbox box — takes `--color-border-current-interactive`. Phase 2 §15.2 recorded this as a gap and specified text-colour substitutes; the interactive tokens now exist and supersede that workaround.

`--border-width-strong` 2px is permitted in exactly the places the code uses it: the selected variant chip's border, the variant swatch's selection ring, the left rule on an error / success / editor-notice line, and the paginator's current-page marker. It is never used for a hover — **hover never changes a thickness**; a ring that must read thicker is drawn with `box-shadow: 0 0 0 Npx`, which paints outside the border box without affecting layout.

**When a separator is justified — four cases only:** a change of function that is otherwise invisible (an ink band between ink bands); a repeated cell divider inside one band (and a divider that changes axis at a breakpoint must cancel itself on the other axis in the same rule); a control boundary (3:1); a current-state marker. Not justified: boxing a product card, outlining an image, framing a section that already changes background colour, a decorative rule between a heading and its body, or a border standing in for spacing.

**When a border and spacing would do the same job, spacing wins.** The product grid needs no card borders: the gap is the separation and the tile ground already gives every card a visible edge. Budget: at most one horizontal rule per band.

Every border colour is alpha, which ties separators to the surface beneath them — so an alpha border over a photograph is unpredictable and `--color-border-current` is used only on flat surfaces. **Focus is not a border**: it is an `outline` outside the box, so it never changes layout. No border token is exposed to the Theme Editor.

---

### Radius

| Token | Value | Permitted on | Never on |
|---|---|---|---|
| `--radius-none` | `0` | **the default for everything** — sections, bands, media, cards, badges, drawers, modals | — |
| `--radius-sm` | `2px` | text inputs, search inputs, the select, textareas, the quantity control, buttons, chips, the skip link, and the Shopify accelerated-checkout / account custom properties | a product card, a section, an image |
| `--radius-md` | `4px` | held in reserve — **zero consumers in the theme** | anything currently in the design |
| `--radius-full` | `9999px` | circles only: the header cart count, the card swatch dot, the variant swatch | **any button** — 9999px on a 44px control is a pill, which is prohibited |

**A component that is not in that table is square.** Four reasons the system stays flat and none of them is taste: the prototype used `border-radius` exactly twice and both were `50%`; full-bleed bands cannot be rounded without their contents reading as cards floating on a page; rounded corners read as app UI where this brand is positioned as fashion editorial; and a radius on a 1:1 product image clips four corners of the garment on every card in the grid.

`--radius-sm` is the **only** radius exposed to the merchant, under "Button/input style", and the control is a fixed choice of 0, 2 or 4px. A free numeric field would let a merchant set 24px and dissolve the identity in one click. A 2px input beside a 0px button looks like a mistake, which is why the buttons take `--radius-sm` too and follow the merchant automatically.

---

### Shadow

| Token | Value | Status in the theme |
|---|---|---|
| `--shadow-none` | `none` | the default for every component |
| `--shadow-subtle` | `0 1px 2px rgba(13,12,10,.08)` | **zero consumers**; reserved for a future light-surface autocomplete panel |
| `--shadow-elevated` | `0 12px 32px rgba(13,12,10,.28)` | header search panel, facets drawer (light) |
| `--shadow-on-dark` | `0 12px 32px rgba(0,0,0,.55)` | added because ink at low alpha is invisible on `--color-bg-primary`: announcement/header chrome, mobile panel, cart drawer, facets drawer (dark) |
| `--shadow-current` | resolves to `--shadow-on-dark` / `--shadow-elevated` by surface | the surface-aware handle |

**The rule:** depth comes from contrast (the ink/cream band alternation at 17.04:1), spacing (`--section-pad-block`) and photography — never from shadow. Product cards, value tiles, badges, buttons, inputs, swatches and images all carry no shadow. **There is no card-elevation scale and none will be added.**

**An element may carry a shadow only if it also carries a z-index token above `--z-sticky` 100.** If it does not float above the page, it does not get a shadow. The ladder: `--z-header` 200, `--z-overlay` 800, `--z-drawer` 900, `--z-modal` 1000, `--z-toast` 1100. The sticky header is the one conditional case: at rest it overlays the hero and is backed by `--scrim-header`, so it carries no shadow until it detaches and takes a solid ground.

Prohibited: coloured shadows and gold glow (gold is an accent, not a light source); `text-shadow` (text over a photograph is made legible by a scrim); inset shadows standing in for borders; a shadow appearing on hover as the hover affordance; any shadow on an element whose background is `--color-bg-primary`, where an ink shadow would not render at all.

---

### Motion

Three durations, two easings, three shorthands. **No other duration or curve exists**; a component that needs a fourth is over-designed.

| Token | Value | Use |
|---|---|---|
| `--duration-fast` | 150ms | colour, opacity and decoration changes on controls |
| `--duration-medium` | 250ms | transforms and reveals: menu panel, drawer, disclosure, product image scale |
| `--duration-slow` | 400ms | full-surface changes only — an overlay scrim behind a drawer or modal |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | default for everything |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | elements leaving; entrances that must feel immediate |
| `--transition-fast` / `-medium` / `-slow` | duration + `--ease-standard` | what components actually write |

**Every `transition` declaration in the theme, measured across all 21 stylesheets** — this is the whole motion surface:

| Declaration | Count |
|---|---|
| `transition: none` (inside `prefers-reduced-motion` blocks) | 8 |
| `color var(--transition-fast)` | 6 |
| `transform var(--transition-medium)` | 4 |
| `transform var(--transition-fast)` | 3 |
| `opacity var(--transition-slow)` | 2 |
| multi-property `--transition-fast` (button: background/color/border/opacity; paginator: color/border) | 2 |
| `text-decoration-color`, `opacity var(--transition-medium)`, and three two-property `--transition-fast` pairs | 5 |

There is **not one hardcoded duration** in any stylesheet. The only `ms` literals in CSS are the four `1ms !important` declarations in `base.css`'s reduced-motion block.

**Permitted:** `opacity` and `transform` for anything that moves or appears, plus — on control-sized surfaces only — `color`, `background-color`, `border-color`, `text-decoration-color`, `outline-color` and `box-shadow`.

**Never animate:** `width` / `height`, `top` / `left` / `right` / `bottom`, `margin` / `padding`, `border-width` / `text-decoration-thickness` / `outline-width`, `letter-spacing` / `font-size` / `font-weight`, `background-color` on a full-bleed section, `filter` / `backdrop-filter` on imagery, `transform: rotate()` as decoration, scroll-linked parallax or scroll-triggered reveals, or page-entry animation on headline type. No animation library, no JavaScript tweening. `will-change` is applied for the duration of an interaction and removed after.

**Assignment:**

| Interaction | Property | Duration |
|---|---|---|
| Nav link, footer link, icon colour | `color` | fast |
| Button fill and label | `background-color`, `color` | fast |
| Underline reveal | `text-decoration-color` | fast |
| Chevron disclosure | `transform: rotate()` | fast |
| Product image scale | `transform` | medium |
| Menu panel / drawer entry and exit | `transform`, `opacity` | medium |
| **Overlay scrim behind a drawer or modal** | `opacity` | **slow** |

The panel/scrim split is deliberate and was corrected in Phase 18: the mobile menu's scrim had been running at `--transition-medium` and was moved to `--transition-slow`, because Phase 2 §21.4 gives the panel medium and the scrim slow, and restricts 400ms to full-surface changes. The cart drawer already had both right.

**Reduced motion.** `design-tokens.css` collapses `--duration-fast`, `-medium` and `-slow` to 1ms and `--hover-image-scale` to 1; `base.css` sweeps `animation-duration`, `animation-iteration-count`, `transition-duration` and `scroll-behavior` with `!important`. **Those four declarations are the only `!important` in the entire theme** and they are correct there: a user preference must beat an author declaration. Components that transition also ship an explicit `transition: none` under the query. The rules that follow:

1. Every animated element is usable and complete at its end state with no transition. Nothing exists only during an animation.
2. No content is reachable only after motion.
3. **Durations are read from tokens, never hardcoded, or the reduced-motion block cannot reach them.** The one sanctioned exception is the 250ms cart debounce, which is a literal *because* a token would collapse.
4. Reduced motion is a preference, not a downgrade — colour, focus and state feedback are identical, they simply arrive instantly.

Two mechanics a new component will need. An **exit** transition must be driven by a class held until `transitionend` with a timeout fallback (`facets.js` uses `.is-closing` with a 500ms fallback, the cart drawer pattern) — flipping `visibility` in the same frame as the transform kills the animation. And when **measuring**, disable transitions first: a transitioned property reads as its start value in the same frame, and headless virtual time does not advance transform transitions at all, so an un-disabled panel reports `translateX(-100%)` forever.

---

### Hover and focus states

**Six governing rules.** These are the most frequently violated rules in the project — Phase 18 found nine ungated hover rules across five stylesheets and three missing hovers, all in already-reviewed code.

1. **Hover is never the only signal.** Every hover has a focus equivalent, and any hover that conveys state also carries it non-visually — `aria-current`, `aria-pressed`, `aria-expanded` or visible text. Pointer-only affordances are prohibited.
2. **Hover never changes layout and never changes a thickness.** Permitted: `color`, `background-color`, `border-color`, `text-decoration-color`, `opacity`, `transform`, `box-shadow`. Nothing else. Rings that need to read thicker use `box-shadow: 0 0 0 Npx`.
3. One property per element per interaction wherever the interaction allows.
4. `--transition-fast` for colour and decoration, `--transition-medium` for transform.
5. **Hover is pointer-scoped.** Every hover rule sits inside `@media (hover: hover) and (pointer: fine)` — the full query, both conditions, **never a width query**. The theme's state after Phase 18 is 29 hover rules, 29 gated, 0 ungated, held by `phase18/hovergate.py`. A width query is what makes a tablet with a mouse and a phone behave identically.
6. **No global `a:hover`.** Hover colour is `--accent-current`, which the surface class resolves.

**Focus.** One ring for the whole theme, in `base.css`:

```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}
```

`--focus-width` 2px, `--focus-offset` 2px, and `--focus-ring` is reassigned by the surface class — gold is 11.01:1 on ink and 1.55:1 on cream, so a single fixed ring colour would be invisible on one of them. **A component never chooses its ring.** `:where()` contributes zero specificity, which cuts both ways: a component can override the ring without fighting a long selector, and a stray component-level `outline` wins silently. Buttons therefore declare no `outline` at all.

`outline: none` appears exactly four times, and each is the same sanctioned pattern — remove one ring, immediately draw an equivalent on an enclosing box: the product card anchor (ring on the card), the quantity input (ring on the bordered control), the cart drawer panel and the cart page form. **Never remove a ring without substituting one.** A visually hidden native input keeps its ring on the label it controls.

The 2px offset is load-bearing on the hero CTA: gold on the cream button face is 1.55:1 and would fail SC 1.4.11 if the ring touched the button; the offset puts dark backdrop (9.24:1) on both sides.

---

### Icons

**Nine inline-SVG snippets, and that is the whole set in the theme:** `icon-account`, `icon-arrow`, `icon-cart`, `icon-chevron`, `icon-close`, `icon-menu`, `icon-minus`, `icon-plus`, `icon-search`. All in `god-squad-theme/snippets/`, all rendered with `{% render 'icon-name' %}`.

Phase 2 §18.1 named thirteen UI glyphs. **The four value glyphs — `globe`, `crown`, `community`, `diamond` — do not exist in the theme**, because the Our Story value tiles ship without icons ("a title and one line each, no icons, no dividers") and the footer's social marks are rendered as **words, not marks**, pending confirmed accounts and official brand-kit SVGs. `assets/` contains only CSS and JS; there is no image file in the theme.

**The construction contract, identical in all nine files:**

```html
<svg class="icon icon--chevron {{ class }}" xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round"
     aria-hidden="true" focusable="false">…</svg>
```

- 24×24 `viewBox`, `fill="none"`, monoline strokes, `stroke-width="1.5"`, `currentColor` throughout, `aria-hidden="true"`, `focusable="false"`.
- **Deviation from Phase 2, and the code is the truth:** §18.3 rule 2 specifies `stroke-linecap="square"` and `stroke-linejoin="miter"`. Every shipped glyph uses **round** caps and joins. The deviation belongs to the set, not to any one file, and was recorded in Phase 8 rather than half-corrected. **A new glyph is drawn round, to match the set.**
- `--icon-stroke-width: 1.5` exists as a token with **zero consumers** — the weight is a hardcoded SVG attribute. A `viewBox`-scaled SVG scales its stroke proportionally, so no size needs intervention.
- **`currentColor` is not negotiable.** An icon never carries its own colour value. That is what lets one file serve both surfaces and lets hover and focus reach the glyph at all. Gold is never hardcoded on a glyph.
- Drawn from coordinates, not traced. The prototype's rasters carry matting halos and baked colour that a trace would inherit; `icon-cart.png` carried a sliver of a sprite sheet's gold badge, so the cart count was drawn twice.

**Sizing.** `.icon` in `header.css` (layout-loaded, therefore global) sets the default: `display: block`, `width`/`height` `--icon-md` 24px, `flex: none`. A component that needs another size writes a parent-scoped rule — `.button .icon { width: var(--icon-sm) }`, `.quantity__button .icon { --icon-md }`, `.facets__summary .icon { --icon-sm }`.

| Token | Value | Consumers |
|---|---|---|
| `--icon-sm` | 16px | button/CTA arrow, filter-group chevron, cart-note chevron, announcement raster icon |
| `--icon-md` | 24px | the `.icon` default — header utilities, close, quantity steppers, product-details chevron |
| `--icon-lg` | 28px | **zero consumers** — reserved for the footer social row, which is unbuilt. Must never be used for UI: a 28px glyph beside a 24px one is exactly the optical unevenness the audit recorded. |
| `--icon-xl` | 44px | **zero consumers** — value-tile glyphs only, which do not exist |

**Do not build `.icon--sm/md/lg/xl` utilities.** Phase 18 rejected that explicitly: it would add a second sizing mechanism beside the parent-scoped one the theme actually uses. Note also that all nine snippets accept a `class` parameter that **no stylesheet defines** — recorded, unfixed; do not rely on passing one.

**The chevron rotation rule — the highest-corroborated defect of Phase 18, found seven times across four review dimensions.** `icon-chevron.svg` is drawn **pointing right** and exists once; every disclosure rotates it rather than shipping a second glyph. Therefore **every consumer must apply a base rotation**:

```css
.facets__summary .icon { transform: rotate(90deg); transition: transform var(--transition-fast); }
.facets__group[open] .facets__summary .icon { transform: rotate(-90deg); }
```

Before the fix, the filter groups and the cart note applied no base rotation, so the chevron pointed **right when closed and left when open** — a 180° flip with nothing to flip from. Measured after, with transitions disabled:

| Disclosure | Closed | Open | Sweep | Size |
|---|---|---|---|---|
| Filter group (`component-facets.css:107`) | DOWN (90°) | UP (270°) | 180° | 16px |
| Cart note (`component-cart-line.css:411`) | DOWN (90°) | UP (270°) | 180° | 16px |
| Product details (`section-main-product.css:503`) | DOWN (90°) | UP (270°) | 180° | 24px |

**The chevron legitimately ships at two sizes and must not be unified.** Phase 2 line 1428 assigns it both — `--icon-sm` 16px inline, `--icon-md` in controls. The "two sizes" finding was returned CONFIRMED by reviewers and **rejected** with that citation: a 24px glyph beside a 12px filter label would be the defect.

**State.** The 180° chevron sweep is the **only permitted transform in the icon system**. An icon never scales, rotates (otherwise) or translates on hover, and a glyph is never swapped for a second file to express a state.

| State | Change | Duration |
|---|---|---|
| Hover | `color` only → `--accent-current` | `--transition-fast` |
| Focus-visible | the surface-aware ring on the 44px box, **not** on the glyph | — |
| Active | `color` → `--color-accent-hover` on dark; no transform | `--transition-fast` |
| Disabled | `opacity` (`.45` in the shipped controls) plus the control's own disabled semantics; never colour alone | — |

**Alignment and accessibility.** An icon is `inline-flex`, `flex: none`, in a flex row with its label at `--space-2` 8px, aligned to the cap height of the adjoining tracked caps. **Ad-hoc optical nudges are prohibited** — no `margin-top: -1px`, no `position: relative; top:`. If a glyph looks misaligned, the glyph is redrawn on the 24px grid. An icon-only control centres the glyph in a `--target-min` 44px box; the box, not the glyph, is the hit area. A decorative icon beside a visible label is `aria-hidden="true"`; an icon-only control carries a text accessible name in a visually hidden span (or the component's own `aria-label`), and state is `aria-expanded`, never a swapped glyph.

**The one raster icon path in the theme, and it is an open owner decision.** `sections/announcement-bar.liquid` gives each message block an `image_picker` `icon` setting and emits it as `<img class="announcement-bar__icon" width="16" height="16" alt="" loading="lazy">` through `image_url: width: 48`. It is the only `<img>` glyph in the theme and it cannot inherit `currentColor`. Phase 18 lists it among the five decisions the owner must make.

**Standing prohibitions:** no icon font, no sprite sheet, no runtime sprite fetch, no `<img>` for a UI glyph, no `filter` or `mask` effects on glyphs, and never `asset_url` + `<img>` for a theme SVG — theme icons are inlined through `{% render %}`. `images/social-sprite.png` is explicitly **not a licensing-safe source for platform trademarks**: any platform mark must be downloaded from that platform's own brand kit as SVG and used unmodified, and no social mark ships without a confirmed account and URL.

**The set is closed to decorative additions.** A glyph enters only when a phase names the interaction it serves and no existing glyph serves it. `check`, `filter` and `external-link` are pre-approved on that basis and enter when the template that needs them is specified. There is deliberately **no bin/trash glyph** — cart removal is a text control, because the icon set has no such mark and the set is closed.

---

## Surfaces — header, navigation, hero, collections, Our Story, footer

### What exists, and where each surface is wired

| Surface | Section file | Stylesheet | Wired from | Schema `tag` | Settings | Blocks | Presets |
|---|---|---|---|---|---|---|---|
| Announcement bar | `sections/announcement-bar.liquid` | `assets/header.css` (shared) | `sections/header-group.json` | `aside` | 2 | `message` ×3 | 1 |
| Header | `sections/header.liquid` | `assets/header.css` (loaded by the layout) | `sections/header-group.json` | `div` | 8 | — | — |
| Hero | `sections/hero.liquid` | `assets/section-hero.css` (section-requested) | `templates/index.json` | `div` | 14 | — | 1 |
| Collection row | `sections/featured-collection.liquid` | `assets/section-featured-collection.css` + `component-product-card.css` (both section-requested) | `templates/index.json` ×2 | `section` | 19 | — | 2 |
| Our Story | `sections/our-story.liquid` | `assets/section-our-story.css` (section-requested) | `templates/index.json` | `section` | 14 | `value` ×6 | 1 |
| Footer | `sections/footer.liquid` | `assets/section-footer.css` (requested unwrapped) | `sections/footer-group.json` | `div` | 6 | `link_list` ×4, `text` ×2 | — |

`layout/theme.liquid` renders `{% sections 'header-group' %}` above `<main id="MainContent" tabindex="-1">` and `{% sections 'footer-group' %}` below it, with a `.skip-link` before the header group. Both group sections declare `"enabled_on": { "groups": [...] }`, so neither the header, the announcement bar nor the footer can be dropped into a page template.

The home page order shipped in `templates/index.json` is `hero → new-drop → best-sellers → our-story`. There is no standalone Verse section, no social gallery, no standalone `brand-values` section and no newsletter block; the brand-values row lives inside Our Story as blocks.

### Rules that bind every surface

- **Surface class, never a background colour.** Every band carries `.surface-dark` or `.surface-light` and inherits text, border, accent and focus colour from it. The merchant control is a `select` labelled **Colour scheme** with options *Ink* / *Cream* in all seven sections that expose it (Phase 11 brought the announcement bar's "Surface / Dark (near black) / Light (warm cream)" wording into line). Muted gold `#D8C08A` is dark-surface only; on cream `--accent-current` resolves to `--color-accent-strong` `#82672B` (4.66:1).
- **One container utility.** `.container` (`max-width: var(--container-standard)`, `padding-inline: var(--gutter)`), with `--container--wide` / `--narrow` variants, lives in `assets/component-container.css` and is used by `.header__inner`, `.hero__inner`, `.featured-collection__inner`, `.our-story__inner`, `.our-story__values` and `.footer__inner`. Built in **Phase 18**, which swept up twelve private copies of the same four declarations across eleven stylesheets after verifying all twelve byte-identical; geometry was re-measured as pixel-identical to Phase 13. `--container-standard` is overridden from `settings.container_width` in `snippets/css-variables.liquid`, so the merchant's page width reaches every surface through one property. `.header__search-form`, `.main-page__column` and `.main-search__form` are deliberately **not** swept in — they use a narrow measure with no gutter padding.
- **Gutters are the ladder, not per-section values:** `--gutter` = 24px base, 32px from 768, 48px from 1024.
- **Section rhythm is `padding-block` only**, through `--section-pad-block` `clamp(--space-7, 6vw, --space-10)` and `--section-pad-block-tight` `clamp(--space-6, 4vw, --space-8)`. The hero, the collection rows and Our Story expose `spacing_top` / `spacing_bottom` as a three-option select (None / Tight / Standard) that maps onto those tokens. No surface accepts a free pixel spacing value. The footer exposes no spacing settings at all — it is page chrome bound to a group, not a band in the rhythm.
- **Zero JavaScript except the header.** Hero, collection row, Our Story and footer ship no script, no inline handler and no `shopify:section:load` handler, because there is nothing to re-initialise. `assets/header.js` (13,963 B) is the only script any of these surfaces loads.
- **Render guards, and the stylesheet sits inside them.** An unconfigured collection row or Our Story band emits no markup *and no `stylesheet_tag`*, so it costs zero requests. The footer is the exception and always renders — the thing Phase 1 §16 recorded as missing is the `contentinfo` landmark and the copyright line, and both exist the moment the section does.
- **Editor notices, never a different layout.** Four sections carry a `request.design_mode` branch (`featured-collection`, `our-story`, `main-page`, `footer`); each is a configuration notice naming what is missing, and each renders nothing on the live storefront.
- **Heading levels derive from the heading setting.** The hero owns the page's single `<h1>`. `featured-collection` renders an `<h2>` and passes `heading_level: 3` to the card — but `2` when the merchant has cleared the heading, so the outline never skips. Our Story does the same for its value tiles (`value_level = 3`, or `2` with the heading cleared). Footer column headings are fixed `<h2>`, because nothing in the footer sits under a clearable heading.
- **First-section header clearance is a selector, not a setting.** See the header section below.

---

### Announcement bar

A non-dismissible system notice above the header, ordered first in `header-group.json`. It renders nothing when it has no blocks.

| Property | Value |
|---|---|
| Height | `--announcement-height` **40px** from 768px up; `--announcement-height-stacked` **64px** below it |
| Composition | below 768px: `flex-direction: column`, centred, `padding: var(--space-3) var(--gutter)`; from 768px: `row`, `justify-content: space-between`, `padding-block: 0` |
| Type | `--type-caption-size` / `--type-caption-weight` / `--type-caption-ls`, uppercase |
| Accent | **only the first message** takes `--accent-current`; the rest stay in body colour, so gold never becomes the bar's dominant tone |
| Divider | `border-bottom: var(--border-width) solid var(--color-border-current-subtle)` — the only visible line at the hero seam, and intentional |
| Link target | `--target-min-aa` (24px) on `.announcement-bar__item--link`; hover is pointer-scoped and adds an underline as well as colour |

Settings: `surface` (Ink / Cream, default Ink) and `alignment` (**Spread to the edges** / Centred together, default edges, added in Phase 11). The alignment control is labelled **"Alignment on desktop"** and says so in its `info`, because below 768px the bar always stacks and centres.

Blocks: `message`, limit 3, with `text`, optional `link` (`url`) and optional `icon` (`image_picker`, rendered at 16×16 with `alt: ''`). The preset and `header-group.json` both ship two messages: *"Good People. Higher Purpose."* and *"Worldwide Shipping"*.

Two things to know before you touch this:

1. **The `icon` setting is a merchant-uploaded raster** — the only glyph in the theme that is not an inline SVG inheriting `currentColor`. Phase 18 flagged restricting it to the icon set as an **open owner decision**, not a defect to fix unilaterally.
2. **"Worldwide Shipping" is an unsupported business claim.** It ships in the bar on every page while the identical claim is deliberately withheld from the Our Story values row (no shipping policy, destination list or rate table exists). Phase 18 lists resolving the contradiction as an owner decision and did not remove it.
3. The file's own header comment says the bar stacks "below `--bp-sm`". **The code is the truth: the breakpoint is `@media (min-width: 768px)`**, i.e. `--bp-md`. The comment is stale.

---

### Header

#### Architecture

`.header__inner` is a three-column grid — `auto 1fr auto`, `gap: var(--space-4)` — holding the start cluster (menu toggle), centred branding, and the end cluster (search / account / cart). `min-height` is `--header-height-mobile` **88px**, rising to `--header-height-desktop` **122px** at the single breakpoint, `@media (min-width: 1024px)`. At that breakpoint `.header__cluster--start` goes `display: none`, `.header__branding` moves to `justify-self: start`, `.header__nav` becomes `display: flex`, and the panel and its overlay both go `display: none`.

`header.css` is loaded by the **layout**, not by the section, because the header is on every page.

#### Overlay, sticky and the scrim

Two merchant switches, both checkboxes:

| Setting | Default | Behaviour |
|---|---|---|
| `overlay_first_section` | **true** | Only applies when `template.name == 'index'`. Adds `.header--overlay` and renders `<div class="header__scrim" aria-hidden="true">`. |
| `sticky` | **false** | `.header--sticky:not(.header--overlay)` is `position: sticky; top: 0`. |

- `.header--overlay` is `position: absolute; inset-inline: 0; background-color: transparent` and **sets no `top`**. An absolutely positioned box with no offset keeps its static position, so the header lands directly below the announcement bar while still lifting out of flow. `top: 0` pulled it over the announcement bar and its scrim dimmed that text.
- Overlay + sticky together: `.header--overlay.header--sticky.header--scrolled` becomes `position: fixed; top: 0`, takes `background-color: var(--color-bg-primary)` and fades the scrim to `opacity: 0` — past the first section there is no artwork for a scrim to sit on. `header.js` toggles `.header--scrolled` at `window.scrollY > 8` and only binds the scroll listener when the sticky class is present.
- **The scrim is mandatory and stronger than Phase 2 specified.** Phase 1 measured three nav links at 2.4–2.9:1 over the hero sky. Phase 2's original ramp (0.85 → 0.55 at 60% → 0) had already faded by the band the links occupy, and measured **1.09–1.11:1 at the worst pixel — worse than the prototype**. Phase 4 re-derived it: cream text over a worst-case near-white sky needs at least 0.85 alpha. The shipped token is

  ```css
  --scrim-header: linear-gradient(180deg,
      rgba(13,12,10,.93) 0%, rgba(13,12,10,.86) 66%, rgba(13,12,10,0) 100%);
  --scrim-header-overhang: 4rem;
  ```

  and `.header__scrim` is `height: calc(100% + var(--scrim-header-overhang))`, so the fade happens **below** the content band. Re-measured worst pixel in the nav band: **13.61:1** (median 17.38, p98 14.55). Both `PHASE-2-DESIGN-TOKENS.css` and `assets/design-tokens.css` were updated together. Do not soften this token; the acceptance gate is ≥4.5:1 at the worst composited pixel, per hero image.

#### First-section clearance (corrected in Phase 11)

The header publishes, **only when it actually overlays**:

```liquid
<style>
  :root { --header-overlay-offset: var(--header-height-mobile); }
  @media (min-width: 1024px) {
    :root { --header-overlay-offset: var(--header-height-desktop); }
  }
</style>
```

Phase 5 documented the hero as consuming that property directly. **It no longer does, and the code is the truth.** The property says how tall the header is, not which section it sits over, and the home page is reorderable. Each of the three body sections now defines a local clearance of `0px` and raises it only when it is first:

```css
.hero { --hero-header-clearance: 0px; }
#MainContent > .shopify-section:first-child .hero { --hero-header-clearance: var(--header-overlay-offset, 0px); }
main > .shopify-section:first-child .featured-collection { --fc-header-clearance: var(--header-overlay-offset, 0px); }
main > .shopify-section:first-child .our-story { --os-header-clearance: var(--header-overlay-offset, 0px); }
```

Measured at 1440: hero first → clearance 122px, `padding-top` 170px; hero demoted → clearance 0, `padding-top` 48px. Note the hero uses `#MainContent >` and the other two use `main >`; both resolve to the same element. Any new section that could become first needs the same treatment; a section that cannot be first does not.

#### Navigation

- **Destinations are never in the theme.** The header renders `linklists[section.settings.menu]` and iterates `link.title` / `link.url`. There is no hardcoded menu label anywhere in the theme — not HOME, SHOP, COLLECTIONS, OUR STORY or VERSE (grep-verified; `phase16/refs.py` also confirms every literal internal `href` is a route Shopify serves). The prototype's six `href="#"` anchors are not reproduced. `main-menu` is the setting's `default` handle.
- Active state comes from `link.active`: class `is-active` plus `aria-current="page"`, never hardcoded. Desktop marks it with `color: var(--accent-current)` **and** `border-bottom-color` — colour is never the only signal.
- Desktop nav: `.header__nav-list` is flex with `gap: var(--nav-gap)` (40px); links are `--type-label-size`, `--weight-medium`, `--type-label-ls`, uppercase, `min-height: var(--target-min)`.
- Logo link: `min-height: var(--target-min)`, `aria-current="page"` on the index template, and a text-wordmark fallback (`.header__wordmark`, display family, `--weight-black`) when no logo is uploaded. `.header__wordmark` is deliberately left on the display family — a logotype is not an interface heading.
- With no menu selected the desktop `<nav>` is omitted entirely and the panel shows `header.no_menu`.

#### Mobile panel

`.header__panel` is `position: fixed; inset-block: 0; inset-inline-start: 0`, `width: var(--drawer-width)` = `min(90vw, 420px)`, `transform: translateX(-100%)`, `transition: transform var(--transition-medium)` (250ms).

- **The closed panel is `display: none`** via `.header__panel[hidden]` (specificity 0,2,0, so it beats `.header__panel`'s `display: flex` regardless of source order). This was the Phase 4/6/7 carried defect: the closed panel kept its five links and close button in the tab order on every page. Measured at 375×812: reachable controls with the menu shut went **22 → 16**; at 1440 the count is 20 either way. Fixed in **Phase 9**.
- The rule does not cost the slide, because `header.js` sets `hidden = false`, forces a reflow, then adds the open class. **Keep that sequence.**
- The overlay scrim is `position: fixed; inset: 0`, `background-color: var(--color-overlay)`, `transition: opacity var(--transition-slow)` — **400ms, corrected from 250ms in Phase 18**. Phase 2 §21 gives the panel `--duration-medium` and the scrim behind a drawer or modal `--duration-slow`; the cart drawer already had this right and the two scrims open from the same header.
- The current page in the panel carries `color: var(--accent-current)` **plus** an underline (`--link-underline-offset`, `--link-underline-thickness`) — split out of the `:hover` block in **Phase 18**, which had made "current page" and "a passing cursor" literally the same state (SC 1.4.1). The `:hover` half is now inside `@media (hover: hover) and (pointer: fine)`.
- Safe area: inside `@supports (padding: max(0px))`, the panel takes `max(var(--space-5), env(safe-area-inset-top))`, `max(var(--space-8), env(safe-area-inset-bottom))` and `max(var(--gutter), env(safe-area-inset-left))`. **Caveat: `viewport-fit=cover` is not enabled, so these insets are currently 0 and the padding is inert.** Enabling it is a sequenced four-step job (meta change, `.header__inner` top inset, make the clearance account for it, re-measure the hero everywhere), not a one-liner.
- Scroll lock is `.menu-open body { overflow: hidden }` — a class on `<html>`, set by JS. The filter drawer follows this pattern; `cart.js` uses a different `position: fixed` lock. Do not mix them.
- The panel is the **only** navigation below 1024px, which is why its defects were treated as header-critical. Its **type is an open decision**: it sets links as Playfair 900 at `--type-h3-size` where Phase 2 §19.6 specifies the eyebrow triplet. No phase document defends the deviation; Phase 18 left it because correcting it re-types the primary mobile navigation.

#### `assets/header.js` contract

Disclosure contract, verified by driving the component rather than by inspection: opening sets `aria-expanded="true"`, reveals panel and overlay, moves focus into the panel, locks body scroll; Tab from the last item wraps to the first; **all three** close paths (Escape, the close button, the overlay) hide the panel, restore scroll and **return focus to the trigger** — not to whatever was focused when it opened (a real defect found in Phase 4).

Theme Editor lifecycle, fixed in Phase 11:

- Every binding the header makes is recorded in one registry and released as a unit on `shopify:section:load` and `shopify:section:unload`. Before that, the `menu-open` scroll lock survived a re-render (page locked with no menu on screen), the document-level focus trap stayed bound to the detached panel, and each load bound a fresh `matchMedia` and `scroll` listener without removing either.
- The teardown **closes the panel first**, so it cannot leave a panel open on screen with its lock already released.
- `initHeader` is **idempotent per element**, because `shopify:section:load` can fire for a node that was not replaced — binding the toggle twice made one click open the menu twice.
- A `matchMedia('(min-width: 1024px)')` listener closes the panel on resize, so focus is never stranded in a hidden panel.
- `shopify:block:select` is deliberately not implemented; no section hides or sequences block content.

#### Utility cluster

| Control | Element | Gate |
|---|---|---|
| Search | `<a href="{{ routes.search_url }}" data-search-trigger>` | `show_search` |
| Account | `<shopify-account>` | `shop.customer_accounts_enabled` **and** `show_account` |
| Cart | `<a href="{{ routes.cart_url }}" data-cart-bubble>` rendering `{% render 'cart-icon-bubble' %}` | `show_cart` |

Every control is a real control with a visually hidden label and `min-width`/`min-height: var(--target-min)` from the shared `.header__control` class; `:hover` is pointer-scoped (Phase 18). Icons are inline SVG at `--icon-md` inheriting `currentColor`; there is no raster icon in the header.

- **Search (Phase 13).** The trigger is left byte-identical as a plain link — with scripting off it navigates to a complete search page, where a `<button>` would be a control that does nothing. `header.js` intercepts the click and opens `#HeaderSearch`, a **layer**, never an expanding field: at 375px `.header__inner` has 327px of content box, the start cluster takes 44, the end cluster 148 and the two gaps 32, leaving the branding track 103px against the ~180px a usable field needs. `.header__search` is `position: absolute; inset-block-start: 100%`, with a real `role="search"` GET form carrying a labelled `q` input, `<input type="hidden" name="type" value="product">` (matching `templates/search.json`), a submit button and a close button. `aria-haspopup="dialog"`, `aria-expanded` and `aria-controls` are **applied by JS at upgrade, never printed by Liquid** — they would otherwise claim behaviour that does not exist without the script. The input is `min-height: var(--control-height)` at `--type-body-size` (16px, so iOS does not zoom on focus); the form goes from one column to `1fr auto auto` at 768px. Predictive search is **not built** (deferred by owner decision); its full contract is recorded in Phase 13 §2.
- **Account (Phase 15).** `<shopify-account>` replaced the old `<a href="{{ routes.account_url }}">` and nothing else in the file changed. `menu="{{ settings.customer_account_menu | default: 'customer-account-main-menu' }}"`. The Phase 3 account mark is supplied through the contractual `slot="signed-out-avatar"`, with a visually hidden name inside the slot as belt and braces. Do not reach inside the element with descendant selectors — only the published `--shopify-account-*` properties, `::part(signed-out-avatar)` and that slot are contractual. The 44px floor comes from `.header__control`, not from any account-specific rule; two dead rules (a `:not(:defined)` size reservation and account sizing) were measured dead and removed — do not reintroduce them.
- **Cart.** `cart.item_count` via one snippet with two consumers; **no badge at all on an empty cart** (the prototype shipped the literal `0`). `.header__cart-count` is an 18px gold pill at `top: 6px; right: 6px` — Phase 18 explicitly exempted it from badge-size unification, because growing it to 24px inside a 44px control risks clipping the glyph at 375px. `aria-controls="CartDrawer"` is emitted only when `settings.cart_type != 'page'` **and** `template.name != 'cart'` (the second condition added in Phase 16).

#### Header settings (8)

| Group | ID | Type | Default |
|---|---|---|---|
| Branding | `logo_height_desktop` | range 40–120px, step 2 | 78 |
| Branding | `logo_height_mobile` | range 32–80px, step 2 | 56 |
| Navigation | `menu` | link_list | `main-menu` |
| Utility | `show_search` | checkbox | true |
| Utility | `show_account` | checkbox | true |
| Utility | `show_cart` | checkbox | true |
| Behaviour | `sticky` | checkbox | false |
| Behaviour | `overlay_first_section` | checkbox | true |

**Phase 4 documented twelve header settings including the logo upload. That is superseded:** Phase 11 promoted the upload to the global `settings.logo` (Theme settings → Brand) so the header and footer show the same mark from one upload, and the header keeps only the two **size** controls. The migration cost was zero precisely because no logo had ever been uploaded — Shopify does not migrate a section setting to a theme setting. The heights are emitted as an inline style built with `append`:

```liquid
assign logo_style = '--logo-height-desktop: ' | append: logo_h_desktop | append: 'px; --logo-height-mobile: ' | append: logo_h_mobile | append: 'px;'
```

**Never use `#{...}` here.** Shopify Liquid does not interpolate inside a string literal; the earlier form emitted the literal text `#{logo_h_desktop}px`, which is a *valid* custom-property declaration with a garbage value, set on the `<img>` where it shadowed the good `:root` defaults — so `height: var(--logo-height-mobile)` fell back to `auto` and the logo drew at intrinsic size. It only bit once a logo existed, which is why every fixture through Phase 9 looked right.

`show_cart` ships with its cost written into its own `info` text: with it off the header has no cart control at all. The `<footer>`/`<header>` landmark reasoning is identical (`tag: div` keeps `<header>` mapping to `banner`), but note that unlike the footer the header does **not** write `role="banner"` explicitly — it relies on the element plus the `div` wrapper.

`header-group.json` ships `menu: main-menu`, the two heights, `show_search`, `show_account`, `sticky: false`, `overlay_first_section: true` and **no `show_cart` key** (so it takes the schema default `true`).

---

### Hero

The home page's LCP element. **Not a slideshow, not a video, no entrance animation, and zero JavaScript** — the cheapest hero is one the browser paints from markup and CSS.

#### DOM

```
section.hero.surface-dark
├── div.hero__media                       (absolute, inset: 0, overflow hidden)
│   ├── img.hero__image  (or <picture>, or div.hero__image--placeholder)
│   └── div.hero__scrim  aria-hidden="true"        (omitted when overlay == none)
└── div.hero__inner.container
    └── div.hero__content
        ├── p.hero__eyebrow
        ├── h1.hero__heading  →  span.hero__heading-accent (display: block)
        ├── p.hero__scripture
        ├── p.hero__description   (::before draws the 32px gold hairline)
        └── a.hero__cta.button.button--primary       (only when it has a link)
```

Fixed structural rules: exactly **one `<h1>`** with the gold accent as a `<span>` inside it, never a second heading; the eyebrow is a `<p>` (promoting it would put an `h2` above the `h1`); the scripture is a `<p>` rendered verbatim as `2 Corinthians 5:7` and the validator asserts nothing else is added; the separator is a `::before`, not an `<hr>`; the scrim is `aria-hidden`. DOM order is reading order is visual order — nothing is reordered in CSS. `{{ section.shopify_attributes }}` is emitted on the root; Phase 6 established this is a **no-op** (`shopify_attributes` exists on `block`, not `section`) and Phase 5's claim that it is a working editor hook is a documentation error. It is harmless and still in the code.

#### Image delivery

```liquid
{{ img | image_url: width: 3000 | image_tag:
     class: 'hero__image', loading: 'eager', fetchpriority: 'high', decoding: 'async',
     widths: '420, 640, 750, 960, 1100, 1280, 1440, 1680, 1920, 2200, 2600, 3000',
     sizes: '100vw', alt: img.alt }}
```

- `widths:` **and** `sizes:` are always explicit — `image_url: width:` alone emits neither a `srcset` nor a `sizes`.
- `fetchpriority` is set on the `<img>`. Shopify's `preload: true` does *not* set fetch priority; it emits a preload link, and for an image this high in the document the preload scanner finds the `<img>` anyway, so no duplicate preload is emitted.
- `alt` comes from the image object and is **never** invented. Empty merchant alt correctly announces the photograph as decorative.
- No CDN URL is hand-built anywhere; the validator checks.
- When `mobile_image` is set, a `<picture>` wraps a `(max-width: 749px)` source at 420/640/750/900/1200w with `width`/`height` from the object; the desktop fallback in that branch starts its ladder at 640w (below 750 the mobile source applies).
- **With no image chosen the section still renders its message**, over `div.hero__image--placeholder`. `templates/index.json` ships **no `image` value**, so the shipped home page renders the placeholder ground, not a photograph.
- The master is 1672×941. The CDN does not upscale, so ladder entries above 1672 resolve to the master and the browser stretches it — 1.15× at 1920, worse on a high-density display. That is a sourcing gap, not a processing one.

#### Focal point and the scrim

```css
.hero__image { object-position: var(--hero-focal-x, 50%) 30%; }
.hero--focal-left { --hero-focal-x: 20%; }  .hero--focal-centre-left { --hero-focal-x: 40%; }
.hero--focal-centre { --hero-focal-x: 50%; } .hero--focal-centre-right { --hero-focal-x: 62%; }
.hero--focal-right { --hero-focal-x: 80%; }
```

The vertical is **fixed at 30%** for every option, because that holds the faces in frame at every crop. Default `centre-left` (40%) sits between the two values that tested clean at 375×320. The setting is labelled *"Focal point on narrow screens"*: above 1024 the frame is wider than 16:9 so the whole width is visible and the setting has no visible effect. It is also **silently overridden** by any admin focal point, because `image_tag` writes `object-position` as an inline style that outranks every stylesheet rule — Phase 11 wrote that into the `info` rather than deleting a composition control.

**The scrim is not decoration.** Column luminance sampled in twenty bands peaks at 0.41 between 15% and 20% of the frame width and averages 0.29 across the left third — the brightest part of the picture is exactly where the copy sits. Rendered with the scrim removed, the worst backdrop pixel behind all four text elements carries cream at **1.00:1** at both 375 and 1440.

Below 1024px the wash is vertical and bottom-weighted (the copy sits low over the picture and the upper third holds the faces). From 1024px it turns horizontal and left-weighted, and holds its alpha across the content column rather than fading at a fixed point, because where the column ends as a fraction of the viewport moves with width:

| Breakpoint | `--hero-wash-hold` | `--hero-wash-end` |
|---|---|---|
| ≥ 1024px | 66% | 90% |
| ≥ 1280px | 54% | 82% |
| ≥ 1440px | 48% | 76% |

This protects the **column**, not today's copy: sampled across the full column with the hold pinned at 50%, 1024px fails at 2.43:1 cream / 1.57:1 gold. The 1280 and 1440 steps *relax* the wash to give the photograph back; only 1024 needs the long hold.

Measured worst single pixel per overlay setting (against the approved photograph):

| Setting | 375 eyebrow | 375 heading | 1440 eyebrow | 1440 heading | Verdict |
|---|---|---|---|---|---|
| Subtle | 4.67 | 5.71 | 7.88 | 5.16 | PASS |
| **Medium (default)** | 11.98 | 12.97 | 13.67 | 12.16 | PASS |
| Strong | 14.52 | 14.96 | 15.29 | 13.50 | PASS |
| None | 1.00 | 1.00 | 1.00 | 1.00 | **FAIL** |

`None` is retained for a future image that is already dark where the words sit, and its `info` says exactly that. `hero--overlay-none` and `hero--align-left` are styleless classes on purpose. **Centre and right text alignment swap in their own gradients and have never been contrast-measured** — the AA guarantee does not carry to them.

#### Typography

Everything is a token; nothing is a literal. Heading Playfair Display 900 via `--font-display`, everything else Jost via `--font-body`.

| Element | Token | 375 | 768 | 1440 |
|---|---|---|---|---|
| Eyebrow | `--type-eyebrow-*` | 13px / 500 / 3.9px tracking | 13px | 13px |
| Heading | `--type-display-xl-*` | 56px / lh 49.28 / ls −0.56 | 65.28px | 112px / lh 98.56 / ls −1.12 |
| Scripture | `--type-label-size` + eyebrow tracking | 12px / 3.6px | 12px | 12px |
| Supporting | `--type-label-*` + `--type-tagline-lh` | 12px / lh 20.4 / 2.64px | 12px | 12px |

The heading is fluid 56 → 112px and capped at 112px. `.hero__heading-accent` is `display: block`, so the two-line lockup is **structural**, not a wrapping outcome — measured two lines at 375/390/430/768/900/1024/1280/1366/1440/1920, three only at 320 (where "WALK BY" at 56px is ~258px against a 272px column). `text-wrap: balance` now only governs longer merchant headings.

**Gold appears exactly twice:** the heading accent and the 32px hairline above the supporting statement. **The eyebrow is cream, not gold, and that is measured** — at 13px gold is normal text needing 4.5:1, and on the Subtle overlay the worst pixel gives cream 4.67:1 against gold 3.02:1. Rescuing gold would mean a heavier wash on every setting.

Content column: `max-width: 34rem` base, `38rem` from 768, `42rem` from 1024 (measured 672px at every width from 1024 up). `.hero__description` is capped at `--measure-narrow`.

#### CTA

**In the shipped configuration the button does not render, on purpose.**

```liquid
assign has_cta = false
if btn_label != blank and btn_link != blank
  assign has_cta = true
endif
```

`button_link` has **no default** in the schema and none in `templates/index.json`, so the button stays hidden until a merchant points it somewhere — one Theme Editor field, no code change. Rendered with a link supplied it measures 259×48px at both 375 and 1440, `min-height: var(--target-min)`, padding 16px 32px, cream on ink at **17.04:1**, `--radius-sm` 2px (a rectangle, not a pill), hover swaps the face to `--color-accent`. The 2px gold focus ring keeps its 2px offset because gold on the cream face is only 1.55:1; the offset puts dark backdrop (9.24:1 worst) on both sides of the ring.

Any harness measuring the CTA must build a fixture with `button_link` set. A Phase 9 measurement was wrong precisely because the default fixture renders no button at all.

#### Height and landscape

```css
.hero--h-small  { min-height: clamp(24rem, 52svh, 34rem); }   /* 384–544px */
.hero--h-medium { min-height: clamp(32rem, 68svh, 45rem); }   /* 512–720px */
.hero--h-large  { min-height: clamp(38rem, 82svh, 55rem); }   /* 608–880px */
.hero--h-full   { min-height: calc(100svh - var(--hero-header-clearance, 0px) - var(--announcement-height)); }
@media (max-width: 767px) { .hero--h-full { … - var(--announcement-height-stacked)); } }
```

`svh`, never `vh` — on phones a dynamic toolbar makes `vh` jump and would resize the hero under the reader's thumb. Measured heights on the default *medium*: 517 / 530 / 558 / 612 / 546 / 584 / 590 / 666 px at 375 / 390 / 430 / 768 / 1024 / 1280 / 1440 / 1920.

`.hero__inner` padding is `calc(var(--hero-header-clearance, 0px) + var(--space-7)) var(--space-8)` base, becoming `+ var(--space-8) / var(--space-9)` at 1024.

**Landscape (Phase 9).** A phone turned sideways was the theme's worst viewport: the `32rem` clamp **floor** (512px) exceeded the whole viewport, so the CTA was below the fold at every landscape size. The fix is additive and bounded on **both** axes — `@media (max-height: 540px) and (max-width: 1023px)`, with no `orientation` query anywhere, because orientation says nothing about available height:

- all four height classes → `min-height: calc(100svh - var(--hero-header-clearance, 0px))`
- `.hero__inner { padding-block: var(--hero-header-clearance, 0px) var(--space-4); }` — clears the overlaid header exactly, no extra band
- `.hero__heading { font-size: clamp(1.75rem, 9svh, 3rem); }` — re-clamped against **height**, because the display scale is normally set from width, the dimension that is not scarce in landscape (34px on a 375-tall phone, 39px on a 430)
- eyebrow / scripture / description / hairline / CTA each drop one spacing step

Measured CTA lower edge, before → after: 812×375 494px (below fold) → 319px; 932×430 512 → 327; 667×375 474 → 319; 568×320 474 → 310; 812×342 → 313. Nothing is removed, reordered or hidden. These blocks also fire on a short desktop *window*, which is why the `max-width: 1023px` bound is there.

#### Hero settings (14, four groups)

| Group | ID | Type | Default |
|---|---|---|---|
| Image | `image` | image_picker | — |
| Image | `mobile_image` | image_picker | — (empty by design) |
| Image | `focal_point` | select ×5 | `centre-left` |
| Image | `overlay` | select ×4 | `medium` |
| Content | `eyebrow` | text | Streetwear With A Purpose. |
| Content | `heading` | text | Walk By |
| Content | `heading_accent` | text | Faith. |
| Content | `scripture` | text | 2 Corinthians 5:7 |
| Content | `description` | textarea | Different People. Same Purpose. |
| Call to action | `button_label` | text | Shop The Collection |
| Call to action | `button_link` | url | **none** |
| Layout | `height` | select ×4 | `medium` |
| Layout | `text_position` | select ×3 | `centre` |
| Layout | `text_alignment` | select ×3 | `left` |

One preset, **God Squad Hero**. **No blocks, deliberately** — a reorderable eyebrow / heading / accent / scripture would let a merchant put the scripture above the headline and destroy the lockup. Every select value the schema can emit has a CSS class, verified automatically. No `enabled_on` restriction: the hero is available on any template.

The `image` setting's `info` was rewritten in **Phase 18** from project vocabulary into a merchant instruction: the supplied image is AI-generated with unconfirmed rights, and must be replaced with the merchant's own photography or confirmed as cleared **before launch**. Keep that substance.

---

### Collection rows (New Drop / Best Sellers)

**One section, two presets.** `sections/best-sellers.liquid` deliberately does not exist — the two rows differ only in the chosen collection and the copy, so a second file would mean fixing every future bug twice. `templates/index.json` uses `featured-collection` twice, keyed `new-drop` (Cream, copy beside, 3 products, 3/2/2 columns, anchor `shop`) and `best-sellers` (Ink, copy above, 4 products, 4/2/2 columns).

**Shopify is the only source of product data.** There is no product, price, currency, rating, review, inventory figure, availability claim, colour value or bestseller ranking anywhere in the theme. "Best Sellers" names a collection the merchant chooses; ranking comes from that collection's *sort order* in admin. The section ships with **no collection handle at all**, so both rows render nothing on the live store until a merchant picks one. **Zero JavaScript** — the grid is server-rendered Liquid and every state (hover, focus, sold out, on sale, empty) is markup and CSS.

#### Render behaviour

| Case | Result |
|---|---|
| No collection, live store | Renders **nothing** — no markup and no stylesheet requests, because both `stylesheet_tag` calls sit inside the guard |
| No collection, Theme Editor | Copy column plus `sections.featured_collection.no_collection` |
| Collection chosen but empty, live | Renders nothing. The guard tests `has_products`, not "is a collection chosen" — a merchant can empty or unpublish a collection later |
| Collection chosen but empty, editor | `sections.featured_collection.empty_collection` |
| Fewer products than requested | Renders what exists. No placeholders, ever |
| View all | `collection.url` unless `view_all_url` overrides it (a `url` setting cannot default to a dynamic value). Renders only with both a label and a destination |

#### Layout and grid

`--split-30-70` (`0.9fr 2.4fr`) arrives at 1024px with `gap: var(--grid-gap-large)` for the *copy beside* layout; the *copy above* layout is one column throughout. A 0.9fr rail inside a 704px tablet row is ~190px and cannot hold the display heading, which is why the rail waits for 1024.

```css
.product-grid {
  --product-cols: 2;
  --product-track-ideal: calc((100% - (var(--product-cols) - 1) * var(--product-grid-gap)) / var(--product-cols));
  grid-template-columns: repeat(auto-fill,
    minmax(max(var(--product-track-floor, var(--product-col-min)), var(--product-track-ideal)), 1fr));
  gap: var(--product-grid-gap);
}
@media (max-width: 767px) {
  .product-grid { --product-grid-gap: var(--space-4); row-gap: var(--space-6); --product-track-floor: 8rem; }
}
```

**The merchant's column count is a ceiling, not a command.** `auto-fill` asks how many tracks of at least `max(floor, ideal)` fit; where the viewport cannot carry the requested count the grid **drops a column instead of squeezing one**. The catalogue floor is `--product-col-min` `17rem` (272px, Phase 2 §9.3, derived to retire the prototype's 230px three-up squeeze between 901 and 1100). Below 768 the floor relaxes to `8rem` (128px) so two columns are possible on a phone, and the column gap drops to `--space-4` (16px) while the **row** gap stays `--space-6` (32px) — vertical space is not the scarce dimension on a phone. There is no column count a merchant can choose that produces a broken grid, and no horizontal overflow at any width including 320.

Column counts are emitted as **section-scoped custom properties** inside `{% style %}`, keyed `#shopify-section-{{ section.id }} .product-grid`, at the three tiers — never as an inline `style` on the grid, which would outrank every media query and pin the mobile count everywhere. That scoping is also what lets two instances on one page carry different counts.

Measured ladder (New Drop asks 3 with copy beside; Best Sellers asks 4 with copy above): 320 → 1×272 both; 375 → 2×147; 768 → 2×336; 1024 → 2×300 / 3×288; 1280 → 2×396 / **4×272**; 1440 → **3×297** / 4×312. Two consequences, both surfaced in editor help text rather than hidden: the copy-beside layout reaches three columns at **1440, not 1024** (the rail takes about a third of the row), and a three-product collection leaves one tile alone on a row below 1440 — a consequence of the count, not the grid.

#### The `sizes` derivation

The **section** computes `sizes` and passes it to the card, because the section is what knows the grid. It is exact, not conservative, and it emits **six clauses**: a fixed-pixel clause above the container cap, then two desktop clauses, a tablet clause, and two mobile clauses. Two rules govern it:

1. **A clause may not claim a width before the layout that produces it applies.** `threshold_d` is floored at 1024 (`if threshold_d < 1024 … = 1024`), or a three-column full-bleed row would compute 976 and declare a desktop slot while the grid was still painting the tablet count.
2. **A clause may not divide by more columns than actually fit.** Above the container cap the row stops growing, so `fits_d` is recomputed from the floor and `cols_capped` is the smaller of requested and fitting — with four columns at a 1200px container, dividing by four declares 253px for a track that paints 346px.

Other arithmetic that must be kept in step: `gap_m = 16` feeds `need_m`, `threshold_m`, `gaps_m` and `gaps_m_low`; the copy-column layout scales the needed row by `1000/727` (integer division, `+1`, because Liquid truncates and truncating downward would put the threshold below the width that fits); `capped_track` rounds **up** by `plus: 1` for the same reason. Verified against the rendered grid: zero clauses under-declare, largest over-declaration 9px (3%).

**`featured-collection` is deliberately NOT consolidated into `snippets/grid-sizes.liquid`** (the shared derivation used by `main-collection` and `main-search`), because its 1000/727 scaling makes the derivation genuinely different. The code says so at the site. A future change to the shared rules must be applied here too.

#### Settings (19, six groups)

| Group | ID | Type | Default |
|---|---|---|---|
| Collection | `collection` | collection | — |
| Collection | `products_to_show` | range 2–12 | 3 |
| Content | `eyebrow` | text | New Drop / |
| Content | `heading` | text | The Faithful |
| Content | `description` | textarea | Premium Essentials for a Higher Purpose. |
| View all | `show_view_all` | checkbox | true |
| View all | `view_all_label` | text | View All Products |
| View all | `view_all_url` | url | blank (falls back to `collection.url`) |
| Layout | `surface` | select Cream / Ink | Cream |
| Layout | `layout` | select `with-copy-column` / `full-width` | `with-copy-column` |
| Grid | `columns_desktop` | range 2–4 | 3 |
| Grid | `columns_tablet` | range 2–3 | 2 |
| Grid | `columns_mobile` | range 1–2 | 2 |
| Product card | `show_price` | checkbox | true |
| Product card | `show_compare_at_price` | checkbox | true |
| Product card | `show_swatches` | checkbox | true |
| Spacing | `spacing_top` | select none/tight/standard | standard |
| Spacing | `spacing_bottom` | select none/tight/standard | standard |
| Advanced | `anchor_id` | text | blank (New Drop preset sets `shop`) |

Three deliberate departures from Phase 2 §29.3, all recorded rather than quietly taken:

1. **`image_ratio` is NOT a section setting.** The ratio is `product_image_ratio` at **theme** level (Square 1:1 / Portrait 4:5, default Square), mapped onto `--product-aspect` in the layout. Two rows of one shop with different image shapes is a bug, not a choice, and a validator check asserts no section-level `image_ratio` exists.
2. **`show_vendor` is not offered** — no God Squad surface uses a vendor name while the catalogue is single-brand.
3. **All three column counts ARE offered** (Phase 2 wanted tablet and mobile derived), because the grid mechanism removes the risk mechanically. The two `spacing_*` selects pick from system values, never free pixels.

`section.shopify_attributes` is deliberately **absent** from this section — it exists on `block` only. The section is safe to duplicate: every generated id is scoped by `section.id` and nothing derives from a hardcoded section id.

Phase 18 landed on this surface: the shared `.container`, the shared paginator (`snippets/pagination.liquid` + `assets/component-pagination.css`, merged from the two per-template paginators that had drifted), the collection description's rich-text link hover, and the empty-state title moved off the page `<h1>`'s type onto the interface-heading row.

---

### Our Story + brand purpose

One section carrying the whole band: eyebrow, hard-broken display heading, body, optional CTA, a 70%-width photograph with a mandatory scrim, a caption rail, a value-tile row from blocks, and an editor notice. **Zero JavaScript** — the band is complete and legible with JS disabled, animation disabled and CSS gradients unsupported; the scrim only ever softens an edge, it never carries meaning.

**The copy is the approved copy, not new copy.** Every default is the prototype's own wording, and every one is a Theme Editor field, so an alternative direction is one edit away rather than imposed.

| Field | Default | Provenance |
|---|---|---|
| Eyebrow | `Our Story` | prototype line 129 |
| Heading | `Real People.` ⏎ `Bigger Purpose.` | prototype line 130 |
| Body | "God Squad is a Philippine streetwear brand built on faith, creativity, and community. We create pieces that inspire a generation to live different — with purpose." | prototype line 131 |
| Caption | `Faith` ⏎ `Lives` ⏎ `Different` ⏎ `Here.` | prototype line 136 |
| Button label | `Discover Our Story` | new label, replacing the prototype CTA that repeated the eyebrow verbatim |
| Button link | blank | no page exists; the button does not render |
| Value tiles | Faith Driven / More Than Clothing · Community / People With Purpose · Premium Quality / Crafted To Inspire | prototype lines 180–183 |

Nothing invents a founder, date, place, partnership, statistic, testimonial or theological claim; no star ratings, customer counts, "trusted by", press mentions or endorsements. **The prototype's fourth tile, "Worldwide / Shipping Available", is deliberately not shipped** — it is the one value that is a checkable commercial promise with no shipping policy, destination list or rate table behind it. A merchant who can stand behind it adds a fourth block in one edit. The block's `info` states that every line is brand messaging, never a measurable claim.

#### Composition

The band is the **three-track rail**, not a two-column block. At 1024px:

```css
grid-template-columns: minmax(26rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr);   /* image right */
grid-template-columns: minmax(9rem, 0.4fr) minmax(0, 1.6fr) minmax(26rem, 0.9fr);   /* image left  */
```

with the caption track growing to `11rem` at 1440. Inner tracks measured at 1440: **416 / 688 / 176**.

**The 26rem copy-track floor is measured, not chosen.** With the real face and tracking the approved heading's two lines set at 253/325 (32px), 285/366 (36px) and 316/**406** (40px); the scale caps at 40px from a 1000px viewport, so a 397px track re-broke the second line even with the break in the markup. A longer merchant heading still wraps — the floor guarantees the approved lockup sets as drawn, not that any text will.

Three tiers:

| | < 768 | 768–1023 | ≥ 1024 |
|---|---|---|---|
| Composition | stacked | stacked | three-track rail |
| Media | full width, `--hero-aspect-mobile` (4/5) | full width, `3 / 2` | `width: 70%`, offset, `min-height: var(--band-min-height-story)` (520px), `aspect-ratio: auto` |
| Scrim | bottom fade | bottom fade | horizontal, toward the copy |
| Body measure | `--measure-body` (68ch) | `--measure-body` | `--measure-narrow` (40ch) |
| Caption rail | not rendered | not rendered | rendered, with its own backing |
| Value tiles | 1 column | 2 | 3 at 1024, up to 4 above |

`4/5` below 768 is the same portrait the hero uses on a phone. `3/2` from 768 because `4/5` there is a 960px-tall band that pushes every word below the fold (measured), and 3:2 is the canonical asset's own ratio. Phase 2 defines no editorial landscape ratio token, so the `3/2` is written out in this stylesheet and recorded as a token gap.

Measured at ten widths (320–1920): no horizontal overflow, heading two lines at 375–1920 and three at 320, media 375×469 at 375 up to 1344×874 at 1920, copy column 24–351 at 375 and 48–464 at 1024–1440.

Value row: `repeat(auto-fit, minmax(min(17rem, 100%), 1fr))`. The floor is 17rem rather than 14 because the row is capped at `--container-standard`: at 1440 a 14rem floor fits five tracks and the schema's sixth permitted block then sits alone on a second row. Measured: 3 blocks span the full width at every tier; 6 blocks give 3+3 at 1024 and 4+2 from 1280. Three tiles wrap 2+1 at 768–1023, accepted deliberately.

#### Image

- `image_picker`, never a hardcoded path; the validator asserts no image path appears anywhere in the markup.
- `image_tag` with `widths: '480, 640, 900, 1200, 1500, 1800, 2100, 2400'`, `image_url: width: 2400`, `loading: 'lazy'`, `decoding: 'async'`, `alt: img.alt`.
- **`sizes` is `(min-width: 1024px) 70vw, 100vw`** and that is exact, not an approximation: `.our-story__media` is 70% of a band that is 100% wide **with no max-width** — only the copy container and the values row are capped at `--container-standard`. Measured error 0px at 375/768/1024/1280/1440/1920. An earlier revision capped the slot at 70% of `settings.container_width` and declared 1008px for a slot rendering 1344px. **Do not cap the media at the container width.**
- Optional `mobile_image` via `<picture><source media="(max-width: 1023px)">` at 480–2048w (2048 reaches past DPR 3 at 1023 CSS px).
- **No theme-side focal control, deliberately.** `image_tag` writes `style="object-position: X% Y%"` directly onto the `<img>` whenever the image carries an admin focal point, and an inline style outranks every stylesheet rule — a theme select would have moved nothing on exactly the images a merchant had bothered to position. Shopify admin's focal point is the single source of truth; the stylesheet's default for an image with no focal point is `object-position: center 33%` (the prototype's `center top` discarded about a fifth of the picture's height).
- The **media block is inside the image guard**, not around it: the wrapper carries a ratio and an ink fill, so emitting it without an image ships a tall empty rectangle above the copy — which is the state `templates/index.json` ships, since it sets no `image`.
- **The scrim is mandatory and not a merchant choice.** Phase 2 §29.4's `overlay_style` select is deliberately not exposed. Its direction derives from `image_side` so it always fades toward the copy, and its base colour follows the surface (`--os-scrim-rgb`) so the photograph dissolves into the band it is actually in. It is `aria-hidden="true"` and `pointer-events: none`, behind the content layer.
- The caption rail's backing is anchored to the **rail**, not to the photograph — a horizontal gradient starting fully transparent 10rem to its left, masked vertically so it fades above and below rather than cutting hard lines across the picture. A stop in the photograph's own gradient cannot work, because the rail's position across the picture moves with the viewport (73.2% at 1024, 78.6% at 1280, 77.8% at 1440, 65.5% at 1920) — left over the open photograph the rail's cream 12px measured 1.69–2.14:1. `--scrim-story-horizontal` exists in the token file and **cannot be used** here: its stops are a fixed ink while this band must also fade into cream.

#### Settings (14, five groups) and blocks

| Group | ID | Type | Default |
|---|---|---|---|
| Content | `eyebrow` | text | Our Story |
| Content | `heading` | **textarea** | `Real People.\nBigger Purpose.` |
| Content | `body` | richtext | the approved statement |
| Image | `image` | image_picker | — |
| Image | `mobile_image` | image_picker | — |
| Image | `image_side` | select Right / Left | Right |
| Call to action | `button_label` | text | Discover Our Story |
| Call to action | `button_url` | url | blank |
| Caption rail | `show_caption` | checkbox | true |
| Caption rail | `caption` | textarea | `Faith\nLives\nDifferent\nHere.` |
| Layout | `surface` | select Ink / Cream | **Ink** |
| Layout | `spacing_top` | select | standard |
| Layout | `spacing_bottom` | select | standard |
| Layout | `anchor_id` | text | `story` in the preset |

`heading` is a `textarea` rendered with `| newline_to_br` — each typed line becomes a rendered line, so **the break is the merchant's, never the browser's**. Left to wrap, the approved heading came out on three lines at every width measured.

Blocks: `value`, limit 6, fields `title` and `body`. `{{ block.shopify_attributes }}` is on every `<li>`. One preset, "Our Story", shipping three value blocks.

**Switching to Cream changes three things automatically:** the scrim base flips to cream; the eyebrow takes `--color-accent-strong` `#82672B` (4.66:1) because muted gold on cream is 1.55:1; and the CTA switches from `button--accent` to `button--primary`, because Phase 2 gives the accent variant no light-surface rule at all and it would render with no fill and no visible border.

**Gold is spent once per band** — the eyebrow is the band's single accent mark. The value titles inherit the band's text colour (17.04:1), not gold; an earlier revision set them in gold, making four marks against Phase 2 §26.5's budget of two. Weight, tracking and caps carry the hierarchy.

48 pixel-sampled contrast measurements across both surfaces at 1024/1280/1440/1920, zero failures. Worst figures: Ink body `#BDB6A8` 9.56:1, Ink caption rail 8.01:1; Cream eyebrow `#82672B` 4.66:1, Cream body `#5F5A50` 5.80:1, Cream caption rail 7.32:1.

The caption rail is `display: none` below 1024, so it leaves the accessibility tree as well as the layout — it is not read out on a phone. `show_caption` turns it off at every width.

Phase 18 on this band: no visual change beyond the container consolidation (geometry verified identical), the body's rich-text link gained a pointer-scoped `:hover` to `var(--accent-current)`, and the `body` setting's `info` was de-jargoned. Approved value copy unchanged; no marks, claims or statistics added.

---

### Footer

`sections/footer.liquid` in `footer-group.json`, on every page. **Zero JavaScript.** It is the only content surface with **no render guard** — the thing Phase 1 §16 records as missing is the `contentinfo` landmark and the copyright line, and both exist the moment the section does, so the stylesheet link sits at the top of the file unwrapped.

#### The landmark, and why `tag` is `div`

```liquid
<footer class="{{ classes }}" role="contentinfo">
```

`<footer>` maps to `contentinfo` only while it is not a descendant of `article`, `aside`, `main`, `nav` or `section`. Setting the schema `tag` to `"section"` would wrap this in sectioning content and silently demote the site's only `contentinfo` to a generic group. **The `tag` must stay `div`**, and the role is written out as well so the file states its own contract.

#### Every destination comes from Shopify

- **Menu columns:** `link_list` blocks, limit 4. A column renders only when `menu_object != blank and menu_object.links.size > 0` — the test is the rendered outcome, not the setting, because a merchant can pick a menu and later empty it. With no `heading`, the column falls back to **the menu's own title from Navigation** rather than inventing a word, so its `nav` landmark is never unlabelled (`aria-labelledby="FooterMenu-{{ block.id }}"`, `<h2 class="footer__heading">` — a fixed level, unlike the Phase 6/7 derived levels). In the editor, an empty column shows `sections.footer.no_menu`.
- **`footer-group.json` ships with no menu bound.** Phase 10 bound it to the `footer` handle Shopify auto-creates, and with no heading the column printed Shopify's admin vocabulary — "Footer menu" — as customer-facing copy on every page, duplicating the policy row beneath it. Corrected in Phase 11.
- **Policies:** iterated from `shop.policies`, per policy, with Shopify's own titles and URLs in the store's language. An unpublished policy simply does not appear. The row exists only if at least one policy is published (`has_policies`, found by breaking on the first non-blank).
- **Copyright:** `footer.copyright` = `© {{ year }} {{ name }}` with `year = 'now' | date: '%Y'` and `name = shop.name`. **Never a hardcoded year, and there is no `copyright_text` field** — a typed year is stale the moment it is typed. There is no `show_copyright` either: a `contentinfo` landmark without a copyright line is the defect being fixed.
- **Social:** read from `settings.social_facebook_url` and `settings.social_instagram_url` — **theme** settings, because a brand's Instagram address is one store-wide fact. Both ship blank, each link is emitted only when its URL is set, and the whole row is suppressed when both are empty (with `sections.footer.no_social` in the editor). **No profile was invented, and there is no TikTok setting** because no TikTok profile was supplied. No `target="_blank"` — opening a new window is a change of context the link gives no warning of.
- **The social marks are words, not icons, and that is deliberate.** `icon-facebook.liquid` / `icon-instagram.liquid` have never been drawn, and the prototype's 130×130 RGBA rasters have colour baked into their pixels so they cannot follow `--accent-current`, a hover or a light surface. A word is a real accessible name at every surface and needs no asset. When the marks are drawn they take `--icon-lg` 28px, the size Phase 2 §18.2 reserves for this row, and each must come from that platform's official brand kit as SVG, used unmodified — never traced, redrawn or taken from `images/social-sprite.png`.
- **Logo:** `show_logo` (default **false**) renders `settings.logo` only when the merchant asks for it **and** a logo exists — a checkbox that produces an empty gap is worse than no checkbox. Sized by `--logo-height-footer` (56px), a token that had been waiting since Phase 2. The image is `alt: ''` (decorative — the adjacent tagline names the brand) **plus a `<span class="visually-hidden">{{ shop.name }}</span>` inside the anchor**, added in Phase 16: `alt=""` on the only content of an anchor leaves the link with no accessible name at all (SC 2.4.4 / 4.1.2), and the tagline is a sibling, not a child, so it never named the link.

#### Layout

- `.footer` carries `border-block-start: var(--border-width) solid var(--color-border-current-subtle)` so it still reads as its own band when the section above it is Ink too; `.footer__bottom` carries the same hairline.
- `.footer__blocks`: one column base, `repeat(2, minmax(0, 1fr))` from 768, and `repeat(auto-fit, minmax(11rem, 1fr))` with `grid-auto-columns: minmax(0, 1fr)` from 1024 — **auto-fit wraps to rows instead of thinning**, which is what fixed Phase 10's six-column ceiling. `.footer__column { min-width: 0 }` stops a long menu item pushing its track past `minmax(0, 1fr)`.
- Targets: `.footer__link` takes `min-height: var(--target-min-aa)` (24px); `.footer__social-link` takes the full `var(--target-min)` 44×44 box.
- `.footer__link.is-active` adds an **underline** as well as colour, under the comment that the state is not carried by colour alone — this is the pattern the mobile menu panel was corrected to match in Phase 18.
- Phase 18 fixed two ungated hover rules here (`.footer__link`, `.footer__text a`) and rewrote four merchant-facing schema strings to drop project vocabulary while keeping every instruction — including that the theme supplies no contact details and guesses nothing.

#### Settings (6) and blocks

| Group | ID | Type | Default |
|---|---|---|---|
| Brand band | `show_logo` | checkbox | false |
| Brand band | `tagline` | text | Different People. Same Purpose. |
| Brand band | `strapline` | text | A Brighter Tomorrow |
| Store policies | `show_policies` | checkbox | true |
| Social | `show_social` | checkbox | true |
| Layout | `surface` | select Ink / Cream | Ink |

Both default strings are prototype lines 156 and 164, checked against the source before acceptance. BRAND-08 is open — the project holds four competing taglines with no canonical set — so nothing here adds a fifth.

Blocks: `link_list` (heading, menu) limit 4; `text` (heading, richtext body) limit 2, with contact details as its intended use. `{{ block.shopify_attributes }}` on every wrapper, including the editor-only notice variants.

**No presets** — the footer belongs to a group, not to a template. **No spacing or anchor settings** — it is page chrome, taking the page padding directly. Deliberately absent: a newsletter block (Phase 1 FOOT-03 is still a business decision, and Phase 2 reserves a second group section for it), payment icons, and a country/currency selector — the last two need no business information (`shop.enabled_payment_types` and a localization form would do it) but are new surfaces rather than the missing footer.

**Recorded, not changed (Phase 18):** the footer stacks two link type systems — policy/menu links at 14px sentence case directly above social links at 12px uppercase tracked — and four controls reveal an underline by two incompatible mechanisms, three of them with `text-decoration`, which cannot be transitioned. Both are type/motion changes to a live surface; **the link-type decision is an open owner call.**

---

### Open on these surfaces

Business information, not code:

- **Navigation destinations.** The menu cannot be populated until Shop, Collections, Our Story and Verse have real targets — and until it is decided what Verse is. The theme is correct without them.
- **Hero CTA destination.** One Theme Editor field closes Phase 1 HERO-01; the home page currently has no forward path out of the hero.
- **Hero imagery.** No image is set in `templates/index.json`; the supplied master is AI-generated with unverified licensing, is 1672px wide (upscales above that), and there is no mobile portrait master — the `mobile_image` picker and the `<picture>` source are wired and empty, because inventing a crop is not art-directing one.
- **Our Story master.** `images/our-story.webp` is 535×348 and upscales ~1.9× in this slot; a master of at least 2000px with **no text baked into the pixels** is required (the prototype's slot showed a hero crop with "A PURPOSE", "K BY" and "TH." baked in). The band ships with no image and renders as copy on flat ink.
- **An Our Story page**, for `button_url`. Until it exists the CTA does not render; `href="#"` is forbidden.
- **Collections.** Both rows are invisible on the live store until a merchant creates and selects collections (and sets the Best Sellers collection's sort order to "Best selling" — the theme never decides what sells).
- **Vector logo and favicon.** The only wordmark is a 500×500 PNG whose transparent padding makes the visible mark render at roughly half its intended size. Once a vector master exists, upload it as the theme logo and inline it from a snippet where it must inherit colour — `image_url` does not transform SVG.
- **Social channels.** Two blank URL settings; the row does not render. Nothing is displayed that the business has not confirmed.
- **The "Worldwide Shipping" claim**, shipped in the announcement bar while withheld from the Our Story values.

Owner decisions Phase 18 escalated rather than took: the **mobile menu panel's type**, the **footer's two link type systems**, and whether the **announcement bar icon** should be restricted to the inline SVG icon set.

---

## Surfaces — product, cart, checkout, search and filtering, accounts, 404 and pages

Everything in this part of the manual lives under `C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme`. Paths below are relative to that root.

### Surface inventory

Shopify serves an error page for any storefront route whose template is missing, so the full route set has to exist even where the design is minimal. Seven JSON templates ship. Every `main-*` section is locked to its own template by `enabled_on.templates`, so a merchant cannot drop the product page into a page template.

| Route | Template | Section | `enabled_on` | Section-loaded assets |
|---|---|---|---|---|
| `/products/*` | `templates/product.json` | `sections/main-product.liquid` | `product` | `section-main-product.css`, `product.js` |
| `/collections/*` | `templates/collection.json` | `sections/main-collection.liquid` | `collection` | `component-product-card.css`, `section-main-collection.css`, plus `component-facets.css` + `facets.js` **only** when filters exist |
| `/search` | `templates/search.json` | `sections/main-search.liquid` | `search` | `component-product-card.css`, `section-main-search.css` |
| `/cart` | `templates/cart.json` | `sections/main-cart.liquid` | `cart` | `section-main-cart.css` |
| `/pages/*` | `templates/page.json` | `sections/main-page.liquid` | `page` | `section-main-page.css` |
| 404 | `templates/404.json` | `sections/main-404.liquid` | `404` | `section-main-404.css` |
| every page except `/cart` | — | `sections/cart-drawer.liquid`, rendered by `layout/theme.liquid` | *(no `enabled_on`; not in any template)* | `section-cart-drawer.css` |
| — | — | `sections/cart-icon-bubble.liquid` | *(no schema at all)* | none |

`layout/theme.liquid` loads `component-button.css`, `component-quantity.css` and `component-cart-line.css` because the drawer is rendered there on nearly every page; linking them from the sections as well produced two `<link>` tags for one URL. `cart.js` also loads from the layout. `component-container.css` and `component-pagination.css` (both new in Phase 18) are shared components; pagination is rendered by `snippets/pagination.liquid` from both the collection and the search template.

Still missing against Shopify's Theme Store list: `article`, `blog`, `list-collections`, `page.contact`, `password`, `gift_card`. Each is an error page for anyone who reaches its URL. `templates/customers/` is absent and **must stay absent** — see Accounts.

---

### The product page

#### Composition and file tree

```
templates/product.json
  └── sections/main-product.liquid                    the whole page
        ├── snippets/product-media-gallery.liquid
        ├── snippets/product-variant-picker.liquid
        ├── snippets/quantity-selector.liquid          shared with both carts
        └── {% form 'product', product %}              Shopify's own form
```

`--split-60-40` (1.6fr 0.9fr, renders 64/36) from `--bp-lg` up: media left, buying right. Below that it is one column in DOM order — media, title, price, variants, quantity, add to cart, buy now, description — so nothing is moved visually away from the order a screen reader reads. The buying column carries a **22rem (352px) floor**, which is what keeps the variant chips and the quantity control from wrapping at 1024.

The buying column is `<div class="main-product__info" tabindex="0" role="group" aria-label>`. The `tabindex` is load-bearing, not decoration: the stylesheet turns the column into a scroll container when it is sticky and taller than the viewport, and Safari (and Chrome before 127) do not put scroll containers in the tab order.

#### Settings — 10, in four groups, no blocks

`main-product` is a fixed composition of settings, not a block list. A product page's title, price, picker and add-to-cart have a correct order.

| Group | id | Type | Default |
|---|---|---|---|
| Media | `media_layout` | select `stacked` / `carousel` | `stacked` |
| Buying | `show_quantity` | checkbox | `true` |
| Buying | `show_accelerated_checkout` | checkbox | `true` |
| Details | `description_layout` | select `open` / `collapsible` | `open` |
| Details | `show_vendor` | checkbox | `false` |
| Details | `show_product_type` | checkbox | `false` |
| Details | `show_sku` | checkbox | `false` |
| Details | `low_stock_threshold` | range 0–20 | `3` |
| Layout | `sticky_info` | checkbox | `true` |
| Layout | `surface` | select `light` (Cream) / `dark` (Ink) | `light` |

Image shape is **not** here: `--product-aspect` comes from the theme-level `product_image_ratio` (`square` 1/1 default, `portrait` 4/5), resolved in `snippets/css-variables.liquid`. One ratio for the whole catalogue.

The cost of settings-not-blocks: an app that ships a product-page block cannot place itself here. The fix is a `blocks` array with a `{% when '@app' %}` arm, and it is small.

#### The product form contract

Four things are easy to get wrong and are all written into `sections/main-product.liquid`:

1. **The theme supplies `<input type="hidden" name="id">` itself.** `{% form 'product' %}` emits `form_type`, `utf8` and `product-id`. `product-id` is not `id` and adds nothing to a cart.
2. **Passing `class:` replaces the tag's own default**, so `shopify-product-form` is repeated inside the string rather than added to it.
3. **The variant input carries `disabled` whenever the variant cannot be bought**, so no submission route — Enter in the quantity field, a script, browser autofill — can post a sold-out variant.
4. **There is no `novalidate`.** Dawn has it; here it switched off exactly the browser constraint validation the quantity control depends on. With scripting off, `min="1"` is the only thing between a typed `-3` and a POST to `/cart/add`.

The variant picker is rendered **inside** the form. Outside it, its radios were unassociated with the form entirely.

Buyability is read from the variant, never from whether one resolved:

```liquid
assign can_buy = false
if current_variant != blank and current_variant.available
  assign can_buy = true
endif
```

`product.selected_or_first_available_variant` returns the **first** variant when everything is sold out, so a nil check always passes and would report a sold-out product as buyable.

Three independent guards stop a wrong variant reaching `/cart/add`: the `disabled` hidden input, `addButton.disabled`, and a capture-phase `submit` listener in `assets/product.js` that calls `preventDefault()` + `stopImmediatePropagation()` if the variant input is disabled or empty.

#### Media

`product.media`, never `product.images` — `images` cannot represent a video or 3D model, and only `featured_media` can carry a variant's. `snippets/product-media-gallery.liquid` dispatches on `media.media_type` with an `{% else %}` arm so a type Shopify adds later still draws.

| `media_type` | Rendered by | Notes |
|---|---|---|
| `image` | `image_url` → `image_tag` | nine srcset candidates, `360…1800` |
| `video` | `video_tag`, `controls: true`, `preload: 'metadata'` | **autoplay off** |
| `external_video` | `external_video_url: autoplay: false` → `external_video_tag` | order matters and fails silently if reversed |
| `model` | the preview image only | `model_viewer_tag` is inert until the theme calls `Shopify.loadFeatures({name:'model-viewer-ui'})`; AR needs a second call. Neither is shipped |

Loading discipline — corrected in Phase 16: **`fetchpriority: 'high'` follows `is_active`, not `forloop.first`.** `is_active` is the variant's `featured_media` when it has one and falls back to the first medium. `forloop.first` keeps `loading: 'eager'` because the stacked desktop layout renders every slide in document order. Everything else is `lazy`. Exactly one `fetchpriority` per page.

No `style:` parameter is ever passed to `image_tag`: it writes the image's focal point as an inline style, which outranks every stylesheet rule. Cropping uses `object-fit` only, and the focal point is set in Shopify admin (*Content → Files → Edit*). And because `image_tag` emits `width`/`height` **attributes**, any CSS rule for such an image must constrain **both** axes — setting only `width` left a cart thumbnail 948px tall and made `aspect-ratio` inert.

`media_layout` governs the **desktop composition only**. Below `--bp-lg` the gallery is always a carousel, whatever the setting says. `assets/product.js` cancels the thumbnail rail's anchor jump (so no history entry per photograph) and scrolls smoothly; with the script blocked the anchor still brings its slide into view.

The gallery `sizes` is computed in Liquid across five regions and was measured against the rendered box at sixteen widths (0 under-declarations):

```
(min-width: {{container}}px) {{media_cap}}px,
(min-width: 1106px) calc((100vw - 128px) * 0.64),
(min-width: 1024px) calc(100vw - 480px),
(min-width: 768px)  calc(100vw - 64px),
calc(100vw - 48px)
```

`media_cap = (container - 128) * 0.64 + 1`. The `+1` is deliberate: integer division floors, and under-declaring is the direction that costs image quality. `1106` is where the 352px buying-column floor stops binding — `128 + 352 / 0.36`.

#### Variants

Built from `product.options_with_values`, never `product.variants` (which truncates silently at 250 and costs render time on every request). Each `product_option_value` carries its own `selected` and `available`, so the server renders the correct initial state with no JavaScript.

Radios, not a `<select>`. The input is `visually-hidden`; the **focus ring is drawn on the label**.

| State | Treatment |
|---|---|
| Rest | 1px `--color-border-current-interactive` (3.02:1 on ink, 3.13:1 on cream) |
| Selected | `--border-width-strong` 2px in `currentColor`, plus the checked radio. Padding gives back the pixel the border takes, so choosing does not nudge the row |
| Unavailable | struck through, muted, **still in the DOM and still focusable**, with the state in the accessible name via `[data-unavailable-note]` |
| Focus | ring on the label |

The chip boundary must **not** use `--color-border-current` (≈1.3:1, fails SC 1.4.11's 3:1). The interactive border token is the measured one. The same substitution applies to `.button--secondary` and to the quantity control's box.

Swatches render only from Shopify's own swatch data (`value.swatch.color` / `.swatch.image`, emitted as `style="--swatch-fill: …"` / `--swatch-image`). A value with no swatch in a mixed option falls back to its name so it stays choosable. No colour is ever guessed from an image or a name.

`available` on a `product_option_value` means *some* variant carrying that value is available — not that the combination the customer has built is. The combination is resolved against the embedded variant table by `assets/product.js`. **Server-rendered state is correct on load and refined on interaction, never the other way round.**

#### The embedded variant table

`<script type="application/json" data-variant-data>` carries a hand-written field list, never `{{ product.variants | json }}` — the whole-object dump publishes `inventory_quantity` and `inventory_management` into the page source, which is a stock-level leak, and is several times larger. Nine keys per variant:

`id`, `available`, `options`, `price` (money-formatted by Liquid), `compare_at_price` (null unless it exceeds price), `media_id`, `sku`, `low_stock` (boolean), `quantity_rule` (`{min, max, increment}` or null).

*Phase 8 documented six fields; `low_stock` and its companions arrived in Phase 12. The code is the list above.*

Money strings are formatted by Liquid against the store's own format, because that is the one thing the browser genuinely cannot do correctly.

#### What a variant change updates

`assets/product.js`, with **no network request**: the hidden `name="id"` input and its `disabled` state; the price and whether compare-at shows; the add button's label and `disabled`; the SKU value and whether its row is `hidden`; the low-stock line; the option legends' chosen-value text; which values are marked unavailable and their accessible names; the active gallery slide when the variant carries `featured_media`; the URL via `history.replaceState` (**never `pushState`** — trying three sizes must not put three entries between the customer and the page they came from); and the quantity control's `min`, `max` and `step`, because `quantity_rule` is carried **per variant**.

Three states on the button, not two:

| Resolution | Label source |
|---|---|
| variant exists and `available` | `data-label-idle` |
| variant exists, not available | `data-label-sold-out` |
| **no variant at all** | `data-label-unavailable` (`products.variants.unavailable`) |

A null variant is a combination that was never manufactured. Saying "Sold out" there tells the customer something false — that it existed and ran out, so it might come back.

When nothing resolves, **the price is left as it was**. An empty price where a number used to be reads as a broken page.

`updateQuantityRule` re-dispatches a bubbling `change` event on the quantity input rather than reimplementing the stepper's disabled logic — `cart.js` owns that function.

#### With scripting off, the picker switches nothing

The radios render, they can be chosen, and nothing about the page changes; the value submitted is the hidden `name="id"` input the server rendered. A customer without scripting can buy that variant and no other. This is where Shopify itself stands (the platform dropped the no-JS variant-switching requirement and Dawn behaves identically), but it is a real cost: a control that looks operable and is not. The honest fix is a small no-JS `<select name="id">` mirror, and it needs a real store to test the duplicate-`id` submit behaviour.

#### Quantity selector — `snippets/quantity-selector.liquid`

Three consumers: the product form, the drawer line, the cart page line. Parameters: `id` (required), `name` (default `quantity`; cart lines pass `updates[]`), `value`, `min` (default 1), `max`, `step`, `label`, `describe`, `form`, `line_key`, `compact`, `disabled`.

| Rule | Implementation |
|---|---|
| Minimum 1 | `min` on the input; the minus takes `aria-disabled="true"` at the floor rather than clamping silently |
| Buttons ≥ 44px | `min-width`/`min-height: var(--target-min)`. SC 2.5.8's spacing exception cannot rescue two flush steppers |
| Value 16px, centred, untracked | `--type-body-size`, `letter-spacing: 0`. 16px also stops iOS zooming on focus |
| Ceiling is Shopify's | `max`/`step` from `variant.quantity_rule`, simply absent when the merchant set none |
| No stock figure, ever | `variant.inventory_quantity` is public on the storefront and is never rendered |
| Accessible names per product | "Increase quantity for Heavyweight Hoodie", not `+` |
| 250ms debounce | a **literal** in `cart.js`, deliberately *not* `--duration-medium`: a motion token collapses to 1ms under `prefers-reduced-motion`, removing the debounce for exactly the people most likely to be stepping from a keyboard |
| Cart-line floor is 1, not 0 | stepping to nothing would make the minus destructive at its last press; removal is the explicit control beside it |

**Without `cart.js` there are no steppers.** *Correcting Phase 8's wording:* the two `type="button"` buttons **are** in the markup unconditionally; `assets/component-quantity.css` gives `.quantity__button { display: none }` and only `.cart-js .quantity__button { display: flex }`. The same class gates removal of the native spinners (`appearance: textfield`, `::-webkit-*-spin-button`), so with no script the browser's own spinner is left in place and the field is still steppable. `.cart-js` is set on `<html>` by `cart.js`'s own `init()` — never by the layout's inline `no-js`/`js` swap, which runs whether or not `cart.js` arrives.

When `show_quantity` is off the section still submits a quantity, through a hidden `<input name="quantity" value="{{ qty_min }}" data-quantity-input>`. Without that branch, turning a cosmetic setting off submitted no quantity, Shopify defaulted to 1, and any variant with `quantity_rule.min > 1` was refused with a 422 the customer could not act on. **A presentation setting must never remove required form data.**

#### Low stock — product page only

New in Phase 12. The comparison happens **in Liquid, server-side**; only a boolean reaches the page. Render-time guard, all on one line because inside a `{% liquid %}` block every line is its own statement:

```liquid
if low_stock_at > 0 and current_variant.inventory_management == 'shopify' and current_variant.inventory_policy == 'deny' and current_variant.available and current_variant.inventory_quantity > 0 and current_variant.inventory_quantity <= low_stock_at
```

Two guards matter beyond the threshold: `inventory_management == 'shopify'` (an untracked variant reports 0 forever) and `inventory_policy == 'deny'` (a continue-selling variant is never low, it is unlimited). The threshold is a merchant setting at **3**, set in both the schema default and `templates/product.json`; `0` disables the line. `aria-live` is deliberately absent — the variant change is already announced, and a second live region would make one action speak twice.

There is no permanent "In stock" line: the enabled Add to bag button already says it. And the line is product-page only — repeated down a grid, "Low stock" stops being information and becomes urgency marketing.

#### SKU, type, structured data

The SKU row renders if **any** variant carries a SKU (`for v in product.variants … break`), and hides itself with `hidden` when the selected variant has none. Gated on the render-time variant's SKU, the hook `[data-variant-sku]` was never in the DOM when the first variant had none, so the SKU could never appear for any later variant.

`{{ product | structured_data }}` is emitted **once**, theme-wide, by Shopify's own filter. Never hand-built: that is what keeps price, currency, availability URL and per-variant identifier derived from real data, and what makes a fabricated rating impossible — the filter emits none and no review data exists. Canonical lives in `layout/theme.liquid` only. Exactly one `<h1>` per template, and on a product page it is `product.title`.

**Not verified:** whether `page_description` falls back to the product body on a real store. A description must **not** be synthesised.

#### No zoom, no size guide, no reviews

Deliberately absent: reviews, ratings, star rows, stock counters, invented materials or care instructions, country of origin, shipping estimates, recommendations, wishlist, and any zoom layer. A zoom system would add a modal, a focus trap and a second media request per product. Size guide, materials and care are blocked on approved copy (ECOM-04) and inventing them is forbidden.

---

### Add to cart

`assets/cart.js` intercepts `submit` on `form[action*="/cart/add"]` — which matches `routes.cart_add_url` under a locale prefix too.

| Step | What happens |
|---|---|
| 1 | Submit intercepted. A second submit while one is in flight returns early, keyed on `aria-busy` |
| 2 | `showFormError(form, null)` and `showFormSuccess(form, null)` clear any previous result |
| 3 | The button takes `aria-busy="true"` and its label becomes `data-label-busy`. It is **never `disabled`** |
| 4 | `new FormData(form)` plus `sections` and `sections_url` appended |
| 5 | `seq = ++requestSeq`, shared with quantity changes |
| 6 | On response: `setButtonBusy(button, false)`; `applySections(result.sections)` if `seq === requestSeq` |
| 7 | If the drawer auto-opens and exists → `Drawer.open(button)`, nothing announced. Otherwise `showFormSuccess(...)`, and `announce(...)` **only** if the form has no success line |

**`aria-busy` only, never `disabled`.** Disabling the element that holds focus blurs it, so every add dropped a keyboard user to `<body>`; and restoring it afterwards asserted `disabled = false` with no knowledge of why it might be disabled — switch to a sold-out size mid-flight and the response re-enabled a button for a variant that cannot be bought. `setButtonBusy` only restores the idle label `if (label && !button.disabled)`.

| State | Produced by |
|---|---|
| Default | `data-label-idle` |
| Adding | `aria-busy="true"` + `data-label-busy` |
| Added | the drawer opens, **or** `[data-product-success]` |
| Sold out | `disabled` + `data-label-sold-out`, from `variant.available` |
| Unavailable | `data-label-unavailable` |
| Error | Shopify's own `description` in `[data-product-error]` |

The add button uses the `disabled` attribute rather than `aria-disabled`, departing from the design system's §10.3 on purpose: the reason is the control's own label ("Sold out"), so nothing is put out of reach — and a submit with `aria-disabled` still submits on Enter, which with scripting off would post an unavailable variant.

#### The visible confirmation (Phase 14)

`[data-product-success]` is a `role="status"` line under the form carrying the sentence and a plain link to `routes.cart_url`. **`role="status"`, not `alert`** — the customer got what they asked for, so it waits its turn. That also makes it self-announcing, which is why `cart.js` writes to the live region only when the form has no such line:

```js
if (!showFormSuccess(form, stringFor('added', null))) { announce(stringFor('added', null)); }
```

When the drawer opens, **the drawer is the confirmation** and nothing is announced: announcing and moving focus at the same moment makes a screen reader talk over itself. No confetti, no full-screen animation.

#### Errors

| Failure | What the customer sees |
|---|---|
| 422 from `/cart/add` | Shopify's own `description`, in the form's error line |
| 422 from `/cart/change` or `/cart/update` | Shopify's `description`, on the cart surface's error line |
| Transport failure | the theme's own sentence from the locale file (`data-error-network`) |
| Anything else | `data-error-generic` |
| A line Shopify cannot honour | `item.error_message`, the platform's own text |

**No raw API error is ever shown** — no status code, no exception, no stack. **A 422 from `/cart/add` can mean the cart changed anyway**: when the requested quantity exceeds stock, Shopify adds the maximum it can *and* returns the error, so the returned sections are applied either way — showing the old cart would be a lie. If a failure returns no sections and was not a transport failure, `refreshSections()` re-reads the cart rather than guessing. The button is restored on every path; there is no code path that leaves it saying "Adding…".

---

### The Ajax cart contract

`assets/cart.js` — 39,750 bytes on disk, **12,008 B gzipped measured now**, roughly half of it comment. No framework, no dependency, no polyfill. One global: `window.GodSquad.cart = {open, close, refresh}`. `window.Shopify` is never written to. (The last recorded figure was 12,073 B gz; either way it is over Shopify's `AssetSizeJavaScript` 10,000 B threshold. The answer is a minification step at deploy, not surgery on a 24 KB-total codebase.)

#### Four invariants

1. **Shopify is the cart.** No client-side cart object, no `localStorage`, `sessionStorage`, `indexedDB` or `document.cookie` anywhere in any theme script. After a refresh the cart is whatever the server says, because that is the only place it has ever been.
2. **Every control works without JavaScript.** The product form posts natively to `/cart/add`; the cart form posts to `routes.cart_url` with `updates[]`; removal is `item.url_to_remove`; the header cart control is a link to `/cart`. `cart.js` only cancels those defaults.
3. **One file, no dependencies.**
4. **Mutations carry their own re-render.** Sections are requested in the same round trip as the mutation, so every surface is the server's view of the cart after the change — never a number the theme calculated.

#### URLs

```js
function root() {
  var r = window.Shopify && window.Shopify.routes && window.Shopify.routes.root;
  return r || '/';
}
function url(path) { return root() + path; }
```

Never a literal `/cart/add.js`. A store with Markets or a second language serves the cart under a locale prefix, and a hardcoded path silently 404s there.

#### Two request shapes, one failure test

| Endpoint | Body | Headers |
|---|---|---|
| `cart/add.js` | `FormData` from the form | `Accept: application/json` **only** — setting `Content-Type` overwrites the multipart boundary the browser generated and the request arrives unparseable |
| `cart/change.js` | `{id, quantity, sections, sections_url}` | `Content-Type: application/json`, `Accept: application/json` |
| `cart/update.js` | `{note}` — **no sections requested** | as above |

```js
var failed = !result.response.ok || typeof data.description === 'string';
```

A response counts as failed when `description` is present **or** the status is not ok. `data.status` is sometimes the integer `422` and sometimes the string `bad_request`, so it is not a reliable test on its own. `post()` always resolves to `{ok, data, message, sections, network?}` — a rejected promise would make every call site handle transport and application errors differently.

#### Line identity

Lines are identified by their **line item key**, never by index and never by variant id. Two lines can share a variant id — the same variant with different properties, or split by an automatic discount — and an index shifts the moment anything is removed. The key is **not stable across mutations**, so it is re-read from freshly rendered markup every time rather than cached.

#### Render targets, collected at init

```js
var SECTIONS = ['cart-icon-bubble'];
function collectSections() { … }
```

| Target | When it is requested |
|---|---|
| `cart-icon-bubble` | always — a standalone section file whose id is its filename |
| `cart-drawer` | whenever `[data-cart-drawer]` is in the document, i.e. every template except `/cart`, and not at all when `settings.cart_type == 'page'` |
| the cart page's own section id | only on `/cart`, read from `[data-cart-page-section]` |

At most three sections per request; Shopify's limit is five. `collectSections()` re-runs on `shopify:section:load`.

Both static targets have **stable ids**: a section placed in a JSON template gets a generated id such as `sections--1234__header`, which changes. `sections/cart-icon-bubble.liquid` carries **no schema** — a standalone render target cannot receive settings, and a preset would wrongly expose an internal render target in the merchant's Add section list.

`sections_url` is always `window.location.pathname`. It **must begin with a slash** or the whole request returns 400, and Shopify's docs warn that such a 400 does not mean the mutation was rolled back.

A section that comes back `null` is skipped. The response always carries the `<div id="shopify-section-…">` wrapper, so `sectionInner()` takes the wrapper's **inside** — replacing `outerHTML` would nest a second wrapper on every update.

#### Delegation and lifecycle

Seven delegated listeners on `document`, bound once in `init()`: `submit`, `click` ×3 (opener, quantity, remove), `change` ×2 (quantity, note), `input` (note). Markup the Section Rendering API swaps in needs no re-binding, which is also what stops the file leaking listeners. Measured: five section re-renders add **zero** document listeners.

`shopify:section:load` → `collectSections()`, and `Drawer.init()` if the loaded node contains the drawer. `shopify:section:unload` → `Drawer.reset()` and `Drawer.el = null`. `Drawer.init()` itself begins with `this.reset()`, and `reset()` returns immediately unless the drawer is open, so it is idempotent.

#### Error scoping (Phase 14 D2)

```js
var CART_ERROR_BOXES = '[data-cart-drawer] [data-cart-error], [data-cart-page] [data-cart-error]';
```

`showCartError()` used to select `[data-cart-error]` **document-wide**, and a quick-add product card carried one — so a quantity Shopify refused in the drawer would have written "You can't add more…" into the error line of every product tile on the page behind it. Per-form failures are `showFormError()`'s job, which looks for `[data-product-error], [data-cart-error]` **inside the form**.

#### Quantity race handling

| Behaviour | Result |
|---|---|
| The number on screen | moves on every press, with no wait |
| Five rapid presses | **one** request, carrying the fifth value |
| Two lines changed quickly | one request each, each with its own line key |
| A superseded response | its markup is discarded; **its busy state and its error are not** |
| Remove during the debounce | the queued change is cancelled |

`changeLine()` clears `pending[key]` on entry (Phase 14 D3 — removal called `changeLine` directly and a step made inside the 250ms window fired *after* the removal and re-added the line). Only the markup swap is gated on `seq === requestSeq`: returning early on the sequence check left a line dimmed and inert forever and swallowed the reason a change was refused.

---

### The cart drawer

`sections/cart-drawer.liquid` + `assets/section-cart-drawer.css`. Rendered once from `layout/theme.liquid`:

```liquid
{%- if settings.cart_type != 'page' -%}
  {%- unless template.name == 'cart' -%}
    {% section 'cart-drawer' %}
  {%- endunless -%}
{%- endif -%}
```

Rendering it on `/cart` too put two views of one cart on one screen — which can disagree after an update — and gave every cart line a duplicate DOM id, so `<label for>` resolved to the first match and the drawer's quantity labels silently pointed at the page's inputs. `cart.js` tolerates an absent drawer everywhere: `onOpenerClick` returns early when `Drawer.el` is null, `Drawer.open()` guards on `this.el`, and the add path gates auto-open on `Drawer.el` explicitly.

#### It is a real cart form first and a drawer second

Everything inside is Shopify's documented no-JavaScript cart: a form posting to `routes.cart_url`, one `updates[]` field per line in cart order, a submit named `checkout`, and `item.url_to_remove` links. With scripting disabled the drawer is simply not openable and the header's cart control is what it has always been — a link to the cart page.

#### Structure

```
<div class="cart-drawer surface-dark" id="CartDrawer" role="dialog" aria-modal="true"
     aria-labelledby="CartDrawerTitle" data-cart-drawer data-auto-open="…" hidden>
  <div class="cart-drawer__overlay" data-cart-overlay aria-hidden="true">   pointer-only; Escape is the keyboard equivalent
  <div class="cart-drawer__panel">
    <div class="cart-drawer__header">
      <h2 id="CartDrawerTitle" tabindex="-1">        focus lands here — OUTSIDE the swapped region
      <button data-cart-close>
    <div role="status" aria-live="polite" data-cart-drawer-status>   the drawer's own announcements
    <p data-cart-error role="alert" hidden>          the visible failure line
    <div data-cart-drawer-inner>                    replaced after every cart change
      <form action="{{ routes.cart_url }}" method="post" id="CartDrawerForm" data-cart-form>
        <div class="cart-drawer__scroller">  … lines …  cart-note …
        <div class="cart-drawer__footer">    totals · update · checkout · view cart · continue shopping
```

**The heading, the live region and the error line sit outside `[data-cart-drawer-inner]` on purpose.** A focused element inside a replaced subtree is destroyed and the browser drops focus to `<body>`; a live region recreated together with its text announces nothing at all.

#### Open / close lifecycle

| Event | Where focus goes |
|---|---|
| Drawer opens | `#CartDrawerTitle` (`tabindex="-1"`) — not the close button, which announces "Close, button" and says nothing about what just happened |
| Escape, overlay click, close button, Continue shopping | back to `this.opener`, checked with `document.contains()`, else `[data-cart-bubble]` — focusing a detached node silently puts focus on `<body>` |
| A cart line is updated | the equivalent control in the freshly rendered line, preferring the line's own quantity input, excluding `[aria-hidden="true"]` |
| A cart line is removed | that surface's own heading — the drawer's `h2` or the cart page's `h1` |
| Add to cart, start to finish | stays on the add button |

`open()` sets `hidden = false`, forces a frame with `void this.el.offsetWidth` so the slide has a start state, then adds `.cart-drawer-open` to `<html>`. `close()` removes the class, un-inerts, removes the keydown listener, then hides the node on `transitionend` with a 500ms fallback — and immediately under `prefers-reduced-motion`.

#### `inert`, not `aria-hidden`

`aria-hidden` leaves content focusable while removing it from the accessibility tree, stranding a screen reader on an element it cannot describe. `inert` handles focus, pointer input, find-in-page and the accessibility tree in one attribute. Where `inert` is unavailable (`SUPPORTS_INERT` is false) a minimal Tab-cycling trap takes over, and **never alongside it**.

**The drawer's own section wrapper is excluded by `contains()`, not by identity.** Shopify wraps every section in `<div id="shopify-section-…">`, so the drawer is never itself a child of `<body>`. Comparing identity marked the wrapper inert, which made the drawer inert with it — and focus could not be moved into a drawer that had just been opened. Elements carrying `data-cart-no-inert` (the layout's live region and strings host) are also skipped, as are `SCRIPT`, `STYLE` and `LINK`.

#### Two live regions, because `aria-modal` hides one

`aria-modal="true"` instructs assistive technology to treat everything **outside** the dialog as absent. The layout's `#CartStatus` is a sibling of the drawer, not a descendant, so every status produced while the drawer was open was announced to nobody.

| When | Region |
|---|---|
| Drawer open | `[data-cart-drawer-status]`, inside the panel and outside the swapped node |
| Otherwise | `#CartStatus` in `layout/theme.liquid`, carrying `data-cart-no-inert` |

`announce()` routes between them. Both are empty at page load and text is injected inside a `setTimeout` — a region created together with its content announces nothing.

Every sentence comes from the locale file, through `data-` attributes on `[data-cart-strings]` in the layout (`data-added`, `data-updated`, `data-removed`, `data-note-saved`, `data-quantity-announce`, `data-error-generic`, `data-error-network`). `cart.js` writes no user-facing English of its own. Counted strings use a `[count]` token that Liquid places, because where the number falls in a sentence is a translation decision.

#### Scroll lock

`body.style.position = 'fixed'` plus `top: -scrollY`, restored with `window.scrollTo(0, scrollY)` on close. `overflow: hidden` does not lock iOS Safari, and `position: fixed` without saving the offset is the "close the cart and you are back at the top of the page" bug — both halves are needed. `scrollbar-gutter: stable` is set permanently on `html` in `section-cart-drawer.css` so locking does not move the layout sideways.

**This lock does not compose.** Two owners each recording one scroll position fight over it. The header's menu panel and the filter drawer both lock with a class instead (`.menu-open body { overflow: hidden }`, `.facets-open body { overflow: hidden }`), and classes compose. Any new dismissable surface follows the class pattern, not the cart's.

#### Totals — three lines, not one

| Line | Source |
|---|---|
| Subtotal | `cart.items_subtotal_price` — after line-level discounts, before cart-level |
| Each cart-level discount | `cart.cart_level_discount_applications` → `discount.total_allocated_amount` |
| Estimated total | `cart.total_price` |

Showing `items_subtotal_price` alone as "the price" silently overstates what the customer will pay the moment a cart-level discount is active.

The note below them is **derived, not asserted**: it branches on `cart.taxes_included`. Printing "Taxes and shipping are calculated at checkout" unconditionally is a claim about this merchant's tax configuration nobody supplied, and wrong for any tax-inclusive market — which the Philippines is. There is **no shipping claim, no delivery estimate and no free-shipping threshold** anywhere in the theme.

`snippets/cart-totals.liquid` and `snippets/cart-empty-state.liquid` are shared by both cart surfaces. They were two byte-identical copies under renamed classes until a review pointed out that a correction to one would never reach the other.

#### The update submit comes first

A browser submits a form with its **first** submit button when Enter is pressed in a field. If checkout came first, pressing Enter after typing a quantity would take the customer to checkout instead of applying the change. In the drawer the update control is `visually-hidden visually-hidden--until-focus`; in both surfaces it is removed once the cart script runs, keyed on `.cart-js` — the class **the cart script sets on itself**, never the layout's `js` class.

#### The order note (Phase 14)

`snippets/cart-note.liquid`, two consumers, **off by default on both**. Whether this store wants order notes is business information nobody supplied.

- **One field named `note`.** Shopify's cart carries a single free-text note. A second field, a dropdown of reasons or a gift-message variant would all be inventing store policy.
- **Labelled "Order note"**, never "Special instructions". Both strings are in the locale file.
- **A native `<details>`**, rendered `open` when `cart.note != blank`. A permanently open textarea costs ~120px, which in a 420px drawer is taken from the cart lines. Safe because form controls inside a **closed** `<details>` are still submitted.
- **`{{ cart.note | escape }}`** — `escape`, not `escape_once`. Liquid does not escape output, the note is customer-supplied and also settable through `/cart/update.js`, and a `</textarea>` inside it closes the element early. Verified by rendering a payload.
- **A real `<label>`**, visually hidden because the summary above carries the same words.

**It lives in the drawer's scroller, not its footer.** The footer is chrome — the totals and the actions, the things that must stay put. The note is content, and content in the chrome makes the chrome grow with it. Measured with a note written at 812×283: footer 451px tall in a 283px viewport, scroller 0px against 474px of cart lines. The customer could read their note and reach Checkout, and could not see a single thing they were buying.

Saving rules:
- **On `change`, not `input`** — one request when the field is left with a different value, not one per keystroke.
- **Through `/cart/update.js` with `{note: value}` and no sections requested**, because nothing on the page displays the note's value. It is the cheapest mutation the cart makes.
- **An unsaved note is carried across a section swap** (`captureNote()` / `noteDirty`), and the dirty flag is cleared only if `field.value === value` after the response, because the customer may have typed on while it was in flight.
- Focus returns to the field rather than the heading — the note is the one control in the swapped node that does not belong to a line, so the key-based focus path could not find it and threw the customer to the heading mid-sentence.

There is **no length limit**: Shopify's own limit applies at the API, and inventing one would reject text Shopify would have accepted.

#### Continue shopping (Phase 14)

Different controls on the two surfaces, deliberately. **Drawer: a `<button>` that closes the drawer**, reusing `[data-cart-close]` so it is the drawer's one close path rather than a second one — the drawer is a layer over the page the customer was shopping, and closing it returns them there. **Cart page: a link** to `section.settings.empty_link | default: routes.root_url` — arriving on `/cart` is a navigation and there is nothing to return to. Both are quiet text controls under the two buttons, **not a third button**: this is the way *out* of a decision and giving it a button's weight would compete with Checkout.

#### Removal

A text control — "Remove" — not a glyph. The icon set is closed to decorative additions and contains no bin mark, and in a 420px drawer a word is less ambiguous than an icon at 44px. `href` is Shopify's own `item.url_to_remove`; `cart.js` cancels the navigation and does the same over the Ajax API, falling back to `link.href` if no `data-line-key` is present. Accessible name: "Remove Heavyweight Hoodie from your cart". **There is no undo.**

#### Empty state

`snippets/cart-empty-state.liquid`. **No checkout control, no quantity control, no cart line, no note field, no invented product.** The checkout CTA is not disabled, it is **absent**, which is the strongest form of "not active".

Default destination is **`routes.root_url`** — the home page — not `routes.all_products_collection_url`. *The snippet's own comment still says "no `templates/collection.json` exists yet"; that is stale — Phase 10 added it. The default stays the home page anyway, as Phase 14 §8 records, because it is the page certain to render, and the merchant can point `empty_link` anywhere.* **Phase 8's admin checklist item 9 says the empty-cart destination "Defaults to the store's all-products collection" — that is wrong; the code defaults to the home page.**

#### Why it is not a `<dialog>`

`showModal()` would give inertness, the top layer, Escape and focus return for free. The trade was made against three costs:

1. The panel is promoted out of its stacking and containing-block context and `::backdrop` is a separate pseudo-element, so scrim and panel cannot animate as one composited group; the UA's centring and max-size defaults must all be overridden.
2. The exit animation needs `@starting-style` plus `transition: display … allow-discrete, overlay … allow-discrete` — omit the `overlay` line and the drawer snaps away instead of sliding out.
3. Any stray `method="dialog"` or `formmethod="dialog"` on a control inside it silently closes the dialog and discards the POST. In a cart, that is a discarded `/cart/change`.

Worth revisiting when `closedby="any"` is Baseline.

#### Drawer geometry

`--drawer-width: min(90vw, 420px)` — 420px at 1280/1440/1920, and 338/351/387px at 375/390/430, leaving the remaining scrim tappable to dismiss. Height is `height: 100vh; height: 100dvh` (the `vh` line as the fallback). The footer reserves `max(var(--space-5), env(safe-area-inset-bottom))`; the panel publishes `--drawer-pad-inline-end` for a trailing-edge notch. Note that `env(safe-area-inset-*)` resolves to 0 under `viewport-fit=auto`, which is what the theme ships, so the reservations are currently inert — enabling `viewport-fit=cover` is a sequenced four-step job, not a one-line change.

Below **540px of height and 1023px of width** the drawer stops pinning its footer and becomes one scrolling column (`.cart-drawer__panel { overflow-y: auto }`, `.cart-drawer__scroller { flex: 0 0 auto; overflow: visible }`). The structural fault is that the scroller is `flex: 1; min-height: 0` — the only thing that can give — while the footer is intrinsically sized. Whenever header + footer exceed the panel, the scroller goes to zero and the footer overflows. Checkout is no longer permanently on screen but it is always **reachable**, which on a screen that cannot show both is the correct trade. Bounded on width as well, so a short desktop window is untouched.

---

### The cart page

`sections/main-cart.liquid` + `assets/section-main-cart.css`, driven by `templates/cart.json`. It exists because with JavaScript off the product form posts natively to `/cart/add` and Shopify redirects to `/cart` — and the drawer's own View cart link goes there too.

It is a render target for its own Ajax. `[data-cart-page-inner]` is what `cart.js` replaces; `data-cart-page-section="{{ section.id }}"` is how the script learns the id. Without it the script would intercept both controls and have nowhere to put the answer — and after a removal the page's **positional** `updates[]` inputs would no longer line up with the server's lines, so pressing Checkout would have applied each surviving quantity to the wrong product. The `h1` (`#CartPageTitle`) and the error line sit outside the swapped node.

**Layout.** One column below 1024px — lines, then totals under them. From 1024px:

```css
.main-cart__form { display: grid; grid-template-columns: minmax(0, 1fr) 24rem;
                   gap: var(--space-8); align-items: start; }
```

`24rem` fixed, not a fraction: the summary holds a fixed set of short lines and a button. At the 1440 container the single column ran cart lines to 1344px, so a 120px thumbnail sat beside a title with ~1000px of empty rule between it and its own price. The summary is `position: sticky` at `top: var(--header-offset-desktop)` with `max-height: calc(100dvh - var(--header-offset-desktop) - var(--space-6))` and its own scroll, so a long note or a stack of discounts can never hide Checkout under the column's own bottom edge (SC 2.4.11).

The first cart line's thumbnail is `eager` (`eager: forloop.first`); every other is lazy.

**Phase 14 D1:** the rule hiding the no-JS Update button used to live in `assets/section-cart-drawer.css` — a stylesheet the cart page never loads, because the layout does not render the drawer there. Measured before the fix: `display: inline-flex`. `.cart-js .main-cart__update { display: none }` now lives in `section-main-cart.css`. **A selector is not a rule until something on the page it names has read the file it is in.**

`.surface-light` selectors in the cart stylesheets are unreachable and must not be added: both cart surfaces hardcode `surface-dark` and neither schema exposes a surface setting.

#### The cart line — `snippets/cart-line-item.liquid`

Parameters: `item`, `index`, `form_id`, `scope` (namespaces every id, because two surfaces can render the same line and an id built from the key alone collides across them), `compact`, `eager`.

- **`updates[]` is positional.** Exactly one input per line, in `cart.items` order, with no gaps and **no conditionals**. A quantity field wrapped in a condition that can be false would shift every later line's quantity onto the wrong product.
- **`item.key`, not `item.id`.** In a cart context `item.id` is the variant id.
- **Field names that look right and are not.** `line_item.product_title` and `line_item.variant_title` **do not exist in Liquid** — they exist only in the Ajax Cart API's JSON. The name comes from `item.product.title`; the variant line from `item.options_with_values`, guarded by `has_only_default_variant` so a product with no options does not print "Title: Default Title".
- **Line properties are escaped on both halves** (Phase 17): `{{ property.first | escape }}: {{ property.last | escape }}`. A property is supplied by whoever posted to `/cart/add.js`, so both name and value are untrusted input. Without the filter a value of `</p><img src=x onerror=…>` produced a live element with an event handler — verified by rendering it. Properties whose name begins with `_` are private and not shown; empty values are skipped.
- Discounts come only from `item.line_level_discount_allocations`; the theme creates no discount logic.
- `item.error_message` is rendered in a `role="alert"` when Shopify sets it.
- The thumbnail is inside a `tabindex="-1" aria-hidden="true"` link with `alt: ''`, because the title link beside it already names the product. `image_url: width: 300`, `widths: '76, 96, 120, 152, 192, 240, 300'`, `sizes` = `76px` in the drawer and `(min-width: 768px) 120px, 96px` on the cart page. No original-resolution photography is ever requested.
- Sale state carries visually-hidden "Sale price" / "Regular price" labels around `item.final_line_price` and a struck `item.original_line_price`.
- `.cart-line__title` measures ~230×24 and stays flagged UNDER-44. It meets SC 2.5.8's 24px AA minimum; the 76px thumbnail beside it links to the same product (the equivalent-control exception). Growing it to 44px would add 20px per line to a drawer already fighting for 100px of scroller in landscape. **This is a deliberate call, not a regression.**

#### Cart count

`snippets/cart-icon-bubble.liquid`, rendered in two places: inline by `sections/header.liquid`, and alone by `sections/cart-icon-bubble.liquid` as the Section Rendering target. Dawn keeps two parallel copies and they drift; one snippet cannot.

```liquid
{%- if cart.item_count > 0 -%}
  <span class="header__cart-count" data-cart-count aria-hidden="true">{{ cart.item_count }}</span>
  <span class="visually-hidden" data-cart-count-text>{{ 'cart.item_count' | t: count: cart.item_count }}</span>
{%- endif -%}
```

An empty cart shows **no badge at all** — the prototype painted a literal `0` whether or not anything was in a cart that did not exist. The control's own name is still "Cart", which is the whole message when it is empty. The badge is replaced from the server's render, never incremented in JavaScript.

The header cart control keeps `href="{{ routes.cart_url }}"` and carries `aria-controls="CartDrawer"` only when `settings.cart_type != 'page' and template.name != 'cart'` — never on `/cart`, where the drawer does not exist. A modified click (cmd, ctrl, shift, alt, non-primary button) is left alone, so it still opens the cart page in a new tab. Known trade-off: a screen reader announces "Cart, 3 items, link" and the customer gets a drawer. Focus moves to a heading that says "Your cart", so they are told where they are; it is what keeps the no-JavaScript fallback a real link.

---

### Checkout

**Shopify's, entirely.**

- A `<button type="submit" name="checkout">` inside the cart form, on both surfaces. It applies any pending quantity edit *and then* goes to checkout, in one action. A plain link to `/checkout` would silently discard an edit the customer had just made.
- The form posts to `{{ routes.cart_url }}`.
- **No checkout URL is constructed anywhere**, and no `checkout_url` is referenced.
- **No payment field of any kind exists in the theme** — no card number, no CVV, no expiry.
- **No shipping calculator and no tax calculator.** The tax sentence is derived from `cart.taxes_included`.
- `content_for_additional_checkout_buttons` renders on the **cart page only**, guarded by `{%- if additional_checkout_buttons -%}`. It can appear only once per page, and the drawer's Checkout submit reaches the same place. On the product page, `{{ form | payment_button }}` is emitted un-wrapped behind `show_accelerated_checkout` — the filter emits its own container and `data-shopify` attribute, and a second wrapper is what makes Shopify's script bind twice. Its colours, type and label live in a closed shadow DOM; the stylesheet sets two of the five documented custom properties so its height and radius match the primary button above it.

Checkout branding, shipping rates, taxes and accelerated-checkout availability are all Shopify Admin concerns and none is reproduced in the theme.

---

### Search

#### The results page — `sections/main-search.liquid`

A real `role="search"` GET form to `routes.search_url` with a labelled `q` input, three states (no query, results, zero results), `{% paginate %}`, product results through `snippets/product-card.liquid`, and non-product results in a separate group.

Hidden inputs that must not be dropped:

| Input | Why |
|---|---|
| `type` = `search_types` | omit it and the merchant's configured scope silently reverts to Shopify's all-types default |
| `options[prefix]` = `last` | omit it and the partial last-word match stops applying |

`search.terms` is echoed back in the input's `value` through `| escape` — an attribute value is the one place on the page where nothing else escapes it. The two `| t` calls that put the term into sentences pass it unfiltered, because translated content is escaped by default and no locale key here carries the `_html` suffix. *That documented rule has not been empirically confirmed for interpolated variables, and can only be confirmed on a real store.*

Heading levels come from `search.types`, not from what a given page of results happens to contain: `group_headings` is true when `search.types.size > 1`, and result titles are `h3` then, `h2` otherwise. A page-by-page derivation would put card titles at `h3` on page one and `h2` on page two, so the same query would change its own outline as the customer paged through it.

`search.results` is a **mixed array** — products, pages and articles in relevance order — and `paginate` slices it without regard to type, so the slice is rendered twice, each pass taking only its own type, with both counted first so an empty `<ul>` or an empty group heading never ships. The eager tile is chosen by counting **tiles actually emitted** (`tiles_emitted == 1`), not `forloop.first`: on a query whose top result is a page, `forloop.first` would be true for that page and no product would ever load eagerly. Articles get `excerpt_or_content | strip_html | truncatewords: 25`; pages get none, because truncating `page.content` would print the first 25 words of a shipping policy under its own title.

Settings: `search_types` (default **`product`**), `results_per_page` (12–48, default 24), `surface`, and the three column ceilings (4/2/2).

#### The header search panel (Phase 13)

The header control stays a **plain link** to `routes.search_url`, left byte-identical, carrying `data-search-trigger`. `assets/header.js` intercepts the click, with the same modified-click guard `cart.js` applies to the cart bubble. With scripting off the control still navigates to a complete search page; a `<button>` would have been a control that does nothing.

It is a **panel** — an overlay layer — never an expanding field in the header row. Arithmetic, not taste: at 375px the header row has 327px of content box; the start cluster takes 44px, the end cluster 148px (3 × 44 + 2 × 8), the two grid gaps 32px, leaving the branding track exactly **103px**. A usable field needs about 180px. `.header__inner`'s grid never changes and nothing is added to that row.

`aria-haspopup="dialog"` and `aria-expanded` are set by JavaScript at initialisation, **never printed by Liquid** — they are claims about behaviour that only exists once the script runs. The panel's bindings go in `header.js`'s existing registry and are released by the Phase 11 teardown.

**A live inconsistency worth fixing:** the panel hardcodes `<input type="hidden" name="type" value="product">` with a comment saying it matches `templates/search.json`. It does today, because `search_types` ships as `product`. If a merchant switches the section to *Products, pages and articles*, the header panel will still submit products only and the two surfaces will disagree. The panel should read `settings`-level or section state, or the section setting should be promoted to theme level.

#### Predictive search — deferred, with its contract recorded

Not built, by the owner's decision, because its value is a function of catalogue size (below ~25 products a customer reaches everything faster by scrolling one collection) and the launch catalogue is small. Cost measured at roughly 7 KB gzipped plus a section, a snippet, a stylesheet, an ARIA combobox and a third dismissable surface. **A catalogue count unblocks it.**

If it is ever built, this is the contract:

- Shopify's **section-rendering endpoint** — `routes.predictive_search_url` with `section_id` — never the JSON endpoint and never a hardcoded `/search/suggest`, which is locale-prefixed on non-primary locales. Section rendering keeps every escaping decision in Liquid and reuses the theme's own card.
- **Six stale-response guards, because no single one closes the window:** 300ms debounce; 2-character minimum; an `AbortController` per request; a captured-term comparison at resolve, because `abort()` is not synchronous; a monotonic generation counter; and a cache keyed on the normalised term.
- `resources[limit]=4` with **`limit_scope=each`** — the default `limit_scope=all` means ten results across all types.

The header panel already provides the surface, the trigger interception, the focus management and the Escape handling, so this is a drop-in rather than a rewrite.

#### Filtering is deliberately not on `/search`

shopify.dev states that applying filters on the search results page **strips out all non-product results**, and `main-search.liquid` renders a non-product group whose setting help text promises the merchant that "pages and articles come back as a titled list below it". The moment any filter were active that promise would silently stop being true.

`snippets/facets.liquid` is written against a generic `results` parameter precisely so adding it later is one `{% render %}`. What must accompany it: three hidden inputs in the facets form — `q` (or the search is discarded), `type`, and `options[prefix]=last` — plus `search.sort_options`, because a lone sort control over a relevance-ranked set is a downgrade.

---

### Collection and filtering

#### `sections/main-collection.liquid`

Real `collection.title` (the page's one `h1`), `collection.description`, collection image and product count; a GET sort form that works with JavaScript off; `{% paginate %}`; and two distinct empty states. `products_per_page` defaults to **24**, which divides evenly into 4, 3 and 2 columns so no tier ends on a ragged row. The section ships **zero JavaScript** of its own.

**The grid/empty split tests `paginate.items`, never `collection.products.size`.** Inside a paginate block `collection.products` is the *page slice*, so an out-of-range `?page=` — which Shopify answers with a 200 and an empty slice rather than a 404 — printed "This collection is empty." over a collection that has products. The product count already read `paginate.items` correctly; the empty test simply had not followed the section's own reasoning. *This fix is verified at source level only: the harness's `{% paginate %}` always serves page 1.*

Column counts arrive as scoped custom properties, never inline styles:

```liquid
#shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_m }}; }
@media … { … {{ cols_t }} … {{ cols_d }} … }
```

**The merchant's column count is a ceiling, not a command.** `.product-grid` is `auto-fill` with a 272px track floor above 768 and 8rem (128px) below it, so the grid drops a column rather than squeezing one. There is no setting a merchant can choose that produces a broken grid, and no horizontal overflow at any width including 320.

The collection header's bottom margin is placed on `.main-collection__header`, **not** on `.facets` — below `--bp-md` that element becomes `.facets--drawer`, which is `position: fixed` with `inset-block: 0`, so a margin there would displace the fixed drawer rather than space the page.

#### `snippets/grid-sizes.liquid` — the shared `sizes` derivation

Shared by `main-collection` and `main-search`. Parameters: `cols_d`, `cols_t`, `cols_m`, and `chrome_d` (default 96; `featured-collection`'s copy-column preset passes 128).

Constants: `gap` 32, `gap_m` 16, `col_min` 272, `col_min_m` 128, `chrome_m` 48, `chrome_t` 64, `container` = `settings.container_width | default: 1440`.

Two correctness rules, both learned the hard way, both of whose violations ran in the **under-declaring** direction — the direction that costs image quality:

1. **A clause may not claim a width before the layout that produces it applies.** `threshold_d` is derived from column arithmetic and is then floored at 1024, because the desktop column count does not take effect until `--bp-lg`. Unfloored, at three columns it computed 976 and declared 280px for a slot painting 452px between 976 and 1023.
2. **A clause may not divide by more columns than actually fit.** At the container cap the row stops growing, but the grid is auto-fill with a 272px floor. `fits_d = (capped_row + gap) / (col_min + gap)`; `cols_capped = min(cols_d, fits_d)`. With four columns and the container narrowed to 1200, dividing by the requested four declared **253px for a track that paints 346px** — a 27% under-declaration reachable with default settings. `capped_track` rounds **up** (`… | plus: 1`) because integer division truncates.

It was three copies of the same ninety lines. Phase 10 fixed the desktop-clause bug in one of them and the other two carried it for two more phases, **because the fix was applied to an instance rather than to the rule.** `sections/featured-collection.liquid` is deliberately still not consolidated — its copy-column preset scales the needed row by 1000/727 because the grid occupies only 72.7% of it — so **a future change to the shared rules must be applied there too.**

#### `snippets/facets.liquid` — Shopify native filtering only

No custom filter database, no second product index, no filtering logic in JavaScript. Parameters: `results` (anything carrying `.filters`), `form_id`, `id_prefix`.

**One form, one set of controls — the most consequential decision in this area.** The filter controls are rendered **exactly once** in the document. At `--bp-md` and above they are a horizontal row of `<details>` dropdowns above the toolbar; below it, once script has upgraded them, the same element is a fixed drawer. That is a CSS difference, not a second copy. Themes that render a desktop sidebar and a mobile drawer separately must keep two sets of checkboxes in step and submit both; here there is one checked state, one submitted value per choice, and nothing to synchronise.

Every control binds to the one `<form method="get">` by the HTML **`form` attribute**, not by DOM nesting — which also keeps the product grid outside the form, so a future quick-add `<form>` cannot nest inside it.

**A horizontal bar, not a sidebar, in numbers.** With `chrome_d` 96, the 1440 container's capped row is 1344 and `(1344 + 32) / 304 = 4` columns fit. A 240px sidebar plus a 48px gap makes `chrome_d` 384: the capped row is 1056 and only **3** fit — and at the 1200px container a merchant may set, only **2**. A sidebar narrow enough to keep four columns is about 112px, which is narrower than the word "Availability". The bar costs one control height plus one gap, once, and leaves every number in `grid-sizes` untouched.

**The sort form was going to drop every filter.** Before Phase 13 it existed only for sorting and its own comment recorded that it "sends `sort_by` and nothing else". The form is now rendered whenever there is **either** a sort control or a filter control (`{%- if show_sorting or has_filters -%}`), with the sort label and select behind their own condition inside it. Its submit button carries **no `name`**, so it contributes nothing to the query string and nothing named `submit` shadows the form's own submit method. No `page` parameter is rendered, so any submission returns to page 1 — which is what Shopify's own `url_to_add` does anyway.

**Sort submits on a button, never on change.** Submit-on-change is a WCAG 2.2 SC 3.2.2 *On Input* failure at Level A, and it is worst for a keyboard user arrowing through options, who triggers a navigation on every option they pass.

**Filter quality.** A group with a single value is **dropped** — Shopify returns one whenever a collection happens to hold one vendor or one product type, and it gives the customer a control whose only effect is to filter nothing out. The rule lives in the snippet so every caller inherits it, and the section's `has_filters` counts only groups the snippet would actually render, so a collection whose only filter is degenerate shows no Filter button at all. A `price_range` group is kept regardless, because its `values` array is empty by design — its controls come from `min_value`, `max_value` and `range_max` (which arrives in cents and is divided by 100 for display).

Every label, value, count and URL comes from Shopify. The only literal parameter names are `filter.v.price.gte` and `filter.v.price.lte`, used as fallbacks when the customer has set no bound, and those are the names Shopify documents.

**Nothing renders until a merchant configures filters** in *Apps › Search & Discovery › Filters*. Until then `collection.filters` is empty, there is no panel, no Filter button and no active-filter row, and **`component-facets.css` and `facets.js` are not loaded at all** — a store with no filters pays nothing. In the **Theme Editor only** (`request.design_mode`) a note explains why; the live storefront says nothing.

#### Active filters

Applied values render as removable chips **outside** the panel, so a customer on a phone can see what is applied without opening anything. Each chip is a link carrying Shopify's own `url_to_remove`; Clear all is a link to `collection.url`.

**Chips act immediately while checkboxes apply on confirm, and that split is deliberate and written into the snippet so it is not "harmonised" away.** SC 3.2.2 governs changing the setting of a control; activating a link is not that. Chips are 24px — the SC 2.5.8 floor — because removal is also reachable from the group the value came from, which is the equivalent control that exception allows. Filter values themselves are 44px, because there is no larger equivalent beside them.

#### URL state

Entirely Shopify's scheme. Checkboxes are named for the filter's own `param_name` and carry Shopify's own `value`, so checking two boxes in one group submits the parameter twice — which is exactly the OR encoding Shopify documents. The no-script path produces the same URL the scripted one would. Back and Forward behave normally because nothing manipulates history: every state change is an ordinary navigation.

#### `assets/facets.js` — the drawer, and only the drawer

10,937 bytes raw, **3,848 B gzipped measured now** (this supersedes Phase 13's 7,055/2,473, which predates the Phase 16 fix and the Phase 18 exit animation).

**The drawer is opt-in, not the base state.** `position: fixed` applies only under `.facets--drawer`, a class the script adds. That ordering is load-bearing: with no script the panel must be in flow and visible, because the button that would open a drawer is the thing the script was going to reveal. A fixed panel with no opener is a filter UI a customer cannot reach. So the no-script mobile experience is a stack of collapsed groups above the grid — already a usable filter UI, with zero JavaScript.

**The width gate is evaluated at load, not only on change** (Phase 16 P0, a desktop keyboard trap reproduced at 1440/1280/768):

```js
var mq = window.matchMedia('(min-width: 768px)');
function applyWidth(isDesktop) { … }
applyWidth(mq.matches);                       // ← this line is the fix
mq.addEventListener('change', onChange);
```

The listener only ran on `change`, so it correctly closed a drawer left open by a rotation and **never once evaluated the width the page loaded at**. `open()` also refuses when `mq.matches`, and `component-facets.css` retires the trigger at `min-width: 768px` — the same pattern `header.css` uses to retire the mobile menu.

`aria-expanded` and `aria-controls` are set by the script, truthful only once the panel can actually be controlled. The drawer traps focus, closes on Escape, returns focus to its trigger, and its exit slide is driven by an `.is-closing` class held until `transitionend` with a 500ms fallback. **Its scroll lock follows the header's class-based lock** (`.facets-open body { overflow: hidden }`), never `cart.js`'s `position: fixed` lock.

`facets.js` follows the Phase 11 lifecycle contract: idempotent per element, every global binding recorded and released as one unit, teardown on `shopify:section:unload`.

There is **no overlay behind the filter drawer.** Escape, the close button and the trigger all dismiss it.

#### Two empty states that say different things

A collection with **no products** is a merchandising state the customer cannot act on: `collection.empty.title` / `.body` plus a link to `empty_link | default: routes.root_url`. A collection whose **active filters match nothing** is one they can fix in a click: `collection.filters.none_match.title` / `.body` plus **Clear all** to `collection.url`. Telling a customer the collection is empty when they have four filters applied would be false. Neither invents a product.

`snippets/cart-empty-state.liquid` is deliberately **not** reused here — its three strings are about a cart, and a shared empty-state component with a strings parameter is worth building only once a third surface needs one.

Empty-state titles (`.cart-empty__title`, `.main-collection__empty-title`, and search's) are `<p>` on the interface-heading row — body family (Jost), `--type-h3-size`, weight 600, sentence case — never the page `h1`'s type.

#### Shopify's own ceilings

At most 25 filters per store; none on collections over 5,000 products; none on search results over 1,000. **Filtering cannot be demoed or QA'd without the Search & Discovery app on a real store** — the harness proves the guard renders nothing, proves the populated markup against documented fixtures (`FILTERS_NONE`, `FILTERS_ALL`, `FILTERS_ACTIVE`, `FILTERS_DEGENERATE`, every field one shopify.dev documents), and proves the responsive behaviour. It cannot prove the real filter values look right.

---

### The product card, badges and pricing

`snippets/product-card.liquid` is the **single** card, used by `featured-collection`, `main-collection` and `main-search` with zero page-scoped CSS overrides. No second card was created, and none should be.

Contract: one anchor wrapping the media and the title with **no other interactive element inside it**; swatches and price outside it; the focus ring drawn around the **whole card** by `:has(:focus-visible)` with an `@supports not selector(:has(*))` `:focus-within` fallback; a real heading at a caller-chosen level (`heading_level`, default 3 — 2 when the section has no `h2`, so the outline never skips); and every value read from the Shopify product object.

**Pricing.** Every price goes through `| money` against the store's own format. No currency symbol is hardcoded anywhere in the theme — grep-verified for `₱`, `PHP`, `USD` and `$<digit>`, which hits only comment prose. A varying price renders "From X" and **no** compare-at: a range beside a strike-through is not information. The sale state carries visually-hidden "Sale price" / "Regular price" labels.

**One badge, SOLD OUT**, from `product.available`, inside the media box, marked `aria-hidden` with the same words appended to the link's accessible name. **No SALE badge and no NEW badge, by decision.** SALE's question is already answered twice, by the struck compare-at and by those labels. NEW has no honest native source — `published_at` resets on re-publishing, unhiding, an import or a store migration, so a date-based badge would eventually lie about every product at once. If NEW is ever wanted, the **only** approved mechanism is a merchant-set tag name, default empty, with SOLD OUT always winning the slot. `.product-card__error` is owned by `component-product-card.css` only; it does not share rules with the cart-line grouping.

**Secondary image on hover** (`card_hover_secondary_image`, theme-level, **default off**). Pure CSS, no JavaScript. Both images share the same `aspect-ratio: var(--product-aspect)` box so the swap cannot shift anything. The reveal rule lives **inside `@media (hover: hover) and (pointer: fine)`**, so a touch device has no state in which it can appear. It picks **the first image that is not the featured one**, not `images[1]` — a merchant can promote any image to featured without reordering the others. It is always lazy and is never an LCP candidate. It is off by default because the approved card hover is the 1.03 image lift plus the title underline, and turning a swap on by default would change the approved hover on every store.

The defect it shipped with is worth remembering as a method lesson: `.product-card--sold-out .product-card__image` is specificity (0,2,0) and `.product-card__image--secondary { opacity: 0 }` is (0,1,0), and the secondary `<img>` carries **both** classes — so a sold-out product with two photos painted both images superimposed at 60% **on every device including touch**. The fix is `:not(.product-card__image--secondary)` on the dim, plus a rule that dims the secondary when it is revealed on a sold-out card. **The first test of this passed, because it asserted the rule *contained* `opacity: 0`. String-matching CSS cannot verify the cascade — only a browser can answer which rule won**, and a probe must render the card through a section, because the card's CSS is linked by the sections that use it, not by the snippet.

Missing image: the tile ground renders and nothing stands in for a photograph that does not exist. Fewer products than requested: renders what exists, **no placeholders, ever**. Alt text comes from the image object, and is emitted empty when Shopify has defaulted it to the product title, which is already inside the same link.

#### Quick add — built, correct, and unreachable

`snippets/product-card.liquid` contains a complete quick-add implementation behind a `quick_add` parameter. **No section passes it.** `grep -rn "quick_add" sections/` returns nothing, so no template renders it today.

When it is enabled it refuses to guess: more than one variant → a **Choose options** link to the product page; one available variant → a real form posting `product.selected_or_first_available_variant.id` to `routes.cart_add_url`; unavailable → a real `<button type="button" aria-disabled="true">`, **never a `<span>` wearing button classes**. It therefore cannot add an incorrect variant.

It must carry all three cart hooks, and the third one's **name** matters: `[data-add-to-cart]`, `[data-add-to-cart-label]`, and **`[data-product-error]`** — not `data-cart-error`, which is the attribute the drawer and the cart page use for their own failure lines, read by a different function. The consequence of getting it wrong ran both ways: a failed quick add showed the customer nothing, and `showCartError` printed a cart-line failure onto every product tile on the page. Both halves are fixed. **Exposing quick add is one setting per section; it is an open decision, not an oversight.**

---

### Customer accounts, order history and tracking

**Shopify deprecated legacy customer accounts on 26 February 2026. Order history, order details, tracking and customer information are not theme-buildable.** This is not descoping — there is no surface. Those pages are served from `shopify.com/<store-id>/account`, on a different origin, and their branding comes from **checkout** settings, which is the exact inverse of legacy accounts.

Five primary-source facts:

1. *"Legacy customer accounts are no longer available to new stores and existing stores not using it."* — shopify.dev changelog, 2026-02-26
2. *"Theme developers should no longer include legacy customer account liquid files."* — same changelog
3. *"Publishing a theme without these templates automatically upgrades merchants to the latest customer accounts experience, which operates independently of themes."* — templates reference. **Shipping `templates/customers/*` does not make a theme safer; it withholds the merchant's upgrade.**
4. Dawn v16.0.0 (2026-08-10) deleted all seven templates and all seven sections.
5. *"Customer accounts: use branding from your checkout settings"* — against legacy's *"use branding from your online store theme settings"*.

**`templates/customers/` does not exist and never has, and it must stay absent.** That absence is the auto-upgrade trigger. Eight assertions hold it, each seen to fail against a seeded violation: no `templates/customers/`, none of the seven template names, no `main-account`/`main-order`/`main-login`/… section, and no customer `{% form %}` tag anywhere in the theme.

#### One code path, branching on nothing

**There is no Liquid-readable way to detect which account system is active.**

- `shop.customer_accounts_enabled` is documented as *"Returns true if the store shows a login link."* It is **true under both systems**.
- `shop.customer_accounts_optional` is an independent *checkout policy* flag. The name invites the wrong reading.
- No third property exists — all 33–36 `shop` properties were enumerated. No `customer_accounts_version`, no `customer_accounts_url`.
- The popular forum workaround `{% if routes.account_login_url contains 'shopify.com' %}` is **unsound**: `account_login_url`'s documented value is the relative `/account/login` even on a store whose `account_profile_url` is an absolute `shopify.com` URL.

A merchant can also revert an upgrade within 30 days with no signal, so a theme that hard-assumed one system at install time could be wrong a week later on the same store. `shop.customer_accounts_enabled` is used **exactly once**, as the show/hide gate it is documented to be, and a test asserts that count is one.

#### The entry point — the whole of the account code surface

```liquid
{%- if shop.customer_accounts_enabled and section.settings.show_account -%}
  <shopify-account
    class="header__control header__account"
    menu="{{ settings.customer_account_menu | default: 'customer-account-main-menu' }}"
  >
    <span class="header__account-avatar" slot="signed-out-avatar">
      {% render 'icon-account' %}
      <span class="visually-hidden">{{ 'header.account' | t }}</span>
    </span>
  </shopify-account>
{%- endif -%}
```

- **One entry point, not two.** The old `<a href>` is gone. Two account controls would behave differently — one opening a sheet in place, one navigating off-site — and the 375px end cluster has no room for a second.
- **The `signed-out-avatar` slot keeps the brand's mark.** It is one of three things Shopify publishes as contractual; without it the header shows Shopify's default avatar.
- **The visually-hidden name stays.** If Shopify sets its own `aria-label` that wins and this is ignored; if it does not, the control is still named. Omitting it has an outcome that is an unnamed control (SC 4.1.2).
- **Two gates, both preserved:** the platform flag and the merchant's `show_account`.
- **The 44px target floor comes from the shared `header__control` class**, which sets `min-width`/`min-height: var(--target-min)` inside a flex cluster. Measurement killed both a `:not(:defined)` size reservation and every account-specific sizing rule — the element measured 44×44 at all seven viewports without them. **Do not reintroduce either.** An author rule on the element wins over the component's own `:host` styles, so the floor holds permanently; a `:not(:defined)` rule stops applying the instant the component upgrades. The end cluster measures 148px at every viewport from 375 to 1920 — unchanged from before the component landed.
- `--shopify-account-dialog-position-top` is **deliberately unset.** Its semantics could not be settled from the documentation, and this theme has a sticky header that a wrong guess would put the sheet underneath.

#### Login and dashboard

The theme contains **no authentication of any kind**: no login form, no password field, no session handling, no `customer_login` form tag, no token. Under current accounts there is no password and no registration step to build — sign-in is passwordless. On a legacy store the component degrades to linking directly to the sign-in page, so the replacement loses nothing either way.

`routes.account_login_url` and `routes.storefront_login_url` are **not interchangeable**: the first lands the customer on the account order index after sign-in, the second returns them to the page they came from. For a storefront the second is almost always the one you want. The theme links neither, because the component owns the transition. And `routes.account_url` goes to the **order index**, not a profile landing page — worth knowing before anyone labels a link "My account" and expects a dashboard.

The account menu is a **global** setting, not a section setting:

| Setting | Type | Default | Where |
|---|---|---|---|
| `customer_account_menu` | `link_list` | `customer-account-main-menu` | Theme settings › Customer accounts |

shopify.dev's component page shows `section.settings.customer_account_menu`; Dawn v16 defines it as a global `link_list`. **Dawn is right and the doc example is misleading** — copying the doc's form into a theme that defines the global yields an empty `menu` attribute and a sheet with no links. The help text says the part that is easy to miss: leaving it empty does **not** fall back to a default set of links.

#### Four absences the theme is held to

Asserted across every `.liquid` and `.js` file, each seeded as a violation and caught:

- no read of any `order.*` field
- no read of any `fulfillment` or `tracking_*` field
- no hand-built `/account/orders/…`, `order_status_url`, `customer_order_url` or `/authenticate?key=` URL
- no `routes.account_*` link at all

And a security rule that goes further: **no read of any customer field at all, printed or otherwise.** The `customer` object is global for any signed-in visitor, *"directly accessible globally when a customer is logged in"*, and the **Section Rendering API inherits the Liquid context of the requested page** — so one `{{ customer.email }}` in a shared snippet would be serialised into every `?sections=` response the cart makes. The leak vector is a shared snippet plus section rendering.

Also asserted absent from every theme script: `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`, `caches.open`, service-worker registration, and console logging. No customer data in a URL, a `data-` attribute or a query string.

Two facts that contradict reasonable assumptions: **a Liquid theme cannot set any HTTP response header** (the widely-repeated `Cache-Control` advice for customer routes is Hydrogen/Oxygen guidance with no Liquid counterpart; Shopify already serves account routes `private, no-store`), and **the order-status page is not private** — *"The unauthenticated Order status page can be accessed by anyone who has a direct link."* It redacts PII rather than blocking access, so no future phase may treat that URL as a secret.

#### If anyone ever builds order surfaces on legacy accounts

Only relevant if the store stays on legacy — and staying means shipping the seven templates, which withholds the upgrade for as long as they are there. These are the traps, all expensive and mostly silent:

- **`order.fulfillments` does not exist in theme Liquid.** It exists in Admin REST, Admin GraphQL, the Customer Account API and Order Printer Liquid, so nearly every search result uses it. In a theme it iterates nothing, renders nothing, throws nothing and passes Theme Check. Tracking is reachable only via `line_item.fulfillment.tracking_number` / `.tracking_url` / `.tracking_company`.
- **`order.total_price` is calculated *before* refunds.** Use `order.total_net_amount`.
- **`{% if line_item.product %}` is not a deleted-product guard.** A deleted product returns an EmptyDrop and EmptyDrops are truthy. Use `!= blank`. Dawn ships the truthy pattern in its *cart*, where the product provably still exists — copying that snippet onto an order page is the likeliest way to ship this bug.
- **`line_item.variant_title` does not exist** in Liquid. Use `line_item.variant.title`.
- **`line_item.price`, `.line_price`, `.total_discount`, `.discounts` are deprecated** — they exclude automatic discounts and codes, so they render a plausible number that is wrong on any discounted order and right on all your undiscounted test data.
- **`fulfillment_status_label` is localized.** Never string-compare a label; the raw `fulfillment_status` field has no documented values at all.
- **`customer.orders` caps at 20 per `{% paginate %}`** and truncates silently at 50 unpaginated.
- **Every money field is an integer in the currency subunit.** `{{ order.total_price }}` without `| money` prints `12999`.
- **There are three different order URLs** — `customer_url` (token path), `order_status_url` (`/authenticate?key=`), `customer_order_url` (shopify.com host, numeric id + JWT) — and `/account/orders/<id>?key=` is none of them.

#### Open, and needing a live store

1. **Which account system this store uses** — *Settings › Customer accounts*. Still a business decision. The theme is correct either way, but the answer determines whether anything else applies.
2. **The component's accessible name needs one live screen-reader check.** Dawn ships it with no label, implying Shopify names it; this theme supplies one in the slot so the control is named under either behaviour. What cannot be checked from here is whether the two combine into a doubled announcement. **If it announces twice, delete the `<span class="visually-hidden">` from the slot.**
3. **The control is not focusable until Shopify's script upgrades it** — measured `tabIndex` of -1 while undefined. The old `<a href>` worked with no script. Inherent to the component; not worked around, because a fallback link inside the slot would nest an anchor inside the upgraded button.
4. The harness can never test the component — it does not load Shopify's script, so every measurement is of the *reservation*, never of the component.

---

### 404 and pages

#### `sections/main-404.liquid`

The surface every mistyped URL, dead link, deleted product and shared sold-out URL lands on. **Zero JavaScript.** `surface-dark` is fixed rather than a setting, because the accent button variant has no light-surface rule at all — gold on cream measures 1.55:1 — so the page's one call to action paints only on ink.

Two settings, `button_url` and `button_label`. The default destination is **`routes.root_url`**, the same answer the empty cart gives, and for the same reason: `routes.all_products_collection_url` depends on a collection template, and **sending a customer who has just hit one error page to a second one is the worst outcome this file can produce.** `button_label` carries **no schema default** on purpose — a schema default would freeze one language into `settings_data.json` and every other locale would render English, so an untouched theme reads the label out of `locales/en.default.json`.

Deliberately absent: no search form (the header already carries the store's search control on this page like every other); no product recommendations or "you might like" row, because there is no data behind either; no list of suggested destinations, because every destination in this project is business information and the merchant's header menu is the supported answer; and **no automatic redirect** — URL redirects are a Shopify admin feature, and a client-side one takes the address bar away from someone who may have mistyped one character. The heading and message are generic UI locale strings, not brand voice: no tagline, no scripture, no joke about being lost, no claim of any kind.

#### `sections/main-page.liquid`

Title and text come from the page in Shopify admin; nothing on the page is written in the theme. Settings: `show_heading` (default true), `surface`, `spacing_top`, `spacing_bottom`.

**`show_heading` hides the `h1` visually; it never removes it.** The setting appends the shared `visually-hidden` utility to the title's class list, so the heading stays in the accessibility tree and the page never ships with no `h1`. The help text tells the merchant to start their own text at Heading 2, because Heading 1 belongs to the title and the theme cannot change the level of text already written. `page.title` goes through `| escape`; `page.content` is merchant HTML from Shopify's rich-text editor and is rendered as-is inside `.rte`.

Line length is **not** a setting: the text sits in a single reading column capped at the design system's measure and stays there on the widest screen. Prose surfaces carry `overflow-wrap` on the content root. The merchant rich-text inline link has a pointer-scoped `:hover` to `var(--accent-current)` in all five stylesheets that declare its rest rule — collection description, product description, Our Story body, footer and page content.

---

### Conversion, analytics and structured data on these surfaces

- **No analytics of any kind** exists in the theme and none may be added. On current Shopify a theme cannot publish standard events; every one is emitted by Shopify from a sandbox the theme cannot reach. `layout/theme.liquid` emits `{{ content_for_header }}` once, unmodified — that is the theme's entire load-bearing dependency for analytics and consent, and a standing assertion protects it.
- **Opening the drawer makes no network call** — it is rendered with the page and shown, never fetched. A drawer that fetched on open would make Shopify emit a cart event on every open. Consequence: `cart_viewed` fires rarely on this store, by design.
- Whether `product_added_to_cart` fires for an **Ajax** add is undocumented and is recorded as an unknown. **Verify it on the real store.** If it does not, the fix is a custom pixel subscribing to a custom event the theme publishes via `Shopify.analytics.publish` with a prefixed name — and that is the *one* circumstance in which this theme should ever contain analytics code.
- Measured Shopify-call counts per customer action: variant select 0, quantity press 0 (the request is the debounced mutation), add 1, drawer open 0, reopen 0, line increase 1, removal 1.
- All three GET forms (search, collection toolbar, header panel) **discard UTM parameters**, by the same mechanism that drops the `page` parameter. **This is harmless and must not be "fixed":** Shopify records `landingPage`/`utmParameters` server-side at first request, GA4 fixes session source at session start, Meta has already written `_fbc`, and Dawn behaves identically — while carrying UTMs through internal forms would create self-referrals. A **reserved-parameter guard** is in place: Shopify special-cases `ref`, `source` and `r` storefront-wide as the marketing referral code, so no form field on any surface may use those names.
- Structured data on these surfaces is `{{ product | structured_data }}` and nothing else. `Organization` is not implemented (a `sameAs` array that is empty half the time is worse than no block) and `BreadcrumbList` is not implemented (the theme has no navigation hierarchy to describe; a fabricated trail is fake structure).
- `snippets/meta-social.liquid` covers Open Graph. Every value is a Shopify object; the `og:image` chain is product → collection → `settings.share_image` → logo, each branch guarded so a store with no image emits no `og:image` rather than a URL that 404s. Height is derived from `width`/`height` and guarded against a zero width — **never from `aspect_ratio`**, which is not populated on every image drop, where Liquid treats the missing value as 0 and it threw a division by zero in the head on all seven templates.

---

### Measured asset weight on these surfaces

Measured now, gzip -9:

| Asset | Raw | Gzip |
|---|---:|---:|
| `assets/cart.js` (layout, every page) | 39,750 | 12,008 |
| `assets/product.js` (product only) | 18,096 | 5,608 |
| `assets/facets.js` (filtered collection only) | 10,937 | 3,848 |
| `assets/header.js` (layout) | 13,963 | 4,329 |

`cart.js` alone exceeds Shopify's `AssetSizeJavaScript` 10,000 B threshold, and about half of it is comment. The recorded answer is a **minification step at deploy**, not restructuring the cart with import-on-interaction. The binding budget: JS all pages ≤ 30 KB gz, per page-load script ≤ 10 KB gz, CSS worst page ≤ 55 KB gz, requests worst page ≤ 30, load CLS ≤ 0.05, handler time ≤ 50 ms, eager images **exactly 1**, `fetchpriority` ≤ 1, third-party scripts each one justified in writing (currently zero).

The cart page's 0.0125 load CLS is the deliberate price of a working no-JavaScript Update button and is recorded rather than hidden.

---

### Open items and things that were not verified

**Business information still required:** no products exist, so every state on these surfaces was rendered against mock data; shipping scope (no claim, threshold or estimate appears anywhere and none can until a policy exists); currency and Markets; the size run; the peso glyph (Jost carries neither `₱` nor `→`, so the peso falls back to a per-platform face in the most legibility-critical string on the page); whether accelerated checkout should show at all; a catalogue count for predictive search; the badge vocabulary; whether quick add should be exposed; and a free-shipping threshold, cart recommendations or a cart discount field — none of which may be invented.

**Never verified against a real store:** Theme Check has never been run (no Shopify CLI in this environment — **run `shopify theme check` before going live**; the two residual Theme Check errors are the missing `theme_support_email` and `theme_documentation_url`); `{{ product | structured_data }}`'s real output; `page_description`'s fallback; real PHP money formatting; real discount allocations; checkout itself; the account sheet and its dialog position; the `<shopify-account>` accessible name; `| t` interpolation escaping for variables; and the out-of-range `?page=` empty-state fix, which is verified at source level because the harness's `{% paginate %}` always serves page 1.

**Browser coverage is Chromium-only.** Edge 153 and Chrome both pass, which mainly rules out harness artefacts. **Safari (WebKit) and Firefox (Gecko) are untested**, and the two things most worth checking there are the `position: fixed` scroll lock on iOS Safari and `inert` support, which the Tab trap falls back to without. No real device was tested at all.

**Not measured:** no Lighthouse score exists anywhere in this project and none may be invented; no field Core Web Vitals; font-swap CLS; TTFB/FCP/LCP/INP on a real server.

**Code-versus-document discrepancies found while writing this section — the code is the truth:**

1. `snippets/quantity-selector.liquid` **does** render the stepper buttons; `assets/component-quantity.css` hides them with `display: none` until `.cart-js`. Phase 8's "not rendered" is imprecise.
2. The embedded variant table carries **nine** keys, not the six Phase 8 documented — `low_stock` and `quantity_rule` arrived later.
3. Phase 8 §13.9 says the empty-cart destination "Defaults to the store's all-products collection". It defaults to `routes.root_url`, the home page, in both the snippet and both schemas.
4. `snippets/cart-empty-state.liquid` and `sections/main-404.liquid` still comment that no collection template exists. `templates/collection.json` exists. The home-page default stands anyway, deliberately.
5. Seven sections emit `{{ section.shopify_attributes }}` on their root — `hero`, `main-404`, `main-cart`, `main-collection`, `main-page`, `main-product`, `main-search` — while `sections/featured-collection.liquid` deliberately omits it on the documented ground that `shopify_attributes` exists on the **block** object only. Harmless either way (it resolves to nothing), but the theme is internally inconsistent about it. `{{ block.shopify_attributes }}` is correctly present on every block wrapper in `announcement-bar`, `footer` and `our-story`.
6. `sections/header.liquid`'s search panel hardcodes `type=product`; `sections/main-search.liquid` reads `search_types`. They agree only while the shipped default holds.
7. Byte figures in Phases 8, 13 and 14 predate later edits: `cart.js` is 39,750 B (Phase 8 said 27 KB, Phase 14 measured 38,737 B) and `facets.js` is 10,937 B (Phase 13 measured 7,055 B).

---

## The Shopify integration contract

This is what the theme needs **from** Shopify. Nothing in this section is a code task: it is the set of platform facts the theme was built against, the admin configuration without which built surfaces render nothing, and the list of things a theme is no longer permitted to do at all. The theme is at `C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme\` — 75 files, Online Store 2.0, JSON templates and section groups, `theme_info.theme_version` `0.5.0`.

**It has never been uploaded to a Shopify store.** Every behaviour below was verified against a mini-Liquid harness and headless Chromium. Section Rendering API responses, real `content_for_header` output, real image-CDN behaviour, `paginate.parts` URLs and Theme Check against a live store are all unverified against the platform. Treat the integration as designed-and-tested-offline, not proven.

---

### 1. The one load-bearing platform hook

`layout/theme.liquid:127` emits `{{ content_for_header }}` once, unmodified, inside `<head>`. A standing assertion protects it (`phase17/tracking.py`).

Everything the theme relies on from the platform arrives through it:

| What it delivers | Who consumes it in this theme |
|---|---|
| `window.Shopify.routes.root` | `assets/cart.js:105` — every Ajax URL is built from it |
| Shopify analytics + Web Pixels runtime | nothing in the theme; Shopify emits all events itself |
| Customer-privacy / consent API | nothing in the theme; there is no tracking to gate |
| The `<shopify-account>` element's script | `sections/header.liquid:217` |

Shopify documents that this output must not be parsed or altered. It is not. **Do not add anything to it, and do not move it below the stylesheets** — the Phase 10 fix that put `{% style %}` around `font_face` and ordered `css-variables` after the stylesheets depends on head order staying as it is.

---

### 2. Routes: the theme builds no URLs

Every storefront URL comes from the `routes` object or from a Shopify object's own URL property. There is no hand-built path anywhere, and this is asserted.

| Route object | Where used |
|---|---|
| `routes.root_url` | `header.liquid:98,138`, `footer.liquid:182`, and as the fallback destination for the 404 (`main-404.liquid:50`), the empty collection (`main-collection.liquid:172`) and the empty cart (`cart-empty-state.liquid:30`) |
| `routes.cart_url` | the cart form action on both surfaces (`cart-drawer.liquid:103`, `main-cart.liquid:54`), the drawer's View cart link, the header cart link, the add-confirmation link |
| `routes.cart_add_url` | the quick-add form in `product-card.liquid:295` |
| `routes.search_url` | the header search trigger and panel form, `main-search.liquid:152` |
| `routes.account_url` | **no longer linked** — replaced by `<shopify-account>` (§8) |
| `collection.url`, `item.url_to_remove`, `filter.url_to_remove`, `paginate.parts` | View all, cart removal, filter chips, pagination |
| `window.Shopify.routes.root` | `assets/cart.js` — `url(path)` prefixes every Ajax call |

Two rules behind this, both from measurement not preference:

- **A hardcoded `/cart/add.js` 404s silently on any store with Markets or a second language**, because those stores serve the cart under a locale prefix. `cart.js` falls back to `'/'` only if `window.Shopify.routes.root` is absent.
- **`routes.all_products_collection_url` is deliberately *not* used** as the empty-state or 404 destination (`main-404.liquid:18`, `cart-empty-state.liquid:15`). It was judged the wrong answer for this store and the destination is a merchant setting instead — see §10.

`routes.account_login_url` and `routes.storefront_login_url` are **not interchangeable**: the first lands the customer on the account order index after sign-in, the second returns them to the page they came from. The theme links neither.

---

### 3. The Ajax Cart API

`assets/cart.js` (39,750 B raw, 12,073 B gz, zero dependencies, one global `window.GodSquad.cart`) is the only consumer.

| Endpoint | Body | Notes |
|---|---|---|
| `cart/add.js` | `FormData` from the real `<form>` | **No `Content-Type` header** — setting one overwrites the multipart boundary the browser generated |
| `cart/change.js` | JSON, keyed by **line item key** | Never by index, never by variant id; the key is re-read from freshly rendered markup every time, because it is not stable across mutations |
| `cart/update.js` | `{note: value}`, **no sections requested** | The order note only; nothing on the page depends on the note's own re-render |

Failure detection: a response counts as failed when `data.description` is present **or** the status is not ok — because Shopify's `status` field "is sometimes the integer 422 and sometimes the string `bad_request`".

**A 422 from `/cart/add` can mean the cart changed anyway.** The returned sections are applied either way; if there are none and it was not a transport failure, the cart is re-read. Showing the old cart after a partial add would be a lie. No raw API error, status code or exception is ever shown to a customer.

Every control degrades without the script: the product form posts natively to `/cart/add`, the cart form posts to `routes.cart_url` with positional `updates[]`, removal is `item.url_to_remove`, the header cart control is a link to `/cart`. `cart.js` only cancels those defaults.

---

### 4. The Section Rendering API

Requested in the **same round trip as the mutation**, so every surface shows the server's view of the cart after the change — never a number the theme calculated.

```
sections      = the render-target list, collected at init
sections_url  = window.location.pathname
```

Rules that are not optional:

- **`sections_url` must be `location.pathname`** and must begin with a slash, or the whole request returns 400 — and Shopify's docs warn that a 400 for this reason does **not** mean the mutation was rolled back.
- **Targets are collected from the page at init, not fixed** (`cart.js:73` `collectSections()`): always `cart-icon-bubble`; plus `cart-drawer` when `[data-cart-drawer]` exists; plus the cart page's runtime section id read from `[data-cart-page-section]`. At most three of Shopify's five-section limit.
- **`sections/cart-icon-bubble.liquid` carries no schema, no preset and no `enabled_on`/`disabled_on`, deliberately.** A section placed in a JSON template gets a generated id like `sections--1234__header` which changes; a section file rendered standalone keeps its filename as its id, so `cart.js` can ask for `"cart-icon-bubble"` by name. Its whole body is `{% render 'cart-icon-bubble' %}` — the same snippet the header renders inline, so the two cannot drift.
- **Take the returned `<div id="shopify-section-…">` wrapper's *inside*.** Replacing `outerHTML` nests a second wrapper on every update. `swapInner()` does this.
- **A `null` section in the response is skipped**, not treated as empty markup.
- **The drawer is never rendered on `/cart`** and the cart page is itself a render target of every mutation. Rendering both put two views of one cart on one screen with duplicate DOM ids; not re-rendering the page left its **positional** `updates[]` inputs misaligned with the server's lines, so Checkout would have applied each surviving quantity to the wrong product.
- **The heading, live region and error line sit *outside* the swapped node.** A focused element inside a replaced subtree is destroyed and focus drops to `<body>`; a live region recreated with its text announces nothing.

**Security consequence, and it governs the whole theme:** the Section Rendering API *inherits the Liquid context of the requested page*. One `{{ customer.email }}` in any shared snippet would be serialised into every `?sections=` response the cart makes. The theme is therefore asserted to contain **no read of any customer field at all**, printed or otherwise.

---

### 5. Theme settings the merchant must configure

`config/settings_schema.json` — 14 settings across 8 groups plus `theme_info`. Read from the file:

| Group | id | Type | Default | Blocking? |
|---|---|---|---|---|
| Colours | `color_scheme` | select | `godsquad` | no — one scheme only ships |
| Typography | `type_display_font` | font_picker | `playfair_display_n9` | no |
| Typography | `type_body_font` | font_picker | `jost_n4` | no |
| Layout | `container_width` | range 1200–1800 | `1440` | no |
| Layout | `radius_sm` | range 0–8 | `2` | no |
| Products | `product_image_ratio` | select square/portrait | `square` | no |
| Products | `card_hover_secondary_image` | checkbox | `false` | no |
| Brand | `logo` | image_picker | empty | **yes** — header falls back to text |
| Brand | `favicon` | image_picker | empty | **yes** — feeds 32px, 192px and the 180px `apple-touch-icon` |
| Brand | `share_image` | image_picker | empty | **yes** for non-product pages' `og:image` |
| Cart | `cart_type` | select drawer/page | `drawer` | no |
| Customer accounts | `customer_account_menu` | link_list | `customer-account-main-menu` | **yes** — see §8 |
| Social | `social_facebook_url` | url | empty | **yes** — row suppressed while empty |
| Social | `social_instagram_url` | url | empty | **yes** |

Three structural facts about this schema:

- **The colour scheme is a `select`, not three colour pickers.** A Shopify `color` setting is unconstrained — there is no validation hook and no on-save callback, so a ratio cannot be checked at save time. The scheme is resolved in exactly one place, `snippets/css-variables.liquid`, which emits the dark-surface gold `#D8C08A` and its light-surface partner `#82672B` **together** so they cannot desynchronise. Adding a second scheme needs brand-approved values plus a measurement pass across the full contrast matrix; it is not an engineering decision.
- **`theme_documentation_url` and `theme_support_url`/`theme_support_email` are absent, not empty.** They shipped as empty strings against a `format: uri` schema, which was the theme's only Theme Check ERROR; Phase 10 removed them rather than fabricate URLs. Phase 16 records the two residual Theme Check errors as exactly these missing `theme_info` keys.
- **There is no `locales/en.default.schema.json` and no `t:` schema keys.** Merchant-facing schema strings are literal English. Converting them without shipping the schema locale file in the same change turns a non-defect into an error, so both halves were kept together and the pair is still outstanding.

---

### 6. Navigation menus

Navigation is **entirely Shopify's**. There is no hardcoded menu label anywhere in the theme — not HOME, SHOP, COLLECTIONS, OUR STORY or VERSE. The header iterates `linklists[section.settings.menu]` and reads `link.title` / `link.url`; active state comes from `link.active` with `aria-current="page"`, never hard-coded.

| Menu | Bound where | Shipped value |
|---|---|---|
| Header primary nav | `sections/header-group.json` → `header.settings.menu` | `"main-menu"` (Shopify's auto-created handle) |
| Footer link columns | `footer.liquid` `link_list` **block**, max 4 | `footer-group.json` ships `"block_order": []` — **no menu bound** |
| Account sheet | global `settings.customer_account_menu` | `customer-account-main-menu` — the menu must be created |

The footer menu is deliberately unbound: Phase 10 bound it to the auto-created `footer` handle, which printed Shopify's own admin vocabulary — "Footer menu" — as customer-facing copy on every page. A footer column falls back to the menu's own title, so the merchant's menu name *is* the column heading.

**Create in Navigation:** `main-menu` (or repoint the header setting), one menu per footer column the store wants, and `customer-account-main-menu`.

---

### 7. Filters require the Search & Discovery app

This is the single most likely thing to be mistaken for a bug after install.

`collection.filters` is empty until filters are created in **Apps › Search & Discovery › Filters**. Until then `main-collection.liquid` renders **no filter panel, no Filter button and no active-filter row**, and `component-facets.css` and `facets.js` are **not loaded at all** (`main-collection.liquid:241` — the asset tags sit inside the `has_filters` guard). A store with no filters pays nothing for the feature.

In the **Theme Editor only** a note explains why (`main-collection.liquid:330`, gated on `request.design_mode`). The live storefront says nothing.

What the theme does and does not do with filters:

- Shopify's native filtering only. No custom filter database, no second product index, no filtering logic in JavaScript.
- Controls render **exactly once** in the document. Above `--bp-md` they are a horizontal row of `<details>` dropdowns; below it, once `facets.js` adds `.facets--drawer`, the same element is a fixed drawer. One checked state, nothing to synchronise. `position: fixed` is applied **only** under that class, so the no-script path is a usable in-flow filter stack.
- Every control binds to one `<form method="get">` by the HTML `form` attribute, not by DOM nesting — which keeps the product grid outside the form. Sort and filters submit together.
- Names and values are Shopify's: `v.param_name` with Shopify's own `value`, so two boxes in one group submit the parameter twice, which is Shopify's OR encoding. The only literal parameter names in the file are `filter.v.price.gte` and `filter.v.price.lte` (`facets.liquid:173,190`), used as fallbacks and documented by Shopify.
- The form renders **no `page` parameter**, so every submission returns to page 1 — matching what Shopify's own `url_to_add` does.
- A filter group Shopify returns with a **single value is dropped**, in the snippet so every caller inherits it, and `has_filters` counts only groups the snippet would actually render.
- Nothing manipulates history. Back and Forward work because every state change is an ordinary navigation.

**A horizontal bar, not a sidebar, and the reason is arithmetic.** `snippets/grid-sizes.liquid` derives the card slot from the row left after chrome. With `chrome_d = 96`, the 1440 container gives a 1344px row and `(1344 + 32) / 304 = 4` columns. A 240px sidebar plus a 48px gap makes `chrome_d = 384`: 1056px row, **3** columns — and only **2** at the 1200px container a merchant may set. A sidebar that still paints four columns would be about 112px wide, narrower than the word "Availability".

**Shopify's own ceilings apply:** at most 25 filters per store, no filters on collections over 5,000 products, none on search results over 1,000.

**Filtering is deliberately not on `/search`.** shopify.dev states that applying filters on the search results page strips out all non-product results, and `main-search.liquid` renders a non-product group whose own help text promises the merchant that "pages and articles come back as a titled list below it." `snippets/facets.liquid` takes a generic `results` parameter so adding it is one `{% render %}`, but it must arrive with three hidden inputs — `q` (or the search is discarded), `type` (or the merchant's configured scope silently reverts to Shopify's all-types default) and `options[prefix]=last` — plus `search.sort_options`.

---

### 8. Search, and predictive search

`sections/main-search.liquid` is a real `role="search"` GET form with a labelled `q` input and three states (no query, results, zero results). It submits:

| Field | Value | Why |
|---|---|---|
| `q` | the customer's term | echoed back with `escape` in the attribute; the two `\| t` calls pass it unfiltered because translated content is escaped by default and neither key carries the `_html` suffix |
| `type` | `{{ search_types }}` from the section setting | defaults to all types without it, contradicting the merchant's own choice |
| `options[prefix]` | `last` | partial match on the final term, so a half-typed last word still matches |

`options[unavailable_products]` is deliberately not sent: its default `last` puts sold-out products after available ones, which is the order this page wants, and changing it would be a merchandising decision.

**Code-level discrepancy worth knowing before integration.** `templates/search.json` ships `"search_types": "product"` and the header search panel hardcodes `<input type="hidden" name="type" value="product">` (`header.liquid:318`). Nothing in `header.js` rewrites it. If a merchant switches the search template's *What search looks through* setting to "Products, pages and articles", the results page will honour it but a search launched from the header panel will still return products only. This is not recorded in any phase document; it is what the code does.

**Predictive search is deferred by the owner's decision, and the deferral is the deliverable.** Its value is a function of catalogue size (roughly: below 25 products, scrolling one collection is faster; above 150 it is the fastest path in the store) and nobody on this project has that number. Cost is measured: ~7 KB gzipped, about a 37% increase on the theme's entire JavaScript payload, plus a new section, snippet, stylesheet, an ARIA combobox and a third dismissable surface.

The header **panel** was built so predictive search is a drop-in rather than a rewrite — the surface, the trigger interception, focus management and Escape handling all exist. The contract it must be built to, recorded so it is not re-researched:

- Shopify's **section-rendering endpoint** (`routes.predictive_search_url` with `section_id`) — never the JSON endpoint and never a hardcoded `/search/suggest`, which is locale-prefixed on non-primary locales.
- Six stale-response guards, because no single one closes the window: 300 ms debounce, 2-character minimum, an `AbortController` per request, a captured-term comparison at resolve (because `abort()` is not synchronous), a monotonic generation counter, and a cache keyed on the normalised term.
- `resources[limit]=4` with **`limit_scope=each`** — the default `limit_scope=all` means ten results across all types.

**Unblocker: a catalogue count.**

---

### 9. Customer accounts — the platform moved, and most of the brief has no theme surface

**Legacy customer accounts were deprecated on 2026-02-26.** Five primary-sourced facts govern everything here:

1. *"Legacy customer accounts are no longer available to new stores and existing stores not using it."* — shopify.dev changelog, 2026-02-26
2. *"Theme developers should no longer include legacy customer account liquid files."* — same changelog
3. *"Publishing a theme without these templates automatically upgrades merchants to the latest customer accounts experience, which operates independently of themes."* — templates reference. **Shipping `templates/customers/*` does not make a theme safer; it withholds the merchant's upgrade.**
4. Dawn v16.0.0 (2026-08-10) deleted all seven templates *and* all seven sections.
5. The account experience is served from `shopify.com/<store-id>/account`, and its branding comes from **checkout** settings — the exact inverse of legacy, which used online-store theme settings.

**Consequences for this theme, all enforced by assertion:**

- `templates/customers/` does not exist and never has. **It must remain absent** — that absence is the auto-upgrade trigger. Eight assertions hold it: no directory, none of the seven template names, no `main-account`/`main-order`/`main-login` section, no customer `{% form %}` tag anywhere.
- Order history, order details, tracking and customer information are **not implementable in a theme**. The theme is asserted to contain no read of any `order.*` field, no `fulfillment`/`tracking_*` read, no hand-built `/account/orders/…`, `order_status_url`, `customer_order_url` or `/authenticate?key=` URL, and no `routes.account_*` link at all.
- **No authentication of any kind**: no login form, no password field, no session handling, no `customer_login` form tag, no token. Under current accounts sign-in is passwordless, so there is no password or registration step to build.

**Which system is the store on? No Liquid property can tell you.** `shop.customer_accounts_enabled` is documented as *"Returns true if the store shows a login link"* — true under both systems. `shop.customer_accounts_optional` is an unrelated checkout-policy flag. All 33–36 `shop` properties were enumerated: there is no `customer_accounts_version`. The popular forum workaround `{% if routes.account_login_url contains 'shopify.com' %}` is unsound, because `account_login_url`'s documented value is the relative `/account/login` even on stores whose `account_profile_url` is absolute. **So the theme has one code path and branches on nothing** — which is also correct because a merchant can revert an upgrade within 30 days with no signal. `shop.customer_accounts_enabled` is used exactly once, as a show/hide gate, and the suite asserts that count is one.

The entire code surface is `sections/header.liquid:216-226`:

```liquid
{%- if shop.customer_accounts_enabled and section.settings.show_account -%}
  <shopify-account
    class="header__control header__account"
    menu="{{ settings.customer_account_menu | default: 'customer-account-main-menu' }}"
  >
    <span class="header__account-avatar" slot="signed-out-avatar">
      {% render 'icon-account' %}
      <span class="visually-hidden">{{ 'header.account' | t }}</span>
    </span>
  </shopify-account>
{%- endif -%}
```

Rules around it:

- **Only three things about this element are contractual**: the published `--shopify-account-*` custom properties, `::part(signed-out-avatar)`, and the `signed-out-avatar` slot. Nothing reaches inside it with a descendant selector, because that breaks the first time Shopify ships a change.
- The 44×44 target floor comes from the shared `header__control` class, **not** from an account-specific rule. A `:not(:defined)` size reservation and all account sizing rules were measured dead and removed — the element still measured 44×44 at all seven viewports without them. Do not reintroduce them: `:not(:defined)` stops applying the instant the component upgrades, whereas an author rule on the element beats the component's own `:host` styles permanently.
- `--shopify-account-dialog-position-top` is deliberately unset. The semantics could not be settled from the docs and this theme has a sticky header a wrong guess would put the sheet underneath.
- `customer_account_menu` is a **global** `link_list`. shopify.dev's component page shows `section.settings.customer_account_menu`; Dawn v16 defines it globally. Dawn is right; copying the doc's form yields an empty `menu` attribute and a sheet with no links. **An empty value does not fall back to a default set of links — the sheet simply has none.**
- `routes.account_url` goes to the **order index**, not a profile landing page. Worth knowing before labelling anything "My account".

One open item the theme cannot resolve: **the accessible name of the account control needs one live screen-reader check.** Dawn ships the component with no label, implying Shopify names it; "implies" was not good enough for a Level A requirement, so a visually-hidden name goes in the slot. If Shopify sets its own `aria-label` it wins; if not, the control is still named.

---

### 10. Cart and checkout: Shopify owns it entirely

Verified by test on both surfaces:

- Checkout is a `<button type="submit" name="checkout">` **inside the cart form** — Shopify's own control, which applies pending quantity edits *and then* goes to checkout in one action. A plain link to `/checkout` would silently discard an edit the customer just made.
- The update submit is ordered **before** the checkout submit, because a browser submits a form with its *first* submit button when Enter is pressed in a field.
- **No checkout URL is constructed anywhere**, and `checkout_url` is never referenced.
- **No payment field of any kind exists in the theme** — no card number, no CVV, no expiry.
- **No shipping calculator and no tax calculation.** The tax sentence is *derived* from `cart.taxes_included`, not asserted, because printing "Taxes and shipping are calculated at checkout" unconditionally would be a claim about this merchant's tax configuration that nobody supplied — and wrong for any tax-inclusive market, which the Philippines is. There is no free-shipping threshold and no delivery estimate anywhere.
- `content_for_additional_checkout_buttons` renders on the **cart page only** (`main-cart.liquid:102-104`), guarded by `additional_checkout_buttons`, so accelerated checkout appears only if the store actually has it. **The drawer has no accelerated checkout** — a recorded limitation, not an oversight.
- **Shopify is the cart.** No client-side cart object, no `localStorage`, `sessionStorage`, `indexedDB` or `document.cookie` in any theme script — asserted across all files.

Cart images are sized for their slot: `image_url: width: 300` with `widths: '76, 96, 120, 152, 192, 240, 300'` and `sizes` declaring 76px in the drawer, 96px on the cart page below 768 and 120px above. No original-resolution product photography is ever requested.

---

### 11. Product data the store must supply

Nothing about products lives in the theme. There is no product name, price, currency symbol or collection handle in any Liquid file, no ranking logic, and no "choose bestseller #1" setting.

**Required before a customer can buy:**

1. **Add products.** Every price, variant, image, description, SKU and stock level comes from admin.
2. **Model the options in admin.** Colour and size are product *options*, not theme settings. The picker is built from `options_with_values` — never `product.variants`, which truncates silently at 250. The size run itself is still a business decision.
3. **Set colour swatches** — *Settings › Products › Swatches*, or per option value. A value renders as a swatch **only** when Shopify carries `value.swatch.color` or `value.swatch.image` (`product-variant-picker.liquid:56`). No colour is ever guessed from an image or a name; without swatch data the value renders as a named chip.
4. **Set each image's focal point** — *Content › Files › (image) › Edit*. This is the only crop control. The theme offers no second one, because `image_tag` writes the focal point as an inline `style="object-position: X% Y%"` that outranks every stylesheet rule. With no focal point set, Our Story defaults to `object-position: center 33%`.
5. **Set the store currency and money format** — *Settings › Store details*. Every price goes through `money`; no currency symbol is hardcoded anywhere (grep-verified).
6. **Check the peso glyph.** Jost carries neither `₱` nor `→`, so the peso falls back to a per-platform face in the most legibility-critical string on the page. Still open.

**Optional but honoured:**

- **Quantity rules** — *Products › (variant) › Quantity rules*. `min`, `max` and `increment` come from `variant.quantity_rule` and are re-applied **per variant** on every variant change, because the rule travels with the variant. Absent when the merchant has set none.
- **Low stock line** — `low_stock_threshold` on the product section, default 3, `0` disables. The comparison is server-side in Liquid behind two guards: `inventory_management == 'shopify'` **and** `inventory_policy == 'deny'` (`main-product.liquid:89`). Only a boolean reaches the page — `inventory_quantity` is never rendered, and `{{ product.variants | json }}` is never emitted because it would publish stock levels into the page source.
- **Accelerated checkout** — *Settings › Payments*.
- **Publish the policies** — *Settings › Policies*. The footer iterates `shop.policies` and tests **per policy** (`footer.liquid:286-287`), so an unpublished policy produces no link rather than a link to an empty page.

Collections are a real `collection` picker setting on `featured-collection`, served through two presets (New Drop, Best Sellers) from one section file. Both ship **with no collection handle at all**, so both home rows render nothing — no markup and no stylesheet requests either — until a merchant picks one. `products_per_page` on the collection template is 24; `results_per_page` on search is 24.

---

### 12. What a theme cannot do

This is the part most likely to be assumed away.

**A theme cannot publish Shopify standard events.** Quoted from shopify.dev, Web Pixels API: *"To ensure the quality of standard events, partners and merchants cannot publish standard events. `Shopify.analytics.publish` only exposes the method to publish custom events."* Every event a marketing brief asks for — `view_item`, `add_to_cart`, `begin_checkout`, `purchase` — is emitted by **Shopify**, from a sandbox the theme cannot reach, in response to storefront calls the theme already makes.

Shopify emits **exactly 15** standard events:

```
page_viewed   product_viewed   collection_viewed   search_submitted
product_added_to_cart   product_removed_from_cart   cart_viewed
checkout_started   checkout_contact_info_submitted
checkout_address_info_submitted   checkout_shipping_info_submitted
payment_info_submitted   checkout_completed   alert_displayed
ui_extension_errored
```

There is **no `cart_updated`, no `cart_created`, no `variant_viewed`**. Bulk subscription is via `all_events`, `all_standard_events`, `all_custom_events`, `all_dom_events`. Five DOM events exist on the storefront — `clicked`, `form_submitted`, `input_blurred`, `input_changed`, `input_focused` — and are **not** available on customer-account pages or the order-status page.

Also out of reach:

| Cannot | Why |
|---|---|
| Fire a `purchase` event | `checkout_completed` belongs to Shopify. Post-purchase offers move it to the first upsell page; *"if the page where the event is supposed to be triggered fails to load, then the `checkout_completed` event isn't triggered"* — so under-counting is possible and over-counting is what Shopify prevents. Refreshing the thank-you page does not re-fire it. |
| Maintain a `dataLayer` | App pixels run in a **strict web-worker sandbox** (no `window`, no `document`); custom pixels run in a lax sandboxed iframe. A `window.dataLayer` is unreachable from either. Shopify also prohibits DOM scraping for events, metadata and user info. |
| Add a `gtag`/`fbq`/TikTok snippet | *"Code snippets can be used to bypass customer consent requirements, which violates the Shopify Terms of Service and can lead to legal liability for you."* — Shopify Help Center |
| Set any HTTP response header | A Liquid theme cannot. The widely-repeated `Cache-Control` advice for customer routes is Hydrogen/Oxygen guidance with no Liquid counterpart. |
| Style the customer-account pages | Different origin, branded from *checkout* settings. The design tokens do not reach them and hiding built-in elements there is explicitly unsupported. |
| Detect which account system is active | §9. No property exists. |
| Treat the order-status URL as secret | *"The unauthenticated Order status page can be accessed by anyone who has a direct link."* It redacts PII rather than blocking access. |

The theme publishes **no** custom events either, because it needs none, and three prohibitions are enforced by the test suite rather than by good intentions: no analytics `<script>` in any Liquid file; no call to `customerPrivacy.setTrackingConsent()` (consent must never be given automatically on a visitor's behalf); and nothing reading the six retired cookies.

**The one escape hatch, stated narrowly:** if `product_added_to_cart` turns out not to fire for an Ajax add (undocumented — see §15), the fix is a custom pixel subscribing to a **custom** event the theme publishes via `Shopify.analytics.publish` with an app prefix. That is the single circumstance in which this theme should ever contain analytics code.

---

### 13. Platform deadlines and deprecations

**Every date below is in the past as of 2026-09-25.** Any tutorial that tells you to paste a purchase tag into Additional Scripts, or to read `_landing_page` from `document.cookie`, describes a storefront that no longer exists.

| Mechanism | Status |
|---|---|
| `checkout.liquid` (Information, Shipping, Payment steps) | unsupported |
| `checkout.liquid` + **Additional Scripts** (Thank you, Order status) | **sunset 2025-08-28** |
| Script tags, Shopify Plus | **sunset 2025-08-28** |
| Script tags, non-Plus | sunset 2026-08-26 |
| `_landing_page`, `_orig_referrer`, `_tracking_consent` cookies | **removed 2025-09-15** |
| `_shopify_s`, `_shopify_y` cookies | **removed 2026-01-01** |
| Legacy customer accounts | **deprecated 2026-02-26** |
| Dawn removed all legacy customer templates + sections | v16.0.0, **2026-08-10** |

The theme is asserted to read none of the six retired cookies.

**Shopify's own cookie policy page is stale and still lists the removed cookies.** The developer changelog is the source that is correct. Follow the changelog, not the help-centre cookie page.

---

### 14. Attribution: what the theme's GET forms do to UTM parameters

Measured, real, and deliberately not changed. All three GET forms discard campaign parameters, by the same mechanism Phase 13 relied on to drop the `page` parameter — a GET form discards its action's query string and rebuilds it from its own fields:

```
landing   ?utm_source=facebook&utm_medium=paid_social&utm_campaign=drop_01
sort   →  ?sort_by=price-ascending
filter →  ?filter.v.price.gte=&filter.v.price.lte=&sort_by=manual
search →  ?q=tee&type=product
```

**This is harmless and "fixing" it would be worse.** Shopify records `landingPage` and `utmParameters` **server-side at the session's first request**. GA4 fixes session source at session start and does not open a new session on a mid-session source change — Universal Analytics did the opposite, which would have made these forms genuinely destructive, and reasoning from UA intuition here is the stale-platform-assumption class that has cost this project phases. Meta has already written `fbclid` into `_fbc` with a 90-day life. Dawn behaves identically. Carrying UTM through internal forms would make internal navigation look like campaign traffic and create self-referrals.

The one genuine loss is narrow: land with UTM → sort → idle past the 30-minute session timeout → re-enter from the now-stripped URL. That second session is attributed to direct.

**A reserved-parameter guard is in force.** Shopify special-cases `ref`, `source` and `r` storefront-wide as the marketing referral code, and the value lands in every order's conversion detail. A theme form field with one of those names would silently overwrite real attribution. The theme submits exactly `add`, `checkout`, `description`, `id`, `note`, `options[prefix]`, `q`, `quantity`, `sort_by`, `type`, `update`, `viewport` — none reserved, and asserted.

Campaign conventions, for whoever tags the links (no campaign was created): lowercase everywhere, because GA4 is case-sensitive and `Facebook`/`facebook` become two sources; underscores not spaces; never tag an internal link; `utm_campaign = {objective}_{subject}_{yymm}`; ad-platform campaigns `{platform}_{objective}_{subject}_{audience}_{creative}_{yymm}`.

---

### 15. Apps: what to install, and what not to

| App | Why | Rule |
|---|---|---|
| **Search & Discovery** | The only app the storefront *depends on*. Populates `collection.filters` server-side; adds **no storefront script**. | Install and configure filters before launch or filtering is invisible. |
| **Google & YouTube** | Registers its own pixel; Google Ads conversion tracking shares its purchase signal. | **Do not** also paste a `gtag` or `AW-` tag anywhere. |
| **Facebook & Instagram** | Registers an app pixel and handles the Conversions API server-side. | **Do not** add a second `fbq` — a duplicated pixel double-counts every event including purchases. |
| **TikTok** | Registers its own pixel. | One pixel; the app owns it. |
| Abandoned cart | Shopify-native (*Settings › Notifications*, timing in *Settings › Checkout*). | **Do not build one.** |
| Email (Shopify Email / Klaviyo / Mailchimp) | Integrates as an app. The theme has no newsletter form. | Whether the footer gets one is still a business decision. |

**Install at most one app per platform.** The theme currently carries zero third-party code and `content_for_header` is untouched, so Theme Check's `ContentForHeaderModification` passes and none of the duplicate-tracking hazards can occur — a state that survives only if nothing is pasted in.

Two measured facts about how the theme drives Shopify's events:

- Shopify-call counts per customer action, measured in a browser: variant select **0**, quantity press **0** (debounced to one request), add **1**, drawer open **0**, drawer reopen **0**, line increase **1**, removal **1**. Opening the drawer makes no call because it is rendered with the page and shown, never fetched — a drawer that fetched on open would make Shopify emit a cart event every time.
- `cart_viewed` will fire rarely, because the cart is drawer-first and that event is `/cart`-page only. That is a design consequence, not a defect.
- **Whether `product_added_to_cart` fires for an Ajax `/cart/add.js` is undocumented.** Recorded as an unknown. One add to cart with the pixel debugger open settles it, and Phase 17 calls this the highest-value fifteen minutes in the whole analytics review.

---

### 16. Templates Shopify can route to that this theme does not have

Each serves Shopify's error page to anyone who reaches its URL:

`article` · `blog` · `gift_card` · `list-collections` · `password`

None is referenced by anything the theme renders, so none was built speculatively. `templates/customers/*` is a separate case and must stay absent (§9). The recommendation on record is to treat the five as their own small phase.

---

### 17. Theme Check and the CLI

**The Shopify CLI has never been present in this environment, so Theme Check has never run against a real store.** Phase 16 did run `@shopify/theme-check-node` locally and found the Phase 10 runner had been pointed at the *project* root, which stopped being the theme root the moment Phase 10 moved the theme into `god-squad-theme/` — it had been scanning a directory with no theme in it and reporting zero offenses. **Run it against `god-squad-theme/`, not the project root.**

Result at the correct root — 49 files scanned, 84 checks:

| Config | Before | After | Residual |
|---|---|---|---|
| default | 4 offenses | **2** | 2 × ERROR `ValidJSON` |
| `theme-check:all` | 7 offenses | **5** | plus 3 × ERROR `AssetSizeJavaScript` |

- The two `ValidJSON` errors are **business information, not code**: `theme_support_email` and `theme_documentation_url` missing from `theme_info`. Supply them and the default config is clean.
- `AssetSizeJavaScript` flags three script tags against a 10,000-byte compressed threshold. `cart.js` at **12,073 B gz** is genuinely over it. Comments-stripped it is 4,930 B, so the threshold is not reachable by deleting prose. Recommended, not done: a **minification step at deploy**. Restructuring tested cart code with import-on-interaction is the wrong response to a theme whose total JavaScript is 24 KB gzipped with no dependencies.

The theme's own performance budget, set from its measured numbers rather than round figures, is the acceptance bar for anything added during integration:

| Budget | Current worst | Target |
|---|---:|---|
| JavaScript, all pages | 22.0 KB gz | ≤ 30 KB gz |
| JavaScript, per page-load script | 12.1 KB gz | ≤ 10 KB gz (Shopify's own threshold) |
| CSS, worst page | 55.1 KB gz (homepage) | ≤ 55 KB gz |
| Requests, worst page | 26 (homepage) | ≤ 30 |
| Load CLS | 0.0125 | ≤ 0.05 |
| Theme handler time | 0.00 ms | ≤ 50 ms |
| Eager images per page | 1 | exactly 1 |
| `fetchpriority="high"` per page | 1 | ≤ 1 |
| Third-party scripts | 0 | each one justified in writing |

---

### 18. The consolidated pre-launch Admin checklist

Carried forward and still outstanding across Phases 13–18. None of it is a code task, and the theme is correct without it — it simply renders nothing where the data is absent.

| # | Action | Where | Consequence if skipped |
|---|---|---|---|
| 1 | Confirm which customer-account system the store uses | *Settings › Customer accounts* | Determines whether items 2–4 apply at all. **Do this first.** |
| 2 | Create the account menu, handle `customer-account-main-menu`, then select it | *Navigation › Add menu*, then *Theme settings › Customer accounts* | The account sheet opens with no links |
| 3 | Brand the account pages | *Settings › Checkout › Customize* | Account pages will not look like the store; the theme cannot reach them |
| 4 | Optionally connect an account subdomain | Domains | Account pages stay on `shopify.com/<store-id>/account` |
| 5 | Create filters | *Apps › Search & Discovery › Filters* | No filter UI renders at all; `facets.js`/`component-facets.css` never load |
| 6 | Brand the checkout | *Settings › Checkout › Branding* | Checkout does not match the store |
| 7 | Configure shipping rates | *Settings › Shipping and delivery* | Checkout cannot quote |
| 8 | Configure taxes | *Settings › Taxes and duties* | Drives `cart.taxes_included`, which chooses the cart's tax sentence |
| 9 | Enable accelerated checkout (optional) | *Settings › Payments* | Dynamic checkout buttons absent from the cart page |
| 10 | Publish the policies | *Settings › Policies* | Footer policy links absent; no purchase surface can link them |
| 11 | Create `main-menu` and the footer menus | *Navigation* | Header nav empty; footer has no link columns |
| 12 | Add products, options, swatches, focal points, currency + money format | *Products*, *Settings › Products*, *Content › Files*, *Settings › Store details* | Home rows, collection, search and product page render nothing or render wrong |
| 13 | Upload logo, favicon and a ~1200×630 social sharing image | *Theme settings › Brand* | Header falls back to text; browsers show a default icon; shared links fall back to the logo, which crops badly |
| 14 | Supply the two Facebook / Instagram profile URLs | *Theme settings › Social* | Footer social row is suppressed entirely |
| 15 | Decide the hero CTA destination and the empty-cart / 404 destination | Theme Editor | Both fall back to the home page, which as shipped has no product link. `/collections/all` is servable now. |
| 16 | Supply `theme_support_email` and `theme_documentation_url` | `config/settings_schema.json` | Two Theme Check ERRORs remain |
| 17 | Install at most one channel app per platform | *Apps* | No pixel; or, if duplicated, double-counted purchases |
| 18 | Check customer privacy state and configured regions; confirm whether Network Intelligence is on | *Settings › Customer privacy* | Consent banner state unknown; if Network Intelligence is on, Shopify's Consumer Privacy Policy should be linked from the store's own privacy page (ordinary page content, no theme code) |
| 19 | Take Philippine RA 10173 / NPC applicability to counsel | — | Shopify publishes no APAC-specific consent guidance; this is a legal question |
| 20 | Verify `product_added_to_cart` fires on an Ajax add, with the pixel debugger open | Live store | The one undocumented event in the funnel |
| 21 | Back or remove the "Worldwide Shipping" announcement-bar claim | `sections/header-group.json` ships it as `message-2` | It is the store's only unsupported commercial claim and there is no shipping policy, destination list or rate table behind it |
| 22 | Run Theme Check against `god-squad-theme/` on a development store | Shopify CLI | 5 known offenses; anything else is new |

**Do not paste any tag into the theme or into Additional Scripts.** Additional Scripts was sunset 2025-08-28.

---

### 19. What is unverified, and must be checked on the real store first

Stated plainly because none of it was measurable offline:

- Section Rendering API responses, including the wrapper shape `cart.js` depends on.
- Real `content_for_header` output — and therefore `window.Shopify.routes.root` actually being present.
- Real image-CDN behaviour: WebP auto-conversion, the no-upscale rule, and `image_tag`'s `srcset` output.
- `paginate.parts` URLs. The harness models pagination links as `?page=N`; on a real store Shopify supplies its own.
- The accessible name `<shopify-account>` gives its control (§9).
- `| t` escaping of *interpolated variables*. shopify.dev states translated content is escaped by default with `_html` as the only opt-out, and no locale key in this theme carries that suffix — so the two `| t` calls echoing `search.terms` are safe under the documented rule, but the docs do not explicitly address interpolated variables.
- Whether `product_added_to_cart` fires for an Ajax add (§15).
- Safari. All browser testing was Chromium — Edge 153 and Chrome, both green, 0 console errors across 38 pages. No real device was ever tested.
- Lighthouse and field Core Web Vitals. **No Lighthouse score appears anywhere in this project**, because inventing one was forbidden and there was nothing to report. TTFB, FCP and field LCP/INP are reported as unavailable, not estimated.

---

## The store-setup runbook

The order of operations for connecting this theme to a real Shopify store. §9 states the platform facts; this is the sequence, and it exists because a correctly-built surface in this theme renders **nothing** when its data is absent — which is the failure an integrator hits first and diagnoses last.

Every requirement below is quoted from the theme's own schema strings or derived from a setting that ships with no default. None of it is general Shopify advice.

### Stage 0 — before the theme goes anywhere

| Do this | Why |
|---|---|
| Put the project under version control | There is no `git` repository. Phase 1 logged it as DEBT-12/DEBT-13 and recommended fixing it before Phase 2; nineteen phases later it is still a plain OneDrive folder. Do this before anything starts changing against a live store |
| Preserve the QA suite | 228 Python files and the only Theme Check runner live in a session temp directory, not in the project. When it is cleared, every measured claim in every phase document stops being reproducible |
| Decide the customer-accounts mode | `templates/customers/` is **deliberately absent** — that absence is Shopify's auto-upgrade trigger for new customer accounts, and the header uses `<shopify-account>`. Do not add legacy customer templates back |
| Fill two theme properties | `theme_support_email` and `theme_documentation_url` are the only two Theme Check offences outstanding. They are business information, not code |

### Stage 1 — upload

There is **no Shopify CLI in this project** and the theme has never been uploaded. Zip `god-squad-theme/` and upload it through Shopify admin → Online Store → Themes → Add theme → Upload zip. Do **not** publish it yet.

Expect, on first preview: every image slot empty, the hero without a photograph, the featured-collection band absent, no footer menus, and the filter UI missing. All of that is correct for a store with no data. Stages 2–6 fill it.

### Stage 2 — brand and global settings

Theme settings → Brand. These are the settings that ship with **no default**, so nothing renders until each is filled:

| Setting | Consequence while empty |
|---|---|
| `logo` | The wordmark falls back to text. The current raster wordmark carries heavy transparent padding and renders at roughly half its intended size — **upload a vector master**, not the existing PNG |
| `favicon` | Browsers show their own default mark. None exists in the project |
| `share_image` | Social shares have no image card |
| `social_facebook_url`, `social_instagram_url` | "Each icon appears once its address is filled in, and none is shown otherwise." Add only accounts that actually exist |

Also confirm the two font families resolve in Shopify's library. The theme loads exactly two — Playfair Display 900 and Jost 400/500/600, the latter with 500 and 600 registered through `font_modify`. There is no third font: the design names a script accent, but nothing in the theme consumes it.

### Stage 3 — navigation

The theme ships **no menus of its own** and reads the merchant's.

1. Build the main menu in **Navigation**. The header renders it directly; below `--bp-lg` it is the *only* navigation, through the mobile panel.
2. Build the footer menus. `footer.liquid`'s `menu` setting is a `link_list` with no default, and its own schema warns: *"The theme ships no footer menu of its own, and a column with no links does not render on the live store."* Each footer column needs its own menu selected.

### Stage 4 — pages and policies

Two buttons in the theme are **hidden until a destination exists**, deliberately, so they never render as dead links:

| Control | Requirement |
|---|---|
| Our Story button (`our-story.liquid` → `button_url`) | *"No Our Story page exists in this project yet… Create the page in Shopify admin first, then select it here."* |
| Hero button (`hero.liquid` → `button_link`) | *"The button is hidden until this points somewhere. No destination has been supplied for the collection yet."* Point it at the collection you want the hero to sell |

Publish the store policies as well — the footer renders whichever ones exist.

### Stage 5 — the catalogue

Nothing about products is in the theme; Shopify is the source of truth for every product, price, variant, image and stock level.

1. **Create products with real names.** Not a formality: a wrapped product name in the cart exposed a live typography defect in Phase 18 that the short invented fixture names had hidden completely. Long names, real descriptions and real image aspect ratios are what will surface the next one.
2. **Create the collection the homepage points at.** `featured-collection.liquid`'s own schema is explicit: *"Products, prices, images and availability all come from this collection. Nothing is set in the theme. Until a collection is chosen the section does not render on the live store."*
3. **Configure option-value swatches.** Swatch rendering appears in six files (product cards, facets, the variant picker). Colour swatches read Shopify's option-value swatch data; without it the colour name still shows — the mark is never the only carrier — but the swatch does not.
4. **Turn on inventory tracking.** The low-stock line and the sold-out states read real inventory. `low_stock_threshold` is **3**, set in both `templates/product.json` and the schema default.
5. Choose the product image ratio (`product_image_ratio`) — one ratio governs the whole catalogue.

### Stage 6 — the one app dependency

**Install Shopify's Search & Discovery app and create at least one filter.** Until you do, the collection page's filter UI does not exist, whatever the theme setting says. The theme states it plainly: *"Filters are created in Shopify admin under Apps › Search & Discovery › Filters. Until at least one exists, nothing is shown here whatever this is set to."*

This is the only app the theme depends on.

### Stage 7 — payments, checkout and markets

| Item | Note |
|---|---|
| Wallets | `payment_button` is rendered on the product page and the cart page. Enabling Shop Pay / Apple Pay / Google Pay makes the accelerated buttons appear. Their internals are Shopify's markup — the theme styles the container only and cannot restyle the button |
| Currency and money format | Every price runs through the `money` filter; the format is a store setting |
| Markets / multiple languages | `cart.js` builds every Ajax URL from `window.Shopify.routes.root` precisely so a locale-prefixed store keeps working. If you enable Markets, re-test add-to-cart first — a hardcoded path would have 404'd silently, and this is the guard against it |

### Stage 8 — the five things only a real store can verify

The theme was built and measured entirely offline. These five were explicitly **not** verifiable and should be the first smoke test after upload:

1. **Section Rendering API responses** — the Ajax cart applies returned sections; only a live store returns real ones.
2. **Real `content_for_header` output** — emitted once, unmodified, at `layout/theme.liquid:127`. Everything the theme gets from the platform arrives through it.
3. **Image CDN behaviour** — `image_url` / `image_tag` widths, formats and focal-point crops against real uploads.
4. **`paginate.parts` URLs** — the shared paginator builds its links from them.
5. **Theme Check against a live store** — the offline run reports two business-information offences; a live run can see more.

Add one more to that list: **open the Theme Editor and click through every section's settings.** Phase 11 found that a purely cosmetic toggle had broken the purchase flow, and editor defects only surface in the editor's own section lifecycle.

### Stage 9 — what will still look empty, and why that is correct

| Surface | Renders nothing until |
|---|---|
| Hero photograph | an image is uploaded (Stage 2/4) |
| Featured collection band | a collection is chosen (Stage 5) |
| Collection filters | Search & Discovery has a filter (Stage 6) |
| Footer columns | each has a menu (Stage 3) |
| Footer social icons | each address is filled (Stage 2) |
| Hero and Our Story buttons | each has a destination (Stage 4) |
| Announcement-bar icon and link | filled, both optional |
| Accelerated checkout buttons | wallets are enabled (Stage 7) |

None of these is a bug. The theme was built so that absent merchant data renders nothing rather than rendering a placeholder, a dead link or an invented value — which is the same rule that kept fake products, fake reviews and fake claims out of it for nineteen phases.

---

## Accessibility posture

### The standard, and where it is written down

The acceptance bar for the whole programme is **WCAG 2.2 Level AA**, fixed in `PHASE-2-DESIGN-SYSTEM.md` §24 ("The acceptance bar is **WCAG 2.2 Level AA**") and never revised. Every later phase measured against it on rendered output rather than asserting it from source. The theme root is `C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme`; all paths below are relative to it.

Accessibility is not concentrated in one file. It is carried by four mechanisms you need to know before changing anything:

| Mechanism | Lives in | What it guarantees |
|---|---|---|
| Surface classes `.surface-dark` / `.surface-light` | `assets/design-tokens.css:466-490` | reassign `--focus-ring`, `--accent-current`, `--color-text-current-muted`, `--color-border-current-interactive` so a component cannot pick an illegal colour |
| One global focus rule | `assets/base.css:58` | `:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible` — zero specificity, so components can override intentionally |
| One global motion suppression | `assets/base.css:71-78` plus `assets/design-tokens.css:506-513` | the only four `!important` declarations in the theme |
| Two target-size tokens | `assets/design-tokens.css:364-365` | `--target-min: 44px`, `--target-min-aa: 24px` |

Phase 1 originally assigned "an axe pass and a full keyboard audit" to a dedicated *Phase 14 — Accessibility*. The roadmap was re-ordered; Phase 14 became cart and checkout and **no dedicated accessibility phase ever ran**. Accessibility was instead delivered per-surface (Phases 4–15) and audited as one of ten dimensions in Phase 16. See *What was never tested* at the end — that reassignment is why axe, a screen reader and forced-colors mode are still unrun.

### The AA-versus-AAA calls, made deliberately

The theme is held to AA and in most places lands well above it. Three calls are explicit and should not be "harmonised" later:

1. **Target size: 44px is the design goal, 24px is the conformance floor.** `--target-min` 44px corresponds to SC 2.5.5 (AAA) and the Apple/Google platform guidance; `--target-min-aa` 24px is SC 2.5.8 (AA), the level the theme is actually held to. Phase 2 §24.2 rule 4: *"Targets are not reduced at any breakpoint. If a row cannot hold four 44px targets at 375px, an item moves into the menu panel — it is not shrunk."*
2. **Text contrast is usually AAA but only AA is required.** Most roles measure 9–17:1. Two roles are deliberately AA-only and must not be "improved" into a different colour: `--color-accent-strong` `#82672B` at **4.66:1** on cream (the light-surface accent, e.g. the Our Story eyebrow) and `--color-text-inverse-muted` `#5F5A50` at **5.97:1** on cream (body copy and the compare-at price).
3. **Two controls sit at the 24px AA floor rather than 44px**, each with a written justification (below).

Everything else meets 44px. Phase 9 enumerated every interactive element at twelve viewports across every page: **zero elements below 24px anywhere**, and exactly one between 24 and 44.

### Contrast

**The one prohibition that governs the palette.** Muted gold `--gs-gold` `#D8C08A` measures **1.55:1** on warm cream `#F3EFE6` and **1.43:1** on the product-tile cream `#EBE6DC`. Gold is a **dark-surface accent only** — never text, icon, border or focus ring on a light surface. On light surfaces the accent role is `--color-accent-strong` `#82672B` (4.66:1). This is enforced structurally: `.surface-light` reassigns `--accent-current` and `--focus-ring`, so a component that reads the `-current` names cannot produce the illegal pairing. Also prohibited: stone `#BDB6A8` on cream (**1.76:1**) — use `--color-text-inverse-muted` instead.

**Verified pairings** (the register; a pairing absent from it is unverified and may not be used):

| Pairing | Ratio |
|---|---:|
| cream `#F3EFE6` on ink `#0D0C0A`, and the reverse | 17.04:1 |
| gold `#D8C08A` on ink | 11.01:1 |
| `--gs-cream-200` `#E9E4D8` on ink | 15.41:1 |
| stone `#BDB6A8` on ink | 9.70:1 |
| gold hover `#E6D3A6` on ink | 13.25:1 |
| `#82672B` on cream | 4.66:1 |
| `#5F5A50` on cream | 5.97:1 |
| olive `#4B5443` on cream | 6.91:1 |

**Non-text contrast (SC 1.4.11) needs its own tokens.** The four decorative border tokens composite to 1.17–1.35:1, which is right for a hairline rule and fails a control boundary. Form fields, checkboxes, radios, selects and outlined buttons therefore use `--color-border-interactive` `rgba(243,239,230,0.36)` = **3.02:1 on ink** and `--color-border-interactive-inverse` `rgba(13,12,10,0.46)` = **3.13:1 on cream**, reached through `--color-border-current-interactive`. A control that uses `--color-border-current` for its boundary is a defect.

**Text over photography is measured composited, at its worst pixel — not against the scrim's nominal value.** This is the single most consequential contrast finding in the project. Phase 1 measured three nav links at **2.4–2.9:1** over the hero sky. Phase 2 answered with a `--scrim-header` token; **Phase 4 measured that token against the real hero and found it insufficient** — the brightest pixels behind the links sat at 1.1–1.7:1, *worse than the prototype*, because the ramp had already faded by the time it reached the link band. The required alpha is arithmetic: for cream to reach 4.5:1 over a worst-case near-white sky the ink layer must hold **≥0.85 alpha**. The shipped token (`assets/design-tokens.css:131`) holds ~0.86 through the entire header and fades only below it, via a companion `--scrim-header-overhang: 4rem` so the fade happens outside the content band:

| Nav-band backing | Median | p90 | p98 | Worst pixel |
|---|---:|---:|---:|---:|
| No scrim (Phase 1 condition) | 4.11:1 | 1.43:1 | 1.39:1 | 1.09:1 |
| Phase 2 scrim as specified | 6.11:1 | 1.73:1 | 1.43:1 | 1.11:1 |
| **Phase 4 scrim as shipped** | 17.38:1 | 14.82:1 | 14.55:1 | **13.61:1** |

The same rule produced the hero's scrim: with the wash removed, the worst backdrop pixel behind all four hero text elements carries cream at **1.00:1**. The wash is not stylistic — without it the hero has no readable text. The `None` overlay option is retained but is documented as unsafe and only for an image already dark where the words sit. Consequence for anyone changing hero art: **re-measure per image.** A scrim is always a child of the media wrapper and sized to the media, never to the section, and the header scrim is never anchored to the hero section.

**Measurement counts, by surface.** Hero: 40 measurements across eight widths (worst body-size figure 11.98:1, worst heading 8.18:1 on the gold accent). Collections: 14 text roles, verified twice — computed from tokens *and* sampled from rendered pixels. Our Story: 48 pixel-sampled measurements through the actual photograph and scrim (page captured twice, once with text hidden, reporting both the worst glyph pixel and the worst pixel in the bounding box) across two surfaces and four widths. Product and cart: 55 rows, product page and cart composited from computed styles because those surfaces are flat. The **standing theme-wide suite is 73 measurements (`contrast8`), 73 passing**, re-run unchanged in Phases 14, 15, 16 and 18.

### Target sizes

Rules, all from Phase 2 §24.2 and still current:

- Every interactive element has a hit area of at least 44 × 44 regardless of how small its visible mark is. A 16px swatch dot gets a 44px box.
- Adjacent targets are separated by at least `--space-2` (8px), or their hit boxes are enlarged until they are.
- An icon-only control is a box with a glyph centred in it, never a bare glyph. `.header__control` sets `min-width` and `min-height` to `--target-min` (`assets/header.css:248-254`) — this is what gives the `<shopify-account>` custom element its 44 × 44 floor, since an author rule on the element beats the component's own `:host` styles.
- Targets are never reduced at any breakpoint, and the header is never reduced in landscape: it keeps its full 88px height and every control.

**The two deliberate 24px controls**, both recorded so nobody re-derives the reasoning:

| Control | Size | Why it stays |
|---|---|---|
| `.cart-line__title` (`assets/component-cart-line.css:72`) | 230×24 to 202×28 | a text link inside a list, not a primary control; meets the 24px AA minimum; the 76px thumbnail beside it is an equivalent pointer target to the same product. Growing it to 44px would add 20px per line to a drawer that fought for 100px of landscape scroller. Phase 18 keeps it **flagged UNDER-44** rather than silently passing it |
| `.facets-active__chip` (`assets/component-facets.css:289`) | 24px floor | removal is also reachable from the filter group the value came from, which is SC 2.5.8's equivalent-control exception. **Filter values themselves are 44px** (`:149`) because there is no larger equivalent beside them |

Note the code comment on `.cart-line__title` argues *"neither exception rescues this one"* for the **24px floor** — that is why the box exists at all (the text is 14px). The thumbnail argument is the separate reason it is not grown to 44px. Both are true; do not conflate them.

Two targets were corrected in Phase 9: the skip link (38 → 44px, `assets/header.css:26-46`) and the five mobile menu links, which were *focusable while invisible* — the most severe form of target failure.

### Focus management

**The ring.** 2px solid at 2px offset (`--focus-width`, `--focus-offset`), applied through `:focus-visible` so pointer users never see it and keyboard users always do. `--focus-ring` defaults to `--focus-ring-on-dark` (gold, 11.01:1 on ink) and is reassigned to `--focus-ring-on-light` (ink, 17.04:1 on cream) by `.surface-light`. A component **never chooses its ring**. `outline: none` / `outline: 0` is prohibited unless the same block substitutes an equally visible indicator; there is no global outline removal anywhere in the theme.

One doc/code drift worth knowing: several comments (e.g. `assets/component-quantity.css:116`, `assets/component-button.css:31`) say the global ring lives in "the token file". **The code is the truth: it is `assets/base.css:58`**, moved there by the Phase 10 stylesheet split. `design-tokens.css` owns only the ring's tokens.

**Three surfaces, three different correct answers**, each with the failure it avoids written into the file:

| Pattern | File | Failure avoided |
|---|---|---|
| `.product-card:has(.product-card__link:focus-visible)` with the anchor's own `:focus-visible` outline suppressed, plus an `@supports not selector(:has(*))` → `:focus-within` fallback | `assets/component-product-card.css:122-145` | the ring being drawn around the anchor's box instead of the whole card. The two rules are mutually exclusive by construction; an engine too old for `@supports selector()` gets neither and falls back to the browser default, which is why the suppression uses `:focus-visible` not `:focus` |
| `.quantity:has(.quantity__input:focus-visible)` — **`:has()`, not `:focus-within`** | `assets/component-quantity.css:114-126` | `:focus-within` matched when *any* descendant held focus, painting two concentric rings when you tabbed to the minus button |
| Ring drawn on the `<label>`, radio carries `.visually-hidden` | `snippets/product-variant-picker.liquid`, `snippets/facets.liquid` | a visually-hidden radio is still focusable, so the ring must be on the thing you can see. Both reuse the shared `.visually-hidden` utility (`assets/header.css:13`) rather than re-declaring the clip/clip-path pair |

**Focus destinations, in every cart path** (Phase 8, refined in 14 and 16):

| Event | Focus goes to |
|---|---|
| Drawer opens | the drawer **heading** (`tabindex="-1"`), not the close button — "Close, button" says nothing about what just happened |
| Escape / overlay click / close button | whatever opened it, checked with `document.contains()` first — focusing a detached node silently drops focus to `<body>`; otherwise the header cart control |
| A cart line is updated | the equivalent control in the freshly rendered line, preferring the line's own quantity input |
| A cart line is removed | that surface's own heading — the drawer's `h2` or the cart page's `h1`. **This is why both headings sit outside the node the section render replaces** |
| Add to cart, start to finish | stays on the add button |
| Note field saved across a swap | back to the field, not the heading |

**Focused elements are never disabled.** `aria-busy="true"` is the busy state and the double-submit guard reads it (`assets/cart.js:526-544, 590`). Disabling the element that holds focus blurs it, and re-enabling can re-enable a button for a variant that can no longer be bought.

**Phase 16 fixed a subtle focus-recovery bug worth repeating:** the last-resort focus sweep after a section swap could land on `.cart-line__media-link`, which carries `tabindex="-1" aria-hidden="true"` precisely so it is *not* a stop. The sweep now excludes `[aria-hidden="true"]`.

**Focus not obscured (SC 2.4.11).** The drawer's footer is pinned *below* the scroller, not over it, and the scroller carries `scroll-padding-block-end: var(--space-6)`. The sticky product buying column and the sticky cart summary both carry `scroll-padding-block` and their own `max-height` plus scroll. In Our Story the scrim and caption backing are `pointer-events: none` and sit behind the content layer.

**Skip link.** First focusable element in `layout/theme.liquid:195`, `href="#MainContent"` targeting `<main id="MainContent" tabindex="-1">`. Styled at `assets/header.css:26-50`: `min-height: var(--target-min)`, `z-index: var(--z-toast)`, hidden with `transform: translateY(-200%)` and revealed on `:focus` — not with `display: none`, which would make it unfocusable.

**A related pattern worth copying:** the drawer's no-JS Update button is `.visually-hidden .visually-hidden--until-focus` (`sections/cart-drawer.liquid:159`, styles at `assets/section-cart-drawer.css:263`) — it occupies no space until a keyboard reaches it, then becomes a real visible 44px button. *"A control that is permanently invisible but focusable is worse than no control."* Once `assets/cart.js` runs it is removed from the document entirely, keyed on the `cart-js` class the cart script sets **on itself** — never the layout's `js` class, which an inline script sets whether or not the cart script arrives.

### Scroll lock: two mechanisms, and which one to use

This is a live composition hazard. There are two locks in the theme and they are not interchangeable:

| Owner | Mechanism | Where |
|---|---|---|
| Mobile menu panel | class on `<html>` → `.menu-open body { overflow: hidden }` | `assets/header.js:66`, `assets/header.css:573` |
| Filter drawer | class on `<html>` → `.facets-open body { overflow: hidden }` | `assets/facets.js:157`, `assets/component-facets.css:466` |
| Cart drawer | `body.style.position = 'fixed'` + `top: -scrollY`, restored with `window.scrollTo()` on close | `assets/cart.js:500-516` |

**The class-based locks compose; the cart's does not.** Two owners each recording and restoring a scroll position fight over one value. Phase 13 therefore made the filter drawer follow the header, not the cart, and asserts it in the test suite against the code *with comments stripped*. **Any new overlay uses a class.** The cart's `position: fixed` lock is correct for the cart and is left alone.

### `inert`, dialogs and live regions

**`inert`, not `aria-hidden`.** `aria-hidden` leaves content focusable while removing it from the accessibility tree, stranding a screen reader on an element it cannot describe. `inert` handles focus, pointer input, find-in-page and the tree in one attribute. `SUPPORTS_INERT` is feature-detected (`assets/cart.js:100`); where it is unavailable a minimal Tab-cycling trap takes over, and **never alongside it**.

**The drawer's own section wrapper is excluded by `contains()`, not by identity** (`assets/cart.js:477-489`). Shopify wraps every section in `<div id="shopify-section-…">`, so the drawer is never itself a child of `<body>`. Identity comparison marked the wrapper inert, which made the drawer inert with it, and focus could not be moved into a drawer that had just opened. Phase 8 calls this the single most consequential defect it found in its own work. Elements that must survive the sweep carry `data-cart-no-inert`.

**Not a native `<dialog>`.** `role="dialog"` + `aria-modal="true"` + `aria-labelledby` on a plain element, because `showModal()` splits the scrim into a `::backdrop` the theme cannot style as one piece, and a stray `method="dialog"` silently closes the panel and discards the POST.

**Two live regions, because `aria-modal` hides one of them.** `aria-modal="true"` tells assistive technology to treat everything *outside* the dialog as absent, so the layout's region was announcing to nobody while the drawer was open. `announce()` routes between them:

| When | Region |
|---|---|
| Drawer open | `[data-cart-drawer-status]`, inside the panel and **outside** the swapped node |
| Otherwise | `#CartStatus` in `layout/theme.liquid:253-259` — `role="status" aria-live="polite" data-cart-no-inert` |

Both are empty at page load and text is injected inside a `setTimeout`: a region created together with its content announces nothing, and a region destroyed by a section swap announces nothing either — which is why both sit outside the replaced node.

**A live region is not feedback for everyone.** Failures used to reach only the live region: a sighted customer saw the quantity snap back with no explanation. Each cart surface now carries a `role="alert"` line outside its swapped node — text plus a left rule, never colour alone. Successes use `role="status"` and the live region stays silent when the visible line is used, so nothing is announced twice. When the drawer opens, the drawer *is* the confirmation and nothing is announced at all. **Every sentence comes from `locales/en.default.json`** — `assets/cart.js` writes no user-facing English, so none of it is untranslatable.

**Escape is bound only while open.** Every keydown handler is added on open and removed on close, tracked in the header's binding registry for Theme Editor teardown (`assets/header.js:72-86, 207-219`; `assets/cart.js:402-411`). One item remains open from Phase 16 §18: the search panel and the cart drawer install *independent* capture-phase document handlers, so with both layers open a single Escape closes both. Recorded, not fixed.

**The Phase 16 P0 — a keyboard trap, SC 2.1.2.** `assets/facets.js` revealed the filter trigger unconditionally, while every drawer rule in `component-facets.css` lives inside `@media (max-width: 767px)` — but `.facets-open body { overflow: hidden }` is top level. Measured at 1440, 1280 and 768: the trigger was visible, pressing it locked page scroll and opened nothing, and because `.facets__bar` (which holds the close button) is `display: none` at that width, `closeBtn.focus()` was a no-op. Escape was the only way out of a page that no longer scrolled. **The cause was that the `matchMedia` listener only ran on `change` and never once evaluated the width the page loaded at.** The fix: one `applyWidth()` called immediately *and* on change, `open()` refuses above the breakpoint, and CSS retires the trigger at `min-width: 768px`. Guarded permanently by `facetsgate` (10/10). **Rule for any new media-query-gated overlay: evaluate at load, not only on change.** The filter drawer also closes itself if the viewport grows past the breakpoint, so focus is never trapped in something that is no longer a drawer.

### Reduced motion

Two halves, and both are required:

- **Token half** (`assets/design-tokens.css:506-513`): `--duration-fast`, `--duration-medium`, `--duration-slow` all collapse to **1ms**; `--hover-image-scale` drops from 1.03 to **1**.
- **Element half** (`assets/base.css:71-78`): a `*, *::before, *::after` sweep setting `animation-duration: 1ms`, `animation-iteration-count: 1`, `transition-duration: 1ms` and `scroll-behavior: auto`, all `!important`. **These four are the only real `!important` declarations in the theme** — a user preference must beat an author declaration, and it has to reach declarations that were never written as tokens, including app markup.

Handled in **13 assets** (`base.css`, `design-tokens.css`, `component-button.css`, `component-cart-line.css`, `component-quantity.css`, `header.css`, `section-cart-drawer.css`, `section-main-cart.css`, `section-main-product.css`, and `matchMedia` checks in `cart.js`, `facets.js`, `header.js`, `product.js`). `component-product-card.css` mentions it in a comment only, because its fade is a transition the sweep already collapses.

Rules that follow:

1. **Durations are read from tokens, never hard-coded**, or the reduced-motion block cannot reach them.
2. Every animated element must be usable and complete at its end state with no transition. Nothing exists only during an animation.
3. No content may be reachable only after motion. Scroll-triggered reveals and parallax are prohibited. The hero has no entrance animation at all.
4. Reduced motion is a preference, not a downgrade: colour, focus and state feedback are identical, they just arrive instantly.
5. Only `opacity` and `transform` may be animated, plus colour properties on control-sized surfaces. `--duration-fast` 150ms, `--duration-medium` 250ms (panel, drawer, disclosure, image scale), `--duration-slow` 400ms (a scrim behind a drawer or modal, full-surface changes only). No fourth duration exists. Phase 18 corrected the menu scrim from 250ms to 400ms to match.

**The one thing that must not be tokenised: the 250ms quantity debounce in `assets/cart.js` is a hard literal, deliberately.** `--duration-*` collapses to 1ms under reduced motion, which would remove the debounce for exactly the people most likely to be stepping a quantity from a keyboard. Do not "fix" it into a token.

Phase 18's drawer-exit change holds the panel visible for 250ms after close via an `.is-closing` class released on `transitionend` with a 500ms fallback — and **skips the wait entirely under `prefers-reduced-motion`**. Focus has already returned to the trigger and the keydown trap is released at that point.

### Keyboard, semantics and names

- **Every control is a real `<button>` or `<a>`.** Zero clickable `<div>` or `<span>` anywhere. **Zero positive `tabindex`** in the theme. DOM order equals visual order at every breakpoint — no section uses `order`, `row-reverse` or grid placement to reorder content away from reading order.
- **The closed mobile panel is removed from the tree, not just from view.** `.header__panel[hidden] { display: none }` (`assets/header.css:459`) — written with the attribute selector so its 0,2,0 specificity beats `.header__panel` (0,1,0) regardless of source order. Before this, a keyboard user tabbing from the logo walked five invisible menu links plus a close button on every page at every mobile width (SC 2.4.3, 2.4.7). It does not cost the slide: `assets/header.js` sets `hidden = false`, forces a reflow, *then* adds the open class.
- **Nothing is hidden on mobile.** Control counts are identical across viewports — 15 on the product page, 27 on the cart with the drawer open.
- **No control auto-submits on change.** The collection sort select had a `change` handler and a hidden button (SC 3.2.2 On Input, Level A); it now has a visible submit and that section ships zero JavaScript. Filter *chips* act immediately while filter *checkboxes* apply on confirm — activating a link is not changing the setting of a control. That split is written into `snippets/facets.liquid` so it is not harmonised away.
- **Disclosures are native `<details>`/`<summary>`** — no `aria-expanded`, no `aria-controls`, no `role="button"`. Keyboard-operable and announced correctly by default. Filter groups render server-side **open** when they hold an applied value.
- **State lives in ARIA and in words.** `aria-expanded` + `aria-controls` on the menu toggle; `aria-current="page"` from `link.active`, never hard-coded; `aria-current` on the current pagination link and the active gallery thumbnail; `fieldset`/`legend` per product option; a real `<label for>` on every input.
- **Names, not pictures.** Icon-only controls carry a `.visually-hidden` span naming the *action*; every decorative glyph is `aria-hidden="true"`. `snippets/quantity-selector.liquid` emits "Increase quantity for {title}", not "+". Phase 16 fixed the footer logo link, which was `<a href="/">` containing only `<img alt="">` and announced as "link" (SC 2.4.4, 4.1.2, Level A) — the name is now a visually-hidden span *inside* the anchor and the image stays decorative, so the brand is not announced twice. Phase 16 also stopped `aria-controls="CartDrawer"` being emitted on `/cart`, where the layout renders no drawer and the id did not exist.
- **`aria-disabled`, not `disabled`, on the quantity steppers** — the control stays focusable so its reason can be reached, and the reason is the value beside it.
- **Colour is never the sole carrier of state (SC 1.4.1).** Sold out is a word on the button; an unavailable variant chip is struck through **and** says so through one shared server-rendered hook (so a screen reader does not hear "Small, Unavailable, Unavailable"); sale pricing carries visually-hidden "Sale price" / "Regular price" labels; swatch colours are named in hidden text. Phase 18 closed the last two gaps: the mobile menu's current page now carries an underline as well as colour (`.header__panel-link.is-active`, `assets/header.css:553`), and the shared paginator's current page uses weight plus a rule rather than gold.
- **Hover is never the only signal**, and every hover rule sits inside `@media (hover: hover) and (pointer: fine)` so a touch tap never leaves an element stuck. Phase 18's `hovergate` moved the last nine ungated rules: **29 rules, 29 gated, 0 ungated** — enforced as a standing test.
- **Heading order.** Exactly one `<h1>` per template (hero on index, `product.title` on product), no skipped levels. A card's or tile's heading level **follows its section**: `h3` when the section renders its `h2`, `h2` when the merchant has cleared the heading — so clearing a setting cannot create a jump. Home page measured: 1 h1, 2 h2, 7 h3.
- **Landmarks.** `<header>`, `<main id="MainContent">`, `<nav>`, and the footer's `contentinfo` role written out explicitly with its section schema `tag` set to `div`, because `<footer>` maps to `contentinfo` only while it is not a descendant of `article`, `aside`, `main`, `nav` or `section`.

### Reflow, zoom and text spacing

**Reflow (SC 1.4.10): zero horizontal scroll at 320px**, verified on every surface at every tested width — twelve viewports, and in Phase 16 across 17 pages × 12 viewports. The nine specified widths are **375, 390, 430 / 768, 820, 1024 / 1280, 1440, 1920**, plus 480 and both landscape orientations. Phase 18 corrected the suite, which had been carrying 834 (iPad Pro) where the spec names 820 — so nine required widths had been tested as eight.

**Landscape is gated on height, never orientation:** `(max-height: 540px) and (max-width: 1023px)`. *Orientation says nothing about how much height there is.* There is no `orientation: landscape` query anywhere. Full-height and fixed elements use `svh`/`dvh`, never `vh` (gallery `max-height: 100dvh`, drawer `height: 100vh; height: 100dvh`, cart page `60svh`).

**Zoom (SC 1.4.4).** Measured on the hero only: no horizontal scroll or loss of content at 200% (720 CSS px) or 400% (360 CSS px). Not measured page-by-page across the theme — but zoom resolves to reflow, and the breakpoint ladder (480/768/1024) exists specifically so a 1440 desktop at 160% reaches a real tablet tier rather than the prototype's bare phone layout with no navigation.

**Text spacing (SC 1.4.12).** Measured on the hero with line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em and paragraph spacing 2em forced: nothing clips or overlaps; the section grows 517→649px at 375 and 590→959px at 1440 and absorbs it. The structural rule behind it: **no component's height is derived from a string's expected length**, and no fixed-height container is placed around tracked uppercase — 0.22em and 0.30em tracking expands the line.

**Body copy is 16px at every viewport and is never reduced on mobile.** Headings scale with `clamp()` and an `h1` never falls below 32px. The cart note field is 16px for a second reason: below 16px iOS zooms the viewport the moment the field takes focus, and a zoomed cart has to be panned to read.

**Safe-area insets are currently inert, and that is documented rather than hidden.** The viewport meta is `width=device-width, initial-scale=1`; `viewport-fit` is unset, so it defaults to `auto`, under which the browser insets the layout viewport itself and every `env(safe-area-inset-*)` reports 0 — confirmed empirically (`--drawer-pad-inline-end` resolves to `max(1.5rem, 0px)`). The `max()` padding added in Phase 9 is kept because it costs nothing and leaves one piece of work for whoever enables `viewport-fit=cover`, which is a sequenced four-step job (meta change, `.header__inner` top inset, make `--header-overlay-offset` account for it, re-measure the hero everywhere) and **should not be done as one line**. One CSS trap recorded from that work: a `padding-block` shorthand inside a media query overrides an earlier `@supports` rule at equal specificity, so the `@supports` must be nested inside the media query.

### The success criteria cited across the project, and where each is enforced

| SC | Level | Enforced by |
|---|---|---|
| 1.1.1 Non-text content | A | `alt` from the image object, never invented; emitted empty when Shopify defaulted it to a title already inside the same link; decorative glyphs `aria-hidden` |
| 1.3.1 Info and relationships | A | real headings, `<ul role="list">`, `fieldset`/`legend`, `role="list"` on the cart line list |
| 1.4.1 Use of colour | A | every colour state has a text or ARIA counterpart (see above) |
| 1.4.3 Contrast | AA | the verified-pairings register + 73 standing measurements; composited measurement over photography |
| 1.4.4 Resize text | AA | hero measured at 200%/400%; otherwise carried by reflow |
| 1.4.10 Reflow | AA | 320px, zero horizontal scroll, all surfaces |
| 1.4.11 Non-text contrast | AA | `--color-border-interactive` 3.02:1 / 3.13:1; focus rings 11.01:1 and 17.04:1 |
| 1.4.12 Text spacing | AA | no height derived from string length; hero measured under forced spacing |
| 2.1.1 Keyboard | A | every control real; 0 positive `tabindex` |
| 2.1.2 No keyboard trap | A | the Phase 16 filter-drawer P0; `facetsgate` 10/10 |
| 2.3.3 Animation from interactions | AAA (held anyway) | the two-half reduced-motion implementation |
| 2.4.1 Bypass blocks | A | skip link → `<main id="MainContent">` |
| 2.4.2 Page titled | A | closed in Phase 10 (`layout/theme.liquid`); the prototype's `<title>` was empty |
| 2.4.3 Focus order | A | DOM order; the `[hidden]` panel fix |
| 2.4.4 Link purpose | A | footer logo link name; link text stands alone out of context |
| 2.4.6 Headings and labels | AA | one h1, no skipped levels, caller-chosen card levels |
| 2.4.7 Focus visible | AA | the global `:focus-visible` rule + three component patterns |
| 2.4.11 Focus not obscured (minimum) | AA | drawer footer below the scroller; `scroll-padding-block` on both sticky columns |
| 2.5.5 Target size (enhanced) | AAA (goal, not bar) | `--target-min` 44px |
| 2.5.8 Target size (minimum) | AA | `--target-min-aa` 24px; zero elements below it |
| 3.1.1 Language of page | A | `<html lang="{{ request.locale.iso_code }}">`; closed in Phase 4/10 |
| 3.2.2 On input | A | no control auto-submits; sort has a visible button |
| 4.1.2 Name, role, value | A | every control exposes all three |

### What was never tested, and must be before any conformance claim

State these as gaps, not as passes:

1. **No axe or Lighthouse run, anywhere in the project.** Phase 1 recorded it as a gap and assigned it to a "Phase 14 — Accessibility" that the re-ordered roadmap never produced. Phase 16 established that Theme Check *was* available all along (the Phase 10 runner had been pointed at the project root, which stopped being the theme root when Phase 10 moved the theme into `god-squad-theme/`, so it scanned an empty directory and reported zero offenses) — but Lighthouse is genuinely unavailable and **no Lighthouse score appears in any document**.
2. **No screen-reader session.** Not NVDA, JAWS or VoiceOver, at any point. One specific open item needs one: the `<shopify-account>` control supplies a visually-hidden name in the `signed-out-avatar` slot so it is named whether or not Shopify names it — what cannot be checked without a live store and a screen reader is whether the two combine into a **doubled announcement**. Open the store, listen to the header control once; if it announces twice, delete the `<span class="visually-hidden">` from the slot.
3. **No forced-colors / high-contrast mode test**, and no `forced-colors` media query in the theme.
4. **No real device.** Every reading was taken in headless Chromium (Edge 153 and Chrome, both Chromium) through an iframe of the exact target CSS size, cropped, with transitions disabled first — because headless virtual time does not advance transform transitions and an un-disabled panel reports `translateX(-100%)` forever. **Safari is untested.** iOS Safari and Android Chrome verification is an outstanding carry-forward.
5. **The account experience itself is unverifiable here.** The harness never loads Shopify's script, so `<shopify-account>` is permanently un-upgraded and every measurement is of the *reservation*, not the component. The component is also **not focusable until Shopify's script upgrades it** (`tabIndex` is -1 while undefined) — inherent to the approach, where the old `<a href>` worked with no script. `--shopify-account-dialog-position-top` is deliberately unset; it is the first knob to check live against the sticky header.
6. **Alt-text *content* cannot be assessed**, because no merchant photography exists. The alt *path* is verified end to end (`alt: img.alt`, never invented, empty alt correctly announcing a mood photograph as decorative); what a real photograph's alt text should say depends on photographs that have not been taken. The same gap makes the image half of any visual accessibility review impossible — recorded in Phase 18 as **NOT ASSESSABLE**, not as a pass.
7. **One recorded-not-fixed keyboard item:** one Escape closes two layers when the header search panel and the cart drawer are both open (Phase 16 §18, item 6).

Phase 18's verdict on the accessibility dimension is worth carrying verbatim into any handover, because it is a measured claim and not a conformance statement: keyboard, focus, contrast (73/73), labels and reduced motion all pass; two SC 1.4.1 improvements were made; **no accessibility regression was introduced**; and a *CONFIRMED* audit verdict is a claim, not a fact — every finding in this project was verified against the files before being acted on, and five reviewer findings were overruled with citations rather than fixed.

---

## Performance and SEO posture

Phase 16 (2026-09-24) is the measurement pass; Phase 18 (2026-09-25) re-measured after its CSS consolidation. **Phase 18's figures are the current ones** and supersede Phase 16's baseline table wherever the two differ.

### What was measured, and what was not

Everything in this section came from rendered output or the files on disk. Nothing was estimated. Five things could not be measured at all, and no number is given for any of them:

| Not measured | Why | What stands in |
|---|---|---|
| LCP, FCP, TTFB **timings** | No Shopify server, no network. The harness serves localhost. | A static audit of which image carries `loading="eager"` / `fetchpriority="high"` per surface |
| Field INP | Needs real users | Handler duration, measured per control, labelled as *an input to* INP |
| Image **bytes** | No merchant photography exists — Phase 3 recorded sourcing, not processing, as the ceiling | Image count, declared `widths`, declared `sizes` |
| CLS from **font swap** | The harness has no font files, so no swap occurs | Nothing. Called out rather than silently scored zero — and it matters more since Phase 16 added two font faces (below) |
| Lighthouse | Not installed; `npm` has no network here | Nothing. **No Lighthouse score appears anywhere in this project and none may be invented.** |

Two corrections a reader needs to know about:

- **Theme Check was always available and phases 10–15 wrongly reported it unavailable.** `@shopify/theme-check-node` — the engine the Shopify CLI wraps — had been in the scratchpad's `node_modules` since Phase 10, but the runner pointed at the *project* root, which stopped being the theme root the moment Phase 10 moved the theme into `god-squad-theme/`. It was scanning a directory containing no theme and reporting zero offenses. Pointed correctly it found four. **Always run Theme Check with the root set to `god-squad-theme/`.**
- Two early performance readings were wrong and were discarded, not published. A `PerformanceObserver` named the collection page's LCP as the **78px header logo** — an artifact of a harness that ships no image files, so every `<img>` 404s. And CLS was counting the measurer's own synthetic clicks, because `dispatchEvent` does not set `hadRecentInput`; load shift and interaction shift are now measured separately.

The pass's own P0 was found by the JavaScript and accessibility audits independently: `assets/facets.js` revealed the Filter trigger at every width while every drawer rule in `component-facets.css` sat inside `@media (max-width: 767px)` — except `.facets-open body { overflow: hidden }`, which was top level. At 1440, 1280 and 768 the button locked page scroll, opened nothing, and trapped the keyboard (SC 2.1.2), because `.facets__bar` holding the close button was `display: none`. The cause: the `matchMedia` listener only ran on **change** and never evaluated the width the page loaded at. The fix is one `applyWidth()` called immediately *and* on change, `open()` refusing above the breakpoint, and CSS retiring the trigger at `min-width: 768px`. **A media-query listener that is never evaluated at load is a bug, not a style.**

### Page weight

Gzipped, CSS + JS, measured after every Phase 18 change:

| Surface | Requests | CSS gz | JS gz |
|---|---:|---:|---:|
| Homepage | 26 | 55,093 | 16,392 |
| Collection | 21 | 46,599 | 16,392 |
| Collection + filters | 23 | 51,708 | 20,230 |
| Product | 23 | 40,519 | 21,989 |
| Cart page | 17 | 31,421 | 16,392 |
| Search | 18 | 46,507 | 16,392 |
| 404 | 15 | 38,316 | 16,392 |

**Duplicate requests: 0 on every surface.** Phase 18 added two stylesheets (`component-container.css`, `component-pagination.css`) and the CSS payload still went *down*, because both files absorbed duplicated rules: comments-stripped CSS fell 98,129 B → 95,628 B (−2,501 B, −2.5%) and declarations 2,451 → 2,380 (−71), across 19 → 21 stylesheets.

The icon set costs **zero requests** on every surface: 8 to 14 inline SVG snippets per page rather than files. There are no `<link rel="preload">`, no `preconnect`, no `dns-prefetch`, no `@import`, and no request to `fonts.googleapis.com`, `fonts.gstatic.com`, Typekit or any CDN anywhere in the theme — verified by grep across all 75 files.

Per script:

| File | raw | gzip | code only | code gz |
|---|---:|---:|---:|---:|
| `cart.js` | 39,750 | 12,073 | 20,616 | 4,930 |
| `header.js` | 13,963 | 4,319 | 9,062 | 2,091 |
| `product.js` | 18,096 | 5,597 | 11,734 | 2,863 |
| `facets.js` | 10,937 | ~3,848 | — | — |

`facets.js` grew from 8,818 B raw in Phase 16 to 10,937 B when Phase 18 added the `.is-closing` exit transition; that is why collection-with-filters JS is 20,230 B gz rather than Phase 16's 19.5 KB. **Zero dependencies** — no framework, no jQuery, no Swiper, no GSAP, no polyfill, verified rather than assumed — and exactly one global, `window.GodSquad`. All four scripts are `defer`. The only inline script in the layout is the one line that swaps `no-js` for `js` on `<html>`.

### The performance budget

Set in Phase 16 from what the theme measures, not from round numbers. It binds on future work.

| Budget | Target | Status |
|---|---:|---|
| JavaScript, all pages | ≤ 30 KB gz | 22.0 KB gz — pass |
| JavaScript, per page-load script | ≤ 10 KB gz | **`cart.js` 12,073 B — breached, see below** |
| CSS, worst page | ≤ 55 KB gz | 55,093 B on the homepage — **headroom is gone**; whether this is a breach depends on whether KB means 1000 or 1024 |
| Requests, worst page | ≤ 30 | 26 — pass |
| Load CLS | ≤ 0.05 | 0.0125 worst — pass |
| Theme handler time | ≤ 50 ms | 0.00 ms — pass |
| Eager images per page | exactly 1 | 1 on every measured surface; the product gallery can emit 2 (below) |
| `fetchpriority="high"` per page | ≤ 1 | 1 — pass |
| Third-party scripts | 0, **each future one justified in writing** | 0 |

### The asset strategy

**Per-section stylesheets, requested by the section that owns them.** A page without a hero never downloads hero CSS; a store with no filters configured downloads neither `component-facets.css` nor `facets.js`, because both sit inside the `has_filters` guard in `sections/main-collection.liquid`. The promotion rule is written into the files themselves: *a component moves to the layout the moment a second surface renders it.* That rule promoted the button system (Phase 6), the cart line and quantity control (Phase 8), the container (Phase 18) and the paginator (Phase 18).

`layout/theme.liquid` loads eight stylesheets, in this order and for these reasons:

| Order | File | Why it is in the layout |
|---|---|---|
| 1 | `design-tokens.css` | defines every custom property; **no token definition lives anywhere else** |
| 2 | `base.css` | element layer (reset, focus ring, reduced motion); consumes the tokens, so it must follow them |
| 3 | `header.css` | the header is on every page |
| 4 | `component-container.css` | the content column; every other component sits inside it |
| 5 | `component-button.css` | hero + every collection section |
| 6 | `component-pagination.css` | collection + search |
| 7 | `component-quantity.css` | product form, cart drawer, cart page |
| 8 | `component-cart-line.css` | drawer + cart page |

Then `{% render 'css-variables', part: 'style' %}` — **after** the stylesheets, so its `:root` declarations beat `design-tokens.css`.

**`theme.css` was deliberately never created.** Phase 1's recommended tree named it; there is no third layer to put in it. Likewise there is no `mobile.css`: responsive rules live in the file that already owns the component.

`base.css` holds the only four real `!important` declarations in the theme, all inside the `prefers-reduced-motion` block, where a user preference must beat an author declaration. Verified: every other `!important` match in `assets/*.css` is inside a comment.

**The homepage's duplicate `<link>` tags are a measured non-problem.** `templates/index.json` renders `featured-collection` twice (`new-drop`, `best-sellers`) and each emits `component-product-card.css` and `section-featured-collection.css`, so the head carries four tags for two URLs. Measured at the network layer the browser deduplicates: **11 CSS requests, not 13.** Promoting those stylesheets to the layout would push ~4 KB onto four surfaces that do not need them to remove two `<link>` elements. Recorded, not changed.

### The cart.js size offence

Theme Check's `AssetSizeJavaScript` flags three script tags against a **10,000-byte compressed** threshold, and `cart.js` at **12,073 B gzipped is genuinely over it.** Re-gzipping the file today gives 12,008 B at `-9`, so the breach is not an artifact of a compression setting.

The diagnostic that matters: **the executable code is 4,930 B gzipped; the other 7,143 B is comments.** The whole theme's JavaScript is 24 KB gzipped with no dependencies.

Two rules follow, and both have been broken by well-meaning reviewers before:

1. **Do not "fix" this by deleting comments.** The comments are the only record of why the cart behaves as it does (positional `updates[]`, line-key identity, the `aria-busy`-not-`disabled` guard, the `inert` `contains()` exclusion). Phase 18 restated it: the threshold "is not reachable by deleting prose."
2. **Do not restructure the cart with import-on-interaction to chase 2 KB.** The recommended answer — recorded in both Phase 16 and Phase 18 and still not done — is **a minification step at deploy time.** It clears all three offenses without touching a line of tested logic, and it is a tooling decision rather than a code one. This is the single highest-value performance change available on the theme as it stands.

### Image handling

Every image on every surface goes through `image_url | image_tag`. There is no hand-written `<img>` and **no hand-built CDN URL anywhere** — validators in several phases assert it.

The delivery contract:

- `image_url: width: N` is the **cap** — one URL, no `srcset`, no `sizes`. `image_tag` builds the `srcset` from `widths:` and writes `sizes:`. **Both `widths:` and `sizes:` are stated explicitly on every `image_tag` call, never on `image_url`.** A bare `image_url` would ship one fixed width to every device.
- **The Shopify CDN does not output AVIF.** WebP is the delivery format and the CDN serves it automatically from any uploaded master. Any checklist asking for an AVIF ladder is asking for something the platform will not produce.
- **The CDN does not upscale.** A `widths` entry larger than the uploaded master returns the master at native size while the `srcset` still advertises the larger descriptor, so every ladder is capped at the master's real width. Product ladders are currently capped at 235 px because the masters are 235×230, 235×235 and 215×190 crops of the mockup; the ladder opens to `288, 576, 864, 1200` **the moment a real master lands and not before.**
- `image_tag` writes `width` and `height` as **attributes**. Do not strip them, and where CSS reshapes the box **constrain both axes** — setting only `width` left a cart thumbnail 948 px tall and made `aspect-ratio` inert (found by the Phase 8 harness, not by review).
- **Never pass `style:` to `image_tag`.** It writes Shopify admin's focal point as an inline style that outranks any stylesheet rule; cropping uses `object-fit` only, and admin's focal point is the single source of truth.
- `alt` comes from the image object and is never invented. An empty merchant alt correctly announces a mood photograph as decorative.

Eager/priority, audited statically because timings are unmeasurable:

| Surface | eager | lazy | the eager one | `fetchpriority` |
|---|---:|---:|---|---|
| Homepage | 1 | 8 | `hero__image` | high ×1 |
| Collection | 1 | 4 | banner if present, else first `product-card__image` | — |
| Search | 1 | 1 | `product-card__image` | — |
| Product | 1 | 7 | `product-gallery__image` (active slide) | high ×1 |
| Cart page | 1 | 3 | `cart-line__image` | — |

Two code rules produce that, and both are worth knowing because both were wrong once:

- **Collection: banner and first card are mutually exclusive.** `sections/main-collection.liquid` sets `card_eager = true` only `if forloop.first and show_banner == false`. Where a banner renders it takes the eager load and every card stays lazy. Exactly one eager image in both configurations.
- **Product gallery: `fetchpriority` follows `is_active`, not `forloop.first`.** Before Phase 16 it followed `forloop.first`, so on any product whose selected variant's featured medium is not the first medium the browser was told to hurry an image nobody was looking at and to lazy-load the actual LCP element. **Note the live consequence in the code:** `forloop.first` still receives `loading: 'eager'` (deliberately, because the stacked desktop layout renders every slide in document order), so on such a product the page carries **two** eager images, one of which has `fetchpriority="high"`. Every measured fixture had `is_active == forloop.first`, which is why the table reads 1.

Verified across six surfaces, 54 checks: every `<img>` has `width` and `height`; every content image has `srcset` **and** a matching `sizes`; no `srcset` overshoots 3× its largest declared slot; every `<img>` has an `alt` and none reads as keyword stuffing; video goes through Shopify's own filters with `autoplay: false`, `controls: true`, `preload: 'metadata'` and a lazy external player, and there is no background or decorative video.

Shared `sizes` arithmetic lives in **`snippets/grid-sizes.liquid`**, used by `main-collection` and `main-search`. It encodes two rules learned the hard way, both correcting *under*-declaration, the direction that costs image quality:

1. **A clause may not claim a width before the layout that produces it applies.** The desktop threshold is floored at 1024 (`if threshold_d < 1024`), because column arithmetic alone computes 976 while the desktop column count does not take effect until `--bp-lg`.
2. **A clause may not divide by more columns than actually fit.** At the container cap the row is a fixed pixel value, but the grid is `auto-fill` with a 272 px floor (128 px below 768), so dividing by the *requested* column count declared 253 px for a track painting 346 px.

`sections/featured-collection.liquid` carries its own copy of this derivation and was **deliberately not consolidated**. A future change to the shared rules must be applied there too. That duplication exists because Phase 10 fixed the desktop-clause bug in one instance rather than in the rule, and the other two copies carried it for two more phases.

**Open image items, unfixed:**

- `sections/hero.liquid` and `sections/our-story.liquid` declare `sizes: '100vw'` for boxes that are `object-fit: cover` (our-story's is `(min-width: 1024px) 70vw, 100vw`), under-declaring the phone tier by roughly 1.9×. Confirmed P2 in Phase 16 §18, still present in the code.
- **No mobile hero master exists.** The `mobile_image` picker and its `(max-width: 749px)` `<picture>` source are wired and deliberately left empty — inventing a crop is not art-directing one.
- **Image bytes remain unmeasurable and untested**, because the merchant's photography does not exist. The hero currently ships an AI-generated image with unconfirmed rights, and the section schema tells the merchant to replace or clear it before launch.

### Structured data

**Current state: `{{ product | structured_data }}` in `sections/main-product.liquid`, emitted exactly once per page, and nothing else.** That is Shopify's own filter, so price, currency, availability URL and per-variant identifier all come from the platform and cannot drift. It also cannot emit a rating or a review count, because no review data exists.

**Confirmed missing and deliberately not implemented:** Organization, WebSite, BreadcrumbList, and any collection-level markup.

- **Organization** is blocked on business information. Its useful fields — `sameAs`, `logo`, `contactPoint` — are exactly the values this project has refused to invent. `social_facebook_url` and `social_instagram_url` are both empty settings; a block whose `sameAs` array is empty half the time is worse than no block. **Unblock condition: real social URLs plus a contact route.**
- **BreadcrumbList** is declined on stronger grounds: the theme has **no navigation hierarchy to describe.** Products are not scoped to a parent collection in the URL and the menu belongs to the merchant. A fabricated trail is fake structure.

### Head metadata

Measured on the rendered `<head>` of all seven templates.

| Tag | State | Source |
|---|---|---|
| `canonical` | exactly one per template, nothing competing | `{{ canonical_url }}`, in `layout/theme.liquid` only |
| `<title>` | correct | `page_title`, with `shop.name` appended only when absent, current tags named, and page number named on paginated views |
| `description` | correct | `page_description | escape`, emitted only when present |
| `og:*` / `twitter:*` | **added Phase 16** | `snippets/meta-social.liquid` |
| `rel="icon"` 32px + 192px, `apple-touch-icon` 180px | **192 and apple-touch added Phase 16** | one `settings.favicon`, resized by Shopify |
| meta-robots | none, deliberately | Shopify's defaults are not competed with |
| `robots.txt.liquid` | absent | — |
| custom sitemap | none | Shopify's own |
| `content_for_header` | emitted once, unmodified, in `<head>` | Shopify — **never parse or alter it** |
| `lang` | `{{ request.locale.iso_code }}` | — |

`snippets/meta-social.liquid` emits `og:site_name`, `og:url`, `og:title`, `og:type`, `og:description`, `og:image` (+ `secure_url`, width, height, alt), `twitter:card`, `twitter:title`, `twitter:description`. Its rules:

- **Every value is a Shopify object. There is no written marketing copy in the file** and no invented claim.
- `og:type` is `product` on a product page, `article` on an article, `website` elsewhere.
- The image chain, most specific first: **product featured image → collection featured image → `settings.share_image` → `settings.logo`**, each branch guarded, so a store with no image at any level emits **no `og:image` at all** rather than a URL that 404s. A failed og:image is worse than none, because the platform caches the failure.
- `og:image:width` is the **literal 1200** with the height derived for *that* rendering. Reading `image.width` would publish the source asset's dimensions beside a 1200 px URL.
- **Height is derived from `width`/`height`, never from `aspect_ratio`.** The first version divided 1200 by `share_image.aspect_ratio`; `aspect_ratio` is not populated on every image drop, Liquid treats the missing value as 0, and it threw a **division by zero in the head on all seven templates, on every page.** The test caught it before it shipped. The guard is `if share_image.width > 0 and share_image.height > 0`.
- **No `twitter:image`** — X falls back to `og:image` for `summary_large_image`, and a second copy of the URL can only drift. **No `og:price`** — `structured_data` already publishes price and availability in the vocabulary search engines consume, and the OG price tags are legacy.
- `twitter:card` is `summary_large_image` only when there is an image; otherwise `summary`, because promising a picture the scraper cannot find renders the degraded card.

The gap that produced this work was an orphan, not a decision: Phase 1's SEO-04 specified `snippets/meta-tags.liquid` and routed it to "Phase 13 — SEO", but the Phase 13 that was actually briefed was Search and Filtering.

**Heading structure is clean on every surface** — exactly one `h1`, no skipped levels:

```
Homepage    h1 h2 h3 h3 h3 h2 h3 h3 h3 h3 h2 h3 h3 h3 h2
Collection  h1 h2 h2 h2 h2 h2 h2 h2 h2
Product     h1 h2          Cart  h1          404  h1 h2 h2
```

Card and value-tile heading levels **follow their section**: a card is `h3` when its section renders its `h2` and `h2` when the merchant has cleared the heading, so the outline never skips.

`settings.share_image` is a global `image_picker` in **Theme settings › Brand › Social sharing image**, ~1200×630. A merchant must upload it; without it, shared links to the five non-product, non-collection templates fall back to the logo, which crops badly.

### Fonts

**The one Phase 16 finding a customer would have seen on every page.** `design-tokens.css` spends three weights on the body family — `--type-eyebrow-weight` 500, `--type-label-weight` and `--type-price-weight` 600 — covering 19+ rules, which is every label, price and eyebrow in the store. `layout/theme.liquid` called `font_face` exactly twice, once per family, and each call emits a face for the **one** variant in the setting: `jost_n4` and `playfair_display_n9`. **Jost 500 and 600 had no `@font-face` at all** and the browser synthesised them from Jost 400. Faux bold is thicker, wider and differently tracked than a real cut — on a type system built out of tracked caps, visible everywhere.

Four faces are now emitted — Jost 400, Jost 500, Jost 600, Playfair Display 900 — via `font_modify`:

```liquid
assign body_medium   = settings.type_body_font | font_modify: 'weight', '500'
assign body_semibold = settings.type_body_font | font_modify: 'weight', '600'
```

Three rules that must not regress:

1. **Every `font_modify` call is guarded**, because it returns `nil` when a family has no such variant. A merchant who picks a single-weight font must get exactly what they got before, not a broken rule. Negative-controlled against a single-weight family: two faces emitted, nothing broken.
2. **All four faces stay inside one `{% style %}` block.** `font_face` returns a bare `@font-face` rule, not a style element. Emitted unwrapped in Phase 10 it registered no face at all *and*, because a non-whitespace character token ends the HTML "in head" insertion mode, printed the CSS text as visible content above the logo, with the Shopify head, every stylesheet and both scripts then parsed in body context.
3. `font_display: swap` is unchanged.

Consequence to act on: **font-swap CLS is the one CLS source this environment cannot reproduce, and two faces were just added. Verify CLS on a real store.**

### CLS

Load CLS, measured before any interaction:

| Surface | CLS | source |
|---|---:|---|
| Homepage | 0.0003 | header nav settling |
| Collection | 0.0003 | header nav settling |
| Collection + filters | 0.0003 | header nav settling |
| Product | 0.0000 | none |
| **Cart page** | **0.0125** | the no-JS Update button being hidden |
| Search | 0.0003 | header nav settling |

The worst surface is 8× under Google's 0.1. **Every `<img>` on every surface carries `width` and `height`** — the precondition — verified across six surfaces.

The cart page's 0.0125 is a deliberate trade and must not be "fixed". `.cart-js .main-cart__update { display: none }` removes the no-JavaScript Update button once `cart.js` confirms it is running. It keys on `cart-js` — a class the cart script sets on itself — **not** on the layout's `js` class, because keying on `js` would hide the only control that can apply a quantity change in exactly the case where nothing else can. Reserving the space leaves a gap; reordering it visually breaks DOM/visual order. **0.0125 is the correct price for a working no-JavaScript fallback, and it is recorded rather than hidden.**

### INP

| Control | handler time |
|---|---:|
| menu toggle | 0.00 ms |
| cart bubble | 0.00 ms |
| quantity stepper | 0.00 ms |
| filter toggle | 0.00 ms |
| search trigger | 0.00 ms |

No long tasks on any surface during load. This is handler duration, one component of INP, and is reported as such — field INP needs real users. The posture is structural rather than tuned: **one delegated listener per event type for the whole document**, no framework, no polling, no `setInterval` anywhere. The only debounce is a deliberate **250 ms literal** on cart quantity, written as a literal on purpose: `--duration-*` collapses to 1 ms under `prefers-reduced-motion`, so a motion token there would defeat the debounce.

### Third-party load

**Zero.** No Meta Pixel, no Google Analytics or Ads tag, no TikTok pixel, no chat widget, no reviews app, no social embed, no `dataLayer`, no third-party host reached — verified by search across every file. Shopify's own analytics arrive through the single unmodified `{{ content_for_header }}` at `layout/theme.liquid:127`, so Theme Check's `ContentForHeaderModification` passes. Search & Discovery, the one app the storefront depends on, adds no storefront script: it populates `collection.filters` server-side. The current platform position is that a theme cannot legitimately contain tracking code at all — if a pixel is ever wanted it belongs in a channel app or a custom pixel, never pasted into the theme.

### Theme Check

```
root: god-squad-theme/     files scanned: 49     checks: 84

default config      4 offenses  ->  2 offenses
  2 ERROR  ValidJSON          2 ERROR  ValidJSON  (business information)
  2 WARNING UnusedAssign      fixed

theme-check:all     7 offenses  ->  5 offenses
  3 ERROR  AssetSizeJavaScript   3 ERROR  AssetSizeJavaScript  (unchanged)
```

The two `ValidJSON` errors are **business information, not code**: `config/settings_schema.json`'s `theme_info` block carries `theme_name`, `theme_version` (`0.5.0`) and `theme_author` but no `theme_support_email` or `theme_documentation_url` — confirmed in the file. They are distribution metadata for themes shipped to other merchants and have no functional effect on a bespoke theme. Supply them and the default config is clean. The three `AssetSizeJavaScript` errors are the `cart.js` offence above.

### Broken references

Every reference the theme makes was resolved, and the resolver was negative-controlled with four seeded breakages, all caught:

| Kind | Referenced | Missing |
|---|---:|---:|
| `asset_url` | 23 | **0** |
| `render` (snippets) | 22 | **0** |
| sections (tags, JSON, groups) | 15 | **0** |
| translation keys used | 117 | **0** |
| translation keys defined but unused | — | **0** |
| literal internal hrefs | all | **0** unknown |

No orphaned asset, snippet or section, the sole exception being `cart-icon-bubble`, which is reached by name through the Section Rendering API. One method note: the resolver first called `grid-sizes` an orphan because inside a `{% liquid %}` block `render` is a bare statement with no tag around it.

**Five storefront templates Shopify can route to that this theme does not have:** `article`, `blog`, `gift_card`, `list-collections`, `password`. Each serves Shopify's error page to anyone reaching its URL. `templates/` currently holds exactly seven files: `404.json`, `cart.json`, `collection.json`, `index.json`, `page.json`, `product.json`, `search.json`.

### Confirmed and deliberately unchanged

- **`.variant-picker__swatch--square` is unreachable** — the snippet accepts a `swatch_shape` parameter and its only caller never passes it. Measured across 26 pages, one of only two non-reachable CSS classes in the theme (the other is `shopify-payment-button`, which is Shopify's own output). 40 bytes and a documented extension point. Recorded, not deleted.
- **40 of 192 design tokens were unreferenced** at the Phase 16 measurement. A design system is allowed a vocabulary larger than its current usage.
- **The header search form hardcodes `type=product`** (`sections/header.liquid:318`), diverging from the search-types setting. Confirmed P2, open.
- **One Escape closes two layers** — the search panel and the cart drawer install independent document-level handlers. Confirmed P2, open.
- 48 of Phase 16's 62 confirmed findings were left open, all P2/P3; three of the six "worth doing next" were then done by Phase 18 (the duplicated paginator, the twelve-times-copied container, the double-defined `.product-card__error`).

### What an integration must still do

Theme-side, in priority order: **add a deploy-time minification step** (clears all three `AssetSizeJavaScript` errors without touching tested logic), then fix the hero and Our Story `sizes="100vw"` under-declaration, then ship the five missing templates (`password` first if the store will ever sit behind a password page).

Merchant-side, none of which is code: upload a **social sharing image** (~1200×630) and a **favicon** (it now feeds three icon sizes including the iOS home-screen icon); decide the **hero CTA destination** and the **empty-cart/404 destination** (`/collections/all` is servable now that a collection template exists); **publish the policies** so `shop.policies` becomes available to the footer; and supply **`theme_support_email` and `theme_documentation_url`**.

On a real store, measure what this environment could not: **CLS after the font change**, one Lighthouse run per template, real LCP/FCP/TTFB, and field INP. Safari is untested throughout — Edge 153 and Chrome are both Chromium, so the cross-browser coverage mainly rules out harness artifacts. The two things most worth checking in Safari are the `position: fixed` cart scroll lock on iOS and `inert` support.

---

## Analytics and marketing posture

### The governing position

**A Shopify theme cannot do tracking any more, and this one does none.** That is not an omission or a deferral — it is what the platform requires. Two primary sources settle it:

> *"To ensure the quality of standard events, partners and merchants cannot publish standard events. `Shopify.analytics.publish` only exposes the method to publish custom events."* — shopify.dev, Web Pixels API

> *"Code snippets can be used to bypass customer consent requirements, which violates the Shopify Terms of Service and can lead to legal liability for you."* — Shopify Help Center

Every event a marketing brief asks for — `view_item`, `add_to_cart`, `begin_checkout`, `purchase` — is emitted by **Shopify**, from a sandbox the theme cannot reach, in response to the storefront calls the theme already makes. The theme's entire contribution to measurement is to keep making those calls correctly, exactly once per customer action, and to stay out of the way.

Phase 17 (delivered 2026-09-25) therefore shipped **no tracking code**. Its deliverables are a measured absence, a standing set of prohibition tests, the Admin configuration the business must do itself, and — surfaced by the privacy question rather than the tracking question — a fix for a live stored-XSS vector in the cart.

Phase 18 re-ran the tracking, funnel, negative-control and escaping suites because it touched purchase surfaces. `tracking` still returns 31/31, NO TRACKING PRESENT.

### The measured absence, verified against the code

Confirmed by direct inspection of all 75 files in `god-squad-theme/` (the theme was 72 files at the end of Phase 17; Phase 18 added `snippets/pagination.liquid`, `assets/component-pagination.css`, `assets/component-container.css`).

| Platform | API surface present |
|---|---|
| Google Analytics (GA4 or legacy) | none |
| Google Tag Manager | none |
| Google Ads conversion | none |
| Meta Pixel | none |
| TikTok Pixel | none |
| Pinterest, Snapchat | none |
| Microsoft Clarity, Hotjar | none |
| Segment, Plausible, Matomo, PostHog | none |
| `dataLayer` | none |
| Error monitoring (Sentry, Bugsnag, Rollbar, Datadog, New Relic) | none |

**Hardcoded account identifiers: none.** No `G-`, `AW-`, `GTM-`, `UA-`, no Meta-shaped 15–16 digit literal, no TikTok-shaped literal. The single `UA-` substring in the theme is `layout/theme.liquid:32`, `<meta http-equiv="X-UA-Compatible">`.

**Third-party hosts: none.** The only absolute URL literal anywhere in the theme source is `http://www.w3.org/2000/svg`, the SVG namespace declaration on the nine `snippets/icon-*.liquid` glyphs — a namespace URI, not a network fetch. Every script and stylesheet URL is built by `| asset_url`, so it resolves to the store's own CDN.

**Every `<script>` in the theme, exhaustively — seven:**

| Location | What it is |
|---|---|
| `layout/theme.liquid:183` | one inline line: `document.documentElement.classList.replace('no-js', 'js')` |
| `layout/theme.liquid:184` | `header.js` via `asset_url`, `defer` |
| `layout/theme.liquid:191` | `cart.js` via `asset_url`, `defer` |
| `sections/main-collection.liquid:243` | `facets.js` via `asset_url`, `defer` |
| `sections/main-product.liquid:141` | `product.js` via `asset_url`, `defer` |
| `sections/main-product.liquid:519` | `type="application/json"` variant data block |
| `sections/main-product.liquid:551` | `type="application/ld+json"`, `{{ product | structured_data }}` |

**Absent from all five theme scripts:** `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`, `navigator.sendBeacon`, `new Image(`, `caches.open`, service-worker registration, and any off-origin `fetch`. There are exactly two `fetch` call sites, both same-origin: `cart.js:179` (URL built from `window.Shopify.routes.root`) and `cart.js:651` (`window.location.pathname + '?sections=' + …`). There is no `setInterval` anywhere — the five `setTimeout` calls are debounces and `transitionend` fallbacks. `window.Shopify` is read (`cart.js:105`) and never written. The theme creates one global, `window.GodSquad.cart` (`cart.js:938`). `Shopify.analytics` is never referenced.

**Correction to the Phase 17 text.** Phase 17 §13 states that "any `console` logging" is absent. The code carries two guarded diagnostic calls, and the code is the truth:

- `assets/cart.js:205` — `if (window.console && console.warn) console.warn('[god-squad] cart request failed', error);` on transport failure.
- `assets/product.js:45` — the same shape when the embedded variant JSON fails to parse.

Neither logs customer data, cart contents or a request payload. State the rule as what it actually is: **no customer or cart payload may be written to the console**; two guarded developer diagnostics exist and are permitted.

**Word matches that survive comment-stripping — two, both harmless and both still at the cited lines:** `sections/hero.liquid:224` ("…the worst pixel behind the heading measures 1.0:1…", overlay contrast help text) and `locales/en.default.json:70` (`"info_region": "Product details and purchase"`, a landmark label).

### The one load-bearing line

`layout/theme.liquid:127` emits `{{ content_for_header }}` once, unmodified, inside `<head>` — after the `{% style %}` block that carries the four `font_face` declarations and before `design-tokens.css`. Shopify documents it as required and warns it must not be parsed or altered.

**That single line is the theme's entire dependency for analytics, attribution and consent.** Do not split it, reorder it, wrap it, or run string operations over it. A standing assertion protects it.

### What a theme can and cannot publish

Shopify emits **exactly 15 standard events**:

```
page_viewed              product_viewed            collection_viewed
search_submitted         product_added_to_cart     product_removed_from_cart
cart_viewed              checkout_started          checkout_contact_info_submitted
checkout_address_info_submitted     checkout_shipping_info_submitted
payment_info_submitted   checkout_completed        alert_displayed
ui_extension_errored
```

There is **no `cart_updated`, no `cart_created`, no `variant_viewed`** — do not build a funnel that expects one. A pixel may subscribe in bulk via `all_events`, `all_standard_events`, `all_custom_events`, `all_dom_events`.

Five **DOM events** are available on the storefront — `clicked`, `form_submitted`, `input_blurred`, `input_changed`, `input_focused` — and are *not* available on customer-account pages or the order-status page.

A theme may publish **custom events only**, via `Shopify.analytics.publish`, prefixed (`my_app:event_name`). This theme publishes none, because it needs none.

**Why there is no `dataLayer`, and why there must not be one.** A `dataLayer` exists to feed GTM; GTM belongs in a pixel; a pixel cannot read the page. Under the Web Pixels API, **app pixels run in a strict sandbox implemented with web workers** — no `window`, no `document` — and **custom pixels run in a lax sandbox**, a sandboxed iframe where `window.location` returns the sandbox URL rather than the storefront's. A `dataLayer` on `window` is unreachable from either. Shopify prohibits the workaround directly: pixels cannot capture *"events from DOM scraping, metadata from DOM scraping, user information such as email and phone from DOM scraping"*.

### Purchase tracking

**A theme cannot fire a purchase event, and this one does not try.** `checkout_completed` fires *"once for each checkout, typically on the Thank you page"*. Three facts any duplicate-protection design depends on:

- **Upsells move it.** With post-purchase offers it fires *"on the first upsell offer page instead"*.
- **It can fail to fire at all.** *"If the page where the event is supposed to be triggered fails to load, then the `checkout_completed` event isn't triggered."* Under-counting is possible; over-counting is what Shopify prevents.
- **Refreshing the thank-you page does not re-fire it.** The guarantee is per checkout and it belongs to Shopify.

### Every legacy purchase-tracking mechanism is retired

All dates are in the past as of 2026-09-26. Any tutorial that tells you to paste a purchase tag into Additional Scripts, or to read `_landing_page` from `document.cookie`, describes a storefront that no longer exists.

| Mechanism | Status |
|---|---|
| `checkout.liquid` (Information, Shipping, Payment) | unsupported |
| `checkout.liquid` + Additional Scripts (Thank you, Order status) | **sunset 2025-08-28** |
| Script tags, Shopify Plus | **sunset 2025-08-28** |
| Script tags, non-Plus | sunset 2026-08-26 |
| `_landing_page`, `_orig_referrer`, `_tracking_consent` cookies | **removed 2025-09-15** |
| `_shopify_s`, `_shopify_y` cookies | **removed 2026-01-01** |

Shopify's own cookie-policy help page is **stale** and still lists the removed cookies. Where the help centre and the developer changelog disagree, the changelog is correct. The theme is asserted to read none of the six, and a grep confirms none appears.

### The consent model

**No consent work is required in the theme**, and the reason is structural: Shopify's pixels respect consent because Shopify runs them, and the theme has no tracking to gate. There is no banner to build, no gate to write, and no consent API to call.

Three prohibitions are enforced by the test suite rather than by good intentions, and all three hold in the code today:

1. **No analytics `<script>` in any Liquid file.** (See the exhaustive seven-script table above.)
2. **No call to `customerPrivacy.setTrackingConsent()`.** Consent must *"never [be] done automatically on behalf of the visitor"*. No reference to `customerPrivacy`, `setTrackingConsent` or `trackingConsent` exists anywhere in the theme.
3. **Nothing reads the six retired cookies.**

The prohibition suite was **negative-controlled**: 12 realistic violations were seeded into throwaway theme copies — GA4 and Meta in the layout, a TikTok pixel in a section, a `dataLayer` push from `cart.js`, `{{ customer.email }}` in the footer, an ID in `localStorage`, a pixel built with `new Image()`, a `sendBeacon` to an off-origin collector, a `console.log` of a payload, customer data in a cart attribute, Hotjar, a GTM container — and all 12 were caught. Two seeds exposed auditor bugs first: `rollbar` matched inside `scrollbar-gutter` and reported a CSS rule as an installed error monitor; and the host check read only `src`/`href` attributes, so it missed a seeded Meta Pixel entirely — because every real pixel injects its own `<script>` and therefore carries its host as a **string literal inside JavaScript**, which is precisely the case the check exists for. Keep that lesson: **an absence assertion nobody has seen fail is indistinguishable from a typo in a regex.**

### The theme's actual measurement job: one action, one call

The theme cannot emit an event, so it cannot emit a duplicate. What it *can* do is make Shopify emit one twice by making two storefront calls for one customer action. That was measured in a browser:

| Customer action | Shopify calls | Endpoint |
|---|---:|---|
| select a variant | **0** | — |
| set quantity to 2 | **0** | — |
| add to cart (one press) | **1** | `/cart/add.js` |
| open the cart drawer | **0** | — |
| close and reopen the drawer | **0** | — |
| increase a cart line quantity | **1** | `/cart/change.js` q=2 |
| remove the line | **1** | `/cart/change.js` q=0 |

The invariants that produce those numbers, and that must not be broken:

- **The drawer is rendered with the page and shown, never fetched.** `layout/theme.liquid:234` renders `{% section 'cart-drawer' %}` inside `{%- if settings.cart_type != 'page' -%}`. A drawer that fetched on open would make Shopify emit a cart event on every open.
- **Quantity changes are debounced at a hard 250 ms literal** — `QUANTITY_DEBOUNCE_MS = 250` at `cart.js:53`, applied in `queueChange` (`cart.js:717`). It is deliberately **not** a `--duration-*` motion token, because those collapse to 1 ms under `prefers-reduced-motion` and would turn the debounce off for the users most likely to press slowly. Five rapid presses send one request.
- **`queueChange` clears `pending[key]` before re-queueing**, so a removal cancels the queued change for that line rather than sending both.
- **The add path is guarded with `aria-busy`, never `disabled`** — disabling the focused element drops a keyboard user to `<body>`.
- **Mutations carry their own re-render in the same round trip.** `SECTIONS` is collected at init (`cart.js:70`): `['cart-icon-bubble']`, plus `cart-drawer` when the drawer exists, plus the cart page's section id on `/cart`. Every rendered number is the server's view of the cart after the change, never a figure the theme calculated.

#### Two events this theme's design affects

- **`cart_viewed` will fire rarely, by design.** It is documented as *"a customer visited the cart page"*, and the reference does not mention drawers, modals or overlays. This store is drawer-first, so `cart_viewed` fires only when someone reaches `/cart`. A funnel that expects `cart_viewed` between `add_to_cart` and `begin_checkout` will look broken and will not be. Expected, not a defect.
- **Whether `product_added_to_cart` fires for an Ajax add is undocumented.** The reference says only that the event *"logs an instance where a customer adds a product to their cart"* and is *"available on the online store page"*. It says nothing about Ajax versus form POST. This theme adds exclusively over `/cart/add.js`. **This is recorded as an unknown, not assumed either way, and it is the single highest-value thing to verify on the live store.**

### Event matrix

Every row is emitted by Shopify, not by the theme. "Theme role" is what the theme does to make the event possible and correct.

| Event | Trigger | Theme role | Frequency | Duplicate risk |
|---|---|---|---|---|
| `page_viewed` | any storefront page | none | 1 / page | none — Shopify owns it |
| `collection_viewed` | collection page renders | none | 1 / view | none |
| `product_viewed` | product page renders | none | 1 / view | none |
| `search_submitted` | search results render | one GET form, `q` + `type` | 1 / search | none |
| `product_added_to_cart` | add succeeds | exactly one `/cart/add.js` per press, double-submit guarded | 1 / add | guarded and measured |
| `product_removed_from_cart` | quantity → 0 | one `/cart/change.js`, pending change cancelled | 1 / removal | guarded |
| `cart_viewed` | **`/cart` page only** | drawer makes no call | rare — see above | none |
| `checkout_started` | customer enters checkout | native `name="checkout"` submit | 1 / entry\* | none |
| `checkout_completed` | thank-you page (or first upsell) | **none possible** | 1 / order | Shopify's guarantee |

\* every entry on Checkout Extensibility shops; first entry only otherwise.

There is deliberately **no row for filter clicks or keystrokes.** Neither is a standard event, and instrumenting them is explicitly out of scope.

### Attribution and UTM behaviour

**All three GET forms in the theme discard campaign parameters. This was measured, is real, and was deliberately left alone.**

| Form | File | Submits |
|---|---|---|
| collection sort + filters | `sections/main-collection.liquid:392` | `?sort_by=…` and/or `?filter.v.…` |
| header search panel | `sections/header.liquid:297` | `?q=…&type=product` |
| search page | `sections/main-search.liquid:152` | `?q=…&type=product` |

The mechanism is that **a GET form discards its action's query string and rebuilds it from its own fields** — the same mechanism Phase 13 relied on to drop the `page` parameter so any filter or sort submission returns to page 1.

**Why this is harmless, and why "fixing" it would be worse.** Verified against primary sources:

- Shopify records `landingPage` and `utmParameters` **server-side at the session's first request**.
- **GA4 fixes session source at session start** and does not open a new session on a mid-session source change. *Universal Analytics did the opposite, which would have made these forms genuinely destructive — but UA is retired. Reasoning from UA intuition here is exactly the stale-platform-assumption class this project has been bitten by.*
- Meta has already written `fbclid` into `_fbc` with a 90-day life.
- **Dawn behaves identically** — only `q` and `options[prefix]` survive its facet forms. No Shopify documentation asks for UTM preservation on filter forms.

Carrying UTM through internal forms would make internal navigation look like campaign traffic and create self-referrals. **The one genuine loss** is a narrow sequence: land with UTM → sort → idle past the 30-minute session timeout → re-enter from the now-stripped URL. That second session is attributed to direct.

#### The reserved-parameter rule

Shopify special-cases **`ref`, `source` and `r`** storefront-wide as the marketing referral code, and the value lands in every order's conversion detail. **A theme form field named `ref`, `source` or `r` would silently overwrite a real attribution on every submission.** That is now asserted.

The complete set of `name=` attributes in the theme today: `add`, `checkout`, `description`, `id`, `note`, `options[prefix]`, `q`, `quantity`, `sort_by`, `type`, `update`, `updates[]` (form fields), plus `viewport`, `theme-color`, `twitter:card`, `twitter:title`, `twitter:description` (`<meta>` names, not fields). None is reserved. Facet field names are interpolated from Shopify's own `filter.param_name` / `value.param_name`, so they cannot collide by construction; the only literals are `filter.v.price.gte` and `filter.v.price.lte`.

### UTM and campaign naming conventions

Conventions only — **no campaign was created or launched.**

```
utm_source    the platform            facebook | instagram | tiktok | google | email
utm_medium    how it was paid for     paid_social | organic_social | cpc | email | referral
utm_campaign  {objective}_{subject}_{yymm}    launch_thefaithful_2610
utm_content   the creative            video01 | carousel_a | static_gold
utm_term      keyword, paid search only

ad platform   {platform}_{objective}_{subject}_{audience}_{creative}_{yymm}
              meta_conv_thefaithful_retarget_video01_2610
```

Rules that keep the data usable: **lowercase everywhere** (GA4 is case-sensitive, so `Facebook` and `facebook` become two sources); underscores, not spaces; **never tag an internal link**; and never use `ref`, `source` or `r` as a parameter name.

### What the theme *does* publish for marketing

Two things, both built from Shopify objects with no written marketing copy anywhere.

**`snippets/meta-social.liquid`** (added Phase 16) emits `og:site_name`, `og:url`, `og:title`, `og:type`, a guarded `og:description`, and an `og:image` resolved through a four-step guarded chain — `product.featured_media.preview_image` → `collection.featured_image` → `settings.share_image` → `settings.logo`. A store with no image at any level emits **no `og:image` at all** rather than a URL that 404s. Rules encoded in that file:

- The image is served at `image_url: width: 1200`, not the original. `og:image:width` is the **literal `1200`**; height is derived as `image.height × 1200 ÷ image.width`, guarded on `share_image.width > 0 and share_image.height > 0`. **Never derive it from `aspect_ratio`** — that property is not populated on every image drop, Liquid treats the missing value as `0`, and the first version threw a division by zero in the `<head>` of all seven templates on every page.
- **No `twitter:image`** — X falls back to `og:image` for a `summary_large_image` card, so a second copy is dead weight. `twitter:card` is `summary_large_image` when an image resolved and `summary` otherwise.
- **No `og:price`** — `structured_data` already publishes price and availability in the format search engines consume.

**Product JSON-LD** is `{{ product | structured_data }}` at `sections/main-product.liquid:552` — Shopify's own filter, emitted once theme-wide, never hand-built, so price, availability and SKU come from the platform and cannot drift.

**Organization and BreadcrumbList are deliberately not implemented.** Organization needs the social URLs the business has not supplied, and *"a `sameAs` array that is empty half the time is worse than no block"*. BreadcrumbList has no real navigation hierarchy to describe, and a fabricated trail is precisely the fake structure this project forbids. Revisit Organization once real social URLs exist.

### Marketing readiness

The store is ready for paid acquisition in the only sense a theme can be: nothing in it will break, duplicate or misattribute a campaign.

- **Meta, Google, TikTok** — install the channel app; the pixel and the server-side integration arrive with it. **At most one app per platform.** Nothing to change in the theme.
- **Retargeting** — product viewers, cart abandoners and checkout abandoners all derive from `product_viewed`, `product_added_to_cart` and `checkout_started`, which fire without theme involvement.
- **Abandoned cart** — Shopify's native abandoned-checkout emails (*Settings › Notifications*, plus *Settings › Checkout* for timing). **Do not build one.**
- **Email** — Shopify Email, Klaviyo and Mailchimp all integrate as apps. **The theme has no newsletter form.** Phase 1 recorded FOOT-03 as BUSINESS DECISION REQUIRED and it still is.
- **Social profiles** — two settings in the `Social` group of `config/settings_schema.json`, both `"type": "url"`: `social_facebook_url` and `social_instagram_url`. Both carry the info string *"No address has been supplied for the brand yet."*, neither appears in `settings_data.json`, each link renders only behind `{%- if … != blank -%}` (`sections/footer.liquid:306`, `:313`), and the whole `footer__social` nav is suppressed when both are empty. **No profile was invented.** There is no TikTok setting because no TikTok profile was supplied. No `target="_blank"` on either link — a change of context is not the theme's decision to make.
- **Error monitoring** — none present, and not recommended at this size. The console suite (38 pages, 0 errors) is the current substitute. If it is ever wanted, **it belongs in a pixel or an app, not in `theme.liquid`.**

### The only theme code Phase 17 changed

Two `| escape` filters, both a stored-XSS fix, both surfaced by the privacy question rather than the tracking work. Both confirmed present today:

| File | Change |
|---|---|
| `snippets/cart-line-item.liquid:142` | `{{ property.first \| escape }}: {{ property.last \| escape }}` |
| `snippets/cart-note.liquid` | `<textarea …>{{ cart.note \| escape }}</textarea>` |

The rule: **Shopify Liquid does not escape output.** A line item property is supplied by whoever posted to `/cart/add.js`, and the cart note is settable through `/cart/update.js`, so both are untrusted input however they arrived. Rendered with `</textarea><img src=x onerror=…>` and `<img src=x onerror=…>` respectively, both broke out and produced a live element carrying an event handler. Use `escape`, **not `escape_once`** — the stored value is plain text, and `escape_once` would leave a customer-typed `&amp;` rendering as an entity. Verification renders real payloads through the real snippets rather than grepping for the filter.

This brought the theme from 27 to 30 `| escape` filters. The one path that deliberately does not escape is `search.terms` passed into `| t` at `sections/main-search.liquid:239` and `:263`: Shopify's storefront locale documentation states translated content is escaped by default and the only opt-out is the `_html` key suffix, which neither key carries, so escaping the argument as well would print entities instead of the customer's words. The attribute-context use at `:211` **does** carry `| escape`, because an attribute value is the one place on that page where nothing else escapes it. Phase 13 recorded the `| t` interpolation behaviour as documented-but-not-live-confirmed.

### What a future integration would have to do

1. **Install one channel app per platform you actually intend to spend on.** *Google & YouTube* covers GA4 **and** Google Ads conversion tracking from one purchase signal — there is no separate Ads tag to add and nothing to de-duplicate, provided nobody also pastes an `AW-` tag. *Facebook & Instagram* registers an app pixel and handles the Conversions API server-side. *TikTok* likewise. **Add no theme code for any of them.**
2. **Paste nothing into the theme and nothing into Additional Scripts.** Additional Scripts was sunset 2025-08-28. A `gtag`, `fbq` or `ttq` snippet in `theme.liquid` runs outside the consent framework, which Shopify states violates its Terms of Service. A second `fbq` alongside the app pixel double-counts every event, including purchases — the most common tracking defect on a Shopify store.
3. **If you need an event Shopify does not emit**, the only sanctioned route is: the theme publishes a prefixed custom event via `Shopify.analytics.publish('my_app:event_name', payload)`, and a custom pixel subscribes to it. Nothing goes on `window` — a custom pixel runs in a sandboxed iframe and cannot read the page, and an app pixel runs in a web worker with no `window` or `document` at all.
4. **Do not build a `dataLayer`, a consent banner, an abandoned-cart flow, a purchase tag, or a cookie reader.** Each of those is either unreachable from a pixel, owned by Shopify, or built on a mechanism that has already been sunset.
5. **Keep the prohibition tests running.** They are the reason the next developer cannot quietly paste a `gtag` snippet into `theme.liquid` and break consent compliance. If you add a suite, negative-control it by seeding the violation and confirming the failure before trusting the pass.

### Shopify Admin actions required

None of these is theme work.

1. **Check *Settings › Customer events* before installing anything.** There may already be an app pixel registered in an Admin nobody on this project has seen.
2. **Install the channel apps** you intend to spend on — at most one per platform.
3. **Check *Settings › Customer privacy*** for banner state and configured regions. Confirm whether Shopify Network Intelligence is on; if it is, Shopify's Consumer Privacy Policy should be linked from your own privacy-policy page (ordinary page content, no theme code).
4. **Take Philippine RA 10173 / NPC applicability to counsel.** Shopify publishes no APAC-specific consent guidance; this is a legal question, not a technical one.
5. **Verify `product_added_to_cart` fires on an Ajax add.** One add to cart with the pixel debugger open settles it. This is the highest-value fifteen minutes in this section.
6. **Supply the two social profile URLs** if the footer social row is wanted, and the `settings.share_image` for social sharing. Nothing is invented on the business's behalf.
7. Carried forward: Search & Discovery filters (Phase 13), checkout branding (Phase 14), confirm the customer-account system (Phase 15), `theme_support_email` and `theme_documentation_url` (Phase 16).

### Open items and what was not measured

- **No live store existed.** "Not configured" for GA4, Meta, TikTok and Google Ads means **not in the theme** — it is not a statement about the Admin.
- **No test purchase was made.** There was no store, no checkout and no payment method. `checkout_completed` is documented, not observed.
- **Ajax `product_added_to_cart` is undocumented** and this theme adds exclusively over Ajax. Recorded as an unknown.
- **`cart_viewed` will be rare** because the cart is a drawer. Expected, not a defect.
- **Shopify's own cookie documentation is stale.** Follow the developer changelog.
- **Two Theme Check offenses remain, both business information**, carried from Phase 16: `theme_support_email` and `theme_documentation_url` are absent from the `theme_info` block, which today carries only `theme_name` ("God Squad"), `theme_version` ("0.5.0") and `theme_author` (`config/settings_schema.json` lines 2–7). They were omitted rather than filled with a fabricated URL.
- **Safari untested.** Browser suites were green in Edge and Chrome only, as in every prior phase.
- **Give attribution two weeks before judging it.** `momentsCount` returns null while processing, and the admin conversion summary *"might take up to 48 hours to display"*. QA that checks an order seconds after placing it produces a false negative.

Phase 17 closed with **992 assertions, 0 failures** (its own suites: `tracking` 31, `negctl` 12 seeded, `funnel` 8, `escaping` 7, `utm` 6 measured), and the theme's analytics surface has not changed since.

---

## QA harness and test inventory

### Where the harness is, and the first thing to do about it

There is no test code inside the theme. Every suite, every fixture and the Liquid engine itself live outside the project, in a **session-scoped scratchpad**:

```
C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\
  de238d03-508d-43ce-a377-210f71ff0033\scratchpad\
```

The project directory (`C:\Users\TEST\OneDrive\Documents\GodSquad Website`) **is not a git repository**, and the scratchpad is under `Temp`. 192 Python files across `phase2/`…`phase18/` and `design/`, plus `node_modules/@shopify/theme-check-node`, are the only evidence that any of the numbers in this manual were ever measured. **Before the Shopify integration starts, copy the scratchpad into the project and put both under version control.** Losing it does not break the theme; it makes every figure in this manual unreproducible and hands the next phase a 75-file theme with no regression net.

There is **no single runner**. You invoke suites individually with `python <path>`. Two directories are load-bearing:

| Path | Role |
|---|---|
| `scratchpad/phase9/miniliquid.py` | the current Liquid engine — 1,139 lines, 43,374 B |
| `scratchpad/phase9/build.py` | mock Shopify data + page assembly — 674 lines, 31,969 B |
| `scratchpad/phase8/validate.py` | the canonical structural validator — 28,527 B, 199 checks |
| `scratchpad/phase9/site/` | fixture site served on **port 8809** — 38 pages |
| `scratchpad/phase8/site/` | fixture site served on **port 8808** — 22 pages |

Later suites bind to the core explicitly — `sys.path.insert(0, os.path.join(HERE, '..', 'phase9'))` then `import build` — in `phase15/accounts.py`, `phase16/seo.py` and `phase17/escaping.py`. Older `miniliquid.py` copies still sit in `phase6/` (22,487 B), `phase7/` (22,805 B) and `phase8/` (40,705 B); **only `phase9/` is current.** Do not run a phase-6 or phase-7 validator against today's theme and treat its failures as defects — Phase 8 §12 already recorded three false failures of exactly that kind from Phase 7's validator (`cart-icon-bubble.liquid no schema`, and two `cart.item_count` failures caused by a locale flattener that did not understand `one`/`other` pluralisation).

### The Mini-Liquid engine: what it is

A strict Liquid interpreter written for this project, which renders **the real `.liquid` files** against mock Shopify data. No fixture HTML is hand-written anywhere in the project. Its defining property is strictness: an unknown tag, an unimplemented filter, a missing translation key or malformed syntax **raises `LiquidError`** rather than rendering empty — which is the opposite of what real Liquid does, and is the point. Real Liquid silently prints nothing for an undefined variable; that is precisely the failure mode Phase 0 identified as making a copy-and-adapt migration unsafe.

Tags implemented: `comment`, `raw`, `schema`, `style`, `assign`, `capture`, `echo`, `increment`/`decrement`, `liquid`, `render`, `include`, `section`, `sections`, `if`, `unless`, `for`, `case`, `break`, `continue`, `form`, `paginate`. Roughly 70 filters, including the ones that matter for this theme: `image_url`, `image_tag`, `t`, `font_face`, `font_modify`, `money`/`money_with_currency`/`money_without_trailing_zeros`, `structured_data`, `asset_url`, `stylesheet_tag`, `script_tag`, `payment_button`, `video_tag`/`media_tag`/`model_viewer_tag`, `newline_to_br`, `handle`, `within`, `weight_with_unit`, `highlight_active_tag`, `inline_asset_content`, `metafield_tag`.

Two stubs are deliberately faithful rather than convenient, and both exist because a lazy stub would let the harness pass markup Shopify rejects:

- **`{% form %}` emits the platform's hidden inputs**, not just a `<form>` element. Rendering the element alone would have hidden the Phase 8 defect where `{% form 'product' %}` emits `product-id` — which is not `name="id"` and adds nothing to a cart.
- **`font_modify` returns `nil` when the family has no such variant.** The fixture declares which weights exist via a `variants` list, and anything outside it comes back nil. That nil case is the whole reason callers must guard `font_modify`, and Phase 16's four `@font-face` declarations depend on the guard.

### What the harness does *not* model

This list is the boundary of every claim in this manual. Anything outside it was not verified locally and must be verified on a development store.

| Not modelled | Consequence for the integration |
|---|---|
| `{% sections %}` returns `''` | the header group and footer group are **never rendered as groups**. `sections/header.liquid`, `cart-drawer.liquid` and the footer are rendered individually and assembled by `build.py`'s `write()`. Group ordering, `enabled_on: {groups: [...]}` enforcement and group-level JSON are untested. |
| `image_url` ignores `width:` | it returns the mock `src` unchanged and records `(src, width)` in `engine.image_requests`. The harness verifies that the theme *declares* the right `widths`/`sizes`/`loading`/`fetchpriority`; it never verifies that the CDN serves a matched candidate, and it cannot see the CDN's no-upscale behaviour. |
| Section Rendering API | `phase8/interact.py` replaces `window.fetch` before `assets/cart.js` runs with a stub that answers the way the Ajax Cart API documents — items-only body from `/cart/add.js`, a `sections` object keyed by section id with the `shopify-section` wrapper, a 422 body of `{status, message, description}`, `null` for a missing section, and a rejected promise for transport failure. Every request is recorded so tests assert on what was **sent**. Real `?sections=` responses have never been seen. |
| `content_for_header` | `phase9/layout.py` injects a placeholder. The real payload — analytics, consent, the `<shopify-account>` upgrade script — is absent. This is why Phase 15 §18 records that the harness *can never* test the account component. |
| `{% increment %}` / `{% decrement %}` | no-ops returning `''`. |
| Collection filtering | `filters` come from four hand-built fixtures (below). Real filtering needs the Search & Discovery app on a live store. |
| Merchant photography | the harness serves six mock images (`site/img/cap.webp`, `hero.webp`, `hoodie.webp`, `logo.png`, `story.webp`, `tee.webp`). Image **bytes**, crops, focal points and art direction are not assessable — Phase 18's preface states this as the reason the image half of a visual audit was not done by anyone. |
| Web fonts | no font files, so **font-swap CLS cannot occur** and is reported as unmeasurable rather than scored zero. |
| Timings | TTFB, FCP, field LCP and field INP. No Lighthouse (not installed, no network). No number is claimed anywhere. |

The mock data lives only in `build.py`. **Nothing in the theme knows the harness exists** — no test hook, no fixture flag, no `data-test` attribute.

### How the engine grew, and which phase added what

Useful when a suite from an early phase suddenly raises: the tag it needs may post-date it.

| Phase | Added |
|---|---|
| 6 | the engine itself (`phase6/miniliquid.py`, ~600 lines), `build.py` driving 15 static pages |
| 8 | `{% form %}`, `{% case %}`, 28 filters, `#{}` handling, translation interpolation and pluralisation, a `structured_data` stand-in |
| 10 | `{% paginate %}` (two of the five new surfaces could not render at all without it); `font_face` made to emit a **real** `@font-face` rule; asset copying and translation scanning changed from hand-written lists to **discovery** |
| 13 | four filter fixture states |
| 9 | the undefined-custom-property check taught to honour same-file definitions |

Two of those are worth restating as rules rather than history. **`font_face` was a stub returning `''`, and the first version of `layout.py` passed with the P0 bug present** — a test that cannot fail proves nothing. **Asset copying was a hand-written list, so the Phase 10 surface stylesheets were never copied into the harness**, and the first responsive run measured the new surfaces *unstyled* and reported 17px footer links and a 19px select as real defects; with the CSS actually served they measured 24px and passed. Phase 10 §7 states the resulting rule: *every "defect" a harness reports is worthless until you have proved the harness is serving what the theme references.*

### Harness defects that produced plausible wrong numbers

These are recorded because a wrong number that looks right is more dangerous than a crash. Every one was caught by a measured result contradicting arithmetic, never by reading code.

| Defect | The wrong answer it gave |
|---|---|
| `break` inside `for` discarded text rendered before it | the product-card swatch row looked absent while the Liquid was correct |
| a CSS override injected outside any rule block | the portrait-ratio test rendered square — a false pass on the only evidence for `product_image_ratio` |
| `#{}` interpolation unimplemented | the header logo drew at 133px and the header appeared to overflow at 320px. **The theme never had that defect** |
| `blank` did not compare equal to itself | `assign x = blank` then `if x != blank` took the true branch; the quantity input rendered `max=""` |
| `read_probe.py` parsed a dump already on disk | reported the **previous** build's geometry after an edit. Fixed with `run_probe.py`, which regenerates the dump on a throwaway browser profile |
| `http.server` answers `If-Modified-Since` at one-second granularity | rewriting a probe filename inside the same second returned a 304 and the previous page's geometry. Every reading now writes a unique filename |
| `image_tag` did not emit `width`/`height` attributes | hid the defect that made every cart line 948px tall |

### Measurement technique: the standing rules

Violate any of these and the number you get will be confident and wrong.

1. **Capture through an iframe of the exact target CSS size, then crop.** Headless Edge on Windows will not lay out below roughly **492 CSS pixels**, and `--screenshot` crops or scales to the requested window size rather than re-laying out. A `--window-size=375,760` request produced a 375px-wide PNG of a **492px-wide layout**; at 768 it produced a 768px PNG of a 744px layout. Verified by rendering a page that prints `window.innerWidth` with a 50% colour split: at `--window-size=375` it reported `innerWidth=492` with the split at x=246; through the iframe wrapper it reports 375 with the split at x=187. Established Phase 5, re-confirmed every phase since. Headless `--screenshot` **never** matches `--window-size` at any width.
2. **Verify the capture contains the photograph before measuring it.** Large WebP renders occasionally miss the screenshot deadline; a capture that missed is silently blank in the region you are about to sample.
3. **Disable transitions before measuring.** Headless virtual time does not advance transform transitions, so an un-disabled panel reports `translateX(-100%)` forever, and a transitioned property reads as its **start** value if read in the same frame. Recorded in Phase 4, forgotten by Phase 18's chevron probe, which first reported the filter chevron as unchanged after flipping `[open]`.
4. **Use a `Range` over the text node, not `getClientRects()` on the element.** `getClientRects()` on an atomic inline returns **one** rect however many lines its content occupies. Two Phase 18 probes reported the cart title as "1 line" and "2 lines" from the same element; the Range method produced the real 14.0px vs 17.4px leading measurement.
5. **Measure computed styles in a browser, not strings in a stylesheet.** *String-matching CSS cannot verify the cascade — only a browser can answer which rule won.* `catalog.py` confirmed the secondary image's rule *said* `opacity: 0` while a higher-specificity sold-out rule quietly repainted it to `0.6`. `phase9/cardcascade.py` exists for this and is negative-controlled: without the fix the sold-out secondary computes `0.6`, with it `0`.
6. **Render a snippet through a section that uses it.** `cardcascade.py`'s first run reported 900px stacked images — the shape of *no stylesheet*. The card's CSS is linked by the **sections** that use the card, not by the snippet.
7. **Confirm the fixture renders the element.** Phase 9 measured hero CTA geometry against a fixture where `templates/index.json` ships `button_label` with no `button_link`, so `has_cta` is false and **no button renders at all**. `site/home-cta.html` exists for this.
8. **Strip comments before asserting on source.** A test that greps a file will match the file's own prose. Phase 13's "no hardcoded option parameter" and "does not use the cart's lock" assertions both initially failed against comments explaining the very rule being asserted.
9. **Baseline and diff.** Phase 12 captured a `sizes` baseline across 21 configurations *before* refactoring `grid-sizes.liquid` and diffed after — which caught a malformed output caused by single-line `comment … endcomment` inside a `{% liquid %}` block, where every line is its own statement and a `%}` inside prose terminates the enclosing tag.
10. **A "nothing moved" result may mean the rule never applied.** Phase 18's blast-radius probe reported no change from the line-height fix; a negative control showed the rule *had* applied but the fixture's titles did not wrap at that width. Without the control the conclusion was backwards.
11. **Do not measure CLS with synthetic clicks.** `dispatchEvent` does not set `hadRecentInput`, so shifts you cause by opening a drawer score as load instability. An early reading put the product page at 0.0035 and the cart at 0.0036; load and interaction shift are now measured separately.
12. **Do not measure LCP with `PerformanceObserver` here.** It named the collection page's largest paint as the **78px header logo**. Replaced by a static eager/lazy/`fetchpriority` attribute audit, which is what actually decides LCP on a real store.
13. **Watch for cross-origin `contentDocument`.** Pages on the second port are cross-origin; `contentDocument` threw and the `catch` marked every selector as seen, so CSS coverage reported 100% including two deliberately dead selectors. The same pass also split `:where(a, button)` on its internal commas and took only the last line of multi-line selector lists.
14. **`render` inside a `{% liquid %}` block is a bare statement with no tag around it.** Phase 16's reference resolver called `grid-sizes.liquid` an orphan because of this.
15. **Negative-control every assertion, and absence assertions especially.** *An absence assertion that has never been seen to fail is indistinguishable from a typo in a regex.* `phase15/negctl.py` seeds 22 violations into a throwaway copy of the theme, one at a time, and requires the suite to catch each; `phase17/negctl.py` seeds 12. `phase9/editor.py` installs a counting shim on `EventTarget.prototype` before any theme script runs, so it can measure net listeners bound to `window` and `document` by type — with the teardown disabled it reports *"html still carries menu-open, so the page is stuck."* That shim caught a defect the first fix missed: `initHeader` re-bound the in-subtree toggle, so one click opened the menu three times.
16. **`negctl.py` caught its own blind spot.** Three `accounts.py` assertions read a *pre-built* harness page, so a seed that changed the theme never reached them — one genuinely broken theme (an account control stripped of its shared class) passed clean. The suite now renders the header **from the theme under test**, which makes every markup assertion seed-sensitive.

### The trap that is live today: a browser suite with no reading prints a pass

Re-running the suites on 2026-09-26 surfaced this, and it is the single most important operational fact in this section. **Headless Edge `--dump-dom` produces no output in this environment.** Verified against a trivial local file with `--headless=new`, `--headless=old` and `--headless`: all three return zero bytes, exit 0.

Several browser suites do not distinguish "no measurement" from "pass":

- `phase18/chevron.py` produced zero rows and printed `OVERALL: *** 0 disclosure(s) still wrong:  ***`.
- `phase18/coherence.py` printed `NO READING from port 8809` / `NO READING from port 8808`, then a full table of zeros and `roles with drift: 0`.
- `phase14/notes.py` printed `NO READING from c-noted.html` and `0 assertions, 0 failed` because its DOM dump was absent.

**Rule: before believing any browser-driven result, grep the output for `NO READING` and check the assertion count is non-zero.** `phase18/chevron.py` also starts its own `http.server` with `Popen` and launches Edge immediately with no readiness wait; a slow start yields an empty dump and a green verdict.

### Contrast measurement: two methods, and when each applies

| Method | Used where | Why |
|---|---|---|
| **Per-pixel sampling** | Phase 5 hero (40 measurements, 8 widths), Phase 7 Our Story (48 measurements, 6 roles × 4 widths × 2 surfaces) | the copy sits over a photograph, so the backdrop is only knowable from pixels. Two renders per width: the page as shipped, and the same page with the text elements set to `visibility: hidden`. For every pixel a glyph touches, the backdrop is read from the text-hidden capture and measured against the element's computed colour |
| **Exact composite from computed styles** | Phase 8 onward — `phase8/contrast8.py`, now **73 measurements** | the product page and cart are flat surface tokens, so the effective background composites exactly from computed styles. *That is stronger evidence, not weaker — there is no sampling error in it* |

Pixel sampling reports two figures per element and both are recorded: **glyph worst** (the darkest-contrast pixel under an actual glyph — the WCAG-relevant number) and **box worst** (the worst pixel anywhere in the element's block box, including where there is no text today — the headroom for a longer merchant heading, and the stricter figure). Each role is reported with the size and weight it renders at, because SC 1.4.3's threshold depends on them: 4.5:1 normal, 3:1 for large (24px, or 18.66px at 700+).

### Theme Check

Theme Check **runs, and always could**. Every phase from 10 to 15 reported it unavailable "because Shopify CLI is not installed". That was true of the CLI and false of the checker: `@shopify/theme-check-node` — the engine the CLI wraps — has been in `scratchpad/node_modules` since Phase 10. The Phase 10 runner pointed at the **project** root, which stopped being the theme root the moment Phase 10 moved the theme into `god-squad-theme/`. It had been scanning a directory with no theme in it and reporting zero offenses for three phases.

```
cd scratchpad
node phase16/themecheck.mjs          # default config
node phase16/themecheck.mjs --all    # extends: theme-check:all, ignoring node_modules
```

`ROOT` is hardcoded in `themecheck.mjs` to the absolute `god-squad-theme` path — **update it if the theme moves.** Re-run today:

| Config | Files scanned | Checks | Offenses |
|---|---:|---:|---|
| default | 50 | 84 | **2** — 2 × `ERROR ValidJSON` |
| `theme-check:all` | 50 | 84 | **6** — 4 × `ERROR AssetSizeJavaScript`, 2 × `ERROR ValidJSON` |

The two `ValidJSON` errors are **business information, not code**: `config/settings_schema.json:2` is missing `theme_support_email` and `theme_documentation_url`. Those are distribution metadata for themes shipped to other merchants; the project chose bespoke in Phase 15, so they have no functional effect. Supply them and the default config is clean.

`AssetSizeJavaScript` fires at `layout/theme.liquid:184`, `layout/theme.liquid:191`, `sections/main-collection.liquid:243` and `sections/main-product.liquid:141`. It is `assets/cart.js`, quantified by `phase16/weight.py`:

| Script | raw | gzip | comments stripped, gzip |
|---|---:|---:|---:|
| `cart.js` | 39,750 | **12,073** | 4,930 |
| `header.js` | 13,963 | 4,319 | 2,091 |
| `product.js` | 18,096 | 5,597 | 2,863 |
| `facets.js` | 10,937 | 3,838 | 1,535 |

Shopify's threshold is 10,000 B compressed per page-load script. The threshold is **not** reachable by deleting prose — 4,930 B stripped proves the comments are not the problem — so the answer recorded is a minification step at deploy, not a restructure of tested cart code. Phase 16's reasoning stands: *"restructure the cart with import-on-interaction" is the wrong response to 7 KB of documentation on a theme whose total JavaScript is 24 KB gzipped with no dependencies.*

### Fixtures

Fixture pages are built by `build.py` into two site roots, served by `python -m http.server` on the ports the suites hardcode.

**Port 8809 → `phase9/site/` (38 pages).** `home`, `home-cart`, `home-cta`, `home-one`, `home-three`, `home-eight`, `home-reordered`, `hero-cta`, `hero-full`, `hero-large`, `p-single`, `p-multi`, `p-sizes`, `p-soldout`, `p-long`, `p-minimal`, `p-carousel`, `p-details`, `p-ink`, `p-nosticky`, `p-rule`, `c-empty`, `c-one`, `c-many`, `c-noted`, `c-noview`, `c-page-empty`, `c-page-many`, `c-page-note`, `s-collection`, `s-collection-empty`, `s-collection-filters`, `s-collection-filtered`, `s-search`, `s-search-none`, `s-page`, `s-404`, `frame`.

**Port 8808 → `phase8/site/` (22 pages)** — the Phase 8 product-and-cart set, including `c-note` and `p-nodrawer`, which `phase9/site` does not carry.

Filter fixtures (`phase13_fixtures.py`, consumed by `phase9/facets.py`) are four states, and **every field in them is one shopify.dev documents; nothing is invented**:

| Fixture | Covers |
|---|---|
| `FILTERS_NONE` | no filters configured in admin — the section must render nothing and must not load `component-facets.css` or `facets.js` |
| `FILTERS_ALL` | `list` × 2 (one with swatches), `boolean`, `price_range` — every type the API has |
| `FILTERS_ACTIVE` | the same, with values applied and a price floor set |
| `FILTERS_DEGENERATE` | a one-value group, which is not a choice and must be dropped |

Phase 12's `cardcascade.py` composes a fixture the shipped set does not contain — a sold-out product with two images — from `P_MULTI` by marking its variants unavailable. The fields are the ones Shopify itself sets; nothing is fabricated.

### Suite inventory and current pass counts

Re-run on **2026-09-26** against the 75-file theme. "Today" records what I observed in this environment; where the browser leg is dead the last recorded figure is given and labelled.

**Static suites — Liquid, markup, JSON, CSS, JS source. All re-ran and passed today.**

| Suite | Path | Covers | Today |
|---|---|---|---:|
| `validate.py` | `phase8/` | structure, schemas, tokens, translations both directions, banned constructs, source-of-truth prohibitions, the product-form and cart contracts, and **44 original prototype files byte-identical** | **199/199** |
| `layout.py` | `phase9/` | the real `layout/theme.liquid`, parsed with a model of the HTML "in head" insertion rule | **19/19** |
| `surfaces.py` | `phase9/` | the five Phase 10 surfaces (collection, page, 404, search, footer) in every state | **41/41** |
| `catalog.py` | `phase9/` | card, SKU, quick-add, low stock, the collection empty test | **55/55** |
| `facets.py` | `phase9/` | filtering against the four fixture states; the lifecycle contract | **62/62** |
| `settings.py` | `phase9/` | every Phase 11 setting, rendered both ways | **28/28** |
| `cartdoc.py` | `phase14/` | cart markup and platform contract, data hygiene across all seven cart Liquid files | **85/85** |
| `accounts.py` | `phase15/` | the `<shopify-account>` entry point, and the absences (no `templates/customers/`, no `order.*`, no `fulfillment`, no customer field read) | **52/52** |
| `hygiene.py` | `phase15/` | placeholder/demo/private-data patterns across shipping code | **0 findings** |
| `tracking.py` | `phase17/` | every tracking platform, hardcoded IDs, third-party hosts, the six retired cookies | **31/31, NO TRACKING PRESENT** |
| `escaping.py` | `phase17/` | XSS: `\| escape` on cart line-item properties and the cart note, verified by re-rendering real payloads through the real snippets | **7/7** |
| `seo.py` | `phase16/` | head, social metadata, fonts, heading structure | **52/52** |
| `images.py` | `phase16/` | `width`/`height`, `srcset` with matching `sizes`, no 3× overshoot, non-stuffed `alt`, video via Shopify filters with `autoplay: false` | **54/54** |
| `refs.py` | `phase16/` | every `asset_url`, `render`, `section`, translation key and internal href resolves | **10/10** |
| `weight.py` | `phase16/` | requests and bytes per surface; the `AssetSizeJavaScript` quantification | measurement, ran |
| `hovergate.py` | `phase18/` | every hover rule inside `@media (hover: hover)` | **29 rules, 29 gated, 0 ungated** |
| `deadcode.py` | `phase18/` | orphan classes and unread `data-` hooks — **candidates only** | 28 markup-orphan classes, 2 css-orphan, 25 unread hooks |
| `themecheck.mjs` | `phase16/` | Shopify Theme Check | **2 default / 6 all** |

**Negative-control harnesses.** Not run today (they write a throwaway theme copy). Last recorded: `phase15/negctl.py` **22 seeds, 22 caught**; `phase17/negctl.py` **12 seeds, 12 caught**; `phase16/refs.py` **+4 seeded breakages caught**.

**Browser-driven suites — headless Edge. Cannot be re-run in this environment (`--dump-dom` returns empty).** Figures are as last recorded.

| Suite | Path | Covers | Last recorded |
|---|---|---|---|
| `interact.py` | `phase8/` | cart drawer against the stubbed Ajax Cart API: open, close, Escape, overlay, focus, `inert` through the section wrapper, scroll lock, request URL/body/headers/sections, the section swap, the debounce, the line key, the minimum, removal, a 422, transport failure, a null section, the visible failure line, the in-dialog announcement | 49 |
| `interact_cartpage.py` | `phase8/` | no drawer on `/cart`, its own render hook and section id, `updates[]` realignment, focus to the `h1` | 17 |
| `interact_product.py` | `phase8/` | variant resolution, legends, URL, history, availability, unavailable combinations, the sold-out label, the gallery rail, the hash | 26 |
| `contrast8.py` | `phase8/` | contrast composited from computed styles | 73 measurements, 73 pass |
| `console.py` | `phase8/`, `phase9/` | console and Liquid errors | Phase 16: 0 errors / 38 pages. **Phase 18: 0 errors / 22 pages** — a reduction the report does not explain |
| `respond.py` | `phase9/` | overflow, target size, grid ladder, panel geometry | 0 hard problems; 17–18 pages |
| `editor.py` | `phase9/` | section load/unload lifecycle, net listener accounting via the `EventTarget` shim, scroll-lock release | 10/10 |
| `cardcascade.py` | `phase9/` | computed card styles, sold-out secondary-image cascade | 10/10 |
| `cartqa.py` | `phase14/` | five rapid quantity presses, two lines at once | 14 |
| `notes.py` | `phase14/` | order note save-on-change, geometry at 812×283 and 375×812 | 40 |
| `lifecycle.py` | `phase14/` | drawer open during an editor re-render; five setting toggles add no listeners | 18 |
| `geom.py` | `phase15/` | account control 44×44, header end cluster 148px | 7 viewports, 0 problems |
| `facetsgate.py` | `phase16/` | the P0 desktop keyboard trap, reproduced then fixed | 10/10 |
| `vitals.py` | `phase16/` | LCP element, **load** CLS, handler cost, long tasks | 6 surfaces |
| `cssuse.py` | `phase16/` | selector coverage | 497 selectors across 26 pages |
| `funnel.py` | `phase17/` | Shopify call count per customer action | 8 |
| `utm.py` | `phase17/` | the 12 submitted field names, reserved-parameter guard | 6 measured |
| `chevron.py` | `phase18/` | disclosure direction, all three `<details>` | 3/3 |
| `drawerexit.py` | `phase18/` | the `.is-closing` exit animation and its 500ms fallback | 12/12, negative-controlled |
| `coherence.py` | `phase18/` | 15 design roles grouped by computed signature; radii, shadows, durations, easings | 10 of 15 roles single-signature |
| probes | `phase18/` | `lineheight.py`, `linebox.py`, `gap.py`, `emptystate.py`, `whichh3.py`, `blastradius.py`, `focus.py`, `overflow.py`, `longtitle.py` | one-shot measurements |

**Assertion totals as reported per phase.** Cumulative, because every phase re-ran everything before it: Phase 10 **405**, Phase 11 **443**, Phase 12 **508**, Phase 13 **570**, Phase 14 **744**, Phase 15 **796**, Phase 16 **945**, Phase 17 **992**. **Phase 18 publishes no single total** — only the per-suite block. Suites that grew: `validate` 197 → 198 (Phase 12) → 199 (Phase 16); `catalog` 54 → 55; `cartdoc` 84 → 85; `contrast8` 56 → 73.

**Viewports.** `phase9/respond.py` declares **13** viewports in code: 375×812, 390×844, 430×932, 480×1040, 768×1024, 820×1180, 834×1194, 1024×1366, 1280×800, 1440×900, 1920×1080, plus landscape 812×375 and 932×430. Phase 18 added 820 because the spec names it where the list carried 834 (iPad Pro), and kept both — so the **spec's nine required widths are covered by eleven**. The reports say "12 viewports"; the code says 13. **The code is right.** `respond.py` takes `page:mode` arguments; run bare it covers only six pages.

### The adversarial review layer

Every phase from 6 onward put its own work through a multi-agent review in which each finding was handed to independent skeptics instructed to refute it. The counts are the audit trail:

| Phase | Raised | Confirmed | Refuted |
|---|---:|---:|---:|
| 6 | 30 | 20 | 10 |
| 7 | 44 | 30 | — |
| 8 | 58 | 46 | 12 |
| 10 | 44 (3 blockers, 15 major, 26 minor) | — | — |
| 16 | 82 | 62 | 12 |
| 18 | 98 confirmed → **70 distinct defects** | 12 FIXED (+4 by measurement), 55 RECORDED, 2 MERCHANT, 1 REJECTED | — |

Two Phase 18 findings the reviewers rated HIGH were **rejected against citations** — the chevron's two sizes (`--icon-sm` 16px inline, `--icon-md` in controls, PHASE-2 line 1428) and "Add to bag" versus "cart" (PHASE-2 line 943, PHASE-12 line 209). Phase 18 records the governing rule: **a CONFIRMED audit verdict is a claim, not a fact.** Two defects reading alone could not have found were found only by driving the component: `inert` inherits through the Shopify section wrapper, and `image_tag`'s `width`/`height` **attributes** become presentational hints for both dimensions, so a rule setting only `width` left every cart line 948px tall with `aspect-ratio` inert.

### What is explicitly not tested, and belongs to the integration

1. **No real Shopify store.** Section Rendering API responses, `content_for_header`, the image CDN, the Theme Editor itself, metafield dynamic sources, and filtering (needs the Search & Discovery app) have never been exercised.
2. **No Lighthouse, no field Core Web Vitals.** Handler duration is measured (0.00 ms on all five controls) and labelled as an input to INP, not INP. Load CLS is measured (worst surface the cart page at **0.0125**, 8× under Google's 0.1); the cart page figure is the deliberate price of hiding the no-JS Update button and is recorded rather than hidden.
3. **Safari untested** — unavailable on Windows. The two things most worth checking there are the `position: fixed` cart scroll lock on iOS and `inert` support. Browser suites ran green under **Edge 153 and Chrome**, both Chromium.
4. **No real device.** Real iOS Safari and Android Chrome — actual toolbar behaviour, actual safe-area values, a real touch digitiser. `env(safe-area-inset-*)` is 0 under `viewport-fit=auto`, so the safe-area padding Phase 9 added is **currently inert**; enabling `viewport-fit=cover` is a sequenced four-step job, not a one-line change.
5. **Sub-320px untested.**
6. **The `<shopify-account>` component can never be tested here** — it upgrades from a script delivered by `content_for_header`. Its accessible name needs one live screen-reader check.
7. **No test purchase was made**, as the brief permits. Whether `product_added_to_cart` fires for an Ajax add is undocumented and recorded as an unknown — verify it first on the live store.

### Where the documents and the code disagree today

**The code is the truth. These are the live discrepancies found by re-measuring on 2026-09-26.**

1. **`assets/base.css` changed after Phase 18 shipped, and no phase document records it.** Its mtime is `2026-09-26 08:27`; every other theme file is `2026-09-25 17:51` or earlier. The change adds `body { font-family: var(--font-body) }` plus a comment block explaining it: the two-typeface rule had been enforced by roughly sixty components each declaring `font-family` individually, with **223 elements across thirteen surfaces inheriting Times New Roman** — all screen-reader-only, so nothing was visibly wrong. The file grew 2,670 → 3,722 B raw, 1,253 → 1,729 B gzip. Integrity is intact: `validate.py` still passes 199/199 and the theme still contains **exactly four real `!important` declarations**, all in `base.css`'s `prefers-reduced-motion` block.
2. **A post-Phase-18 design-review pass exists in `scratchpad/design/`** and is documented in no phase report: `review.py` (the six stated design guidelines, measured from computed styles rather than judged), `unstyled.py` (which elements render with browser defaults, and whether they are the theme or the harness scaffolding), `fallback.py` (visible vs screen-reader-only fallback typefaces — 36 found, nearly all `.visually-hidden`), `bodyfont.py` (what moves if `body` gets a `font-family`: 1 element of 919 across 8 surfaces against a probe noise floor of 756 — i.e. nothing), `qty.py` (every quantity stepper read individually rather than one exemplar per class), `offscale.py` (the 8.9% of spacing declarations off the `--space-1..10` scale, named element by element, with fluid `clamp()`, `.visually-hidden`'s `margin: -1px`, em/ch-relative padding and `auto` margins recognised as legitimate rather than reported as drift). `offscale-8808.html` and `offscale-8809.html` are 0 bytes, dated today — the dead-browser symptom.
3. **Phase 18 §20's byte column is stale.** Measured today versus Phase 18: homepage CSS **55,569 B gz** (Phase 18: 55,093), and a uniform **+476 B on all seven surfaces** — which localises exactly to item 1 above. Requests and duplicate-request counts are unchanged.
4. **The CSS budget is at its ceiling.** Phase 16 §21 set *CSS, worst page ≤ 55 KB gz* when the worst was 50.2 KB. Today's worst is the homepage at **55,569 B** across 13 stylesheets. At 1024 B/KB the budget holds with 751 B of headroom; at 1000 B/KB it is already exceeded. The budget does not state its unit. **Restate the unit and re-measure before the integration adds another stylesheet.** Requests: 26 today against a budget of ≤30, up from 24 at Phase 16.
5. **`theme-check:all` now reports 6 offenses, not 5.** Phase 16 recorded 3 × `AssetSizeJavaScript`; today it is 4, at the four sites listed above. The default-config result (2 × `ValidJSON`) matches Phase 18 exactly.
6. **Theme Check scans 50 files, not 49.** Phase 16's figure predates `snippets/pagination.liquid`.
7. **`respond.py` declares 13 viewports, not 12** (item under *Viewports* above).

### Current theme shape, for reference

75 files: `assets/` 25 (21 CSS, 4 JS), `sections/` 16, `snippets/` 23, `templates/` 7, `config/` 2, `layout/` 1, `locales/` 1. No `blocks/` and no `templates/customers/` — **both absences are decisions, and `templates/customers/` must stay absent** because it is Shopify's auto-upgrade trigger for new customer accounts.

---

## Open decisions, business information required, and known limitations

This is the list to work through before launch. Nothing here is a code defect waiting for a developer's judgement unless it says so: most of it is information the theme deliberately refused to invent, and a smaller set is work that was measured, understood and left undone on purpose.

Two standing rules govern the whole list and explain why so much ships empty:

- **Business facts are never invented.** Anything unknown is escalated, not guessed (Phase 0 §11, rule 4). Where a value is missing the theme ships the surface **empty or hidden** — never a placeholder, never `href="#"`, never a fabricated price, statistic, review, claim or URL.
- **The phrase does not appear in the theme.** Phase 18 rewrote ten merchant-facing schema strings to remove internal vocabulary, including the literal words *BUSINESS INFORMATION REQUIRED*, while keeping every instruction. Do not grep the theme for that phrase — the gaps are recorded here and in each setting's `info` text, not tagged in the code.

Theme as it stands: **75 files** at `god-squad-theme/`, `theme_version` `0.5.0`, never uploaded to a Shopify store.

---

### 1. The five decisions the owner was asked for and has not answered

These are the open items Phase 18 escalated by name (§25). Each was verified, each is real, and each was deliberately not decided by the build.

| # | Decision | Current state in code | Why it is not a developer's call |
|---|---|---|---|
| 1 | **"Add to bag" vs "cart"** | `locales/en.default.json` lines 36 and 47 both set `add_to_cart: "Add to bag"`; 14 other lines in the same file say "cart" | Not drift — a recorded decision (Phase 2 line 943 "add-to-bag is a `<button>`", Phase 12 §5). The action is "add to bag", the container is the "cart", by choice. Unifying the voice is a brand call |
| 2 | **Mobile menu panel type** | Playfair Display 900 at `--type-h3-size`, where Phase 2 §19.6 specifies the eyebrow triplet. No phase document defends the deviation | Correcting it re-types the primary mobile navigation — a visible design change, not polish |
| 3 | **Footer link type systems** | Policy/menu links at 14px sentence case sit directly above social links at 12px uppercase tracked | Same reasoning as (2): two link systems in one band is either the brand's intent or it is not |
| 4 | **"Worldwide Shipping"** | Ships as announcement-bar block `message-2` in `sections/header-group.json`, so it appears on **every page** | It is a commercial claim. The identical claim is deliberately *withheld* from the Our Story values row pending a shipping policy. Either it is true of the business or it is not |
| 5 | **Announcement-bar icon** | `announcement-bar.liquid` block setting `icon` is an `image_picker` — the only glyph in the theme that is not an inline SVG inheriting `currentColor` | Restricting it to the nine-glyph icon set is a merchant-capability decision, not a bug |

---

### 2. What the theme ships empty, and what a live store will actually show

Read this table before concluding the theme is broken. Every blank below is intentional and every one has a visible consequence.

| Setting / template key | Shipped value | Consequence on a live storefront |
|---|---|---|
| `settings.logo` | `""` (`config/settings_data.json`) | Header and footer render the shop name as a text wordmark. No image |
| `settings.favicon` | `""` | No favicon; `/favicon.ico` 404s. The slot now feeds three icon sizes including the iOS home-screen icon |
| `settings.share_image` | `""` | `snippets/meta-social.liquid` falls back product → collection → `share_image` → logo, each branch guarded. With no image anywhere it emits **no `og:image`** rather than a URL that 404s |
| `settings.social_facebook_url`, `settings.social_instagram_url` | absent | Each link renders only when its URL exists; the whole social row is suppressed when both are empty. **There are only these two settings** — no TikTok, YouTube, X, Pinterest, LinkedIn |
| `settings.customer_account_menu` | `"customer-account-main-menu"` | A *handle*, not a menu. Until a menu with that handle exists in Navigation, the `<shopify-account>` sheet opens **with no links**; there is no fallback link set |
| header `menu` | `"main-menu"` | Every nav label and destination comes from the merchant's linklist. There is **no hardcoded menu label anywhere in the theme** — not HOME, SHOP, COLLECTIONS, OUR STORY or VERSE |
| `sections/footer-group.json` → `block_order` | `[]` | The footer has **no navigation columns**. Binding a menu is a merchant action; Phase 11 deliberately unbound the auto-created `footer` handle because it printed Shopify's admin vocabulary ("Footer menu") as customer-facing copy |
| hero `button_link` | absent from `templates/index.json` | The CTA **does not render at all** (`has_cta` requires both label and link). `button_label` "Shop The Collection" is set and unused. The shipped home page therefore has no forward path out of the hero |
| hero `image` | absent | The hero renders its copy over the scrim with no photograph. The intended source (`images/hero-group.png`, 1672×941) is AI-generated with unconfirmed rights and must be uploaded by the merchant |
| both `featured-collection` sections' `collection` | absent | **Both home rows render nothing** — no markup, and `section-featured-collection.css` / `component-product-card.css` are not even requested, because the `stylesheet_tag` calls sit inside the render guard. The guard tests `has_products`, not "is a collection chosen" |
| our-story `image` | absent | The band renders correctly as copy on flat ink; the Theme Editor shows a configuration notice naming the gap |
| our-story `button_url` | absent | "Discover Our Story" does not render. `href="#"` is forbidden |
| our-story fourth value tile | not shipped | "Worldwide / Shipping Available" is withheld — it is the one checkable commercial promise with no policy, destination list or rate table behind it |
| product `low_stock_threshold` | `3` (`templates/product.json` **and** the schema default) | The low-stock line fires at ≤3 units, only when `inventory_management == 'shopify'` and `inventory_policy == 'deny'`. `0` disables it. No figure is ever rendered — only a boolean reaches the page |
| `theme_info.theme_support_email`, `theme_info.theme_documentation_url` | **absent from the file** | Two Theme Check `ValidJSON` **errors**. Phase 10 omitted them rather than shipping empty strings, which the schema rejects as non-URIs. No functional effect on a bespoke theme |

The four `request.design_mode` branches (`featured-collection`, `our-story`, `main-page`, `footer`) are configuration notices only. They render **nothing** on the live storefront.

---

### 3. Business information required

Phase 1 Appendix A consolidated this into thirty decisions in seven clusters. Below is the surviving register, grouped by who must answer and annotated with what the build did in the meantime. **None of the thirty has been formally answered.**

#### 3.1 Catalogue, pricing, currency

| Required | Depends on it |
|---|---|
| Real product catalogue — titles, descriptions, launch prices; whether ₱1,290 / ₱2,490 / ₱890 are actual prices or placeholders | Every product surface. Shopify is the only source of product data; the theme contains no product name, price, currency symbol or collection handle |
| Variant model per product — the size run, and **names** for the three swatch colours the prototype carries as bare hexes (`#0d0c0a`, `#f3efe6`, `#4b5443`) | The variant picker renders whatever options exist in admin. Swatches render only from native Shopify swatch data — the theme will never guess a colour from a name or an image |
| Store currency and money format (`₱` glyph vs `PHP` code), and whether the prototype's $/€ options represent planned Markets | Every price goes through `money`. **The peso glyph gap is still open:** Jost carries neither `₱` (U+20B1) nor `→` (U+2192), so both fall back to a per-platform face in the most legibility-critical string on the page. Options are a subset face carrying U+20B1, a different body face, or documented acceptance |
| Compare-at / sale policy, and whether from-pricing applies | Compare-at is suppressed when the price varies (a range beside a strike-through is not information) |
| Launch catalogue size in products and SKUs | **This is also what unblocks predictive search** (Phase 13 §2) and settles auto-fill vs auto-fit questions in the grid |
| Whether prices display tax-inclusive | Not a theme setting — `cart.taxes_included` drives the cart's tax sentence automatically |
| Badge vocabulary and the condition that fires each badge | The card ships **one** badge, SOLD OUT. No SALE, no NEW. If NEW is wanted the only pre-approved mechanism is a merchant-set tag name, default empty, with SOLD OUT always winning the slot |
| Size guide, materials and care copy | Blocked on ECOM-04. The product page already has the `<details>` accordion pattern. A description must never be synthesised |
| Whether low-stock messaging is wanted at all, and whether 3 reads as scarce for the size run a garment carries | Review once real stock levels exist |

#### 3.2 Collections, navigation and site structure

| Required | Notes |
|---|---|
| Which collection feeds **New Drop / The Faithful**, and whether "The Faithful" is a collection or a drop name | It appears in the prototype only as a section heading over three products |
| Whether a **Best Sellers** row launches and which products qualify | The section is built and presetted. Set the collection's sort order to *Best selling* in admin — the theme never decides what sells |
| Full collection taxonomy: names, handles, descriptions, banner images, default sort, and whether a collections index page is wanted | `list-collections` is not built |
| Destinations for HOME, SHOP, COLLECTIONS, OUR STORY, VERSE and the prototype's six `href="#"` links | The theme carries none of them |
| **What "Verse" is** — a page, a home-page section, or rotating scripture; and which scriptures beyond `2 Corinthians 5:7` are approved | Nothing named Verse exists in the theme. The hero renders that one reference verbatim; Phase 5 forbids changing it or adding another, and a validator asserts both |
| Whether an Our Story **page** exists and its long-form copy; whether the nav item targets the page or the home-page band | The band's anchor is `story`. The nav item still targets the home-page section |
| Whether a Social / Community section launches, and its content source | Never built |
| "View All Products" destination | Defaults to `collection.url`, never constructed by hand |
| Hero CTA destination, and the empty-cart / 404 destination | Both currently fall back to the home page — which, as shipped, has no product link. `/collections/all` is servable now that a collection template exists |

#### 3.3 Brand assets — the launch-gating cluster

This is Phase 3's ceiling and Phase 18's stated reason the theme **is not launchable**. It is a sourcing problem, not a processing problem: re-encoding does not create pixels that were never captured.

| Required | Hard facts on record |
|---|---|
| **Which logo file is official** | Six LOGO files exist and are not the same artwork. `images/WHITE FONT LOGO.png` (500×500, 37,836 B) is the one the prototype loads; `images/logo.png` (500×500, 47,147 B) is a different, unreferenced file; two root PNGs share a byte count (43,606 B) and dimensions but are **not** md5-identical |
| **A vector logo master** (SVG/AI/EPS) | None exists anywhere in the project. The raster's transparent padding leaves the visible mark at roughly 66×50 inside a 78px box. Layered PSD sources sit **outside** the project at `C:\Users\TEST\OneDrive\Desktop\GODSQUAD\PSD FILES` and have never been opened — **authorise that search before commissioning a vector** |
| **A favicon** | None of any kind. Which mark, and whether it is a cropped monogram or the full wordmark — the 500×500 wordmark is illegible at 32×32 |
| **Whether an inverse (dark-ink) logo is wanted** | Three of the eight documented logo contexts need one; none exists |
| **High-resolution product masters** — 1:1, 2048px minimum, sRGB with profile | Present masters are 235×230, 235×235 and 215×190 crops of the 1024×1536 mockup. Best case 1.23× upscale, worst 4.88× |
| **One catalogue-wide product background**, chosen once | A cream sweep, a white sweep and a knocked-out alpha each produce a visibly different grid. The prototype's tile ground is `#EBE6DC` and the crops' own off-white boxes remain visible against it |
| **A high-resolution story master** — 2000px minimum (2400 preferred), 16:9 or wider, subject in the right-hand 45%, left 35% clear, **no baked text** | The live slot uses a 650×480 crop of the mockup *hero* with the fragments "A PURPOSE", "K BY" and "TH." baked into the pixels. Also: name which source is canonical — the manifest proposes `story-community.webp` for two different files |
| **A mobile hero master** | None. The phone crops the 16:9 desktop frame and loses about a third of its width, taking the third model and the back print with it. The `mobile_image` picker and its `(max-width: 749px)` `<picture>` source are wired and deliberately empty |
| **A desktop hero above 1672px** | The master is 1672 wide and the CDN does not upscale: `widths:` entries above it resolve to the master and the browser stretches — 1.15× at a 1920 viewport, 2× on a high-density laptop |
| **Product back views, detail views, colourway frames (nine), packaging, fabric/craft, size-guide imagery** | None exist. Back-print garments cannot be shown at all |
| **Collection / editorial banners**, 2400px+, purpose-made | Zero COLLECTION assets exist. Standing rule: **no collection slot is ever filled from a product image and no banner is cut from the mockup** — the slot stays empty until purpose-made art is commissioned |
| **Provenance and licensing of the AI-generated assets** | The hero, both sprite sheets (2172×724, 833,929 B and 927,973 B) and the nine icon PNGs cut from them are AI-generated. Rights are unverified. This is surfaced in the hero's own schema `info` so it cannot be forgotten before launch |
| **Model releases** for the people in the hero and story frames, and whether the same people appear in the replacement shoot | Never established |
| **Authorisation to extract full-quality pixels** from `uploads/GODSQUAD WEBSITE MOCKUP.png` | A different decision from using the mockup directly, which is forbidden |
| **Official platform brand marks** as unmodified SVG from each platform's brand kit | The project holds circled two-tone badges cut from `images/social-sprite.png`, which is not a licensing-safe source for trademarks. The mockup shows a plain glyph |
| **Feature-icon treatment** — crown, community, diamond, globe: faithful trace, WebP re-encode, or commissioned redraw | Low urgency for the theme: the shipped values row carries **title and line only, no icons**. The globe survives as the announcement bar's optional raster (decision 5 in §1) |
| **Archive dispositions** | Twelve ARCHIVE files (8,541,085 B) and the two sprite sheets await approval to move. ARCHIVE and REMOVE both mean *after approval* — nothing has been deleted, renamed or overwritten, and all 44 original prototype files remain byte-identical |

#### 3.4 Commercial policy, claims and legal

| Required | What it blocks |
|---|---|
| **Shipping scope** behind "Worldwide Shipping" — countries, rates, duties, policy text | Decision 4 in §1; the withheld fourth value tile; any free-shipping threshold. There is **no shipping claim, estimate or threshold anywhere** in the purchase flow |
| **Returns, refunds, privacy, terms** — or confirmation that Shopify admin policy pages will be used | The footer renders `shop.policies` the moment they exist and shows an editor notice until then. No purchase surface can link a policy today |
| **Legal entity name, contact email, phone, address** | The footer copyright is built from `shop.name` and `'now' | date` — never a hardcoded year — and the theme supplies no contact details and guesses none. There is **no contact route**: `page.contact` does not exist |
| **Confirmation of the brand-origin statement** "a Philippine streetwear brand built on faith, creativity, and community" | It is the shipped Our Story body copy, taken from the prototype |
| **Live social URLs**, and whether the TikTok and YouTube channels shown in the mockup exist | Three conflicting channel counts are on record: 2 files, 4 in the mockup, 10 on the sprite. Only Facebook and Instagram settings exist in `settings_schema.json` |
| **Philippine RA 10173 / NPC applicability** | A legal question for counsel. Shopify publishes no APAC-specific consent guidance |
| **Error, success and out-of-stock message wording and tone** | Currently plain; all strings are in the locale file |

#### 3.5 Store and platform facts

| Required | Consequence |
|---|---|
| **Which customer-account system the store uses** (*Settings › Customer accounts*) | Phase 15's first pre-launch check. The theme is correct under all configurations because it has **one code path and branches on nothing** — there is no Liquid-readable way to detect the active system, and a merchant can revert an upgrade within 30 days with no signal |
| **Newsletter capture** — wanted or not, provider, copy, incentive | FOOT-03 is still a business decision. The theme has no newsletter form. Email belongs in an app |
| Wishlist, payment icons, blog, gift cards | None built |
| **Store URL / custom domain, plan, whether a store exists, who administers it, primary language and locale** | Nothing has ever been verified against a real store |
| Home-page `<title>` and meta description | The layout's `meta-tags` output plus `meta-social.liquid`; every value comes from a Shopify object, with no written marketing copy in the file |
| Whether the three approved colours may be merchant-editable at all | Currently they are **not**: the three free colour pickers were replaced by a single `color_scheme` select with one option, resolved in one place (`snippets/css-variables.liquid`) so an illegal gold-on-cream pairing is structurally impossible |
| `theme_support_email` and `theme_documentation_url` | The last two Theme Check errors |

#### 3.6 The four Phase 1 decisions that were supposed to gate the design system

All four were built against a documented default rather than an answer. The defaults are defensible and measured; **the confirmations are still outstanding**, and two of them imply downward changes to a brand-approved mockup that need explicit sign-off.

| Decision | What the build chose | Still open |
|---|---|---|
| #15 Extended palette beyond the three primaries — `#bdb6a8`, `#e9e4d8`, `#ebe6dc`, olive `#4b5443`, the scrims, `--color-text-inverse-muted #5F5A50`, six status colours | Shipped as documented derivations with measured contrast for every pairing | Formal approval that these enter the brand palette |
| #16 Whether the 9–13px tracked labels are brand-mandated on phones | A **12px floor for persistent interface text and 16px body**, no breakpoint-specific font-size overrides | It *raises* the prototype's 9px cart badge and 11px announcement/value/footer lines, and *lowers* the 14px hero verse and taglines to 13px and the 13px value title to 12px. The two reductions need sign-off, not just the raises |
| #17 Browser and device support matrix | Never supplied, and never revisited after Phase 2. The theme uses `:has()` (with an `@supports not selector(:has(*))` `:focus-within` fallback in `component-product-card.css`), `aspect-ratio`, `clamp()`, `svh`/`dvh` (`height: 100vh` written first as the fallback in `section-cart-drawer.css`), `text-wrap: balance`, `inert` (with a minimal Tab trap where absent) | The matrix. Every use has a documented fallback, so the risk is low — but no target has been agreed |
| #18 Behaviour above 1440px | Settled by construction: full-bleed section backgrounds with inner containers, `container_width` a merchant range defaulting to 1440 | Confirmation that dark gutters are not wanted |
| #19 The three deliberate owner deviations from the mockup — three-model hero, gold announcement globe, two-icon social set | Treated as approved | Formal confirmation only |
| #20 Typeface finality and font hosting — Playfair Display, Jost, Kaushan Script; Shopify library vs self-hosted woff2 | `font_picker` settings with `playfair_display_n9` and `jost_n4`; four faces emitted through guarded `font_modify` calls (Jost 400/500/600 + Playfair 900) inside one `{% style %}` block | Whether the library carries Kaushan Script at all, and whether self-hosting is preferred. This also gates any font preloading work |
| #21 Descriptions of who and what the hero and story photographs show | Alt text is **never written by the theme** — it comes from the image object, and empty alt correctly announces a mood photograph as decorative | Accurate alt text cannot exist until the photography does |

#### 3.7 Process items, still open

Phase 1 Appendix A.6 recommended these before Phase 2 and they were never done: the project is **not under version control** and sits in a OneDrive sync folder (DEBT-12, DEBT-13), and the Claude Design prototype has never been formally frozen as the design baseline. All 44 original prototype files are verified byte-identical, which is the only thing standing in for a commit history.

---

### 4. Shopify Admin work required before a customer can buy

None of this is theme work, and the theme is complete without it. Consolidated from Phases 6, 7, 8, 11, 13, 14, 15, 16 and 17, in the order to do it.

1. **Add products** — every price, variant, image, description, SKU and stock level comes from here.
2. **Model the options in admin** — colour and size are product *options*, not theme settings. The picker renders whatever exists, in the order set.
3. **Set colour swatches** — *Settings › Products › Swatches*, or per option value. Without swatch data an option renders as a named chip, not a dot.
4. **Set each image's focal point** — *Content › Files › (image) › Edit*. This is the **only** crop control; `image_tag` writes it as an inline `object-position` style that no stylesheet can override, which is why the theme offers no second control (and why the hero's own `focal_point` select is silently inert for any image that carries an admin focal point). With none set, Our Story centres at `center 33%`.
5. **Set store currency and money format** — *Settings › Store details*. Then check the peso glyph renders.
6. **Create the collections** — one for the drop, one for Best Sellers with sort order *Best selling* — then point each home row at one in *Customize*.
7. **Create the main menu and the footer menu**, then add a footer column block per menu.
8. **Create the Our Story page** and set the section's Button link; **create any page the hero CTA should open**.
9. **Upload the logo, favicon and a ~1200×630 social sharing image** (*Theme settings › Brand*).
10. **Publish the policies** — *Settings › Policies*.
11. **Configure filters** — *Apps › Search & Discovery › Filters*. Until then nothing filter-related renders and neither `component-facets.css` nor `facets.js` is loaded. Shopify's own ceilings apply: at most 25 filters per store, none on collections over 5,000 products, none on search over 1,000 results.
12. **Confirm the customer-account system**, then create a Navigation menu with handle `customer-account-main-menu` and select it in *Theme settings › Customer accounts*.
13. **Brand the account pages in the checkout and accounts editor** (*Settings › Checkout › Customize*) — the Phase 2 tokens do not reach those pages and the theme cannot make them look like the store. Optionally connect an `account.` subdomain.
14. **Brand checkout** (*Settings › Checkout › Branding*), configure **shipping rates** and **taxes**, and enable **accelerated checkout** if wanted (the Buy it now button only appears when the store has it, and its colours, typeface and label are Shopify's).
15. **Install at most one channel app per platform** (Google & YouTube, Facebook & Instagram, TikTok) and **paste no tag into the theme or into Additional Scripts** — Additional Scripts was sunset 2025-08-28, and a snippet that bypasses the consent framework violates Shopify's Terms of Service. Check *Settings › Customer events* first, in case a pixel already exists.
16. **Check *Settings › Customer privacy*** — banner state, configured regions, and whether Network Intelligence is on.
17. **Verify `product_added_to_cart` fires on an Ajax add** with the pixel debugger open. This theme adds exclusively over Ajax and the behaviour is undocumented — described as the highest-value fifteen minutes available.
18. **Supply `theme_support_email` and `theme_documentation_url`** to clear the last two Theme Check errors.
19. Optionally: quantity rules per variant, the empty-cart destination, whether the drawer auto-opens after adding, and the product image shape (`product_image_ratio`, catalogue-wide by design).

---

### 5. What could not be verified, and therefore is not claimed

| Gap | Detail |
|---|---|
| **No real Shopify store, ever** | Every measurement renders the real `.liquid` files against mock Shopify data through the mini-Liquid harness plus headless Edge. Unverified against the platform: the Section Rendering API's real responses, real `content_for_header`, real image-CDN behaviour, real PHP money formatting, real discount allocation, `{{ product | structured_data }}`'s actual output, `paginate.parts` URLs (modelled as `?page=N`), `page_description` on a product page, `| t` escaping of *interpolated variables*, and checkout itself |
| **Theme Check** | **Correction, Phase 16:** Phases 6–15 recorded "Theme Check never run, no Shopify CLI" — but `@shopify/theme-check-node` was present all along, and the Phase 10 runner had been pointed at the *project* root, which stopped being the theme root when Phase 10 moved the theme into `god-squad-theme/`. It had been scanning a directory with no theme in it and reporting zero offenses. Run correctly (49 files, 84 checks): **2 offenses on the default config**, both `ValidJSON` for the missing `theme_info` strings; **5 on `theme-check:all`**, the extra three being `AssetSizeJavaScript`. Still run `shopify theme check` against a development store before launch |
| **No Lighthouse, no field Core Web Vitals** | Not installed, no network to install it. **No Lighthouse score appears anywhere in this project and none may be invented.** LCP/FCP/TTFB timings and field INP need a live store and real users |
| **Font-swap CLS** | The single CLS source that cannot be reproduced locally — the harness has no font files. This matters *more* since Phase 16 added two Jost faces. **Verify CLS on a real store** |
| **Image bytes** | The largest real contributor to page weight cannot be measured because the merchant's photography does not exist. Image count and declared sizes are reported instead |
| **Safari and Firefox** | Untested; Edge 153 and Chrome only, and they share an engine. The two things most worth checking in WebKit: the `position: fixed` scroll lock on iOS and `inert` support |
| **Real devices** | Every reading is headless Edge through an exact-size iframe, cropped. Real toolbar behaviour, real `env(safe-area-inset-*)` values, a real touch digitiser and real network timing are all unverified — Phase 9 called this its largest gap. Specifically unverified: `hero--h-full`'s `svh` behaviour under a live collapsing browser toolbar |
| **The account component** | The harness never loads Shopify's script, so `<shopify-account>` is permanently un-upgraded there. **Every account measurement is of the reservation, never of the component.** The sheet's layout, token mapping and dialog position are verifiable only live |
| **One live screen-reader check outstanding** | The theme supplies a visually-hidden name inside the component's slot so the control is named under either Shopify behaviour. Whether the two combine into a *doubled* announcement cannot be checked from here. **Listen to the header account control once; if it announces twice, delete the `<span class="visually-hidden">` from the slot** |
| **`--shopify-account-dialog-position-top` deliberately unset** | Its semantics could not be settled from the documentation and this theme has a sticky header a wrong guess would put the sheet under. Shopify's default is in place; first knob to check live |
| **Visual review of imagery** | Not done by anyone. Everything reviewed is the *reservation* — the aspect box, `object-fit`, the scrim, the alt path — never the picture. Alt-text content depends on images that do not exist |
| **Hero centre/right alignment contrast** | Those two options swap in their own gradients and pass visual inspection; their contrast was **never measured pixel by pixel** because they are not the approved configuration. If a merchant selects either, the AA guarantee does not automatically carry. Cheap to measure and should be done before launch |
| **Sub-320px** | 320×568 and 568×320 both pass; nothing smaller was measured, and no landscape tier exists below 320px of height |
| **The `form-tags` research dimension** | Never reconciled across six attempts. It covered legacy customer `{% form %}` tags, which this theme does not use — so nothing rests on it. Redo it if legacy account templates are ever built |

---

### 6. Known limitations in the shipped code

#### 6.1 Platform limits that cannot be engineered away

- **Order history, order details, tracking and customer information are not theme-buildable.** Shopify deprecated legacy customer accounts on 2026-02-26. The account experience is on a different origin, styled from checkout settings. `templates/customers/` **does not exist and must remain absent** — shipping it does not make the theme safer, it *withholds the merchant's auto-upgrade* to new customer accounts.
- **The account control is inert until Shopify's script upgrades it.** Measured: `tabIndex` is -1 while undefined. A custom element cannot be tabbed to or clicked before its script runs, where the old `<a href>` worked with no script at all. Inherent to the approach; not worked around, because a fallback link inside the slot would nest an anchor inside the upgraded button.
- **A theme cannot fire a purchase event, and cannot publish Shopify standard events** — Shopify: *"partners and merchants cannot publish standard events."* There is no `dataLayer` and there should not be: app pixels run in a strict web-worker sandbox with no `window` or `document`, custom pixels in a sandboxed iframe. The theme's entire load-bearing contribution to analytics is the single unmodified `{{ content_for_header }}` at `layout/theme.liquid:127`.
- **`product.variants` truncates at 250**, which is the ceiling on the embedded variant table. Not realistic for apparel; recorded rather than papered over.
- **3D models render their preview image, not a model viewer.** `model_viewer_tag` produces inert markup until the theme calls `Shopify.loadFeatures({name: 'model-viewer-ui'})`, and AR needs a second independent call. Neither can be verified in the harness because `Shopify.loadFeatures` arrives via `content_for_header`.

#### 6.2 Missing surfaces

**Five templates Shopify can route to that this theme does not have** — `article`, `blog`, `gift_card`, `list-collections`, `password`. Each serves Shopify's error page to anyone who reaches its URL. `page.contact` is a sixth absence (an alternate page template, not an auto-route), which is why the store has no contact route. Phase 1 SHOP-09 tracks the same list. `password` matters most if the store ever goes behind a password page. This is their own small phase.

#### 6.3 Deliberate functional gaps

| Limitation | Detail and reasoning |
|---|---|
| **With scripting off, the variant picker switches nothing** | The radios render and can be chosen; the value submitted is the hidden `name="id"` input the server rendered for the default variant. A customer without scripting can buy that variant and no other. This is where Shopify itself stands (the platform dropped the no-JS requirement; Dawn behaves identically) and the documented alternatives either collide with the hidden input on submit or force per-value variant resolution in Liquid. Recorded as a **genuine gap**: a control that looks operable and is not has a real cost. The honest fix is a small no-JS `<select>` once duplicate-`id` submit behaviour can be tested on a real store |
| **Quick add is unreachable** | `snippets/product-card.liquid` carries a complete, correct implementation (a `Choose options` link for multi-variant, a real form for one available variant, a real `<button aria-disabled>` when unavailable — never a `<span>` wearing button classes). **No section passes `quick_add`**, and no section exposes a setting to turn it on. Its two former defects are fixed but latent. Exposing it is a one-line setting per section and a catalog decision nobody has taken |
| **No filtering on `/search`** | Applying filters on the search page strips all non-product results, and `main-search` renders a non-product group (`search_types` offers *Products only* and *Products, pages and articles*). If it is ever added it needs three hidden inputs — `q` (or the search is discarded), `type` (or the merchant's scope reverts to all types) and `options[prefix]=last` — plus `search.sort_options`. **The pages/articles question must be decided first** |
| **Predictive search deferred** by owner decision | The full contract is recorded: the section-rendering endpoint (`routes.predictive_search_url` with `section_id`, never the JSON endpoint, never a hardcoded `/search/suggest`), `resources[limit]=4` with `limit_scope=each`, and all six stale-response guards — 300ms debounce, 2-character minimum, an `AbortController` per request, a captured-term comparison at resolve because `abort()` is not synchronous, a monotonic generation counter, and a cache keyed on the normalised term. **A catalogue count unblocks it** |
| **No overlay behind the filter drawer** | Escape, the close button and the trigger all dismiss it. A click-outside layer would need markup the brief listed only conditionally |
| **Filter controls are not rendered on a zero-result collection** | They sit inside the `paginate.items > 0` branch. The copy was corrected to match the control actually offered (a prominent **Clear all** is always present). Rendering them there is the better fix and requires hoisting the form, which restructures the single-form design |
| **`viewport-fit=cover` is not enabled, so the safe-area padding is inert** | `env(safe-area-inset-*)` resolves to 0 under `viewport-fit=auto`; `layout/theme.liquid:33` is `width=device-width, initial-scale=1`. Enabling it is a **sequenced four-step job**, not a one-line change: add `viewport-fit=cover`; inset `.header__inner`'s top padding by `env(safe-area-inset-top)`; make `--header-overlay-offset` account for it (it is currently the static 88px token, and the hero's landscape padding is computed from it); then re-measure the hero at every viewport. On a device with a real inset the current arrangement is safe because the browser letterboxes |
| **No sticky mobile purchase bar** | Optional in the brief, which says to remove rather than force one. Add to Cart is inside the single-column flow. A bar would need scroll-position JavaScript Phase 9 was told not to add, and would cover content on a 375px-tall landscape viewport |
| **The cart drawer is not full-screen on a phone** | `--drawer-width` is `min(90vw, 420px)` — 338px on a 375px viewport. The remaining 37px of scrim is what makes tap-to-dismiss possible. Reversible in one token |
| **`.cart-line__title` is 24–28px, not 44px** | Meets WCAG 2.2 SC 2.5.8 (AA, the theme's conformance level) and is covered by the equivalent-control exception — the 76px thumbnail beside it links to the same product. Growing it would add 20px per line to a drawer that fought for 100px of scroller in landscape. A deliberate Phase 8 call, flagged UNDER-44 on every run |
| **Two navigation trees** | A desktop list and a mobile panel with five duplicated links. Consolidating them is a header rebuild |
| **The header's cart control is a link that opens a dialog** | A screen reader announces "Cart, 3 items, link" and the customer gets a drawer. Focus moves to a heading reading "Your cart", it is what Dawn does, and it is what keeps the no-JS fallback a real link |
| **The drawer and the mobile menu can in principle both be open** | The menu traps focus and covers the screen so it is not a realistic path, and both respond to Escape. Untested on a real device |
| **`show_cart` can hide the only header path to the cart** | Shipped because the brief lists it, with the cost written into the setting's own `info`: a customer who has added something can only reach the cart by typing the address |
| **The order note has no length limit** | Shopify's own limit applies at the API; inventing one would reject text Shopify would have accepted |
| **No accelerated checkout in the drawer** | `content_for_additional_checkout_buttons` can appear only once per page, so only the cart page renders it. The drawer's Checkout submit reaches the same place |
| **The landscape blocks fire on a small desktop window** | A 900×500 browser window satisfies both `(max-height: 540px)` and `(max-width: 1023px)` and gets the landscape hero and drawer proportions. Intended — a 500px-tall window has the same problem — but someone resizing a desktop browser will see it |
| **The caption rail is not rendered below 1024px** | `display: none`, so it leaves the accessibility tree too. The STORY-04 decision; `show_caption` turns it off at every width |
| **Three value tiles wrap 2 + 1 at 768–1023** | A floor low enough for three tracks there would put five tracks back at 1440 and re-orphan a sixth block |
| **`main-product` uses settings rather than blocks** | An app that ships a product-page block cannot place itself there. The fix is a `blocks` array with a `{% when '@app' %}` arm — a small change |
| **One colour scheme** | Adding a second is **not an engineering decision**: it needs brand approval of the values and a measurement pass across the whole contrast matrix. Inventing alternates would be the identity redesign every phase has been forbidden |
| **Schema labels are plain English, not `t:` keys, and there is no `locales/en.default.schema.json`** | Verified: zero `"t:` occurrences across all 14 section schemas and `settings_schema.json`. Customer-facing strings *are* all in the locale file. Converting roughly 236 merchant-facing strings is a large mechanical change whose failure mode is a raw `t:sections.x.y` showing in the editor; both halves must ship together with a validator proving every key resolves. Carried Phase 10 → 11 → 12 and never done |

#### 6.4 Confirmed findings left open, by count

- **48 confirmed P2/P3 findings from Phase 16** and **55 verified-but-unchanged items from Phase 18** (full evidence in `PHASE-18-VISUAL-AUDIT.md`). Every Phase 18 row carries the same deferral test verbatim: *"it is cosmetic or structural tidying whose risk outweighs its benefit in a phase that is explicitly not a redesign."*
- Phase 16's three highest-value consolidations **were done in Phase 18** — the duplicated paginator became `snippets/pagination.liquid` + `assets/component-pagination.css`, the twelve copy-pasted container rules became `assets/component-container.css`, and `.product-card__error` moved out of the cart grouping. **Do not re-open them.**
- The three that remain from that list, verified still present in the code:

| Open finding | Evidence |
|---|---|
| **The hero and Our Story under-declare `sizes` on the phone tier by roughly 1.9×** | `sections/hero.liquid` lines 84/97/111 declare `sizes="100vw"` / `sizes: '100vw'`; `sections/our-story.liquid:105` sets `img_sizes = '(min-width: 1024px) 70vw, 100vw'`. Both boxes are `object-fit: cover` on a shorter aspect box than the frame |
| **The header search form hardcodes `type=product`** | `sections/header.liquid:318` emits `<input type="hidden" name="type" value="product">`. It agrees with `templates/search.json`'s `search_types: "product"` **today**, and will not follow a merchant who switches that setting to *Products, pages and articles* |
| **One Escape closes two layers** | `assets/cart.js:441`, `assets/facets.js:119` and `assets/header.js:128`/`:195` each install independent document-level Escape handlers |
| **`featured-collection` still carries its own ~100-line `sizes` derivation** | `snippets/grid-sizes.liquid` is rendered by `main-collection` and `main-search` only; `featured-collection.liquid` keeps `need_m` / `threshold_m` / `capped_track` locally, with a comment saying why. **A future change to the shared rules must be applied there too** |

---

### 7. Design-system gaps still open

Token-level gaps recorded across phases and verified against the current CSS. Each is a request against the design system, not licence to invent a literal.

| Gap | Verified state |
|---|---|
| **No product-page title scale** | Phase 2 §27.1 covers only the card's 12px label, so the product `h1` takes the story scale's size and tracking with the interface family (Jost, per §5.5) |
| **No price scale above the card's 15px** | `assets/section-main-product.css:185` uses `--type-body-lg-size` while `component-product-card.css:325` and `component-cart-line.css:186` use `--type-price-size` |
| **`--link-underline-offset: 0.2em` exists and three rules hardcode `0.25em`** | `component-facets.css:260`, `component-product-card.css:290`, `section-main-product.css:471` |
| **`--scrim-story-horizontal` is defined and unused** | `design-tokens.css:434`. Its stops are the prototype's, the caption rail over them measured 1.69–2.14:1, and it is a fixed ink while the band must also fade into cream. A token the band *cannot* use, not one overlooked |
| **No editorial landscape ratio token** | The `3/2` used from 768 in Our Story is written out in that stylesheet |
| **Phase 2 §27.4 names `--color-border-current` for a variant chip's boundary and §12.2 contradicts it** | Those tokens composite to about 1.3:1 and fail SC 1.4.11. §12.2 wins — fields, Secondary buttons and swatch rings take an interactive-border token instead |
| **Icon caps and joins** | Every glyph Phase 3 drew and Phases 4–8 shipped uses round caps and mitre-free joins; Phase 2 §18.3 rule 2 specifies the opposite. Matching the set is what keeps the icons looking like one drawing, so the deviation was left whole. **Settle it for all glyphs at once or not at all** |
| **40 of 192 design tokens are unreferenced** | Recorded, not pruned: a design system is allowed a vocabulary larger than its current usage |
| **Phase 2 §26.1 allows one body paragraph; Our Story accepts up to four** | A deliberate, recorded departure; the schema says so |
| **10 of 15 design roles are single-signature** | Up from 9 before Phase 18. Three radii, one shadow, two durations, one easing across the whole site |

---

### 8. The performance budget, and the one line currently over it

Set from what the theme measures, not from round numbers. Current values are Phase 18's re-measurement.

| Budget | Current worst | Target |
|---|---:|---:|
| JavaScript, all pages | 22.0 KB gz | ≤ 30 KB gz |
| **JavaScript, per page-load script** | **12,073 B gz (`cart.js`)** | **≤ 10,000 B gz** (Shopify's own `AssetSizeJavaScript`) |
| CSS, worst page (homepage) | 55,093 B gz | ≤ 55 KB gz |
| Requests, worst page | 26 | ≤ 30 |
| Load CLS | 0.0125 | ≤ 0.05 |
| Theme handler time | 0.00 ms | ≤ 50 ms |
| Eager images per page | 1 | exactly 1 |
| `fetchpriority="high"` per page | 1 | ≤ 1 |
| Third-party scripts | 0 | each one justified in writing |

**`cart.js` is genuinely over the per-script threshold** (39,750 B raw / 12,073 B gz) and has been since Phase 16 — it was not introduced by Phase 18. The executable code is **4,930 B gzipped; the other 7,143 B is comments**, so the threshold is not reachable by deleting prose. The recommended answer is **a deploy-time minification step** — it clears all three `AssetSizeJavaScript` errors without touching a line of tested cart logic, and it is a tooling decision, not a code one. "Restructure the cart with import-on-interaction" is the wrong response on a theme whose *total* JavaScript is 22 KB gzipped with zero dependencies.

Note the homepage CSS figure sits exactly at its own target; Phase 18 added two stylesheets while reducing rules-only CSS by 2,501 B (−2.5%, −71 declarations). The budget's basis is 11 stylesheets on the homepage, and any twelfth needs its own justification.

---

### 9. Things that look like defects and must not be "fixed"

Every item below was measured, argued and deliberately left as it is. Changing one without reading its reasoning will regress the theme.

| Looks wrong | Why it is right |
|---|---|
| **All three GET forms discard UTM parameters** | Harmless, and fixing it would be worse. Shopify records `landingPage` / `utmParameters` server-side at the first request; GA4 fixes session source at session start; Meta has already written `_fbc`; Dawn behaves identically. Carrying UTMs through internal forms would create self-referrals. A **reserved-parameter guard** additionally keeps `ref`, `source` and `r` out of the 12 submitted field names, because Shopify special-cases those storefront-wide as the marketing referral code |
| **`cart_viewed` will almost never fire** | The cart is drawer-first and the drawer is rendered with the page, never fetched. A drawer that fetched on open would make Shopify emit a cart event on every open. Expected, not a defect — but a funnel report looks odd until someone knows why |
| **The homepage emits two duplicate stylesheet `<link>` tags** | Measured at the network layer: **11 CSS requests, not 13 — the browser deduplicates.** Zero extra requests. Promoting the stylesheets to the layout would push ~4 KB onto four surfaces that do not need it |
| **`.variant-picker__swatch--square` is unreachable** | 40 bytes and a documented extension point; the sole genuinely dead selector across 26 measured pages. The adversarial verifier disagreed and the measurement stands. Recorded, not deleted |
| **The cart page's 0.0125 load CLS** | The correct price for a working no-JavaScript Update button (`.cart-js .main-cart__update { display: none }` keys on a class `cart.js` sets on itself). Recorded rather than hidden |
| **The chevron ships at two sizes** | Phase 2 line 1428 assigns it both — `--icon-sm` 16px inline (filter groups, cart note) and `--icon-md` in controls (product details). A 24px glyph beside a 12px filter label *would* be the defect. This finding was rejected with the citation |
| **The `None` hero overlay is unsafe over the current image** (1.00:1) | Retained for a future image already dark where the words sit; the setting's help text says exactly that |
| **Quick add is off in every shipped configuration** | A multi-variant product gets a link to its page rather than a silent default-variant add |
| **There is no free-shipping threshold, cart recommendation, discount field or newsletter form** | Each needs a real business input, and inventing one is the fake-data failure this project has refused at every phase. A second discount field that can disagree with checkout is also a support burden |
| **`templates/customers/` is absent** | That absence *is* Shopify's auto-upgrade trigger for new customer accounts |
| **Sold-out media dims to 0.6, and the sale price is struck through** | Neither is the only signal: the state is in the link's accessible name ("Utility Cap Sold out") and each figure carries a visually hidden "Sale price" / "Regular price" label. Colour is never the sole carrier of meaning (SC 1.4.1) |
| **The four `!important` declarations in `base.css`** | All inside the `prefers-reduced-motion` block, where a user preference must beat an author declaration. They are the only real `!important`s in the theme |
| **The quantity debounce is a hard 250ms literal, not a motion token** | `--duration-*` collapses to 1ms under `prefers-reduced-motion`, which would break the debounce |
| **The prohibition test suites** (`tracking.py`, `negctl.py`, `escaping.py`, `hygiene.py`) | Keep them running. They are the reason the next person cannot quietly paste a `gtag` snippet into `theme.liquid`, read a customer field into a shared snippet, or drop an `| escape` from the cart note. Every absence assertion is negative-controlled, because an absence assertion that has never been seen to fail is indistinguishable from a typo in a regex |

**The one circumstance in which analytics code may ever enter this theme:** if `product_added_to_cart` does not fire for Ajax adds, the fix is a custom pixel subscribing to a prefixed custom event the theme publishes via `Shopify.analytics.publish`. Nothing else.

---

## Phase-by-phase record

The programme ran as nineteen gated phases (0–18) over 2026-09-20 to 2026-09-25, each with its own written specification and its own document in `C:\Users\TEST\OneDrive\Documents\GodSquad Website`. This is the provenance trail only: one entry per phase giving what it delivered, the decision that still binds, and the most important thing it got wrong and corrected. Where a later phase overrode an earlier one, the entry says so — read the later phase. The subject chapters above carry the current rules; this chapter carries who decided them and why.

| Phase | Document | Date | Delivered |
|---|---|---|---|
| 0 | `PHASE-0-PROJECT-FOUNDATION.md` | work 2026-09-20, written 2026-09-21 | Read-only inspection, six standing rules, the rebuild judgement |
| 1 | `PHASE-1-WEBSITE-AUDIT.md` | audit 2026-09-20, reviewed 2026-09-21 | 200-issue work list, 44-file inventory, the phase plan |
| 2 | `PHASE-2-DESIGN-SYSTEM.md` + `PHASE-2-DESIGN-TOKENS.css` | 2026-09-21 | Design system spec, 191 tokens, 46-check QA list |
| 3 | `PHASE-3-ASSET-SYSTEM.md` + `PHASE-3-ASSET-MANIFEST.csv` | 2026-09-22 | Asset manifest, 9 authored SVGs, hero WebP ladder |
| 4 | `PHASE-4-HEADER-NAVIGATION.md` | 2026-09-22 | First theme code: header group, nav, icons, minimal layout |
| 5 | `PHASE-5-HERO.md` | 2026-09-22 | `sections/hero.liquid`, zero JS, measured scrim |
| 6 | `PHASE-6-COLLECTIONS-BEST-SELLERS.md` | 2026-09-22 | One collection section, two presets, the product card |
| 7 | `PHASE-7-OUR-STORY.md` | 2026-09-23 | `sections/our-story.liquid` + brand-value blocks |
| 8 | `PHASE-8-PRODUCT-SHOPPING-UX.md` | 2026-09-23 | Product page, variants, Ajax cart, drawer, cart page |
| 9 | `PHASE-9-MOBILE-RESPONSIVE.md` | 2026-09-23 | Responsive pass: 9 defects found, 9 fixed, no new files |
| 10 | `PHASE-10-THEME-ARCHITECTURE.md` | 2026-09-24 | Theme rooted at `god-squad-theme/`, five new surfaces, two P0 fixes |
| 11 | `PHASE-11-THEME-EDITOR.md` | 2026-09-24 | Global settings, section-lifecycle fixes |
| 12 | `PHASE-12-PRODUCT-COLLECTION-UX.md` | 2026-09-24 | `grid-sizes.liquid`, secondary image, low-stock line |
| 13 | `PHASE-13-SEARCH-FILTERING-DISCOVERY.md` | 2026-09-24 | Native filtering, header search panel |
| 14 | `PHASE-14-CART-CHECKOUT-UX.md` | 2026-09-24 | Cart audit + order note, continue shopping, 2-col cart |
| 15 | `PHASE-15-CUSTOMER-ACCOUNT-POST-PURCHASE.md` | 2026-09-24 | `<shopify-account>`, and the absences asserted |
| 16 | `PHASE-16-PERFORMANCE-SEO-CONVERSION.md` | 2026-09-24 | Social metadata, font faces, the P0 filter trap, the budget |
| 17 | `PHASE-17-ANALYTICS-TRACKING-MARKETING.md` | 2026-09-25 | Measured absence of tracking, prohibition tests, XSS fix |
| 18 | `PHASE-18-FINAL-POLISH-REPORT.md` + `PHASE-18-VISUAL-AUDIT.md` | 2026-09-25 | 70 defects triaged, container/paginator consolidation |

---

### Phase 0 — Project Foundation

**Delivered.** A read-only inspection of the Claude Design prototype: a recursive md5 inventory, a runtime analysis of `support.js`, DOM measurements at thirteen widths, network/font/bundle figures, and pixel-sampled contrast of the navigation over the hero. No code, and no contemporaneous document — the record was written retrospectively on 2026-09-21 from the preserved evidence base, after Phase 3 was halted because its specification required a Phase 0 document that did not exist.

**Key decision.** The project is a *rebuild against a preserved design*, not a conversion. The prototype's template delimiters are `{{ }}` — Liquid's own — so pasting its markup into a section would make Liquid evaluate `{{ products }}` and `{{ p.name }}` as undefined and render empty tiles silently, with no error. From that follow the six standing rules every later phase inherited: the visual direction is preserved, phases are gated, inspect before changing, business facts are never invented, originals are never destructively processed, and the prototype is the design baseline rather than the codebase.

**Got wrong, corrected.** Two of the lead's own claims were refuted in the three-sceptic round and are recorded as corrections: the prototype's CTA hover styles *do* work (the runtime compiles them into generated `.scp0:hover` / `.scp1:hover` rules), and the page *does* boot from a plain `file://` open — only the unpkg React fetch needs the network. Both had been asserted the other way first.

---

### Phase 1 — Website Audit & Technical Assessment

**Delivered.** The 3,190-line audit that every later phase executed against: per-dimension verdicts, an md5-hashed inventory of all 44 prototype files, and a 200-issue work list (3 P0, 65 P1, 80 P2, 52 P3; by severity 5 CRITICAL, 49 HIGH, 85 MEDIUM, 61 LOW) with each issue assigned to exactly one owning phase. Appendix A holds the thirty consolidated business decisions in seven clusters; Appendix B names the evidence files.

**Key decision.** KEEP the design, REPLACE the architecture. Nothing from the prototype is copied: the theme starts from an empty scaffold, the prototype folder becomes a read-only archive, and the design tokens and copy are *transcribed, not copied*. `support.js`, the unpkg loads and the `data-dc-script` block are deleted rather than ported, and the theme's own JavaScript is authored from scratch, deferred and framework-free.

**Got wrong, corrected.** Nine sections (§17–22, §24, §27, §29) were issued on 2026-09-20 as unreviewed first drafts because their reviewers could not complete, and were put through the same hostile-review cycle the next day — about sixty itemised corrections, including: a fabricated footer link-group set (SHOP / ABOUT / HELP / FOLLOW) removed entirely because neither prototype nor mockup has one; a false zoom claim withdrawn (1366 ÷ 1.5 = 911 CSS px, still above the 900px breakpoint); "Reflow passes" withdrawn because SC 1.4.10 is defined at 320 CSS px and 320px was never captured; a new Level A issue **A11Y-11** (missing `lang`, empty `<title>`) added, growing the register from 24 to 25 in that area; and AVIF struck from three places because the Shopify CDN does not output it. The lesson carried forward: an unreviewed section is a draft, whatever the document around it looks like.

---

### Phase 2 — Design System & Visual Language

**Delivered.** A specification, not an implementation: sixteen token groups, the type/spacing/container/grid systems, button, link, form, card, image, border, radius, shadow, icon, navigation, motion, hover, focus and accessibility rules, the Shopify settings policy, worked section schemas, a 46-item design-QA checklist with an evidence method per check, and the companion `PHASE-2-DESIGN-TOKENS.css`.

**Key decision.** THE PROHIBITION, and the mechanism that enforces it. Muted gold `#D8C08A` measures 1.55:1 on warm cream `#F3EFE6` and 1.43:1 on the tile cream `#EBE6DC`, so gold is a dark-surface accent only and on light surfaces the accent is `--color-accent-strong` `#82672B` at 4.66:1. It is not enforced by discipline: colour arrives by surface class (`.surface-dark` / `.surface-light`), and a component that reads `--accent-current` and `--color-border-current` *cannot* put gold on cream because on a light surface those names do not resolve to gold.

**Got wrong, corrected.** The document was written against token file v1.0.0 and, in doing so, found nine missing tokens and two wrong citations in its own companion file. All were verified against the source and folded in before issue (§30.99), taking the file to 191 declared tokens — Appendix B's "164 tokens" is the pre-adoption figure and should be read as stale. The one that mattered was accessibility, not tidiness: the four decorative border tokens composite to 1.17–1.35:1, correct for a hairline but failing SC 1.4.11 for a control boundary, so `--color-border-interactive` (3.02:1) and `--color-border-interactive-inverse` (3.13:1) were added and fields, Secondary buttons and swatch rings point at them. Two requests were deliberately left open because they need a design decision, not a mechanical fix: `--focus-ring-companion` and `--type-label-weight-nav`.

---

### Phase 3 — Asset Preparation & Image System

**Delivered.** `PHASE-3-ASSET-MANIFEST.csv` (62 rows, seventeen fixed columns), nine authored SVG UI icons (2,612 B total, 24×24 canvas, stroke 1.5, `currentColor`, **drawn from coordinates, not traced**), a five-rung hero WebP ladder (1672 / 1280 / 960 / 640 / 420 at q0.82, 311,174 B), and `phase-3-assets/README.md`. 48 files scanned, 18,077,379 B, nine md5 duplicate groups covering 20 files (11 redundant copies, 6,733,692 B — 39.4% of all image bytes). Zero originals modified, renamed or deleted.

**Key decision.** The ceiling is sourcing, not processing. Every photographic and product asset is a crop of one 1024×1536 mockup — tee 235×230, hoodie 235×235, cap 215×190, story 535×348 — rendering at 288px desktop and 327–382px on phones, about 2.8× device-pixel upscale. Re-encoding does not create pixels that were never captured, so all five P0s in Appendix A are external sourcing or licensing gaps, not defects in the work. Two platform facts settled here still bind: the CDN serves WebP automatically and **does not output AVIF**, and the CDN **does not upscale**, so a `widths:` ladder is capped at the master's real width.

**Got wrong, corrected.** Four drafting clusters produced 52 risk entries describing roughly 25 distinct risks, each scoring severity on its own reading; they were consolidated and rescored against one definition into AR-01…AR-25 so the register did not inflate against Phase 1's three P0s. One erratum is recorded but **still uncorrected at source**: `phase-3-assets/README.md:42` claims the nine SVGs replace "the nine raster PNGs … a 99.2% reduction". The two sets of nine are not the same nine; the like-for-like figure is three icons, 85,933 B → 948 B, **98.9%**. Fix the README rather than re-deriving the claim.

---

### Phase 4 — Header & Navigation

**Delivered.** The first production theme code: 16 files, 68,855 B — `sections/header-group.json` rendered by `{% sections 'header-group' %}`, the announcement bar, the header with primary/utility/mobile navigation, the icon snippets, `header.css` / `header.js`, and the minimal layout and config that make the theme structurally valid. `templates/index.json` was deliberately left empty.

**Key decision.** The header backing is arithmetic, not taste. Phase 1 measured nav links at 2.4–2.9:1 over the hero sky; Phase 2 answered with `--scrim-header`; Phase 4 measured *that token against the real hero* and found the ramp had already faded by the band the links occupy — brightest pixels 1.1–1.7:1, worse than the prototype. For cream text to clear 4.5:1 over a worst-case near-white sky the ink layer must hold ≥0.85 alpha, so the token now holds about 0.86 through the **entire** header and fades only below it via `--scrim-header-overhang`. Worst single pixel in the band after the change: 13.61:1.

**Got wrong, corrected.** The overlay header first shipped with `top: 0`, which pulled it to the top of the page and dimmed the announcement bar with its own scrim; an absolutely positioned box with no offset keeps its static position, so *removing* `top` lands it directly below the bar while still lifting out of flow. Found by looking at the render, not the code. A second defect was found by driving the component rather than reading it: focus was returned to whatever had focus when the panel opened, stranding focus inside a closed panel — a disclosure always returns focus to its own trigger. The standing method note from this phase: both the desktop preview pane and headless Chromium under a virtual time budget freeze CSS transitions at their start value, so **disable transitions before measuring animated state**.

*Superseded:* Phase 4's three free brand-colour theme settings were replaced in Phase 10 by a single colour-scheme select resolved in `snippets/css-variables.liquid`.

---

### Phase 5 — Hero Section

**Delivered.** `sections/hero.liquid` + `assets/section-hero.css`: one `<h1>` with a `display: block` gold accent span, eyebrow as `<p>`, verbatim `2 Corinthians 5:7`, `image_tag` delivery with explicit `widths:` / `sizes: '100vw'` / `loading: 'eager'` / `fetchpriority: 'high'`, fourteen settings in four groups, a God Squad Hero preset, and zero JavaScript. Theme at 18 files / 97,079 B.

**Key decision.** The scrim is mandatory, not stylistic: with it removed, the worst backdrop pixel behind every one of the four text elements carries cream at **1.00:1**. The `None` overlay option is retained but documented as unsafe over this image. Heights use `svh`, never `vh`, and every option is clamped.

**Got wrong, corrected.** An entire first round of measurements was invalidated by a capture artifact. Headless Edge on Windows will not lay out below roughly 492 CSS px, and `--screenshot` crops or scales rather than re-laying out, so `--window-size=375,760` produced a 375px-wide PNG of a **492px-wide layout** — proved by rendering a page that prints `window.innerWidth` beside a 50% colour split (`innerWidth=492`, split at x=246). Every capture is now taken through a wrapper page holding an iframe of the exact target width and cropped, and each capture is verified to contain the photograph before it is measured. This technique is reused by every later phase.

**Still open (verified in code today).** The CTA does not render: `button_link` has no schema default, and `templates/index.json` ships `"button_label": "Shop The Collection"` with no link. A destination is a business decision, not a code gap.

---

### Phase 6 — Collections & Best Sellers

**Delivered.** `sections/featured-collection.liquid`, `snippets/product-card.liquid` and the shared button component: 19 section settings in six groups plus the theme-level `product_image_ratio`, two presets (New Drop, Best Sellers), server-rendered from a merchant-chosen collection with zero JavaScript. Theme at 24 files / 158,461 B.

**Key decision.** One section, not two — `sections/best-sellers.liquid` deliberately does not exist, because a second file would mean fixing every future bug twice. Shopify is the only source of product data: the section ships with **no collection handle**, so both home rows render nothing at all on a live store (not even a stylesheet request) until a merchant picks a collection. And the merchant's column count is a ceiling, not a command: the grid is `auto-fill` with a 272px catalogue track floor above 768 and an 8rem phone floor, so no setting a merchant can choose produces a broken grid.

**Got wrong, corrected.** Two harness faults each produced a confident wrong answer. `break` inside a `for` discarded the output rendered before it, so the swatch row looked absent when the Liquid was correct — the interpreter was fixed to carry partial output, as Liquid does. And the portrait-ratio test injected its override outside any rule block, so the declaration was discarded and the page rendered square: a **false pass on the only evidence for `product_image_ratio`**, caught by review and re-measured at `aspect-ratio: 4 / 5`, 312 × 390. Of 30 adversarial findings, 20 survived two independent sceptics; the most valuable was the `sizes` under-declaration, reproduced in a real browser by three of six verifiers.

---

### Phase 7 — Our Story + Brand Purpose

**Delivered.** `sections/our-story.liquid` (20,009 B) + `assets/section-our-story.css` (20,448 B): the editorial band on the three-track rail `--split-rail` (0.9fr 1.6fr 0.4fr) — copy / offset image window / caption rail — with fourteen settings in five groups and a `value` block limited to six. Zero JavaScript; 48 pixel-sampled contrast readings across both surfaces.

**Key decision.** The theme offers no focal-point control. Shopify admin's focal point is the single source of truth, because `image_tag` writes `style="object-position: X% Y%"` **inline on the `<img>`** and an inline style outranks every stylesheet rule; Phase 2's `overlay_style` select is likewise not exposed, because the scrim is mandatory. With no admin focal point the default is `object-position: center 33%`.

**Got wrong, corrected.** The band first shipped value-block copy written for it, over approved copy the project already held; it was replaced with the prototype's own three tiles, and a fourth line that duplicated the hero's copy was removed. "Worldwide / Shipping Available" was deliberately *not* shipped as a fourth tile — it is the one checkable commercial promise with no shipping policy, destination list or rate table behind it. 44 review findings, 30 confirmed. Two harness hazards were also recorded: `read_probe.py` only parses a dump already on disk, so run alone after an edit it reports the *previous* build's geometry (it now has a driver that regenerates first), and `http.server` answers `If-Modified-Since` at one-second granularity, handing back a 304 and the previous page — each reading now writes a unique filename.

---

### Phase 8 — Product & Shopping UX

**Delivered.** The first phase in which the theme can take money: `templates/product.json` → `sections/main-product.liquid` with the media gallery, variant picker and shared quantity selector inside Shopify's own `{% form 'product' %}`; `assets/cart.js` with no dependencies; `sections/cart-drawer.liquid`; the cart page; `snippets/cart-icon-bubble.liquid`. 197 structural checks, 92 browser interaction assertions, 56 contrast measurements.

**Key decision.** Buyability is read from the variant, never from whether a variant resolved. `product.selected_or_first_available_variant` returns the **first** variant when everything is sold out, so a nil check always passes and would report a sold-out product as buyable; `can_buy` therefore tests `current_variant != blank and current_variant.available`, and the form's `name="id"` input carries `disabled` whenever it is false. Alongside it: `updates[]` is positional, so exactly one input is emitted per line in `cart.items` order, with no gaps and no conditionals.

**Got wrong, corrected.** Two of the eight blockers would have taken a customer's money for the wrong product. The cart page was intercepted but never re-rendered, so removing a line did nothing on screen *and* the page's positional `updates[]` inputs no longer lined up with the server's lines — pressing Checkout would have applied each surviving quantity to the wrong product. And the drawer rendered on `/cart` as well, giving two views of one cart that can disagree plus a duplicate DOM id on every line, so the drawer's `<label for>` resolved to the page's inputs. Fixed by making the cart page a render target and never rendering the drawer on it. Two further defects were only findable by driving a browser: `inert` is inherited, so putting it on the section wrapper made the drawer itself inert (and the first version of that test gave a false pass by checking `hasAttribute('inert')` instead of `closest('[inert]')`); and because `image_tag` emits `width`/`height` **attributes**, a rule setting only `width` left every cart line 948px tall.

**Retracted by Phase 10.** The harness's `#{}` interpolation. A 133px logo and a 320px overflow were diagnosed as a harness bug and the harness was taught to interpolate `#{}`. Shopify Liquid has no such feature: the fix hid a real theme defect, and hid it for two phases.

---

### Phase 9 — Mobile UX + Responsive Polish

**Delivered.** No feature and no content — a measurement pass over every band Phases 4–8 had shipped, at twelve viewports in both orientations. Nine defects found, nine fixed, across six existing files; zero JavaScript added; one Liquid arithmetic change.

**Key decision.** Landscape adaptation is gated on **height** and bounded on both axes — `(max-height: 540px) and (max-width: 1023px)`. There is no `orientation: landscape` query anywhere in the theme, on purpose, because orientation says nothing about how much height there is. Full-height and fixed boxes are sized by the visible viewport (`100dvh`, `60svh`), never `100vh`, and nothing is hidden, shrunk or reordered on a phone: DOM order equals visual order at every breakpoint, body copy stays 16px, and the product page offers the same fifteen reachable controls at every viewport.

**Got wrong, corrected.** The fix for the landscape cart drawer silently deleted the safe-area padding the same phase had just added: a `padding-block` shorthand inside the landscape media query overrides an earlier `@supports` rule at equal specificity, and the control underneath it is **Checkout**. Caught in self-review after the fix, and repaired by nesting the `@supports` inside the landscape query. Honest caveat recorded with it: `env(safe-area-inset-*)` is 0 under `viewport-fit=auto`, so the new padding is inert until `viewport-fit=cover` is enabled — which is a sequenced four-step job, not a one-line change.

*Superseded:* this phase's "200.5 KB raw / 65.5 KB gzip" delivered-weight figure was corrected in Phase 13 to 22.2 KB gz JavaScript and roughly 72 KB gz CSS across nineteen files; Phases 16 and 18 carry the per-surface numbers.

---

### Phase 10 — Shopify Theme Architecture + Conversion

**Delivered.** The theme got its own root: 49 files relocated into `god-squad-theme/` and finished as a 66-file uploadable Online Store 2.0 theme. Five missing storefront surfaces added (collection, page, 404, search, footer group), the `design-tokens.css` / `base.css` split drawn so that **no token definition moved**, and the colour-scheme guardrail resolved in exactly one place (`snippets/css-variables.liquid`, rendered twice via a `part` parameter). 405 assertions across nine suites. Three deliberate absences that must stay: no `blocks/`, no `templates/customers/*`, and `assets/` holds only CSS and JS.

**Key decision — the two production defects, both live since Phase 4.** `font_face` returns a bare `@font-face` **rule**, not a style element. Emitted unwrapped it registered no face storewide (all of Phase 2's typography absent, everything falling back to a generic family) *and* printed the CSS text above the logo — because per the HTML parser's "in head" insertion mode a non-whitespace character token ends `<head>`, so `content_for_header`, all five stylesheets, the `:root` block and both scripts were parsed in body context. Both calls now sit inside one `{% style %}` block (`layout/theme.liquid`, lines 116–125 today). Second: **Shopify Liquid does not interpolate inside a string literal.** `"--logo-height-desktop: #{logo_h_desktop}px"` produced a valid declaration with a garbage value on the `<img>`, shadowing the good `:root` defaults, so `height` fell back to `auto` and the logo drew at intrinsic size — and it only bit once a logo was uploaded, which is the merchant's first Customize action. Built with `append` now.

**Got wrong, corrected.** The reason nine phases missed both: **the harness had never executed `layout/theme.liquid`.** Every suite from Phase 4 on rendered sections against a hand-written page template. `layout.py` now renders the real layout and parses it with a model of the in-head insertion rule — and its first version *passed with the bug present*, because `font_face` was stubbed to return `''` and no font settings were defined. A test that cannot fail proves nothing, so the filter was made to emit a real rule, the fix was reverted, two checks were confirmed to fail with exact evidence, and only then restored. Asset copying and translation scanning were also changed from hand-written lists to discovery, because "every defect a harness reports is worthless until you have proved the harness is serving what the theme references."

---

### Phase 11 — Theme Editor + Merchant Customization

**Delivered.** Every merchant-editable aspect made reachable and safe from the Theme Editor: `logo` and `cart_type` promoted to global settings (eleven global settings in eight groups), 100 section settings across thirteen sections, four block types with limits, and the section-lifecycle fixes. 443 assertions. Twelve of the brief's sixteen merchant tasks already passed before the phase; all sixteen after.

**Key decision.** The editor is the only place a section is replaced while the page stays alive, so a script's bindings outside its own subtree must be managed as state: every binding `header.js` makes is recorded in one registry and released as a unit on re-render and on removal, the teardown **closes the panel first** so it cannot leave a panel on screen with its lock already released, and `initHeader` is idempotent per element because `shopify:section:load` can fire for a node that was not replaced. Header clearance for the first section is expressed as a selector — `#MainContent > .shopify-section:first-child` — because position is a fact only a selector can know, not a setting a merchant must keep in sync with the order they just dragged.

**Got wrong, corrected.** A setting that looked purely cosmetic broke the purchase flow: hiding the quantity input removed form data `/cart/add` needs. The hidden branch now submits `qty_min` and carries `data-quantity-input` so `product.js`'s `updateQuantityRule` keeps it in step on a variant change through the same hook the visible control uses — and the governing schema rule became "do not expose settings that can break the product purchase flow", including ones that do not look like they can. The first lifecycle fix was also incomplete, and only a negative control found it: `editor.py` installs a counting shim on `EventTarget.prototype` before any theme script runs, and it showed `initHeader` re-binding the in-subtree toggle, so **one click opened the menu three times**.

---

### Phase 12 — Product + Collection + Catalog UX

**Delivered.** A correction phase: the brief audited into 104 checkable requirements, 91 already passing. Created `snippets/grid-sizes.liquid` (the shared `sizes` derivation for `main-collection` and `main-search`) and modified twelve files — a CSS-only secondary-image hover swap behind one global `card_hover_secondary_image` (off by default), a server-side low-stock line (boolean only, threshold default 3, product page only), the SKU row, and a third "Unavailable" button state for a variant combination that was never manufactured. 508 assertions.

**Key decision.** Fix the rule, not the instance. Phase 10 fixed the `sizes` desktop-clause bug in one of three copies, and the other two carried it for two more phases — hence one shared snippet and two written rules: a clause may not claim a width before the layout that produces it applies (desktop threshold floored at 1024), and a clause may not divide by more columns than actually fit. `featured-collection` deliberately keeps its own derivation and says so in the file (`sections/featured-collection.liquid:135`), so a change to the shared rules must be applied there too.

**Got wrong, corrected.** The secondary-image swap shipped with a cascade defect. `.product-card--sold-out .product-card__image` is (0,2,0); the rule hiding the secondary image, `.product-card__image--secondary { opacity: 0 }`, is (0,1,0) — and the secondary `<img>` carries both classes, so a sold-out product with two photos painted both superimposed at 60%, **on every device including touch**, while the stylesheet's own comment claimed a phone had no state in which it could appear. The first test passed because it asserted the rule *contained* `opacity: 0`: string-matching CSS cannot verify the cascade, only a browser can answer which rule won. `cardcascade.py` now measures computed styles and is negative-controlled (0.6 without the fix, 0 with) — and its own first run reported 900px stacked images, the shape of *no stylesheet*, because it rendered the snippet bare: the card's CSS is linked by the sections that use the card, not by the snippet.

---

### Phase 13 — Search, Filtering & Product Discovery

**Delivered.** `snippets/facets.liquid`, `assets/component-facets.css` and `assets/facets.js` for Shopify-native collection filtering, plus a header search disclosure panel layered over a byte-identical link to `/search`. 62 new assertions against four fixture states (none / all / active / degenerate), 570 in total.

**Key decision.** One form, one set of controls. The filter controls are rendered exactly once in the document and bound to a single `<form method="get">` by the HTML `form` attribute rather than by DOM nesting, so the desktop dropdown row and the mobile drawer are a CSS difference, not a second copy, and sort and filters submit together. Nothing filter-related renders — and neither asset loads — until a merchant configures filters in Apps › Search & Discovery; the "no filters configured" note appears in the Theme Editor only. The header search trigger stays a plain link because with scripting off it must still reach a complete search page; a `<button>` would have been a control that does nothing.

**Got wrong, corrected.** Two assertions in the new suite failed against the file's own **comments** — prose explaining the very rule being asserted ("no hardcoded option parameter", "does not use the cart's lock"). Strip comments before asserting on code. The phase also corrected a figure the project had been repeating since Phase 9: the theme is 22.2 KB gz JavaScript and roughly 72 KB gz CSS across nineteen files, of which no single page loads more than a fraction — not "~65 KB gzipped".

**Open by owner decision.** Predictive search is deferred, with its full implementation contract recorded (section-rendering endpoint via `routes.predictive_search_url`, six stale-response guards, `resources[limit]=4` with `limit_scope=each`). Filtering is deliberately not on `/search`, because applying a filter there strips all non-product results.

---

### Phase 14 — Cart + Cart Drawer + Checkout Experience

**Delivered.** An audit-with-repairs of the Phase 8 cart plus the four things Phase 8 never owned: `snippets/cart-note.liquid` (off by default on both surfaces, one field named `note`, native `<details>`), Continue shopping (a link on the cart page, a button reusing `[data-cart-close]` in the drawer), a `role="status"` add confirmation for stores whose cart style is "Cart page", and the two-column desktop cart page (`minmax(0, 1fr) 24rem` from 1024px with a sticky summary). 744 assertions.

**Key decision (method).** Every defect was reproduced with a failing test **before** it was fixed, and every fix was negative-controlled — reverted, watched to fail again, restored — "because a test that has never been seen to fail proves nothing, and this project has twice shipped a green test that was asserting on a comment."

**Got wrong, corrected — four defects, three live.** D1: the rule hiding the no-JS Update button lived in `section-cart-drawer.css`, and the cart page is the one page that never loads that stylesheet, so the button was `display: inline-flex` in production — *a selector is not a rule until something on the page it names has read the file it is in*. D2: `showCartError()` selected `[data-cart-error]` document-wide, so a quantity Shopify refused in the drawer would have printed "You can't add more…" into the error line of every product tile behind it. D3: a removal called `changeLine()` directly while quantity steps were debounced 250ms, and neither cancelled the other — a removed line returned at quantity 2; `changeLine()` now clears `pending[key]` on entry. D4: the quick-add card carried `data-cart-error` while `showFormError()` looks for `data-product-error`, so a failed add was announced to a screen reader and shown to nobody — and the Phase 12 test asserted the box *existed* rather than that the add path could *find* it.

---

### Phase 15 — Customer Account + Order Tracking + Post-Purchase UX

**Delivered.** One code change and a large body of asserted absence. The header's account `<a href>` became Shopify's `<shopify-account>` custom element with the `signed-out-avatar` slot keeping the brand mark and a visually-hidden name inside the slot; a global `customer_account_menu` `link_list` setting was added (default `customer-account-main-menu`). No theme file was created — the theme stayed at 71 files, five modified. 52 account assertions plus 22 seeded violations.

**Key decision.** Never ship `templates/customers/*`. Shopify deprecated legacy customer accounts on 2026-02-26, and publishing a theme *without* those templates is what upgrades the merchant — so shipping them does not make the theme safer, it **withholds the merchant's upgrade**. `templates/customers/` does not exist and never has (still true in the tree), held by eight assertions. Because there is no Liquid-readable way to detect which account system a store uses — `customer_accounts_enabled` is a show/hide gate, and the popular `routes.account_login_url contains 'shopify.com'` workaround is unsound — the theme has **one code path and branches on nothing**, and reads no customer field at all, printed or otherwise, because the Section Rendering API inherits the requested page's Liquid context and one `{{ customer.email }}` in a shared snippet would be serialised into every `?sections=` response the cart makes. Order history, order details, tracking and customer information have no theme surface on the current platform.

**Got wrong, corrected.** The phase's first version shipped a Dawn-style `:not(:defined)` size reservation plus account-specific sizing rules. Measurement killed both: with them removed the element still measured 44×44 at all seven viewports, because `class="header__control"` already sets `min-width` and `min-height` to `--target-min` inside a flex cluster. Both dead rules were removed — and an author rule on the element is *better* than `:not(:defined)`, which stops applying the instant the component upgrades. Then the negative-control suite caught its own blind spot: three assertions read a **pre-built** harness page, so a seed that changed the theme copy never reached them and one genuinely broken theme (an account control stripped of its shared class) passed clean. The suite now renders the header from the theme under test.

---

### Phase 16 — Performance + SEO + Conversion Optimization

**Delivered.** Ten audit dimensions, 82 findings raised, 62 confirmed, 12 rejected by the verifying pass. Seven changes plus two correctness fixes; one new file, `snippets/meta-social.liquid` (theme to 72 files), whose every value is a Shopify object with no written marketing copy; Jost 500 and 600 finally registered through guarded `font_modify` calls inside the same single `{% style %}` block; and the performance budget derived from the theme's own numbers — JS all pages ≤ 30 KB gz, per page-load script ≤ 10 KB gz, CSS worst page ≤ 55 KB gz, requests ≤ 30, load CLS ≤ 0.05, handler time ≤ 50 ms, eager images exactly 1, `fetchpriority` ≤ 1, third-party scripts each justified in writing. 945 assertions.

**Key decision — the P0.** A media-query listener that only runs on `change` never evaluates the width the page loaded at, so a desktop load left the filter drawer holding a scroll lock and a keyboard trap. Both directions now run through one `applyWidth()` called immediately **and** on change, `open()` refuses above the breakpoint, and CSS retires the trigger at `min-width: 768px` — the pattern `header.css` already used for the mobile menu. `applyWidth` is in `assets/facets.js` today.

**Got wrong, corrected.** "Theme Check cannot run because Shopify CLI is absent" had been repeated for three phases and was false of the checker: `@shopify/theme-check-node` had been in the scratchpad's `node_modules` since Phase 10, but the runner pointed at the *project* root, which stopped being the theme root the moment Phase 10 moved the theme — it had been scanning a directory with no theme in it and reporting zero offenses. Pointed correctly it found four: 4 → 2 on the default config, 7 → 5 on `theme-check:all`, the two residual `ValidJSON` errors being the missing `theme_support_email` and `theme_documentation_url`. Four of the phase's own measurements were also wrong before they were right: an LCP observer named a 78px logo because the harness has no image files and every image 404s; CLS counted synthetic clicks because `dispatchEvent` does not set `hadRecentInput`; CSS coverage reported 100% because cross-origin `contentDocument` threw and the catch marked every selector as seen; and the reference resolver called `grid-sizes` an orphan because inside a `{% liquid %}` block `render` is a bare statement. Lighthouse genuinely is unavailable, and no Lighthouse number appears anywhere in the document.

---

### Phase 17 — Analytics + Tracking + Marketing Integration

**Delivered.** A measured absence as the deliverable: 31 checks across 72 files found no GA4, GTM, Google Ads, Meta, TikTok, Pinterest, Snapchat, Clarity, Hotjar, Segment, Plausible, Matomo, PostHog, `dataLayer`, error monitor, hardcoded account identifier or third-party host (the only external origins are `shopify.com`, `schema.org`, `w3.org`). Plus standing prohibition tests, the UTM and campaign-naming conventions, a reserved-parameter guard for `ref` / `source` / `r`, and the Admin configuration the business must do itself. Two theme files changed.

**Key decision.** A theme cannot do tracking on Shopify any more, so it should not try. Standard events are emitted by Shopify from sandboxes the theme cannot reach — app pixels in a strict web worker with no `window` and no `document`, custom pixels in a sandboxed iframe — partners and merchants cannot publish standard events, and a snippet that bypasses the consent framework violates Shopify's Terms of Service. Therefore: no `gtag`, no second `fbq`, no `dataLayer`, at most one channel app per platform, nothing pasted into the theme or into Additional Scripts (sunset 2025-08-28), and the theme's whole load-bearing dependency is the single unmodified `{{ content_for_header }}`. The UTM discard by the theme's three GET forms is harmless and **must not be "fixed"**: Shopify records landing page and UTM parameters server-side at first request, GA4 fixes session source at session start, and carrying UTMs through internal forms would manufacture self-referrals.

**Got wrong, corrected.** The privacy question — *what customer-controlled data does the theme render?* — found a live stored-XSS the tracking question would never have asked. **Shopify Liquid does not escape output**, and both a cart line-item property and the cart note broke out of their markup and produced a live element with an event handler; both are settable by whoever posts to `/cart/add.js` or `/cart/update.js`. Both now carry `| escape` (`snippets/cart-line-item.liquid:142`, `snippets/cart-note.liquid:80`), verified by re-rendering the same payloads through the real snippets rather than grepping for the filter. Two seeded violations also exposed bugs in the auditor before they exposed anything about the theme: `rollbar` matched inside `scrollbar-gutter`, and the host check read only `src`/`href` attributes and so missed a seeded Meta Pixel entirely — because every real pixel injects its own `<script>` and therefore carries its host as a string literal inside JavaScript, which is precisely the case the check exists for.

---

### Phase 18 — Final Polish + Award-Level UI/UX QA

**Delivered.** A measured pass plus fourteen review agents over seven dimensions: 98 confirmed findings deduplicating to 70 distinct defects — 12 fixed (+4 found only by measurement), 55 recorded as verified but deliberately unchanged, 2 raised to the merchant, 1 rejected. Three new files (`snippets/pagination.liquid`, `assets/component-pagination.css`, `assets/component-container.css`) and 34 modified, taking the theme to its current 75 files, with the CSS rules-only payload **down 2,501 B (−2.5%)** despite two more stylesheets. Twelve elements across eleven stylesheets that each carried a private copy of the container's four declarations were swept into `.container` / `--wide` / `--narrow`; the two per-template paginators became one.

**Key decision.** A CONFIRMED review verdict is a claim, not a fact. Two findings the reviewers rated HIGH were overruled with citations: the chevron legitimately ships at two sizes (Phase 2 assigns it both `--icon-sm` 16px inline and `--icon-md` in controls — a 24px glyph beside a 12px filter label would be the defect), and "Add to bag" is a decided brand term, not drift from the fourteen "cart" strings. Everything left alone carries the same written deferral test: cosmetic or structural tidying whose risk outweighs its benefit in a phase that is explicitly not a redesign.

**Highest-corroborated defect (found seven times across four dimensions).** `icon-chevron.svg` is drawn pointing **right** and rotated per consumer. The product page rotated it correctly; the filter groups and the cart note applied no base rotation at all, so the chevron pointed right when closed and *left* when open — the 180° sweep had been implemented, the direction it rotates *from* had not. All three disclosures now measure DOWN (90°) closed, UP (270°) open, one 180° sweep.

**Got wrong, corrected (method).** `getClientRects()` on an atomic inline returns one rect however many lines its content occupies, so two probes called the same cart title "1 line" and "2 lines"; a `Range` over the text node produced the real 14.0px-in-cart versus 17.4px-on-card reading that justified `--type-label-lh: 1.45`. A transitioned property reads as its start value if read in the same frame — Phase 4's lesson, which the chevron probe forgot. The dead-code scanner was wrong three times before it was right; its first answer, 162 items, would have been a fabricated number in the report. And a "nothing moved" blast-radius result meant the injected rule had never applied, not that the fix was inert.

**Open against the code, found while writing this manual.** Phase 4 established that the canonical `PHASE-2-DESIGN-TOKENS.css` and the theme copy `god-squad-theme/assets/design-tokens.css` must carry identical token sets, and Phase 6 kept them in step. They have since diverged by exactly one token: the theme copy declares `--type-label-lh` (`design-tokens.css:217`, added in Phase 18) and the canonical file does not. Every other token name matches. Add it to the canonical file, or record the divergence deliberately.

**Closing status.** The theme is code-complete and internally coherent, and not launchable, for reasons that are not development tasks: merchant photography (the hero currently ships an AI-generated image with unconfirmed rights, and the section schema now instructs the merchant to replace or clear it before launch), a vector logo master and favicon, and the business information Theme Check is still asking for. The image half of a visual audit is recorded as **NOT ASSESSABLE** — everything reviewed was the reservation (aspect box, `object-fit`, scrim, alt path), never a picture. Five decisions remain with the owner: bag vs cart, the mobile menu link type, the footer link type, the unsupported "Worldwide Shipping" claim, and the announcement-bar raster icon.

---

## Appendix — completeness review of this manual

Two independent critics checked this manual against the index of all 514
governing decisions: one for material dropped in the consolidation, one for
whether an integrator could actually work from it.

### Critic 1

**Verdict.** Partly trustworthy, and trustworthy in an uneven way that makes it dangerous to use unsupervised. Its spine is excellent: I checked the hard numbers against disk and the prototype inventory (44 files / 17,185,754 bytes), `support.js` (69,150 B / 1,911 lines), the entry HTML (15,632 B), both mockups (1024×1536 / 1,872,888 B and 182,250 B), the theme file count (75), `theme_version` 0.5.0, the absence of `.git` and of `templates/customers/`, `design-tokens.css:49-51`, `our-story.liquid:342`, the `header-group.json` message-1/message-2 pair, the missing `button_link`, the two collection-less `featured-collection` sections, the zero hardcoded menu labels, the zero hardcoded currency symbols, the absent BreadcrumbList/Organization JSON-LD, the guarded social row, and the BUSINESS INFORMATION REQUIRED / DECISION counts (169 / 52) — all correct, and I independently recomputed the 1.55:1, 1.43:1, 4.66:1 and 17.04:1 contrast figures and Appendix A's four Phase-2-gating decisions and got the same answers. It also handles supersession well where it matters most: the 17-row roadmap, THE PROHIBITION over Phase 0 §5's unconstrained gold, and Theme Check's availability are all correctly marked current. But it fails in the one direction a consolidated manual must not: where it fills gaps in the sources it does so without saying so, and twice the filler is wrong in a way no reader can detect. The disposition statistic is a grep count dressed as an audit result and is arithmetically impossible on its face. The "hero ships an AI-generated image" line is contradicted by the theme's own schema string. The brand-message table asserts a shipped script-accent level for a typeface the theme never loads and a token nothing reads. And the section that exists to state what is approved and what ships omits the one homepage band — Best Sellers, with two strings authored nowhere in the twenty documents and one of them an endorsement claim — that its own standing rules 1, 8 and 9 would forbid. As a replacement working reference for project identity I would use it for the standing rules, the phase table, the register and the prototype archaeology, but I would re-derive every "ships today in" cell and every statistic against the code before quoting it, and I would restore the two dropped Phase 0 measurement constraints and the approved-copy row before treating its scope and visual-direction statements as complete.

**Governing rules it could not find in this manual (8):**

| Rule | From | Belongs in |
|---|---|---|
| "The page must be served over HTTP to be inspected in the desktop preview pane. Opened as a local file there, it renders as a static snapshot in which the runtime and images never resolve. A | Phase 0 §7.1 (L224) | This section — "Two working constraints  |
| "The preview pane screenshot captures only part of an emulated viewport. Full-page images come from headless Edge; the pane is used for DOM measurement." — Phase 0 §7.1 constraint 3, which d | Phase 0 §7.1 (L226) | This section — "Two working constraints  |
| "**Copy:** every headline, eyebrow, tagline, verse reference and the Our Story paragraph as written" — one of the six rows of Phase 1's "What is approved and must be preserved" list. The sec | Phase 1 §1 (L60) | This section — "The approved visual dire |
| The mockup PNG "is the approved design master... **It is never a production website image**, and any re-cut should take full-quality pixels from the PNG rather than from the WebP derivative. | Phase 3 §2 (L186) | This section — "The approved visual dire |
| The restraint test: "Before any element is added in a later phase, two questions: *does the prototype already do this?* If not, *what changed, and what is being removed to pay for it?* **Res | Phase 2 §2 (L123–196) | This section — "The brand", where LUXURY |
| Phase 2's register of strings that are NOT brand messages has six entries; the section lists four. Missing: "`A Higher Purpose.` (line 93)" and "`A Brighter Tomorrow` (line 164)" — "all sect | Phase 2 §2, "Strings tha | This section — "The brand", the paragrap |
| "Fix the rule, not the instance." Phase 10 fixed the `sizes` desktop-clause bug in one copy; "the other two carried the bug for two more phases, because the fix was applied to an instance ra | Phase 12 §2 (L83) | This section — "The standing rules", as  |
| Phase 0's exit-criteria checklist leaves exactly one box unticked: "[ ] Scope and exclusions drafted from the foundation conversation, but **not formally confirmed by the owner**." Eighteen  | Phase 0 §13 (L319) | This section — "Scope" |

**Stale rules it found repeated (2):**

- Standing rule 8: "`theme_documentation_url` and `theme_support_url` are omitted rather than filled with a fabricated URL." — in *The standing rules → rule 8 ("No fake da*, superseded by Phase 16 §19 names the actual pair Theme
- The brand-message table reserves a "Script accent — one per page" level for `More Than Clothing.`, and the visual-direction table lists "Kaushan Script hand-lettered acce — in *The brand → the five-message table; The *, superseded by Phase 16 §9 fixes the registered set at 

**Internal contradictions it found (6):**

- Standing rule 8: "`theme_documentation_url` and `theme_support_url` ar vs "Where the work stands now": "the outstanding business information — i — The section names two different key pairs for the same omission four screens apart, and never reconciles them. `config/settings_schema.json` contains 
- "Phase 18's verdict... no merchant photography (the hero ships an AI-g vs `god-squad-theme/sections/hero.liquid:183`, the merchant-facing `info` — The code disproves the claim. `templates/index.json`'s hero block carries no `image` and no `mobile_image` key at all, and `image_picker` settings can
- "On light surfaces the accent is `--color-accent-strong` `#82672B` (4. vs `assets/design-tokens.css:63` is `--gs-gold-strong: #82672B;` — the ra — The citation points at the wrong layer. Phase 2's R2, which this manual restates elsewhere, forbids anything outside the token file from referencing `
- "Phase 1 classified each of its 200 issues with a fixed disposition vo vs Phase 1 §28's own counts: "P0 — BLOCKER: 3 issues. P1: 65. P2: 80. P3: — The six numbers sum to 235, which cannot be a per-issue classification of 200 issues — the section contradicts itself in the same sentence. Worse, the
- "`More Than Clothing.` | Script accent — one per page | Ships today in vs `templates/index.json:74` ships the `faith` value block as `"title": " — Two errors in one cell. The shipped string has no full stop, so it is not the canonical message as quoted. And a value-tile body paragraph in the inte
- "Section order | Announcement bar, header, hero, New Drop, Our Story,  vs `templates/index.json` order is `hero`, `new-drop`, `best-sellers`, `o — "Chosen by the community." appears in the prototype zero times and in all twenty phase documents zero times; "The Pieces That Define The Movement" app

### Critic 2

**Verdict.** Trustworthy on structure, untrustworthy on its rules. Every quantity I could measure against disk was exact — 75 files (25/2/1/1/16/23/7), 21 CSS and 4 JS with no images or fonts, 104 section settings across 13 schema-bearing sections with every per-section settings/header/block/preset/tag/enabled_on cell correct, 117 locale leaves in 8 groups, 193 distinct tokens in 207 declarations with 187 inside :root and all 17 group names, the 65-block media-query census to the last row, four !important all in base.css's reduced-motion block, 17 hex in the token file plus four #000 in section-our-story.css, zero {% include %}, zero {% stylesheet %}/{% javascript %}, seven sections emitting the dead section.shopify_attributes, eight surface sections, three spacing sections, three section-scoped {% style %} blocks, every byte count (design-tokens 26,309; base 3,722; cart.js 39,750; header.js 13,963; product.js 18,096; facets.js 10,937), every token value in the values table, the surface-class CSS and the focus-ring rule quoted verbatim, section-hero.css:31 to the line, and the stale design-tokens.css header comment it honestly flags. As an inventory of the theme as built, it can replace the twenty documents. As a statement of the rules the theme holds itself to, it cannot yet: five of the fifteen closing conventions are stated as absolutes the code refutes (tag/class on every section, no size setting below theme level, no inline style outside a section root, no hardcoded section id, stylesheets inside their render guard), the design_mode count is two phases stale, radius_sm's type is simply wrong in a way that inverts a Phase 2 guardrail, the cart.js threshold row prints a gzipped figure as raw and then draws the opposite conclusion from it, the card-stylesheet promotion exception rests on a premise index.json disproves, the canonical token file is one token out of step with the copy the manual says is kept in step, and about a dozen governing rules that belong here — no-JS operability of every control, no browser storage or console logging in theme scripts, no eval/new Function, no undefined custom property, no magic numbers, the block-granularity test, "anything a merchant could change to break the hierarchy stays out of the schema", the layout's lang attribute, "a selector is not a rule until the page has read its file" — are absent entirely. Fix the fifteen-item conventions list and the four numeric/typing errors and it is a sound working reference; used as-is, a developer checking compliance would flag correct code as defective in at least three places and miss real rules in a dozen more.

**Governing rules it could not find in this manual (17):**

| Rule | From | Belongs in |
|---|---|---|
| "A selector is not a rule until something on the page it names has read the file it is in." (D1: the rule hiding the no-JS Update button had to be moved into section-main-cart.css because .m | Phase 14 §1.1 | This section — "The asset set / Who link |
| The block-granularity test: "If a block type has one field, it is a setting. If it has more than four, it is a section. A block is never created to let a merchant reorder two items that have | Phase 2 §29 | This section — "Sections — the schema co |
| "Anything a merchant could change to break the hierarchy is left out of the schema" — with the named exclusion list: the section grid ratios, the gradient fade technique, the letter-spacing  | Phase 1 §29 (restated in | This section — the schema conventions; i |
| "Behaviours the specification does not name are exposed as theme settings with the approved design as the default, rather than being decided silently." | Phase 4 §0/§3 | This section — the schema conventions (i |
| "header.css must use tokens only: no raw hex, no !important, no reach into the --gs-* palette layer, and every token it references must exist." The fourth clause — no undefined custom proper | Phase 4 §5 / Phase 9 §15 | This section — "The conventions the them |
| "no !important, no raw hex (other than the #000 keyword inside a mask gradient), no magic numbers — every value is a Phase 2 token or a measured floor with its arithmetic in a comment." The  | Phase 7 §10 | This section — "The conventions the them |
| "Every control works without JavaScript." The product form posts natively to /cart/add, the cart form to routes.cart_url with updates[], removal is item.url_to_remove, the header cart contro | Phase 14 §1 (one of the  | This section — the JavaScript subsection |
| "No customer data in any client-side store. localStorage, sessionStorage, indexedDB, document.cookie, caches.open and service-worker registration are each asserted absent from every theme sc | Phase 15 §11 / Phase 17  | This section — "The conventions the them |
| "the theme's own JavaScript must not use eval or new Function." | Phase 1 §24 (line 2430) | This section — "The conventions the them |
| "Do not build .icon--sm/md/lg/xl utilities: that would add a second sizing mechanism beside the parent-scoped one the theme actually uses. Icon size is set by the consuming component's own . | Phase 18 (Visual Audit,  | This section — the snippet-set icon cont |
| "One section, not two." Best Sellers and New Drop are the same section type with two presets; "sections/best-sellers.liquid deliberately does not exist, so a second file would mean fixing ev | Phase 6 §1 | This section — "Five absences are decisi |
| layout/theme.liquid must set "<html lang=\"{{ request.locale.iso_code }}\">" (Phase 1 §29.2 requires it; Phase 4 records it as delivered and it retires audit finding HTML-02). | Phase 1 §29 / Phase 4 §5 | This section — the layout inventory, whi |
| "Approved existing brand copy is preserved rather than replaced — every default is the prototype's own wording, and every one is a Theme Editor field so an alternative direction stays one ed | Phase 7 §1 (with Phase 5 | This section — the schema conventions; i |
| "Checkboxes use the theme's shared .visually-hidden utility rather than re-declaring the hiding rules" — there is one hiding utility and components must consume it. (On disk it lives in asse | Phase 13 §10 | This section — "The asset set" three-lay |
| "The footer logo renders only when the merchant asks for it and a logo exists — a checkbox that produces an empty gap is worse than no checkbox." | Phase 11 §2.1 | This section — the schema conventions (s |
| Duplicate stylesheet <link> tags are left in place on purpose: "Measured at the network layer: 11 CSS requests, not 13 — the browser deduplicates. ... Promoting the stylesheets to the layout | Phase 16 §18 | This section — "the promotion rule" para |
| Theme asset naming: "lower case, hyphens only, ASCII, no version words, no generator hashes, no numeric ordering prefixes, semantic order type-subject-qualifier, one extension matching the r | Phase 3 §16 / Phase 1 §2 | This section — "The asset set", which li |

**Stale rules it found repeated (2):**

- "Every `request.design_mode` branch is a configuration notice, never a different layout. **Four sections carry one** — `featured-collection`, `our-story`, `main-page`, `f — in *Sections — the schema conventions, conve*, superseded by Phase 13 §4.5 added a fifth: main-collec
- "There is no spacing, size, colour, tracking or z-index setting anywhere below theme level except `surface`." — in *Sections — the schema conventions, conve*, superseded by Phase 2 §28's absolute was superseded by

**Internal contradictions it found (12):**

- "Every section declares `tag` and `class`." (convention 1) vs The table immediately above it shows an empty `tag` cell for `cart-dra — The convention is stated as universal two paragraphs after the section's own table disproves it. Verified: of 14 section files, 13 have a schema and o
- Global settings table: "`radius_sm` | range 0–8 step 1 | 2 | `--radius vs `config/settings_schema.json` defines `radius_sm` as `"type": "select" — The code disproves the type, the range and the value shape. This is not a harmless slip: Phase 2 §16 makes the constraint load-bearing — "the merchant
- "`component-product-card.css` has three consumers but is **never doubl vs The section's own JSON-templates table says `index.json` holds "two `f — The stated exception to the promotion rule rests on a false premise, and by the rule as written ("a component stylesheet with more than one consumer o
- "`cart.js` | 39,750 | … 12,073 B gzipped, above Shopify's 10,000 B `As vs Measured on disk: stripping every comment from cart.js leaves 20,616 r — Two defects in one row. (1) The number is printed in a table whose "Bytes" column is raw, where 4,930 B is arithmetically impossible (39,750 − 18,190 
- "Spacing is a select of system values, never free pixels… There is no  vs "which is why `logo` is global while its two *heights* stay on the hea — The absolute in convention 6 is refuted by convention 7 one bullet later and by two `"unit": "px"` range settings in the code. There are 15 section-le
- "nothing in the theme derives from a hardcoded section id" (closing th vs The same section states, three paragraphs earlier, that "rendered stat — Two hardcoded section ids are load-bearing in cart.js, and the manual presents them as a design feature in one place and as impossible in another. Pha
- "**No inline `style` attribute** except the Liquid-generated custom-pr vs On disk there is no inline `style` attribute on any section root. The  — The named exception does not occur and the occurrences are not covered by the exception. The section itself explains why no section root carries one —
- "**Stylesheets sit inside their section's render guard, not at the top vs On disk 9 of the 15 section-emitted stylesheet links sit at the top of — Stated as a universal, true only of the three sections that have a render guard at all (featured-collection, our-story, and main-search's card sheet /
- "It is the theme copy of the canonical `PHASE-2-DESIGN-TOKENS.css` in  vs Measured: `PHASE-2-DESIGN-TOKENS.css` in the project root declares 192 — The two files are out of step right now, and the section states the invariant — Phase 4's "must carry identical token sets" — as though it holds. This
- "Phase 18 deleted four of them and recorded the single reinstatement c vs `assets/component-cart-line.css` records it twice — at ~line 131 and a — The code disproves the "once" and also disproves the implied completeness of the Phase 18 sweep. Phase 18's decision text ("the single reinstatement c
- "Loaded from its own section (**13 links, 11 files**)" vs The table under that heading lists 13 distinct filenames (11 `section- — Both numbers are wrong and they are wrong in a way the section's own arithmetic catches: 8 + 11 = 19 ≠ 21. Correct is 15 links across 13 files.
- "`config/settings_data.json` carries a `current` block and one preset, vs `current` carries 12 keys including `"favicon": ""`; the `"God Squad"` — Minor but checkable: the two blocks are not identical, and a merchant who resets to the preset does not get the favicon key back. The section's next s

### Critic 3

**Verdict.** This is a strong section and, on measurement, the most trustworthy kind of reference — but it is not yet a safe replacement for the documents it folds in. Almost everything I could check on disk held exactly: 193 tokens in the theme copy against 192 canonical with `--type-label-lh` the only difference, and all 57 colour-family token values byte-identical between the two files; design-tokens.css at theme.liquid:135 immediately before base.css; the two surface blocks quoted verbatim with their seven reassignments each; consumer counts 47 / 31 / 15 / 7 / 2 all exact; the hero wash stops 66-90, 54-82, 48-76; all sixteen hero contrast figures to two decimals against Phase 5; the status-colour line numbers 423, 453, 125, 352, 405; the footer hairline at section-footer.css:27 and 202; the mask gradient at 468 and 470; eight surface selects with the exact "Colour scheme" / Ink / Cream vocabulary and the exact defaults listed, five hardcoded sections, index.json's two alternations; 39 of 193 tokens unreferenced matching its named list; zero `prefers-color-scheme` / `forced-colors` / `prefers-contrast` anywhere; 29 hover rules with 0 ungated; and the stale `[THEME SETTING]` comment exactly as flagged. Where it overrules Phase 2 it overrules it correctly — the swatch ring moving to `--color-text-current-muted`, the corrected scrim alpha, the added interactive border family. What it cannot yet be trusted on is its counts and its absolutes. Three of its "only / two / four" claims are false against the code (`--color-accent` is read directly in three more places in header.css; the `--gs-` grep returns three comment hits, not four; four `info` strings state the gold consequence, not two), one table row is inverted by the code and by the section's own prose (`--color-surface-raised` is the Primary-on-light hover), and the Borders table both forbids the only shipped use of two of its tokens and authorises two pairings its own R4 register does not contain. More seriously, it asserts that one rule owns focus and that a component never chooses its own ring while eight stylesheets declare an outline and five declare `outline: none`, and it drops Phase 2 §23.4 — the single rule that makes those five legal and bounds them. It also loses the two governance rules that protect the mechanism it exists to explain: Phase 2 §28's deliberate refusal of Shopify's native `color_scheme` setting type, and R5 plus the MAJOR-bump half of the versioning policy. Use it for the measurements, the token inventory and the surface mechanism; re-read Phase 2 §§1, 23, 28 and Appendix A.1 before touching focus, the scheme select or the palette's admission rules, and verify every "only" in it against a grep.

**Governing rules it could not find in this manual (14):**

| Rule | From | Belongs in |
|---|---|---|
| "`surface`, not `color_scheme`. Each band exposes `surface` — a two-option select, dark or light, mapping to the `.surface-dark` / `.surface-light` classes — and nothing else. Shopify's nati | Phase 2 §28 (PHASE-2-DES | "Merchant-facing colour: the scheme sele |
| "`outline: none` and `outline: 0` are prohibited unless the same rule substitutes an equally visible indicator in the same declaration block. Acceptable substitutions are a `box-shadow` ring | Phase 2 §23.4 "Never rem | "The focus ring is surface-aware for the |
| "Gold may carry at most one word inside a headline. `Faith.` (line 84) is the precedent and the ceiling." — carried forward in the restraint-budget table as "Gold words inside a headline \| 1 | Phase 2 §2 (LUXURY THROU | "Gold budgets". The section lists one go |
| "The outline is never clipped: any ancestor with `overflow: hidden` around a focusable element must leave room for `--focus-width` + `--focus-offset`." And: "The ring is drawn on the control | Phase 2 §23.2 (The ring) | "The focus ring is surface-aware for the |
| The focus ring's third ground: "Product tile ground `#EBE6DC` \| `--focus-ring-on-light` \| ink \| ~16.5:1". | Phase 2 §23.3 (Why the r | The focus-ring token table. The section' |
| "**R5 — Gaps are raised, not filled.** Where a value is needed and no token exists, §30 records it as a token request under the versioning rules below. Inventing a token name or value locall | Phase 2 §1 ("How to use  | "Group 2 — the semantic layer, and the t |
| The MAJOR half of the token versioning policy: "A token is removed or renamed, or a value change alters a verified contrast pairing → MAJOR", with "changing `--gs-gold`" as the worked exampl | Phase 2 §1 (Versioning)  | The "Admission test for a new colour" an |
| The seven-row colour acceptance gate with its evidence methods — notably check 1, "Every colour comes from a semantic token; no raw hex in component code \| Evidence: Search the stylesheet fo | Phase 2 Appendix A.1 (De | A colour-QA subsection this section does |
| "...and **no brand colours**: Facebook blue and Instagram's gradient would both break the monochrome footer, and the current two-tone circled badges already cannot take the theme's link colo | Phase 2 §22.6 (Social ic | "The prohibition" / "Admission test for  |
| "The scrim and the caption backing are `pointer-events: none` and sit behind the content layer; nothing overlays a focusable element (2.4.11), and the scrim is `aria-hidden="true"`." | Phase 7 (L422), restatin | "Scrims", beside the two structural rule |
| "**Editorial sections** are a composition pattern, not a surface: they may be dark or light and are governed by §26." | Phase 2 §4 (immediately  | Operating rule 3, "Nesting, and what 'in |
| The colour-usage permitted-uses mapping: "MUTED GOLD → accent, selected states, small labels, editorial details, borders where appropriate, subtle emphasis → `--accent-current` on dark; `--c | Phase 2 §4 ("Colour usag | "Group 2 — the semantic layer". The sect |
| "An inline link inside running copy is always underlined at rest: on cream, `--color-accent-strong` at 4.66:1 is legible as text but is not a sufficient sole indicator of link-ness, and gold | Phase 2 §22.7 (Links in  | "Colour is never the only carrier of mea |
| "Rendered only from native Shopify swatch data (`value.swatch.color` / `.image`). **No colour is ever guessed from an image or a name**" — with the dots `aria-hidden` and the colourway names | Phase 6 (L203) and Phase | "Colour is never the only carrier of mea |

**Stale rules it found repeated (4):**

- "One rule owns focus for the entire theme, in `assets/base.css:58`... `:where()` contributes **zero specificity**, so any component-level `outline` would silently win...  — in *Surface-aware tokens → "The focus ring i*, superseded by Phase 6 ("The ring is drawn around the *
- "`--color-surface-raised` | `--gs-ink-raised` `#2A2823` | **Hover fill on dark**" (Surfaces table) and "`--gs-ink-raised` | `#2A2823` | **Dark button hover fill** | 12.83 — in *Group 1 — the core palette; Group 2 → Su*, superseded by Phase 2 §22.3's own button matrix, and t
- "`--color-border-interactive` | `rgba(243,239,230,0.36)` | ... | Permitted on: Form fields, checkboxes, radios, selects, outlined buttons, **swatch rings** — dark" and "` — in *Group 2 → "Borders — two families, and t*, superseded by Phase 8 / Phase 12, which put the swatch
- "`--color-accent` is named directly only inside `component-button.css`'s `.surface-dark .button--accent` rules, where the surface is already in the selector." — in *Group 2 → "Accent (3)"*, superseded by Phase 15, which added two more direct re

**Internal contradictions it found (10):**

- Surfaces table: "`--color-surface-raised` | `--gs-ink-raised` `#2A2823 vs Gold budgets: "Primary on dark now lifts to `--color-text-secondary` ( — The section calls one token a dark-surface hover fill in two tables and a light-surface hover fill in its prose. The code decides against the tables: 
- "`--color-accent` is named directly only inside `component-button.css` vs `assets/header.css:319` `--shopify-account-color-accent: var(--color-a — Three further direct reads of `--color-accent` ship, in a second file, and none of the three selectors carries `.surface-dark`. They are defensible un
- "Grepping every `.css`, `.liquid` and `.js` file for `--gs-` outside t vs The grep returns three comment occurrences on two lines — one `--gs-cr — The claimed count matches neither the cited line numbers nor the file. The section explicitly invites the reader to run this grep as the proof that th
- Borders table: "`--color-border` | `rgba(243,239,230,0.12)` | ~1.32:1  vs `component-button.css:123` `.surface-light .button--secondary:hover {  — The shipped theme's sole direct uses of these two tokens are control background washes, which the permitted-on column forbids. Every actual hairline r
- "**R4 — no colour pairing ships without a measured ratio.** A pairing  vs The same section's Borders table ships `--color-border-subtle` and `-- — The section authorises two pairings that its own register does not contain, which is precisely what R4 forbids. Phase 2 §30.99 recorded the range ("th
- Contrast register: "`#FFFFFF` white | `#0D0C0A` ink | 19.55:1 | AAA —  vs Group 1: "Three approved colours, seven derived values. Spec-approved  — White is not a palette token, is not derived from ink or cream by lightness, and has no cream-surface measurement (it would be 1.09:1), so the section
- "Two sections state the consequence of the switch in their own merchan vs Four shipped `info` strings state it. `sections/featured-collection.li — The section undercounts the shipped merchant-facing copy by half and, by naming only two, implies the other six surface selects say nothing about the 
- "Two cart stylesheets record that they deliberately carry **no** `.sur vs Both notes are in one file: `component-cart-line.css:131` ("No .surfac — Phase 18 deliberately consolidated this — "the single reinstatement condition is documented once in component-cart-line.css rather than twice". The se
- "On a section whose surface cannot vary, reading the surface-specific  vs The two direct `--color-text-muted` reads are at `header.css:513` and  — The stated exception is narrower than the theme's, so the one place the theme legitimately pins both ends of a verified pairing on a variable-surface 
- Scrim divergence table: "`--scrim-header` | Consumers: 2 (`header.css` vs `header.css` reads `--scrim-header` once, at line 179. The second refe — The consumer count conflates two tokens, so the table's only non-zero photographic-scrim figure cannot be reproduced from the table's own terms — and 

### Critic 4

**Verdict.** Qualified yes — this is the strongest kind of reference for its subject in the places that matter most, and it should not be shipped as-is. Its load-bearing content survived every check I made against disk: the 11 `font-family: var(--font-display)` rules and their exact selectors, the 92 `font-family: var(--font-body)` rules, zero consumers of `--font-script`/`--type-script-*`/`--type-h1-*`, two `font_picker` settings with the `playfair_display_n9`/`jost_n4` defaults, the four guarded `font_face`/`font_modify` calls inside one `{% style %}`, the 900-face trap (no shipped rule pairs a sub-900 weight with `--font-display`), `--type-label-lh: 1.45` at design-tokens.css:217 with exactly its two wrapping consumers, `base.css:44` as the only element type rule in the theme, 57 `text-transform: uppercase` and zero `none`/`capitalize`/`lowercase`, exactly one all-caps string (`SKU`) among 117 locale strings, `font-variant-numeric: tabular-nums` once at component-facets.css:194, no `font-synthesis` anywhere, no literal `→` or `₱`, and exactly one `font-size` inside a media query (section-hero.css:424) — and every cell of the 375→1920 clamp table recomputes correctly, including the 659px, 870px, 1318px and 1467px thresholds. The judgement in the prose is also better than its sources: the correction that Phase 9's \"605px\" is 68ch, i.e. `--measure-body` not `--measure-narrow`, is right, and the refusal to merge `--type-label-lh` with `--type-tagline-lh` is exactly the distinction a later phase would collapse. What fails is the census work and the standing-rule layer. Four of fourteen rows in the \"as actually shipped\" table cannot be reproduced (`--type-body` is stated as \"13 across 14 files\", which is arithmetically impossible and is really 13 declarations in 14 rules across 10 files), the corpus those counts claim to come from — \"24 component/section stylesheets\" — does not exist (there are 21 CSS files, 19 component/section), the reading-measure inventory omits five real consumers including the product page's whole description column and mis-names a sixth, the display inventory is declared complete while a twelfth site hands Playfair 900 uppercase to the entire `<shopify-account>` sheet, and the merchant rich-text H5/H6 rows render as labels with no mention anywhere. On the rules side it drops the one rule that protects the display voice from being loosened (\"display line-heights are fixed by token and are not a per-section decision\"), the `h1` 32px floor that its own landscape exception breaks at 28px, the 16px input floor and its iOS-zoom reason, the stylesheet-ordering precondition without which the merchant font picker it advertises silently stops working, the script accent's rotation, and the Phase 4 rule that the canonical token file and the theme copy stay identical — a rule that is broken right now, by this section's own `--type-label-lh`, and that the section is the only place anyone would notice. It also credits the pre-integration design review's `body { font-family }` change to Phase 18. Treat the mechanics, thresholds, exceptions and contrast reasoning as authoritative; re-derive every count from the 19 stylesheets, rebuild the consumer inventories from grep, and fold the six dropped rules back in before it replaces the source documents.

**Governing rules it could not find in this manual (10):**

| Rule | From | Belongs in |
|---|---|---|
| "A tight line-height under a 900 serif at 112px is the whole composition... it is the first thing a later phase will be tempted to loosen. The rule is: display line-heights are fixed by toke | Phase 2 §5.2 (The displa | Design system — typography (this section |
| "The canonical PHASE-2-DESIGN-TOKENS.css and the theme copy (assets/design-tokens.css) must carry identical token sets" (Phase 4 decision, L86; restated in Phase 6: `body { margin: 0 }` was  | Phase 4 (§5/decisions),  | Design system — typography (the one dive |
| "Headings scale with `clamp()` and never fall below 32px for an `h1`." (PHASE-9-MOBILE-RESPONSIVE.md:493-494, stated alongside the 16px body rule the manual DOES quote.) The manual carries o | Phase 9 §11 / §6 | Design system — typography (this section |
| "The note field is 16px for a reason beyond type: below 16px iOS zooms the viewport the moment the field takes focus, and a zoomed cart is a cart the customer has to pan to read." (PHASE-14- | Phase 14 §12.1 | Design system — typography (this section |
| "The `css-variables` snippet takes a `part` parameter and is rendered twice — the theme-color meta belongs early, and **the style element must come after the stylesheets or its `:root` decla | Phase 10 §6 | Design system — typography (this section |
| The 12px/16px floor "moves **eight** things, in both directions" — and the manual lists only six. PHASE-2-DESIGN-SYSTEM.md §6.2's table has eight rows: cart badge 9→12, announcement 11→12, v | Phase 2 §6.2 (and Append | Design system — typography (this section |
| The script accent is **rotated**. Phase 2 §26.2 specifies it as "Kaushan, rotated, at most once per page \| `--type-script-size`, `--type-script-lh` 1.10 \| line 91, `rotate(-8deg)`" (PHASE-2- | Phase 2 §26.2 / §21 | Design system — typography (this section |
| "No external font requests (no fonts.googleapis, fonts.gstatic, @import or Typekit)." (Phase 9 §12; re-asserted in the Phase 16 font work.) Verified still true — `grep -rn "googleapis\|gstati | Phase 9 §12 (restated Ph | Design system — typography (this section |
| "Still open, and deliberately so. `--focus-ring-companion` ... and `--type-label-weight-nav` (the prototype's 500 nav weight against the label triplet's 600) are recorded as recommendations  | Phase 2 §30.99 (and §19) | Design system — typography (this section |
| "Phase 2 defines the loaded set as Playfair Display 900, Jost 400/500/600 and Kaushan Script 400 — five faces, not the six the prototype's font URL requests. The sixth is Playfair Display 70 | Phase 2 §5.1 (PERF-04) | Design system — typography (this section |

**Stale rules it found repeated (2):**

- "`--type-label` | **65 across 15 files**" in the "Family, weight and transform per row, as actually shipped" table, presented as "Measured by parsing all 24 component/sec — in *Design system — typography → "Family, we*, superseded by Phase 18 (2026-09-25) itself. 65 is the 
- "The `body` line was added in **Phase 18** as a safety net after measuring 223 elements across thirteen surfaces inheriting Times New Roman (all screen-reader-only, so no — in *Design system — typography → "The floor *, superseded by The pre-integration design review of 202

**Internal contradictions it found (8):**

- "**Measured against the code (grep over the 24 component/section style vs god-squad-theme/assets contains **21** `.css` files in total (`ls asse — The measurement basis is wrong by any reading — 21 files exist, 19 of them component/section. 24 was the whole theme's file count at the end of Phase 
- "The **eleven** display-family rules are the **entire Playfair invento vs The eleven `font-family: var(--font-display)` rules are correct and th — Playfair 900 uppercase is handed to every heading of the `<shopify-account>` sign-in sheet — a whole rendered surface — through a custom-property cont
- "`--measure-body` on `.main-collection__description`, `.main-search__e vs `grep -rn -- "--measure-narrow|--measure-body" assets/*.css` gives nin — The reading-measure inventory omits five real consumers, including the product page's entire description column (`.main-product__description`), and mi
- The "Declarations" column: `--type-display-xl` 2, `--type-display-l` 2 vs Code: `--type-display-xl-*` = 1 rule, 3 declarations, 1 file (`.hero__ — Three faults in one column. (1) "13 across 14 files" is self-impossible — you cannot have 13 declarations spread over 14 files; it is 13 size declarat
- "**Label** (12px / 600 / 0.22em / lh 1.45) — anything the customer *ac vs There are **26** rules consuming `var(--type-label-*)` in assets/*.css — The last omission is the substantive one: merchant rich-text **H5 and H6 render as 12px tracked-uppercase labels** (section-main-page.css), and the se
- "Read against the computed table above, only `--type-display-xl`, `-l` vs The section's own computed table, three paragraphs earlier, gives `--t — The section contradicts its own table. It cannot be a "shipped roles only" filter either, because the list includes `--type-h1`, which the same sectio
- The quoted loading code: "```liquid\nassign body_medium   = settings.t vs layout/theme.liquid:112-125 wraps those two assignments in a `{%- liqu — As transcribed, the two `assign` lines sit outside any Liquid tag and would render as literal text in the document head — the same class of failure as
- "**Eyebrow** (13px / 500 / 0.30em) ... **Five consumers**." and the ro vs Six rules consume `var(--type-eyebrow-*)`: the five listed plus `.hero — Minor but it is the same self-inconsistency as the count column: the prose says five, the exceptions table says there is a sixth, and the "16 across 5

### Critic 5

**Verdict.** Trustworthy on mechanics, unreliable as a rulebook. Almost every value, line reference and computation I checked against disk is exact — the ten spacing tokens at `design-tokens.css:239-248`, the two clamps at `:251-252` and their full computed table, the gutter ladder at `:266-269` switched at `:503-504` and every content-box figure derived from it, `component-container.css` loaded at `layout/theme.liquid:151` after the three files it must beat, all twelve `.container` consumers at the exact section-and-line given, the header overlay block at `sections/header.liquid:52-66`, the drawer gate at `layout/theme.liquid:232-236`, `scrollbar-gutter` at `section-cart-drawer.css:23`, every media-query tier count (11 at 768, 9 at 1024, 1 at 1280, 2 at 1440, three `max-width: 767px` at the named file:line, two height-bounded landscape blocks, zero uses of `--bp-sm`), exactly four `!important` declarations all in `base.css`'s reduced-motion block, the two raw-px spacing exemptions, every unreferenced token, all column ranges and defaults and all three spacing selects in the schemas, `settings.container_width` emitted at `snippets/css-variables.liquid:93`, the `grid-sizes.liquid` constants and the `| plus: 1` truncation fix, and the `--measure-body`/`--measure-narrow` correction of Phase 9's mislabelling. That is an unusually high hit rate and it is the section's real strength. But the rules are in worse shape than the numbers. Five of the six grid rules and two of the seven spacing application rules Phase 2 wrote are simply gone — including the two that govern gaps, which is conspicuous because the shipped theme has diverged from them almost completely (57 of 64 gap declarations read `--space-*` rather than a grid-gap token) and the section, which opens by promising to name every divergence, names none of it. Four of its own statements are disproven by the code it cites (`#MainContent` vs `main` on the clearance selectors, the `overflow: hidden` inventory, \"nothing is hidden on mobile\" against `.our-story__caption { display: none }`, and \"no explicit grid placement\" against `.our-story--image-left`), it contradicts itself on whether 320px renders one column or two — the justification for `--product-track-floor` — and it carries Phase 2's \"the phone composition was formalised rather than changed\" into a document whose own table proves Phase 9 changed it. Use it as the authority for what the values are and where they live; do not use it alone to decide whether a new rule is permitted, and re-derive the 320px, 834px and margin-direction claims before acting on them.

**Governing rules it could not find in this manual (14):**

| Rule | From | Belongs in |
|---|---|---|
| "Gaps come from tokens only — `--grid-gap`, `--grid-gap-large`, `--product-grid-gap`. A section may not invent a gap, which is how the prototype ended up with 20, 32, 36 and 40px gaps in fou | Phase 2 §9.6 (grid rules | This section (Design system — spacing, c |
| "`gap` over margins. Anything inside a flex or grid container is spaced with `gap`, from the scale." Restated in §9.6 as "`gap`, never margins between grid children." | Phase 2 §7.5 and §9.6 | This section. Its entire margin discussi |
| "Two-track splits come from `--split-30-70` (line 98), `--split-40-60` (line 125), `--split-50-50` and `--split-60-40`. A band that needs a ratio outside this set needs a reason recorded in  | Phase 2 §26.3 rule 4 | This section, in "Editorial splits". Wit |
| "The value tile is a tile, not a section. Its 44px block / 24px inline padding (line 144) normalises to `--space-8` / `--space-5` and does not take `--section-pad-block`; the strip as a whol | Phase 2 §7.5 (last appli | This section. The spacing table's `--spa |
| "`--section-pad-block-tight` `clamp(32px, 4vw, 48px)` **where a band abuts another of the same surface**." | Phase 2 §26.2 | This section. The `-tight` row's "For" c |
| "The margin belongs here and not on `.facets`. Below `--bp-md` that element becomes `.facets--drawer`, which is `position: fixed` with `inset-block: 0` and only zeroes `margin-block-end` — a | Phase 18 (decision recor | This section. It cites the same rule's l |
| The scroll-lock composition rule: "The lock is a class on `<html>`, matching the header's menu panel and NOT `assets/cart.js`'s inline fixed-position lock. Two class-based owners compose: ea | Phase 13 §6.1 (shipped a | This section, beside the "No page-level  |
| "A grid sharing its row with a copy column **drops one column** against the standalone ladder, floored at 1." | Phase 2 §25.3 ("Governin | This section. It reports "`columns_deskt |
| "No column count may render a tile wider than its source; today's 235px crops make that an asset requirement for the phase that supplies photography (**BUSINESS INFORMATION REQUIRED**), not  | Phase 2 §25.3, reinforce | This section. It publishes measured card |
| "Splits collapse to one track below `--bp-md` 768px, in DOM order: copy first, media second. **Sections may collapse later than that but never earlier.**" | Phase 2 §9.4 | This section. It reduces the rule to "Sp |
| "Full-width is the fourth editorial layout spec §12 names, **not the absence of one**. A hero image that bleeds to both viewport edges is a deliberate layout choice with its own rules — it t | Phase 2 §9.4 (the fifth  | This section's "Editorial splits" table, |
| "Whitespace is the second most expensive material on the page after photography. A band that fills its column is wrong even when every token in it is correct." | Phase 2 §26.2 | This section. It is the only stated prin |
| "Every interactive element has a hit area of at least `--target-min` 44 × 44, regardless of how small its visible mark is, **adjacent targets separated by ≥8px**." | Phase 2 §24 (touch targe | This section (or Accessibility posture,  |
| "Every later phase verifies … additionally at **1440 × 160% zoom** (= 900 CSS px) and **1440 × 200% zoom** (= 720 CSS px), the two zoom levels that expose the RESP-12 navigation cliff." | Phase 2 §25.7 | This section's "Test widths". It demotes |

**Stale rules it found repeated (4):**

- "327, 342 and 382 are the product tile widths Phase 1 measured on the prototype at those widths, so the phone composition was formalised rather than changed." — in *The gutter ladder — the sentence under t*, superseded by Phase 9 §5. The sentence is Phase 2 §8.3
- "Phone floor | `--product-track-floor: 8rem` = 128px | Measured, not chosen. **Two columns need 2F + 32px**; 8rem is what lets a merchant who asks for two columns get two — in *The product grid — "Constants and where *, superseded by Phase 9 §5 (the gap fix). The 32px const
- "`--space-9` | `4rem` | 64 | Separation between stacked blocks inside one section" — in *The spacing scale — table row for `--spa*, superseded by Phases 5 and 7. The row is Phase 2 §7.1'
- "`--space-3` | `0.75rem` | 12 | Button block padding; **announcement bar block padding**" — in *The spacing scale — table row for `--spa*, superseded by Phase 11 (`header.css:117-124`). `.annou

**Internal contradictions it found (12):**

- "Four sections carry the same `#MainContent > .shopify-section:first-c vs `section-hero.css:31` — `#MainContent > .shopify-section:first-child . — The code disproves both halves. Only three stylesheets carry a clearance selector, not four (404/collection/search carry prose comments and no rule — 
- "**No page-level `overflow: hidden`.** … Every `overflow: hidden` in t vs `header.css:574` — `.menu-open body { overflow: hidden }`; `component- — Three of the seven `overflow: hidden` declarations in the theme are none of the three permitted categories, and two of them are literally page-level —
- "Phone floor | `--product-track-floor: 8rem` = 128px | … **320px still vs The section's own measured geometry table, ten lines later: "| Viewpor — The section states in one paragraph that 320px renders one column and in the next that it renders two 128px columns with a 16px gap. The table is righ
- Responsive rule 8: "DOM order equals visual order at every breakpoint. vs `section-our-story.css:236-237` — `.our-story__caption { display: none — The approved caption copy ("Faith / Lives / Different / Here.") is hidden below 1024px and deliberately removed from the accessibility tree. Phase 7 §
- Responsive rule 8: "No section uses `order`, `row-reverse` or **explic vs `section-our-story.css:429-430` — `.our-story--image-left .our-story__ — With the merchant setting `image_side: left` (a real schema option at `our-story.liquid:363`; the default is `right`), explicit grid placement puts th
- "Five places consume it outside `.container`, and each is a full-bleed vs `section-our-story.css:314` is `padding: var(--space-5) var(--gutter)` — The list cites the same line number for two different selectors, and one of the two is wrong. There are four gutter-bound bands outside `.container`, 
- "28 `(hover: hover) and (pointer: fine)` blocks and 10 `prefers-reduce vs `grep -c '@media (hover: hover) and (pointer: fine) {'` across `assets — The block count is a grep total that includes a comment line — the exact methodological error Phase 13's appendix and Phase 18 §22 both warn about ("a
- "The shipped CSS carries **51 leading-margin declarations and 20 non-z vs Counted on disk: 45 `margin-block-start` + 6 `margin-top` = 51 — but 1 — The two numbers in one sentence are counted by different rules — 51 includes zero-valued resets, 20 excludes them — and neither counts the `margin: 0 
- "**No fixed section heights.** … Where a minimum is genuinely wanted i vs Responsive rule 5 in the same section: "`100dvh` for the gallery cap a — The container/rhythm bullet states "never `vh`" and "clamped" absolutely; the section's own responsive rules record a deliberate `100vh` fallback line
- "**Test widths.** The current responsive suite is the nine widths Phas vs The section's own measured product-grid table reports columns, card wi — Two problems. The stated suite excludes 320 and 834, yet the section's authoritative geometry table depends on both — so either the suite list is inco
- "`--section-pad-block-tight` | `clamp(var(--space-6), 4vw, var(--space vs Every consumer on disk: `section-featured-collection.css:32,35`, `sect — The "For" column describes a class of bands that does not exist in the shipped theme: `-tight` is reachable only when a merchant picks "Tight" in one 
- "Phase 18 put `margin-block-end: var(--space-7)` on `.main-collection_ vs `section-main-collection.css:70-76`: "The margin belongs here and not  — Cause and effect are inverted. The code (and Phase 18's own decision list) gives the fixed-drawer hazard as the reason the margin is trailing on the h

### Critic 6

**Verdict.** Partly — it is the best-sourced section I could have hoped for on structure and the worst on enumeration, and the difference matters because almost everything it says is phrased as an exhaustive list. What it gets right it gets right to the line number: the four real `!important` declarations, the four `outline: none` sites, 29 hover rules all gated, the three chevron consumers at `component-facets.css:107` / `component-cart-line.css:411` / `section-main-product.css:503`, `QUANTITY_DEBOUNCE_MS = 250` at `cart.js:53`, the nine icon snippets and their construction contract, the twelve `.container` consumers across eleven stylesheets and the three deliberate exclusions, the `:not(.product-card__image--secondary)` cascade trap, the grid's `max(floor, ideal)` expression with its 17rem/8rem floors and the 16px column-only gap, the product card's three consumers and zero page-scoped overrides, `grid-sizes.liquid` shared by two sections with `featured-collection` deliberately outside it, and eight separate zero-consumer tokens flagged by name. A reader can trust its architecture and its prohibitions-with-reasons; the "why" behind the surface-class mechanism, the `:active` specificity fix, the chevron rotation and the 250ms literal is intact and better explained than in the sources. But every list that claims completeness is short, and three of the shortfalls are live defects the section's own rules would have caught: the collection sort select ships at 14px inside a blanket "every field carries 16px"; the active-filter chip's control boundary is the 1.32:1 decorative token inside an "absolute" 3:1 rule; and the header search panel and desktop facet dropdown both carry `--shadow-elevated` over a `--color-bg-primary` ground with `z-index: 1`, violating both the z-index precondition and the ink-on-ink prohibition the section states two paragraphs apart. Add a motion census that claims to be the whole surface and misses `header.css:407`, a `--border-width-strong` list said to be "exactly the places the code uses it" that misses two, `--shadow-current` and `--ease-out` presented as live when nothing reads them, `.button--full` said to have one exception when it has six, and error lines mis-sized against both the spec and five of six consumers. On the dropped side the omissions are systematic rather than random: Phase 2's fifth contract rule, the whole of form validation and the textarea, the hover-scale prohibition list, the "every product must have a second photograph" precondition, the focus-ring clipping rule, the #82672B warning/accent collision, and the paginator — a layout-loaded shared component the section names three times and never specifies. Usable as the working reference for how the component layer is built; not yet usable as the reference a new component is reviewed against, and not safe as a conformance checklist until the enumerations are re-derived from disk rather than from the phase documents.

**Governing rules it could not find in this manual (30):**

| Rule | From | Belongs in |
|---|---|---|
| "**R5 — Gaps are raised, not filled.** Where a value is needed and no token exists, §30 records it as a token request under the versioning rules below. Inventing a token name or value locall | Phase 2 — Design System  | This section — "The component contract", |
| On dark, gold may fill "at most one button per page" and mark "one selected state per navigation bar" — the accent budget that sits beside "One primary per band, at most". | Phase 2 — Design System  | This section — Buttons. It carries "One  |
| "No gradients" on a button. | Phase 2 — Design System  | This section — Buttons, "Rules a new but |
| The governing model behind the state matrix: "**hover lifts one step, active drops the lift, focus adds a ring without changing the fill.**" | Phase 2 — Design System  | This section — Buttons. The section repr |
| The product card's quick action is "a single `<button>` in the **Secondary** variant (§10.1), full card width, below the price at `--space-4`, **never overlaying the media**, never hover-onl | Phase 2 — Design System  | This section — Buttons and Product cards |
| "A product with more than one variant routes to the product page rather than silently adding a default" — quick add "refuses to guess": >1 variant renders a Choose options link, one availabl | Phase 2 §13.7, re-decide | This section — Product cards. The sectio |
| "A badge states a stock or catalogue fact the customer can verify — sold out, for example — never a marketing adjective and never a scarcity phrase (§13.5 bans low-stock urgency, and **a bad | Phase 2 — Design System  | This section — Product cards, Badge. The |
| The hover image scale is "Prohibited on the hero image, the story image, the logo, the value glyphs and any full-bleed editorial band. Those are compositions, not controls" — and `--hover-im | Phase 2 — Design System  | This section — Images (or Product cards, |
| "A second 'back' photograph revealed on hover is permitted **only if every product has one** — a partial set makes the grid look broken." | Phase 2 — Design System  | This section — Product cards, Secondary  |
| "`object-fit: cover` is the default; `contain` only where a product must not be cropped." | Phase 2 — Design System  | This section — Images. The section says  |
| "The outline is never clipped: any ancestor with `overflow: hidden` around a focusable element must leave room for `--focus-width` + `--focus-offset`." | Phase 2 — Design System  | This section — Hover and focus states, F |
| What counts as an acceptable substitute for a removed ring: "a `box-shadow` ring of at least `--focus-width` meeting 3:1 against **both** the control and its ground, or a background inversio | Phase 2 — Design System  | This section — Hover and focus states. T |
| "`--color-warning` and `--color-accent-strong` are the same hex, #82672B. On cream, an accent-bordered control and a warning-bordered control would be identical. **Warning is therefore carri | Phase 2 — Design System  | This section — Forms (or Borders). Verif |
| Textarea: "Minimum five lines — `min-height: calc(5 * var(--type-body-size) * var(--type-body-lh))` ≈ 132px, plus the field's own padding. **No spacing token lands on this value; do not subs | Phase 2 — Design System  | This section — Forms. The section lists  |
| "Validation timing: on blur for the first pass, then on input once a field has errored. Never on every keystroke of a first attempt. Multi-field forms carry an error summary at the top of th | Phase 2 — Design System  | This section — Forms, "Rules for any new |
| Error and success announcement: `aria-invalid="true"` on the field plus a message "referenced by `aria-describedby`"; success "applies only after a field has passed validation following an e | Phase 2 — Design System  | This section — Forms. The section gives  |
| Text fields: "`autocomplete` always set (`name`, `given-name`, `address-line1`)". Email: "`type=\"email\"`, `inputmode=\"email\"`, `autocomplete=\"email\"`". | Phase 2 — Design System  | This section — Forms, "Rules for any new |
| "Only `--icon-xl` 44px is redrawn, because 1.5 scaled to 44px reads heavy beside the same glyph at 24px." | Phase 2 — Design System  | This section — Icons. The section states |
| Icon colour, muted / secondary: "`--color-text-muted` on dark only; on light, `--color-text-inverse-muted` — never `--gs-stone`, which is 1.76:1 on cream." | Phase 2 — Design System  | This section — Icons, "State". The state |
| "**No composed artefacts.** A glyph contains the glyph and nothing else. The cart count is a separate element positioned against the cart icon, never part of the drawing." | Phase 2 — Design System  | This section — Icons, "The construction  |
| Do-not-animate list entry: "The logo, the announcement bar, the gold hairlines \| fixed elements of the identity". | Phase 2 — Design System  | This section — Motion, "Never animate".  |
| Motion assignment: "Swatch ring \| `box-shadow` \| `--duration-fast`", with the resting ring at `var(--border-width)` and selection drawn as `box-shadow: 0 0 0 var(--border-width-strong) var(- | Phase 2 — Design System  | This section — Motion, "Assignment". The |
| "Budget: at most one horizontal rule per band, **and no band carries both a top and a bottom rule unless it is bracketed by same-colour bands**, which is case 1." | Phase 2 — Design System  | This section — Borders. The section carr |
| "Links inside a run of text take SC 2.5.8's inline exception, **but the run stays at `--type-body-lh` 1.65 so adjacent lines do not collide.**" | Phase 2 — Design System  | This section — Links. The table's Target |
| "Every link state change transitions on `--transition-fast` … and only `color`, `text-decoration-color`, `border-color` and `opacity` transition — never `text-decoration-thickness` or `paddi | Phase 2 — Design System  | This section — Links. The section states |
| "Do not add a second `--link-underline-offset-caps` token — nothing in the shipped theme needs it and PHASE-2's only 0.25em case (section 20.6) already renders at the token." | Phase 18 — Visual Audit  | This section — Links, beside `--link-und |
| "Do not lift a shared `.field` rule yet — PHASE-2 §12.2's anatomy has three consumers but two sit inside grid parents with different column behaviour, so the promotion is larger than a polis | Phase 18 — Visual Audit  | This section — Forms. The section presen |
| "If a shared `.editor-notice` component is built later, `component-facets.css:472-479` must be folded in too, or the theme keeps two notice languages." | Phase 18 — Visual Audit  | This section — Forms or Borders. The sec |
| "The pagination gap's `aria-hidden` belongs on the `<li>`, not on the span inside it." | Phase 18 — Final Polish  | This section — components. `component-pa |
| "A cosmetic setting must never remove required form data" — when the quantity input is hidden, "the hidden branch now submits `qty_min`, and carries `data-quantity-input` so `product.js`'s ` | Phase 11 — Theme Editor  | This section — Forms, Quantity selector. |

**Stale rules it found repeated (3):**

- Links table: "Footer / policy / social | `section-footer.css` | `color: inherit`, `--type-body-sm-size`, no underline | … | Target: `--target-min-aa` 24px" — the social r — in *Design system — components → Links (row *, superseded by Phase 10 — Theme Architecture, §9: "unde
- Borders table: "`--border-width-strong` | 2px | — | **reserved**; see below". — in *Design system — components → Borders*, superseded by Phases 8, 12, 14 and 18 gave the token s
- Radius: "`--radius-sm` is the only radius exposed to the merchant, **under \"Button/input style\"**". — in *Design system — components → Radius*, superseded by The shipped setting label is "Corner rad

**Internal contradictions it found (20):**

- Forms, field-anatomy table: "`font-size` | `--type-body-size` 16px | a vs `assets/section-main-collection.css:176-186` — `.main-collection__sort — CODE DISPROVES. The collection sort select — a control the section itself lists among "the controls that exist" — renders at `--type-body-sm-size` 0.8
- Shadow table: "`--shadow-current` | resolves to `--shadow-on-dark` / ` vs `grep -rn "var(--shadow-current)" god-squad-theme/` returns nothing. A — CODE DISPROVES. `--shadow-current` is defined twice (design-tokens.css:478, 490) and read zero times. The section flags every other zero-consumer toke
- Shadow: "**An element may carry a shadow only if it also carries a z-i vs `header.css:591-597` — `.header__search { z-index: var(--z-raised); …  — CODE DISPROVES. `--z-raised` is 1, two orders of magnitude below `--z-sticky` 100. Both `--shadow-elevated` consumers the section names fail the preco
- Shadow: "`--shadow-elevated` … header search panel, facets drawer (lig vs Same section, four paragraphs later: "Prohibited: … any shadow on an e — SELF-CONTRADICTION, CONFIRMED BY CODE. The section sanctions as consumers the exact two elements its own prohibition forbids. `--shadow-elevated` is i
- Shadow table: "`--shadow-elevated` … facets drawer (light)" and "`--sh vs `component-facets.css:424` `@media (min-width: 768px)` → `:437 .facets — CODE DISPROVES. `--shadow-elevated` is not on the facets drawer at any surface; it is on the **desktop filter dropdown**, above 768px, on both surface
- Borders: "`--border-width-strong` 2px is permitted in exactly the plac vs `section-main-product.css:102` — `.product-gallery__thumb { border: va — CODE DISPROVES an explicitly exhaustive list ("exactly the places the code uses it"). There are six consumer sites, not four. The table-head rule is t
- Borders, "The governing split": "Anything that is the visual boundary  vs `component-facets.css:288-292` — `.facets-active__chip { … border: var — CODE DISPROVES the split. The active-filter chip is a real interactive control — an anchor that removes a filter on click — whose entire visible bound
- Radius: "`--radius-none` | `0` | **the default for everything** — sect vs `component-facets.css:82` and `:501` — two count badges (`min-width: 1 — CODE DISPROVES. Four `--radius-sm` consumers are absent from the "Permitted on" column, and two of them are badges, which the table assigns to `--radi
- Buttons: "`.button--full` is mobile-only, except the product card's qu vs `component-button.css:188-190` — `.button--full { width: 100% }` with  — CODE DISPROVES a stated single exception. Five further consumers apply `button--full` unconditionally at every viewport, and two of them (the drawer's
- Buttons: "the prohibition is enforced twice. There is no `.surface-lig vs `sections/main-404.liquid:73` — `<a class="button button--accent main- — CODE DISPROVES "every consumer". Three of five accent consumers hardcode the class and rely on a hardcoded `surface-dark`, which is a different and un
- Motion: "**Every `transition` declaration in the theme, measured acros vs `grep -h "transition:" god-squad-theme/assets/*.css | wc -l` = **31**. — CODE DISPROVES a census that claims to be exhaustive. The table is one declaration short: `header.css:407` (`.header__nav-link`, `color` + `border-col
- Motion, Reduced motion: "Components that transition also ship an expli vs Eleven stylesheets declare transitions; only seven declare `transition — CODE DISPROVES. Four of eleven transitioning stylesheets do not follow the stated practice, and one of them states in a comment that it deliberately d
- Forms: "**Error and success lines are left-ruled, not boxed**: `border vs `section-main-product.css:426` and `:456`, `component-cart-line.css:12 — CODE DISPROVES, and the section also contradicts the specification it cites. Five of the six left-ruled error/success/notice lines render at 14px; the
- The component contract, R4: "No colour pairing ships without a measure vs The same section's "Variants and their measured states" table gives `b — SELF-CONTRADICTION. The section states R4 as the gate on shipping any pairing and then ships a variant table with a hole in exactly the place R4 says 
- Motion: "Three durations, two easings, three shorthands. **No other du vs `grep -rn "var(--ease-out)" god-squad-theme/` returns nothing. `--tran — CODE DISPROVES the implied status. `--ease-out` has zero consumers and is structurally unreachable, because the only three shorthands a component may 

### Critic 7

**Verdict.** Mostly trustworthy on mechanism, unreliable on counts and attribution — usable as the working reference for these six surfaces only with the eight corrections above applied. The engineering substance holds up under verification better than I expected: I checked roughly sixty concrete claims against disk and the great majority are exact. Every setting inventory is right id-by-id (header 8, hero 14, Our Story 14, footer 6, collection row 19, with every range bound, default, option order and preset matching the schemas); every token figure resolves (scrim gradient and 4rem overhang byte-for-byte, 88/122px, 40/64px, 24/32/48px gutters, 17rem floor, 520px band, 34/38/42rem hero column, 26rem/9rem/11rem rail tracks); the hero type table's arithmetic is internally consistent with `--type-display-xl-*` at 375/768/1440 to two decimals; the six-clause `sizes` derivation, the `threshold_d` 1024 floor, the `1000/727` scaling and the non-consolidation note are all where it says; the three first-child clearance selectors, the `[hidden]` specificity argument, the 250ms/400ms split, the `.menu-open body` lock on `<html>`, the binding registry, the idempotency guard and the `scrollY > 8` threshold are all verbatim correct; and the image masters check out on disk at 1672×941, 535×348 and 500×500. It also does the hard thing well in three places — overruling Phase 5 on `--header-overlay-offset`, overruling the announcement bar's own file comment on `--bp-sm`, and marking Phase 4's twelve header settings as superseded. What fails is bookkeeping and provenance, and it fails in the direction a reader cannot detect: three enumerations are miscounted (eight schema groups called six, eight colour-scheme sections called seven, three list items called two), one dimension is wrong twice over (the hero hairline is `--space-7` 40px, not 32px), one rule is stated as implemented when the code does the opposite (focus return prefers `lastFocused` over the trigger), one is stated as implemented when two other scripts load on the same page (cart.js at 39,750 B), one exclusion reason is wrong about the header's own element (`.header__search-form` uses the standard container, not a narrow measure), and a whole Phase 18 paragraph credits this surface with a paginator, an empty state and a description rule that live in section 8's files. Against that, fifteen governing rules that belong here are simply gone — the entire announcement-bar prohibition set, Phase 2's surface-boundary and scrim-anchoring rules, the sticky-header hairline (which the code already violates), the mobile panel's utility-repeat requirement, the hero's own-your-top-spacing handoff, the hero master's composition band, the header's landscape exemption, and a predictive-search contract the manual discharges by pointing at Phase 13 §2 — a document this manual is supposed to retire. A reference that delegates a contract to a file being decommissioned is not yet a replacement for it.

**Governing rules it could not find in this manual (15):**

| Rule | From | Belongs in |
|---|---|---|
| Announcement bar, prohibited content: "Prohibited outright: discount codes, countdowns, urgency language, rotating or carousel messages, marquee scrolling, and any claim that is not verifiab | Phase 2 — Design System  | Surfaces — the Announcement bar subsecti |
| Announcement bar §20.8 Prohibitions: "No animation of any kind, including fade-in on load. No icons other than `globe` at `--icon-sm`. No second accent colour. No border other than the botto | Phase 2 — Design System  | Surfaces — Announcement bar. This is the |
| Announcement bar link ceiling: "At most **one** of the two messages may be a link" — and "'Worldwide Shipping' may not link until a shipping policy page exists (BUSINESS INFORMATION REQUIRED | Phase 2 — Design System  | Surfaces — Announcement bar. The manual  |
| Announcement bar permitted copy: "Permitted content is limited to the pair in the source — `Good People. Higher Purpose.` and `Worldwide Shipping` — plus … `The Faithful Collection`. Nothing | Phase 2 — Design System  | Surfaces — Announcement bar. The manual  |
| Surface-boundary rule (operating rule 4): "the colour change is the transition, and no gradient, hairline or shadow is added across a surface boundary. A hairline at `--color-border-current` | Phase 2 — Design System  | Surfaces — "Rules that bind every surfac |
| Sticky-header treatment: "A sticky header on scroll becomes opaque `--color-bg-primary` with a `--color-border-subtle` bottom hairline at `--z-header` 200. `--shadow-elevated` is permitted o | Phase 2 — Design System  | Surfaces — Header, "Overlay, sticky and  |
| Scrim anchoring prohibition: "The scrim is never anchored to the hero section. Anchoring an overlay to a parent the header shares is the exact mechanism behind the hero fade defect … and it  | Phase 2 — Design System  | Surfaces — the "Rules that bind every su |
| Mobile panel requirement: "Utilities \| repeated at the foot of the panel at `--target-min`, with visible text labels." | Phase 2 — Design System  | Surfaces — Header, "Mobile panel". The s |
| Header logo: "The logo is height-constrained and `width: auto` at every tier; it is never rotated, never animated and never given a hover state." | Phase 2 — Design System  | Surfaces — Header, "Navigation" / logo l |
| "The section below the hero must own its own top spacing. The hero ends at its own bottom padding (`--space-8` below 1024, `--space-9` above). It does not reserve space for whatever follows. | Phase 5 — Hero (§16, han | Surfaces — the "Rules that bind every su |
| Hero master composition standard: "Any future hero master must place its subject inside that band or the scrim will bury it" — the photograph is readable only between roughly 48% and 68% of  | Phase 3 — Asset System ( | Surfaces — "Open on these surfaces", bes |
| Predictive-search contract: it must use "Shopify's section-rendering endpoint (`routes.predictive_search_url` with `section_id`), never the JSON endpoint and never a hardcoded `/search/sugge | Phase 13 — Search, Filte | Surfaces — Header, the Search bullet. Th |
| "The header is never reduced in landscape: it keeps its full 88px height and every control" — "nothing in the header is hidden, shrunk or collapsed at any viewport." | Phase 9 — Mobile UX + Re | Surfaces — Header. The manual's landscap |
| "The skip link is 44px tall — `display: inline-flex; align-items: center; min-height: var(--target-min)`" (raised from a measured 38px). | Phase 9 — Mobile UX + Re | Surfaces — the wiring paragraph, which a |
| Header search placeholder: "Search placeholder is 'Search the store…', agreeing with its own accessible label and the results page, because the form posts to `routes.search_url` which search | Phase 18 — Visual Audit  | Surfaces — Header, the Search bullet. Th |

**Stale rules it found repeated (2):**

- "**Editor notices, never a different layout.** Four sections carry a `request.design_mode` branch (`featured-collection`, `our-story`, `main-page`, `footer`); each is a c — in *Surfaces — "Rules that bind every surfac*, superseded by Phase 13 added a fifth. `grep -rn design
- "The merchant control is a `select` labelled **Colour scheme** with options *Ink* / *Cream* in all seven sections that expose it." — in *Surfaces — "Rules that bind every surfac*, superseded by The code has eight. `grep -rl '"label": 

**Internal contradictions it found (8):**

- Hero, DOM: "`p.hero__description` (::before draws the 32px gold hairli vs `assets/section-hero.css:323-329` — `.hero__description::before { … wi — The hairline is 40px, not 32px, and the figure is stated twice. 32px is `--space-6`; the rule uses `--space-7`. No media query changes the width (the 
- Hero, Typography/Layout: "#### Settings (19, six groups)" for the coll vs The same subsection's own table lists eight distinct groups — Collecti — Self-contradictory and code-disproved in one line. The 19-setting count is correct (verified id-by-id, with every range bound and default matching); t
- "**Zero JavaScript except the header.** … `assets/header.js` (13,963 B vs `layout/theme.liquid:183-191` loads, unconditionally on every page: an — The first half of the rule is true and verified — hero, featured-collection, our-story, footer and announcement-bar contain no `<script>`, no inline h
- Header, `assets/header.js` contract: "**all three** close paths (Escap vs `assets/header.js:107-122` — `var target = toggle; if (lastFocused &&  — The shipped code does the opposite of the stated contract: `lastFocused` (the element focused when the panel opened) wins whenever it is still valid, 
- "One container utility … `.header__search-form`, `.main-page__column`  vs `assets/header.css:600-608` — `.header__search-form { width: 100%; max — `.header__search-form` uses the *standard* 1440px container, not a narrow measure — it is three of `.container`'s four declarations with the gutter le
- Our Story: "Measured: 3 blocks span the full width at every tier" — im vs `assets/section-our-story.css:273-274` — `grid-template-columns: repea — Two mutually exclusive statements about the same row, one sentence apart. `auto-fit` collapses only tracks that are empty; it cannot manufacture a thi
- Collection rows: "Phase 18 landed on this surface: the shared `.contai vs `snippets/pagination.liquid` is rendered only from `sections/main-coll — Three of the four items did not land on this surface at all — they belong to the collection and search *pages*, which the manual itself assigns to sec
- Announcement bar: "Two things to know before you touch this:" vs Three numbered items follow (1 the raster `icon`, 2 the "Worldwide Shi — Trivial on its own, but it is the third counting error in this section (alongside "six groups" for eight and "seven sections" for eight), and all thre

### Critic 8

**Verdict.** On mechanism this section is unusually good, and I tried hard to break it: cart.js at 39,750 B raw / 12,008 B gz, product.js 18,096/5,608, facets.js 10,937/3,848 and header.js 13,963/4,329 all match the disk exactly; so do the nine-key variant table, the `low_stock` guard line verbatim, the 1106px threshold and `media_cap = (container - 128) * 0.64 + 1`, grid-sizes' gap/col_min/chrome constants with threshold_d floored at 1024 and capped_track rounding up, the seven delegated document listeners in init(), `--drawer-width: min(90vw, 420px)`, the `@media (max-height: 540px) and (max-width: 1023px)` gate, `scrollbar-gutter: stable` on `html`, `.quantity__button { display: none }` unlocked only by `.cart-js`, `CART_ERROR_BOXES`, the `!result.response.ok || typeof data.description === 'string'` failure test, the cart page's `minmax(0, 1fr) 24rem` sticky summary, the ten product settings in four groups, the `<shopify-account>` block character for character, `shop.customer_accounts_enabled` appearing exactly once, `grep -rn quick_add sections/` returning nothing, and exactly seven sections carrying `section.shopify_attributes`. It is not yet safe as the working reference, for three reasons. It repeats a limitation Phase 16 explicitly retired — "Theme Check has never been run" — while citing that same run's residual errors in the next clause, and understates them from five to two. It flattens measured facts into claims its own tables disprove: cart.js is not "alone" over the AssetSizeJavaScript threshold (three other scripts are, and Phase 16 counted three errors), "eager images exactly 1" is broken by the gallery's own if/elsif whenever the active medium is not the first, and "no shipping claim anywhere in the theme" is contradicted by the very sentence the totals note prints. And it mis-describes two pieces of live markup — `.rte` on the page surface (which uses `.main-page__content`, and `.rte` has no CSS at all) and script-only `aria-expanded` on the filter toggle (Liquid prints it) — while asserting that the two search forms agree today when Phase 18 recorded that they already post different queries because the header panel omits `options[prefix]=last`. Beneath that sits a layer of rules cheap to lose and expensive to rediscover: the card's two-line clamp and no-chrome contract, the native-`<details>`-no-ARIA rule shared by the three disclosures this section itself describes, the server-hidden Filter trigger, the fact that filter and sort controls vanish entirely on a zero-result collection, the unit price that never updates on a variant change, and the deliberate "Add to bag" naming. Fix the Theme Check paragraph, the three overstated absolutes, the `.rte` and `aria-expanded` descriptions, and fold back the seventeen dropped rules, and this becomes a genuine replacement for the eight phase documents it consolidates; until then it should be read alongside Phases 12, 13, 16 and 18.

**Governing rules it could not find in this manual (17):**

| Rule | From | Belongs in |
|---|---|---|
| The product card title is clamped to exactly two lines, with the box always reserving both so prices align across a row; clamping is visual only — the complete title stays in the DOM and in  | Phase 6 §6 ("Two lines m | This section — "The product card, badges |
| Native <details>/<summary> are the whole disclosure: no aria-expanded, no aria-controls, no role="button", no script. This is the shared reasoning for all three disclosures in this section's | Phase 13 §10 ("Filter gr | This section. It describes all three as  |
| A filter group is server-rendered open when it holds an applied value, so an applied filter is never hidden behind a control the customer has to find. | Phase 13 §10 ("a group i | This section — "snippets/facets.liquid — |
| Facet checkboxes use the theme's shared .visually-hidden utility rather than re-declaring the hiding rules, so they stay focusable with the ring drawn on the label. | Phase 13 §10 | This section. It states exactly this rul |
| The Filter trigger is server-rendered with the `hidden` attribute and is unhidden only by assets/facets.js — never keyed off the layout's `js` class, because that class is set in <head> befo | Phase 13 §6 / §4 (drawer | This section — "assets/facets.js — the d |
| The filter controls, the sort control and the product count are not rendered at all on a zero-result collection — they all sit inside {% if paginate.items > 0 %} — so Clear all is the custom | Phase 16 §14 (the fixed  | This section — "Two empty states that sa |
| The search results page must echo the customer's term back exactly as typed and never uppercased. | Phase 10 §9 ("Search mus | This section — "The results page". It re |
| The results page carries a visible <label> and no placeholder at all (placeholder-only labels are forbidden, and a placeholder repeating the label is noise); the header panel's placeholder i | Phase 2 §12.6 as applied | This section — Search. It describes "a l |
| The unit price is rendered from the variant the page opened on and is not updated on a variant change; it carries no data hook and no field in the embedded variant table. | Phase 12 §5 ("The unit p | This section — "What a variant change up |
| sticky_info is desktop-only: the sticky positioning, the max-height, the column's own scroll and its scroll-padding all live inside @media (min-width: 1024px), and sticky info can never cove | Phase 12 §4 ("sticky inf | This section — the product page. Its set |
| og:image:width is the literal 1200 with the height derived for that rendering (reading image.width would publish the source asset's dimensions beside a 1200px URL); no og:price is emitted, b | Phase 16 §10 | This section — "Conversion, analytics an |
| "Add to bag" is a decided brand term, not drift, and must not be silently harmonised with the fourteen "cart" strings: the action is "add to bag" and the container is the "cart" by choice. | Phase 18 Visual Audit (f | This section — Add to cart / the button  |
| The header's show_cart setting can leave the header with no cart control at all, so a customer who has added something can only reach the cart by typing the address; the cost is written into | Phase 11 §2.1 and §14 | This section — "Cart count", which docum |
| The empty-cart CTA is the accent (gold) button variant, which has no light-surface rule at all; it is legible only because both cart surfaces hardcode surface-dark. | Phase 2 §10.1 as applied | This section. It states exactly this dep |
| Pagination is one implementation for both surfaces, taking its type and current-page marker from the collection version and its accessibility from the search version; aria-hidden goes on the | Phase 18 §8 and Visual A | This section — it claims pagination in i |
| Card swatches are information, not controls, so SC 2.5.8 does not govern their 16px size; and a swatch row renders only when more than one value in the option carries Shopify swatch data. | Phase 6 §6 ("Information | This section. It records the equivalent- |
| Hover behaviour on the card is gated on @media (hover: hover) and (pointer: fine), never on viewport width, and the card itself takes no background, border, shadow or lift in any state. | Phase 6 §6 | This section. It applies the pointer gat |

**Stale rules it found repeated (2):**

- "Theme Check has never been run (no Shopify CLI in this environment — run `shopify theme check` before going live)", listed under "Never verified against a real store". — in *"Open items and things that were not ver*, superseded by Phase 16 §0, which retires this exact li
- The asset inventory names only the Phase 8 trio as loading from the layout — "layout/theme.liquid loads component-button.css, component-quantity.css and component-cart-li — in *"Surface inventory", the paragraph under*, superseded by Phase 18 §23/§24, which promoted both to

**Internal contradictions it found (9):**

- "There is **no shipping claim, no delivery estimate and no free-shippi vs The same Totals subsection: "The note below them is derived, not asser — The code disproves the absolute claim. snippets/cart-totals.liquid:48-54 prints one of two sentences on every cart render: locales/en.default.json giv
- "Theme Check has never been run (no Shopify CLI in this environment…" vs "…; the two residual Theme Check errors are the missing `theme_support — Self-contradicting in one sentence: a residual-error count can only come from a run. It also understates that run — Phase 16 §19 records 2 ValidJSON e
- "`cart.js` alone exceeds Shopify's `AssetSizeJavaScript` 10,000 B thre vs The byte table printed six lines earlier in the same subsection: produ — The section's own table disproves "alone". The check measures the asset, and every one of the four scripts listed is over 10,000 bytes raw; Phase 16 §
- "`page.title` goes through `| escape`; `page.content` is merchant HTML vs sections/main-page.liquid:116 renders `<div class="main-page__content" — Wrong on both counts, and consequentially so: main-page owns a complete private typographic treatment under `.main-page__content` (section-main-page.c
- "**A live inconsistency worth fixing:** the panel hardcodes `<input ty vs Two paragraphs earlier, in the same Search subsection: "Hidden inputs  — The two surfaces already disagree, today, on every query. `grep -rn "options\[prefix\]"` over the whole theme returns exactly one hit, sections/main-s
- The performance budget: "eager images **exactly 1**, `fetchpriority` ≤ vs The product-page loading discipline: "`fetchpriority: 'high'` follows  — The two cannot both hold. snippets/product-media-gallery.liquid uses a per-iteration `{% if is_active %} … {% elsif forloop.first %} … {% else %}` cha
- "`aria-expanded` and `aria-controls` are set by the script, truthful o vs sections/main-collection.liquid:356 prints `aria-expanded="false"` dir — Half the rule is disproved by the code. In effect the theme is safe — the button also ships `hidden` and is revealed only by facets.js — but the secti
- main-404: "`button_label` carries **no schema default** on purpose — a vs The same section documents both cart surfaces' empty-state button with — The section presents the no-schema-default localisation rule as reasoned and governing for a merchant-editable button label, while the two surfaces it
- Discrepancy 4: "`snippets/cart-empty-state.liquid` and `sections/main- vs sections/main-404.liquid says `routes.all_products_collection_url` "is — The discrepancy list — the part of the section that exists to be the audited truth — was itself not checked against one of the two files it names. mai

### Critic 9

**Verdict.** Trustworthy on its core subject, and unusually so — but not yet trustworthy as the sole reference. Where this section describes the platform contract the theme was actually built against, it is excellent and I could not break it: every one of the ~25 line-number citations I checked is exact, the Section Rendering API rules in §4 are all present in `cart.js` as described (null skipped, `swapInner` taking the wrapper's inside, headings and live regions outside the swapped node, `sections_url = location.pathname`, at most three of five sections), the no-`Content-Type`-on-FormData and `description`-or-not-ok failure test are in the code with the reasoning intact, §7's sidebar-versus-bar arithmetic reconciles against `grid-sizes.liquid`'s real constants (chrome_d 96, col_min 272, pitch 304, and the 112px sidebar figure is correct), the 14-settings/8-group schema matches disk exactly, `shop.customer_accounts_enabled` really does appear exactly once, and cart.js's 39,750 B / 12,073 B gz reproduce byte-for-byte. The failures are of two kinds and both are fixable. First, the section's authority rests on assertions that no longer exist: it cites `phase17/tracking.py` as a *standing* protection and calls fifteen behaviours \"asserted\" when the project contains zero Python files, no harness and no Theme Check install — so a manual that reads as verified is in fact unverifiable, and it should say so as plainly as §19 says everything else. Second, it drops platform facts that belong nowhere else: the stored-XSS rule governing the two cart endpoints §3 documents, Phase 15's eight-item order/fulfillment trap list, metafields and dynamic sources entirely, the SVG-through-`image_url` fact that bites the very logo upload §5 and §18 demand, and three admin steps (pick the collections, create the pages, write the alt text) without which a merchant can complete all 22 checklist rows and still have an empty home page. Add the mistyped `radius_sm` control, the self-contradiction about whether Phase 10 ever ran Theme Check, a CSS budget line silently in breach of its own target, and a field list that includes two `<meta>` names while omitting `updates[]`, and the honest verdict is: keep it as the working reference for the integration contract, repair these fifteen items first, and do not let the word \"asserted\" stand anywhere until the suites are back in the repository.

**Governing rules it could not find in this manual (12):**

| Rule | From | Belongs in |
|---|---|---|
| "Shopify Liquid does not escape output." Cart line item properties and the cart note are untrusted input (settable via /cart/add.js and /cart/update.js) and "Both now carry `\| escape`", veri | Phase 17 — Analytics + T | §3 The Ajax Cart API — it tabulates exac |
| The order/fulfillment trap list, preserved "for one reason: if this store is on legacy accounts and you decide to stay there, somebody will have to build these surfaces, and these are the tr | Phase 15 — Customer Acco | §9 Customer accounts. §9 correctly says  |
| "There are three different order URLs — `customer_url` (token path), `order_status_url` (`/authenticate?key=`), `customer_order_url` (shopify.com host, numeric id + JWT) — and the brief's as | Phase 15 — Customer Acco | §9. This one is worse than a plain omiss |
| "Shopify exposes dynamic sources automatically for compatible setting types, and the theme already uses those types throughout — so metafield binding is available today on every `text`, `tex | Phase 11 — Theme Editor  | §5 Theme settings the merchant must conf |
| "Once the vector master exists, image_url no longer applies: Shopify does not transform SVG through image_url, and a widths: ladder on an SVG does nothing. Upload the vector as the theme log | Phase 3 — Asset Preparat | §5, on the Brand → `logo` row. This is n |
| "The CDN does not output AVIF. Any recommendation, checklist or audit that asks for an AVIF ladder on Shopify is asking for something the platform will not produce. WebP is the delivery form | Phase 3 — Asset Preparat | §11 Product data the store must supply,  |
| "{% form 'product', product %} generates the method, the action, the form_type and utf8 inputs and the product-id input. It does NOT generate the variant input — product-id is not id and add | Phase 8 — Product & Shop | §3, which already documents the no-JS de |
| The merchant must point each `featured-collection` section at a collection and set its View all destination — from Phase 6's seven admin steps: "create collections, add products, configure s | Phase 6 — Collections &  | §18, the consolidated pre-launch Admin c |
| The merchant must create the store's content pages and link them — Phase 11's admin prerequisites include "pages"; Phase 7's four required pre-launch steps are "upload image, set alt, set fo | Phase 11 — Theme Editor  | §18. `templates/page.json` and `sections |
| Alt text is merchant data that the theme never invents — "`alt: img.alt` — alt text comes from the uploaded image and is never invented by the theme", with "set alt" listed as a required pre | Phase 7 — Our Story (§6, | §18 item 12, beside focal points and swa |
| The missing-template list is six, not five: "`article`, `blog`, `list-collections`, `page.contact`, `password`, `gift_card`" — with `password` singled out as mattering "if the store ever goe | Phase 15 — Customer Acco | §16 Templates Shopify can route to that  |
| "No customer data in any client-side store. `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`, `caches.open` and service-worker registration are each asserted absent from ever | Phase 15 — Customer Acco | §10, which reproduces this list but drop |

**Stale rules it found repeated (3):**

- "Result at the correct root — 49 files scanned, 84 checks", presented as the theme's current Theme Check state, and underwriting §18 item 22's "5 known offenses; anything — in *§17 Theme Check and the CLI*, superseded by Phase 18 — Final Polish, §23 Files creat
- "`theme_documentation_url` and `theme_support_url`/`theme_support_email` are absent, not empty." — in *§5 Theme settings the merchant must conf*, superseded by Phase 16 — Performance/SEO, §19, which i
- "Safari. All browser testing was Chromium — Edge 153 and Chrome, both green, 0 console errors across 38 pages." — in *§19 What is unverified, and must be chec*, superseded by Phase 18 — Final Polish (Acceptance crit

**Internal contradictions it found (6):**

- §1: "A standing assertion protects it (`phase17/tracking.py`)." And th vs The project tree. `find . -name "*.py"` returns 0 results across the e — `phase17/tracking.py` does not exist, and neither does any of the ~30 suites, the mini-Liquid harness, or the local `@shopify/theme-check-node` instal
- §5 settings table: "| Layout | `radius_sm` | range 0–8 | `2` | no |" vs `config/settings_schema.json`: `radius_sm` is `"type": "select"` with  — The code disproves the manual on both the type and the range. A `range 0–8` would expose 6px and 8px, which the governing Phase 2 decision exists to f
- §5: "They shipped as empty strings against a `format: uri` schema, whi vs §17: "**The Shopify CLI has never been present in this environment, so — The section contradicts itself about whether Phase 10 ever saw a Theme Check result. §5 credits Phase 10 with observing "the theme's only Theme Check 
- §17 performance budget: "| CSS, worst page | 55.1 KB gz (homepage) | ≤ vs Phase 16 §21 set that target at "≤ 55 KB gz" when the measured current — The manual has substituted Phase 18's later measurement into Phase 16's target and produced a budget line that is already in breach — 55.1 KB against 
- §14: "The theme submits exactly `add`, `checkout`, `description`, `id` vs Every `name="..."` attribute in `sections/` and `snippets/`: `add`, `c — The code disproves the list twice over. `description` and `viewport` are not form fields at all — the list was evidently produced by grepping `name="`
- §18 item 22: "Run Theme Check against `god-squad-theme/` on a developm vs §17's own table: default config = **2** residual offenses (2 × ERROR V — The section contradicts itself on the baseline it tells the reader to check against. §18 item 22 gives an unqualified "5 known offenses" without namin

### Critic 10

**Verdict.** Trustworthy on mechanism and measurement, not yet trustworthy as the complete register of what governs accessibility in this theme. Almost everything I could check against disk checks out exactly: the four real `!important` declarations really are the only four and really are all in base.css:73-76; the global ring really is base.css:58 and the comments really do misattribute it to the token file; `--scrim-header` really holds .93/.86/0 at design-tokens.css:131; the nav-band table, the 40/48/14/55/73 measurement counts, the 8.18:1 and 11.98:1 hero figures, the 1.00:1 no-scrim reading, the 3.02:1/3.13:1 border tokens, the `:has()`-not-`:focus-within` quantity fix, the `contains()`-not-identity inert fix, the two live regions, the `facets.js` `applyWidth` P0 fix and `open()`'s second guard, zero positive `tabindex`, zero `role="button"`/`onclick`, no `orientation` query, no `forced-colors` query, 9/9 icon snippets `aria-hidden`, and the hovergate claim (I counted 29 `:hover` selectors, 0 ungated) are all correct as stated. The failures are of a single kind, and it is the dangerous kind for a replacement reference: the section reports the target-size and heading-order posture as of Phase 9 and Phase 6 respectively and never reconciles it with Phases 10, 13 and 7 — so it asserts a 44px box for 16px swatches that Phase 6 explicitly exempted and the code does not give them, counts two 24px controls where the code has four, repeats a home-page heading tally invalidated the moment Our Story shipped, and invents a gallery `max-height` by double-reading the sticky column's. Alongside that it omits about twenty live rules that belong to no other section — the entire mobile-menu focus contract, the rule that ARIA describing script behaviour is written by the script and not by Liquid, the `overflow-wrap`-on-the-content-root rule that actually delivers its own 320px reflow claim, the reason the 2px focus offset is load-bearing, the paginator's `aria-hidden`-on-the-`<li>` and aria-label-versus-hidden-text rules, and the never-set-`background-color`-directly rule without which its four-mechanism table does not hold. Use it as the authoritative account of contrast, focus mechanics, inert/live regions, scroll lock, reduced motion and the untested gaps; do not use it to audit target sizes, heading counts or component naming until the four stale claims are corrected against the code and the dropped rules are folded in.

**Governing rules it could not find in this manual (20):**

| Rule | From | Belongs in |
|---|---|---|
| "The mobile menu disclosure contract: opening sets aria-expanded="true", reveals panel and overlay, moves focus into the panel and locks body scroll; Tab from the last item wraps to the firs | Phase 4 — Header & Navig | Accessibility posture → Focus management |
| "swatches are 'Information, not controls', so SC 2.5.8 does not govern their 16px size" — Phase 6 explicitly removed product-card swatches from target-size governance. The section not only o | Phase 6 — Collections &  | Accessibility posture → Target sizes (it |
| "`aria-haspopup="dialog"` and `aria-expanded` are set by JavaScript at initialisation, not rendered by Liquid." The same rule is implemented a second time in facets.js:114-117 ("Truthful onl | Phase 13 — Search, Filte | Accessibility posture → Keyboard, semant |
| "undersized controls get the `--target-min` box (24px floor, 44px for the social row per Phase 2 line 2126)" — the standing policy that secondary navigation clears 24px while the social row  | Phase 10 — Theme Archite | Accessibility posture → Target sizes |
| "Prose surfaces carry `overflow-wrap` on the content root" — set on the content root specifically so it inherits to every text-bearing descendant, and deliberately `break-word` not `anywhere | Phase 10 — Theme Archite | Accessibility posture → Reflow, zoom and |
| "The 2px gold focus ring must keep its 2px offset: 'gold on the cream button face is only 1.55:1 — which would fail SC 1.4.11 if the ring touched the button.' The offset puts dark backdrop ( | Phase 5 — Hero §7 | Accessibility posture → Focus management |
| "The pagination gap's `aria-hidden` belongs on the `<li>`, not on the span inside it" — because "hiding only the span leaves a list item with no accessible content, which is announced as a b | Phase 18 — Visual Audit  | Accessibility posture → Keyboard, semant |
| "links are named with `aria-label`, which is safe on an anchor because an anchor has a role that supports naming, while the current page — a bare span — uses hidden text, because `aria-label | Phase 18 — Final Polish  | Accessibility posture → Keyboard, semant |
| "A section declares its surface. Every `<section>` carries `.surface-dark` or `.surface-light` and never sets `background-color` directly" — because "a cream band authored as background-colo | Phase 2 — Design System  | Accessibility posture → "The standard, a |
| "Two lines maximum, with the box always reserving both... Clamping is visual only: the complete title stays in the DOM and in the link's accessible name." The section says the card title is  | Phase 6 — Collections &  | Accessibility posture → Keyboard, semant |
| "Sold out is a Solid ink badge with a cream label... Media dims to 0.6 as the *secondary* cue. The state is in the link's accessible name, reading 'Utility Cap Sold out'." The section's SC 1 | Phase 6 — Collections &  | Accessibility posture → Keyboard, semant |
| The gallery "keeps video controls on with autoplay off" (re-asserted by Phase 16 §7 as "video rendered through Shopify filters with autoplay false"). The section prohibits scroll-triggered r | Phase 8 — Product & Shop | Accessibility posture → Reduced motion ( |
| "Hover never changes layout, and never changes a thickness... Rings that need to read thicker are drawn with `box-shadow: 0 0 0 Npx`." The section carries the two other §22.1 rules (hover is | Phase 2 — Design System  | Accessibility posture → Keyboard, semant |
| "the scrim is `aria-hidden`" (Phase 5 §2) / "the scrim is `aria-hidden="true"`" (Phase 7 §9). The section discusses scrims at length under Contrast and says they are `pointer-events: none` a | Phase 5 — Hero §2 and Ph | Accessibility posture → Keyboard, semant |
| "The busy state is always cleared, even for a superseded request, so the customer can always retry" / "the cart is never left disabled." The section has the converse rule ("Focused elements  | Phase 14 — Cart + Checko | Accessibility posture → Focus management |
| "The checkout CTA is not disabled, it is absent." The empty cart renders no checkout control, no quantity control and no note field rather than disabled ones. The section states "`aria-disab | Phase 14 — Cart + Checko | Accessibility posture → Keyboard, semant |
| "The teardown **closes the panel first**, so it cannot leave the half-torn state of a panel still open on screen with its lock already released." The section cites the binding registry only  | Phase 11 — Theme Editor  | Accessibility posture → Scroll lock, or  |
| "Both dead rules were removed" — do not reintroduce a `:not(:defined)` size reservation or any account-specific sizing on `<shopify-account>`, because `header__control` already sets the 44px | Phase 15 — Customer Acco | Accessibility posture → Target sizes |
| "The filter controls are rendered exactly once in the document — the desktop dropdown row and the mobile drawer are the same element, 'a CSS difference, not a second copy.'" The section clai | Phase 13 — Search, Filte | Accessibility posture → Keyboard, semant |
| "Accessibility behaviour is verified by driving the component, not by inspection alone." The section's evidence base is measurement and enumeration, and "What was never tested" lists the gap | Phase 4 — Header & Navig | Accessibility posture → What was never t |

**Stale rules it found repeated (5):**

- "Every interactive element has a hit area of at least 44 × 44 regardless of how small its visible mark is. A 16px swatch dot gets a 44px box." — in *Target sizes (Rules, "all from Phase 2 §*, superseded by Phase 6 §6 removed swatches from target-
- "Phase 9 enumerated every interactive element at twelve viewports across every page: zero elements below 24px anywhere, and exactly one between 24 and 44." — in *The AA-versus-AAA calls, made deliberate*, superseded by Phase 13 added `.facets-active__chip` at
- "Home page measured: 1 h1, 2 h2, 7 h3." — in *Keyboard, semantics and names (Heading o*, superseded by This is the Phase 6 §9 figure, taken whe
- "Two controls sit at the 24px AA floor rather than 44px, each with a written justification (below)." — in *The AA-versus-AAA calls, made deliberate*, superseded by Phase 10 §9 established a blanket policy
- "Full-height and fixed elements use `svh`/`dvh`, never `vh` (gallery `max-height: 100dvh`, ...)." — in *Reflow, zoom and text spacing (Landscape*, superseded by Phase 9 §7 described its one change as b

**Internal contradictions it found (8):**

- Target sizes: "Every interactive element has a hit area of at least 44 vs The shipped product card: snippets/product-card.liquid:260-262 renders — The code disproves the rule outright — and the same section already knows why, because its own SC 1.4.1 bullet says "swatch colours are named in hidde
- "Two controls sit at the 24px AA floor rather than 44px, each with a w vs `grep -rn 'target-min-aa' assets/` returns four interactive consumers, — Two of the four 24px controls — the announcement-bar link and every footer/policy link — are simply absent from the manual, and section-footer.css:100
- "Full-height and fixed elements use `svh`/`dvh`, never `vh` (gallery ` vs There is no gallery max-height in the theme. `grep -n 'max-height' ass — The manual counts one rule twice — it lists the sticky buying column's max-height in the SC 2.4.11 paragraph and then lists the same declaration again
- Contrast: "A control that uses `--color-border-current` for its bounda vs component-facets.css:291 draws the shipped active-filter chip — `<a cl — The manual generalised Phase 2's narrow rule ("fields, Secondary buttons and swatch rings" must not use the decorative token) into an absolute one tha
- "Once `assets/cart.js` runs it is removed from the document entirely,  vs section-cart-drawer.css:249 is the whole mechanism: `.cart-js .cart-dr — `display: none` takes the control out of rendering, the tab order and the accessibility tree, but the element stays in the document. The phrasing is l
- "`outline: none` / `outline: 0` is prohibited unless the same block su vs All four uses in the theme put the substitute in a separate adjacent r — The rule as written is false of every instance it is meant to license. The correct formulation is that the suppression and its replacement must ship t
- "Phase 18's drawer-exit change holds the panel visible for 250ms after vs `.is-closing` exists only in assets/facets.js (lines 155, 182, 196, 19 — The sentence sits at the end of the Reduced motion section with no owner named, directly after cart-scoped material, so it reads as the cart drawer's 
- Citation drift in the section's own tables: surface classes at "`asset vs On disk `.surface-dark` opens at design-tokens.css:469 and `.surface-l — Two different line ranges are given for the skip link inside one section, and the surface-class range is off at both ends. Every other cite in the sec

### Critic 11

**Verdict.** Trustworthy on reasoning, not yet trustworthy on numbers — and the numbers are what a performance section exists to supply. Its judgements are excellent and nearly all reproduce against the code: the P0 filter-drawer trap and its `applyWidth()` fix, the eight layout stylesheets in exactly the stated order with `css-variables part: 'style'` after them, the four real `!important` declarations in `base.css` (every other match in `assets/*.css` is inside a comment), `content_for_header` unmodified at `layout/theme.liquid:127`, the gallery's `is_active`-vs-`forloop.first` split and its honest admission that two eager images can result, `html`-level heading outlines, the whole `meta-social.liquid` contract down to the `aspect_ratio` division-by-zero and the `twitter:card` degradation, the hardcoded `type=product` at `sections/header.liquid:318`, the two `ValidJSON` errors and their exact missing keys, and `cart.js`/`header.js`/`product.js` gzipping to 12,073/4,319/5,597 to the byte. But three of its seven page-weight rows silently omit `section-footer.css`, which the code proves loads everywhere, and that omission flips the CSS budget from "headroom is gone" to a 3.1 KB breach under either KB convention. Its Theme Check block is wrong in four particulars — 50 files not 49, 6 offenses not 5, 4 `AssetSizeJavaScript` errors not 3, and none of the framing that attributes them all to `cart.js` — and the threshold it reasons about is applied to raw bytes, not gzipped, which undermines the single recommendation the section calls the highest-value change available. It also repeats Phase 16 counts (11 CSS requests, 23 `asset_url`, 22 snippets) that Phase 18's own additions superseded, in a section whose preamble promises the opposite. Alongside roughly a dozen governing rules that did not survive the fold — the preload contract, `scrollbar-gutter: stable`, the always-lazy secondary image, search's tile-counting eager test, the ban on synthesising a description, `decoding="async"`, one-request-per-cart-action, the body-emitted render-blocking trade, Our Story's second mobile picker — this section is a reliable guide to *why* the theme performs as it does and an unreliable one to *what it currently measures*. Keep it, but re-run the weight harness with the footer included and re-run Theme Check before anyone treats a single figure here as a baseline.

**Governing rules it could not find in this manual (13):**

| Rule | From | Belongs in |
|---|---|---|
| "A preload only if measurement shows it helps, and then with `imagesrcset` and `imagesizes` mirroring the `image_tag` ladder exactly... A mismatched preload is the standard way to trigger a  | Phase 3 §15 (GOVERNING,  | Page weight, beside "There are no `<link |
| "`scrollbar-gutter: stable` is set permanently on `html` so locking the page scroll does not move the layout sideways by the scrollbar's width" — and it is not toggled, "because switching it | Phase 8 §11 (GOVERNING) | CLS. This is the theme's only other stru |
| "The secondary image is **always** lazy: it is never an LCP candidate. Its cost is one additional image request per multi-photo card, which is why it is off by default." (`settings.card_hove | Phase 12 §15 / §1.1 (GOV | Image handling — the eager/priority tabl |
| On the search results page `forloop.first` is the wrong test for the eager tile: "The loop runs over the mixed slice, so on a query whose top result is a page it would be true for that page  | Phase 12 §15 (GOVERNING) | Image handling — "Two code rules produce |
| "A description must **not** be synthesised — a generated sentence about a garment nobody on this project has seen is invented product copy." With the open item: "Not verified: whether `page_ | Phase 12 §14 (GOVERNING) | Head metadata (the `description` row) an |
| `decoding: 'async'` is passed on every `image_tag` call alongside `loading` and `fetchpriority`. | Phase 5 §3 (hero) and Ph | Image handling — "The delivery contract" |
| "One network request per cart action, not two. Sections are bundled into the mutation rather than fetched afterwards." And: "Opening the drawer costs no request at all — it is already render | Phase 8 §11 (GOVERNING), | Page weight / INP. The section counts re |
| Section stylesheets are emitted in the body by the section, and that render-blocking position is the deliberate trade: "`section-hero.css` ... blocks rendering of what follows it, which is t | Phase 5 §13 (GOVERNING) | The asset strategy. The section explains |
| "hero and Our Story each take a separate mobile image because the 16:9 desktop frame loses about a third of its width on a phone." | Phase 11 §7 (GOVERNING) | Open image items. The section names only |
| "Once the vector master exists, `image_url` no longer applies: Shopify does not transform SVG through `image_url`, and a `widths:` ladder on an SVG does nothing. Upload the vector as the the | Phase 3 §3 (GOVERNING, l | Image handling — the delivery contract.  |
| "The alt fallback is assigned first. Written inline as `alt: product.featured_media.alt \| default: product.title`, Liquid applies `default` to the output of `image_tag`, not to the alt argum | Phase 3 §15 (GOVERNING,  | Image handling — the `alt` rule. The sec |
| "`window.Shopify` is never written to. `product.js` creates no global at all." | Phase 8 §11 (GOVERNING) | Page weight, beside "exactly one global, |
| The `<shopify-account>` custom element's script arrives through `content_for_header`; the theme adds zero JavaScript and zero network requests for it, and the control is inert until Shopify' | Phase 15 §12 / §18 (GOVE | Third-party load. The section credits `c |

**Stale rules it found repeated (4):**

- "Measured at the network layer the browser deduplicates: **11 CSS requests, not 13.**" — in *Performance and SEO posture → The asset *, superseded by Phase 18, which put `component-container
- Broken references table: "`asset_url` | 23 | **0**" and "`render` (snippets) | 22 | **0**" — in *Performance and SEO posture → Broken ref*, superseded by Phase 18 created `assets/component-conta
- "root: god-squad-theme/ files scanned: 49 checks: 84" — in *Performance and SEO posture → Theme Chec*, superseded by Phase 18's addition of `snippets/paginat
- "theme-check:all 7 offenses -> 5 offenses ... 3 ERROR AssetSizeJavaScript (unchanged)" — in *Performance and SEO posture → Theme Chec*, superseded by Phase 18 itself, which the section credi

**Internal contradictions it found (7):**

- Theme Check: "theme-check:all     7 offenses  ->  5 offenses ... 3 ERR vs "The three `AssetSizeJavaScript` errors are the `cart.js` offence abov — Both are false, and they cannot both be true even in principle. `cart.js` is referenced by exactly one `<script src>` in the whole theme (`layout/them
- "Theme Check's `AssetSizeJavaScript` flags three script tags against a vs The check's implementation in `@shopify/theme-check-common/dist/checks — The check measures the **raw byte count on disk**. The word "compressed" appears only in Shopify's own message string, not in the comparison. Every gz
- Page weight table: "Homepage | 26 | 55,093 | 16,392", "Product | 23 |  vs `sections/footer-group.json` binds the `footer` section, `layout/theme — Three of the seven CSS figures omit the footer stylesheet. Recomputing every surface with Python's `gzip` over the files on disk reproduces Collection
- Budget: "CSS, worst page | ≤ 55 KB gz | 55,093 B on the homepage — **h vs The homepage's fourteen stylesheets as the code actually links them (l — The budget is breached, not met, and the KB-convention hedge is moot: 58,189 B exceeds 55,000 and also exceeds 56,320 (55 KiB). This is the most conse
- "The promotion rule is written into the files themselves: *a component vs "Promoting those stylesheets to the layout would push ~4 KB onto four  — The rule and the refusal are applied in opposite directions to the same trade, within eight paragraphs. `component-product-card.css` is rendered by **
- Per-script table: "`facets.js` | 10,937 | ~3,848" vs "that is why collection-with-filters JS is 20,230 B gz rather than Pha — 16,392 + 3,848 = 20,240, not 20,230. Python's `gzip` gives `facets.js` 3,838 B — the value the 20,230 total actually uses — while GNU `gzip -9` gives 
- "There are no `<link rel="preload">`, no `preconnect`, no `dns-prefetc vs "**The Shopify CDN does not output AVIF.** WebP is the delivery format — The claim is true of the source text and false of the rendered page, and the section states the counter-evidence itself. Every font file is fetched fr

### Critic 12

**Verdict.** Trustworthy on its central subject, and unusually well evidenced there — but not safe to use unchecked on the cart mechanics and privacy rules it borrows from other phases. Everything I could verify about the tracking posture itself held against the code: all seven `<script>` citations land on the exact lines (theme.liquid 183/184/191, main-collection 243, main-product 141/519/551), `content_for_header` really is at theme.liquid:127 between `{% endstyle %}` (125) and design-tokens.css (135), theme.liquid:32 is the only `UA-` substring, there are exactly nine `w3.org` namespace URIs and no other absolute-URL host literal, the theme is 75 files, `grep` finds zero occurrences of every prohibited API (`dataLayer`, `gtag`, `fbq`, `Shopify.analytics`, `customerPrivacy`, all six retired cookies, `localStorage`/`sessionStorage`/`indexedDB`/`document.cookie`/`sendBeacon`/`new Image(`/`caches.open`/service-worker, `setInterval`), there are exactly two same-origin `fetch` sites at cart.js:179 and :651, 30 `| escape` filters on disk, and hero.liquid:224 / en.default.json:70 are quoted verbatim. Its two best contributions are original: the correction of Phase 17's false \"no console logging\" claim against cart.js:205 and product.js:45, and the repair of Phase 17's field-name list (adding `updates[]`, separating the `<meta>` names). Against that, it loses the privacy half of Phase 17 §13 — \"no customer field is read anywhere\" and \"nothing is written into a cart attribute\" both vanish while the negative-control seeds that enforce them are still cited, and Phase 15's reason (the Section Rendering API inherits page context, so one `{{ customer.email }}` leaks into every `?sections=` response) is gone with them. It also misattributes the removal/queued-change guard to `queueChange` when cart.js:670-673 puts it in `changeLine`, states \"mutations carry their own re-render in the same round trip\" as an unbroken invariant although `refreshSections()` (cart.js:650, called from 624 and 702) issues a second storefront call for one customer action, omits the order note's `/cart/update.js` save and the change-not-input rule that keeps it to one request, and contradicts itself on whether Phase 17 added two or three `| escape` filters. Keep it as the working reference for what a theme may and may not do about tracking; re-derive the cart-call invariants and the customer-data prohibitions from Phase 14, 15 and 17 before relying on them.

**Governing rules it could not find in this manual (10):**

| Rule | From | Belongs in |
|---|---|---|
| "No customer field is read anywhere." (Verified against the code today: the only match for `customer.` in any .liquid file is prose inside a comment at sections/main-page.liquid:122, and `sh | Phase 17 §13 (Privacy an | 12 — Analytics and marketing posture, in |
| "Nothing is written into a cart attribute." (Confirmed today: no `cart.attributes`, `attributes[` or `properties[` write anywhere in the theme.) | Phase 17 §13 | 12 — Analytics and marketing posture. Th |
| "The **Section Rendering API inherits the Liquid context of the requested page**", so one `{{ customer.email }}` in a shared snippet "would be serialised into every `?sections=` response the | Phase 15 §11 (Security) | 12 — Analytics and marketing posture. Th |
| "**No customer data in a URL, a `data-` attribute or a query string.** The hygiene sweep checks these shapes directly." | Phase 15 §11 | 12 — Analytics and marketing posture, al |
| "If a pixel is added later, the one rule that matters here: a purchase event must come from Shopify's order-status integration, **never from the theme observing a cart or a checkout click**. | Phase 16 §13 (Analytics  | 12 — "Purchase tracking". The section pr |
| The note is saved "on **change**, not `input`" — "so a note is one request rather than one per keystroke" — through `/cart/update.js` with `{note: value}` and **no sections requested**. (car | Phase 14 §9.1 (The order | 12 — "The theme's actual measurement job |
| The absence audit also covers classes the manual's platform table omits: "no chat widget, no reviews app, no social embed, no third-party script of any kind … no custom event dispatch." | Phase 16 §13 | 12 — the "Platform / API surface present |
| "**Search & Discovery** (Phase 13) is the one app the storefront depends on, and it adds **no storefront script**: it populates `collection.filters` server-side." | Phase 16 §15 (Third-part | 12 — "Third-party hosts: none" / "What a |
| `content_for_header` is Shopify's own and is untouched — "the `ContentForHeaderModification` check passes." | Phase 16 §15 | 12 — "The one load-bearing line". The se |
| No analytics identifier may be invented: "Not configured. No measurement ID exists, and none was invented" (repeated for GA4, Meta Pixel, TikTok and Google Ads), and "the theme ships **no**  | Phase 17 §§3-6; restated | 12 — "The measured absence". The section |

**Stale rules it found repeated (1):**

- "**Error monitoring** — none present, and not recommended at this size. The console suite (**38 pages**, 0 errors) is the current substitute." — in *12 — Analytics and marketing posture, "M*, superseded by Phase 18's full regression run, which is

**Internal contradictions it found (7):**

- "### The only theme code Phase 17 changed — **Two `| escape` filters** vs The same subsection's next paragraph: "This brought the theme from 27  — Self-contradiction, and the code settles it: `grep -o '| escape' --include=*.liquid` returns exactly 30 occurrences across 29 lines (line 142 carries 
- "**`queueChange` clears `pending[key]` before re-queueing**, so a remo vs `assets/cart.js:718-724` — `queueChange` clears `pending[key]` only to — The manual names the wrong function as the guard against the removal/queued-change race. Removal never passes through `queueChange`, so `queueChange`'
- "**Mutations carry their own re-render in the same round trip.** `SECT vs `assets/cart.js:650-657` defines `refreshSections()`, a second same-or — The section's whole duplicate-event thesis is "what the theme can do is make Shopify emit an event twice by making two storefront calls for one custom
- "There is no `setInterval` anywhere — the five `setTimeout` calls are  vs The five `setTimeout` calls are cart.js:158, cart.js:423, cart.js:720, — The count is right and `setInterval` really is absent, but the characterisation is wrong for one of the five. It matters because this is the accessibi
- "`layout/theme.liquid:234` renders `{% section 'cart-drawer' %}` insid vs `layout/theme.liquid:232-236` — the guard is two-deep: `{%- if setting — The quoted guard is incomplete, and the omitted half is load-bearing for two of this section's own claims. It is why the event matrix can say `cart_vi
- "The complete set of `name=` attributes in the theme today: `add`, `ch vs `snippets/product-variant-picker.liquid:94` emits `name="{{ group }}"` — The set is asserted as complete and is not. The conclusion survives — a `section_id`-derived name can never be `ref`, `source` or `r`, and the product
- "**Third-party hosts: none.** The only absolute URL literal anywhere i vs `snippets/meta-social.liquid:81` — `<meta property="og:image" content= — The theme does hardcode URL schemes and publish an absolute `http://` URL from source, which the "only absolute URL literal" claim reads as excluded (

### Critic 13

**Verdict.** Trustworthy on everything it measured today, unreliable on everything it inherited. I re-ran the section's own suites and reproduced its headline numbers exactly: validate 199/199, layout 19/19, surfaces 41/41, catalog 55/55, facets 62/62, settings 28/28, cartdoc 85/85, accounts 52/52, hygiene 0 findings, tracking 31 NO TRACKING PRESENT, escaping 7/7, seo 52/52, images 54/54, refs 10/10, hovergate 29 gated 0 ungated, deadcode 28/2/25; Theme Check 50 files, 84 checks, 2 default and 6 all, at the four exact offense sites it lists; cart.js 39,750/12,073/4,930 and the other three scripts to the byte; the theme at 75 files in the stated split with exactly four real !important declarations and base.css at 3,722 B mtime 08:27; respond.py's 13 viewports matching its list item for item; the +476 B CSS delta uniform across all seven surfaces; the 55 KB budget arithmetic (751 B headroom at 1024 B/KB, exceeded at 1000); and the assertion totals 405/443/508/570/744/796/945/992 against the source documents. Its two most valuable contributions are verified and I could not break them: `--dump-dom` returns zero bytes and exit 0 under all three headless flags, and chevron.py really does print `OVERALL: *** 0 disclosure(s) still wrong ***` on zero rows while notes.py prints `NO READING` and `0 assertions, 0 failed` — so the grep-for-NO-READING rule is sound and load-bearing. Against that, the section fails as a replacement reference in three specific ways. It revives a conclusion Phase 10 explicitly retracted, inverting the `#{}` story so that a shipped P0 becomes a defect "the theme never had" — contradicted in the very file it calls current — and then drops the governing rule that retraction produced, that a harness must model the platform and never the behaviour we expect from it, which is precisely the rule its own error breaks. Its inventory is wrong at the edges that matter for the migration it urges: the Python count and directory range are both incorrect, phase2/ holds no Python, phase10-13 have no directories, three design/ scripts are missing, one gzip pair is silently measured with a different compressor than everything else, a homepage duplicate-request regression is asserted to be unchanged, and "every phase from 6 onward" claims a review layer that six phase documents do not contain. And the canonical-versus-theme token-parity rule is absent from the test inventory, checked by no live suite, and violated on disk right now. Use the standing rules, the boundary table and the suite matrix as they stand; re-derive the file inventory from disk, re-measure the two base.css gzip figures with weight.py, and strike the `#{}` row before anyone builds on it.

**Governing rules it could not find in this manual (7):**

| Rule | From | Belongs in |
|---|---|---|
| "A harness must model the platform, never the behaviour we expect from it." (recorded verbatim in the live engine at phase9/miniliquid.py:216-217, and as reasoning in Phase 10 §2.2: "Teachin | Phase 10 §2.2 (correctin | 13 — "Measurement technique: the standin |
| "The canonical PHASE-2-DESIGN-TOKENS.css and the theme copy (assets/design-tokens.css) must carry identical token sets" — restated at Phase 6: "`body { margin: 0 }` added to both assets/desi | Phase 4 §3/L86, restated | 13 — the suite inventory. This is a test |
| "The preview pane screenshot captures only part of an emulated viewport. Full-page images come from headless Edge; the pane is used for DOM measurement." | Phase 0 §7.1 (GOVERNING) | 13 — "Measurement technique: the standin |
| "Accessibility behaviour is verified by driving the component, not by inspection alone." | Phase 4 §9/L183 | 13 — "Measurement technique: the standin |
| "The page must be served over HTTP to be inspected in the desktop preview pane... A local static server was configured for this purpose in `.claude/launch.json`. That file is audit tooling,  | Phase 0 §7.1 (GOVERNING) | 13 — "Where the harness is, and the firs |
| Fix the rule, not the instance: "Phase 10 fixed the desktop-clause bug in one copy and the other two carried the bug for two more phases, because the fix was applied to an instance rather th | Phase 12 §2.1/L83 | 13 (or 1) — "Measurement technique: the  |
| The two 375px captures "`mobile-375.png` / `mobile-375-raw.png` are marked never to be cited." | Phase 0 §7.1 (GOVERNING) | 13 — "Measurement technique: the standin |

**Stale rules it found repeated (2):**

- The "Harness defects that produced plausible wrong numbers" table records: "`#{}` interpolation unimplemented | the header logo drew at 133px and the header appeared to o — in *"Harness defects that produced plausible*, superseded by Phase 10 §2.2, which retracts exactly th
- The engine-growth table credits Phase 8 with adding "`{% form %}`, `{% case %}`, 28 filters, **`#{}` handling**, translation interpolation and pluralisation, a `structure — in *"How the engine grew, and which phase ad*, superseded by Phase 10 removed that capability as inco

**Internal contradictions it found (8):**

- "`#{}` interpolation unimplemented ... **The theme never had that defe vs phase9/miniliquid.py:209-217, the live engine: "That assumption was ma — The code disproves the document, and the code is the truth. The theme did have that defect: Phase 10 §2.2 records `"--logo-height-desktop: #{logo_h_de
- "Tags implemented: comment, raw, schema, style, assign, capture, echo, vs The next table, "What the harness does *not* model", lists "`{% sectio — Three of the twenty-two tags in the implemented list are in the not-modelled list two paragraphs later. I read the dispatcher: phase9/miniliquid.py:79
- Discrepancy 3: "Phase 18 §20's byte column is stale. Measured today ve vs phase16/weight.py run today reports the Homepage at `dupe 2`, with its — The duplicate-request count is not unchanged: it went 0 → 2 on the homepage against the section's own named tool, and that tool declares 2 a violation
- Discrepancy 1: base.css "grew 2,670 → 3,722 B raw, **1,253 → 1,729 B g vs The current file gzips to **1,741 B** under the method that produced e — The base.css gzip pair is measured with a different compressor than the rest of the section, and the 12-byte gzip-vs-zlib header difference is what ma
- "**192 Python files** across `phase2/`…`phase18/` and `design/`, plus  vs On disk: 197 .py files in those directories, 231 in the scratchpad ove — The count is wrong and the range is wrong in both directions: it names a directory with no Python in it and implies four directories that do not exist
- "Every phase from 6 onward put its own work through a multi-agent revi vs The table that follows gives rows for Phases 6, 7, 8, 10, 16 and 18 on — "Every phase" is an overclaim the section's own table refutes, and the gaps are not incidental — Phase 14 is the cart and checkout work, the money-tak
- "### How the engine grew, and which phase added what — Useful when a s vs The table's rows run 6, 8, 10, 13, **9** — the Phase 9 row ("the undef — A lookup table built to answer "does this capability post-date my suite?" is ordered chronologically except for its final row, which is four phases ou
- Discrepancy 2 inventories "A post-Phase-18 design-review pass ... in ` vs `scratchpad/design/` holds **nine** .py files. Omitted: `assemble.py`, — The section's stated job in this item is to inventory work that "is documented in no phase report", and it misses a third of it — including a contrast

### Critic 14

**Verdict.** Trustworthy on the specifics, unreliable on the totals. Almost every discrete fact I sampled against the code checked out exactly and often to the byte: theme_version 0.5.0 and 75 files; cart.js at 39,750 B raw with comment-stripped code gzipping to ~4.9 KB; the twelve ARCHIVE rows summing to precisely 8,541,085 B; low_stock_threshold 3 in both templates/product.json and the schema default; footer-group.json's empty block_order; hero button_label present with button_link absent and our-story using button_url; the four !important declarations all inside base.css's reduced-motion block; hero.liquid 84/97/111, our-story.liquid:105, header.liquid:318, cart.js:441 / facets.js:119 / header.js:128 and :195, design-tokens.css:434 and :443, the three 0.25em hardcodes, section-main-product.css:185 against component-product-card.css:325 and component-cart-line.css:186; the og:image fallback chain; three favicon sizes including apple-touch-icon; zero hardcoded menu labels and zero live href="#". Its five open decisions, its five missing templates plus page.contact, and its Phase 15/16/17 limitation set are all faithful and correctly de-staled, including the Theme Check correction. Where it fails is in three recurring ways. First, it carries Phase 16's measurement frame forward as current even though Phase 18 invalidated it: the stylesheet and request counts, the Theme Check scope, the unreferenced-token ratio and the 48-finding total are all pre-Phase-18 numbers, and §9's duplicate-stylesheet item flatly contradicts §2's own render-guard explanation. Second, §2 — the one table it tells the reader to trust before concluding the theme is broken — gets the footer wordmark wrong and silently omits several shipped blanks and shipped defaults with visible consequences (the announcement blocks' empty link, cart.json's empty_link, footer show_logo false, card_hover_secondary_image false, show_accelerated_checkout true). Third, the asset and admin registers lose Phase 3's and Phase 7's preconditions rather than their facts: the pixel diff that must precede any archiving, the sprite-survival dependency, the manifest hash on intake, the WebP quality floor, the single-lighting-setup half of the shoot standard, and two required merchant actions — setting alt text and pasting the social URLs — that the manual's own rules ("alt text is never written by the theme", "the row is suppressed when both are empty") make load-bearing. Use it as the launch checklist, but re-measure every count in §5, §7 and §8 against the 75-file theme, rewrite the footer-logo row, and restore the missing preconditions before anyone treats it as complete.

**Governing rules it could not find in this manual (21):**

| Rule | From | Belongs in |
|---|---|---|
| "Neither pair may be archived as redundant until this is done" — a pixel or perceptual diff must first resolve the two near-duplicate pairs md5 cannot see: images/hero-model.webp vs 01-hero- | Phase 3 (Appendix B; §11 | §3.3, the "Archive dispositions" row |
| The two sprite sheets "are the only source for the feature-icon artwork, so they must survive until item 8 [feature-icon treatment] is settled." The manual says the sprites merely "await app | Phase 3 §20 item 7 | §3.3, the "Archive dispositions" and "Fe |
| Product names, prices and currency must be "confirmed before any media is uploaded" — they drive the production filenames, the product handles and the media filenames baked into CDN URLs, an | Phase 3 §20 item 10 and  | §3.1 and §4 |
| The merchant must set each image's alt text in admin — "Content → Files → (the image) → Edit alt text. The theme never writes alt text." This is a REQUIRED pre-launch step. The manual's own  | Phase 7 §13 required ste | §4, beside step 4 (focal point) and step |
| The merchant must paste the Facebook and Instagram profile URLs into Theme settings › Social; each link is emitted only when its URL is set and the whole row is suppressed until then. Verifi | Phase 11 §15 (admin prer | §4, with step 9 (Theme settings uploads) |
| "Which announcement strings ship" and "the announcement bar's link target" are outstanding business inputs — spec §23 forbids inventing further promotional copy, and the "Worldwide Shipping" | Phase 2 Appendix C; Phas | §1 decision 4, §2 and §3.4 |
| Whether every product will carry a second "back" photograph is the gate on the hover image swap, because "a partial set — some products with a back photograph, some without — makes the grid  | Phase 2 §14.3 / §22.4; P | §2 (what ships empty/off) and §3.1 |
| The nineteen acceptance checks every incoming master must pass before intake, including check 19 — "the incoming file is hashed and checked against the manifest before intake" — and check 8, | Phase 3 §12 | §3.3, ahead of the master-standard rows |
| The product master standard includes lighting and framing consistency, not just resolution: "One key and fill setup, one key direction, one colour temperature, one fill ratio, documented and | Phase 3 §5 (product mast | §3.3, the "High-resolution product maste |
| "A numerically verified WebP quality floor" is required before encoding a storefront's worth of assets: Phase 3 encoded exactly one source at q0.82 and verified it by eye, so no measured art | Phase 3 Appendix B (§14. | §3.3 |
| "The phone wash is heavy." Because the copy sits over the picture on a phone, the medium wash reaches 0.86 alpha by 30% down the frame and the lower two thirds are noticeably dimmed; "the be | Phase 5 §15 limitation 2 | §6.3 (deliberate functional gaps) and §3 |
| Required variant information includes "variant images, inventory and backorder policy," not only the size run and swatch names. The manual's variant row asks only for "the size run, and name | Phase 1 Appendix A #2 (a | §3.1, the variant-model row |
| "Do not add a second `--link-underline-offset-caps` token — nothing in the shipped theme needs it and PHASE-2's only 0.25em case (§20.6) already renders at the token." The manual raises the  | Phase 18 (Visual Audit,  | §7, the `--link-underline-offset` row |
| If a shared `.editor-notice` component is ever built, component-facets.css's notice rule must be folded in too, "or the theme keeps two notice languages." Verified: six notice classes now ex | Phase 18 (Visual Audit) | §6 or §7, beside the editor-notice state |
| "Do not lift a shared `.field` rule yet" — Phase 2 §12.2's field anatomy has three consumers, but two sit inside grid parents with different column behaviour, so the promotion is larger than | Phase 18 (Visual Audit) | §6.3 or §7 |
| "Interface strings use the platform noun and brand nouns stay in prose": `collection.product_count` and "View All Products" must NOT be swept to brand vocabulary — "that is a voice project,  | Phase 18 (Visual Audit) | §9 (things that look like defects and mu |
| `section.shopify_attributes` does not exist — "shopify_attributes exists on the block object only, not on section" — so it renders as an empty string. Verified: seven sections still emit it  | Phase 6 §4 and limitatio | §6 (known limitations in the shipped cod |
| Organization JSON-LD is deliberately not implemented and is gated on the social URLs, because "a `sameAs` array that is empty half the time is worse than no block"; BreadcrumbList is not imp | Phase 16 §11 and §26 rec | §3.4, the "Live social URLs" row ("what  |
| Missing brand assets the register still owes: M-04 model and lifestyle photography "identifying a garment as a catalogue SKU" (the hero and story frames show people in garments but nothing t | Phase 3 §19 (M-04, M-14, | §3.3 |
| "Whether accelerated checkout should show at all, and for which payment methods. It defaults to on and cannot be previewed until the store is configured." Verified: main-product.liquid schem | Phase 8 §14 item 4 | §2 (what ships on) and §3.5 |
| "Add 'Worldwide / Shipping Available' only once a shipping policy, destination list and rates exist, and link it to the shipping policy when the brand-values section arrives." The manual rec | Phase 7 §13 optional ste | §2's withheld-tile row and §3.4's shippi |

**Stale rules it found repeated (6):**

- "The four `request.design_mode` branches (`featured-collection`, `our-story`, `main-page`, `footer`) are configuration notices only." — in *§2, closing paragraph*, superseded by Phase 13 §4.5 added a fifth editor-only 
- "The homepage emits two duplicate stylesheet `<link>` tags … Measured at the network layer: 11 CSS requests, not 13 — the browser deduplicates. Zero extra requests." — in *§9*, superseded by Phase 18. That arithmetic only works wit
- "The budget's basis is 11 stylesheets on the homepage, and any twelfth needs its own justification." — in *§8, closing note*, superseded by Phase 16 §21 set that basis; Phase 18 th
- "Run correctly (49 files, 84 checks): 2 offenses on the default config … 5 on `theme-check:all`." — in *§5, the Theme Check row*, superseded by Phase 18 §23 added snippets/pagination.l
- "**48 confirmed P2/P3 findings from Phase 16**" remain open. — in *§6.4*, superseded by Phase 18 closed three of the 48 (the pag
- "40 of 192 design tokens are unreferenced — Recorded, not pruned." Presented under a heading that says the gaps were "verified against the current CSS." — in *§7*, superseded by Phase 16 §18 measured 40/192. Phase 18 t

**Internal contradictions it found (9):**

- §2: "`settings.logo` | `""` | Header and footer render the shop name a vs sections/footer.liquid:181 — `{%- if section.settings.show_logo and se — The code disproves it. The footer has no text-wordmark branch at all: with the logo blank it renders nothing, and `shop.name` reaches the footer only 
- §2: both `featured-collection` sections render nothing and "`section-f vs §9: "The homepage emits two duplicate stylesheet `<link>` tags" (the d — The section asserts both that the shipped homepage requests neither stylesheet and that the shipped homepage emits two duplicates of them. Verified ag
- §6.4: "The three that remain from that list, verified still present in vs The table that follows carries four rows — hero/Our Story `sizes`, the — Self-contradicting count. Phase 16 §18's six-item list contained only the first three of those four; the featured-collection duplication came from Pha
- §6.4: "**48 confirmed P2/P3 findings from Phase 16** and **55 verified vs §6.4, next bullet: "Phase 16's three highest-value consolidations **we — The same bullet list states 48 remain and that three of them are closed. Only 45 are open. The figure matters because §6.4 is the only place the manua
- §3.6 heading and intro: "The four Phase 1 decisions that were supposed vs The table beneath it has seven rows, numbered #15 through #21 — Verified against Phase 1 Appendix A: only #15-#18 carry "**gates Phase 2**". #19 (the three mockup deviations) is marked "Treated as approved — formal
- §3.3: "Twelve ARCHIVE files (8,541,085 B) **and the two sprite sheets* vs PHASE-3-ASSET-MANIFEST.csv — the twelve ARCHIVE rows total exactly 8,5 — The sprites are two of the twelve and their bytes are already inside the 8,541,085 B, so the sentence double-counts them and implies fourteen files aw
- §1 decision 1: "`locales/en.default.json` lines 36 and 47 both set `ad vs `grep -ni cart locales/en.default.json` returns 14 lines total, two of — Twelve other lines say "cart," not fourteen. Phase 18's source figure ("the 14 'cart' strings") is the total including the two bag lines; the manual a
- §8: "CSS, worst page (homepage) | 55,093 B gz | ≤ 55 KB gz" and "Note  vs The same table renders JavaScript as "22.0 KB gz" for what Phase 18 me — The table mixes units without resolving them. On the decimal convention its own JS row uses, 55 KB is 55,000 B and the homepage is 93 B over, which ma
- §6.3: enabling `viewport-fit=cover` requires making "`--header-overlay vs sections/header.liquid:60-64 — `:root { --header-overlay-offset: var(- — It is not a static token: it is 88px below 1024px and 122px at and above. The claim is inherited verbatim from Phase 9 §16, which wrote it while reaso

### Critic 15

**Verdict.** Trustworthy on what it set out to do, and not yet trustworthy as the sole provenance record. Where it makes a checkable claim it is usually right, often impressively so: the closing "Open against the code" note is exactly correct (the canonical token file and god-squad-theme/assets/design-tokens.css differ by precisely one name, --type-label-lh at design-tokens.css:217, and every other token name matches); layout/theme.liquid's single {% style %} block really does sit at lines 116–125 with {{ content_for_header }} at 127; the escape fixes are at cart-line-item.liquid:142 and cart-note.liquid:80; applyWidth is in facets.js; featured-collection.liquid:135 does carry the non-consolidation note; the hero CTA is still hidden because button_link has no schema default; the theme really is 75 files with no blocks/, no templates/customers/ and only CSS and JS in assets/; and the Phase 1, 3, 4 and 7 numbers I spot-checked (200 issues split 3/65/80/52 and 5/49/85/61; the nine unreviewed sections §17–22, §24, §27, §29; 1366 ÷ 1.5 = 911; A11Y-11 taking the register from 24 to 25; 2,612 B of SVG and 85,933 → 948 B at 98.9%; the five-rung ladder summing to 311,174 B; the 13.61:1 worst pixel; 44 findings and 30 confirmed) all hold against the sources. The failures are of a single kind, and they matter because this chapter is the audit trail rather than a summary: it does not keep its own supersession promise. Phase 0's 17-row roadmap and its dependency-ordering rationale are gone, so nothing records that the programme was re-scoped from Phase 12 onward and that the planned Accessibility and Ecommerce QA phases never ran; Phase 1's issue-retirement trail — the closures tabled in Phases 4, 5, 6 and 7, and the fate of the three P0 blockers — is absent entirely, even though the chapter repeats the rule that every issue had exactly one owning phase; Phase 4's truncated specification and the "expose it as a setting rather than decide it silently" rule it forced are unrecorded, while the opening sentence asserts every phase had its own written specification; Phase 18's statement that nothing was published and no Admin change was made is missing. On top of that, five figures do not reconcile (191 tokens against 192 on disk, eleven global settings against 14, six groups against the eight in the file, 62 + 12 against 82, and 39.4% against the denominator printed beside it), one entry contradicts itself three paragraphs apart on whether one or two findings were overruled and misstates a CRITICAL as HIGH, the closing status asserts a shipped hero image that hero.liquid:183 and templates/index.json both deny, and the only change made to the theme since Phase 18 — the body font-family now live at assets/base.css:44-47, added 2026-09-26 — falls outside the window the chapter claims and belongs to no entry in it. Fix the seven dropped provenance items and the six reconciliations and this becomes the reference it wants to be; until then, use it to find which phase document to open, not to settle what a phase decided.

**Governing rules it could not find in this manual (8):**

| Rule | From | Belongs in |
|---|---|---|
| "The ordering is dependency-driven rather than cosmetic. The design system precedes every section phase because those phases consume its vocabulary. Asset preparation precedes the hero, coll | Phase 0 — Project Founda | 15. Phase-by-phase record — the chapter' |
| The roadmap supersession itself. PHASE-0 §3 is a 17-row table (Phases 0–16) marked [SUPERSEDED], in which Phase 12 = Performance, 13 = SEO, 14 = Accessibility, 15 = Ecommerce QA, 16 = Final  | Phase 0 — Project Founda | 15. Phase-by-phase record — Phase 0 entr |
| "Behaviours the specification does not name are exposed as theme settings with the approved design as the default, rather than being decided silently." (PHASE-4-HEADER-NAVIGATION.md:17). Its | Phase 4 — Header & Navig | 15. Phase-by-phase record — Phase 4 entr |
| The issue-retirement trail. The chapter repeats Phase 1's rule that the 200 issues come "with each issue assigned to exactly one owning phase", but records not one closure. Phase 4 §6 retire | Phase 1 (§28) with Phase | 15. Phase-by-phase record — per-phase en |
| "If any order surface is ever built (only relevant on legacy accounts), the §5.1 trap list binds: order.fulfillments does not exist in theme Liquid (use line_item.fulfillment.tracking_number | Phase 15 — Customer Acco | 15. Phase-by-phase record — Phase 15 ent |
| "Every one traced to a measured finding or a Theme Check offense; nothing was changed on taste." (PHASE-16:57). This is the rule that bounds what an audit phase is permitted to change, and i | Phase 16 — Performance + | 15. Phase-by-phase record — Phase 16 ent |
| Phase 18's scope boundary and its closing assertion about the live world: "Not in scope, and not done: redesign, deployment, publishing, domain, payment, advertising, irreversible Admin chan | Phase 18 — Final Polish  | 15. Phase-by-phase record — Closing stat |
| The Appendix A gating fact: PHASE-0 §12 carries forward "the four Phase 1 Appendix A decisions that gate the design system." The chapter's Phase 1 entry says only that "Appendix A holds the  | Phase 0 §12 / Phase 1 Ap | 15. Phase-by-phase record — Phase 1 entr |

**Stale rules it found repeated (3):**

- "eleven global settings in eight groups" is given as Phase 11's delivery with no note that it is a Phase 11 snapshot. config/settings_schema.json today carries 14 real se — in *Phase 11 — Theme Editor + Merchant Custo*, superseded by Phase 12 (card_hover_secondary_image), P
- "taking the file to 191 declared tokens" is offered as the settled count of PHASE-2-DESIGN-TOKENS.css, with the chapter expressly correcting Appendix B's "164 tokens" as  — in *Phase 2 — Design System & Visual Languag*, superseded by Phase 4 (--scrim-header-overhang added t
- The Phase 9 "Superseded" note hands the reader Phase 13's replacement figure — "22.2 KB gz JavaScript and roughly 72 KB gz CSS across nineteen files" — as the correction  — in *Phase 9 — Mobile UX + Responsive Polish,*, superseded by Phase 18 (+2 stylesheets, CSS rules −2,5

**Internal contradictions it found (6):**

- Closing status: "the hero currently ships an AI-generated image with u vs sections/hero.liquid:183 — the shipped schema info reads "The hero ima — The code disproves the claim. The theme ships no hero image; the warning is conditional on a merchant choosing to upload the mockup image. The chapter
- Opening: "The programme ran as nineteen gated phases (0–18) over 2026- vs PRE-INTEGRATION-DESIGN-REVIEW.md, dated 2026-09-26: "**One change was  — The chapter presents itself as the complete provenance trail for the theme as it stands and closes its window at 2026-09-25, but the most recent chang
- Phase 18 "Delivered": "98 confirmed findings deduplicating to 70 disti vs Phase 18 "Key decision": "**Two** findings the reviewers rated **HIGH* — Self-contradictory count (1 rejected vs two overruled) and a wrong severity: the chevron finding was CRITICAL, not HIGH, and it was fixed rather than 
- Phase 6 "Delivered": "sections/featured-collection.liquid, snippets/pr vs sections/featured-collection.liquid's schema carries 19 real settings  — The code disproves the group count. The chapter copied a figure its source contradicts on the same page, and did so in the one chapter whose job is to
- Phase 16 "Delivered": "Ten audit dimensions, 82 findings raised, 62 co vs PHASE-16 §3's table has four columns and four totals: findings 82, con — 62 + 12 = 74, leaving eight findings unaccounted for in a chapter that exists to keep the count. The dropped column is not incidental — "needs-measure
- Phase 3 "Delivered": "48 files scanned, 18,077,379 B, nine md5 duplica vs PHASE-3 §11:784 — "39.4% of the project's 17,100,416 bytes of image we — The percentage is computed against a denominator the chapter withholds while printing a different one in the same sentence. 6,733,692 / 18,077,379 = 3

### Critic 16

**Verdict.** No — not as the working reference for the step that comes next, though it is close and the deficit is one section wide rather than diffuse. On its own terms the structure is strong: sections 2–8 and 10–13 cover the theme's interior thoroughly, and section 9 is genuinely the best thing in the manual — nineteen subsections that name every platform hook, route, deprecation and admin dependency the theme has, with §14.2's 'what ships empty and what a live store will actually show' table doing exactly the job an integrator needs when a correctly-built surface renders nothing. What the fifteen sections have no home for is the ACT of integration: the manual documents the theme and the store's data contract, and says nothing about the deployment. There is no statement of how the theme reaches the store (the Shopify CLI is absent, so it is a ZIP upload, and the ZIP must have layout/ and sections/ at its root — zip the contents of god-squad-theme/, not the folder); no dependency-ordered sequence, only three overlapping unordered admin lists with one ordering hint between them, printed in an order that has the integrator creating Search & Discovery filters before any product exists; no smoke test attached to the seven unknowns §9.19 and §13 correctly enumerate; no account of where merchant edits live after upload, or that a second ZIP adds a theme rather than updating one, which for a project with no version control is the whole change-management story; no rollback plan; and no table joining the image files that exist on disk outside the theme to the admin destinations they belong in. Two specific omissions will cost real time: the password page — the theme has neither layout/password.liquid nor templates/password.liquid, the store is behind it for the entire pre-launch engagement, and the manual files it as a hypothetical — and the absence of any committed .theme-check.yml or package.json, which is how the Phase 16 wrong-root defect happened in the first place. Fix: add a sixteenth section, an ordered store-setup-and-deployment runbook (step 0 confirm the store, plan and admin access; then the dependency sequence; then upload, preview, smoke test, publish, rollback), give §9 a 'what to upload, and where' subsection and a 'locales, Markets and currency' subsection, point §13 at Phase 2 Appendix A's 46 acceptance checks as the pass to re-run once real photography and a real catalogue exist, and repair the six contradictions above — particularly the drawer's inverted <body>-parentage claim and the radius_sm range, both of which state a violation as the rule. With that, it replaces the twenty documents; without it, sections 9 and 14 send the integrator back to Phases 3, 13, 14, 15 and 16 for the operational half.

**Governing rules it could not find in this manual (12):**

| Rule | From | Belongs in |
|---|---|---|
| How the theme physically reaches the store. The Shopify CLI is absent, so the only route is Online Store › Themes › Add theme › Upload ZIP — and the ZIP must carry layout/ sections/ snippets | Nowhere. Phase 0 §7 reco | NEW SECTION 16 — 'Integration runbook: g |
| The dependency ORDER of the store build. Admin work is currently three overlapping unordered lists (§9.18's 22 rows, §14.4, and the Blocking? column of §9.5) with exactly one ordering instru | Distributed across eight | NEW SECTION 16 — as a numbered sequence  |
| A first-upload smoke test with pass criteria. §9.19 and §13 name the seven things only a real store can prove, but attach no procedure to any of them. The procedure is concrete and short: ad | Phase 8 §6/§12, Phase 14 | NEW SECTION 16, as 'the first hour after |
| What happens to the theme after it is uploaded. Theme Editor edits write into the STORE's copy of templates/*.json and config/settings_data.json; the local files never learn about them; a se | Nowhere. Phase 1 DEBT-12 | NEW SECTION 16, with a pointer from §2 ( |
| Rollback and theme-library hygiene. Keep the previously published theme in the library and publish by swapping, not by editing the live theme; duplicate before any post-launch change; the pu | Nowhere in any of the tw | NEW SECTION 16. |
| The storefront password page blocks every pre-launch review, and that is not filed as a blocker. The theme has no layout/password.liquid and no templates/password.liquid, and an unlaunched s | Phase 1 §29.5 and Phase  | §9.16 ('Templates Shopify can route to t |
| Which file on disk goes to which admin destination. The theme deliberately contains no imagery, and every candidate master sits OUTSIDE it: images/hero-group.png (1672×941, AI-generated, rig | Phase 3 §16 (naming), §1 | §9 as a new 'What to upload, and where'  |
| The design QA pass must be re-run once real content lands, and there is a procedure for it: Phase 2 Appendix A's 46 numbered acceptance checks, each with the evidence method that makes its r | Phase 2 Appendix A (46 c | §13 (QA harness and test inventory) as t |
| How to reconstitute the verification tooling. §13 correctly says to copy the session-scoped scratchpad into the project and version it, but the project itself has no package.json and no .the | Phase 10 (harness) and P | §13, in 'Where the harness is, and the f |
| Locales, Markets and currency as one contract. locales/en.default.json is the only locale file and there is no en.default.schema.json, so a store that enables a second language or Markets at | Phase 10/11/12 (the t: k | §9 as a new subsection 'Locales, Markets |
| How the owner reviews the theme before it is published, and what they will misread. An unpublished theme is reviewed through its preview link, and the four request.design_mode configuration  | Phase 11 §9 establishes  | NEW SECTION 16, cross-referencing §14.2. |
| Step zero: confirm the store exists. The Shopify store is still an open unknown — store URL or custom domain, plan, development store versus live, and who holds admin access — and every one  | Phase 0 §12 and Phase 1  | NEW SECTION 16 as step 0, with §14.3.5 r |

**Stale rules it found repeated (4):**

- "Theme Check has never been run (no Shopify CLI in this environment — run shopify theme check before going live; the two residual Theme Check errors are the missing theme — in *Section 8 — Surfaces: product, cart, che*, superseded by Phase 16 §0, which the manual itself rep
- "Headless Edge on this machine cannot lay out narrower than roughly 490 CSS pixels; a capture requested at 375 px is laid out at about 490 and clipped." — in *Section 1 — Project identity, scope and *, superseded by Phase 5 §14 re-measured the floor to ~49
- cart.js is "12,073 B gzipped, above Shopify's 10,000 B AssetSizeJavaScript threshold" with "three AssetSizeJavaScript" offenses implied by the Theme Check tables. — in *Section 2 — The theme as built, 'The ass*, superseded by The manual's own re-measurement of 2026-
- The missing theme_documentation_url / theme_support_url pair "shipped as empty strings against a format: uri schema, which was the theme's only Theme Check ERROR." — in *Section 9.5 — Theme settings the merchan*, superseded by Phase 16 §0: no offense count taken befo

**Internal contradictions it found (6):**

- Section 2 — The theme as built (layout/theme.liquid): the cart drawer  vs Section 8 (cart drawer) and Section 10 (accessibility), both: "The dra — Flatly incompatible, and §2 has it inverted. Phase 8 calls the identity-comparison version 'the single most consequential defect it found in its own w
- Section 2's global-settings table and Section 9.5's settings table bot vs Section 6 — Design system, components: "--radius-sm is the only radius — config/settings_schema.json ships a select with exactly three options (0 / 2 / 4, default 2), so §6 is right and the two tables an integrator will act
- Section 1 — the approved visual direction table: "Playfair Display 900 vs Section 4 — typography, measured over the code: "0 declare var(--font- — Both cannot be true, and the consequence is live at integration time: only four faces are registered (Jost 400/500/600 and Playfair 900) and settings_
- Section 2 — asset set: cart.js "12,073 B gzipped, above Shopify's 10,0 vs The same cell's own arithmetic, and §11's restatement that the answer  — Self-refuting in one sentence: 4,930 B is less than half of 10,000 B, so stripping comments is precisely what reaches the threshold. The conclusion th
- Section 8 — templates: "Still missing against Shopify's Theme Store li vs Section 14 §6.2: the same list, with "password matters most if the sto — An unlaunched store is behind the password page for the whole integration, so by §8's own rule the first surface the owner is shown after upload is br
- Section 2: "assets/ | 25 | 21 CSS, 4 JS", and the asset-set table's ow vs Section 4, twice: "grep over the 24 component/section stylesheets" and — Three incompatible counts for one set of files. 8 + 11 = 19, not 21; and 24 exceeds the 21 CSS files that exist on disk. Verified by listing assets/: 

---

*Consolidated from PHASE-0 through PHASE-18. The design review conducted
alongside this consolidation is in `PRE-INTEGRATION-DESIGN-REVIEW.md`.*
